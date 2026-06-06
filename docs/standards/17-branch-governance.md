# 17: Branch Governance Standards

**Date:** 2026-05-26
**Status:** ACTIVE — applies to all ~148 repos across the eight-organ system + personal repos under `4444J99`
**Derived from:** In-session codification (S-2026-05-26 daily-review followups), authored to bound autonomous scheduled tasks
**Complements:** `10-repository-standards.md` (root hygiene), `13-organ-identity-and-placement.md` (organ assignment), `INST-INDEX-RERUM-FACIENDARUM.md` (work registry); supersedes ad-hoc branching practice

---

## 1. Purpose & Scope

This document codifies branch governance across the system **and serves as the durable authorization contract for scheduled automation that writes to GitHub state.** Any scheduled task that modifies branches, merges PRs, or pushes commits MUST cite this document and operate within its hard constraints (Section 10).

The contract is the safety. The constraints below — not the absence of writes — are what make scheduled PR automation acceptable under Universal Rule #29 ("never make the human look stupid") and the workspace CLAUDE.md "no main pushes without explicit per-session authorization" rule. **This document IS that authorization**, codified once durably rather than re-granted each session.

When in doubt at scheduled-run time: the task degrades to report-only. Never escalate beyond the contract.

---

## 2. Branch Models (taxonomy)

### Git Flow (Traditional)
- `main` (production-ready) + `develop` (integration)
- Feature branches: `feature/*`
- Release branches: `release/*`
- Hotfix branches: `hotfix/*`
- **Best for:** Scheduled releases, semantic versioning
- **Overhead:** Multiple long-lived branches, more ceremony

### GitHub Flow (Lightweight)
- `main` (always deployable)
- Feature branches off `main`, merged via PR
- Auto-deploy on merge
- **Best for:** Continuous deployment, rapid iteration
- **Overhead:** Minimal — assumes main is production-ready

### Trunk-Based Development (TBD)
- Single long-lived branch (`main`/`trunk`)
- Short-lived feature branches (hours, max 1–2 days)
- Frequent small merges, heavy CI/testing
- **Best for:** High-velocity teams, microservices
- **Overhead:** Requires mature CI/CD and testing discipline

### Environment Branching
- `main`, `staging`, `production` long-lived
- Deploy from different branches to different environments
- **Useful for:** Approval workflows, staged rollouts
- **Risk:** Branch drift if not carefully managed

---

## 3. ORGANVM default: GitHub Flow with tier-modulated protection

Across the eight-organ system, the default is **GitHub Flow**. Rationale: most repos are single-maintainer with continuous-deployment posture (the AI-conductor model), and the overhead of Git Flow's long-lived `develop` branch produces no value when there is no scheduled release cadence to gate.

**Per-tier protection modulates the strictness** (see Section 8). Tier-1 repos (the canonical/graduated set) get the strictest protections; Tier-3 (experimental/archived) get the most permissive.

`develop` may be used for repos that have a multi-stage deploy pipeline (e.g., `portfolio` uses `quality.yml` → `deploy.yml`); when used, treat as Git Flow per the rules in Section 4.

---

## 4. Branch Protection Rules

### `main` / `master` (all tiers)

```
✓ Require pull request reviews (Tier 1: 2+; Tier 2: 1+; Tier 3: 0+)
✓ Require status checks (tests, linting, security scans)
✓ Require branches to be up-to-date before merge
✓ Restrict who can push directly
✓ Auto-delete head branches after merge
✓ Allow force pushes: NO
✓ Allow deletions: NO
```

### `develop` (where used)

```
✓ Require PR reviews (1+)
✓ Require CI checks pass
✓ More lenient than main (since it's integration, not production)
```

### Branch-protection admin-bypass disclaimer

Per `reference_branch_protection_admin_bypass.md`: GitHub's `enforce_admins: false` allows the owner (`4444J99` / `4444jPPP`) to direct-push to protected branches. This bypass is **NOT** a license for scheduled tasks to push to main — the auto-mode classifier still blocks, and this document's Section 10 explicitly forbids the pattern. The bypass exists for the conductor's interactive use only.

---

## 5. Naming Conventions

```
feature/<description>          # New features
fix/<issue-description>        # Bug fixes
chore/<dependency-update>      # Maintenance, deps
refactor/<component-name>      # Code restructuring
docs/<what-docs>               # Documentation only
perf/<optimization-area>       # Performance improvements
test/<feature-coverage>        # Test additions
ci/<workflow-description>      # CI/CD changes
hotfix/<critical-fix>          # Production-critical (skips dev cycle)
```

