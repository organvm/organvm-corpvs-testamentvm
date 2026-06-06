#!/usr/bin/env python3
"""Organ Audit — Full system health check across all eight organs.

Reads repo-registry.json and governance-rules.json, validates:
1. Every organ has minimum repo count
2. All repos have required fields and documentation
3. Dependency graph: no cycles, no back-edges, targets exist
4. ORGAN-V essay count meets threshold
5. Stale repos (no update in 90+ days)
6. CI/CD coverage
7. Implementation status distribution

Outputs: Markdown audit report + JSON metrics.
Exit code: 1 if critical alerts, 0 otherwise.

Usage:
    python3 scripts/organ-audit.py \
        --registry repo-registry.json \
        --governance governance-rules.json \
        --output audit-report.md \
        [--metrics metrics.json] \
        [--github]  # Enable GitHub API checks (README existence, CI workflow)
"""

import argparse
import json
import subprocess
import sys
import time
from collections import defaultdict

# ISOTOPE DISSOLUTION: Gate memory--remember G2 (CORPUS_SCRIPTS_DISSOLVED)
try:
    from organvm_engine.registry.loader import load_registry as _engine_load
except ImportError:
    _engine_load = None
from datetime import datetime, timezone
from pathlib import Path


def check_file_on_github(org: str, repo: str, path: str) -> bool:
    """Check if a file exists on GitHub via gh CLI."""
    result = subprocess.run(
        ["gh", "api", f"/repos/{org}/{repo}/contents/{path}"],
        capture_output=True, text=True
    )
    return result.returncode == 0


def build_repo_map(registry: dict) -> tuple[dict, list]:
    """Build repo lookup and flat list from registry organs."""
    repo_map = {}
    all_repos = []
    for organ_key, organ_data in registry.get("organs", {}).items():
        for repo in organ_data.get("repositories", []):
            key = f"{repo['org']}/{repo['name']}"
            repo["_organ_key"] = organ_key
            repo_map[key] = repo
            all_repos.append(repo)
    return repo_map, all_repos


def validate_dependency_graph(repo_map: dict, all_repos: list, governance: dict) -> tuple[list, dict]:
    """Validate the full dependency graph. Returns (report_lines, alerts)."""
    report = ["\n## Dependency Validation\n"]
    alerts = {"critical": [], "warning": []}

    organ_levels = {
        "organvm-i-theoria": 1,
        "organvm-ii-poiesis": 2,
        "organvm-iii-ergon": 3,
        "organvm-iv-taxis": 4,
        "organvm-v-logos": 5,
        "organvm-vi-koinonia": 6,
        "organvm-vii-kerygma": 7,
        "meta-organvm": 8,
    }
    restricted = {1, 2, 3}

    deps = []
    for repo in all_repos:
        key = f"{repo['org']}/{repo['name']}"
        for dep in repo.get("dependencies", []):
            deps.append((key, dep))

    report.append(f"Total dependency edges: {len(deps)}\n")

    # Check 1: All targets exist
    missing = [(f, t) for f, t in deps if t not in repo_map]
    if missing:
        for f, t in missing:
            alerts["warning"].append(f"Dependency target missing: {f} -> {t}")
        report.append(f"- Missing targets: {len(missing)}\n")

    # Check 2: No self-deps
    self_deps = [(f, t) for f, t in deps if f == t]
    if self_deps:
        for f, _ in self_deps:
            alerts["warning"].append(f"Self-dependency: {f}")

    # Check 3: No back-edges in I->II->III
    back_edges = []
    for from_key, to_key in deps:
        from_org = from_key.split("/")[0]
        to_org = to_key.split("/")[0]
        from_level = organ_levels.get(from_org)
        to_level = organ_levels.get(to_org)
        if from_level and to_level:
            if from_level in restricted and to_level in restricted:
                if from_level < to_level:
                    back_edges.append((from_key, to_key))

    if back_edges:
        for f, t in back_edges:
            alerts["critical"].append(f"Back-edge violation: {f} -> {t}")
        report.append(f"- Back-edge violations: {len(back_edges)}\n")
    else:
        report.append("- Back-edges: 0 (PASS)\n")

    # Check 4: No circular dependencies (DFS)
    adj = defaultdict(list)
    for f, t in deps:
        adj[f].append(t)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(lambda: WHITE)
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)
        for neighbor in adj[node]:
            if color[neighbor] == GRAY:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
            elif color[neighbor] == WHITE:
                dfs(neighbor, path)
        path.pop()
        color[node] = BLACK

    for node in list(repo_map.keys()):
        if color[node] == WHITE:
            dfs(node, [])

    if cycles:
        for cycle in cycles:
            alerts["critical"].append(f"Circular dependency: {' -> '.join(cycle)}")
        report.append(f"- Circular dependencies: {len(cycles)}\n")
    else:
        report.append("- Circular dependencies: 0 (PASS)\n")

    # Check 5: Transitive depth
    max_depth = governance.get("dependency_rules", {}).get("max_transitive_depth", 4)

    def measure_depth(node, visited=None):
        if visited is None:
            visited = set()
        if node in visited:
            return 0
        visited.add(node)
        if not adj[node]:
            return 0
        return 1 + max(measure_depth(n, visited) for n in adj[node])

    deepest = 0
    deepest_node = ""
    for node in repo_map:
        d = measure_depth(node)
        if d > deepest:
            deepest = d
            deepest_node = node

    if deepest > max_depth:
        alerts["warning"].append(f"Transitive depth {deepest} exceeds limit {max_depth} at {deepest_node}")
    report.append(f"- Max transitive depth: {deepest} (limit: {max_depth})\n")

    return report, alerts


