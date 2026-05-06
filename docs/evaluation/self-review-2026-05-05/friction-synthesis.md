# U12 — Cross-Source Friction Synthesis

**Unit:** U12 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by parent-context coordinator (background worker rate-limited)

---

## 1. Context

Three friction sources exist across the system: session-meta `tool_errors` and `user_interruptions` (515 sessions), facets `friction_counts` and `user_satisfaction_counts` (169 sessions analyzed), and fossil-record commits with revert/fix/oops messages (10,510 commits). This unit asks: do these signals correlate? Is there a unified friction profile, or are they three independent failure modes?

## 2. Method

- Loaded `~/.claude/usage-data/session-meta/*.json` (515 files): extracted `tool_errors`, `user_interruptions`, `duration_minutes`
- Loaded `~/.claude/usage-data/facets/*.json` (169 files): extracted `friction_counts`, `user_satisfaction_counts`
- Loaded `data/fossil/fossil-record.jsonl` (10,510 entries): filtered messages matching `\b(revert|fix|wrong|oops|rollback|undo)\b`
- Cross-correlated: for sessions with `tool_errors >= 5`, what is the dissatisfaction rate vs baseline?

## 3. Findings

**F1 — Sessions with `tool_errors ≥ 5` have a 33% dissatisfaction rate vs ~13% baseline.** Of 43 sessions with elevated tool errors, 14 also showed dissatisfaction signals — 2.5× the baseline rate. This confirms tool errors are a real friction driver, not just incidental noise.

**F2 — 1,921 fossil commits (18% of all commits) contain "fix/revert/wrong/oops/rollback/undo" in their message.** Almost 1 in 5 commits is a *correction commit*. This is the rate at which the codebase requires retroactive cleanup — high. Sample SHAs: from any organ's commit log filtering for "fix:" or "revert:".

**F3 — Top facet friction categories (across 169 analyzed sessions):**
- `wrong_approach`: 60 instances
- `buggy_code`: 48
- `misunderstood_request`: 25
- `user_rejected_action`: 14

The 60-vs-25 ratio between `wrong_approach` and `misunderstood_request` confirms what INSIGHTS-FULL-HISTORY found: Claude understands intent (low misunderstanding rate) but picks the wrong execution branch (high wrong-approach rate). 2.4× more execution-path errors than comprehension errors.

**F4 — 7 sessions had 3+ dissatisfaction signals.** That's a small but identifiable cluster of *bad sessions* — concentrated friction. These deserve targeted post-mortems rather than aggregate analysis.

**F5 — `hook_false_positives` (4 instances) and `tool_blocked` (3) are small but persistent.** The very session producing this report is hitting a hook false-positive in real time (the LaunchAgent substring guard firing on content that doesn't propose any LaunchAgent). The fact that it shows up in the facet friction data confirms this is a recurring system-level pathology, not session-specific.

**F6 — 43 sessions had `tool_errors >= 5` (8.3% of all 515 sessions).** Tool errors aren't rare — about 1 session in 12 has elevated error rates. Combined with F1, this means roughly 1 in 36 sessions delivers high-error AND-dissatisfaction.

## 4. Quantitative Table

| Friction Source | Volume | Cross-correlation |
|---|---:|---|
| Sessions with tool_errors ≥ 5 | 43 / 515 (8.3%) | 33% also dissatisfied (vs 13% baseline) |
| Sessions with user_interruptions ≥ 3 | (counted separately) | — |
| Facet `wrong_approach` | 60 | 2.4× misunderstood_request |
| Facet `buggy_code` | 48 | parallel to wrong_approach |
| Fossil revert/fix/oops commits | 1,921 / 10,510 (18%) | retroactive cleanup rate |
| Hook false-positives | 4 (and one occurring in this very session) | system-level pathology |
| 3+ dissatisfaction sessions | 7 | concentrated bad-session cluster |

## 5. Negative Findings

- **NF1 — `missing_context` and `incomplete_initial_work` are rare (3 each).** Claude rarely fails for lack of context — when failures happen, it's wrong-approach, not under-informed.
- **NF2 — `api_error` is small (6 instances, plus 4 `external_api_error`).** Most friction is *cognitive* (wrong choice, buggy logic) not *infrastructural* (network, rate limit). Note: this report was prompted in part by an actual API rate-limit incident truncating 11 of 13 worker agents — that incident IS in the data going forward but isn't yet captured in the 169 facets.
- **NF3 — Friction is bimodal: 7 high-dissatisfaction sessions out of 169 facets.** Most sessions are clean; bad sessions cluster.

## 6. Recommendations

**R1 — Throttle parallel-agent dispatch to avoid rate-limit cliffs.** Today's batch attempted 13 parallel background agents and 11 hit Anthropic's rate limit before completing. Rate-limit-aware dispatch (max 4-5 parallel, queue the rest) would have produced 13 successful reports instead of 2. This is a concrete behavioral change, not a hypothetical.

**R2 — Build a "wrong-approach early-detection" gate.** Since `wrong_approach` is 2.4× more common than misunderstanding, the lever is *before action*, not better intent-parsing. After Claude produces a plan but before executing, gate: "Is this approach the highest-leverage one given the user's stated goal?" Pre-execution sanity check, not post-hoc apology.

**R3 — Convert the 4 `hook_false_positives` into a hook self-test suite.** The substring-match guard for "LaunchAgent" fires on content that mentions but doesn't propose LaunchAgents. Build a small test suite: `hook_should_block(content)` returns True only if content actually creates a `~/Library/LaunchAgents/*.plist`. Substring matching is the wrong abstraction; semantic matching is the right one.

---

**Validation gate:** 6 findings, 8+ evidence anchors (session/facet counts + fossil totals), 3 recommendations tied to findings, method explicit, scope strict (no atom-stream corrections — those are U7's territory). Negative findings include direct observation of the rate-limit incident affecting this session's own batch.
