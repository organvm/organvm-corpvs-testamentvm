#!/usr/bin/env python3
"""Route OPEN atoms to dispatch targets.

Reads open-atoms-cache.json (or prompt-atoms.json fallback),
classifies each OPEN atom by dispatch target, and outputs
DISPATCH-QUEUE.md + dispatch-queue.json.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CACHE_FILE = SCRIPT_DIR / "open-atoms-cache.json"
ATOMS_FILE = SCRIPT_DIR / "prompt-atoms.json"
DISPATCH_MD = SCRIPT_DIR / "DISPATCH-QUEUE.md"
DISPATCH_JSON = SCRIPT_DIR / "dispatch-queue.json"

# Patterns for routing
HUMAN_UNIVERSES = {"financial", "health", "housing", "relationships"}
MECHANICAL_PATTERNS = re.compile(
    r"\b(scaffold|boilerplate|create file|add ci|generate|template|stub|migrate)\b", re.I
)
RESEARCH_PATTERNS = re.compile(
    r"\b(research|landscape|compare|evaluate|survey|analyze|investigate|review literature)\b", re.I
)
STRATEGIC_PATTERNS = re.compile(
    r"\b(design|architect|formalize|theorem|proof|governance|system design|specification)\b", re.I
)


def route_atom(atom: dict) -> str:
    """Determine dispatch target for an atom."""
    universes = set(atom.get("universes", []))
    content = atom.get("summary", "") or atom.get("content", "")
    atom_type = atom.get("type", "")
    atom_id = atom.get("atom_id", "")

    # Human-only domains
    if universes & HUMAN_UNIVERSES:
        return "HUMAN"

    # Billing/auth blockers
    if any(kw in content.lower() for kw in ("billing", "payment", "revoke", "password", "login")):
        return "HUMAN"

    # Governance rules → Claude strategic
    if atom_type == "governance-rule" and "UNIVERSAL" in universes:
        return "CLAUDE"

    # Corrections need judgment
    if atom_type == "correction":
        return "CLAUDE"

    # Mechanical patterns → Codex
    if atom_type == "directive" and MECHANICAL_PATTERNS.search(content):
        return "CODEX"

    # Research patterns → Gemini/Perplexity
    if atom_type == "directive" and RESEARCH_PATTERNS.search(content):
        return "GEMINI"

    # Strategic patterns → Claude
    if atom_type == "directive" and STRATEGIC_PATTERNS.search(content):
        return "CLAUDE"

    # Constraints → Claude governance audit
    if atom_type == "constraint":
        return "CLAUDE"

    # Default
    return "CLAUDE"


def truncate(text: str, length: int = 120) -> str:
    text = text.replace("\n", " ").strip()
    return text[:length - 3] + "..." if len(text) > length else text


def route_all() -> None:
    # Load atoms
    if CACHE_FILE.exists():
        print(f"Loading from cache: {CACHE_FILE}")
        with open(CACHE_FILE) as f:
            atoms = json.load(f)
    elif ATOMS_FILE.exists():
        print(f"Cache not found, loading full: {ATOMS_FILE}")
        with open(ATOMS_FILE) as f:
            all_atoms = json.load(f)
        atoms = [a for a in all_atoms if a.get("status") == "OPEN"]
    else:
        print("ERROR: No atom files found", file=sys.stderr)
        sys.exit(1)

    print(f"Routing {len(atoms)} OPEN atoms...")

    # Route each atom
    dispatch: dict[str, list[dict]] = {}
    for atom in atoms:
        target = route_atom(atom)
        dispatch.setdefault(target, []).append({
            "atom_id": atom["atom_id"],
            "type": atom.get("type", "unknown"),
            "summary": truncate(atom.get("summary", atom.get("content", "")), 200),
            "universes": atom.get("universes", []),
            "date": atom.get("date", ""),
            "priority": atom.get("priority", 3),
            "priority_score": atom.get("priority_score", 0.0),
            "target": target,
        })

    # Sort within each target by priority level, then priority_score descending
    for target in dispatch:
        dispatch[target].sort(key=lambda a: (
            a.get("priority", 3),
            -(a.get("priority_score", 0.0)),
            -(int((a.get("date") or "0").replace("-", "") or "0")),
        ))

    # Write dispatch-queue.json
    with open(DISPATCH_JSON, "w") as f:
        json.dump(dispatch, f, indent=1)
    print(f"Wrote {DISPATCH_JSON}")

    # Write DISPATCH-QUEUE.md
    target_order = ["HUMAN", "CLAUDE", "CODEX", "GEMINI"]
    target_labels = {
        "HUMAN": "Requires Human Hands",
        "CLAUDE": "Claude (Strategic)",
        "CODEX": "Codex (Mechanical)",
        "GEMINI": "Gemini/Perplexity (Research)",
    }

    lines = [
        "# Dispatch Queue",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Total OPEN atoms:** {len(atoms)}",
        "",
        "## Summary",
        "",
        "| Target | Count |",
        "|--------|-------|",
    ]

    for target in target_order:
        if target in dispatch:
            lines.append(f"| {target_labels.get(target, target)} | {len(dispatch[target])} |")
    lines.append("")

    for target in target_order:
        if target not in dispatch:
            continue
        items = dispatch[target]
        lines.append(f"## {target_labels.get(target, target)} ({len(items)})")
        lines.append("")

        for atom in items:
            aid = atom["atom_id"]
            date = atom.get("date", "?")
            p = atom.get("priority", 3)
            ps = atom.get("priority_score", 0.0)
            universes = ", ".join(atom.get("universes", [])[:2])
            summary = atom["summary"]
            lines.append(f"- **[P{p} {ps:.2f}]** `{aid}` ({date}, {universes}) — {summary}")

        lines.append("")

    lines.append(f"*Engine: route_atoms.py | Run: {datetime.now().isoformat()}*")

    DISPATCH_MD.write_text("\n".join(lines))
    print(f"Wrote {DISPATCH_MD}")


if __name__ == "__main__":
    route_all()
