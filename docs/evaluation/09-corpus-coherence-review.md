# 09: Evaluation-to-Growth — Corpus Coherence Review

**Date:** 2026-02-09
**Status:** ACTIVE — audit trail for the post-cross-validation coherence pass
**Predecessor:** `08-canonical-action-plan.md` (canonical decisions D-01 through D-08)
**Framework:** Evaluation-to-Growth (E2G) — applied to the active Layer 3 planning corpus
**Agent:** Claude Opus 4.6

---

## Purpose

`08-canonical-action-plan.md` resolved all contradictions from the three-AI cross-validation cycle and made 8 human decisions (D-01 through D-08). However, the 7 documents it supersedes or updates still contained pre-decision language — rejected comparables, rejected grant targets, stale repo counts, and pre-Bronze scope descriptions. A reader entering the corpus from any document other than `08` would encounter contradictions that `08` has already resolved.

This document applies the Evaluation-to-Growth framework to the active Layer 3 corpus, providing:
1. **Evaluation** — what inconsistencies exist and where
2. **Reinforcement** — what's working well and should be preserved
3. **Risk Analysis** — what happens if these inconsistencies are left unresolved
4. **Growth** — the specific edits made to propagate `08`'s decisions

---

## 1. Evaluation: Inconsistency Inventory

### 1.1 Rejected Practitioner Comparables

**The problem:** `08` §6 explicitly rejects Holly Herndon, Zach Lieberman, and Gene Kogan as comparables ("too aspirational for current portfolio state"). `08` §7 provides replacements: Julian Oliver, Nicky Case, Hundred Rabbits. But 5 documents still reference the rejected comparables as if they were active positioning:

| Document | Location | Content |
|----------|----------|---------|
| `parallel-launch-strategy.md` | Lines 25–29 | 4-practitioner exemplar list (Herndon, Lieberman, Kogan, McCarthy) |
| `orchestration-system-v2.md` | Line 27 | "Holly Herndon, Zach Lieberman, Gene Kogan" in practitioner alignment |
| `public-process-map-v2.md` | Line 130 | "Herndon/Dryhurst, Lieberman, Kogan" connection reference |
| `public-process-map-v2.md` | Line 152 | "Herndon/Dryhurst (The Call), Lieberman (openFrameworks), Kogan (ml4a)" |
| `repo-registry.json` | Line 21 | `supporting_evidence` field with all 4 rejected names |
| `ANNOTATED-MANIFEST.md` (in `docs/`) | Lines 326, 338 | Practitioner precedents summary |

**Severity:** HIGH — external readers (grant reviewers, hiring managers) would encounter these names and check, finding the comparison doesn't hold at current portfolio scale.

### 1.2 Rejected NSF Convergence Accelerator Grant Target

**The problem:** `08` §6 rejects the NSF Convergence Accelerator program as "timeline misaligned" for a solo operator (requires team-led consortium). NSF as a general funding category is fine; it's the specific Convergence Accelerator program that's rejected. But 5 documents still list NSF alongside Knight/Mellon/NEA without qualification:

| Document | Location | Content |
|----------|----------|---------|
| `parallel-launch-strategy.md` | Line 101 | NSF in target funder list |
| `parallel-launch-strategy.md` | Lines 120–125 | Full NSF CA pitch paragraph |
| `implementation-package-v2.md` | Line 25 | NSF in strategic framing parenthetical |
| `implementation-package-v2.md` | Line 124 | NSF CA as specific target |
| `orchestration-system-v2.md` | Line 20 | NSF in grants parenthetical |
| `orchestration-system-v2.md` | Line 421 | NSF CA alignment claim |
| `public-process-map-v2.md` | Line 29 | NSF in grants parenthetical |
| `public-process-map-v2.md` | Line 148 | "NSF wants systems thinking" |
| `ANNOTATED-MANIFEST.md` (in `docs/`) | Line 329 | NSF in grant strategy summary |

**Severity:** MEDIUM — the NSF CA application pitch paragraphs could mislead the human operator into preparing an application that doesn't fit. Retention as annotated reference material is fine.

### 1.3 Stale Repo Count ("60+")

**The problem:** Multiple documents use "60+" as the repo count. The actual count is 44 registered repos in `repo-registry.json` + 14 local repos pending migration = 58 total. "60+" was a rough estimate that was never corrected. After `08`'s Bronze scoping (which focuses on flagships, not all repos), the inflated number is misleading.

