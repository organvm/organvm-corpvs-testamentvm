# Sprint 22: METRICUM

**Date:** 2026-02-16
**Focus:** Metrics automation
**Status:** COMPLETE

## Problem

Every time a repo was added, an essay published, or a sprint completed, the same numbers had to be manually find-and-replaced across 40+ files. This happened in TRIPARTITUM (13 files), SUBMISSIO (24+ files), and every prior sprint. Root cause: metrics were hardcoded as literal strings in dozens of markdown files and Python scripts instead of derived from a single source of truth.

## Solution

Three-script pipeline: **compute → store → propagate**.

```
repo-registry.json ──┐
docs/specs/sprints/ ┼──→ calculate-metrics.py ──→ system-metrics.json ──→ propagate-metrics.py ──→ 40+ files
gh API (essays)  ───┘         (compute)                 (source of truth)        (cascade)
```

## Deliverables

### 1. Rewritten `scripts/calculate-metrics.py`
- Computes all metrics from three sources: repo-registry.json, sprint specs directory, and essay count via GitHub API
- New `system-metrics.json` schema v1.0 with `computed` (auto-derived) and `manual` (human-maintained) sections
- `--skip-essays` flag for offline mode
- Manual section preserved across runs (word counts, code file counts — values that can't be auto-computed)

### 2. New `scripts/propagate-metrics.py`
- Reads system-metrics.json, updates hardcoded numbers in whitelisted markdown files via contextual pattern matching
- 39 regex patterns with surrounding context to prevent false positives
- Skip markers for historical lines, before/after tables, sprint descriptions, essay-specific word counts
- `--dry-run`, `--verbose`, `--file` flags
- Whitelist covers: README.md, CLAUDE.md, applications/, docs/applications/, docs/operations/, docs/essays/09-ai-conductor-methodology.md
- Exclusions: _posts/, essays/meta-system/, docs/archive/, docs/specs/sprints/, docs/evaluation/

### 3. Refactored `scripts/praxis-application-generator.py`
- Reads from system-metrics.json instead of hardcoding "89 repos", "82 production-grade", "28 essays", "10 sprints"
- All generators (`generate_system_overview`, `generate_metrics_snapshot`, `generate_application`) accept metrics parameter
- `emphasis_template` supports metric interpolation via Python format strings

### 4. Updated `scripts/praxis-validate.py`
- `check_dashboard()` now handles both old and new system-metrics.json schema

## Metrics

| Metric | Value |
|--------|-------|
| Files updated by propagation | 23 |
| Total replacements | 66 |
| Patterns defined | 39 |
| Skip markers | 60+ |
| Validation score | 12/12 PASS |

## Verification

- `calculate-metrics.py` produces: 97 repos, 90 ACTIVE, 7 ARCHIVED, 31 edges, 77 CI, 29 essays, 21 sprints
- `propagate-metrics.py --dry-run` reports changes in stale files, zero in current files
- `grep -r "91 repositor" docs/ applications/` returns zero matches
- `grep -r "82 production" scripts/` returns zero matches
- `praxis-validate.py` passes 12/12

## Operational Workflow (Post-Sprint)

After any metric change:
```bash
python3 scripts/calculate-metrics.py    # recompute from sources
python3 scripts/propagate-metrics.py    # cascade to all files
git diff && git add -A && git commit    # review and commit
```

Two commands. No more find-and-replace sweeps.
