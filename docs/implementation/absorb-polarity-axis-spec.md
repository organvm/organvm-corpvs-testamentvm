# ABSORB Polarity Axis — Design Specification

**Date:** 2026-06-15
**Status:** DESIGN SPEC (ready for implementation — vocabulary now validated per GH#97)
**Resolves:** GH#96
**Implements:** [`docs/genesis/01-artistic-triforce-creative-ontology.md`](../genesis/01-artistic-triforce-creative-ontology.md) §7 (Relationship to Existing Infrastructure — the ABSORB Classifier and Seed Contract subsections)
**Validated by:** GH#97 / [`docs/genesis/01a-polarity-repo-mapping.md`](../genesis/01a-polarity-repo-mapping.md)
**House style:** consistent with [`docs/standards/27-logos-bypass-feedback-routing.md`](../standards/27-logos-bypass-feedback-routing.md)

---

## 0. Scope and a note on where the code lives

This is a **design specification**, not an implementation. The artifacts it specifies live in **other repositories** that are not present in this corpus:

- The classifier code — `alchemia-ingestvm/src/alchemia/absorb/classifier.py`
- The seed/intake schema — `schema-definitions/schemas/seed-v1.schema.json`
- The registry-browser UI — `system-dashboard`

This document defines the contract those repos must implement. Every schema fragment and code sketch below is **target shape**, to be lifted into the owning repo verbatim or adapted to its conventions. Nothing here is executable in the governance corpus; the corpus is the source of truth for the *design*, the owning repos are the source of truth for the *implementation*.

The vocabulary itself (Conscious / Subconscious / Temporal) was deliberately **not** encoded in automation until it had survived human-driven creative practice. That gate is now passed: GH#97 / `01a-polarity-repo-mapping.md` tagged 15 repos and reported the vocabulary PASS on sufficiency, non-overlap, and usefulness, with exactly one refinement carried forward here — **polarity must be nullable for infrastructure/scaffolding repos** (value `N/A — infrastructure`).

## 1. The polarity enum

The polarity axis is a fourth classification dimension, orthogonal to organ membership, content type, and deployment readiness (genesis §7, "The ABSORB Classifier"). It has three real values plus an explicit infrastructure sentinel, and may be absent entirely.

- `CONSCIOUS` — present reality, clarity, direct engagement.
- `SUBCONSCIOUS` — the hidden, masked, dreamlike; atmosphere over clarity.
- `TEMPORAL` — deep past / speculative future; canon, weight, time.
- `N/A — infrastructure` — the artifact is scaffolding, not a creative work (the GH#97 refinement).
- `null` / absent — not yet classified (the pre-classification default).

`N/A — infrastructure` and `null` are distinct: the first is a *decision* ("this repo is not a creative work, no polarity applies"); the second is the *absence of a decision* ("not yet classified"). The classifier and any consumer must not collapse them.

JSON-schema fragment (target for `schema-definitions`):

```json
"polarity_value": {
  "description": "Creative polarity per the Artistic Triforce ontology.",
  "oneOf": [
    { "type": "string", "enum": ["CONSCIOUS", "SUBCONSCIOUS", "TEMPORAL"] },
    { "type": "string", "const": "N/A — infrastructure" },
    { "type": "null" }
  ]
}
```

Python `Enum` sketch (target for `alchemia-ingestvm`):

```python
from enum import Enum
from typing import Optional

class Polarity(str, Enum):
    CONSCIOUS = "CONSCIOUS"
    SUBCONSCIOUS = "SUBCONSCIOUS"
    TEMPORAL = "TEMPORAL"
    NA_INFRASTRUCTURE = "N/A — infrastructure"

# An unclassified or non-applicable artifact is modeled as Optional[Polarity]:
#   None                       -> not yet classified
#   Polarity.NA_INFRASTRUCTURE -> classified as non-creative scaffolding
PolarityField = Optional[Polarity]
```

## 2. `polarity` field in the ABSORB classifier output

The ABSORB stage currently emits a classification record per ingested artifact. This spec adds a `polarity` block to that record. Because the genesis doc and the GH#97 mapping both document **blends** (e.g. `example-choreographic-interface` = C+S, Styx = S+C), the model is **primary + optional secondary**, each carried with a **confidence** score.

Output schema delta (additive; existing fields unchanged):

```json
"polarity": {
  "type": "object",
  "properties": {
    "primary":   { "$ref": "#/definitions/polarity_value" },
    "secondary": { "$ref": "#/definitions/polarity_value" },
    "confidence": {
      "type": "number", "minimum": 0.0, "maximum": 1.0,
      "description": "Classifier confidence in the PRIMARY assignment."
    },
    "secondary_confidence": {
      "type": ["number", "null"], "minimum": 0.0, "maximum": 1.0
    },
    "source": {
      "type": "string",
      "enum": ["auto-proposed", "human-confirmed", "human-override"],
      "description": "Provenance of the assignment; see §6 human-in-the-loop gate."
    },
    "rationale": { "type": "string" }
  },
  "required": ["primary", "confidence", "source"]
}
```

Rules:

- `primary` is mandatory once a record is classified; for scaffolding it is `N/A — infrastructure`.
- `secondary` is optional and `null` for a pure (single-polarity) work. When present it must differ from `primary`.
- When `primary` is `N/A — infrastructure` or `null`, `secondary` must be `null`.
- `confidence` always describes the **primary**. Low primary confidence with a high secondary is a signal to route to human review (§6).
- `source` records whether the value was machine-proposed or human-settled. The classifier only ever writes `auto-proposed`; the other two values are written by the human-in-the-loop gate.

## 3. Query capability: "all Subconscious-oriented material across organs"

The genesis doc names the target query verbatim: *"Show me all Subconscious-oriented material across all organs"* and *"What Temporal work is in the pipeline for ORGAN-I?"* The classifier output must be indexed so these resolve without a full scan.

Index shape (owning store: the ABSORB output index in `alchemia-ingestvm`; mirrored into the registry where repo-level):

- Maintain a secondary index keyed on `polarity.primary` (and a separate one on `polarity.secondary`) mapping to artifact/repo IDs, with `organ` and `confidence` carried as filterable attributes.
- A "Subconscious-oriented" query is the **union** of `primary == SUBCONSCIOUS` and `secondary == SUBCONSCIOUS` (so blends surface), de-duplicated, with primary matches ranked above secondary.

Query signature (target API):

```
absorb.query_polarity(
    polarity: Polarity,
    organ: Optional[str] = None,         # filter to one organ, or None = all organs
    include_secondary: bool = True,      # union primary+secondary, or primary-only
    min_confidence: float = 0.0,
) -> list[ClassificationRecord]
```

`N/A — infrastructure` and `null` records are excluded from polarity queries by default (a Subconscious query never returns scaffolding). The cross-organ resonance the genesis §Seed Contract section anticipates — e.g. `cognitive-archaelogy-tribunal` (I, S) adjacent to `example-generative-music` (II, S), noted in `01a` §4.3 — is exactly what the `organ=None, include_secondary=True` form surfaces.

## 4. `seed.yaml` schema update

Each repo's `seed.yaml` contract may declare its polarity so that repo-level intent is authoritative and need not be re-inferred. The declaration is **optional, nullable, additive only** — no existing field is changed or removed. (This corpus's No-Deletion Principle, `docs/standards/23-no-deletion-principle--alchemical-evolution.md`, governs the corpus; for the seed schema the binding constraint is simply: this change is additive, existing seeds without a `polarity:` block remain valid.)

`seed.yaml` fragment (target for `schema-definitions`):

```yaml
# Optional. Absent => unclassified. Use the infrastructure sentinel for scaffolding.
polarity:
  primary: SUBCONSCIOUS            # CONSCIOUS | SUBCONSCIOUS | TEMPORAL | "N/A — infrastructure"
  secondary: CONSCIOUS             # optional; omit for a pure work; must differ from primary
  rationale: >                     # optional human note
    Excavates hidden behavioral mechanics (S); productized for a real market (C).
```

Schema fragment:

```json
"polarity": {
  "type": ["object", "null"],
  "additionalProperties": false,
  "properties": {
    "primary":   { "$ref": "#/definitions/polarity_value" },
    "secondary": { "$ref": "#/definitions/polarity_value" },
    "rationale": { "type": "string" }
  },
  "required": ["primary"]
}
```

When `seed.yaml` declares a polarity, the classifier treats it as a **human-confirmed** assignment (source `human-confirmed`, confidence `1.0`) and does not overwrite it; auto-classification only fills records where the seed is silent.

## 5. `system-dashboard` registry-browser polarity column

The registry browser gains one column and one filter:

- **Column "Polarity":** renders `primary` with a small swatch/glyph per value (C / S / T), the secondary as a subscript when present (e.g. `S·c`), and `N/A — infrastructure` rendered muted/greyed to read as "not a creative work." Unclassified (`null`) renders as an em-dash. The column shows a confidence affordance (e.g. a faded glyph below ~0.6 confidence) so low-confidence auto-proposals are visible at a glance.
- **Filter (requirement):** a multi-select polarity filter that, when set to a value, applies the §3 union semantics (matches both primary and secondary) and offers a toggle for "include infrastructure" (default off) and a confidence threshold slider. The filter must compose with the existing organ filter so "Subconscious across all organs" and "Temporal in ORGAN-I" are both one-click views.

## 6. Classification heuristics (auto-proposal signals)

These map textual and structural signals to each polarity, derived from the genesis polarity descriptions (§I–III). They drive the **auto-proposal only** — never an unattended final assignment (see §7). Signals are evidence, weighted into the confidence score.

**CONSCIOUS — clarity / present reality.** Textual: first-person present-tense, autobiographical/documentary framing, "case study," "how it actually works," "building in public," named real-world referents (places, dates, the system itself). Structural: README leads with concrete present-state description; ORGAN-V/VII register; persona-as-lens (named author voice, not a mask). Maps to repos like `public-process`, `public-record-data-scrapper`, `metasystem-master` (`01a` rows 5, 8, 12).

**SUBCONSCIOUS — atmosphere / hidden.** Textual: thriller/horror/surreal vocabulary, "hidden," "mask," "shadow," "excavate," dream/uncanny imagery, atmosphere-over-clarity prose; subject is internal/psychological or behavioral-beneath-the-surface. Structural: generative/pattern-disruption art, persona-as-mask, behavioral/surveillance mechanics. Maps to `example-generative-music`, `cognitive-archaelogy-tribunal`, Styx (`01a` rows 6, 3, 10).

**TEMPORAL — weight / canon-time.** Textual: deep-past/future framing, "canon," "lineage," "myth," "prophecy," "constitutional," historical or speculative arc, references to texts/traditions that outlast any instance. Structural: ontology/theory, world-building, futures/forecasting products, constitutional/archival self-documentation. Maps to `recursive-engine--generative-entity`, `trade-perpetual-future`, this corpus itself (`01a` rows 1, 9, 15).

**Infrastructure sentinel.** Structural-only signal: `functional_class == infrastructure`, absence of creative subject, scaffolding repos (`.github`, `schema-definitions`, `organvm-engine`). When this fires, the classifier proposes `N/A — infrastructure` and must **not** force a creative polarity (the GH#97 §4.4 refinement). This is the one case where structural signal overrides any weak textual lean.

**Blends.** When two polarity signal-sets both exceed threshold, the higher scores `primary`, the lower scores `secondary` with its own confidence. A close score gap (e.g. within 0.15) is a strong trigger for human review.

## 7. Human-in-the-loop gate

Per the genesis doc's explicit stance that the polarity vocabulary "must be established and tested in human-driven creative practice before it is encoded in automation," **automation proposes; the human confirms.** This gate is non-negotiable and mirrors the AI-conductor model (AI generates, human refines).

- The classifier writes only `source: "auto-proposed"`. An auto-proposed polarity is a **suggestion**, never authoritative.
- A polarity becomes authoritative only when a human sets `source: "human-confirmed"` (accepts the proposal) or `source: "human-override"` (changes it). A `seed.yaml` declaration counts as human-confirmed at the repo level (§4).
- Proposals below a confidence floor (recommend 0.6) or with a near-tie blend are flagged for review and excluded from authoritative query results until confirmed (they remain visible as proposals in the dashboard, faded).
- The gate is consistent with the Logos-Bypass house principle (`27-...`): an automated signal flows into the system as *proposed material*, and a human judgment stage stands between proposal and canonical state. Automation never silently rewrites creative intent.

## 8. Acceptance criteria

- [ ] `polarity_value` enum (`CONSCIOUS | SUBCONSCIOUS | TEMPORAL | "N/A — infrastructure" | null`) defined in `schema-definitions/schemas/seed-v1.schema.json`, with `null` and `N/A — infrastructure` distinct. (§1)
- [ ] ABSORB classifier output carries the additive `polarity` block (`primary`, optional `secondary`, `confidence`, `source`, optional `rationale`); existing output fields unchanged. (§2)
- [ ] Blends modeled as primary + optional secondary, each with confidence; secondary differs from primary; null when primary is infrastructure/unclassified. (§2)
- [ ] `absorb.query_polarity(...)` resolves "all Subconscious across organs" and "Temporal in ORGAN-I" via primary∪secondary union, excluding infrastructure/null by default. (§3)
- [ ] `seed.yaml` gains an optional, nullable `polarity:` block (additive only); seeds without it remain valid; a declared seed polarity is treated as human-confirmed and not overwritten. (§4)
- [ ] `system-dashboard` registry browser shows a Polarity column (primary glyph + optional secondary + confidence affordance) and a composable polarity filter with union semantics, an "include infrastructure" toggle, and a confidence threshold. (§5)
- [ ] Classifier never assigns a final polarity unattended: all auto outputs are `source: auto-proposed`; only human action yields `human-confirmed` / `human-override`. (§7)
- [ ] Infrastructure repos are assignable `N/A — infrastructure` and are never force-classified into a creative polarity. (§1, §6, GH#97 §4.4)

## 9. Cross-references

- Genesis source: [`docs/genesis/01-artistic-triforce-creative-ontology.md`](../genesis/01-artistic-triforce-creative-ontology.md) §7, §I–III, §Orthogonality.
- Validation: [`docs/genesis/01a-polarity-repo-mapping.md`](../genesis/01a-polarity-repo-mapping.md) (GH#97) — the nullable-for-infrastructure refinement (§4.4).
- House-style precedent: [`docs/standards/27-logos-bypass-feedback-routing.md`](../standards/27-logos-bypass-feedback-routing.md) — propose-then-confirm routing.
- Additive-change posture: [`docs/standards/23-no-deletion-principle--alchemical-evolution.md`](../standards/23-no-deletion-principle--alchemical-evolution.md).
- Owning repos (implementation, not in this corpus): `alchemia-ingestvm` (classifier), `schema-definitions` (seed schema), `system-dashboard` (registry browser).
