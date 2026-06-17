# SPEC-002 Literature Matrix

```
Date:      2026-06-15
Status:    COMPLETE
Resolves:  GH#134
Phase:     R (Research) — gate G0 for SPEC-002 Phase F
Spec:      SPEC-002 (Primitive Register)
Scope:     Sources grounding the seven primitives + the §2 composition framework
```

---

## 1. Purpose

This matrix records every source that bears on SPEC-002's seven irreducible primitives
(Entity, Value, Relation, Event, State, Constraint, Capability) and on the §2 composition
framework (non-extensional mereology, dependent record types, typed composition). Each row
states the source's core claim, what SPEC-002 *borrows*, and — critically for honest
ontological engineering — *where SPEC-002 departs* from it. Departure columns are the
substance of the risk register; this matrix supplies their evidentiary basis.

BibTeX keys marked **[in bibliography.bib]** are cited by SPEC-002 but are not yet present in
`specs/bibliography.bib` (current bib carries only `MartinLof1984`, `CrawfordOstrom1995`,
and the type-theory lineage `WhiteheadRussell1910`/`Curry1934`/`Howard1980`/`MartinLof1982`).
The ontology-foundations cluster (Simons, Guarino & Welty, Masolo et al., Arp et al., Pierce,
von Wright, Johansson, Armstrong, Gruber, Searle, Ostrom) must be added to the canonical
bibliography during Phase F. See `source-archive.md` for full citations.

---

## 2. Matrix

