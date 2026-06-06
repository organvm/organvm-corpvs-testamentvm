# Alchemical I/O — `meta-organvm/organvm-corpvs-testamentvm`

> *Signal Transformations. The narrative of the corpus's metabolic inputs, processes, and outputs.*
> *What raw material does the corpus consume; what alchemical operation does it perform; what refined signal does it return?*

**Status:** Initial draft (filling the documented vacuum per `14-logos-documentation-layer.md`)
**Date:** 2026-05-09
**Counterpart files:** `telos.md`, `pragma.md`, `praxis.md`, `receptio.md`

---

## 1. Source (Inputs)

The corpus consumes raw signals from a wide contextual surface. Inputs cluster into seven streams:

### 1.1 Conversational Material
- **Live agent sessions** (Claude, Gemini, Codex, GPT) — every session that touches the corpus deposits prompts and atoms. Captured in `data/prompt-registry/sessions/` and `data/atoms/`.
- **Historical transcripts** — `docs/genesis/00-a-system-genesis-transcript.md` (~400KB ChatGPT session), `00-b-local-remote-structure-transcript.md` (~150KB), gemini-session transcripts. The corpus's foundational vocabulary is distilled from these.
- **Per-session continuation prompts** — emitted by the corpus *back into itself* for resuming paused work; consumers: ALL agents (per `seed.yaml`).

### 1.2 Registry and Telemetry
- **`repo-registry.json`** updates from cross-organ sprints — the canonical state of all 145 repos
- **`data/pulse/`** — system-pulse telemetry from `organvm` daemons
- **`data/dashboard/`** — system-dashboard data feeds
- **`data/organism/`** — organism-state snapshots
- **Live System Variables** (per CLAUDE.md auto-gen) refreshed by `organvm refresh`

### 1.3 Sibling-Repo Material (Cross-Organ Absorption)
Per CLAUDE.md "Edges": the corpus *consumes* `orchestration-artifact` from ORGAN-IV. The corpus also reads from sibling repos in `meta-organvm/`:
- `alchemia-ingestvm` (raw-material ingestion engine)
- `schema-definitions` (machine-readable schemas)
- `organvm-engine` (research-task implementation engine)
- `praxis-perpetua` (rolling library of plans, chains, SOPs)
- `system-dashboard` (telemetry presenter)
- `organvm-mcp-server` (MCP-protocol surface)
- `stakeholder-portal` (external-stakeholder interface)
- `materia-collider` (high-bandwidth ingestion)
- `organvm-ontologia` (canonical entity registry)
- `vigiles-aeternae--agon-cosmogonicum`, `cvrsvs-honorvm` (specialized siblings)

Each sibling produces artifacts that flow into the corpus via either direct file references, MCP tool calls, or registry updates.

### 1.4 External Scholarly and Tooling Surfaces
- **arXiv / HuggingFace Hub** (via MCP `hf_hub_query`, `hub_repo_search`) — paper IDs, model cards, dataset cards relevant to AI-conductor methodology
- **GitHub ecosystem** (via the GitHub MCP server) — sibling-org metadata, issue/PR streams, release tags
- **Anthropic API generation** — every Claude completion that lands in this corpus is itself an absorbed signal from Claude's distribution
- **Calendar, Drive, Notion** (per the loaded MCP tool list) — administrative context that may be referenced or imported

### 1.5 Public-Process Reverse Channel
- Essays published to ORGAN-V `public-process` — when external readers respond (via comments, citations, social-media engagement), the response flows back as receptio-typed material absorbed into `docs/applications/`, `docs/pitch/`, or new IRF entries

### 1.6 Validation-Run Outputs
- Cross-AI runs in `docs/validation-runs/` deposit critique into the corpus's self-knowledge; the corpus absorbs its own reflection

### 1.7 Constitutional and Standards Updates
- `docs/memory/constitution.md` Articles I–VI plus Amendments A–D and beyond
- `docs/standards/10`–`14` (and now `15`) — successive standards declarations
- IRF entries (`INST-INDEX-RERUM-FACIENDARUM.md`) — the work-registry's evolving content

## 2. Transmutation (Process)

The corpus's core alchemical operation is **distillation followed by structuration**. Six transformations in sequence:

### Stage 1 — Capture
Raw signal lands in an intake surface (`~/Workspace/intake/`, `data/atoms/`, `data/corpora/<week>/`, fossil append-points). At this stage the material is unprocessed and unrouted.

### Stage 2 — Triage and Routing
Per CLAUDE.md "Artifact Routing" decision tree (Q1/Q2/Q2b/Q3):
- Working code → `~/Workspace/<github-org>/<repo>/`
- Governance/planning → this corpus (routed by document layer to `docs/<layer>/`)
- Application materials → split between canonical (`docs/applications/`) and pipeline (`~/Workspace/4444J99/application-pipeline/`)
- Unsorted → `~/Workspace/intake/`

Triage classifies the system: CORPUS / ENGINE / SURFACE per `15-three-pure-systems.md`.

### Stage 3 — Distillation
Long-form raw material (transcripts, conversation corpora, validation-run logs) is distilled into shorter, structured forms:
- `docs/genesis/00-c-master-summary.md` is the distillation of `00-a` and `00-b` raw transcripts
- Sprint specs in `docs/specs/sprints/` distill rolling work into single-purpose specifications
- Essays in `essays/meta-system/` distill multi-week threads into single readable pieces

Distillation is performed by AI under human direction (the AI-conductor model). Volume is generated by the AI; the human enforces accuracy, voice, and routing.

