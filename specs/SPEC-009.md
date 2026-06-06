# SPEC-009: Structural Interrogation

```
Document ID:      SPEC-009
Title:            Structural Interrogation
Version:          1.0
Status:           RATIFIED
Layer:            L4B — Diagnosis & Meta-Evolution
Authoritative:    Multi-Dimensional System Diagnostics
Parent Specs:     SPEC-000 (System Manifesto), SPEC-003 (Invariant Register)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/SPEC-009/grounding.md
Risk Register:    post-flood/specs/SPEC-009/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. Purpose

A system that cannot diagnose itself degrades without detection. SPEC-003's invariant monitoring detects specific violations -- a dependency cycle, a governance gap, a stale metric. But invariant violations are symptoms, not diagnoses. The question "why did this invariant violation occur?" requires a different analytical apparatus: one that examines the system's health across multiple dimensions simultaneously, identifies structural tensions before they become violations, and provides actionable diagnostic output.

The gap between "no invariant is currently violated" and "the system is healthy" is the gap SPEC-009 fills.

The architecture synthesizes three critical systems thinking traditions: Checkland's (1981) Soft Systems Methodology provides the structured inquiry process; Ulrich's (1983) Critical Systems Heuristics provides the normative reflexivity (is/ought distinction, boundary critique); Jackson's (2003) Critical Systems Thinking provides the meta-methodology (choosing the right analytical lens for each dimension).

**Risk profile: 50% GROUNDED, 17% ADAPTED, 33% NOVEL.**

---

## 2. The Seven Diagnostic Dimensions

### DIAG-001: Existence

**Question:** Does the entity exist with proper constitutional authorization?

**Is-mode:** Is this entity registered in repo-registry.json? Does it have a seed.yaml? Is it tracked in ontologia with a ULID?

**Ought-mode:** Per AX-000-004 (Constitutional Governance), every component must be constitutionally authorized. Per INV-000-002 (Governance Reachability), every active component must be reachable from the constitutional root.

**Methodology:** Hard systems analysis -- binary existence checks, registry lookups, seed discovery.

**Diagnostic output:** List of entities that exist in the workspace but not in the registry (environment, not system), or in the registry but not in the workspace (orphaned entries).

### DIAG-002: Identity

**Question:** Is the entity's identity stable, continuous, and properly tracked?

**Is-mode:** Does the entity have a ULID in ontologia? Are all name records current? Is the lineage chain intact (predecessor/successor UIDs for archived entities)?

**Ought-mode:** Per INV-000-003 (Identity Persistence), no UID may be destroyed. Per AX-000-007 (Alchemical Inheritance), dissolved components must carry structured lineage.

**Methodology:** Hard systems analysis -- UID validation, name record currency, lineage chain integrity.

**Diagnostic output:** Entities with missing UIDs, broken lineage chains, or unresolvable name records.

### DIAG-003: Structure

**Question:** Is the entity's structural position correct -- its containment, dependencies, and cross-organ edges?

**Is-mode:** What organ does it belong to? What are its declared dependencies? What does it produce and consume? What is its position in the dependency DAG?

**Ought-mode:** Per INV-000-001 (Dependency Acyclicity), the dependency graph must be a DAG. Per AX-000-008, dependency flow is I -> II -> III, with no back-edges. Per seed.yaml contracts, declared edges must match actual usage.

**Methodology:** Graph theory -- centrality analysis, cycle detection, community structure, resilience simulation (per INST-GRAPH-INDICES).

**Diagnostic output:** Structural anomalies: high-betweenness bottlenecks, undeclared dependencies, cross-organ edges violating dependency direction.

### DIAG-004: Law

**Question:** Is the entity governed correctly -- does it comply with applicable rules, and are those rules consistent with constitutional authority?

**Is-mode:** What promotion state is the entity in? Does it satisfy the criteria for its current state? What governance rules apply to it?

**Ought-mode:** Per INV-000-004 (Constitutional Supremacy), no lower-level rule may override a higher-level constitutional constraint. Per SPEC-005 (Rulebook), governance rules are evaluable first-class objects.

**Methodology:** Organizational cybernetics and Critical Systems Heuristics -- authority hierarchy analysis, constraint consistency checking, boundary critique (who decides what counts as compliant?).

**Diagnostic output:** Entities violating their current promotion criteria, governance rules contradicting constitutional constraints, authority gaps (no rule governs a relevant operation).

### DIAG-005: Process

**Question:** Are the entity's operational processes healthy -- producing expected outputs at expected cadence with expected feedback?

**Is-mode:** What is the CI run frequency? What is the metric observation cadence? What is the promotion velocity? Are feedback loops functioning (are metric changes producing governance responses)?

**Ought-mode:** Per INST-TEMPORAL-METRICS, metrics should follow expected reference modes. Per INST-HEARTBEAT, vital parameters should be within healthy ranges. Per SPEC-004, state transitions should follow the governed state machine.

**Methodology:** System dynamics -- feedback loop analysis, delay measurement, reference mode comparison (per INST-TEMPORAL-METRICS).

**Diagnostic output:** Process anomalies: stale CI, missing metric observations, feedback loops with excessive delay, reference mode deviations.

### DIAG-006: Relation

**Question:** Are the entity's relationships with other entities healthy -- correctly typed, appropriately coupled, and governmentally consistent?

**Is-mode:** What are its actual dependency edges? What signal flows does it participate in? What events does it emit and consume? What is its coupling profile (degree, betweenness, clustering)?

**Ought-mode:** Per AX-000-008, inter-organ flow is multiplex (five edge families, each independently governed). Per AX-000-009, every connection is observable. Per INST-GRAPH-INDICES, coupling risk should be within thresholds.

**Methodology:** Graph theory and network analysis -- centrality, resilience, assortative mixing (per INST-GRAPH-INDICES).

**Diagnostic output:** Relational anomalies: excessive coupling (high betweenness), isolation (low closeness), maturity mismatch (GRADUATED repo depending on LOCAL repo), undeclared signal flows.

### DIAG-007: Teleology

**Question:** Is the entity fulfilling its purpose -- contributing to the system's teleological objective?

**Is-mode:** What is the entity's declared purpose (from seed.yaml, ecosystem.yaml, or repo description)? What does it actually produce? Does its output reach its intended consumers?

**Ought-mode:** Per AX-000-003 (Individual Primacy), the system exists to amplify individual creative capacity. Per SPEC-000 Section 2, every component should participate in the epistemic loop from theory through implementation to governance. Per the formation protocol, every formation has declared signal outputs and exit conditions.

**Methodology:** Soft Systems Methodology and Critical Systems Heuristics -- purpose assessment, boundary critique (whose purpose does this serve?), worldview examination (does the entity's design reflect the constitutional worldview?).

**Diagnostic output:** Teleological anomalies: repos with no declared consumers, formations with unsatisfied exit conditions, entities whose actual outputs diverge from declared purpose.

---

## 3. Fast Tension Scan

### DIAG-008: Ten Compressed Questions

The Fast Tension Scan provides rapid triage (5-10 minutes) across all seven dimensions. Each question produces a traffic-light assessment and identifies dimensions requiring deeper analysis.

| # | Question | Dimension(s) | Source |
|---|----------|-------------|--------|
| 1 | Are there entities in the workspace not in the registry, or in the registry not in the workspace? | Existence | Seed discovery + registry comparison |
| 2 | Are all active entities tracked in ontologia with valid UIDs? | Identity | Ontologia resolve sweep |
| 3 | Is the dependency graph acyclic with all edges respecting organ direction? | Structure | `organvm governance check-deps` |
| 4 | Do all repos satisfy the criteria for their current promotion state? | Law | `organvm governance audit` |
| 5 | Are all metrics fresh (observed within their cadence window)? | Process | Freshness check across all temporal metrics |
| 6 | Are there repos with betweenness centrality above the risk threshold? | Relation | Graph index computation (CRI) |
| 7 | Is the system gestalt COHERENT or better? | Process, Relation | INST-HEARTBEAT gestalt |
| 8 | Does every active repo have at least one declared consumer of its outputs? | Teleology | Seed graph: repos with no outgoing `produces` edges consumed by any `consumes` edge |
| 9 | Are there governance rules that contradict constitutional constraints? | Law | Constitutional supremacy check (INV-000-004) |
| 10 | Is the system in the target regime (neither frozen nor chaotic)? | All | Edge-of-chaos assessment (INST-HEARTBEAT) |

### DIAG-009: Scan Output

The scan produces a structured diagnostic:

```
FAST TENSION SCAN — [timestamp]
Gestalt: COHERENT

  1. Existence    [GREEN]  0 orphans, 0 phantoms
  2. Identity     [GREEN]  179/179 entities resolved
  3. Structure    [GREEN]  DAG valid, direction compliant
  4. Law          [YELLOW] 3 repos below current-state criteria
  5. Process      [GREEN]  All metrics fresh
  6. Relation     [YELLOW] 1 repo above CRI threshold (organvm-engine)
  7. Gestalt      [GREEN]  COHERENT, stable trajectory
  8. Teleology    [GREEN]  All repos have consumers
  9. Supremacy    [GREEN]  No contradictions detected
  10. Regime      [GREEN]  Target regime

