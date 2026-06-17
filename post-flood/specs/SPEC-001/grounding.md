# SPEC-001 Grounding Narrative: Ontology Charter

```
Date:        2026-06-15
Status:      DRAFT (Phase-R deliverable)
Resolves:    GH#133
Phase:       R (Research) — gate G0 for SPEC-001 Phase F
Parent Spec: SPEC-001 (Ontology Charter, v1.1, RATIFIED 2026-03-18)
Bibliography: specs/bibliography.bib
```

---

## 1. What this narrative grounds

SPEC-001 replaces ORGANVM's original flat entity enumeration —
`ORGAN | REPO | MODULE | DOCUMENT | SESSION | VARIABLE | METRIC` — with a
stratified taxonomy rooted at a single sortal (Entity, ONT-001) and branching
through three mutually exclusive top-level categories: Continuant (ONT-002),
Occurrent (ONT-013), and Abstract (ONT-023). Beneath Continuant the charter
distinguishes Independent, Specifically-Dependent, and Generically-Dependent
continuants; beneath Occurrent it distinguishes Process, Event, and Temporal
Region; beneath Abstract it places Governance Objects, Capability, and Type.

The question this document answers is the one AX-000-001 (Ontological Primacy)
places before all others: *on what authority does this particular carving of
being rest?* The answer is that the taxonomy is borrowed, almost in its
skeleton, from the formal-ontology tradition that matured around Basic Formal
Ontology (BFO) and the Descriptive Ontology for Linguistic and Cognitive
Engineering (DOLCE), and that the two points where ORGANVM departs from that
tradition are deliberate, disclosed, and defensible.

## 2. The borrowed skeleton: BFO and DOLCE convergence

The single most important fact for grounding SPEC-001 is that two upper
ontologies built on opposite metaphysical commitments nonetheless *converge* on
the structural distinctions ORGANVM needs. Arp, Smith & Spear (2015), the
canonical engineering manual for BFO, partition reality into Continuants
(entities wholly present at each moment they exist) and Occurrents (entities
that unfold and have temporal parts). Masolo et al. (2003), the WonderWeb D18
specification of DOLCE, draw the same line under different names — Endurants and
Perdurants. When a realist ontology and a descriptivist ontology, designed by
rival research programmes, agree on a partition, that partition is about as
close to a settled result as applied ontology offers. SPEC-001 takes ONT-002 and
ONT-013 directly from this convergence (risk register RC-001, GROUNDED).

The same convergence underwrites the dependence structure. BFO's tripartite
split of continuants — Independent Continuant, Specifically-Dependent Continuant
(SDC), Generically-Dependent Continuant (GDC) — gives ORGANVM exactly the
distinctions it needs to model three observably different lifecycles. An ORGAN,
REPO, or MODULE (ONT-004–006) bears qualities and stands on its own: it is an
Independent Continuant. A VARIABLE or METRIC (ONT-008/009) cannot exist apart
from the entity it characterizes and dies with it: it is an SDC, inhering in
exactly one bearer (the inherence relation, ONT-036, is lifted straight from
BFO). A DOCUMENT or SCHEMA (ONT-011/012) depends on *some* carrier but can be
copied and migrated without losing identity: it is a GDC, an information content
entity. This is RC-002 (GROUNDED): the BFO categories map onto behaviors the
running system already exhibits, so the ontology is descriptively adequate
before any new code is written.

DOLCE supplies two things BFO does not emphasize. First, **Quality as a
first-class entity**: DOLCE treats a quality as an entity with its own identity
and temporal history, not as a mere attribute of its bearer. This is precisely
how `organvm-ontologia` already behaves — VARIABLE and METRIC instances receive
their own ULIDs and carry append-only value histories — so DOLCE, not BFO,
licenses the implementation that already exists (§6, criterion 3). Second,
DOLCE admits **Abstract** as a disjoint third top-level category alongside
endurants and perdurants. ORGANVM needs this category badly: RULE, CONSTRAINT,
Capability, and Type are neither persisting things nor unfolding processes —
they are non-spatiotemporal, logically constituted entities. ONT-023 takes
DOLCE's Abstract wholesale (RC-006, GROUNDED, with a JUDGMENT boundary noted at
the abstract/concretization seam).

