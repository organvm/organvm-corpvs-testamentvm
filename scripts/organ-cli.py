#!/usr/bin/env python3
"""Unified CLI for the organvm system — wraps common operations.

Single entry point for registry management, metrics, essay deployment,
soak test status, pulse generation, and governance ID lookup.

Usage:
    python3 scripts/organ-cli.py registry show <repo>
    python3 scripts/organ-cli.py registry validate
    python3 scripts/organ-cli.py registry update <repo> <field> <value>
    python3 scripts/organ-cli.py metrics refresh
    python3 scripts/organ-cli.py invoke <ID> [<ID> ...]
    python3 scripts/organ-cli.py soak status
    python3 scripts/organ-cli.py deploy essay [--dry-run]
    python3 scripts/organ-cli.py pulse
    python3 scripts/organ-cli.py plugin list
    python3 scripts/organ-cli.py plugin run <name> [<plugin-args>...]
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
REGISTRY_PATH = ROOT / "repo-registry.json"
METRICS_PATH = ROOT / "system-metrics.json"
SOAK_DIR = ROOT / "data" / "soak-test"

# Valid values for registry fields
VALID_STATUSES = {"ACTIVE", "PROTOTYPE", "SKELETON", "DESIGN_ONLY", "ARCHIVED"}
VALID_REVENUE_MODELS = {"subscription", "freemium", "one-time", "advertising", "marketplace", "internal", "none"}
VALID_REVENUE_STATUSES = {"pre-launch", "beta", "live", "deprecated", "n/a"}

# Required fields for all repos
REQUIRED_FIELDS = {"name", "org", "implementation_status", "public", "description"}
# Additional required fields for ORGAN-III repos
ORGAN_III_EXTRA = {"type", "revenue_model", "revenue_status"}


# ── Registry helpers ──────────────────────────────────────────────────


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


def save_registry(data: dict):
    # Guard: refuse to write a suspiciously small registry
    repo_count = sum(
        len(organ.get("repositories", []))
        for organ in data.get("organs", {}).values()
        if isinstance(organ, dict)
    )
    if repo_count < 50:
        raise ValueError(
            f"Refusing to write registry with only {repo_count} repos. "
            f"This looks like test/corrupt data."
        )

    # Backup before overwrite
    import shutil
    backup = REGISTRY_PATH.with_suffix(".json.bak")
    if REGISTRY_PATH.exists():
        shutil.copy2(REGISTRY_PATH, backup)

    with open(REGISTRY_PATH, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def find_repo(registry: dict, name: str) -> tuple[str, dict] | None:
    """Find a repo entry by name. Returns (organ_key, repo_dict) or None."""
    for organ_key, organ in registry.get("organs", {}).items():
        for repo in organ.get("repositories", []):
            if repo.get("name") == name:
                return organ_key, repo
    return None


def all_repos(registry: dict):
    """Yield (organ_key, repo_dict) for every repo."""
    for organ_key, organ in registry.get("organs", {}).items():
        for repo in organ.get("repositories", []):
            yield organ_key, repo


# ── Subcommands ───────────────────────────────────────────────────────


def cmd_registry_show(args):
    """Pretty-print a registry entry."""
    registry = load_registry()
    result = find_repo(registry, args.repo)
    if not result:
        print(f"ERROR: Repo '{args.repo}' not found in registry")
        return 1

    organ_key, repo = result
    print(f"\n  {repo['name']}")
    print(f"  {'─' * max(len(repo['name']), 40)}")
    print(f"  Organ:       {organ_key}")
    for key, value in repo.items():
        if key == "name":
            continue
        if isinstance(value, list):
            print(f"  {key + ':':<15}{', '.join(str(v) for v in value)}")
        elif isinstance(value, dict):
            print(f"  {key + ':':<15}{json.dumps(value)}")
        else:
            print(f"  {key + ':':<15}{value}")
    print()
    return 0


def cmd_registry_validate(args):
    """Validate repo-registry.json schema."""
    registry = load_registry()
    errors = []
    warnings = []

    total = 0
    for organ_key, repo in all_repos(registry):
        total += 1
        name = repo.get("name", f"<unnamed in {organ_key}>")

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in repo:
                errors.append(f"{name}: missing required field '{field}'")

        # Check status enum
        status = repo.get("implementation_status")
        if status and status not in VALID_STATUSES:
            errors.append(f"{name}: invalid status '{status}' (valid: {', '.join(sorted(VALID_STATUSES))})")

        # Check ORGAN-III specific fields
        if organ_key == "ORGAN-III":
            for field in ORGAN_III_EXTRA:
                if field not in repo:
                    warnings.append(f"{name}: ORGAN-III repo missing '{field}'")

            rm = repo.get("revenue_model")
            if rm and rm not in VALID_REVENUE_MODELS:
                errors.append(f"{name}: invalid revenue_model '{rm}'")

            rs = repo.get("revenue_status")
            if rs and rs not in VALID_REVENUE_STATUSES:
                errors.append(f"{name}: invalid revenue_status '{rs}'")

        # Check dependencies don't create back-edges (I→II→III only)
        organ_num = {"ORGAN-I": 1, "ORGAN-II": 2, "ORGAN-III": 3}.get(organ_key)
        for dep in repo.get("dependencies", []):
            dep_result = find_repo(registry, dep)
            if dep_result:
                dep_organ = dep_result[0]
                dep_num = {"ORGAN-I": 1, "ORGAN-II": 2, "ORGAN-III": 3}.get(dep_organ)
                if organ_num and dep_num and dep_num > organ_num:
                    errors.append(f"{name}: back-edge dependency on {dep} ({organ_key} → {dep_organ})")

    # Check counts
    organs = registry.get("organs", {})
    declared_total = registry.get("total_repos")
    if declared_total and declared_total != total:
        warnings.append(f"total_repos declares {declared_total} but found {total}")

    for organ_key, organ in organs.items():
        declared = organ.get("repository_count")
        actual = len(organ.get("repositories", []))
        if declared and declared != actual:
            warnings.append(f"{organ_key}: repository_count={declared} but found {actual}")

    # Report
    print(f"\nRegistry Validation: {total} repos checked")
    print("─" * 40)

    if errors:
        print(f"\nERRORS ({len(errors)}):")
        for e in errors:
            print(f"  ✗ {e}")

    if warnings:
        print(f"\nWARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  ⚠ {w}")

    if not errors and not warnings:
        print("  All checks passed.")

    print()
    return 1 if errors else 0


def cmd_registry_update(args):
    """Update a field in a registry entry."""
    registry = load_registry()
    result = find_repo(registry, args.repo)
    if not result:
        print(f"ERROR: Repo '{args.repo}' not found in registry")
        return 1

    organ_key, repo = result
    old_value = repo.get(args.field, "<unset>")

    # Type coercion
    value = args.value
    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    elif value.isdigit():
        value = int(value)

    repo[args.field] = value
    print(f"  {args.repo}.{args.field}: {old_value} → {value}")

    # Validate before saving
    if args.field == "implementation_status" and value not in VALID_STATUSES:
        print(f"ERROR: Invalid status '{value}'")
        return 1

    save_registry(registry)
    print("  Registry saved.")
    return 0


def cmd_metrics_refresh(args):
    """Run calculate-metrics → propagate-metrics pipeline."""
    print("Running calculate-metrics.py...")
    r1 = subprocess.run(
        [sys.executable, str(SCRIPTS / "calculate-metrics.py")],
        cwd=str(ROOT),
    )
    if r1.returncode != 0:
        print("ERROR: calculate-metrics.py failed")
        return 1

    print("\nRunning propagate-metrics.py...")
    r2 = subprocess.run(
        [sys.executable, str(SCRIPTS / "propagate-metrics.py")],
        cwd=str(ROOT),
    )
    if r2.returncode != 0:
        print("ERROR: propagate-metrics.py failed")
        return 1

    print("\nMetrics refreshed successfully.")
    return 0


def cmd_invoke(args):
    """Wrapper around invoke.py."""
    cmd = [sys.executable, str(SCRIPTS / "invoke.py")] + args.ids
    return subprocess.run(cmd, cwd=str(ROOT)).returncode


def cmd_soak_status(args):
    """Show latest soak test snapshot + VIGILIA timer."""
    snapshots = sorted(SOAK_DIR.glob("daily-*.json"))

    if not snapshots:
        print("No soak test data found.")
        return 1

    # Load latest
    latest_path = snapshots[-1]
    with open(latest_path) as f:
        data = json.load(f)

    date = data.get("date", latest_path.stem.replace("daily-", ""))
    dry_run = data.get("dry_run", False)

    print("\nSoak Test Status")
    print("─" * 40)
    print(f"  Latest snapshot:  {date} {'(dry-run)' if dry_run else ''}")
    print(f"  Total snapshots:  {len(snapshots)}")

    # Non-dry-run count
    real = sum(1 for p in snapshots if not load_json_quick(p).get("dry_run", True))
    print(f"  Real data points: {real}")

    # VIGILIA timer (30 days from 2026-02-16)
    soak_start = datetime(2026, 2, 16, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    elapsed = (now - soak_start).days
    remaining = max(0, 30 - elapsed)
    pct = min(100, int(elapsed / 30 * 100))
    bar = "█" * (pct // 5) + "░" * (20 - pct // 5)
    print(f"\n  VIGILIA: Day {elapsed}/30 ({pct}%)")
    print(f"  [{bar}] {remaining} days remaining")

    # Validation summary
    val = data.get("validation", {})
    print(f"\n  Registry:    {'PASS' if val.get('registry_pass') else 'FAIL'}")
    print(f"  Dependencies:{'PASS' if val.get('dependency_pass') else 'FAIL'}")

    # CI summary
    ci = data.get("ci", {})
    if ci.get("total_checked", 0) > 0:
        print(f"\n  CI: {ci['passing']}/{ci['total_checked']} passing")
    else:
        print("\n  CI: awaiting first real data point")

    print()
    return 0


def load_json_quick(path):
    """Load JSON, return empty dict on error."""
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return {}


def cmd_deploy_essay(args):
    """Wrapper around essay-deploy.py."""
    cmd = [sys.executable, str(SCRIPTS / "essay-deploy.py")]
    if not args.dry_run:
        cmd.append("--deploy")
    cmd.append("--verbose")
    return subprocess.run(cmd, cwd=str(ROOT)).returncode


def cmd_pulse(args):
    """Wrapper around system-pulse-generator.py."""
    cmd = [sys.executable, str(SCRIPTS / "system-pulse-generator.py"), "--skip-api"]
    return subprocess.run(cmd, cwd=str(ROOT)).returncode


# ── Plugin registry ───────────────────────────────────────────────────
# Maps the kebab-case plugin name (as users type it) to the module under
# scripts/plugins/. Each module exposes a `run(argv)` callable returning
# an int exit code. New meta-plugins land here. See IRF-SYS-184.

PLUGINS = {
    "session-orchestrator": "session_orchestrator",
    "vacuum-radar": "vacuum_radar",
    "triple-reference-tracker": "triple_reference_tracker",
    "atom-logger": "atom_logger",
}


def cmd_plugin_list(args):
    """List registered meta-plugins."""
    print("\nRegistered meta-plugins:\n")
    for name, module in PLUGINS.items():
        print(f"  {name:<28} scripts/plugins/{module}.py")
    print()
    return 0


def cmd_plugin_run(args):
    """Dispatch to a registered plugin's run(argv) entry point."""
    module_name = PLUGINS.get(args.plugin_name)
    if not module_name:
        print(f"ERROR: unknown plugin '{args.plugin_name}'. Known: {', '.join(sorted(PLUGINS))}",
              file=sys.stderr)
        return 2
    import importlib
    sys.path.insert(0, str(SCRIPTS))
    mod = importlib.import_module(f"plugins.{module_name}")
    return mod.run(args.plugin_args)


