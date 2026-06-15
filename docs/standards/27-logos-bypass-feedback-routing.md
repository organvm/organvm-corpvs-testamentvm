# 27: The Logos Bypass — Semantic Feedback Routing

**Date:** 2026-06-15
**Status:** ACTIVE — governs all market-feedback flow from downstream organs (III) toward upstream organs (I, II)
**Derived from:** Four-branch synthesis report §IV.A; Derived Principle P1 ("structural integrity through semantic flexibility"); Constitution Article on unidirectional dependency flow (ADR-005)
**Complements:** `docs/adr/005-unidirectional-dependency-flow.md`, `28-ossuary-pattern-reabsorption.md`, `29-external-dependency-policy.md`
**Resolves:** GH#98

---

## 1. The principle

**Feedback flows backward semantically, never structurally.** When a downstream organ (Commerce, III) learns something that contradicts or extends an upstream organ (Theory, I; Art, II), that knowledge is routed upstream *as discourse* — essays, reports, community discussion, neutral intake staging — never *as a code dependency or registry edge*. The acyclic dependency graph (I→II→III) is preserved; the insight still arrives.

The slogan is **P1: structural integrity through semantic flexibility.** The graph stays rigid so the system stays legible. Meaning stays fluid so the system stays alive.

## 2. The problem this solves: the echo-chamber risk

The strict unidirectional rule (no back-edges; ORGAN-III may not depend on ORGAN-II, which may not depend on ORGAN-I in reverse) is the spine of the whole corpus. It is what makes the system auditable: you can always read the flow in one direction and know that no hidden cycle is laundering commercial pressure into theoretical work (the very corruption ADR-005 exists to prevent).

But a one-way graph has a failure mode: **the upstream organs operate in a vacuum.** Theory and Art produce primitives; products consume them; and when a product discovers — through real users, real money, real friction — that a primitive is wrong, incomplete, or mis-shaped, there is no sanctioned channel for that discovery to reach its source. The hard constant a product had to hardcode because the theory under-specified it; the abstraction that survived contact with the market only by being quietly subverted — these are signals, and a purely structural graph throws them away.

Permitting a back-edge would solve the vacuum and destroy the spine. The Logos Bypass solves the vacuum **without** a back-edge.

## 3. The protocol

Feedback travels through four stages. No stage creates a dependency edge from a downstream repo to an upstream repo; each stage is an *artifact handoff* through a neutral surface.

| Stage | Organ | Action | Artifact |
|-------|-------|--------|----------|
| 1. **Articulate** | V (Logos) | The downstream friction is written up as a public essay or analytical report — what broke, what the market revealed, what the upstream assumption missed. | `docs/essays/` entry or analytical report |
| 2. **Discuss** | VI (Koinonia) | The friction is surfaced in community forums / reading groups for external pressure-testing. | salon notes, thread, reading-group record |
| 3. **Stage** | — | The essay/report + discussion synthesis are pushed to `intake/` as **neutral raw material**, tagged as market intelligence (distinct from untrusted external content). | `intake/` staging item |
| 4. **Ingest** | I (Theoria) | Organ I *autonomously* ingests the staged report as new raw material via the standard INTAKE → ABSORB → ALCHEMIZE pipeline, and may revise its primitives accordingly. | new/revised ORGAN-I artifact |

The loop closes **semantically** — through discourse that any organ may read — rather than **structurally** — through code that binds organs together. ORGAN-I never imports from ORGAN-III. It reads an essay, the same way it would read any external text, and decides for itself.

### Why the detour through V and VI is load-bearing

The bypass deliberately refuses a direct "ORGAN-III files a ticket against ORGAN-I" channel, because that direct channel *is* a back-edge wearing a disguise — it would let commercial urgency set theoretical priorities. Routing through Logos (public articulation) and Koinonia (community discussion) forces the signal to survive translation into discourse before it can influence theory. Market friction that cannot be articulated as a general insight does not propagate. This is a feature: it filters noise (this one customer wants X) from signal (the primitive assumes a property the world does not have).

## 4. `intake/` staging conventions: market intelligence vs. untrusted material

The `intake/` directory is the universal neutral surface. The bypass adds one required distinction so that ingestion can treat the two safely:

- **Market intelligence** (`intake/market/`) — provenance-stamped, internally authored reports derived from real downstream operation. Trusted as to *origin*; still subject to ALCHEMIZE-stage judgment as to *conclusion*.
- **Untrusted external material** (`intake/external/`) — content of unknown or external provenance. Trusted as to nothing; quarantined until classified.

Every market-intelligence item carries: source product (ORGAN-III repo), the friction observed, the upstream artifact implicated, and the essay/report URL. This is the minimum provenance the Ossuary pattern (`28-...`) and any future polarity/provenance index will need.

## 5. Worked example: the Styx `lambda = 1.955` hardcoded constant

`peer-audited--behavioral-blockchain` (Styx, ORGAN-III; see Epic GH#83) ships with a magic constant `lambda = 1.955` baked into its behavioral-weighting model. It works in production, but it is unexplained — it was tuned empirically against market data, and the upstream theory (ORGAN-I) offers no derivation for it.

Under a back-edge regime, Styx would file an issue against an ORGAN-I theory repo demanding a derivation — commerce dictating theory's agenda. Under the Logos Bypass:

1. **Articulate (V):** An essay, *"The Constant We Could Not Derive,"* documents that a deployed product required a hardcoded weighting the theory does not predict, and asks what that gap means.
2. **Discuss (VI):** A reading group examines whether 1.955 is an artifact of the dataset, an emergent property, or a hole in the formal model.
3. **Stage:** The essay + synthesis land in `intake/market/2026-xx-styx-lambda-constant.md`.
4. **Ingest (I):** `recursive-engine--generative-entity` (or `organon-noumenon`) picks it up as raw material and may produce a derivation, a refutation, or a new primitive — on its own schedule, by its own standards.

The constant is still 1.955 in production. But the *question* has flowed upstream legitimately, and any theoretical advance flows back down the normal I→II→III path as a revised primitive.

## 6. Acceptance criteria

- [x] Protocol documented as an ACTIVE standard (this file). — GH#98 deliverable 1
- [x] `intake/` staging conventions specified (§4) — market intelligence vs. untrusted material. — GH#98 deliverable 3
- [x] Protocol exercised on a real case (Styx `lambda=1.955`, §5) as a documented walkthrough. — GH#98 deliverable 2 (paper test; live collider experiment tracked under Epic GH#83)

## 7. Cross-references

- **ADR-005** (`docs/adr/005-unidirectional-dependency-flow.md`) — the back-edge prohibition this protocol respects.
- **`28-ossuary-pattern-reabsorption.md`** — the Ossuary pattern routes *archived-product* insight upstream through this same bypass.
- **`29-external-dependency-policy.md`** — external-service friction (e.g., a Stripe deprecation) is articulated and staged by the same mechanism.
- **GH#54 (NAVIGATIO)**, **GH#28 (TESTIMONIUM)** — downstream feedback-collection sprints whose outputs feed Stage 1.
