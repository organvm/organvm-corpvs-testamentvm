# SPEC-006: Architecture Document

```
Document ID:      SPEC-006
Title:            Architecture Document
Version:          1.0
Status:           RATIFIED
Layer:            L3A — Structural Architecture
Authoritative:    System Structure
Parent Specs:     SPEC-000 (System Manifesto), SPEC-001 (Ontology Charter), SPEC-002 (Primitive Register), SPEC-003 (Invariant Register)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/SPEC-006/grounding.md
Risk Register:    post-flood/specs/SPEC-006/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. The 7-Layer Module Stack

ORGANVM's architecture is a seven-layer stack where each layer provides services to the layers above and depends only on the layers below. The layering is the structural realization of Simon's near-decomposable hierarchies (1962): each layer is a stable intermediate subsystem that can evolve independently as long as it preserves its interface to adjacent layers. Each layer hides design decisions from the layers above (Parnas 1972).

### ARCH-001: Constitutional Substrate

**Layer 1 — Design Rules.**

The constitutional substrate consists of the SPEC corpus, `repo-registry.json`, and `governance-rules.json`. These are the visible design parameters in Baldwin and Clark's (2000) vocabulary — the constraints that bind all downstream modules. Every other layer depends on the constitutional substrate; the substrate depends on nothing within the system.

**Contents:** SPEC-000 through SPEC-017, `repo-registry.json` (source of truth for all repos), `governance-rules.json` (promotion criteria, organ dictums, dependency rules), the post-flood corpus (constitutional source narratives).

**Hides:** The specific format of governance documents, the prose structure of SPEC narratives, the versioning history of constitutional amendments. Upper layers interact with the substrate through the engine's registry and governance APIs, not through direct file reads.

**Traces to:** AX-000-004 (Constitutional Governance), INV-000-004 (Constitutional Supremacy).

### ARCH-002: Schema Layer

**Layer 2 — Data Contracts.**

The schema layer (`schema-definitions/`) defines the data contracts shared across the system. Six JSON Schemas — registry-v2, seed-v1, governance-rules, dispatch-payload, soak-test, system-metrics — plus the ontologia schemas (entity-identity, name-record, ontologia-event) constitute the type system governing all inter-layer data exchange.

**Contents:** Canonical JSON Schemas in `schema-definitions/schemas/`, validation scripts, schema examples.

**Hides:** The specific JSON Schema dialect and validation library. Upper layers interact with schemas through validation functions, not through direct schema file inspection.

**Dependency:** Constrained by ARCH-001 (schemas must conform to constitutional definitions of valid data structures).

**Traces to:** AX-000-008 (Multiplex Flow Governance — schemas define the types carried by each flow), INV-000-001 (the registry schema enforces the dependency-edge structure that the DAG validator checks).

### ARCH-003: Engine Layer

**Layer 3 — Governance Execution.**

The engine layer (`organvm-engine/`) is the governance execution machinery: registry operations, promotion transitions, governance audit, metrics computation, dependency validation, seed discovery, context-sync, and CLI interface. The engine is the central mediator between constitutional intent (ARCH-001) and system state.

**Contents:** 21 domain modules + 4 foundation modules in `src/organvm_engine/`. CLI package with 23 command modules. 1937+ tests.

**Hides:** The implementation of governance algorithms (audit traversal, metric propagation, dependency graph construction, statechart evaluation). Upper layers invoke engine functions through the CLI or Python API; they do not import internal governance logic.

**Dependency:** Reads schemas from ARCH-002 for validation. Reads registry and governance rules from ARCH-001 for state.

**Traces to:** AX-000-002 (Organizational Closure — the engine is a constitutive process specified by constitutional rules), AX-000-005 (Evolutionary Recursivity — the engine evaluates rules that govern the engine's own evolution).

### ARCH-004: Identity Layer

**Layer 4 — Entity Registry.**

The identity layer (`organvm-ontologia/`) provides the ULID-based entity registry: persistent identity, name records, hierarchy edges, lifecycle events, and temporal naming. The identity layer reifies the three-scale decomposition (system, organ, repo) into machine-visible entity relationships.

**Contents:** 44 source files, 353 tests. Store at `~/.organvm/ontologia/` (entities.json, names.jsonl, events.jsonl). 179 bootstrapped entities (8 organs + 113 repos + 58 modules).

**Hides:** The specific storage format (JSON/JSONL), the ULID generation algorithm, the hierarchy edge data structure. Upper layers resolve entities through `resolve_entity(name_or_uid, registry)` without knowledge of the store's internal layout.

**Dependency:** Bootstraps from ARCH-001 (`repo-registry.json`). Uses ARCH-002 schemas for entity validation.

**Traces to:** AX-000-007 (Alchemical Inheritance — lineage records preserve structural history), INV-000-003 (Identity Persistence — the append-only store enforces UID monotonicity).

### ARCH-005: Orchestration Layer

**Layer 5 — Routing and Observation.**

The orchestration layer consists of the Conductor MCP server (ORGAN-IV/Taxis) and the ORGANVM MCP server (`organvm-mcp-server/`). The Conductor routes tasks to agent sessions, enforces the FRAME-SHAPE-BUILD-PROVE lifecycle, and manages cross-agent handoffs. The MCP server exposes the full system graph — registry, seeds, governance, metrics, organism state — to every agent session through 88 tools in 16 groups.

**Contents:** Conductor (tool-interaction-design in ORGAN-IV). MCP server: 207+ tests, 88 tools, stdio transport.

**Hides:** The agent communication protocol, the session lifecycle state machine, the tool dispatch table. Application-layer repos interact with the orchestration layer by declaring `produces`/`consumes` edges in seed.yaml and registering event subscriptions; they do not invoke orchestration internals directly.

**Dependency:** Imports from ARCH-003 (engine registry, governance, seed functions). Reads from ARCH-004 (entity resolution for cross-repo awareness).

**Traces to:** AX-000-008 (Multiplex Flow Governance — the MCP server exposes all five graph layers), INV-000-005 (Observability — the MCP server and dashboard are the primary diagnostic instruments).

### ARCH-006: Application Layer

**Layer 6 — Substantive Work.**

The application layer comprises all repos across Organs I through VII — the substantive creative, productive, governance, and communicative work of the system. Each application-layer repo is an independent component in Szyperski's (2002) sense: contractually specified interfaces (seed.yaml), explicit context dependencies (consumes field), and independent deployability (own CI, own promotion status, own git history).

**Contents:** 112 repos across 8 organs, organized by functional domain. Tier hierarchy: flagship, standard, infrastructure.

**Hides:** Each repo's internal implementation. Inter-repo interaction is mediated by seed.yaml contracts and schema-validated event payloads. No repo may import another repo's internal modules without declaring the dependency.

**Dependency:** Governed by ARCH-003 (engine enforces promotion, audit, dependency rules). Identity tracked by ARCH-004. Orchestrated by ARCH-005.

**Traces to:** AX-000-004 (Constitutional Governance — every repo requires seed.yaml), AX-000-006 (Topological Plasticity — the organ structure is the first-era instantiation of the application topology).

### ARCH-007: Interface Layer

**Layer 7 — External Presentation.**

The interface layer provides external-facing views of the system: the system dashboard (`system-dashboard/`), the stakeholder portal (`stakeholder-portal/`), kerygma distribution profiles, and pitch decks. Interface-layer components are consumers of system state; they do not mutate governance data.

**Contents:** FastAPI + Jinja2 + HTMX dashboard (62 tests, routes: /health/, /registry/, /graph/, /soak/, /essays/, /omega/, /ontologia/). Next.js stakeholder portal. 83 HTML pitch decks. 23 kerygma profiles.

**Hides:** Presentation format (HTML, JSON API), rendering technology (Jinja2, React), deployment platform (Vercel, local). The interface layer is a pure read-only consumer of the engine and organism APIs.

**Dependency:** Reads from ARCH-003 (registry, metrics, organism state). Reads from ARCH-004 (entity browsing). Routed through ARCH-005 (MCP tools for portal AI chat).

**Traces to:** INV-000-005 (Observability — the dashboard and portal are the primary human-facing diagnostic instruments).

---

## 2. Near-Decomposability Analysis

ORGANVM exhibits near-decomposability at three nested scales, each following Simon's (1962) pattern of strong internal coupling and weak external coupling.

### ARCH-010: System-Level Near-Decomposability

At the system level, organs are the intermediate subsystems. Intra-organ coupling is dense: repos within an organ share aesthetic identity (`organ-aesthetic.yaml`), governance dictums (organ-specific rules in `governance-rules.json`), event namespaces, and dependency edges. Inter-organ coupling is sparse and governed: the unidirectional dependency rule (I to II to III, no back-edges) restricts the dependency graph, while cross-organ communication is mediated by declared `produces`/`consumes` edges in seed.yaml.

The constitutional topology — Production Core (I-III), Control Plane (IV), Interface Layer (V-VII), Meta (zero-order substrate) — maps to Simon's nested hierarchy: three functional groups with qualitatively different coupling patterns.

### ARCH-011: Organ-Level Near-Decomposability

Within each organ, repos are the intermediate subsystems. Repos share tier hierarchies, CI patterns, and internal dependency edges, but maintain independent CI workflows, independent promotion statuses, and independent test suites. Each repo is a stable intermediate form: it can be independently developed, tested, promoted, and archived without destabilizing sibling repos.

### ARCH-012: Repo-Level Near-Decomposability

Within repos, modules are the intermediate subsystems. The excavation engine identified 58 sub-packages across the workspace exhibiting strong intra-module coupling (shared imports, shared data structures) and weak inter-module coupling (limited cross-module imports, clean interface boundaries). The module bridge reifies this scale by creating MODULE entities in ontologia with hierarchy edges from parent repos.

### ARCH-013: Multiplex Near-Decomposability (NOVEL)

Near-decomposability operates differently across the five edge types defined by AX-000-008. This is SPEC-006's novel finding: "coupling" is not a single-valued architectural property but a vector across graph layers.

| Graph Layer | Coupling Pattern | Near-Decomposability |
|-------------|-----------------|---------------------|
| **G^dep** (Dependency) | Sparse, unidirectional | Strongly near-decomposable. Intra-organ dense, inter-organ sparse and DAG-constrained. |
| **G^info** (Information) | Dense, recursively cyclic | Deliberately NOT near-decomposable. Context-sync, MCP server, and Living Data Organism create system-wide information flow. |
| **G^gov** (Governance) | Hub-and-spoke from META | Hub-decomposable. Strong internal organ governance; weak inter-organ governance coupling mediated by registry and promotion state machine. |
| **G^evo** (Evolution) | Time-monotonic | Lineage-decomposable. Each entity's evolution is primarily independent; cross-entity evolution coupling occurs only at era transitions. |
| **G^mod** (Signal) | Type-compatible, attenuated | Pattern-decomposable. Signal coupling follows formation type constraints; prohibited couplings prevent structural entanglement. |

The architectural consequence: optimizing for one coupling dimension may degrade another. The unidirectional dependency rule produces excellent dependency decoupling but says nothing about information coupling. The context-sync mechanism produces excellent information coupling but could create governance confusion if cross-organ awareness is mistaken for cross-organ authority.

**Traces to:** AX-000-008 (Multiplex Flow Governance — "the dependency graph must be acyclic, but the information graph must be recursively cyclic").

---

## 3. Conway's Law Mapping

### ARCH-020: Organizational Homomorphism

Conway's law (1968) states that system structure mirrors organizational communication structure. ORGANVM presents a distinctive case: the "organization" is a single operator with AI agents, not a multi-person team. The homomorphism still holds through the conductor-agent communication topology.

**Cognitive domain mapping.** The eight organs correspond to the operator's cognitive domains: theory (I), art (II), commerce (III), governance (IV), discourse (V), community (VI), distribution (VII), meta (0). Organ boundaries are cognitive boundaries as much as functional ones.

**Agent topology mapping.** Agent sessions are scoped per organ; cross-organ work requires explicit handoff protocols (`SOP--cross-agent-handoff.md`). The Conductor MCP server is the communication structure made architectural: its routing topology determines which agents communicate about which concerns.

### ARCH-021: Inverse Conway Maneuver

ORGANVM employs the inverse Conway maneuver deliberately: the desired organ structure was specified first (in the post-flood constitutional corpus), and the agent topology was shaped to match. This is intentional architectural design, not emergent organizational coupling.

**Risk.** Conway identifies organizational disintegration under overpopulation. ORGANVM faces the opposite risk: organizational *constriction* — a single operator cannot attend to all organs simultaneously, creating temporal near-decomposability (the operator works on one organ at a time) in addition to structural near-decomposability. The Conductor's FRAME phase is the architectural counter-measure: it forces cross-organ awareness before organ-specific BUILD work begins.

**Traces to:** AX-000-002 (Organizational Closure — the communication structure is itself a constitutive process).

---

## 4. Quality Attribute Scenarios

Following Bass, Clements, and Kazman (2012), ORGANVM's architectural quality attributes are documented through six-part scenarios. The framework is ADAPTED from runtime software architecture to governance architecture: quality attributes of interest are modifiability, testability, interoperability, observability, and evolutionary capacity — not latency and throughput.

### ARCH-030: Modifiability

**Scenario.** Stimulus: a new product repo is added to ORGAN-III. Source: human operator. Environment: normal operation. Artifact: ORGAN-III registry section, new repo's seed.yaml, ORGAN-III dependency subgraph. Response: the addition is absorbed by creating seed.yaml, registering in repo-registry.json, bootstrapping in ontologia. Response measure: no modification required to any existing repo's seed.yaml, no modification required to any other organ's registry section, no governance audit finding generated that was not already present.

**Supporting tactics:** Information hiding (the new repo is hidden behind its seed.yaml interface), modular decomposition (the organ boundary contains the change scope), design-time binding (seed.yaml contract is established at creation).

### ARCH-031: Testability

**Scenario.** Stimulus: governance audit detects a potential invariant violation. Source: engine audit subsystem. Environment: CI pipeline or manual invocation. Artifact: invariant register and registry. Response: structured audit finding with (a) which invariant is violated, (b) which entity is in violation, (c) causal trace from entity state to violation condition. Response measure: the finding is actionable without reading engine source code.

**Supporting tactics:** Invariant formalization as Hoare triples (SPEC-003), structured evaluation output (SPEC-005 Section 4.4), per-repo CI independence (2700+ tests across subprojects).

### ARCH-032: Interoperability

**Scenario.** Stimulus: a repo in ORGAN-III needs to consume events produced by a repo in ORGAN-II. Source: developer declaring consumes edge. Environment: seed.yaml modification. Artifact: both repos' seed.yaml files, schema-definitions dispatch-payload schema. Response: seed graph validator confirms the edge is type-compatible, dependency graph validator confirms no cycle is created. Response measure: the cross-organ flow is operational within one seed-discovery cycle.

**Supporting tactics:** Shared schemas (ARCH-002), typed signal classes (SPEC-007), DAG validation (INV-000-001).

### ARCH-033: Observability

**Scenario.** Stimulus: the operator requests system-wide health assessment. Source: human principal via CLI or dashboard. Environment: normal operation. Artifact: Living Data Organism, organism state model. Response: the organism computes per-organ density, per-repo gate evaluations, and overall affective state (thriving/coherent/strained/brittle). Response measure: every active component's status is reflected; no stale or fabricated data.

**Supporting tactics:** INV-000-005 (Observability invariant), gate evaluation in `metrics/organism.py`, AMMOI compressed summary, dashboard + MCP server as dual diagnostic interfaces.

### ARCH-034: Evolutionary Capacity

**Scenario.** Stimulus: the operator determines the eight-organ topology should gain a ninth organ. Source: governed constitutional revision (SPEC-000 Section 9). Environment: era transition. Artifact: `organ_config.py`, `repo-registry.json`, `governance-rules.json`, all seed.yaml files referencing organ taxonomy. Response: topology change enacted through constitutional revision proposal, organ_config update, registry extension, governance-rules extension, seed.yaml updates. Response measure: no invariant violated during transition; AMMOI summary reflects new topology within one metric refresh cycle.

**Architectural debt disclosure:** The architecture *partially* supports this scenario. Data structures accommodate extension (registry keyed by organ, adding a key is trivial). However, the hardcoding in `organ_config.py` violates AX-000-006 and requires code modification rather than configuration change. This is the most significant architectural debt.

**Traces to:** AX-000-006 (Topological Plasticity), AX-000-006 (Topological Plasticity).

---

## 5. Architectural Constraints

### ARCH-040: Unidirectional Dependency Flow

The inter-organ dependency graph must form a DAG with the ordering: I to II to III. No back-edges. ORGAN-IV orchestrates all. ORGAN-V observes (read-many-write-one). ORGAN-VII is a pure consumer.

**Source:** INV-000-001 (Dependency Acyclicity), AX-000-008 (Multiplex Flow Governance).

**Enforcement:** `governance/dependency_graph.py::validate_dag_invariant()` performs DFS cycle detection on every registry load.

### ARCH-041: Seed Contract Boundary

Every inter-component interface passes through the seed.yaml contract. No component may access another component's internal structure without declared dependency. The seed.yaml is the Parnas information-hiding boundary reified as a file.

**Source:** AX-000-004 (Constitutional Governance), RULE-014 (Seed Contract Mandate).

**Enforcement:** `organvm governance audit` detects repos without seed.yaml. Undeclared cross-organ flows violate RULE-002 (Epistemic Membranes).

### ARCH-042: Layered Dependency

Dependencies between the seven layers of the module stack (ARCH-001 through ARCH-007) must be downward-only. No lower layer may depend on a higher layer. The schema layer (ARCH-002) does not import from the engine (ARCH-003). The engine does not import from the dashboard (ARCH-007).

**Source:** Simon 1962 (hierarchical decomposition preserves near-decomposability only when inter-layer coupling is unidirectional).

**Enforcement:** Python import structure and `pyproject.toml` dependency declarations. Not currently validated by automated tooling.

### ARCH-043: Constitutional Orthogonality

META-ORGANVM (Organ 0) is orthogonal to the Production Core / Control Plane / Interface Layer hierarchy. Meta constrains all other layers without being in their dependency chain. This is structurally closer to a constitutional court model than a software layering model.

**Source:** SPEC-000 Section 5 (Authority Stack — zero-order, first-order, domain).

**Contestation:** Standard layered architectures have linear dependency (layer N depends on layer N-1). ORGANVM's topology has Meta as an orthogonal constitutional layer. The architectural soundness rests on whether orthogonal authority can be enforced without creating hidden coupling.

---

## 6. Contestation Disclosures

### 6.1 Quality Attribute Framework Adaptation

**Status:** ADAPTED (risk register).

Bass, Clements, and Kazman's quality attribute scenarios were designed for runtime software systems. SPEC-006 applies them to a governance architecture with both software and documentary components. The quality attributes of interest — modifiability, testability, evolutionary capacity — differ from the original framework's emphasis on latency, throughput, and availability. The structural apparatus (scenario format, tactic identification, view decomposition) transfers; the specific quality attribute inventory does not.

### 6.2 Conway's Law in Single-Operator Systems

**Status:** ADAPTED (risk register).

Conway's law was formulated for multi-person design organizations. In a single-operator + AI-agent system, the "organization" is the conductor-agent session topology. The law still predicts system-structure-mirrors-communication-structure, but the communication structure is cognitive rather than organizational. The inverse Conway maneuver (designing agent topology to match desired system structure) is deliberate but untested at ORGANVM's scale.

### 6.3 Meta as Zero-Order Substrate

**Status:** ADAPTED (risk register).

The three-layer constitutional topology with Meta as orthogonal zero-order substrate has no direct precedent in the software architecture literature. Standard layered architectures have linear dependency. ORGANVM's topology combines hierarchical layering with orthogonal constitutional authority. The primary risk is that orthogonal authority creates hidden coupling paths not visible in the dependency graph.

### 6.4 Multiplex Near-Decomposability

**Status:** NOVEL (risk register).

The finding that near-decomposability operates differently across different edge types on the same vertex set — producing a coupling vector rather than a coupling scalar — is a novel analytical contribution without direct precedent. The finding emerges from applying Simon's framework to a system with AX-000-008's multiplex graph structure. It is an empirical observation about ORGANVM's architecture, not a contested theoretical claim.

---

## 7. Evolution Constraints

SPEC-006 may be amended through the following governed process only.

### 7.1 Amendment Types

| Type | Definition | Requirements |
|------|-----------|-------------|
| **Conservative Refinement** | Adds architectural detail without changing the layer topology or constraint set. Examples: refining a quality attribute scenario, adding a near-decomposability observation. | Adversarial review + creator sign-off |
| **Constrained Extension** | Adds new layers, new architectural constraints (new ARCH-NNN identifiers), or new quality attribute scenarios. Must preserve all existing layer dependencies and constraints. | Adversarial review + impact assessment on SPEC-007 (Interface Contract Spec) and SPEC-008 (Evolution Law) + creator sign-off |
| **Breaking Revision** | Changes layer topology (merging, splitting, or reordering layers), changes dependency direction between layers, or modifies architectural constraints in ways that invalidate existing decomposition. | New grounding narrative + adversarial review + human spot-check + review of all downstream specs + creator sign-off |

### 7.2 Permanent Identifiers

ARCH identifiers (ARCH-001 through ARCH-043) are permanent. Removed items have their identifiers retired, not reassigned.

### 7.3 Versioning

The original SPEC-006 is never overwritten. Amendments are versioned: SPEC-006-v1.1, v1.2, etc.

---

## 8. Traceability

### 8.1 Upward Traceability (to SPEC-000)

| SPEC-000 Element | SPEC-006 Grounding |
|------------------|--------------------|
| AX-000-001 (Ontological Primacy) | ARCH-004 — identity layer defines what exists before orchestration layer defines behavior |
| AX-000-002 (Organizational Closure) | ARCH-003 — engine is itself a constitutive process specified by constitutional rules |
| AX-000-004 (Constitutional Governance) | ARCH-001 — constitutional substrate is the foundational layer; ARCH-041 — seed contract boundary |
| AX-000-005 (Evolutionary Recursivity) | Section 7 — the architecture document itself evolves through governed revision |
| AX-000-006 (Topological Plasticity) | ARCH-034 — evolutionary capacity scenario; architectural debt disclosure |
| AX-000-007 (Alchemical Inheritance) | ARCH-004 — identity layer preserves lineage through hierarchy edges |
| AX-000-008 (Multiplex Flow Governance) | ARCH-013 — multiplex near-decomposability analysis across five graph layers |
| AX-000-009 (Modular Alchemical Synthesis) | ARCH-012 — repo-level near-decomposability via 58 identified modules |
| INV-000-001 (Dependency Acyclicity) | ARCH-040 — unidirectional dependency flow constraint |
| INV-000-002 (Governance Reachability) | ARCH-043 — META orthogonality ensures governance path to all organs |
| INV-000-003 (Identity Persistence) | ARCH-004 — ontologia store is structurally append-only |
| INV-000-004 (Constitutional Supremacy) | ARCH-001 — constitutional substrate at the base of the layer stack |
| INV-000-005 (Observability) | ARCH-033 — observability quality attribute scenario |

### 8.2 Lateral Traceability

| Peer Spec | Connection |
|-----------|-----------|
| SPEC-001 (Ontology Charter) | ONT-004/005/006 (ORGAN/REPO/MODULE) are the entity types at the three near-decomposability scales |
| SPEC-002 (Primitive Register) | Architectural layers are CompositeObjects (Section 2.2) composed of primitives |
| SPEC-003 (Invariant Register) | ARCH-040/041/042/043 operationalize INV-000-001/002/004/005 at the architectural level |
| SPEC-004 (Logical Specification) | Promotion statechart operates within the engine layer (ARCH-003) |
| SPEC-005 (Rulebook) | RULE-001 through RULE-018 enforce architectural constraints within the engine's evaluation cycle |

### 8.3 Downward Traceability (to implementation)

| SPEC-006 Element | Current Code Location | Alignment |
|------------------|-----------------------|-----------|
| 7-layer module stack (Section 1) | Physical directory structure across submodules | ALIGNED (structural) |
| Near-decomposability (Section 2) | `governance/dependency_graph.py` (G^dep only) | DRIFT — only dependency layer tracked |
| Conway's Law mapping (Section 3) | Conductor session scoping, `SOP--cross-agent-handoff.md` | ALIGNED (procedural) |
| Quality attribute scenarios (Section 4) | Scattered across engine, dashboard, MCP server | PARTIAL — no formal scenario documentation |
| Unidirectional dependency (ARCH-040) | `governance/dependency_graph.py::validate_dag_invariant()` | ALIGNED |
| Seed contract boundary (ARCH-041) | `organvm governance audit`, `seed/discover.py` | ALIGNED |
| Layered dependency (ARCH-042) | Python import structure, `pyproject.toml` | DRIFT — not validated by tooling |
| Constitutional orthogonality (ARCH-043) | `organ_config.py` (hardcoded) | DRIFT — AX-000-006 conflict |

### 8.4 Academic Lineage

| SPEC-006 Element | Traditions | Key Sources |
|------------------|-----------|-------------|
| 7-layer module stack | Hierarchical systems theory, information hiding | Simon 1962, Parnas 1972 |
| Near-decomposability analysis | Complexity science | Simon 1962 |
| Modularity operators | Design theory, economics | Baldwin & Clark 2000 |
| Conway's Law mapping | Organizational homomorphism | Conway 1968 |
| Quality attribute scenarios | Software architecture practice | Bass, Clements & Kazman 2012 |
| Multiplex near-decomposability | Novel (grounded in AX-000-008) | — |

Full grounding narrative: `post-flood/specs/SPEC-006/grounding.md` (4,540 words)
Full risk register: `post-flood/specs/SPEC-006/risk-register.md` (6 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
