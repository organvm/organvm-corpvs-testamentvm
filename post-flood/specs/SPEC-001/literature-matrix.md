# SPEC-001 Literature Matrix: Ontology Charter

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

This matrix maps each load-bearing source behind SPEC-001's stratified entity
taxonomy (SPEC-001 §2, §6) to (a) the tradition it represents, (b) its core
ontological claim, (c) what SPEC-001 borrows from it, (d) where SPEC-001
*departs* from it, and (e) the BibTeX key under which it should be cited.

**Bibliography status (RESOLVED 2026-06-15).** SPEC-001 cites all of the sources
below, and the formal-ontology keys are now **present in `specs/bibliography.bib`**
(added 2026-06-15 alongside this Phase-R work — `Guarino1998`, `Smith2004`,
`Gruber1993`/`Gruber1995`, `Sowa2000`, `ArpSmithSpear2015`, `Baader2003`,
`MasoloEtAl2003`, `GuarinoWelty2004`, `FongSpivak2019`, `Luhmann1995`,
`Ostrom1990`). The earlier bibliography-debt that blocked gate G0 is therefore
**cleared**; the `[in bibliography.bib]` marker in the table below confirms each
key resolves. See `source-archive.md` for full citations. Keys follow the
existing `AuthorYEAR` / `AuthorYEARa` convention.

---

## Matrix

| Source | Tradition | Core claim | What SPEC-001 borrows | Where it departs | BibTeX key |
|--------|-----------|------------|-----------------------|------------------|------------|
| Guarino (1998), *Formal Ontology in Information Systems* | Formal ontology / applied ontology engineering | Ontologies are engineering artifacts; a four-level hierarchy separates top-level, domain, task, and application ontologies, and the top level must be domain-independent | The four-level layering — SPEC-001 positions itself as a *top-level* ontology (ONT-001–ONT-003 are domain-independent) on which domain compositions (SPEC-002) sit; the principle that ontological commitment must be made explicit | Guarino treats the top level as ideally universal/discoverable; SPEC-001 treats its top level as *constitutively* real (declared by the constitution), not mind-independently universal | `Guarino1998` `[in bibliography.bib]` |
| Smith (2004), *Beyond Concepts: Ontology as Reality Representation* | Basic Formal Ontology (BFO) / philosophical realism | Ontological categories name universals existing in mind-independent reality; ontologies should be *discovered*, not designed | The Continuant/Occurrent partition and the SDC/GDC structure of dependent entities | Rejects BFO's realism: SPEC-001 holds entity types are designed and constitutionally sustained, not discovered universals (§8.1) | `Smith2004` `[in bibliography.bib]` |
| Arp, Smith & Spear (2015), *Building Ontologies with Basic Formal Ontology* | BFO engineering manual | Operationalizes BFO: Continuant vs Occurrent; Independent / Specifically-Dependent / Generically-Dependent Continuants; inherence; process boundaries | The entire spine of ONT-002–ONT-020: Continuant/Occurrent, the three dependence modes, inherence (ONT-036), process boundary as event (ONT-017, ONT-052) | Drops BFO's realist commitment and its single mandated upper ontology; treats BFO categories as a *descriptive scaffold* rather than a map of reality | `ArpSmithSpear2015` `[in bibliography.bib]` |
| Masolo et al. (2003), *Ontology Library (DOLCE)* (WonderWeb D18) | Descriptive ontology / cognitive-linguistic pluralism | DOLCE is a *descriptive* upper ontology: categories track cognitive/linguistic structure of a domain; Endurant/Perdurant/Quality/Abstract; Quality is a first-class entity | The pluralist stance (§1, §8.1); Abstract as a disjoint third top-level category (ONT-023); Quality-as-entity for VARIABLE/METRIC (ONT-008/009) | SPEC-001 narrows DOLCE's four leaves to the ORGANVM domain and grounds reality in *constitutional constitution* rather than DOLCE's neutrality on realism | `MasoloEtAl2003` `[in bibliography.bib]` |
| Gruber (1993), *A Translation Approach to Portable Ontology Specifications* | Applied ontology / knowledge sharing | An ontology is "a specification of a conceptualization"; design criteria: clarity, coherence, extendibility, minimal encoding bias, minimal ontological commitment | The five design criteria are adopted verbatim as the acceptance test for the taxonomy (§6, "Gruber's five criteria"); the "specification of a conceptualization" framing | None material — SPEC-001 treats Gruber's criteria as binding design constraints rather than departing | `Gruber1993` `[in bibliography.bib]` |
| Gruber (1995), *Toward Principles for the Design of Ontologies Used for Knowledge Sharing* | Applied ontology / knowledge sharing | Journal-length statement of the same design principles; minimal ontological commitment lets multiple agents share knowledge without over-specifying | Cited as the principled basis for "minimal ontological commitment" — only categories needed for cross-organ knowledge sharing are committed to | None material; SPEC-001 uses the 1995 principles to justify *demoting* the Stage-II domain entities to compositions (§6) | `Gruber1995` `[in bibliography.bib]` |
| Sowa (2000), *Knowledge Representation: Logical, Philosophical, and Computational Foundations* | Knowledge representation / conceptual structures | A KR ontology must integrate logic, philosophy (Peirce/Whitehead categories), and computation; relations are triadic and are themselves first-class | Relations treated as first-class *Relative* entities mediating between relata, not reducible to either (SPEC-001 §3) | SPEC-001 does not adopt Sowa's full Peircean Firstness/Secondness/Thirdness lattice; it borrows only the triadic-relation insight | `Sowa2000` `[in bibliography.bib]` |
| Baader et al. (2003), *The Description Logic Handbook* | Description logics / formal KR | Concepts, roles, and individuals admit decidable subsumption reasoning; TBox (terminology) vs ABox (assertions); rigor in subsumption hierarchies | The discipline of machine-checkable subsumption; the FORMAL/FORMALIZABLE formalization-status vocabulary is DL-flavored (what a reasoner could decide); category_path as a TBox-style classification | SPEC-001 does *not* commit to a DL reasoner or to decidability; it uses DL as a regulative standard, with "JUDGMENT"-tier categories explicitly outside DL's reach | `Baader2003` `[in bibliography.bib]` |
| Guarino & Welty (2004), *An Overview of OntoClean* | Applied ontology methodology (meta-properties) | Subsumption must respect meta-properties: rigidity (R), identity (I), dependence (D), unity (U); anti-rigid types may not subsume rigid types | The +/-R, +/-I, +/-D annotations on every ONT category; the structural argument against the flat enum (§8.2); the constraint that VARIABLE/METRIC (-R) sit under a rigid supertype | SPEC-001 omits Unity (U) and applies OntoClean as a *design audit*, not as a runtime validator (it is FORMALIZABLE, not yet FORMAL) | `GuarinoWelty2004` `[in bibliography.bib]` |
| Fong & Spivak (2019), *An Invitation to Applied Category Theory* | Applied category theory | Compositional systems are modeled as categories; relations are morphisms; structure-preserving maps are functors | Relation types as morphisms, composition laws as invariants, schema migration as functorial mapping (§8.3) | Adopted only as a *regulative ideal* — "categorically informed, not categorically implemented"; no proof assistant or categorical language is used | `FongSpivak2019` `[in bibliography.bib]` |
| Luhmann (1995), *Social Systems* | Sociological systems theory / communicative autopoiesis | Social systems are real but constituted by communication, not by physical substrate | The pluralist grounding of "constitutive reality" — entity types are real but communicatively/constitutionally constituted (§1) | Inherited from SPEC-000; SPEC-001 uses it only to license the constitutive-reality reading of DOLCE pluralism | `Luhmann1995` `[in bibliography.bib]` |
| Ostrom (1990), *Governing the Commons* | Institutional design / polycentric governance | Durable institutions arise from explicit, monitored, graduated rules under collective choice | Justification for promoting Governance Object to an ontological category (ONT-024) and for ORGAN/REPO as constitutional units (ONT-004/005) | SPEC-001 uses Ostrom only at the institutional-design layer; it does not import her empirical commons findings | `Ostrom1990` `[in bibliography.bib]` |

