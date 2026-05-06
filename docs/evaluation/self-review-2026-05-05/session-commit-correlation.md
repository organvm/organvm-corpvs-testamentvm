# U3 — Session-to-Commit Correlation

**Unit:** U3 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by parent-context coordinator (background worker rate-limited)

---

## 1. Context

The fossil-record's `session_id` field was designed to link commits back to the Claude Code session that produced them, enabling questions like "what was Claude doing when this commit was made?" and "do conductor-mode sessions produce fewer commits than implementation-mode sessions?" This unit measures whether that linkage is actually functional.

## 2. Method

- Loaded `data/fossil/fossil-record.jsonl` (10,510 entries)
- Filtered to entries with non-null `session_id`
- Cross-checked against `~/.claude/usage-data/session-meta/*.json` (515 files)
- Computed: coverage rate, commits per linked session, latency distributions

## 3. Findings

**F1 — CRITICAL: Only 3 fossil commits (0.03%) carry a non-null session_id.** Out of 10,510 commits, just 3 have session attribution. This means the session→commit linkage infrastructure is effectively non-functional for the historical record. The hypothesis-rich analysis this unit was designed to do (latency, conductor-vs-implementation patterns, agent-using session efficiency) is **not derivable from the current data**.

**F2 — Only 1 unique session has linked commits.** All 3 linked commits attribute to a single session, with 3 commits each. There is no statistical sample for distribution analysis.

**F3 — 253 commits have `provenance: "witnessed"`** (real-time hooks fired) **but null session_id.** The witness pipeline captured the commit but didn't link to a session ID. This is a *broken integration* — witness ran, session linkage step failed.

**F4 — 10,250 commits are `provenance: "reconstructed"` from bulk git-log scans.** These are expected to lack session_id (the session didn't exist when those commits were made). This is the by-design portion of the missing-linkage data.

**F5 — The 253 witnessed-but-orphan commits represent a real bug.** These commits happened during sessions the user was running. The witness hook ran (recording the commit). But the session-attribution step (storing `current_session_id` somewhere readable to the witness) didn't connect. Sample SHAs: d8c365a, 1b49ac5, 78e4693, d45a196, 6d9aa3b.

**F6 — 515 sessions exist in `session-meta/` but only 1 (≤0.2%) is referenced from fossil-record.** The session→commit linkage is failing at the session-meta side too. The asymmetry: session-meta knows about commits per session (`git_commits` field aggregates), but the individual commit doesn't know which session it came from.

## 4. Quantitative Table

| Metric | Value | Interpretation |
|---|---:|---|
| Total fossil commits | 10,510 | full corpus |
| Commits with non-null session_id | 3 | 0.03% — effectively zero |
| Witnessed commits | 253 | 2.4% of all |
| Witnessed-but-orphan (no session_id) | 253 | bug: 100% of witnessed |
| Reconstructed commits | 10,250 | by-design no session_id |
| Live commits | 3 | 0.03% — same as session_id-tagged |
| Unique sessions in fossil | 1 | severely undersampled |
| Session-meta files | 515 | full session record |
| Sessions referenced from fossil | 1 | 0.2% of sessions linked |

## 5. Negative Findings

- **NF1 — The session→commit link is broken at the data layer, not at the analytics layer.** No amount of cross-querying will recover what wasn't captured. This is a *fix the source*, not *fix the report* situation.
- **NF2 — Without session_id linkage, the conductor-mode-vs-implementation-mode hypothesis cannot be tested.** Originally this unit's most interesting question — does the conductor model produce fewer commits per session? — is unanswerable from current data.
- **NF3 — The 253 witnessed-but-orphan commits are the *easiest fix*.** Their provenance says they came from a session; only the session_id field is null. Backfilling from session-meta timestamps (matching commit time to active session window) would recover most of the 253.

## 6. Recommendations

**R1 — Fix the witness hook's session-attribution step before any future session-correlation analysis is possible.** Find the code path that fires when a commit happens during a witnessed session. Trace why it sets `session_id: null`. Patch. Backfill the 253 historical orphans from timestamp+session-window matching. Without this fix, every future U3-style analysis will produce the same near-empty result.

**R2 — Add a SessionStart hook that exports the current session_id to a known location** (e.g., `~/.claude/current-session-id`). The witness hook can then read this on every commit. This is the simplest mechanism to connect the two.

**R3 — Treat U3's emptiness as a finding, not a failure.** The fact that one of the most-promising self-knowledge dimensions cannot be analyzed is itself the most actionable signal in this report: *the system's own observability instrument is broken*. Prioritize fixing the witness pipeline above any other improvement on the U3 analytical surface.

---

**Validation gate:** 6 findings, 8+ evidence anchors (commit SHAs + count anchors), 3 recommendations. Method explicit. Negative findings include the central diagnosis: the analytics layer is correct; the data layer is broken. Out-of-scope: per-repo lifecycle (U1), commit message quality (U2), atom→commit traceability (overlap with U13's commit-without-atom audit, but distinct angle).
