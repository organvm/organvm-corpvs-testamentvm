# Codex Cloud — Walkthrough

> Walks an operator through invoking the Telos Beacon Protocol from an OpenAI Codex Cloud agent environment. References https://developers.openai.com/codex/cloud/environments.

## Why Codex Cloud

Codex Cloud is OpenAI's hosted agent-environment platform — a sibling to Claude Code (https://claude.com/code), Cursor's background agents, and devcontainer-based dev agents. The Beacon Protocol is designed to be invoked safely from any of them, but Codex Cloud is the first-class target because (a) it has a clear devcontainer contract, (b) its `repository_dispatch` integration makes the agent leg of the Beacon's distribution trivial, and (c) the original request that birthed this protocol explicitly mentioned `developers.openai.com/codex/cloud/environments`.

## Prerequisites

Before invoking the Beacon from Codex Cloud, the operator must have:

1. An OpenAI account with Codex Cloud access enabled.
2. Access to this repository (`a-organvm/organvm-corpvs-testamentvm`).
3. The Cloudflare account with R2 + KV provisioned (one-time, see `workers/DEPLOY.md`).
4. The `.env` file populated locally (template at [`./env.example`](./env.example)).
5. (Optional) The Beacon's signing key generated, if you want signed emissions.

## Setup — first run

### 1. Open the repo in Codex Cloud

Navigate to https://platform.openai.com/codex/cloud/ and create a new environment pointed at this repo + branch. Codex Cloud will:

- Read [`./devcontainer.json`](./devcontainer.json) and provision the container.
- Mount the workspace at `/workspaces/organvm-corpvs-testamentvm`.
- Install Python 3.12, Node 20, GitHub CLI per `features`.
- Run the `postCreateCommand` which validates `beacon-schema.json` parses.
- Auto-open `docs/logos/telos.md`, `cloud/AGENTS.md`, and this walkthrough.

### 2. Configure secrets

In the Codex Cloud environment settings:

- Add the `BEACON_*`, `CLOUDFLARE_*`, `MASTODON_*`, `DISCORD_*`, `OPENAI_*`, and (optionally) `BEACON_SIGNING_KEY` environment variables from your local `.env`.
- Codex Cloud treats these as session-scoped secrets — they are never written to disk inside the container.

### 3. Verify the Beacon is reachable

Inside the Codex Cloud terminal:

```bash
# Verify the schema parses
python -c "import json; json.load(open('docs/beacon/beacon-schema.json')); print('OK')"

# Verify the Workers /emit endpoint is up (only after DEPLOY)
curl -sf -H "Accept: application/json" "$BEACON_WORKERS_ROUTE/emit?repo=system" | head -200
```

If both succeed, the environment is ready.

## Invoking the Beacon

The Codex Cloud agent has three high-level entry points.

### Entry A — Read the system telos

The simplest possible action. The agent reads `docs/logos/telos.md` and acknowledges the AX-7 contract. This costs nothing and is the recommended way to begin every session.

```text
> Read docs/logos/telos.md and summarize the Beacon's idealized form
> in three sentences. Identify the four constitutive Tetradic dimensions
> per AX-7.
```

The agent should respond with a faithful summary and confirm: telos, pragma, praxis, receptio.

### Entry B — Compose a new emission

When the operator wants the agent to produce a new Beacon emission:

```text
> Compose a new Beacon emission with polarity=mixed and reach=public,
> drawing the formal payload from docs/audits/STRUCTURED-CANDIDATES.json
> top 5 candidates and the aesthetic payload from a new 600-word essay
> reflecting on what's changed since the last emission. Validate the
> result against docs/beacon/beacon-schema.json. Save the three portal
> surfaces to docs/beacon/examples/{ts}-emission.json,
> {ts}-portal-markdown.md, {ts}-portal-graphml.xml. Open a draft PR.
```

The agent honours `cloud/AGENTS.md` §Safe-modification boundaries — it never modifies the constitutional core, only writes new files under `docs/beacon/examples/`.

### Entry C — Append a receptio entry

When the agent observes a Beacon emission's reception (e.g. a fresh review on a Beacon PR), append a row to `docs/logos/receptio.md`:

```text
> Append a new receptio.md §III row for the chatgpt-codex-connector
> review of PR #357 commit fda13ff. Use the BEACON-RECEPTIO-USE-NNN
> sub-namespace and a brief one-sentence summary of the feedback.
> Open a PR titled `receptio(beacon): log codex review of fda13ff`.
```

The agent appends append-only — it never edits prior rows.