| # | Source | Tradition | Core claim | What SPEC-002 borrows | Where it departs | BibTeX key |
|---|--------|-----------|------------|------------------------|------------------|------------|
| 1 | Simons, *Parts: A Study in Ontology* (1987) | Analytic / formal mereology | Classical Extensional Mereology is too strong; **Minimal Mereology (MM)** drops extensionality + unrestricted composition while keeping reflexivity, antisymmetry, transitivity, weak supplementation. Integral wholes are individuated by structure-determining relations, not by their parts alone. | §2.1 axiom table verbatim (MM retains 4 axioms, drops extensionality + unrestricted composition); the *integral whole* notion for organs/repos; essential vs. generic vs. rigid dependence (§2.3). | Simons is a pure descriptive metaphysician with no normative apparatus. SPEC-002 makes the structure-determining relations include **Constraints** (PRIM-006) — a deontic category Simons never countenances. Composition is governed, not merely structural. | `Simons1987` **[in bibliography.bib]** |
| 2 | Martin-Löf, *Intuitionistic Type Theory* (1984) | Constructive type theory | Types are built in a universe hierarchy (`Type_0 : Type_1 : …`); dependent function types (Π) and dependent pair types (Σ); propositions-as-types (a proposition is the type of its proofs). | Every primitive's *formal definition* is a Martin-Löf type signature. State as a Π-type over dimensions (PRIM-005). Constraint-as-`Prop` via propositions-as-types: a satisfying State is a term inhabiting the Constraint type (PRIM-006). `Type_0` as Entity's home universe (PRIM-001). | Martin-Löf type theory is purely constructive and value-free; SPEC-002 layers **deontic modality** (`MUST/SHOULD/MAY`) onto the `Prop` of Constraint, which standard ITT does not provide. SPEC-002 also uses **dependent record types** (§2.2), a definitional extension beyond bare Σ-types. | `MartinLof1984` (present) |
| 3 | Guarino & Welty, "Evaluating Ontological Decisions with OntoClean" (2002) | Applied ontology / formal methodology | Meta-properties — Rigidity (R), Identity (I), Unity (U), Dependence (D) — discipline subsumption taxonomies. Constraints: anti-rigid cannot subsume rigid; a property carrying identity cannot subsume one that does not; etc. | The OntoClean profile attached to each of the 7 primitives (+R/−R/~R, +I/−I, +U/−U, +D/−D). The §1 summary table's OntoClean column. Used as the gating discipline in `grounding.md` §(a). | OntoClean is a *taxonomic* discipline for is-a hierarchies; SPEC-002's seven primitives are **not** a subsumption taxonomy but a flat register of disjoint categories. SPEC-002 therefore borrows the meta-properties as *descriptive profiles* and *consistency checks*, not as subsumption constraints. | `GuarinoWelty2002` **[in bibliography.bib]** |
| 4 | Masolo et al., *Ontology Library (WonderWeb D18) — DOLCE* (2003) | Descriptive / cognitive upper ontology | DOLCE partitions reality into Endurants, Perdurants, Qualities, Abstracts; descriptive (cognitive-bias-friendly) rather than realist; recognizes Quality, State, Achievement/Accomplishment. | DOLCE alignment column for all 7 primitives. Endurant↔Entity, Quality↔Value, Perdurant↔Event, **State↔DOLCE State (homeomeric perdurant)** — the only foundational ontology that gives State partial credit (0.5/1). | DOLCE has **no normative category**, so Constraint and Capability score 0/1 against it. SPEC-002 retains both. SPEC-002 also flattens DOLCE's Endurant/Perdurant time-ontology distinction into a register where Event (perdurant) and Entity (endurant) are peers, not branches of a continuant/occurrent tree. | `MasoloEtAl2003` **[in bibliography.bib]** |
| 5 | Arp, Smith & Spear, *Building Ontologies with Basic Formal Ontology* (2015) | Realist upper ontology (BFO 2.0) | BFO partitions into Continuants (Independent / Specifically-Dependent / Generically-Dependent) and Occurrents (Process / Process Boundary). Dispositions split into the **Disposition/Role/Function** trichotomy. Realist: ontology mirrors mind-independent reality. | BFO alignment column for all 7. Entity↔Independent Continuant, Value↔Quality (SDC), Relation↔Relational Quality, Event↔Process, Capability↔Disposition/Realizable. The Disposition/Role/Function table under PRIM-007. | BFO **rejects State** as a category (aggregate of qualities → 0/1) and has **no normative category** (Constraint 0/1). BFO's realism conflicts with SPEC-002/SPEC-001's *constitutive* stance (entities are real because the constitution sustains them, not mind-independently). SPEC-002's unified Capability conflates BFO's trichotomy — acknowledged in the PRIM-007 disclosure. | `ArpSmithSpear2015` **[in bibliography.bib]** |
| 6 | Pierce, *Types and Programming Languages* (2002) | Programming-language theory | Operational treatment of type systems: records, variants, subtyping, references, recursive types; types as a tractable, decidable static discipline. | Mechanization bridge: the dependent **record type** of §2.2 (`CompositeObject = Record {…}`) and the §3 domain compositions (Agent, Artifact, Signal, GovernanceObject, Evidence, Process) are expressed in record syntax that Pierce's machinery makes implementable. Underwrites the FORMAL/FORMALIZABLE distinction. | Pierce's systems are largely **non-dependent** (record field types do not depend on prior field values); SPEC-002 needs *dependent* records, which exceeds TAPL's core and requires the Martin-Löf layer (row 2). Pierce supplies engineering tractability, not the dependent-type semantics. | `Pierce2002` **[in bibliography.bib]** |
| 7 | von Wright, "Deontic Logic" (1951) | Modal / deontic logic | Obligation (O), Permission (P), Prohibition (F) as modal operators over propositions, with interdefinability (F = ¬P; O = ¬P¬). | The `Deontic = MUST \| SHOULD \| MAY` parameter on Constraint (PRIM-006); MUST↔O, MAY↔P, ¬MAY↔F. The "deontic force is constitutive" argument in the PRIM-006 reduction test. | von Wright treats deontic operators over propositions in the abstract; SPEC-002 binds them to **States** as their argument domain (`Constraint : State -> Deontic -> Prop`), making the deontic operator range over complete configurations rather than arbitrary propositions. SHOULD (soft obligation) also exceeds the classic O/P/F triad. | `vonWright1951` **[in bibliography.bib]** |
| 8 | Crawford & Ostrom, "A Grammar of Institutions" (1995) | Institutional analysis / political economy | The **ADICO** syntax (Attributes, Deontic, aIm, Conditions, Or-else) decomposes institutional statements into rules, norms, and strategies. | Cited as the target grammar for full Constraint formalization (PRIM-006 defers ADICO structuring to SPEC-003/SPEC-005). The Deontic component of ADICO maps to SPEC-002's Deontic parameter. | SPEC-002 deliberately does **not** implement full ADICO at the primitive layer — it carries only the Deontic component and defers Attributes/aIm/Conditions/Or-else downstream. The departure is one of scope/timing, not disagreement. | `CrawfordOstrom1995` (present) |
| 9 | Ostrom, *Understanding Institutional Diversity* (2005) | Institutional analysis | Rules-in-use vs. rules-in-form: the operative rule may differ from the written rule; institutions are layered (operational/collective-choice/constitutional). | The PRIM-006 distinction between Constraints-as-declared (`governance-rules.json`) and Constraints-as-enforced (engine validators). Motivates the DRIFT classification in SPEC-002 §7.3. | Ostrom studies human commons-governance empirically; SPEC-002 applies the form/use distinction to a software-governance register where "rules-in-use" are validator code. Adaptation of domain, not a doctrinal departure. | `Ostrom2005` **[in bibliography.bib]** |
| 10 | Searle, *The Construction of Social Reality* (1995) | Philosophy of society / speech acts | Constitutive rules ("X counts as Y in context C") create institutional facts; collective intentionality and status functions. | Backstops the Contestation Disclosure for Constraint (§5.2): governance Constraints are *constitutive* rules, which justifies importing normativity into an ontological register. | SPEC-002 keeps only the constitutive-rule schema; it does not adopt Searle's collective-intentionality apparatus or his realism about brute facts. Used as philosophical cover, not as a formal source. | `Searle1995` **[in bibliography.bib]** |
| 11 | Johansson, *Ontological Investigations* (2004) | Realist category ontology | Dispositions/tendencies are **irreducible** to their manifestations (a sugar cube is soluble even while dry); relations and qualities are real categories. | The retention argument for Capability (PRIM-007): a deploy-capability exists even when unexercised. Independent (non-BFO) validation that tendencies are first-class. | Johansson would likely *also* accept a finer disposition taxonomy; SPEC-002 uses him to justify keeping a **unified** Capability now, flagging subdivision as future work. Selective use of an irreducibility thesis. | `Johansson2004` **[in bibliography.bib]** |
| 12 | Armstrong, *A Theory of Universals* (1978) | Analytic metaphysics | States of affairs and universals (properties/relations) as the truthmakers of predication; immanent realism about qualities. | Secondary grounding for Value (PRIM-002, qualities as first-class) and for State (PRIM-005, "states of affairs" as a respectable category). | Armstrong's states of affairs are truthmaker-theoretic, not the governance-domain snapshots SPEC-002 needs; SPEC-002's State is functionally motivated (the domain of Constraints), which Armstrong's apparatus neither requires nor supplies. | `Armstrong1978` **[in bibliography.bib]** |
| 13 | Gruber, "Toward Principles for the Design of Ontologies" (1993) | Knowledge engineering | **Minimal ontological commitment**: an ontology should commit only to what its application domain requires; clarity, coherence, extendability. | The decisive principle for *excluding* Process and Evidence from the register (§3.5–3.6, §5.4–5.5): do not elevate reducible domain concepts to primitives. Also licenses *including* Constraint (the governance domain requires it). | Gruber's principle cuts both ways and is a heuristic, not a proof; SPEC-002 uses it asymmetrically (to exclude Process/Evidence yet admit a non-standard Constraint), which is a defensible but contestable application. | `Gruber1993` **[in bibliography.bib]** |

---

## 3. Coverage Notes

- **Composition framework (§2)** is grounded by rows 1 (Simons / MM), 2 (Martin-Löf / dependent
  records), and 6 (Pierce / record mechanization). These three are load-bearing for the §3
  domain compositions and the Process/Evidence reductions.
- **Normative cluster** (rows 7–10) grounds the single most-contested primitive, Constraint
  (PRIM-006, NOVEL), which scores 0/2 against the descriptive ontologies (rows 4–5). The risk
  register treats this concentration of bespoke grounding as the spec's principal exposure.
- **OntoClean (row 3)** is methodological rather than substantive: it does not *justify* any
  primitive but disciplines the profiles assigned to all seven and is the engine of the
  `grounding.md` §(a) evaluation.
- All `[in bibliography.bib]` keys are cited in SPEC-002's body and lineage table (§7.4) but absent from the
  canonical `specs/bibliography.bib`; adding them is a Phase-F precondition (gate item).
