#!/usr/bin/env python3
"""Generate prioritized work queue from prompt atoms.

Reads prompt-atoms.json, filters to OPEN atoms, sorts by priority,
and outputs WORK-QUEUE.md (human-readable) + open-atoms-cache.json (lightweight).
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ATOMS_FILE = SCRIPT_DIR / "prompt-atoms.json"
WORK_QUEUE_MD = SCRIPT_DIR / "WORK-QUEUE.md"
CACHE_FILE = SCRIPT_DIR / "open-atoms-cache.json"


def parse_priority(atom: dict) -> int:
    """Read computed priority from atom, falling back to type-based default.

    Priority is computed by prioritize_atoms.py across the full corpus.
    The 'priority' field (0-3) is written directly into prompt-atoms.json.
    """
    # Use pre-computed priority if available (set by prioritize_atoms.py)
    if "priority" in atom:
        return atom["priority"]

    # Fallback for atoms not yet scored
    atom_id = atom.get("atom_id", "")
    content = atom.get("content", "")

    if atom_id.startswith("BACKLOG"):
        if "[P0]" in content:
            return 0
        if "[P1]" in content:
            return 1
        if "[P2]" in content:
            return 2
        if "[P3]" in content:
            return 3
        return 1

    type_priority = {
        "correction": 1,
        "governance-rule": 2,
        "constraint": 2,
        "directive": 3,
    }
    return type_priority.get(atom.get("type", ""), 3)


def parse_date(atom: dict) -> str:
    """Extract date string for sorting. Returns empty string if missing."""
    return atom.get("date", "") or ""


def cluster_by_universe(atoms: list[dict]) -> dict[str, list[dict]]:
    """Group atoms by their primary universe."""
    clusters: dict[str, list[dict]] = {}
    for atom in atoms:
        universes = atom.get("universes", [])
        primary = universes[0] if universes else "unscoped"
        clusters.setdefault(primary, []).append(atom)
    return clusters


def truncate(text: str, length: int = 120) -> str:
    """Truncate text to length, adding ellipsis if needed."""
    text = text.replace("\n", " ").strip()
    if len(text) <= length:
        return text
    return text[:length - 3] + "..."


def generate_work_queue() -> None:
    if not ATOMS_FILE.exists():
        print(f"ERROR: {ATOMS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {ATOMS_FILE}...")
    with open(ATOMS_FILE) as f:
        atoms = json.load(f)

    # Filter to OPEN atoms
    open_atoms = [a for a in atoms if a.get("status") == "OPEN"]
    print(f"Found {len(open_atoms)} OPEN atoms out of {len(atoms)} total")

    if not open_atoms:
        print("No OPEN atoms found.")
        WORK_QUEUE_MD.write_text("# Work Queue\n\nNo OPEN atoms.\n")
        CACHE_FILE.write_text("[]")
        return

    # Sort: priority level first, then priority_score descending within level,
    # then date descending as tiebreaker
    open_atoms.sort(key=lambda a: (
        parse_priority(a),
        -(a.get("priority_score", 0.0)),
        -(int(parse_date(a).replace("-", "") or "0")),
    ))

    # Build clusters
    clusters = cluster_by_universe(open_atoms)
    cluster_summary = sorted(clusters.items(), key=lambda x: -len(x[1]))

    # Generate WORK-QUEUE.md
    lines = [
        "# Work Queue",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Total OPEN atoms:** {len(open_atoms)}",
        "",
        "## Priority Items",
        "",
    ]

    # Top 30 items
    for i, atom in enumerate(open_atoms[:30], 1):
        aid = atom["atom_id"]
        priority = parse_priority(atom)
        p_label = f"P{priority}"
        p_score = atom.get("priority_score", 0.0)
        date = parse_date(atom) or "unknown"
        universes = ", ".join(atom.get("universes", ["unscoped"])[:3])
        summary = truncate(atom.get("content", atom.get("summary", "")))
        lines.append(f"{i}. **[{p_label} {p_score:.2f}]** `{aid}` ({date}, {universes})")
        lines.append(f"   {summary}")
        lines.append("")

    if len(open_atoms) > 30:
        lines.append(f"*... and {len(open_atoms) - 30} more OPEN atoms*")
        lines.append("")

    # Cluster summary
    lines.append("## Universe Clusters")
    lines.append("")
    lines.append("| Universe | Count |")
    lines.append("|----------|-------|")
    for universe, atoms_in_cluster in cluster_summary:
        lines.append(f"| {universe} | {len(atoms_in_cluster)} |")
    lines.append("")

    # Type breakdown
    type_counts: dict[str, int] = {}
    for atom in open_atoms:
        t = atom.get("type", "unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    lines.append("## By Type")
    lines.append("")
    lines.append("| Type | Count |")
    lines.append("|------|-------|")
    for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
        lines.append(f"| {t} | {c} |")
    lines.append("")

    lines.append(f"*Engine: generate_work_queue.py | Run: {datetime.now().isoformat()}*")

    WORK_QUEUE_MD.write_text("\n".join(lines))
    print(f"Wrote {WORK_QUEUE_MD}")

    # Write lightweight cache
    cache_atoms = []
    for atom in open_atoms:
        cache_atoms.append({
            "atom_id": atom["atom_id"],
            "type": atom["type"],
            "summary": truncate(atom.get("content", atom.get("summary", "")), 200),
            "universes": atom.get("universes", []),
            "date": atom.get("date", ""),
            "priority": parse_priority(atom),
            "priority_score": atom.get("priority_score", 0.0),
        })

    with open(CACHE_FILE, "w") as f:
        json.dump(cache_atoms, f, indent=1)
    print(f"Wrote {CACHE_FILE} ({len(cache_atoms)} atoms, {CACHE_FILE.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    generate_work_queue()
