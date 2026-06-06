# SPEC-000: System Manifesto

```
Document ID:      SPEC-000
Title:            System Manifesto
Version:          1.1
Status:           RATIFIED (G3 review incorporated)
Layer:            L1 — Metaphysical Identity
Authoritative:    Entire System
Parent Specs:     None (root document)
Date Ratified:    2026-03-18
Grounding:        post-flood/specs/SPEC-000/grounding.md
Risk Register:    post-flood/specs/SPEC-000/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. System Identity

ORGANVM is a self-governing sociotechnical organism whose purpose is to enable a single creative practitioner to operate with the coherence and reach of an institution, steering automation toward empowerment rather than collapse.

The system is constituted by functionally differentiated organs — bounded domains of creative, productive, governance, and communicative activity — interconnected through typed signal flows and governed by a constitutional architecture grounded in autopoietic systems theory (Maturana & Varela 1980; Luhmann 1995), cybernetics (Ashby 1956; Beer 1972), institutional design (Ostrom 1990), and actor-network theory (Latour 2005).

ORGANVM claims *institutional-computational autopoiesis*: the system's governance communications (event dispatches, context-sync documents, agent prompts, promotion decisions, metric computations) recursively produce further governance communications through computationally traceable chains. This is an adaptation of Luhmann's communicative autopoiesis, with the explicit departure that the system does not claim biological self-production, metabolic precariousness, or phenomenal experience. The production mechanism is computational, not biochemical; the closure is organizational, not material.

### Contestation Disclosure

Maturana rejected extending autopoiesis beyond biology. Varela (1992) cautioned against formal abstraction. Fleischaker (1988) tied autopoiesis constitutively to life. McMullin (2004) found no uncontested achievement of computational autopoiesis in 30 years. ORGANVM proceeds via Luhmann's communicative route while fully disclosing these objections. The claim is an extension, not a direct application.

---

## 2. System Purpose

The system exists to solve a structural asymmetry: individual creative practitioners need institutional-scale infrastructure but cannot sustain institutional-scale bureaucracy.

ORGANVM provides a closed epistemic loop:

```
theory → ontology → logic → architecture → implementation → verification → governance → theory
```

where every implementation artifact has traceable theoretical origin and every theoretical commitment has verifiable implementation.

The system treats theory, structure, behavior, implementation, and verification as layers of a single continuous structure — not separate concerns managed by separate tools.

---

## 3. System Scope

ORGANVM governs the design, implementation, and evolution of creative-institutional infrastructure requiring:

- Structured knowledge modeling across multiple domains
- Polycentric governance with constitutional authority
- Multi-agent AI orchestration with governed authority
- Traceable refinement from theory through implementation
- Evolutionary self-modification through governed processes

The system boundary is defined by registry inclusion: what is registered in `repo-registry.json` is inside ORGANVM; what is not registered is environment.

---

## 4. Axioms

The following axioms are the irreducible commitments of the system. Each is derived from the academic grounding documented in `post-flood/specs/SPEC-000/grounding.md`. No downstream specification, implementation, or governance decision may violate these axioms. Amendment requires constitutional revision through the process defined in Section 9.

Each axiom carries a **Formalization Status**:
- **FORMAL**: Machine-checkable validator exists or can be written against current definitions
- **FORMALIZABLE**: Validator can be specified but requires downstream specs (SPEC-003, 006, 007) for formal semantics
- **JUDGMENT**: Requires human assessment; not reducible to machine-checkable constraint

### AX-000-001: Ontological Primacy

**Define what exists before defining how it behaves.**

Every entity, relation, and process in the system must be ontologically declared (SPEC-001) before behavioral rules are applied to it (SPEC-004). Implementation without ontological grounding is structurally unauthorized.

*Formalization: FORMALIZABLE. Checkable as: every entity in ontologia has creation timestamp prior to first governance action referencing it. Formal semantics deferred to SPEC-001.*

*Grounded in: Guarino 1998, formal ontology; Smith 2004, reality representation; Sowa 2000, knowledge representation.*

### AX-000-002: Organizational Closure

**Every constitutive process of the system is specified by processes within the system.**

The pattern of governance relations is self-produced: the engine validates the registry, the registry defines what the engine governs, the governance rules constrain how the registry may change, and the constitutional specs constrain the governance rules. No external authority defines the system's organization. Material substrates (GitHub, Python, hardware) are environment, not organization.

*Formalization: FORMALIZABLE. Constitutive processes are: registry load/save, governance audit, promotion transition, dependency validation, seed discovery, context sync, metric computation. Closure verifiable as: each constitutive process is invoked only by other constitutive processes or by the human principal. Current gap: the governance loader does not validate governance-rules.json against its own schema (DRIFT per inventory).*

*Grounded in: Maturana & Varela 1980, autopoiesis; Luhmann 1995, communicative self-production. Departure: organizational, not material closure.*

### AX-000-003: Individual Primacy

**The system exists to amplify individual creative capacity, not to replace it.**

System optimization is constitutionally subordinate to individual empowerment. No governance rule, automation, or agent action may be justified solely by system-level efficiency if it diminishes the creative autonomy of the individual practitioner. This is a guiding constitutional principle — a value commitment that shapes all downstream design decisions.

*Formalization: JUDGMENT. This axiom cannot be reduced to a machine-checkable constraint because "creative autonomy" and "diminishment" are value judgments. Enforcement is through constitutional review: any proposal for system-wide optimization must include an individual-impact assessment documenting how the change preserves or enhances individual creative capacity. The assessment is reviewed by the human principal, not by automated validators.*

*Novel: no direct academic precedent. Ethical architectural decision.*

### AX-000-004: Constitutional Governance

**No component may exist, operate, or evolve without constitutional authorization.**

Every repository requires a `seed.yaml` contract declaring at minimum: organ membership, tier, and promotion status. Every status transition follows the governed promotion path. Every dependency edge is declared and validated. Governance is not optional overhead but a constitutive feature of the system's autopoiesis — without it, the system is not self-producing but merely accumulating.

Code artifacts that exist in the workspace but are not registered (e.g., personal projects in LIMINAL, intake staging areas) are environment, not system, regardless of their location in the workspace directory structure.

*Formalization: FORMAL. Checkable as: every registered repo has seed.yaml with organ/tier/status fields; every transition in promotion history follows state_machine.py valid paths; every dependency edge appears in allowed_edges.*

*Grounded in: Ostrom 1990, design principles; Beer 1972, viability requires governance; Crawford & Ostrom 1995, institutional grammar (ADICO).*

### AX-000-005: Evolutionary Recursivity

**The system must be capable of modifying its own rules, including the rules for rule-modification, through governed processes.**

First-order change: state and structure evolve within existing rules. Second-order change: the rules themselves evolve through governed revision (SPEC-008). Third-order change: the meta-rules governing rule-change evolve through the meta-evolution protocol (SPEC-011). No level of the governance hierarchy is exempt from governed evolution. No level may evolve without governance.

*Formalization: FORMALIZABLE. Checkable as: (a) a code path exists for modifying governance-rules.json through a governed process, (b) modification generates an audit trail, (c) the state machine transitions are loaded from data, not hardcoded. Current gap: state machine transitions are hardcoded in Python (DRIFT per inventory); evolution-policy schema exists but no engine code evaluates it.*

*Inspired by: Ashby 1952, structural reorganization under feedback failure; von Foerster 1981, second-order observation. The extension to three orders of change (state → rules → meta-rules) is a novel application beyond Ashby's original formulation.*

### AX-000-006: Topological Plasticity

**The system's functional differentiation into distinct organs is designed to be a governed variable, not a frozen constant.**

The current topology — eight organs numbered 0-VII — is the first-era instantiation, not the eternal form. New functional domains may crystallize from formation activity when evidence demonstrates structural irreducibility: a formation's outputs have become load-bearing for the system as a whole. Existing domains may fuse, split, or dissolve through governed constitutional revision and era transition.

*Formalization: FORMALIZABLE. Checkable as: organ topology is loaded from a data configuration, not hardcoded in Python source. Current gap: CONFLICT per inventory — topology is hardcoded in organ_config.py (Python dict literal), dependency_graph.py (ORGAN_LEVELS), and organ-definitions.schema.json (regex). Implementation target: Layer 3B refactors topology to data-driven configuration.*

*Novel: no existing systems theory prescribes governed topological mutation as a design feature. Inspired by Luhmann 1995 (functional differentiation as evolutionary achievement), Kauffman 1993 (emergent order), Gersick 1991 (punctuated equilibrium). These describe how topology changes; ORGANVM proposes how to govern that change constitutionally.*

### AX-000-007: Alchemical Inheritance

**The system's prior structural failures are not waste but prima materia.**

Every dissolved, archived, or superseded component carries structured lineage information (at minimum: predecessor UIDs, successor UIDs, dissolution reason, dissolution date, lineage type) that subsequent formations may draw upon. The post-flood corpus is a constitutional artifact with the same authority as living code. No era may discard the memory of prior eras; it may only transform it. What the system was shapes what it may become.

*Formalization: FORMALIZABLE. Checkable as: every entity with lifecycle_status=ARCHIVED or DISSOLVED has a LineageRecord in ontologia with at least one predecessor or successor edge. Current gap: DRIFT per inventory — 52 dissolved repos have freetext `note` fields, not structured LineageRecords. Ontologia's lineage system exists but is not wired to registry archival operations.*

*Novel: analogical grounding in alchemical tradition (nigredo precedes rubedo); North 1990, path dependence; Ashby 1952, failed adaptations inform subsequent reorganization.*

### AX-000-008: Multiplex Flow Governance

**Inter-organ flow is not a single relation but a family of distinct, independently governed edge types.**

At minimum five flow types are defined for the shared topology (currently only the dependency layer is fully governed; the remaining four are implementation targets for SPEC-006 and SPEC-007):

| Flow Type | Constraint | Character |
|-----------|-----------|-----------|
| **Dependency** (G^dep) | Acyclic (DAG) | Structural, production-directional |
| **Information** (G^info) | Recursively cyclic | Epistemic, learning-directional |
| **Governance** (G^gov) | Reachability from constitutional roots | Supervisory, authorization-directional |
| **Evolution** (G^evo) | Time-monotonic | Historical, lineage-directional |
| **Signal/Modulation** (G^mod) | Type-compatible, attenuated | Real-time, behavior-modifying |

The central theorem: **the dependency graph must be acyclic, but the information graph must be recursively cyclic.** This is the mathematical signature of a healthy recursive organism. No single "dependency direction" rule can adequately govern a multiplex system.

*Formalization: FORMALIZABLE. Dependency layer: FORMAL (DAG check implemented). Information, governance, evolution, signal layers: require SPEC-006/007 for formal edge-type definitions and constraint specifications. Current gap: DRIFT per inventory — only dependency flow is governed; other 4 layers are not tracked as independent graph layers.*

*Grounded in: post-flood corpus graph-theoretic model; Newman 2018, multiplex networks; Beer 1972, variety in communication channels; Boccaletti et al. 2006, complex network dynamics.*

### AX-000-009: Modular Alchemical Synthesis

**The organism is designed to operate as a modular synthesis architecture.**

Every component will have declared inputs and outputs. Any output may be routed to any compatible input. Modulation — one signal shaping another signal's processing behavior — is a first-class constitutional operation, distinct from dependency, information flow, or governance.

The routing substrate (Taxis) patches connections but does not generate signals. Signal compatibility will be governed by typed signal classes. Attenuation policies will govern signal strength at every patch point. Every connection will be observable: the event spine records signal flow, the temporal metric fabric tracks frequency and amplitude, and the graph indices measure routing health.

The patch matrix — what is connected to what, through what, at what gain — is a first-class constitutional artifact to be maintained alongside the registry.

*Formalization: FORMALIZABLE. Requires: signal class definitions (14 canonical types from Formation Protocol), seed.yaml schema extension for signal_inputs/signal_outputs, patch matrix data structure, attenuation policy schema. Current gap: MISSING per inventory — no part of this architecture is currently implemented. Implementation target: Layer 3B (signal classes, formation protocol) + Layer 4A (event spine, temporal metrics).*

*Novel: grounded by analogy in modular synthesis (Moog, Buchla, Serge); Beer 1972, communication channel variety; Ashby 1956, requisite variety in routing; Callon 1986, translation as signal exchange. The treatment of modulation as constitutionally distinct from other edge types has no precedent in systems theory or software architecture.*

---

## 5. Constitutional Topology (First Era)

The current era instantiates 8 functionally differentiated organs. Per AX-000-006, this topology is subject to governed revision.

### Authority Stack

| Layer | Authority | Function |
|-------|----------|----------|
| **Zero-order** | META-ORGANVM (Organ 0) | Constitution, schema, registry, migration, era-change |
| **First-order** | ORGAN-IV / Taxis | Routing, orchestration, promotion, enforcement, coupling |
| **Domain** | Organs I-VII | Substantive domains under constitutional/orchestral constraints |

### Organ Sequence (Era 1)

The numbering encodes the logical sequence through which the institution comes into being:

**0 (Meta)** — constitutional substrate → **I (Theoria)** — conceptual generation → **II (Poiesis)** — creative bringing-forth → **III (Ergon)** — practical embodiment → **IV (Taxis)** — systemic coordination → **V (Logos)** — reflective articulation → **VI (Koinonia)** — communal participation → **VII (Kerygma)** — outward proclamation

This progression: **constitution → thought → creation → work → coordination → articulation → community → proclamation** expresses the full lifecycle through which a single practitioner operates with institutional coherence and reach.

### VSM Mapping (Era 1)

| Beer's System | ORGANVM Mapping |
|---------------|----------------|
| System 1 (Operations) | Organs I-VII |
| System 2 (Coordination) | Distributed: seed.yaml contracts, schema-definitions, dependency DAG |
| System 3 (Inside-and-now) | ORGAN-IV (Taxis) — governance enforcement |
| System 4 (Outside-and-future) | ORGAN-IV (Taxis) — ecosystem module, Living Data Organism |
| System 5 (Identity/ethos) | META-ORGANVM — constitution, registry, schemas |

Known viability risk: S3/S4 conflated in Taxis. Per Beer's diagnostic criteria, these should be structurally separate. This may be the first governed topological mutation.

---

## 6. Primitives

The irreducible conceptual units of the system are defined in SPEC-002 (Primitive Register). SPEC-000 declares their existence without exhaustively defining them:

**Entity** — a thing that exists with persistent identity
**Value** — a datum attached to an entity
**Relation** — a typed connection between entities
**Event** — a state change with timestamp and causation
**State** — the current configuration of an entity's values
**Constraint** — a rule limiting what states or transitions are lawful
**Capability** — an operation an entity may perform

Every organ, repository, formation, signal, governance rule, metric, and agent is a composition of these primitives.

---

## 7. Invariants

The following truths must remain valid across all versions, eras, and topological mutations. SPEC-000 *declares* invariants (prose definitions with constitutional authority for intent). SPEC-003 (Invariant Register) *formalizes* them (machine-checkable definitions with authority for formal semantics). When prose and formalization diverge, the prose is authoritative for intent; the formalization is authoritative for enforcement.

**INV-000-001: Dependency Acyclicity.** The dependency graph G^dep must be a directed acyclic graph at all times.

**INV-000-002: Governance Reachability.** For every active component, there must exist a path from a constitutional root to that component in G^gov. Constitutional roots are the set of entities with registry_key META-ORGANVM (the zero-order constitutional substrate).

**INV-000-003: Identity Persistence.** No entity's canonical identity (UID) may be destroyed. Entities may be archived, dissolved, merged, or split, but their identity and lineage must be preserved.

**INV-000-004: Constitutional Supremacy.** No lower-level rule (organ dictum, repo rule, agent action) may override a higher-level constitutional constraint (axiom, invariant, spec).

**INV-000-005: Observability.** The system must be capable of accurately reporting its own state — every active component's status, every active relation's type, every active metric's value — through its own diagnostic instruments. Reports must reflect current system state; a diagnostic instrument that returns stale, hardcoded, or fabricated data violates this invariant.

---

## 8. Failure Modes

The following conditions constitute violations of SPEC-000:

| Failure | Violated Axiom/Invariant | Detection |
|---------|------------------------|-----------|
| Ungoverned component (repo without seed.yaml, unregistered entity) | AX-000-004, INV-000-002 | `organvm governance audit` |
| Circular dependency | INV-000-001 | `organvm governance check-deps` |
| Identity destruction (UID deleted without lineage) | INV-000-003, AX-000-007 | Ontologia integrity check |
| Rule change without governed process | AX-000-005 | Git history audit of governance-rules.json |
| Topology change without constitutional revision | AX-000-006 | Manual review (not yet automated) |
| Undeclared inter-organ signal flow | AX-000-008, AX-000-009 | Not yet automated (SPEC-007 target) |
| System optimization overriding individual autonomy | AX-000-003 | Manual review (value judgment) |
| Unobservable component (no metrics, no status) | INV-000-005 | `organvm organism` gate checks |

---

## 9. Evolution Constraints

SPEC-000 may be amended through the following governed process only. This process is self-contained — it does not depend on any downstream spec for its authority. Future specs (particularly SPEC-008 and SPEC-011) may extend or refine this process, but the core amendment procedure defined here is sufficient and operative from the moment of ratification.

1. A revision proposal must cite specific evidence (research finding, implementation discovery, or structural interrogation result) demonstrating that the current manifesto is insufficient or incorrect
2. The proposal must classify its change as Conservative Refinement (adds detail, preserves meaning), Constrained Extension (adds scope, preserves invariants), or Breaking Revision (changes semantics)
3. Conservative Refinements require: adversarial review by a different agent/model + creator sign-off
4. Constrained Extensions require: (a) adversarial review, (b) impact assessment on downstream specs, (c) creator sign-off
5. Breaking Revisions require: (a) a new grounding narrative addressing the change, (b) adversarial review by a different agent/model, (c) human spot-check of cited sources, (d) explicit creator sign-off, (e) review of all downstream specs for consistency
6. The original SPEC-000 is never overwritten — amendments are versioned addenda (SPEC-000-v1.1, v1.2, etc.)
7. All amendment proposals, reviews, and sign-offs are recorded in the PHASE-STATE tracking system

---

## 10. Traceability

This specification is the root of the traceability ladder. All downstream specs trace to elements defined here:

```
SPEC-000 (this document)
├── AX-000-001 through AX-000-009 → referenced by all downstream specs
├── INV-000-001 through INV-000-005 → validated by SPEC-003
├── Primitives → defined by SPEC-002
├── Constitutional topology → formalized by SPEC-006
├── Evolution constraints → implemented by SPEC-008, SPEC-011
└── Failure modes → detected by SPEC-009
```

### Academic Lineage

Every axiom traces to its academic grounding:

| Axiom | Traditions | Key Sources |
|-------|-----------|-------------|
| AX-001 | Formal ontology | Guarino 1998, Smith 2004 |
| AX-002 | Autopoiesis, social systems | Maturana & Varela 1980, Luhmann 1995 |
| AX-003 | (Novel) | Ethical architectural commitment |
| AX-004 | Institutional design | Ostrom 1990, Crawford & Ostrom 1995, Beer 1972 |
| AX-005 | Cybernetics | Ashby 1952, von Foerster 1981 |
| AX-006 | Systems evolution | Luhmann 1995, Kauffman 1993, Gersick 1991 |
| AX-007 | (Novel) | North 1990, Ashby 1952, alchemical tradition |
| AX-008 | Network science | Newman 2018, Boccaletti 2006, Beer 1972 |
| AX-009 | Cybernetics, ANT | Beer 1972, Ashby 1956, Callon 1986 |

Full bibliography: `post-flood/specs/bibliography.bib` (40+ entries)
Full grounding narrative: `post-flood/specs/SPEC-000/grounding.md` (8,100+ words)
Full risk register: `post-flood/specs/SPEC-000/risk-register.md` (22 classified claims)
Current state inventory: `post-flood/specs/SPEC-000/inventory.md` (9 axiom alignment assessments)
