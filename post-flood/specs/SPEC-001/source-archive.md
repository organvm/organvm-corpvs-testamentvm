# SPEC-001 Source Archive: Ontology Charter

```
Date:        2026-06-15
Status:      DRAFT (Phase-R deliverable)
Resolves:    GH#133
Phase:       R (Research) — gate G0 for SPEC-001 Phase F
Parent Spec: SPEC-001 (Ontology Charter, v1.1, RATIFIED 2026-03-18)
Bibliography: specs/bibliography.bib
```

---

## Purpose and method

This is the annotated bibliography behind SPEC-001's entity taxonomy. Each entry
gives a full citation, a 2–4 sentence annotation explaining its role in the
charter, an open-access availability note, and the BibTeX key under which it
should appear in `specs/bibliography.bib`.

**Network restriction.** This archive was produced without network access; no
files were downloaded. Availability notes record the *known* open-access status
of each work from prior knowledge and should be re-verified by a human during
Phase F's source spot-check (required for any Categorical Restructuring per
SPEC-001 §9). They are claims about availability, not retrieved artifacts.

**Bibliography debt.** None of the eleven formal-ontology keys below currently
exist in `specs/bibliography.bib` — the present bibliography (68 entries) is
weighted toward the SPEC-018 logic/foundations lineage and contains no applied-
ontology sources. Inserting these entries is the primary action item for closing
gate G0. Proposed BibTeX stubs are provided after each annotation. Keys follow
the file's `AuthorYEAR` / `AuthorYEARa` convention.

---

## A. Mandatory sources (GH#133)

### Guarino, N. (1998) — Formal ontology and the four-level hierarchy

