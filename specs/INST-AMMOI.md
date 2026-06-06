# INST-AMMOI: AMMOI Reconciliation

```
Document ID:      INST-AMMOI
Title:            AMMOI Reconciliation
Version:          1.0
Status:           RATIFIED
Layer:            L4B — Diagnosis & Meta-Evolution
Authoritative:    Six-Layer Ontological Index Coherence
Parent Specs:     SPEC-000 (System Manifesto), SPEC-001 (Ontology Charter)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/ammoi-reconciliation/grounding.md
Risk Register:    post-flood/specs/ammoi-reconciliation/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. AMMOI Definition

AMMOI -- the Adaptive Macro-Micro Ontological Index -- is a recursively self-revising ontological graph anchored by hierarchical containment, enriched by lateral relations, animated by event-driven state comparison, and governed by adaptive policies that preserve identity continuity while permitting structural and semantic evolution.

AMMOI reconciliation is the process by which the six-layer index maintains coherence: when a change occurs at one layer, the effects propagate correctly to all other layers. An ontological index that does not reconcile its layers is not an index but a collection.

The architecture draws on Boisot and Child's (1999) Information Space (I-Space) model, which provides the codification-abstraction-diffusion framework for analyzing knowledge flows and the dual-strategy model (complexity reduction vs. complexity absorption) for managing internal variety.

**Risk profile: 20% GROUNDED, 60% ADAPTED, 20% NOVEL.**

---

## 2. Six Coupled Layers

### AMMOI-001: Identity Layer

**I-Space position:** High codification, high abstraction, high diffusibility.
**Content:** ULID-based entity identifiers. Each entity in ORGANVM has exactly one UID that persists across all mutations (INV-000-003).
**Reconciliation responsibility:** When a new entity is created in any other layer, the Identity layer must assign a UID. When an entity is dissolved, the UID persists in the historical record.

**Implementation:** `organvm-ontologia/` -- `entity/identity.py` (EntityIdentity, ULID generation), `store/store.py` (append-only entity store).

### AMMOI-002: Hierarchy Layer

**I-Space position:** High codification, moderate abstraction, moderate diffusibility.
**Content:** Containment edges defining the organ-repo-module tree. Each repo belongs to exactly one organ. Each module belongs to exactly one repo.
**Reconciliation responsibility:** When a repo is added or moved, the Hierarchy layer must update the containment tree. When an organ boundary changes (era transition per INST-ERA), the Hierarchy layer must restructure all affected containment edges.

**Implementation:** `organvm-ontologia/` -- `structure/hierarchy.py` (ContainmentEdge), `governance/module_bridge.py` (module entity creation).

### AMMOI-003: Relation Layer

**I-Space position:** Moderate codification, moderate abstraction, moderate diffusibility.
**Content:** Lateral typed edges: `produces`, `consumes`, `subscribes`, dependency edges, governance edges, evolution edges. The five edge families defined in SPEC-000 AX-000-008.
**Reconciliation responsibility:** When a relation edge is added or removed, the Relation layer must check consistency with the Hierarchy (edge endpoints must exist), the State (edge must be compatible with both endpoints' promotion states), and the Governance (edge must respect dependency direction and constitutional constraints).

**Implementation:** `organvm-engine/` -- `seed/graph.py` (produces/consumes edges), `governance/dependency_graph.py` (dependency edges).

### AMMOI-004: State Layer

**I-Space position:** Moderate codification, low abstraction, low diffusibility.
**Content:** Current promotion state, implementation status, CI status, metric values, and all other mutable properties of each entity.
**Reconciliation responsibility:** When state changes (promotion, metric update), the State layer must check governance constraints (is this transition valid?) and emit an event to the Event layer. When a governance rule changes, the State layer must reassess all affected entities.

**Implementation:** `organvm-engine/` -- `registry/` (repo state), `governance/state_machine.py` (promotion transitions), `metrics/` (metric observations).

### AMMOI-005: Event Layer

**I-Space position:** Low codification, low abstraction, low diffusibility.
**Content:** Append-only record of every state mutation with timestamp, causation, and payload (INST-EVENT-SPINE).
**Reconciliation responsibility:** When any other layer changes, the Event layer must record the change as an immutable event. Events are never modified or deleted. The Event layer is the constitutional memory of the system.

**Implementation:** MISSING. Currently, state mutations are applied directly to repo-registry.json without event recording. Target: INST-EVENT-SPINE implementation.

### AMMOI-006: Governance Layer

**I-Space position:** High codification, high abstraction, low diffusibility.
**Content:** Constitutional constraints (invariants, axioms), governance rules (promotion criteria, dependency constraints), policies (soak-test parameters, escalation thresholds).
**Reconciliation responsibility:** When governance rules change (meta-evolution per SPEC-011), the Governance layer must propagate the change to the State layer (re-evaluate all entities) and the Relation layer (re-check all edges). Governance changes are the highest-impact reconciliation trigger.

**Implementation:** `organvm-engine/` -- `governance/rules.py` (governance rules), `governance/audit.py` (compliance checking). `organvm-corpvs-testamentvm/governance-rules.json` (rule definitions).

---

## 3. Reconciliation Mechanisms

### AMMOI-007: Vertical Propagation

Vertical propagation maintains coherence between layers in the codification gradient. Changes flow from high-codification layers (Identity, Hierarchy) downward to low-codification layers (State, Event).

| Trigger | Propagation Path |
|---------|-----------------|
| Entity creation | Identity (assign UID) -> Hierarchy (assign containment) -> State (set initial state) -> Event (record creation) |
| Entity archival | State (set ARCHIVED) -> Event (record archival) -> Identity (UID preserved) |
| Entity rename | Identity (UID unchanged) -> Hierarchy (containment unchanged) -> State (name record updated) -> Event (record rename) |

### AMMOI-008: Horizontal Propagation

Horizontal propagation maintains coherence between layers at the same codification level. Changes at one layer trigger consistency checks at adjacent layers.

| Trigger | Horizontal Check |
|---------|-----------------|
| Relation edge added | State: are both endpoints compatible? (GRADUATED should not depend on LOCAL) |
| Relation edge added | Governance: does this edge respect dependency direction? |
| State change (promotion) | Relation: are all dependency prerequisites satisfied at the new state? |
| State change (promotion) | Governance: does the entity satisfy the target state's criteria? |

### AMMOI-009: Circular Propagation (Sense Cycle)

Circular propagation implements the AMMOI sense cycle -- the recursive loop through which the system refines its self-model:

| Phase | Operation | Layer(s) |
|-------|-----------|----------|
| **Observe** | Read current state from sensors and data sources | State, Event |
| **Normalise** | Map observations to the ontological schema | Identity, Hierarchy |
| **Compare** | Diff current state against previous state | State (temporal comparison) |
| **Infer** | Apply inference rules to derive governance conclusions | Governance |
| **Decide** | Select governance action based on conclusions | Governance |
| **Revise** | Update the ontological model (state, structure, or categories) | State, Hierarchy, or Identity |
| **Propagate** | Push changes to all affected layers and consumers | All layers |
| **Archive** | Record the cycle's changes as events | Event |

The sense cycle operates at the cadences defined in INST-HEARTBEAT:
- Fast cadence: observe + compare only (quick state check)
- Medium cadence: full cycle through decide (daily governance)
- Slow cadence: full cycle including revise (structural evolution)

---

## 4. Evolution Modes

### AMMOI-010: Passive Evolution

**Stratum correspondence:** META-001 (State Evolution).
**Scope:** State values change; structure and categories are unchanged.
**Example:** A repo's promotion state changes from CANDIDATE to PUBLIC_PROCESS. A metric observation is recorded. CI status updates.
**Reconciliation:** State -> Event propagation. No structural or ontological impact.

This is the most frequent evolution mode. Most sense cycles produce only passive evolution.

### AMMOI-011: Structural Evolution

**Stratum correspondence:** META-002 (Structural Evolution).
**Scope:** Hierarchy or Relation edges change; categories are unchanged.
**Example:** A new repo is added to an organ. A dependency edge is created between existing repos. A module is extracted from a repo.
**Reconciliation:** Full vertical + horizontal propagation. Identity assigns UID; Hierarchy assigns containment; Relation updates edges; State initialises values; Event records changes; Governance validates constraints.

### AMMOI-012: Ontological Evolution

**Stratum correspondence:** META-003 (Ontological Evolution).
**Scope:** Categories themselves change.
**Example:** A new entity type is introduced. An organ's functional domain is redefined. A new relation type is added to the seed graph.
**Reconciliation:** Full system reconciliation. All six layers may be affected. This is the only evolution mode that corresponds to Boisot's knowledge spiral in its full sense -- the ontological model is genuinely enriched, not merely updated.

### AMMOI-013: Complexity Strategy

AMMOI supports both complexity strategies simultaneously (Boisot & Child 1999):

| Strategy | Layers | Mechanism |
|----------|--------|-----------|
| **Complexity reduction** | Identity, Hierarchy | Uniform codification (UIDs, typed containment edges) imposed across the entire system |
| **Complexity absorption** | Relation, Event | Many valid configurations supported (any valid produces/consumes combination, any event sequence) |

The Governance layer mediates between the two strategies: it reduces complexity by imposing constraints (invariants, promotion criteria) while absorbing complexity by allowing organ-level governance autonomy within constitutional limits.

---

## 5. Reconciliation with Ontologia

### AMMOI-014: AMMOI-Ontologia Alignment

AMMOI is the theoretical model. Ontologia is the implementation. The alignment mapping:

| AMMOI Layer | Ontologia Component | Alignment Status |
|-------------|-------------------|-----------------|
| Identity | EntityIdentity (ULID, entity_type) | ALIGNED |
| Hierarchy | ContainmentEdge (organ -> repo -> module) | ALIGNED |
| Relation | (not yet in ontologia; in seed/graph.py) | PARTIAL |
| State | (not yet in ontologia; in repo-registry.json) | PARTIAL |
| Event | (not yet implemented) | MISSING |
| Governance | (in governance-rules.json, not ontologia) | MISSING |

Full AMMOI reconciliation requires extending ontologia to manage the Relation, State, Event, and Governance layers, or establishing formal interfaces between ontologia and the engine modules that currently manage these layers.

### AMMOI-015: Bootstrap Reconciliation

When the AMMOI system is bootstrapped (from repo-registry.json as the initial state), the bootstrap process must establish coherence across all six layers:

1. **Identity:** Create EntityIdentity for every registered entity (done: `bootstrap_from_registry()`)
2. **Hierarchy:** Create containment edges for every organ-repo-module relationship (done: `sync_modules_from_excavation()`)
3. **Relation:** Import produces/consumes/subscribes edges from seed.yaml (partial: seed graph exists)
4. **State:** Import current promotion state, CI status, metric values (partial: repo-registry.json)
5. **Event:** Synthesise a bootstrap event for each entity and relation (missing)
6. **Governance:** Import governance rules and validate all entities against them (partial: audit exists)

---

## 6. Implementation Status

| Component | Status | Location |
|-----------|--------|----------|
| Identity layer | ALIGNED | `organvm-ontologia/src/ontologia/entity/identity.py` |
| Hierarchy layer | ALIGNED | `organvm-ontologia/src/ontologia/structure/hierarchy.py` |
| Relation layer | PARTIAL | `organvm-engine/src/organvm_engine/seed/graph.py` (not in ontologia) |
| State layer | PARTIAL | `organvm-engine/src/organvm_engine/registry/` (not in ontologia) |
| Event layer | MISSING | Target: INST-EVENT-SPINE implementation |
| Governance layer | PARTIAL | `organvm-engine/src/organvm_engine/governance/` |
| Vertical propagation | PARTIAL | Bootstrap does Identity -> Hierarchy; other paths not automated |
| Horizontal propagation | PARTIAL | Governance audit checks State against Governance rules |
| Sense cycle | MISSING | Target: automated reconciliation loop |

---

## 7. Failure Modes

| Failure | Violated Element | Detection |
|---------|-----------------|-----------|
| Cross-layer inconsistency (entity in State but not in Identity) | AMMOI-007 | Reconciliation sweep: compare entity sets across layers |
| Orphaned hierarchy edge (containment to a deleted entity) | AMMOI-002, INV-000-003 | Hierarchy integrity check: verify all edge endpoints exist |
| Unrecorded state change (State changed without Event) | AMMOI-005, EVT-004 | Event-state comparison: replay events and compare against current state |
| Governance rule change without state reassessment | AMMOI-009, AMMOI-006 | Post-rule-change audit: re-evaluate all entities against new rules |
| Sense cycle stall (no cycle completed within cadence window) | AMMOI-009 | Heartbeat monitoring of last-cycle-completed timestamp |

---

## 8. Evolution Constraints

INST-AMMOI may be amended through the governed process defined in SPEC-000 Section 9. New layers may be added to the six-layer model (constrained extension) but existing layers may not be removed. The sense cycle phases may be refined but their sequential ordering must be preserved. Evolution modes are ordered by impact: passive < structural < ontological; this ordering may not be inverted.

---

## 9. Traceability

```
SPEC-000 AX-000-001 (Ontological Primacy) → AMMOI-001 (Identity layer: define existence before behaviour)
SPEC-000 AX-000-002 (Organizational Closure) → AMMOI-009 (sense cycle: constitutive self-observation process)
SPEC-000 AX-000-007 (Alchemical Inheritance) → AMMOI-001 (Identity layer: UIDs persist through dissolution)
SPEC-000 AX-000-008 (Multiplex Flow Governance) → AMMOI-003 (Relation layer: five edge families)
SPEC-001 (Ontology Charter) → AMMOI-001/002/003 (three structural layers implement ontological classification)
INST-EVENT-SPINE → AMMOI-005 (Event layer is the event spine)
INST-HEARTBEAT → AMMOI-009 (sense cycle cadence aligned with heartbeat cadence)
SPEC-011 (Meta-Evolution Architecture) → AMMOI-010/011/012 (evolution modes correspond to meta-evolution strata)
```

Full grounding narrative: `post-flood/specs/ammoi-reconciliation/grounding.md` (2,915 words)
Full risk register: `post-flood/specs/ammoi-reconciliation/risk-register.md` (5 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
