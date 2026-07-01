#!/usr/bin/env python3
"""Quick status dashboard for the prompt atom registry."""

import json
from pathlib import Path

ATOMS_FILE = Path(__file__).parent / "prompt-atoms.json"


def main():
    atoms = json.loads(ATOMS_FILE.read_text(encoding="utf-8"))
    total = len(atoms)

    # Status counts
    status_counts: dict[str, int] = {}
    for a in atoms:
        s = a.get("status", "UNKNOWN")
        status_counts[s] = status_counts.get(s, 0) + 1

    done = status_counts.get("DONE", 0)
    open_ = status_counts.get("OPEN", 0)
    unreviewed = status_counts.get("UNREVIEWED", 0)
    na = status_counts.get("N/A", 0)

    print("=" * 60)
    print("  ORGANVM Prompt Atom Status")
    print("=" * 60)
    print(f"\n  Total atoms:  {total:,}")
    print(f"  DONE:         {done:,} ({done/total*100:.1f}%)")
    print(f"  OPEN:         {open_:,} ({open_/total*100:.1f}%)")
    print(f"  UNREVIEWED:   {unreviewed:,} ({unreviewed/total*100:.1f}%)")
    print(f"  N/A:          {na:,}")

    # Top 10 OPEN directives
    open_directives = [a for a in atoms if a["status"] == "OPEN" and a["type"] == "directive"]
    # Sort: BACKLOG items first (they have priority), then by date
    open_directives.sort(key=lambda a: (
        0 if a["atom_id"].startswith("BACKLOG") else 1,
        a.get("date", "9999"),
    ))

    print(f"\n{'─' * 60}")
    print(f"  Top OPEN Directives ({len(open_directives)} total)")
    print(f"{'─' * 60}")
    for a in open_directives[:15]:
        universes = ", ".join(a.get("universes", [])[:3])
        summary = a["summary"][:70]
        print(f"  {a['atom_id']:15s} [{a.get('date','')}] ({universes})")
        print(f"                  {summary}")

    # By source
    source_counts: dict[str, dict[str, int]] = {}
    for a in atoms:
        src = a.get("source", "unknown")
        s = a.get("status", "UNKNOWN")
        if src not in source_counts:
            source_counts[src] = {}
        source_counts[src][s] = source_counts[src].get(s, 0) + 1

    print(f"\n{'─' * 60}")
    print("  By Source")
    print(f"{'─' * 60}")
    print(f"  {'Source':<25s} {'Total':>7s} {'DONE':>7s} {'OPEN':>7s} {'UNREV':>7s}")
    for src in sorted(source_counts.keys()):
        counts = source_counts[src]
        t = sum(counts.values())
        d = counts.get("DONE", 0)
        o = counts.get("OPEN", 0)
        u = counts.get("UNREVIEWED", 0)
        print(f"  {src:<25s} {t:>7,d} {d:>7,d} {o:>7,d} {u:>7,d}")

    # By universe (top 10)
    universe_counts: dict[str, int] = {}
    for a in atoms:
        for u in a.get("universes", []):
            universe_counts[u] = universe_counts.get(u, 0) + 1

    print(f"\n{'─' * 60}")
    print("  By Universe (top 15)")
    print(f"{'─' * 60}")
    for u, c in sorted(universe_counts.items(), key=lambda x: -x[1])[:15]:
        print(f"  {u:<25s} {c:>7,d}")

    print(f"\n{'═' * 60}")


if __name__ == "__main__":
    main()
