# Intent-Routing: The Casting Director Layer

**Date:** 2026-06-15
**Status:** DESIGN PROPOSAL
**Derived from:** Four-branch synthesis report §IV.D ("the director must know the cast by name") and §VI.5 (intent-to-specialist matching gap)
**Complements:** `docs/standards/27-logos-bypass-feedback-routing.md`, ORGAN-IV orchestration (`orchestration-start-here`, `agentic-titan`)
**Resolves:** GH#101

---

## 1. The principle

**A director declares intent; the system casts the specialists.** The orchestration layer should accept a statement of *what needs to happen* and resolve it to *who can make it happen* — without the director memorizing the roster. The director's job is to know the scene they want; the Casting Director's job is to know the cast.

The slogan: **intent in, cast out.** A director should never have to recall that protecting a product means invoking `security-threat-modeler` *and* `contract-risk-analyzer` by name. They say "this project needs protection," and the resolver returns the cast.

## 2. The problem this solves: the named-roster bottleneck

ORGANVM now carries 70+ skills (in `a-i--skills/`) and 22 archetypes (the Titan topologies in `agentic-titan`, ORGAN-IV). Invocation today is *nominal*: a director types `/security-threat-modeler` and must already know (a) that the skill exists, (b) its exact name, and (c) that it is the right specialist for the intent at hand. This scales poorly in three ways:

- **Discovery cost.** A roster of 90+ specialists exceeds what any director holds in working memory. Specialists that are not remembered are not used, however good they are.
- **Composition cost.** Real intents span domains. "Protect this product" is simultaneously a security concern and a legal/contract concern. A nominal interface forces the director to decompose the intent themselves and remember both names.
- **Drift cost.** As the roster grows and renames, every director's mental index goes stale. The knowledge of *who does what* lives in human memory rather than in the system, so it cannot be audited or kept current.

The bottleneck is that **intent-to-specialist mapping is implicit and human-held.** The Casting Director makes it explicit and system-held.

## 3. Recommendation: an ORGAN-IV orchestration feature with a skill front-end

The issue asks whether the Casting Director should be (a) a skill, (b) a Titan topology, or (c) a collider protocol. **Recommendation: build it as an ORGAN-IV orchestration feature, fronted by a thin skill.** Rationale:

- **Why ORGAN-IV owns it.** Casting is a *routing* concern, and routing is ORGAN-IV's domain (orchestration, governance, dispatch). The capability manifest and resolver are infrastructure that all directors share; they belong with `orchestration-start-here` / `agentic-titan`, not duplicated per-caller. This also keeps the manifest co-located with the dispatch-bandwidth model that ORGAN-IV already needs (see `organ-iii-multi-product-interference.md`).
- **Why not a Titan topology alone.** A Titan topology *is* one of the things being cast; making the caster itself a topology conflates the catalog with an entry in it. The resolver should sit *above* the topologies it selects.
- **Why not a collider protocol.** Collider protocols are for adversarial / generative synthesis between organs. Casting is deterministic lookup-and-rank, not synthesis. Using a collider would be over-engineering a problem that keyword overlap solves at the MVP tier.
- **Why a skill front-end.** Directors already live in the `/skill-name` invocation surface. A `/cast` skill is the lowest-friction entry point: it takes the intent string, calls the ORGAN-IV resolver, and presents the proposed cast. The skill is a façade; the logic is orchestration infrastructure.

## 4. Interaction with the existing `/skill-name` pattern

**The Casting Director augments the nominal interface; it does not replace it.** Both coexist:

- A director who *knows* the specialist still types `/security-threat-modeler` directly. Nothing changes for them.
- A director who knows only the *intent* types `/cast "this project needs protection"`. The resolver returns an ordered cast and the director confirms, after which `/cast` expands into the underlying `/skill-name` invocations.

`/cast` is therefore a **resolver over the existing namespace**, not a parallel one. Its output is always a set of concrete `/skill-name` calls — the same calls a director could have typed by hand. This keeps one source of truth for *what a specialist is* (its skill/archetype definition) and adds one new thing (*how intent maps to it*). The expansion is transparent: the director sees exactly which specialists were cast and why, so the layer never becomes an opaque black box between intent and execution.

## 5. The capability manifest (MVP mechanism)

Every skill and archetype declares a small manifest block stating *what it is for*. This is the single new piece of authored data the system needs; everything else is derived from it.

```yaml
# capability manifest — declared per skill/archetype
id: security-threat-modeler
kind: skill                      # skill | archetype
domain: security                 # primary domain
intent_tags:                     # the language a director would use
  - protect
  - protection
  - threat
  - attack-surface
  - vulnerability
  - harden
composes_with:                   # known good co-casts (optional hint)
  - contract-risk-analyzer
  - dependency-auditor
summary: "Models attack surface and threat scenarios for a product or system."
```

