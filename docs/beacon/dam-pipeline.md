# Beacon DAM — Asset Pipeline

> The Digital Asset Management (DAM) pipeline of the Telos Beacon Protocol. Every stage maps to an *existing* ORGANVM primitive; the Beacon adds one new pipe (the Beacon-emit workflow) and one new sink (the Workers `/emit` endpoint).

## Pipeline stages (Styx progression)

The ORGANVM-canonical asset pipeline runs INTAKE → ABSORB → ALCHEMIZE → ATOMIZE → STORE → EXPORT → DISTRIBUTE → ORCHESTRATE (the Styx pipeline traversal SOP). Beacon emissions ride this exact rail with one prepended stage (CAPTURE-FROM-LOGOS) and one extended sink (HTTP `/emit` + Codex agent).

```
                       (Beacon-specific entry)
┌───────────────────────────────────────┐
│  CAPTURE-FROM-LOGOS                      │
│  Source = docs/logos/{telos,pragma,      │
│           praxis,receptio}.md            │
│  Trigger = beacon-emit.yml (scheduled)   │
└──────────────────┬─────────────────────┘
                   │
                   ▼
       ┌─────────────────────┐
       │  INTAKE               │  ← alchemia-ingestvm `intake`
       │  alchemia intake      │     (existing primitive)
       └───────────┬───────────┘
                   │
                   ▼
       ┌─────────────────────┐
       │  ABSORB               │  ← alchemia-ingestvm `absorb`
       │  alchemia absorb      │     (existing primitive)
       └───────────┬───────────┘
                   │
                   ▼
       ┌─────────────────────┐
       │  ALCHEMIZE            │  ← alchemia-ingestvm `alchemize`
       │  alchemia alchemize   │     (existing primitive)
       └───────────┬───────────┘
                   │
                   ▼
       ┌─────────────────────┐
       │  ATOMIZE              │  ← mesh `atomize` primitive
       │  mesh atomize         │     (existing primitive)
       │  SHA-256 12-char hash │
       └───────────┬───────────┘
                   │
        ┌──────────┼──────────┐
        ▼                     ▼
┌──────────────┐    ┌──────────────────┐
│ STORE (loc.) │    │ STORE (cloud)    │  ← see dam-storage.md
│ SQLite+FTS5  │    │ Cloudflare R2    │
└──────┬───────┘    └────────┬─────────┘
       │                     │
       └──────────┬──────────┘
                  │
                  ▼
       ┌────────────────────────────┐
       │  EXPORT (polymorphic)      │  ← mesh.export (Obsidian/GraphML/JSONL)
       │  + portal-markdown.md      │
       │  + portal-graphml.xml      │
       │  + beacon-emission.json    │
       └────────────┬───────────────┘
                    │
        ┌───────────┼────────────┬──────────────┬─────────────┐
        ▼           ▼            ▼              ▼             ▼
    Mastodon    Discord     newsletter     Workers       Codex Cloud
    (POSSE      (POSSE      (POSSE         /emit         agent
    via         via         via            (new,         (new,
    dist-       dist-       dist-          this PR)      this PR)
    content)    content)    content)
        │           │            │              │             │
        └───────────┴────────────┴──────────────┴─────────────┘
                            │
                            ▼
               ┌──────────────────────┐
               │  RECEPTIO            │  ← receptio.md §III ingest
               │  (closes the loop)   │
               └──────────────────────┘
```

## Stage-by-stage wiring

### CAPTURE-FROM-LOGOS

- **Source**: the four `docs/logos/*.md` files plus selected `docs/beacon/*.md` files referenced from telos.
- **Trigger**: scheduled emission via `.github/workflows/beacon-emit.yml` (to be authored Session 3). Cron: biweekly (alternating Formal / Aesthetic polarity per `ia-schema.md` §1 → Oscillation Phase).
- **Manual trigger**: `workflow_dispatch` for ad-hoc emissions.
- **Inputs**: nothing required. The workflow reads the current HEAD of the Logos directory.
- **Outputs**: a structured payload file `.beacon/payload/{ts}.yaml` consumed by INTAKE.

