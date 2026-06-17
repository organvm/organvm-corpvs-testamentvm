# Beacon IA — Index Cross-References

> Map of how the Beacon's namespaces connect to the four classical indices the ORGANVM has been building. Two of the four indices already exist; two are planned. The Beacon does not invent new indices — it weaves into the ones constitutionally promised.

## The four classical indices

| Index | Subject | Status | File |
|-------|---------|:------:|------|
| **Index Rerum Faciendarum** (things-to-be-done) | The universal work registry. Every IRF-XXX-NNN item. | ✅ EXISTS | [`/INST-INDEX-RERUM-FACIENDARUM.md`](../../INST-INDEX-RERUM-FACIENDARUM.md) |
| **Index Locorum** (places) | Repository topology, workspace layout, organ directories. | ✅ EXISTS | [`/INST-INDEX-LOCORUM.md`](../../INST-INDEX-LOCORUM.md) |
| **Index Nominum** (names) | All canonical identifiers — entity UIDs, agent names, person names with explicit role, repo aliases, organ epithets. | ⏳ PLANNED | `/INST-INDEX-NOMINUM.md` (to be authored) |
| **Index Rerum** (ontological things) | Every ontologically distinct artifact in the system — schemas, axioms, dictums, amendments, primitives. | ⏳ PLANNED | `/INST-INDEX-RERUM.md` (to be authored) |

The four together are the system's classical apparatus for being knowable. Until all four exist, the system can be searched for *what to do*, *where things are*, but cannot be searched comprehensively for *who* and *what kinds of thing*.

## How Beacon IDs cross-link

Every `BEACON-NNN` and `TBP-NNN` ID created by the Beacon Protocol participates in the four indices as follows.

### 1 — IRF (Index Rerum Faciendarum)

Every `BEACON-NNN` work-item gets an IRF anchor under a new domain `BEA`:

| IRF anchor pattern | Maps to |
|--------------------|---------|
| `IRF-BEA-001..099` | Attack Vector A items (Logos & Beacon authoring). |
| `IRF-BEA-100..199` | Attack Vector B items (per-repo Tetradic backfill). |
| `IRF-BEA-200..299` | Attack Vector C items (close the 17 pragma vacuums). |
| `IRF-BEA-300..399` | Attack Vector D items (10-phase roadmap). |
| `IRF-BEA-400..499` | Attack Vector E items (failure modes / circuit-breakers). |

The first IRF entries to add (this PR):

- `IRF-BEA-001` — Author docs/logos/{telos,pragma,praxis,receptio}.md and docs/beacon/{README,architecture,ia-schema,ia-indices}.md *(Session 1+2 of this PR)*.
- `IRF-BEA-002` — Author docs/beacon/dam-{pipeline,storage,distribution}.md *(Session 2)*.
- `IRF-BEA-003` — Author docs/beacon/seed-extension-v1.1.md + beacon-schema.json *(Session 2)*.
- `IRF-BEA-004` — Author docs/beacon/cloud/{devcontainer.json, .env.example, AGENTS.md, codex-cloud.md} + workers/ stub *(Session 3)*.
- `IRF-BEA-005` — Author docs/beacon/examples/{beacon-emission.json, portal-markdown.md, portal-graphml.xml} *(Session 3)*.
- `IRF-BEA-006` — Author docs/beacon/verification.md and run 8-point self-check *(Session 3)*.
- `IRF-BEA-101..245` — Per-repo seed.yaml.beacon backfill, one per repo in registry-v2.json.

When IRF entries close, they appear with `DONE-NNN` rows in IRF and `BEACON-PRAXIS-DONE-NNN` rows in `../logos/receptio.md` §III. This enforces AX-9 (Triple Reference Invariant): IRF + repo-level file + GitHub issue.

### 2 — Locorum (Index Locorum)

Every Beacon artifact has a stable file location. Locorum gains the following rows on PR #357 merge:

| Path | Kind | First appears |
|------|------|---------------|
| `docs/logos/` | directory | This PR |
| `docs/logos/README.md` | doc | This PR |
| `docs/logos/telos.md` | doc | This PR |
| `docs/logos/pragma.md` | doc | This PR |
| `docs/logos/praxis.md` | doc | This PR |
| `docs/logos/receptio.md` | doc | This PR |
| `docs/beacon/` | directory | This PR |
| `docs/beacon/README.md` | doc | This PR |
| `docs/beacon/architecture.md` | doc | This PR |
| `docs/beacon/ia-schema.md` | doc | This PR |
| `docs/beacon/ia-indices.md` (this file) | doc | This PR |
| `docs/beacon/dam-{pipeline,storage,distribution}.md` | doc × 3 | This PR |
| `docs/beacon/seed-extension-v1.1.md` | spec | This PR |
| `docs/beacon/beacon-schema.json` | schema | This PR |
| `docs/beacon/cloud/devcontainer.json` | config | Session 3 |
| `docs/beacon/cloud/.env.example` | config | Session 3 |
| `docs/beacon/cloud/AGENTS.md` | config | Session 3 |
| `docs/beacon/cloud/codex-cloud.md` | doc | Session 3 |
| `docs/beacon/cloud/workers/wrangler.toml` | config | Session 3 |
| `docs/beacon/cloud/workers/worker.ts` | code | Session 3 |
| `docs/beacon/cloud/workers/DEPLOY.md` | doc | Session 3 |
| `docs/beacon/examples/beacon-emission.json` | example | Session 3 |
| `docs/beacon/examples/portal-markdown.md` | example | Session 3 |
| `docs/beacon/examples/portal-graphml.xml` | example | Session 3 |
| `docs/beacon/verification.md` | doc | Session 3 |

