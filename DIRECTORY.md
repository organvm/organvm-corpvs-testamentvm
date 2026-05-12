# Directory

Concise map of the corpus. For detailed per-file annotations, see [`docs/ANNOTATED-MANIFEST.md`](docs/ANNOTATED-MANIFEST.md).

## Root

| File | Purpose |
|------|---------|
| `README.md` | Public landing page and quick navigation |
| `LICENSE` | CC BY-SA 4.0 |
| `CLAUDE.md` | Claude Code agent context and project rules |
| `DIRECTORY.md` | This file — corpus directory map |
| `registry-v2.json` | Single source of truth for all repo state |
| `INST-INDEX-RERUM-FACIENDARUM.md` | Universal work registry — the canonical gap between what the system IS and what it NEEDS TO BE. Part of the four-index classical apparatus (Faciendarum, Locorum, Nominum, Rerum). 76 items across 19 domains. |

## `.config/` — Org Naming Configuration

| File | Purpose |
|------|---------|
| `organvm.env` | Template env vars with `${ORGAN_PREFIX}` placeholders |
| `organvm.config.json` | Machine-readable organ→suffix→domain mapping |
| `organvm.env.local` | Instance config with resolved org names (gitignored) |

## `docs/` — All Documentation

### `docs/genesis/` — Layer 0: Foundational Transcripts & Audit

| File | Purpose |
|------|---------|
| `00-a-system-genesis-transcript.md` | Original ChatGPT session designing the organ system (~400KB) |
| `00-b-local-remote-structure-transcript.md` | Follow-up session on local/remote repo structure (~150KB) |
| `00-c-master-summary.md` | Executive summary distilling genesis into actionable plan |
| `00-d-organ-system-audit.md` | Current-state repo inventory per organ |
| `preparing-ai-handoff-autonomous-agent-scaffolding.md` | Pre-launch agent scaffolding and handoff protocols |
| `universal-orchestrator-architecture.md` | Early universal orchestrator design (pre-ORGAN-IV split) |
| `gemini-session-2026-02-15-organ-iv-architecture.md` | Gemini CLI session: ORGAN-IV automation engine design reasoning |
| `01-artistic-triforce-creative-ontology.md` | Creative ontology: three polarities (Conscious, Subconscious, Temporal) orthogonal to 8-organ structure |

### `docs/planning/` — Layer 1: Phase 1 Planning Toolkit

| File | Purpose |
|------|---------|
| `01-readme-audit-framework.md` | Scoring rubric for README quality assessment |
| `02-repo-inventory-audit.md` | Per-repo current state and gap analysis |
| `03-per-organ-readme-templates.md` | README templates customized per organ type |
| `04-per-organ-validation-checklists.md` | Quality checklists for each organ's deliverables |
| `05-risk-map-and-sequencing.md` | Risk assessment and optimal execution order |

### `docs/strategy/` — Layer 2: Execution Strategy & Roadmap

| File | Purpose |
|------|---------|
| `parallel-launch-strategy.md` | Strategic rationale for simultaneous 8-organ launch |
| `phase-1-execution-index.md` | Sprint-level execution plan for Phase 1 |
| `roadmap-there-and-back-again.md` | Full phased roadmap from Phase -1 through launch |

### `docs/implementation/` — Layer 3: v2 Active Specifications

| File | Purpose |
|------|---------|
| `implementation-package-v2.md` | Master execution plan with per-task TE budgets |
| `orchestration-system-v2.md` | Governance rules, promotion state machine, dependency model |
| `public-process-map-v2.md` | ORGAN-V content strategy and essay outlines |
| `github-actions-spec.md` | 5 CI/CD workflow specifications (YAML + Python) |
| `organ-iv-taxis-architecture.md` | ORGAN-IV automation engine architecture: API contracts, cascade flows, runbooks |

### `docs/evaluation/` — Layer 4: Cross-AI Validation & Review

| File | Purpose |
|------|---------|
| `06-evaluation-to-growth-analysis.md` | Evaluation-to-growth methodology applied to corpus |
| `07-cross-ai-logic-check-prompts.md` | Prompts for cross-AI validation of corpus coherence |
| `07-cross-ai-logic-check-results.md` | Results from cross-AI logic checks |
| `08-canonical-action-plan.md` | Consolidated action plan from evaluation findings |
| `09-corpus-coherence-review.md` | Full corpus coherence review |

