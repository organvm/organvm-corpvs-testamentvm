# INST-GRAPH-INDICES: Composite Graph Indices

```
Document ID:      INST-GRAPH-INDICES
Title:            Composite Graph Indices
Version:          1.0
Status:           RATIFIED
Layer:            L4B — Diagnosis & Meta-Evolution
Authoritative:    Multiplex Graph Diagnostics
Parent Specs:     SPEC-000 (System Manifesto), SPEC-006 (Architecture Document), SPEC-008 (Evolution & Migration Law)
Date Ratified:    2026-03-19
Grounding:        post-flood/specs/graph-indices/grounding.md
Risk Register:    post-flood/specs/graph-indices/risk-register.md
Bibliography:     post-flood/specs/bibliography.bib
Principal Author: https://orcid.org/0009-0008-2007-3596
```

---

## 1. Purpose

ORGANVM is a graph before it is anything else. Every repo is a node. Every dependency, information flow, governance relationship, and evolutionary trajectory is an edge. The five composite graph indices -- CCI, DDI, FVI, CRI, ECI -- are purpose-built governance diagnostics constructed from network science primitives.

Raw network metrics (node count, edge count, average degree) are too general to diagnose specific governance concerns. The five indices answer governance-specific questions: Is every node constitutionally covered? Are dependency structures disciplined? Are information feedback loops vital? Are coupling patterns risky? Are evolutionary trajectories coherent?

The architecture draws on Freeman's (1978/79) canonical centrality measures, Newman's (2010) comprehensive network analysis toolkit, and Watts and Strogatz's (1998) small-world topology model.

**Central theorem:** The dependency graph must be acyclic, but the information graph must be recursively cyclic. This is the mathematical signature of a healthy recursive organism.

**Risk profile: 67% GROUNDED, 17% ADAPTED, 17% NOVEL.**

---

## 2. The Five Indices

### IDX-001: Constitutional Coverage Index (CCI)

**Question:** Is every node constitutionally covered -- visible to the governance framework with complete metadata?

**Formula:**

```
CCI = (nodes_with_complete_governance_metadata) / (total_active_nodes)
```

where "complete governance metadata" requires:
- seed.yaml present and schema-valid
- repo-registry.json entry present with all required fields
- ontologia entity with valid ULID
- at least one declared `produces` or `consumes` edge

**Interpretation:**

| CCI Value | Assessment | Governance Response |
|-----------|-----------|-------------------|
| 1.0 | Full coverage | No action needed |
| 0.90 - 0.99 | Near-complete | Identify uncovered nodes; prioritise remediation |
| 0.80 - 0.89 | Significant gaps | Governance blind spots; elevated risk of ungoverned drift |
| < 0.80 | Constitutional deficit | Urgent: large portions of the system are ungoverned |

**Network primitive:** Graph completeness (fraction of nodes satisfying metadata predicates).

### IDX-002: Dependency Discipline Index (DDI)

**Question:** Are dependency structures disciplined -- acyclic, well-distributed, without fragile hubs or bottlenecks?

**Components:**

| Sub-index | Formula | Source | Weight |
|-----------|---------|--------|--------|
| DAG validity | Binary: 1 if acyclic, 0 if cycle detected | DFS cycle detection | Veto (DDI = 0 if cycle) |
| Degree distribution health | 1 - (max_in_degree / total_nodes) | Freeman 1978/79 | 0.3 |
| Betweenness distribution health | 1 - (max_betweenness / theoretical_max) | Freeman 1978/79 | 0.3 |
| Network centralisation health | 1 - centralisation(G^dep) | Freeman 1978/79 | 0.4 |

**Formula:**

```
DDI = 0                                   if cycle detected
DDI = 0.3 * degree_health
    + 0.3 * betweenness_health
    + 0.4 * centralisation_health         otherwise
```

**Interpretation:**

