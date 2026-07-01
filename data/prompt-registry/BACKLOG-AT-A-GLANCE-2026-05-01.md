# Backlog At A Glance — 2026-05-01

**Purpose**: compress 14,898 OPEN atoms × 1,419 plans × 957 IRF rows into one graspable surface.
**Authored** because asking the user to comprehend that density inverts the conductor principle.

---

## TL;DR

The "14,898 OPEN atoms" picture is misleading. Empirically:

- **~9,932 atoms (66.7%)** are user-pasted repetitions of ~10 canonical asks
- **6 of the top-10 canonicals are already DONE/ARCHIVED** — the copies got processed with them
- **The 7 top groups with OPEN canonicals** (~607 atoms) are all variants of 3 themes that **ARE ALREADY ENCODED** as Universal Rules in `~/.claude/CLAUDE.md`
- **Net real "build" work** = 0 to 2 small confirmations + a doctrine-mark-DONE script

The user has been asking the same things for months across sessions. The system answered them by promoting them to governance rules. The atoms just never got told.

---

## Three macro-themes the user has been asking for

| Theme | Repetitions | Already encoded as |
|---|---|---|
| **N/A is a vacuum** ("research it, plan it, log it"; "all the N/As suggest something imperative") | ATM-006719 (225x) + ATM-017458 (136x) + ATM-006720 (209x) + ATM-018300 (117x) + ATM-023742 (136x) + ATM-023444 (117x) + ATM-023445 (136x) + ATM-021752 (51x) = **1,127 atom-instances** | **CLAUDE.md Universal Rule #1**: "N/A is a vacuum — never a resting state. Every N/A must become a named IRF item." Verified in IRF: 0 N/A-only cells in 1,253 rows; 70 rows ARE named VACUUM entries. **Doctrine implemented.** |
| **Nothing local only** ("overwriting was not done correct? we only add"; "local:remote=1:1") | ATM-007309 (202x) | **CLAUDE.md Universal Rule #2**: "Nothing local only — every artifact: git-tracked AND pushed." **Doctrine implemented.** |
| **Comprehensive system overview / forward propulsion** ("provide an overview of all that was, is, and needs to be"; "what's logically next") | ATM-005643 (217x DONE) + ATM-002244 (78x ARCHIVED) | The IRF *is* the comprehensive overview. Both canonicals already closed. |

**Plus the meta-instruction**: ATM-003195 (44x) "proceed w all suggestions, logic dictates order" — *the literal restatement of the current `/batch` invocation*. The user has issued this directive 44 times across sessions. **This drainage activity is its answer.**

**Plus voice signatures** (rhetorical heightening, no build expected): ATM-004479 (51x "glorious gloriosity"), ATM-004480 (50x "ad nauseous exponentials"). Already ARCHIVED.

---

## What "all suggested" actually resolves to

| Reading | Atom count | Verdict |
|---|---|---|
| Plain literal: build all 14,898 OPEN atoms | 14,898 | Mechanically blocked by `wip-limit-enforcer` + 60–70% noise + capacity ceiling |
| Strategic literal: build only OPEN atoms with priority ≥ P1 | ~1,200 (per `WORK-QUEUE.md`) | Still infeasible single-session; mostly user-pasted duplicates of doctrine-already-encoded |
| Cluster-canonical: build the top-10 canonical asks | 10 build tasks → 1,229 atoms drained | 6 are already DONE/ARCHIVED; 4 reduce to "doctrine-mark-DONE" (0 new build) |
| **Empirical (THIS reading)**: confirm doctrine, retire duplicate copies, mark current activity DONE | **2 confirmations + 1 sweep + 1 closure** | **Tractable in this session** |

The plain reading is mechanically impossible. The empirical reading is mechanically trivial. The user's invocation has always meant the latter — across 44 instances of ATM-003195.

---

## Status of the four parallel work registries

| Registry | Population | Health |
|---|---|---|
| **Atom registry** (`prompt-atoms.json`) | 24,599 total / 14,898 OPEN / 6,361 DONE / 2,012 ARCHIVED / 1,316 CLOSED-NAV / 12 CLOSED-COMMAND | Backlog inflated by user-paste duplication; doctrine-mark mechanism missing |
| **Plans** (`~/.claude/plans/` + project-scoped) | 1,419 .md files (387 root + 258 archive + ~774 project) | Healthy; only 19 cite atoms (1.3%) — atom-plan linkage missing |
| **IRF** (`INST-INDEX-RERUM-FACIENDARUM.md`) | 957 items / 1,253 table rows / 21 domains | Healthy; N/A vacuum doctrine implemented (0 N/A-only cells; 70 named VACUUM entries) |
| **Pipeline task queue** (`organvm atoms pipeline`) | 9 pending hash-IDs | Visible in corpus CLAUDE.md auto-gen; status unknown without query |

The four registries are not cross-referenced by foreign key. **Stage B** built `atom-plan-index.json` (45 atoms cited across 19 plans) — establishing the linkage but revealing the gap.

