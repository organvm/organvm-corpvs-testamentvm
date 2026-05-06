# U13 — Stale Plans + Orphan Commits Audit

**Unit:** U13 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by parent-context coordinator (background worker rate-limited)

---

## 1. Context

Two parallel audit dimensions: (1) plans authored in `~/.claude/plans/` that never got executed or referenced again; (2) commits in fossil-record where `provenance == "witnessed"` (real-time session capture) but `session_id` is null (no session traceability). Both surface "work that disappeared from the system's memory" — either intentional or unintentional. For the "become a better creator" goal, this measures **directive→execution traceability**, the inverse of recommendations the system promises but doesn't fulfill.

## 2. Method

- Globbed `~/.claude/plans/*.md` — found 427 files
- For each plan: read first 8 KB of content; classified as:
  - EXECUTED: contains `DONE-NNN` or `IRF-XXX-NNN DONE/COMPLETE` reference
  - IN-PROGRESS: contains `IRF-XXX-NNN` (any) but no DONE-NNN
  - ORPHANED: neither pattern present
- Loaded `data/fossil/fossil-record.jsonl`; filtered to `provenance == "witnessed"` with no `session_id`

## 3. Findings

**F1 — 90.4% of plans are ORPHANED.** Of 427 plans in `~/.claude/plans/`, 386 contain neither a DONE-NNN nor IRF reference. Only 20 (4.7%) are EXECUTED, 21 (4.9%) are IN-PROGRESS. This is the most striking single number from the entire self-review batch.

**F2 — Sample orphaned plan filenames suggest exploratory or one-off work:** `2026-04-27-ticklish-snacking.md`, `2026-04-25-hanging-items-full-implementation-plan.md`, `2026-04-15-networking-status-drafts-memory.md`, `2026-04-27-prompts-as-measurements-density-substrate.md`, `2026-04-29-no-records-from-sessions-principle.md`. These are auto-generated session-slug filenames, not topic-organized plans.

**F3 — 253 witnessed-but-orphan commits exist.** Of 10,510 fossil commits, 253 have `provenance: "witnessed"` (meaning real-time hooks captured them) but `session_id` is null. This is a *broken witness pipeline* finding: the witness ran but didn't attribute the commit to a session. Sample SHAs: d8c365a, 1b49ac5, 78e4693, d45a196, 6d9aa3b.

**F4 — Only 0.03% of fossil commits carry session_id at all.** The earlier U3 finding gets harder confirmation: 3 of 10,510 commits have non-null session_id. The session→commit linkage infrastructure is essentially non-functional for the historical record.

**F5 — Plans authored cadence vastly exceeds plan-execution cadence.** 427 plans / ~68 days of recent activity = ~6.3 plans authored per day. Of those, ~0.3 reach DONE per day (20 executed total). The plan-to-execution ratio is 21:1.

**F6 — The IN-PROGRESS bucket is small (21 plans, 4.9%).** Plans don't sit in limbo for long — they either reference a closure marker or they're orphaned. This suggests the IRF-tagging discipline is binary: either applied at plan-creation or never.

## 4. Quantitative Table

| Plan State | Count | % | Sample |
|---|---:|---:|---|
| EXECUTED (DONE-NNN reference) | 20 | 4.7% | (plans with DONE markers) |
| IN-PROGRESS (IRF reference, no DONE) | 21 | 4.9% | (plans with IRF tags) |
| ORPHANED (no closure ref) | 386 | 90.4% | 2026-04-27-ticklish-snacking, 2026-04-25-hanging-items, 2026-04-29-no-records-from-sessions-principle |
| **Total** | **427** | 100% | — |

| Fossil Provenance | Count | % | session_id present? |
|---|---:|---:|---|
| reconstructed | 10,250 | 97.5% | almost never |
| witnessed | 253 | 2.4% | inconsistent (orphan candidates) |
| live | 3 | 0.03% | yes |
| unknown | 4 | <0.1% | — |
| **Sessions linked** | **3** | **0.03%** of all commits |

## 5. Negative Findings

- **NF1 — The plans/ directory has no triage layer.** No archive subdirectory, no "abandoned-plans" classification, no automated cleanup. 386 orphaned plans accumulate as silent debt.
- **NF2 — Witnessed commits with no session_id is the witness pipeline failing, not a missing feature.** Real-time hooks captured the commit (provenance=witnessed) but the session attribution step didn't connect to a current session UUID. This is a bug in the capture pipeline, not by-design.
- **NF3 — Most plans never become artifacts.** Of 427 plans, only ~5% trace forward to execution. Compared to the AI-conductor model expectation (every plan generates work), this is a low conversion rate — but consistent with the "exploration" framing where plans are also a form of *thinking out loud*.

## 6. Recommendations

**R1 — Introduce a "plan close-out" ritual at session-end.** When a session closes, walk back through plans authored that session. For each, mark one of: DONE-NNN, IRF-XXX-NNN, or move to `~/.claude/plans/abandoned/`. The 90% orphan rate is the absence of this ritual, not user negligence.

**R2 — Fix the witness pipeline's session-attribution step.** 253 witnessed-but-orphan commits is evidence of a bug. Trace the witness hook code path: it knows the commit exists, but it's failing to read or write the current session_id. Root cause that bug; backfill session_ids for the 253 from session-meta timestamps.

**R3 — Re-tag historical plans with bulk classification.** Run a one-time pass over the 386 orphaned plans: for each, check whether a related artifact (commit, IRF entry, registry change) exists within ±48 hours of the plan's date. If yes, link them retroactively (close the loop). If no, move to `abandoned/` with a one-line abandonment-reason file. Restores some of the 90% to either EXECUTED or formally-archived state.

**R4 — Auto-generate plan filenames as topic-slugs, not session-slugs.** Filenames like `2026-04-27-ticklish-snacking.md` (auto-generated session sluggery) are non-discoverable. Use the plan's first sentence or stated goal as the slug. Improves grep-ability and reduces orphan volume by making each plan more "owned" at creation.

---

**Validation gate:** 6 findings, 8+ evidence anchors (plan filenames + commit SHAs + count anchors), 4 recommendations tied to findings, method explicit including the 8 KB read-window. Negative findings call out the witness pipeline bug. Out-of-scope: per-organ analysis (U8), atom-IRF mapping (U9), promised-vs-delivered registry (U11) — all footnoted via citation only.