| DDI Value | Assessment | Governance Response |
|-----------|-----------|-------------------|
| 0.0 | Cycle detected | INVARIANT VIOLATION (INV-000-001). Immediate remediation. |
| 0.0 - 0.4 | Hub-and-spoke fragility | Identify bottleneck repos; redistribute dependencies |
| 0.4 - 0.7 | Moderate concentration | Monitor; plan dependency redistribution |
| 0.7 - 1.0 | Well-distributed | Healthy dependency structure |

**Network primitives:** Freeman's three centrality measures (degree, betweenness, closeness) plus DAG validation.

### IDX-003: Feedback Vitality Index (FVI)

**Question:** Are information feedback loops vital -- enabling the system to sense its own state across organ boundaries?

**Components:**

| Sub-index | Formula | Source | Weight |
|-----------|---------|--------|--------|
| Clustering coefficient | C / C_target (capped at 1.0) | Watts & Strogatz 1998 | 0.3 |
| Characteristic path length | L_target / L (capped at 1.0) | Watts & Strogatz 1998 | 0.3 |
| Community alignment | fraction of detected communities matching organ partition | Newman 2010 | 0.4 |

**Formula:**

```
FVI = 0.3 * min(C / C_target, 1.0)
    + 0.3 * min(L_target / L, 1.0)
    + 0.4 * community_alignment
```

where:
- `C` = clustering coefficient of the information graph G^info
- `C_target` = target clustering coefficient (empirically determined, initially 0.3)
- `L` = characteristic path length of G^info
- `L_target` = target path length (empirically determined, initially 3.0)
- `community_alignment` = fraction of modularity-detected communities that align with the eight-organ partition

**Interpretation:**

| FVI Value | Assessment | Governance Response |
|-----------|-----------|-------------------|
| 0.8 - 1.0 | Small-world regime | Healthy information flow topology |
| 0.5 - 0.8 | Partial connectivity | Some organs isolated from information flow; add cross-organ edges |
| 0.3 - 0.5 | Weak feedback | Information not flowing across organ boundaries; structural concern |
| < 0.3 | Feedback starvation | System cannot sense its own state; urgent structural intervention |

**Network primitives:** Watts-Strogatz small-world metrics plus Newman's community detection.

**Central theorem application:** FVI measures the information graph's cyclicity. If FVI is low, the information graph lacks recursive cycles -- the system cannot observe itself. INV-000-005 (Observability) requires FVI above the feedback starvation threshold.

### IDX-004: Coupling Risk Index (CRI)

**Question:** Are coupling patterns risky -- is the system fragile to targeted node removal?

**Components:**

| Sub-index | Formula | Source | Weight |
|-----------|---------|--------|--------|
| Resilience (random removal) | fraction of graph remaining connected after random 10% node removal (averaged over 100 trials) | Newman 2010 | 0.3 |
| Resilience (targeted removal) | fraction of graph remaining connected after removing top-3 betweenness nodes | Newman 2010 | 0.4 |
| Degree assortativity | (1 + assortativity_coefficient) / 2 (normalised to 0-1) | Newman 2010 | 0.3 |

**Formula:**

```
CRI = 1 - (0.3 * random_resilience
         + 0.4 * targeted_resilience
         + 0.3 * normalised_assortativity)
```

Note: CRI is inverted -- higher values mean higher risk.

**Interpretation:**

| CRI Value | Assessment | Governance Response |
|-----------|-----------|-------------------|
| < 0.2 | Low risk | Healthy coupling; no single points of failure |
| 0.2 - 0.4 | Moderate risk | Some hub dependencies; monitor |
| 0.4 - 0.6 | Elevated risk | Significant hub fragility; plan dependency redistribution |
| > 0.6 | Critical risk | System brittle to targeted failure; urgent remediation |

**Flagged repos:** Any repo whose individual removal disconnects more than 20% of the graph is flagged as a coupling risk hub, regardless of the aggregate CRI score.

**Network primitives:** Newman's resilience analysis plus Freeman's betweenness as fragility indicator.

### IDX-005: Evolutionary Coherence Index (ECI)

