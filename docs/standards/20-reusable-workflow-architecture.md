# 20: Reusable Workflow Architecture

**Date:** 2026-05-27
**Status:** ACTIVE — codifies the elevated form's Class-(III) server-side workflow surface
**Derived from:** 2026-05-27 audit revealing ~140 cron entries across ~80 repos, dominated by duplicate fabrics (40× `stale.yml`, 25× `codeql.yml`, etc.); 47-workflow `${ORG_SYSTEM_TEMPLATE}` org repo carrying redundant scheduling
**Complements:** `17-branch-governance.md`, `18-scheduled-process-contract.md`, `19-two-org-consolidation-architecture.md`, `22-essence-function-naming-convention.md`

---

## 1. Purpose & Scope

The elevated form collapses ~140 scattered GH Actions cron entries into **8 canonical reusable workflows** in `${ORG_SYSTEM_TEMPLATE}/.github/workflows/`. Each per-repo workflow becomes a 5-line caller invoking the canonical reusable.

This document specifies:
- The 8 canonical workflows (essence-function-named per doc 22)
- Per-repo caller pattern
- Versioning convention (`@v1`, `@v2`)
- Migration path from per-repo bespoke workflows

## 2. The 8 canonical reusables

All live at `${ORG_SYSTEM_TEMPLATE}/.github/workflows/<name>.yml` — typically `${ORG_SYSTEM}/.github/.github/workflows/<name>.yml` after URL resolution.

| Env var | Filename | Trigger | Purpose |
|---|---|---|---|
| `${WF_STALE_WARDEN}` | `stale-warden--issue-pr-close.yml` | `workflow_call` (called by per-repo cron) | Close stale issues/PRs; uniform across all repos. Replaces 40× per-repo `stale.yml`. |
| `${WF_REPO_AUDITOR}` | `repo-state-auditor--unpushed-orphan-report.yml` | `on: push: branches: [main]` + `workflow_call` | Report per-repo state (ahead/behind, orphan plans, no-upstream branches) via issue comment or check-run. Replaces local-token `${ROUTINE_REPO_WARDEN}` (Phase B). |
| `${WF_PR_CASCADE}` | `pr-cascade--tier-merge-report.yml` | `on: pull_request: types: [opened, ready_for_review, synchronize, labeled]` | Promote drafts → ready, enable Tier-2 auto-merge, perform Tier-3 squash-merges. Replaces local-token `${ROUTINE_PR_CASCADE}`. Operates under `${DOC_BRANCH_GOVERNANCE}` Section 10. |
| `${WF_COMMIT_SUMMARIZER}` | `commit-summarizer--push-retrospective.yml` | `on: push: branches: [main]` | Invokes Claude API to summarize the push; opens an issue or posts a check-run with the summary. Replaces local-token `${ROUTINE_COMMIT_SUMMARIZER}`. |
| `${WF_METRICS_REFRESHER}` | `metrics-refresher--corpvs-daily.yml` | `on: schedule: cron: '0 6 * * *'` | Daily metrics refresh (existing in corpvs; lifts to reusable). |
| `${WF_SOAK_PROBER}` | `soak-prober--corpvs-daily.yml` | `on: schedule: cron: '0 8 * * *'` | Daily soak / health check (existing in corpvs). |
| `${WF_SYSTEM_PULSE}` | `system-pulse--corpvs-weekly.yml` | `on: schedule: cron: '0 12 * * 0'` | Weekly system pulse (existing in corpvs). |
| `${WF_ORGAN_AUDITOR}` | `organ-auditor--corpvs-monthly.yml` | `on: schedule: cron: '0 2 1 * *'` | Monthly per-organ audit (existing in corpvs; lifts to reusable). |

## 3. Per-repo caller pattern

Each repo's `.github/workflows/<workflow>.yml` becomes a 5-line caller:

```yaml
# .github/workflows/stale.yml — per-repo caller, ~5 LOC
name: stale
on:
  schedule: [ { cron: '0 9 * * 1' } ]
  workflow_dispatch:
jobs:
  call:
    uses: ${ORG_SYSTEM}/.github/.github/workflows/stale-warden--issue-pr-close.yml@v1
```