## How the Codex Cloud agent participates in the Beacon distribution

When `beacon-emit.yml` (the orchestrator workflow, planned) runs a cycle, it issues a `repository_dispatch` of type `beacon-emit`. Codex Cloud agents subscribed to that event receive the dispatch payload, which carries the new `emission_id`. The agent then:

1. `GET ${BEACON_WORKERS_ROUTE}/emit?id={emission_id}` to fetch the emission (formal polarity JSON).
2. Perform one of three permitted derivative actions:
   - Compose a one-paragraph summary and open a PR appending it to `docs/logos/receptio.md`.
   - Compose a draft essay reflecting on the emission, save to `docs/beacon/examples/{ts}-essay.md`.
   - Propose a praxis closure if the emission contains evidence that a row in `docs/logos/praxis.md` is complete — comment on the praxis PR or the row's IRF issue.
3. End the session with a breadcrumb per the breadcrumb-protocol.

The agent never:

- Modifies the constitutional core (see `cloud/AGENTS.md` boundaries).
- Disables `private_fields_stripped` or any pre-emission gate.
- Pushes to `main`.

## Multi-agent etiquette

If multiple agents (Codex Cloud + Claude Code + Gemini Code Assist) operate in the same repo concurrently:

- Each agent prefixes its branch with its identifier: `codex/`, `claude/`, `gemini/`. The branch pattern is in `cloud/AGENTS.md` `push_targets`.
- Each agent reads `breadcrumb-protocol.md` to discover what prior agents did.
- Each agent opens at most one PR per session.
- The constructed-polis (AX-8) benefits from the diversity of bot reviewers; this is intentional.

## Cost expectations

| Item | Per emission | Per month (4 emissions) |
|------|-------------:|------------------------:|
| Codex Cloud agent invocation | ~$0.02 (8K tokens × $0.0025/1K) | ~$0.08 |
| OpenAI API for re-emission summaries | ~$0.01 | ~$0.04 |
| Cloudflare R2 storage | 0 (well within free tier) | 0 |
| Cloudflare KV operations | 0 (well within free tier) | 0 |
| Cloudflare Workers requests | 0 (well within 100K free) | 0 |
| **Total** | **~$0.03** | **~$0.12** |

If the Beacon goes viral and Workers requests exceed 100K/month, add ~$0.30 per additional 1M requests.

## Troubleshooting

### Codex Cloud cannot find the devcontainer

Codex Cloud expects the devcontainer at one of `.devcontainer/devcontainer.json`, `.devcontainer.json`, or specified explicitly. The Beacon's devcontainer is at `docs/beacon/cloud/devcontainer.json` because that is the contract-anchor. To make Codex Cloud find it:

```bash
# In the repo root, create a thin symlink:
ln -s docs/beacon/cloud/devcontainer.json .devcontainer/devcontainer.json
git add .devcontainer/devcontainer.json
git commit -m "chore(beacon): expose cloud devcontainer at .devcontainer/"
```

Or, configure the Codex Cloud environment's "Devcontainer path" setting to `docs/beacon/cloud/devcontainer.json`.

### `BEACON_WORKERS_ROUTE` returns 503

This indicates a mirror lag (local SQLite ahead of R2 / KV) per `../dam-storage.md` §Sync rule. Wait ~30s and retry; the orchestrator's next ALCHEMIZE pass should reconcile.

### Codex Cloud reports `Schema validation failed`

The emission record violates `beacon-schema.json`. Run locally:

```bash
python -m jsonschema -i path/to/emission.json docs/beacon/beacon-schema.json
```

Inspect the error and revise the emission.

### Agent boundary violation

If the agent halts citing `cloud/AGENTS.md` §write_blocked, the agent is behaving correctly — it caught itself before modifying a constitutional file. Investigate why the agent tried; usually the prompt was overly broad. Refine the prompt with explicit boundary acknowledgement.

## Refs

- OpenAI Codex Cloud documentation: https://developers.openai.com/codex/cloud/environments
- Devcontainer spec: https://containers.dev
- Cloudflare Workers: https://developers.cloudflare.com/workers/
- Cloudflare R2: https://developers.cloudflare.com/r2/
- This protocol's AGENTS contract: [`./AGENTS.md`](./AGENTS.md)
- This protocol's distribution spec: [`../dam-distribution.md`](../dam-distribution.md)
- The Workers `/emit` implementation: [`./workers/`](./workers/)

---

*Operators reading this walkthrough are part of the polis. Document your first Codex Cloud run in `../../logos/receptio.md` §III.*
