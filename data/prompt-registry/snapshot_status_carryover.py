#!/usr/bin/env python3
"""Snapshot a content-keyed status map from prompt-atoms.json.

The extract → atomize pipeline is full-rebuild: it resets every atom to
UNREVIEWED and reassigns sequential ATM ids, so statuses and priority fields
must be carried over by content identity, not by id. This script captures
the map BEFORE a rebuild; apply it after with an (timestamp, sha1(content))
join.

Key: "{timestamp}|{sha1(content)}" → {status, produced, priority, priority_score}
Output: status-carryover.json (gitignored alongside the other registry JSONs).

Memory-lean by design (16GB machine): the source file is read as one string
(~74MB) but array elements are decoded incrementally and discarded; only the
small carry-over map is retained.
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

REGISTRY_DIR = Path(__file__).parent
INPUT_FILE = REGISTRY_DIR / "prompt-atoms.json"
OUTPUT_FILE = REGISTRY_DIR / "status-carryover.json"

# Progression order for collision resolution: keep the most-progressed status.
STATUS_RANK = {
    "DONE": 5,
    "ARCHIVED": 4,
    "CLOSED-NAV": 3,
    "CLOSED-COMMAND": 3,
    "OPEN": 2,
    "UNREVIEWED": 1,
    "N/A": 0,
}

CARRY_FIELDS = ("status", "produced", "priority", "priority_score")


def iter_atoms(text: str):
    decoder = json.JSONDecoder()
    idx = text.index("[") + 1
    n = len(text)
    while idx < n:
        while idx < n and text[idx] in " \t\r\n,":
            idx += 1
        if idx >= n or text[idx] == "]":
            return
        obj, idx = decoder.raw_decode(text, idx)
        yield obj


def main() -> int:
    text = INPUT_FILE.read_text()
    carry = {}
    statuses = Counter()
    collisions = 0
    total = 0
    for atom in iter_atoms(text):
        total += 1
        statuses[atom.get("status", "?")] += 1
        content = atom.get("content") or ""
        key = f"{atom.get('timestamp', '')}|{hashlib.sha1(content.encode()).hexdigest()}"
        entry = {f: atom[f] for f in CARRY_FIELDS if f in atom}
        if key in carry:
            collisions += 1
            old_rank = STATUS_RANK.get(carry[key].get("status", ""), -1)
            new_rank = STATUS_RANK.get(entry.get("status", ""), -1)
            if new_rank <= old_rank:
                continue
        carry[key] = entry
    OUTPUT_FILE.write_text(json.dumps(carry, separators=(",", ":")))
    print(f"atoms scanned: {total}")
    print(f"unique keys:   {len(carry)}  (collisions: {collisions})")
    print(f"status counts: {dict(statuses)}")
    print(f"wrote: {OUTPUT_FILE} ({OUTPUT_FILE.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
