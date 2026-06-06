# SPEC-001: Ontology Charter

```
Document ID:      SPEC-001
Title:            Ontology Charter
Version:          1.1
Status:           RATIFIED (G3 review incorporated)
Layer:            L1 — Metaphysical Identity
Authoritative:    Entire System
Parent Specs:     SPEC-000 (System Manifesto)
Date Ratified:    2026-03-18
Grounding:        post-flood/specs/SPEC-001/grounding.md
Risk Register:    post-flood/specs/SPEC-001/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. System Identity

SPEC-001 defines the formal ontological categories of ORGANVM: what kinds of things exist, how they are classified, how they relate, how they change state, and how they unfold through time. It provides the answer to the question that AX-000-001 (Ontological Primacy) places before all others: *define what exists before defining how it behaves.*

This charter replaces the flat entity-type enumeration (`ORGAN | REPO | MODULE | DOCUMENT | SESSION | VARIABLE | METRIC`) with a stratified taxonomy grounded in five traditions: formal ontology in information systems (Guarino 1998), upper ontology engineering (Arp, Smith & Spear 2015; Masolo et al. 2003), description logics (Baader et al. 2003), applied ontology methodology (Gruber 1993; Guarino & Welty 2004), and applied category theory (Fong & Spivak 2019).

ORGANVM adopts a DOLCE-aligned pluralist stance: entity types are real organizational structures — not merely conceptual conveniences — but their reality is constitutive (they exist because the constitutional architecture declares and sustains them) rather than mind-independent (they do not exist apart from the system that constitutes them). This is consistent with Luhmann's treatment of social systems as real but communicatively constituted, as grounded in SPEC-000.

---

## 2. Entity Classes

ORGANVM commits to three fundamental, mutually exclusive categories of entity, following the BFO/DOLCE consensus on the Continuant/Occurrent partition and DOLCE's addition of Abstract as a disjoint third category.

### ONT-001: Entity *(top-level sortal)*

**Definition:** A thing that exists within ORGANVM with persistent identity, tracked by a ULID-based UID.

*Formalization: FORMAL. Every entity carries a UID satisfying the regex `ent_[a-z]+_[0-9A-Za-z]{26}`. Identity is intrinsic: two entities are the same if and only if their UIDs are equal.*

*OntoClean: +R (rigid — being an entity is essential to all entities), +I (identity via UID), -D (independent of other entities at this level).*

*Traces to: SPEC-000 Section 6 ("Entity — a thing that exists with persistent identity"), INV-000-003 (Identity Persistence).*

### ONT-002: Continuant

**Definition:** An entity that persists through time and is wholly present at each moment of its existence. Continuants undergo qualitative change (gaining or losing properties) while maintaining identity.

*Formalization: FORMALIZABLE. Checkable as: entity exists at multiple timestamps without temporal-part decomposition. Requires SPEC-003 for temporal semantics.*

*Traces to: Arp, Smith & Spear 2015 (BFO Continuant); Masolo et al. 2003 (DOLCE Endurant).*

#### ONT-003: Independent Continuant

**Definition:** A continuant that bears qualities, has organizational extent, and does not depend on another entity for its existence. Independent continuants participate in containment hierarchies and are the primary bearers of governance state.

*Formalization: FORMAL. Checkable as: entity participates as parent or child in HierarchyEdge relations; entity bears promotion_status, tier, and implementation_status fields.*

*OntoClean: +R (rigid), +I (identity via UID + domain criteria), -D (independent).*

##### ONT-004: ORGAN

**Definition:** An organizational unit with functional differentiation, constitutional authority over a bounded domain, and a position in the organ sequence. Organs are the top-level containment boundaries.

*Formalization: FORMAL. Checkable as: entity appears as a top-level key in repo-registry.json with name, description, and repositories array. Identity criterion: organ position (0-VII).*

*Traces to: SPEC-000 Section 5 (Constitutional Topology), AX-000-006 (Topological Plasticity).*

##### ONT-005: REPO

**Definition:** A version-controlled repository within an organ, bearing a seed.yaml contract, governance state (promotion_status), and dependency declarations. Repos are the primary unit of constitutional governance.

*Formalization: FORMAL. Checkable as: entity appears in repo-registry.json repositories array with name, org, status, tier, promotion_status fields; corresponding seed.yaml exists in workspace.*

*Traces to: AX-000-004 (Constitutional Governance), INV-000-002 (Governance Reachability).*

##### ONT-006: MODULE

**Definition:** An extractable sub-package within a repository, identified by the excavation engine through structural analysis. Modules are the finest-grained independent continuants tracked by the system.

*Formalization: FORMAL. Checkable as: entity created by module_bridge.py with hierarchy edge to parent repo; entity_type=MODULE in ontologia store.*

*Traces to: AX-000-009 (Modular Alchemical Synthesis — modular decomposition).*

##### [Extension point for future independent entity types]

*Per AX-000-006 (Topological Plasticity), new independent continuant subtypes may be introduced through constitutional amendment. Examples: FORMATION (pre-organ crystallization), WORKSPACE (multi-repo grouping).*

#### ONT-007: Specifically Dependent Continuant

**Definition:** A continuant that inheres in exactly one bearer entity and cannot exist without it. Specifically dependent continuants are qualities — they characterize their bearer but are themselves entities with identity and temporal history.

*Formalization: FORMALIZABLE. Checkable as: entity has a mandatory bearer_uid field referencing an independent continuant; deletion of bearer cascades to deletion of dependent. Requires SPEC-003 for cascade semantics.*

*OntoClean: -R (anti-rigid — a variable is not essentially a variable; it is a quality that happens to be tracked), -I (identity derived from bearer + name), +D (dependent on bearer).*

*Traces to: Arp, Smith & Spear 2015 (Specifically Dependent Continuant); Masolo et al. 2003 (DOLCE Quality as first-class entity).*

##### ONT-008: VARIABLE

**Definition:** A named quality with temporal value history, inhering in a bearer entity. Variables track how a quality changes over time without the bearer losing its identity. Examples: `code_files`, `test_count`, `promotion_status`.

*Formalization: FORMAL. Checkable as: entity has name, bearer_uid, value, and timestamp fields; value history is append-only.*

*Traces to: SPEC-000 Section 6 ("Value — a datum attached to an entity").*

##### ONT-009: METRIC

**Definition:** A measured quality with thresholds, formulas, and gate associations, inhering in a bearer entity. Metrics are variables with additional normative structure: they define what values are healthy, strained, or critical. Examples: `test_coverage`, `dependency_health`, `seed_compliance`.

*Formalization: FORMAL. Checkable as: entity has name, bearer_uid, value, formula, and threshold fields; threshold defines gate levels.*

*Traces to: SPEC-000 INV-000-005 (Observability — metrics are the diagnostic instruments).*

##### [Extension point for future dependent quality types]

*Examples: DISPOSITION (a tendency or capacity that inheres in a bearer — e.g., a repo's "deployability"), ROLE (a function-dependent quality — e.g., "flagship" as a quality of certain repos).*

#### ONT-010: Generically Dependent Continuant

**Definition:** An information content entity that can be copied, versioned, and migrated between bearers without loss of identity. Generically dependent continuants depend on *some* bearer for their existence but are not bound to *one specific* bearer.

*Formalization: FORMALIZABLE. Checkable as: entity can be associated with multiple bearer_uids over time; copying does not create a new entity but a new concretization. Requires SPEC-003 for concretization semantics.*

*OntoClean: +R (rigid — a document is essentially a document), +I (identity via content hash or assigned UID), +D (dependent on some bearer, not a specific one).*

*Traces to: Arp, Smith & Spear 2015 (Generically Dependent Continuant — information content entity).*

##### ONT-011: DOCUMENT

**Definition:** An authored information content entity — specifications, plans, SOPs, governance narratives, grounding papers. Documents carry meaning that is independent of their storage location.

*Formalization: FORMALIZABLE. Checkable as: entity references a file path or content identifier; entity can be moved between repos without identity change.*

##### ONT-012: SCHEMA

**Definition:** A structural specification that constrains the form of other entities — JSON Schemas, seed.yaml contracts, governance-rules definitions. Schemas are information content entities whose purpose is to define validity conditions for other information content.

*Formalization: FORMAL. Checkable as: entity references a schema file in schema-definitions/schemas/; schema can be applied to validate instances.*

*Traces to: SPEC-000 AX-000-004 (Constitutional Governance — schemas as governance instruments).*

##### [Extension point for future information content types]

*Examples: TEMPLATE (a generative pattern for producing documents), PITCH (a presentation artifact derived from registry data).*

### ONT-013: Occurrent

**Definition:** An entity that unfolds through time and has temporal parts. Occurrents are not wholly present at any single moment — they accumulate through their duration. An occurrent's identity encompasses its entire temporal extent.

*Formalization: FORMALIZABLE. Checkable as: entity has start_time and (optionally) end_time; entity contains temporal sub-parts (messages in a session, stages in a build). Requires SPEC-003 for temporal-part semantics.*

*Traces to: Arp, Smith & Spear 2015 (BFO Occurrent); Masolo et al. 2003 (DOLCE Perdurant).*

#### ONT-014: Process

**Definition:** A bounded or continuous occurrent — an episode of activity with temporal extent and internal structure.

*Formalization: FORMALIZABLE. Checkable as: entity has duration > 0 and contains at least one temporal sub-part.*

##### ONT-015: SESSION

**Definition:** A bounded agent work episode with messages as temporal parts. Sessions have a defined start (agent invocation), a sequence of interactions (prompts, tool calls, responses), and a defined end (agent exit or timeout).

*Formalization: FORMAL. Checkable as: entity has agent_type, start_time, end_time, and message_count fields; source JSONL file exists at a discoverable path.*

##### ONT-016: BUILD

**Definition:** A CI pipeline execution — a bounded process triggered by code change, producing test results, lint reports, and deployment artifacts.

*Formalization: FORMAL. Checkable as: entity corresponds to a GitHub Actions workflow run with run_id, status, and conclusion fields.*

##### [Extension point for future process types]

*Examples: AUDIT (a governance verification pass), MIGRATION (a schema or data transformation process), INGESTION (an alchemia pipeline execution).*

#### ONT-017: Event

**Definition:** An instantaneous or near-instantaneous occurrent marking the boundary between two states. Events do not have duration — they mark transitions.

*Formalization: FORMALIZABLE. Checkable as: entity has a single timestamp (not a duration), a source entity, and a state-change description. Requires SPEC-003 for event-sourcing semantics.*

*Traces to: Arp, Smith & Spear 2015 (Process Boundary); SPEC-000 Section 6 ("Event — a state change with timestamp and causation").*

##### ONT-018: StateTransition

**Definition:** A governed change in an entity's promotion status, lifecycle status, or organism state. Examples: promotion from CANDIDATE to PUBLIC_PROCESS, archival, dissolution.

*Formalization: FORMAL. Checkable as: event references source entity UID, previous state, new state, and the governance rule authorizing the transition.*

*Traces to: SPEC-000 AX-000-004 (Constitutional Governance — governed transitions).*

##### ONT-019: SignalDispatch

**Definition:** An inter-organ event delivery — the transmission of a typed signal from a producing entity to one or more consuming entities through the event spine.

*Formalization: FORMALIZABLE. Checkable as: event references source entity, target entities, signal type, and payload. Requires SPEC-007 for signal-type definitions.*

*Traces to: SPEC-000 AX-000-008 (Multiplex Flow Governance), AX-000-009 (Modular Alchemical Synthesis).*

##### [Extension point for future event types]

*Examples: THRESHOLD_BREACH (a metric crossing a critical boundary), CLAIM_EVENT (an agent punching in or out of a coordination slot).*

#### ONT-020: Temporal Region

**Definition:** A duration that contextualizes occurrents — providing temporal framing without being an active process.

*Formalization: FORMALIZABLE. Checkable as: entity has start_time and end_time defining a closed or open interval; other occurrents reference this region as their temporal context.*

##### ONT-021: ERA

**Definition:** A constitutional epoch — a period during which a specific constitutional topology holds. Era transitions are governed by SPEC-008 and AX-000-006.

*Formalization: FORMALIZABLE. Checkable as: era has a topology snapshot (organ count, organ identities) and a boundary event marking its start.*

*Traces to: SPEC-000 AX-000-006 (Topological Plasticity — eras are the temporal units of topological change).*

##### ONT-022: SPRINT

**Definition:** A bounded work period with defined scope, start date, and end date. Sprints contextualize sessions, builds, and governance actions within a planning horizon.

*Formalization: FORMAL. Checkable as: entity has name, start_date, end_date, and scope description; tracked in corpus issue tracker.*

##### [Extension point for future temporal regions]

*Examples: SOAK_WINDOW (a 30-day stability monitoring period), FORMATION_PERIOD (the incubation interval before a formation crystallizes into an organ).*

### ONT-023: Abstract

**Definition:** A non-spatiotemporal entity that exists through logical constitution rather than physical or organizational instantiation. Abstracts do not persist through time like continuants or unfold through time like occurrents — they exist atemporally as normative, logical, or taxonomic structures.

*Formalization: JUDGMENT. The boundary between abstract entities and their concretizations (the JSON file that encodes a rule, the Python class that implements a constraint) is a modeling decision, not a machine-checkable property.*

*Traces to: DOLCE's treatment of abstract entities as a disjoint third category alongside endurants and perdurants.*

#### ONT-024: Governance Object

**Definition:** A normative entity that constrains behavior without itself being behavioral. Governance objects define what is permitted, required, or forbidden — they are the system's constitutional and regulatory instruments.

*Formalization: FORMALIZABLE. Checkable as: entity has conditions, effects, and scope; entity is referenced by governance audit results.*

*Traces to: SPEC-000 Section 6 ("Constraint — a rule limiting what states or transitions are lawful"), AX-000-004 (Constitutional Governance).*

##### ONT-025: RULE

**Definition:** An enforceable governance dictum — a specific, evaluable constraint on entity behavior or state. Examples: "dependency edges must form a DAG," "promotion from CANDIDATE requires CI workflow."

*Formalization: FORMAL. Checkable as: rule is encoded in governance-rules.json with conditions and enforcement mechanism; rule can be evaluated by `organvm governance audit`.*

##### ONT-026: CONSTRAINT

**Definition:** A structural invariant — an axiom, dependency rule, or topological restriction that must hold across all system states. Constraints are more fundamental than rules: rules may be revised through governed process; constraints may only be revised through constitutional amendment.

*Formalization: FORMAL. Checkable as: constraint corresponds to an INV-### or AX-### identifier in SPEC-000; violation detection mechanism exists or is specified.*

*Traces to: SPEC-000 Section 7 (Invariants), Section 4 (Axioms).*

##### [Extension point for future governance types]

*Examples: POLICY (a parameterized governance template), PRECEDENT (a recorded governance decision that informs future decisions).*

#### ONT-027: Capability

**Definition:** A declared ability of an entity — what a repo can do, what an agent can perform, what a pipeline can process. Capabilities are abstract entities that describe potential behavior without being behavior itself.

*Formalization: FORMALIZABLE. Checkable as: capability is declared in seed.yaml (produces/consumes) or agent profile; capability can be matched against requirements.*

*Traces to: SPEC-000 Section 6 ("Capability — an operation an entity may perform").*

#### ONT-028: Type

**Definition:** The taxonomy itself — the entity classes defined in this charter. Types are abstract entities that classify concrete entities. The inclusion of Type as an entity class provides self-referential closure: the ontology can describe its own structure.

*Formalization: JUDGMENT. Self-referential closure is a design commitment, not a machine-checkable property. The taxonomy must be consistent (no type is an instance of itself at the same level), but consistency requires human review of proposed extensions.*

*Traces to: Guarino 1998 (four-level ontology hierarchy — types belong to the top level); AX-000-005 (Evolutionary Recursivity — the taxonomy must be capable of governed self-modification).*

---

## 3. Relation Types

Entity relations in ORGANVM are typed and constrained. Following Sowa's (2000) triadic analysis, relations are themselves Relative entities — they mediate between Independent entities without being reducible to either relatum.

### ONT-030: Containment (HierarchyEdge)

**Definition:** A parent-child structural relation between independent continuants. Containment is transitive (if ORGAN contains REPO and REPO contains MODULE, then ORGAN contains MODULE), antisymmetric (if A contains B, B does not contain A), and acyclic.

*Formalization: FORMAL. Implemented as HierarchyEdge in ontologia with parent_uid, child_uid, edge_type, and structure_version fields. Transitivity and acyclicity are enforced by the hierarchy validator.*

*Domain constraint: Only independent continuants (ONT-003) may participate in containment hierarchies. A VARIABLE does not contain a MODULE; a DOCUMENT does not contain an ORGAN.*

*Traces to: INV-000-001 (Dependency Acyclicity — containment is a special case of the acyclic constraint).*

### ONT-031: Lineage (LineageRecord)

**Definition:** A temporal relation between entities recording predecessor/successor, derived-from, and merged-into links. Lineage is the structural implementation of AX-000-007 (Alchemical Inheritance) — no entity's history is lost; it is transformed.

*Formalization: FORMAL. Implemented as LineageRecord in ontologia with source_uid, target_uid, lineage_type, and timestamp fields.*

*Traces to: AX-000-007 (Alchemical Inheritance), INV-000-003 (Identity Persistence).*

### ONT-032: Naming (NameRecord)

**Definition:** A temporal alias relation tracking an entity's naming history. An entity may be known by different names at different times; the naming history is itself an information content entity (generically dependent continuant).

*Formalization: FORMAL. Implemented as NameRecord in ontologia with entity_uid, name, valid_from, and valid_until fields.*

### ONT-033: Dependency

**Definition:** A structural production-directional relation between repos (or organs). The dependency graph G^dep must be acyclic at all times. Dependency declares: "A requires B to function."

*Formalization: FORMAL. Implemented in governance/dependency_graph.py with DAG validation. Declared in seed.yaml `dependencies` field and repo-registry.json `dependencies` array.*

*Traces to: INV-000-001 (Dependency Acyclicity), AX-000-008 (Multiplex Flow Governance — G^dep).*

### ONT-034: Data Flow (produces/consumes)

**Definition:** A declared information flow relation between repos. Unlike dependencies, data flow edges may form cycles — information legitimately flows in recursive loops (AX-000-008: "the information graph must be recursively cyclic").

*Formalization: FORMAL. Declared in seed.yaml `produces` and `consumes` fields. Validated by seed graph builder.*

*Traces to: AX-000-008 (Multiplex Flow Governance — G^info).*

### ONT-035: Subscription

**Definition:** An event-type interest declaration — a repo declares which event types it wishes to receive through the event spine. Subscriptions are the pull-side complement to signal dispatches.

*Formalization: FORMAL. Declared in seed.yaml `subscriptions` field. Event types are validated against the dispatch payload schema.*

*Traces to: AX-000-009 (Modular Alchemical Synthesis — routing substrate).*

### ONT-036: Inherence

**Definition:** The relation between a specifically dependent continuant (ONT-007) and its bearer. A VARIABLE inheres in an ORGAN; a METRIC inheres in a REPO. Inherence is non-transferable: the dependent entity cannot migrate to a different bearer without becoming a different entity.

*Formalization: FORMALIZABLE. Checkable as: dependent entity's bearer_uid references an independent continuant; bearer_uid is immutable after creation. Requires SPEC-003 for immutability semantics.*

*Traces to: Arp, Smith & Spear 2015 (inherence as the relation between SDC and bearer); Guarino & Welty 2004 (dependence meta-property).*

### ONT-037: Promotion Constraint

**Definition:** A conditional relation between an entity's properties and its allowed state transitions. Promotion constraints define prerequisites: "to transition from CANDIDATE to PUBLIC_PROCESS, entity must have ci_workflow=true and platinum_status=true."

*Formalization: FORMAL. Implemented in governance/state_machine.py. Conditions are evaluated by `organvm governance promote`.*

*Traces to: AX-000-004 (Constitutional Governance), SPEC-000 Section 8 (Failure Modes — ungoverned component).*

---

## 4. State Models

Continuant entities undergo state changes while maintaining identity. ORGANVM defines two primary state models.

### ONT-040: Promotion State Machine

**Definition:** The lifecycle state model for repositories (and, by extension, any governed independent continuant). States and valid transitions:

```
LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED → ARCHIVED
```

Each transition has prerequisites defined by promotion constraints (ONT-037). Demotion (reverse transitions) is permitted through governed process. ARCHIVED is a terminal absorbing state from which re-promotion requires constitutional exception.

*Formalization: FORMAL. Implemented in governance/state_machine.py. Valid transitions, prerequisites, and demotion paths are fully specified.*

*OntoClean note: Promotion status is anti-rigid (-R) — a repository is not essentially a CANDIDATE; it merely occupies that state temporarily. The status is a specifically dependent continuant (a quality) inhering in the repository.*

*Traces to: SPEC-000 AX-000-004 (Constitutional Governance).*

### ONT-041: Organism State Model

**Definition:** The affective state model for the Living Data Organism, derived from gate evaluation across multiple metrics:

```
thriving | coherent | strained | brittle
```

This is a diagnostic projection for the human operator (Damasio 1999, adapted per SPEC-000), not a claim about machine phenomenology. The state is computed, not declared — it emerges from the aggregate health of constituent metrics.

*Formalization: FORMAL. Implemented in metrics/organism.py and metrics/gates.py. State is computed from gate pass rates; thresholds are defined in code.*

*Traces to: SPEC-000 Section 1 (institutional-computational autopoiesis — the organism metaphor), INV-000-005 (Observability).*

---

## 5. Process Types

Occurrents in ORGANVM fall into three categories, following BFO's process taxonomy.

### ONT-050: Bounded Process

**Definition:** A process with defined start and end points. Bounded processes are the primary occurrents tracked by the system. Examples: sessions, builds, governance audits, promotion events.

*Formalization: FORMAL. Checkable as: entity has non-null start_time and end_time; duration is finite and positive.*

### ONT-051: Continuous Process

**Definition:** A process with no defined endpoint — operationally circular processes that instantiate the system's communicative autopoiesis. Examples: context-sync pipeline, metric propagation, registry validation loop.

*Formalization: JUDGMENT. Continuous processes are identified by operational role (they run indefinitely and restart on failure), not by formal temporal properties. Whether a process is "continuous" is a design designation, not a discoverable property.*

*Traces to: SPEC-000 AX-000-002 (Organizational Closure — constitutive processes are self-producing).*

### ONT-052: Process Boundary (Event)

**Definition:** An instantaneous occurrent marking the transition between two states. Events in ORGANVM's event spine are process boundaries — they do not have duration but mark the boundary between two states of a continuant or two phases of a process.

*Formalization: FORMALIZABLE. Checkable as: entity has a single timestamp, references a source entity, and records a before-state and after-state. Requires SPEC-003 for event-sourcing formalization.*

*Traces to: Arp, Smith & Spear 2015 (Process Boundary as a subtype of Occurrent).*

---

## 6. Formal Definitions: Stratified Taxonomy

The complete stratified taxonomy, replacing the flat `EntityType` enum:

```
Entity (ONT-001, top-level sortal, +R rigid, +I identity via UID)
├── Continuant (ONT-002, persists through time, wholly present at each moment)
│   ├── IndependentContinuant (ONT-003, bears qualities, organizational extent)
│   │   ├── ORGAN      (ONT-004) — organizational unit with functional differentiation
│   │   ├── REPO       (ONT-005) — version-controlled repository within an organ
│   │   ├── MODULE     (ONT-006) — extractable sub-package within a repository
│   │   └── [extension point for future independent entity types]
│   ├── SpecificallyDependentContinuant (ONT-007, inheres in exactly one bearer)
│   │   ├── VARIABLE   (ONT-008) — named quality with temporal value history
│   │   ├── METRIC     (ONT-009) — measured quality with thresholds and formulas
│   │   └── [extension point for future dependent quality types]
│   └── GenericallyDependentContinuant (ONT-010, information content, copyable)
│       ├── DOCUMENT   (ONT-011) — authored information content entity
│       ├── SCHEMA     (ONT-012) — structural specification (JSON Schema, seed contract)
│       └── [extension point for future information content types]
├── Occurrent (ONT-013, unfolds through time, has temporal parts)
│   ├── Process (ONT-014, bounded or continuous temporal entity)
│   │   ├── SESSION    (ONT-015) — bounded agent work episode
│   │   ├── BUILD      (ONT-016) — CI pipeline execution
│   │   └── [extension point for future process types]
│   ├── Event (ONT-017, instantaneous process boundary)
│   │   ├── StateTransition  (ONT-018) — promotion, demotion, archive
│   │   ├── SignalDispatch   (ONT-019) — inter-organ event delivery
│   │   └── [extension point for future event types]
│   └── TemporalRegion (ONT-020, duration contextualizing occurrents)
│       ├── ERA        (ONT-021) — constitutional epoch
│       ├── SPRINT     (ONT-022) — bounded work period
│       └── [extension point for future temporal regions]
└── Abstract (ONT-023, non-spatiotemporal, logically constituted)
    ├── GovernanceObject (ONT-024, normative entity constraining behavior)
    │   ├── RULE        (ONT-025) — enforceable governance dictum
    │   ├── CONSTRAINT  (ONT-026) — structural invariant (axiom, dependency rule)
    │   └── [extension point for future governance types]
    ├── Capability (ONT-027, declared ability of an entity)
    └── Type (ONT-028, the taxonomy itself — self-referential closure)
