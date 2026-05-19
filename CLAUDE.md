# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **planning and governance documentation corpus** — not a source code repository. It contains the complete planning, audit, and implementation record for an eight-organ creative-institutional system ("ORGAN I–VII + Meta") that coordinates 97 GitHub repositories across 8 GitHub organizations (7 organ orgs + 1 meta-org).

**Owner:** @4444j99 / @4444J99
**Status:** LAUNCHED (2026-02-11) — all 8 organs OPERATIONAL
**Repository:** `a-organvm/organvm-corpvs-testamentvm` (canonical; `meta-organvm/organvm-corpvs-testamentvm` is a GitHub redirect to the same repo — both URLs resolve identically. Local clone tracks the canonical `a-organvm/` remote.)
**Documentation deployed:** ~882K+ words across 148 repos + 8 org profiles + 0 meta-system essays

There is no build system or unified test suite here. Executable artifacts include ~51 Python/shell scripts in `scripts/` (validation, deployment, audit, registry tooling), 16 GitHub Actions workflows in `.github/workflows/`, and YAML/Python workflow specifications in `docs/implementation/github-actions-spec.md`.

## The Eight-Organ Model

| Organ | Domain | GitHub Org | Repos | Flagships |
|-------|--------|-----------|-------|-----------|
| I | Theory (epistemology, recursion, ontology) | `organvm-i-theoria` | 20 | recursive-engine--generative-entity |
| II | Art (generative, performance, experiential) | `organvm-ii-poiesis` | 30 | metasystem-master, a-mavs-olevm |
| III | Commerce (SaaS, B2B, B2C products) | `organvm-iii-ergon` | 27 | public-record-data-scrapper |
| IV | Orchestration (governance, routing) | `organvm-iv-taxis` | 7 | orchestration-start-here, agentic-titan |
| V | Public Process (essays, building in public) | `organvm-v-logos` | 2 | public-process |
| VI | Community (salons, reading groups) | `organvm-vi-koinonia` | 4 | — |
| VII | Marketing (POSSE distribution, announcements) | `organvm-vii-kerygma` | 4 | — |
| VIII | Meta (umbrella org) | `meta-organvm` | 3 | organvm-corpvs-testamentvm |

## Key Invariants (Enforced Across All Documents)

1. **`registry-v2.json` is the single source of truth** — all repo state lives there
2. **No back-edges in dependency graph** — flow is I→II→III only; ORGAN-III cannot depend on ORGAN-II
3. **All 8 organs are represented at launch** — each organ has at least one flagship repo fully documented; remaining repos may launch as stubs or in-progress (compatible with Bronze/Silver/Gold tiered approach)
4. **Documentation precedes deployment** — no Phase 2 until Phase 1 is complete
5. **Every README is a portfolio piece** — written for grant reviewers and hiring managers, not just developers
6. **Promotion is a state machine** — LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED → ARCHIVED (governs cross-organ promotion; repo documentation status uses a separate vocabulary: ACTIVE/DEPLOYED/SKELETON/EMPTY)

## Document Architecture

### Reading Order

1. `docs/genesis/00-c-master-summary.md` — Executive summary, start here (30 min)
2. `docs/strategy/parallel-launch-strategy.md` — Strategic rationale for simultaneous launch
3. `docs/genesis/00-d-organ-system-audit.md` — Current-state repo inventory per organ
4. `registry-v2.json` — Machine-readable source of truth (skim)
5. `docs/implementation/implementation-package-v2.md` — Master execution plan with subtask TE budgets
6. `docs/implementation/orchestration-system-v2.md` — Governance rules and dependency model
7. `docs/planning/01` through `05` — Phase 1 planning details (audit framework, templates, checklists, risk map)
8. `docs/implementation/public-process-map-v2.md` — ORGAN-V content strategy and essay outlines
9. `docs/implementation/github-actions-spec.md` — 5 CI/CD workflow specifications (YAML + Python)
10. `docs/standards/10-repository-standards.md` — Repository standards for all repos (naming, licensing, community health)
11. `docs/standards/11-specification-driven-development.md` — SDD methodology adapted for documentation deliverables
12. `docs/genesis/00-a` and `00-b` — Deep genesis transcripts (optional, 60+ min each)