The capture stage does not transform content. It packages the Logos files plus relevant metadata (current REPRWA pragma counts, current mesh coverage, current `distance(receiver)` table) into a single payload.

### INTAKE — `alchemia intake`

- **Existing primitive**: `meta-organvm/alchemia-ingestvm` CLI command `alchemia intake`.
- **What it does for the Beacon**: accepts the captured payload as a normalised intake record; validates structure; deduplicates against prior captures by content hash.
- **No new code**: invoke as `alchemia intake --source docs/logos/ --emit-channel beacon`. The `--emit-channel` flag is the only Beacon-specific addition; lands as a Session 2 extension to alchemia.

### ABSORB — `alchemia absorb`

- **Existing primitive**: `alchemia absorb`.
- **What it does for the Beacon**: applies the aesthetic-cascade rules from `taste.yaml` → `organ-aesthetic.yaml` (ORGAN-META is the Beacon's organ for system-wide emissions) → repo-aesthetic. Records the absorption with provenance.
- **Result**: each Beacon emission inherits the system-meta aesthetic identity without per-emission styling work.

### ALCHEMIZE — `alchemia alchemize`

- **Existing primitive**: `alchemia alchemize`.
- **What it does for the Beacon**: combines the captured payload with the aesthetic identity into a transformed artifact ready for atomization. This is where polarity is selected.
- **Two outputs** (one per polarity, even when only one channel will be used in this cycle):
  - `payload.formal.json` — structured, schema-validated against `beacon-schema.json`.
  - `payload.aesthetic.md` — narrative markdown styled by ORGAN-META aesthetic.

Both are stored. EXPORT later picks the one matching the cycle's oscillation phase.

### ATOMIZE — `mesh atomize`

- **Existing primitive**: `organvm-i-theoria/mesh` `atomize` primitive (SHA-256 12-char content addressing).
- **What it does for the Beacon**: decomposes each Beacon transmission into article → section → paragraph atoms. Each atom is content-addressed and stored once; subsequent emissions referencing the same content (e.g. AX-7 quotation) reuse the prior atom.
- **Outputs**: atom IDs returned to STORE; edges (REFERENCE, CATEGORY, SEMANTIC, INFLUENCE) inferred via mesh's `link` primitive in the next sub-stage.

### LINK — `mesh link`

- **Existing primitive**: mesh `link` (REFERENCE / CATEGORY / SEMANTIC / INFLUENCE edges).
- **What it does for the Beacon**: connects each new emission's atoms to (a) the seed text in telos.md, (b) the pragma row each claim addresses, (c) the praxis vector that produced the claim, (d) prior emissions on the same topic.
- **Outcome**: the constellation graph (per `architecture.md` §Mechanism 4) updates with new edges, making `distance(receiver)` queryable for each repo.

### STORE — local + cloud

Detail in [`dam-storage.md`](./dam-storage.md). Two sinks:

- **Local**: SQLite + FTS5 via mesh's store/sqlite.py.
- **Cloud**: Cloudflare R2 bucket for emission artifacts; KV namespace for atom-ID → emission-record indexing. Provisioned via Cloudflare MCP tools (`r2_bucket_create`, `kv_namespace_create`).

### EXPORT — polymorphic (Portal B)

- **Existing primitive**: mesh `export` (Obsidian, GraphML, JSONL).
- **What it does for the Beacon**: every emission must ship in three forms, satisfying the dialectic-gateway requirement (`architecture.md` §Portal B). Source = the alchemized payload + atoms + edges.

| Output | Audience | File |
|--------|----------|------|
| `portal-markdown.md` | Aesthetic mind | `docs/beacon/examples/portal-markdown.md` (Session 3); production emissions land in the Jekyll site under `public-process/beacon/{ts}.md` |
| `beacon-emission.json` | AI agent / formal mind | `docs/beacon/examples/beacon-emission.json` (Session 3); production emissions land in Cloudflare R2 + Workers KV |
| `portal-graphml.xml` | Analyst / graph reader | `docs/beacon/examples/portal-graphml.xml` (Session 3); production exports land in R2 |

### DISTRIBUTE — four channels

Detail in [`dam-distribution.md`](./dam-distribution.md). Two existing channels (POSSE: Mastodon + Discord + newsletter via `distribute-content.yml`), two new (Workers `/emit` HTTP endpoint, Codex Cloud agent invocation).

### RECEPTIO — close the loop

Every emission's distribution events stream back into `../logos/receptio.md`:

- Each POSSE post's engagement metrics → `BEACON-RECEPTIO-USE-NNN` entries on threshold crossings.
- Each Workers `/emit` GET request → access log → aggregated weekly into receptio §III.
- Each Codex Cloud agent re-emission → logged as `BEACON-ECHO-NNN`.
- Each GitHub PR / issue comment referencing this directory → ingested by the existing PR-comment webhook (already wired for prior PRs).

When a transmission has zero receptio after 90 days → `BEACON-COLD-RECEPTIO-NNN` event → praxis circuit-breaker (per Attack Vector E).

## Trigger model

| Trigger | When | What runs |
|---------|------|-----------|
| `schedule: cron('0 14 * * 1')` | Every Monday 14:00 UTC | One full Beacon emission cycle. Polarity alternates by ISO-week parity. |
| `workflow_dispatch` | Manual | One Beacon emission cycle with optional polarity override. |
| `repository_dispatch{type=beacon-amend}` | On `governance-amendments.jsonl` append | A re-emission with the amendment text as the lead. |
| `push` on `docs/logos/**` | When any Logos file changes | A *test* emission to local store only (no distribution); produces a preview comment on the PR. |
| `repository_dispatch{type=praxis-closed}` | When a praxis row closes | Append a `BEACON-PRAXIS-DONE-NNN` entry to receptio.md without an emission. |

## Failure handling

| Failure | Detection | Action |
|---------|-----------|--------|
| INTAKE rejects payload (schema fail) | exit code != 0 | Open issue tagged `tbp-pipeline-fail`; do not distribute. |
| ATOMIZE produces 0 atoms | atom-count check | Block emission; route as `BEACON-PRAGMA-UPDATE-NNN` (likely a malformed Logos file). |
| Workers `/emit` 5xx > 30 min | uptime monitor | Rollback wrangler version; file `BEACON-OUTAGE-NNN`. |
| Codex Cloud agent unreachable | `gh api` health check | Degrade gracefully — POSSE channels continue without the agent leg. |

## Reuse summary

Existing primitives (no new code):
- `alchemia intake` / `absorb` / `alchemize` — INTAKE/ABSORB/ALCHEMIZE stages.
- `mesh atomize` / `link` — ATOMIZE/LINK stages.
- `mesh.store.sqlite` — local STORE.
- `mesh.export {obsidian|graphml|jsonl}` — EXPORT polymorphism.
- `distribute-content.yml` — POSSE legs (Mastodon, Discord, newsletter).
- existing PR-comment webhook listener — RECEPTIO ingest.

New code (lands in Sessions 2-3):
- `.github/workflows/beacon-emit.yml` — the orchestrator workflow.
- `docs/beacon/cloud/workers/worker.ts` — Workers `/emit` endpoint.
- `docs/beacon/seed-extension-v1.1.md` — per-repo beacon field spec.
- `docs/beacon/beacon-schema.json` — emission record schema.

The pipeline is composed, not invented. Most of it already runs.

---

*Updates to this file flow to `../logos/receptio.md` as `BEACON-PIPELINE-UPDATE-NNN`.*
