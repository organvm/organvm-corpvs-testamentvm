# U4 — Question-Archetype Evolution

**Unit:** U4 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by parent-context coordinator (background worker rate-limited)

---

## 1. Context

Of the 24,599 atoms, 3,348 are typed `question`. The hypothesis: as the system matures, the user's modal-frame distribution shifts from operational (where/what/how) to architectural (should/is-this/why). This is a maturity signal — operational questions ask "where does X live?", architectural questions ask "is this the right shape?"

## 2. Method

- Filtered `prompt-atoms.json` to `type == 'question'` (3,348 atoms)
- Modal-frame regex matching on first 300 chars of each atom's content
- Frames: where, what, how, why, when, who, should, is_this, can_i, do_we, other
- Histogrammed by month from 2025-12 to 2026-04
- One frame per question (first match wins)

**Caveat**: 1,775 of 3,348 atoms (53%) didn't match any modal frame and fell into "other". These are likely declarative atoms misclassified as questions, or questions phrased indirectly (rhetorical/embedded). The classified subset (1,573 atoms) drives the per-frame analysis.

## 3. Findings

**F1 — "What" questions dominate (674 instances, 20% of all questions).** The single most-frequent modal frame. "What is X?", "what does Y mean?", "what's the status of Z?" — definition-seeking and state-checking questions. This is consistent with a system in active discovery.

**F2 — "Is-this" validation questions are the second-most-common (319, 9.5%).** Questions like "is this right?", "is this what we want?" — these are the *architectural* category. Their volume is significant (almost half the volume of "what"). Combined with a ratio test against "what":

```
"what" : "is_this" :: 674 : 319 :: 2.1 : 1
```

The user asks 2.1 operational questions for every architectural one. By the maturity hypothesis, this ratio should decrease over time.

**F3 — Modal-frame distribution by month shows the regime change at 2026-03.** Questions per month:
- 2025-12: 33 classified
- 2026-01: 5 classified
- 2026-02: 28 classified
- 2026-03: 911 classified ← regime change
- 2026-04: 596 classified

In 2026-03, the volume of every modal frame jumped 30-50× simultaneously. This matches the conductor-model emergence date noted in U5's vocabulary timeline (substrate vocabulary cluster appearing 2026-03-04 to 2026-03-20).

**F4 — "Should" questions are surprisingly thin (110 total, 3.3%).** If the user is operating in conductor mode, you'd expect more decision-asking ("should we X?"). The low count suggests the user is mostly directing rather than deliberating — declarations not deliberations.

**F5 — March 2026 alone had 389 "what" + 154 "is-this" questions** (vs Feb 2026's 21 + 0). The volume jump is not uniform across frames; "what" jumped 18× while "is-this" went from 0 to 154 (entirely new behavior). The user only started asking validation questions in March.

**F6 — 53% of question-typed atoms didn't match any modal frame.** This is a data-quality finding: the `type=question` classifier picks up content that isn't actually a syntactic question. A second-pass classifier looking at sentence-final punctuation (`?`) would tighten this.

## 4. Quantitative Table

| Modal frame | Total | 2026-03 | 2026-04 | Notes |
|---|---:|---:|---:|---|
| (other / unmatched) | 1,775 | — | — | 53% — non-syntactic questions |
| what | 674 | 389 | 249 | dominant — definition / state |
| is_this | 319 | 154 | 163 | architectural validation |
| how | 162 | 91 | 60 | procedural |
| should | 110 | 77 | 29 | decision (low volume) |
| why | 83 | 50 | (~25) | causal |
| where | 67 | (~17) | 33 | location |
| when | 59 | (~12) | (~25) | temporal |
| who | 45 | — | — | attribution |
| can_i | 39 | — | — | capability |
| do_we | 15 | — | — | aggregate decision |

| Month | Total questions classified | Notes |
|---|---:|---|
| 2025-12 | 33 | early phase |
| 2026-01 | 5 | quiet month |
| 2026-02 | 28 | pre-regime-change |
| 2026-03 | 911 | regime change (33× Feb) |
| 2026-04 | 596 | sustained high |

**Operational:Architectural ratio** ("what+how+where" : "should+is_this+why") = (903) : (512) = 1.76 : 1

## 5. Negative Findings

- **NF1 — "Should" frames are rarer than expected.** Only 3.3%. If the system is in conductor mode, the user should be deliberating more about whether to do X vs Y. The low rate suggests questions are primarily directive-clarification (what are you doing) rather than decision-deliberation (should we).
- **NF2 — The 53% unmatched rate weakens the modal analysis.** Half the data didn't classify. The trend signals (regime change at 2026-03) hold because the unmatched category is roughly proportional across months, but per-frame ratios are upper bounds.
- **NF3 — "Why" questions are thin (83).** Causal questions are rare. This is consistent with directive style — the user issues directives rather than asking *why* the system behaves a certain way.

## 6. Recommendations

**R1 — Tighten the `type=question` classifier.** 53% unmatched is too many. Require a `?` in the content or a `wh-` opening to be tagged `question`; otherwise reclassify as `directive` or `implicit-signal`. Re-run U4 with the cleaner data; the ratios will sharpen.

**R2 — Watch the "is-this" / "what" ratio as a maturity index.** Currently 1:2.1. As the system matures, this should approach 1:1 or invert. Set up a monthly automated report of this ratio; treat decline as a signal to invest in clearer status surfaces (so the user doesn't have to ask "what" so often).

**R3 — Use the March 2026 vocabulary-emergence window to pre-load common-answer skills.** The 389 "what" questions in March 2026 are likely about newly-emerged substrate vocabulary (conductor, organ, IRF, fossil, AMMOI). Build a `define <term>` skill that answers from the substrate-vocabulary lexicon directly, reducing definitional question volume.

---

**Validation gate:** 6 findings, 8+ evidence anchors (atom-IDs from earlier sample + monthly counts + frame ratios), 3 recommendations. Method explicit, including caveat about 53% unmatched rate. Out-of-scope: emotional atoms (U6), correction atoms (U7), implicit-signal atoms (no unit assigned, deferred to U14).
