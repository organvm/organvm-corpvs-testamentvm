#!/usr/bin/env python3
"""Priority Stratification Engine for ORGANVM prompt-atoms.

Scores all atoms (not just OPEN) on 6 dimensions and assigns P0-P3 priority.
Priority is orthogonal to status — even DONE/CLOSED atoms get scored for
retrospective analysis and triage validation.

Dimensions:
  1. Recency          (0.15) — exponential decay from creation date
  2. Type urgency     (0.25) — correction > governance-rule > constraint > ...
  3. Universe crit.   (0.20) — security > personal > UNIVERSAL > meta > ...
  4. Content specif.  (0.15) — file paths, repo names, tool names, commands
  5. Cross-ref density(0.10) — how many other atoms share keywords
  6. Completion traj. (0.15) — boost last-mile + neglected universes

Outputs:
  - Writes `priority` (0-3) and `priority_score` (0.0-1.0) into prompt-atoms.json
  - Prints distribution table

Usage:
    python3 prioritize_atoms.py
"""

from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
ATOMS_PATH = SCRIPT_DIR / "prompt-atoms.json"

# Reference date for recency calculation
TODAY = datetime.now()

# ---------------------------------------------------------------------------
# Weights
# ---------------------------------------------------------------------------

WEIGHTS = {
    "recency": 0.12,
    "type_urgency": 0.20,
    "universe_criticality": 0.18,
    "content_specificity": 0.12,
    "cross_reference": 0.08,
    "completion_trajectory": 0.12,
    "repetition": 0.18,
}

# ---------------------------------------------------------------------------
# Dimension 2: Type urgency lookup
# ---------------------------------------------------------------------------

TYPE_URGENCY = {
    "correction": 1.0,
    "governance-rule": 0.8,
    "constraint": 0.7,
    "question": 0.6,
    "directive": 0.5,
    "implicit-signal": 0.3,
    "emotional": 0.1,
    "data": 0.1,
    "command": 0.0,
}

# ---------------------------------------------------------------------------
# Dimension 3: Universe criticality lookup
# ---------------------------------------------------------------------------

UNIVERSE_CRITICALITY = {
    "security": 1.0,
    "financial": 0.95,
    "housing": 0.90,
    "health": 0.85,
    "employment": 0.85,
    "personal": 0.80,
    "UNIVERSAL": 0.70,
    "enforcement": 0.70,
    "meta": 0.65,
    "organ-iv": 0.55,
    "persistence": 0.55,
    "naming": 0.50,
    "organ-i": 0.50,
    "organ-ii": 0.50,
    "organ-iii": 0.50,
    "organ-v": 0.45,
    "organ-vi": 0.45,
    "organ-vii": 0.45,
    "relationships": 0.80,
    "unscoped": 0.30,
}

# Default for unlisted universes
DEFAULT_UNIVERSE_CRITICALITY = 0.40

# ---------------------------------------------------------------------------
# Keyword extraction (reused from measure_implementation.py)
# ---------------------------------------------------------------------------

MIN_KEYWORD_LEN = 4

STOP_WORDS = frozenset({
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "it", "this", "that", "are", "was",
    "were", "be", "been", "being", "have", "has", "had", "do", "does",
    "did", "will", "would", "shall", "should", "may", "might", "must",
    "can", "could", "not", "no", "all", "each", "every", "both", "few",
    "more", "most", "other", "some", "such", "than", "too", "very",
    "just", "also", "now", "then", "when", "where", "how", "what",
    "which", "who", "whom", "why", "here", "there", "about", "above",
    "after", "again", "against", "below", "between", "into", "through",
    "during", "before", "until", "while", "use", "used", "using",
    "make", "made", "need", "needs", "new", "get", "set", "add", "run",
    "file", "files", "see", "like", "only", "over", "same", "work",
    "if", "so", "up", "out", "any", "its", "they", "them", "their",
    "you", "your", "we", "our", "my", "me", "he", "she", "his", "her",
    "one", "two", "first", "last", "next", "well", "way", "even",
})

DOMAIN_STOP_WORDS = frozenset({
    "agent", "completed", "done", "session", "audit", "commit", "vacuum",
    "claude", "none", "resolved", "added", "yaml", "created", "json",
    "seed", "tests", "repo", "human", "github", "repos", "meta-organvm",
    "docs", "organvm", "governance", "registry", "entry", "data", "closed",
    "across", "entries", "organ", "system", "update", "status", "build",
    "deploy", "spec", "sprint", "phase", "check", "pass", "rule", "rules",
    "implement", "implemented", "implementation", "config", "configure",
    "configured", "ensure", "verified", "fixed", "test", "merged",
    "pushed", "remaining", "advanced", "partially", "further",
    "chore", "feat", "sync", "context", "submodule", "auto-generated",
    "refresh", "dependabot", "remove", "checkpoint", "workflow",
    "pointers", "changes", "readme", "updates", "local", "bump",
    "standards", "plans", "version", "deps", "initial", "merge",
    "branch", "revert", "release", "moved", "rename", "renamed",
    "refactor", "cleanup", "minor", "style", "format",
    "create", "review", "these", "output", "start", "proceed",
    "write", "clean", "users", "project", "state", "source",
    "should", "given", "based", "using", "every", "follow",
    "apply", "point", "define", "include", "current", "specific",
    "existing", "running", "right", "within", "keep", "thing",
    "things", "type", "types", "must", "want", "back", "full",
    "takes", "look", "show", "move", "step", "ensure", "require",
})

