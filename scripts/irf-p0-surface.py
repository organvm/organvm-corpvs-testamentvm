#!/usr/bin/env python3
"""
IRF P0 Surface - Rolling delta reporter for GitHub issue #489.
Extracts open P0 items from INST-INDEX-RERUM-FACIENDARUM.md and reports the delta.
"""

import argparse
import datetime
import json
import os
import re
import sys
import urllib.request
import urllib.error

def get_open_p0_items(filepath="INST-INDEX-RERUM-FACIENDARUM.md"):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    items = {}
    for line in content.splitlines():
        if line.startswith("|") and "P0" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 7:
                irf_id = parts[1]
                prio = parts[2]
                desc = parts[3]
                owner = parts[4]
                session = parts[5]
                status = parts[6]
                
                # Check for open P0 items
                if "P0" in prio and not irf_id.startswith("~~") and not "DONE" in irf_id and not "~~" in prio:
                    items[irf_id] = {
                        "id": irf_id,
                        "desc": desc,
                        "status": status
                    }
    return items

def fetch_latest_state(repo, issue_number, token):
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments?per_page=100"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "irf-p0-surface-bot"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    comments = []
    
    while url:
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as response:
                page_comments = json.loads(response.read().decode("utf-8"))
                comments.extend(page_comments)
                
                link_header = response.getheader('Link')
                url = None
                if link_header:
                    links = link_header.split(',')
                    for link in links:
                        parts = link.split(';')
                        if len(parts) == 2 and 'rel="next"' in parts[1]:
                            url = parts[0].strip()[1:-1]
                            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return {}
            else:
                print(f"Failed to fetch comments: {e}", file=sys.stderr)
                sys.exit(1)

    for comment in reversed(comments):
        body = comment.get("body", "")
        if "<!-- STATE: " in body:
            match = re.search(r'<!-- STATE:\s*(.*?)\s*-->', body, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    continue
    return {}

def post_comment(repo, issue_number, body, token):
    url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "irf-p0-surface-bot"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    data = json.dumps({"body": body}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"Failed to post comment: {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Surface open P0 items to GitHub Issue #489")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "organvm/organvm-corpvs-testamentvm"), help="Target repository")
    parser.add_argument("--issue", type=int, default=489, help="Target issue number")
    parser.add_argument("--dry-run", action="store_true", help="Print instead of commenting")
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token and not args.dry_run:
        print("Error: GH_TOKEN or GITHUB_TOKEN environment variable required.")
        sys.exit(1)

    current_items = get_open_p0_items()
    
    if args.dry_run and not token:
        previous_items = {}
    else:
        previous_items = fetch_latest_state(args.repo, args.issue, token)

    new_ids = []
    closed_ids = []
    changed_ids = []

    for irf_id, item in current_items.items():
        if irf_id not in previous_items:
            new_ids.append(irf_id)
        else:
            prev = previous_items[irf_id]
            if prev["desc"] != item["desc"] or prev["status"] != item["status"]:
                changed_ids.append(irf_id)

    for irf_id in previous_items.keys():
        if irf_id not in current_items:
            closed_ids.append(irf_id)

    date_str = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    
    total_open = len(current_items)
    delta_new = len(new_ids)
    delta_closed = len(closed_ids)
    delta_changed = len(changed_ids)

    # Format output
    body_lines = [
        f"**IRF P0 surface {date_str} — {total_open} open (delta: +{delta_new} re-emerged / \u2212{delta_closed} closed / ~{delta_changed} status-changed)**",
        ""
    ]

    if delta_new > 0:
        body_lines.append("### 🔴 Re-emerged / New")
        for irf_id in new_ids:
            item = current_items[irf_id]
            body_lines.append(f"- **{irf_id}**: {item['desc']} (Status: `{item['status']}`)")
        body_lines.append("")

    if delta_closed > 0:
        body_lines.append("### 🟢 Closed")
        for irf_id in closed_ids:
            item = previous_items[irf_id]
            body_lines.append(f"- **~~{irf_id}~~**: {item['desc']}")
        body_lines.append("")

    if delta_changed > 0:
        body_lines.append("### 🟡 Status / Description Changed")
        for irf_id in changed_ids:
            item = current_items[irf_id]
            body_lines.append(f"- **{irf_id}**: {item['desc']} (Status: `{item['status']}`)")
        body_lines.append("")

    if delta_new == 0 and delta_closed == 0 and delta_changed == 0:
        body_lines.append("_No changes since last run._")
        body_lines.append("")

    # Add invisible state
    state_json = json.dumps(current_items, separators=(',', ':'))
    body_lines.append(f"<!-- STATE: {state_json} -->")

    final_body = "\n".join(body_lines)

    if args.dry_run:
        print(final_body)
    else:
        # Only post if there is a delta or we want to force daily?
        # The prompt says: "Each comment reports only the delta since the previous comm"
        # It's typical to just post the delta. If there's NO delta, do we post?
        # Let's post anyway so we see the bot is alive, or maybe we skip? "Each comment reports only the delta" 
        # I'll post it.
        print(f"Posting to {args.repo}#{args.issue}")
        post_comment(args.repo, args.issue, final_body, token)

if __name__ == "__main__":
    main()
