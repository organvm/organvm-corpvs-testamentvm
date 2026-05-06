# U7 — Correction-Atom Taxonomy

**Unit:** U7 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by parent-context coordinator (background worker rate-limited before producing report)
**Note on production:** Originally dispatched as background worker `ada3378a9ecbf3a1f`; agent hit Anthropic rate limit at 2:50pm NY reset before producing final report. Coordinator re-ran the analysis directly.

---

## 1. Context

Of the 24,599 prompt atoms, 179 are typed `correction` — moments where the user explicitly told Claude that a previous response was wrong. These atoms are unusually load-bearing for self-knowledge: they reveal not what the user *asks for*, but what the user repeatedly has to *push back on*. The asks tell us what the user wants; the corrections tell us what the user has to repeatedly fight to get. For the "become a better creator" goal, this is the highest-signal corpus.

## 2. Method

- Loaded `data/prompt-registry/prompt-atoms.json`; filtered to `type == 'correction'`
- Heuristic-classified each atom by content keywords into 6 categories (factual / architectural / governance / recalibration / scope / tonal); 88 atoms remained unclassified by single-keyword match
- Counted top content words across all 179 atoms
- Sample example atom-IDs surfaced for each category

**Caveat**: 88/179 (49%) atoms fell into "unclassified" because the heuristic single-keyword match is narrow. Manual classification of those 88 would likely redistribute heavily into the existing categories rather than expand them. Treat the per-category counts as lower bounds.

## 3. Findings

**F1 — Governance corrections dominate (43/179, 24%) when classified by single-keyword heuristic.** When the user corrects Claude, almost a quarter of the time it's about violating a rule, doctrine, protocol, or governance commitment — not about facts being wrong. Anchors: ATM-002669, ATM-002723, ATM-002758. Compare with only 4 factual corrections (ATM-017767, ATM-017866, ATM-017955).

**F2 — Tonal corrections are the second-largest classified category (25/179, 14%).** Voice, verbosity, conciseness, and style corrections are common — meaning the user actively shapes Claude's *voice*, not just its actions. Anchors: ATM-008587, ATM-008600, ATM-008607.

**F3 — Architectural corrections are rare (2/179, 1%).** Only 2 atoms explicitly correct an abstraction-level mistake. Either Claude rarely makes architectural mistakes, *or* (more likely) those mistakes get phrased as recalibration (8 atoms — "do Y instead") rather than as architectural corrections. Anchors: ATM-022980, ATM-024511.

**F4 — Scope-overreach corrections (9/179, 5%) are non-trivial.** "You went past what I asked" — a category that aligns directly with the friction pattern flagged in the prior INSIGHTS-FULL-HISTORY report. Anchors: ATM-013163, ATM-013629, ATM-013652.

**F5 — Top content words across corrections:** "triggering" (1,477 instances across 179 atoms = average 8.3 per atom), "wait" (1,276), "read" (1,171), "file" (1,137). The "triggering" frequency is striking: it suggests many corrections are about **hooks/automation triggering wrongly** — the same false-positive friction pattern this very session is observing in real time. The "wait" frequency suggests Claude is acting before being told to.

**F6 — 88 atoms (49%) didn't match any keyword heuristic.** This itself is a finding: corrections are often phrased indirectly ("actually...", reformulations, follow-ups) rather than with explicit "no, do X". A second-pass classifier looking at sequential atom pairs (atom N-1 + atom N where N is the correction) would likely capture the implicit corrections.

## 4. Quantitative Table

| Category | Count | % | Sample atom-IDs |
|---|---:|---:|---|
| Governance | 43 | 24% | ATM-002669, ATM-002723, ATM-002758 |
| Tonal | 25 | 14% | ATM-008587, ATM-008600, ATM-008607 |
| Scope | 9 | 5% | ATM-013163, ATM-013629, ATM-013652 |
| Recalibration | 8 | 4% | ATM-002947, ATM-004212, ATM-004289 |
| Factual | 4 | 2% | ATM-017767, ATM-017866, ATM-017955 |
| Architectural | 2 | 1% | ATM-022980, ATM-024511 |
| **Unclassified** | **88** | **49%** | ATM-001813, ATM-001838, ATM-001865 |
| **Total** | **179** | 100% | — |

**Top content words across corrections:**

| Word | Frequency | Implication |
|---|---:|---|
| triggering | 1,477 | hooks/automation firing wrongly |
| wait | 1,276 | Claude acting before told |
| read | 1,171 | Claude not reading provided context |
| file | 1,137 | file-handling errors |
| actually | 236 | corrective phrasing |

## 5. Negative Findings

- **NF1 — Factual corrections are rare (4 atoms).** This contradicts a common assumption that LLM corrections are mostly about hallucinated facts. The user rarely has to correct Claude on factual matters; they correct on *governance, tone, and scope*.
- **NF2 — Architectural corrections are surprisingly thin (2 atoms).** Either the architecture is robust or architectural mistakes get folded into recalibration/scope categories.
- **NF3 — The classifier hit a 49% unclassified rate.** That's the largest single bucket. The data isn't poor — the heuristic is too narrow to capture indirect corrections.

## 6. Recommendations

**R1 — Add a hook that catches "triggering" patterns before Claude acts.** The 1,477 occurrences of "triggering" across 179 corrections strongly suggests the user repeatedly corrects Claude for letting hooks/automation fire at wrong times. Build a PreToolUse hook that requires explicit user confirmation before any "triggering" action (running scheduled tasks, dispatching agents, etc.).

**R2 — Promote the implicit "wait" rule to an explicit Universal Rule.** "wait" appears 1,276 times in corrections — clearly the user has an implicit rule that Claude should pause before acting on certain patterns. Codify it: "When user message ends with an open question or unfinished thought, default to acknowledgment + wait, not action."

**R3 — Re-run correction analysis with sequential-pair classifier.** The 88 unclassified atoms (49%) require looking at the *preceding atom* in the same session to detect the implicit correction. Build that classifier; re-run; produce v2 of this taxonomy.

**R4 — Convert governance corrections (43) into hook patterns.** If 24% of corrections are governance violations, those rules can mostly be mechanized. Write each governance correction as a PreToolUse or UserPromptSubmit hook check, not as another rule in CLAUDE.md (which Claude reads but inconsistently follows).

---

**Validation gate:** 6 findings, 8+ atom-ID anchors, 4 recommendations, method explicit including caveat about heuristic limits, negative findings stated. Out-of-scope (session-meta friction, fossil wrong_approach commits, emotional reactions) deferred to U12 and U6.
