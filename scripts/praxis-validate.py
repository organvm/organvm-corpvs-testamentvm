#!/usr/bin/env python3
"""PRAXIS Sprint: Consolidated validation report.

Extends convergence-validate.py with PRAXIS-specific checks:
  - Phase A: Portfolio site live and accessible
  - Phase B: Flagship repos have real code (not skeleton)
  - Phase C: Distribution channels active
  - Phase D: Application materials generated and clean
  - Phase E: Dashboard metrics available
  - Phase F: Revenue products deployed
  - Phase G: Community infrastructure

Also runs all CONVERGENCE checks for regression.

Usage:
    python3 scripts/praxis-validate.py
"""

import json
import subprocess
import sys
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent.parent / "repo-registry.json"
PROVENANCE_PATH = Path(__file__).parent.parent / "provenance-registry.json"
SCRIPTS_DIR = Path(__file__).parent
SITE_DATA_DIR = Path(__file__).parent.parent / "site-data"
APPLICATIONS_DIR = Path(__file__).parent.parent / "applications"
FLAGSHIP_REPORT = Path(__file__).parent.parent / "praxis-flagship-report.json"
METRICS_FILE = Path(__file__).parent.parent / "system-metrics.json"


# ── CONVERGENCE checks (regression) ──────────────────────

def check_registry():
    """Verify registry implementation_status distribution."""
    with open(REGISTRY_PATH) as f:
        reg = json.load(f)

    valid_statuses = {"ACTIVE", "PROTOTYPE", "SKELETON", "DESIGN_ONLY", "ARCHIVED"}
    counts = {}
    invalid = []
    for organ_data in reg["organs"].values():
        for r in organ_data["repositories"]:
            s = r.get("implementation_status", "UNKNOWN")
            counts[s] = counts.get(s, 0) + 1
            if s not in valid_statuses:
                invalid.append(f"{r['name']}: {s}")

    total = sum(counts.values())
    active = counts.get("ACTIVE", 0)
    archived = counts.get("ARCHIVED", 0)
    other = total - active - archived

    parts = [f"{total} repos", f"{active} ACTIVE", f"{archived} ARCHIVED"]
    if other > 0:
        for s, c in sorted(counts.items()):
            if s not in ("ACTIVE", "ARCHIVED") and c > 0:
                parts.append(f"{c} {s}")
    print(f"  Registry: {', '.join(parts)}")

    if invalid:
        print(f"  INVALID statuses: {invalid}")
    return len(invalid) == 0 and total >= 89


def check_provenance():
    """Verify provenance None-target resolution."""
    if not PROVENANCE_PATH.exists():
        print("  Provenance: registry not found (skipped)")
        return True  # Not a regression if file is absent

    with open(PROVENANCE_PATH) as f:
        prov = json.load(f)

    source_map = prov.get("source_to_repo", {})
    total = len(source_map)
    none_untriaged = sum(
        1 for v in source_map.values()
        if "/None" in v.get("target", "") and "triage" not in v
    )

    print(f"  Provenance: {total} files, {none_untriaged} untriaged None-targets")
    return none_untriaged == 0


