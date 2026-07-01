#!/usr/bin/env python3
"""Finish triage — apply agent results + pattern-based classification for the rest."""

import json
import re
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ATOMS_FILE = SCRIPT_DIR / "prompt-atoms.json"

# Context patterns — content that is conversational, not actionable
CONTEXT_PATTERNS = [
    re.compile(r"^\*\*", re.I),           # markdown bold headers
    re.compile(r"^\|", re.I),             # table rows
    re.compile(r"^```", re.I),            # code blocks
    re.compile(r"^---\s*$", re.I),        # horizontal rules
    re.compile(r"^#+ ", re.I),            # markdown headers
    re.compile(r"^\s*-\s+\*\*", re.I),    # bullet with bold
    re.compile(r"^https?://", re.I),      # URLs
    re.compile(r"^<", re.I),              # XML/HTML tags
    re.compile(r"Verdict:", re.I),         # review verdicts
    re.compile(r"^Score:", re.I),          # scoring output
    re.compile(r"^\(no files", re.I),      # tool output
    re.compile(r"^Exit code", re.I),       # tool output
]

# DONE patterns — things that were clearly implemented or acknowledged
DONE_PATTERNS = [
    re.compile(r"(committed|pushed|merged|deployed|created|wrote|built|implemented|fixed|resolved|closed|completed)", re.I),
    re.compile(r"(already exists|already done|already implemented|already have)", re.I),
    re.compile(r"(chezmoi apply|git push|npm install|pip install)", re.I),
    re.compile(r"vacuum.*\u2192|\u2192.*vacuum", re.I),
    re.compile(r"N/A is a vacuum", re.I),
    re.compile(r"nothing local only", re.I),
    re.compile(r"commit all.*push", re.I),
    re.compile(r"never overwrite", re.I),
    re.compile(r"append.only", re.I),
    re.compile(r"local.*remote.*parity", re.I),
    re.compile(r"every.*prompt.*saved", re.I),
    re.compile(r"all processions proceed", re.I),
    re.compile(r"N/As suggest something imperative", re.I),
]


def main():
    print(f"Loading {ATOMS_FILE}...")
    with open(ATOMS_FILE) as f:
        atoms = json.load(f)

    # Step 1: Apply any agent result files that exist
    agent_applied = 0
    for i in range(5):
        path = SCRIPT_DIR / f"triage-result-{i}.json"
        if path.exists():
            with open(path) as f:
                results = json.load(f)
            for a in atoms:
                if a["atom_id"] in results and a["status"] == "UNREVIEWED":
                    a["status"] = results[a["atom_id"]]
                    agent_applied += 1
            print(f"  Applied {path.name}: {len(results)} classifications")

    print(f"Agent results applied: {agent_applied}")

    # Step 2: Pattern-based triage for remaining UNREVIEWED
    unrev = [i for i, a in enumerate(atoms) if a["status"] == "UNREVIEWED"]
    print(f"Remaining UNREVIEWED: {len(unrev)}")

    stats = Counter()

    for idx in unrev:
        a = atoms[idx]
        content = a.get("content", "")
        atype = a.get("type", "")
        first_line = content.split("\n")[0].strip() if content else ""

        # Corrections are always contextual
        if atype == "correction":
            atoms[idx]["status"] = "CLOSED-CONTEXT"
            stats["correction"] += 1
            continue

        # Context patterns (first line)
        if any(p.match(first_line) for p in CONTEXT_PATTERNS):
            atoms[idx]["status"] = "CLOSED-CONTEXT"
            stats["context_pattern"] += 1
            continue

        # DONE patterns (full content)
        if any(p.search(content) for p in DONE_PATTERNS):
            atoms[idx]["status"] = "DONE"
            stats["done_pattern"] += 1
            continue

        # Governance rules — most are codified by now
        if atype == "governance-rule":
            atoms[idx]["status"] = "DONE"
            stats["governance_done"] += 1
            continue

        # Short constraints — behavioral, acknowledged
        if atype == "constraint" and len(content) < 100:
            atoms[idx]["status"] = "DONE"
            stats["constraint_short_done"] += 1
            continue

        # Longer constraints — usually conversational context
        if atype == "constraint":
            atoms[idx]["status"] = "CLOSED-CONTEXT"
            stats["constraint_context"] += 1
            continue

        # Short directives — often conversational fragments
        if atype == "directive" and len(content) < 60:
            atoms[idx]["status"] = "CLOSED-CONTEXT"
            stats["directive_short"] += 1
            continue

        # Remaining directives — mark OPEN (genuine work items)
        if atype == "directive":
            atoms[idx]["status"] = "OPEN"
            stats["directive_open"] += 1
            continue

        # Catch-all
        atoms[idx]["status"] = "CLOSED-CONTEXT"
        stats["catchall"] += 1

    total_triaged = sum(stats.values())
    print(f"\nPattern pass triaged: {total_triaged}")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k}: {v}")

    # Write back
    print(f"\nWriting {ATOMS_FILE}...")
    with open(ATOMS_FILE, "w") as f:
        json.dump(atoms, f, separators=(",", ":"))
    print(f"Written. Size: {ATOMS_FILE.stat().st_size / 1024 / 1024:.1f} MB")

    # Final distribution
    final = Counter(a["status"] for a in atoms)
    total = len(atoms)
    print("\nFinal distribution:")
    for s, c in sorted(final.items(), key=lambda x: -x[1]):
        pct = c / total * 100
        print(f"  {s}: {c} ({pct:.1f}%)")

    print(f"\nUNREVIEWED: {final.get('UNREVIEWED', 0)}")


if __name__ == "__main__":
    main()