| Document | Location | Content |
|----------|----------|---------|
| `parallel-launch-strategy.md` | Line 81 | "coordinating 60+ repositories" |
| `public-process-map-v2.md` | Lines 283–284 | "60+ repositories" in system overview |
| `public-process-map-v2.md` | Lines 375–376 | "60+ repos" in social media thread |
| `implementation-package-v2.md` | Line 100 | "60+ repos" in cover letter |
| `implementation-package-v2.md` | Line 479 | "60+ repositories" in pitch |
| `repo-registry.json` | Line 462 | Essay title "Across 60 GitHub Repositories" |
| `ANNOTATED-MANIFEST.md` (in `docs/`) | Line 528 | "60+ repos" in workflow deployment note |

**Severity:** MEDIUM — the number is verifiable (someone could count the repos). Precision matters for credibility with technical audiences.

### 1.4 Rigid Launch Criteria (Pre-Selection vs. Exploration-First)

**The problem:** `orchestration-system-v2.md` lines 100–107 specify rigid per-organ launch minima ("At least 3 flagship theory repos", "At least 3 flagship products with case studies"). `08` D-02 and D-07 explicitly reject pre-selection, deferring to exploration. The rigid counts contradict the exploration-first approach.

**Severity:** HIGH — these criteria would gate-block launch unnecessarily. A reader following `orchestration-system-v2.md` would think 3 flagships per organ are required; `08` says one per organ is sufficient for Bronze.

### 1.5 Monthly vs. Quarterly Audit Cadence

**The problem:** `orchestration-system-v2.md` specifies "Monthly audit" (line 294) and "Monthly audit runs successfully" (line 517). `08` §6 rejects monthly governance audits at launch: "Quarterly is sufficient. Monthly creates overhead with no audience."

**Severity:** LOW — affects operational planning but not external positioning.

### 1.6 Fixed Timeline References

**The problem:** `public-process-map-v2.md` line 6 says "Week 3-4 (parallel with other organs)". `08` D-08 replaces fixed timelines with success criteria: "Do not fix a sprint count."

**Severity:** LOW — one line, easily corrected.

### 1.7 Missing Back-Reference Banners

**The problem:** Five superseded documents lack any banner directing readers to `08`. A reader entering from `parallel-launch-strategy.md` or `orchestration-system-v2.md` would have no signal that these documents have been partially superseded.

**Severity:** HIGH — this is the primary navigation failure. Without banners, the corpus has no coherent reading path after `08`.

---

## 2. Reinforcement: What's Working

The corpus has several structural strengths that should be preserved:

1. **Layered architecture.** The Genesis → Planning → Execution → v2 Active layer model is sound. `08` sits cleanly at the top of Layer 3 as the canonical resolver.

2. **Document-level notes.** `parallel-launch-strategy.md` and `implementation-package-v2.md` already have header notes explaining their retained role. These just need expansion, not replacement.

3. **repo-registry.json as SSOT.** The registry's role as single source of truth is reinforced by `08`'s schema hardening decisions (SC-1).

4. **Cross-validation provenance.** The `gemini-cli/`, `codex-cli/`, and `github-copilot-cli/` directories are correctly frozen as source material consumed by `08`. No edits needed there.

5. **Archive discipline.** The `docs/archive/` directory convention is maintained — v1 files are frozen, v2+ variants live at root.

6. **`roadmap-there-and-back-again.md` as execution roadmap.** The phased plan structure (Phase -1 → 0 → 1 → 2 → 3) provides a clear temporal backbone.

---

## 3. Risk Analysis: Consequences of Inaction

If these inconsistencies are left unresolved:

1. **Portfolio credibility risk.** A grant reviewer or hiring manager encountering "60+ repositories" and then checking GitHub finds ~44. The Herndon/Lieberman comparisons invite scrutiny the portfolio can't yet support. These are self-inflicted credibility wounds.

2. **Operator confusion risk.** The human operator (who made the D-01 through D-08 decisions) will encounter pre-decision language when returning to these documents weeks later. Memory fades; the documents need to be self-consistent without remembering the decision process.

3. **AI agent confusion risk.** Future AI agents (including this one) working on Phase 1 execution will read these documents as instructions. Pre-decision language (monthly audits, 3 flagships per organ, NSF CA pitch) would generate incorrect work products.

