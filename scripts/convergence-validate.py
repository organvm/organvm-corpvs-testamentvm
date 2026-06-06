#!/usr/bin/env python3
"""CONVERGENCE Sprint Phase G: Consolidated validation report.

Runs all validators and produces a unified pass/fail summary.
"""

import json
import subprocess
import sys
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent.parent / "repo-registry.json"
PROVENANCE_PATH = Path(__file__).parent.parent / "provenance-registry.json"
SCRIPTS_DIR = Path(__file__).parent


def check_registry():
    """Verify registry implementation_status distribution."""
    with open(REGISTRY_PATH) as f:
        reg = json.load(f)

    counts = {}
    for organ_data in reg["organs"].values():
        for r in organ_data["repositories"]:
            s = r.get("implementation_status", "UNKNOWN")
            counts[s] = counts.get(s, 0) + 1

    total = sum(counts.values())
    active = counts.get("ACTIVE", 0)
    archived = counts.get("ARCHIVED", 0)
    other = total - active - archived

    print(f"  Registry: {total} repos, {active} ACTIVE, {archived} ARCHIVED, {other} other")
    return other == 0 and total == 89


def check_provenance():
    """Verify provenance None-target resolution."""
    with open(PROVENANCE_PATH) as f:
        prov = json.load(f)

    source_map = prov["source_to_repo"]
    total = len(source_map)
    none_untriaged = sum(
        1 for v in source_map.values()
        if "/None" in v.get("target", "") and "triage" not in v
    )
    deployed = sum(1 for v in source_map.values() if v.get("deployed"))
    triaged = sum(1 for v in source_map.values() if "triage" in v)

    print(f"  Provenance: {total} files, {deployed} deployed, {triaged} triaged, {none_untriaged} untriaged None")
    return none_untriaged == 0


def check_essays():
    """Verify essay count in public-process."""
    result = subprocess.run(
        ["gh", "api", "repos/organvm-v-logos/public-process/git/trees/HEAD?recursive=1",
         "--jq", '[.tree[] | select(.path | startswith("_posts/"))] | length'],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  Essays: FAILED to query (API error)")
        return False

    count = int(result.stdout.strip())
    print(f"  Essays: {count} in _posts/")
    return count >= 28


def check_dependencies():
    """Run dependency validation."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "v4-dependency-validation.py")],
        capture_output=True, text=True,
    )
    output = result.stdout + result.stderr
    passed = "V4 RESULT: PASS" in output
    violations = "0" if passed else "unknown"
    for line in output.split("\n"):
        if "Total violations:" in line:
            violations = line.split(":")[-1].strip()
    print(f"  Dependencies: {violations} violations {'(PASS)' if passed else '(FAIL)'}")
    return passed


def main():
    print("=" * 60)
    print("CONVERGENCE Sprint — Final Validation Report")
    print("=" * 60)
    print()

    checks = [
        ("Registry integrity", check_registry),
        ("Provenance resolution", check_provenance),
        ("Essay deployment", check_essays),
        ("Dependency validation", check_dependencies),
    ]

    results = []
    for name, check_fn in checks:
        print(f"[CHECK] {name}")
        try:
            passed = check_fn()
        except Exception as e:
            print(f"  ERROR: {e}")
            passed = False
        results.append((name, passed))
        print()

    print("=" * 60)
    print("RESULTS")
    print("=" * 60)
    all_passed = True
    for name, passed in results:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"  [{status}] {name}")

    print()
    if all_passed:
        print("CONVERGENCE VALIDATION: ALL CHECKS PASSED")
    else:
        print("CONVERGENCE VALIDATION: SOME CHECKS FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
