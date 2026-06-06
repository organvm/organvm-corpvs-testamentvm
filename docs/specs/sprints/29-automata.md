# Sprint 29: AUTOMATA

**Date:** 2026-02-17
**Focus:** Autonomous systems activation
**Status:** COMPLETE

## Problem

28 sprints completed, all internal. The autonomous infrastructure (11 workflows, 25 scripts) is ~80% built but largely dormant. The soak test runs in dry-run mode only, the distribution pipeline has a 1-label gap preventing auto-distribution, there is no auto-deployment, and no self-generating content. The user's goal — "eventually stop working altogether" — requires closing these gaps.

## Solution

Activate every dormant autonomous system. Close the essay-monitor → distribute-content pipeline gap. Add cron workflows for soak testing, metrics refresh, and system pulse generation. Create an auto-deploy workflow for the beta product. Write a one-time setup guide for the secrets that enable social distribution.

## Deliverables

### 1. Distribution pipeline gap closed
- `essay-monitor.yml` now creates issues with both `essay-detected` AND `ready-to-distribute` labels
- Issue body updated to reflect auto-distribution (removed manual checklist)
- **Impact:** Once distribution secrets are configured, every new essay auto-posts to social channels — zero human intervention

### 2. Auto-close for distributed issues
- `distribute-content.yml` now auto-closes issues after distribution completes
- Adds `distributed` label for tracking
- **Impact:** No manual issue cleanup — the pipeline is self-cleaning

### 3. Soak test cron workflow (`soak-test-daily.yml`)
- Daily at 08:00 UTC: runs `soak-test-monitor.py collect` (real data, no --dry-run)
- Sundays: also generates 30-day summary report
- Auto-commits snapshots to `data/soak-test/`
- **Impact:** Continuous health monitoring with zero human intervention

### 4. Auto-deploy for life-my--midst--in (`auto-deploy.yml`)
- On push to `master`: runs tests → deploys to Render via deploy hook
- Test gate prevents deploying broken code
- Gracefully skips if `RENDER_DEPLOY_HOOK` secret not configured
- **Impact:** Code changes deploy automatically after passing tests

### 5. System pulse generator (`system-pulse-generator.py`)
- Generates weekly markdown status report from automated data sources
- Pulls from system-metrics.json, soak test snapshots, registry, GitHub API
- Outputs structured report to `data/pulse/weekly-YYYY-MM-DD.md`
- **Impact:** Self-generating content — the system writes about itself

### 6. System pulse cron workflow (`system-pulse-weekly.yml`)
- Sunday at 12:00 UTC: generates pulse report, commits, creates distribution issue
- Distribution issue triggers POSSE pipeline → social media posts
- **Impact:** Fully autonomous content generation AND distribution

### 7. Metrics auto-refresh workflow (`metrics-refresh.yml`)
- Monday at 06:00 UTC: runs calculate-metrics.py + propagate-metrics.py
- Auto-commits any changes to system-metrics.json and whitelisted docs
- **Impact:** Metrics never go stale again

### 8. Autonomous setup guide (`docs/operations/autonomous-setup-guide.md`)
- Step-by-step for Mastodon, Discord, Render, LinkedIn, Ghost secret setup
- Verification commands for testing the autonomous loop
- Complete schedule table for all autonomous workflows

### 9. Sprint spec (`docs/specs/sprints/29-automata.md`)
This document.

## Key Decisions

- **Label bridging over event chaining:** Rather than creating a separate "bridge" workflow, simply adding `ready-to-distribute` to the essay-monitor's label list. One line change, maximum simplicity.
- **Test gate for auto-deploy:** Render can auto-deploy on push directly, but the workflow gives us the safety of "tests must pass first." Correctness over convenience.
- **Self-generating content via system pulse:** The pulse generator produces factual, data-driven reports — not creative writing. This avoids quality concerns while still creating regular social media presence.
- **Graceful degradation:** All workflows check for missing secrets and skip steps rather than failing. The system works incrementally as secrets are configured.

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Sprint specs | 28 | 29 |
| Autonomous cron workflows | 6 | 9 (+3: soak-test, pulse, metrics) |
| Distribution pipeline gaps | 1 (label gap) | 0 |
| Auto-deploy workflows | 0 | 1 |
| Self-generating content sources | 0 | 1 (system pulse) |
| Human tasks in distribution loop | 3 (label, review, close) | 0 |
| Scripts in corpus | 6 | 7 (+system-pulse-generator) |

## Autonomous Loop After Completion

```
DAILY:
  08:00 UTC — soak-test-daily.yml collects health data (auto-commits)
  09:00 UTC — essay-monitor.yml detects new essays → creates issue with ready-to-distribute
  09:01 UTC — distribute-content.yml fires → posts to channels → auto-closes issue

WEEKLY:
  Mon 06:00 UTC — metrics-refresh.yml recalculates + propagates metrics (auto-commits)
  Mon 07:00 UTC — orchestrator-agent.yml builds system graph
  Wed 10:00 UTC — distribution-agent.yml audits POSSE coverage
  Sun 08:00 UTC — soak-test-daily.yml generates weekly report (auto-commits)
  Sun 12:00 UTC — system-pulse-weekly.yml generates status → creates issue → auto-posts

MONTHLY:
  1st 08:00 UTC — promotion-recommender.yml evaluates status changes

ON PUSH (life-my--midst--in):
  auto-deploy.yml runs tests → deploys to Render
```

## What this sprint did NOT do

- Did not configure any external service secrets (that is one-time human setup per the setup guide)
- Did not deploy life-my--midst--in to Render (requires RENDER_DEPLOY_HOOK secret)
- Did not create social media accounts (human action per setup guide)
- Did not write essays (the pulse generator creates operational reports, not essays)
- Did not modify repo-registry.json (no status changes)

## Lessons

- **Activation > construction.** The autonomous infrastructure was 80% built but 0% activated. This sprint changed zero architectural decisions and wrote one new script — the rest was connecting existing pieces. The gap between "built" and "running" was smaller than expected.
- **One line can close the loop.** The entire distribution pipeline was blocked by a single missing label. The fix was literally one line: `['essay-detected']` → `['essay-detected', 'ready-to-distribute']`. Always look for the smallest change that unblocks the largest flow.
- **Graceful degradation enables incremental activation.** Every workflow checks for missing secrets and skips gracefully. This means the system can be activated one channel at a time, in any order, at any pace.