> Guarino, Nicola. "Formal Ontology in Information Systems." In *Formal Ontology
> in Information Systems (FOIS '98)*, ed. N. Guarino, 3–15. Amsterdam: IOS Press,
> 1998.

The founding statement that ontologies are engineering artifacts subject to
design discipline, and the source of the four-level distinction (top-level,
domain, task, application ontologies). SPEC-001 positions itself as a *top-level*
ontology on which SPEC-002's domain compositions sit, and inherits Guarino's
insistence that ontological commitment be made explicit. Used in SPEC-001 §1 and
§ONT-028 (the four-level hierarchy places Type at the top level).

*Open access: the FOIS '98 proceedings volume is not uniformly open; an
author preprint of this paper has historically circulated freely from CNR-ISTC
(Trento/Padova) institutional pages. Treat as likely-available preprint,
verify.*

```bibtex
@inproceedings{Guarino1998,
  author    = {Nicola Guarino},
  title     = {Formal Ontology in Information Systems},
  booktitle = {Formal Ontology in Information Systems (FOIS '98)},
  editor    = {Nicola Guarino},
  publisher = {IOS Press},
  address   = {Amsterdam},
  pages     = {3--15},
  year      = {1998},
  keywords  = {formal-ontology, four-level-hierarchy, ontological-commitment, SPEC-001}
}
```

### Smith, B. (2004) — Ontology as reality representation (BFO realism)

> Smith, Barry. "Beyond Concepts: Ontology as Reality Representation." In
> *Formal Ontology in Information Systems (FOIS 2004)*, ed. A. Varzi and L. Vieu,
> 73–84. Amsterdam: IOS Press, 2004.

The clearest statement of BFO's realist programme: ontological categories name
universals in mind-independent reality, and ontologies are discovered rather than
designed. SPEC-001 §8.1 cites Smith precisely as the position it *declines* to
adopt, choosing DOLCE-aligned pluralism instead. Essential as the named
counterposition to the central ADAPTED claim (risk register RC-007).

*Open access: a freely downloadable author copy has long been available from
Barry Smith's University at Buffalo publications page (ontology.buffalo.edu).
Likely available, verify.*

```bibtex
@inproceedings{Smith2004,
  author    = {Barry Smith},
  title     = {Beyond Concepts: Ontology as Reality Representation},
  booktitle = {Formal Ontology in Information Systems (FOIS 2004)},
  editor    = {Achille Varzi and Laure Vieu},
  publisher = {IOS Press},
  address   = {Amsterdam},
  pages     = {73--84},
  year      = {2004},
  keywords  = {BFO, realism, universals, reality-representation, SPEC-001}
}
```

### Gruber, T. (1995) — Design principles for shared ontologies

> Gruber, Thomas R. "Toward Principles for the Design of Ontologies Used for
> Knowledge Sharing." *International Journal of Human-Computer Studies* 43,
> nos. 5–6 (1995): 907–928.

The journal-length statement of Gruber's design criteria and the source of the
"minimal ontological commitment" principle that lets multiple agents share
knowledge without over-specifying. SPEC-001 uses this principle to demote the
Stage-II domain entities to compositions (§6). Companion to the earlier 1993
technical report (below), which states the five criteria SPEC-001 §6 enumerates;
SPEC-001's §1 currently cites "Gruber 1993," so both keys are archived and the
§6 citation should be made precise during Phase F.

*Open access: an author preprint (KSL-93-04 lineage) has circulated freely from
Stanford KSL / tomgruber.org for decades. Likely available, verify.*

```bibtex
@article{Gruber1995,
  author    = {Thomas R. Gruber},
  title     = {Toward Principles for the Design of Ontologies Used for Knowledge Sharing},
  journal   = {International Journal of Human-Computer Studies},
  volume    = {43},
  number    = {5--6},
  pages     = {907--928},
  year      = {1995},
  keywords  = {ontology-design, minimal-commitment, knowledge-sharing, SPEC-001}
}

@techreport{Gruber1993,
  author      = {Thomas R. Gruber},
  title       = {A Translation Approach to Portable Ontology Specifications},
  institution = {Stanford Knowledge Systems Laboratory},
  number      = {KSL 92-71},
  year        = {1993},
  note        = {Also in Knowledge Acquisition 5(2): 199--220, 1993},
  keywords    = {ontology-as-specification, five-criteria, conceptualization, SPEC-001}
}
```

### Sowa, J. (2000) — Knowledge representation foundations

> Sowa, John F. *Knowledge Representation: Logical, Philosophical, and
> Computational Foundations*. Pacific Grove, CA: Brooks/Cole, 2000.

A comprehensive synthesis of logic, philosophy (Peirce's and Whitehead's
categories), and computation as the three legs of knowledge representation.
SPEC-001 §3 borrows Sowa's analysis of relations as first-class triadic
*Relative* entities that mediate between relata without reducing to either —
grounding HierarchyEdge, LineageRecord, and NameRecord as identity-bearing
relations (risk register RC-004). SPEC-001 does not adopt Sowa's full Peircean
Firstness/Secondness/Thirdness lattice.

*Open access: a commercial textbook; not open access. Portions and Sowa's
conceptual-structures material are freely available on jfsowa.com. Verify
chapter availability for any quoted passage.*

```bibtex
@book{Sowa2000,
  author    = {John F. Sowa},
  title     = {Knowledge Representation: Logical, Philosophical, and Computational Foundations},
  publisher = {Brooks/Cole},
  address   = {Pacific Grove, CA},
  year      = {2000},
  keywords  = {knowledge-representation, triadic-relations, conceptual-structures, SPEC-001}
}
```

### Arp, R., Smith, B. & Spear, A. (2015) — Building Ontologies with BFO

> Arp, Robert, Barry Smith, and Andrew D. Spear. *Building Ontologies with Basic
> Formal Ontology*. Cambridge, MA: MIT Press, 2015.

The canonical engineering manual for BFO and the structural backbone of SPEC-001.
It supplies the Continuant/Occurrent partition, the Independent / Specifically-
Dependent / Generically-Dependent continuant distinction, the inherence relation,
and the treatment of process boundaries as instantaneous occurrents — i.e. the
spine of ONT-002 through ONT-020 and ONT-036. SPEC-001 keeps this structure but
strips BFO's realist commitment, reading the categories as descriptive scaffolding
(§8.1).

*Open access: published by MIT Press; the book is available open access under a
Creative Commons license via MIT Press Direct / OAPEN. Likely freely available
as full-text PDF, verify.*

```bibtex
@book{ArpSmithSpear2015,
  author    = {Robert Arp and Barry Smith and Andrew D. Spear},
  title     = {Building Ontologies with Basic Formal Ontology},
  publisher = {MIT Press},
  address   = {Cambridge, MA},
  year      = {2015},
  keywords  = {BFO, continuant, occurrent, SDC, GDC, inherence, SPEC-001}
}
```

### Baader, F. et al. (2003) — The Description Logic Handbook

> Baader, Franz, Diego Calvanese, Deborah L. McGuinness, Daniele Nardi, and
> Peter F. Patel-Schneider, eds. *The Description Logic Handbook: Theory,
> Implementation, and Applications*. Cambridge: Cambridge University Press, 2003.

The reference work for description logics — concepts, roles, individuals, TBox/
ABox, and decidable subsumption reasoning. SPEC-001 borrows DL's discipline of
machine-checkable subsumption and its flavor in the FORMAL / FORMALIZABLE /
JUDGMENT status vocabulary, treating `category_path` as a TBox-style
classification. The charter does *not* commit to a DL reasoner or to
decidability; JUDGMENT-tier categories are explicitly outside DL's reach.

*Open access: a commercial CUP handbook; not open access. The editors' draft
chapters have at times circulated from TU Dresden / institutional pages. Treat
the full handbook as paywalled; verify any draft chapter.*

```bibtex
@book{Baader2003,
  editor    = {Franz Baader and Diego Calvanese and Deborah L. McGuinness and Daniele Nardi and Peter F. Patel-Schneider},
  title     = {The Description Logic Handbook: Theory, Implementation, and Applications},
  publisher = {Cambridge University Press},
  year      = {2003},
  keywords  = {description-logic, subsumption, TBox, ABox, SPEC-001, SPEC-004}
}
```

---

## B. Optional / supporting sources cited by SPEC-001

### Masolo, C. et al. (2003) — DOLCE (WonderWeb Deliverable D18)

> Masolo, Claudio, Stefano Borgo, Aldo Gangemi, Nicola Guarino, and Alessandro
> Oltramari. *Ontology Library*. WonderWeb Deliverable D18, Laboratory for
> Applied Ontology, ISTC-CNR, Trento, 2003.

The specification of DOLCE, the descriptive upper ontology that grounds SPEC-001's
pluralist stance. It supplies the descriptive reading of categories (cognitive/
linguistic adequacy rather than mind-independent universals), the treatment of
Quality as a first-class entity (grounding VARIABLE/METRIC as identity-bearing
qualities), and Abstract as a disjoint third top-level category (ONT-023).
SPEC-001 chooses DOLCE over BFO at the realism hinge (§8.1, RC-007).

*Open access: the WonderWeb D18 deliverable is a freely distributed technical
report, long available from the Laboratory for Applied Ontology (loa.istc.cnr.it).
Likely freely available, verify.*

```bibtex
@techreport{MasoloEtAl2003,
  author      = {Claudio Masolo and Stefano Borgo and Aldo Gangemi and Nicola Guarino and Alessandro Oltramari},
  title       = {Ontology Library (DOLCE)},
  institution = {Laboratory for Applied Ontology, ISTC-CNR},
  number      = {WonderWeb Deliverable D18},
  address     = {Trento},
  year        = {2003},
  keywords    = {DOLCE, descriptive-ontology, quality, endurant, perdurant, abstract, SPEC-001}
}
```

### Guarino, N. & Welty, C. (2004) — OntoClean

> Guarino, Nicola, and Christopher A. Welty. "An Overview of OntoClean." In
> *Handbook on Ontologies*, ed. S. Staab and R. Studer, 151–171. Berlin:
> Springer, 2004.

The methodology behind the +/-R (rigidity), +/-I (identity), +/-D (dependence)
meta-property annotations on every ONT node. Its rigid-cannot-be-subsumed-by-
anti-rigid theorem is the formal basis for SPEC-001 §8.2's argument that the flat
enum is structurally unsound (METRIC, -R, cannot be a peer of ORGAN, +R). SPEC-001
omits OntoClean's Unity (U) meta-property and applies the method as a design audit
(FORMALIZABLE), not a runtime validator.

*Open access: the *Handbook on Ontologies* is a commercial Springer volume;
author copies of the OntoClean overview have circulated freely. An earlier CACM
version (Guarino & Welty 2002, "Evaluating ontological decisions with OntoClean")
is more widely accessible. Verify.*

```bibtex
@incollection{GuarinoWelty2004,
  author    = {Nicola Guarino and Christopher A. Welty},
  title     = {An Overview of OntoClean},
  booktitle = {Handbook on Ontologies},
  editor    = {Steffen Staab and Rudi Studer},
  publisher = {Springer},
  address   = {Berlin},
  pages     = {151--171},
  year      = {2004},
  keywords  = {OntoClean, meta-properties, rigidity, identity, dependence, SPEC-001}
}
```

### Fong, B. & Spivak, D. (2019) — Applied category theory

> Fong, Brendan, and David I. Spivak. *An Invitation to Applied Category Theory:
> Seven Sketches in Compositionality*. Cambridge: Cambridge University Press,
> 2019.

The accessible introduction to applied category theory that SPEC-001 §8.3 invokes
as a *regulative ideal*: relation types as morphisms, composition laws as
invariants, schema migrations as functorial mappings. The charter is "categorically
informed, not categorically implemented" — no proof assistant is used and full
formalization is a deferred horizon-5 aspiration (RC-009, ADAPTED).

*Open access: the authors' preprint, "Seven Sketches in Compositionality," is
freely available on arXiv (arXiv:1803.05316). Freely available.*

```bibtex
@book{FongSpivak2019,
  author    = {Brendan Fong and David I. Spivak},
  title     = {An Invitation to Applied Category Theory: Seven Sketches in Compositionality},
  publisher = {Cambridge University Press},
  year      = {2019},
  note      = {Preprint arXiv:1803.05316},
  keywords  = {applied-category-theory, morphisms, functors, compositionality, SPEC-001}
}
```

### Luhmann, N. (1995) — Social Systems (constitutive reality)

> Luhmann, Niklas. *Social Systems*. Trans. John Bednarz Jr. with Dirk Baecker.
> Stanford: Stanford University Press, 1995.

Inherited from SPEC-000; SPEC-001 §1 uses Luhmann to license the "constitutive
reality" reading of entity types — real, but communicatively/constitutionally
constituted rather than mind-independent. This is the philosophical move that
makes DOLCE pluralism coherent for an artifact like ORGANVM.

*Open access: a commercial Stanford UP translation; not open access. Verify
library access for any quotation.*

```bibtex
@book{Luhmann1995,
  author    = {Niklas Luhmann},
  title     = {Social Systems},
  translator = {John Bednarz Jr. and Dirk Baecker},
  publisher = {Stanford University Press},
  address   = {Stanford},
  year      = {1995},
  keywords  = {social-systems, communicative-autopoiesis, constitutive-reality, SPEC-000, SPEC-001}
}
```

### Ostrom, E. (1990) — Governing the Commons (institutional grounding)

> Ostrom, Elinor. *Governing the Commons: The Evolution of Institutions for
> Collective Action*. Cambridge: Cambridge University Press, 1990.

The institutional-design grounding for treating ORGAN/REPO as constitutional
units (ONT-004/005) and for elevating Governance Object to a first-class
ontological category (ONT-024, RC-008). Read alongside Crawford & Ostrom (1995),
already in the bibliography as `CrawfordOstrom1995`, which supplies the
institutional grammar (ADICO) behind RULE/CONSTRAINT.

*Open access: a commercial CUP monograph; not open access. The companion paper
Crawford & Ostrom 1995 (already keyed) is the more accessible institutional-
grammar source. Verify.*

```bibtex
@book{Ostrom1990,
  author    = {Elinor Ostrom},
  title     = {Governing the Commons: The Evolution of Institutions for Collective Action},
  publisher = {Cambridge University Press},
  year      = {1990},
  keywords  = {institutional-design, commons, governance, SPEC-000, SPEC-001}
}
```

---

## C. Already in the bibliography (cross-reference)

The following SPEC-001-relevant source is already present in
`specs/bibliography.bib` and needs no new entry:

| Author | Existing key | SPEC-001 use |
|--------|-------------|--------------|
| Crawford & Ostrom (1995), *A Grammar of Institutions* | `CrawfordOstrom1995` | Institutional grammar (ADICO) behind ONT-025 RULE / ONT-026 CONSTRAINT |

SPEC-001 §10's "Academic Lineage" table also cites Beer (1972), Ashby (1956),
Newman (2018), and Damasio (1999) for the cybernetics/systems clusters
(ONT-040–052). These are SPEC-000-lineage sources outside the formal-ontology
scope of GH#133 and are not archived here; they are flagged as additional
bibliography debt for whichever Phase-R deliverable grounds the state/process
clusters.

---

## D. Action items for gate G0

1. **Insert 11 proposed entries** (Section A: 6 mandatory + Gruber1993 companion;
   Section B: 5 supporting) into `specs/bibliography.bib`. None exist today.
2. **Reconcile the Gruber citation** in SPEC-001 §1/§6 (currently "Gruber 1993")
   against the GH#133 source list ("Gruber 1995"); keep both keys, cite the 1993
   report for the five criteria and the 1995 paper for minimal commitment.
3. **Human source spot-check** of availability notes (network was restricted
   during this Phase-R pass) — required anyway under SPEC-001 §9 for any future
   Categorical Restructuring, and prudent before Phase F sign-off.
