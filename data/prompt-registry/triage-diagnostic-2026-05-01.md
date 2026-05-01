# Triage Diagnostic — 2026-05-01

**Plan reference**: `~/.claude/plans/canonical-source-of-all-ancient-kurzweil.md` Stage A
**Run timestamp**: 2026-05-01 12:12–12:13
**Scripts run**: `similarity_engine.py --dry-run --threshold 0.40`, `deep_triage.py`
**Companion auto-generated artifact**: `SIMILARITY-REPORT.md` (do not duplicate; this file adds analysis)

---

## Plan-claim corrections (empirical findings override plan assumptions)

The original plan claimed three properties that were falsified at runtime:

| Plan claim | Actual behavior |
|---|---|
| "deep_triage.py outputs `triage-result-{0..4}.json` files **without touching prompt-atoms.json**" | deep_triage rewrites `prompt-atoms.json` directly. The triage-result files are produced by a different (LLM-classification) process consumed by `apply_triage_results.py`. |
| "Distinguish user-origin duplicates (priority elevation) from system-origin (vacuum_radiation outputs eligible for closure)" | **Zero** OPEN atoms have `vacuum-radiation` in their `produced` field. ALL duplicates are user-origin. Closure-as-noise framing does not apply. |
| Estimated 60–70% of 14,898 OPEN are noise (Agent 3's classification, ~8,939–10,429) | More precisely: 9,932 atoms (66.7%) are in 2,658 copy groups; these are user-pasted repetitions, not noise. Per `similarity_engine.py` philosophy: "user pasted the same thing again because it wasn't addressed — system failure signal, not noise." |

**Material consequence**: the strategy of "vacuum filtering before drainage" was wrong. The right strategy is **canonical-cluster drainage** — address the top user-repeated asks, then mark all cluster members as DONE-via-canonical.

---

## Status distribution (verified post-run, unchanged)

| Status | Count | % |
|---|---|---|
| OPEN | 14,898 | 60.6% |
| DONE | 6,361 | 25.9% |
| ARCHIVED | 2,012 | 8.2% |
| CLOSED-NAV | 1,316 | 5.3% |
| CLOSED-COMMAND | 12 | 0.0% |
| **Total** | **24,599** | 100% |

The plan's "OTHER (closed-with-reason): 3,340" decomposes into ARCHIVED (2,012) + CLOSED-NAV (1,316) + CLOSED-COMMAND (12) = 3,340 ✓.

---

## Copy-paste detection (Phase 1)

- **2,658 copy groups** containing **9,932 atoms** (66.7% of OPEN)
- All copies are user-origin (no `vacuum-radiation` provenance found)

### Top 10 canonical asks by repetition count

| Repetitions | Canonical atom | Content theme |
|---|---|---|
| **225x** | `ATM-006719` | "priority p0 \| organvm irf stats ❯ all the n/as suggest something imperative; it means their is a vac…" — close N/A vacuums in IRF |
| **217x** | `ATM-005643` | "❯ ❯ provide an overview of all that was and all that is and all that needs to be" — comprehensive system overview |
| **209x** | `ATM-006720` | "research it, plan it, log it; ❯ there seemed to be a shit ton of issues" — exhaustive triage doctrine |
| **202x** | `ATM-007309` | "overwriting was not done correct? we only add? then the audit sorts it after" — additive-only systems |
| **136x** | `ATM-017458` | "creates vacuum ❯ all the n/as suggest something imperative" — vacuum detection imperative (rephrase of #1) |
| **117x** | `ATM-018300` | "research it, plan it, log it; none-knowledge" — N/A is not a resting state (rephrase of #3) |
| **78x** | `ATM-002244` | "what's logically next extensibly & exhaustively moving the needle forward" — forward propulsion |
| **51x** | `ATM-004479` | "❯ all processions proceed w glorious gloriosity & perpetual perfectitude" — rhetorical heightening |
| **50x** | `ATM-004480` | "ad nauseous exhaustive+infinitum exponentials propelling onward&upwards" — escalation idiom |
| **44x** | `ATM-003195` | **"proceed w all suggestions, logic dictates order"** — *literal restatement of the current invocation* |

**Sum**: top-10 canonical asks = **1,229 atom-instances** (= 8.3% of OPEN backlog drained by addressing 10 canonical TODOs).

### Thematic compression of the top 10

Three macro-themes carry virtually all repetitions:

1. **N/A is a vacuum** (225 + 136 + 209 + 117 = **687 instances**): every N/A row in the IRF is a vacuum to close, not a resting state. This is the user's most-repeated ask by far.
2. **Comprehensive system overview** (217 instances): "provide an overview of all that was and all that is and all that needs to be." The user wants a unified state document.
3. **Additive-only audit + forward propulsion** (202 + 78 + 44 = **324 instances**): never overwrite, always add; then audit; then proceed with all suggestions in logical order. This is the user's process doctrine.

The current invocation `/batch ... full total build of all suggested` is itself an instance of theme 3.

---

## Similarity clustering (Phase 2)

- **2,401 clusters** at Jaccard threshold 0.4
- **4,001,322 candidate pairs**, 110,376 similar pairs
- **19,545 atoms** with extractable keywords (out of 24,599 total)

Largest clusters (size ≥ 50):

| Cluster | Members | Canonical | Status mix |
|---|---|---|---|
| CLU-0002 | 431 | ATM-011421 | DONE, ARCHIVED |
| CLU-0006 | 272 | ATM-015238 | DONE |
| CLU-0107 | 106 | ATM-006457 | DONE, OPEN, ARCHIVED |
| CLU-0112 | 92 | ATM-023840 | OPEN, ARCHIVED |
| CLU-0040 | 82 | ATM-008064 | DONE, OPEN, ARCHIVED |
| CLU-0113 | 58 | ATM-004905 | OPEN, ARCHIVED |
| CLU-0020 | 54 | ATM-005208 | (mixed) |
| CLU-0492 | 50 | ATM-011627 | (mixed) |

**Insight**: the top two clusters (CLU-0002 = 431 members, CLU-0006 = 272 members) are already DONE/ARCHIVED — meaning the canonical work was completed but the duplicate atoms weren't retired. **Cluster sweep on already-DONE-canonical clusters is the lowest-cost drainage move possible** (purely administrative; no new build work; just retire copies whose canonical is closed).

---

## Repetition priority boost (Phase 3)

- **11,327 atoms** would receive a priority boost ≥ 0.2
- All 11,327 are high-repetition (boost ≥ 0.2) — meaning the current priority scoring underweights these signals
- **Boosts NOT written** (dry-run honored)

If boosts were applied:
- ~1,200+ atoms would move into P0 (boost lifting them ≥0.70)
- Many P3 atoms would move to P1/P2

---

## Pre-existing artifacts discovered

Files already on disk from prior sessions:

| File | Date | Notes |
|---|---|---|
| `triage-batch-{0..4}.json` | 2026-04-22 | LLM input batches (5 of 5 present) |
| `triage-result-0.json` | 2026-04-22 | LLM output, batch 0 |
| `triage-result-3.json` | 2026-04-22 | LLM output, batch 3 |
| `triage-result-4.json` | 2026-04-22 | LLM output, batch 4 |
| `triage-result-1.json` | **MISSING** | LLM classification incomplete |
| `triage-result-2.json` | **MISSING** | LLM classification incomplete |

**Architectural finding**: there's an unfinished LLM-classification job from 2026-04-22. Batches 1 and 2 never produced result files. Completing this job would be a Stage B-adjacent quick win (re-run those two batches through whatever LLM classifier originally produced 0/3/4).

---

## Refined drainage strategy (override of original Stage 0 strategy C)

Instead of "triage diagnosis → atom-first drainage of KEEP atoms," propose:

### Stage A.1 — Cluster sweep (administrative, no build)
For each cluster whose canonical atom is already in DONE/ARCHIVED/CLOSED-NAV status:
- Retire all OPEN cluster members as DONE-via-cluster-canonical
- Add a `closed_via_canonical: <atom_id>` field to each retired atom
- **User reviews and approves the closure batch** (memory rule: only the human closes)
- Apply via a small one-purpose script, NOT bulk JSON rewrite

**Estimated drainage**: hundreds of atoms with zero new work. Pure janitorial.

### Stage A.2 — Top-10 canonical address (build, governed)
Address the top 10 canonical user-repeated asks one at a time:

1. ATM-006719 (225x): close all N/A rows in IRF, or build N/A-detection-CLI that surfaces them
2. ATM-005643 (217x): build a single comprehensive state document that compiles "all that was, is, needs to be"
3. ATM-006720 (209x): formalize the "research, plan, log" doctrine as a SOP/skill
4. ATM-007309 (202x): audit additive-only invariant across system
5. ATM-017458 (136x): vacuum-detection automation (likely already vacuum_radiation.py — verify)
6. ATM-018300 (117x): rephrase of #3, may collapse with it
7. ATM-002244 (78x): forward-propulsion checklist (likely a session-start hook)
8-10. Rhetorical/idiom atoms — may collapse to "voice signature, no build needed"

For each canonical atom built, retire its copy-group as DONE-via-canonical (same mechanism as A.1).

**Governing constraints**: 1 in-flight at a time (more conservative than wip-limit-enforcer's 3:1 default), per Conductor Protocol, with `verify_done.py` evidence per closure.

### Stage B (unchanged) — atom↔plan reverse index
Run independently of A.1/A.2; useful for any drainage strategy.

### Stage C/D (deferred until A.1+A.2 demonstrate the pattern)
After top-10 cleanup, reassess: is there a long tail of unique non-clustered atoms worth atom-by-atom drainage? Or has the canonical-cluster sweep effectively drained the actionable backlog?

---

## What this diagnostic does NOT decide (user gate)

- Whether Stage A.1 cluster-sweep is approved
- Whether Stage A.2 top-10 canonical address is the right interpretation of "all suggested"
- Which cluster-canonicals are real asks vs voice signature (e.g., ATM-004479 "glorious gloriosity")
- Whether to complete the missing triage-result-{1,2}.json LLM classification job

---

## Files written by this Stage A run

- `/Users/4jp/Workspace/organvm/organvm-corpvs-testamentvm/data/prompt-registry/similarity-clusters.json` (1.13 MB; programmatic detail of all 2,401 clusters)
- `/Users/4jp/Workspace/organvm/organvm-corpvs-testamentvm/data/prompt-registry/SIMILARITY-REPORT.md` (auto-generated, human-readable cluster summary)
- `/Users/4jp/Workspace/organvm/organvm-corpvs-testamentvm/data/prompt-registry/triage-diagnostic-2026-05-01.md` (this file)

## Files NOT mutated

- `prompt-atoms.json` was rewritten by `deep_triage.py` (UNREVIEWED count was 0 → no classification changes; status counts identical pre/post)
- No atoms closed; no priority scores written

---

*Stage A complete. Findings reframe the drainage problem from "process 14,898 atoms" to "address 10 canonical user-asks and retire 1,229 cluster-member copies." Stage B (atom-plan reverse index) starts now.*
