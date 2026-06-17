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

    # Every edge section is modelled as a list (produces/consumes/implements/
    # subscriptions). A mapping or scalar in any of them is a malformed section.
    for section in EDGE_SECTIONS:
        if section in data and data[section] is not None and not isinstance(data[section], list):
            annotate("error", path,
                     f"'{section}' must be a list, got {type(data[section]).__name__} "
                     f"— a mapping or scalar here is a malformed section")
            violations += 1

    # Edge-identifier and self-reference checks apply to the dependency sections.
    for section in ("produces", "consumes"):
        if section not in data or not isinstance(data.get(section), list):
            continue
        node = data[section]
        for i, edge in enumerate(node):
            if not isinstance(edge, dict):
                annotate("error", path, f"{section}[{i}] must be a mapping, got {type(edge).__name__}")
                violations += 1
                continue
            # Edge identifier rules:
            #  - internal edge: a `type` (seed/v1.0), or an org/repo reference in
            #    `id`/`from` (contains '/')
            #  - external edge (standard 29): a service `id` WITH source: EXTERNAL
            # A bare service `id` without source: EXTERNAL is rejected — it would
            # otherwise vanish from external-dependency tracking (standard 29).
            edge_id = edge.get("id")
            edge_from = edge.get("from")
            src = edge.get("source")
            is_external = isinstance(src, str) and src.upper() == "EXTERNAL"
            repo_ref = next((v for v in (edge_id, edge_from) if isinstance(v, str) and "/" in v), None)
            if not edge.get("type") and not repo_ref and not (edge_id and is_external):
                if isinstance(edge_id, str) and not is_external:
                    annotate("error", path,
                             f"{section}[{i}] service id '{edge_id}' must declare source: EXTERNAL (standard 29), "
                             f"or use a 'type'/org-repo id for an internal edge")
                else:
                    annotate("error", path,
                             f"{section}[{i}] needs a 'type' (internal), an org/repo id|from (internal), "
                             f"or an id + source: EXTERNAL (external)")
                violations += 1
            # self-reference detection across consumers / source / consumer / from / id
            refs = []
            for v in (edge.get("consumers"), src, edge.get("consumer"), edge_from, edge_id):
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

    # implements/subscriptions entries are mappings (ADR-013): implements has
    # `concept`, subscriptions has `event`/`source`/`action`. A bare-string entry
    # (e.g. `subscriptions: [governance.updated]`) is a malformed contract.
    for section in ("implements", "subscriptions"):
        node = data.get(section)
        if isinstance(node, list):
            for i, entry in enumerate(node):
                if not isinstance(entry, dict):
                    annotate("error", path,
                             f"{section}[{i}] must be a mapping, got {type(entry).__name__}")
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
        idservice = "organ: Meta\nrepo: x\norg: meta-organvm\nconsumes:\n  - id: stripe\n    kind: payments\n"
        fromref = "organ: Meta\nrepo: x\norg: meta-organvm\nconsumes:\n  - type: t\n    from: META-ORGANVM/x\n"
        subbad = "organ: Meta\nrepo: x\norg: meta-organvm\nsubscriptions:\n  event: governance.updated\n"
        sublist = "organ: Meta\nrepo: x\norg: meta-organvm\nsubscriptions:\n  - governance.updated\n"
        with tempfile.TemporaryDirectory() as d:
            paths = {k: os.path.join(d, f"{k}.yaml") for k in ("g", "b", "s", "isv", "fr", "sub", "sl")}
            for k, content in (("g", good), ("b", bad), ("s", selfref), ("isv", idservice),
                               ("fr", fromref), ("sub", subbad), ("sl", sublist)):
                with open(paths[k], "w", encoding="utf-8") as fh:
                    fh.write(content)
            assert validate(paths["g"]) == 0, "valid seed (incl. external edge) should pass"
            assert validate(paths["b"]) == 1, "non-list consumes should fail"
            assert validate(paths["s"]) == 1, "self-reference should fail"
            assert validate(paths["isv"]) == 1, "bare service id without source: EXTERNAL should fail"
            assert validate(paths["fr"]) == 1, "case-insensitive 'from' self-reference should fail"
            assert validate(paths["sub"]) == 1, "non-list subscriptions should fail"
            assert validate(paths["sl"]) == 1, "bare-string subscription entry should fail"
        print("self-test OK")
        return 0
    if not os.path.exists(args.seed):
        annotate("warning", args.seed, "no seed.yaml found — registry-gate skipped")
        return 0
    return validate(args.seed)


if __name__ == "__main__":
    raise SystemExit(main())