```yaml
id: contract-risk-analyzer
kind: skill
domain: legal
intent_tags:
  - protect
  - protection
  - contract
  - liability
  - terms
  - risk
composes_with:
  - security-threat-modeler
summary: "Reviews agreements and terms for liability and obligation risk."
```

The manifests aggregate into a derived index (e.g. `data/capability-manifest.json`), generated from the declarations the same way the external-dependency index is generated from seed.yaml edges (`docs/standards/29-external-dependency-policy.md` §Q4). One writer (the per-specialist declarations), one derived consumer (the resolver). No second source of truth.

## 6. The resolution algorithm

### MVP — keyword / tag overlap (ship first)

1. **Normalize** the intent string: lowercase, strip punctuation, tokenize into terms, expand a small synonym table (`protect → protection, harden, secure`).
2. **Score** each manifest entry by overlap between intent terms and `intent_tags`. Score = count of matched tags, weighted so a domain-name match counts double.
3. **Rank** specialists by score; drop anything scoring zero.
4. **Detect span:** group surviving candidates by `domain`. If the top candidates fall in two or more distinct domains, the intent *spans domains* and the cast is multi-specialist (see §7).
5. **Propose** the ordered cast back to the director via `/cast`, with the matched tags shown as the *reason* for each casting. The director confirms or trims, then the cast expands to `/skill-name` calls.

This is deterministic, debuggable, and requires no model inference — exactly the MVP tier the issue calls for. Its quality is bounded only by how well manifests are tagged, which is a tractable, incremental authoring task.

### V2 — semantic search (second)

Replace step 2's exact-tag overlap with embedding similarity: embed each manifest `summary` + `intent_tags` once, embed the intent string at query time, rank by cosine similarity. This catches intents whose vocabulary does not match any declared tag ("make sure nobody can break in" → `security-threat-modeler`). V2 keeps the *same* manifest and the *same* compose/confirm flow; only the scoring function changes. The MVP keyword path remains as a fast first pass and a fallback when embeddings are unavailable.

## 7. Composition example — an intent spanning two domains

Director input:

```
/cast "this project needs protection"
```

Resolution (MVP path):

| Specialist | Domain | Matched tags | Score |
|------------|--------|--------------|-------|
| `security-threat-modeler` | security | protect, protection | 2 |
| `contract-risk-analyzer` | legal | protect, protection | 2 |
| `dependency-auditor` | security | protect | 1 |

The two top-scoring candidates fall in **two distinct domains** (security, legal), so the resolver flags the intent as domain-spanning and proposes a **composed cast**:

```
Proposed cast for "this project needs protection":
  1. /security-threat-modeler   (security — matched: protect, protection)
  2. /contract-risk-analyzer    (legal    — matched: protect, protection)
Confirm to expand into the two invocations above. [y/trim/cancel]
```

On confirmation, `/cast` expands to the two underlying `/skill-name` invocations. "Protection" correctly resolved to *both* the technical and the legal sense of the word — the composition the nominal interface would have forced the director to assemble by hand. The `composes_with` hints on each manifest corroborate the pairing, raising confidence that the two-specialist cast is coherent rather than coincidental.

## 8. Acceptance criteria

- [x] Design recommends a build site with rationale (ORGAN-IV feature + skill front-end; §3). — GH#101 open question 1
- [x] Interaction with `/skill-name` specified — augments, does not replace; `/cast` expands to concrete `/skill-name` calls (§4). — GH#101 open question 2
- [x] MVP defined as keyword/tag matching with semantic search as V2 (§6). — GH#101 open question 3
- [x] Capability-manifest schema sketched (YAML, §5) with a derived-index generation model matching std 29 §Q4.
- [x] Resolution algorithm specified for both MVP (keyword overlap) and V2 (embeddings) (§6).
- [x] Worked composition example spanning two domains ("protection" → `security-threat-modeler` + `contract-risk-analyzer`, §7).
- [ ] Reference implementation of the resolver in ORGAN-IV — **deferred** to an orchestration follow-up (needs the manifest declarations authored across the 70+ skills / 22 archetypes first).

## 9. Cross-references

- **`docs/standards/29-external-dependency-policy.md`** §Q4 — the derived-index pattern (one writer, one derived consumer) the capability manifest reuses.
- **`docs/standards/27-logos-bypass-feedback-routing.md`** — where a *miscast* (director's intent the roster cannot satisfy) routes as a capability-gap signal.
- **`agentic-titan` / `orchestration-start-here`** (ORGAN-IV) — the topologies and dispatch surface the resolver casts over.
- **`docs/evaluation/organ-iii-multi-product-interference.md`** — the dispatch-bandwidth model the Casting Director shares ORGAN-IV residency with.
- **GH#100 (ergon-prime)** — a concrete consumer: business-orchestration workflows that would cast specialists by intent.
