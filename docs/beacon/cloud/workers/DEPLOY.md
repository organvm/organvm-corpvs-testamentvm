# Deploy — Telos Beacon Protocol Workers

> Runbook for first-deploy and subsequent updates of the `/emit` endpoint. Uses the Cloudflare MCP tools (`r2_bucket_create`, `kv_namespace_create`, etc.) for cloud-state operations.

## Prerequisites

- Cloudflare account with Workers + R2 + KV enabled (free tier suffices for projected volume; see `../../dam-storage.md` §Cost projection).
- `wrangler` CLI installed locally (`npm install -g wrangler` or `npx wrangler`).
- `CLOUDFLARE_API_TOKEN` with scopes: `R2:read,write`, `KV:read,write`, `Workers:read,write` for this account only.
- `CLOUDFLARE_ACCOUNT_ID` (32-hex; from dashboard).

## First-deploy procedure

### 1. Provision R2 bucket

Use the Cloudflare MCP tool (if available) or `wrangler`:

```bash
# Via MCP (preferred — leaves provenance in the MCP audit log)
# Invoke the r2_bucket_create tool with:
#   account_id: $CLOUDFLARE_ACCOUNT_ID
#   bucket_name: organvm-telos-beacon

# Via wrangler (fallback)
npx wrangler r2 bucket create organvm-telos-beacon
```

Confirm:

```bash
npx wrangler r2 bucket list | grep organvm-telos-beacon
```

### 2. Provision KV namespace

```bash
# Via MCP
# Invoke the kv_namespace_create tool with:
#   account_id: $CLOUDFLARE_ACCOUNT_ID
#   title: BEACON_INDEX

# Via wrangler
npx wrangler kv namespace create BEACON_INDEX
npx wrangler kv namespace create BEACON_INDEX --preview
```

Capture the two namespace IDs returned. Edit `wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "BEACON_KV"
id = "<production-namespace-id>"
preview_id = "<preview-namespace-id>"
```

### 3. Seed the first emission (optional, for smoke test)

```bash
# Write a minimal emission to R2 + KV so /emit returns something.
EMISSION_ID=$(python -c "import hashlib, json; r={'emission_id':'aaaaaaaaaaaa','ts':'2026-06-15T00:00:00Z','schema_version':'1.0.0','polarity':'mixed','reach_radius':'system','source_repo':'system','payload':{'aesthetic':{'title':'First emission','body_markdown':'See docs/logos/telos.md.'}}}; print(hashlib.sha256(json.dumps(r,sort_keys=True).encode()).hexdigest()[:12])")
echo "Seed emission_id: $EMISSION_ID"

# Write the seed record locally
mkdir -p /tmp/beacon-seed
python -c "
import hashlib, json
r = {
  'emission_id': '$EMISSION_ID',
  'ts': '2026-06-15T00:00:00Z',
  'schema_version': '1.0.0',
  'polarity': 'mixed',
  'reach_radius': 'system',
  'source_repo': 'system',
  'payload': {
    'aesthetic': {
      'title': 'First emission',
      'body_markdown': 'See docs/logos/telos.md for the seed text.'
    }
  }
}
open('/tmp/beacon-seed/$EMISSION_ID.json', 'w').write(json.dumps(r, indent=2))
"

# Push to R2
npx wrangler r2 object put \
  organvm-telos-beacon/emissions/by-id/$EMISSION_ID.json \
  --file=/tmp/beacon-seed/$EMISSION_ID.json \
  --content-type="application/json"

# Index in KV
npx wrangler kv key put --binding=BEACON_KV \
  "latest:system:mixed" "$EMISSION_ID"
npx wrangler kv key put --binding=BEACON_KV \
  "emission:$EMISSION_ID" "emissions/by-id/$EMISSION_ID.json"
```

### 4. Dry-run deploy

```bash
cd docs/beacon/cloud/workers/
npx wrangler deploy --dry-run
```

Expected output: `Total Upload: < 5 KiB / gzip: < 2 KiB` and no errors.

### 5. Live deploy

Staging first:

```bash
npx wrangler deploy --env staging
```

The staging URL is printed; smoke-test it:

```bash
curl -sf https://organvm-telos-beacon-staging.<your-subdomain>.workers.dev/health | jq
curl -sf https://organvm-telos-beacon-staging.<your-subdomain>.workers.dev/emit?repo=system | jq
```

Both should return JSON. If `/emit` returns 404, the KV seed step (3) was skipped — re-run.

Production:

```bash
npx wrangler deploy --env production
```

### 6. Custom domain (optional)

If you have a Cloudflare-managed domain:

```bash
# Add the route via wrangler.toml (uncomment and edit) or via dashboard:
#   beacon.<your-domain>/emit* → organvm-telos-beacon
```

Update `BEACON_WORKERS_ROUTE` env var across `.env`, `devcontainer.json`, and the orchestrator workflow.

## Subsequent updates

For code-only updates (modifying `worker.ts`):

```bash
npx wrangler deploy --env production
```

For config updates (modifying `wrangler.toml`):

```bash
# Validate first
npx wrangler deploy --dry-run --env production

# Deploy
npx wrangler deploy --env production
```

For schema bumps (modifying `../../beacon-schema.json`):

This is a TBP amendment. Follow `../../seed-extension-v1.1.md` §TBP-001 protocol:

1. Open an issue tagged `tbp-amendment`.
2. PR the schema change. Title: `beacon(schema): bump to vX.Y — <reason>`.
3. After merge, redeploy:

```bash
npx wrangler deploy --env production
```

4. Log the amendment in `governance-amendments.jsonl` with a new `TBP-NNN` ID.

## Rollback

Workers maintain deployment history. To rollback:

```bash
npx wrangler deployments list --name organvm-telos-beacon-prod
# Pick a prior deployment_id
npx wrangler rollback --deployment-id <id> --env production
```

Log the rollback as `BEACON-OUTAGE-NNN` in `../../../logos/receptio.md`.

## Monitoring

- Cloudflare dashboard → Workers → organvm-telos-beacon-prod → Metrics
- Logs: `npx wrangler tail --env production`
- Receptio aggregation: weekly cron in `beacon-emit.yml` runs `mesh ingest-receptio --from-workers-logs`.

If 5xx errors > 1% over any 30-minute window:

1. `npx wrangler tail --env production` to inspect.
2. If R2 / KV is the cause, check Cloudflare status page.
3. If logic regression, rollback per above.
4. File `BEACON-OUTAGE-NNN` in receptio.

## Costs

Per `../../dam-storage.md` §Cost projection: zero expected at projected volume. The Workers free tier covers 100K req/day; R2 free tier covers 10 GB storage + 10M Class A ops/mo.

If the Beacon exceeds free tier, that is a *success indicator* (the receptio has gone wide). Budget will not be a surprise — Cloudflare emails on overage approach.

## Refs

- `wrangler` documentation: https://developers.cloudflare.com/workers/wrangler/
- R2 documentation: https://developers.cloudflare.com/r2/
- KV documentation: https://developers.cloudflare.com/kv/
- Endpoint contract: [`../../dam-distribution.md`](../../dam-distribution.md) §HTTP /emit
- Storage spec: [`../../dam-storage.md`](../../dam-storage.md)
- Agent contract: [`../AGENTS.md`](../AGENTS.md)
