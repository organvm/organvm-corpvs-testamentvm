# Data Mesh + Medallion Architecture (Standard 16)

**Status:** Codified 2026-05-22 | **Domain:** SYS / data-architecture | **Scope:** universal (applies to every ORGANVM organ producing or consuming data)

## Purpose

Codify the architecture for transforming raw logs, transcripts, and database state into curated, domain-owned data products. The pattern is Data Mesh (decentralized ownership) implemented on a Medallion Lakehouse (bronze → silver → gold) under a single governance plane.

This standard names what ORGANVM has *already been doing* implicitly — the prompt-atomization pipeline, the IRF, the four-registry split, and the per-organ trivium are all instantiations of this pattern. The doc anchors them under one named convention so future work can be evaluated against it.

---

## 1. Architecture Blueprint

A decentralized lakehouse with three storage tiers and a single governance plane:

```
[ RAW SOURCE ] ──► [ INGESTION ] ──► [ BRONZE ] ──► [ SILVER ] ──► [ GOLD ] ──► [ CONSUMPTION ]
 (Logs/DBs)        (extractors)       (raw logs)    (cleaned)     (products)     (BI/AI/Apps)
                                          │              │              │
                                          ▼              ▼              ▼
                                 ┌──────────────────────────────────────────────┐
                                 │      CENTRAL GOVERNANCE & CATALOG PLANE       │
                                 │   (metadata, frontmatter, unique IDs, RBAC)   │
                                 └──────────────────────────────────────────────┘
```

### 1.1 Ingestion Layer

- **Tool families:** Airbyte, Fivetran, Apache Kafka (streaming), or simple file-drop for self-contained sources.
- **Role:** Extract from sources and land in bronze without modification. No business logic at this stage.
- **ORGANVM instantiation today:** Claude/Codex/Gemini/OpenCode session JSONLs landing in their respective on-disk session stores (`~/.claude/projects/<slug>/*.jsonl`, `~/.codex/sessions/...`, etc.); `intake/canonical/sources/` in `my-knowledge-base`; manual takeout exports.

### 1.2 Storage & Compute Layer (the Lakehouse)

| Tier | Role | Convention | ORGANVM instantiation |
|---|---|---|---|
| **Bronze** | Append-only raw landing zone | Schema-on-read; no mutations | Session JSONL files, raw takeout exports, `my-knowledge-base/intake/` |
| **Silver** | Cleaned, deduplicated, conformed | Normalized timestamps (UTC), strict typing, anomaly-handled | `my-knowledge-base/atomized/` prior to ID assignment |
| **Gold** | Curated data products | Atomized, unique-ID'd, indexed, schema-validated | `data/prompt-registry/prompt-atoms.json` (24,599 atoms, ATM-XXXXXX IDs); `INST-INDEX-RERUM-FACIENDARUM.md` (IRF-XXX-NNN); `data/prompt-registry/BACKLOG-AT-A-GLANCE-*.md` compressed views |

**Tool families:** Snowflake, Databricks, AWS S3 + Apache Iceberg. ORGANVM uses git + JSON/Markdown files as the lakehouse substrate — fits the same access pattern at smaller scale.

### 1.3 Central Governance Plane (the Glue)

- **Tool families:** dbt, Atlan, Collibra.
- **Role:** Metadata catalog, frontmatter standards, lineage tracking, row-level access.
- **ORGANVM instantiation today:** `repo-registry.json` (repo metadata), `docs/operations/concordance.md` (ID prefix table), per-memory-file YAML frontmatter (`name`, `description`, `metadata.type`), the four-registry table in home-scope `CLAUDE.md`. The lineage tracking is the gap (see §4).

---

## 2. The Domain Process Cycle (Six-Phase Lifecycle)

Every domain following this standard moves data through six phases. The cycle is continuous — phase 6 feeds back into phase 1.

```
┌────────────────────────────────────────────────────────┐
│  1. INGEST  ──►  2. CLEAN  ──►  3. ATOMIZE & INDEX     │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│  6. REFRESH ◄──  5. GOVERN ◄──  4. PUBLISH & DELIVER   │
└────────────────────────────────────────────────────────┘
```

### Phase 1 — Ingest (Raw → Bronze)

- Raw logs and database snapshots land in the domain's bronze bucket.
- Data is **immutable** and retains its original messy structure.
- **Test:** can you trace any silver/gold record back to its bronze source byte-for-byte? If no, ingest is degrading on landing.

### Phase 2 — Clean & Standardize (Bronze → Silver)

- Anomalies and null values handled per documented policy.
- Timestamps normalized to UTC.
- Data types strictly cast (strings → integers, ISO dates → datetimes).
- **Test:** does every silver record pass schema validation? If no, cleaning is incomplete.

### Phase 3 — Atomize & Index (Silver → Gold)

- **Atomization:** monolithic log objects (e.g., massive JSON blobs, full session transcripts) are shredded into granular, single-purpose records.
- **Identification:** deterministic hashing (MD5, UUIDv5) generates permanent unique IDs that survive across systems.
- **Indexing:** cluster keys / indexes applied for rapid query performance.
- **Test:** can you retrieve any atom by ID in O(1) without scanning? If no, indexing is missing.
- **ORGANVM example:** `organvm atoms pipeline --write` shreds session transcripts into ATM-XXXXXX atoms; `organvm atoms fanout --write` indexes them by domain and target organ.

