# SOP-001: Vector Pipeline Activation

**Version:** 1.0
**Derived from:** Stakeholder Portal (Hermeneus) activation session, 2026-03-06
**Scope:** Any ORGANVM project requiring semantic search over corpus content
**Owner:** META-ORGANVM / Governance
**Status:** ACTIVE

---

## 1. Purpose

Activate a vector embedding pipeline for any project that needs semantic search over text content. This SOP covers: provisioning a vector-capable database, adapting embedding functions for a free/OSS provider, running ingestion, and verifying end-to-end retrieval.

This is a **universal pattern**. The stakeholder portal was the first instantiation. Every future project that needs "search by meaning" follows this same skeleton.

## 2. When to Use This SOP

A project needs this SOP when:
- It has a corpus of text (docs, code, notes, transcripts, research)
- It needs retrieval beyond keyword matching (semantic similarity)
- It stores or will store embeddings in Postgres with pgvector
- The `document_chunks` table (or equivalent) exists but is empty

## 3. Prerequisites Checklist

Before starting, verify:

| # | Prerequisite | How to verify |
|---|-------------|---------------|
| 1 | Schema defines a vector column | `grep "vector(" src/lib/db/schema.*` |
| 2 | Embedding function exists in code | `grep -r "fetchEmbedding\|embedQuery" src/` |
| 3 | Ingestion worker exists | Check for chunking + embedding loop |
| 4 | Query-time embedding call exists | Check retrieval/search module |
| 5 | HuggingFace token available | `cat ~/.cache/huggingface/token` |
| 6 | Neon account exists | `neon projects list` or MCP tool |
| 7 | Deployment platform CLI authed | `vercel whoami` / `netlify status` / etc. |

## 4. Procedure

### Phase 1: Provision Database

**Step 1.1 — Create Neon project**
```
Name: {project-slug}
Region: us-east-2 (default free tier)
```
Record: `PROJECT_ID`, `CONNECTION_STRING`

