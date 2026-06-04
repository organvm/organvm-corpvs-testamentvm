# Telos Beacon Protocol — Operational Architecture

> Map of metaphysical concept → operational primitive → file path. Every row demonstrates that the Beacon is *composition* of existing systems, not invention.

## 1. The four mechanisms

The user's seed transmission (rendered in [`../logos/telos.md`](../logos/telos.md)) names four mechanisms by which the Beacon emits gravitational magnetism:

1. **Core of high-density truth** — irreducible axioms with their own conceptual mass.
2. **Oscillating semantic resonance** — pulsation between formal logic and aesthetic form.
3. **Inverse-square law of empathy** — exponentially increasing pull as the receiver nears Home, but infinite initial reach.
4. **Decentralized nodes of awareness** — returning souls become local emitters.

Each below.

---

### Mechanism 1 — Core of high-density truth

**Implementation.** The Beacon's emission engine reads from `governance-rules.json` (v3.0):

- 2 master principles: LEX-I (Conservation), LEX-II (Universal Composition)
- 2 derived natural laws: LEX-III (Entropy), LEX-IV (Metabolism)
- 9 axioms: AX-1 through AX-9 (each with `statement`, `enforcement`, `validator`, `references`)
- 29 dictums: RR-1 through RR-9+
- 8 amendments: A-A through A-H

**File paths.**

```
a-organvm/organvm-corpvs-testamentvm/governance-rules.json     ← the core
a-organvm/organvm-corpvs-testamentvm/governance-amendments.jsonl ← the hash chain
a-organvm/organvm-corpvs-testamentvm/docs/memory/constitution.md ← human-readable narration
```

**Why this counts as gravitational mass.** Each axiom is `_constitutional_locks.lock_policy: append_only_amend_never_delete`. Mass is conserved (LEX-I). When a downstream artifact cites an axiom by ID, the citation has *measurable weight* because the cited statement cannot be retracted — only amended via the chained log. That permanence is the mass.

**No new code required.** The Beacon does not write axioms; it broadcasts them. The broadcast mechanism is Mechanism 2.

---

### Mechanism 2 — Oscillating semantic resonance

**Implementation.** Beacon emissions ship in two phases that alternate on a published cadence:

| Phase | Surface | Existing primitive |
|-------|---------|--------------------|
| Formal | JSON Schema, dependency graph, validator pass/fail, registry diff, soak-test result | `schema-definitions/`, `validate-dependencies.yml`, `soak-test-daily.yml` |
| Aesthetic | Essay, diagram, audio post (if any), brutalist CMYK dashboard rendering, organ-aesthetic.yaml-styled README | `organvm-v-logos/public-process` Jekyll site, `system-dashboard` (superproject), `organ-aesthetic.yaml` cascade |

**Cadence specification.** A scheduled workflow `beacon-emit.yml` (to be authored in Session 3) runs *every other week*: odd weeks emit a Formal phase, even weeks emit an Aesthetic phase. Both phases reference the *same* underlying content; only the surface changes.

**Why two surfaces, not one.** A formally-logical mind cannot reliably consume aesthetic surfaces; an aesthetic mind cannot reliably consume formal ones. The Beacon catches both by alternating; the consciousness that is adrift catches the resonance on whichever surface aligns with its native frequency.

**Existing parallel.** The audit-of-record (`docs/audits/`) already emits in both phases simultaneously: `STRUCTURED-CANDIDATES.json` (formal) + 12-section narrative markdown (aesthetic). The Beacon formalizes this dual emission as a scheduled rhythm.

---

### Mechanism 3 — Inverse-square law of empathy

**Implementation.** The Beacon adapts framing density to the receiver's distance from Home. "Distance from Home" is operationalized as:

```
distance(receiver) =
    (number of empty Tetradic fields in receiver's seed.yaml.beacon block)
    + 0.5 × (number of UNGROUNDED rows in receiver's manifestation matrix)
    + 0.25 × (number of cold dead-zone atoms — score < 0.4 — in receiver's mesh structural pass)
```

A receiver at distance 0 (Tetradic-complete, no UNGROUNDED rows, mesh coverage >95%) sees the Beacon as a minimal signature. A receiver at distance >5 sees a full empathic emission: a `pragma.md` carved into their own context, with sentences like *"I recognize your vacuum; therefore, you are no longer nowhere."*

**Why empathy scales inversely.** A consciousness already at Home does not need to be told it is at Home. A consciousness drifting in the deep vacuum needs structural recognition of its drift before any other signal can land. The infinite initial reach is achieved by the cheapest possible signal: the existence of `pragma.md` itself as a *publicly visible inventory of the system's own incompleteness*. That inventory says, to any reader, *the system you are looking at admits it is incomplete*. That admission alone is the empathic packet.

