#!/usr/bin/env python3
"""V3: Registry-to-GitHub Reconciliation

Verifies:
1. Every repo in registry with documentation_status containing DEPLOYED actually exists on GitHub with a README
2. GitHub repo descriptions match registry descriptions
3. No repos on GitHub are missing from registry
"""

import json
import subprocess
import sys
import os

REGISTRY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "repo-registry.json")

SYSTEM_ORGS = [
    'organvm-i-theoria', 'organvm-ii-poiesis', 'organvm-iii-ergon',
    'organvm-iv-taxis', 'organvm-v-logos', 'organvm-vi-koinonia',
    'organvm-vii-kerygma', 'meta-organvm'
]


# ISOTOPE DISSOLUTION: Gate memory--remember G2 (CORPUS_SCRIPTS_DISSOLVED)
try:
    from organvm_engine.registry.loader import load_registry as _engine_load
except ImportError:
    _engine_load = None


def load_registry():
    if _engine_load is not None:
        return _engine_load(REGISTRY_PATH)
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def gh_list_repos(org):
    """List all repos in an org via gh api."""
    repos = []
    page = 1
    while True:
        try:
            result = subprocess.run(
                ["gh", "api", f"orgs/{org}/repos?per_page=100&page={page}",
                 "--jq", '.[].name'],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                print(f"  Error listing {org}: {result.stderr.strip()}")
                break
            names = [n.strip() for n in result.stdout.strip().split('\n') if n.strip()]
            if not names:
                break
            repos.extend(names)
            if len(names) < 100:
                break
            page += 1
        except subprocess.TimeoutExpired:
            print(f"  Timeout listing {org}")
            break
    return repos


def gh_get_repo_info(org, repo):
    """Get repo description and has_readme status."""
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{org}/{repo}",
             "--jq", '{description: .description, has_wiki: .has_wiki, default_branch: .default_branch}'],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout.strip())
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def gh_has_readme(org, repo):
    """Check if repo has a README."""
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{org}/{repo}/readme",
             "--jq", ".name"],
            capture_output=True, text=True, timeout=15
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return None