### Stage 4 — Coagulation
Distilled material is set into authoritative containers:
- Schema-conformant entries in `repo-registry.json`
- Numbered standards in `docs/standards/`
- Constitutional Articles and Amendments in `docs/memory/constitution.md`
- IRF entries (each with a stable ID under one of 19 namespaces — IRF-SYS, IRF-OPS, IRF-DOC, IRF-RES, etc.)

Coagulation is irreversible at the artifact level: an `IRF-OPS-018` entry can be closed, archived, or referenced, but its identity is stable.

### Stage 5 — Cross-Reference Weaving
Coagulated artifacts are woven into the corpus's link graph:
- Per CLAUDE.md "Cross-Document Dependency Map", new content adds edges to the dependency graph
- The concordance (`docs/operations/concordance.md`) symbol table is updated with new namespace IDs
- `DIRECTORY.md` and `docs/ANNOTATED-MANIFEST.md` are updated to reflect the new artifacts

### Stage 6 — Broadcast (Optional)
For artifacts deemed publicly significant, the POSSE distribution workflow (`.github/workflows/posse-distribution.yml` per CLAUDE.md) syndicates to ORGAN-VII channels. This is the corpus's RETURN to the wider polis.

## 3. Return (Outputs)

Refined signals returned to the system fall into four classes:

### 3.1 Meta-Documentation (to ORGAN-IV)
Per `seed.yaml` `produces`: the corpus produces `meta-documentation` consumed by ORGAN-IV. Specifically: governance updates, process documentation, audit reports, and orchestration-relevant context.

### 3.2 Research Tasks (to META-ORGANVM/organvm-engine, praxis-perpetua)
The corpus produces `research-tasks` — implementation tasks extracted from the IRF research programme (IRF-RES entries). Consumers are the engine and praxis-perpetua, which execute the research.

### 3.3 Work Registry (to ALL)
The corpus produces the `work-registry` — the IRF (`INST-INDEX-RERUM-FACIENDARUM.md`) — consumed by every organ for gap-tracking. This is the corpus's most universally consumed output.

### 3.4 Prompt Registry and Continuation Prompts (to ALL)
- `prompt-registry`: 8,218 prompts → 31,649 atoms with implementation scorecard
- `session-continuation-prompts`: context-loaded continuation prompts emitted to resume paused sessions

These are the corpus's **operational outputs** — they don't just describe work, they enable subsequent work.

## 4. Future Self (Evolution Vector)

How does this implementation feed the corpus's own evolution?

1. **Logos symmetry restoration** (this PR) closes a long-standing self-violation: the corpus had a standard (`14-logos-documentation-layer.md`) it did not honor. Restoring symmetry is itself a step toward Future Self.
2. **Three-pure-systems doctrine** (`15-three-pure-systems.md` in this PR) makes explicit the architecture under which the corpus's own self-knowledge is organized. Future evolution will expand each pure system independently without contaminating the others.
3. **Generator manifest pipeline** (deferred to a follow-up PR in ENGINE territory) will mechanize the inner-form classification, so future additions to `docs/` are automatically classified. Drift detection becomes a CI check.
4. **Schema v1.2 adoption for `seed.yaml`** (deferred) will formalize the four logos summaries as machine-readable, enabling cross-repo logos symmetry computation.
5. **Logos→Essay extraction pipeline** (deferred, per `14-logos-documentation-layer.md` §5) will turn each significant logos update into a publishable essay, completing the public-process feedback loop.
6. **Cross-organ logos absorption** — once this corpus's `docs/logos/` is canonical, the patterns established here will roll outward to other meta-organvm repos and then to organ flagships, raising system-wide symmetry.
7. **Bibliography absorption** (open IRF entry under IRF-DOC) — explicit citation of the scholarly lineages enumerated in `receptio.md` §3.5, organized into a `docs/logos/bibliography.md` if and when the standard expands beyond the mandated five files.

## 5. Metabolic Cadence

| Cadence | Inputs absorbed | Outputs returned |
|---|---|---|
| Per-session | Conversation atoms, fossil entries | Updated atom registry, session-close prompts |
| Daily (soak) | System-pulse data | `data/soak-test/` snapshot |
| Daily (auto-refresh) | Live System Variables | Refreshed CLAUDE.md auto-gen zone |
| Per-PR | Standards updates, registry deltas | New permanent entries; cross-reference weave |
| Per-sprint close | Sprint deliverables | Promoted state in registry; closed IRF entries |
| Quarterly (proposed) | Logos symmetry audit | Cross-repo logos status report |

## 6. The Corpus as a Living Metabolism

The corpus is not a static archive. It is a **living metabolism** that continuously absorbs raw conversational, registry, and sibling-repo signal; transforms it through distillation–coagulation–weaving; and returns refined documentation, registry-state, and work-registry artifacts to the wider eight-organ system.

The metabolism's health is measurable:
- **Absorption rate** — atoms per week deposited (currently autonomous via post-commit hooks)
- **Transmutation latency** — time from intake to coagulated artifact (target: same-sprint)
- **Output reach** — consumers per produced artifact type (registry: ALL; meta-docs: ORGAN-IV; research-tasks: engine + praxis-perpetua)
- **Symmetry index** — Logos coverage ratio across the corpus (per `14-logos-documentation-layer.md` enforcement; tracked in CLAUDE.md auto-gen)

A defect in any of these metrics is itself absorbed (logged as a fossil, opened as an IRF entry, surfaced in `pragma.md`) — the metabolism's most distinctive property is that *its defects feed its own remediation*.