```

### Formal Criteria Satisfied

1. **BFO categorical completeness** (Arp, Smith & Spear 2015): Every current EntityType maps to exactly one BFO category. No BFO category relevant to ORGANVM's domain is unrepresented.

2. **OntoClean subsumption soundness** (Guarino & Welty 2004): Entity is rigid (+R), and all intermediate categories maintain rigidity. Anti-rigid types (VARIABLE, METRIC) are properly subordinated under a rigid supertype (SpecificallyDependentContinuant), satisfying the constraint that anti-rigid cannot subsume rigid.

3. **DOLCE quality-as-entity** (Masolo et al. 2003): VARIABLE and METRIC are first-class entities with their own identity and temporal history, not mere attributes of their bearers. This matches the ontologia implementation, which assigns them ULIDs.

4. **Gruber's five criteria** (Gruber 1993): Clarity (each category has a formal BFO/DOLCE definition), coherence (the taxonomy is internally consistent), extendibility (every leaf level includes an extension point), minimal encoding bias (the taxonomy is representation-neutral), minimal ontological commitment (only categories necessary for cross-organ knowledge sharing are included).

5. **Topological plasticity** (AX-000-006): Extension points at every level ensure new entity types can be added without revising existing definitions.

### Domain Entities as Compositions

The Stage-II corpus proposed eight "core primitive entities": Agent, Artifact, Capability, Process, Signal, Relation, Governance Object, Evidence Object. These are not ontological primitives but domain-level compositions of the SPEC-002 primitives:

| Domain Entity | Composition | Ontological Classification |
|---------------|------------|---------------------------|
| Agent | IndependentContinuant + Capability + State | Domain role, not ontological primitive |
| Artifact | IndependentContinuant + Value + State | Domain role, not ontological primitive |
| Signal | Event + Value + Relation | Domain role, not ontological primitive |
| Governance Object | Abstract + Constraint + State | Promoted to ontological category (ONT-024) |

*Formalization: JUDGMENT. Whether a domain entity is "truly" a composition or "really" a primitive is a design decision governed by Gruber's minimal ontological commitment principle. SPEC-001 defines only what is necessary at the ontological level; domain compositions belong to SPEC-002 and above.*

---

## 7. Reconciliation

Three distinct primitive sets required harmonization. SPEC-001 resolves the reconciliation problem identified in the pre-spec inventory:

| Source | Original Set | SPEC-001 Resolution |
|--------|-------------|-------------------|
| SPEC-000 (7 primitives) | Entity, Value, Relation, Event, State, Constraint, Capability | Confirmed as primitive categories. Each maps to an ONT-### definition. Entity→ONT-001, Relation→Section 3, Event→ONT-017, State→Section 4, Constraint→ONT-026, Capability→ONT-027. Value is a property of SpecificallyDependentContinuants, not itself an entity class. |
| Stage-II root classes (8) | Entity, Value, Relation, Event, State, Process, Constraint, Evidence | Process restored as ONT-014 (SPEC-000 omitted it). Evidence subsumed under DOCUMENT (ONT-011) — evidence is authored information content, not a separate ontological category. |
| Stage-II domain entities (8) | Agent, Artifact, Capability, Process, Signal, Relation, Governance Object, Evidence Object | Demoted to domain-level compositions (see Section 6). Governance Object elevated to ontological category (ONT-024) due to its constitutive role in ORGANVM's autopoiesis. |
| Ontologia implementation (7) | ORGAN, REPO, MODULE, DOCUMENT, SESSION, VARIABLE, METRIC | All preserved as leaf-level entity types in the stratified taxonomy. Each gains a category_path (e.g., Entity > Continuant > IndependentContinuant > ORGAN). |

*Formalization: FORMAL. Reconciliation is complete and deterministic. Every member of every prior set maps to exactly one ONT-### definition or is explicitly marked as a domain composition.*

---

## 8. Contestation Disclosures

Two design decisions involve active disagreement in the formal ontology literature. Intellectual honesty requires explicit disclosure, following the protocol established in SPEC-000.

### 8.1 BFO Realism versus DOLCE Pluralism

BFO's realist stance (Smith 2004; Arp, Smith & Spear 2015) demands that ontological categories correspond to universals existing in mind-independent reality. Under strict BFO realism, ORGANVM's entity types should be discovered, not designed.

DOLCE's pluralist stance (Masolo et al. 2003) treats ontological categories as reasonable cognitive-linguistic constructs for a given domain.

**ORGANVM adopts DOLCE-aligned pluralism.** Entity types are real organizational structures — not merely conceptual conveniences — but their reality is constitutive (they exist because the constitutional architecture declares and sustains them) rather than mind-independent. The practical consequence: when AX-000-006 enables topological mutation, the DOLCE stance permits these changes as legitimate ontological evolution, while BFO realism would require demonstrating that new categories better reflect mind-independent universals.

*Risk classification: ADAPTED (per risk register). 60% of SPEC-001's claims are GROUNDED in BFO/DOLCE consensus; 30% are ADAPTED from one tradition with explicit justification; 10% are NOVEL with original argument. No claims are CONTESTED.*

### 8.2 The Flat-Enum Problem

The existing `organvm-ontologia` module implements entity types as a flat Python enum. The stratified taxonomy requires restructuring this into a hierarchical classification.

This is not merely a code-quality improvement but a structural necessity demonstrated by OntoClean analysis. The flat enum treats ORGAN (+R rigid, -D independent, +I position-based identity) and METRIC (-R anti-rigid, +D dependent, -I formula-based identity) as ontological peers, violating the OntoClean constraint that rigid and anti-rigid types should be distinguished in the subsumption hierarchy.

**Migration path:** The existing ULID-based identity system, HierarchyEdge relations, and NameRecord temporal naming all remain intact. The EntityType enum gains intermediate categories. Existing entity UIDs maintain their identity — the taxonomy change is a reclassification, not a re-creation. The ontologia module's `entity_type` field carries the leaf-level type (ORGAN, REPO, etc.) while a new `category_path` field carries the full classification (Entity > Continuant > IndependentContinuant > ORGAN).

### 8.3 Category Theory as Regulative Ideal

Category theory (Fong & Spivak 2019) provides the most rigorous compositional framework for the entity taxonomy. ORGANVM's relation types are morphisms, composition laws are structural invariants, and schema migrations are functorial mappings.

**ORGANVM adopts category theory as a regulative ideal, not an implementation requirement.** The taxonomy is *categorically informed* (it respects compositional principles and morphism typing) without being *categorically implemented* (no categorical programming language or proof assistant is used). Full category-theoretic formalization is a horizon-5 aspiration.

---

## 9. Evolution Constraints

SPEC-001 may be amended through the following governed process. This process is self-contained and does not depend on any downstream spec for its authority.

1. A revision proposal must cite specific evidence (new entity type discovered through system operation, OntoClean violation detected, reconciliation gap found) demonstrating that the current taxonomy is insufficient or incorrect
2. Proposed changes are classified as:
   - **Leaf Extension**: Adding a new entity type under an existing intermediate category via an extension point. Requires: OntoClean meta-property analysis of the proposed type, demonstration that subsumption constraints are preserved, adversarial review by a different agent/model, creator sign-off
   - **Intermediate Revision**: Modifying an intermediate category (e.g., splitting IndependentContinuant into sub-categories). Requires: (a) OntoClean analysis, (b) impact assessment on all leaf types under the modified category, (c) adversarial review, (d) creator sign-off
   - **Categorical Restructuring**: Modifying the top-level tripartite split (Continuant/Occurrent/Abstract) or adding a fourth top-level category. Requires: (a) a new grounding narrative with peer-reviewed academic justification, (b) full OntoClean audit of the revised taxonomy, (c) adversarial review, (d) human spot-check of cited sources, (e) impact assessment on all downstream specs, (f) explicit creator sign-off
3. Extension points are constitutionally guaranteed by AX-000-006 — they may not be removed or restricted except through Categorical Restructuring
4. Every new ONT-### definition must specify: Formalization Status (FORMAL / FORMALIZABLE / JUDGMENT), OntoClean meta-properties (+/-R, +/-I, +/-D), and traces to at least one SPEC-000 axiom or invariant
5. The original SPEC-001 is never overwritten — amendments are versioned addenda (SPEC-001-v1.1, v1.2, etc.)
6. All amendment proposals, reviews, and sign-offs are recorded in the governance audit trail

---

## 9b. ONT Numbering Allocation

| Block | Range | Category |
|-------|-------|----------|
| Entity Classes | ONT-001 — ONT-028 | What kinds of things exist |
| ONT-029 | Reserved | |
| Relation Types | ONT-030 — ONT-037 | How things connect |
| ONT-038 — ONT-039 | Reserved | |
| State Models | ONT-040 — ONT-041 | How things change state |
| ONT-042 — ONT-049 | Reserved | |
| Process Types | ONT-050 — ONT-052 | How things happen |
| ONT-053 — ONT-059 | Reserved | |

## 9c. Implementation Status

SPEC-001 defines 28 entity types. The current `organvm-ontologia` implementation supports 7. The remaining 21 are constitutional commitments with implementation debt.

### Ratified and Implemented (reclassify existing code)

These 7 types exist in `ontologia/entity/identity.py` as `EntityType` enum values. SPEC-001 reclassifies them within the stratified taxonomy without requiring new code:

| ONT-### | Type | Current EntityType | Category Path |
|---------|------|-------------------|---------------|
| ONT-004 | ORGAN | `EntityType.ORGAN` | Entity > Continuant > IndependentContinuant > ORGAN |
| ONT-005 | REPO | `EntityType.REPO` | Entity > Continuant > IndependentContinuant > REPO |
| ONT-006 | MODULE | `EntityType.MODULE` | Entity > Continuant > IndependentContinuant > MODULE |
| ONT-008 | VARIABLE | `EntityType.VARIABLE` | Entity > Continuant > SpecificallyDependentContinuant > VARIABLE |
| ONT-009 | METRIC | `EntityType.METRIC` | Entity > Continuant > SpecificallyDependentContinuant > METRIC |
| ONT-011 | DOCUMENT | `EntityType.DOCUMENT` | Entity > Continuant > GenericallyDependentContinuant > DOCUMENT |
| ONT-015 | SESSION | `EntityType.SESSION` | Entity > Occurrent > Process > SESSION |

Implementation target: Add `category_path` field to EntityIdentity (engine #26). Existing UIDs and data remain intact.

### Ratified with Implementation Debt (new types requiring code)

| ONT-### | Type | Target Layer | Engine Issue |
|---------|------|-------------|-------------|
| ONT-012 | SCHEMA | L3A (SPEC-007) | — |
| ONT-016 | BUILD | L4A (Event Spine) | #12 |
| ONT-017 | StateTransition | L4A (Event Spine) | #12 |
| ONT-018 | SignalDispatch | L3B (Formation Protocol) | #20 |
| ONT-021 | ERA | L3B (Era Model) | — |
| ONT-022 | SPRINT | L3B | — |
| ONT-025 | RULE | L2 (SPEC-005) | #15 |
| ONT-026 | CONSTRAINT | L2 (SPEC-003) | #15 |
| ONT-027 | Capability | L3B | #27 |

Note: Intermediate categories (ONT-001 Entity, ONT-002 Continuant, ONT-003 IndependentContinuant, etc.) are structural classifications, not implementation types — they do not require new `EntityType` enum values.

**ONT-021 (ERA) dependency disclosure:** ERA instantiation depends on resolving the AX-000-006 implementation conflict documented in SPEC-000's inventory (organ topology hardcoded in 3 locations). ERA cannot be operationalized until organ topology becomes data-driven.

---

## 10. Traceability

### Upstream: SPEC-000 (System Manifesto)

| SPEC-000 Element | SPEC-001 Resolution |
|-----------------|-------------------|
| AX-000-001 (Ontological Primacy) | Fulfilled — SPEC-001 defines what exists before downstream specs define behavior |
| AX-000-004 (Constitutional Governance) | ONT-004, ONT-005, ONT-025, ONT-026, ONT-037 — governance entities and constraints |
| AX-000-005 (Evolutionary Recursivity) | ONT-028 (Type as self-referential), Section 9 (amendment procedure) |
| AX-000-006 (Topological Plasticity) | Extension points at every level; ONT-021 (ERA for topological epochs) |
| AX-000-007 (Alchemical Inheritance) | ONT-031 (Lineage), inherence semantics for dependent continuants |
| AX-000-008 (Multiplex Flow) | ONT-033 (Dependency), ONT-034 (Data Flow), ONT-035 (Subscription) |
| AX-000-009 (Modular Synthesis) | ONT-006 (MODULE), ONT-019 (SignalDispatch), ONT-027 (Capability) |
| INV-000-001 (Dep. Acyclicity) | ONT-030 (Containment acyclicity), ONT-033 (Dependency DAG) |
| INV-000-003 (Identity Persistence) | ONT-001 (Entity identity via UID), ONT-031 (Lineage) |
| INV-000-005 (Observability) | ONT-009 (METRIC), ONT-041 (Organism State) |
| Primitives (Section 6) | Each primitive maps to ONT-### definitions per Section 7 reconciliation |

### Downstream: Forward Links

```
SPEC-001 (this document)
├── ONT-001 through ONT-052 → referenced by all downstream specs
├── Stratified taxonomy → implemented by SPEC-002 (Primitive Register)
│   SPEC-002 must demonstrate that its primitives compose correctly
│   with the stratified taxonomy — domain entities derivable from
│   SPEC-002 compositions must be classifiable within SPEC-001
│   without forcing or residue
├── Relation types → formalized by SPEC-003 (Behavioral Contract)
│   SPEC-003 defines invariant semantics for ONT-030 through ONT-037
├── State models → implemented by SPEC-003 (Behavioral Contract)
│   SPEC-003 formalizes ONT-040 and ONT-041 as machine-checkable
│   statecharts with guard conditions and effect declarations
├── Process types → detected by SPEC-009 (Sensing Framework)
│   SPEC-009 defines how occurrents are observed and recorded
├── Entity taxonomy evolution → governed by SPEC-008 (Evolution Protocol)
│   SPEC-008 extends Section 9's amendment procedure with
│   cross-specification consistency checks
└── Extension points → exercised by future specs as new entity types
    are discovered through system operation