def audit_organ(organ_key: str, organ_data: dict, governance: dict,
                enable_github: bool) -> tuple[list, dict]:
    """Audit a single organ. Returns (report_lines, alerts)."""
    report = []
    alerts = {"critical": [], "warning": []}

    repos = organ_data.get("repositories", [])
    name = organ_data.get("name", organ_key)
    status = organ_data.get("launch_status", "UNKNOWN")
    completion = organ_data.get("completion", "N/A")

    report.append(f"\n## {organ_key}: {name}\n")
    report.append(f"**Status:** {status}\n")
    report.append(f"**Completion:** {completion}\n")
    report.append(f"**Repos:** {len(repos)}\n")

    # Organ-level requirements
    organ_reqs = governance.get("organ_requirements", {}).get(organ_key, {})
    min_repos = organ_reqs.get("min_repos", 1)

    if len(repos) < min_repos:
        alerts["critical"].append(f"{organ_key} has {len(repos)} repos (min: {min_repos})")
        report.append(f"- CRITICAL: Below minimum repo count ({len(repos)} < {min_repos})\n")

    # Per-repo checks
    stale_threshold = governance.get("audit_thresholds", {}).get("warning", {}).get("stale_repo_days", 90)
    now = datetime.now(timezone.utc)

    for repo in repos:
        org = repo.get("org", "")
        repo_name = repo.get("name", "")
        full = f"{org}/{repo_name}"

        # Documentation status
        doc_status = repo.get("documentation_status", "")
        if doc_status in ("EMPTY", ""):
            alerts["warning"].append(f"Missing documentation: {full}")

        # Staleness check
        last_validated = repo.get("last_validated", "")
        if last_validated:
            try:
                last_dt = datetime.fromisoformat(last_validated.replace("Z", "+00:00"))
                age_days = (now - last_dt).days
                if age_days > stale_threshold:
                    alerts["warning"].append(f"Stale repo ({age_days}d since validation): {full}")
            except (ValueError, TypeError):
                pass

        # CI workflow field
        if not repo.get("ci_workflow"):
            alerts["warning"].append(f"No CI workflow configured: {full}")

        # GitHub-level checks (expensive, optional)
        if enable_github:
            if not check_file_on_github(org, repo_name, "README.md"):
                alerts["critical"].append(f"Missing README on GitHub: {full}")
            time.sleep(0.3)

    # Organ-specific checks
    if organ_key == "ORGAN-III":
        for repo in repos:
            if not repo.get("type"):
                alerts["warning"].append(
                    f"ORGAN-III repo missing 'type' field: {repo.get('org')}/{repo.get('name')}"
                )

    if organ_key == "ORGAN-V":
        min_essays = organ_reqs.get("min_essays", 10)
        if enable_github:
            result = subprocess.run(
                ["gh", "api", "/repos/organvm-v-logos/public-process/contents/essays/meta-system"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                essays = [f for f in data if f["name"].endswith(".md")]
                essay_count = len(essays)
                report.append(f"**Essays found:** {essay_count} (target: {min_essays})\n")
                if essay_count < min_essays:
                    alerts["warning"].append(
                        f"ORGAN-V has {essay_count} essays (target: {min_essays})"
                    )
            else:
                alerts["warning"].append("Could not fetch ORGAN-V essay count from GitHub")

    # Status distribution for this organ
    statuses = defaultdict(int)
    for repo in repos:
        s = repo.get("implementation_status", "UNKNOWN")
        statuses[s] += 1

    report.append("\n**Implementation status:**\n")
    for s in ["PRODUCTION", "PROTOTYPE", "SKELETON", "DESIGN_ONLY", "UNKNOWN"]:
        if statuses[s]:
            report.append(f"- {s}: {statuses[s]}\n")

    return report, alerts


def calculate_metrics(registry: dict, all_repos: list, alerts: dict) -> dict:
    """Calculate system-wide metrics for the audit."""
    organs = registry.get("organs", {})
    operational = sum(
        1 for o in organs.values()
        if o.get("launch_status") == "OPERATIONAL"
    )

    status_dist = defaultdict(int)
    tier_dist = defaultdict(int)
    promotion_dist = defaultdict(int)
    ci_count = 0
    platinum_count = 0

    for repo in all_repos:
        status_dist[repo.get("implementation_status", "UNKNOWN")] += 1
        tier_dist[repo.get("tier", "unknown")] += 1
        promotion_dist[repo.get("promotion_status", "UNKNOWN")] += 1
        if repo.get("ci_workflow"):
            ci_count += 1
        if repo.get("platinum_status"):
            platinum_count += 1

    return {
        "audit_date": datetime.now(timezone.utc).isoformat(),
        "total_repos": len(all_repos),
        "total_organs": len(organs),
        "operational_organs": operational,
        "critical_alerts": len(alerts["critical"]),
        "warnings": len(alerts["warning"]),
        "completion": round(operational / max(len(organs), 1) * 100, 1),
        "implementation_status": dict(status_dist),
        "tier_distribution": dict(tier_dist),
        "promotion_status": dict(promotion_dist),
        "ci_coverage": ci_count,
        "platinum_repos": platinum_count,
    }


def main():
    parser = argparse.ArgumentParser(description="Organ Audit — full system health check")
    parser.add_argument("--registry", required=True, help="Path to repo-registry.json")
    parser.add_argument("--governance", required=True, help="Path to governance-rules.json")
    parser.add_argument("--output", required=True, help="Path for Markdown audit report")
    parser.add_argument("--metrics", default=None, help="Path for JSON metrics output")
    parser.add_argument("--github", action="store_true", help="Enable GitHub API checks (slower)")
    args = parser.parse_args()

    if _engine_load is not None:
        registry = _engine_load(args.registry)
    else:
        with open(args.registry) as f:
            registry = json.load(f)
    with open(args.governance) as f:
        governance = json.load(f)

    repo_map, all_repos = build_repo_map(registry)

    report = []
    all_alerts = {"critical": [], "warning": []}

    report.append(f"# Monthly Organ Audit — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}\n")
    report.append(f"**Registry version:** {registry.get('version', '?')}\n")
    report.append(f"**Total repos:** {len(all_repos)}\n")
    report.append(f"**GitHub checks:** {'enabled' if args.github else 'disabled'}\n")

    # Audit each organ
    organ_order = [
        "ORGAN-I", "ORGAN-II", "ORGAN-III", "ORGAN-IV",
        "ORGAN-V", "ORGAN-VI", "ORGAN-VII"
    ]
    for organ_key in organ_order:
        organ_data = registry.get("organs", {}).get(organ_key, {})
        if not organ_data:
            all_alerts["critical"].append(f"Organ {organ_key} missing from registry")
            report.append(f"\n## {organ_key}: MISSING FROM REGISTRY\n")
            continue

        organ_report, organ_alerts = audit_organ(
            organ_key, organ_data, governance, args.github
        )
        report.extend(organ_report)
        all_alerts["critical"].extend(organ_alerts["critical"])
        all_alerts["warning"].extend(organ_alerts["warning"])

    # Check Meta organ separately
    meta = registry.get("organs", {}).get("META", registry.get("organs", {}).get("meta-organvm", {}))
    if meta:
        report.append(f"\n## Meta Organ\n")
        report.append(f"**Status:** {meta.get('launch_status', 'N/A')}\n")
        meta_repos = meta.get("repositories", [])
        report.append(f"**Repos:** {len(meta_repos)}\n")

    # Dependency validation
    dep_report, dep_alerts = validate_dependency_graph(repo_map, all_repos, governance)
    report.extend(dep_report)
    all_alerts["critical"].extend(dep_alerts["critical"])
    all_alerts["warning"].extend(dep_alerts["warning"])

    # Alerts summary
    report.append("\n## Alerts\n")
    if all_alerts["critical"]:
        report.append(f"### Critical ({len(all_alerts['critical'])})\n")
        for alert in all_alerts["critical"]:
            report.append(f"- {alert}\n")
    else:
        report.append("### Critical: 0\n")

    if all_alerts["warning"]:
        report.append(f"\n### Warnings ({len(all_alerts['warning'])})\n")
        for alert in all_alerts["warning"]:
            report.append(f"- {alert}\n")
    else:
        report.append("\n### Warnings: 0\n")

    # Write report
    report_text = "".join(report)
    with open(args.output, "w") as f:
        f.write(report_text)
    print(f"Audit report written to {args.output}")

    # Calculate and write metrics
    metrics = calculate_metrics(registry, all_repos, all_alerts)
    if args.metrics:
        with open(args.metrics, "w") as f:
            json.dump(metrics, f, indent=2)
        print(f"Metrics written to {args.metrics}")

    # Print summary
    print(f"\n{'=' * 60}")
    print("AUDIT SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total repos: {metrics['total_repos']}")
    print(f"Operational organs: {metrics['operational_organs']}/{metrics['total_organs']}")
    print(f"Critical alerts: {metrics['critical_alerts']}")
    print(f"Warnings: {metrics['warnings']}")
    print(f"CI coverage: {metrics['ci_coverage']}/{metrics['total_repos']}")
    print(f"Platinum repos: {metrics['platinum_repos']}")

    if all_alerts["critical"]:
        print(f"\nCRITICAL ALERTS:")
        for a in all_alerts["critical"]:
            print(f"  - {a}")
        return 1

    if all_alerts["warning"]:
        print(f"\nWARNINGS (non-blocking):")
        for a in all_alerts["warning"][:10]:
            print(f"  - {a}")
        if len(all_alerts["warning"]) > 10:
            print(f"  ... and {len(all_alerts['warning']) - 10} more")

    print("\nAUDIT PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
