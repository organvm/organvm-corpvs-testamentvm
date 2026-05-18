# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is a **planning and governance documentation corpus** — not a source code repository. It contains the complete planning, audit, and implementation record for an eight-organ creative-institutional system ("ORGAN I–VII + Meta") that coordinates 97 GitHub repositories across 8 GitHub organizations (7 organ orgs + 1 meta-org).

**Owner:** @4444j99 / @4444J99
**Status:** LAUNCHED (2026-02-11) — all 8 organs OPERATIONAL
**Repository:** `a-organvm/organvm-corpvs-testamentvm` (canonical; `meta-organvm/organvm-corpvs-testamentvm` is a GitHub redirect to the same repo — both URLs resolve identically. Local clone tracks the canonical `a-organvm/` remote.)
**Documentation deployed:** ~6K+ words across 148 repos + 8 org profiles + 29 meta-system essays

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

> **Auto-generated zone below.** Everything between `<!-- ORGANVM:AUTO:START -->
## System Context (auto-generated — do not edit)

**Organ:** META-ORGANVM (Meta) | **Tier:** flagship | **Status:** GRADUATED
**Org:** `meta-organvm` | **Repo:** `organvm-corpvs-testamentvm`

### Edges
- **Produces** → `ORGAN-IV`: meta-documentation
- **Produces** → `META-ORGANVM/organvm-engine, META-ORGANVM/praxis-perpetua`: research-tasks
- **Produces** → `ALL`: work-registry
- **Produces** → `ALL`: prompt-registry
- **Produces** → `ALL`: session-continuation-prompts
- **Consumes** ← `ORGAN-IV`: orchestration-artifact

### Siblings in Meta
`.github`, `alchemia-ingestvm`, `schema-definitions`, `organvm-engine`, `system-dashboard`, `organvm-mcp-server`, `praxis-perpetua`, `stakeholder-portal`, `materia-collider`, `organvm-ontologia`, `vigiles-aeternae--agon-cosmogonicum`, `cvrsvs-honorvm`, `custodia-securitatis`

### Governance
- *Standard ORGANVM governance applies*

*Last synced: 2026-05-18T02:20:45Z*

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

Plans: 269 indexed | Chains: 5 available | SOPs: 8 active
Discover: `organvm plans search <query>` | `organvm chains list` | `organvm sop lifecycle`
Library: `/Users/4jp/Code/organvm/praxis-perpetua/library`


## Active Directives

| Scope | Phase | Name | Description |
|-------|-------|------|-------------|
| repo | any | registry-update-protocol | registry-update-protocol |
| system | any | atomic-clock | The Atomic Clock |
| system | any | execution-sequence | Execution Sequence |
| system | any | multi-agent-dispatch | Multi-Agent Dispatch |
| system | any | session-handoff-avalanche | Session Handoff Avalanche |
| system | any | system-loops | System Loops |
| system | any | prompting-standards | Prompting Standards |
| system | any | background-task-resilience | background-task-resilience |
| system | any | context-window-conservation | context-window-conservation |
| system | any | session-self-critique | session-self-critique |
| system | any | the-descent-protocol | the-descent-protocol |
| system | any | the-membrane-protocol | the-membrane-protocol |
| system | any | theory-to-concrete-gate | theory-to-concrete-gate |
| system | any | triangulation-protocol | triangulation-protocol |
| unknown | any | cicd-resilience | SOP: CI/CD Pipeline Resilience & Recovery |
| unknown | any | corpus-ontology-instantiation | SOP: Corpus Ontology Instantiation |
| unknown | any | document-audit-feature-extraction | SOP: Document Audit & Feature Extraction v2.0 |
| unknown | any | ira-grade-norming | SOP: Diagnostic Inter-Rater Agreement (IRA) Grade Norming |
| unknown | any | pitch-deck-rollout | SOP: Pitch Deck Generation & Rollout |
| unknown | any | ira-grade-norming | ira-grade-norming |
| unknown | any | SOP-001-vector-pipeline-activation | SOP-001: Vector Pipeline Activation |

Linked skills: SOP-TRIADIC-REVIEW-PROTOCOL, cicd-resilience-and-recovery, continuous-learning-agent, evaluation-to-growth, genesis-dna, multi-agent-workforce-planner, promotion-and-state-transitions, quality-gate-baseline-calibration, repo-onboarding-and-habitat-creation, session-self-critique, structural-integrity-audit, the-membrane-protocol, triple-reference


**Prompting (Anthropic)**: context 200K tokens, format: XML tags, thinking: extended thinking (budget_tokens)


## Task Queue (from pipeline)

**292** pending tasks | Last pipeline: unknown

- `cf0e6a3618d5` Vacuum Field Burn — 2026-04-22 Continuation (COMPLETED) [astro, chezmoi, python]
- `32bbf53c387b` Contains a specific, concrete, verifiable build/create/implement action [python]
- `0cf55989523a` Not a conversational fragment [python]
- `2132a5f8a357` Plausibly unfulfilled (not from a session that completed the work) [python]
- `df6c41742d78` Not a governance rule or behavioral constraint [python]
- `752ce7f34b39` Loads triage-batch-1.json [python]
- `62a994d3e34f` Applies classification rules in priority order [python]
- `f2b23b51a154` Writes {atom_id: status} mapping to triage-result-1.json [python]
- ... and 284 more

Cross-organ links: 264 | Top tags: `mcp`, `python`, `rollup`, `chezmoi`, `bash`

Run: `organvm atoms pipeline --write && organvm atoms fanout --write`


## System Density (auto-generated)

AMMOI: 25% | Edges: 0 | Tensions: 0 | Clusters: 0 | Adv: 27 | Events(24h): 37452
Structure: 8 organs / 148 repos / 1654 components (depth 17) | Inference: 0% | Organs: META-ORGANVM:63%, ORGAN-I:53%, ORGAN-II:48%, ORGAN-III:54% +5 more
Last pulse: 2026-05-18T02:20:27 | Δ24h: n/a | Δ7d: n/a


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