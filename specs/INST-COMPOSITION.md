# INST-COMPOSITION: Composition Grammar

```
Document ID:      INST-COMPOSITION
Title:            Composition Grammar
Version:          1.0
Status:           DRAFT
Layer:            L3B — Governance Instruments
Authoritative:    Primitive composition operators, formation crystallization protocol, topological rules
Parent Specs:     SPEC-000 (System Manifesto), SPEC-025 (Institutional Primitive Vocabulary), SPEC-019 (Liquid Constitutional Order)
Companion to:     INST-FORMATION (Formation Protocol — defines formation types; this spec defines how primitives compose INTO formations)
Date Drafted:     2026-04-20
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 0. Scope and Relationship to INST-FORMATION

INST-FORMATION defines formation TYPES (Generator, Transformer, Router, etc.) — what a formation IS once it exists. INST-COMPOSITION defines how primitives COMPOSE into formations — the grammar by which atomic operations combine into institutional capabilities.

INST-FORMATION classifies the creature. INST-COMPOSITION describes embryogenesis.

---

## 1. The Shared Primitive Pool

### COMP-001: Pool Architecture

All primitives inhabit a single flat pool:

**Production primitives** (13): reader, classifier, labeler, scheduler, credential, writer, renderer, publisher, distributor, broadcaster, analyzer, indexer, orchestrator.

**Institutional primitives** (19): assessor, guardian, advocate, insulator, appraiser, ledger, optimizer, collector, allocator, negotiator, representative, registrar, liaison, counselor, auditor, archivist, incorporator, enforcer, strategist, mandator.

**Pool properties:**
- Flat — no hierarchy between production and institutional primitives
- Open — new primitives may be admitted per SPEC-025 Section 7 or production primitive evolution
- Addressable — every primitive has a unique identifier (PRIM-PROD-* or PRIM-INST-*)
- Stateless — primitives themselves hold no state; state lives in the formation context

### COMP-002: The Orchestrator's Role

The `orchestrator` (production primitive) is the composition authority. It:
- Receives a formation invocation (trigger condition met or explicit invocation)
- Selects and instantiates the required primitives from the pool
- Wires them according to the composition operators (Section 2)
- Routes escalation flags to the principal
- Passes audit trails to archivist

The orchestrator does not belong to any formation — it is the meta-primitive that enables all formations. Every formation invocation passes through the orchestrator.

---

## 2. Composition Operators

Four operators define how primitives combine. These four are sufficient to express any institutional formation. If a composition cannot be expressed, that signals a primitive decomposition problem (Section 5), not a missing operator.

### COMP-003: CHAIN (→)

**Syntax**: `A → B`

**Semantics**: Output of primitive A feeds as context to primitive B. Sequential dependency — B cannot begin until A completes.

**Interface contract**: A.output becomes B.context. A.confidence propagates (B inherits the lower of A.confidence and its own). A.escalation_flag, if true, halts the chain until human review.

**Example**:
```
assessor(legal_frame) → counselor → mandator
```
"Assess the legal situation, synthesize a recommendation, formalize the directive."

**Properties**:
- Deterministic ordering
- Confidence degrades along the chain (weakest link)
- Any escalation_flag halts propagation

---

### COMP-004: PARALLEL (||)

**Syntax**: `A || B || C`

**Semantics**: Multiple primitives operate on the same context simultaneously. Outputs are merged before passing downstream.

**Interface contract**: All parallel primitives receive the same context, frame, and principal_position. Outputs are collected into a composite output. Confidence = minimum across parallel branches. Any escalation_flag propagates.

**Merge strategy**: Outputs are concatenated with source attribution. Downstream primitives (typically counselor) receive all parallel outputs and synthesize.

**Example**:
```
assessor(legal) || assessor(financial) || assessor(relational) → counselor
```
"Assess simultaneously across legal, financial, and relational frames, then synthesize."

**Properties**:
- No ordering between parallel branches
- Execution time = max(branch times), not sum
- Conflict between parallel outputs is not resolved by the operator — resolution is the downstream primitive's job

---

### COMP-005: ENVELOPE (⊃)

**Syntax**: `A ⊃ B` (A envelopes B)

**Semantics**: Primitive A wraps primitive B, constraining or transforming B's operation. A defines the boundary conditions within which B operates. A may filter B's inputs, attenuate B's outputs, or impose constraints on B's execution.

**Interface contract**: A receives the original context. A may transform context before passing to B. B operates within A's constraints. A may filter B's output before propagation. A's audit_trail records both its own operation and B's operation.

**Example**:
```
insulator ⊃ (negotiator → advocate)
```
"Negotiate and advocate, but within an information barrier that limits what can be disclosed."

**Properties**:
- Envelopes are NOT sequential — A doesn't "run first." A is ACTIVE DURING B's execution.
- Envelopes can nest: `A ⊃ (B ⊃ C)` — multiple constraint layers
- The outer primitive has authority over the inner primitive's operation

---

### COMP-006: FEEDBACK (↻)

**Syntax**: `A → B → C ↻ A`

**Semantics**: Output of a downstream primitive loops back as new context to an upstream primitive, creating iterative refinement. The cycle continues until a convergence condition is met.

**Interface contract**: The loopback output replaces (or augments) the original context for the upstream primitive. Each iteration produces a new audit_trail entry. Convergence is detected when the delta between successive outputs falls below a threshold, or after a maximum iteration count.

**Convergence rules**:
- Maximum iterations: 5 (default, configurable per formation)
- Convergence threshold: delta(output_n, output_n-1) < epsilon (defined per primitive)
- Divergence detection: if confidence decreases on successive iterations, halt and escalate

**Example**:
```
strategist → assessor → counselor ↻ strategist
```
"Model position, assess exposure, recommend, then re-model with the recommendation's effects. Repeat until the model stabilizes."

**Properties**:
- Convergence is NOT guaranteed — divergence detection + iteration cap prevent infinite loops
- Each iteration increases audit_trail depth
- Feedback loops are the mechanism for self-correcting institutional judgment

---

## 3. Operator Composition

Operators compose freely. Complex formations use multiple operators:

```
guardian(threats) → [assessor(legal) || assessor(financial)] → counselor → mandator
                                                                    ↑
                                                                archivist (precedent)