### Phase 4 — Publish & Deliver (the Product)

- **Frontmatter injection:** `schema.yml` (dbt) or equivalent metadata block defines ownership, column types, lineage. ORGANVM analog: YAML frontmatter on memory files and atom records.
- **Delivery:** the dataset is exposed as a secure view or shared table directly inside the domain owner's workspace.
- **Test:** can the domain owner consume the product without engineering intervention? If no, delivery is not autonomous.

### Phase 5 — Govern & Secure

- **RBAC:** only authorized domain users read the data.
- **Quality monitors:** Great Expectations, dbt tests, or equivalents run automatically — uniqueness, non-null, referential integrity.
- **Test:** does a quality failure block downstream consumption? If no, quality is advisory not enforced.

### Phase 6 — Refresh & Iterate

- **Orchestration:** Apache Airflow, Prefect, or scheduled GitHub Actions trigger the pipeline on schedule or event.
- **Feedback:** domain owners feed schema-evolution requests back to data engineers.
- **Test:** does a schema-evolution request take less than N business days from filing to merge? If no, the feedback loop is broken.

---

## 3. Cross-Registry Lineage (the ORGANVM-specific constraint)

ORGANVM's four parallel work registries (see home-scope `CLAUDE.md`) are independent gold-layer products with *no foreign-key cross-reference*:

| Registry | Identity | Gold-layer role |
|---|---|---|
| Atom registry | ATM-XXXXXX | every prompt ever issued, atomized |
| Plans | filename slug | per-task implementation plans |
| IRF | IRF-XXX-NNN | universal work registry (the gap) |
| Pipeline task queue | hash IDs | computed routing of atoms to organs |

**Standard 16 demands:** any new data product MUST be cross-referenceable to *at least one* existing registry's identity scheme. Two preferred (per universal rule #23, "triple reference — every entity exists in 3+ locations"). New floating identity spaces are forbidden without explicit registration in `docs/operations/concordance.md`.

---

## 4. Known Gaps (drives IRF entries)

- **Lineage tracking is largely absent.** Gold-layer artifacts (atoms, IRF rows, plans) cannot be programmatically traced back to the bronze session JSONL that birthed them. The forensic shortcut (`~/.claude/jobs/<short>/timeline.jsonl` first-prompt) is single-step, not full chain.
- **Quality gates are advisory, not enforced.** `pre-commit` runs locally, GitHub Actions enforce on push, but no quality failure currently blocks atom *creation* — failures are noted post-hoc.
- **Refresh cadence is mixed.** Some pipelines refresh on commit (autogen tail), others nightly (soak test), others on-demand (`organvm refresh`). No single SLA.
- **The gitignore gap surfaced in this session's closeout** (`my-knowledge-base/{intake/,atomized/,.specstory/,.test-tmp/}` carrying 5.5 GB untracked) is a Phase-1-Ingest hygiene violation: bronze landing zones are *meant* to be append-only, but they should also be classified as either replicate-to-remote (rare, only when reproducibility demands it) or gitignored (default, since bronze is reproducible from sources).

---

## 5. Anti-patterns (forbidden)

- **Re-ingesting from gold back into bronze.** Gold is downstream; reversing the flow erases atomization.
- **In-place mutation of gold records without lineage.** Per universal rule about additive-vs-overwrite: gold mutations are permitted (e.g., IRF row status updates) but must be auditable through git history or equivalent.
- **Creating a new identity prefix without registering in concordance.** New ID spaces fragment the catalog plane.
- **Skipping silver and going bronze → gold directly.** Silver is where the system absorbs the cost of cleaning; bypassing it pushes mess into gold and corrupts downstream queries.

---

## 6. Acceptance criteria (when is a domain considered "Standard-16-compliant"?)

A domain is compliant when:

1. ✅ Raw sources land in an identifiable bronze bucket with append-only semantics.
2. ✅ Silver layer schema is documented (even informally — column types, normalization rules).
3. ✅ Gold layer records carry stable unique IDs registered in `concordance.md`.
4. ✅ At least one frontmatter convention is consistently applied (YAML on memory files, JSON schema on atom records, etc.).
5. ✅ Refresh trigger is documented (cron, event, on-demand) — even if irregular.
6. ✅ At least one quality check fires on the pipeline (pre-commit hook, GitHub Action, manual review checklist).

A domain is *not yet* compliant when any of these is missing. Compliance is a state to grow into, not a launch gate.

---

## 7. Related standards & docs

- `10-repository-standards.md` — applies the naming, frontmatter, and ownership conventions that Standard 16 depends on.
- `11-specification-driven-development.md` — provides the spec-before-build discipline that prevents bronze-to-gold shortcuts.
- `13-organ-identity-and-placement.md` — defines the domain ownership boundaries that Data Mesh decentralizes to.
- Home-scope `CLAUDE.md` four-registry table — the canonical list of gold-layer products in ORGANVM today.
- `docs/operations/concordance.md` — the catalog plane's identity registry.