ALL_STOP = STOP_WORDS | DOMAIN_STOP_WORDS


def extract_keywords(text: str) -> set[str]:
    """Extract meaningful lowercase keywords from text."""
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", text.lower())
    return {w for w in words if len(w) >= MIN_KEYWORD_LEN and w not in ALL_STOP}


# ---------------------------------------------------------------------------
# Dimension 4: Content specificity patterns
# ---------------------------------------------------------------------------

# Indicators of specific, actionable content
SPECIFICITY_SIGNALS = [
    re.compile(r"[~/.][\w/.-]+\.\w{1,5}"),          # file paths
    re.compile(r"\b[\w-]+--[\w-]+\b"),                # double-hyphen repo names
    re.compile(r"\b(npm|pip|brew|cargo|just|pytest|ruff|gh|op|chezmoi)\b", re.I),  # tool names
    re.compile(r"`[^`]{3,}`"),                        # inline code
    re.compile(r"\b[A-Z]{2,}-\d+\b"),                 # ticket/ID references (IRF-SYS-001)
    re.compile(r"\bhttps?://\S+"),                     # URLs
]

# Indicators of vague, unactionable content
VAGUENESS_SIGNALS = [
    re.compile(r"\b(maybe|perhaps|consider|could|might|someday|eventually|potentially)\b", re.I),
    re.compile(r"\b(think about|look into|explore|brainstorm)\b", re.I),
]


def score_content_specificity(content: str) -> float:
    """Score how specific and actionable the content is. Returns 0.0-1.0."""
    if not content:
        return 0.0

    score = 0.0
    # Each specificity signal adds weight
    for pattern in SPECIFICITY_SIGNALS:
        matches = pattern.findall(content)
        if matches:
            score += min(len(matches) * 0.15, 0.3)  # cap per signal type

    # Vagueness penalizes
    for pattern in VAGUENESS_SIGNALS:
        if pattern.search(content):
            score -= 0.15

    # Length bonus: very short content (<50 chars) is likely vague
    if len(content) < 50:
        score -= 0.2
    elif len(content) > 200:
        score += 0.1

    return max(0.0, min(1.0, score))


# ---------------------------------------------------------------------------
# Corpus-wide computations
# ---------------------------------------------------------------------------

def compute_universe_completion(atoms: list[dict]) -> dict[str, float]:
    """Compute % DONE for each universe."""
    universe_total: Counter[str] = Counter()
    universe_done: Counter[str] = Counter()

    for atom in atoms:
        for u in atom.get("universes", []):
            universe_total[u] += 1
            if atom.get("status") == "DONE":
                universe_done[u] += 1

    return {
        u: universe_done[u] / universe_total[u] if universe_total[u] > 0 else 0.0
        for u in universe_total
    }


def build_keyword_index(atoms: list[dict]) -> tuple[dict[str, set[str]], dict[str, set[int]]]:
    """Build per-atom keywords and inverted keyword index.

    Returns:
        atom_keywords: atom_id -> set of keywords
        inverted: keyword -> set of atom indices (positions in list)
    """
    atom_keywords: dict[str, set[str]] = {}
    inverted: dict[str, set[int]] = defaultdict(set)

    for i, atom in enumerate(atoms):
        content = atom.get("content", "") or atom.get("summary", "")
        kws = extract_keywords(content)
        atom_keywords[atom["atom_id"]] = kws
        for kw in kws:
            inverted[kw].add(i)

    return atom_keywords, inverted


def compute_cross_reference_scores(
    atoms: list[dict],
    atom_keywords: dict[str, set[str]],
    inverted: dict[str, set[int]],
) -> dict[str, float]:
    """Compute normalized cross-reference density for each atom.

    For each atom, sum the index frequency of each of its keywords.
    Normalize by max score across the corpus.
    """
    raw_scores: dict[str, int] = {}

    for i, atom in enumerate(atoms):
        aid = atom["atom_id"]
        kws = atom_keywords.get(aid, set())
        if not kws:
            raw_scores[aid] = 0
            continue
        # Sum index sizes for each keyword, excluding self
        total = sum(len(inverted[kw]) - 1 for kw in kws if kw in inverted)
        raw_scores[aid] = total

    max_score = max(raw_scores.values()) if raw_scores else 1
    if max_score == 0:
        max_score = 1

    return {aid: score / max_score for aid, score in raw_scores.items()}