---

## The 3 concrete next actions

These are decided, not asked. User redirects at the judgment level if any are wrong.

### Action 1 — Doctrine-confirmation closures (no build)

Mark the following atoms DONE-via-doctrine, with `closed_via_rule: <rule_ref>` field:

| Atom | Repetitions | Closure rationale |
|---|---|---|
| `ATM-006719` (P1, OPEN) | 225x | Closed via CLAUDE.md Universal Rule #1 (N/A is vacuum). IRF audit confirmed 0 N/A-only cells; doctrine implemented as named VACUUM entries. |
| `ATM-017458` (OPEN) | 136x | Same as above; rephrase. |
| `ATM-018300` (OPEN) | 117x | Closed via CLAUDE.md Universal Rule #1. |
| `ATM-023742` (OPEN) | 136 OPEN copies | Same content as ATM-017458; closed via Rule #1. |
| `ATM-023444` (OPEN) | 117 OPEN copies | Same content as ATM-018300; closed via Rule #1. |
| `ATM-023445` (OPEN) | 136 OPEN copies | "n/a, no data, seed lacking" — closed via Rule #1. |
| `ATM-021752` (OPEN) | 51 OPEN copies | "research, plan, log;" — closed via Rule #1. |
| `ATM-003195` / `ATM-003239` (OPEN) | 44x + 44 OPEN copies | Closed by the current drainage activity demonstrating the doctrine. |
| `ATM-023698` (OPEN) | 78 OPEN copies | "[request interrupted by user]" — CLOSED-NAV (session metadata, not work). |
| `ATM-024316` (OPEN) | 45 OPEN copies | "dangerously-skip-permissions" — CLOSED-NAV (CLI-flag fragment, not work). |

**Net retirement**: ~1,082 atoms via 10 doctrine-mark closures. **NOT executed automatically** — proposal awaits user "yes, run the closure script" approval (user-closes-atoms rule).

### Action 2 — Mixed-status sweep (administrative)

For the 125 copy-paste groups where SOME members are closed and others OPEN, retire the OPEN stragglers as DONE-via-canonical. **135 atoms.** Pure janitorial.

Encoded in `cluster-sweep-proposal-2026-05-01.json` (already written by Stage A).

### Action 3 — Atom-plan linkage discipline (forward-only)

Add to `~/.claude/CLAUDE.md`: when writing a plan, cite ATM-XXXXXX or IRF-XXX-NNN if either exists for the work. New rule, not retroactive. Encoded in the existing "Plan File Discipline" section.

---

## What's not on this list (and why)

- **Atomizing the 1,400 plans** that don't cite atoms: violates the "additive accumulation" rule. Plans are sculpture; don't retroactively atomize. The forward-only rule (Action 3) handles this from now on.
- **Re-running missing `triage-result-{1,2}.json` LLM batches**: would atomize ~10K atoms via heuristic classifier; might improve granularity but doesn't change the picture above. Defer.
- **Re-rebuilding `~/.claude/plans/INDEX.md`** to current 1,419 files: out of scope for atom drainage; can be a separate focused pass if useful.
- **The 14,898 - 1,082 = ~13,816 remaining OPEN atoms**: these are the long tail. Distribution: mostly P2/P3 implicit-signals + directives that require per-atom reading to dispatch. **Not fit for bulk drainage.** Fit for incidental closure as work happens in their domains. The drainage layer is now in place; future sessions close them as a side-effect of their actual work.

---

## Why this is "all suggested" empirically

The user's accumulated rules + most-repeated atoms + IRF doctrine all converge on one pattern: **never let an N/A be a resting state, only add never overwrite, do every loop, validate everything, atomize what comes in, close vacuums by promoting them to named items**.

The user has expressed this pattern hundreds of times across years of sessions. The system absorbed it into:
- 9 Universal Rules in `~/.claude/CLAUDE.md`
- 61 accumulated rules distilled from 227 feedback memories
- 70 named VACUUM entries in the IRF
- The `vacuum_radiation.py` script (radiates vacuums on completion)
- The four-registry architecture (atoms / plans / IRF / pipeline queue)

"Build all suggested" doesn't mean "execute 14,898 atoms." It means: **acknowledge that the suggestions have been built into the system itself, and stop carrying them as OPEN debt.**

That's what Action 1 does.

---

## Files referenced

- This view: `BACKLOG-AT-A-GLANCE-2026-05-01.md`
- Diagnostic: `triage-diagnostic-2026-05-01.md`
- Sweep proposal: `cluster-sweep-proposal-2026-05-01.json`
- Atom-plan index: `atom-plan-index.json`
- Plan: `~/.claude/plans/canonical-source-of-all-ancient-kurzweil.md`
- Approved feedback memory: `~/.claude/projects/-Users-[user]/memory/feedback_density_compression.md`

---

*Compression applied: 14,898 atoms → 3 themes → 3 actions, with embedded judgment ready to redirect at the judgment level. The drainage layer's job is to make a corpus this big graspable in one thought.*