```

This expresses: "Guardian detects threat → parallel legal and financial assessment → counselor synthesizes with archivist precedent lookup → mandator formalizes directive."

**Precedence rules**:
1. ENVELOPE (⊃) binds tightest — its scope is explicit in the grouping
2. CHAIN (→) is the default sequential connector
3. PARALLEL (||) groups co-equal operations
4. FEEDBACK (↻) is an explicit annotation on a chain segment

**Grouping**: Parentheses or brackets clarify scope when operators nest.

---

## 4. Formation Crystallization Protocol

This protocol governs how ad hoc compositions stabilize into named formations. It extends INST-FORMATION Section 4 (Formation Lifecycle) with the specific mechanism for institutional formation emergence.

### COMP-007: Crystallization Stages

**Stage 1 — OCCURRENCE**: A composition is invoked ad hoc to handle a specific situation. The orchestrator wires primitives on the fly. Archivist records the composition graph and its outcome.

**Stage 2 — RECURRENCE**: Archivist detects that the same or structurally similar composition has been invoked 3+ times within a recognition window (default: 30 days). "Structurally similar" means: same primitives in the same operator relationships, with variation only in frame parameters or context.

**Stage 3 — NOMINATION**: The system proposes a name for the recurring composition. Naming follows ORGANVM ontological density standards:
- Single Latin/Greek-derived noun where possible
- Names the institutional function, not the constituent primitives
- Must be utterable as a command: "Invoke [formation]" must sound like giving an order

The principal confirms, renames, or rejects the nomination.

**Stage 4 — CRYSTALLIZATION**: The composition is registered as a named formation with:
- **Trigger conditions**: When this formation should be invoked (can be automatic or manual)
- **Primitive graph**: The operator-connected composition with default frames
- **Variation points**: Which parts of the graph are context-dependent (may substitute primitives or change frames)
- **Escalation policies**: Which primitives in this formation always escalate vs. execute autonomously
- **Exit conditions**: Per INST-FORMATION FORM-013

**Stage 5 — EVOLUTION**: Auditor detects when a formation's actual invocations diverge from its crystallized form. If divergence persists across 3+ invocations, re-crystallization is triggered — the formation's graph is updated to match its actual operational pattern.

### COMP-008: Formation Registry

Crystallized formations are registered in the ORGANVM registry (extending repo-registry.json or in a dedicated formations registry). Each entry contains:

```yaml
formation:
  name: aegis
  status: crystallized  # | occurring | recurring | nominated | evolved
  trigger: "threat detected by guardian AND stakes >= significant"
  graph: "guardian → [assessor(legal) || assessor(financial)] → counselor → mandator"
  variation_points:
    - primitive: assessor
      parameter: frame
      options: [legal, financial, relational, reputational]
  escalation_policy:
    always_escalate: [mandator]  # human approves all directives
    threshold_escalate: [counselor]  # escalate if confidence < 0.7
  exit_conditions:
    - "threat resolved (no guardian alerts for 7+ days)"
    - "escalated to enforcer (formation handoff)"
  crystallized_date: 2026-04-20
  invocation_count: 0
  last_invoked: null
