#!/usr/bin/env python3
"""Platinum Sprint validation script — FULL (no sampling).

Checks every platinum repo for:
1. Registry schema fields (implementation_status, ci_workflow, platinum_status)
2. CI workflow on GitHub (.github/workflows/ci.yml)
3. CHANGELOG.md on GitHub
4. Badge row in README (img.shields.io or badge.svg)
5. ADRs in docs/adr/ (001-initial-architecture.md)
6. ORGAN-V has 10 essays
7. Dependency validation (no back-edges)
8. Implementation status distribution
"""

import json
import subprocess
import sys
import time
from pathlib import Path

# ISOTOPE DISSOLUTION: Gate memory--remember G2 (CORPUS_SCRIPTS_DISSOLVED)
try:
    from organvm_engine.registry.loader import load_registry as _engine_load
except ImportError:
    _engine_load = None

REGISTRY_PATH = Path(__file__).parent.parent / "repo-registry.json"


def check_file_exists(org, repo, path):
    """Check if a file exists on GitHub."""
    result = subprocess.run(
        ["gh", "api", f"/repos/{org}/{repo}/contents/{path}"],
        capture_output=True, text=True
    )
    return result.returncode == 0


def get_readme_content(org, repo):
    """Get README content from GitHub."""
    result = subprocess.run(
        ["gh", "api", f"/repos/{org}/{repo}/contents/README.md",
         "-H", "Accept: application/vnd.github.raw+json"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        return result.stdout
    return ""


def main():
    if _engine_load is not None:
        registry = _engine_load(REGISTRY_PATH)
    else:
        with open(REGISTRY_PATH) as f:
            registry = json.load(f)

    issues = []
    warnings = []
    checks_passed = 0
    checks_total = 0

    print("=" * 60)
    print("PLATINUM SPRINT VALIDATION — FULL (NO SAMPLING)")
    print("=" * 60)

    # Collect all platinum repos
    platinum_repos = []
    all_repos = []
    for organ_key, organ_data in registry["organs"].items():
        if "repositories" not in organ_data:
            continue
        for repo in organ_data["repositories"]:
            all_repos.append(repo)
            if repo.get("platinum_status"):
                platinum_repos.append(repo)

    print(f"\nTotal repos in registry: {len(all_repos)}")
    print(f"Platinum repos: {len(platinum_repos)}")
    print(f"Non-platinum repos: {len(all_repos) - len(platinum_repos)}")

    # =========================================================
    # CHECK 1: Registry schema fields
    # =========================================================
    print("\n--- CHECK 1: Registry Schema Fields (all repos) ---")
    missing_fields = 0
    for repo in all_repos:
        for field in ["implementation_status", "ci_workflow", "platinum_status"]:
            checks_total += 1
            if field not in repo:
                issues.append(f"Missing {field} in {repo.get('org','?')}/{repo.get('name','?')}")
                missing_fields += 1
            else:
                checks_passed += 1
    print(f"  Repos checked: {len(all_repos)}")
    print(f"  Fields checked: {len(all_repos) * 3}")
    print(f"  Missing fields: {missing_fields}")
    print(f"  {'PASS' if missing_fields == 0 else 'FAIL'}")

    # =========================================================
    # CHECK 2: CI workflows on GitHub (ALL platinum repos)
    # =========================================================
    print(f"\n--- CHECK 2: CI Workflows (all {len(platinum_repos)} platinum repos) ---")
    ci_pass = 0
    ci_fail = 0
    for i, repo in enumerate(platinum_repos):
        org = repo["org"]
        name = repo["name"]
        checks_total += 1
        exists = check_file_exists(org, name, ".github/workflows/ci.yml")
        if exists:
            ci_pass += 1
            checks_passed += 1
        else:
            ci_fail += 1
            issues.append(f"Missing CI workflow: {org}/{name}")
        # Progress indicator every 10 repos
        if (i + 1) % 10 == 0:
            print(f"  ... checked {i+1}/{len(platinum_repos)}", flush=True)
        # Rate limit: ~0.3s between API calls
        time.sleep(0.3)
    print(f"  CI workflows found: {ci_pass}/{len(platinum_repos)}")
    if ci_fail > 0:
        print(f"  FAIL ({ci_fail} missing)")
    else:
        print(f"  PASS")

    # =========================================================
    # CHECK 3: CHANGELOG.md on GitHub (ALL platinum repos)
    # =========================================================
    print(f"\n--- CHECK 3: CHANGELOG.md (all {len(platinum_repos)} platinum repos) ---")
    cl_pass = 0
    cl_fail = 0
    for i, repo in enumerate(platinum_repos):
        org = repo["org"]
        name = repo["name"]
        checks_total += 1
        exists = check_file_exists(org, name, "CHANGELOG.md")
        if exists:
            cl_pass += 1
            checks_passed += 1
        else:
            cl_fail += 1
            issues.append(f"Missing CHANGELOG.md: {org}/{name}")
        if (i + 1) % 10 == 0:
            print(f"  ... checked {i+1}/{len(platinum_repos)}", flush=True)
        time.sleep(0.3)
    print(f"  CHANGELOGs found: {cl_pass}/{len(platinum_repos)}")
    if cl_fail > 0:
        print(f"  FAIL ({cl_fail} missing)")
    else:
        print(f"  PASS")

    # =========================================================
    # CHECK 4: Badge rows in README (ALL platinum repos)
    # =========================================================
    print(f"\n--- CHECK 4: Badge Rows in README (all {len(platinum_repos)} platinum repos) ---")
    badge_pass = 0
    badge_fail = 0
    for i, repo in enumerate(platinum_repos):
        org = repo["org"]
        name = repo["name"]
        checks_total += 1
        readme = get_readme_content(org, name)
        if "img.shields.io" in readme or "badge.svg" in readme:
            badge_pass += 1
            checks_passed += 1
        else:
            badge_fail += 1
            warnings.append(f"No badges in README: {org}/{name}")
        if (i + 1) % 10 == 0:
            print(f"  ... checked {i+1}/{len(platinum_repos)}", flush=True)
        time.sleep(0.3)
    print(f"  Badge rows found: {badge_pass}/{len(platinum_repos)}")
    if badge_fail > 0:
        print(f"  WARNING ({badge_fail} missing)")
    else:
        print(f"  PASS")

    # =========================================================
    # CHECK 5: ADRs on GitHub (ALL platinum repos)
    # =========================================================
    print(f"\n--- CHECK 5: ADRs (all {len(platinum_repos)} platinum repos) ---")
    adr_pass = 0
    adr_fail = 0
    for i, repo in enumerate(platinum_repos):
        org = repo["org"]
        name = repo["name"]
        checks_total += 1
        exists = check_file_exists(org, name, "docs/adr/001-initial-architecture.md")
        if exists:
            adr_pass += 1
            checks_passed += 1
        else:
            adr_fail += 1
            issues.append(f"Missing ADR-001: {org}/{name}")
        if (i + 1) % 10 == 0:
            print(f"  ... checked {i+1}/{len(platinum_repos)}", flush=True)
        time.sleep(0.3)
    print(f"  ADRs found: {adr_pass}/{len(platinum_repos)}")
    if adr_fail > 0:
        print(f"  FAIL ({adr_fail} missing)")
    else:
        print(f"  PASS")

    # =========================================================
    # CHECK 6: ORGAN-V essays (10 expected)
    # =========================================================
    print("\n--- CHECK 6: ORGAN-V Essays ---")
    checks_total += 1
    essay_count = 0
    result = subprocess.run(
        ["gh", "api", "/repos/organvm-v-logos/public-process/contents/essays/meta-system"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        data = json.loads(result.stdout)
        essays = [f for f in data if f["name"].endswith(".md")]
        essay_count = len(essays)
        print(f"  Essays found: {essay_count}")
        for e in sorted(essays, key=lambda x: x["name"]):
            print(f"    {e['name']} ({e['size']:,} bytes)")
    if essay_count >= 10:
        print(f"  PASS")
        checks_passed += 1
    else:
        print(f"  FAIL (expected 10, found {essay_count})")
        issues.append(f"Only {essay_count} essays found (expected 10)")

    # =========================================================
    # CHECK 7: Dependency validation (all repos, no back-edges)
    # =========================================================
    print("\n--- CHECK 7: Dependency Validation (all repos) ---")
    checks_total += 1
    dep_violations = 0
    dep_edges = 0
    organ_order = {
        "organvm-i-theoria": 1,
        "organvm-ii-poiesis": 2,
        "organvm-iii-ergon": 3,
        "organvm-iv-taxis": 4,
        "organvm-v-logos": 5,
        "organvm-vi-koinonia": 6,
        "organvm-vii-kerygma": 7,
        "meta-organvm": 8,
    }
    for organ_key, organ_data in registry["organs"].items():
        if "repositories" not in organ_data:
            continue
        for repo in organ_data["repositories"]:
            repo_org = repo.get("org", "")
            repo_order = organ_order.get(repo_org, 0)
            for dep in repo.get("dependencies", []):
                dep_edges += 1
                dep_org = dep.split("/")[0] if "/" in dep else ""
                dep_order = organ_order.get(dep_org, 0)
                # Back-edge: lower-numbered organ depending on higher-numbered
                # Flow is I→II→III, so II can depend on I, III on I or II
                # Violation: I depending on II/III, or II depending on III
                if repo_order < dep_order and repo_order > 0 and dep_order <= 3:
                    dep_violations += 1
                    issues.append(f"Back-edge: {repo_org}/{repo['name']} -> {dep}")
    print(f"  Total dependency edges: {dep_edges}")
    print(f"  Violations: {dep_violations}")
    if dep_violations == 0:
        print(f"  PASS")
        checks_passed += 1
    else:
        print(f"  FAIL")

    # =========================================================
    # CHECK 8: Implementation status distribution
    # =========================================================
    print("\n--- CHECK 8: Implementation Status Distribution ---")
    checks_total += 1
    status_dist = {"PRODUCTION": 0, "PROTOTYPE": 0, "SKELETON": 0, "DESIGN_ONLY": 0}
    for repo in all_repos:
        s = repo.get("implementation_status", "DESIGN_ONLY")
        if s in status_dist:
            status_dist[s] += 1
    total_categorized = sum(status_dist.values())
    print(f"  PRODUCTION:  {status_dist['PRODUCTION']}")
    print(f"  PROTOTYPE:   {status_dist['PROTOTYPE']}")
    print(f"  SKELETON:    {status_dist['SKELETON']}")
    print(f"  DESIGN_ONLY: {status_dist['DESIGN_ONLY']}")
    print(f"  Total:       {total_categorized}")
    checks_passed += 1
    print(f"  PASS")

    # =========================================================
    # CHECK 9: Non-platinum repos have schema fields too
    # =========================================================
    print("\n--- CHECK 9: Non-Platinum Repos Have Default Fields ---")
    non_plat = [r for r in all_repos if not r.get("platinum_status")]
    non_plat_missing = 0
    for repo in non_plat:
        for field in ["implementation_status", "platinum_status"]:
            checks_total += 1
            if field not in repo:
                non_plat_missing += 1
                issues.append(f"Non-plat missing {field}: {repo.get('org','?')}/{repo.get('name','?')}")
            else:
                checks_passed += 1
    print(f"  Non-platinum repos checked: {len(non_plat)}")
    print(f"  Missing fields: {non_plat_missing}")
    if non_plat_missing == 0:
        print(f"  PASS")
    else:
        print(f"  FAIL")

    # =========================================================
    # SUMMARY
    # =========================================================
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Total checks: {checks_total}")
    print(f"Passed:       {checks_passed}")
    print(f"Failed:       {checks_total - checks_passed - len(warnings)}")
    print(f"Warnings:     {len(warnings)}")
    if issues:
        print(f"\nISSUES ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  - {w}")
    if not issues:
        print(f"\nALL {checks_total} CHECKS PASSED")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