### Document Layers

- **Layer 0 (Genesis):** `docs/genesis/00-a`, `00-b`, `00-c`, `00-d` — conversational source material and audit
- **Layer 1 (Phase 1 Planning):** `docs/planning/01` through `05`, `docs/standards/10-repository-standards.md`, `docs/standards/11-specification-driven-development.md` — sequential planning toolkit (scoring rubric, inventory, templates, checklists, risk map, repository standards, SDD methodology)
- **Layer 2 (Execution):** `docs/strategy/phase-1-execution-index.md`, `docs/strategy/parallel-launch-strategy.md`, `docs/strategy/sprint-catalog.md` (76 named sprints across 18 categories)
- **Layer 3 (v2 Active):** `docs/implementation/implementation-package-v2.md`, `docs/implementation/orchestration-system-v2.md`, `docs/implementation/public-process-map-v2.md`, `registry-v2.json`, `docs/implementation/github-actions-spec.md`
- **Operations:** `docs/operations/` — rolling-todo.md (work queue), operational-cadence.md (anti-patterns, review rhythm), concordance.md (invocation symbol table), stranger-test-protocol.md, key-workflows.md
- **Archive:** `docs/archive/` contains v1 predecessors (superseded by v2 documents)

### Cross-Document Dependency Map

```
docs/genesis/00-a (Genesis Q&A)
  ├─→ 00-b (Local/Remote Structure)
  ├─→ 00-d (System Audit)
  │     ├─→ registry-v2.json
  │     └─→ docs/implementation/orchestration-system-v2.md
  └─→ 00-c (Master Summary)
        ├─→ docs/planning/01–05 (Phase 1 Planning)
        └─→ docs/strategy/phase-1-execution-index

docs/strategy/parallel-launch-strategy
  ├─→ docs/implementation/implementation-package-v2
  ├─→ docs/implementation/orchestration-system-v2
  ├─→ docs/implementation/public-process-map-v2
  ├─→ docs/implementation/github-actions-spec
  └─→ registry-v2.json
```

## Implementation History (All Complete)

- **Phase -1 (2026-02-09):** Org architecture — 8 GitHub orgs created, env-var config, naming scheme
- **Phase 0 (2026-02-10):** Corpus refinement — repo transfers, cross-AI validation, task manifest
- **Phase 1 (2026-02-10):** Documentation audit — Bronze Sprint (7 flagships), Silver Sprint (58 READMEs, ~202K words), Gold Sprint (essays, health files, workflows)
- **Phase 2 (2026-02-10):** Micro-validation — all 8 organs locked, 1,267 links audited, 31 dependency edges validated
- **Phase 3 (2026-02-10):** Integration — 5 GitHub Actions workflows, POSSE distribution, branch protection
- **Launch (2026-02-11):** 9/9 criteria met, all 8 organs OPERATIONAL
- **Gap-Fill Sprint (2026-02-11):** 11 repos created, 14 READMEs deployed, 14 tier promotions, ~270K total words

## TE (Tokens-Expended) Budget Model

Effort is measured in LLM API tokens, not human-hours. The AI-conductor model means: AI generates volume, human reviews and refines.

### Token Arithmetic
- 1 token ≈ 4 characters ≈ 0.75 words
- 3,000-word README ≈ 4,500 output tokens
- One generation pass (system + template + context + output) ≈ 15,000–20,000 tokens
- With 2–3 revision iterations + validation ≈ 50,000–90,000 tokens per README

### Per-Task TE Estimates
| Task Type | TE Budget |
|-----------|-----------|
| README REWRITE | ~72K TE |
| README REVISE | ~50K TE |
| README POPULATE | ~88K TE |
| README EVALUATE | ~24K TE |
| README ARCHIVE | ~12K TE |
| Essay (4,000–5,000 words) | ~120K TE |
| Validation Pass (per repo) | ~15K TE |
| GitHub Actions Workflow | ~55K TE |