```

---

## 5. Topological Relationships

### COMP-009: Context-Dependent Topology

Institutional formations relate to production formations (organ pipelines) in three modes simultaneously. The mode is determined per-invocation, not per-formation:

**Substrate (beneath)**: The institutional formation provides ground that a production formation relies upon.
- Example: Ledger + insulator provide the economic/legal ground for ORGAN-III product sales.
- Signal direction: Production formation calls DOWN into institutional formation.

**Peer (alongside)**: Institutional and production formations operate in parallel on the same situation.
- Example: A legal threat arrives while ORGAN-V is publishing. Aegis and the publication pipeline respond simultaneously.
- Signal direction: Both respond to the same event; orchestrator coordinates.

**Envelope (wrapping)**: Institutional formation constrains/gates a production formation.
- Example: Insulator + assessor wrap any publishing pipeline, checking for liability before release.
- Signal direction: Production pipeline PASSES THROUGH institutional membrane.

### COMP-010: No Fixed Layer Assignment

A formation's topological relationship is NOT a fixed property. The same formation may operate as substrate in one invocation, peer in another, and envelope in a third. This is why the system is built from primitives and operators rather than layers — layers would force a fixed topology.

The orchestrator determines topology per-invocation based on:
1. What triggered the formation (event type determines relationship)
2. What else is active (concurrent formations determine peer/envelope)
3. What the formation's output feeds into (downstream determines substrate/peer)

---

## 6. The Hybrid Formation Pattern

Most operationally interesting formations are **hybrid** — containing both production and institutional primitives. Hybrid formations are the normal case, not the exception.

### COMP-011: Hybrid Formation Example

**Publishing with Institutional Awareness**:
```
writer → renderer → assessor(liability) → insulator(entity_attribution) → publisher → distributor
                          ↓ (if escalation_flag)
                     guardian(hold) → counselor → mandator(proceed | modify | kill)
```

This is a production pipeline (writer → renderer → publisher → distributor) with institutional primitives woven in. Neither "production with an institutional check" nor "institutional pipeline that publishes." It is a single formation drawing from the shared pool.

### COMP-012: Hybrid Formation Classification

When a hybrid formation crystallizes, its INST-FORMATION type is determined by which function DOMINATES:
- If production output is primary → classify by production type (GENERATOR, TRANSFORMER, etc.)
- If institutional operation is primary → classify as SYNTHESIZER (the cross-configurational type)
- If truly balanced → SYNTHESIZER

---

## 7. Prohibited Compositions

Per INST-FORMATION FORM-009 (Prohibited Couplings), certain compositions are constitutionally prohibited:

### COMP-013: Prohibited Patterns

| Prohibition | Expression | Rationale |
|------------|-----------|-----------|
| **Assessor self-assessment** | `assessor ↻ assessor` (same frame) | Unbounded self-reference without external ground |
| **Mandator without counselor** | `assessor → mandator` (skipping synthesis) | Directives without integrated recommendation bypass judgment |
| **Enforcer without guardian** | `enforcer` invoked without prior guardian alert | Enforcement without detection is aggression, not defense |
| **Allocator without ledger** | `optimizer → allocator` (no ledger state) | Cannot allocate without knowing current position |
| **Representative without insulator** | `representative` in adversarial context without insulator envelope | Information leakage risk in adversarial engagement |

These prohibitions are constitutive — a composition violating them is malformed, not merely risky. The orchestrator refuses to wire prohibited compositions.

---

## 8. Evolution Constraints

INST-COMPOSITION may be amended per the governed process:

| Type | Definition | Requirements |
|------|-----------|--------------|
| **Conservative Refinement** | Adjusts convergence defaults, adds examples, refines topological descriptions | Adversarial review + principal sign-off |
| **Constrained Extension** | Adds new composition operators (must be proven necessary — four operators insufficient) | Adversarial review + proof that existing operators cannot express the needed composition + impact assessment on all crystallized formations + principal sign-off |
| **Breaking Revision** | Changes operator semantics, modifies interface contract propagation rules, removes prohibited compositions | New grounding + adversarial review + formation migration plan + principal sign-off |

COMP identifiers are permanent. The four operators (CHAIN, PARALLEL, ENVELOPE, FEEDBACK) are constitutive — changing them changes the grammar of institutional agency.

---

## 9. Traceability

### 9.1 Upward Traceability

| SPEC-000 Element | INST-COMPOSITION Grounding |
|------------------|---------------------------|
| AX-000-006 (Topological Plasticity) | COMP-009, COMP-010 — topology is context-dependent, not fixed |
| AX-000-009 (Modular Alchemical Synthesis) | The entire spec — primitives are atoms, operators are bonds, formations are compounds |
| INV-000-001 (Dependency Acyclicity) | FEEDBACK (↻) is bounded — convergence rules prevent unbounded cycles |

### 9.2 Lateral Traceability

| Peer Spec | Connection |
|-----------|-----------|
| SPEC-025 (Institutional Primitives) | Defines the atoms that this grammar composes |
| INST-FORMATION (Formation Protocol) | Defines formation types; COMP-007 extends lifecycle with crystallization mechanism |
| SPEC-007 (Interface Contract) | Primitive interface contract (SPEC-025 Section 2) is a specialized interface contract |
| SPEC-004 (Logical Specification) | Crystallization stages are a state machine governed by SPEC-004 |
