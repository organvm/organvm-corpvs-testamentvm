# SPEC-002 Grounding Narrative

```
Date:      2026-06-15
Status:    COMPLETE
Resolves:  GH#134
Phase:     R (Research) — gate G0 for SPEC-002 Phase F
Spec:      SPEC-002 (Primitive Register)
Scope:     Ground the seven primitives in mereology + type theory; OntoClean
           evaluation; cross-ontology alignment; dependent-type sketches;
           defense of Process/Evidence as compositions.
```

---

## 1. The Two Pillars

SPEC-002 rests on two formal pillars. The first is **mereology** — the theory of parts and
wholes — which answers how the seven atomic primitives combine into composites (organs, repos,
modules, governance structures) without those composites being reducible to their parts. The
second is **dependent type theory** — Martin-Löf's *Intuitionistic Type Theory* (1984) — which
gives each primitive a precise type signature and gives composition a precise formal shape
(dependent record types). Mereology answers *what composes*; type theory answers *how it is
written down and checked*. The register is sound only if both pillars hold; neither alone
suffices.

The mereological choice is deliberate and consequential. Classical Extensional Mereology (CEM)
asserts **extensionality**: two wholes with the same parts are identical. ORGANVM cannot accept
this. Two organs may hold the very same repositories yet differ in their governance Constraints,
their aesthetic Values, or their dependency Relations — and that difference is real, not nominal.
So SPEC-002 adopts Simons' **Minimal Mereology** (1987), which retains reflexivity, antisymmetry,
transitivity, and weak supplementation while dropping both extensionality and unrestricted
composition. Under MM a whole is an *integral whole*: its identity is fixed by the
structure-determining relations among its parts, not by the parts alone. This is precisely what
ORGANVM needs, because the structure-determining relations include Relations (PRIM-003) and
Constraints (PRIM-006) — categories that are themselves primitives in the register. The whole is
individuated by primitives that are not among its material parts.

Type theory supplies the writing system. Martin-Löf's universe hierarchy gives Entity its home
(`Entity : Type_0`). Dependent function types (Π) let a State range over *all* of an entity's
dimensions. Dependent pair types (Σ) express loose aggregation. And the propositions-as-types
correspondence (Curry 1934; Howard 1980; Martin-Löf 1984) lets a Constraint be a *type* whose
inhabitants are *proofs* that a State satisfies it — an uninhabited Constraint type is an
unsatisfiable rule. Pierce's *Types and Programming Languages* (2002) supplies the engineering
bridge: the dependent **record types** of SPEC-002 §2.2 are implementable by extending the record
machinery Pierce formalizes with the dependency Martin-Löf provides.

---

## 2. (a) OntoClean Evaluation of the Seven Primitives

Guarino & Welty's OntoClean (2002) supplies four meta-properties — **Identity** (I, does the kind
supply a criterion of individuation?), **Rigidity** (R, is membership essential?), **Unity** (U,
does each instance have a principled whole/part boundary?), and **Dependence** (D, does existence
require another entity?). SPEC-002's seven primitives are a flat register of disjoint categories,
not a subsumption taxonomy, so OntoClean is applied here as a *consistency discipline on profiles*
rather than as a constraint on is-a edges.

| Primitive | Identity | Rigidity | Unity | Dependence | Reading |
|-----------|:--------:|:--------:|:-----:|:----------:|---------|
| PRIM-001 Entity | +I | +R | +U | −D | The sortal substrate: UID gives identity, Entity-hood is essential, each Entity has a boundary, and it needs nothing else. |
| PRIM-002 Value | −I | −R | −U | +D | A datum: no own identity (two "PUBLIC_PROCESS" tokens are indistinguishable), changeable, atomic, needs a bearer. |
| PRIM-003 Relation | −I | +R | +U | +D | Identified by relata+type not UID; necessarily a Relation; a unified whole of relata/direction/type; depends on its relata. |
| PRIM-004 Event | +I | +R | −U | +D | Carries identity (timestamp+causation+affected entity); essentially an Event; temporally bounded (no persistent unity); depends on Entities/States. |
| PRIM-005 State | −I | ~R | +U | +D | A complete snapshot: no own identity; **anti-rigid** (an Entity changes State while persisting); a unified configuration; depends on Entities+Values. |
| PRIM-006 Constraint | −I | +R | +U | +D | A rule: identified by content; necessarily a Constraint; unified (condition+deontic+consequence); depends on what it constrains. |
| PRIM-007 Capability | −I | ~R | −U | +D | A power: identified by type+bearer; **anti-rigid** (gained/lost); atomic; depends on bearer and enabling States. |

