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
    # GitHub repo full-names are case-insensitive; normalize for comparison.
    me_full = f"{me_org}/{me_repo}".lower() if me_org and me_repo else ""

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
            # An edge is identified by `type` (the internal seed/v1.0 form) or by
            # `id` (the external-dependency form in standard 29, e.g. id: stripe +
            # source: EXTERNAL). Require at least one identifier.
            if not edge.get("type") and not edge.get("id"):
                annotate("error", path,
                         f"{section}[{i}] needs a 'type' (internal edge) or 'id' (external edge, standard 29)")
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
                if me_full and r.lower() == me_full:
                    annotate("error", path,
                             f"{section}[{i}] self-reference: '{r}' — a repo may not consume from / produce to itself")
                    violations += 1

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

        good = (
            "organ: Meta\nrepo: x\norg: meta-organvm\n"
            "consumes:\n  - type: t\n    source: ORGAN-IV\n"
            "  - id: stripe\n    source: EXTERNAL\n    kind: payments\n"
        )
        bad = "organ: Meta\nrepo: x\norg: meta-organvm\nconsumes:\n  id: organ/repo\n"
        selfref = "organ: Meta\nrepo: x\norg: meta-organvm\nconsumes:\n  - type: t\n    source: meta-organvm/x\n"
        with tempfile.TemporaryDirectory() as d:
            g, b, s = os.path.join(d, "g.yaml"), os.path.join(d, "b.yaml"), os.path.join(d, "s.yaml")
            with open(g, "w", encoding="utf-8") as fh:
                fh.write(good)
            with open(b, "w", encoding="utf-8") as fh:
                fh.write(bad)
            with open(s, "w", encoding="utf-8") as fh:
                fh.write(selfref)
            assert validate(g) == 0, "valid seed (incl. external edge) should pass"
            assert validate(b) == 1, "non-list consumes should fail"
            assert validate(s) == 1, "self-reference should fail"
        print("self-test OK")
        return 0
    if not os.path.exists(args.seed):
        annotate("warning", args.seed, "no seed.yaml found — registry-gate skipped")
        return 0
    return validate(args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
