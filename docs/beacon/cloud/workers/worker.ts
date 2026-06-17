/**
 * Telos Beacon Protocol — Cloudflare Workers `/emit` endpoint
 *
 * Contract: see docs/beacon/dam-distribution.md §HTTP /emit
 * Schema: see docs/beacon/beacon-schema.json
 * Constitutional anchor: AX-7 (Tetradic Self-Knowledge)
 *
 * This is the stub. It is intentionally minimal — enough to demonstrate
 * the contract and pass `wrangler deploy --dry-run`. Production hardening
 * (per-IP rate limiting via Cloudflare Rate Limiting Rules, full continuation
 * walking with Link: rel=next, signed-emission verification) lands in
 * subsequent commits.
 *
 * Constitutional bounds:
 *   - This worker is READ-ONLY against R2 and KV. It never writes.
 *   - It never modifies governance-rules.json (it can't — different Cloudflare account).
 *   - It honours the append-only contract by not exposing any DELETE / PUT.
 */

export interface Env {
  BEACON_R2: R2Bucket;
  BEACON_KV: KVNamespace;
  BEACON_VERSION: string;
  BEACON_DEFAULT_POLARITY: string;
  BEACON_DEFAULT_REACH: string;
  BEACON_RATE_LIMIT_PER_MIN: string;
}

interface EmissionRecord {
  emission_id: string;
  ts: string;
  schema_version: string;
  polarity: 'formal' | 'aesthetic' | 'mixed';
  reach_radius: 'local' | 'organ' | 'system' | 'public';
  source_repo: string;
  payload: {
    formal?: Record<string, unknown>;
    aesthetic?: { title: string; subtitle?: string; body_markdown: string };
  };
}

function json(body: unknown, init: ResponseInit = {}): Response {
  return new Response(JSON.stringify(body), {
    ...init,
    headers: {
      'content-type': 'application/json; charset=utf-8',
      'cache-control': 'public, max-age=300',
      'access-control-allow-origin': '*',
      ...(init.headers ?? {}),
    },
  });
}

function markdown(body: string, init: ResponseInit = {}): Response {
  return new Response(body, {
    ...init,
    headers: {
      'content-type': 'text/markdown; charset=utf-8',
      'cache-control': 'public, max-age=300',
      'access-control-allow-origin': '*',
      ...(init.headers ?? {}),
    },
  });
}

function graphml(body: string, init: ResponseInit = {}): Response {
  return new Response(body, {
    ...init,
    headers: {
      'content-type': 'application/graphml+xml; charset=utf-8',
      'cache-control': 'public, max-age=300',
      'access-control-allow-origin': '*',
      ...(init.headers ?? {}),
    },
  });
}

function negotiate(accept: string | null, polarity?: string): 'json' | 'markdown' | 'graphml' {
  if (accept?.includes('application/graphml+xml')) return 'graphml';
  if (accept?.includes('text/markdown')) return 'markdown';
  if (accept?.includes('application/json')) return 'json';
  // Default polarity-derived
  if (polarity === 'formal') return 'json';
  if (polarity === 'aesthetic') return 'markdown';
  return 'json';
}

async function fetchEmission(
  env: Env,
  repoSlug: string,
  polarity: string | null,
  explicitId: string | null,
): Promise<EmissionRecord | null> {
  let emissionId = explicitId;

  if (!emissionId) {
    // Look up the latest emission for this repo + polarity
    const kvKey = `latest:${repoSlug}:${polarity ?? 'system'}`;
    emissionId = await env.BEACON_KV.get(kvKey);
    if (!emissionId) return null;
  }

  // Resolve emission_id -> R2 URL via KV index
  const r2KeyHint = await env.BEACON_KV.get(`emission:${emissionId}`);
  const r2Key = r2KeyHint ?? `emissions/by-id/${emissionId}.json`;

  const object = await env.BEACON_R2.get(r2Key);
  if (!object) return null;

  const body = await object.text();
  try {
    return JSON.parse(body) as EmissionRecord;
  } catch {
    return null;
  }
}

