# Telos Beacon Protocol — `docs/beacon/`

> The operational companion to [`../logos/`](../logos/). Where Logos is the prose corpus (telos, pragma, praxis, receptio), this directory is the schemas, configs, pipelines, and deployment glue.

## Two-directory split

| Directory | Holds | Audience |
|-----------|-------|----------|
| [`../logos/`](../logos/) | The four constitutional Tetradic docs (per `governance-rules.json` AX-7). Prose. | Humans (operators, contributors, philosophers); AI agents looking for context. |
| [`./`](./) (this dir) | Architecture, IA schema, DAM pipeline, env/container/cloud configs, examples, verification. | AI agents looking for instructions; engineers deploying or wiring; downstream REPRWA-style reusers. |

A reader who only wants the philosophical layer can stay in `../logos/`. A reader who wants to invoke, deploy, or extend reads here.

## Contents

| File | Purpose | Status |
|------|---------|--------|
| `README.md` (this file) | Orientation. | committed in this PR |
| `architecture.md` | Operational architecture: emission, portals, tethering, decentralized nodes. Maps every metaphysical concept to an existing primitive. | committed in this PR |
| `ia-schema.md` | Controlled vocabulary; namespaces (BEACON-NNN, TBP-NNN); cross-walk to existing `concordance.md` namespaces. | session 2 |
| `ia-indices.md` | Cross-references to Index Locorum (exists), Index Nominum (planned), Index Rerum (planned), INST-INDEX-RERUM-FACIENDARUM (exists). | session 2 |
| `dam-pipeline.md` | INTAKE → ABSORB → ALCHEMIZE → ATOMIZE → STORE → EXPORT → DISTRIBUTE wiring for Beacon assets, mostly via existing alchemia-ingestvm + mesh + distribute-content. | session 2 |
| `dam-storage.md` | Storage spec: SQLite (local), Cloudflare R2 (cloud), content-addressing via SHA-256, retention/versioning. | session 2 |
| `dam-distribution.md` | Channels: POSSE (existing) + HTTP `/emit` (Workers, new) + Codex Cloud agent invocation. | session 2 |
| `seed-extension-v1.1.md` | Spec for adding `beacon: {}` block to every repo's `seed.yaml`. | session 2 |
| `beacon-schema.json` | JSON Schema for a Beacon emission record (extends `seed.yaml.beacon`). | session 2 |
| `cloud/devcontainer.json` | Codex Cloud-compatible devcontainer. | session 3 |
| `cloud/.env.example` | BEACON_* env vars (documented). | session 3 |
| `cloud/AGENTS.md` | Codex Cloud agent invocation contract (tools expected/exposed; safe-modification boundaries). | session 3 |
| `cloud/codex-cloud.md` | OpenAI Codex Cloud agent integration walkthrough. | session 3 |
| `cloud/workers/wrangler.toml` | Cloudflare Workers config. | session 3 |
| `cloud/workers/worker.ts` | Minimal `/emit` endpoint stub. | session 3 |
| `cloud/workers/DEPLOY.md` | Deploy runbook (Cloudflare MCP tools used to provision R2 + KV). | session 3 |
| `examples/beacon-emission.json` | First emission rendered as a JSON record. | session 3 |
| `examples/portal-markdown.md` | Same emission, polymorphic surface for humans. | session 3 |
| `examples/portal-graphml.xml` | Same emission, polymorphic surface for analysts. | session 3 |
| `verification.md` | 8-point self-check + cross-section integrity rules. | session 3 |

## How the Beacon relates to the rest of ORGANVM

The Beacon is **not** a new system. It is a thin reflexive layer that names, schematizes, and pipes together infrastructure that already exists. The audit-of-record (`docs/audits/`) confirmed: every component the metaphysical theory names is already implemented somewhere in the 145-repo system. The Beacon Protocol is the *act of naming the constellation*; the stars were already there.

Concrete map:

| Telos Beacon concept | Existing primitive | Locator |
|----------------------|--------------------|---------|
| Beacon Core (high-density truth) | `governance-rules.json` LEX/AX axioms | this repo, root |
| Pulse Generator (oscillation formal ↔ aesthetic) | publish-process pipeline + organ-aesthetic.yaml cascade | testamentvm + .github/.github/ |
| Portals (polymorphic surfaces) | mesh `export` + stakeholder-portal Hermeneus + Jekyll site | mesh + meta-organvm + organvm-v-logos |
| Tether (drip-feed awareness) | conductor-playbook + breadcrumb-protocol + NON-INTERACTIVE-AGENT-SAFETY | orchestration-start-here/docs/ |
| Vector of Return (dead-zone detection) | mesh `query` primitive + `growth-vector` CLI | mesh/src/mesh/primitives/ |
| Decentralized nodes | per-repo `seed.yaml.beacon` field (spec in `seed-extension-v1.1.md`) | 145 repos × seed.yaml |
| Receptio sink | POSSE analytics + stakeholder-portal logs + PR comment streams | distribute-content.yml + Vercel + GitHub |

See [`architecture.md`](./architecture.md) for the full mapping with code paths.

## Constitutional anchor

`governance-rules.json` AX-7 (Tetradic Self-Knowledge) mandates the four `../logos/*.md` files. AX-8 (Constructed Polis) mandates the active production of receptio rather than waiting for it. AX-9 (Triple Reference Invariant) requires every referenceable item to exist in three places: IRF + repo-level reference + GitHub Issue — this PR honors AX-9 by anchoring each Beacon work-item to all three.

## License

This directory inherits the surrounding repo's license (CC BY-SA 4.0 for testamentvm). The reusable methodology pieces (templates, schemas, JSON Schema, devcontainer, AGENTS.md) are also tagged for derivation under MIT in `seed-extension-v1.1.md` to enable downstream commercial use; testamentvm-specific prose remains CC BY-SA 4.0.

## Reading order

1. [`../logos/README.md`](../logos/README.md) — the philosophical layer.
2. [`../logos/telos.md`](../logos/telos.md) — the North Star.
3. [`architecture.md`](./architecture.md) — operational architecture.
4. [`ia-schema.md`](./ia-schema.md) — schemas and vocabulary (session 2+).
5. [`dam-pipeline.md`](./dam-pipeline.md) — how content flows (session 2+).
6. [`cloud/codex-cloud.md`](./cloud/codex-cloud.md) — how Codex Cloud agents engage with the Beacon (session 3+).
