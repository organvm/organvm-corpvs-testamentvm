# INST-EVENT-SPINE: Event Spine

```
Document ID:      INST-EVENT-SPINE
Title:            Event Spine
Version:          1.0
Status:           RATIFIED
Layer:            L4A — Sensing & Observation
Authoritative:    Append-Only Event Log and Snapshot Mechanism
Parent Specs:     SPEC-000 (System Manifesto), SPEC-007 (Interface Contract Spec)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/event-spine/grounding.md
Risk Register:    post-flood/specs/event-spine/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. Purpose

A constitutional system that cannot remember its own history governs the present without understanding the past. The Event Spine is ORGANVM's constitutional memory: an append-only event log that records every state mutation across the eight-organ system, enabling temporal queries, consistent snapshots, and multi-consumer state projections.

AX-000-008 (Multiplex Flow Governance) mandates that every governance decision be traceable to its constitutional warrant. AX-000-002 (Organizational Closure) requires that constitutive processes produce further constitutive processes through traceable chains. The Event Spine provides the structural mechanism for both: the warrant for any current state is the sequence of events that produced it.

The architecture synthesizes three traditions: Fowler's (2005) event sourcing pattern establishes the append-only log as the single source of truth; Stopford's (2018) event-driven systems architecture provides the inter-organ coordination model; Chandy and Lamport's (1985) distributed snapshot algorithm guarantees causally consistent observation for invariant checking.

**Risk profile: 83% GROUNDED, 17% ADAPTED.**

---

## 2. Event Structure

### EVT-001: Event Record

Every event in the spine carries the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `event_id` | UUID | Globally unique identifier for this event |
| `timestamp` | ISO 8601 | When the event occurred |
| `event_type` | Enum | Classified per the canonical signal classes (SPEC-007) |
| `source_organ` | OrganKey | Which organ emitted the event |
| `source_repo` | RepoName | Which repo emitted the event (if applicable) |
| `actor` | ActorID | The agent or human principal that caused the event |
| `payload` | Object | Event-type-specific data |
| `causal_predecessor` | UUID | null | The event_id that triggered this event, if any |
| `schema_version` | SemVer | Schema version of the payload |

The `causal_predecessor` field enables replay and dependency tracing. A chain of causal predecessors reconstructs the full governance decision trail for any current state.

### EVT-002: Event Types

Event types are drawn from the 14 canonical signal classes defined in INST-FORMATION and extended with governance-specific types:

| Category | Event Types |
|----------|-------------|
| **Governance** | `governance.promotion`, `governance.demotion`, `governance.audit`, `governance.rule_change` |
| **Registry** | `registry.repo_added`, `registry.repo_updated`, `registry.repo_archived` |
| **Dependency** | `dependency.edge_added`, `dependency.edge_removed`, `dependency.cycle_detected` |
| **Identity** | `identity.entity_created`, `identity.entity_renamed`, `identity.entity_merged`, `identity.entity_split` |
| **Metric** | `metric.observation_recorded`, `metric.threshold_crossed`, `metric.snapshot_generated` |
| **Schema** | `schema.version_bumped`, `schema.migration_required` |
| **Organism** | `organism.heartbeat`, `organism.gate_evaluation`, `organism.density_changed` |
| **Session** | `session.started`, `session.completed`, `session.claim_registered` |

New event types may be introduced through governed SPEC-008 constrained extension. Existing event types may not be removed -- they may only be deprecated (new events of that type are no longer emitted, but historical events remain in the log).

### EVT-003: Immutability Guarantee

Events are immutable facts about things that happened. They are never modified or deleted, only appended. This is a constitutive rule, not a regulative one: a mutable event log is not a degraded Event Spine but a different kind of system entirely.

**Correction mechanism:** Errors are corrected by appending compensating events, not by modifying historical records. If a promotion was incorrectly approved, the correction is a new event (`governance.demotion` with `reason: "compensating"` and `causal_predecessor` pointing to the erroneous promotion). History is preserved; corrections are traceable.

**Formal property:** The event log is a monotonically growing sequence. For any timestamps t1 < t2, `events(t1)` is a prefix of `events(t2)`.

---

## 3. Emission Rules

### EVT-004: Mandatory Emission

Every governance operation that mutates system state MUST emit an event to the spine before the mutation is considered committed. The operation-event mapping is:

| Operation | Required Event |
|-----------|---------------|
| `organvm governance promote` | `governance.promotion` |
| `organvm registry update` | `registry.repo_updated` |
| `organvm governance audit` | `governance.audit` |
| Registry save (any path) | `registry.repo_updated` per changed repo |
| Entity creation (ontologia) | `identity.entity_created` |
| Dependency edge mutation | `dependency.edge_added` or `dependency.edge_removed` |
| Metric observation | `metric.observation_recorded` |
| Organism snapshot | `organism.heartbeat` |

Operations that do not mutate state (queries, reads, display) do not emit events.

### EVT-005: Atomic Emission

Event emission and state mutation are atomic: either both succeed or neither does. A state mutation without a corresponding event is a traceability violation (AX-000-008). An event without a corresponding state mutation is a phantom event and must be detectable by replay verification.

### EVT-006: Causal Chain Integrity

If an operation is triggered by a prior event (e.g., a metric threshold crossing triggers a governance escalation), the resulting event MUST set `causal_predecessor` to the triggering event's `event_id`. The causal chain must be acyclic -- an event cannot be its own causal ancestor.

---

## 4. Ordering Guarantees

### EVT-007: Per-Organ Total Order

Within a single organ, events are totally ordered by timestamp. If two events from the same organ have the same timestamp (possible when the same CLI invocation emits multiple events), they are ordered by emission sequence within that invocation.

### EVT-008: Cross-Organ Partial Order

Across organs, events are partially ordered by causal precedence. Two events from different organs with no causal relationship may be concurrent -- neither happened before the other. The Event Spine does not impose a total order on concurrent events from different organs.

This partial ordering follows Lamport's (1978) happened-before relation: event A happened before event B if A causally precedes B (A is an ancestor of B in the causal chain). If neither A nor B is an ancestor of the other, they are concurrent.

### EVT-009: Consistency Window

The Event Spine provides eventual consistency across consumers. A consumer that has processed all events up to timestamp T has a consistent view of the system as of T. The maximum lag between event emission and consumer processing is a configurable health metric (see INST-TEMPORAL-METRICS).

---

## 5. Snapshot Mechanism

### EVT-010: Consistent Snapshots

A snapshot is a materialized view of the system state at a specific point in the event log. Snapshots satisfy the consistent-cut property (Chandy & Lamport 1985): every event reflected in the snapshot's state was emitted before the snapshot point, and every event that causally precedes a reflected event is also reflected.

### EVT-011: Snapshot Triggers

Snapshots are produced:

1. **On sync:** `organvm git sync-all` commits submodule pointers that collectively represent a consistent system state. Each sync produces a snapshot event (`metric.snapshot_generated`).
2. **On audit:** `organvm governance audit` takes a snapshot before evaluating invariants, ensuring the audit operates on a causally consistent view.
3. **On demand:** `organvm organism snapshot --write` produces an organism-level snapshot.
4. **Periodically:** The heartbeat cadence (INST-HEARTBEAT) triggers periodic snapshots at the slow cadence.

### EVT-012: Snapshot as Recovery Point

repo-registry.json is the current materialized snapshot of the event stream's state. If the event log is lost or corrupted, repo-registry.json serves as the recovery point from which a new event log can be bootstrapped. The snapshot is the backup; the event log is the authority.

---

## 6. CQRS Architecture

### EVT-013: Write Model

The Event Spine is the write model. All state mutations flow through event emission. The append-only log is the single source of truth for system history.

### EVT-014: Read Models

All state representations are read models -- materialized views derived from the event stream:

| Read Model | Consumer | Projection |
|------------|----------|------------|
| `repo-registry.json` | Engine, governance | Current entity state (latest promotion, current dependencies) |
| Dashboard | Human operator | Health visualization, graph rendering, soak monitoring |
| MCP server | AI agents | Query results, context injection, governance status |
| Metrics engine | Temporal metrics | Observation history, trend computation, reference mode classification |
| Omega scorecard | Governance | Binary criterion assessment from accumulated evidence |

When any read model diverges from the event log, the correct response is to rebuild the view from the log, not to modify the log to match the view.

### EVT-015: Consumer Lag

Each read model maintains a cursor into the event log marking the last event it has processed. The gap between the latest event and a consumer's cursor is consumer lag. Consumer lag is a health metric:

| Lag Level | Threshold | Governance Response |
|-----------|-----------|-------------------|
| Current | < 1 minute | Normal operation |
| Lagging | 1 minute - 1 hour | Warning; consumer health check |
| Stale | 1 hour - 24 hours | Escalation; rebuild triggered |
| Disconnected | > 24 hours | Red alert; manual intervention |

---

## 7. Temporal Queries

### EVT-016: Point-in-Time State Reconstruction

Any past system state can be reconstructed by replaying events from the beginning of the log (or from the nearest preceding snapshot) to the desired timestamp. The replay produces the exact state that existed at that time, enabling governance audits to answer: "What was the system state when this promotion was approved?"

### EVT-017: Causal Chain Queries

Given any current state element (a repo's promotion status, a dependency edge, a metric value), the Event Spine can trace the causal chain backward to the originating event. This chain is the constitutional warrant for the current state -- the traceable descent from governance decision to current reality that AX-000-008 mandates.

---

## 8. Implementation Status

| Component | Status | Location |
|-----------|--------|----------|
| Event record schema | MISSING | Target: `schema-definitions/schemas/event-spine.schema.json` |
| Append-only log store | MISSING | Target: `organvm-engine/src/organvm_engine/events/` |
| Event emission from governance operations | MISSING | Target: hooks in `governance/`, `registry/`, `metrics/` |
| Snapshot mechanism | PARTIAL | `organvm git sync-all` produces implicit snapshots via submodule pointers |
| CQRS consumer architecture | PARTIAL | Dashboard and MCP server read from registry (a materialized view) but not from an event log |
| Temporal query engine | MISSING | Target: `organvm-engine/src/organvm_engine/events/replay.py` |

The current system operates with mutable state (repo-registry.json as a directly edited JSON file) rather than event-sourced state. The transition from mutable state to event sourcing is a significant architectural change that this specification authorizes and defines.

---

## 9. Failure Modes

| Failure | Violated Element | Detection |
|---------|-----------------|-----------|
| State mutation without event emission | EVT-004, AX-000-008 | Replay verification: replay log and compare against current state |
| Event modification or deletion | EVT-003, INV-000-003 | Log integrity check: hash chain or checksum verification |
| Causal chain cycle | EVT-006 | Cycle detection on causal predecessor graph |
| Consumer lag exceeding threshold | EVT-015 | Health check: compare consumer cursor against log head |
| Snapshot inconsistency | EVT-010 | Consistent-cut verification: check that all causal ancestors of reflected events are also reflected |

---

## 10. Evolution Constraints

INST-EVENT-SPINE may be amended through the governed process defined in SPEC-000 Section 9. Event types may be added (constrained extension) but never removed. The event record schema may be extended with new optional fields but existing fields may not be removed or have their semantics changed. Schema evolution follows SPEC-008's migration law.

---

## 11. Traceability

```
SPEC-000 AX-000-002 (Organizational Closure) → EVT-004 (mandatory emission creates traceable chains)
SPEC-000 AX-000-008 (Multiplex Flow Governance) → EVT-017 (causal chain as constitutional warrant)
SPEC-000 INV-000-003 (Identity Persistence) → EVT-003 (immutability preserves event identity)
SPEC-000 INV-000-005 (Observability) → EVT-014 (read models enable state reporting)
SPEC-007 (Interface Contract Spec) → EVT-002 (event types drawn from signal classes)
INST-TEMPORAL-METRICS → EVT-015 (consumer lag as temporal metric)
INST-HEARTBEAT → EVT-011 (heartbeat triggers periodic snapshots)
```

Full grounding narrative: `post-flood/specs/event-spine/grounding.md` (3,068 words)
Full risk register: `post-flood/specs/event-spine/risk-register.md` (6 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