## 3. The chosen departure: descriptive pluralism over strict realism

Here the two traditions stop agreeing, and SPEC-001 must choose. Smith (2004)
argues that ontological categories name *universals existing in mind-independent
reality*; under strict BFO realism an ontology is discovered, and a category is
correct only insofar as it carves nature at a real joint. Masolo et al. (2003)
take the descriptivist line: DOLCE's categories are reasonable cognitive and
linguistic constructs adequate to a domain, making no claim to mind-independent
universals.

**ORGANVM adopts DOLCE-aligned descriptive pluralism** (SPEC-001 §1, §8.1; risk
register RC-007, ADAPTED). The reason is not philosophical preference but
structural necessity. ORGANVM's entities are not found in nature; an ORGAN
exists *because the constitution declares and sustains it*. Their reality is
**constitutive** — real, but real in the way Luhmann (1995) holds social systems
to be real: constituted by communication (here, by governance communications and
the registry) rather than by physical substrate. To demand that an ORGAN
correspond to a mind-independent universal would be a category error about what
kind of thing ORGANVM is.

The decisive practical consequence concerns evolution. AX-000-006 (Topological
Plasticity) makes the organ topology a *governed variable*: organs may
crystallize, fuse, split, or dissolve through constitutional revision. Under
strict realism, every such mutation would have to be defended as a better
approximation to a pre-existing real joint — an incoherent demand for an
artifact the system invents. Under descriptive pluralism, a new category is
legitimate when it is clear, coherent, and useful for cross-organ knowledge
sharing — Gruber's criteria, not metaphysical discovery. Pluralism is therefore
the *only* stance consistent with the system's own constitutional commitment to
self-modification. This is why RC-007 is the highest-leverage claim in the risk
register: if a reviewer insists on realism, AX-000-006 loses its grounding. The
mitigation is pre-declared — the pluralist commitment is isolated in §1 and
§8.1, so a future reversal would touch the framing, not the taxonomy tree.

Choosing DOLCE's stance does not mean abandoning BFO's structure. SPEC-001 keeps
the BFO scaffold (Continuant/Occurrent, SDC/GDC, inherence, process boundaries)
and reinterprets its *modal status*: the categories are descriptive scaffolding
sustained by the constitution, not a map of discovered reality. This is the
sense in which the charter is "BFO-shaped, DOLCE-grounded."

## 4. The disciplining instruments: OntoClean, Gruber, Description Logic

Three further sources do not supply categories but discipline how the categories
are arranged.

**OntoClean** (Guarino & Welty 2004) supplies the meta-properties — rigidity
(R), identity (I), dependence (D) — annotated on every ONT node. Its central
theorem is that an anti-rigid type may not subsume a rigid one. This is what
makes the flat-enum problem (§8.2) a *structural* defect rather than a stylistic
one: the old enum treated ORGAN (+R rigid) and METRIC (-R anti-rigid) as
ontological peers. OntoClean shows this is unsound, and the stratified taxonomy
fixes it by subordinating the anti-rigid qualities (VARIABLE, METRIC) under the
rigid SpecificallyDependentContinuant supertype (RC-003, GROUNDED). The analysis
is mechanical and reproducible by a second agent — which is exactly the kind of
checkable grounding Phase F requires.

**Gruber** (1993, 1995) supplies the acceptance test. His five criteria —
clarity, coherence, extendibility, minimal encoding bias, minimal ontological
commitment — are applied explicitly in §6 and adopted as binding (RC-005,
GROUNDED). "Minimal ontological commitment" does real work: it is the principle
under which SPEC-001 *demotes* the Stage-II "domain entities" (Agent, Artifact,
Signal, Evidence Object) to compositions of primitives rather than admitting
them as new top-level kinds (§6). The ontology commits only to categories
necessary for cross-organ knowledge sharing.