4. **Scope creep risk.** The rigid per-organ launch criteria in `orchestration-system-v2.md` could pressure the operator to over-produce for Bronze, defeating the MVL purpose.

---

## 4. Growth: Edit Manifest

The following edits propagate `08`'s decisions across the active corpus. They are organized by priority (highest-impact inconsistencies first) and grouped by type for efficient execution.

### Priority 1: Replace Rejected Practitioner Comparables (7 edits, 5 files)

Replace Holly Herndon/Mat Dryhurst, Zach Lieberman, Gene Kogan, Lauren McCarthy with:
- **Julian Oliver** — artist-engineer, infrastructure focus, governance protocols
- **Nicky Case** — systems thinking, educational tools, documentation-first transparent process
- **Hundred Rabbits** (Devine Lu Linvega & Rekka Bellum) — small-scale sustainable creative infrastructure, extensive documentation

Each replacement includes an annotation: `(updated per 08-canonical-action-plan.md §7)`

**Files:** `parallel-launch-strategy.md`, `orchestration-system-v2.md`, `public-process-map-v2.md`, `repo-registry.json`, `ANNOTATED-MANIFEST.md` (in `docs/`)

### Priority 2: Remove/Annotate NSF Convergence Accelerator (9 edits, 5 files)

- Remove "NSF" from short target lists (where it appears alongside Knight/Mellon/NEA)
- Add deprecation annotation to NSF CA pitch paragraphs (retained as reference, not active strategy)
- Preserve NSF as a general category where context is appropriate

**Files:** `parallel-launch-strategy.md`, `implementation-package-v2.md`, `orchestration-system-v2.md`, `public-process-map-v2.md`, `ANNOTATED-MANIFEST.md` (in `docs/`)

### Priority 3: Fix Stale Repo Count (7 edits, 5 files)

Replace "60+" with "~44" (registered repos) or "~58 including local repos pending migration" where the broader count is contextually appropriate.

**Files:** `parallel-launch-strategy.md`, `public-process-map-v2.md`, `implementation-package-v2.md`, `repo-registry.json`, `ANNOTATED-MANIFEST.md` (in `docs/`)

### Priority 4: Fix Launch Criteria (1 edit, 1 file)

Replace rigid per-organ counts with `08`-aligned exploration-first language: "At least one fully documented flagship per organ (I–V mandatory, VI–VII at least stubs)."

**File:** `orchestration-system-v2.md`

### Priority 5: Fix Audit Cadence (2 edits, 1 file)

Replace "Monthly audit" with "Quarterly audit" per `08` §6.

**File:** `orchestration-system-v2.md`

### Priority 6: Fix Timeline Reference (1 edit, 1 file)

Replace "Week 3-4 (parallel with other organs)" with criteria-driven reference per `08` D-08.

**File:** `public-process-map-v2.md`

### Priority 7: Add Back-Reference Banners (5 edits, 5 files)

Add post-cross-validation banners to all superseded/updated documents, directing readers to `08`.

**Files:** `parallel-launch-strategy.md`, `orchestration-system-v2.md`, `implementation-package-v2.md`, `public-process-map-v2.md`, `roadmap-there-and-back-again.md`

### Priority 8: Resolve Narrative Tension in `08` (1 edit, 1 file)

Add audience-dependent narrative switching table reconciling D-04 ("meta-system first") with §7's "12 deployed products" insight.

**File:** `08-canonical-action-plan.md`

### Priority 9: Add Consistency Propagation Checklist to `08` (1 edit, 1 file)

Add §11 with a checklist tracking whether each superseded document has been updated. Transforms `08` from a decision record into a living consistency enforcement tool.

**File:** `08-canonical-action-plan.md`

---

## 5. Consistency Propagation Checklist

This checklist tracks the coherence pass. Each item corresponds to a specific edit in the manifest above.

### Comparables (Priority 1)
- [x] `parallel-launch-strategy.md` — exemplar list (lines 25–29)
- [x] `orchestration-system-v2.md` — practitioner alignment (line 27)
- [x] `public-process-map-v2.md` — connection reference (line 130)
- [x] `public-process-map-v2.md` — examples list (line 152)
- [x] `repo-registry.json` — `supporting_evidence` field (line 21)
- [x] `ANNOTATED-MANIFEST.md` (in `docs/`) — practitioner precedents (line 326)
- [x] `ANNOTATED-MANIFEST.md` (in `docs/`) — practitioner references note (line 338)

