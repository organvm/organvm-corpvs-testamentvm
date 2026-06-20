#!/usr/bin/env python3
"""Merge parallel atom stores into a unified index.

Combines plan-derived atoms (atomized-tasks.jsonl) and prompt-derived atoms
(prompt-atoms.jsonl) into a single unified index with cross-references.

Usage: python3 scripts/merge_atom_stores.py
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

DATA_DIR = Path.home() / "Workspace/organvm/organvm-corpvs-testamentvm/data/atoms"
PLAN_PATH = DATA_DIR / "atomized-tasks.jsonl"
PROMPT_PATH = DATA_DIR / "prompt-atoms.jsonl"
SHORT_PATH = DATA_DIR / "prompt-atoms-short.jsonl"
ANNOTATED_PATH = DATA_DIR / "annotated-prompts.jsonl"
SUB_PATH = DATA_DIR / "sub-prompt-atoms.jsonl"
UNIFIED_OUTPUT = DATA_DIR / "unified-atoms.jsonl"
LINEAGE_OUTPUT = DATA_DIR / "atom-lineage.jsonl"

STOPWORDS = {
    "this", "that", "with", "from", "have", "been", "will", "would", "could",
    "should", "what", "when", "where", "which", "about", "their", "them",
    "they", "there", "here", "some", "than", "then", "also", "into", "more",
    "very", "just", "like", "make", "need", "want", "each", "please", "help",
    "using", "used", "does", "done", "based", "file", "files", "code",
}


def tokenize(text: str) -> set:
    words = re.sub(r"[^a-z\s]", " ", text.lower()).split()
    return {w for w in words if len(w) > 3 and w not in STOPWORDS}


def normalize_plan_atom(atom: dict) -> dict:
    return {
        "unified_id": f"plan-{atom.get('id', '')}",
        "original_id": atom.get("id", ""),
        "source_type": "plan_task",
        "title": atom.get("title", ""),
        "body": atom.get("raw_text", atom.get("content", ""))[:500],
        "date": atom.get("source", {}).get("plan_date", ""),
        "status": atom.get("status", ""),
        "domain": atom.get("domain", "general"),
        "priority": atom.get("priority", "P2"),
        "tags": atom.get("tags", []),
        "actionable": atom.get("actionable", False),
        "agent": atom.get("agent", ""),
        "linked_ids": [],
    }


def normalize_prompt_atom(atom: dict) -> dict:
    ts = atom.get("source", {}).get("timestamp", "")
    date = ts[:10] if ts and not ts.startswith("1969") else ""
    return {
        "unified_id": atom.get("id", ""),
        "original_id": atom.get("id", ""),
        "source_type": "user_prompt",
        "title": atom.get("title", ""),
        "body": atom.get("content", "")[:500],
        "date": date,
        "status": atom.get("status", "OPEN"),
        "domain": atom.get("domain", "general"),
        "priority": atom.get("priority", "P3"),
        "tags": atom.get("tags", []),
        "actionable": atom.get("actionable", True),
        "agent": atom.get("source", {}).get("provider", ""),
        "linked_ids": [],
    }


def normalize_annotated_atom(atom: dict) -> dict:
    source = atom.get("source", {})
    content = atom.get("content", {})
    classification = atom.get("classification", {})
    signals = atom.get("signals", {})
    text = content.get("text", atom.get("raw_text", ""))
    ts = source.get("timestamp", "")
    date = ts[:10] if ts and not ts.startswith("1969") else ""
    return {
        "unified_id": f"annotated-{atom.get('id', '')}",
        "original_id": atom.get("id", ""),
        "source_type": "annotated_prompt",
        "title": text[:80] if text else "",
        "body": text[:500] if text else "",
        "date": date,
        "status": "OPEN",
        "domain": "general",
        "priority": "P2",
        "tags": signals.get("tags", []),
        "actionable": True,
        "agent": source.get("agent", ""),
        "linked_ids": [],
        "classification": classification,
        "signals": signals,
        "threading": atom.get("threading", {}),
    }


def normalize_sub_atom(atom: dict) -> dict:
    ts = atom.get("source", {}).get("timestamp", "")
    date = ts[:10] if ts and not ts.startswith("1969") else ""
    return {
        "unified_id": atom.get("id", ""),
        "original_id": atom.get("id", ""),
        "source_type": "sub_prompt",
        "title": atom.get("title", ""),
        "body": atom.get("content", "")[:500],
        "date": date,
        "status": atom.get("status", "OPEN"),
        "domain": atom.get("domain", "general"),
        "priority": atom.get("priority", "P3"),
        "tags": atom.get("tags", []),
        "actionable": atom.get("actionable", True),
        "agent": atom.get("source", {}).get("provider", ""),
        "linked_ids": [],
        "parent_id": atom.get("parent_id", ""),
    }


def load_jsonl(path: Path) -> list:
    atoms = []
    if path.exists():
        with open(path) as f:
            for line in f:
                if line.strip():
                    atoms.append(json.loads(line))
    return atoms


def main():
    print("Loading atom stores...")

    plan_raw = load_jsonl(PLAN_PATH)
    prompt_raw = load_jsonl(PROMPT_PATH)
    short_raw = load_jsonl(SHORT_PATH)
    annotated_raw = load_jsonl(ANNOTATED_PATH)
    sub_raw = load_jsonl(SUB_PATH)

    print(f"  Plan atoms: {len(plan_raw)}")
    print(f"  Prompt atoms: {len(prompt_raw)}")
    print(f"  Short prompt atoms: {len(short_raw)}")
    print(f"  Annotated prompt atoms: {len(annotated_raw)}")
    print(f"  Sub-prompt atoms: {len(sub_raw)}")

    # Normalize all
    plan_atoms = [normalize_plan_atom(a) for a in plan_raw]
    prompt_atoms = [normalize_prompt_atom(a) for a in prompt_raw]
    short_atoms = [normalize_prompt_atom(a) for a in short_raw]
    annotated_atoms = [normalize_annotated_atom(a) for a in annotated_raw]
    sub_atoms = [normalize_sub_atom(a) for a in sub_raw]

    # Build domain index for plan atoms
    plan_by_domain = defaultdict(list)
    for i, a in enumerate(plan_atoms):
        plan_by_domain[a["domain"]].append(i)

    # Build token sets
    plan_tokens = [tokenize(a["title"] + " " + a["body"][:100]) for a in plan_atoms]
    prompt_tokens = [tokenize(a["title"] + " " + a["body"][:100]) for a in prompt_atoms]

    # Cross-reference: for each prompt, find best matching plan atom
    print("Cross-referencing prompt → plan atoms...")
    lineage = []
    linked_prompt_ids = set()
    linked_plan_ids = set()

    for pi, pa in enumerate(prompt_atoms):
        domain = pa["domain"]
        candidates = plan_by_domain.get(domain, [])
        if not candidates:
            continue

        p_tokens = prompt_tokens[pi]
        if len(p_tokens) < 2:
            continue

        best_score = 0
        best_plan_idx = -1

        for ci in candidates:
            # Token overlap gate
            shared = p_tokens & plan_tokens[ci]
            if len(shared) < 2:
                continue

            # difflib on title + first 100 chars
            a_text = pa["title"] + " " + pa["body"][:100]
            b_text = plan_atoms[ci]["title"] + " " + plan_atoms[ci]["body"][:100]
            score = SequenceMatcher(None, a_text.lower(), b_text.lower()).ratio()

            if score > best_score:
                best_score = score
                best_plan_idx = ci

        if best_score >= 0.50 and best_plan_idx >= 0:
            plan_a = plan_atoms[best_plan_idx]
            prompt_date = pa["date"]
            plan_date = plan_a["date"]

            lag_days = None
            if prompt_date and plan_date:
                try:
                    pd = datetime.strptime(prompt_date[:10], "%Y-%m-%d")
                    pld = datetime.strptime(plan_date[:10], "%Y-%m-%d")
                    lag_days = (pld - pd).days
                except ValueError:
                    pass

            lineage.append({
                "prompt_atom_id": pa["unified_id"],
                "plan_atom_id": plan_a["unified_id"],
                "similarity": round(best_score, 3),
                "prompt_date": prompt_date,
                "plan_date": plan_date,
                "lag_days": lag_days,
            })

            # Link them
            pa["linked_ids"].append(plan_a["unified_id"])
            plan_a["linked_ids"].append(pa["unified_id"])
            linked_prompt_ids.add(pa["unified_id"])
            linked_plan_ids.add(plan_a["unified_id"])

    # Combine all into unified index
    all_atoms = plan_atoms + prompt_atoms + short_atoms + annotated_atoms + sub_atoms

    # Write unified atoms
    tmp = str(UNIFIED_OUTPUT) + ".tmp"
    with open(tmp, "w") as f:
        for a in all_atoms:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
    os.rename(tmp, UNIFIED_OUTPUT)

    # Write lineage
    tmp = str(LINEAGE_OUTPUT) + ".tmp"
    with open(tmp, "w") as f:
        for l in lineage:
            f.write(json.dumps(l, ensure_ascii=False) + "\n")
    os.rename(tmp, LINEAGE_OUTPUT)

    # Stats
    orphan_prompts = len(prompt_atoms) - len(linked_prompt_ids)
    orphan_plans = len(plan_atoms) - len(linked_plan_ids)

    print(f"\n{'=' * 60}")
    print("UNIFIED ATOM INDEX RESULTS")
    print(f"{'=' * 60}")
    print(f"Total unified atoms: {len(all_atoms)}")
    print(f"  Plan atoms: {len(plan_atoms)}")
    print(f"  Prompt atoms: {len(prompt_atoms)}")
    print(f"  Short atoms: {len(short_atoms)}")
    print(f"  Annotated atoms: {len(annotated_atoms)}")
    print(f"  Sub-prompt atoms: {len(sub_atoms)}")
    print(f"\nLinked pairs: {len(lineage)}")
    print(f"  Linked prompts: {len(linked_prompt_ids)}")
    print(f"  Linked plans: {len(linked_plan_ids)}")
    print(f"  Orphan prompts (no matching plan): {orphan_prompts}")
    print(f"  Orphan plans (no originating prompt): {orphan_plans}")

    if lineage:
        avg_sim = sum(l["similarity"] for l in lineage) / len(lineage)
        lags = [l["lag_days"] for l in lineage if l["lag_days"] is not None]
        print("\nLineage stats:")
        print(f"  Average similarity: {avg_sim:.3f}")
        if lags:
            print(f"  Average prompt→plan lag: {sum(lags)/len(lags):.1f} days")
            print(f"  Lag range: {min(lags)} to {max(lags)} days")

    print("\nOutput files:")
    print(f"  Unified: {UNIFIED_OUTPUT} ({UNIFIED_OUTPUT.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"  Lineage: {LINEAGE_OUTPUT} ({LINEAGE_OUTPUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
