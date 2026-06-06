# SPEC-003: Invariant Register

```
Document ID:      SPEC-003
Title:            Invariant Register
Version:          1.1
Status:           RATIFIED (G3 review incorporated)
Layer:            L2 — Formal Ontology
Authoritative:    Entire System
Parent Specs:     SPEC-000 (System Manifesto), SPEC-001 (Ontology Charter), SPEC-002 (Primitive Register)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/SPEC-003/grounding.md
Risk Register:    post-flood/specs/SPEC-003/risk-register.md
Inventory:        post-flood/specs/SPEC-003/inventory.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. The Invariant Register

A constitutional system that cannot verify its own laws is not governed — it is merely documented. SPEC-000 *declares* five invariants as prose commitments with constitutional authority for intent. SPEC-001 and SPEC-002 *anticipate* six additional invariants through the entity classification and primitive composition frameworks. SPEC-003 *formalizes* all eleven as machine-checkable predicates that fire on every state mutation.

Each invariant is formalized through three convergent traditions:

- **Hoare triple** (Hoare 1969): `{Inv} op(args) {Inv}` — the invariant serves as both precondition and postcondition for every governance operation, a loop invariant preserved by every iteration of the system's operational cycle
- **TLA+ safety property** (Lamport 1999): `[](Inv)` — the invariant holds in every reachable state across all possible execution histories
- **Deontic classification** (von Wright 1951): O (obligation), P (permission), F (prohibition) — the normative force governing enforcement semantics

Hoare provides per-operation verification. Lamport provides system-wide temporal guarantee. Von Wright provides normative force. Together they answer three questions no single tradition addresses alone: *Is this invariant preserved by each operation? Is it preserved across all possible execution histories? What happens when it is violated?*

Each invariant record carries:

| Field | Description |
|-------|-------------|
| **ID** | `INV-SSS-NNN` where SSS = source SPEC, NNN = sequence |
| **Source** | The SPEC-000 axiom or SPEC-001/002 commitment that mandates this invariant |
| **Prose** | Human-readable statement of the truth that must hold |
| **Hoare Triple** | `{P} S {Q}` for every governance operation S |
| **TLA+ Expression** | Temporal logic formula with safety property `[](Inv)` |
| **Deontic Classification** | O (obligation) / P (permission) / F (prohibition), with authority |
| **Formalization Status** | FORMAL / FORMALIZABLE / JUDGMENT |
| **Implementation Status** | ALIGNED / DRIFT / MISSING |

---

### INV-000-001: Dependency Acyclicity

**Source:** SPEC-000 AX-000-004 (Constitutional Governance), AX-000-008 (Multiplex Flow Governance), INV-000-001

**Prose.** The dependency graph G^dep must be a directed acyclic graph at all times. No component may depend — directly or transitively — on itself.

**Hoare Triple.**

```
{G^dep is DAG}
  add_dependency(source, target) | remove_dependency(source, target) | promote(repo, state)
{G^dep is DAG}
```

For every operation that mutates the dependency graph, the DAG property is both precondition and postcondition. The consequence rule (Hoare 1969) permits conservative approximation: the validator may reject operations that *might* create cycles, not merely those that *do*, without sacrificing soundness.

**TLA+ Expression.**

```tla
DAGInvariant ==
  ~ \E path \in Paths(G_dep) : path[1] = path[Len(path)]

THEOREM Spec => [](DAGInvariant)
```

**Deontic Classification.** **Prohibition (F):** MUST NOT create cycles. Authority: SPEC-000 AX-000-004, AX-000-008. Content: the creation of any dependency edge that closes a cycle. Condition: all operations mutating G^dep. Consequence: operation rejected; state unchanged.

**Formalization Status: FORMAL.** Cycle detection is O(V+E) via depth-first search. The algorithm is well-understood, deterministic, and complete — no judgment is required.

**Implementation Status: ALIGNED.** `validate_dag_invariant()` in `governance/dependency_graph.py` performs DFS cycle detection. Runs on registry load and on every dependency mutation. Test coverage in `tests/test_dependency_graph.py`.

---

### INV-000-002: Governance Reachability

**Source:** SPEC-000 AX-000-002 (Organizational Closure), AX-000-004 (Constitutional Governance), INV-000-002

**Prose.** For every active component, there must exist a path from a constitutional root to that component in the governance graph G^gov. Constitutional roots are the set of entities with registry key META-ORGANVM. An active component with no governance path is ungoverned — it exists in the workspace but not in the system.

**Hoare Triple.**

```
{forall e in ActiveEntities : reachable(META, e, G^gov)}
  register(entity) | archive(entity) | promote(repo, state) | add_organ(organ)
{forall e in ActiveEntities : reachable(META, e, G^gov)}
```

Registration must create a governance path; archival removes the entity from the active set; promotion must preserve reachability; organ creation must establish a governance path from META.

**TLA+ Expression.**

```tla
ReachabilityInvariant ==
  \A e \in ActiveEntities :
    \E path \in Paths(G_gov) :
      path[1] = META /\ path[Len(path)] = e

