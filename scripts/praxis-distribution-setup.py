#!/usr/bin/env python3
"""PRAXIS Sprint Phase C: Distribution channel setup and validation.

Validates distribution channel configuration, tests API connectivity,
and reports channel readiness for the POSSE distribution strategy.

Channels:
  - RSS: Validates public-process Jekyll feed.xml exists and is valid
  - Newsletter: Checks for Ghost/Substack configuration
  - Mastodon: Tests API connectivity (requires MASTODON_TOKEN env var)
  - LinkedIn: Validates article drafts exist

Usage:
    python3 scripts/praxis-distribution-setup.py [--output praxis-distribution-report.json]

Environment variables (optional, for API connectivity tests):
    MASTODON_INSTANCE  — e.g. https://mastodon.social
    MASTODON_TOKEN     — API access token
    GHOST_URL          — Ghost publication URL
    GHOST_ADMIN_KEY    — Ghost Admin API key
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent.parent / "repo-registry.json"

# Expected channels from public-process-map-v2.md
CHANNELS = [
    {
        "name": "RSS/Atom Feed",
        "type": "rss",
        "description": "Jekyll-generated Atom feed from public-process site",
        "priority": "HIGH",
        "automation": "Built-in (Jekyll)",
    },
    {
        "name": "Newsletter (Ghost/Substack)",
        "type": "newsletter",
        "description": "Email newsletter with essay digest",
        "priority": "HIGH",
        "automation": "Ghost API or Substack manual",
    },
    {
        "name": "Mastodon",
        "type": "mastodon",
        "description": "Primary social channel for POSSE distribution",
        "priority": "HIGH",
        "automation": "Mastodon API v1",
    },
    {
        "name": "LinkedIn",
        "type": "linkedin",
        "description": "Professional articles condensed from essays",
        "priority": "MEDIUM",
        "automation": "Manual cross-post from newsletter",
    },
]


def check_rss():
    """Validate RSS feed from public-process Jekyll site."""
    report = {"channel": "RSS/Atom Feed", "checks": []}

    # Check if feed.xml exists in public-process repo
    result = subprocess.run(
        ["gh", "api", "repos/organvm-v-logos/public-process/contents/feed.xml",
         "--jq", ".size"],
        capture_output=True, text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        size = int(result.stdout.strip())
        report["checks"].append({
            "name": "feed.xml exists",
            "passed": True,
            "detail": f"Size: {size} bytes",
        })
    else:
        report["checks"].append({
            "name": "feed.xml exists",
            "passed": False,
            "detail": "Not found in repo",
        })

    # Check if Jekyll _config.yml has feed plugin
    result = subprocess.run(
        ["gh", "api", "repos/organvm-v-logos/public-process/contents/_config.yml",
         "--jq", ".content"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        import base64
        try:
            content = base64.b64decode(result.stdout.strip()).decode()
            has_feed = "jekyll-feed" in content or "feed" in content.lower()
            report["checks"].append({
                "name": "Jekyll feed plugin configured",
                "passed": has_feed,
                "detail": "jekyll-feed found in _config.yml" if has_feed else "No feed plugin detected",
            })
        except Exception:
            report["checks"].append({
                "name": "Jekyll feed plugin configured",
                "passed": False,
                "detail": "Could not decode _config.yml",
            })

    # Check live feed URL
    result = subprocess.run(
        ["curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}",
         "https://organvm-v-logos.github.io/public-process/feed.xml"],
        capture_output=True, text=True, timeout=15,
    )
    if result.returncode == 0:
        status = result.stdout.strip()
        report["checks"].append({
            "name": "Live feed URL accessible",
            "passed": status == "200",
            "detail": f"HTTP {status}",
        })

    # RSS is READY if the live feed URL is accessible (HTTP 200), even if
    # feed.xml isn't committed to the repo — Jekyll generates it at build time.
    live_check = next((c for c in report["checks"] if c["name"] == "Live feed URL accessible"), None)
    report["ready"] = live_check is not None and live_check["passed"]
    return report


def check_newsletter():
    """Check newsletter configuration."""
    report = {"channel": "Newsletter", "checks": []}

    ghost_url = os.environ.get("GHOST_URL", "")
    ghost_key = os.environ.get("GHOST_ADMIN_KEY", "")

    if ghost_url and ghost_key:
        report["checks"].append({
            "name": "Ghost credentials configured",
            "passed": True,
            "detail": f"URL: {ghost_url}",
        })
        # Could test API connectivity here
    else:
        report["checks"].append({
            "name": "Ghost credentials configured",
            "passed": False,
            "detail": "Set GHOST_URL and GHOST_ADMIN_KEY env vars. Alternative: use Substack (manual setup).",
        })

    # Check if essay archive is ready for import
    result = subprocess.run(
        ["gh", "api", "repos/organvm-v-logos/public-process/git/trees/HEAD?recursive=1",
         "--jq", '[.tree[] | select(.path | startswith("_posts/"))] | length'],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        count = int(result.stdout.strip())
        report["checks"].append({
            "name": "Essay archive ready for import",
            "passed": count >= 28,
            "detail": f"{count} essays available",
        })

    report["ready"] = all(c["passed"] for c in report["checks"])
    return report


def check_mastodon():
    """Check Mastodon API connectivity."""
    report = {"channel": "Mastodon", "checks": []}

    instance = os.environ.get("MASTODON_INSTANCE", "")
    token = os.environ.get("MASTODON_TOKEN", "")  # allow-secret

    if instance and token:
        report["checks"].append({
            "name": "Mastodon credentials configured",
            "passed": True,
            "detail": f"Instance: {instance}",
        })

        # Test API connectivity
        result = subprocess.run(
            ["curl", "-sH", f"Authorization: Bearer {token}",
             f"{instance}/api/v1/accounts/verify_credentials",
             "-o", "/dev/null", "-w", "%{http_code}"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0:
            status = result.stdout.strip()
            report["checks"].append({
                "name": "API connectivity",
                "passed": status == "200",
                "detail": f"HTTP {status}",
            })
    else:
        report["checks"].append({
            "name": "Mastodon credentials configured",
            "passed": False,
            "detail": "Set MASTODON_INSTANCE and MASTODON_TOKEN env vars",
        })

    report["ready"] = all(c["passed"] for c in report["checks"])
    return report


def check_linkedin():
    """Check LinkedIn distribution readiness."""
    report = {"channel": "LinkedIn", "checks": []}

    # LinkedIn doesn't have a simple API — check for draft articles
    report["checks"].append({
        "name": "LinkedIn article drafts",
        "passed": False,
        "detail": "5 long-form articles need to be drafted from essays (manual step)",
    })

    # Check distribution-agent workflow
    result = subprocess.run(
        ["gh", "api", "repos/organvm-iv-taxis/orchestration-start-here/contents/.github/workflows",
         "--jq", '[.[] | select(.name | contains("distribution"))] | length'],
        capture_output=True, text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        count = int(result.stdout.strip())
        report["checks"].append({
            "name": "Distribution agent workflow exists",
            "passed": count > 0,
            "detail": f"{count} distribution workflow(s) found",
        })

    report["ready"] = all(c["passed"] for c in report["checks"])
    return report


def check_distribution_agent():
    """Check the orchestration distribution-agent workflow configuration."""
    report = {"channel": "Distribution Agent (Orchestration)", "checks": []}

    # Check if distribution-agent.yml exists
    result = subprocess.run(
        ["gh", "api",
         "repos/organvm-iv-taxis/orchestration-start-here/contents/.github/workflows/distribution-agent.yml",
         "--jq", ".size"],
        capture_output=True, text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        report["checks"].append({
            "name": "distribution-agent.yml exists",
            "passed": True,
            "detail": f"Size: {result.stdout.strip()} bytes",
        })
    else:
        report["checks"].append({
            "name": "distribution-agent.yml exists",
            "passed": False,
            "detail": "Workflow not found",
        })

    report["ready"] = all(c["passed"] for c in report["checks"])
    return report


def main():
    parser = argparse.ArgumentParser(description="Validate distribution channel setup")
    parser.add_argument("--output", default="praxis-distribution-report.json",
                        help="Output JSON report path")
    args = parser.parse_args()

    print("=" * 60)
    print("PRAXIS Sprint Phase C — Distribution Channel Validation")
    print("=" * 60)

    channel_checks = [
        ("RSS/Atom Feed", check_rss),
        ("Newsletter", check_newsletter),
        ("Mastodon", check_mastodon),
        ("LinkedIn", check_linkedin),
        ("Distribution Agent", check_distribution_agent),
    ]

    reports = []
    ready_count = 0

    for name, check_fn in channel_checks:
        print(f"\n[CHECK] {name}")
        try:
            report = check_fn()
        except Exception as e:
            report = {"channel": name, "checks": [], "ready": False, "error": str(e)}

        for check in report.get("checks", []):
            icon = "+" if check["passed"] else "-"
            print(f"  [{icon}] {check['name']}: {check.get('detail', '')}")

        if report.get("ready"):
            ready_count += 1
            print(f"  => READY")
        else:
            print(f"  => NOT READY")

        reports.append(report)

    print(f"\n{'=' * 60}")
    print(f"DISTRIBUTION CHANNEL SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Ready: {ready_count}/{len(reports)} channels")
    print(f"  Target: 4+ channels active")

    output_data = {
        "audit_date": datetime.now(timezone.utc).isoformat(),
        "sprint": "PRAXIS",
        "phase": "C",
        "channels_ready": ready_count,
        "channels_total": len(reports),
        "target": 4,
        "channels": reports,
        "next_steps": [
            "Set up Mastodon account and configure MASTODON_INSTANCE + MASTODON_TOKEN",
            "Set up Ghost or Substack newsletter publication",
            "Draft 5 LinkedIn articles from essay corpus",
            "Update distribution-agent workflow with real API endpoints",
            "Submit RSS feed to aggregators",
        ],
    }

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
        f.write("\n")

    print(f"\n  Report: {output_path}")


if __name__ == "__main__":
    main()