The literal value of `${ORG_SYSTEM}` is resolved at workflow-author time from the env file. A migration tool (`migrate-to-reusable-callers.sh`) is authored in a future session to convert existing 60-LOC per-repo workflows to 5-LOC callers.

## 4. Versioning convention

Reusables are tagged via Git: `@v1`, `@v2`, etc. on `${ORG_SYSTEM_TEMPLATE}` releases.

- `@main` allowed only for early development and per-repo workflows that explicitly opt into "always latest" (e.g., security-critical ones).
- `@v1` pinned by default; callers update to `@v2` by edit + commit.
- Breaking changes increment the major; backward-compatible changes within `@v1` are allowed.

Release cadence: tag `@vN` when ≥1 reusable changes in a backward-incompatible way. Otherwise patch-in-place under `@v1`.

## 5. Claude-invoking workflows (Class-(III) migration of class-(I))

Three workflows (`${WF_PR_CASCADE}`, `${WF_COMMIT_SUMMARIZER}`, `${WF_REPO_AUDITOR}`) invoke Claude via API in a GitHub Actions runner. Pattern:

```yaml
# Inside stale-warden, etc.
on:
  workflow_call:
jobs:
  invoke:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
    steps:
      - uses: actions/checkout@v4
      - name: Invoke Claude
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}   # org-level secret
        run: |
          # Use anthropic CLI or claude-code-action@beta to invoke Claude
          # with the same prompt body as the equivalent local SKILL.md
          ...
```

Org secret `ANTHROPIC_API_KEY` lives at `${ORG_SYSTEM}` org settings → Actions → Secrets. Single secret, shared across all reusables.

Cost: each fire = one Claude API session. At ~100K tokens/fire × $3/MTok input + $15/MTok output, ~$0.30/fire if active. Cap with `max_tokens` and `model: claude-haiku-4-5` for low-stakes fires.

## 6. Migration path (per-repo workflow → caller)

For each existing per-repo workflow at `<repo>/.github/workflows/<name>.yml`:

1. Check if a canonical reusable exists for the workflow's purpose
2. If yes: replace the file with the 5-LOC caller pattern (Section 3)
3. If no: leave as-is OR propose a new reusable for adoption

The `migrate-to-reusable-callers.sh` script (future) walks all repos under `${ORG_SYSTEM}` and proposes per-repo changes for conductor approval.

**Per-repo `stale.yml` × 40:** highest-leverage target. Single bulk migration: all 40 repos get the same 5-LOC `stale.yml` caller. Reduces ~40 cron fires/Mon to 1 (the reusable fires once per call but processes all 40 repos individually).

## 7. Out-of-scope for reusables

Some workflows stay per-repo because they're repo-specific:

- `actionlint.yml` (corpvs-specific configuration of `reviewdog/action-actionlint@v1`)
- `quality.yml` (portfolio-specific test/deploy pipeline)
- `pages.yml`, `pages-deploy.yml` (GitHub Pages publishing for the publishing repo)
- `dependabot-auto-merge.yml` (corpvs-specific merge rules)
- Anything truly bespoke per repo

These workflows don't migrate; they live in their owning repo's `.github/workflows/`.

## 8. Cross-references

- `${DOC_BRANCH_GOVERNANCE}` — Section 10 hard-NEVERs apply to `${WF_PR_CASCADE}` and `${WF_REPO_AUDITOR}` (any Claude-invoking workflow inherits the contract)
- `${DOC_SCHEDULED_PROCESS_CONTRACT}` — server-side runs are Class-(III), out of scope for Rule #55a but the (a)-(e) discipline applies analogously
- `${DOC_TWO_ORG_ARCHITECTURE}` — the topology this architecture assumes
- `${DOC_NAMING_CONVENTION}` — workflows named essence-function compound
- Phase 3 of the migration arc (per doc 19 Section 5) is the work that lands this architecture