**Question:** Are evolutionary trajectories coherent -- do repos at similar maturity levels cluster together, and is the system evolving uniformly?

**Components:**

| Sub-index | Formula | Source | Weight |
|-----------|---------|--------|--------|
| Promotion-state assortativity | (1 + r_promotion) / 2 (normalised mixing coefficient) | Newman 2010, adapted | 0.4 |
| Promotion clustering | fraction of each organ's repos within 1 promotion state of the organ's median | Community analysis | 0.3 |
| Evolutionary isolation | 1 - (fraction of repos with closeness centrality below the 10th percentile) | Freeman 1978/79 | 0.3 |

**Formula:**

```
ECI = 0.4 * normalised_promotion_assortativity
    + 0.3 * promotion_clustering
    + 0.3 * (1 - isolation_fraction)
```

**Interpretation:**

| ECI Value | Assessment | Governance Response |
|-----------|-----------|-------------------|
| 0.8 - 1.0 | Coherent evolution | Repos mature together; stable foundations |
| 0.5 - 0.8 | Partial coherence | Some maturity mismatches; monitor dependency stability |
| 0.3 - 0.5 | Fragile maturity | GRADUATED repos depend on CANDIDATE repos; stability risk |
| < 0.3 | Incoherent | System maturity is a patchwork; fundamental structural issue |

**Diagnostic case:** If GRADUATED repos primarily depend on other GRADUATED repos (assortative), the evolutionary trajectory is coherent. If GRADUATED repos depend heavily on CANDIDATE repos (disassortative), the system's maturity is fragile -- stable repos rest on unstable foundations.

---

## 3. Orthogonality

### IDX-006: Why Five Indices, Not One

The five indices cover orthogonal dimensions of graph health and must not be collapsed into a single score (Freeman 1978/79 proved that degree, closeness, and betweenness centrality are mathematically independent):

| Index | Dimension | What It Cannot Tell You |
|-------|-----------|------------------------|
| CCI | Governance completeness | Whether the governed components are well-structured |
| DDI | Dependency structure | Whether the system has feedback loops |
| FVI | Information flow | Whether the system is fragile to component failure |
| CRI | Coupling fragility | Whether the system is evolving coherently |
| ECI | Evolutionary coherence | Whether governance coverage is complete |

A system with CCI = 1.0 (fully covered) but DDI = 0.0 (dependency cycle) is governed but structurally broken. A system with DDI = 1.0 (perfect DAG) but FVI = 0.1 (no feedback) is structurally disciplined but cannot sense itself. Collapsing indices loses diagnostic specificity.

---

## 4. Diagnostic Integration

### IDX-007: Heartbeat Integration

The five indices are computed at the slow cadence (INST-HEARTBEAT BEAT-003) and feed into the heartbeat's structural health dimension. The structural health assessment uses the minimum index value as a conservative diagnostic:

```
structural_health_index = min(CCI, DDI, FVI, 1 - CRI, ECI)
```

### IDX-008: Structural Interrogation Integration

SPEC-009's Structure (DIAG-003) and Relation (DIAG-006) dimensions consume the graph indices as quantitative diagnostics:

| Interrogation Dimension | Indices Used |
|------------------------|-------------|
| Structure (DIAG-003) | DDI (dependency discipline), CCI (coverage) |
| Relation (DIAG-006) | CRI (coupling risk), FVI (feedback vitality), ECI (coherence) |

### IDX-009: Threshold Governance

Each index has configurable thresholds that trigger escalation per SPEC-015:

| Index | Green | Yellow | Red |
|-------|-------|--------|-----|
| CCI | >= 0.95 | 0.80 - 0.95 | < 0.80 |
| DDI | >= 0.70 | 0.40 - 0.70 | < 0.40 or cycle |
| FVI | >= 0.50 | 0.30 - 0.50 | < 0.30 |
| CRI | < 0.30 | 0.30 - 0.50 | > 0.50 |
| ECI | >= 0.50 | 0.30 - 0.50 | < 0.30 |

