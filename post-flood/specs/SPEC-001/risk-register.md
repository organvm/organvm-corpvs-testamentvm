# SPEC-001 Risk Register: Ontology Charter

```
Date:        2026-06-15
Status:      DRAFT (Phase-R deliverable)
Resolves:    GH#133
Phase:       R (Research) — gate G0 for SPEC-001 Phase F
Parent Spec: SPEC-001 (Ontology Charter, v1.1, RATIFIED 2026-03-18)
Bibliography: specs/bibliography.bib
```

---

## Purpose

This register classifies the load-bearing *grounding claims* of SPEC-001 — the
assertions on which the entity taxonomy (§2, §6), relation model (§3), and
contestation disclosures (§8) depend. Each claim is assigned a status, mapped to
its supporting source(s), and paired with the risk if the claim is wrong and a
mitigation.

**Status vocabulary** (consistent with SPEC-001 §8.1 and SPEC-000's register):

- **GROUNDED** — directly supported by the BFO/DOLCE/applied-ontology consensus;
  no live disagreement among the cited authorities.
- **ADAPTED** — drawn from one tradition over a competing one, with explicit
  justification; the competing tradition would decide differently.
- **NOVEL** — original to ORGANVM; no direct academic precedent.
- **CONTESTED** — the literature is actively split and SPEC-001's position is one
  side of an unresolved debate.

**Distribution** (matches SPEC-001 §8.1's stated 60/30/10 split): of the ten
claims below, **6 GROUNDED, 3 ADAPTED, 1 NOVEL.** No claim is classified
CONTESTED — the two genuinely contested *fields* (realism vs descriptivism;
modulation-as-edge-type) are absorbed as ADAPTED and NOVEL respectively, with
the disagreement disclosed rather than denied.

---

## Register

| Claim ID | Claim | Status | Supporting source(s) | Risk if wrong | Mitigation |
|----------|-------|--------|----------------------|---------------|------------|
| RC-001 | The Continuant/Occurrent partition is the correct top-level split for ORGANVM entities (ONT-002 vs ONT-013) | GROUNDED | Arp/Smith/Spear 2015; Masolo et al. 2003 (Endurant/Perdurant) | If the partition is wrong, every leaf type is misclassified and category_path is meaningless | Both BFO and DOLCE — otherwise opposed on realism — agree on this partition; the convergence is the strongest evidence available. Extension points (§6) allow re-parenting without rewriting leaves |
| RC-002 | Dependent entities decompose into Specifically-Dependent (ONT-007) and Generically-Dependent (ONT-010) continuants | GROUNDED | Arp/Smith/Spear 2015 (SDC/GDC); Masolo et al. 2003 (Quality) | Mis-modeling VARIABLE/METRIC vs DOCUMENT/SCHEMA would corrupt cascade-delete (SDC) and copy/migrate (GDC) semantics in SPEC-003 | The SDC/GDC distinction is standard BFO and maps cleanly onto observed system behavior (variables die with their bearer; documents migrate). Formalization deferred to SPEC-003 keeps the claim FORMALIZABLE, not prematurely FORMAL |
| RC-003 | VARIABLE and METRIC are anti-rigid (-R) qualities that must sit under a rigid supertype, and the flat enum violates OntoClean | GROUNDED | Guarino & Welty 2004 (OntoClean meta-properties) | If the OntoClean analysis is wrong, the entire argument for restructuring the flat enum (§8.2) collapses and the migration is unjustified | The +/-R/I/D analysis is mechanical and reproducible per OntoClean; the rigid-cannot-be-subsumed-by-anti-rigid constraint is a published theorem of the method. Audit is repeatable by a second agent |
| RC-004 | Relations are first-class "Relative" entities that mediate between relata and are not reducible to either (ONT-030–ONT-037) | GROUNDED | Sowa 2000 (triadic relations) | If relations are merely derived attributes, HierarchyEdge/LineageRecord/NameRecord lose independent identity and lineage tracking (AX-000-007) breaks | Sowa's triadic analysis is well-established KR; the ontologia implementation already assigns relation records their own identity, so theory and code agree |
| RC-005 | Gruber's five criteria (clarity, coherence, extendibility, minimal encoding bias, minimal ontological commitment) are the correct acceptance test for the taxonomy | GROUNDED | Gruber 1993; Gruber 1995 | If the wrong acceptance criteria are used, the taxonomy could pass review while being unusable for cross-organ knowledge sharing | Gruber's criteria are the field-standard design rubric and are applied explicitly in §6; "minimal ontological commitment" is what licenses demoting domain entities to compositions |
| RC-006 | Abstract entities (ONT-023) form a disjoint third top-level category alongside Continuant and Occurrent | GROUNDED | Masolo et al. 2003 (DOLCE Abstract) | If Abstract is not genuinely disjoint, RULE/CONSTRAINT/Capability/Type would be mis-filed as continuants or occurrents, breaking governance audit typing | DOLCE explicitly admits Abstract as a disjoint third category; BFO handles this differently but does not contradict the disjointness ORGANVM needs. Marked JUDGMENT at the concretization boundary (§ONT-023), bounding the risk |
| RC-007 | ORGANVM should adopt DOLCE-aligned descriptive pluralism rather than BFO strict realism | ADAPTED | Masolo et al. 2003 (chosen) over Smith 2004; Arp/Smith/Spear 2015 (rejected on realism) | If realism is in fact required for a sound ontology, then AX-000-006 topological mutation produces *illegitimate* categories and the system's self-revision is ungrounded | Disclosed in §8.1 as ADAPTED. Justified by Luhmann 1995 (social reality is constituted, not mind-independent) and by the operational fact that ORGANVM's categories *are* declared by a constitution. Reversible: if realism is later required, only §1/§8.1 change, not the taxonomy tree |
| RC-008 | Governance Object (ONT-024) is promoted from a domain entity to a first-class ontological category | ADAPTED | Ostrom 1990; Crawford & Ostrom 1995 (institutional grammar); Gruber 1995 (minimal commitment) | If governance objects are "really" compositions, the ontology over-commits, violating minimal ontological commitment, and the category is dead weight | Disclosed in §6/§7 as a deliberate exception to the demote-to-composition rule, justified by the constitutive role of governance in ORGANVM's autopoiesis (AX-000-002/004). The exception is documented, not silent |
| RC-009 | The taxonomy is "categorically informed" (relations as morphisms, migrations as functors) without being categorically implemented | ADAPTED | Fong & Spivak 2019 | If composition laws are claimed but not enforced, schema migrations could silently lose structure while appearing principled | Disclosed in §8.3 as a regulative ideal, explicitly *not* an implementation requirement; full categorical formalization is deferred to a horizon-5 aspiration, so no enforcement promise is made |
| RC-010 | CONSTRAINT is a primitive ontological category (ONT-026), more fundamental than RULE and distinguished from it by amendment authority | NOVEL | Synthesized from SPEC-000 §7 (invariants) + Guarino & Welty 2004 meta-property reasoning; no single source treats constraint-vs-rule as an *ontological* distinction | If the distinction is unprincipled, the constitution/governance-rule boundary blurs and INV-000-004 (Constitutional Supremacy) loses its ontological footing | Marked NOVEL and FORMAL: the distinction is operationalized (constraints map to INV-###/AX-### in SPEC-000; rules live in governance-rules.json). The claim is testable — a constraint that can be changed without constitutional amendment would falsify it |

---

## Notes

1. **Why no CONTESTED rows.** SPEC-001 §8.1 asserts "No claims are CONTESTED."
   This register honors that by routing the two genuinely live disagreements
   into ADAPTED (RC-007, the realism debate) and NOVEL (RC-010, the
   constraint primitive). The disagreement is disclosed in the risk and
   mitigation columns rather than hidden — which is the intellectually honest
   form of "not CONTESTED": *we took a side and said so.*
2. **The single highest-leverage risk is RC-007.** It is the hinge on which
   AX-000-006 (Topological Plasticity) depends. The grounding narrative
   (`grounding.md` §3) defends it at length. If a future reviewer rejects
   pluralism, the mitigation path (revise only §1/§8.1) is pre-declared so the
   taxonomy tree survives.
3. **FORMALIZABLE ≠ unsupported.** Several GROUNDED claims (RC-001, RC-002) are
   FORMALIZABLE in SPEC-001's status vocabulary because their machine-checkable
   semantics await SPEC-003. The *grounding* is GROUNDED; the *formalization* is
   pending. The two axes are independent.
4. This register lists 10 classified claims, matching the count promised in
   SPEC-001 §10 ("Full risk register … 10 classified claims") and the §8.1
   distribution (6 GROUNDED / 3 ADAPTED / 1 NOVEL).
