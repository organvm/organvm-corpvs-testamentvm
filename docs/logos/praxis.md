# Praxis — `meta-organvm/organvm-corpvs-testamentvm`

> *The Remediation Plan. The attack vectors for closing the gap between telos and pragma.*

**Status:** Initial draft (filling the documented vacuum per `14-logos-documentation-layer.md`)
**Date:** 2026-05-09
**Counterpart files:** `telos.md` (idealized form), `pragma.md` (concrete state), `receptio.md` (reception), `alchemical-io.md` (metabolic narrative)

---

## 1. Praxis Disposition

The corpus does not act *on the world* directly — that is the work of the operating organs (I–VII). The corpus acts *on itself* (and on the system's self-knowledge) by:

1. **Declaring** what should be (TELOS-typed additions to `docs/standards/`, `docs/specs/`, `docs/memory/`)
2. **Recording** what is (PRAGMA-typed updates to `registry-v2.json`, `data/`, `docs/evaluation/`)
3. **Witnessing** what was received (RECEPTIO-typed entries in `docs/applications/`, `docs/validation-runs/`, `docs/archive/`)
4. **Composing** the next move (PRAXIS-typed plans in `docs/operations/rolling-todo.md`, `INST-INDEX-RERUM-FACIENDARUM.md`, `docs/strategy/sprint-catalog.md`)

This document is the highest-level frame for category 4. Specific praxis lives in `docs/operations/rolling-todo.md` and `INST-INDEX-RERUM-FACIENDARUM.md` (the IRF — universal work registry).

## 2. The Governing Quadrilateral

Per CLAUDE.md, four documents govern all corpus praxis. They form a quadrilateral; no single document is sufficient on its own.

| Vertex | Document | Function |
|---|---|---|
| Roadmap | `docs/strategy/there+back-again.md` (referenced) / `docs/strategy/roadmap-there-and-back-again.md` | Phased plan from Phase −1 through launch |
| Cadence | `docs/operations/operational-cadence.md` | Anti-patterns, review rhythm, when to start sprints |
| Catalog | `docs/strategy/sprint-catalog.md` | 76 named sprints across 18 categories |
| Rolling TODO | `docs/operations/rolling-todo.md` | Active work queue (P0/P1/P2/P3) |

Praxis at any moment is *the intersection of these four*. A move that ignores the cadence (e.g., starting a new sprint while AP-1 says "don't start another sprint") is malformed praxis even if the move itself is technically correct.

## 3. Active Attack Vectors (Closing Specific Gaps)

### Vector A — Logos Symmetry (this PR is the first move)
- **Gap**: Symmetry: 0.0 (VACUUM) for this repo per CLAUDE.md auto-gen
- **Move**: Fill `docs/logos/{telos,pragma,praxis,receptio,alchemical-io}.md` with substantive narratives
- **Status**: In progress (the very PR this document ships in)
- **Next**: Roll the same pattern across other meta-organvm repos showing VACUUM status; then roll across organ flagships

### Vector B — Three Pure Systems Doctrine
- **Gap**: The repository's outer-tier architecture (CORPUS / ENGINE / SURFACE) is implicit in tooling but not declared anywhere
- **Move**: Publish `docs/standards/15-three-pure-systems.md` declaring the doctrine; cross-reference from `DIRECTORY.md`
- **Status**: In progress (this PR)
- **Next**: ENGINE and SURFACE publish their own self-descriptions as follow-up PRs, each in the appropriate territory

### Vector C — Implementation Density (System-wide)
- **Gap**: `code_files: 0`, `test_files: 0`, `repos_with_tests: 0` per Live System Variables (2026-04-14)
- **Move**: Drive omega criterion `#8 — Product live` in coordination with ORGAN-III repos that need real product execution
- **Status**: Tracked in IRF as multiple P0/P1 items
- **Next**: Per `rolling-todo.md`, X1–X4 hermetic-seal items and E1–E5 engagement items lead

### Vector D — Logos→Essay Extraction Pipeline
- **Gap**: `14-logos-documentation-layer.md` §5 mandates that significant logos updates extract as essays for ORGAN-V; pipeline is not yet automated
- **Move**: Define the extraction contract; implement extractor in `scripts/`; wire to `.github/workflows/`
- **Status**: NOT STARTED
- **Next**: Open IRF entry under IRF-OPS namespace; defer until logos coverage across organ repos is sufficient to justify the pipeline

### Vector E — Schema v1.2 Adoption for `seed.yaml`
- **Gap**: Current `seed.yaml` is schema v1.0; v1.2 introduces `telos`, `pragma`, `praxis`, `receptio` summary fields per `14-logos-documentation-layer.md` §2
- **Move**: Migrate this repo's `seed.yaml` to v1.2 with summaries of each logos narrative
- **Status**: NOT STARTED in this PR (separate concern, lighter than the narratives)
- **Next**: Schedule as IRF-DOC entry

### Vector F — Generator Script for Logos Manifest
- **Gap**: Inner-form classification (TELOS / PRAGMA / PRAXIS / RECEPTIO / ALCHEMICAL-IO) is asserted prose; no machine-checkable manifest exists
- **Move**: `scripts/generate-logos-manifest.py` — idempotent classifier emitting `docs/logos/manifest.csv`
- **Status**: NOT STARTED in this PR (deliberately deferred; ENGINE work belongs in a separate PR per the three-pure-systems doctrine)
- **Next**: Open as `feat(engine): generate logos manifest` once doctrine is canonized

## 4. Anti-Patterns the Praxis Must Avoid

Per `docs/operations/operational-cadence.md`:

- **AP-1**: Don't start another sprint before the current one is closed.
- **AP-2**: Don't measure activity (commits, words) as a proxy for progress on omega criteria.
- **AP-3**: Don't confuse the registry with the documentation; the registry is fact, the documentation is interpretation.
- **AP-4**: Don't rebuild what `scripts/` already does in shell one-liners.

This document, and the PR it ships in, must respect these. Specifically: the PR closes Vector A and Vector B *cleanly* without trying to also start Vector D (essay pipeline) or Vector F (generator) — those are explicitly deferred.

## 5. Recursive Praxis (How the Corpus Acts on Itself)

The corpus's most distinctive praxis is *self-modification under self-imposed constraint*. The same standards (`10`–`14`, soon `15`) it imposes on other repos govern its own evolution. Specifically:

- The corpus's `docs/logos/` is required by the corpus's own standard (`14-logos-documentation-layer.md`). Until today, the corpus violated its own rule. This PR ends that violation.
- The corpus's `docs/standards/` is the corpus's TELOS layer, and the corpus's praxis must conform to its own TELOS. Adding `15-three-pure-systems.md` is not adding *new* rules; it is declaring rules already implicit in tooling.
- The IRF (Index Rerum Faciendarum, `INST-INDEX-RERUM-FACIENDARUM.md`) is the corpus's praxis registry; every closed entry there is a praxis-act made permanent.

## 6. The Praxis Cadence

| Cadence | Trigger | Action |
|---|---|---|
| Per-session | session-close hook | Append fossil entry to `data/fossil/fossil-record.jsonl`; refresh `data/testament/sessions/` |
| Daily | `bash scripts/daily-soak.sh` | Health snapshot under `data/soak-test/` |
| Daily | scheduled GitHub Action | metrics auto-refresh, ecosystem audits, soak tests, stale detectors, POSSE distribution |
| Per-PR | pre-commit + CI | Lint, validate, fossil-link |
| Per-sprint close | `convergence-validate.py` + `convergence-promote.py` | Promote sprint state on the LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED machine |
| Quarterly (proposed) | manual | Logos symmetry audit across all repos; close VACUUM gaps |

## 7. Ordering Discipline

When two attack vectors compete for attention, the corpus prefers the one that:
1. **Satisfies a self-imposed standard** (e.g., filling logos vacuum) over one that adds new capability
2. **Closes an explicit IRF P0/P1 entry** over one that emerges only from intuition
3. **Strengthens the registry** over one that strengthens narrative
4. **Is reversible** over one that is not (the corpus is append-only at the deep paths but mutable at the standards level — always prefer the level that is correctable)

## 8. Exit Criteria for This Praxis Frame

This document is replaced or revised when:
- Symmetry across the corpus reaches 1.0 sustained for one full quarter
- The IRF P0 list is empty
- All 17 omega criteria are met
- A successor doctrine is canonized that supersedes the three-pure-systems framing

Until then, this is the active praxis frame.