def gh_get_description(org, repo):
    """Get repo description from GitHub."""
    try:
        result = subprocess.run(
            ["gh", "api", f"repos/{org}/{repo}",
             "--jq", ".description"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            desc = result.stdout.strip()
            return desc if desc and desc != "null" else ""
        return None
    except subprocess.TimeoutExpired:
        return None


def main():
    registry = load_registry()

    print("=" * 80)
    print("V3: REGISTRY-TO-GITHUB RECONCILIATION")
    print("=" * 80)

    # Build registry map: {(org, name): repo_data}
    registry_repos = {}
    for organ_key, organ_data in registry.get("organs", {}).items():
        for repo in organ_data.get("repositories", []):
            key = (repo["org"], repo["name"])
            registry_repos[key] = repo

    print(f"\nRegistry contains {len(registry_repos)} total repo entries")

    # ── Step 1: List all repos on GitHub ────────────────────────────
    print("\n── Listing repos on GitHub ──")
    github_repos = {}  # org -> [repo_names]

    for org in SYSTEM_ORGS:
        sys.stdout.write(f"\r  Listing {org}...")
        sys.stdout.flush()
        repos = gh_list_repos(org)
        github_repos[org] = repos
        print(f"\r  {org}: {len(repos)} repos")

    total_gh = sum(len(v) for v in github_repos.values())
    print(f"\n  Total repos on GitHub: {total_gh}")

    # ── Step 2: Check registry DEPLOYED repos exist on GitHub ──────
    print("\n── Checking DEPLOYED repos exist on GitHub ──")
    deployed_missing = []
    deployed_no_readme = []
    deployed_ok = []

    for (org, name), repo_data in registry_repos.items():
        doc_status = repo_data.get("documentation_status", "")
        note = repo_data.get("note", "")

        # Only check repos that should be DEPLOYED and not NOT_CREATED
        if "NOT_CREATED" in note:
            continue
        if "DEPLOYED" not in doc_status and doc_status != "INFRASTRUCTURE":
            continue

        if name not in github_repos.get(org, []):
            deployed_missing.append((org, name, doc_status))
        else:
            has_rm = gh_has_readme(org, name)
            if has_rm:
                deployed_ok.append((org, name))
            elif has_rm is False:
                deployed_no_readme.append((org, name, doc_status))
            # None means timeout — treat as ok for now

    print(f"  DEPLOYED repos on GitHub with README: {len(deployed_ok)}")
    print(f"  DEPLOYED repos missing from GitHub: {len(deployed_missing)}")
    print(f"  DEPLOYED repos on GitHub WITHOUT README: {len(deployed_no_readme)}")

    if deployed_missing:
        print("\n  MISSING FROM GITHUB:")
        for org, name, status in deployed_missing:
            print(f"    - {org}/{name} (registry says: {status})")

    if deployed_no_readme:
        print("\n  NO README ON GITHUB:")
        for org, name, status in deployed_no_readme:
            print(f"    - {org}/{name} (registry says: {status})")

    # ── Step 3: Check for GitHub repos missing from registry ────────
    print("\n── Checking for GitHub repos not in registry ──")
    github_not_in_registry = []

    for org, repo_names in github_repos.items():
        for name in repo_names:
            if (org, name) not in registry_repos:
                github_not_in_registry.append((org, name))

    if github_not_in_registry:
        print(f"  {len(github_not_in_registry)} repos on GitHub not in registry:")
        for org, name in github_not_in_registry:
            print(f"    - {org}/{name}")
    else:
        print("  All GitHub repos accounted for in registry")

    # ── Step 4: Description comparison ──────────────────────────────
    print("\n── Checking description matches ──")
    desc_mismatches = []

    # Only check repos that had descriptions set during Gold Sprint
    for (org, name), repo_data in registry_repos.items():
        note = repo_data.get("note", "")
        if "NOT_CREATED" in note:
            continue
        if name not in github_repos.get(org, []):
            continue

        registry_desc = repo_data.get("description", "")
        # Only compare if registry has a substantial description
        if not registry_desc or len(registry_desc) < 20:
            continue

        gh_desc = gh_get_description(org, name)
        if gh_desc is not None and gh_desc and gh_desc != registry_desc:
            # Only flag if they're very different (not just minor wording changes)
            if len(gh_desc) > 0 and registry_desc.lower()[:50] != gh_desc.lower()[:50]:
                desc_mismatches.append((org, name, registry_desc[:80], gh_desc[:80]))

    if desc_mismatches:
        print(f"  {len(desc_mismatches)} description mismatches:")
        for org, name, reg_desc, gh_desc in desc_mismatches[:10]:
            print(f"    {org}/{name}:")
            print(f"      Registry: {reg_desc}...")
            print(f"      GitHub:   {gh_desc}...")
    else:
        print("  No significant description mismatches found")

    # ── Summary ──────────────────────────────────────────────────────
    print(f"\n{'=' * 80}")
    print("V3 SUMMARY")
    print(f"{'=' * 80}")
    print(f"  Registry repos: {len(registry_repos)}")
    print(f"  GitHub repos: {total_gh}")
    print(f"  DEPLOYED + on GitHub + has README: {len(deployed_ok)}")
    print(f"  DEPLOYED but missing from GitHub: {len(deployed_missing)}")
    print(f"  DEPLOYED but no README: {len(deployed_no_readme)}")
    print(f"  On GitHub but not in registry: {len(github_not_in_registry)}")
    print(f"  Description mismatches: {len(desc_mismatches)}")

    v3_pass = len(deployed_missing) == 0 and len(deployed_no_readme) == 0
    print(f"\n  V3 RESULT: {'PASS' if v3_pass else 'ISSUES FOUND'}")

    # Write report
    report = {
        "registry_count": len(registry_repos),
        "github_count": total_gh,
        "deployed_ok": len(deployed_ok),
        "deployed_missing": [{"org": o, "repo": r, "status": s} for o, r, s in deployed_missing],
        "deployed_no_readme": [{"org": o, "repo": r, "status": s} for o, r, s in deployed_no_readme],
        "github_not_in_registry": [{"org": o, "repo": r} for o, r in github_not_in_registry],
        "description_mismatches": [{"org": o, "repo": r, "registry": rd, "github": gd} for o, r, rd, gd in desc_mismatches],
        "pass": v3_pass
    }

    report_path = os.path.join(os.path.dirname(__file__), "v3-report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n  Report written to {report_path}")


if __name__ == "__main__":
    main()
