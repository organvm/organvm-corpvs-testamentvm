# SPEC-002 Risk Register

```
Date:      2026-06-15
Status:    COMPLETE
Resolves:  GH#134
Phase:     R (Research) — gate G0 for SPEC-002 Phase F
Spec:      SPEC-002 (Primitive Register)
Profile:   11 claims — 4 GROUNDED · 3 ADAPTED · 3 NOVEL · 1 CONTESTED
```

---

## 1. Classification Vocabulary

| Status | Meaning |
|--------|---------|
| **GROUNDED** | Directly supported by ≥1 foundational ontology (BFO or DOLCE) and uncontested across traditions. Low risk. |
| **ADAPTED** | Recognized in some tradition but reshaped for ORGANVM's governance needs; a foundational ontology declines or subsumes it. Moderate risk; departure disclosed. |
| **NOVEL** | No counterpart in BFO/DOLCE/Armstrong/Johansson (0/2 foundational alignment). Grounded only in adjacent traditions (deontic logic, institutional grammar) or by reduction proof. Highest risk. |
| **CONTESTED** | Partially recognized (≈0.5–1/2) but a stronger competing analysis exists (typically BFO's finer carving). Moderate–high risk; refinement trajectory flagged. |

---

## 2. Register

| # | Claim ID | Claim | Status | Source(s) | Risk if wrong | Mitigation |
|---|----------|-------|--------|-----------|---------------|------------|
| 1 | RR-002-01 | **Entity (PRIM-001)** is an irreducible, identity-bearing, independent (−D) substrate; all other primitives depend on it. | GROUNDED | Simons1987; ArpSmithSpear2015 (Independent Continuant); Masolo2003 (Endurant) | None foreseeable — if false, the entire dependency ordering of the register collapses. | Uncontested across all traditions; FORMAL implementation (`ontologia/entity/identity.py`, ULID UIDs) provides machine-checkable backing. |
| 2 | RR-002-02 | **Value (PRIM-002)** is a dependent (+D), non-rigid datum inhering in a bearer Entity along a dimension; logically prior to State, not derivable from it. | GROUNDED | ArpSmithSpear2015 (Quality/SDC); Masolo2003 (Quality+qualia); Armstrong1978 | Circularity with State (PRIM-005) if priority is reversed; mis-typed dimension declarations. | Both BFO and DOLCE recognize qualities first-class; reduction test in SPEC-002 §PRIM-002 explicitly blocks the Value-from-State definition. Future intrinsic/assigned subdivision flagged. |
| 3 | RR-002-03 | **Relation (PRIM-003)** is an irreducible typed, directed connection between Entity relata; not reducible to co-occurring monadic Values. | GROUNDED | Simons1987; ArpSmithSpear2015 (Relational Quality); Johansson2004 | If reducible, directionality + type structure is lost and the dependency graph (INV-000-001) becomes ill-founded. | All traditions recognize relations as first-class (disagreement is classification only). Reduction test shows directionality/type are constitutive. Consolidation of 3 code implementations scheduled (DRIFT, §7.3). |
| 4 | RR-002-04 | **Event (PRIM-004)** is an irreducible timestamped, caused transition between States; not merely a (before, after) State pair. | GROUNDED | ArpSmithSpear2015 (Process/Process Boundary); Masolo2003 (Achievement/Accomplishment) | If reducible to a State pair, causal + temporal provenance is unrepresentable; the append-only event log loses its semantics. | Universal across traditions. Reduction test isolates causation/timestamp/type as constitutive. Layer-4A event-log implementation target named. |
| 5 | RR-002-05 | **State (PRIM-005)** is a primitive holistic configuration (Π-type over all an Entity's dimensions), retained because it is the well-typed **domain of Constraints**. | ADAPTED | Masolo2003 (DOLCE State, 0.5/1); Armstrong1978 (states of affairs); *against:* ArpSmithSpear2015 (BFO subsumes into Quality aggregate, 0/1) | If State is not primitive, Constraint (PRIM-006) has no well-typed domain and the conjunctive structure of multi-dimension governance rules cannot be expressed. | **Functional, not realist, justification** explicitly disclosed (§5.1): State is primitive *for ORGANVM* because governance requires configuration snapshots. DOLCE precedent + Armstrong cited; BFO departure acknowledged. Reduction-to-Value-set blocked by the "complete assignment function" argument. |
| 6 | RR-002-06 | **Constraint (PRIM-006)** is a primitive deontic predicate over States (`State -> Deontic -> Prop`) carrying MUST/SHOULD/MAY normative force. | NOVEL | vonWright1951 (deontic logic); CrawfordOstrom1995 (ADICO); Ostrom2005; Searle1995; *against:* BFO 0/1, DOLCE 0/1 | Highest exposure: a BFO/DOLCE reviewer may reject the register as a category error (smuggling normativity into a descriptive ontology). If sustained, the register's claim to ontological respectability weakens. | Disclosed as the principal risk (§5.2). Grounded in rigorous *adjacent* traditions (deontic logic, institutional grammar) that operate in a different intellectual space. Defense: descriptive/normative boundary is itself a theoretical commitment; a governed ontology *requires* normative primitives (Gruber minimal-commitment, applied to the governance domain). |
| 7 | RR-002-07 | **Capability (PRIM-007)** is a single primitive dispositional power (`Entity -> EventType -> Type_0`); a power exists even when unexercised. | CONTESTED | Johansson2004 (irreducibility of tendencies); ArpSmithSpear2015 (Disposition, 0.5/1); *against:* BFO's Disposition/Role/Function trichotomy; DOLCE 0/1 | The unified primitive conflates three BFO categories; a reviewer may demand subdivision, or argue Capability reduces to a permissive Constraint or to a function type Entity→Event. | Disclosed (§5.3). Retention justified by Johansson's irreducibility thesis + functional necessity (need to express what an Entity CAN do). Reduction tests block both the "permissive Constraint" and "Entity→Event function" readings (former loses deontic/dynamic distinction; latter loses dispositional existence). Subdivision flagged as *type refinement within PRIM-007*, not a new primitive. |
| 8 | RR-002-08 | **Composition is non-extensional**: composites with identical parts can differ (Simons' Minimal Mereology; extensionality + unrestricted composition dropped). | ADAPTED | Simons1987 (MM) | If extensional, two organs with identical repos would be forced identical — false for ORGANVM (differing Constraints/Values/Relations individuate them). Whole-system identity model breaks. | MM axiom table reproduced verbatim (§2.1); integral-whole individuation by structure-determining relations. Departure from CEM is the *point*, and it is the mainstream alternative, not a fringe move. |
| 9 | RR-002-09 | **Composites are dependent record types**, not bare Σ-types; field types/structural constraints depend on earlier fields. | ADAPTED | MartinLof1984 (Π/Σ, universes); Pierce2002 (records) | If only Σ-types are available, structured wholes degrade to loose aggregations and the `constraints`/`values` field dependencies are unexpressible; mechanization target is mis-specified. | Dependent records are a standard definitional extension of ITT; Pierce supplies engineering tractability. The §2.2 `CompositeObject` record is the normative schema. Marked FORMALIZABLE pending downstream type definitions. |
| 10 | RR-002-10 | **Process is NOT a primitive** — it reduces to Entity + ordered Events + ordering Relations + governing Constraints + status State (§3.6). | NOVEL (reconciliation) | Gruber1993 (minimal commitment); ArpSmithSpear2015 (Process as Occurrent subtype — replicated by typing, not by a new primitive) | The Stage-II corpus lists Process as a root class; if the reduction is unsound, the register is *insufficient* and an 8th primitive is forced, breaking the "exactly seven" closure claim. | **This is the CONTESTED-adjacent reduction the issue flags (State/Process-as-composition).** Reduction exhibited explicitly as a dependent record; cross-checked against BFO (Process = Occurrent, reproduced by "process-shaped" typing). Sufficiency verified against all SPEC-000 axioms (§4). Reduction Test Protocol (§6.2) governs any future re-elevation. |
| 11 | RR-002-11 | **Evidence is NOT a primitive** — it reduces to Entity + Value + Event (§3.5). | NOVEL (reconciliation) | Gruber1993 (minimal commitment) | The Stage-II corpus lists Evidence as a root class; if irreducible, register insufficiency again forces an 8th primitive. | Reduction exhibited as a 3-field record; Evidence's operational importance (test results, audit traces) acknowledged but distinguished from ontological irreducibility. Gruber: do not elevate reducible domain concepts. |

---

## 3. Aggregate Risk Posture

- **Concentration:** All foundational-ontology misalignment is concentrated in PRIM-005 (State,
  ADAPTED), PRIM-006 (Constraint, NOVEL), PRIM-007 (Capability, CONTESTED), and the two
  non-primitive reconciliations (Process, Evidence). The four GROUNDED claims (Entity, Value,
  Relation, Event) carry negligible risk.
- **Single largest exposure:** RR-002-06 (Constraint, NOVEL, 0/2). Its mitigation is *disclosure +
  adjacent-tradition grounding*, not foundational alignment — by design, since the governance
  domain is what motivates the register's existence.
- **Closure dependency:** RR-002-10 and RR-002-11 (Process/Evidence reductions) are what license
  the "exactly seven primitives" claim. A failed reduction here is the only path to an 8th
  primitive, gated by the §6.2 Reduction Test Protocol.
- **Implementation drift:** Six of seven primitives are FORMALIZABLE-but-DRIFTED or MISSING in code
  (§7.3). This is a *fidelity* risk (spec vs. implementation), tracked separately from the
  *ontological* risk catalogued above; it does not threaten the register's correctness, only its
  realization.

## 4. Gate Recommendation (G0 → Phase F)

The register's high-risk claims are all (a) explicitly disclosed in SPEC-002 §5, (b) grounded in
named adjacent traditions, and (c) governed by an amendment/reduction protocol (§6). No
undisclosed novel claim was found. **Recommendation: PASS G0**, conditional on adding the 11
`[in bibliography.bib]` BibTeX keys to `specs/bibliography.bib` during Phase F.
