#!/usr/bin/env python3
"""Soak Test Monitor — 30-day system health and engagement tracker.

Runs validation checks (registry integrity, dependency graph, CI status)
and collects engagement metrics (stars, forks, views, clones) via GitHub API.
Outputs daily JSON snapshots and generates a 30-day summary report.

Combines logic from:
  - organ-audit.py (validation, registry loading, dependency graph)
  - praxis-metrics-dashboard.py (GitHub API engagement queries, CI status)
  - calculate-metrics.py (metric computation patterns)

Usage:
    python3 scripts/soak-test-monitor.py collect [--dry-run]
    python3 scripts/soak-test-monitor.py report [--days 30]
"""

import argparse
import json
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Shared, time-invariant validators (single source of truth). Validating
# previous-state-with-current-rules (IRF-RES-013) requires that the soak
# collector and the temporal-staging validator run *identical* logic, so the
# rule-based checks live in one module rather than being duplicated here.
sys.path.insert(0, str(Path(__file__).parent))
from governance_validators import (  # noqa: E402
    build_repo_map,
    project_state,
    validate_dependencies,
    validate_registry,
)

REPO_ROOT = Path(__file__).parent.parent
REGISTRY_PATH = REPO_ROOT / "repo-registry.json"
GOVERNANCE_PATH = REPO_ROOT / "governance-rules.json"
DATA_DIR = REPO_ROOT / "data" / "soak-test"

# Top repos to track engagement (flagships + high-visibility)
TOP_REPOS = [
    ("organvm-i-theoria", "recursive-engine--generative-entity"),
    ("organvm-ii-poiesis", "metasystem-master"),
    ("organvm-ii-poiesis", "a-mavs-olevm"),
    ("organvm-iii-ergon", "public-record-data-scrapper"),
    ("organvm-iv-taxis", "orchestration-start-here"),
    ("organvm-iv-taxis", "agentic-titan"),
    ("organvm-v-logos", "public-process"),
    ("meta-organvm", "organvm-corpvs-testamentvm"),
]


# ISOTOPE DISSOLUTION: Gate memory--remember G2 (CORPUS_SCRIPTS_DISSOLVED)
try:
    from organvm_engine.registry.loader import load_registry as _engine_load
except ImportError:
    _engine_load = None


def load_registry() -> dict:
    if _engine_load is not None:
        return _engine_load(REGISTRY_PATH)
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def load_governance() -> dict:
    with open(GOVERNANCE_PATH) as f:
        return json.load(f)


def gh_api(endpoint: str, jq_filter: str | None = None, timeout: int = 15) -> tuple[int, str]:
    """Run a gh api call, return (returncode, stdout)."""
    cmd = ["gh", "api", endpoint]
    if jq_filter:
        cmd.extend(["--jq", jq_filter])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return result.returncode, result.stdout.strip()


# --- Validation Checks ---
# Rule-based validators (validate_registry, validate_dependencies, build_repo_map)
# are imported from governance_validators so the temporal-staging validator can
# apply the identical logic to a previous state. Only time-relative checks
# (staleness) remain local — they have no meaning when re-run against the past.

def check_stale_repos(registry: dict, threshold_days: int = 90) -> list:
    """Find repos not validated within threshold."""
    _, all_repos = build_repo_map(registry)
    now = datetime.now(timezone.utc)
    stale = []
    for repo in all_repos:
        last = repo.get("last_validated", "")
        if not last:
            continue
        try:
            last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
            age = (now - last_dt).days
            if age > threshold_days:
                stale.append(f"{repo['org']}/{repo['name']} ({age}d)")
        except (ValueError, TypeError):
            pass
    return stale


# --- CI Status ---

