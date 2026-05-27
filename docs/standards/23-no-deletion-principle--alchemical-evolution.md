# 23: No-Deletion Principle — Alchemical Evolution

**Date:** 2026-05-27
**Status:** ACTIVE — applies to every lifecycle transition across every surface (scheduled tasks, apps, repos, orgs, workflows, docs, plans, IRF rows, plist labels, branches)
**Derived from:** Universal Rule #3 (rules are additive), Universal Rule #34 (merge into ideal form, never replace), Universal Rule #60 (alchemy, not absorption — transitions are transmutation, not wrapping/migration), and the empirical observation that "retired" / "uninstall" / "drain" language smuggles deletion into amendment work
**Complements:** `19-two-org-consolidation-architecture.md`, `21-apps-surface-policy.md`, `22-essence-function-naming-convention.md`

---

## 1. The principle

**No deletion. Only amendment, evolution, alchemical update toward higher ideal forms.**

Every artifact in the system has a lifecycle. The lifecycle is **amendment-only**: an artifact can EVOLVE (its form transmutes), MERGE (it joins another), or BECOME-TESTAMENT (it persists as historical record of an earlier form). It never DISAPPEARS.

This is the meta-rule that governs how Rules 3, 34, and 60 manifest at every surface. It supersedes any locally-implied "delete" / "remove" / "drop" semantic.

## 2. The lifecycle vocabulary

Replace deletion-coded language with amendment-coded language across the system:

| Forbidden (deletion-coded) | Required (amendment-coded) |
|---|---|
| RETIRED | EVOLVED INTO `<successor>` / TRANSMUTED INTO `<successor>` |
| REMOVED | EVOLVED OUT OF `<slot>` |
| UNINSTALL | TRANSMUTE OUT OF SLOT (vendor evolves; slot persists) |
| DROPPED | MERGED INTO `<successor>` / FOLDED INTO `<successor>` |
| ARCHIVED | TRANSMUTED-TO-TESTAMENT (the form becomes its historical record) |
| DRAIN | TRANSFER (the contents flow; the vessel persists as testament) |
| DELETE | (NEVER. If you reach for this, you've misunderstood the lifecycle.) |
| DEPRECATE | SUPERSEDED BY `<successor>` (the deprecated form persists as testament) |
| SKIP | LATER (the work persists in the backlog; cadence shifts) |

## 3. Per-surface application

### Scheduled tasks

- A task whose work has merged into another task is **EVOLVED INTO** the merged form (not "retired"). Its SKILL.md persists. Its `lastRunAt` timestamp persists. Its description gets the `[EVOLVED <date> INTO <successor>]` tag.
- `enabled: false` is the mechanical implementation of the lifecycle transition. It does NOT mean "removed"; it means "this form has evolved into a different one that handles the work."
- Example: `daily-pr-promote-and-triage` + `daily-pr-execute-by-tier` were not "retired" — they **EVOLVED INTO** `daily-pr-management` which handles both phases in a single fire.

### Apps

- A slot's vendor is an **occupant**, not the slot's identity. When a vendor evolves out of a slot (e.g., switching `${APP_PR_REVIEWER}` from `sourcery-ai` to `coderabbitai`), the slot persists; the vendor's installation **TRANSMUTES OUT OF SLOT** but the vendor itself persists at GitHub-platform level (other users still use it).
- Per `${DOC_APPS_SURFACE_POLICY}` Section 4: the "UNINSTALL" list is more precisely "TRANSMUTE OUT OF SLOT — vendor was earlier occupant; slot now occupied by canonical vendor per doc 21 Section 2." The vendor's installation on the conductor's org is what evolves; the vendor itself persists at GitHub.
- Removing an app installation via `gh api -X DELETE /orgs/<org>/installations/<id>` is the mechanical implementation. The IRF row for the slot is amended with `[EVOLVED <date> from <old-vendor> to <new-vendor>]`.

### Repos

- A repo transferred via `gh repo transfer` PERSISTS — it just inhabits a different org. The transfer is a lifecycle event, not a deletion.
- A repo no longer actively maintained is **GRADUATED-TO-TESTAMENT** — `gh repo archive` makes it read-only-as-historical-record. Never `gh repo delete`.
- Per `${DOC_TWO_ORG_ARCHITECTURE}` Section 5 Phase 5: "repo transfer" is amendment (the repo evolves to inhabit a different org); the source-org's role correspondingly transmutes.

### Orgs

- A source org post-Phase-6 (per doc 19 § 5) is **TRANSMUTED-TO-TESTAMENT** via `gh org archive` (or equivalent). It persists at GitHub as historical record of the 10-org topology that preceded the 2-org elevated form. URLs continue to redirect.
- The 7 organ orgs + meta-organvm become testaments to the earlier era. They DO NOT get deleted. Anyone reading the system's history can trace `organvm-i-theoria` → archived 2026-XX-XX → repos transmuted to `${ORG_SYSTEM}` with organ tag preserved.

### Workflows

- A per-repo workflow whose work has migrated to a `${ORG_SYSTEM_TEMPLATE}` reusable is **EVOLVED INTO** the reusable. The per-repo workflow file becomes a 5-LOC caller (per doc 20 § 3) — the file persists; its content evolves.
- A reusable workflow superseded by `@v2` of itself is **EVOLVED**, with `@v1` persisting as testament until all callers migrate.

### Docs

- Per Rule #3 (rules are additive), standards docs are NEVER overwritten. A new doc may **SUPERSEDE** an old one; both persist. Cross-references in the new doc point to the superseded one with `[SUPERSEDED BY <new-doc-N>]` annotation.
- Doc 23 (this doc) doesn't delete or replace anything; it AMENDS the lifecycle vocabulary across docs 19-22.

### Plans

- Per Universal Rule #5 (plans are artifacts), plans are NEVER overwritten. Revisions get `-v2`, `-v3` suffixes. Superseded plans **MOVE TO** `plans/archive/YYYY-MM/` — they persist; their location evolves to reflect their inactive state.

### IRF rows

- An IRF row whose work has shipped gets the closure marker (`DONE-NNN`) in the row body. The row PERSISTS — IRF is a historical registry, not a TODO list.
- An IRF row that becomes irrelevant is **SUPERSEDED BY** a new IRF row that captures the changed scope. Both persist.

### Plist labels (Rule #55a context)

- A `com.${CONDUCTOR_LABEL_PREFIX}.<old-name>` LaunchAgent that gets transmuted to a new task name keeps its `.disabled` sentinel forever as testament; the new task gets a new plist with the new label.

## 4. The mechanical implementations

These are the operational verbs that EXPRESS the amendment principle. Use these, not their delete-coded equivalents:

| Lifecycle event | Mechanical implementation | Surface |
|---|---|---|
| Scheduled task evolves into successor | `update_scheduled_task enabled: false` + description tag `[EVOLVED <date> INTO <successor>]` | Class-(I) |
| LaunchAgent evolves into successor | `launchctl bootout` old; new plist gets new label; old plist file persists | Class-(II) |
| Reusable workflow @v1 evolves to @v2 | Author @v2 in same repo; tag both; callers migrate at their own pace | Class-(III) |
| App vendor evolves out of slot | `gh api -X DELETE /orgs/<org>/installations/<id>` for old vendor; install new vendor; update env var `${APP_<SLOT>}` value | Class-(IV) |
| Repo transfers to new org | `gh repo transfer <source>/<repo> <target>` (history preserved by GitHub) | Topology |
| Source org becomes testament | `gh org archive` (when GitHub supports it) OR manual mark-as-historical via org-profile README; never `gh org delete` | Topology |
| Plan supersedes earlier plan | Write new dated plan; move earlier to `plans/archive/YYYY-MM/` | Knowledge |
| Standards doc supersedes earlier | Author new dated doc; add `[SUPERSEDED BY ${DOC_<NEW>}]` annotation to earlier; both persist | Knowledge |

## 5. The audit log perspective

The audit log at `${AUDIT_ROOT}/YYYY-MM-DD.log` is, by Rule #3 + this doc, a perfect amendment-only log: every TSV row is APPENDED; rows are never modified or removed. The log file ITSELF is a daily testament; old days persist as testament to that day's runs.

When the audit log is the only record of a transmuted artifact (e.g., a scheduled task whose SKILL.md got rewritten on rename), it serves as the lineage trace. Searching `grep <old-task-id> ~/.claude/scheduled-tasks/audit/*.log` returns the history of an evolved form.

## 6. The "delete pressure" anti-pattern

Watch for moments where the conductor or an agent reaches for delete-coded language. Common pressure points:
- "Let's just remove the dormant apps" — *no, transmute them out of their slots; the slot persists*
- "Drop the old workflow" — *no, evolve it into a caller or fold it into the reusable*
- "Drain the source org" — *no, transfer the repos; the source org transmutes to testament*
- "Delete the retired tasks" — *no, the disabled SKILL.md files are the historical record*

When this pressure arises, route through the lifecycle vocabulary above. If the situation genuinely requires deletion (rare — usually a data-integrity emergency), file an IRF row articulating the deletion-justification before acting. Default to amendment.

## 7. The "everything is testament" frame

The elevated form treats every artifact in the system as having two phases:
1. **Active form** — the artifact serves a current purpose (a scheduled task fires; a repo holds active code; an app receives PR events)
2. **Testament form** — the artifact's active purpose has evolved into a successor; the artifact persists as historical record

Phase transitions happen via the lifecycle events in Section 4. The transition is LOSSLESS — the testament form retains everything the active form had, just with `enabled: false` or `archived: true` or equivalent.

This is the same principle as `git`: commits are never deleted, only superseded by new commits that reference them. The repo's history IS the testament trail. The elevated form extends this principle to scheduled tasks, apps, orgs, workflows, etc.

## 8. Application to past artifacts (retroactive amendment)

Items where this session used deletion-coded language (now amended):

| Artifact | Old language | Correct lifecycle phrasing |
|---|---|---|
| `daily-pr-promote-and-triage` + `daily-pr-execute-by-tier` | "RETIRED — merged into daily-pr-management" | "EVOLVED 2026-05-27 INTO daily-pr-management (merged Phase C+D into single task with 180s internal gate)" |
| `daily-orphan-plans` + `daily-unpushed-commits` + `daily-push-feature-branches` | "RETIRED — merged into daily-repo-hygiene" | "EVOLVED 2026-05-27 INTO daily-repo-hygiene (folded into Phase B+C+D of unified per-repo walk)" |
| ~21 dormant apps (per doc 21 § 4 "UNINSTALL" list) | "UNINSTALL" | "TRANSMUTE OUT OF SLOT (vendor evolves; slot persists for canonical-vendor occupancy per doc 21 Section 2)" |
| Source-org Phase 6 (per doc 19 § 5) | "archival" | "transmutation-to-testament — orgs persist as historical record of the 10-org topology that preceded the elevated form" |
| Scheduled-task "retired" descriptions | `[RETIRED 2026-05-27 — merged into <X>]` | `[EVOLVED 2026-05-27 INTO <X> — slot transmuted, lastRunAt preserved as testament]` |

The next mechanical step (separate commit) updates the 5 evolved scheduled-task descriptions to use the new lifecycle phrasing.

## 9. Cross-references

- Universal Rules #3, #34, #60 — the constitutional grounding
- `${DOC_TWO_ORG_ARCHITECTURE}` § 5 — Phase 6 amended in next pass
- `${DOC_APPS_SURFACE_POLICY}` § 4 — UNINSTALL list amended in next pass
- `${DOC_NAMING_CONVENTION}` § 9 — already aligned (renaming for renaming's sake forbidden; existing names preserved)
- `${CORPVS_ROOT}/.config/organvm.env` — naming is parameterized, so renaming is amendment-only
- `${IRF_INDEX}` — itself an amendment-only registry (every row persists; closure marked via DONE-NNN)