**Step 1.2 — Enable pgvector**
```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

**Step 1.3 — Verify extension**
```sql
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
```

### Phase 2: Align Dimensions

The embedding model dictates vector dimensions. **All three points must agree:**
1. Schema definition (`vector("embedding", { dimensions: N })`)
2. Embedding model output dimensionality
3. Any hardcoded dimension references in tests or docs

**Free model reference:**

| Model | Provider | Dims | Latency | Cost |
|-------|----------|------|---------|------|
| `all-MiniLM-L6-v2` | HuggingFace Inference | 384 | ~228ms | Free |
| `nomic-embed-text` | Ollama (local only) | 768 | ~50ms | Free (local) |
| `text-embedding-3-small` | OpenAI | 1536 | ~100ms | $0.02/1M tok |

**Step 2.1 — Update schema**
Change the vector dimension in the ORM schema to match the chosen model.

**Step 2.2 — Generate migration**
```bash
DATABASE_URL=<neon-url> npx drizzle-kit generate  # or equivalent ORM migration tool
```

**Step 2.3 — Run migration**
```bash
DATABASE_URL=<neon-url> npx drizzle-kit migrate
```

**Step 2.4 — Update documentation**
Grep for old dimension value in `CLAUDE.md`, `README.md`, comments. Update all references.

### Phase 3: Adapt Embedding Functions

The embedding function must handle multiple API formats. The two primary formats:

| Provider | Request body | Response format |
|----------|-------------|-----------------|
| OpenAI-compatible | `{ input: text, model: name }` | `{ data: [{ embedding: [...] }] }` |
| HuggingFace Inference | `{ inputs: text }` | `[[...]]` (nested array) |

**Step 3.1 — Modify ingestion embedding function**
Add provider detection by URL pattern:
- `huggingface.co` or `hf-inference` → HF format
- Everything else → OpenAI-compatible format

**Step 3.2 — Modify query-time embedding function**
Same logic as 3.1. These are often in different files (ingestion vs. retrieval).

**Step 3.3 — Verify both functions handle errors gracefully**
Embedding failures at ingestion time should log and skip (not crash the pipeline).
Embedding failures at query time should fall back to non-semantic strategies.

### Phase 4: Configure Environments

**Step 4.1 — Local environment (`.env.local` or `.env`)**
```
DATABASE_URL=<neon-connection-string>
EMBEDDING_API_URL=<provider-url>
EMBEDDING_API_KEY=<token>
EMBEDDING_MODEL=<model-name>
```

**Step 4.2 — Production environment**
Set the same four variables in the deployment platform (Vercel, Netlify, Render, etc.).

**Step 4.3 — Preview/staging environments**
Same variables. Use the same Neon DB (free tier has one project) or a separate branch.

### Phase 5: Run Ingestion

**Step 5.1 — Start ingestion**
```bash
nohup <ingestion-command> > /tmp/ingestion-{project}.log 2>&1 &
echo "PID: $!"
```

**Step 5.2 — Monitor**
```bash
tail -f /tmp/ingestion-{project}.log
# In parallel, check DB:
# SELECT count(*), count(DISTINCT repo) FROM document_chunks;
```

**Step 5.3 — Handle rate limits**
HuggingFace free tier has undocumented rate limits. If you see sustained 429s:
1. Add a delay between calls (100-500ms)
2. Split ingestion into batches
3. Re-run — upsert logic (`onConflictDoUpdate`) makes re-runs idempotent

**Step 5.4 — Handle 500 errors**
Sporadic 500s from HF are normal. The pipeline logs and skips failed chunks. After ingestion completes, failed chunks can be retried by re-running the full pipeline (idempotent).

### Phase 6: Verify

| # | Check | Command / Query | Expected |
|---|-------|----------------|----------|
| 1 | Chunk count | `SELECT count(*) FROM document_chunks` | > 0 (thousands for a full corpus) |
| 2 | Dimension check | `SELECT vector_dims(embedding) FROM document_chunks LIMIT 1` | Matches chosen model |
| 3 | Distinct sources | `SELECT count(DISTINCT repo) FROM document_chunks` | Matches number of ingested repos/sources |
| 4 | Similarity works | `SELECT 1-(embedding <=> (SELECT embedding FROM document_chunks LIMIT 1)) as sim FROM document_chunks LIMIT 5` | Non-zero similarities |
| 5 | Tests pass | `npm run test` / `pytest` | All pass |
| 6 | Build succeeds | `npm run build` / equivalent | No errors |
| 7 | Strategy appears | Query the chat/search endpoint with debug mode | Response includes `semantic` in strategy string |

### Phase 7: Deploy

```bash
<deploy-command>  # e.g., vercel deploy --prod
```

Post-deploy verification: query the live endpoint and confirm semantic results appear.

## 5. Rollback

If the pipeline causes issues:
1. **Revert schema** — restore old dimension, generate reverse migration
2. **Revert code** — git revert the embedding function changes
3. **DB is safe** — the chunks table can be truncated without affecting other tables
4. **Env vars** — revert to old values or `dummy` placeholders

The semantic strategy is wrapped in a try/catch that falls back silently. Removing the DB or breaking the embedding API degrades gracefully — other retrieval strategies continue to work.

## 6. Starter Research Questions

When activating this SOP for a new project, answer these first:

### About the corpus
- What text content exists? (docs, code, transcripts, research, user-generated)
- How large is the corpus? (files, total words, growth rate)
- What languages/formats? (markdown, YAML, code, prose)
- Is content static or continuously updated? (one-time ingest vs. incremental)

### About the search need
- Who searches? (users, agents, internal tools)
- What kinds of queries? (factual lookup, conceptual exploration, similarity matching)
- What's the latency budget? (real-time chat vs. batch analysis)
- What's the quality bar? (good-enough vs. state-of-the-art)

### About the infrastructure
- Where does the app deploy? (Vercel, Render, self-hosted)
- Is there an existing DB? (reuse vs. create new)
- What's the budget? ($0 free tier vs. paid services)
- Is local-only embedding acceptable? (Ollama vs. API)

### About the embedding model
- What dimensionality is needed? (384 for lightweight, 768-1536 for higher quality)
- Is the model available at query time from the deployment environment?
- Does the model handle the corpus language well?

## 7. Anti-Patterns (Lessons Learned)

1. **Don't use `dummy` as an API key and hope for the best.** If a service requires auth, either configure it properly or disable the feature explicitly with a feature flag.

2. **Don't assume the ingestion ran.** An empty `document_chunks` table with a fully-built schema creates a false sense of completeness. The schema existing ≠ data existing.

3. **Don't hardcode provider-specific API formats.** The embedding function should be provider-agnostic from day one. URL-based detection is a pragmatic minimum.

4. **Don't skip dimension alignment.** Schema, model, and any mocks/tests must all agree on dimensions. A mismatch causes silent failures or cryptic Postgres errors.

5. **Don't run multiple ingestion processes simultaneously.** Upsert logic prevents data corruption, but concurrent processes waste API calls and can trigger rate limits.

6. **Don't pipe long-running processes through `head`.** It kills the process when the pipe closes. Use `nohup` + log file + `tail -f`.

---

## Appendix A: ORGANVM System Integration Points

This SOP interacts with:
- **seed.yaml** — declares what content a repo produces (used by ingestion to find files)
- **repo-registry.json** — source of truth for repo metadata (used to enumerate repos)
- **CLAUDE.md** — per-repo documentation (primary ingestion target)
- **governance-rules.json** — no direct interaction, but vector search quality is a potential governance metric

## Appendix B: Cost Model

| Component | Free tier limits | Paid alternative |
|-----------|-----------------|------------------|
| Neon DB | 0.5 GB storage, 190 compute hours/mo | Neon Pro ($19/mo) |
| HF Inference | Undocumented rate limits, ~228ms/call | HF Pro ($9/mo) or OpenAI |
| Vercel | 100 GB bandwidth, 1M edge requests | Vercel Pro ($20/mo) |

At 27K+ chunks × 384 dims × 4 bytes = ~40 MB vector storage. Well within free tier.
