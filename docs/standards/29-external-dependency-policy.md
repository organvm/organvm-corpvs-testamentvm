# 29: External Dependency Policy — Third-Party Services in the Unidirectional Model

**Date:** 2026-06-15
**Status:** ACTIVE — governs how external APIs, hosted services, and third-party dependencies relate to the eight-organ dependency graph
**Derived from:** Four-branch synthesis report §VI.4 ("the system is entirely self-referential" gap)
**Complements:** `docs/adr/005-unidirectional-dependency-flow.md`, `27-logos-bypass-feedback-routing.md`, `docs/standards/10-repository-standards.md`
**Resolves:** GH#104

---

## 1. The principle

**External services are honorary Organ-0 inputs: foundational, upstream of everything, and depended-upon by anyone — but never part of the graph's governance.** They sit *below* ORGAN-I the way bedrock sits below a building: every organ may stand on them, and depending on them violates no back-edge rule because they are not organs and have no upstream of their own within the system.

The unidirectional rule (I→II→III, no back-edges) governs *internal* edges between organs. An edge to Stripe or Vercel is **orthogonal** to that rule, not an exception to it — it points out of the system entirely.

## 2. The problem: a system that pretended to be closed

Every governance document treated ORGANVM as self-contained. But ORGAN-III products do not run on theory — they run on Stripe, Vercel, Neon, Cloudflare, Render, Upstash. These services are foundational to whether a product *exists*, yet the model had no concept of them. The `intake/` directory handles external *content*; nothing handled external *services*. A Stripe API deprecation that breaks five products had no representation anywhere in the registry, the seed contracts, or the dependency graph.

## 3. Resolving the open questions

The synthesis report posed four questions. This policy answers each.

### Q1. Are external services honorary ORGAN-I inputs?
**No — they are Organ-0 / `EXTERNAL`, a tier *below* ORGAN-I.** ORGAN-I produces primitives the system *owns and can revise*. External services are primitives the system *rents and cannot revise*. Conflating them would imply Theory could change Stripe's behavior. They get their own designation, `EXTERNAL`, precisely to mark "depended-upon but not governed."

### Q2. Should they be tracked in seed.yaml as `consumes` edges with `source: EXTERNAL`?
**Yes.** This is the chosen mechanism. A repo declares its external dependencies as `consumes` edges carrying a distinguishing `source: EXTERNAL` field:

```yaml
consumes:
  - id: organvm-i-theoria/recursive-engine--generative-entity   # internal edge (governed)
    via: primitive
  - id: stripe                                                   # external edge (orthogonal)
    source: EXTERNAL
    kind: payments
    criticality: revenue-blocking
    failure_mode: "API deprecation halts checkout across subscription products"
```

This keeps external dependencies *visible in the same place* as internal ones (so an audit sees the whole dependency surface) while the `source: EXTERNAL` tag keeps them *out of* acyclicity checks (a tool validating no-back-edges skips `source: EXTERNAL` edges).

### Q3. How do external API changes propagate through the governance model?
Through the **Logos Bypass** (`27-...`), the same way market friction does. An external change (e.g., a Stripe deprecation) is a downstream signal:

1. The affected product(s) observe the breakage.
2. The impact is articulated (which products, which `criticality`).
3. It is staged in `intake/market/` as external-service intelligence.
4. Remediation is coordinated through ORGAN-IV (orchestration), which can fan a single fix across all products sharing the dependency.

Because external edges are declared in seed.yaml, ORGAN-IV can answer "which repos consume Stripe?" mechanically and dispatch one coordinated remediation instead of five uncoordinated ones.

### Q4. Should there be an external-dependency registry parallel to registry-v2.json?
**Not a separate file — a derived view.** Duplicating state into a second registry would violate the single-source-of-truth invariant (`repo-registry.json` is canonical). Instead, the external-dependency registry is *generated* by aggregating every `source: EXTERNAL` edge across all seed.yaml files into a read-only index (e.g., `data/external-dependencies.json`). One writer (the seed files), one derived consumer (the index). This mirrors how the system already treats metrics and context files.

## 4. Audit of current external dependencies (ORGAN-III)

Audited from `repo-registry.json` deployment URLs and revenue models, 2026-06-15. This is a **hosting-and-payments-tier audit from registry metadata**; a per-repo code-level audit (scanning each repo's `package.json` / lockfiles for SDK dependencies) is a follow-up tracked in the IRF.

| External service | Kind | Evidence | Approx. ORGAN-III consumers | Criticality |
|------------------|------|----------|------------------------------|-------------|
| **Netlify** | static/edge hosting | `*.netlify.app` URLs | ≥8 (scrapper, aetheria, trade-perpetual-future, fetch-familiar, sovereign-ecosystem, mirror-mirror, invisible-ledger, elevate-align) | deploy-blocking |
| **Cloudflare Pages** | static/edge hosting | `*.pages.dev` URLs | ≥3 (gamified-coach, the-actual-news, my-block-warfare) | deploy-blocking |
| **GitHub Pages** | static hosting | `*.github.io` URLs | ≥4 (multi-camera, your-fit-tailored, card-trade-social, hokage-chess) | deploy-blocking |
| **Render** | container/web-service hosting | `*.onrender.com` (life-my--midst--in) | ≥1 | deploy-blocking |
| **Stripe** (implied) | payments | every `revenue_model: subscription/freemium/one-time` product requires a payment processor; Stripe is the system default (GH#64) | ≥15 (all monetized products) | revenue-blocking |
| **Neon / Upstash** (planned) | Postgres / Redis | GH#106, GH#63 deployment plans | scrapper + future deployments | revenue-blocking when live |

**Finding:** hosting is fragmented across four providers (Netlify, Cloudflare, GitHub Pages, Render). This is *acceptable* under this policy (no rule mandates a single host), but it raises the coordination cost of any provider-level change. Recommendation logged to IRF: declare these as `source: EXTERNAL` edges in each repo's seed.yaml so the fragmentation becomes queryable rather than archaeological.

## 5. seed.yaml schema update (additive)

Per the No-Deletion Principle (`23-...`), this is purely additive to the existing seed contract schema:

- `consumes[].source: EXTERNAL` — marks an edge as pointing outside the organ system (default for omitted `source` remains internal/governed).
- `consumes[].kind` — service category (`payments`, `hosting`, `database`, `cache`, `auth`, `email`, …).
- `consumes[].criticality` — `revenue-blocking` | `deploy-blocking` | `degraded` | `cosmetic`.
- `consumes[].failure_mode` — one-line description of what breaks if the service changes/disappears.

Acyclicity validators MUST skip edges where `source: EXTERNAL`.

## 6. Acceptance criteria

- [x] Policy document created in the corpus (this file). — GH#104 deliverable 1
- [x] seed.yaml schema update specified to support external dependency declarations (§3 Q2, §5). — GH#104 deliverable 2
- [~] Audit of current external dependencies across ORGAN-III (§4) — **registry-metadata tier complete; per-repo code-level scan deferred** to a follow-up IRF item (requires read access to each ORGAN-III repo's lockfiles). — GH#104 deliverable 3

## 7. Cross-references

- **ADR-005** — the internal back-edge rule this policy is orthogonal to.
- **`27-logos-bypass-feedback-routing.md`** — the channel external-change signals travel.
- **GH#64 (MERCATURA / Stripe)**, **GH#63 (Vercel deploy)**, **GH#106 (first product deploy)** — the concrete external integrations this policy governs.
