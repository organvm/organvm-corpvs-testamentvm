#!/usr/bin/env python3
"""Reopen aggressively-closed atoms that score P0/P1.

The triage pipeline closed atoms on weak heuristics:
  - CLOSED-INFERRED: universe >75% done → assumed done (723 at P1+)
  - CLOSED-STALE: >90 days old (69 at P1+)
  - CLOSED-SIGNAL: implicit signal (47 at P1+)
  - CLOSED-CONTEXT: "contextual" but may contain embedded directives (906 at P1+)
  - CLOSED-QUESTION: "decided" but may be unresolved (499 at P1+)

This script reopens atoms where:
  1. Priority score >= threshold (P0 or P1)
  2. Closure reason was a weak heuristic
  3. Content passes actionability filter (for CONTEXT/QUESTION types)

Usage:
    python3 reopen_atoms.py [--dry-run]
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ATOMS_PATH = SCRIPT_DIR / "prompt-atoms.json"

# Closure types that used weak heuristics — always reopen if high priority
WEAK_CLOSURES = {"CLOSED-INFERRED", "CLOSED-STALE", "CLOSED-SIGNAL"}

# Closure types that need content filtering before reopening
FILTERED_CLOSURES = {"CLOSED-CONTEXT", "CLOSED-QUESTION"}

# Never reopen regardless of priority
HARD_CLOSURES = {"CLOSED-NAV", "CLOSED-COMMAND", "CLOSED-DATA"}

# Minimum priority score to consider reopening
MIN_SCORE_REOPEN = 0.50  # P1 threshold

# Patterns that indicate NON-actionable content (skip these)
NON_ACTIONABLE = re.compile(
    r"^(ok|yes|proceed|continue|got it|understood|noted|sounds good|"
    r"let's do|moving on|next|done|right|sure|agreed|perfect|great|"
    r"<task-notification>|<command-name>)",
    re.I,
)

# Patterns that indicate actionable content (include these)
ACTIONABLE_SIGNALS = [
    re.compile(r"\b(implement|create|build|fix|repair|add|remove|deploy|configure|migrate)\b", re.I),
    re.compile(r"\b(missing|broken|stale|vacuum|gap|need|must|should|required)\b", re.I),
    re.compile(r"\b(IRF-|ATM-|SPEC-|SOP-|DONE-)\w+", re.I),
    re.compile(r"[~/.][\w/.-]+\.\w{1,5}"),  # file paths
    re.compile(r"\bhttps?://\S+"),  # URLs
]

# Minimum content length for actionability
MIN_CONTENT_LEN = 40


def is_actionable(content: str) -> bool:
    """Check if content contains actionable work despite CLOSED status."""
    content = content.strip()

    # Too short = not actionable
    if len(content) < MIN_CONTENT_LEN:
        return False

    # Starts with non-actionable pattern
    if NON_ACTIONABLE.match(content):
        return False

    # Contains task notification XML = not actionable (system noise)
    if "<task-notification>" in content or "<task-id>" in content:
        return False

    # Check for actionable signals
    signal_count = sum(1 for p in ACTIONABLE_SIGNALS if p.search(content))
    return signal_count >= 1


def main() -> None:
    dry_run = "--dry-run" in sys.argv

    if not ATOMS_PATH.exists():
        print(f"ERROR: {ATOMS_PATH} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {ATOMS_PATH}...")
    with open(ATOMS_PATH) as f:
        atoms = json.load(f)

    reopened = 0
    skipped = 0
    by_reason: Counter[str] = Counter()
    by_old_status: Counter[str] = Counter()

    for atom in atoms:
        status = atom.get("status", "")
        score = atom.get("priority_score", 0.0)
        priority = atom.get("priority", 99)

        # Only consider CLOSED atoms at P0/P1
        if not status.startswith("CLOSED"):
            continue
        if score < MIN_SCORE_REOPEN:
            continue

        # Hard closures: never reopen
        if status in HARD_CLOSURES:
            skipped += 1
            by_reason["hard_closure"] += 1
            continue

        # Weak closures: always reopen at P0/P1
        if status in WEAK_CLOSURES:
            atom["status"] = "OPEN"
            atom["produced"] = atom.get("produced", []) + [f"reopened-from-{status}"]
            reopened += 1
            by_old_status[status] += 1
            continue

        # Filtered closures: check content actionability
        if status in FILTERED_CLOSURES:
            content = atom.get("content", "")
            if is_actionable(content):
                atom["status"] = "OPEN"
                atom["produced"] = atom.get("produced", []) + [f"reopened-from-{status}"]
                reopened += 1
                by_old_status[status] += 1
            else:
                skipped += 1
                by_reason["not_actionable"] += 1
            continue

        # Unknown closure type: skip
        skipped += 1
        by_reason["unknown_type"] += 1

    # Count final state
    open_count = sum(1 for a in atoms if a.get("status") == "OPEN")

    print(f"\nReopened: {reopened}")
    print(f"Skipped:  {skipped}")
    print(f"\nBy old status:")
    for st, count in by_old_status.most_common():
        print(f"  {st}: {count}")
    print(f"\nSkip reasons:")
    for reason, count in by_reason.most_common():
        print(f"  {reason}: {count}")
    print(f"\nTotal OPEN atoms now: {open_count}")

    if dry_run:
        print("\n[DRY RUN] No changes written.")
    else:
        print(f"\nWriting {ATOMS_PATH}...")
        with open(ATOMS_PATH, "w") as f:
            json.dump(atoms, f, indent=1)
        print("Done.")


if __name__ == "__main__":
    main()
