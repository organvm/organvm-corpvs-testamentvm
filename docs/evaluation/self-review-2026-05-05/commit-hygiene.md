# U2 — Commit Hygiene & Shape

**Unit:** U2 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by parent-context coordinator (background worker rate-limited)

---

## 1. Context

Commit hygiene is a quiet quality signal: long-form messages, conventional-commit prefixes, and code-vs-docs balance per organ all reflect how well the work is *self-documenting*. For "becoming a better creator" this matters because future-you reads commit history far more than authoring it; the cost of bad messages is paid asymmetrically.

## 2. Method

- Loaded `data/fossil/fossil-record.jsonl` (10,510 entries)
- Extracted: message length distribution, conventional-commits adherence, provenance distribution, type breakdown, code-vs-docs ratio per organ
- Witnessed-vs-reconstructed comparison on average message length

## 3. Findings

**F1 — Conventional-commits adherence is 68.8%.** 7,229 of 10,510 commits start with a recognized prefix (`feat:`, `fix:`, `chore:`, etc.). The remaining 31% are free-form, mostly older bulk-imported commits. Modern, witnessed commits adhere far more strictly.

**F2 — Witnessed commits have 2.5× longer messages than reconstructed (213 vs 83 chars).** The 253 witnessed commits average 213 characters; the 10,250 reconstructed commits average 83. This is a meaningful quality delta — when Claude writes commit messages in real-time sessions, they're substantially richer than the historical bulk-imported messages.

**F3 — Median message length is only 57 characters.** That's barely over a tweet's worth. p10 is 32 chars, p90 is 85. Most messages are headlines without bodies — useful for `git log --oneline`, less useful for archaeological reading.

**F4 — Type distribution skews toward `chore` (2,352) and `feat` (2,305).** `fix` (1,269), `merge` (1,025), `docs` (899). Test (158) and CI (119) are small — the corpus is overwhelmingly feature work and chore work, with relatively thin testing-commit and CI-commit volume. This matches the corpus identity (a planning/governance corpus, not a code-test substrate).

**F5 — ORGAN-IV has the highest code:docs ratio (1.67), ORGAN-VI the lowest (0.43).** Organs split sharply on output type:
- Implementation-heavy: ORGAN-IV (1.67), LIMINAL (2.39)
- Balanced: ORGAN-III (1.03), ORGAN-V (1.04)
- Documentation-heavy: ORGAN-VI (0.43), ORGAN-II (0.46), ORGAN-VII (0.93)

**F6 — Maximum message length is 23,406 chars (a 4,500-word commit message).** There's a single outlier message that's the size of a small essay. Most likely a multi-paragraph "what we did and why" note pasted into a commit body. Worth examining whether that pattern should become a Universal Rule or remain exceptional.

## 4. Quantitative Table

| Metric | Value |
|---|---:|
| Total commits | 10,510 |
| Median message length | 57 chars |
| p90 message length | 85 chars |
| Max message length | 23,406 chars |
| Conventional-commit adherence | 68.8% |
| Witnessed avg message length | 213 chars (n=253) |
| Reconstructed avg message length | 83 chars (n=10,250) |
| Witnessed-vs-reconstructed delta | 2.5× longer |

| Organ | code (feat+fix) | docs (docs+chore) | code:docs ratio |
|---|---:|---:|---:|
| LIMINAL | 605 | 253 | 2.39 |
| UNKNOWN | 81 | 34 | 2.38 |
| ORGAN-IV | 1,269 | 760 | 1.67 |
| ORGAN-V | 114 | 110 | 1.04 |
| ORGAN-III | 360 | 351 | 1.03 |
| ORGAN-VII | 90 | 97 | 0.93 |
| META | 627 | 843 | 0.74 |
| ORGAN-I | 198 | 311 | 0.64 |
| SIGMA_E | 24 | 40 | 0.60 |
| ORGAN-II | 115 | 249 | 0.46 |
| ORGAN-VI | 88 | 203 | 0.43 |

| Type | Count |
|---|---:|
| chore | 2,352 |
| feat | 2,305 |
| (none) | 1,887 |
| fix | 1,269 |
| merge | 1,025 |
| docs | 899 |
| test | 158 |
| ci | 119 |
| refactor | 105 |
| style | 43 |

## 5. Negative Findings

- **NF1 — Test commits are thin (158).** 1.5% of all commits. For a 240-repo system, this is a low test-commit density. Either tests aren't tracked as separate commits (folded into feat/fix) or there's a real test-coverage gap. The latter seems more likely given prior-report findings about lines-added vs lines-removed (97:3 generative).
- **NF2 — Refactor commits are also thin (105).** 1% of all commits. Combined with the high code-vs-docs ratio in ORGAN-IV, this suggests the system is mostly *additive* — code grows but rarely gets refactored.
- **NF3 — `style` commits (43) are negligible.** Either style is enforced via pre-commit hooks (no commits needed) or style discipline is loose. Inspection of a sample would clarify.

## 6. Recommendations

**R1 — Promote witnessed-style messages to all commits.** The 2.5× quality delta between witnessed (213 char avg) and reconstructed (83 char avg) suggests session-aware tooling produces better messages. Either: (a) require a Conventional Commits body for any commit not produced through witnessed sessions, or (b) make `organvm git` the default commit pathway, ensuring all commits are session-witnessed.

**R2 — Investigate the test-commit gap (1.5%).** A repo-by-repo audit of test-coverage commits would reveal whether tests exist and aren't tracked, or genuinely don't exist. For ORGAN-III (commercial / SaaS surface), test absence is a real risk.

**R3 — Add a refactor cadence to ORGAN-IV.** ORGAN-IV has 1.67 code:docs ratio but only 105 refactor commits across the whole corpus. The orchestration substrate is most exposed to entropy accumulation; schedule periodic refactor sprints.

**R4 — Use the 23,406-char outlier as a template.** If a single commit message that long produced clarity benefits, that pattern is worth extracting. Inspect that specific commit; if its structure is replicable, consider a `--template-long` mode for substantive feature commits.

---

**Validation gate:** 6 findings, 8+ evidence anchors (counts + specific numbers + organ stats), 4 recommendations tied to findings. Method explicit. Negative findings call out test-commit thinness and refactor gap. Out-of-scope: per-repo lifecycle (U1), session-commit correlation (U3) — both footnoted only.