def check_essays():
    """Verify essay count in public-process."""
    result = subprocess.run(
        ["gh", "api", "repos/organvm-v-logos/public-process/git/trees/HEAD?recursive=1",
         "--jq", '[.tree[] | select(.path | startswith("_posts/"))] | length'],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  Essays: FAILED to query")
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
    print(f"  Dependencies: {'PASS' if passed else 'FAIL'}")
    return passed


# ── PRAXIS checks ────────────────────────────────────────

def check_portfolio_data():
    """Phase A: Verify portfolio site data was generated."""
    expected = ["landing.json", "projects.json", "essays.json", "graph.json", "about.json", "rss-meta.json"]
    missing = [f for f in expected if not (SITE_DATA_DIR / f).exists()]

    if missing:
        print(f"  Portfolio data: MISSING {missing}")
        return False

    # Check project count
    with open(SITE_DATA_DIR / "projects.json") as f:
        projects = json.load(f)
    curated = projects.get("total_curated", 0)
    print(f"  Portfolio data: {len(expected)} files, {curated} curated projects")
    return curated >= 15  # Target ~19


def check_portfolio_site():
    """Phase A: Check if portfolio site is live.

    Checks that the live portfolio at 4444j99.github.io/portfolio/ returns
    HTTP 200, and that the Dashboard page is accessible (merged from PRAXIS).
    The portfolio lives at 4444J99/portfolio, not the local portfolio-site/ scaffold.
    """
    urls = [
        ("Portfolio home", "https://4444j99.github.io/portfolio/"),
        ("Dashboard page", "https://4444j99.github.io/portfolio/dashboard/"),
    ]

    all_ok = True
    for label, url in urls:
        result = subprocess.run(
            ["curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}", url],
            capture_output=True, text=True, timeout=15,
        )
        status = result.stdout.strip() if result.returncode == 0 else "ERR"
        ok = status == "200"
        if not ok:
            all_ok = False
        print(f"  {label}: HTTP {status}")

    return all_ok


def check_flagship_substance():
    """Phase B: Verify flagship repos have real code."""
    if not FLAGSHIP_REPORT.exists():
        print(f"  Flagships: No audit report (run praxis-flagship-audit.py)")
        return False

    with open(FLAGSHIP_REPORT) as f:
        report = json.load(f)

    cls = report.get("classifications", {})
    substantial = cls.get("SUBSTANTIAL", 0)
    partial = cls.get("PARTIAL", 0)
    total = report.get("total_audited", 0)

    print(f"  Flagships: {substantial} SUBSTANTIAL, {partial} PARTIAL, "
          f"{total - substantial - partial} need work")
    print(f"  NOTE: Pre-PRAXIS baseline was 4 SUBSTANTIAL — no vivification work done")

    # Target: 6+ of 8 flagships at SUBSTANTIAL or PARTIAL
    return (substantial + partial) >= 6


def check_distribution():
    """Phase C: Check distribution channel readiness."""
    report_path = Path(__file__).parent.parent / "praxis-distribution-report.json"
    if not report_path.exists():
        print(f"  Distribution: No report (run praxis-distribution-setup.py)")
        return False

    with open(report_path) as f:
        report = json.load(f)

    ready = report.get("channels_ready", 0)
    total = report.get("channels_total", 0)
    print(f"  Distribution: {ready}/{total} channels ready (target: 2+)")
    print(f"  NOTE: RSS was pre-existing before PRAXIS")
    return ready >= 2


def check_applications():
    """Phase D: Check application materials generated and clean."""
    if not APPLICATIONS_DIR.exists():
        print(f"  Applications: Directory not found")
        return False

    md_files = list(APPLICATIONS_DIR.glob("*.md"))

    if len(md_files) < 5:
        print(f"  Applications: Only {len(md_files)} materials (need 5)")
        return False

    # Check for placeholder content — applications with placeholders are not submittable
    placeholder_count = 0
    watermark_count = 0
    for md_file in md_files:
        content = md_file.read_text()
        if "[Insert " in content:
            placeholder_count += 1
        if "Generated by praxis" in content:
            watermark_count += 1

    issues = []
    if placeholder_count > 0:
        issues.append(f"{placeholder_count} with [Insert...] placeholders")
    if watermark_count > 0:
        issues.append(f"{watermark_count} with machine-generated watermarks")

    if issues:
        print(f"  Applications: {len(md_files)} materials — {', '.join(issues)}")
        return False

    print(f"  Applications: {len(md_files)} materials, no placeholders or watermarks")
    return True


def check_dashboard():
    """Phase E: Check dashboard metrics available and not stale."""
    if not METRICS_FILE.exists():
        print(f"  Dashboard: system-metrics.json not found")
        return False

    with open(METRICS_FILE) as f:
        metrics = json.load(f)

    # Support both old schema (registry/essays/sprint_history/praxis_targets)
    # and new METRICUM schema (computed/manual with schema_version)
    if metrics.get("schema_version") == "1.0":
        # New schema: check computed section has required keys
        computed = metrics.get("computed", {})
        required = ["total_repos", "active_repos", "published_essays", "sprints_completed"]
        present = sum(1 for k in required if k in computed)
        has_manual = "manual" in metrics

        print(f"  Dashboard: schema v1.0, {present}/{len(required)} computed keys, "
              f"manual={'yes' if has_manual else 'no'}")
        return present == len(required) and has_manual
    else:
        # Legacy schema
        has_registry = "registry" in metrics
        has_essays = "essays" in metrics
        has_sprints = "sprint_history" in metrics
        has_targets = "praxis_targets" in metrics
        sections = sum([has_registry, has_essays, has_sprints, has_targets])
        print(f"  Dashboard: legacy schema, {sections}/4 sections present")
        return sections == 4


def check_revenue():
    """Phase F: Check revenue products deployed.

    Validates that at least one ORGAN-III product has a live demo
    and the portfolio products page is accessible.
    """
    checks = {
        "Product demo": "https://organvm-iii-ergon.github.io/gamified-coach-interface/",
        "Products page": "https://4444j99.github.io/portfolio/products/",
    }

    all_ok = True
    for label, url in checks.items():
        try:
            result = subprocess.run(
                ["curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}", url],
                capture_output=True, text=True, timeout=15,
            )
            status = result.stdout.strip() if result.returncode == 0 else "ERR"
        except Exception:
            status = "ERR"
        ok = status == "200"
        if not ok:
            all_ok = False
        print(f"  {label}: HTTP {status}")

    return all_ok


def check_community():
    """Phase G: Check community infrastructure.

    Validates that GitHub Discussions are enabled on at least one
    ORGAN-VI repo and the portfolio community page is accessible.
    """
    # Check Discussions enabled on salon-archive
    result = subprocess.run(
        ["gh", "api", "repos/organvm-vi-koinonia/salon-archive", "--jq", ".has_discussions"],
        capture_output=True, text=True,
    )
    discussions_ok = result.stdout.strip() == "true"
    print(f"  Discussions (salon-archive): {'enabled' if discussions_ok else 'DISABLED'}")

    # Check community page is live
    try:
        page_result = subprocess.run(
            ["curl", "-sI", "-o", "/dev/null", "-w", "%{http_code}",
             "https://4444j99.github.io/portfolio/community/"],
            capture_output=True, text=True, timeout=15,
        )
        page_status = page_result.stdout.strip() if page_result.returncode == 0 else "ERR"
    except Exception:
        page_status = "ERR"
    page_ok = page_status == "200"
    print(f"  Community page: HTTP {page_status}")

    return discussions_ok and page_ok


def main():
    print("=" * 60)
    print("PRAXIS Sprint — Consolidated Validation Report")
    print("=" * 60)

    # Group checks by phase
    check_groups = [
        ("CONVERGENCE Regression", [
            ("Registry integrity", check_registry),
            ("Provenance resolution", check_provenance),
            ("Essay deployment", check_essays),
            ("Dependency validation", check_dependencies),
        ]),
        ("PRAXIS Phase A — Portfolio", [
            ("Portfolio data generation", check_portfolio_data),
            ("Portfolio site deployment", check_portfolio_site),
        ]),
        ("PRAXIS Phase B — Flagships", [
            ("Flagship code substance", check_flagship_substance),
        ]),
        ("PRAXIS Phase C — Distribution", [
            ("Distribution channels", check_distribution),
        ]),
        ("PRAXIS Phase D — Applications", [
            ("Application materials", check_applications),
        ]),
        ("PRAXIS Phase E — Dashboard", [
            ("Dashboard metrics", check_dashboard),
        ]),
        ("PRAXIS Phase F — Revenue", [
            ("Revenue products", check_revenue),
        ]),
        ("PRAXIS Phase G — Community", [
            ("Community infrastructure", check_community),
        ]),
    ]

    all_results = []

    for group_name, checks in check_groups:
        print(f"\n{'─' * 50}")
        print(f"  {group_name}")
        print(f"{'─' * 50}")

        for name, check_fn in checks:
            print(f"\n[CHECK] {name}")
            try:
                passed = check_fn()
            except Exception as e:
                print(f"  ERROR: {e}")
                passed = False
            all_results.append((group_name, name, passed))

    # Summary
    print(f"\n{'=' * 60}")
    print("RESULTS")
    print(f"{'=' * 60}")

    all_passed = True
    for group_name, name, passed in all_results:
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        print(f"  [{status}] {name}")

    passed_count = sum(1 for _, _, p in all_results if p)
    total_count = len(all_results)

    print(f"\n  Score: {passed_count}/{total_count}")
    print()

    if all_passed:
        print("PRAXIS VALIDATION: ALL CHECKS PASSED")
    else:
        failed = [(g, n) for g, n, p in all_results if not p]
        print(f"PRAXIS VALIDATION: {len(failed)} CHECK(S) FAILED")
        for group, name in failed:
            print(f"  - {name} ({group})")
        sys.exit(1)


if __name__ == "__main__":
    main()