---

## Coverage Check (against GH#133 required sources)

| Required source | Covered | Row |
|-----------------|---------|-----|
| Guarino 1998 | Yes | 1 |
| Smith 2004 | Yes | 2 |
| Gruber 1995 | Yes | 6 (with 1993 companion in row 5) |
| Sowa 2000 | Yes | 7 |
| Arp/Smith/Spear 2015 | Yes | 3 |
| Baader et al. 2003 | Yes | 8 |
| Welty/Guarino OntoClean (optional) | Yes | 9 |
| DOLCE / Masolo 2003 (optional) | Yes | 4 |

All six mandatory sources plus both optional sources are represented. Two
additional rows (Fong & Spivak 2019, Luhmann 1995, Ostrom 1990) are included
because SPEC-001 §1, §3, §8.3 and §10 cite them as load-bearing for the
charter's relation model, pluralist stance, and governance categories.

---

## Notes for Phase F

1. **Bibliography debt — CLEARED (2026-06-15).** The eleven formal-ontology keys
   are now present in `specs/bibliography.bib` (full entries added alongside this
   Phase-R work), so every SPEC-001 claim traces to a citable source. This is no
   longer a G0 blocker.
2. **Gruber appears twice** (1993 and 1995). SPEC-001 §1 cites "Gruber 1993" for
   the five criteria; the GH#133 source list names "Gruber 1995." Both are real
   and both state the same design principles; the matrix retains both and the
   source archive notes the relationship so the citation in §6 can be made
   precise.
3. The **departure column is the contested surface.** Rows 2 (Smith) and 4
   (Masolo) encode the BFO-realism-vs-DOLCE-pluralism decision that the
   grounding narrative and risk register treat as the central ADAPTED claim.