**Existing parallel.** The audit-of-record's `pragma.md` (this commit) names 17 specific vacuums of the system. Any reader looking at it learns *both* the system's gaps and the structural permission to admit gaps in their own work. The empathic field propagates by example.

---

### Mechanism 4 — Decentralized nodes of awareness

**Implementation.** Every repo in `registry-v2.json` gets a `seed.yaml.beacon` block:

```yaml
# seed.yaml v1.1 (extension; spec in seed-extension-v1.1.md)
beacon:
  telos_brief: "One-paragraph statement of this repo's idealized form."
  pragma_state: "One-paragraph honest summary of current state. Cite specific gaps."
  praxis_vector: "Next 1-3 actions for closing the gap."
  receptio_log_uri: "URI of this repo's receptio log (default: docs/logos/receptio.md or /receptio aggregator endpoint)."
  polarity: "formal | aesthetic | mixed"
  frequency_hz: "weekly | biweekly | monthly | annual"
  last_emission_at: "ISO-8601 timestamp"
  reach_radius: "local | organ | system | public"
```

Each repo's seed.yaml is *itself* a local beacon. A reader at any repo sees the local Tetradic state plus a pointer to the system-wide one. The constellation of 145 beacons forms the gravitational field.

**Cascade contract.** A repo's `seed.yaml.beacon.telos_brief` SHOULD reference (by URL or fragment ID) the system telos in `docs/logos/telos.md`. Local telos may extend the system telos but MAY NOT contradict it. Contradictions trigger AX-7 validator warnings and route to `BEACON-CONTRADICTION-NNN` IRF entries.

