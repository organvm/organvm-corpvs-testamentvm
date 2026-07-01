#!/usr/bin/env python3
"""Apply agent triage results back to prompt-atoms.json.

Reads triage-result-{0..4}.json files and updates atom statuses.
"""

import json
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ATOMS_FILE = SCRIPT_DIR / "prompt-atoms.json"


def main():
    # Load triage results
    results: dict[str, str] = {}
    for i in range(5):
        path = SCRIPT_DIR / f"triage-result-{i}.json"
        if path.exists():
            with open(path) as f:
                batch = json.load(f)
            results.update(batch)
            print(f"Loaded {len(batch)} classifications from {path.name}")
        else:
            print(f"WARNING: {path.name} not found — skipping")

    if not results:
        print("No triage results found. Nothing to apply.")
        sys.exit(1)

    print(f"\nTotal classifications: {len(results)}")
    status_counts = Counter(results.values())
    for s, c in sorted(status_counts.items(), key=lambda x: -x[1]):
        print(f"  {s}: {c}")

    # Load atoms
    print(f"\nLoading {ATOMS_FILE}...")
    with open(ATOMS_FILE) as f:
        atoms = json.load(f)

    # Apply results
    applied = 0
    skipped = 0
    for atom in atoms:
        aid = atom["atom_id"]
        if aid in results and atom["status"] == "UNREVIEWED":
            atom["status"] = results[aid]
            applied += 1
        elif aid in results:
            skipped += 1

    print(f"Applied: {applied}, Skipped (not UNREVIEWED): {skipped}")

    # Write back
    print(f"\nWriting {ATOMS_FILE}...")
    with open(ATOMS_FILE, "w") as f:
        json.dump(atoms, f, separators=(",", ":"))
    print(f"Written. Size: {ATOMS_FILE.stat().st_size / 1024 / 1024:.1f} MB")

    # Final distribution
    final = Counter()
    for a in atoms:
        final[a["status"]] += 1
    print(f"\nFinal status distribution:")
    total = len(atoms)
    for s, c in sorted(final.items(), key=lambda x: -x[1]):
        pct = c / total * 100
        print(f"  {s}: {c} ({pct:.1f}%)")

    remaining = final.get("UNREVIEWED", 0)
    print(f"\nRemaining UNREVIEWED: {remaining}")

    # Cleanup batch files
    for i in range(5):
        for prefix in ("triage-batch-", "triage-result-"):
            path = SCRIPT_DIR / f"{prefix}{i}.json"
            if path.exists():
                path.unlink()
                print(f"Cleaned up {path.name}")


if __name__ == "__main__":
    main()