### NSF Convergence Accelerator (Priority 2)
- [x] `parallel-launch-strategy.md` — target funder list (line 101)
- [x] `parallel-launch-strategy.md` — NSF CA pitch (lines 120–125)
- [x] `implementation-package-v2.md` — strategic framing (line 25)
- [x] `implementation-package-v2.md` — specific target (line 124)
- [x] `orchestration-system-v2.md` — grants parenthetical (line 20)
- [x] `orchestration-system-v2.md` — NSF CA alignment (line 421)
- [x] `public-process-map-v2.md` — grants parenthetical (line 29)
- [x] `public-process-map-v2.md` — NSF wants systems thinking (line 148)
- [x] `ANNOTATED-MANIFEST.md` (in `docs/`) — grant strategy summary (line 329)

### Repo Count (Priority 3)
- [x] `parallel-launch-strategy.md` — line 81
- [x] `public-process-map-v2.md` — lines 283–284
- [x] `public-process-map-v2.md` — lines 375–376
- [x] `implementation-package-v2.md` — line 100
- [x] `implementation-package-v2.md` — line 479
- [x] `repo-registry.json` — line 462
- [x] `ANNOTATED-MANIFEST.md` (in `docs/`) — line 528

### Launch Criteria (Priority 4)
- [x] `orchestration-system-v2.md` — lines 100–107

### Audit Cadence (Priority 5)
- [x] `orchestration-system-v2.md` — line 294
- [x] `orchestration-system-v2.md` — line 517

### Timeline (Priority 6)
- [x] `public-process-map-v2.md` — line 6

### Back-Reference Banners (Priority 7)
- [x] `parallel-launch-strategy.md` — header area
- [x] `orchestration-system-v2.md` — header area
- [x] `implementation-package-v2.md` — header area
- [x] `public-process-map-v2.md` — header area
- [x] `roadmap-there-and-back-again.md` — header area

### Narrative Table (Priority 8)
- [x] `08-canonical-action-plan.md` — after §7, before §8

### Consistency Checklist (Priority 9)
- [x] `08-canonical-action-plan.md` — new §11

---

## 6. Verification Results

After all edits, the following grep checks were run against the active Layer 3 corpus (excluding `docs/archive/`, `00-a`, `00-b`, cross-validation directories, and `08` §6 rejection table):

| Check | Pattern | Target | Result |
|-------|---------|--------|--------|
| Rejected comparables | `Holly Herndon\|Lieberman\|Gene Kogan` | 0 hits in active docs | ✅ PASS |
| Stale repo count | `60\+` or `60 repo` | 0 hits in active docs | ✅ PASS |
| NSF CA annotations | `NSF.*Convergence` | All annotated or removed | ✅ PASS |
| Monthly audit | `Monthly audit` in orchestration | 0 hits | ✅ PASS |
| Back-reference banners | `08-canonical-action-plan` in headers | Present in all 5 files | ✅ PASS |

---

## 7. Reading Order Update

With this coherence pass complete, the recommended reading order for new readers is:

1. `08-canonical-action-plan.md` — Start here (canonical decisions, Bronze scope)
2. `09-corpus-coherence-review.md` — This document (audit trail)
3. `00-c-master-summary.md` — Executive summary (30 min)
4. `parallel-launch-strategy.md` — Strategic rationale (now with back-ref banner)
5. Remaining Layer 3 documents as needed

For the human operator returning to execution:

1. `roadmap-there-and-back-again.md` — Execution roadmap (Phase 0 → onward)
2. `08-canonical-action-plan.md` §3 — Bronze Sprint definition
3. `08-canonical-action-plan.md` §11 — Consistency propagation checklist

---

## Provenance

**Framework:** Evaluation-to-Growth (E2G), adapted for document corpus coherence review
**Trigger:** Completion of `08-canonical-action-plan.md` with 8 human decisions requiring propagation
**Total edits executed:** ~34 across 9 files
**New files created:** 1 (this document)
**Agent:** Claude Opus 4.6
**Human authority:** All decisions propagated originate from D-01 through D-08 in `08`, made by @4444j99 on 2026-02-09