# ---------------------------------------------------------------------------
# Scoring engine
# ---------------------------------------------------------------------------

def score_recency(atom: dict) -> float:
    """Dimension 1: Exponential decay from creation date."""
    date_str = atom.get("date", "")
    if not date_str:
        return 0.0
    try:
        atom_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return 0.0
    days_old = (TODAY - atom_date).days
    if days_old < 0:
        days_old = 0
    return math.exp(-days_old / 45)


def score_type_urgency(atom: dict) -> float:
    """Dimension 2: Type-based urgency."""
    return TYPE_URGENCY.get(atom.get("type", ""), 0.3)


def score_universe_criticality(atom: dict) -> float:
    """Dimension 3: Max criticality across atom's universes."""
    universes = atom.get("universes", [])
    if not universes:
        return DEFAULT_UNIVERSE_CRITICALITY
    return max(
        UNIVERSE_CRITICALITY.get(u, DEFAULT_UNIVERSE_CRITICALITY)
        for u in universes
    )


def score_completion_trajectory(atom: dict, completion_rates: dict[str, float]) -> float:
    """Dimension 6: Boost based on universe completion rate.

    - Universes >60% DONE: last-mile boost (0.7-1.0 scaled)
    - Universes <20% DONE: neglected-universe boost (0.6-0.8 scaled)
    - Middle ground (20-60%): neutral (0.3-0.5)
    """
    universes = atom.get("universes", [])
    if not universes:
        return 0.3

    scores = []
    for u in universes:
        rate = completion_rates.get(u, 0.0)
        if rate >= 0.60:
            # Last-mile: higher completion = more urgent to finish
            scores.append(0.7 + 0.3 * ((rate - 0.60) / 0.40))
        elif rate <= 0.20:
            # Neglected: lower completion = needs attention
            scores.append(0.6 + 0.2 * ((0.20 - rate) / 0.20))
        else:
            # Middle: linear interpolation
            scores.append(0.3 + 0.2 * ((rate - 0.20) / 0.40))

    return max(scores)


def compute_repetition_scores(atoms: list[dict]) -> dict[str, float]:
    """Dimension 7: Repetition frequency as incompleteness signal.

    If the user said it twice, the first instance wasn't handled.
    If they said it five times, it's critical.

    Uses normalized content fingerprint for exact-match detection,
    plus keyword-based similarity for near-match detection.
    """
    # Exact/near-exact copy detection
    content_groups: dict[str, list[str]] = defaultdict(list)
    for atom in atoms:
        content = atom.get("content", "")
        if len(content) < 30:
            continue
        # Normalize: lowercase, collapse whitespace, first 200 chars
        key = re.sub(r"\s+", " ", content.lower().strip())[:200]
        content_groups[key].append(atom["atom_id"])

    # Count repetitions per atom
    repetition_counts: dict[str, int] = {}
    for key, aids in content_groups.items():
        if len(aids) > 1:
            for aid in aids:
                repetition_counts[aid] = max(
                    repetition_counts.get(aid, 0),
                    len(aids),
                )

    # Normalize: score = min(repetitions / 10, 1.0)
    # 10+ repetitions = max score
    return {
        aid: min(count / 10.0, 1.0)
        for aid, count in repetition_counts.items()
    }


