#!/usr/bin/env python3
"""seed_gate.py — seed.yaml contract validator (GH#94 Template 4: Registry Gate).

Validates a repo's seed.yaml against the seed/v1.0 contract as it actually exists
in this ecosystem (see the repo-root seed.yaml and scripts/generate-seed-yaml.py):

  - identity keys present: organ, repo, org  (schema_version recommended)
  - produces / consumes (if present) MUST be lists of edge mappings, each with a
    `type`; a mapping or scalar in those slots is a malformed section, not an edge
  - no self-reference (a repo may not list its own org/repo as a consumer/source)
  - external edges use the additive `source: EXTERNAL` marker
    (docs/standards/29-external-dependency-policy.md) and are recognised as such;
    ORGAN-name sources (e.g. source: ORGAN-IV) are the normal internal form

This is the engine for the reusable-registry-gate workflow. It is deliberately
schema-light (the authoritative JSON Schema lives in schema-definitions); it
enforces the structural invariants every organ repo must satisfy. Emits GitHub
Actions annotations; exit 1 on violation.
"""
from __future__ import annotations

import argparse
import os

REQUIRED = ("organ", "repo", "org")
EDGE_SECTIONS = ("produces", "consumes", "implements", "subscriptions")


def annotate(level: str, file: str, msg: str) -> None:
    print(f"::{level} file={file}::{msg}")


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

    me_repo = data.get("repo", "")
    me_org = data.get("org", "")
    me_full = f"{me_org}/{me_repo}" if me_org and me_repo else ""

    for section in ("produces", "consumes"):
        if section not in data or data[section] is None:
            continue
        node = data[section]
        if not isinstance(node, list):
            annotate("error", path,
                     f"'{section}' must be a list of edges, got {type(node).__name__} "
                     f"— a mapping or scalar here is a malformed section")
            violations += 1
            continue
        for i, edge in enumerate(node):
            if not isinstance(edge, dict):
                annotate("error", path, f"{section}[{i}] must be a mapping, got {type(edge).__name__}")
                violations += 1
                continue
            if not edge.get("type"):
                annotate("error", path, f"{section}[{i}] missing 'type'")
                violations += 1
            # self-reference detection across consumers/source/consumer fields
            refs = []
            for v in (edge.get("consumers"), edge.get("source"), edge.get("consumer")):
                if isinstance(v, str):
                    refs.append(v)
                elif isinstance(v, list):
                    refs.extend(x for x in v if isinstance(x, str))
            for r in refs:
                if r.upper() == "EXTERNAL":
                    continue  # recognised external-dependency marker (standard 29)
                if me_full and r == me_full:
                    annotate("warning", path, f"{section}[{i}] self-reference: '{r}'")

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
        import tempfile

        good = "organ: Meta\nrepo: x\norg: meta-organvm\nconsumes:\n  - type: t\n    source: ORGAN-IV\n"
        bad = "organ: Meta\nrepo: x\norg: meta-organvm\nconsumes:\n  id: organ/repo\n"
        with tempfile.TemporaryDirectory() as d:
            g, b = os.path.join(d, "g.yaml"), os.path.join(d, "b.yaml")
            open(g, "w").write(good)
            open(b, "w").write(bad)
            assert validate(g) == 0, "valid seed should pass"
            assert validate(b) == 1, "non-list consumes should fail"
        print("self-test OK")
        return 0
    if not os.path.exists(args.seed):
        annotate("warning", args.seed, "no seed.yaml found — registry-gate skipped")
        return 0
    return validate(args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