def fetch_ci_status(registry: dict, dry_run: bool = False) -> dict:
    """Fetch latest CI run status for non-archived repos with CI configured.

    Filters to push events only (excludes Dependabot PRs, scheduled runs, and
    Pages builds). Repos in billing-locked orgs are classified separately so
    they don't inflate the failure count.
    """
    if dry_run:
        return {"total_checked": 0, "passing": 0, "failing": 0, "unknown": 0,
                "billing_locked": 0, "dry_run": True}

    # Orgs with known billing locks — CI runs fail with empty runners.
    # Update this set when billing is resolved or new locks appear.
    BILLING_LOCKED_ORGS = {"organvm-i-theoria"}

    _, all_repos = build_repo_map(registry)
    ci_repos = [
        r for r in all_repos
        if r.get("implementation_status") != "ARCHIVED" and r.get("ci_workflow")
    ]

    passing = 0
    failing = 0
    unknown = 0
    billing_locked = 0
    failures = []
    billing_locked_repos = []

    for repo in ci_repos:
        org = repo["org"]
        name = repo["name"]

        # Skip detailed check for billing-locked orgs — they always fail
        # with empty runner_name, not due to code issues
        if org in BILLING_LOCKED_ORGS:
            billing_locked += 1
            billing_locked_repos.append(f"{org}/{name}")
            time.sleep(0.1)
            continue

        # Filter to push events on default branch to exclude Dependabot PRs,
        # Pages builds, and other non-CI workflow runs
        rc, out = gh_api(
            f"repos/{org}/{name}/actions/runs?per_page=1&event=push",
            '.workflow_runs[0].conclusion // "no_runs"'
        )
        if rc == 0:
            conclusion = out or "no_runs"
            if conclusion == "success":
                passing += 1
            elif conclusion in ("failure", "timed_out", "cancelled"):
                failing += 1
                failures.append(f"{org}/{name}: {conclusion}")
            else:
                unknown += 1
        else:
            unknown += 1
        time.sleep(0.3)  # rate limiting

    return {
        "total_checked": len(ci_repos),
        "passing": passing,
        "failing": failing,
        "unknown": unknown,
        "billing_locked": billing_locked,
        "billing_locked_repos": billing_locked_repos,
        "failures": failures,
    }


# --- Engagement Metrics ---

def fetch_engagement(dry_run: bool = False) -> dict:
    """Fetch stars, forks, views, clones for top repos."""
    if dry_run:
        return {"total_stars": 0, "total_forks": 0, "top_repos": {},
                "dry_run": True}

    total_stars = 0
    total_forks = 0
    top_repos = {}

    for org, name in TOP_REPOS:
        repo_data = {"stars": 0, "forks": 0, "views_14d": 0, "clones_14d": 0}

        # Stars and forks
        rc, out = gh_api(f"repos/{org}/{name}", ".stargazers_count")
        if rc == 0 and out.isdigit():
            repo_data["stars"] = int(out)
            total_stars += int(out)

        rc, out = gh_api(f"repos/{org}/{name}", ".forks_count")
        if rc == 0 and out.isdigit():
            repo_data["forks"] = int(out)
            total_forks += int(out)

        # Traffic (views) — requires push access
        rc, out = gh_api(f"repos/{org}/{name}/traffic/views", ".count")
        if rc == 0 and out.isdigit():
            repo_data["views_14d"] = int(out)

        # Traffic (clones) — requires push access
        rc, out = gh_api(f"repos/{org}/{name}/traffic/clones", ".count")
        if rc == 0 and out.isdigit():
            repo_data["clones_14d"] = int(out)

        top_repos[f"{org}/{name}"] = repo_data
        time.sleep(0.3)

    return {
        "total_stars": total_stars,
        "total_forks": total_forks,
        "top_repos": top_repos,
    }


# --- Collect Command ---