def compute_priority(
    atom: dict,
    completion_rates: dict[str, float],
    cross_ref_scores: dict[str, float],
    repetition_scores: dict[str, float],
) -> tuple[int, float]:
    """Compute composite priority score and P-level for an atom.

    Returns (priority_level, priority_score) where:
        priority_level: 0-3 (P0=critical, P3=backlog)
        priority_score: 0.0-1.0 (raw composite)
    """
    d1 = score_recency(atom)
    d2 = score_type_urgency(atom)
    d3 = score_universe_criticality(atom)
    d4 = score_content_specificity(atom.get("content", ""))
    d5 = cross_ref_scores.get(atom["atom_id"], 0.0)
    d6 = score_completion_trajectory(atom, completion_rates)
    d7 = repetition_scores.get(atom["atom_id"], 0.0)

    composite = (
        WEIGHTS["recency"] * d1
        + WEIGHTS["type_urgency"] * d2
        + WEIGHTS["universe_criticality"] * d3
        + WEIGHTS["content_specificity"] * d4
        + WEIGHTS["cross_reference"] * d5
        + WEIGHTS["completion_trajectory"] * d6
        + WEIGHTS["repetition"] * d7
    )

    # Clamp to [0, 1]
    composite = max(0.0, min(1.0, composite))

    # Map to P-levels
    if composite >= 0.70:
        level = 0
    elif composite >= 0.50:
        level = 1
    elif composite >= 0.30:
        level = 2
    else:
        level = 3

    return level, round(composite, 4)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not ATOMS_PATH.exists():
        print(f"ERROR: {ATOMS_PATH} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Loading {ATOMS_PATH}...")
    with open(ATOMS_PATH) as f:
        atoms = json.load(f)
    print(f"Loaded {len(atoms)} atoms")

    # Corpus-wide computations
    print("Computing universe completion rates...")
    completion_rates = compute_universe_completion(atoms)
    for u in sorted(completion_rates, key=completion_rates.get, reverse=True)[:10]:
        print(f"  {u}: {completion_rates[u]:.1%}")

    print("Building keyword index...")
    atom_keywords, inverted = build_keyword_index(atoms)
    print(f"  {len(inverted)} unique keywords across {len(atom_keywords)} atoms")

    print("Computing cross-reference density...")
    cross_ref_scores = compute_cross_reference_scores(atoms, atom_keywords, inverted)

    print("Computing repetition frequency...")
    repetition_scores = compute_repetition_scores(atoms)
    repeated_count = sum(1 for v in repetition_scores.values() if v > 0)
    print(f"  {repeated_count} atoms with repetition signal")

    # Score every atom
    print("Scoring all atoms...")
    for atom in atoms:
        level, score = compute_priority(
            atom, completion_rates, cross_ref_scores, repetition_scores
        )
        atom["priority"] = level
        atom["priority_score"] = score

    # Write back
    print(f"Writing {ATOMS_PATH}...")
    with open(ATOMS_PATH, "w") as f:
        json.dump(atoms, f, indent=1)
    print(f"  {ATOMS_PATH.stat().st_size / 1024 / 1024:.1f} MB")

    # Distribution report
    print("\n" + "=" * 60)
    print("PRIORITY DISTRIBUTION")
    print("=" * 60)

    # By status x priority
    dist: dict[str, Counter[int]] = defaultdict(Counter)
    for atom in atoms:
        status = atom.get("status", "?")
        # Collapse CLOSED-* variants
        if status.startswith("CLOSED"):
            status = "CLOSED-*"
        dist[status][atom["priority"]] += 1

    statuses = ["DONE", "OPEN", "CLOSED-*"]
    print(f"\n{'Status':<12} {'P0':>6} {'P1':>6} {'P2':>6} {'P3':>6} {'Total':>8}")
    print("-" * 50)
    totals = Counter()
    for status in statuses:
        counts = dist.get(status, Counter())
        total = sum(counts.values())
        totals += counts
        print(
            f"{status:<12} {counts[0]:>6} {counts[1]:>6} "
            f"{counts[2]:>6} {counts[3]:>6} {total:>8}"
        )
    print("-" * 50)
    grand = sum(totals.values())
    print(
        f"{'TOTAL':<12} {totals[0]:>6} {totals[1]:>6} "
        f"{totals[2]:>6} {totals[3]:>6} {grand:>8}"
    )

    # OPEN atoms by priority — the actionable queue
    open_atoms = [a for a in atoms if a.get("status") == "OPEN"]
    if open_atoms:
        print(f"\n{'='*60}")
        print(f"OPEN ATOMS BY PRIORITY ({len(open_atoms)} total)")
        print(f"{'='*60}")
        open_by_p = Counter(a["priority"] for a in open_atoms)
        for p in range(4):
            print(f"  P{p}: {open_by_p.get(p, 0)}")

        # Top 10 P0 OPEN atoms
        p0_open = sorted(
            [a for a in open_atoms if a["priority"] == 0],
            key=lambda a: -a["priority_score"],
        )
        if p0_open:
            print(f"\nTop P0 OPEN atoms ({len(p0_open)} total):")
            for a in p0_open[:10]:
                content = (a.get("content", "") or "")[:80].replace("\n", " ")
                unis = ", ".join(a.get("universes", [])[:2])
                print(f"  [{a['priority_score']:.3f}] {a['atom_id']} ({a['type']}, {unis}) — {content}")

    # Score distribution histogram
    print(f"\n{'='*60}")
    print("SCORE HISTOGRAM")
    print(f"{'='*60}")
    buckets = [0] * 10  # 0.0-0.1, 0.1-0.2, ... 0.9-1.0
    for atom in atoms:
        idx = min(int(atom["priority_score"] * 10), 9)
        buckets[idx] += 1
    for i, count in enumerate(buckets):
        lo = i / 10
        hi = (i + 1) / 10
        bar = "#" * (count // 100)
        print(f"  {lo:.1f}-{hi:.1f}: {count:>6}  {bar}")

    print(f"\nDone. {len(atoms)} atoms scored.")


if __name__ == "__main__":
    main()
