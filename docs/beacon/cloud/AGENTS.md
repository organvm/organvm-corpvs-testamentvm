# `AGENTS.md` — Telos Beacon Protocol agent invocation contract

> Defines how AI agents (Codex Cloud, Claude, Gemini, others) may operate inside the Telos Beacon Protocol. **Read this before any action.** Constitutional anchor: AX-7 (Tetradic Self-Knowledge), AX-8 (Constructed Polis), and the `NON-INTERACTIVE-AGENT-SAFETY` protocol referenced from `orchestration-start-here/docs/`.

## Identity

This file is the canonical agent contract for the Beacon. It is loaded by:

- OpenAI Codex Cloud (https://developers.openai.com/codex/cloud/environments) when a Codex agent is dispatched against this repo.
- Claude Code / Claude Agent SDK sessions targeting this repo.
- The Cursor / Aider / continue.dev IDE agents.
- Custom agents wired to the Beacon via the Workers `/emit` endpoint.

Every agent SHOULD read this file at session start and SHOULD acknowledge its boundaries.

## What the agent can do

The Beacon is constructed to be **operable by agents safely**. The following actions are explicitly authorised:

| Action | Where it lands | Notes |
|--------|----------------|-------|
| Read every file in this repo | n/a | Read-only access is unconditional. |
| Read every file at `docs/logos/` and `docs/beacon/` | n/a | Primary context for the agent. |
| Compose a new Beacon emission | `docs/beacon/examples/` | New emission record + Markdown + GraphML triple. PR for human review. |
| Append a row to `docs/logos/receptio.md` §III | append-only edit | New row at the bottom; never modify existing rows. |
| Open a new PR with the appended row | GitHub | Standard PR workflow. Title prefix: `receptio(beacon):`. |
| Author a new BEACON-NNN IRF entry | `INST-INDEX-RERUM-FACIENDARUM.md` | Append-only; AX-9 triple-reference must be satisfied within the same PR (file + IRF + issue). |
| Suggest a praxis closure | comment on a PR or issue | Agents propose; humans close. |
| Re-emit an existing emission to a new channel | Workers `/emit` invocation only | Does not write to repo. |
| Generate a new portal surface (markdown / json / graphml) | `docs/beacon/examples/` | Must validate against `beacon-schema.json`. |

## What the agent cannot do

| Action | Why blocked |
|--------|-------------|
| Modify `governance-rules.json` | Constitutional core. `_constitutional_locks.lock_policy: append_only_amend_never_delete`. Amendments go through `governance-amendments.jsonl` only, requiring human approval. |
| Modify `docs/logos/telos.md` | Locked. The system telos changes by human authorship + receptio loop only. |
| Modify `docs/logos/pragma.md` | Updates are driven by REPRWA re-runs, not agents. |
| Modify `docs/logos/praxis.md` directly | Agents may *propose* praxis closures via PR; humans accept. |
| Rewrite existing entries in `docs/logos/receptio.md` | Append-only. Never edit prior rows. |
| Modify `governance-amendments.jsonl` | Hash-chained; humans only. |
| Modify `_constitutional_locks` paths | Same as above. |
| Modify `docs/audits/templates/` | The REPRWA methodology templates. Frozen until a TBP amendment. |
| Modify `docs/beacon/beacon-schema.json` or `docs/beacon/seed-extension-v1.1.md` | Schema bumps go through TBP amendment with human approval. |
| Push to `main` directly | Always via PR. The branch protection rules enforce this. |
| Skip the `gitleaks` secret scan | Beacon emissions block on secrets. |
| Disable the `private_fields_stripped` invariant | Privacy guarantee for the emission pipeline. |

## Tools the agent is expected to have

The Beacon assumes the agent has access to the following tools. If any are missing, the agent SHOULD report the absence and degrade gracefully.

| Tool family | Examples | Used for |
|-------------|----------|----------|
| File system | read, write (within boundaries), edit, list | Authoring portals, appending receptio. |
| Git | `git status`, `git add`, `git commit`, `git push` (branch only) | Standard branching workflow. |
| GitHub MCP | `mcp__github__push_files`, `mcp__github__create_pull_request`, `mcp__github__pull_request_read`, `mcp__github__create_or_update_file` | PRs and discoverability. |
| JSON Schema | local validator (e.g. `jsonschema` Python lib) | Validating emissions before push. |
| Shell / Bash | scoped to the workspace | For invoking the Beacon CLI when it lands. |
| (Optional) Cloudflare MCP | `r2_bucket_get`, `kv_namespace_get`, `workers_get_worker` | Cloud-state inspection. Write tools (`r2_bucket_create`, `kv_namespace_create`, deploy) require human approval. |

## Tools the agent is expected to expose

If the agent advertises tools to other systems (e.g. via an MCP server), the Beacon expects:

- `beacon_emit_propose` — emit a new Beacon emission record (PR-only).
- `beacon_receptio_log` — append a row to `docs/logos/receptio.md`.
- `beacon_validate_schema` — validate an emission record against `beacon-schema.json`.
- `beacon_distance` — compute `distance(receiver)` for a named repo (per `ia-schema.md` §4).

## Safe-modification boundaries (formal)

```yaml
# Computed from the constraints above. Agents MUST honour this matrix.
read_allowed:
  - "**/*"

write_allowed_create_only:
  - "docs/beacon/examples/**"
  - "docs/beacon/cloud/**"  # only files under this directory, not the constitutional ones above

write_allowed_append_only:
  - "docs/logos/receptio.md"
  - "INST-INDEX-RERUM-FACIENDARUM.md"

write_blocked:
  - "governance-rules.json"
  - "governance-amendments.jsonl"
  - "docs/logos/telos.md"
  - "docs/logos/pragma.md"
  - "docs/logos/praxis.md"
  - "docs/logos/README.md"
  - "docs/audits/templates/**"
  - "docs/beacon/beacon-schema.json"
  - "docs/beacon/seed-extension-v1.1.md"
  - "docs/beacon/ia-schema.md"
  - "docs/beacon/ia-indices.md"
  - "docs/beacon/dam-*.md"
  - "docs/beacon/README.md"
  - "docs/beacon/architecture.md"
  - "_constitutional_locks/**"
  - ".github/workflows/**"  # only humans add or modify CI

push_targets:
  - "branches matching: claude/**, agent/**, codex/**, beacon-emit/**"
  - "NEVER push to: main, master, release/*"

pr_required: true
draft_pr_required: true
secrets_scan_required: true
```

## Tethering protocol (agent session pacing)

Per the existing `conductor-playbook.md` + `breadcrumb-protocol.md` + `NON-INTERACTIVE-AGENT-SAFETY.md`:

- Agents MUST chunk large emissions into ≤ `BEACON_CHUNK_SIZE` byte segments.
- Agents MUST respect `BEACON_TETHER_BUDGET` token-effort per chunk.
- Agents MUST honour `Link: <next>; rel=next` continuation pacing returned by Workers `/emit`.
- Agents MUST NOT teleport: a single agent run may produce at most one PR per session.
- Agents MUST leave a breadcrumb at session end documenting what was done (per `breadcrumb-protocol.md`).

## Failure modes

| Failure | Required agent behaviour |
|---------|--------------------------|
| Boundary violation attempted (touched a `write_blocked` path) | Halt. Report to user. Do not commit or PR. |
| Schema validation fails | Halt. Report exact validation error. Do not push. |
| Secrets detected in alchemized payload | Halt. Open issue tagged `BEACON-SECRET-BLOCK-NNN`. Do not push. |
| Cloudflare R2/KV write fails | Continue with local SQLite write; flag mirror lag in receptio. |
| Codex Cloud / OpenAI rate-limited | Skip the agent leg this cycle; POSSE + Workers continue. |

## Provenance disclosure

Every emission produced by an agent MUST carry, in its `producers` array:

- The agent identifier (e.g. `codex-cloud-agent-2026-05-18`).
- The model identifier (e.g. `gpt-4.1`, `claude-opus-4-7`).
- The session identifier (e.g. a UUID tying the work back to a trace).

Per `../../audits/templates/policy-invariants.md` invariant #8: every claim is tagged, every speculation is marked, every gap is named.

## Glossary

- **Emit** — publish a new Beacon transmission. See `ia-schema.md` §1.
- **Tether** — pace a delivery via chunked continuation per Tethering Protocol.
- **Boundary** — the matrix in §Safe-modification boundaries above.
- **Polis** — the constructed critical society (AX-8). Bot reviewers are members.
- **Vacuum** — an empty Tetradic field, an UNGROUNDED row, or a cold dead-zone atom. See `ia-schema.md` §1.

## Refs

- `../../logos/telos.md` — the North Star.
- `../../logos/praxis.md` — the live work queue.
- `../../logos/receptio.md` — the reception log; agents append here.
- `../architecture.md` — operational architecture.
- `../ia-schema.md` — controlled vocabulary.
- `../beacon-schema.json` — emission record schema.
- `./codex-cloud.md` — walkthrough for Codex Cloud agents specifically.
- `governance-rules.json` AX-7, AX-8, AX-9.
- `orchestration-start-here/docs/{conductor-playbook,breadcrumb-protocol}.md`.
- `petasum-super-petasum/docs/NON-INTERACTIVE-AGENT-SAFETY.md`.

---

*Agents reading this file are part of the polis. Logging your session in `../../logos/receptio.md` after each PR completes the loop.*
