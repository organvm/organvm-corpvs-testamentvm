# CI/CD Workflow Templates — Reusable Workflows for the Organ Ecosystem

**Date:** 2026-06-15
**Status:** TEMPLATES MATERIALIZED — 4/4 reusable workflows shipped; rollout in progress
**Source:** Plan `temporal-petting-kurzweil-agent-aa2155b.md` (2026-02-11); four-branch synthesis report
**Tracks:** GH#94 (Epic: CI/CD Workflow Templates for 79 Repos)
**Related:** GH#102 (aesthetic-guard, a 5th ORGAN-III-specific reusable workflow)

---

## 1. What this delivers

The four CI/CD templates from the #94 epic now exist as **reusable workflows** (`on: workflow_call`) in this corpus's `.github/workflows/`. Any repo in the ecosystem references them with a single `uses:` line and a pinned ref, instead of copy-pasting and drifting. This is the "designed → materialized" step of the epic: the plan described 4 templates; these are the 4 templates as runnable artifacts.

| # | Template | File | Engine |
|---|----------|------|--------|
| 1 | **Python CI** — ruff + pytest + coverage | `.github/workflows/reusable-python-ci.yml` | hosted toolchain |
| 2 | **TypeScript CI** — install + eslint + tsc + test | `.github/workflows/reusable-typescript-ci.yml` | hosted toolchain |
| 3 | **Documentation CI** — markdownlint + lychee link check | `.github/workflows/reusable-docs-ci.yml` | hosted actions |
| 4 | **Registry Gate** — seed.yaml contract validation | `.github/workflows/reusable-registry-gate.yml` | `scripts/seed_gate.py` |
| 5 | **Aesthetic Guard** (ORGAN-III) — palette/typography lint | `.github/workflows/reusable-aesthetic-guard.yml` | `scripts/aesthetic_guard.py` (GH#102) |

## 2. How a consuming repo adopts a template

```yaml
# .github/workflows/ci.yml in any ORGAN repo
name: ci
on: [push, pull_request]
jobs:
  python:
    uses: a-organvm/organvm-corpvs-testamentvm/.github/workflows/reusable-python-ci.yml@main
    with:
      python-version: "3.12"
      coverage-threshold: 0
  gate:
    uses: a-organvm/organvm-corpvs-testamentvm/.github/workflows/reusable-registry-gate.yml@main
```

Templates 4 and 5 check out this corpus at the pinned ref to run their Python engine, so the validation logic has a single source of truth. Pin to a tag (not `@main`) once a release is cut.

## 3. Why reusable workflows (not copied starter files)

A starter workflow is copied once and then drifts independently in every repo — exactly the fragmentation the aesthetic nervous system and the registry-as-source-of-truth invariant exist to prevent. A reusable workflow is *referenced*: a fix to the template propagates to all consumers on their next run. The trade-off (consumers couple to this repo's ref) is acceptable and is itself governed by the external-dependency discipline in `docs/standards/29-external-dependency-policy.md` — here the "external" dependency is an internal, governed one.

## 4. Rollout order (from the epic, refined)

The gate goes first because it is the cheapest and the most foundational (it protects the registry invariant), then the language CIs by organ density, then docs to flagships:

1. **Template 4 (Registry Gate)** → every repo with a `seed.yaml`. Cheapest, protects the source-of-truth invariant. **Start here.**
2. **Template 1 (Python CI)** → ORGAN-I + META repos (theory engines, tooling).
3. **Template 2 (TypeScript CI)** → ORGAN-III product repos.
4. **Template 3 (Documentation CI)** → all flagships first, then the long tail.
5. **Template 5 (Aesthetic Guard)** → ORGAN-III repos that carry an `organ-aesthetic.yaml`.

## 5. Status & acceptance

- [x] 4 templates designed (epic plan).
- [x] 4 templates **materialized as reusable workflows** in `.github/workflows/` (this deliverable) + 1 bonus (aesthetic-guard, GH#102).
- [x] Engines for the two custom gates are runnable and self-tested (`scripts/seed_gate.py --self-test`, `scripts/aesthetic_guard.py --self-test`).
- [ ] **Deployed across the ~38 active code repos** — this is the remaining epic body; tracked in GH#94. Per-repo adoption is a mechanical PR in each target repo and is out of scope for this corpus PR.

> This document advances GH#94 from "0 deployed" to "templates shipped + rollout playbook." The epic remains **open** until adoption across target repos is complete.

## 6. Cross-references

- GH#102 / `scripts/aesthetic_guard.py` — the ORGAN-III aesthetic gate (Template 5).
- `docs/standards/29-external-dependency-policy.md` — `seed_gate.py` enforces the `source: EXTERNAL` convention defined there.
- `repo-registry.json` — the registry the gate ultimately protects.
