# Closeout: S-2026-05-27 — Code Review → Generator Fixes → PR Backlog Triage

**Session:** code review of pulse/dashboard generators → fixes → runtime verification → open-PR backlog resolution
**Date:** 2026-05-27 | **Phase:** Complete

## Scope

Began as a `/code-review` (xhigh) of the `chore: system pulse report 2026-05-24` commit. Per user direction ("address all findings; full approval; commit & push; source returned improved"), it expanded into: fixing the surfaced generator defects, runtime-verifying them, then triaging and resolving the open-PR backlog toward "all green & main whole & evolved."

## Completed Work

- [x] Code review (xhigh, full coverage) of the pulse/dashboard generators — 13 findings (4 confirmed-medium, 4 confirmed-low, 5 plausible)
- [x] Fixed 8 generator defects in `scripts/system-pulse-generator.py`, `scripts/generate-dashboard.py`, `scripts/soak-test-monitor.py` and regenerated `data/pulse/weekly-2026-05-24.md` + `data/dashboard/index.html` → **#364 (merged)**
- [x] Runtime-verified generator fixes via sandboxed CLI execution (`/tmp/vt` with `ROOT`-relative copies): organs `10/10`, CI sums to 60 incl. billing-locked 11, prototype reconciliation, palette cycling for 10 organs, F12 negative case proven
- [x] Security: re-applied the shell-injection remediation in `promote-repo.yml` cleanly (couldn't merge #278 — no common merge base) → **#367 (merged)**
- [x] Runtime-verified the security fix at the shell surface (malicious label inert under env form; injects under old inline form)
- [x] Dependency currency: astro 5→6 (portfolio-site build green) → **#351 (merged)**
- [x] GitHub Actions version bumps re-applied cleanly (#324 corrupted: stale base + committed conflict marker) → **#372 (open)**
- [x] Cleared actionlint/shellcheck findings (SC2129, SC2034) the #370 guard surfaced in #372's touched files

## PR Dispositions

| PR | Disposition |
|----|-------------|
| #364 | **MERGED** — generator correctness fixes (`97fc6fa`) |
| #367 | **MERGED** — shell-injection remediation in promote-repo.yml; supersedes #278 (`39c5d1e`) |
| #351 | **MERGED** — astro 5→6 (`06a57b1`) |
| #278 | **CLOSED** — no merge base with main; superseded by #367 |
| #324 | **CLOSED** — corrupted (stale May-1 base, committed `<<<<<<< HEAD` marker, conflated doc drift); superseded by #372 |
| #372 | **OPEN** — action-version bumps + lint fixes; validate/portfolio-site/CodeQL green, actionlint re-running after fix |

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Re-apply (not merge) divergent branches #278, #324 | No common merge base / committed conflict markers; clean re-apply on current main is the only correct path |
| Merge the astro major #351 | The portfolio-site **build** passed on astro 6 — the real safety gate for a framework major |
| Clear shellcheck findings rather than weaken the actionlint guard | The guard (#370) is a deliberate shell-injection control; cleaning the workflows preserves strictness |
| Merge own verified PRs directly | All green + verified + reversible; advances "main whole" per explicit directive |

## What's Locked / Not Attempted

- **8 draft PRs** (other sessions' WIP): #356 (SOP-15), #357 (telos-beacon), #358 (conductor-handoff), daily IRF P0-surface bots #359/#360/#362/#363/#365 — not this session's to merge or close.
- **#338, #335** — other workstreams' analysis branches.
- **~100+ open issues** — governance/IRF work registry, including explicit DECISION items (#300 Revenue Agreement, #301 Node Architecture Lock) that require the owner.

## Follow-up Items (discovered this session)

1. **Security (same class as #367):** `distribute-content.yml` still interpolates `EXCERPT` and `ISSUE_URL` via inline `${{ steps.metadata.outputs.* }}` inside a `run:` block (the `TITLE` vector was removed in #372). These derive from issue/essay content — move to `env:` blocks in a focused follow-up security PR and audit the remaining workflows.
2. **Lint (latent):** `system-pulse-weekly.yml:39` has SC2086 (info) — unquoted expansion; not blocking #372 (untouched file) but will surface on any PR that touches it.
3. **Merge #372** once actionlint goes green.

## Verification Evidence

- Generators: `python3 scripts/system-pulse-generator.py --skip-api` and `generate-dashboard.py` against sandboxed fixtures — all fallback/edge branches exercised (missing `total_organs`, >8 organs, empty `per_organ`, missing `billing_locked`, manual-vs-computed word counts, missing META-ORGANVM → validation FAIL).
- Security: bash-surface differential — same malicious label string executes under the old inline form, inert under the new `env:` form.
- Actions bumps: all 7 workflows parse as valid YAML; no residual old action versions; actionlint+shellcheck clean on touched files.
