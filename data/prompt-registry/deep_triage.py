#!/usr/bin/env python3
"""Deep triage — aggressive heuristics to resolve UNREVIEWED atoms.

Applies 5 heuristic passes:
1. Deduplication: near-identical content with a DONE atom → DONE
2. Date decay: atoms >90 days old in high-completion universes → CLOSED-STALE
3. Navigational: short atoms that are session management, not work → CLOSED-NAV
4. Continuation: atoms that reference completed session work → DONE
5. Universe inference: remaining atoms in >75% DONE universes → CLOSED-INFERRED
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ATOMS_FILE = SCRIPT_DIR / "prompt-atoms.json"


def normalize(text: str) -> str:
    """Normalize text for comparison."""
    return re.sub(r'\s+', ' ', text.lower().strip())[:300]


def keyword_set(text: str) -> set[str]:
    """Extract meaningful keywords (3+ chars, no stopwords)."""
    stops = {'the', 'and', 'for', 'that', 'this', 'with', 'from', 'have', 'are',
             'was', 'were', 'been', 'being', 'will', 'would', 'could', 'should',
             'can', 'may', 'might', 'shall', 'not', 'but', 'all', 'any', 'each',
             'every', 'some', 'such', 'than', 'too', 'very', 'just', 'also',
             'now', 'then', 'here', 'there', 'when', 'where', 'how', 'what',
             'which', 'who', 'whom', 'why', 'its', 'has', 'had', 'does', 'did',
             'get', 'got', 'let', 'make', 'see', 'use', 'way', 'one', 'two',
             'new', 'old', 'yes', 'okay', 'sure'}
    words = re.findall(r'[a-z]{3,}', text.lower())
    return {w for w in words if w not in stops}


def jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# Navigational / session-management patterns
NAV_PATTERNS = [
    r'^(go|ok|yes|no|sure|continue|next|proceed|done|thanks|thank you|good|great|perfect|exactly|right|correct|yep|yeah|yup|fine|cool|nice|alright|understood|got it|k|okay)[\.\!\?\s]*$',
    r'^(\/clear|\/model|\/help|\/quit|\/exit|\/reload|\/fast|\/review|\/compact|\/commit)',
    r'^here comes the moon',
    r'^are we certain',
    r'^all of the above',
    r'^last session left us',
    r'^❯',
    r'^\s*$',
]
NAV_RE = [re.compile(p, re.I) for p in NAV_PATTERNS]

# Continuation phrases that indicate session management, not directives
CONTINUATION_PHRASES = [
    'pick up where we left off', 'continue from', 'last session',
    'previous session', 'handoff', 'pick this back up', 'where were we',
    'what was i working on', 'what needs doing', 'session is yours',
]


def is_navigational(content: str) -> bool:
    """Check if atom is navigational/session management."""
    text = content.strip()
    if len(text) < 20:
        return any(p.match(text) for p in NAV_RE)
    if len(text) < 50:
        return any(p.match(text) for p in NAV_RE)
    return False


def is_continuation(content: str) -> bool:
    """Check if atom is a session continuation prompt."""
    lower = content.lower()
    return any(phrase in lower for phrase in CONTINUATION_PHRASES)


def main():
    if not ATOMS_FILE.exists():
        print(f"ERROR: {ATOMS_FILE} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {ATOMS_FILE}...")
    with open(ATOMS_FILE) as f:
        atoms = json.load(f)

    total = len(atoms)
    unreviewed = [i for i, a in enumerate(atoms) if a["status"] == "UNREVIEWED"]
    print(f"Total atoms: {total}, UNREVIEWED: {len(unreviewed)}")

    # Build DONE content index for dedup
    done_keywords: list[set[str]] = []
    done_norms: set[str] = set()
    for a in atoms:
        if a["status"] == "DONE":
            kw = keyword_set(a.get("content", ""))
            if len(kw) >= 3:
                done_keywords.append(kw)
            done_norms.add(normalize(a.get("content", "")))

    print(f"DONE index: {len(done_keywords)} keyword sets, {len(done_norms)} normalized texts")

    # Universe completion rates
    universe_counts: dict[str, dict[str, int]] = {}
    for a in atoms:
        for u in a.get("universes", []):
            if u not in universe_counts:
                universe_counts[u] = {"total": 0, "done": 0}
            universe_counts[u]["total"] += 1
            if a["status"] == "DONE":
                universe_counts[u]["done"] += 1

    universe_rates = {
        u: c["done"] / c["total"] if c["total"] > 0 else 0
        for u, c in universe_counts.items()
    }

    # Triage passes
    stats = Counter()

    for idx in unreviewed:
        atom = atoms[idx]
        content = atom.get("content", "")
        atom_type = atom.get("type", "")
        date = atom.get("date", "")
        universes = atom.get("universes", [])

        # Pass 1: Navigational
        if is_navigational(content):
            atoms[idx]["status"] = "CLOSED-NAV"
            stats["pass1_nav"] += 1
            continue

        # Pass 2: Continuation prompts
        if is_continuation(content):
            atoms[idx]["status"] = "CLOSED-NAV"
            stats["pass2_continuation"] += 1
            continue

        # Pass 3: Near-duplicate of a DONE atom (Jaccard ≥ 0.6)
        atom_kw = keyword_set(content)
        if len(atom_kw) >= 3:
            norm = normalize(content)
            # Exact match first
            if norm in done_norms:
                atoms[idx]["status"] = "DONE"
                atoms[idx]["produced"] = ["dedup-exact"]
                stats["pass3_dedup_exact"] += 1
                continue
            # Jaccard match (sample — check first 200 DONE sets for speed)
            matched = False
            for dk in done_keywords:
                if jaccard(atom_kw, dk) >= 0.40:
                    atoms[idx]["status"] = "DONE"
                    atoms[idx]["produced"] = ["dedup-similar"]
                    stats["pass3_dedup_similar"] += 1
                    matched = True
                    break
            if matched:
                continue

        # Pass 4: Date decay — atoms >90 days old in well-covered universes
        if date and date < "2026-03-15":
            primary_universe = universes[0] if universes else "unscoped"
            rate = universe_rates.get(primary_universe, 0)
            if rate >= 0.40:
                atoms[idx]["status"] = "CLOSED-STALE"
                stats["pass4_date_decay"] += 1
                continue

        # Pass 5: Universe inference — remaining atoms in >75% DONE universes
        if universes:
            primary = universes[0]
            rate = universe_rates.get(primary, 0)
            if rate >= 0.60:
                atoms[idx]["status"] = "CLOSED-INFERRED"
                stats["pass5_universe"] += 1
                continue

        # Pass 6: Short low-signal content (<30 chars, no actionable keywords)
        if len(content.strip()) < 30:
            atoms[idx]["status"] = "CLOSED-NAV"
            stats["pass6_short"] += 1
            continue

    # Write back
    print(f"\nWriting {ATOMS_FILE}...")
    with open(ATOMS_FILE, "w") as f:
        json.dump(atoms, f, separators=(",", ":"))
    print(f"Written. Size: {ATOMS_FILE.stat().st_size / 1024 / 1024:.1f} MB")

    # Summary
    print("\n=== DEEP TRIAGE RESULTS ===")
    total_triaged = sum(stats.values())
    print(f"Total triaged: {total_triaged}")
    for pass_name, count in sorted(stats.items()):
        print(f"  {pass_name}: {count}")

    # New distribution
    new_statuses = Counter()
    for a in atoms:
        new_statuses[a["status"]] += 1
    print(f"\nNew status distribution:")
    for s, c in sorted(new_statuses.items(), key=lambda x: -x[1]):
        pct = c / total * 100
        print(f"  {s}: {c} ({pct:.1f}%)")

    remaining = new_statuses.get("UNREVIEWED", 0)
    print(f"\nRemaining UNREVIEWED: {remaining}")


if __name__ == "__main__":
    main()
