# Polarity × Repo Mapping — Validation of the Artistic Triforce Vocabulary

**Document type:** Genesis-layer companion — validation exercise
**Date:** 2026-06-15
**Companion to:** [`01-artistic-triforce-creative-ontology.md`](./01-artistic-triforce-creative-ontology.md) §4 (the 8×3 polarity × organ matrix)
**Purpose:** Human-driven validation of the three-polarity vocabulary *before* any automated polarity classifier (the prerequisite step named in GH#97; see also the proposed ABSORB polarity axis, GH#96)
**Resolves:** GH#97

---

## 1. Why this exists

The Artistic Triforce genesis document establishes three creative polarities — **Conscious**, **Subconscious**, **Temporal** — and asserts they are orthogonal to the eight organs. Before that vocabulary is encoded into the ABSORB classifier (GH#96), it must survive contact with real repos: are the three polarities *sufficient* (every work fits), *non-overlapping* (assignments are defensible), and *useful* (the lens reveals something)?

This document tags a cross-organ sample of repos with a **primary polarity** and records where the vocabulary strains. It is a manual exercise by design — the genesis doc (§The ABSORB Classifier) is explicit that the vocabulary "must be established and tested in human-driven creative practice before it is encoded in automation."

## 2. The mapping (15 repos across the organs)

Polarity legend — **C** = Conscious (present reality, clarity), **S** = Subconscious (hidden/masked, atmosphere), **T** = Temporal (deep past/future, weight). A `+` denotes a blend with the secondary polarity dominant-second.

| # | Repo | Organ | Primary polarity | Rationale |
|---|------|-------|:---------------:|-----------|
| 1 | `recursive-engine--generative-entity` | I | **T** | Theory of recursion and ontogenesis — concerned with structures that outlast any instance; canonical/temporal register. |
| 2 | `organon-noumenon--ontogenetic-morphe` | I | **T** | Formal ontology of becoming; pre-Socratic + systems-theory lineage. Pure Temporal. |
| 3 | `cognitive-archaelogy-tribunal` | I | **S** + T | "Cognitive archaeology" excavates hidden structures of thought — the Subconscious-as-theory cell of the matrix. Temporal undertone (archaeology). |
| 4 | `narratological-algorithmic-lenses` | I | **C** + T | Narrative analysis as practice-as-research; looks outward at how stories are built. Conscious-leaning. |
| 5 | `metasystem-master` | II | **C** | Documentary/system-reflexive art about the system itself — direct engagement with present reality. |
| 6 | `example-generative-music` | II | **S** | Generative music as atmosphere-first; pattern/disruption from the Eno lineage cited in the genesis doc. |
| 7 | `example-choreographic-interface` | II | **C** + S | Performance/persona work; embodied present-tense (Conscious) shading into the masked/dreamlike (Subconscious). **Ambiguous — see §3.** |
| 8 | `public-record-data-scrapper` | III | **C** | A tool that renders the real (public records) legible — clarity is its whole aesthetic. Textbook Conscious-in-Commerce. |
| 9 | `trade-perpetual-future` | III | **T** | A product *about time* — futures, prophecy-as-pricing. The name is the polarity. |
| 10 | `peer-audited--behavioral-blockchain` (Styx) | III | **S** + C | Behavioral surveillance/trust mechanics operate on the hidden (Subconscious); productized for a real market (Conscious). **Ambiguous — see §3.** |
| 11 | `orchestration-start-here` | IV | **C** | Process documentation and governance reflection — looking directly at how the work works. |
| 12 | `public-process` | V | **C** | Building-in-public, personal-essay register. The Conscious-in-Logos cell, almost by definition. |
| 13 | `salon-archive` | VI | **T** + C | Reading groups on canonical texts = intergenerational transmission (Temporal); facilitation is present-tense (Conscious). |
| 14 | `kerygma-pipeline` | VII | **C** | Authentic-voice marketing / announcement automation — present-reality positioning. |
| 15 | `organvm-corpvs-testamentvm` (this corpus) | VIII | **T** | "The system as living text" — constitutional history, the Whitman *Leaves of Grass* pattern. Self-witnessing across time. |

## 3. Where the vocabulary strains (the interesting cases)

The blends are not failures of the vocabulary — they are exactly where the genesis doc predicts the most interesting work lives ("a field of gravitational centers"). But three cases test the limits:

- **`example-choreographic-interface` (C+S):** Live performance is present-tense and embodied (Conscious), but choreography that works through persona and the dreamlike pulls Subconscious. *Verdict:* the blend is real and the vocabulary handles it — the polarities are gradient, not bins. No refinement needed.
- **`peer-audited--behavioral-blockchain` / Styx (S+C):** A product whose *subject* is hidden behavior (Subconscious) but whose *form* is a market instrument (Conscious). This tests the orthogonality claim: the organ (III, Commerce) is fixed, but two polarities compete. *Verdict:* assignable, with primary = Subconscious (the *intent* excavates the hidden; the commercial wrapper is form, governed by `taste.yaml`, not intent). Confirms polarity ≠ organ.
- **Pure-infrastructure repos** (`.github`, `schema-definitions`, `organvm-engine`): these resist polarity entirely — they are not *creative works*, they are scaffolding. *Verdict:* the vocabulary should **not** be forced onto non-creative artifacts. Proposed refinement (fed back per the genesis doc's protocol): a polarity value of `N/A — infrastructure` is legitimate; the classifier (GH#96) should treat polarity as nullable for `functional_class` infrastructure repos.

## 4. Findings fed back to the vocabulary

1. **Sufficiency: PASS.** Every *creative* repo in the sample mapped to one or two polarities. None required a fourth polarity.
2. **Non-overlap: PASS (gradient, not bins).** Blends were always assignable to a defensible *primary*; the secondary is additive, not contradictory.
3. **Usefulness: PASS.** The lens surfaced a non-obvious adjacency — `cognitive-archaelogy-tribunal` (I, Subconscious) and `example-generative-music` (II, Subconscious) "draw from the same psychic well" across organs, exactly the cross-organ resonance the genesis doc §Seed Contract System anticipated.
4. **One refinement for GH#96:** polarity must be **nullable** — infrastructure/scaffolding repos take `N/A — infrastructure`, not a forced polarity. This is the single concrete change to carry into the ABSORB classifier design.

## 5. Cross-references

- Genesis source: [`01-artistic-triforce-creative-ontology.md`](./01-artistic-triforce-creative-ontology.md)
- Essay adaptation: `docs/essays/42-the-artistic-triforce.md` (GH#95)
- Classifier follow-up: **GH#96** (add polarity axis to ABSORB) — must honor the nullable-for-infrastructure finding (§4.4).