# ── CLI argument parsing ──────────────────────────────────────────────


def build_parser():
    parser = argparse.ArgumentParser(
        prog="organ-cli",
        description="Unified CLI for the organvm system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    # registry
    reg = sub.add_parser("registry", help="Registry operations")
    reg_sub = reg.add_subparsers(dest="registry_command")

    show = reg_sub.add_parser("show", help="Show a registry entry")
    show.add_argument("repo", help="Repository name")

    reg_sub.add_parser("validate", help="Validate registry schema")

    update = reg_sub.add_parser("update", help="Update a registry field")
    update.add_argument("repo", help="Repository name")
    update.add_argument("field", help="Field to update")
    update.add_argument("value", help="New value")

    # metrics
    sub.add_parser("metrics", help="Refresh metrics (calculate + propagate)")

    # invoke
    inv = sub.add_parser("invoke", help="Look up governance IDs")
    inv.add_argument("ids", nargs="+", help="IDs to look up")

    # soak
    soak = sub.add_parser("soak", help="Soak test operations")
    soak_sub = soak.add_subparsers(dest="soak_command")
    soak_sub.add_parser("status", help="Show soak test status + VIGILIA timer")

    # deploy
    dep = sub.add_parser("deploy", help="Deploy operations")
    dep_sub = dep.add_subparsers(dest="deploy_command")
    essay = dep_sub.add_parser("essay", help="Deploy essays to public-process")
    essay.add_argument("--dry-run", action="store_true", default=True,
                       help="Preview only (default)")
    essay.add_argument("--execute", action="store_true",
                       help="Actually deploy essays")

    # pulse
    sub.add_parser("pulse", help="Generate system pulse report")

    # plugin
    plg = sub.add_parser("plugin", help="Meta-plugin operations (IRF-SYS-184)")
    plg_sub = plg.add_subparsers(dest="plugin_command")
    plg_sub.add_parser("list", help="List registered meta-plugins")
    run_p = plg_sub.add_parser("run", help="Run a meta-plugin by name")
    run_p.add_argument("plugin_name", help="plugin name (kebab-case)")
    run_p.add_argument("plugin_args", nargs=argparse.REMAINDER,
                       help="arguments forwarded to the plugin")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "registry":
        if args.registry_command == "show":
            return cmd_registry_show(args)
        elif args.registry_command == "validate":
            return cmd_registry_validate(args)
        elif args.registry_command == "update":
            return cmd_registry_update(args)
        else:
            parser.parse_args(["registry", "--help"])
            return 0

    elif args.command == "metrics":
        return cmd_metrics_refresh(args)

    elif args.command == "invoke":
        return cmd_invoke(args)

    elif args.command == "soak":
        if args.soak_command == "status":
            return cmd_soak_status(args)
        else:
            parser.parse_args(["soak", "--help"])
            return 0

    elif args.command == "deploy":
        if args.deploy_command == "essay":
            if hasattr(args, "execute") and args.execute:
                args.dry_run = False
            return cmd_deploy_essay(args)
        else:
            parser.parse_args(["deploy", "--help"])
            return 0

    elif args.command == "pulse":
        return cmd_pulse(args)

    elif args.command == "plugin":
        if args.plugin_command == "list":
            return cmd_plugin_list(args)
        elif args.plugin_command == "run":
            return cmd_plugin_run(args)
        else:
            parser.parse_args(["plugin", "--help"])
            return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())