**OntoClean consistency checks.** Two profiles carry the anti-rigid marker `~R`: State and
Capability. OntoClean's central constraint is that an anti-rigid property cannot subsume a rigid
one. Because the register is flat (no primitive subsumes another), no such violation can arise *by
construction* — this is one reason the register is deliberately not a taxonomy. The one profile
that warrants scrutiny is **Event (+I, −U)**: it carries identity yet lacks unity. OntoClean
permits this (identity and unity are independent meta-properties), and it is the correct reading —
an Event is individuable by its causal/temporal coordinates yet is not a persisting unified whole.
The remaining latent issue is **Capability's −U with BFO's analysis**: BFO would give a Function
internal unity (it is grounded in configuration), which suggests the unified `~R/−U` profile is an
over-simplification — recorded as the CONTESTED status of PRIM-007. No hard OntoClean violation is
present; the profiles are mutually consistent under a flat register.

---

## 3. (b) Cross-Ontology Alignment Matrix

| Primitive | BFO 2.0 counterpart (Arp, Smith & Spear 2015) | DOLCE counterpart (Masolo et al. 2003) | Score (BFO / DOLCE) |
|-----------|-----------------------------------------------|----------------------------------------|:-------------------:|
| PRIM-001 Entity | Independent Continuant | Endurant | 1 / 1 |
| PRIM-002 Value | Quality (Specifically Dependent Continuant) | Quality (with qualia) | 1 / 1 |
| PRIM-003 Relation | Relational Quality (SDC, multiple bearers) | Abstract | 1 / 1 |
| PRIM-004 Event | Process / Process Boundary (Occurrent) | Perdurant (Achievement / Accomplishment) | 1 / 1 |
| PRIM-005 State | *(no separate category — aggregate of Qualities)* | State (homeomeric Perdurant) | 0 / 0.5 |
| PRIM-006 Constraint | *(no category — BFO describes IS, not OUGHT)* | *(no category — DOLCE is descriptive)* | 0 / 0 |
| PRIM-007 Capability | Disposition / Function (Realizable; split into Disposition/Role/Function) | *(no direct equivalent)* | 0.5 / 0 |

The matrix exposes a clean pattern. The four **descriptive** primitives — Entity, Value, Relation,
Event — align perfectly with both foundational ontologies (the GROUNDED block). The misalignment is
entirely **normative or governance-functional**: State exists in DOLCE but not BFO; Constraint
exists in neither because both are descriptive ontologies that decline to encode normativity; and
Capability is recognized by BFO but at a finer grain (the Disposition/Role/Function trichotomy)
that ORGANVM's single primitive collapses. This is exactly the boundary one would predict for a
*governed* ontology grafted onto descriptive foundations.

---

## 4. (c) Dependent-Type Formalization Sketches

The following sketches use Martin-Löf (1984) notation. They are illustrative, not the final
machine-checked artifact; the FORMALIZABLE status of both primitives reflects that downstream
SPEC-001 dimension declarations are required to close them.

### 4.1 Relation (PRIM-003)

A Relation is a typed, directed dependent triple over two relata. Its constitutive content —
direction and type — is what blocks reduction to monadic Values.

```
RelType : Type_0                          -- enum: DependsOn | Produces | Consumes | HierarchyParentOf | ...

Relation : Entity -> Entity -> RelType -> Type_0
-- inhabitant: a witness that the ordered pair (src, tgt) stands in relation r.

-- A concrete dependency edge as a Σ-bundle that fixes both relata and the type:
edge_engine_schema : Σ (src tgt : Entity) × Σ (r : RelType) × Relation src tgt r
edge_engine_schema = ⟨ engine , schema_defs , DependsOn , depends_proof ⟩

-- Directionality is built in: Relation src tgt r is a DIFFERENT type from Relation tgt src r.
-- No pair of monadic Values (Value src d) , (Value tgt d') can produce this asymmetry.
```

The acyclicity invariant (INV-000-001) is then statable as: there is no finite chain
`Relation e₀ e₁ DependsOn, …, Relation eₙ e₀ DependsOn` — a proposition over the Relation type,
not over the relata's Values.

### 4.2 Constraint (PRIM-006)

A Constraint is a deontic predicate over States. Via propositions-as-types, the predicate *is* a
type family indexed by State, and the deontic mode selects how an inhabitant (or its absence) is
read.

```
Deontic : Type_0
Deontic = MUST | SHOULD | MAY            -- von Wright 1951: O / (soft-O) / P;  ¬MAY = F (prohibition)

Constraint : State -> Deontic -> Prop
-- For a given State s and mode m, (Constraint s m) is a proposition (a type, by PaT).
-- A proof  p : Constraint s MUST  is a term witnessing that s satisfies an obligatory rule.
-- (Constraint s MUST) uninhabited  ==>  the rule is unsatisfiable at s.

-- The governance-rules.json promotion rule, as a MUST-Constraint over a promotion State:
promotion_ok : (s : State repo) -> Constraint s MUST
promotion_ok s =
  ( hasCI s ) × ( platinum s ) × ( implActive s )     -- conjunction over THREE dimensions of s
-- This is a predicate over the COMPLETE configuration s (a Π-typed State, §4.3 of the spec),
-- not three independent predicates over isolated Values. The conjunction is why State must be
-- the argument type: decomposing into per-Value predicates loses the joint structure.
```

