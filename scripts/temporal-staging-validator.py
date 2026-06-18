#!/usr/bin/env python3
"""Temporal Staging Validator — validate previous state with current rules.

IRF-RES-013 / GH#342 (commission INQ-2026-013, Wave 2).

WHY THIS EXISTS
---------------
The soak collector validates the *current* registry against the *current* rules
and stamps the verdict into the *same* snapshot: current-validates-current. That
is self-reference. The generation that produces a state also certifies it, so the
verdict carries no independent information — it is a fixed point, not a measurement.
This is the Goodhart-Campbell collapse (the measure fuses with the target) and,
formally, a violation of Tarski's undefinability theorem: a language cannot define
its own truth predicate.

Temporal staging restores the metalanguage hierarchy *in time*:

    validator(T)  judges  state(T-1)

The state being judged was frozen *before* the current rules existed, so the
current rules are a strictly higher tier. A PASS is therefore informative again,
and rule drift becomes visible: a state that passed under its own contemporaneous
rules may fail under today's rules — that delta is the signal this tool surfaces.

HOW IT WORKS
------------
The soak collector freezes a `state_capsule` (validation-relevant projection of the
registry + the governance version/digest in force at the time) into every daily
snapshot. This validator:
  1. loads the most recent *prior* snapshot that carries a capsule,
  2. reconstructs a registry-shaped object from that capsule,
  3. runs the *current* validators + *current* governance rules against it,
  4. reports drift, and exits non-zero when previously-valid state now fails.

Usage:
    python3 scripts/temporal-staging-validator.py check [--json] [--strict]
    python3 scripts/temporal-staging-validator.py check --before 2026-06-18
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
REGISTRY_PATH = REPO_ROOT / "repo-registry.json"
GOVERNANCE_PATH = REPO_ROOT / "governance-rules.json"
DATA_DIR = REPO_ROOT / "data" / "soak-test"
REPORT_PATH = DATA_DIR / "temporal-staging-latest.json"

sys.path.insert(0, str(Path(__file__).parent))
from governance_validators import (  # noqa: E402
    project_state,
    reconstruct_registry,
    validate_dependencies,
    validate_registry,
)


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def find_prior_snapshot(before: str | None) -> dict | None:
    """Most recent daily snapshot that carries a state capsule.

    If `before` (a YYYY-MM-DD date) is given, only snapshots strictly before it
    are eligible — this lets the tool stage T-1 even on the same day the current
    snapshot was written. Dry-run snapshots are skipped.
    """
    candidates = []
    for path in sorted(DATA_DIR.glob("daily-*.json")):
        snap = load_json(path)
        if snap.get("dry_run"):
            continue
        if "state_capsule" not in snap:
            continue
        if before and snap.get("date", "") >= before:
            continue
        candidates.append(snap)
    return candidates[-1] if candidates else None


def cmd_check(args) -> int:
    print("=" * 60)
    print("Temporal Staging Validator — validate previous-with-current")
    print("=" * 60)

    governance = load_json(GOVERNANCE_PATH)
    registry = load_json(REGISTRY_PATH)
    current_capsule = project_state(registry, governance)

    prior = find_prior_snapshot(args.before)
    if prior is None:
        print(
            "\nINSUFFICIENT HISTORY — no prior snapshot carries a state_capsule yet.\n"
            "Capsules accumulate from the first collector run after this refactor;\n"
            "temporal staging begins once at least one prior capsule exists."
        )
        report = {
            "verdict": "INSUFFICIENT_HISTORY",
            "checked_at": datetime.now(timezone.utc).isoformat(),
            "prior_snapshot": None,
        }
        _write_report(report)
        # Not a failure: absence of history is expected during bootstrap.
        return 0

    capsule = prior["state_capsule"]
    prior_date = prior.get("date", "?")
    prev_registry = reconstruct_registry(capsule)

    # Apply the CURRENT validators + CURRENT governance to the PREVIOUS state.
    reg_result = validate_registry(prev_registry)
    dep_result = validate_dependencies(prev_registry, governance)
    temporal_pass = reg_result["pass"] and dep_result["pass"]

    # What did that previous snapshot say about itself, under its own
    # contemporaneous rules? (current-validated-current, at T-1)
    prev_self = prior.get("validation", {})
    prev_self_pass = bool(prev_self.get("registry_pass")) and bool(prev_self.get("dependency_pass"))

    # Did the rules themselves change since the snapshot? If so, the check is
    # genuinely independent (current rules differ from when the state was made).
    rules_changed = (
        capsule.get("governance_version") != current_capsule.get("governance_version")
        or capsule.get("governance_digest") != current_capsule.get("governance_digest")
    )

    print(f"\nStaging: validator(now) -> state({prior_date})")
    print(f"  Previous state: {capsule.get('repo_count', '?')} repos, "
          f"governance v{capsule.get('governance_version')}")
    print(f"  Current rules:  governance v{current_capsule.get('governance_version')} "
          f"({'CHANGED' if rules_changed else 'unchanged'} since snapshot)")

    print("\n[1/2] Registry integrity of previous state under current rules...")
    print(f"  Issues: {len(reg_result['issues'])}, Pass: {reg_result['pass']}")
    for issue in reg_result["issues"]:
        print(f"    - {issue}")

    print("\n[2/2] Dependency graph of previous state under current rules...")
    print(f"  Back-edges: {len(dep_result['back_edges'])}, Cycles: {len(dep_result['cycles'])}, "
          f"Depth: {dep_result['max_depth']}/{dep_result['depth_limit']}, Pass: {dep_result['pass']}")
    for be in dep_result["back_edges"]:
        print(f"    - back-edge: {be}")
    for cyc in dep_result["cycles"]:
        print(f"    - cycle: {cyc}")

    # Drift: state that certified itself OK at T-1 but fails today's rules.
    drift = prev_self_pass and not temporal_pass

    verdict = "PASS" if temporal_pass else "FAIL"
    report = {
        "verdict": verdict,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "prior_snapshot": prior_date,
        "rules_changed_since_snapshot": rules_changed,
        "previous_self_verdict": prev_self_pass,
        "temporal_verdict": temporal_pass,
        "rule_drift_detected": drift,
        "registry": reg_result,
        "dependencies": {k: v for k, v in dep_result.items()},
    }
    _write_report(report)

    print("\n" + "=" * 60)
    print(f"Temporal verdict (state {prior_date} under current rules): {verdict}")
    if drift:
        print("RULE DRIFT DETECTED — state passed under its own contemporaneous rules\n"
              "but FAILS under current rules. The two tiers disagree; investigate\n"
              "whether the rules tightened legitimately or the state regressed.")
    elif rules_changed and temporal_pass:
        print("Rules changed since the snapshot and previous state still passes —\n"
              "the validation is genuinely independent and the system is consistent.")
    print("=" * 60)

    if not temporal_pass and args.strict:
        return 1
    if drift:
        return 1
    return 0


def _write_report(report: dict) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=2)
        f.write("\n")
    print(f"\nReport written: {REPORT_PATH}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate previous governance state with current rules (IRF-RES-013)."
    )
    sub = parser.add_subparsers(dest="command")
    check = sub.add_parser("check", help="Validate the most recent prior state under current rules")
    check.add_argument("--json", action="store_true", help="Print the JSON report to stdout")
    check.add_argument("--strict", action="store_true",
                       help="Exit non-zero on any failure, not only on rule drift")
    check.add_argument("--before", metavar="YYYY-MM-DD",
                       help="Only consider snapshots strictly before this date")

    args = parser.parse_args()
    if args.command == "check":
        rc = cmd_check(args)
        if getattr(args, "json", False) and REPORT_PATH.exists():
            print("\n--- report.json ---")
            print(REPORT_PATH.read_text().rstrip())
        return rc
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
