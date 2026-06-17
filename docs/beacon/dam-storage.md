# Beacon DAM — Storage

> Two-tier storage for Beacon emissions. Content-addressed via SHA-256. Append-only. Mirrors local ↔ cloud on every emission.

## Tiers

| Tier | Backend | Purpose | Cost model |
|------|---------|---------|------------|
| **Local** | SQLite + FTS5 (via `mesh.store.sqlite`) | Authoring, validation, full-text search, offline replays | Zero |
| **Cloud** | Cloudflare R2 + KV (provisioned via Cloudflare MCP tools) | Durable archive, HTTP-served emissions, agent-fetchable | Per-GB R2 storage + KV operation count |

Both tiers store the same data. The local tier is **authoritative for authoring**; the cloud tier is **authoritative for distribution**. Reconciliation runs on every emission's STORE stage (see [`dam-pipeline.md`](./dam-pipeline.md)).

## Content addressing

Every Beacon artifact is identified by `sha256(canonical_bytes)` truncated to 12 hex characters (matches mesh's atomization convention). Examples:

| Artifact class | Canonicalisation | Example ID |
|----------------|------------------|------------|
| Emission record (full) | `json.dumps(record, sort_keys=True, separators=(',', ':')).encode('utf-8')` | `7a8b2c1d3e4f` |
| Atom (Logos paragraph) | `paragraph_text.strip().encode('utf-8')` | `12ab34cd56ef` |
| Schema (frozen at version) | `json.dumps(schema, sort_keys=True).encode('utf-8')` | `bd9e7f2a1c3d` |

The 48-bit address space is sufficient for the projected emission volume (≤ 1M lifetime emissions × ≤ 1K atoms each = 10⁹ ≪ 2⁴⁸). Collision is theoretically possible; on collision, mesh's atom store falls back to the full 64-character hash and logs a `BEACON-COLLISION-NNN` event.

## Local schema (SQLite)

The Beacon piggybacks on mesh's existing SQLite schema. No new tables required for the core path. Three Beacon-specific tables are added to the same database:

```sql
-- Beacon emission records, one row per transmission.
CREATE TABLE IF NOT EXISTS beacon_emissions (
  emission_id      TEXT PRIMARY KEY,         -- 12-hex content hash of the record
  ts               TEXT NOT NULL,            -- ISO-8601 emission timestamp
  polarity         TEXT NOT NULL CHECK (polarity IN ('formal', 'aesthetic', 'mixed')),
  reach_radius     TEXT NOT NULL CHECK (reach_radius IN ('local', 'organ', 'system', 'public')),
  source_repo      TEXT NOT NULL,            -- which repo emitted (system-level emissions use 'system')
  tether_budget    INTEGER NOT NULL DEFAULT 5000,
  chunk_size       INTEGER NOT NULL DEFAULT 32768,
  payload_atom_ids TEXT NOT NULL,            -- JSON array of mesh atom IDs
  schema_version   TEXT NOT NULL,            -- e.g. '1.1.0' matching beacon-schema.json
  signature        TEXT,                     -- optional Ed25519 signature
  created_at       TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Receptio events, ingested from POSSE / Workers / agent surfaces.
CREATE TABLE IF NOT EXISTS beacon_receptio (
  receptio_id      TEXT PRIMARY KEY,         -- 12-hex content hash
  emission_id      TEXT NOT NULL REFERENCES beacon_emissions(emission_id),
  ts               TEXT NOT NULL,
  surface          TEXT NOT NULL,            -- 'mastodon' | 'discord' | 'workers' | 'codex' | 'pr' | 'manual'
  signal_type      TEXT NOT NULL,            -- 'view' | 'reply' | 'fork' | 'cite' | 'echo'
  source_url       TEXT,                     -- optional URL of the receiver
  payload          TEXT,                     -- optional JSON details
  created_at       TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS idx_receptio_emission ON beacon_receptio(emission_id, ts);

-- BEACON-NNN and TBP-NNN identifier registry. AX-9 triple-reference enforcement.
CREATE TABLE IF NOT EXISTS beacon_ids (
  id_str           TEXT PRIMARY KEY,         -- e.g. 'BEACON-A-001'
  kind             TEXT NOT NULL,            -- 'BEACON' | 'TBP' | sub-namespace
  irf_anchor       TEXT NOT NULL,            -- e.g. 'IRF-BEA-001'
  file_anchor      TEXT NOT NULL,            -- repo-relative path
  github_issue     INTEGER,                  -- issue number; null if not yet opened
  state            TEXT NOT NULL CHECK (state IN ('open', 'in_progress', 'done', 'archived')),
  created_at       TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at       TEXT NOT NULL DEFAULT (datetime('now'))
);
```

FTS5 virtual tables (already present in mesh's schema) cover atom-level full-text search. The Beacon adds no new FTS table.

## Cloud schema (R2 + KV)

### R2 bucket layout

Bucket: `organvm-telos-beacon` (provisioned via `r2_bucket_create` MCP tool).

```
organvm-telos-beacon/
├── emissions/
│   └── {YYYY}/{MM}/{DD}/{emission_id}.json   # full emission record
├── atoms/
│   └── {first_two_hex}/{rest_of_id}.txt      # raw atom text, content-addressed
├── exports/
│   ├── markdown/{emission_id}.md             # Portal B markdown surface
│   ├── graphml/{emission_id}.xml             # Portal B graphml surface
│   └── jsonl/{emission_id}.jsonl             # Portal B JSONL surface
└── manifests/
    └── {YYYY}/{MM}/index.json                # monthly emission index for incremental sync
```

R2 objects are written with `Content-Type` correctly set and a `Cache-Control: public, max-age=86400, immutable` header (atoms and emissions are immutable; manifests rotate monthly).

### KV namespace

KV namespace: `BEACON_INDEX` (provisioned via `kv_namespace_create` MCP tool). Three key prefixes:

| Key prefix | Value | Purpose |
|------------|-------|---------|
| `emission:{emission_id}` | `{R2 URL of record}` | Resolve emission_id → R2 URL. |
| `atom:{atom_id}` | `{R2 URL of atom}` | Resolve atom_id → R2 URL. |
| `latest:{repo_slug}:{polarity}` | `{emission_id}` | Pointer to the latest emission per repo + polarity, served by Workers `/emit` (Session 3). |

TTL: emissions and atoms never expire. `latest:*` keys are overwritten on each new emission.

## Append-only contract

- **Never delete** an emission_id, atom_id, or receptio_id row, in either tier. Per `_constitutional_locks.lock_policy: append_only_amend_never_delete`.
- **Amendments**: emission records may be amended by issuing a new emission with `replaces: {prior_emission_id}`. Both rows persist; downstream queries decide whether to display the amended or the original.
- **Soft delete (rare)**: in case of privacy / legal removal, set `beacon_ids.state = 'archived'` and add an R2 metadata key `archived_reason`; never remove the object itself. Logs the archive event as `BEACON-ARCHIVE-NNN`.

## Versioning

Schema versions are pinned per-emission in `beacon_emissions.schema_version`. The schema file itself is content-addressed in R2 at `atoms/{schema_hash}.txt`. To read an emission produced under an old schema:

```python
schema = r2.get(f'atoms/{record["schema_version"]}.txt')
validate(record, json.loads(schema))
```

This pattern means schemas never break old emissions; new schemas only constrain new emissions.

## Retention

| Tier | Retention |
|------|-----------|
| Local SQLite | Lifetime of the local workspace. Re-buildable from R2 via `mesh fetch-from r2://organvm-telos-beacon/...`. |
| R2 emissions/atoms | Indefinite. No expiry. |
| R2 manifests | Indefinite (monthly index files; cheap; useful for incremental sync). |
| KV `latest:*` | Indefinite; overwritten on new emissions. |
| KV `emission:*` and `atom:*` | Indefinite. |
| `beacon_receptio` | Indefinite locally; sampled into R2 weekly under `receptio/{YYYY}/{MM}/{WW}.jsonl`. |

Cost projection (Cloudflare R2 free tier ~10 GB storage + 10M Class A operations/mo + 1M Class B operations/mo):

- 1 emission ≈ 50 KB (record + 3 export surfaces). 4 emissions/month → 200 KB/month → 2.4 MB/year. Well within free tier.
- KV operations: ~50 reads per Workers `/emit` call. At 100K calls/month → 5M Class B operations → within free tier.
- No paid Cloudflare spend expected in the first year unless the Beacon goes viral (in which case it has succeeded).

## Sync rule

On every emission, both tiers must hold the new record before the emission is considered DISTRIBUTED. The Workers `/emit` endpoint returns 503 (with retry-after) if R2 + KV are stale relative to the local SQLite head. This invariant guarantees external observers never see a phantom emission.

The check is cheap:

```python
local_head = sqlite.fetchone("SELECT emission_id FROM beacon_emissions ORDER BY ts DESC LIMIT 1")
cloud_head = kv.get('latest:system:latest')
assert local_head == cloud_head, f"Mirror lag: local={local_head}, cloud={cloud_head}"
```

## Backup / disaster recovery

The local SQLite database can be lost without data loss because R2 is authoritative for distribution. To rebuild local from cloud:

```bash
mesh fetch-from r2://organvm-telos-beacon/emissions/  ./local-store/
```

The reverse — losing R2 — is more painful but not catastrophic: local SQLite can re-push. Either tier alone suffices to keep operating.

## Security

- Cloudflare API token scope: `R2:read,write` and `KV:read,write` for the specific bucket and namespace only. Token lives in `CLOUDFLARE_API_TOKEN` env (see `cloud/.env.example`, Session 3).
- R2 objects are public-read (the Beacon is a public emitter). Private fields (e.g. unpublished praxis steps) are excluded at the ALCHEMIZE stage, never reach R2.
- Optional Ed25519 signature on emission records: signer key in `BEACON_SIGNING_KEY` env, public key published in `docs/beacon/signing-key.pub`. Receivers can verify.

---

*Updates to this file flow to `../logos/receptio.md` as `BEACON-STORAGE-UPDATE-NNN`.*