**Description logic** (Baader et al. 2003) supplies the standard of rigor for the
subsumption hierarchy and the vocabulary behind the FORMAL / FORMALIZABLE /
JUDGMENT status tags. SPEC-001 does not commit to a DL reasoner or to
decidability; it borrows the discipline (a TBox-style `category_path`
classification a reasoner *could* in principle check) while reserving JUDGMENT
tier for categories like ONT-023 and ONT-028 whose boundaries are modeling
decisions outside any reasoner's reach. Sowa (2000) rounds this out at the
relation layer: relations are first-class triadic *Relative* entities that
mediate between relata without reducing to either, which is why HierarchyEdge,
LineageRecord, and NameRecord (ONT-030–032) carry their own identity (RC-004,
GROUNDED).

Finally, Fong & Spivak (2019) are invoked as a *regulative ideal* (§8.3, RC-009,
ADAPTED): relation types are read as morphisms and schema migrations as
functorial mappings, but the system is "categorically informed, not
categorically implemented." No proof assistant is used; full categorical
formalization is an explicitly deferred horizon-5 aspiration. The honest move
here is the refusal to promise enforcement that does not exist.

## 5. What is genuinely novel

Two commitments have no clean academic precedent and are flagged as such.

The first is **CONSTRAINT as a primitive ontological category** (ONT-026; risk
register RC-010, NOVEL). The formal-ontology literature treats axioms and
integrity constraints as *features of* an ontology's logical encoding, not as
*entities within* the domain. SPEC-001 reifies the constraint: ONT-026 is an
Abstract entity, more fundamental than RULE (ONT-025), distinguished from it by
amendment authority — a rule may change through governed process, a constraint
only through constitutional amendment. This gives INV-000-004 (Constitutional
Supremacy) an ontological footing rather than merely a procedural one. The claim
is genuinely novel but not unfalsifiable: a constraint that could be revised
*without* constitutional amendment would refute the distinction, and the
distinction is operationalized (constraints correspond to INV-###/AX-###
identifiers; rules live in `governance-rules.json`).

The second novelty is closely related: the **elevation of Governance Object**
(ONT-024) from a demoted domain composition to a first-class category (RC-008,
ADAPTED). Minimal ontological commitment would normally demote it alongside
Agent and Artifact. SPEC-001 makes a documented exception because governance is
constitutive of ORGANVM's autopoiesis (AX-000-002, AX-000-004): a system whose
very mode of self-production is governance cannot treat governance objects as
incidental compositions. Ostrom (1990) and Crawford & Ostrom (1995) ground the
institutional reading; the elevation itself is the adaptation.

## 6. Honest account of contestation

This narrative does not claim consensus where there is none. The realism-vs-
descriptivism question (§3) is a live, unresolved dispute in formal ontology, and
ORGANVM has taken the descriptivist side; it has not proved the realist wrong, it
has chosen the stance its own constitution requires and disclosed the choice. The
category-theory commitment (§4) is aspirational, not delivered. The two
novelties (§5) are, by definition, unsupported by prior authority and stand on
internal argument plus falsifiability. SPEC-001 §8.1's stated distribution — 60%
GROUNDED, 30% ADAPTED, 10% NOVEL, 0% CONTESTED — is honest only because the
contested *fields* have been absorbed as disclosed ADAPTED/NOVEL claims rather
than smuggled in as settled. The intellectually honest meaning of "no CONTESTED
claims" is not "nothing here is disputed" but "wherever the field is split, we
have named our side and the price of being wrong."

That price is itemized in `risk-register.md`. The grounding is strongest at the
BFO/DOLCE-convergent core (the partition and the dependence structure),
defensible at the disciplined periphery (OntoClean, Gruber, DL, Sowa), chosen-
and-disclosed at the pluralist hinge, and original-but-falsifiable at the
constraint primitive. That gradient — from settled to chosen to novel — is the
real content of this charter's claim to be grounded.
