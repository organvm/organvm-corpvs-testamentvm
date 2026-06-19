# 27: The Hybrid Topology Law (Effective vs. Nominal Coupling)

**Date:** 2026-06-19
**Status:** ACTIVE — architectural law; applies to all 149 repos across the eight-organ system
**Authority:** META — system-wide architectural invariant
**Derived from:** Codification of existing law per RP-03 §4.6 (SGO research programme, commission INQ-2026-013 Wave 2). Sources: RP-03 §§6.1–6.4 (rhizomatic/hierarchical topology), SYN-02 §4.2 (designed vs. emergent structure).
**Closes:** IRF-RES-011 (GH#341)
**Complements:** `docs/adr/005-unidirectional-dependency-flow.md` (the inter-organ DAG it generalizes), `docs/standards/13-organ-identity-and-placement.md` (organ boundaries), `docs/standards/15-three-pure-systems.md`
**Downstream:** IRF-RES-021 (stigmergic infrastructure), IRF-RES-024 (designed vs. emergent hierarchy), IRF-RES-029 (VSM recursion), IRF-RES-043 (panarchy phase transitions), IRF-RES-046 (rhizomaticity index R(G))

---

## 1. Purpose & Scope

This document codifies, as durable architectural law, a principle the ORGANVM system has practiced since Phase -1 but never named in one place: **the system is hierarchical between organs and rhizomatic within them.** It is a *hybrid* topology, not a uniform one.

ADR-005 already enforces the inter-organ half — the strict `ORGAN-I → ORGAN-II → ORGAN-III` DAG with no back-edges. What ADR-005 does *not* state is that this hierarchy is deliberately confined to the inter-organ boundary, and that the opposite regime — dense, lateral, cyclic connectivity — is not merely tolerated but *required* inside each organ. This document states both halves as one law and supplies the analytic instrument that makes the law enforceable: the distinction between **nominal coupling** (what the architecture declares) and **effective coupling** (what actually co-varies at runtime).

Scope: every repository, every cross-repo edge, every event subscription, and every shared substrate in the eight-organ system. The law governs *where* coupling may be dense, *where* it must be sparse, and *how* the declared graph must relate to the realized one.

---

## 2. The Two Regimes

ORGANVM runs two topological regimes simultaneously, separated by the organ boundary.

### 2.1 Inter-organ: Hierarchical (the compression axis)

Between organs, flow is a strict Directed Acyclic Graph: `I (Theory) → II (Art) → III (Commerce)`, with ORGAN-IV orchestrating and V/VI/VII consuming outputs (ADR-005). The hierarchy is **designed, acyclic, unidirectional, and legible**.

Its purpose is **compression**. A tree of depth *d* over *n* nodes is describable in O(*n*) and navigable in O(log *n*). Hierarchy collapses a 149-repo system into a comprehensible directed flow: *think → make → ship*. Compression buys legibility (a grant reviewer can trace the system), auditability (CI can validate the whole graph), and bounded blast radius (a break in III cannot cascade to I).

### 2.2 Intra-organ: Rhizomatic (the search axis)

Within an organ, repos connect laterally and non-hierarchically — the Deleuze–Guattari rhizome: any point may connect to any other, connections are dense and redundant, and the structure has no privileged root. ORGAN-II's generative-art repos cross-pollinate freely; ORGAN-I's theory repos cite one another in cycles.

Its purpose is **search**. Dense lateral connectivity maximizes the number of paths between ideas, which is exactly what creative recombination, resilience to node loss, and emergence require. A rhizome explores; a hierarchy cannot.

### 2.3 Why both

A pure hierarchy cannot explore — it has one path between any two nodes and rigid flow. A pure rhizome cannot be governed at scale — it is a tangle with no audit surface and no bounded blast radius. The hybrid extracts **compression across domains** and **search within them**. This is the compression/search principle: *hierarchy between organs for legibility; rhizome within organs for emergence.*

| | Inter-organ | Intra-organ |
|---|---|---|
| Topology | Hierarchical DAG | Rhizomatic mesh |
| Cycles | Forbidden | Permitted |
| Optimizes for | Compression (legibility, audit, bounded blast radius) | Search (emergence, resilience, recombination) |
| Enforced by | `validate-dependencies.yml` (DAG check) | `R(G)` rhizomaticity index (IRF-RES-046) |

---

## 3. Effective vs. Nominal Coupling

The two regimes cannot be governed without distinguishing two kinds of coupling, because the declared graph and the realized graph are not the same graph.

**Nominal coupling** is what the architecture *declares*: the `dependencies` arrays in `repo-registry.json`, the `produces`/`consumes` edges in each `seed.yaml`, the I→II→III DAG. Nominal coupling is explicit, validated, and — at the inter-organ boundary — acyclic by law.

**Effective coupling** is what actually *co-varies at runtime*: shared stigmergic substrates (the registry, the dashboard, the IRF), event pub/sub (Redis channels), shared semantic memory (ChromaDB), common governance artifacts (CLAUDE.md, governance-rules.json), and shared human attention. Effective coupling is frequently far denser than nominal, and it need not be acyclic.

The two diverge by design. A repo with an empty `dependencies` array (zero *nominal* coupling) may still be tightly *effectively* coupled to its siblings through a shared event channel and a common dashboard. **The law is not "minimize coupling." The law governs how nominal and effective coupling may diverge in each regime.**

---

## 4. The Law

The hybrid topology law is the pairing of the two regimes (§2) with the coupling distinction (§3). Stated as enforceable invariants:

- **HTL-1 — Inter-organ nominal coupling MUST be a DAG.** No cycles, no back-edges across organ boundaries. (Subsumes and generalizes ADR-005; the validator is `validate-dependencies.yml`.)

- **HTL-2 — Intra-organ coupling MAY be rhizomatic.** Within a single organ, both nominal and effective coupling may be lateral, dense, and cyclic. Cycles inside an organ are not violations — they are how the search regime works.

- **HTL-3 — Effective coupling that crosses an organ boundary MUST surface as nominal coupling.** No hidden inter-organ dependency. If repos in organ A actually depend at runtime on artifacts produced by organ B, that coupling MUST be declared as a nominal edge (registry `dependencies` and/or `seed.yaml` `consumes`) and MUST respect the DAG direction. This is the bridge that keeps the hierarchy honest: the compression guarantee holds only if no undeclared cross-organ effective coupling exists to subvert it.

- **HTL-4 — The nominal/effective relation inverts at the boundary.**
  - *Across organs:* nominal ⊇ effective. The declared edge set must **cover** every realized cross-organ dependency. Cross-organ effective coupling beyond what is declared is a defect (it is exactly the hidden coupling HTL-3 forbids).
  - *Within an organ:* nominal ⊆ effective. The rhizome is permitted to realize **more** couplings than are declared. Undeclared intra-organ effective coupling is not a defect — it is emergence, and over-declaring it would re-impose the hierarchy the rhizome exists to avoid.

- **HTL-5 — Designed and emergent hierarchy are distinct and tracked separately.** The inter-organ hierarchy is *designed*. A flat intra-organ domain may nonetheless grow an *emergent* hub-and-spoke structure (a de-facto flagship every sibling depends on). Emergent hierarchy is not forbidden, but it MUST be observed rather than assumed — monitor centrality distribution over time (SYN-02 §2.2; tracked by IRF-RES-024). An emergent intra-organ hub is a signal, not a violation; an undeclared cross-organ hub is a HTL-3 violation.

---

## 5. Enforcement & Measurement

| Invariant | Substrate it governs | Mechanism | State |
|-----------|---------------------|-----------|-------|
| HTL-1 | Inter-organ `dependencies` (registry) | `validate-dependencies.yml` — cycle, back-edge, max-depth checks | ACTIVE (ADR-005) |
| HTL-2 | Intra-organ edges | No DAG constraint applied within an organ; permitted by exclusion from HTL-1 | ACTIVE |
| HTL-3 | Runtime cross-organ coupling | Audit realized event/substrate coupling against declared edges; any cross-organ effective edge without a matching nominal edge is a finding | PLANNED — depends on effective-coupling instrumentation (IRF-RES-021 stigmergic layer) |
| HTL-4 | Nominal vs. effective edge sets | Set-cover check across the boundary (nominal ⊇ effective inter; nominal ⊆ effective intra) | PLANNED — pairs with HTL-3 instrumentation |
| HTL-5 | Centrality distribution per organ | `R(G)` rhizomaticity index — clustering coefficient, path length, power-law exponent, centrality inequality, modularity | PLANNED (IRF-RES-046, IRF-RES-024) |

**Nominal coupling** is measured today: the registry DAG is machine-validated on every push. **Effective coupling** is not yet instrumented — measuring it is the work item IRF-RES-021 (build the stigmergic infrastructure layer) and IRF-RES-046 (the R(G) index). Until that instrumentation exists, HTL-3/HTL-4 are enforced by review rather than by CI; this document is the standard that review cites.

---

## 6. Consequences

**Positive.** The hierarchy stays legible because HTL-3 forbids hidden cross-organ coupling — the compression guarantee is real, not nominal-only. The rhizome stays free because HTL-2/HTL-4 explicitly license dense, undeclared, cyclic coupling *within* an organ. The effective/nominal distinction gives a precise name to a previously implicit failure mode: a system that *looks* like a clean DAG on paper while being a tangle at runtime.

**Negative / tensions.**
- HTL-3 and HTL-4 cannot be CI-enforced until effective coupling is instrumented (IRF-RES-021). Until then they are review-grade law, not gate-grade.
- The intra/inter boundary is only as crisp as organ assignment (`docs/standards/13-organ-identity-and-placement.md`). A mis-assigned repo can make a legitimate intra-organ rhizome look like an illegal cross-organ cycle, or hide a real cross-organ coupling inside an apparent rhizome.
- HTL-5 requires longitudinal observation; a one-shot snapshot cannot distinguish designed from emergent hierarchy.

---

## 7. Relationship to Prior Law

This standard does not supersede ADR-005; it generalizes it. ADR-005 remains the canonical decision record and CI contract for inter-organ nominal coupling (HTL-1). This document adds three things ADR-005 lacks: (1) the explicit statement that the DAG is confined to the inter-organ boundary, (2) the rhizomatic regime as co-equal law within organs, and (3) the effective/nominal coupling distinction that makes both regimes auditable. Where ADR-005 says "no back-edges," this law says *why* (compression) and *where the rule stops* (the organ boundary), and *what replaces it inside* (search).

---

*Codified 2026-06-19 — IRF-RES-011 / GH#341. Per the AI-conductor model, the principle was practiced before it was named; this document makes the practice law.*