Thresholds are parameter-level interventions (Meadows level 12) and may be tuned through constrained extension.

---

## 5. Computational Considerations

### IDX-010: Tractability

At ORGANVM's current scale (112 nodes, hundreds of edges), all five indices are computationally tractable:

| Operation | Complexity | Estimated Time (112 nodes) |
|-----------|-----------|---------------------------|
| Cycle detection (DDI) | O(V + E) | < 1ms |
| Centrality computation (DDI, CRI, ECI) | O(V * E) | < 100ms |
| Clustering coefficient (FVI) | O(V * k^2) where k = avg degree | < 100ms |
| Community detection (FVI) | O(E * log V) (Louvain) | < 100ms |
| Resilience simulation (CRI) | O(100 * V * E) (100 trials) | < 10s |

At significantly larger scale (1000+ nodes), betweenness centrality and resilience simulation would require approximation algorithms. This is not a current concern.

---

## 6. Implementation Status

| Component | Status | Location |
|-----------|--------|----------|
| CCI computation | PARTIAL | Seed coverage in `organvm-engine/src/organvm_engine/seed/discover.py`; full CCI not aggregated |
| DDI computation | PARTIAL | DAG validation in `governance/dependency_graph.py`; centrality not computed |
| FVI computation | MISSING | Target: `organvm-engine/src/organvm_engine/graph/indices.py` |
| CRI computation | MISSING | Target: `organvm-engine/src/organvm_engine/graph/indices.py` |
| ECI computation | MISSING | Target: `organvm-engine/src/organvm_engine/graph/indices.py` |
| Index dashboard | MISSING | Target: `/graph/indices/` route in system-dashboard |
| Index CLI | MISSING | Target: `organvm graph indices [--json]` |

---

## 7. Failure Modes

| Failure | Violated Element | Detection |
|---------|-----------------|-----------|
| Index not computed within cadence window | IDX-007 | Heartbeat freshness check |
| Threshold crossed without escalation | IDX-009 | Escalation audit: compare index values against threshold table |
| Single index masking multi-dimensional failure | IDX-006 | Orthogonality enforced by maintaining all five separately |
| Resilience simulation producing non-deterministic results | IDX-004 | Averaged over 100 trials; report confidence interval |
| Community detection misaligned with organ partition | IDX-003 | Review: misalignment may indicate organic structure diverging from constitutional structure |

---

## 8. Evolution Constraints

INST-GRAPH-INDICES may be amended through the governed process defined in SPEC-000 Section 9. New indices may be added (constrained extension) but the five existing indices may not be removed. Index formulas may be refined (weight adjustments, threshold tuning). The central theorem (acyclic dependencies, cyclic information flow) is constitutive and may not be weakened. Thresholds are tunable parameters; formulas are structural constraints; the central theorem is paradigmatic.

---

## 9. Traceability

```
SPEC-000 AX-000-004 (Constitutional Governance) → IDX-001 (CCI measures governance coverage)
SPEC-000 AX-000-008 (Multiplex Flow Governance) → IDX-002/003 (DDI/FVI measure discipline per edge family)
SPEC-000 INV-000-001 (Dependency Acyclicity) → IDX-002 (DDI includes DAG validation as veto)
SPEC-000 INV-000-005 (Observability) → IDX-003 (FVI measures information flow enabling self-observation)
SPEC-006 (Architecture Document) → IDX-001/002 (CCI/DDI measure architectural health)
SPEC-008 (Evolution & Migration Law) → IDX-005 (ECI measures evolutionary coherence under change)
INST-HEARTBEAT → IDX-007 (indices feed heartbeat structural health dimension)
SPEC-009 (Structural Interrogation) → IDX-008 (indices consumed by Structure and Relation dimensions)
```

Full grounding narrative: `post-flood/specs/graph-indices/grounding.md` (3,141 words)
Full risk register: `post-flood/specs/graph-indices/risk-register.md` (6 classified claims)
Full bibliography: `post-flood/specs/bibliography.bib`