Each row should be appended to `/INST-INDEX-LOCORUM.md` post-merge.

### 3 — Nominum (Index Nominum) — PLANNED

When Index Nominum is authored (per `praxis.md` BEACON-C-003), the following Beacon-specific names will appear:

- **Identifiers**: `BEACON-NNN`, `BEACON-{LETTER}-NNN`, `BEACON-{SUB}-NNN`, `TBP-NNN`. Each gets a row mapping the ID format to its issuing authority and triple-reference contract.
- **Roles**: `praxis_owner`, `receptio_steward`, `beacon_maintainer`, `tether_observer`. Each defined as a per-repo `seed.yaml.beacon.roles.*` field in the v1.1 schema.
- **Epithets**: every organ has a Greek epithet (Theoria, Poiesis, Ergon, Taxis, Logos, Koinonia, Kerygma, Meta). The Beacon adds an emission-frequency epithet per organ (e.g. Theoria emits annually; Kerygma emits weekly).
- **Entity UIDs**: from `organvm-ontologia`. Beacon-emitted artifacts get UIDs prefixed `ent_beacon_*`.

Stub creation pattern (for the future author):

```markdown
# Index Nominum (planned — IRF-IDX-002)

## I. Identifier formats
- BEACON-NNN — see docs/beacon/ia-schema.md §2
- TBP-NNN    — see docs/beacon/ia-schema.md §2

## II. Roles
- praxis_owner — see docs/beacon/seed-extension-v1.1.md
- ...

## III. Organ epithets
- Theoria — annual emitter
- ...

## IV. Entity UID conventions
- ent_beacon_* — see organvm-ontologia
- ...
```

### 4 — Rerum (Index Rerum) — PLANNED

When Index Rerum is authored (per `praxis.md` BEACON-C-004), the following Beacon-specific kinds of thing will appear:

- **Schemas**: `beacon-schema.json` (this PR), `seed-extension-v1.1` (this PR), the existing `registry-v2.json` schema, `seed.yaml v1.0` schema, `governance-rules.json` schema.
- **Axioms**: AX-7, AX-8, AX-9, plus LEX-I — each as ontological things the Beacon repeatedly cites.
- **Primitives**: the 4 Logos files (telos, pragma, praxis, receptio) as a class. The 5 mesh primitives (seed, crawl, atomize, link, query). The 3 portal types.
- **Workflows**: `beacon-emit.yml` (planned), `validate_tetradic_self_knowledge` (planned). Existing `distribute-content.yml`, `monthly-organ-audit.yml`, `soak-test-daily.yml`.
- **Events**: every `BEACON-{SUB}-NNN` sub-namespace is a kind of event.

Stub creation pattern (for the future author):

```markdown
# Index Rerum (planned — IRF-IDX-003)

## I. Schemas
- beacon-schema.json — docs/beacon/beacon-schema.json
- registry-v2.json   — root
- seed.yaml v1.1     — docs/beacon/seed-extension-v1.1.md
- ...

## II. Axioms cited by the Beacon
- AX-7 Tetradic Self-Knowledge — governance-rules.json
- AX-8 Constructed Polis — governance-rules.json
- AX-9 Triple Reference Invariant — governance-rules.json
- LEX-I Conservation — governance-rules.json
- ...

## III. Primitives
- Logos quartet (telos/pragma/praxis/receptio) — docs/logos/
- mesh primitives (seed/crawl/atomize/link/query) — organvm-i-theoria/mesh
- Portal types (strange-loop, polymorphic-gateway, tether) — docs/beacon/architecture.md
- ...

## IV. Workflows
- beacon-emit.yml — .github/workflows/beacon-emit.yml (planned)
- ...

## V. Events
- BEACON-DRIFT-NNN — telos drift
- BEACON-CONTRADICTION-NNN — local vs system telos conflict
- ...
```

## Closure rule

When all four indices exist and all Beacon items are anchored in each, the Triple Reference Invariant becomes a **Quadruple Reference Invariant** for Beacon-class items: IRF + Locorum + Nominum + Rerum, in addition to the canonical repo-level reference and GitHub issue. The Beacon does not invent this quadruple — it is the natural consequence of completing the four classical indices.

A future amendment `TBP-AMENDMENT-004` will formalise the Quadruple Reference Invariant once Index Nominum and Index Rerum land. Until then, the Triple Reference Invariant from AX-9 is the binding contract.

---

*Updates to this file flow to `../logos/receptio.md` as `BEACON-INDEX-UPDATE-NNN`.*
