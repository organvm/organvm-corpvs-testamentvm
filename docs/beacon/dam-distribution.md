# Beacon DAM — Distribution

> Four distribution channels. Two existing (POSSE via `distribute-content.yml`). Two new (HTTP `/emit` via Cloudflare Workers; Codex Cloud agent invocation). Each channel respects polarity, reach_radius, and tether_budget from `ia-schema.md`.

## Channels

| Channel | Carrier | Polarity served | Reach | Tether-aware? | Status |
|---------|---------|----------------|-------|:-------------:|--------|
| **POSSE — Mastodon** | `distribute-content.yml` → Mastodon API | aesthetic | public | No (single post) | ✅ existing |
| **POSSE — Discord** | `distribute-content.yml` → Discord webhook | aesthetic | organ + system | Partial (chunked posts) | ✅ existing |
| **POSSE — Newsletter** | `distribute-content.yml` → newsletter queue | aesthetic | public | Yes (single email = one Tether unit) | ✅ existing |
| **HTTP `/emit`** | Cloudflare Workers `worker.ts` | both polarities, content negotiated | public + agent | Yes (chunked with continuation tokens) | 🆕 Session 3 |
| **Codex Cloud agent** | OpenAI Codex Cloud agent invocation | formal (JSON) preferred | agent | Yes (per-message budget) | 🆕 Session 3 |

## Channel selection rule

The orchestrator (in `beacon-emit.yml`) selects channels per emission as follows:

```
if polarity == 'aesthetic' or polarity == 'mixed':
    distribute_via: [mastodon, discord, newsletter, workers(md), codex(md_summary)]

if polarity == 'formal' or polarity == 'mixed':
    distribute_via: [workers(json), workers(graphml), codex(json)]

if reach_radius == 'local':
    distribute_via: [workers(md, json) only — no POSSE]

if reach_radius == 'organ':
    distribute_via: [discord, workers — no Mastodon/newsletter (org-internal channels only)]

if reach_radius == 'system' or 'public':
    distribute_via: all channels matching polarity
```

The selection is deterministic. The same emission with the same input parameters always picks the same channels.

## Channel specs

### POSSE — Mastodon

- **Reuse**: `distribute-content.yml` `mastodon` job.
- **Beacon delta**: the workflow accepts a new input `emission_type: beacon-{polarity}-{reach}` so analytics can distinguish Beacon posts from essays.
- **Format**: aesthetic-phase emissions only. ≤ 500 chars body + permalink to the full markdown surface on the Jekyll site.
- **Hashtags**: `#TelosBeacon #ORGANVM #AX7`.
- **Receptio ingest**: Mastodon webhook → POSSE analytics → `beacon_receptio` rows with `surface='mastodon'`.

### POSSE — Discord

- **Reuse**: `distribute-content.yml` `discord` job.
- **Beacon delta**: posts use a dedicated webhook for `#telos-beacon` channel; per-organ webhooks for organ-scoped reach.
- **Format**: aesthetic emission body, no chunking required for typical Beacon (≤ 2000 chars). For longer transmissions, body is chunked with explicit continuation markers.
- **Receptio ingest**: Discord reactions + replies → `beacon_receptio` rows with `surface='discord'`.

### POSSE — Newsletter

- **Reuse**: `distribute-content.yml` `newsletter` job (existing newsletter queue, presumably ConvertKit/Buttondown/Listmonk per the broader ORGANVM stack).
- **Beacon delta**: emissions opt into the newsletter only when `reach_radius == 'public'` AND polarity ∈ {aesthetic, mixed}.
- **Format**: full markdown rendered. Includes link back to the full archive at `https://<workers-domain>/emit?id={emission_id}`.
- **Cadence**: at most one Beacon per newsletter issue. Cap = monthly even if multiple emissions queue.

### HTTP `/emit` — Cloudflare Workers (new, Session 3)

- **Endpoint**: `GET https://<workers-domain>/emit`
- **Query parameters**:
  - `repo=<slug>` — required for repo-scoped emissions; `system` for system-level.
  - `polarity=<formal|aesthetic|mixed>` — defaults to caller's `Accept` header inference.
  - `id=<emission_id>` — optional. If set, returns that specific emission.
  - `tether_budget=<int>` — optional override of `chunk_size`. Default reads from emission record.
- **Headers**:
  - `Accept: application/json` → returns the JSON portal.
  - `Accept: text/markdown` → returns the Markdown portal.
  - `Accept: application/graphml+xml` → returns the GraphML portal.
- **Response**: full emission for that repo (latest matching polarity if `id` not given). 304 Not Modified on `If-None-Match` with the prior emission's content-hash etag.
- **Continuation**: large emissions (> tether_budget) return only the first chunk + `Link: <continuation-uri>; rel=next` header. Receivers walk the chain by following `next` until exhausted.
- **CORS**: `Access-Control-Allow-Origin: *`. The Beacon is public.
- **Rate limit**: 60 req/min per IP via Cloudflare Workers rate limiting. Generous enough for legitimate agent use; protects against scraping bursts.
- **Receptio ingest**: Worker logs each request to a per-day R2 manifest. Aggregated weekly → `beacon_receptio` rows with `surface='workers'`.