### Phase Budgets
| Phase | TE Budget | Calendar |
|-------|-----------|----------|
| Phase 1 (Documentation) | ~4.4M TE | Sprints 1–2 |
| Phase 2 (Validation) | ~1.0M TE | Sprint 3 |
| Phase 3 (Integration) | ~1.1M TE | Sprint 4 |
| **Total** | **~6.5M TE** | **Criteria-driven (D-08)** |

## Org Naming Architecture

Org names are **env-var-driven** for templating. The system uses a prefix + Greek ontological suffix scheme:

- **Template config:** `.config/organvm.env` (committed, provides defaults)
- **Instance config:** `.config/organvm.env.local` (gitignored, contains `ORGAN_PREFIX=organvm`)
- **Machine-readable:** `.config/organvm.config.json` (maps organ numbers to suffixes, env vars, domains)

All org references in docs, registry, and workflows use the resolved instance names (e.g., `organvm-i-theoria`). The template defaults use `${ORGAN_PREFIX}-i-theoria` etc.

## Working With This Corpus

- When editing `registry-v2.json`, maintain the existing JSON schema. Every repo entry has: `name`, `org`, `status`, `public`, `description`, `documentation_status`, `portfolio_relevance`.
- ORGAN-III repos additionally carry `type` (SaaS/B2B/B2C/internal) and `revenue` fields.
- The `docs/archive/` directory is frozen — do not modify v1 files; create v2+ variants in `docs/implementation/` instead.
- Documents `01`–`05` are sequentially numbered outputs of the master summary (`00-c`). They form a cohesive planning toolkit and cross-reference each other. They live in `docs/planning/`.
- The `docs/ANNOTATED-MANIFEST.md` provides an exhaustive per-file annotation of the entire directory and is the best starting point for understanding what each document contains.
- The execution plan is in `docs/strategy/roadmap-there-and-back-again.md` — the phased implementation roadmap from Phase -1 (org architecture) through Phase 3 (launch).
- The project constitution is at `docs/memory/constitution.md` — immutable principles (Articles I-VI) and post-cross-validation amendments (A-D) that govern all specifications and quality gates.
- Feature specifications live in `docs/specs/` — each deliverable (e.g., `docs/specs/bronze-sprint/`) contains a `spec.md` (requirements and success criteria) and `checklists/requirements.md` (validation checklist). The SDD methodology is defined in `docs/standards/11-specification-driven-development.md`.
- The **governance quadrilateral** is: roadmap (`docs/strategy/there+back-again.md`) + cadence (`docs/operations/operational-cadence.md`) + catalog (`docs/strategy/sprint-catalog.md`) + rolling TODO (`docs/operations/rolling-todo.md`). These four documents govern all planning and execution.
- **GitHub issue tracking:** 58 omega-criteria + sprint-catalog issues + 11 RES-bundle commission issues (2026-05-09, INQ-2026-013, #339-#349) on `a-organvm/organvm-corpvs-testamentvm`, and 1 on `a-organvm/organvm-engine` (scorecard fix). All omega criteria and unexecuted sprints have bidirectional links between issues and documentation. (Canonical repo URL is `a-organvm/...`; older `meta-organvm/...` references redirect.)

## Invocation System

The governance corpus uses short IDs across 7 namespaces. When the user references an ID (e.g., "what's X1?", "show me AP-3", "which items advance #8", "status of IRF-SGO-001"), look up context in `docs/operations/concordance.md`.

| Prefix | Namespace | Source | Example |
|--------|-----------|--------|---------|
| X1–X4 | TODO: P0 hermetic seal | rolling-todo.md / e2g-ii | X1 = Submit Creative Lab Five |
| E1–E5 | TODO: P1 engagement | rolling-todo.md / e2g-ii | E3 = Google Creative Fellowship |
| M1-II–M6-II | TODO: P2 quality | rolling-todo.md / e2g-ii | M2-II = Stripe integration |
| S1-II–S6-II | TODO: P3 strategic | rolling-todo.md / e2g-ii | S2-II = Host first salon |
| G1–G3 | TODO: setup guide | rolling-todo.md | G2 = Render hosting |
| #1–#17 | Omega criteria | there+back-again.md | #8 = Product live |
| H1–H5 | Horizons | there+back-again.md | H3 = Generate Revenue |
| AP-1–AP-7 | Anti-patterns | operational-cadence.md | AP-1 = Don't start another sprint |
| W/SP/BS/LC/BL/ET/LO-II | E2G-II findings | e2g-ii-action-items.md | W1-II = Zero external contact |
| 01–33 | Completed sprints | docs/specs/sprints/ | 33 = OPERATIO |
| IRF-XXX-NNN | Index Rerum Faciendarum | INST-INDEX-RERUM-FACIENDARUM.md | IRF-SYS-001 = Consolidate CONSTITUTION.md |

CLI: `python3 scripts/invoke.py <ID>` for terminal lookup. See `docs/operations/concordance.md` for the full symbol table.

### The Index Apparatus

The **Index Rerum Faciendarum** (`INST-INDEX-RERUM-FACIENDARUM.md`) is the universal work registry — the canonical gap between what the system IS and what it NEEDS TO BE. It is the first of four classical indices:
- **Rerum Faciendarum** (things to be done) — governance instrument, THIS EXISTS
- **Locorum** (places) — reference instrument, PLANNED (IRF-IDX-001)
- **Nominum** (names) — reference instrument, PLANNED (IRF-IDX-002)
- **Rerum** (things) — reference instrument, PLANNED (IRF-IDX-003)

When closing a session, check the IRF for items completed or discovered. When starting a session, consult the IRF for P0/P1 items in the relevant domain.

## AI-Conductor Workflow Model

This corpus operates on an **AI-conductor model**: human directs, AI generates volume, human reviews and refines. Key implications for working with these documents:

- **Word count targets** (3,000+ words, 2,500+ words, etc.) are quality specifications, not labor estimates. AI generates the volume; human ensures accuracy and voice.
- **Time estimates** reflect human review time for AI-generated drafts, not writing time.
- **Quality assurance** is AI validation (template compliance, link checking, cross-references) + human strategic review (accuracy, positioning, portfolio language).
- **AI-specific risks** to watch for: hallucinated code examples, generic boilerplate phrasing, incorrect cross-references, missing project-specific context.

## Naming and Path Conventions

The workspace uses a flat 2-level structure that mirrors GitHub exactly:
```
~/Workspace/<github-org>/<repo>/
```
e.g. `~/Workspace/organvm-i-theoria/recursive-engine--generative-entity/`

Repo naming pattern: `[organ]-[type]--[specific-name]` (double-dash separates type from name).

## Artifact Routing

When completing tasks across the organ system, use this decision tree to determine where files should land:

**Q1: Working repo (code/application)?**
→ `~/Workspace/<github-org>/<repo>/`
  e.g. `~/Workspace/organvm-i-theoria/recursive-engine--generative-entity/`

**Q2: Governance/planning/architecture doc for the organ system?**
→ This corpus (`~/Workspace/meta-organvm/organvm-corpvs-testamentvm/`), routed by document layer:

| Artifact type | Destination |
|---|---|
| Raw transcript / session log | `docs/genesis/` |
| Planning toolkit / audit | `docs/planning/` |
| Strategy / roadmap | `docs/strategy/` |
| Implementation spec / workflow | `docs/implementation/` |
| Evaluation / review | `docs/evaluation/` |
| Standard / methodology | `docs/standards/` |
| ADR (short decision record) | `docs/adr/` |
| Sprint spec | `docs/specs/<sprint>/` |
| Application / submission (canonical source) | `docs/applications/` (covenant-ark, tracker, strategy — source of truth for identity/metrics) |
| Application / submission (pipeline ops) | `~/Workspace/4444J99/application-pipeline/` (pipeline YAML, blocks, variants, conversion tracking) |
| Essay draft | `docs/essays/` |

**Q2b: Application materials?**
→ Application work is split between two locations:
- **Canonical identity, metrics, evidence:** Stay in `docs/applications/` (covenant-ark is the source of truth)
- **Pipeline tracking, composable blocks, variants, conversion analytics:** Go to `~/Workspace/4444J99/application-pipeline/`
- When metrics change, update `docs/applications/00-covenant-ark.md` first, then propagate to `application-pipeline/blocks/`

**Q3: Unsorted / temporary / exploratory?**
→ `~/Workspace/intake/` (universal catch-all; triage later)

**NEVER** land files in: `~/` (home) or directly in `~/Workspace/` (only org directories and non-organ projects belong at the top level).

## Parent Directory Context

This corpus lives at `~/Workspace/meta-organvm/organvm-corpvs-testamentvm/`, alongside `~/Workspace/meta-organvm/alchemia-ingestvm/` in the meta-organvm org directory. The old path `~/Workspace/organvm-pactvm/ingesting-organ-document-structure/` is deprecated (restructured 2026-02-16).

## Commands

This corpus has no build system or unified test runner. The executable surface is:

```bash
# Invocation lookup (any namespace ID, e.g. IRF-OPS-018, X1, AP-3)
python3 scripts/invoke.py <ID>

# Regenerate the auto-gen zone of this CLAUDE.md (and sibling repo docs)
python3 scripts/generate-claude-md.py
# or, system-wide:
organvm refresh

# Audit / inventory
python3 scripts/organ-audit.py            # per-organ repo state
python3 scripts/calculate-metrics.py      # registry-driven metrics
python3 scripts/check-done-id.py          # cross-check DONE IDs vs IRF

# Convergence / promotion (state machine: LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED)
python3 scripts/convergence-validate.py
python3 scripts/convergence-promote.py
python3 scripts/convergence-triage.py

# Daily soak / health
bash scripts/daily-soak.sh
bash scripts/backup-all-orgs.sh

# Pre-commit (declared in .pre-commit-config.yaml)
pre-commit run --all-files
```

GitHub Actions live in `.github/workflows/` (16 workflows). CI is `ci.yml`; metrics
refresh, ecosystem audits, soak tests, stale detectors, and POSSE distribution run on
schedule. Trigger any of them manually with `gh workflow run <name>`.

> **Auto-generated zone below.** Everything between `<!-- ORGANVM:AUTO:START -->` and
> `<!-- ORGANVM:AUTO:END -->` is rewritten by `organvm refresh` / `scripts/generate-claude-md.py`.
> Edits inside the fence will be overwritten on the next regeneration. Add new content
> ABOVE the START marker.

<!-- ORGANVM:AUTO:START -->
## System Context (auto-generated — do not edit)

**Organ:** META-ORGANVM (Meta) | **Tier:** flagship | **Status:** GRADUATED
**Org:** `meta-organvm` | **Repo:** `organvm-corpvs-testamentvm`

### Edges
- **Produces** → `ORGAN-IV`: meta-documentation
- **Produces** → `META-ORGANVM/organvm-engine, META-ORGANVM/praxis-perpetua`: research-tasks
- **Produces** → `ALL`: work-registry
- **Consumes** ← `ORGAN-IV`: orchestration-artifact

### Siblings in Meta
`.github`, `alchemia-ingestvm`, `schema-definitions`, `organvm-engine`, `system-dashboard`, `organvm-mcp-server`, `praxis-perpetua`, `stakeholder-portal`, `materia-collider`, `organvm-ontologia`, `vigiles-aeternae--agon-cosmogonicum`, `cvrsvs-honorvm`

### Governance
- *Standard ORGANVM governance applies*

*Last synced: 2026-04-14T21:32:13Z*

## Active Handoff Protocol

If `.conductor/active-handoff.md` exists, **READ IT FIRST** before doing any work.
It contains constraints, locked files, conventions, and completed work from the
originating agent. You MUST honor all constraints listed there.

If the handoff says "CROSS-VERIFICATION REQUIRED", your self-assessment will
NOT be trusted. A different agent will verify your output against these constraints.

## Session Review Protocol

At the end of each session that produces or modifies files:
1. Run `organvm session review --latest` to get a session summary
2. Check for unimplemented plans: `organvm session plans --project .`
3. Export significant sessions: `organvm session export <id> --slug <slug>`
4. Run `organvm prompts distill --dry-run` to detect uncovered operational patterns

Transcripts are on-demand (never committed):
- `organvm session transcript <id>` — conversation summary
- `organvm session transcript <id> --unabridged` — full audit trail
- `organvm session prompts <id>` — human prompts only


## System Library

Plans: 269 indexed | Chains: 5 available | SOPs: 121 active
Discover: `organvm plans search <query>` | `organvm chains list` | `organvm sop lifecycle`
Library: `meta-organvm/praxis-perpetua/library/`


## Active Directives

| Scope | Phase | Name | Description |
|-------|-------|------|-------------|
| repo | any | registry-update-protocol | registry-update-protocol |
| organ | any | commit-and-release-workflow | Commit & Release Workflow |
| organ | any | session-state-management | session-state-management |
| organ | any | submodule-sync-protocol | submodule-sync-protocol |
| system | any | atomic-clock | The Atomic Clock |
| system | any | execution-sequence | Execution Sequence |
| system | any | multi-agent-dispatch | Multi-Agent Dispatch |
| system | any | session-handoff-avalanche | Session Handoff Avalanche |
| system | any | system-loops | System Loops |
| system | any | prompting-standards | Prompting Standards |
| system | any | research-standards-bibliography | APPENDIX: Research Standards Bibliography |
| system | any | phase-closing-and-forward-plan | METADOC: Phase-Closing Commemoration & Forward Attack Plan |
| system | any | research-standards | METADOC: Architectural Typology & Research Standards |
| system | any | sop-ecosystem | METADOC: SOP Ecosystem — Taxonomy, Inventory & Coverage |
| system | any | autonomous-content-syndication | SOP: Autonomous Content Syndication (The Broadcast Protocol) |
| system | any | autopoietic-systems-diagnostics | SOP: Autopoietic Systems Diagnostics (The Mirror of Eternity) |
| system | any | background-task-resilience | background-task-resilience |
| system | any | cicd-resilience-and-recovery | SOP: CI/CD Pipeline Resilience & Recovery |
| system | any | community-event-facilitation | SOP: Community Event Facilitation (The Dialectic Crucible) |
| system | any | context-window-conservation | context-window-conservation |
| system | any | conversation-to-content-pipeline | SOP — Conversation-to-Content Pipeline |
| system | any | cross-agent-handoff | SOP: Cross-Agent Session Handoff |
| system | any | cross-channel-publishing-metrics | SOP: Cross-Channel Publishing Metrics (The Echo Protocol) |
| system | any | data-migration-and-backup | SOP: Data Migration and Backup Protocol (The Memory Vault) |
| system | any | document-audit-feature-extraction | SOP: Document Audit & Feature Extraction |
| system | any | dynamic-lens-assembly | SOP: Dynamic Lens Assembly |
| system | any | essay-publishing-and-distribution | SOP: Essay Publishing & Distribution |
| system | any | formal-methods-applied-protocols | SOP: Formal Methods Applied Protocols |
| system | any | formal-methods-master-taxonomy | SOP: Formal Methods Master Taxonomy (The Blueprint of Proof) |
| system | any | formal-methods-tla-pluscal | SOP: Formal Methods — TLA+ and PlusCal Verification (The Blueprint Verifier) |
| system | any | generative-art-deployment | SOP: Generative Art Deployment (The Gallery Protocol) |
| system | any | market-gap-analysis | SOP: Full-Breath Market-Gap Analysis & Defensive Parrying |
| system | any | mcp-server-fleet-management | SOP: MCP Server Fleet Management (The Server Protocol) |
| system | any | multi-agent-swarm-orchestration | SOP: Multi-Agent Swarm Orchestration (The Polymorphic Swarm) |
| system | any | network-testament-protocol | SOP: Network Testament Protocol (The Mirror Protocol) |
| system | any | open-source-licensing-and-ip | SOP: Open Source Licensing and IP (The Commons Protocol) |
| system | any | performance-interface-design | SOP: Performance Interface Design (The Stage Protocol) |
| system | any | pitch-deck-rollout | SOP: Pitch Deck Generation & Rollout |
| system | any | polymorphic-agent-testing | SOP: Polymorphic Agent Testing (The Adversarial Protocol) |
| system | any | promotion-and-state-transitions | SOP: Promotion & State Transitions |
| system | any | recursive-study-feedback | SOP: Recursive Study & Feedback Loop (The Ouroboros) |
| system | any | repo-onboarding-and-habitat-creation | SOP: Repo Onboarding & Habitat Creation |
| system | any | research-to-implementation-pipeline | SOP: Research-to-Implementation Pipeline (The Gold Path) |
| system | any | security-and-accessibility-audit | SOP: Security & Accessibility Audit |
| system | any | session-self-critique | session-self-critique |
| system | any | smart-contract-audit-and-legal-wrap | SOP: Smart Contract Audit and Legal Wrap (The Ledger Protocol) |
| system | any | source-evaluation-and-bibliography | SOP: Source Evaluation & Annotated Bibliography (The Refinery) |
| system | any | stranger-test-protocol | SOP: Stranger Test Protocol |
| system | any | strategic-foresight-and-futures | SOP: Strategic Foresight & Futures (The Telescope) |
| system | any | styx-pipeline-traversal | SOP: Styx Pipeline Traversal (The 7-Organ Transmutation) |
| system | any | system-dashboard-telemetry | SOP: System Dashboard Telemetry (The Panopticon Protocol) |
| system | any | the-descent-protocol | the-descent-protocol |
| system | any | the-membrane-protocol | the-membrane-protocol |
| system | any | theoretical-concept-versioning | SOP: Theoretical Concept Versioning (The Epistemic Protocol) |
| system | any | theory-to-concrete-gate | theory-to-concrete-gate |
| system | any | typological-hermeneutic-analysis | SOP: Typological & Hermeneutic Analysis (The Archaeology) |
| unknown | any | SOP-001-vector-pipeline-activation | SOP-001: Vector Pipeline Activation |
| unknown | any | cicd-resilience | SOP: CI/CD Pipeline Resilience & Recovery |
| unknown | any | document-audit-feature-extraction | SOP: Document Audit & Feature Extraction v2.0 |
| unknown | any | ira-grade-norming | SOP: Diagnostic Inter-Rater Agreement (IRA) Grade Norming |
| unknown | any | ira-grade-norming | ira-grade-norming |
| unknown | any | pitch-deck-rollout | SOP: Pitch Deck Generation & Rollout |
| unknown | any | SOP-GENESIS-TEMPLATE | SOP: Genesis Template (SPEC-023) |
| unknown | any | SOP-TRIADIC-REVIEW-PROTOCOL | Triadic Review Protocol (TRP) |

Linked skills: cicd-resilience-and-recovery, continuous-learning-agent, cross-agent-handoff, evaluation-to-growth, genesis-dna, multi-agent-workforce-planner, promotion-and-state-transitions, quality-gate-baseline-calibration, repo-onboarding-and-habitat-creation, session-self-critique, structural-integrity-audit


**Prompting (Anthropic)**: context 200K tokens, format: XML tags, thinking: extended thinking (budget_tokens)


## Ecosystem Status

- **delivery**: 1/2 live, 1 planned
- **content**: 1/2 live, 0 planned

Run: `organvm ecosystem show organvm-corpvs-testamentvm` | `organvm ecosystem validate --organ META`


## Task Queue (from pipeline)

**9** pending tasks | Last pipeline: unknown

- `59fa8d4ca738` P0 — #1,#3,#17 [mcp]
- `761cbaa238ba` P1 — #9,#10 [mcp]
- `3aed48a1e4b2` P2 — #7 [mcp]
- `7130133e7f08` P3 — #12 [mcp]
- `854081a9892b` P4 — #2 [mcp]
- `8e800df88867` P5 — #11 [mcp]
- `acaa66097b58` P6 — #15 [mcp]
- `9580e4c16191` P7 — #4,#16 [mcp]
- ... and 1 more

Cross-organ links: 549 | Top tags: `python`, `bash`, `mcp`, `pytest`, `typescript`

Run: `organvm atoms pipeline --write && organvm atoms fanout --write`


## Entity Identity (Ontologia)

**UID:** `ent_repo_01KKKX3RVRY839D7ASSWA4HEZB` | **Matched by:** primary_name

Resolve: `organvm ontologia resolve organvm-corpvs-testamentvm` | History: `organvm ontologia history ent_repo_01KKKX3RVRY839D7ASSWA4HEZB`


## Live System Variables (Ontologia)

| Variable | Value | Scope | Updated |
|----------|-------|-------|---------|
| `active_repos` | 89 | global | 2026-04-14 |
| `archived_repos` | 54 | global | 2026-04-14 |
| `ci_workflows` | 107 | global | 2026-04-14 |
| `code_files` | 0 | global | 2026-04-14 |
| `dependency_edges` | 60 | global | 2026-04-14 |
| `operational_organs` | 10 | global | 2026-04-14 |
| `published_essays` | 29 | global | 2026-04-14 |
| `repos_with_tests` | 0 | global | 2026-04-14 |
| `sprints_completed` | 33 | global | 2026-04-14 |
| `test_files` | 0 | global | 2026-04-14 |
| `total_organs` | 10 | global | 2026-04-14 |
| `total_repos` | 145 | global | 2026-04-14 |
| `total_words_formatted` | 0 | global | 2026-04-14 |
| `total_words_numeric` | 0 | global | 2026-04-14 |
| `total_words_short` | 0K+ | global | 2026-04-14 |

Metrics: 9 registered | Observations: 32128 recorded
Resolve: `organvm ontologia status` | Refresh: `organvm refresh`


## System Density (auto-generated)

AMMOI: 58% | Edges: 42 | Tensions: 33 | Clusters: 5 | Adv: 23 | Events(24h): 32336
Structure: 8 organs / 145 repos / 1654 components (depth 17) | Inference: 98% | Organs: META-ORGANVM:65%, ORGAN-I:53%, ORGAN-II:48%, ORGAN-III:54% +5 more
Last pulse: 2026-04-14T21:31:36 | Δ24h: -1.0% | Δ7d: n/a


## Dialect Identity (Trivium)

**Dialect:** SELF_WITNESSING | **Classical Parallel:** The Eighth Art | **Translation Role:** The Witness — proves all translations compose without loss

Strongest translations: I (formal), IV (structural), V (analogical)

Scan: `organvm trivium scan META <OTHER>` | Matrix: `organvm trivium matrix` | Synthesize: `organvm trivium synthesize`


## Logos Documentation Layer

**Status:** MISSING | **Symmetry:** 0.0 (VACUUM)

Nature demands a documentation counterpart. This formation maintains its narrative record in `docs/logos/`.

### The Tetradic Counterpart
- **[Telos (Idealized Form)](../docs/logos/telos.md)** — The dream and theoretical grounding.
- **[Pragma (Concrete State)](../docs/logos/pragma.md)** — The honest account of what exists.
- **[Praxis (Remediation Plan)](../docs/logos/praxis.md)** — The attack vectors for evolution.
- **[Receptio (Reception)](../docs/logos/receptio.md)** — The account of the constructed polis.

### Alchemical I/O
- **[Source & Transmutation](../docs/logos/alchemical-io.md)** — Narrative of inputs, process, and returns.

- **[Public Essay](https://organvm-v-logos.github.io/public-process/)** — System-wide narrative entry.

*Compliance: Formation is currently void.*

<!-- ORGANVM:AUTO:END -->




## ⚡ Conductor OS Integration
This repository is a managed component of the ORGANVM meta-workspace.
- **Orchestration:** Use `conductor patch` for system status and work queue.
- **Lifecycle:** Follow the `FRAME -> SHAPE -> BUILD -> PROVE` workflow.
- **Governance:** Promotions are managed via `conductor wip promote`.
- **Intelligence:** Conductor MCP tools are available for routing and mission synthesis.