#!/usr/bin/env python3
"""Detect stale metrics in documentation files.

Compares live-computed metrics against system-metrics.json stored values,
then scans whitelisted docs for strings containing outdated numbers.

Usage:
    python3 scripts/stale-detector.py              # report only
    python3 scripts/stale-detector.py --fix         # auto-fix via propagate-metrics.py
    python3 scripts/stale-detector.py --issue       # create GitHub issue if stale
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# ISOTOPE DISSOLUTION: Gate memory--remember G2 (CORPUS_SCRIPTS_DISSOLVED)
try:
    from organvm_engine.registry.loader import load_registry as _engine_load
except ImportError:
    _engine_load = None

ROOT = Path(__file__).resolve().parent.parent
METRICS_FILE = ROOT / "system-metrics.json"
REGISTRY_FILE = ROOT / "repo-registry.json"
SPRINTS_DIR = ROOT / "docs" / "specs" / "sprints"

# Import whitelist from propagate-metrics.py for consistent file scanning
WHITELIST_GLOBS = [
    "README.md",
    "CLAUDE.md",
    "applications/*.md",
    "applications/shared/*.md",
    "docs/applications/*.md",
    "docs/applications/cover-letters/*.md",
    "docs/essays/09-ai-conductor-methodology.md",
    "docs/operations/*.md",
]


@dataclass
class StaleItem:
    """A stale metric found in the system."""
    metric: str
    stored_value: str
    live_value: str
    source: str  # "system-metrics.json" or a file path


def compute_live_metrics() -> dict:
    """Compute current metrics from registry + sprints + essays."""
    # Registry metrics
    if _engine_load is not None:
        registry = _engine_load(REGISTRY_FILE)
    else:
        with open(REGISTRY_FILE) as f:
            registry = json.load(f)

    organs = registry.get("organs", {})
    all_repos = []
    for organ_data in organs.values():
        all_repos.extend(organ_data.get("repositories", []))

    from collections import defaultdict
    status_dist = defaultdict(int)
    ci_count = 0
    dep_count = 0
    for repo in all_repos:
        status_dist[repo.get("implementation_status", "UNKNOWN")] += 1
        if repo.get("ci_workflow"):
            ci_count += 1
        dep_count += len(repo.get("dependencies", []))

    operational = sum(
        1 for o in organs.values()
        if o.get("launch_status") == "OPERATIONAL"
    )

    # Sprint count from spec files
    sprint_specs = sorted(f.stem for f in SPRINTS_DIR.glob("*.md")) if SPRINTS_DIR.is_dir() else []
    sprint_count = len(sprint_specs)

    # Essay count from GitHub API
    essay_count = None
    try:
        result = subprocess.run(
            ["gh", "api",
             "repos/organvm-v-logos/public-process/git/trees/HEAD?recursive=1",
             "--jq", '[.tree[] | select(.path | startswith("_posts/"))] | length'],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip().isdigit():
            essay_count = int(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return {
        "total_repos": len(all_repos),
        "active_repos": status_dist.get("ACTIVE", 0),
        "archived_repos": status_dist.get("ARCHIVED", 0),
        "total_organs": len(organs),
        "operational_organs": operational,
        "ci_workflows": ci_count,
        "dependency_edges": dep_count,
        "published_essays": essay_count,
        "sprints_completed": sprint_count,
        "sprint_names": sprint_specs,
    }


def compare_metrics(stored: dict, live: dict) -> list[StaleItem]:
    """Compare stored vs live metrics. Returns list of stale items."""
    stale = []
    computed = stored.get("computed", {})

    checks = [
        ("total_repos", "total_repos"),
        ("active_repos", "active_repos"),
        ("archived_repos", "archived_repos"),
        ("total_organs", "total_organs"),
        ("operational_organs", "operational_organs"),
        ("ci_workflows", "ci_workflows"),
        ("dependency_edges", "dependency_edges"),
        ("sprints_completed", "sprints_completed"),
    ]

    for metric, key in checks:
        stored_val = computed.get(key)
        live_val = live.get(key)
        if live_val is not None and stored_val != live_val:
            stale.append(StaleItem(
                metric=metric,
                stored_value=str(stored_val),
                live_value=str(live_val),
                source="system-metrics.json",
            ))

    # Essay count (only if we got a live value)
    if live.get("published_essays") is not None:
        stored_essays = computed.get("published_essays")
        live_essays = live["published_essays"]
        if stored_essays != live_essays:
            stale.append(StaleItem(
                metric="published_essays",
                stored_value=str(stored_essays),
                live_value=str(live_essays),
                source="system-metrics.json",
            ))

    # Sprint names list length check
    stored_names = computed.get("sprint_names", [])
    live_names = live.get("sprint_names", [])
    if len(stored_names) != len(live_names):
        missing = set(live_names) - set(stored_names)
        if missing:
            stale.append(StaleItem(
                metric="sprint_names",
                stored_value=f"{len(stored_names)} entries",
                live_value=f"{len(live_names)} entries (missing: {', '.join(sorted(missing))})",
                source="system-metrics.json",
            ))

    return stale


def scan_docs_for_stale(live: dict) -> list[StaleItem]:
    """Scan whitelisted docs for hardcoded stale metric values."""
    stale = []

    files = []
    for pattern in WHITELIST_GLOBS:
        files.extend(sorted(ROOT.glob(pattern)))

    # Build patterns to look for stale values
    sprints = live.get("sprints_completed")
    total_repos = live.get("total_repos")
    live.get("active_repos")
    essays = live.get("published_essays")

    # Common stale patterns: wrong sprint count, wrong repo count, wrong essay count
    patterns = []
    if sprints is not None:
        # Look for old sprint counts in prose (e.g. "29 sprints completed")
        patterns.append((
            re.compile(r'\b(\d+) sprints? completed\b'),
            "sprints_completed",
            sprints,
        ))
        # Table pattern
        patterns.append((
            re.compile(r'Sprints completed \| (\d+)'),
            "sprints_completed",
            sprints,
        ))

    if total_repos is not None:
        patterns.append((
            re.compile(r'\b(\d+) repositor(?:ies|y) across\b'),
            "total_repos",
            total_repos,
        ))

    if essays is not None:
        patterns.append((
            re.compile(r'\b(\d+)\+? published essays?\b'),
            "published_essays",
            essays,
        ))

    seen = set()
    for filepath in files:
        try:
            content = filepath.read_text()
        except (OSError, UnicodeDecodeError):
            continue

        for line_num, line in enumerate(content.splitlines(), 1):
            for pattern, metric, expected in patterns:
                match = pattern.search(line)
                if match:
                    found_val = int(match.group(1))
                    if found_val != expected:
                        key = (str(filepath), line_num, metric)
                        if key not in seen:
                            seen.add(key)
                            rel_path = filepath.relative_to(ROOT)
                            stale.append(StaleItem(
                                metric=metric,
                                stored_value=str(found_val),
                                live_value=str(expected),
                                source=f"{rel_path}:{line_num}",
                            ))

    return stale


def create_github_issue(stale_items: list[StaleItem]) -> bool:
    """Create a GitHub issue listing stale metrics."""
    lines = ["## Stale Metrics Detected\n"]
    lines.append(f"The stale-detector found **{len(stale_items)} stale value(s)**:\n")
    lines.append("| Metric | Location | Stored | Live |")
    lines.append("|--------|----------|--------|------|")

    for item in stale_items:
        lines.append(f"| {item.metric} | `{item.source}` | {item.stored_value} | {item.live_value} |")

    lines.append("\n### Fix")
    lines.append("Run `python3 scripts/calculate-metrics.py && python3 scripts/propagate-metrics.py` to update.")
    lines.append("\n---")
    lines.append("*Auto-generated by stale-detector.py (SENSORIA sprint)*")

    body = "\n".join(lines)

    try:
        result = subprocess.run(
            ["gh", "issue", "create",
             "--repo", "meta-organvm/organvm-corpvs-testamentvm",
             "--title", "Stale metrics detected",
             "--body", body,
             "--label", "maintenance"],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0:
            print(f"  Issue created: {result.stdout.strip()}")
            return True
        else:
            print(f"  Failed to create issue: {result.stderr.strip()}", file=sys.stderr)
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  Failed to create issue: gh CLI not available", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description="Detect stale metrics")
    parser.add_argument("--fix", action="store_true",
                        help="Auto-fix by running calculate-metrics.py + propagate-metrics.py")
    parser.add_argument("--issue", action="store_true",
                        help="Create GitHub issue if stale metrics found")
    args = parser.parse_args()

    # Load stored metrics
    if not METRICS_FILE.exists():
        print(f"ERROR: {METRICS_FILE} not found. Run calculate-metrics.py first.", file=sys.stderr)
        sys.exit(1)

    with open(METRICS_FILE) as f:
        stored = json.load(f)

    # Compute live metrics
    print("Computing live metrics...")
    live = compute_live_metrics()

    # Compare
    print("Comparing stored vs live...")
    stale_metrics = compare_metrics(stored, live)

    print("Scanning docs for stale values...")
    stale_docs = scan_docs_for_stale(live)

    all_stale = stale_metrics + stale_docs

    if not all_stale:
        print("\nNo staleness detected. All metrics are current.")
        return

    # Report
    print(f"\nFound {len(all_stale)} stale item(s):")
    print(f"  {'Metric':<25} {'Location':<40} {'Stored':<10} {'Live':<10}")
    print(f"  {'─' * 25} {'─' * 40} {'─' * 10} {'─' * 10}")

    for item in all_stale:
        source = item.source[:38] if len(item.source) > 38 else item.source
        stored_v = item.stored_value[:8]
        live_v = item.live_value[:8]
        print(f"  {item.metric:<25} {source:<40} {stored_v:<10} {live_v:<10}")

    if args.fix:
        print("\nAuto-fixing...")
        scripts_dir = ROOT / "scripts"

        r1 = subprocess.run(
            ["python3", str(scripts_dir / "calculate-metrics.py")],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        print(f"  calculate-metrics.py: {'OK' if r1.returncode == 0 else 'FAILED'}")

        r2 = subprocess.run(
            ["python3", str(scripts_dir / "propagate-metrics.py")],
            cwd=str(ROOT), capture_output=True, text=True,
        )
        print(f"  propagate-metrics.py: {'OK' if r2.returncode == 0 else 'FAILED'}")

        if r1.returncode == 0 and r2.returncode == 0:
            print("  Fix applied successfully.")
        else:
            print("  Fix had errors. Check output.", file=sys.stderr)

    elif args.issue:
        create_github_issue(all_stale)
    else:
        print("\nRun with --fix to auto-correct, or --issue to create a GitHub issue.")


if __name__ == "__main__":
    main()