```

### Academic Lineage

| ONT Cluster | Traditions | Key Sources |
|-------------|-----------|-------------|
| ONT-001 through ONT-003 | Formal ontology, upper ontology | Guarino 1998, Arp/Smith/Spear 2015, Masolo et al. 2003 |
| ONT-004 through ONT-006 | Institutional design | Ostrom 1990, Beer 1972 |
| ONT-007 through ONT-009 | Quality ontology | DOLCE (Masolo et al. 2003), BFO (Arp/Smith/Spear 2015) |
| ONT-010 through ONT-012 | Information ontology | BFO (Generically Dependent Continuant), Guarino 1998 |
| ONT-013 through ONT-022 | Process ontology | BFO (Occurrent), Luhmann 1995 (autopoietic processes) |
| ONT-023 through ONT-028 | Applied ontology, governance | Gruber 1993, Guarino & Welty 2004 (OntoClean) |
| ONT-030 through ONT-037 | Category theory, network science | Fong & Spivak 2019, Sowa 2000, Newman 2018 |
| ONT-040 through ONT-052 | Cybernetics, systems theory | Beer 1972, Ashby 1956, Luhmann 1995 |

Full grounding narrative: `post-flood/specs/SPEC-001/grounding.md` (5,800+ words)
Full risk register: `post-flood/specs/SPEC-001/risk-register.md` (10 classified claims)
Reconciliation inventory: `post-flood/specs/SPEC-001/inventory.md`