### `docs/standards/` — Layer 5: Repository & Development Standards

| File | Purpose |
|------|---------|
| `10-repository-standards.md` | Naming, licensing, community health standards for all 44 repos |
| `11-specification-driven-development.md` | SDD methodology adapted for documentation deliverables |
| `12-habitat-governance-lifecycle.md` | Habitat governance lifecycle (LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED) |
| `13-organ-identity-and-placement.md` | Organ identity, placement, and inter-organ boundary rules |
| `14-logos-documentation-layer.md` | Inner-tier ontology: required `docs/logos/` files (`telos`, `pragma`, `praxis`, `receptio`, `alchemical-io`) per repo |
| `15-three-pure-systems.md` | Outer-tier ontology: every non-substrate file belongs to exactly one of CORPUS / ENGINE / SURFACE; vocabulary discipline between systems |

### `docs/logos/` — Layer 6: Inner-Tier Logos Narratives (this corpus)

Required by `14-logos-documentation-layer.md`. Closes the previous Symmetry: 0.0 (VACUUM) status reported in CLAUDE.md auto-gen.

| File | Purpose |
|------|---------|
| `telos.md` | The idealized form — what the corpus aspires to be |
| `pragma.md` | The concrete realization — what the corpus currently is |
| `praxis.md` | The remediation plan — attack vectors closing telos↔pragma gap |
| `receptio.md` | Bidirectional reception — what is read out, what is absorbed in from the contextual universe |
| `alchemical-io.md` | Metabolic narrative — sources, transmutation stages, returns, future self |

### `docs/agents/` — AI Agent Onboarding

| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent onboarding instructions and context |
| `GEMINI.md` | Gemini-specific agent configuration |

### `docs/validation-runs/` — Frozen CLI Validation Artifacts

Point-in-time outputs from CLI agent validation sessions. Contents are frozen.

| Directory | Contents |
|-----------|----------|
| `codex-cli/` | OpenAI Codex CLI validation runs |
| `gemini-cli/` | Google Gemini CLI validation runs |
| `github-copilot-cli/` | GitHub Copilot CLI validation runs |

### `docs/archive/` — Frozen v1 Predecessors & Pre-Launch Staging

Superseded by v2 documents at `docs/implementation/`. Do not modify.

| Directory | Contents |
|-----------|----------|
| `org-iv-orchestration-staging/` | Pre-launch ORGAN-IV staging (33 files): agent stubs, dreamcatcher prototype, coordination protocols, flow patterns |

### `docs/memory/` — Project Constitution

| File | Purpose |
|------|---------|
| `constitution.md` | Immutable project principles (Articles I-VI) and amendments |

### `docs/specs/` — Sprint Specifications

| Directory | Contents |
|-----------|----------|
| `bronze-sprint/` | Bronze sprint spec (`spec.md`) and validation checklist |

### `docs/operations/` — Standard Operating Procedures (excerpt)

The full operations directory contains rolling-todo, cadence, concordance, key-workflows, and several `sop--*.md` SOPs. SOPs are flat-named under the `sop--<slug>.md` convention; canonical copies live at `praxis-perpetua/standards/SOP--<NAME>.md`.

| File | Purpose |
|------|---------|
| `sop--corpus-ontology-instantiation.md` | **NEW** — Procedure for bringing any repo into compliance with `14-logos-documentation-layer.md` and `15-three-pure-systems.md`; closes Symmetry: 0.0 (VACUUM) status |
| `sop--cicd-resilience.md` | CI/CD pipeline resilience and recovery |
| `sop--document-audit-feature-extraction.md` | Document audit and feature-extraction protocol |
| `sop--ira-grade-norming.md` | Inter-rater agreement grade norming |
| `sop--pitch-deck-rollout.md` | Pitch deck generation and rollout |
| `operational-cadence.md` | Anti-patterns (AP-1..AP-7), review rhythm, when-to-start-sprints discipline |
| `rolling-todo.md` | Active P0/P1/P2/P3 work queue |
| `concordance.md` | Universal symbol table for invocation IDs across 7 namespaces |
