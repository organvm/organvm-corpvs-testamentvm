# 22: Essence-Function Naming Convention

**Date:** 2026-05-27
**Status:** ACTIVE — applies to all new conductor-authored artifacts (repos, scheduled tasks, LaunchAgents, workflows, scripts)
**Derived from:** Existing repo-naming pattern (`recursive-engine--generative-entity`, `peer-audited--behavioral-blockchain`, `vigiles-aeternae--corpus-mythicum`) extended as the universal naming discipline
**Complements:** `10-repository-standards.md` Section on naming, `19-two-org-consolidation-architecture.md`, `20-reusable-workflow-architecture.md`, `21-apps-surface-policy.md`

---

## 1. The convention

Every named artifact in the system carries two parts joined by `--`:

```
<essence-noun-phrase>--<function-verb-or-domain-phrase>[-<cadence-suffix>]
```

Where:
- **ESSENCE** is what the thing IS (a noun phrase, often Latinate/symbolic for substrate concepts)
- **FUNCTION** is what the thing DOES (verb or specific-domain phrase)
- **CADENCE-SUFFIX** is optional metadata (`-daily`, `-weekly`, `-monthly`) appended for scheduled artifacts

The double-hyphen separator is the existing canonical pattern from the eight-organ repo-naming standard.

## 2. Exemplars (existing system, getting it right)

| Name | Essence | Function |
|---|---|---|
| `recursive-engine--generative-entity` | engine (recursive) | generation of entities |
| `peer-audited--behavioral-blockchain` | blockchain (behavioral) | peer-audit of behavior |
| `vigiles-aeternae--corpus-mythicum` | eternal watchers | corpus of myths |
| `sema-metra--alchemica-mundi` | sign-measures | alchemy of the world |
| `INST-INDEX-RERUM-FACIENDARUM` | index | of things to be done |
| `organvm-corpvs-testamentvm` | corpus | testament/will |

The Latin substrate isn't required — it's a stylistic accent for the meta-system. Plain English works too if essence and function are both clear:

| Name | Essence | Function |
|---|---|---|
| `hook-drift-probe--settings-template-diff` | probe (hook-drift) | diff settings vs template |
| `pr-cascade--tier-merge-report` | cascade (PR) | tier-based merge + report |
| `worktree-warden--triage-clean-safe` | warden (worktree) | triage + safe-clean |
| `launchagent-auditor--rule55a-three-bucket` | auditor (launchagent) | rule-55a 3-bucket classification |

## 3. Anti-patterns (forbidden in new names)

| Bad | Why | Fix |
|---|---|---|
| `daily-pr-management` | Cadence-led ("daily-"); function vague ("management") | `pr-cascade--tier-merge-report-daily` |
| `do-stuff-tool` | No essence; no function | Reject; require both |
| `cleanup-script` | No specificity; "cleanup" is operational metaphor not function spec | `worktree-warden--triage-clean-safe` or similar |
| `daily-orphan-plans` | Cadence-led; "orphan-plans" is missing the verb | `orphan-plans-detector--commit-state-stale-classifier-daily` (now retired into `${ROUTINE_REPO_WARDEN}`) |
| `helper.py` | No essence + no function in filename | `<purpose>-helper--<what-it-helps-with>.py` |

## 4. Cadence-as-suffix, not prefix

Cadence is metadata, not identity. A routine that's currently daily might be weekly tomorrow; the routine's identity shouldn't change with its cadence.

| Forbidden | Allowed |
|---|---|
| `daily-hook-drift` | `hook-drift-probe--settings-template-diff-daily` (cadence as suffix) |
| `weekly-irf-aging` | `irf-decay-monitor--aging-shipped-windows-weekly` |
| `monthly-launchagent-audit` | `launchagent-auditor--rule55a-three-bucket-monthly` |

Cadence-suffix is optional; if the routine has no fixed schedule (event-triggered, on-demand), omit.

## 5. Env-variable indirection

Every literal name in every doc, script, workflow, plist, hook, and scheduled-task SKILL.md SHOULD become an env-var reference. The literal value lives ONCE in `${CORPVS_ROOT}/.config/organvm.env`.

Example:

```bash
# BAD — literal path scattered throughout the system
gh search prs --owner a-organvm --author "app/claude"
echo "see ~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-branch-governance.md"

# GOOD — env-var indirection
source "${CORPVS_ROOT}/.config/organvm.env"
gh search prs --owner ${ORG_SYSTEM} --author "app/${APP_PRIMARY_AGENT}"
echo "see ${DOC_BRANCH_GOVERNANCE}"
```

Renaming `a-organvm` → `organvm` becomes a one-line edit in `organvm.env`; every reference inherits.

## 6. Env-var naming itself

The env-var NAME captures essence (`ROUTINE_PR_CASCADE`, `WF_STALE_WARDEN`). The env-var VALUE captures the full essence-function compound (`pr-cascade--tier-merge-report`, `${ORG_SYSTEM_TEMPLATE}/.github/workflows/stale-warden--issue-pr-close.yml`).

Pattern:

```bash
# <CLASS>_<ESSENCE_WORD>="<essence>--<function>[-<cadence>]"
ROUTINE_PR_CASCADE="pr-cascade--tier-merge-report"
WF_STALE_WARDEN="${ORG_SYSTEM_TEMPLATE}/.github/workflows/stale-warden--issue-pr-close.yml"
LA_SUMMON_DAILY="${LA_LABEL_PREFIX}.archive-summon--daily-md-scrub"
```

Class prefix (`ROUTINE_`, `WF_`, `LA_`, `APP_`, `DOC_`, `ORG_`) categorizes by surface; essence word is the searchable handle.

## 7. Per-machine override

`${CORPVS_ROOT}/.config/organvm.env.local` (gitignored, per existing convention) overrides any value for that machine. A fork or staging instance can rename anything without touching canonical names.

## 8. Renaming flows one direction

Names live in `organvm.env`. References resolve from it. Renaming an entity = edit the env-var value. References inherit on next read.

Never two literal names in different places. If you find one, replace with `${ENV_VAR}` reference and add the env-var to `organvm.env`.

## 9. Migration of existing names

This convention applies to NEW artifacts. Existing names (e.g., `daily-pr-management`, `daily-hook-drift` as currently registered scheduled tasks) STAY as their existing IDs to preserve audit-log history; their descriptions get updated to use essence-function form for clarity. Renaming for renaming's sake is forbidden — only when there's an independent reason (recreate-from-scratch, name-collision, ID-readability blocking work).

Documented exception: when the migration arc (per `${DOC_TWO_ORG_ARCHITECTURE}` Section 5) reaches Phase 5 (repo transfer), repos with names that already follow the convention stay; those that don't get renamed alongside their transfer if practical.

## 10. Discoverability test

A stranger reading the env file alone should be able to:
1. List every scheduled routine in the system (grep `ROUTINE_*`)
2. List every shared workflow (grep `WF_*`)
3. List every LaunchAgent contract (grep `LA_*`)
4. List every canonical app slot (grep `APP_*`)
5. List every canonical doc (grep `DOC_*`)
6. Find the org topology (grep `ORG_*`)

If a name appears in the system but NOT in the env file, that's a violation: every name should be parameterized.

## 11. Cross-references

- `${DOC_TWO_ORG_ARCHITECTURE}` — uses this convention throughout
- `${DOC_REUSABLE_WORKFLOW_ARCHITECTURE}` — workflows named per this convention
- `${DOC_APPS_SURFACE_POLICY}` — apps slots named per this convention
- `${CORPVS_ROOT}/.config/organvm.env` — the canonical name registry
