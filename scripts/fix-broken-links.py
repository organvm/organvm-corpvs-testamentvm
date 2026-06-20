#!/usr/bin/env python3
"""Fix 7 broken system links found by V1 audit.

For each affected README:
1. Fetch current content from GitHub
2. Apply the fix (correct URL or remove dead hyperlink)
3. Push updated README back
"""

import subprocess
import base64
import json

FIXES = [
    {
        "org": "organvm-i-theoria",
        "repo": "organon-noumenon--ontogenetic-morphe",
        "find": "https://github.com/organvm-i-theoria/recursive-engine)",
        "replace": "https://github.com/organvm-i-theoria/recursive-engine--generative-entity)",
        "description": "Fix: recursive-engine → recursive-engine--generative-entity"
    },
    {
        "org": "organvm-i-theoria",
        "repo": "auto-revision-epistemic-engine",
        "find": "[ontological-commit-engine](https://github.com/organvm-i-theoria/ontological-commit-engine)",
        "replace": "ontological-commit-engine",
        "description": "Fix: Remove dead link to non-existent ontological-commit-engine"
    },
    {
        "org": "organvm-i-theoria",
        "repo": "cognitive-archaelogy-tribunal",
        "find": "[ingesting-organ-document-structure](https://github.com/organvm-i-theoria/ingesting-organ-document-structure)",
        "replace": "ingesting-organ-document-structure (planning corpus)",
        "description": "Fix: Remove dead link to non-existent ingesting-organ-document-structure"
    },
    {
        "org": "organvm-i-theoria",
        "repo": "a-recursive-root",
        "find": "[`recursive-ontology`](https://github.com/organvm-i-theoria/recursive-ontology)",
        "replace": "`recursive-ontology`",
        "description": "Fix: Remove dead link to non-existent recursive-ontology"
    },
    {
        "org": "organvm-i-theoria",
        "repo": "4-ivi374-F0Rivi4",
        "find": "[ontology-of-creative-systems](https://github.com/organvm-i-theoria/ontology-of-creative-systems)",
        "replace": "ontology-of-creative-systems",
        "description": "Fix: Remove dead link to non-existent ontology-of-creative-systems"
    },
    {
        "org": "organvm-i-theoria",
        "repo": "4-ivi374-F0Rivi4",
        "find": "[epistemic-artefact-schema](https://github.com/organvm-i-theoria/epistemic-artefact-schema)",
        "replace": "epistemic-artefact-schema",
        "description": "Fix: Remove dead link to non-existent epistemic-artefact-schema"
    },
    {
        "org": "organvm-i-theoria",
        "repo": "collective-persona-operations",
        "find": "https://github.com/organvm-i-theoria/organon-noumenon)",
        "replace": "https://github.com/organvm-i-theoria/organon-noumenon--ontogenetic-morphe)",
        "description": "Fix: organon-noumenon → organon-noumenon--ontogenetic-morphe"
    },
]


def fetch_readme_raw(org, repo):
    """Fetch README with SHA for update."""
    result = subprocess.run(
        ["gh", "api", f"repos/{org}/{repo}/readme",
         "--jq", '{content: .content, sha: .sha, path: .path}'],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        return None, None, None, result.stderr.strip()
    data = json.loads(result.stdout.strip())
    content = base64.b64decode(data['content']).decode('utf-8')
    return content, data['sha'], data['path'], None


def push_readme(org, repo, path, content, sha, message):
    """Push updated README."""
    content_b64 = base64.b64encode(content.encode('utf-8')).decode('ascii')
    payload = json.dumps({
        "message": message,
        "content": content_b64,
        "sha": sha
    })
    result = subprocess.run(
        ["gh", "api", f"repos/{org}/{repo}/contents/{path}",
         "--method", "PUT",
         "--input", "-"],
        input=payload, capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0, result.stderr.strip()


def main():
    print("=" * 80)
    print("FIXING 7 BROKEN SYSTEM LINKS (V1)")
    print("=" * 80)

    # Group fixes by repo to avoid multiple fetches/pushes for same repo
    by_repo = {}
    for fix in FIXES:
        key = (fix['org'], fix['repo'])
        if key not in by_repo:
            by_repo[key] = []
        by_repo[key].append(fix)

    fixed = 0
    errors = []

    for (org, repo), fixes in by_repo.items():
        print(f"\n── {org}/{repo} ──")

        content, sha, path, err = fetch_readme_raw(org, repo)
        if err:
            print(f"  ERROR: Cannot fetch README: {err}")
            errors.append(f"{org}/{repo}: {err}")
            continue

        original = content
        for fix in fixes:
            if fix['find'] in content:
                content = content.replace(fix['find'], fix['replace'])
                print(f"  {fix['description']}")
            else:
                print(f"  WARNING: Pattern not found: {fix['find'][:80]}...")
                # Try a more lenient search
                # For URL-only fixes, the pattern might have different surrounding characters
                errors.append(f"{org}/{repo}: Pattern not found for {fix['description']}")

        if content != original:
            msg = "fix: resolve broken cross-references in README [Phase 2 micro-validation]"
            ok, push_err = push_readme(org, repo, path, content, sha, msg)
            if ok:
                print("  PUSHED successfully")
                fixed += 1
            else:
                print(f"  ERROR pushing: {push_err}")
                errors.append(f"{org}/{repo}: Push failed: {push_err}")
        else:
            print("  No changes needed")

    print(f"\n{'=' * 80}")
    print(f"SUMMARY: {fixed} READMEs updated, {len(errors)} errors")
    print(f"{'=' * 80}")
    if errors:
        for e in errors:
            print(f"  - {e}")


if __name__ == "__main__":
    main()