function renderMarkdownPortal(record: EmissionRecord): string {
  const a = record.payload.aesthetic;
  const lines: string[] = [];
  lines.push(`# ${a?.title ?? `Beacon emission ${record.emission_id}`}`);
  if (a?.subtitle) lines.push(`> ${a.subtitle}`);
  lines.push('');
  lines.push(`- **emission_id**: \`${record.emission_id}\``);
  lines.push(`- **ts**: ${record.ts}`);
  lines.push(`- **polarity**: ${record.polarity}`);
  lines.push(`- **reach_radius**: ${record.reach_radius}`);
  lines.push(`- **source_repo**: ${record.source_repo}`);
  lines.push('');
  if (a?.body_markdown) {
    lines.push(a.body_markdown);
  } else if (record.payload.formal) {
    lines.push('## Claims (formal payload)');
    const claims = (record.payload.formal as Record<string, unknown>)['claims'];
    if (Array.isArray(claims)) {
      for (const c of claims) {
        const obj = c as Record<string, unknown>;
        lines.push(`- ${String(obj.statement ?? '')} _(${String(obj.tag ?? 'EXPLICIT')})_`);
      }
    }
  } else {
    lines.push('_No human-readable body for this emission._');
  }
  return lines.join('\n');
}

function renderGraphmlPortal(record: EmissionRecord): string {
  const claims = (record.payload.formal as Record<string, unknown> | undefined)?.['claims'];
  const claimArr = Array.isArray(claims) ? (claims as Record<string, unknown>[]) : [];
  const escape = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  const nodes = [`<node id="emission-${record.emission_id}"><data key="d0">${escape(record.emission_id)}</data></node>`];
  const edges: string[] = [];
  claimArr.forEach((c, i) => {
    const stmt = String(c.statement ?? '');
    nodes.push(`<node id="claim-${i}"><data key="d0">${escape(stmt.slice(0, 200))}</data></node>`);
    edges.push(`<edge source="emission-${record.emission_id}" target="claim-${i}"/>`);
  });
  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">',
    '<key id="d0" for="node" attr.name="label" attr.type="string"/>',
    `<graph id="beacon-${record.emission_id}" edgedefault="directed">`,
    ...nodes,
    ...edges,
    '</graph></graphml>',
  ].join('\n');
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Health check
    if (url.pathname === '/' || url.pathname === '/health') {
      return json({
        ok: true,
        service: 'organvm-telos-beacon',
        version: env.BEACON_VERSION,
        constitutional_anchor: 'AX-7',
        endpoints: ['/emit'],
      });
    }

    if (url.pathname !== '/emit') {
      return new Response('Not Found', { status: 404 });
    }

    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'access-control-allow-origin': '*',
          'access-control-allow-methods': 'GET, OPTIONS',
          'access-control-allow-headers': 'Accept, If-None-Match',
        },
      });
    }

    if (request.method !== 'GET') {
      return new Response('Method Not Allowed', { status: 405 });
    }

    const repoSlug = url.searchParams.get('repo') ?? 'system';
    const polarity = url.searchParams.get('polarity');
    const explicitId = url.searchParams.get('id');
    const accept = request.headers.get('Accept');

    const record = await fetchEmission(env, repoSlug, polarity, explicitId);
    if (!record) {
      return json(
        {
          error: 'No emission found for the requested repo/polarity.',
          repo: repoSlug,
          polarity,
          id: explicitId,
        },
        { status: 404 },
      );
    }

    // Conditional GET via ETag (content-addressed; emission_id is the ETag)
    const ifNoneMatch = request.headers.get('If-None-Match');
    if (ifNoneMatch && ifNoneMatch === `"${record.emission_id}"`) {
      return new Response(null, { status: 304, headers: { etag: `"${record.emission_id}"` } });
    }

    const surface = negotiate(accept, polarity ?? record.polarity);
    const etagHeaders = { etag: `"${record.emission_id}"` };

    switch (surface) {
      case 'json':
        return json(record, { headers: etagHeaders });
      case 'markdown':
        return markdown(renderMarkdownPortal(record), { headers: etagHeaders });
      case 'graphml':
        return graphml(renderGraphmlPortal(record), { headers: etagHeaders });
    }
  },
};
