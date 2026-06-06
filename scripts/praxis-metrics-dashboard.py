#!/usr/bin/env python3
"""PRAXIS Sprint Phase E: System metrics dashboard generator.

Extends calculate-metrics.py with comprehensive dashboard data:
  - CI status across all repos (live query)
  - Word count / documentation coverage
  - Sprint history timeline
  - Essay publication timeline
  - Dependency graph statistics
  - Flagship vivification progress
  - Distribution channel status

Outputs system-metrics.json for the portfolio dashboard.

Usage:
    python3 scripts/praxis-metrics-dashboard.py [--output system-metrics.json] [--skip-ci]
"""

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent.parent / "repo-registry.json"
FLAGSHIP_REPORT = Path(__file__).parent.parent / "praxis-flagship-report.json"

SPRINT_HISTORY = [
    {"name": "IGNITION", "date": "2026-02-09", "focus": "Org architecture", "deliverables": "8 GitHub orgs created"},
    {"name": "PROPULSION", "date": "2026-02-10", "focus": "Documentation", "deliverables": "Bronze/Silver/Gold sprints"},
    {"name": "ASCENSION", "date": "2026-02-10", "focus": "Validation", "deliverables": "1,267 links audited"},
    {"name": "EXODUS", "date": "2026-02-11", "focus": "Launch", "deliverables": "9/9 criteria met"},
    {"name": "PERFECTION", "date": "2026-02-11", "focus": "Gap-fill", "deliverables": "11 repos, 14 promotions"},
    {"name": "AUTONOMY", "date": "2026-02-12", "focus": "Automation", "deliverables": "seed.yaml, 5 agents, 11 workflows"},
    {"name": "GENESIS", "date": "2026-02-12", "focus": "Creation", "deliverables": "7 new repos from local materials"},
    {"name": "ALCHEMIA", "date": "2026-02-12", "focus": "Aesthetics", "deliverables": "2,012 files, taste.yaml cascading"},
    {"name": "CONVERGENCE", "date": "2026-02-13", "focus": "Coherence", "deliverables": "82 ACTIVE, zero gaps"},
    {"name": "PRAXIS", "date": "2026-02-13", "focus": "Impact", "deliverables": "Portfolio, distribution, revenue"},
    {"name": "VERITAS", "date": "2026-02-13", "focus": "Credibility", "deliverables": "PRODUCTION→ACTIVE, revenue split, essay dates, honesty essay"},
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


def compute_registry_metrics(registry):
    """Compute core metrics from registry."""
    all_repos = []
    organ_metrics = {}

    for organ_key, organ_data in registry["organs"].items():
        repos = organ_data.get("repositories", [])
        all_repos.extend(repos)

        status_dist = defaultdict(int)
        tier_dist = defaultdict(int)
        ci_count = 0
        for r in repos:
            status_dist[r.get("implementation_status", "UNKNOWN")] += 1
            tier_dist[r.get("tier", "unknown")] += 1
            if r.get("ci_workflow"):
                ci_count += 1

        organ_metrics[organ_key] = {
            "name": organ_data.get("name", organ_key),
            "status": organ_data.get("launch_status", "UNKNOWN"),
            "total_repos": len(repos),
            "implementation_status": dict(status_dist),
            "tier_distribution": dict(tier_dist),
            "ci_coverage": ci_count,
        }

    # Global distributions
    global_status = defaultdict(int)
    global_tier = defaultdict(int)
    global_promotion = defaultdict(int)
    global_ci = 0
    dep_count = 0

    for r in all_repos:
        global_status[r.get("implementation_status", "UNKNOWN")] += 1
        global_tier[r.get("tier", "unknown")] += 1
        global_promotion[r.get("promotion_status", "UNKNOWN")] += 1
        if r.get("ci_workflow"):
            global_ci += 1
        dep_count += len(r.get("dependencies", []))

    return {
        "total_repos": len(all_repos),
        "total_organs": len(organ_metrics),
        "operational_organs": sum(1 for o in organ_metrics.values() if o["status"] == "OPERATIONAL"),
        "implementation_status": dict(global_status),
        "tier_distribution": dict(global_tier),
        "promotion_status": dict(global_promotion),
        "ci_coverage": global_ci,
        "dependency_edges": dep_count,
        "organs": organ_metrics,
    }


def fetch_ci_status(registry, skip=False):
    """Fetch latest CI run status for all repos (live query)."""
    if skip:
        return {"skipped": True, "note": "CI status check skipped (--skip-ci)"}

    statuses = {"success": 0, "failure": 0, "no_runs": 0, "error": 0}
    repo_statuses = []

    all_repos = []
    for organ_data in registry["organs"].values():
        for r in organ_data.get("repositories", []):
            if r.get("implementation_status") != "ARCHIVED" and r.get("ci_workflow"):
                all_repos.append(r)

    print(f"  Checking CI for {len(all_repos)} repos...")

    for i, repo in enumerate(all_repos):
        org = repo.get("org", "")
        name = repo["name"]
        result = subprocess.run(
            ["gh", "api", f"repos/{org}/{name}/actions/runs?per_page=1",
             "--jq", ".workflow_runs[0].conclusion // \"no_runs\""],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0:
            conclusion = result.stdout.strip() or "no_runs"
            if conclusion in statuses:
                statuses[conclusion] += 1
            else:
                statuses.setdefault(conclusion, 0)
                statuses[conclusion] += 1
            repo_statuses.append({"org": org, "repo": name, "conclusion": conclusion})
        else:
            statuses["error"] += 1
            repo_statuses.append({"org": org, "repo": name, "conclusion": "error"})

        # Progress indicator every 20 repos
        if (i + 1) % 20 == 0:
            print(f"    ...{i + 1}/{len(all_repos)}")

    return {
        "summary": statuses,
        "total_checked": len(all_repos),
        "repos": repo_statuses,
    }


def fetch_essay_timeline():
    """Fetch essay publication dates."""
    result = subprocess.run(
        ["gh", "api", "repos/organvm-v-logos/public-process/git/trees/HEAD?recursive=1",
         "--jq", '[.tree[] | select(.path | startswith("_posts/")) | .path]'],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return {"error": "Could not fetch essays", "essays": []}

    paths = json.loads(result.stdout.strip())
    timeline = []
    for p in sorted(paths):
        filename = p.replace("_posts/", "")
        parts = filename.split("-", 3)
        if len(parts) >= 4:
            date = f"{parts[0]}-{parts[1]}-{parts[2]}"
            slug = parts[3].replace(".md", "").replace(".markdown", "")
            timeline.append({"date": date, "slug": slug})

    return {
        "total": len(timeline),
        "timeline": timeline,
    }


def load_flagship_progress():
    """Load flagship audit report if available."""
    if FLAGSHIP_REPORT.exists():
        with open(FLAGSHIP_REPORT) as f:
            report = json.load(f)
        return {
            "audit_date": report.get("audit_date", ""),
            "classifications": report.get("classifications", {}),
            "total_audited": report.get("total_audited", 0),
            "repos": [
                {
                    "repo": r["repo"],
                    "org": r["org"],
                    "classification": r.get("classification", "UNKNOWN"),
                    "code_files": r.get("code_files", 0),
                    "test_files": r.get("test_files", 0),
                }
                for r in report.get("repos", [])
            ],
        }
    return {"available": False, "note": "Run praxis-flagship-audit.py first"}


def main():
    parser = argparse.ArgumentParser(description="Generate system metrics dashboard data")
    parser.add_argument("--output", default="system-metrics.json",
                        help="Output JSON metrics path")
    parser.add_argument("--skip-ci", action="store_true",
                        help="Skip live CI status check (faster)")
    args = parser.parse_args()

    print("=" * 60)
    print("PRAXIS Sprint Phase E — System Metrics Dashboard")
    print("=" * 60)

    registry = load_registry()

    # 1. Registry metrics
    print("\n[METRICS] Registry analysis...")
    reg_metrics = compute_registry_metrics(registry)
    print(f"  {reg_metrics['total_repos']} repos, "
          f"{reg_metrics['operational_organs']}/{reg_metrics['total_organs']} organs, "
          f"{reg_metrics['ci_coverage']} CI, "
          f"{reg_metrics['dependency_edges']} edges")

    # 2. CI status
    print("\n[METRICS] CI status...")
    ci_metrics = fetch_ci_status(registry, skip=args.skip_ci)
    if not ci_metrics.get("skipped"):
        summary = ci_metrics.get("summary", {})
        print(f"  Success: {summary.get('success', 0)}, "
              f"Failure: {summary.get('failure', 0)}, "
              f"No runs: {summary.get('no_runs', 0)}")

    # 3. Essay timeline
    print("\n[METRICS] Essay timeline...")
    essay_metrics = fetch_essay_timeline()
    print(f"  {essay_metrics.get('total', 0)} essays")

    # 4. Flagship progress
    print("\n[METRICS] Flagship vivification...")
    flagship_metrics = load_flagship_progress()
    cls = flagship_metrics.get("classifications", {})
    print(f"  SUBSTANTIAL: {cls.get('SUBSTANTIAL', 0)}, "
          f"PARTIAL: {cls.get('PARTIAL', 0)}, "
          f"MINIMAL: {cls.get('MINIMAL', 0)}, "
          f"SKELETON: {cls.get('SKELETON', 0)}")

    # 5. Assemble dashboard
    dashboard = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "sprint": "PRAXIS",
        "system": {
            "name": "ORGANVM",
            "launch_date": registry.get("launch_date", "2026-02-11"),
            "project_status": registry.get("project_status", ""),
        },
        "registry": reg_metrics,
        "ci": ci_metrics,
        "essays": essay_metrics,
        "flagship_vivification": flagship_metrics,
        "sprint_history": SPRINT_HISTORY,
        "praxis_targets": {
            "portfolio_site": {"target": "Live", "current": "In development"},
            "flagship_repos_with_code": {"target": "30+", "current": str(cls.get("SUBSTANTIAL", 0) + cls.get("PARTIAL", 0))},
            "distribution_channels": {"target": "4+", "current": "1 (RSS)"},
            "applications_submitted": {"target": "3-5", "current": "0"},
            "community_events": {"target": "Salon launched", "current": "0"},
            "revenue_products": {"target": "2-3", "current": "0"},
            "real_test_suites": {"target": "30+", "current": str(cls.get("SUBSTANTIAL", 0))},
        },
    }

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        json.dump(dashboard, f, indent=2)
        f.write("\n")

    print(f"\n{'=' * 60}")
    print(f"Dashboard metrics: {output_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
