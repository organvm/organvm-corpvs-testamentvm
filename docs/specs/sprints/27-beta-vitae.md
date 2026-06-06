# Sprint 27: BETA-VITAE

**Date:** 2026-02-16
**Focus:** life-my--midst--in beta deployment preparation
**Status:** COMPLETE

## Problem

Sprint 25 (INSPECTIO) identified life-my--midst--in as the beta candidate — feature-complete, 291 tests passing, deployment blueprints written. But the product had never been run against a real database. The Neon project existed but contained only default `neon_auth` tables. No migration had been executed, no seed data loaded, and several migration-time bugs lay dormant.

Additionally, application materials across 9 files still referenced stale metrics from before sprints 22-26 (METRICUM through PROPAGATIO).

## Solution

Execute the full database provisioning pipeline (migrations + seeds), fix all bugs that surface, verify the API against the live database, write deployment documentation, reconcile application materials, and draft two essays for the bi-weekly cadence.

## Deliverables

### 1. Database provisioning (Neon)

- Ran 21 migration files against Neon project `in-midst-my-life` (damp-mouse-79328625)
- **44 tables** created in public schema: identity (7), CV (12), verification (8), commerce (7), content (6), operations (4)
- Seed data loaded: 2 profiles, 16 masks, 8 epochs, 8 stages, 12 settings, 1 task

### 2. Migration bug fixes

- **016_settings.sql:** `COALESCE()` inside `PRIMARY KEY` constraint is invalid in PostgreSQL. Fix: surrogate PK with functional unique index on `(profile_id, COALESCE(mask_id, '00000000-0000-0000-0000-000000000000'), key)`
- **002_masks.sql:** Missing `redaction` column queried by the repository layer. Fix: added `redaction JSONB DEFAULT '{}'::jsonb`
- **Seed ordering:** `covenant_personas.sql` depends on `profiles.sql` but ran first alphabetically. Fix: renamed to `y_covenant_personas.sql`

### 3. Auth prefix bug fix

- API registers routes at `/v1/` (canonical) and `/` (deprecated)
- Auth middleware checked request URLs against public route list without stripping the `/v1` prefix
- Versioned endpoints that should be public returned 401
- Fix: strip `/v1` prefix before matching against public/optional-auth route lists

### 4. render.yaml duplicate-services-key fix

- YAML had two `services:` top-level keys — second key (Redis) silently overwrote first (web/API/orchestrator)
- Fix: merged all services under single `services:` key

### 5. Deployment documentation (`DEPLOY.md`)

- Quick Start guide: Neon + Render recommended path
- Alternative: Vercel (web) + Render (API) hybrid
- Environment variables reference table (7 vars, 2 required)
- Database state snapshot (44 tables, seed data inventory)
- External service fallback documentation (Stripe mock, OpenAI mock, Sentry disabled)

### 6. Root render.yaml for Deploy Button

- Neon-optimized variant pushed to repo root (original at `infra/render.yaml` preserved)
- Removed `databases:` section (uses existing Neon)
- `generateValue: true` for JWT_SECRET and PROFILE_KEY_ENC_KEY
- `sync: false` for DATABASE_URL (user sets Neon connection string post-deploy)

### 7. Application materials reconciliation

- 9 files updated with current metrics (essay count, sprint count, code audit numbers)
- Stale references from pre-METRICUM era corrected

### 8. Essay drafts

- **#34:** "What It Takes to Ship a Product from Inside an Organ System" (product update, 2,800 words)
- **#35:** "Twenty-Six Sprints in Six Days" (sprint retrospective, 3,100 words)
- Both deployed to `organvm-v-logos/public-process/_posts/` (33→35 total essays)

### 9. Sprint spec (`docs/specs/sprints/27-beta-vitae.md`)

- This document

## Key Decisions

- **Neon over Render PostgreSQL:** Used existing Neon instance rather than provisioning Render's free PostgreSQL. Preserves the free DB allocation for other projects and keeps data in one place.
- **Surrogate PK over expression PK:** PostgreSQL doesn't support expressions in PRIMARY KEY constraints. Rather than restructuring the settings table, added a serial surrogate PK with a functional unique index to maintain the COALESCE-based uniqueness logic.
- **Seed file rename over ordering config:** The simplest fix for alphabetical ordering was renaming the file (`covenant_personas.sql` → `y_covenant_personas.sql`). A migration runner config would be cleaner but overkill for 5 seed files.
- **Two render.yaml files:** Root `render.yaml` (Neon variant) coexists with `infra/render.yaml` (self-contained). The infra version remains as documentation for the full managed-DB deployment path.

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Neon tables | 3 (neon_auth defaults) | 44 |
| Migration bugs | 3 (undiscovered) | 0 |
| Auth bugs | 1 (undiscovered) | 0 |
| render.yaml bugs | 1 (undiscovered) | 0 |
| Tests passing | 291 | 291 (no regressions) |
| Packages building | 7/7 | 7/7 |
| Deployment docs | 0 | 1 (DEPLOY.md) |
| Essay drafts | 0 | 2 (#34, #35) |
| Essays deployed | 33 | 35 |
| Application files with stale metrics | 9 | 0 |

## What this sprint did NOT do

- Did not deploy to production hosting (deployment prep only; user deploys via Render Blueprint)
- Did not configure custom domains or SSL
- Did not set up monitoring/alerting (Sentry, Grafana)
- Did not run integration tests against live Neon (unit tests only; API manually verified via curl)
- Did not modify repo-registry.json (no status changes)