The deontic parameter is the formal carrier of normativity: dropping it would reduce Constraint to
a bare `State -> Bool` predicate, which classifies but does not prescribe — the loss the PRIM-006
reduction test identifies. SHOULD encodes soft obligation (defeasible), exceeding the classical
O/P/F triad and flagged for ADICO-structured refinement in SPEC-003/SPEC-005 (Crawford & Ostrom
1995).

---

## 5. (d) Why Process and Evidence Are Compositions, Not Primitives

The Stage-II corpus listed both Process and Evidence as root classes. SPEC-002 demotes both to
compositions. This is the register's most consequential pair of *reductions*, because the claim
"exactly seven primitives" survives only if these reductions are sound. The defense is honest:
each reduction is exhibited as a dependent record, and each is cross-checked against a foundational
ontology and against Gruber's (1993) minimal-commitment principle.

**Evidence = Entity + Value + Event.** An item of evidence — a test result, an audit trace, a
metric reading — is a thing with identity (PRIM-001) that carries a measured datum (PRIM-002,
e.g. `pass/fail`, `coverage %`) recorded by an act of observation at a time (PRIM-004). That is
the whole of it. There is no residue requiring a sui generis category. The honest worry is that
Evidence *feels* primitive because it is operationally central — governance decisions ride on it.
But operational centrality is not ontological irreducibility (Gruber's principle: commit only to
what irreducibility forces). Evidence's three-field record loses nothing of evidential force: the
"act of measurement at a time" is exactly an Event, and the recorded reading is exactly a Value on
an identity-bearing Entity. Reduction is clean; no constitutive property is lost.

**Process = Entity + ordered Events + ordering Relations + governing Constraints + status State.**
This is the harder and more contestable reduction — the one the risk register marks as the
CONTESTED-adjacent claim (RR-002-10). A promotion process *has* identity (PRIM-001), *is* an
ordered sequence of Events (PRIM-004: governance audit → CI verification → state transition),
whose order is fixed by ordering Relations (PRIM-003), whose valid step-sequences are bounded by
Constraints (PRIM-006), and whose lifecycle is tracked by a status State (PRIM-005). The honest
defense must confront the strongest objection: process philosophers (and BFO, which makes Process
a first-class Occurrent) would say a process is not *assembled* from events but is an ontologically
prior unfolding. SPEC-002's reply is two-pronged. First, the **ordering and governance** that make
a sequence-of-events into a *process* come from Relation and Constraint, which are already in the
register; the process adds no new constitutive ingredient beyond *being typed as process-shaped* —
and "process-shaped" is a composition pattern, not a primitive. Second, BFO's own move is
replicated, not contradicted: BFO types certain occurrents as Processes; SPEC-002 types certain
*composite objects* as process-shaped. The disagreement is about whether "Process" earns a slot in
the *primitive* register, not about whether processes exist. They exist — as compositions.

The principled guard against over-reduction is the **Reduction Test Protocol** (SPEC-002 §6.2): a
candidate is admitted as an 8th primitive only if (1) reduction fails or loses constitutive
properties, *and* (2) at least one of BFO/DOLCE/Armstrong/Johansson recognizes it as irreducible,
*and* (3) its absence creates an expressibility gap against a SPEC-000 axiom or SPEC-001 class. Both
Process and Evidence fail condition (1) — their reductions succeed without loss — so neither is
admitted. Were a future analysis to show that, say, the *temporal continuity* of a long-running
process cannot be captured by an ordered Event list plus ordering Relations, condition (1) would
flip and the protocol would re-open the question. Until then, the register holds at seven.

---

## 6. Sufficiency

SPEC-002 §4 demonstrates that all SPEC-000 axioms (AX-000-001 through AX-000-009) and all SPEC-001
entity classes are expressible in the seven primitives without recourse to Process, Evidence,
Agent, or any excluded candidate. The two pillars — Minimal Mereology for composition, dependent
type theory for formal expression — are jointly sufficient to constitute every system object as a
dependent record of the seven atoms. The register is complete for ORGANVM's governance
architecture, and its three high-risk commitments (State ADAPTED, Constraint NOVEL, Capability
CONTESTED) are disclosed, grounded in adjacent formal traditions, and governed by an amendment
protocol.

---

*Word count (body, §1–§6, excluding code blocks and tables): ~1,950 words.*
*Sources: see `literature-matrix.md` and `source-archive.md`; BibTeX in `specs/bibliography.bib`.*