THEOREM Spec => [](ReachabilityInvariant)
```

**Deontic Classification.** **Obligation (O):** every active entity MUST be reachable from the constitutional root. Authority: SPEC-000 AX-000-002, AX-000-004. Content: the governance path from META to every active component. Condition: all operations that create, modify, or remove entities. Consequence: entity flagged as ungoverned in audit.

**Formalization Status: FORMAL.** BFS/DFS from the constitutional root is O(V+E). The algorithm determines reachability with certainty — no judgment required.

**Implementation Status: MISSING.** No code checks governance reachability. The governance graph G^gov is not tracked as an independent data structure. Remediation: implement BFS from META roots across governance relation edges; add to `organvm governance audit`.

---

### INV-000-003: Identity Persistence

**Source:** SPEC-000 AX-000-003 (Individual Primacy), AX-000-007 (Alchemical Inheritance), INV-000-003; SVSE framework (post-flood corpus)

**Prose.** No entity UID may be destroyed. The UID set is monotonically non-decreasing: new UIDs may be created (by entity creation, merge, split); existing UIDs may never be removed. An entity may be archived, dissolved, merged, or split, but its identity and lineage must be preserved. This encodes the SVSE framework's core principle: "Identity is stable. Expression is mutable. Relationship is versioned."

**Hoare Triple.**

```
{forall e : uid(e) in UIDs}
  any_operation(args)
{forall e : uid(e) in UIDs  /\  UIDs_pre <= UIDs_post}
```

The postcondition is stronger than mere preservation: it asserts monotonicity. A renamed entity retains its UID. A reclassified entity retains its UID. A merged entity produces a new UID while preserving both source UIDs in the lineage chain.

**TLA+ Expression.**

```tla
IdentityPersistence ==
  /\ \A uid \in UIDs : uid \in UIDs'
  /\ Cardinality(UIDs') >= Cardinality(UIDs)

THEOREM Spec => [](IdentityPersistence)
```

The first conjunct asserts per-UID survival; the second asserts set-level monotonicity.

**Deontic Classification.** **Prohibition (F):** MUST NOT destroy UIDs. Authority: SPEC-000 AX-000-003, AX-000-007, SVSE framework. Content: the deletion of any UID from the system's identity store. Condition: all operations. Consequence: operation rejected; lineage audit triggered.

**Formalization Status: FORMAL.** UID monotonicity is checkable by comparing UID sets before and after any operation: `UIDs_pre` is a subset of `UIDs_post`. The check is O(n) with set operations.

**Implementation Status: DRIFT.** The ontologia store (`store.py`) is structurally append-only — entities cannot be deleted through the store API, which enforces persistence at the store level. However, `repo-registry.json` is a plain JSON file editable by hand, and manual editing can remove entries without triggering any persistence check. Full enforcement requires either (a) routing all registry mutations through the engine's API, or (b) adding a git pre-commit hook that rejects UID deletions by comparing the proposed registry against its predecessor.

---

### INV-000-004: Constitutional Supremacy

**Source:** SPEC-000 AX-000-004 (Constitutional Governance), INV-000-004

**Prose.** No lower-level rule (organ dictum, repo rule, agent action) may override a higher-level constitutional constraint (axiom, invariant, spec). The authority hierarchy is: axioms > organ dictums > repo rules > agent actions.

**Hoare Triple.**

```
{forall c_low, c_high :
    level(c_low) < level(c_high) => ~ contradicts(c_low, c_high)}
  add_constraint(c) | modify_constraint(c) | add_organ_dictum(d) | modify_repo_rule(r)
{forall c_low, c_high :
    level(c_low) < level(c_high) => ~ contradicts(c_low, c_high)}
```

**TLA+ Expression.**

```tla
ConstitutionalSupremacy ==
  \A c1, c2 \in Constraints :
    level(c1) < level(c2) /\ Contradicts(c1, c2) => FALSE

THEOREM Spec => [](ConstitutionalSupremacy)
```

**Deontic Classification.** **Obligation (O):** the constraint hierarchy MUST be consistent. This is a *second-order* norm — a norm governing norms (von Wright 1963). Authority: SPEC-000 (self-referential: the constitutional supremacy axiom grounds its own authority). Content: consistency of the constraint hierarchy across authority levels. Condition: all operations that create or modify constraints at any level. Consequence: constraint rejected; escalation to human principal.

**Formalization Status: JUDGMENT (partitioned).** The fundamental difficulty is formalizing `contradicts`. Two constraints contradict when one obligates what the other prohibits in the same context: `O(p)` and `F(p)`. For *first-order* constraints — predicates over observable state (e.g., "ORGAN-I repos MUST have no downstream dependencies" vs. a hypothetical repo rule "this repo MAY depend on ORGAN-III") — contradiction detection is decidable, reducing to satisfiability checking over finite domains. For *higher-order* constraints — norms governing the constraint system itself (e.g., "the evolution law MUST NOT be self-defeating") — contradiction detection may be undecidable, triggering Godelian limits on self-referential evaluation. SPEC-003 partitions INV-000-004 into two enforcement tiers:

| Tier | Scope | Checkability |
|------|-------|-------------|
| **Automated** | First-order constraints: predicates over observable system state | Machine-checkable via satisfiability checking |
| **Judgment** | Higher-order constraints: norms about the constraint system itself | Human-reviewed at constitutional revision |

The boundary follows the first-order/higher-order distinction established in computability theory.

**Implementation Status: MISSING.** No code checks constitutional supremacy. Remediation: formalize the constraint hierarchy as a data structure mapping each constraint to its authority level; implement first-order contradiction detection as satisfiability checking over the constraint set; flag higher-order constraints for human review.

---

### INV-000-005: Observability

**Source:** SPEC-000 AX-000-002 (Organizational Closure), INV-000-005

**Prose.** The system must be capable of accurately reporting its own state — every active component's status, every active relation's type, every active metric's value — through its own diagnostic instruments. Reports must reflect current system state; a diagnostic instrument that returns stale, hardcoded, or fabricated data violates this invariant.

Observability decomposes into three sub-properties:

| Sub-property | Definition | Checkability |
|-------------|-----------|--------------|
| **Presence** | Every active entity has a non-null status, a validation timestamp, and computed metrics | FORMAL |
| **Freshness** | Validation timestamps are within a staleness threshold (configurable, default 30 days) | FORMAL |
| **Accuracy** | Reported state matches actual state | Requires external comparison — JUDGMENT |

**Hoare Triple.**

```
{forall e in ActiveEntities :
    status[e] != NULL  /\
    last_validated[e] > NOW - STALENESS_THRESHOLD  /\
    metrics[e] != EMPTY}
  any_operation(args)
{same}
```

**TLA+ Expression.**

```tla
Observability ==
  \A e \in ActiveEntities :
    /\ status[e] # NULL
    /\ last_validated[e] > NOW - STALENESS_THRESHOLD
    /\ metrics[e] # EMPTY

THEOREM Spec => [](Observability)
```

**Deontic Classification.** **Obligation (O):** every active entity MUST be observable. Authority: SPEC-000 AX-000-002. Content: the presence, freshness, and accuracy of diagnostic data for every active component. Condition: all operations. Consequence: entity flagged as unobservable in organism gate checks.

**Formalization Status: FORMALIZABLE.** Presence and freshness are fully checkable. Accuracy requires external comparison (does the reported promotion_status match the actual CI state?) — this sub-property is JUDGMENT.

**Implementation Status: DRIFT.** `metrics/organism.py` gate evaluation checks for field presence but does not verify freshness against a staleness threshold or accuracy against external state. Remediation: extend gate checks to compare `last_validated` against a configurable threshold; add external accuracy probes for CI status and test results.

---

### INV-001-001: Ontological Categorization

**Source:** SPEC-001 (Ontology Charter) — ONT-001 Entity, Continuant/Occurrent/Abstract partition

**Prose.** Every entity in the system has exactly one ontological category. The three root categories — Continuant, Occurrent, Abstract — are mutually exclusive and jointly exhaustive over the entity space. No entity may be simultaneously classified as Continuant and Occurrent, or exist without classification.

**Hoare Triple.**

```
{forall e in Entities : |categories(e)| = 1}
  create_entity(e, type, category) | reclassify_entity(e, new_category)
{forall e in Entities : |categories(e)| = 1}
```

Entity creation must assign exactly one category. Reclassification replaces the old category with the new one (never accumulates).

**TLA+ Expression.**

```tla
OntologicalCategorization ==
  \A e \in Entities :
    /\ Cardinality({c \in Categories : classified(e, c)}) = 1
    /\ \A c \in Categories : classified(e, c) =>
         c \in {CONTINUANT, OCCURRENT, ABSTRACT}

THEOREM Spec => [](OntologicalCategorization)
```

**Deontic Classification.** **Obligation (O):** every entity MUST have exactly one category. Authority: SPEC-001 ONT-001. Condition: entity creation and reclassification operations.

**Formalization Status: FORMALIZABLE.** Fully machine-checkable once the EntityType enum is stratified into the Continuant/Occurrent/Abstract partition. Currently `entity_type` in ontologia carries flat types (ORGAN, REPO, MODULE) without stratification.

**Implementation Status: MISSING.** The stratified taxonomy defined in SPEC-001 is not yet implemented. EntityType in `ontologia/entity/identity.py` uses a flat enum. Prerequisite: implement SPEC-001's entity classification hierarchy.

---

### INV-001-002: Subsumption Discipline

**Source:** SPEC-001 (Ontology Charter) — OntoClean metaproperty constraints (Guarino & Welty 2002)

**Prose.** Anti-rigid types cannot subsume rigid types in any taxonomy hierarchy. A type is rigid (+R) if every instance is necessarily of that type; anti-rigid (~R) if instances can cease to be of that type. The OntoClean constraint prevents incoherent taxonomies: if a rigid type (Entity: necessarily an Entity) were subsumed by an anti-rigid type (State: contingently a State), the taxonomy would assert that an Entity is necessarily an Entity *only contingently* — a contradiction.

**Hoare Triple.**

```
{forall t1, t2 in Types :
    anti_rigid(t1) /\ subsumes(t1, t2) => ~ rigid(t2)}
  modify_taxonomy(t1, t2, relation)
{same}
```

**TLA+ Expression.**

```tla
SubsumptionDiscipline ==
  \A t1, t2 \in Types :
    anti_rigid(t1) /\ subsumes(t1, t2) => ~ rigid(t2)

THEOREM Spec => [](SubsumptionDiscipline)
```

**Deontic Classification.** **Prohibition (F):** MUST NOT subsume rigid types with anti-rigid types. Authority: SPEC-001, OntoClean (Guarino & Welty 2002). Condition: any operation modifying the taxonomy hierarchy.

**Formalization Status: FORMALIZABLE.** Fully machine-checkable once metaproperty annotations (+R/~R/-R) are attached to each entity type. Requires the OntoClean profiles declared in SPEC-002 to be encoded as data.

**Implementation Status: MISSING.** No taxonomy hierarchy implementation exists beyond the flat EntityType enum. Prerequisite: implement SPEC-001's entity classification with metaproperty annotations.

---

### INV-001-003: Identity Criteria

**Source:** SPEC-001 (Ontology Charter) — ONT-001 Entity identity, OntoClean +I requirement

**Prose.** Every entity carries identity criteria appropriate to its ontological category. Continuants are individuated by ULID-based UIDs (persistent through state changes). Occurrents are individuated by timestamp, causation, and affected entity (each Event is uniquely identified by when it occurred, what caused it, and what it affected). Abstracts are individuated by structural content (two Schemas with identical content are the same Schema).

**Hoare Triple.**

```
{forall e in Entities :
    identity_criterion(e) = category_criterion(category(e))}
  create_entity(e, type, category)
{same}
```

**TLA+ Expression.**

```tla
IdentityCriteria ==
  \A e \in Entities :
    identity_criterion(e) = CategoryCriterion(category(e))

THEOREM Spec => [](IdentityCriteria)
```

**Deontic Classification.** **Obligation (O):** every entity MUST carry category-appropriate identity criteria. Authority: SPEC-001 ONT-001, OntoClean +I. Condition: entity creation.

**Formalization Status: FORMALIZABLE.** Machine-checkable once a category-to-criterion mapping is encoded. Requires SPEC-001's entity classification to define which criterion applies to which category.

**Implementation Status: MISSING.** ULID-based identity exists for Continuants via ontologia. Occurrent and Abstract identity criteria are not implemented. Prerequisite: implement SPEC-001's full identity criterion framework.

---

### INV-002-001: Primitive Composition

**Source:** SPEC-002 (Primitive Register) — Section 4 Sufficiency Verdict

**Prose.** Every domain object in the system decomposes into the seven primitives defined in SPEC-002 (Entity, Value, Relation, Event, State, Constraint, Capability). No domain object requires an eighth primitive; no domain object is itself a primitive unless it appears in the register.

**Hoare Triple.**

```
{forall obj in DomainObjects :
    decomposable(obj, {PRIM-001..PRIM-007})}
  introduce_object(obj, composition)
{same}
```

**TLA+ Expression.**

```tla
PrimitiveComposition ==
  \A obj \in DomainObjects :
    \A component \in Parts(obj) :
      type(component) \in {Entity, Value, Relation, Event, State, Constraint, Capability}

THEOREM Spec => [](PrimitiveComposition)
```

**Deontic Classification.** **Obligation (O):** every domain object MUST decompose into the seven primitives. Authority: SPEC-002 Section 4. Condition: introduction of any new domain object type.

**Formalization Status: FORMALIZABLE.** This is a structural invariant — verified by design at specification time, not at runtime. Each new domain object type (Agent, Artifact, Signal, GovernanceObject, Evidence, Process) is defined as a dependent record type over primitives in SPEC-002 Section 3. Validation is code review against the composition framework, not automated predicate checking.

**Implementation Status: ALIGNED (structural).** SPEC-002 demonstrates composition for all six current domain object types. Future domain objects must include a composition record as a condition of introduction.

---

### INV-002-002: Non-Extensional Mereology

**Source:** SPEC-002 (Primitive Register) — Section 2.1 Non-Extensional Mereology

**Prose.** Composition is non-extensional: two composites with identical parts are NOT necessarily identical. An organ's identity is not exhausted by its repositories — it includes its governance rules (Constraints), aesthetic identity (Values), and dependency structure (Relations). The system adopts Simons' Minimal Mereology (Simons 1987), dropping classical extensional mereology's extensionality and unrestricted composition axioms while retaining reflexivity, antisymmetry, transitivity, and weak supplementation.

**Hoare Triple.** This invariant is not a per-operation predicate but a design constraint on the identity semantics:

```
Design Constraint:
  parts(a) = parts(b)  does NOT imply  a = b
```

Equivalently: identity is determined by ULID, not by part composition. Two organs with identical repository lists but different UIDs are different organs.

**TLA+ Expression.**

```tla
NonExtensional ==
  \E a, b \in Composites :
    Parts(a) = Parts(b) /\ a # b

\* This is a design property, not a per-state invariant.
\* Verified by: ULID-based identity (INV-000-003) ensures composites
\* with identical parts can differ.
```

**Deontic Classification.** **Prohibition (F):** MUST NOT use extensional identity for composites (i.e., MUST NOT identify composites solely by their parts). Authority: SPEC-002 Section 2.1, Simons 1987. Condition: all identity comparisons.

**Formalization Status: FORMAL.** ULID-based identity (ontologia) structurally satisfies non-extensionality: every entity gets a unique ULID at creation regardless of its parts. Two entities with identical part sets have different UIDs by construction.

**Implementation Status: ALIGNED (structural).** Ontologia's ULID-based identity system inherently satisfies non-extensionality. No entity identity comparison in the codebase uses part-set equality. Verified by code review.

---

### INV-002-003: Constraint Domain

**Source:** SPEC-002 (Primitive Register) — PRIM-005 State, PRIM-006 Constraint

**Prose.** Constraints operate on States (complete configurations), not on individual Values. The governance rule "promotion requires CI workflow AND platinum status AND implementation_status=ACTIVE" is a predicate over the *joint* configuration of three dimensions — a predicate over State, not three independent predicates over individual Values. Without this invariant, conjunctive governance rules lose their structural integrity: they could be decomposed into independent per-Value checks that miss cross-dimension interactions.

**Hoare Triple.**

```
{forall c in Constraints : domain(c) is State type}
  add_constraint(c, domain, predicate) | modify_constraint(c, new_domain)
{forall c in Constraints : domain(c) is State type}
```

**TLA+ Expression.**

```tla
ConstraintDomain ==
  \A c \in Constraints :
    domain(c) \in States

THEOREM Spec => [](ConstraintDomain)
```

**Deontic Classification.** **Obligation (O):** constraints MUST target States, not individual Values. Authority: SPEC-002 PRIM-005, PRIM-006. Condition: constraint creation and modification.

**Formalization Status: FORMALIZABLE.** Machine-checkable once State is reified as a first-class type (per SPEC-002 PRIM-005). Currently governance rules in `governance-rules.json` implicitly operate over State (they check conjunctions of field values) but the State abstraction is not explicit in the code.

**Implementation Status: DRIFT.** Governance rules in `governance/rules.py` procedurally check conjunctions of repo fields — structurally operating on States — but do not declare their domain as a State type. The implicit correctness is not enforced by the type system. Remediation: reify State as a first-class construct; require Constraint declarations to explicitly name their State domain.

---

### Summary: Invariant Register

| ID | Name | Deontic | Formalization | Implementation | Source |
|----|------|---------|---------------|----------------|--------|
| INV-000-001 | Dependency Acyclicity | F | FORMAL | ALIGNED | SPEC-000 AX-000-004, AX-000-008 |
| INV-000-002 | Governance Reachability | O | FORMAL | MISSING | SPEC-000 AX-000-002, AX-000-004 |
| INV-000-003 | Identity Persistence | F | FORMAL | DRIFT | SPEC-000 AX-000-003, AX-000-007 |
| INV-000-004 | Constitutional Supremacy | O | JUDGMENT | MISSING | SPEC-000 AX-000-004 |
| INV-000-005 | Observability | O | FORMALIZABLE | DRIFT | SPEC-000 AX-000-002 |
| INV-001-001 | Ontological Categorization | O | FORMALIZABLE | MISSING | SPEC-001 ONT-001 |
| INV-001-002 | Subsumption Discipline | F | FORMALIZABLE | MISSING | SPEC-001 OntoClean |
| INV-001-003 | Identity Criteria | O | FORMALIZABLE | MISSING | SPEC-001 ONT-001 |
| INV-002-001 | Primitive Composition | O | FORMALIZABLE | ALIGNED | SPEC-002 Section 4 |
| INV-002-002 | Non-Extensional Mereology | F | FORMAL | ALIGNED | SPEC-002 Section 2.1 |
| INV-002-003 | Constraint Domain | O | FORMALIZABLE | DRIFT | SPEC-002 PRIM-005/006 |

| INV-000-006 | Topological Data-Drivenness | O | FORMALIZABLE | MISSING | SPEC-000 AX-000-006 |
| INV-000-009 | Signal Observability | O | FORMALIZABLE | MISSING | SPEC-000 AX-000-009 |

**INV-000-006: Topological Data-Drivenness.** The organ topology must be loaded from a data configuration at runtime, not hardcoded in source code. Any code path that references a fixed set of organ identifiers violates this invariant. *Formalization: FORMALIZABLE. Implementation: MISSING — topology is hardcoded in organ_config.py, dependency_graph.py, and organ-definitions.schema.json (AX-000-006 CONFLICT per SPEC-000 inventory). Target: Layer 3B.*

**INV-000-009: Signal Observability.** Every active signal connection between organs must be recorded in the patch matrix and observable through the event spine. Unrecorded signal flows violate this invariant. *Formalization: FORMALIZABLE. Implementation: MISSING — no patch matrix, no signal I/O declarations, no event spine (AX-000-009 MISSING per SPEC-000 inventory). Target: Layer 3B + Layer 4A.*

**Totals:** 3 ALIGNED, 3 DRIFT, 7 MISSING. 4 FORMAL, 8 FORMALIZABLE, 1 JUDGMENT. 7 Obligations, 4 Prohibitions, 0 Permissions.

---

## 2. The Contract Model

### 2.1 seed.yaml as Design by Contract

Each `seed.yaml` is a contract in Meyer's (1997) formal sense. The isomorphism is structural, not metaphorical:

| Meyer's DbC | seed.yaml | Example |
|-------------|-----------|---------|
| **Preconditions** (caller obligations) | `dependencies`, `consumes` | "engine requires schema-definitions" |
| **Postconditions** (supplier guarantees) | `produces` | "engine emits registry_updated events" |
| **Class invariants** (lifecycle properties) | `organ`, `tier`, `promotion_status` | "engine belongs to META, is flagship, at PUBLIC_PROCESS" |

Contracts compose through the dependency graph. When repo B declares a dependency on repo A, B's preconditions incorporate A's postconditions — B's build assumes A's `produces` edges are satisfied. The DAG acyclicity invariant (INV-000-001) is precisely the condition preventing circular contract dependency, the contract equivalent of mutual recursion without a base case.

In a DAG, preconditions can always be satisfied in topological order: build the leaves first, then their dependents, then their dependents' dependents, with each layer's postconditions satisfying the next layer's preconditions.

The contract model explains why `seed.yaml` is mandatory (SPEC-000 AX-000-004). A repo without a `seed.yaml` is a class without a contract: it makes no commitments about requirements, outputs, or constraints. The system cannot reason about it, schedule it, or integrate it into the dependency graph. `seed.yaml` is not bureaucratic overhead but the minimal condition for governance.

### 2.2 Promotion as Liskov-Constrained Refinement

The Liskov Substitution Principle (Liskov & Wing 1994) creates a monotonic refinement ordering on promotion states: each level imposes strictly more constraints than the level below, and no promotion transition may remove a constraint the current level imposes.

| State | Constraints |
|-------|------------|
| LOCAL | Organ membership, `seed.yaml` presence |
| CANDIDATE | +description, +implementation_status |
| PUBLIC_PROCESS | +CI workflow, +platinum status, +active implementation |
| GRADUATED | +sustained soak-test, +documentation completeness, +cross-organ validation |
| ARCHIVED | All prior constraints frozen; entity moved to historical record |

Promotion is subtyping: GRADUATED strengthens postconditions (more guarantees about stability, documentation, cross-organ compliance) while inheriting all lower-state prerequisites. If PUBLIC_PROCESS requires CI, then GRADUATED must also require CI. This monotonicity is encoded in `governance/state_machine.py` as a structural property of the transition table — higher states inherit all lower-state prerequisites by construction, not by convention.

Demotion is the inverse: relaxing postconditions by moving to a less constrained state. The Liskov constraint ensures demotion is always safe — a less constrained state accepts all states that satisfy a more constrained one.

---

## 3. Verification Methodology

### 3.1 TLA+ Specification Pattern

The full governance system is expressible as a TLA+ specification of the form:

```tla
Spec == Init /\ [][Next]_vars
```

Where:

- **Init:** All repos at LOCAL, empty dependency graph, empty UID set, governance graph contains only META root
- **Next:** Disjunction of atomic governance operations:
  - `Promote(repo, target_state)`
  - `Demote(repo, target_state)`
  - `Archive(repo)`
  - `AddDependency(source, target)`
  - `RemoveDependency(source, target)`
  - `CreateEntity(entity, type, category)`
  - `AddConstraint(constraint, level, domain)`
  - `ModifyTaxonomy(type1, type2, relation)`
- **Inv:** Conjunction of all eleven invariants
- **Safety Property:** `[](Inv)` — the conjunction holds in every reachable state

The inductive invariant structure (Lamport 1999) maps directly to the validator architecture:

| TLA+ Concept | ORGANVM Implementation |
|-------------|----------------------|
| Init => Inv | Bootstrap validation: registry creation validates all invariants |
| Inv /\ Next => Inv' | Per-operation validation: each governance operation validates invariants post-mutation |
| Spec => [](Inv) | System-wide guarantee: the conjunction of bootstrap + per-operation validation |

### 3.2 Model Checking

The raw state space of ~112 repos in 5 promotion states yields 5^112 possible configurations — intractable for exhaustive model checking. Three reduction strategies make targeted verification feasible:

**Symmetry reduction.** Repos within the same organ and tier are interchangeable for invariant verification purposes. The system has 8 organs with a maximum of ~28 repos each; symmetry reduces the effective state space to 5^8 promotion configurations times structural variations.

**Abstraction.** For DAG acyclicity (INV-000-001), tracking only edge topology at the organ level yields 2^(n^2) = 2^64 states for n=8 organs — manageable with symbolic model checking methods (Clarke, Grumberg & Peled 1999).

**Bounded model checking.** Exploring traces up to length k=20 covers typical governance workflows (promotion pipelines, dependency additions, entity creation sequences). Bounded model checking finds counterexamples without requiring full state exploration.

**Practical recommendation:** Implement the TLA+ specification for the promotion state machine with abstracted dependency topology. Verify under symmetry reduction using TLC (the TLA+ model checker). Encode TLC counterexamples as pytest test cases, creating a bidirectional link between specification and implementation.

### 3.3 Conformance Checking

**Structural conformance.** Each engine validator function should correspond to exactly one TLA+ invariant conjunct. The mapping is:

| Invariant | Validator Function | TLA+ Conjunct |
|-----------|-------------------|---------------|
| INV-000-001 | `governance/dependency_graph.py::validate_dag_invariant()` | DAGInvariant |
| INV-000-002 | (not implemented) | ReachabilityInvariant |
| INV-000-003 | `ontologia/store.py` (structural append-only) | IdentityPersistence |
| INV-000-004 | (not implemented) | ConstitutionalSupremacy |
| INV-000-005 | `metrics/organism.py` (gate evaluation, partial) | Observability |

Structural conformance is verifiable by code review: for each TLA+ conjunct, there is exactly one validator function, and vice versa.

**Behavioral conformance.** TLC counterexamples (concrete traces from Init to a violating state) should be encoded as pytest test cases. Each test case exercises the operation sequence from the counterexample and asserts the invariant holds. This creates a bidirectional link: the TLA+ specification generates test cases; the test cases verify the implementation against the specification.

**Weakest precondition derivation.** Dijkstra's (1975) wp calculus suggests an alternative validator architecture: instead of hand-writing validators, *derive* them from invariants. `wp(promote(repo, GRADUATED), conjunction-of-all-INVs)` yields the exact promotion prerequisites. The current hand-written validators are correct but not formally derived; the TLA+ specification provides the reference for future derivation.

---

## 4. Constitutive Force

ORGANVM's invariants are not regulative rules — optional best practices that the system could violate while remaining ORGANVM. They are *constitutive rules* in Searle's (1995) sense: rules that create the very categories they regulate.

Searle distinguishes:

- **Regulative rules** govern pre-existing activities. "Drive on the right side of the road" regulates driving, which exists independently of the rule.
- **Constitutive rules** create new categories of reality. "X counts as Y in context C" — a checkmate is constituted by the rules of chess; without the rules, there is no checkmate.

ORGANVM's invariants are constitutive: "a directory with a `seed.yaml` (X) counts as an organ member (Y) in the context of the constitutional corpus (C)." Without INV-000-001 (dependency acyclicity), there is no directed flow — only arbitrary coupling. Without INV-000-002 (governance reachability), there is no governed system — only a collection of repositories. Without INV-000-003 (identity persistence), there is no continuity — only a sequence of disconnected snapshots.

The constitutive/regulative distinction has direct engineering consequences:

| Property | Regulative Rule | Constitutive Rule |
|----------|----------------|-------------------|
| Relaxation | Can be relaxed under pressure ("skip the lint check for this hotfix") | Cannot be relaxed without destroying what the system is |
| Violation | Produces a poorly-governed system | Produces a non-system |
| Enforcement | Convenience | Necessity |
| Verification investment | Cost-benefit analysis | Required for existence |

This constitutive force is what justifies the investment in formal verification, TLA+ specification, and model checking. One does not model-check optional guidelines. One model-checks the conditions for existence.

### Contestation Disclosure

Searle's constitutive rules require *collective intentionality* — the shared acceptance by a community that "X counts as Y in C." ORGANVM has a single operator, making this a weaker form of constitution than Searle describes. The constitution is valid because the operator constitutes it through sustained practice, not because a collective recognizes it. This is structurally analogous to Searle's account but lacks the social dimension that Searle considers essential. The adaptation is explicitly acknowledged.

---

## 5. Contestation Disclosures

### 5.1 Sufficiency of the Invariant Set

**Classification: NOVEL.** The claim that eleven invariants suffice is the register's most significant theoretical risk. Sufficiency means: no valid system state can violate the system's identity without violating at least one declared invariant.

The mitigation is operational, not formal. SPEC-000's axioms define the system's identity. Each axiom maps to at least one invariant. If the axioms are the complete identity definition, the invariant set is sufficient by construction. The risk is that the axioms themselves are incomplete — that some identity-relevant property is not captured by any axiom and therefore not covered by any invariant.

This risk cannot be eliminated by formal methods but is managed by the monotonic extension principle: as new identity-relevant properties are discovered, invariants are added, never removed — mirroring INV-000-003 (identity persistence) applied to the register itself. The invariant register is subject to its own identity persistence invariant: its history is preserved, its evolution is traceable, and its current state is the accumulation of every invariant ever declared.

### 5.2 Meta-Reasoning for INV-000-004

**Classification: ADAPTED.** Constitutional supremacy requires detecting contradictions between authority levels. The meta-reasoning challenge is well-understood in the formal methods literature but has no off-the-shelf solution for ORGANVM's specific constraint language.

For first-order constraints, contradiction detection reduces to satisfiability checking over finite domains — a solved problem with efficient algorithms (SAT/SMT solvers). For higher-order constraints, contradiction detection is undecidable in the general case: a norm that says "no norm may be self-defeating" triggers Godelian self-reference.

SPEC-003's resolution — partitioning into automated (first-order) and judgment (higher-order) tiers — is intellectually honest. It identifies the precise decidability boundary, implements automated checking up to it, and flags everything beyond for human review. The boundary is not a compromise but a mathematical fact about the limits of formal systems.

### 5.3 Machine-Checkability Spectrum

**Classification: GROUNDED.** The three formalization statuses (FORMAL, FORMALIZABLE, JUDGMENT) are well-established in the formal methods literature. The spectrum from fully automated to human-reviewed is not a weakness but a design feature: it prevents the false confidence of claiming full automation where formal limits preclude it (INV-000-004), while ensuring that every invariant that *can* be automated *is* automated.

---

## 6. Evolution Constraints

SPEC-003 may be amended through the following governed process only. This process is self-contained — it does not depend on any downstream spec for its authority.

### 6.1 Amendment Types

| Type | Definition | Requirements |
|------|-----------|-------------|
| **Invariant Addition** | Adds a new invariant (INV-NNN-NNN) to the register. Must trace to a SPEC-000 axiom, SPEC-001 entity class, or SPEC-002 primitive. | Hoare triple + TLA+ expression + deontic classification + adversarial review + creator sign-off |
| **Invariant Refinement** | Strengthens an existing invariant (tighter predicate, higher formalization status). Preserves identifier. | Demonstration that refinement is monotonic (new predicate implies old predicate) + adversarial review + creator sign-off |
| **Status Upgrade** | Moves an invariant from MISSING to DRIFT or from DRIFT to ALIGNED. Records the implementation that achieves alignment. | Code reference + test evidence + adversarial review + creator sign-off |
| **Breaking Revision** | Weakens an existing invariant or changes its deontic classification. | New grounding narrative + demonstration that weakening does not compromise system identity + adversarial review + human spot-check + creator sign-off |

### 6.2 Monotonicity Principle

Invariants may be added but never removed. An invariant that is discovered to be unnecessary may be weakened (via Breaking Revision with full justification) but its identifier is never reassigned. The register's history is preserved: every invariant ever declared remains in the historical record, with its amendment chain visible.

This principle is itself an instance of INV-000-003 (identity persistence): the register's invariant identifiers are UIDs. They are stable. Their expression (the predicate content) is mutable. Their history (the amendment chain) is versioned.

### 6.3 Versioning

The original SPEC-003 is never overwritten. Amendments are versioned: SPEC-003-v1.1, v1.2, etc. New invariants are added in the next version; existing invariants are refined in place with amendment annotations.

---

## 7. Traceability

### 7.1 Upward Traceability (to SPEC-000)

| SPEC-000 Element | SPEC-003 Invariant(s) | Relationship |
|------------------|-----------------------|-------------|
| AX-000-001 (Ontological Primacy) | INV-001-001 (Ontological Categorization) | Axiom mandates that every entity is ontologically declared; invariant enforces the categorization |
| AX-000-002 (Organizational Closure) | INV-000-002 (Governance Reachability), INV-000-005 (Observability) | Closure requires reachability and self-reporting |
| AX-000-003 (Individual Primacy) | INV-000-003 (Identity Persistence) | Individual identity must be preserved through all mutations |
| AX-000-004 (Constitutional Governance) | INV-000-001 (Dependency Acyclicity), INV-000-002 (Governance Reachability), INV-000-004 (Constitutional Supremacy) | Governance requires acyclic dependencies, reachable components, and consistent authority hierarchy |
| AX-000-005 (Evolutionary Recursivity) | (SPEC-003 enables evolution via governed amendment — Section 6) | The invariant register is itself subject to governed evolution |
| AX-000-007 (Alchemical Inheritance) | INV-000-003 (Identity Persistence) | Lineage preservation through dissolution, archival, merge, split |
| AX-000-008 (Multiplex Flow Governance) | INV-000-001 (Dependency Acyclicity) | G^dep DAG constraint is the first of five flow-type constraints |
| INV-000-001 through INV-000-005 (prose declarations) | INV-000-001 through INV-000-005 (formal definitions) | SPEC-000 declares intent; SPEC-003 formalizes enforcement |

### 7.2 Lateral Traceability (to SPEC-001 and SPEC-002)

| Lateral Spec | SPEC-003 Element | Relationship |
|-------------|------------------|-------------|
| SPEC-001 ONT-001 (Entity) | INV-001-001 (Ontological Categorization) | Entity classification generates the categorization invariant |
| SPEC-001 OntoClean (+R/~R/−R) | INV-001-002 (Subsumption Discipline) | Metaproperty annotations generate the subsumption invariant |
| SPEC-001 ONT-001 (+I) | INV-001-003 (Identity Criteria) | Identity criteria per category generate the identity invariant |
| SPEC-002 Section 4 (Sufficiency) | INV-002-001 (Primitive Composition) | Primitive sufficiency generates the composition invariant |
| SPEC-002 Section 2.1 (Non-Extensional Mereology) | INV-002-002 (Non-Extensional Mereology) | Mereological commitment generates the non-extensionality invariant |
| SPEC-002 PRIM-005/006 (State/Constraint) | INV-002-003 (Constraint Domain) | Constraint's dependence on State generates the domain invariant |
| SPEC-002 PRIM-006 (Constraint: deontic modality) | Section 1 deontic classification scheme | The Constraint primitive's O/P/F typing provides the formal semantics for invariant deontic classification |
| SPEC-002 Section 3.4 (GovernanceObject) | Section 4 constitutive force | GovernanceObject composition validates that invariants are compositions of primitives, not sui generis entities |

### 7.3 Downward Traceability (to SPEC-004, SPEC-005, and implementation)

| SPEC-003 Element | Downstream Target | Relationship |
|-----------------|-------------------|-------------|
| INV-000-001 through INV-000-005 | SPEC-004 (Logical Specification) | Invariants constrain the behavioral rules defined in SPEC-004 |
| Deontic classifications (O/P/F) | SPEC-005 (Rulebook) | The rulebook must be consistent with invariant deontic force |
| Contract model (Section 2) | `seed.yaml` schema (`schema-definitions/`) | Contract semantics constrain schema evolution |
| TLA+ specification (Section 3.1) | `governance/state_machine.py` | TLA+ Spec is the normative reference for implementation |
| Validator mapping (Section 3.3) | `governance/dependency_graph.py`, `metrics/organism.py` | One-to-one mapping: each invariant has exactly one validator |
| Counterexample traces (Section 3.2) | `tests/` (pytest test cases) | TLC counterexamples should be encoded as regression tests |
| Promotion as Liskov refinement (Section 2.2) | `governance/state_machine.py` transition table | Monotonic constraint accumulation must be verified in the transition table |

### 7.4 Academic Lineage

| Tradition | Key Sources | SPEC-003 Application |
|-----------|-------------|---------------------|
| Axiomatic verification | Hoare 1969, Floyd 1967 | Per-operation Hoare triples for each invariant |
| Design by Contract | Meyer 1997, Liskov & Wing 1994 | seed.yaml as DbC; promotion as Liskov refinement |
| Temporal logic specification | Lamport 1999 | TLA+ safety properties `[](Inv)` for each invariant |
| Deontic logic | von Wright 1951, von Wright 1963 | O/P/F classification and enforcement semantics |
| Model checking | Clarke, Grumberg & Peled 1999 | Verification methodology and counterexample generation |
| Weakest precondition | Dijkstra 1975 | Validator derivation as future architecture target |
| Constitutive rules | Searle 1995 | Philosophical warrant for invariants as system-defining |
| Institutional design | Crawford & Ostrom 1995, Ostrom 2005 | ADICO grammar for constraint structure |
| Non-extensional mereology | Simons 1987 | Grounding for INV-002-002 |
| Ontological analysis | Guarino & Welty 2002, Guarino 1998 | OntoClean grounding for INV-001-002 |

Full grounding narrative: `post-flood/specs/SPEC-003/grounding.md` (3,217 words)
Full risk register: `post-flood/specs/SPEC-003/risk-register.md` (10 classified claims)
Current state inventory: `post-flood/specs/SPEC-003/inventory.md` (11 invariant enforcement assessments)
Full bibliography: `post-flood/specs/bibliography.bib`