Dimensions requiring deeper analysis: Law (4), Relation (6)
```

---

## 4. Meta-Developer Descent Check

### DIAG-010: Five-Level Descent

The Meta-Developer Descent Check traces from constitutional principle to observable outcome, identifying where the governance chain breaks:

| Level | Question | Example |
|-------|----------|---------|
| **Principle** | Which constitutional axiom applies? | AX-000-004: Constitutional Governance |
| **Structure** | What structural commitment implements it? | Every repo has seed.yaml declaring organ, tier, status |
| **Process** | What operational process enforces it? | `organvm seed validate` checks seed presence and schema |
| **Implementation** | What code/config/schema realizes it? | `seed/discover.py` walks workspace; `seed/reader.py` parses; schema validates |
| **Outcome** | What observable result demonstrates it? | `organvm seed validate` reports 0 violations; `organvm governance audit` finds no ungoverned repos |

### DIAG-011: Chain Break Analysis

At each level, the descent checks whether the chain from the level above is intact:

| Break Point | Meaning | Example |
|-------------|---------|---------|
| Principle -> Structure | Axiom not yet expressed as structural commitment | AX-000-009 (Modular Alchemical Synthesis) has no structural implementation |
| Structure -> Process | Structural commitment not yet enforced by a process | Governance reachability (INV-000-002) defined but no audit process checks it |
| Process -> Implementation | Process defined but code does not implement it | Constitutional supremacy check defined but no validator exists |
| Implementation -> Outcome | Code exists but does not produce expected results | Seed validation exists but does not catch all violations |

Each break point is a governance gap with a severity proportional to its level: principle-level breaks are constitutional deficits; outcome-level breaks are engineering bugs.

---

## 5. Interrogation Protocol

### DIAG-012: Three Levels of Depth

| Level | Scope | Duration | Trigger | Output |
|-------|-------|----------|---------|--------|
| **Level 1: Fast Tension Scan** | All dimensions, surface check | 5-10 min | Any governance review, sprint boundary | Traffic-light scan (DIAG-009) |
| **Level 2: Dimensional Analysis** | One or more flagged dimensions, deep dive | 30-60 min | Yellow/red scan results, structural concern | Tension report with is/ought comparison, root cause analysis |
| **Level 3: Meta-Developer Descent** | Specific principle-to-outcome chain | 15-30 min | Persistent tension, invariant violation investigation | Chain break analysis (DIAG-011) with remediation recommendation |

### DIAG-013: Methodology Selection Per Dimension

Per Jackson's (2003) Creative Holism, each dimension is analyzed with the methodology most suited to its nature:

| Dimension | Primary Methodology | Tooling |
|-----------|-------------------|---------|
| Existence | Hard systems analysis | `organvm seed discover`, `organvm registry validate` |
| Identity | Hard systems analysis | `organvm ontologia resolve`, `organvm ontologia status` |
| Structure | Graph theory | `organvm governance check-deps`, INST-GRAPH-INDICES |
| Law | Organizational cybernetics, CSH | `organvm governance audit`, constitutional review |
| Process | System dynamics | INST-TEMPORAL-METRICS, INST-HEARTBEAT |
| Relation | Network analysis | INST-GRAPH-INDICES, `organvm seed graph` |
| Teleology | SSM, CSH | Formation protocol review, ecosystem audit |

---

## 6. Implementation Status

| Component | Status | Location |
|-----------|--------|----------|
| Fast Tension Scan (automated questions 1-7) | PARTIAL | Individual CLI commands exist; no unified scan |
| Fast Tension Scan (questions 8-10) | MISSING | Require graph indices, constitutional supremacy check |
| Dimensional analysis framework | MISSING | Target: `organvm-engine/src/organvm_engine/diagnostics/` |
| Meta-Developer Descent Check | MISSING | Target: `organvm-engine/src/organvm_engine/diagnostics/descent.py` |
| Unified interrogation CLI | MISSING | Target: `organvm interrogate [--level 1|2|3] [--dimension X]` |

---

## 7. Evolution Constraints

SPEC-009 may be amended through the governed process defined in SPEC-000 Section 9. New diagnostic dimensions may be added (constrained extension) but the seven existing dimensions may not be removed. The Fast Tension Scan's ten questions may be refined or extended but the minimum coverage of all seven dimensions must be preserved.

---

## 8. Traceability

```
SPEC-000 AX-000-002 (Organizational Closure) → DIAG-001 (existence verification of constitutive components)
SPEC-000 AX-000-004 (Constitutional Governance) → DIAG-004 (law dimension checks governance compliance)
SPEC-000 INV-000-005 (Observability) → DIAG-005 (process dimension checks observation health)
SPEC-003 (Invariant Register) → DIAG-008 Q3/Q4/Q9 (scan checks invariant health)
INST-TEMPORAL-METRICS → DIAG-005 (process dimension consumes reference mode analysis)
INST-HEARTBEAT → DIAG-008 Q7/Q10 (scan checks gestalt and regime)
INST-GRAPH-INDICES → DIAG-003/006 (structure/relation dimensions consume graph indices)
SPEC-010 (Alpha-Omega Phase Map) → DIAG-007 (teleology dimension assesses phase-appropriate purpose)
```

Full grounding narrative: `post-flood/specs/SPEC-009/grounding.md` (2,931 words)
Full risk register: `post-flood/specs/SPEC-009/risk-register.md` (6 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
