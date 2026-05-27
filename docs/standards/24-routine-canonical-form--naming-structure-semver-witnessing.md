# 24: Routine Canonical Form — Naming, Structure, SemVer, Witnessing

**Date:** 2026-05-27
**Status:** ACTIVE — applies to every Class-(I) routine (scheduled-tasks-MCP entries; future Class-(III) reusable workflows that invoke Claude)
**Derived from:** 2026-05-26 defect inventory (7 of 8 routines missing audit-log writes) + the user's framing "naming protocols & standards & structure & semver for both the routines but also as routines"
**Complements:** `17-branch-governance.md` (write contract), `18-scheduled-process-contract.md` (Rule #55a + §9 audit-log universal applicability), `19-two-org-consolidation-architecture.md`, `20-reusable-workflow-architecture.md`, `21-apps-surface-policy.md`, `22-essence-function-naming-convention.md` (general naming), `23-no-deletion-principle--alchemical-evolution.md`

---

## 1. Purpose & Scope

The system runs ~8 Class-(I) routines today. Without canonical form, the routines drift — different SKILL.md shapes, inconsistent audit-log discipline, no clear "what counts as a breaking change," no way to detect a routine that has stopped being conformant.

This document codifies four interlocking requirements:

1. **Naming** — task IDs + descriptions + label conventions
2. **Structure** — what every SKILL.md MUST contain (sections, ordering, frontmatter)
3. **SemVer** — versioning convention (when to bump major/minor/patch, what counts as breaking)
4. **Witnessing** — the routines that audit other routines for conformance (self-enforcement layer)

Together these make the routine surface **self-correcting**: a routine that drifts from canonical form gets flagged by the witness on its next run.

## 2. Naming protocol (extending doc 22)

### 2.1 Three coexisting name forms

Per the scheduled-tasks-MCP architecture, every routine carries THREE name forms:

| Form | Where | Pattern | Example |
|---|---|---|---|
| **taskId** | `{taskId}/SKILL.md` directory; MCP `list_scheduled_tasks` key | `<cadence>-<short-essence>` | `daily-pr-management` |
| **Description** | Frontmatter `description:` + sidebar label | `<essence>--<function>[-<cadence>] (<class>, v<semver>) — Class-(I) per docs/standards/22 …` | `pr-cascade--tier-merge-report (daily, v1.0.0) — Class-(I) per docs/standards/22 essence-function naming` |
| **LaunchAgent label** (Class-(II) only) | `~/Library/LaunchAgents/<label>.plist` | `com.${CONDUCTOR_LABEL_PREFIX}.<essence>--<function>-<cadence>` | `com.conductor.archive-summon--daily-md-scrub` |

The taskId is the audit-log key (preserves lookup history); the description is the canonical essence-function name (per doc 22); the LaunchAgent label encodes the conductor-author class.

### 2.2 Cadence-prefix vs cadence-suffix

Per doc 22 §4: **cadence is metadata, not identity** — so cadence appears as suffix in the canonical essence-function name (`pr-cascade--tier-merge-report-daily`). However, the taskId form keeps cadence as prefix for sidebar grouping (`daily-pr-management`). Both coexist; the description carries the canonical form.

### 2.3 Essence-suffix lexicon

Per the existing system, certain noun-phrases recur as essence suffixes:

| Essence noun | Use |
|---|---|
| `warden` | Bounded enforcement (`worktree-warden`, `repo-warden`, `stale-warden`) |
| `probe` | Read-only sensor that flags drift (`hook-drift-probe`) |
| `monitor` | Continuous-state observer (`irf-decay-monitor`) |
| `witness` | Self-audit routine that audits other routines (`scope-pattern-witness`, `apps-dormancy-witness`, `topology-witness`) |
| `auditor` | Periodic compliance check producing a 3-bucket report (`launchagent-auditor`) |
| `cascade` | Multi-phase write workflow with internal gating (`pr-cascade`) |
| `summarizer` | Reduces a time-window into a report (`commit-summarizer`) |
| `triage` | Sort-and-classify task (rarely standalone; usually compound) |

New essence nouns are allowed but require IRF-row justification (doc 24's own enforcement applies: an unrecognized essence noun is a `weekly-routine-conformance-witness` finding).

## 3. Structural standard (SKILL.md canonical shape)

Every Class-(I) routine SKILL.md MUST contain these sections in this order:

```markdown
---
name: <taskId>
description: <essence>--<function>[-<cadence>] (<class>, v<semver>) — Class-(I) per docs/standards/22 essence-function naming
---

## Version: v<semver>
## Status format: <status-pattern-spec>

## Audit log (start — invoke FIRST)
Run: `~/.local/bin/scheduled-task-audit-bookend <taskId> start`
Per docs/standards/18 §9, every Class-(I) fire must emit start + end entries regardless of writes.

## [Operate under clause — cite governing standards docs]

## Pre-flight
[List of required preconditions]

## Procedure

### Phase A: [enumerate / read]
### Phase B: [classify / analyze]
### Phase C: [report / safe writes]
### Phase D: [higher-authority writes] (if applicable)
### Phase E: [unified report] (if Phase D exists)

## What this task NEVER does
[Hard constraints per docs/standards/17 §10 hard-NEVERs]

## Audit log (end — invoke LAST, after the report)
Run: `~/.local/bin/scheduled-task-audit-bookend <taskId> end <status>`
where `<status>` follows the format declared above. Use hyphens; no whitespace.
```

### 3.1 Mandatory sections (the conformance witness checks)

| Section | Required? | Rationale |
|---|---|---|
| Frontmatter with `name:` + `description:` | YES | MCP needs name; description carries canonical essence-function form per doc 22 |
| `## Version: v<semver>` header | YES | Per §4 below |
| `## Status format:` header | YES | Declares the contract for the bookend-end `<status>` parameter |
| `## Audit log (start)` invocation | YES | Per doc 18 §9 invariant |
| Operate-under clause citing standards docs | YES | Routes durable authorization through docs 17 + 18 + 24 |
| Pre-flight section | YES | Surfaces required preconditions |
| Procedure section with phases | YES | Structures the work |
| What-this-task-NEVER-does | YES | Codifies hard constraints (mirrors doc 17 §10 pattern) |
| `## Audit log (end)` invocation | YES | Per doc 18 §9 invariant |

### 3.2 Optional sections

- `## Context` — why the task exists (often a memory-file reference)
- `## Failure semantics` — how partial failures cascade
- `## Higher-authority writes` — for Phase D Tier-3 work per doc 17 §10
- `## Cross-references` — other docs/routines this task relates to

## 4. SemVer convention

Versions encode: `MAJOR.MINOR.PATCH`

### MAJOR bump (vN → v(N+1).0.0)

A breaking change to behavior, interface, or downstream-readable contract. Examples:
- Changing the status format (breaks dashboards that grep `<status>`)
- Changing the taskId (breaks audit-log lookup history)
- Removing a write action (e.g., Tier-2 enablement removed from `daily-pr-management`)
- Removing a phase
- Tightening a write-class hard constraint (e.g., per-run cap reduced from 5 to 3)

### MINOR bump (v1.N → v1.(N+1).0)

Additive feature, no breaking change. Examples:
- New bucket added to classification (e.g., adding `STALE-PRUNABLE` to `daily-worktree-triage` Phase B)
- New optional flag or environment variable
- New canonical-replies template added
- Loosening a constraint (e.g., per-run cap raised)
- New phase added (additive only)

### PATCH bump (v1.0.N → v1.0.(N+1))

Bug fix, prompt clarification, no behavior change. Examples:
- Fixing a regex typo in the procedure
- Clarifying wording in the pre-flight section
- Updating a doc cross-reference path
- Adding missing audit-log entries to existing phases (the recent doc 18 §9 fix was a v0.1.0 → v1.0.0 MAJOR bump for the existing routines because the bookend-end status format is a new downstream contract)

### Version persistence

Version lives in the SKILL.md prompt header (`## Version: v1.0.0`) AND in the description (`(<class>, v1.0.0)`). Both must match. The conformance witness verifies match.

### Version-zero

New routines start at `v0.1.0` until shipped through their first scheduled fire successfully. After first successful fire, the conductor bumps to `v1.0.0` to signal "operational." Versions below `v1.0.0` indicate pre-flight; downstream consumers (the witnesses) should report-only-not-flag-defects on `v0.X.Y` routines.

## 5. Witnessing — the self-enforcement layer

Two Class-(I) witness routines audit Class-(I) routines (eating their own dog food):

### 5.1 `weekly-routine-conformance-witness`

**Cadence:** Weekly (Sunday 10:07 EDT — chosen to fall AFTER all daily-Sunday runs but BEFORE the new week starts)

**Purpose:** Read every active scheduled-task SKILL.md; verify each follows doc 24 §3 structural standard. Report violations.

**Status format:** `<R>-routines-<C>-conformant-<V>-violations`

**Checks (per routine):**
- Frontmatter has `name:` + `description:` ✓
- Description carries `(<class>, v<semver>)` marker ✓
- Prompt has `## Version: v<semver>` header matching description ✓
- Prompt has `## Status format:` header ✓
- Prompt has `## Audit log (start)` invocation ✓
- Prompt has `## Audit log (end)` invocation ✓
- Prompt has Pre-flight section ✓
- Prompt has Procedure with at least one Phase ✓
- Prompt has What-this-task-NEVER-does section ✓
- Essence noun matches doc 24 §2.3 lexicon OR has IRF-row justification ✓

**Violations report:** per-routine listing of which checks failed, with severity (missing-bookend = P0; missing-version = P1; unknown-essence = P2).

### 5.2 `weekly-audit-log-coverage-witness`

**Cadence:** Weekly (Sunday 10:09 EDT — staggered after conformance witness)

**Purpose:** Grep the last 7 days of audit logs; verify every active routine fired the expected number of times AND every fire produced a matching start+end pair.

**Status format:** `<R>-routines-<F>-fires-<P>-paired-<U>-unpaired-<M>-missing`

**Checks (per routine × per expected-day):**
- For each active routine + each day in the last 7 where the cron would fire: expect exactly one `start` entry + one `end` entry
- Missing pair → defect (routine didn't fire OR didn't bookend)
- `start` without `end` → mid-fire failure (routine crashed)
- `end` without `start` → corrupted log OR routine skipped its bookend-start (defect)

**Violations report:** per-routine + per-day listing of missing/unpaired entries with classification.

### 5.3 Recursion — the witnesses witness themselves

Both witnesses are themselves Class-(I) routines following doc 24. They:
- Are named per §2 lexicon (`witness` is a canonical essence noun)
- Carry `v1.0.0` versions per §4
- Bookend per doc 18 §9
- Will appear in each other's reports

Self-witnessing closure: if a witness stops firing or stops conforming, the OTHER witness will surface it next Sunday. The system catches its own audit-instrumentation defects.

## 6. Migration of existing routines

Per doc 23 §3 (no deletion; only alchemical evolution):
- Existing taskIds stay (preserves audit-log history)
- Descriptions get the `(<class>, v<semver>)` marker added in the next prompt update
- Prompt headers get the `## Version:` + `## Status format:` declarations added in the next prompt update

The 8 active routines as of doc 24's landing are at implicit `v0.1.0` until updated; the `weekly-routine-conformance-witness` will report all 8 as "version-zero, please bump after next successful fire" on first run.

A future session updates the 8 prompts to add the version + status format headers (low-effort batch — 8 update_scheduled_task calls). After that, the routines are at `v1.0.0` and the witnesses report `8-routines-8-conformant-0-violations`.

## 7. Status format conventions (canonical examples)

Per routine, the `<status>` parameter to `scheduled-task-audit-bookend end` follows a declared format. The conformance witness verifies the format declaration exists; doesn't verify (yet) that emitted statuses match the format.

| Routine | Status format |
|---|---|
| `daily-hook-drift` | `no-drift` \| `drift-detected-<event-types>` \| `error-<reason>` |
| `daily-repo-hygiene` | `<N>-repos-<U>-unpushed-<O>-orphan-<S>-stale-<P>-pushes` |
| `daily-pr-management` | `<N>-prs-tier1=<X>-tier2=<Y>-tier3=<Z>-writes=<W>` |
| `daily-worktree-triage-and-cleanup` | `<R>-repos-<W>-worktrees-<C>-removals-<D>-dirty-<L>-locked` |
| `daily-code-review` | `<N>-commits-summarized-<R>-repos` \| `no-commits-since-yesterday` |
| `weekly-irf-aging` | `<R>-rows-<A>-aging-<S>-shipped-<O>-overdue` |
| `weekly-sibling-scope-drift` | `<S>-scopes-<C>-cross-3plus-<P>-promotion-candidates` |
| `monthly-launchagent-audit` | `compliant=<C>-exempt=<E>-violation=<V>` |
| `weekly-routine-conformance-witness` | `<R>-routines-<C>-conformant-<V>-violations` |
| `weekly-audit-log-coverage-witness` | `<R>-routines-<F>-fires-<P>-paired-<U>-unpaired-<M>-missing` |

Future format extension: when a routine's status needs richer structure, bump MAJOR (per §4) and declare the new format.

## 8. Cross-references

- `${DOC_NAMING_CONVENTION}` (doc 22) — general essence-function naming; doc 24 §2 specializes for routines
- `${DOC_SCHEDULED_PROCESS_CONTRACT}` (doc 18) §9 — audit-log universal applicability that doc 24 §3 codifies as mandatory section
- `${DOC_BRANCH_GOVERNANCE}` (doc 17) §10 — write-action hard-NEVERs that doc 24 §3 codifies as mandatory section
- `${DOC_NO_DELETION}` (doc 23) — lifecycle vocabulary; doc 24 §6 (migration) uses "evolution" not "rewrite"
- `${CORPVS_ROOT}/.config/organvm.env` — `ROUTINE_*` env vars; doc 24 §2 names map to env values

## 9. The closure

After doc 24 + the 2 witnesses + the 8 SKILL.md prompt updates (to add `## Version:` + `## Status format:` headers) land:

- Every routine has a canonical form (§3)
- Every routine is versioned (§4)
- Every routine writes audit log (§5 + doc 18 §9)
- Every routine is audited by other routines (§5)
- Routines that drift get reported within 7 days
- Routines that fail to fire get reported within 7 days
- The system catches its own routine-defects

This is the self-correcting layer. The standards aren't *enforced by hooks at write-time* (too brittle); they're *audited by routines at fire-time* (catch-up rather than block). The witness pattern matches the alchemical evolution principle: nothing prevented at write; everything surfaced for amendment.

---

# AMENDMENT — extension sections §10-§13 (codified 2026-05-27)

The four sections below extend the canonical form with **sorting**, **extended metadata**, **frontmatter specification**, and **general governance**. Per doc 23 alchemical-evolution, these are ADDITIVE — §9 closure above remains intact as testament to v1.0.0; this amendment bumps doc 24 to v1.1.0.

## 10. Sorting — canonical enumeration order

When routines are listed (in MCP sidebar, in docs, in IRF rows, in audit-log summaries), the canonical order is:

```
1. daily-*    — alphabetized within cadence-class
2. weekly-*   — alphabetized within cadence-class
3. monthly-*  — alphabetized within cadence-class
4. ad-hoc     — no fixed cadence; alphabetized
5. retired/evolved testaments (per doc 23) — listed LAST as historical record
```

**Why cadence-then-essence:** cadence is the most-frequently-used filter ("what's firing this week?"); essence-name is the secondary search axis. Putting cadence first matches how the conductor mentally indexes the routines.

**Audit-log ordering:** chronological by timestamp (no opinion needed; TSV append-only).

**Per-doc ordering:** standards docs that enumerate routines (this doc §7, docs 18-22 cross-references) follow the canonical order above. Witness routines verify this in their reports.

## 11. Extended metadata (beyond frontmatter + description)

Every routine SKILL.md MUST contain a `## Metadata` block within the prompt with the following fields:

```markdown
## Metadata
- **Owner:** <conductor | organ-team-name>     (default: conductor `4444J99` / `4444jPPP`)
- **Class:** <I | II | III | IV>                (per the four-class taxonomy from doc 18 §X analog)
- **Cadence:** <daily | weekly | monthly | ad-hoc>
- **IRF row:** <IRF-XXX-NNN | -none-but-planned->  (justifies existence; analogous to Rule #55a (e))
- **Depends on:** <list of routines/tools this depends on | none>
- **Audit log path:** `~/.claude/scheduled-tasks/audit/YYYY-MM-DD.log`
- **Conformance:** docs/standards/24 v<semver>  (which version of the canonical-form spec the routine claims)
- **Last semver bump:** <YYYY-MM-DD> — <reason>
```

**Why these fields:**
- **Owner** — clarifies who can update/disable (default conductor; future shared routines might be team-owned).
- **Class** — places the routine in the four-class scheduling discipline; informs witness severity (Class-(I) absent-fire = P0; Class-(III) absent-fire = info-only since server-side).
- **Cadence** — redundant-with-taskId-prefix but explicit; supports future routines whose cadence isn't reflected in their taskId (e.g., event-triggered).
- **IRF row** — every routine must trace back to an IRF row that justifies its existence. Per Rule #55a (e) (LaunchAgent contract), extended here to all Class-(I).
- **Depends on** — surfaces inter-routine dependencies (e.g., `weekly-audit-log-coverage-witness` depends on all others). Witness uses this to detect "cascade defect" (a missing fire of A may explain missing fire of B that depends on A).
- **Audit log path** — explicit for verification (always the same canonical path; declaring it makes the dependency visible).
- **Conformance** — which version of doc 24 the routine claims to follow. When doc 24 bumps to v2.0.0 (breaking change), routines at v1.X conformance are flagged for migration.
- **Last semver bump** — date + reason for the most recent version change. Provides lineage per doc 23.

The conformance witness checks for presence of each field; missing field = P1 violation.

## 12. Frontmatter specification (exact YAML shape)

The SKILL.md YAML frontmatter is MCP-controlled (managed by `create_scheduled_task` / `update_scheduled_task`). The conductor doesn't edit it directly. But the CANONICAL form is:

```yaml
---
name: <taskId>
description: <essence>--<function>[-<cadence>] (<class>, v<semver>) — Class-(I) per docs/standards/24
---
```

**Required fields:**
- `name` — must match the directory name and the `<taskId>` used in audit-log bookends
- `description` — must follow the format:
  ```
  <essence>--<function>[-<cadence>] (<cadence-class>, v<semver>) — Class-(I) per docs/standards/24
  ```
  Where:
  - `<essence>--<function>[-<cadence>]` is the canonical essence-function name per doc 22 + doc 24 §2
  - `(<cadence-class>, v<semver>)` is the metadata marker: cadence-class ∈ {daily, weekly, monthly, ad-hoc}; semver per §4
  - `— Class-(I) per docs/standards/24` is the standards anchor

**Example:**
```yaml
---
name: daily-hook-drift
description: hook-drift-probe--settings-template-diff (daily, v1.0.0) — Class-(I) per docs/standards/24
---
```

**Optional fields:**

MCP doesn't currently support arbitrary frontmatter fields beyond `name` + `description`. Any extended metadata (per §11) lives in the prompt body, not frontmatter. If/when MCP gains custom-frontmatter support (e.g., `version:`, `class:`, `irf:`), doc 24 will be amended (v1.2.0+) to move §11 fields into frontmatter for cleaner machine-parsing.

## 13. General governance

### 13.1 Ownership

- **Default owner:** conductor (the human, identified by `4444J99` / `4444jPPP`).
- **Shared ownership** (future): a routine could be owned by an organ team (e.g., ORGAN-IV taxis team owns the orchestration routines). Requires explicit declaration in §11 `Owner` field + a `seed.yaml` entry in the routine-hosting repo.
- **Witness ownership:** the two witnesses (`weekly-routine-conformance-witness`, `weekly-audit-log-coverage-witness`) are conductor-owned and self-mutually-witnessed.

### 13.2 Change policy

- **Mutation surface:** `mcp__scheduled-tasks__update_scheduled_task` is the canonical mutation API. Direct edits to `~/.claude/scheduled-tasks/<task>/SKILL.md` are not authoritative (MCP may re-canonicalize).
- **Mutation authorization:** only the conductor can mutate. Scheduled tasks themselves cannot mutate other routines (per doc 17 §10 hard-NEVERs analog).
- **Mutation classes:**
  - PATCH bump → no IRF row required; bump version + declare in §11 `Last semver bump`
  - MINOR bump → IRF row update recommended (note the additive change in the row's body)
  - MAJOR bump → IRF row update REQUIRED + add `[SUPERSEDED ROUTINE: <old-form>]` testament per doc 23

### 13.3 Approval gates

- **New routine creation:** requires IRF row at creation time (mirrors Rule #55a (e) extended to all Class-(I)). The IRF row justifies the routine's existence and lists closure conditions.
- **Routine evolution to successor:** the predecessor routine is `enabled: false` with `[EVOLVED <date> INTO <successor>]` description (per doc 23). The successor routine's IRF row references the predecessor.
- **Routine deletion:** **forbidden** per doc 23 §1 (no-deletion principle). Only evolution to successor or transmutation-to-testament.

### 13.4 Lifecycle states

| State | Trigger | Marker |
|---|---|---|
| **NEW** | `create_scheduled_task` called | `v0.X.Y` in description; conformance witness reports info-only |
| **ACTIVE** | First successful fire + conductor bumps to `v1.0.0` | `v1.0.0+` in description; full conformance enforcement |
| **EVOLVED** | Routine's work merges into a successor | `[EVOLVED INTO <successor>]` description; `enabled: false` |
| **TESTAMENT** | Long-disabled routine retained as historical record | Stays in scheduled-tasks-MCP with `enabled: false`; never deleted |

### 13.5 IRF policy (extended Rule #55a (e) to all Class-(I))

Every active routine MUST have an IRF row that:
- Names the routine
- States its purpose (one-line)
- Lists closure conditions (under what circumstances would this routine retire — i.e., what successor would it evolve into?)
- References any related routines (dependents)

The 8 existing routines as of doc 24 v1.1.0 trace back to:
- `daily-hook-drift` → IRF-SYS-210
- `daily-repo-hygiene` → IRF-SYS-212 (rolled-up; merger of 3 prior routines)
- `daily-pr-management` → IRF-SYS-211 (rolled-up; merger of 2 prior routines)
- `daily-worktree-triage-and-cleanup` → IRF-SYS-212
- `daily-code-review` → no explicit IRF row (predates the canonical-form discipline) — file IRF-SYS-213 to remediate
- `weekly-irf-aging` → IRF-SYS-212
- `weekly-sibling-scope-drift` → IRF-SYS-173 (pre-existing; the routine instantiates the closure mechanism)
- `monthly-launchagent-audit` → IRF-SYS-211

The 2 new witnesses (`weekly-routine-conformance-witness`, `weekly-audit-log-coverage-witness`) trace to doc 24 §5 itself; IRF-SYS-213 (to be filed) will rollup their existence justification.

### 13.6 Doc 24 self-governance

This doc itself follows the lifecycle:
- v1.0.0 (codified earlier in this session) — initial form with §1-§9
- v1.1.0 (this amendment) — additive §10-§13; no breaking change to v1.0.0 consumers
- Future v1.2.0+ — frontmatter spec extension if MCP gains custom-frontmatter support
- Future v2.0.0 — would require breaking change (e.g., re-architecting witness pattern)

Per doc 23 §3.3 (Doc lifecycle): never overwritten; only superseded with cross-reference annotation.
