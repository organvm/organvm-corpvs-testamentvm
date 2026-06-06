# Sprint 24: CANON

**Date:** 2026-02-16
**Focus:** Catalog reconciliation and stale document cleanup
**Status:** COMPLETE

## Problem

The sprint catalog (`sprint-catalog.md`) had 4 numbering collisions between catalog assignments and actual executed sprints (19–22). Catalog items MEMORIA, ANNOTATIO, DECISIO, and CANON were assigned numbers 19–22, but actual sprints 19–22 were CONCORDIA, TRIPARTITUM, SUBMISSIO, and METRICUM respectively. Additionally, 4 implementation-era documents referenced "44 repos" (now 97), used "PRODUCTION" (renamed to ACTIVE in VERITAS), and described completed work as pending. These inconsistencies undermine omega criterion #2 (stranger test) — a stranger reading the catalog or implementation docs would get a misleading picture of the system.

## Solution

Two work packages: (1) Reconcile the catalog by acknowledging the divergence between catalog numbers and execution numbers, marking displaced items as unscheduled, and adding the missing completed sprints. (2) Add historical document headers to 4 implementation-era documents pointing readers to current authoritative docs, without rewriting the documents themselves.

## Deliverables

### 1. Catalog reconciliation (`docs/strategy/sprint-catalog.md`)

- **Conventions updated**: Added explanation that catalog numbers 17–23 diverged from execution — actual sprint numbers in `docs/specs/sprints/` are canonical
- **Sprint 19**: Changed from MEMORIA to CONCORDIA (what actually executed); MEMORIA moved to unscheduled item with note about completion via TRIPARTITUM
- **Sprint 20**: Changed from ANNOTATIO to TRIPARTITUM (what actually executed); ANNOTATIO moved to unscheduled item
- **DECISIO**: Sprint number removed — marked as unscheduled future work (displaced by Sprint 21 SUBMISSIO)
- **CANON**: Sprint number removed — marked as COMPLETE, unscheduled (displaced by Sprint 22 METRICUM, executed as Sprint 24)
- **Sprint 22 METRICUM**: Added as completed item in Category 3
- **Sprint 23 PUBLICATIO**: Updated to COMPLETE with deliverable summary
- **Sprint 41 SUBMISSIO**: Marked COMPLETE (prep executed as Sprint 21)
- **Appendix A**: Counts updated to reflect actual execution
- **Appendix C**: Meta organ coverage updated
- **Appendix D**: SUBMISSIO marked COMPLETE, remaining critical path count reduced from 11 to 10

### 2. Historical document headers

Added `⚠ HISTORICAL DOCUMENT` blockquote headers to 4 files:

| File | Header Date | Key Clarification |
|------|-------------|-------------------|
| `implementation-package-v2.md` | 2026-02-03 | All phases COMPLETE, repo count 44→97 |
| `public-process-map-v2.md` | 2026-02-03 | 33 essays deployed, cadence in operational-cadence.md |
| `implementation-sprint-specs.md` | 2026-02-12 | All 5 repos validated, PRODUCTION→ACTIVE |
| `orchestration-system-v2.md` | 2026-02-03 | Design implemented, 44→97 repos |

Each header points to current authoritative documents (repo-registry.json, sprint-catalog.md, operational-cadence.md) without rewriting the historical content.

## Key Decisions

- **Don't rewrite history**: Historical documents retain their original "44 repos" and "PRODUCTION" references — they reflect the state when written. Headers redirect readers to current docs.
- **Catalog numbers vs. execution numbers**: Rather than renumbering the entire catalog (which would break cross-references), we acknowledge the divergence in the conventions section and let `docs/specs/sprints/` be the canonical record of what actually happened.
- **Displaced items lose their numbers**: DECISIO and the original CANON (catalog items 21–22) no longer claim those numbers since SUBMISSIO and METRICUM took those execution slots.

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Sprint specs | 23 | 24 |
| Catalog numbering collisions | 4 | 0 |
| Implementation docs with historical headers | 0 | 4 |
| Completed sprints in catalog | 5 (17–20, partial 23) | 8 (17–24) |

## What this sprint did NOT do

- Did not rewrite historical documents (they're artifacts of the planning era)
- Did not update "44 repos" → "97" throughout stale docs (headers clarify this)
- Did not fix "PRODUCTION" → "ACTIVE" in implementation-sprint-specs.md body (header clarifies)
- Did not change any system metrics (essay count stays at 33, repo count stays at 97)
- Did not create new infrastructure (AP-1 compliant — this is bug-fixing)