Branches NOT matching one of these prefixes are **outside** the scheduled-task-eligible set and will be reported as "unclassified" by `daily-push-feature-branches` for the conductor to rename or close.

The 2026-05-26 corpvs feature branch (`daily-review-followups-2026-05-26`) is grandfathered as `<descriptive-slug>-<date>` — a date-suffixed compound. Going forward, prefer `feature/daily-review-followups` with the date in the PR title.

---

## 6. PR Review Protocol

- **CODEOWNERS** required for critical paths (`/governance/`, `/repo-registry.json`, `/.github/workflows/`, any `seed.yaml`).
- Auto-request reviewers by file path via `CODEOWNERS` syntax.
- Enforce **conventional commits** in PR title (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `perf:`, `test:`, `ci:`, `build:`, `revert:`).
- Block merges if reviews are **stale (>7 days)** — auto-detect via `gh pr view --json reviews`.
- Require **commit signing** for sensitive repos (Tier 1 + any repo with secrets management).

The `pr-review-toolkit:review-pr` skill is the canonical review workflow for human-in-the-loop reviews. The `/ultrareview` slash command is the canonical multi-agent cloud review (user-triggered, billed).

---

## 7. Merge Strategy

**ORGANVM default: squash + merge** for feature branches.

- **Squash + merge** — cleaner history; collapses WIP commits; recommended for all feature/fix/chore branches.
- **Create a merge commit** — preserves branch history; reserved for Git Flow release branches.
- **Rebase + merge** — linear history but rewrites commits; **forbidden** in shared branches; allowed only on solo branches before opening PR.

Per Universal Rule #11 (atomic commits): **before** squashing, ensure the PR title and body name the single `DONE-NNN` being closed. If multiple closures are inseparable, list them in the squash-commit body.

---

## 8. Repository Tier Classification

Tiers derive from `repo-registry.json` (single source of truth per workspace CLAUDE.md). Mapping:

| Tier | Registry-v2 criteria | Branch protection | Scheduled-task write authority |
|---|---|---|---|
| **Tier 1 (Core/Canonical)** | `status = GRADUATED` AND `tier ∈ {infrastructure, flagship, sovereign}` | Strictest: 2+ reviews, all checks, no force-push, signed commits | **Report only.** No autonomous writes. Human merges via `/ultrareview` or GitHub UI. |
| **Tier 2 (Standard/Active)** | `status ∈ {PUBLIC_PROCESS, CANDIDATE}` OR `tier = standard` | Standard: 1+ review, CI checks | Auto-merge **enablement** only (`gh pr merge --auto`). The merge itself fires only when CI + reviews + branch protection are satisfied — GitHub gates it, not the task. |
| **Tier 3 (Experimental/Archived)** | `status ∈ {LOCAL, ARCHIVED}` OR repo is solely authored by `4444J99` with no external contributors | Minimal: optional review, CI optional | Full auto-merge **perform** (`gh pr merge --squash`) when author is `4444J99` AND PR is approved (or no review required) AND CI is clean. |

Tier override: a repo's `seed.yaml` may declare `branch_governance_tier: <N>` to override the registry-v2 inference. Useful for repos that are technically Tier 3 by registry but should be treated as Tier 1 (e.g., a security-research repo where caution exceeds the scheduled-task contract).

Architectural review: any tier promotion or demotion of a repo requires updating `repo-registry.json` AND adding an IRF row (per `10-repository-standards.md`).

---

## 9. Cross-Repo Coordination

- Tag releases semantically (`v1.2.3`); use GitHub releases with auto-changelog generation.
- Dependency version pinning: pin to minor (`^1.2.0`) for internal deps; pin exact (`1.2.0`) for security-critical externals.
- **Deprecation timeline**: minimum 30 days between deprecation notice and removal; longer for Tier 1.
- Inter-organ dependency edges (per workspace CLAUDE.md "Unidirectional dependency flow: I → II → III") MUST NOT be crossed by automation; scheduled tasks scan and refuse if a PR introduces a back-edge.

---

## 10. The Scheduled-Task Contract (HARD CONSTRAINTS)

The following constraints apply to every scheduled task that writes to GitHub state — `daily-pr-promote-and-triage`, `daily-pr-execute-by-tier`, `daily-worktree-triage-and-cleanup`, `daily-push-feature-branches`, and any future task in this class.