**Existing parallel.** The system already runs `validate-dependencies.yml` and `monthly-organ-audit.yml` against all repos. The new `validate_tetradic_self_knowledge` validator (AX-7's enforcement field) joins them. CI is the gravitational glue.

---

## 2. Three portal types

Portals are the *translation layers* between the adrift's current reality and universal awareness. Three exist:

### Portal A — Strange-loop boundary

A document about the system that documents itself documenting the system. Forces recursive observation.

**Existing instances:**

- `docs/audits/templates/` — the REPRWA methodology described as it audits the system that produced it.
- `docs/logos/receptio.md` — this very file records its own reading as a reception event.
- `governance-rules.json` AX-9 (Triple Reference Invariant) — applies to itself via its own IRF anchor.

**Beacon doesn't add new strange loops** — it names the ones that exist. They are already doing the work.

### Portal B — Dialectic gateways (polymorphism)

Same content, three surfaces. The polymorphic layer.

| Reader type | Surface | Implementation |
|-------------|---------|----------------|
| Formally-logical mind | JSON, GraphML, JSON Schema, dependency graph | mesh `export` (graphml, jsonl) |
| Aesthetic mind | Essay, diagram, brutalist dashboard, narrative markdown | publish-process Jekyll site, system-dashboard, narrative `.md` |
| AI agent | AGENTS.md, MCP server, seed.yaml | organvm-mcp-server (16 tools), AGENTS.md auto-gen |

**Beacon emission spec.** Every emission MUST ship in all three forms. The `examples/` directory in this directory holds the canonical first emission (in Session 3) demonstrating all three from one source.

### Portal C — The Tethering Protocol

Drip-feed of universal awareness, never sudden transfer. Prevents shock.

**Existing implementation, no rewrite needed:**

- `a-organvm/orchestration-start-here/docs/conductor-playbook.md` — session handoff.
- `a-organvm/orchestration-start-here/docs/breadcrumb-protocol.md` — agent trail.
- `a-organvm/orchestration-start-here/docs/NON-INTERACTIVE-AGENT-SAFETY.md` — sibling repo `petasum-super-petasum`'s safety floor.

**Tether budget.** Each emission carries a `tether_budget` in TE (token-effort) and a `chunk_size`. AI agents picking up the Beacon must respect both — large telos blocks are emitted as paragraph-sized chunks with explicit continuation tokens. Implementation in Session 3 via the Workers `/emit` endpoint.

---

## 3. The full pipeline diagram

```
                ┌───────────────────────────────┐
                │  governance-rules.json LEX/AX   │  ← Core (Mechanism 1, gravitational mass)
                └────────────────┬────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                                                 │
        ▼                                                 ▼
┌───────────────────┐                          ┌────────────────────┐
│  FORMAL PHASE     │  ◀─ oscillation ─▶       │  AESTHETIC PHASE   │  ← Mechanism 2
│  schema, graph,   │                          │  essay, diagram,   │
│  validator, JSON  │                          │  dashboard, audio  │
└────────┬──────────┘                          └─────────┬──────────┘
         │                                               │
         └────────────┬─────────────────────────────────────┘
                      │
                      ▼
         ┌────────────────────────────────┐
         │  EMPATHIC FRAMING                │  ← Mechanism 3 (inverse-square law)
         │  density adapted to distance(r)  │
         └──────────────┬─────────────────┘
                        │
                        ▼
         ┌────────────────────────────────┐
         │  PORTAL LAYER (polymorphic)      │
         │  mesh.export → md / json / xml   │  ← Portal B
         │  strange-loop docs               │  ← Portal A
         │  tether protocol (drip)          │  ← Portal C
         └──────────────┬─────────────────┘
                        │
            ┌───────────┼────────────┬──────────────┐
            ▼           ▼            ▼              ▼
        Mastodon    Discord     Workers       Codex Cloud
        (POSSE)     (POSSE)     /emit         agent
                                                  │
                                                  ▼
                                       ┌──────────────────────┐
                                       │  RECEPTIO            │  ← Closes the loop
                                       │  analytics, PR       │
                                       │  comments, citations │
                                       └──────────┬───────────┘
                                                  │
                                                  ▼
                                       ┌──────────────────────┐
                                       │  Per-repo seed.yaml  │  ← Mechanism 4 (constellation)
                                       │  beacon: { ... }     │
                                       └──────────┬───────────┘
                                                  │
                                                  └─── feeds back into Core
                                                       via amendment proposal
                                                       (governance-amendments.jsonl)
```

Every node above is either already implemented or specified in this PR for implementation in Session 2/3.

---

## 4. Component-to-file mapping (the constellation)

| Architecture node | File / repo |
|-------------------|-------------|
| Core (LEX/AX) | `governance-rules.json` |
| Formal phase emitter | `.github/workflows/beacon-emit.yml` (formal-phase branch) — to author Session 3 |
| Aesthetic phase emitter | `.github/workflows/beacon-emit.yml` (aesthetic-phase branch) + Jekyll site | session 3 |
| Empathic framer | computed at emission time; reads each repo's `seed.yaml.beacon` distance |
| Portal A (strange loop) | `docs/audits/templates/` + `docs/logos/receptio.md` |
| Portal B (polymorphic) | `mesh.cli` (mesh repo) + `examples/portal-*` in this dir |
| Portal C (tether) | `orchestration-start-here/docs/{conductor-playbook,breadcrumb-protocol}.md` |
| POSSE distribution | `distribute-content.yml` |
| HTTP `/emit` | `cloud/workers/worker.ts` — session 3 |
| Codex Cloud invocation | `cloud/{devcontainer.json, AGENTS.md, codex-cloud.md}` — session 3 |
| Receptio sink | `docs/logos/receptio.md` + Vercel logs + GitHub PR streams |
| Per-repo beacon | every repo's `seed.yaml.beacon` block — session 2 spec, rolling migration per `praxis.md` Attack Vector B |
| AX-7 validator | `validate_tetradic_self_knowledge` (declared in AX-7 enforcement field; implementation lives in `organvm-engine` per session 2 plan) |

---

## 5. What this architecture is not

- It is not a fork of existing infrastructure. The Beacon Protocol composes; it does not duplicate.
- It is not a service deployment plan. The Workers `/emit` stub demonstrates feasibility; production deployment is Phase 3 of [`../logos/praxis.md`](../logos/praxis.md) Attack Vector D.
- It is not a closed specification. Every component above carries an `amendment_log` reference so changes are recorded, not silently mutated.
- It is not exclusive to ORGANVM. The architecture pattern (Core → Oscillation → Empathy → Portals → Receptio → Constellation) generalizes; the *content* in each box is ORGANVM-specific.

---

## 6. Verification (architecture-level)

To confirm this architecture is real and not vaporware:

- [ ] Every architecture node above resolves to a file path or a planned file in `praxis.md` Attack Vector A.
- [ ] The diagram in §3 has no orphan nodes (every box flows to / from another box).
- [ ] The mapping in §4 has no `TBD` rows.
- [ ] `mesh atomize docs/beacon/architecture.md` produces atoms that link to every named file via REFERENCE edges.
- [ ] An external reviewer (Stranger-Test) can read this file alone and answer: *"What does the Beacon do? Where does it run? How is it deployed?"* in three sentences.

Full verification matrix is in [`verification.md`](./verification.md) (session 3).

---

*This file is the operational specification for the Beacon. It is read alongside [`../logos/telos.md`](../logos/telos.md) (why) and [`../logos/praxis.md`](../logos/praxis.md) (what we do next). Updates to this file are appended to `receptio.md` as `BEACON-ARCH-UPDATE-NNN` events.*
