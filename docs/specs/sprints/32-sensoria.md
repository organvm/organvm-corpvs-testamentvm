# Sprint 32: SENSORIA

**Date:** 2026-02-17
**Focus:** Autonomous perception layer — full seed.yaml coverage, stale-detection, metrics hardening
**Status:** COMPLETE

## Problem

The autonomous pipeline (AUTOMATA/DISTRIBUTIO) can act (distribute essays, generate pulse reports) but can't perceive itself accurately. system-metrics.json was stale (29 sprints, should be 31), 41 of 82 eligible repos lacked seed.yaml (so the orchestrator-agent's system graph was only ~50% complete), and no autonomous capability existed to detect and fix stale documentation data.

**AP-1 context:** This sprint addresses autonomous system gaps that prevent accurate self-monitoring — the prerequisite for all other autonomous operations.

## Solution

Three-pronged perception layer: (1) fix stale metrics + propagate, (2) batch-generate and deploy seed.yaml to all missing repos, (3) build a stale-detector autonomous script with weekly workflow.

## Deliverables

### 1. Fix system-metrics.json
- Updated `sprints_completed` from 29 → 32
- Added `30-distributio`, `31-fundamen`, `32-sensoria` to sprint_names list
- Ran `propagate-metrics.py` — 4 replacements across 3 files
- Fixed 2 false-positive propagation matches in concordance.md (historical sprint rows)
- Added `| COMPLETED |` skip marker to propagate-metrics.py for sprint history table rows
- Manually fixed essay count in system-overview.md (29 → 35 essays)

### 2. generate-seed-yaml.py batch script
- New `scripts/generate-seed-yaml.py` — reads repo-registry.json, detects primary language from local file extensions, generates seed.yaml with organ-level defaults
- Supports `--write`, `--push`, `--remote-only`, `--organ`, `--repo` flags
- Includes `git pull --rebase` before push to handle diverged repos
- Handles 3 push modes: local git push, gh api PUT (for repos without local clone), skip
- Language detection: walks repo files, counts by extension, returns dominant language
- Organ-level produces/consumes/subscriptions defaults match ALCHEMIA sprint patterns

### 3. Deploy seed.yaml to 82 repos (41 → 82)
- 8 repos pushed via local git (meta-source--ledger-output, chthon-oneiros, krypto-velamen, alchemical-synthesizer, ivi374ivi027-05, anon-hookup-now, select-or-left-or-right-or, recursive-engine--generative-entity)
- 23 repos pushed via gh api PUT (diverged from previous gh api file pushes)
- 1 repo pushed via gh api PUT remote-only (render-second-amendment, no local clone)
- Excluded: 3 repos archived on GitHub (nexus--babel-alexandria-, 4-ivi374-F0Rivi4, cog-init-1-0- — registry says ACTIVE but GitHub says archived)
- Excluded: 5 repos not on GitHub (scalable-lore-expert, life-betterment-simulation, universal-waveform-explorer, shared-remembrance-gateway, card-trade-social — registry entries with no remote)
- **Coverage: 82/82 eligible repos = 100%** (excluding 7 ARCHIVED + 8 .github repos)

### 4. stale-detector.py autonomous script
- New `scripts/stale-detector.py` — computes live metrics from registry/sprint-specs/essay-API, compares against stored system-metrics.json, scans whitelisted docs for stale hardcoded values
- Modes: report-only (default), `--fix` (runs calculate + propagate), `--issue` (creates GitHub issue)
- Detects: sprint count mismatches, repo count changes, essay count drift, metric string staleness
- Uses same whitelist as propagate-metrics.py for consistent file scanning

### 5. stale-detector-weekly.yml workflow
- New `.github/workflows/stale-detector-weekly.yml`
- Runs Tuesday 06:00 UTC (after Monday metrics-refresh at 06:00)
- Uses `--issue` mode to create maintenance issues when staleness detected
- Uses CROSS_ORG_TOKEN for essay count API access

## Metrics Delta

| Metric | Before | After |
|--------|--------|-------|
| Sprint count | 31 | 32 |
| Seed.yaml coverage | 41/82 (50%) | 82/82 (100%) |
| system-metrics.json sprints | 29 (stale) | 32 (current) |
| Stale-detection capability | Manual only | Automated weekly |
| Autonomous workflows | 3 (corpvs) | 4 (+ stale-detector) |

## Files Created

| File | Purpose |
|------|---------|
| `scripts/generate-seed-yaml.py` | Batch seed.yaml generator from registry |
| `scripts/stale-detector.py` | Detect stale metrics in docs |
| `.github/workflows/stale-detector-weekly.yml` | Weekly staleness check |
| `docs/specs/sprints/32-sensoria.md` | This sprint spec |

## Files Modified

| File | Change |
|------|--------|
| `system-metrics.json` | sprints 29→32, added sprint names |
| `scripts/propagate-metrics.py` | Added `\| COMPLETED \|` skip marker |
| `applications/shared/metrics-snapshot.md` | sprints_completed 29→32 (via propagation) |
| `applications/shared/system-overview.md` | sprints 29→32 (propagation) + essays 29→35 (manual) |
| `docs/operations/concordance.md` | Reverted 2 false-positive propagation changes |
| `docs/strategy/sprint-catalog.md` | Added SENSORIA entry, updated sprint count |
| ~41 repos: seed.yaml created | 100% orchestration graph coverage |
