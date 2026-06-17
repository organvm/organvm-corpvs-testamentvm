# ORGAN-III Multi-Product Interference Model

**Date:** 2026-06-15
**Status:** EVALUATION — models how the 33 ORGAN-III product repos interact under shared orchestration and shared infrastructure
**Derived from:** Four-branch synthesis report (intra-organ interaction gap); ADR-005 (unidirectional flow)
**Complements:** `docs/standards/27-logos-bypass-feedback-routing.md`, `docs/standards/29-external-dependency-policy.md`
**Resolves:** GH#103

---

## 1. The principle

**Products in the same organ are siblings, not strangers — they share an organ, an orchestrator, and infrastructure, but they do not share code.** The acyclic dependency rule applies *within* ORGAN-III exactly as it applies between organs: products may declare `produces`/`consumes` edges to each other, but those edges must never form a cycle, and they must never collapse two products into one repo. Interference is real; it is managed through declared edges and a bandwidth model, not through merging.

## 2. The problem: 33 products, no interaction model

ORGAN-III now holds 33 product repos (per `repo-registry.json`). Each was documented as a standalone product, but nothing modeled how they *interact* — and they unavoidably do, in two ways the governance corpus had not addressed:

1. They contend for the same finite **ORGAN-IV orchestration bandwidth** (one dispatch surface, many products wanting attention).
2. They face the same pull toward **shared infrastructure** (billing, auth, database) that single-repo-per-product appears to forbid.

This evaluation models both, plus the two edge-semantics questions the issue raises.

## 3. Audit of intra-ORGAN-III edges (registry tier)

Audited from `repo-registry.json` dependency fields, 2026-06-15:

| Source product | Edge | Target |
|----------------|------|--------|
| `classroom-rpg-aetheria` | `consumes` | `organvm-iii-ergon/gamified-coach-interface` |

