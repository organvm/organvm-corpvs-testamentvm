#!/usr/bin/env python3
"""seed_gate.py — seed.yaml contract validator (GH#94 Template 4: Registry Gate).

Validates a repo's seed.yaml against the structural contract:
  - required top-level keys present (id, organ)
  - produces/consumes are lists of edges with an `id`
  - no self-dependency (a repo may not consume its own id)
  - external edges are correctly marked (`source: EXTERNAL`) and are EXEMPT from
    intra-system acyclicity expectations (per docs/standards/29-external-dependency-policy.md)

This is the engine for the reusable-registry-gate workflow. It is deliberately
schema-light (the authoritative JSON Schema lives in schema-definitions); it
enforces the invariants that every organ repo must satisfy regardless of schema
version. Emits GitHub Actions annotations; exit 1 on violation.
"""
from __future__ import annotations

import argparse
import os
import sys

REQUIRED = ("id", "organ")


def annotate(level: str, file: str, msg: str) -> None:
    print(f"::{level} file={file}::{msg}")


def edge_ids(node) -> list[tuple[str, dict]]:
    out = []
    for e in node or []:
        if isinstance(e, str):
            out.append((e, {}))
        elif isinstance(e, dict):
            out.append((e.get("id", ""), e))
    return out


def validate(path: str) -> int:
    import yaml

    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        annotate("error", path, "seed.yaml top-level must be a mapping")
        return 1

    violations = 0
    for key in REQUIRED:
        if not data.get(key):
            annotate("error", path, f"missing required key: {key}")
            violations += 1

    me = data.get("id", "")
    for direction in ("produces", "consumes"):
        for eid, meta in edge_ids(data.get(direction)):
            if not eid:
                annotate("error", path, f"{direction}: edge missing 'id'")
                violations += 1
                continue
            if direction == "consumes" and eid == me:
                annotate("error", path, f"self-dependency: consumes its own id '{eid}'")
                violations += 1
            # external edges must self-declare; internal edges must not borrow EXTERNAL
            src = (meta.get("source") or "").upper() if isinstance(meta, dict) else ""
            looks_internal = "/" in eid  # org/repo form = internal system edge
            if src == "EXTERNAL" and looks_internal:
                annotate("warning", path,
                         f"edge '{eid}' marked source:EXTERNAL but looks internal (org/repo form)")
            if src != "EXTERNAL" and not looks_internal and direction == "consumes":
                annotate("warning", path,
                         f"edge '{eid}' is bare (not org/repo) and not marked source:EXTERNAL "
                         f"— if this is a third-party service, add source: EXTERNAL (see standard 29)")

    if violations:
        annotate("error", path, f"registry-gate: {violations} violation(s)")
        return 1
    print(f"registry-gate: {path} OK")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="seed.yaml registry gate (GH#94)")
    ap.add_argument("--seed", default="seed.yaml", help="path to seed.yaml")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)
    if args.self_test:
        assert edge_ids([{"id": "x"}, "y"]) == [("x", {"id": "x"}), ("y", {})]
        print("self-test OK")
        return 0
    if not os.path.exists(args.seed):
        annotate("warning", args.seed, "no seed.yaml found — registry-gate skipped")
        return 0
    return validate(args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