def cmd_collect(args):
    """Daily snapshot: validate + collect engagement."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"{'=' * 60}")
    print(f"Soak Test Monitor — Collect ({today})")
    print(f"{'=' * 60}")

    if args.dry_run:
        print("[DRY RUN] Skipping GitHub API calls\n")

    registry = load_registry()
    governance = load_governance()

    # 1. Registry validation
    print("\n[1/4] Registry validation...")
    reg_result = validate_registry(registry)
    print(f"  Repos: {reg_result['total_repos']}, Issues: {len(reg_result['issues'])}, "
          f"Pass: {reg_result['pass']}")

    # 2. Dependency validation
    print("\n[2/4] Dependency validation...")
    dep_result = validate_dependencies(registry, governance)
    print(f"  Edges: {dep_result['total_edges']}, Back-edges: {len(dep_result['back_edges'])}, "
          f"Cycles: {len(dep_result['cycles'])}, Depth: {dep_result['max_depth']}/{dep_result['depth_limit']}, "
          f"Pass: {dep_result['pass']}")

    # 3. CI status
    print("\n[3/4] CI status...")
    ci_result = fetch_ci_status(registry, dry_run=args.dry_run)
    print(f"  Checked: {ci_result['total_checked']}, Passing: {ci_result.get('passing', 0)}, "
          f"Failing: {ci_result.get('failing', 0)}, Unknown: {ci_result.get('unknown', 0)}, "
          f"Billing-locked: {ci_result.get('billing_locked', 0)}")

    # 4. Engagement
    print("\n[4/4] Engagement metrics...")
    eng_result = fetch_engagement(dry_run=args.dry_run)
    print(f"  Stars: {eng_result['total_stars']}, Forks: {eng_result['total_forks']}")

    # Stale repos
    stale = check_stale_repos(registry)

    # Freeze the validation-relevant state so a future run can re-validate this
    # snapshot under whatever rules are then current (temporal staging, IRF-RES-013).
    state_capsule = project_state(registry, governance)

    # Assemble snapshot
    snapshot = {
        "date": today,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "state_capsule": state_capsule,
        "validation": {
            "registry_pass": reg_result["pass"],
            "registry_issues": reg_result["issues"],
            "dependency_pass": dep_result["pass"],
            "dependency_violations": len(dep_result["back_edges"]) + len(dep_result["cycles"]),
            "stale_repos": stale,
        },
        "ci": {
            "total_checked": ci_result["total_checked"],
            "passing": ci_result.get("passing", 0),
            "failing": ci_result.get("failing", 0),
            "unknown": ci_result.get("unknown", 0),
            "billing_locked": ci_result.get("billing_locked", 0),
            "billing_locked_repos": ci_result.get("billing_locked_repos", []),
            "failures": ci_result.get("failures", []),
        },
        "engagement": eng_result,
    }

    if args.dry_run:
        snapshot["dry_run"] = True

    # Write snapshot
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / f"daily-{today}.json"
    with open(output_path, "w") as f:
        json.dump(snapshot, f, indent=2)
        f.write("\n")

    print(f"\n{'=' * 60}")
    print(f"Snapshot written: {output_path}")

    # Summary verdict (informational only — collector always returns 0
    # so that CI commits the snapshot regardless of system health)
    all_pass = reg_result["pass"] and dep_result["pass"]
    if ci_result.get("failing", 0) > 5:
        all_pass = False
    print(f"Validation: {'PASS' if all_pass else 'ISSUES DETECTED'}")
    print(f"{'=' * 60}")

    return 0


# --- Report Command ---

def cmd_report(args):
    """Generate summary report from collected daily snapshots."""
    print(f"{'=' * 60}")
    print(f"Soak Test Monitor — Report")
    print(f"{'=' * 60}")

    snapshots = sorted(DATA_DIR.glob("daily-*.json"))
    if not snapshots:
        print("No snapshots found. Run 'collect' first.")
        return 1

    # Load all snapshots (skip dry-run ones for report)
    data = []
    for path in snapshots:
        with open(path) as f:
            snap = json.load(f)
        if not snap.get("dry_run"):
            data.append(snap)

    if not data:
        print("No non-dry-run snapshots found.")
        return 1

    # Limit to requested days
    data = data[-args.days:]

    print(f"\nAnalyzing {len(data)} snapshots ({data[0]['date']} to {data[-1]['date']})\n")

    # Validation trends
    validation_passes = sum(1 for d in data
                           if d["validation"]["registry_pass"]
                           and d["validation"]["dependency_pass"])

    # CI trends
    ci_days = [d for d in data if d["ci"]["total_checked"] > 0]
    avg_passing = (sum(d["ci"]["passing"] for d in ci_days) / len(ci_days)) if ci_days else 0
    avg_failing = (sum(d["ci"]["failing"] for d in ci_days) / len(ci_days)) if ci_days else 0

    # Engagement trends
    eng_days = [d for d in data if d["engagement"].get("total_stars") is not None
                and not d["engagement"].get("dry_run")]
    first_stars = eng_days[0]["engagement"]["total_stars"] if eng_days else 0
    last_stars = eng_days[-1]["engagement"]["total_stars"] if eng_days else 0
    first_forks = eng_days[0]["engagement"]["total_forks"] if eng_days else 0
    last_forks = eng_days[-1]["engagement"]["total_forks"] if eng_days else 0

    # Recurring failures
    all_failures = []
    for d in data:
        all_failures.extend(d["ci"].get("failures", []))
    failure_counts = defaultdict(int)
    for f in all_failures:
        failure_counts[f] += 1
    chronic_failures = {k: v for k, v in failure_counts.items() if v >= 3}

    # Build report markdown
    report_lines = [
        f"# 30-Day Soak Test Report",
        f"",
        f"**Period:** {data[0]['date']} to {data[-1]['date']}",
        f"**Snapshots:** {len(data)}",
        f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"",
        f"---",
        f"",
        f"## Validation Integrity",
        f"",
        f"- Days with clean validation: **{validation_passes}/{len(data)}**",
        f"- Registry integrity issues: {sum(len(d['validation']['registry_issues']) for d in data)} total across period",
        f"- Dependency violations: {sum(d['validation']['dependency_violations'] for d in data)} total across period",
        f"",
    ]

    # List any validation issues
    all_reg_issues = set()
    for d in data:
        all_reg_issues.update(d["validation"]["registry_issues"])
    if all_reg_issues:
        report_lines.append("### Registry Issues Observed")
        report_lines.append("")
        for issue in sorted(all_reg_issues):
            report_lines.append(f"- {issue}")
        report_lines.append("")

    avg_billing_locked = (sum(d["ci"].get("billing_locked", 0) for d in ci_days)
                          / len(ci_days)) if ci_days else 0

    report_lines.extend([
        f"## CI Stability",
        f"",
        f"- Average passing: **{avg_passing:.1f}** per day",
        f"- Average failing: **{avg_failing:.1f}** per day",
        f"- Average billing-locked: **{avg_billing_locked:.1f}** per day",
        f"- Days with CI data: {len(ci_days)}",
        f"",
    ])

    if chronic_failures:
        report_lines.append("### Chronic Failures (3+ days)")
        report_lines.append("")
        for repo, count in sorted(chronic_failures.items(), key=lambda x: -x[1]):
            report_lines.append(f"- {repo} ({count} days)")
        report_lines.append("")

    report_lines.extend([
        f"## Engagement Trends",
        f"",
        f"| Metric | Start | End | Delta |",
        f"|--------|-------|-----|-------|",
        f"| Stars | {first_stars} | {last_stars} | {last_stars - first_stars:+d} |",
        f"| Forks | {first_forks} | {last_forks} | {last_forks - first_forks:+d} |",
        f"",
    ])

    # Per-repo engagement if available
    if eng_days:
        report_lines.append("### Top Repo Engagement (Latest)")
        report_lines.append("")
        report_lines.append("| Repo | Stars | Forks | Views (14d) | Clones (14d) |")
        report_lines.append("|------|-------|-------|-------------|--------------|")
        latest = eng_days[-1]["engagement"].get("top_repos", {})
        for repo, metrics in sorted(latest.items()):
            report_lines.append(
                f"| {repo} | {metrics['stars']} | {metrics['forks']} "
                f"| {metrics['views_14d']} | {metrics['clones_14d']} |"
            )
        report_lines.append("")

    # Verdict
    report_lines.extend([
        f"## Verdict",
        f"",
    ])
    if validation_passes == len(data) and avg_failing < 3:
        report_lines.append("**PASS** — System ran stably for the observed period.")
    elif validation_passes >= len(data) * 0.9:
        report_lines.append("**PASS WITH NOTES** — Minor issues observed but no systemic failures.")
    else:
        report_lines.append("**ISSUES DETECTED** — Review validation failures and chronic CI issues above.")

    report_text = "\n".join(report_lines) + "\n"

    # Write report
    report_path = DATA_DIR / "report.md"
    with open(report_path, "w") as f:
        f.write(report_text)

    print(report_text)
    print(f"\nReport written: {report_path}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Soak Test Monitor — 30-day system health and engagement tracker"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # collect
    collect_parser = subparsers.add_parser("collect", help="Collect daily snapshot")
    collect_parser.add_argument("--dry-run", action="store_true",
                                help="Skip GitHub API calls (validate registry only)")

    # report
    report_parser = subparsers.add_parser("report", help="Generate summary report")
    report_parser.add_argument("--days", type=int, default=30,
                               help="Number of days to include (default: 30)")

    args = parser.parse_args()

    if args.command == "collect":
        return cmd_collect(args)
    elif args.command == "report":
        return cmd_report(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