Violation of any constraint below is a system bug, not a feature decision. Scheduled tasks MUST degrade to report-only if they cannot satisfy the constraints.

### Hard NEVERs (no override, no exception)

1. **NEVER force-push** to `main`, `master`, or `develop` on any repo, any tier.
2. **NEVER perform a direct `git push origin main`** (only `gh pr merge` or PR-mediated merges).
3. **NEVER auto-amend code** in response to review comments. Code changes ALWAYS require human-in-the-loop. Scheduled tasks may *rebase* a feature branch onto its base, but may not modify the code being merged.
4. **NEVER post substantive comment replies** in the author's name. Only **metadata replies** allowed: "rebased onto main", "CI passed, re-requesting review", "auto-merge enabled", "draft promoted to ready". The full allowed-replies whitelist is maintained at `~/.claude/scheduled-tasks/canonical-replies.md`.
5. **NEVER merge a PR with unanswered maintainer-other-than-author comments.** If any human other than `4444J99` / `4444jPPP` posted a comment newer than the most recent author response, the PR is human-gated.
6. **NEVER act on a PR whose title contains `WIP`, `DRAFT`, `[wip]`, `[draft]`, or `DO NOT MERGE`** — even if the PR is technically not in draft state.
7. **NEVER act on a Tier 1 repo** beyond reporting. Per Section 8.

### Per-run caps (stagger per Universal Rule #26)

- **Max 5** draft→ready promotions per task run
- **Max 3** auto-merges performed per task run
- **Max 3** metadata comments posted per task run
- **Minimum 60 seconds** between consecutive writes targeting different repos
- **Minimum 30 seconds** between consecutive writes targeting the same repo

### Mandatory audit trail

- Every write MUST be logged to `~/.claude/scheduled-tasks/audit/YYYY-MM-DD.log` in TSV: `timestamp\ttask-id\trepo\tpr-number\taction\tresult`.
- If the audit log path is not writable, the task aborts before any write.
- The conductor reviews the audit log weekly as part of `weekly-irf-aging` (Section 12 below).

### Failure semantics

- If any single write fails (auth, rate-limit, classifier-block, branch-protection rejection), the task **continues** with remaining candidates but **logs the failure** and **does NOT retry** within the same run.
- If three writes in a single run fail, the task **aborts** all remaining candidates and reports.
- The next scheduled run gets a fresh quota and a fresh state read; nothing is queued across runs.

### Authorization-by-reference

Each scheduled-task SKILL.md MUST cite this document by path and section:

```
This task operates under `docs/standards/17-branch-governance.md` Section 10.
Any action not explicitly permitted by Sections 8 + 10 is forbidden.
```

If this document is moved, renamed, or deleted, every dependent task fails its pre-flight check and degrades to report-only on next run.

---

## 11. Automation Standards

- **Renovate / Dependabot** for dependency updates; auto-merge enabled for patch-version bumps in Tier 2/3 repos with green CI; review required for minor/major bumps in all tiers.
- **GitHub Actions** for auto-labeling (by file path), auto-stale management (close after 90 days no activity, exempt `pinned` / `security`).
- **Branch auto-deletion after merge** — enabled across all repos.
- **Auto-rebase stale PR branches** — opt-in per repo via `.github/auto-rebase-bot.yml`; never enabled by scheduled tasks autonomously.

---

## 12. Cross-references

- Section 10 is enforced by: `daily-pr-promote-and-triage`, `daily-pr-execute-by-tier`, `daily-worktree-triage-and-cleanup`, `daily-push-feature-branches` (all at `~/.claude/scheduled-tasks/<name>/SKILL.md`).
- Per-tier scheduling cadence reviewed by: `weekly-irf-aging`.
- Audit-log review embedded in: `weekly-irf-aging`'s "shipped-but-open" category (a noisy audit log signals contract drift).
- Worktree-housekeeping context: `~/.claude/projects/-Users-4jp/memory/project_session_2026_05_23_worktree_housekeeping_enforcement_disposition.md` (the worktree problem that motivated `daily-worktree-triage-and-cleanup`).

---

## 13. Open extensions (future work, not blocking)

- **CODEOWNERS rollout** — currently only ~14/148 repos have CODEOWNERS files. Audit + fill is a separate IRF row (candidate IRF-OPS-NNN).
- **Conventional-commits enforcement** — bot in CI to reject non-conforming PR titles; out-of-scope for this document.
- **Tier override via seed.yaml** — Section 8 mentions `branch_governance_tier`; the seed.yaml schema needs an additive field, tracked separately.