**Finding: exactly one declared intra-ORGAN-III dependency edge exists — and it is a remediation risk, not a healthy edge.** `classroom-rpg-aetheria` (ACTIVE/DEPLOYED) consumes `organvm-iii-ergon/gamified-coach-interface`, but that target is **ARCHIVED** ("Dissolved to materia-collider 2026-03-11" per the registry). An active product therefore depends on a dissolved sibling — a dangling intra-organ edge that should be remediated (re-point to the dissolved component's new home in `materia-collider`, inline the needed capability, or drop the dependency). This is exactly the kind of interference the audit must surface.

A second ORGAN-III edge also warrants correction: `styx-behavioral-commerce` declares a dependency on `organvm-ii-poiesis/styx-behavioral-art` (and `organvm-i-theoria/styx-behavioral-economics-theory`). The II edge is **not** a sanctioned flow — `scripts/v4-dependency-validation.py` explicitly flags `organvm-iii-ergon → organvm-ii-poiesis` as a **BACK-EDGE** (the dependency points against the I→II→III order; a *consumes* edge must not run III→II). It is one of the repo's pre-existing dependency violations and should be resolved either by promoting the needed `styx-behavioral-art` output through the proper flow or by routing the dependency via the Logos Bypass (std 27) rather than a structural edge. **Teams should not treat this edge as a template for new cross-organ dependencies** — the validator will reject `III → II`.

The practical reading: today's *declared* intra/cross-organ edges are few but already include one dangling-to-archived edge and one flagged back-edge; the larger interference is *implicit* (bandwidth and infrastructure contention), modeled below.

## 4. Open question — orchestration bandwidth contention

**Do multiple products compete for ORGAN-IV orchestration bandwidth? Yes — and it should be modeled as a finite resource with a priority queue.**

ORGAN-IV exposes one dispatch surface. When several products need orchestration at once (a deploy, a coordinated external-dependency fix, a casting request), they contend for it. Treat dispatch bandwidth as a **finite-bandwidth resource** and govern access with an explicit queue rather than first-come scrambling:

- **Priority tiers.** Rank pending dispatches by product state, with `revenue-blocking` work outranking `deploy-blocking`, which outranks `degraded`, which outranks `cosmetic` — reusing the criticality vocabulary already defined for external dependencies (`docs/standards/29-external-dependency-policy.md` §5). A revenue proof-point product in production preempts a pre-launch experiment.
- **Fair-share floor.** Within a tier, round-robin across products so a single noisy product cannot starve its siblings.
- **Coalescing.** When N products request the *same* coordinated action (e.g. a shared-dependency remediation), ORGAN-IV fans one fix across all N rather than queuing N separate jobs — the same fan-out logic std 29 §Q3 describes for external-service changes.

This makes contention observable (a queue you can inspect) instead of emergent (whichever product shouted last).

## 5. Open question — shared infrastructure vs. single-repo-per-product

**Can products share a DB, auth, or billing without violating single-repo-per-product? Yes — via a shared-services repo, declared as `consumes` edges, never code-merged.**

The single-repo-per-product invariant forbids *merging two products into one repo*. It does **not** forbid a product depending on a shared service that lives in its own repo. The recommended pattern:

- A dedicated **shared-services repo** acts as the billing/orchestration hub for the organ. `ergon-prime--business-orchestrator` (GH#100; registered in the registry as the ORGAN-III ENGINE/orchestration layer) is exactly this: a hub coordinating product operations, billing, and cross-product workflows.
- Products that use the hub declare it as a `consumes` edge in seed.yaml — the same declared-edge mechanism used everywhere else. The shared service is *depended upon*, not *absorbed*.
- The hard rule: **shared services are consumed across a repo boundary, never copied into the product.** No code-merge. If billing logic appears inside three product repos, the invariant is violated; if three products each declare `consumes: ergon-prime--business-orchestrator`, it is honored.

This keeps each product a single coherent repo while letting the organ amortize billing/auth/DB across the portfolio — and, because the sharing is declared, an audit can answer "which products depend on the billing hub?" mechanically.

## 6. Open question — intra-organ vs. cross-organ edges

**Both kinds of edge obey acyclicity; the difference is scope, not rule.**

- **Cross-organ edges** follow the global directional law I→II→III with no back-edges (ADR-005). `styx-behavioral-commerce → ORGAN-I/ORGAN-II` is the canonical example: commerce consuming theory and art, never the reverse.
- **Intra-organ edges** (product → product within ORGAN-III) are *permitted* but constrained by the same acyclicity requirement: they must not create a cycle among ORGAN-III repos. The lone existing edge (`classroom-rpg-aetheria → gamified-coach-interface`, §3) is acyclic and therefore valid.

There is no separate "intra-organ rule" — there is one acyclicity invariant applied at two scopes. An acyclicity validator treats the whole declared graph (minus `source: EXTERNAL` edges, per std 29 §5) uniformly. Practically: a new intra-ORGAN-III edge is fine as long as it does not let product A transitively depend on itself through product B.

## 7. Open question — two products, one upstream artifact

**When two products consume the same ORGAN-I artifact, they may diverge in usage but must not fork the artifact; divergence pressure routes upstream via the Logos Bypass.**

Two ORGAN-III products consuming the same ORGAN-I primitive will inevitably use it differently — different parameters, different edge cases, different real-world friction. This is allowed: **divergence in *usage* is normal; divergence in the *artifact* is forbidden.** Neither product may fork the upstream primitive into a private copy, because two forks of one truth is the cycle-laundering ADR-005 exists to prevent (each product would then carry hidden, unreconciled theory).

When the divergence becomes pressure — both products straining the same primitive in incompatible directions — that pressure is a signal, and it routes upstream through the **Logos Bypass** (`docs/standards/27-logos-bypass-feedback-routing.md`): articulate the friction (V), pressure-test it (VI), stage it in `intake/market/`, and let ORGAN-I decide whether to revise the primitive. The products keep consuming the single shared artifact; the *question* of whether it should change flows upstream semantically, not as a fork or a back-edge.

## 8. Acceptance criteria (proposed-research checklist)

The issue's proposed-research checklist, with current status:

- [x] **Registry-tier audit of intra-ORGAN-III edges** — complete: exactly 1 intra-organ edge found (`classroom-rpg-aetheria → gamified-coach-interface`), acyclic; styx edges confirmed cross-organ (§3).
- [x] **Bandwidth-contention model** — proposed: finite-resource dispatch with criticality-tiered priority queue, fair-share floor, and coalescing (§4).
- [x] **Shared-infrastructure model** — proposed: shared-services repo pattern (`ergon-prime`, GH#100), consumed via declared edges, never code-merged (§5).
- [x] **Edge-semantics clarification** — intra- and cross-organ edges obey one acyclicity invariant at two scopes (§6).
- [x] **Shared-artifact divergence model** — diverge in usage, never fork; pressure routes via Logos Bypass (§7).
- [~] **Per-repo `seed.yaml` file audit** — **deferred** follow-up: the registry-tier audit above reads declared `dependencies` in `repo-registry.json`; a definitive intra-organ edge map requires reading each of the 33 ORGAN-III repos' `seed.yaml` files directly (needs read access to each repo). Tracked as an IRF follow-up.

## 9. Cross-references

- **GH#100 (`ergon-prime--business-orchestrator`)** — the shared-services / billing hub recommended in §5.
- **GH#104 / `docs/standards/29-external-dependency-policy.md`** — external `source: EXTERNAL` edges (excluded from intra-organ acyclicity checks) and the criticality vocabulary reused in §4.
- **`docs/standards/27-logos-bypass-feedback-routing.md`** — the upstream channel for shared-artifact divergence pressure (§7).
- **ADR-005** (`docs/adr/005-unidirectional-dependency-flow.md`) — the acyclicity invariant applied at both scopes (§6).
