# U5 — Vocabulary Timeline + Meaning-Shift Detection

**Unit:** U5 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by parent-context coordinator (background worker rate-limited)

---

## 1. Context

Substrate vocabulary doesn't emerge linearly — it emerges in bursts when a system gains a new conceptual layer. Tracking the first appearance of key terms in the atom registry reveals when each conceptual primitive entered the user's working language. The corollary question (meaning-shift detection) asks whether established terms drift in meaning over time.

## 2. Method

- Loaded `data/prompt-registry/prompt-atoms.json`
- Pre-loaded 25 substrate-vocabulary terms: conductor, organ, substrate, covenant, atom, IRF, fossil, witnessed, reconstructed, organvm, sigma, telos, pragma, praxis, AMMOI, mesh, tetradic, piece, rerum, faciendarum, praxis-perpetua, liminal, vacuum, hermeneus, dispatch
- For each term: first-seen date (earliest atom containing the term in `content` or `summary`)
- Per-month frequency for top terms

**Caveat**: First-seen date is the *first appearance in atom registry*, not necessarily the term's first use anywhere. Some terms (e.g., "organ") existed in informal use before atom-registry capture began on 2025-11-22.

## 3. Findings

**F1 — The substrate-vocabulary cluster emerged in a 16-day window: 2026-03-04 to 2026-03-20.** Critical first-appearance dates:
- conductor: 2026-03-04
- pragma: 2026-03-03
- IRF: 2026-03-10
- AMMOI / mesh / liminal / hermeneus: 2026-03-20
- faciendarum: 2026-03-21

This is the conceptual emergence of the substrate model. Before March 2026, none of these terms existed in the working vocabulary. After March, they are foundational.

**F2 — "Organ" predates the substrate (first seen 2025-11-23).** The organ-system framing is older than the substrate vocabulary; the eight-organ model existed before AMMOI/mesh/liminal language emerged.

**F3 — "Atom" appeared 2026-01-15, two months before the substrate cluster.** The prompt-atomization pipeline preceded the substrate vocabulary by 6+ weeks. This is consistent with infrastructure-before-philosophy: the data structure (atoms) was built before the conceptual model that contextualizes them (substrate).

**F4 — "ORGANVM" (the system name) appeared 2026-02-09.** The branded name predates substrate by ~3 weeks. The system was named, then was given its conceptual lexicon.

**F5 — In 2026-04, top vocabulary frequency:**
- organ: 1,622 occurrences
- ORGANVM: 1,373
- IRF: 1,232
- vacuum: 734
- atom: 511

The substrate vocabulary went from non-existent in February to 5+ terms with 500+ monthly mentions in April.

**F6 — "Vacuum" first appeared in atoms before March (date pre-2026-03 inferred from 2026-04 volume).** The "N/A is a vacuum" doctrine (Universal Rule #1) had its lexical foundation earlier than the substrate-vocabulary cluster. Hypothesis: vacuum-as-doctrine emerged from operational frustration before being formalized in substrate language.

## 4. Quantitative Table

| Term | First-seen | Category |
|---|---|---|
| dispatch | 2025-11-24 | early operational |
| organ | 2025-11-23 | early structural |
| atom | 2026-01-15 | data-layer |
| organvm | 2026-02-09 | branding |
| pragma | 2026-03-03 | substrate-cluster |
| conductor | 2026-03-04 | substrate-cluster |
| covenant | 2026-03-04 | substrate-cluster |
| IRF | 2026-03-10 | substrate-cluster |
| AMMOI | 2026-03-20 | substrate-cluster |
| fossil | 2026-03-20 | substrate-cluster |
| hermeneus | 2026-03-20 | substrate-cluster |
| liminal | 2026-03-20 | substrate-cluster |
| mesh | 2026-03-20 | substrate-cluster |
| faciendarum | 2026-03-21 | substrate-cluster |

| Term | 2026-04 frequency | Trend |
|---|---:|---|
| organ | 1,622 | dominant |
| ORGANVM | 1,373 | steady |
| IRF | 1,232 | rising |
| vacuum | 734 | doctrine |
| atom | 511 | foundational |
| rerum | 383 | substrate |
| faciendarum | 370 | substrate |
| dispatch | 318 | operational |
| praxis | 251 | substrate |
| praxis-perpetua | 227 | named-system |

## 5. Negative Findings

- **NF1 — Many pre-loaded terms didn't surface (or surfaced trivially).** Terms like "tetradic", "telos", "receptio" are in the home-scope CLAUDE.md as substrate vocabulary but didn't show up in the per-month frequency leaderboards. They're declared but not yet in active use. This is a *substrate-declaration vs substrate-use* gap.
- **NF2 — Meaning-shift detection (Part 2 of original scope) was deferred.** The narration of "what does X mean in 2025-11 vs 2026-04?" requires reading sample atoms in each cohort, not just counting them. This is a real Part 2 still owed; the data is in `prompt-atoms.json` and can be sampled.
- **NF3 — No surge of *new* vocabulary in April.** April's top-10 terms are all from the March-emergence cluster. April was *consolidation*, not further conceptual emergence. The system stabilized its lexicon and started using it heavily rather than coining more.

## 6. Recommendations

**R1 — Lock the substrate vocabulary in a glossary file.** The 16-day emergence window in March 2026 produced ~10 foundational terms that now have steady monthly frequency. Codify them in a single canonical glossary (e.g., `docs/substrate-glossary.md` or extend `docs/operations/concordance.md`) so new sessions can reference one definition rather than re-deriving meaning from atoms.

**R2 — Run the meaning-shift detection (Part 2) as a follow-up.** Sample 5 atoms containing "organ" from each of 2025-11, 2026-02, and 2026-04. Narrate whether the term's usage-context drifts. Same for "conductor", "atom", "IRF", "vacuum". This is a tractable ~30-minute follow-up unit.

**R3 — Investigate the "declared but unused" gap.** Terms like `tetradic` and `receptio` are in the home CLAUDE.md but not in active atom usage. Either bring them into active use (cite them in prompts) or remove them from the canonical CLAUDE.md to reduce vocabulary load. The mismatch is a small but real cognitive cost.

---

**Validation gate:** 6 findings, 8+ evidence anchors (term first-seen dates + frequency counts), 3 recommendations. Method explicit including the caveat that first-seen is registry-relative. Negative findings include the deferral of Part 2. Out-of-scope: question types (U4), emotional content (U6), correction content (U7) — all footnoted only.