### Codex Cloud agent (new, Session 3)

- **Mechanism**: Codex Cloud agents subscribe to a `repository_dispatch` event of type `beacon-emit`. The orchestrator workflow dispatches the event with the new emission_id; the agent fetches via `/emit?id=...`.
- **Agent contract**: defined in `cloud/AGENTS.md` (Session 3). The agent receives the formal-polarity JSON, performs allowed actions (re-emit summary, log a receptio entry, propose a praxis closure), then ends its session.
- **Safety**: agent actions are bounded by `cloud/AGENTS.md` safe-modification boundaries. The agent may write to `docs/beacon/examples/` and `docs/logos/receptio.md` (append-only); it may *not* modify `governance-rules.json`, telos.md, or any axiom-anchor.
- **Receptio ingest**: agent run-summaries are PR'd back as `BEACON-ECHO-NNN` events.

## Channel fan-out matrix

For each combination of (polarity, reach_radius), the channels selected:

| polarity \ reach | local | organ | system | public |
|------------------|:-----:|:-----:|:------:|:------:|
| formal | W(json,graphml), C(json) | W(json,graphml), C(json) | W(json,graphml), C(json) | W(json,graphml), C(json) |
| aesthetic | W(md) | D, W(md) | D, W(md) | M, D, N, W(md), C(md_summary) |
| mixed | W(json,md,graphml), C(json,md_summary) | D, W(*), C(*) | D, W(*), C(*) | M, D, N, W(*), C(*) |

(M=Mastodon, D=Discord, N=Newsletter, W=Workers, C=Codex; *=all surfaces.)

## Throughput and quotas

| Channel | Per-emission ceiling | Monthly quota | Failure mode |
|---------|---------------------|---------------|---------------|
| Mastodon | 1 post per emission | 30 posts/mo (Mastodon API generous) | Skip if rate-limited; retry next cycle |
| Discord | 1 post per emission | unlimited | Retry with exponential backoff |
| Newsletter | 1 issue / month max | ≤ 12/year | Queue overflow → skip with `BEACON-NEWSLETTER-SKIP-NNN` |
| Workers | unlimited reads | 100K req free; ~$0.30 per additional 1M | Degrade to KV-only response if R2 lookup fails |
| Codex Cloud | 1 dispatch per emission | Per OpenAI quota; ~$0.01-0.05 per agent invocation | Skip if quota exceeded; POSSE legs unaffected |

## Distribution safety

- **Pre-emission privacy review**: ALCHEMIZE stage strips any field tagged `private: true` in the source Logos files. The Beacon never accidentally emits a private praxis row.
- **Pre-emission legal review**: emissions referencing licensed external content (e.g. a quoted Logos doc citing an external paper) must carry a `license_ack` field. Workflow asserts.
- **Pre-emission security review**: `gitleaks` runs on the alchemized payload before STORE. Any secret pattern blocks the emission and opens a `BEACON-SECRET-BLOCK-NNN` event.
- **Provenance**: every emission carries `producers: [@4444J99, claude-{model-id}]` or equivalent. AI-Conductor methodology applies (per ../audits/templates/policy-invariants.md item 8).

## Failure handling

| Failure | Where | Action |
|---------|-------|--------|
| All POSSE channels down | distribute-content.yml job log | Continue with Workers + Codex; receptio logs the partial distribution. |
| Workers down | Cloudflare uptime alert | POSSE continues; receptio reads from POSSE only this cycle. |
| Codex Cloud rate-limited | OpenAI API response | Skip silently; agent re-tries on next cycle. |
| Mirror lag (local vs R2) | `dam-storage.md` sync check | 503 from Workers; emission is recalled but local store keeps the record for next cycle. |
| Emission marked `private` after the fact | manual `tbp-privacy-revoke` issue | Append `BEACON-ARCHIVE-NNN`; flip `beacon_ids.state='archived'`; do not re-emit. |

## Cross-references

- Pipeline → storage: [`./dam-pipeline.md`](./dam-pipeline.md) and [`./dam-storage.md`](./dam-storage.md).
- Schema for what flows through channels: [`./beacon-schema.json`](./beacon-schema.json).
- Per-repo distribution preferences: `seed.yaml.beacon.{polarity, reach_radius, frequency_hz}` per [`./seed-extension-v1.1.md`](./seed-extension-v1.1.md).
- Workers implementation: [`./cloud/workers/`](./cloud/workers/) (Session 3).
- Agent contract: [`./cloud/AGENTS.md`](./cloud/AGENTS.md) (Session 3).

---

*Updates to this file flow to `../logos/receptio.md` as `BEACON-DISTRIBUTION-UPDATE-NNN`.*
