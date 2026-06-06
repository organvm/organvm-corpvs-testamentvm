# Sprint 31: FUNDAMEN

**Date:** 2026-02-17
**Focus:** Infrastructure hardening for Organs V/VI/VII/Meta
**Status:** COMPLETE

## Problem

Organs V, VI, VII, and Meta are the lightest in the system. Local clones for 6 repos were stale (5 community-health files vs 20+ files on remote including Python prototypes, seed.yaml, and CI). The Python prototypes deployed during CONSOLIDATION-II had well-structured dataclass stubs with tests, but several repos lacked real functional implementations beyond mock returns. alchemia-ingestvm (Meta) had 52 files of real code but no README, no CI, and no seed.yaml. Seed.yaml coverage for these organs was 0% locally (all existed on remote but weren't pulled).

**AP-1 context:** This sprint addresses infrastructure gaps that block other work — stale locals prevent development, missing README makes alchemia-ingestvm invisible to audits, and stub-only code means CI validates structure but not logic.

## Solution

Full infrastructure pass: sync all stale locals, add README/CI/seed.yaml to alchemia-ingestvm, add real HTTP POST logic to social-automation, enhance test coverage across all 4 prototype repos.

## Deliverables

### 1. Sync 6 stale local repos
- `git pull` / `git reset --hard origin/main` for 5 repos (salon-archive, reading-group-curriculum, social-automation, distribution-strategy, announcement-templates)
- Fresh `git clone` for adaptive-personal-syllabus (was a non-git directory with broken symlinks to deleted `~/world/` paths)
- Old adaptive-personal-syllabus content moved to `~/Workspace/intake/adaptive-personal-syllabus-old-local`
- All 6 repos now match remote HEAD

### 2. alchemia-ingestvm infrastructure
- **README.md** (~2,700 words): Documents three-stage pipeline (INTAKE → ABSORB → ALCHEMIZE), aesthetic nervous system (taste.yaml cascade), 5 capture channels, full module reference, CLI usage, data directory layout
- **seed.yaml**: Schema v1.0, Organ: Meta, produces classified-artifacts/deployment-manifests/provenance-records/creative-briefs/aesthetic-chains, consumes repo-registry.json from corpvs-testamentvm
- **.github/workflows/ci.yml**: Python CI matrix (3.11, 3.12), ruff lint + pytest

### 3. social-automation real HTTP logic (ORGAN-VII)
- `mastodon.py`: Added `_post_to_api()` method with real `urllib.request` HTTP POST to Mastodon API (`/api/v1/statuses`), `live` mode flag for production vs test
- `discord.py`: Added `_send_to_webhook()` method with real `urllib.request` HTTP POST to Discord webhook URLs, `live` mode flag
- `posse.py`: Wired `syndicate()` to accept and use actual client instances for real platform posting
- New `tests/test_discord.py` with embed and webhook tests
- All 9+ tests pass

### 4. distribution-strategy enhanced coverage (ORGAN-VII)
- New `tests/test_analytics.py` with 8 tests covering engagement rate calculation, channel aggregation, top content ranking, to_dict serialization
- All 16+ tests pass

### 5. salon-archive enhancements (ORGAN-VI)
- `sessions.py`: Added `search_by_date_range()` and `update_session()` methods
- `transcription.py`: Enhanced `process_audio()` to generate multi-speaker, multi-segment transcriptions instead of single placeholder
- New tests for date range search, session updates, multi-segment transcription
- All 36+ tests pass

### 6. reading-group-curriculum enhanced coverage (ORGAN-VI)
- New `tests/test_guides.py` with 9 tests covering guide generation, custom questions/activities, template management, export
- All 24+ tests pass

### 7. Sprint spec + doc updates
- This document
- sprint-catalog.md updated with FUNDAMEN entry and sprint count

## Metrics Delta

| Metric | Before | After |
|--------|--------|-------|
| Sprint count | 30 | 31 |
| Repos with README | 96/97 | 97/97 (alchemia-ingestvm) |
| Repos with seed.yaml (local) | 38/86 (44%) | 39/86 (45%) + 6 synced |
| Stale local clones | 6 | 0 |
| ORGAN-VI/VII test count | 60 | 85+ |
| alchemia-ingestvm CI | None | Python CI active |
| social-automation HTTP logic | Mock-only | Real urllib.request POST (Mastodon + Discord) |

## Files Changed

| File | Repo | Action |
|------|------|--------|
| `README.md` | meta-organvm/alchemia-ingestvm | Created |
| `seed.yaml` | meta-organvm/alchemia-ingestvm | Created |
| `.github/workflows/ci.yml` | meta-organvm/alchemia-ingestvm | Created |
| `src/mastodon.py` | organvm-vii-kerygma/social-automation | Modified |
| `src/discord.py` | organvm-vii-kerygma/social-automation | Modified |
| `src/posse.py` | organvm-vii-kerygma/social-automation | Modified |
| `tests/test_discord.py` | organvm-vii-kerygma/social-automation | Created |
| `tests/test_analytics.py` | organvm-vii-kerygma/distribution-strategy | Created |
| `src/sessions.py` | organvm-vi-koinonia/salon-archive | Modified |
| `src/transcription.py` | organvm-vi-koinonia/salon-archive | Modified |
| `tests/test_sessions.py` | organvm-vi-koinonia/salon-archive | Modified |
| `tests/test_transcription.py` | organvm-vi-koinonia/salon-archive | Modified |
| `tests/test_guides.py` | organvm-vi-koinonia/reading-group-curriculum | Created |
| `docs/specs/sprints/31-fundamen.md` | corpvs-testamentvm | Created |
| `docs/strategy/sprint-catalog.md` | corpvs-testamentvm | Modified |
