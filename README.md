# Eight-Organ System: Planning & Governance Corpus

[![CI](https://github.com/meta-organvm/organvm-corpvs-testamentvm/actions/workflows/ci.yml/badge.svg)](https://github.com/meta-organvm/organvm-corpvs-testamentvm/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-pending-lightgrey)](https://github.com/meta-organvm/organvm-corpvs-testamentvm)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/LICENSE)
[![Organ VIII](https://img.shields.io/badge/Organ-VIII%20Meta-6B7280)](https://github.com/meta-organvm)
[![Status](https://img.shields.io/badge/status-active-brightgreen)](https://github.com/meta-organvm/organvm-corpvs-testamentvm)
[![Python](https://img.shields.io/badge/lang-Python-informational)](https://github.com/meta-organvm/organvm-corpvs-testamentvm)


[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC%20BY--SA%204.0-lightgrey?style=flat-square)](LICENSE)
[![Status: LAUNCHED](https://img.shields.io/badge/Status-LAUNCHED-2e7d32?style=flat-square)](#current-status)
[![Organs: 8](https://img.shields.io/badge/Organs-8-1a237e?style=flat-square)](#the-eight-organ-model)
[![Repos: 97](https://img.shields.io/badge/Repos-148-2e7d32?style=flat-square)](#the-eight-organ-model)
[![Docs: ~6K+ words](https://img.shields.io/badge/Docs-~6K%2B%20words-6a1b9a?style=flat-square)](#current-status)

> Complete planning, audit, and implementation corpus for an eight-organ creative-institutional system coordinating 97 GitHub repositories across 8 organizations (7 organs + 1 meta). The system is **live** — all organs are operational.

This is **not a source code repository**. It is the authoritative planning and governance corpus for the organvm system — a framework that protects distinct modes of work (theory, art, commerce, community) from collapsing into each other, while presenting the meta-system itself as a portfolio asset. The system launched on 2026-02-11 with all 8 organs operational, 97 repositories, ~6K+ words of documentation, 29 meta-system essays, and automated governance via GitHub Actions.

---

## Quick Navigation

| If you want to... | Read this |
|-------------------|-----------|
| Understand the whole system in 30 minutes | [`00-c-master-summary.md`](docs/genesis/00-c-master-summary.md) |
| See the strategic rationale | [`parallel-launch-strategy.md`](docs/strategy/parallel-launch-strategy.md) |
| Know what repos exist and their status | [`registry-v2.json`](registry-v2.json) |
| See the execution plan | [`implementation-package-v2.md`](docs/implementation/implementation-package-v2.md) |
| Understand governance rules | [`orchestration-system-v2.md`](docs/implementation/orchestration-system-v2.md) |
| See the historical timeline (launch) | [`roadmap-there-and-back-again.md`](docs/strategy/roadmap-there-and-back-again.md) |
| See the forward roadmap (omega) | [`there+back-again.md`](docs/strategy/there+back-again.md) |
| Read the meta-system essays | [public-process on GitHub Pages](https://organvm-v-logos.github.io/public-process/) |
| See the orchestration hub | [orchestration-start-here](https://github.com/organvm-iv-taxis/orchestration-start-here) |
| See every file annotated | [`ANNOTATED-MANIFEST.md`](docs/ANNOTATED-MANIFEST.md) |

---

## Document Architecture

The corpus is organized in layers, each building on the previous:

```
Layer 0: Genesis (docs/genesis/)
  00-a (Q&A transcript) → 00-b (local/remote structure) → 00-c (master summary) → 00-d (system audit)

Layer 1: Phase 1 Planning (docs/planning/)
  01 (scoring rubric) → 02 (inventory) → 03 (templates) → 04 (checklists) → 05 (risk map)

Layer 2: Execution & Strategy (docs/strategy/)
  phase-1-execution-index → parallel-launch-strategy → roadmap-there-and-back-again

Layer 3: v2 Active Documents (docs/implementation/)
  implementation-package-v2 → orchestration-system-v2 → public-process-map-v2 → registry-v2.json → github-actions-spec

Layer 4: Evaluation & Cross-Validation (docs/evaluation/)
  06 (evaluation) → 07 (prompts + results) → 08 (canonical action plan) → 09 (corpus coherence review)

Layer 5: Standards & Configuration (docs/standards/ + .config/)
  10-repository-standards → 11-specification-driven-development → organvm.env → organvm.config.json

Archive: v1 predecessors (docs/archive/, frozen, superseded by v2)
```

The full cross-document dependency map and per-file annotations are in [`ANNOTATED-MANIFEST.md`](docs/ANNOTATED-MANIFEST.md).

For a concise directory map, see [`DIRECTORY.md`](DIRECTORY.md).

---

## Current Status

**The system is LAUNCHED.** All 8 organs are operational as of 2026-02-11.

| Milestone | Status |
|-----------|--------|
| Phase -1: Org architecture + config files | **DONE** (2026-02-09) |
| Phase -1: GitHub orgs live + repo transfers | **DONE** (2026-02-10) |
| Bronze Sprint: 7 flagship READMEs | **DONE** (2026-02-10) |
| Silver Sprint: 58 repo READMEs (~202K words) | **DONE** (2026-02-10) |
| Gold Sprint: Essays, health files, workflows, descriptions | **DONE** (2026-02-10) |
| Phase 2: Micro-validation (all 8 organs locked) | **DONE** (2026-02-10) |
| Phase 3: GitHub Actions, POSSE, branch protection | **DONE** (2026-02-10) |
| Launch: 9/9 criteria met | **DONE** (2026-02-11) |
| Gap-Fill Sprint: Uniform quality across all repos | **DONE** (2026-02-11) |
| Platinum Sprint: CI + CHANGELOG + ADR for every repo | **DONE** (2026-02-11) |
| Ignition Sprint: Essays 19-21, dependabot, evidence audit | **DONE** (2026-02-12) |
| Propulsion Sprint: 17 PROTOTYPE→ACTIVE promotions | **DONE** (2026-02-12) |
| Ascension Sprint: 12 promotions, 2 new repos, CI fixes | **DONE** (2026-02-12) |
| Exodus Sprint: Final promotions, app materials updated | **DONE** (2026-02-12) |
| Perfection Sprint: Portfolio site full-spectrum coverage | **DONE** (2026-02-12) |
| Autonomy Sprint: Autonomous orchestration + seed.yaml contracts | **DONE** (2026-02-13) |
| Genesis Sprint: Cross-org wiring + dispatch receivers | **DONE** (2026-02-13) |
| Alchemia Sprint: Orphan resolution + dependency consolidation | **DONE** (2026-02-13) |
| Convergence Sprint: System graph validation + edge audit | **DONE** (2026-02-13) |
| Praxis Sprint: Code audit + validation scripts hardened | **DONE** (2026-02-13) |
| Veritas Sprint: PRODUCTION→ACTIVE rename, revenue field split, honesty essay | **DONE** (2026-02-13) |
| Illustratio Sprint: Portfolio CMYK redesign, 17 cron workflows disabled | **DONE** (2026-02-14) |
| Manifestatio Sprint: Re-audit (7× more code), CI fixes, workflow validation | **DONE** (2026-02-14) |
| Operatio Sprint: Soak test, runbooks, stranger test protocol, AI-conductor essay | **DONE** (2026-02-16) |
| Synchronium Sprint: Clone missing repos, sync workspace | **DONE** (2026-02-16) |
| Concordia Sprint: Registry reconciliation, 6 orphan repos registered (91→97) | **DONE** (2026-02-16) |
| Tripartitum Sprint: Combined metrics correction + 19 sprint specs + doc alignment | **DONE** (2026-02-16) |
| Submissio Sprint: Application verification, 9 bundles verified, checklist created | **DONE** (2026-02-16) |
| Metricum Sprint: Metrics variable system (calculate→store→propagate pipeline) | **DONE** (2026-02-16) |
| Publicatio Sprint: 4 essays deployed (29→33), 3 new essays written | **DONE** (2026-02-16) |
| Canon Sprint: Catalog reconciliation, 4 numbering fixes, 4 historical headers | **DONE** (2026-02-16) |
| Inspectio Sprint: ORGAN-III beta assessment, life-my--midst--in selected | **DONE** (2026-02-16) |
| Propagatio Sprint: Findings propagation, fit scores reconciled, roadmap extended | **DONE** (2026-02-16) |
| Beta-Vitae Sprint: life-my--midst--in DB provisioned (44 tables), 3 migration bugs fixed, 2 essays deployed | **DONE** (2026-02-16) |

### Launch Metrics

| Metric | At Launch (02-11) | Current (02-17) |
|--------|-------------------|-----------------|
| Repos on GitHub | 77 | 97 |
| Documented repos (2,000+ word READMEs) | 72 | 73+ |
| Total documentation | ~270,000 words | ~404,000+ words |
| Flagship repos | 7 | 7 |
| Standard repos | 57 | 57 |
| ACTIVE status repos | — | 87 (89.7%) |
| Meta-system essays | 5 (21,625 words) | 36 (~132,000 words) |
| CI/CD workflows (across all repos) | 5 (meta-level) | 82+ (17 crons disabled for billing) |
| Dependency edges validated | 31 (0 violations) | 31 (0 violations) |
| POSSE channels | Mastodon + Discord | Mastodon + Discord |
| GitHub Pages | [public-process](https://organvm-v-logos.github.io/public-process/) | [public-process](https://organvm-v-logos.github.io/public-process/) |

---

## The Eight-Organ Model

| Organ | Domain | GitHub Org | Repos | Flagships | Portfolio Angle |
|-------|--------|-----------|-------|-----------|-----------------|
| I | Theory (epistemology, recursion, ontology) | [`organvm-i-theoria`](https://github.com/organvm-i-theoria) | 20 | recursive-engine--generative-entity | Intellectual foundations |
| II | Art (generative, performance, experiential) | [`organvm-ii-poiesis`](https://github.com/organvm-ii-poiesis) | 30 | metasystem-master, a-mavs-olevm | Creative practice |
| III | Commerce (SaaS, B2B, B2C products) | [`organvm-iii-ergon`](https://github.com/organvm-iii-ergon) | 27 | public-record-data-scrapper | Deployed products |
| IV | Orchestration (governance, routing) | [`organvm-iv-taxis`](https://github.com/organvm-iv-taxis) | 7 | orchestration-start-here, agentic-titan | System architecture |
| V | Public Process (essays, building in public) | [`organvm-v-logos`](https://github.com/organvm-v-logos) | 2 | public-process | Transparent methodology |
| VI | Community (salons, reading groups) | [`organvm-vi-koinonia`](https://github.com/organvm-vi-koinonia) | 4 | — | Relational infrastructure |
| VII | Marketing (POSSE distribution, announcements) | [`organvm-vii-kerygma`](https://github.com/organvm-vii-kerygma) | 4 | — | External communication |
| VIII | Meta (umbrella org) | [`meta-organvm`](https://github.com/meta-organvm) | 3 | organvm-corpvs-testamentvm | System-level coordination |

The organ model prevents three pathologies that commonly destroy creative systems: art corrupted by commercial pressure (when every project needs revenue justification), theory compromised by the need to scale (when ideas must be production-ready before they're explored), and community colonized by engagement metrics (when relationships are valued only for their conversion rates). Each organ has its own GitHub organization, its own governance rules, its own documentation standards, and its own definition of success. What counts as excellent work in ORGAN I (intellectual depth, novel frameworks) is deliberately different from what counts in ORGAN III (revenue potential, user experience).

Dependencies flow unidirectionally: **I → II → III**. Theory feeds art, art feeds commerce — but ORGAN-III cannot depend on ORGAN-II for ongoing maintenance, and ORGAN-II cannot demand that ORGAN-I produce "commercially viable" theory. This constraint, enforced by automated validation across all 31 declared dependency edges, is the system's most important design decision. It creates genuine creative tension: theory must commit to artistic expression without knowing if it will become a product, and products must stand on their own without leaning on the prestige of the theoretical work that inspired them. All organs are documented by V (Logos, the public process organ) and amplified by VII (Kerygma, the distribution organ).

---

## Implementation History

The eight-organ system was designed, documented, and deployed in a concentrated sequence of sprints — each with defined success criteria and measurable outputs. This velocity is itself evidence of the AI-conductor methodology's effectiveness.

**Phase -1 (2026-02-09):** Org architecture. Eight GitHub organizations created with Greek ontological suffixes (Theoria, Poiesis, Ergon, Taxis, Logos, Koinonia, Kerygma, plus meta-organvm). Environment variable configuration established via `.config/organvm.env` so that naming is templatable rather than hardcoded. Org-level profile READMEs deployed. The architectural decision to use separate GitHub organizations (rather than a monorepo or topic-based organization within a single org) was the system's foundational choice — it enforces organ boundaries at the platform level, preventing accidental coupling between theory, art, and commerce.

**Phase 0 (2026-02-10):** Corpus refinement. Repositories transferred to correct organizations, resolving naming conflicts and ensuring every repo lived under the org matching its organ assignment. Cross-AI validation of planning documents — Claude, Gemini, and GPT-4 each reviewed the corpus independently, producing the evaluation documents in `docs/evaluation/`. This triangulation caught inconsistencies that no single model would have found. The resulting task manifest drove all subsequent work.

**Phase 1 (2026-02-10):** Documentation audit across three sub-sprints. The **Bronze Sprint** produced 7 flagship READMEs (3,000+ words each) for the system's most important repositories — including recursive-engine--generative-entity, metasystem-master, agentic-titan, and orchestration-start-here. The **Silver Sprint** then generated 58 standard READMEs (2,000+ words each), totaling ~202K words of project documentation. Every README was written for a dual audience: grant reviewers evaluating creative practice, and hiring managers evaluating technical skill. The **Gold Sprint** completed the surrounding infrastructure — community health files (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY), five GitHub Actions workflow specifications, org descriptions, topic tags, and the first 5 meta-system essays published via ORGAN V.

**Phase 2 (2026-02-10):** Micro-validation. All 8 organs locked and audited. 1,267 links checked for integrity across the entire corpus. 31 dependency edges validated with zero violations — confirming the no-back-edges constraint holds across every declared relationship. Constitutional compliance verified against Articles I-VI.

**Phase 3 (2026-02-10):** Integration. Five GitHub Actions workflow specifications deployed (dependency validation, monthly audit, promotion, publish-process, content distribution). POSSE distribution channels configured for Mastodon and Discord. Branch protection rules established where org-level plans permitted.

**Launch (2026-02-11):** All 9/9 launch criteria met. Every organ had at least one flagship repository fully documented, the registry was complete and validated, dependency graph was acyclic, documentation exceeded quality gates, and POSSE channels were live. All 8 organs declared OPERATIONAL.

---

## Post-Launch Sprint History

After launch, a series of targeted sprints drove the system from launch-ready to portfolio-standard:

**Gap-Fill Sprint (2026-02-11):** Uniform quality across all repos. 11 new repos created to fill architectural gaps, 14 READMEs deployed, 14 tier promotions executed. Total documentation reached ~270K words across 77 repos.

**Platinum Sprint (2026-02-11):** CI/CD and health file standardization. Every repo received a CI workflow, CHANGELOG, and architectural decision record (ADR). 228 validation checks passed across the Platinum validation suite.

**Ignition Sprint (2026-02-12):** Three new essays (19-21) published, bringing the total to 21 essays (~88K words). The `nexus--babel-alexandria-` repo promoted to ACTIVE. Portfolio site fixed and live. Dependabot deployed across all orgs. Evidence URL audit passed.

**Propulsion Sprint (2026-02-12):** The largest batch promotion — 17 repos moved from PROTOTYPE to ACTIVE status. Stale CI configurations cleaned up. All application materials updated with current metrics.

**Ascension Sprint (2026-02-12):** 12 additional repo promotions. Three CI workflow fixes. Two new art-from repos (`art-from--recursive-engine` and `art-from--lingua-franca`) created in ORGAN II and deployed to ACTIVE. Dependabot alerts triaged across all organizations.

**Exodus Sprint (2026-02-12):** Final promotions including `commerce--meta` to ACTIVE, bringing the total to 84 ACTIVE repos (92.3%). All application materials updated to reflect current numbers (~386K+ words, 82+ CI workflows, 29 essays). Nine application bundles finalized as submission-ready — each tailored for a specific role or organization, with cover letters, project selections, and evidence URLs verified against the live system.

**Perfection Sprint (2026-02-12):** Portfolio site expanded from 14 to 20 curated projects across all 8 organs. Organs V (Logos), VI (Koinonia), and VII (Kerygma) — previously absent from the portfolio — received dedicated project pages. Orphan pages (Generative Music, AI-Conductor Model) integrated into the organ group structure. All stale statistics updated across the portfolio site, resume, and about page. The meta-README (this document) expanded from ~1,049 words to 3,000+ words to meet the portfolio standard.

**Autonomy Sprint (2026-02-13):** Autonomous orchestration infrastructure. The `seed.yaml` contract schema (v1.0) deployed across all repos, establishing produces/consumes/subscriptions edges. The orchestrator-agent, promotion-recommender, and validate-dependencies workflows deployed to ORGAN-IV. 115 seed.yaml contract edges declared across the system.

**Genesis Sprint (2026-02-13):** Cross-org wiring. `dispatch-receiver.yml` deployed to all 8 org `.github` repos. `CROSS_ORG_TOKEN` secret established for cross-org `repository_dispatch` events. The autonomous system can now route events between organs without manual intervention.

**Alchemia Sprint (2026-02-13):** Orphan resolution. 34 repos received organ-level produces/consumes declarations (e.g., ORGAN-II produces `creative-artifact`, consumes `theory` from ORGAN-I). The dependency graph gained meaningful semantic edges beyond the structural I→II→III flow.

**Convergence Sprint (2026-02-13):** System graph validation. All seed.yaml files audited for consistency. Back-edge violations detected and fixed (2 repos had incorrect dependency directions). Distribution-agent and essay-monitor workflows deployed and validated.

**Praxis Sprint (2026-02-13):** Code substance audit and validation hardening. `praxis-validate.py` updated to accept all valid implementation statuses (ACTIVE, PROTOTYPE, SKELETON, DESIGN_ONLY, ARCHIVED). E2G full-system review completed, producing the prioritized action items that guided subsequent sprints.

**Veritas Sprint (2026-02-13):** Honesty sprint. `implementation_status: PRODUCTION` renamed to `ACTIVE` across 82 repos — acknowledging that "production" overstates reality for documented-but-not-deployed repos. Revenue field split: `revenue` → `revenue_model` + `revenue_status` across all 24 ORGAN-III repos. 9 future-dated essays corrected to actual creation dates. Honesty essay deployed to ORGAN-V.

**Illustratio Sprint (2026-02-14):** Portfolio CMYK redesign. Jost font + cyan/magenta/yellow color scheme deployed. p5.js generative sketches added to 9 portfolio pages. Puter.js LLM consultation page created. 17 cron workflows disabled across ORGAN-I and ORGAN-III to resolve GitHub Actions billing overrun (48,880 minutes on organvm-i-theoria).

**Manifestatio Sprint (2026-02-14):** System-wide re-audit revealing 7× more code than previously measured (3,586 code files vs ~500 estimated). Language detection fixed (agentic-titan: TypeScript→Python). 3 CI workflow fixes deployed. 2 back-edge dependency violations corrected. Application materials and engagement baseline prepared.

**Operatio Sprint (2026-02-16):** Operational readiness. 30-day soak test monitor built (`scripts/soak-test-monitor.py`) and started. 3 operational runbooks written (minimum viable operations, emergency procedures, key workflows). Stranger test protocol drafted. AI-conductor methodology essay drafted (4,000+ words). The system transitions from construction sprints to sustained operation.

**Remedium Sprint (2026-02-16):** Workflow health investigation. All orchestration workflows diagnosed — no actual failures found. "Failing" signals were phantom failures caused by push events triggering schedule-only workflows. CI already replaced by Minimal CI. Validate-dependencies already fixed in Convergence. The system is healthier than monitoring suggested.

**Synchronium Sprint (2026-02-16):** Full workspace synchronization. All 97 repos cloned to flat `~/Workspace/<org>/<repo>/` layout. 14 missing repos cloned, 8 `.github` org profiles retrieved, 68 repos migrated from legacy 7-level hierarchy, 39 symlinks removed, git remotes converted SSH→HTTPS. 29 GB freed from disk.

**Concordia Sprint (2026-02-16):** Registry reconciliation with actual GitHub state. 6 orphan repos discovered and registered (91→97 total). `render-second-amendment` deleted locally (14 GB freed). 2 LFS checkout failures fixed. Seed.yaml coverage audited (38/86 = 44%).

**Tripartitum Sprint (2026-02-16):** Three-part combined sprint — metrics correction, sprint spec writing, and document alignment. 13 files updated with ~70 edits correcting stale metrics. 19 retrospective sprint specs written in `docs/specs/sprints/`. All active documents aligned with `registry-v2.json`.

**Submissio Sprint (2026-02-16):** Application verification and submission preparation. All 9 submission bundles verified against current metrics (97 repos, ~398K+ words, 33 essays). Step-by-step submission checklist created (`docs/applications/08-submission-checklist.md`). Human form-filling is the remaining step.

**Metricum Sprint (2026-02-16):** Metrics variable system. Three scripts deployed: `calculate-metrics.py` (compute live counts from registry + GitHub API), `metrics-variables.json` (persistent store), and `propagate-metrics.py` (find-and-replace stale values across documents). Ensures metrics consistency without manual cross-referencing.

**Publicatio Sprint (2026-02-16):** Essay deployment push. 4 essays deployed to public-process (29→33 total, ~123K essay words). 3 new essays written: autonomous systems guide, commerce-vs-theory philosophical piece, governance frameworks for artists. 1 existing draft deployed (promotions-in-practice). Metrics propagated across 18 files.

**Canon Sprint (2026-02-16):** Catalog reconciliation. The sprint catalog had 4 numbering collisions between hypothetical catalog assignments and actually-executed sprints (19-22). Collisions resolved: canonical numbers established in `docs/specs/sprints/`, displaced catalog items marked as unscheduled. 4 historical document headers added to implementation-era files pointing readers to current authoritative documents.

**Inspectio Sprint (2026-02-16):** First product assessment sprint. The top 5 ORGAN-III repos evaluated across 10 dimensions (tech stack, feature completeness, deployment readiness, test coverage, revenue model fit). `life-my--midst--in` selected as the recommended beta product — feature-complete with 1,694 code files, Docker/Railway/Vercel deployment infrastructure, and a clear freemium revenue model. Product brief written. Operational cadence updated with staleness note.

---

## The AI-Conductor Model

This corpus was produced using an **AI-conductor model** of human-AI collaboration: the human acts as conductor — setting direction, making structural decisions, maintaining quality standards, and approving every output — while AI acts as the orchestra, generating volume at speed.

This is not "AI wrote my portfolio." It is a designed production methodology with explicit roles:

- **Human provides:** Strategic direction, structural decisions, quality criteria, voice and tone, factual accuracy review, and final approval for every document.
- **AI provides:** Draft generation at speed, consistent formatting, template compliance, volume production, and initial cross-reference checking.

The methodology is measured in LLM API tokens, not human-hours. A typical 3,000-word README consumes ~50-90K tokens across 2-3 revision iterations (system prompt + template + project context + generation + revision). An essay (4,000-5,000 words) costs ~120K tokens. A validation pass costs ~15K tokens per repository. The total system budget across all phases was ~6.5 million tokens, producing ~6K+ words of reviewed, deployed documentation. The bottleneck is never generation speed — it's review quality. Every document passes through human accuracy review before deployment.

The most important aspect of the AI-conductor model is its quality infrastructure. Every AI-generated document passes through the same promotion state machine as everything else in the system — specifications, quality gates, validation checklists. This prevents the most common AI failure mode: plausible text that doesn't say anything useful. The risks we actively monitor include hallucinated code examples (all samples tested or sourced from actual repos), generic boilerplate (project-specific briefs and human review for voice), and incorrect cross-references (automated link checking across 1,267+ links).

The AI-conductor model is documented extensively in the ORGAN V essays, particularly in the methodology and token economics essays. Every document in the system is transparent about its production method. The 41 essays at [public-process](https://organvm-v-logos.github.io/public-process/) provide the most detailed account, including honest post-mortems on what the model gets wrong and where human oversight is non-negotiable.

---

## Repository Standards

Every repository in the eight-organ system meets a defined quality floor:

- **README:** 2,000+ words minimum (flagships: 3,000+), written for grant reviewers and hiring managers. Each README includes a badge row, project description, architecture overview, and honest assessment of tradeoffs.
- **CI/CD:** 70+ repos carry GitHub Actions workflows — linting, testing, or build validation depending on the repo's tech stack. CI status is tracked in `registry-v2.json`.
- **CHANGELOG:** Present in every repo, following Keep a Changelog format. Documents the progression from initial creation through documentation sprints to current status.
- **Community health files:** CONTRIBUTING.md, CODE_OF_CONDUCT.md, and SECURITY.md inherited from org-level `.github` repositories where possible, with repo-specific overrides where needed.
- **Architectural Decision Records:** 130+ ADRs across the system documenting key design choices — technology selections, dependency declarations, naming decisions, and tradeoff analyses.

The complete standards specification is in [`docs/standards/10-repository-standards.md`](docs/standards/10-repository-standards.md). The Specification-Driven Development methodology used to produce deliverables is in [`docs/standards/11-specification-driven-development.md`](docs/standards/11-specification-driven-development.md).

---

## Validation Infrastructure

Five validation scripts in [`scripts/`](scripts/) enforce system integrity:

1. **Registry validation** — verifies `registry-v2.json` schema compliance: every repo entry has required fields (name, org, status, public, description, documentation_status, portfolio_relevance), ORGAN-III entries carry additional `type`, `revenue_model`, and `revenue_status` fields.
2. **Dependency graph validation** — checks all 62 dependency edges for acyclicity and enforces the no-back-edges constraint (I→II→III only). Detects circular dependencies and cross-organ violations.
3. **Documentation completeness** — audits every repo for README presence, minimum word count, badge row, and required sections.
4. **Link integrity** — checks all cross-references across the corpus (1,267+ links audited at launch).
5. **Constitutional compliance** — verifies adherence to the system constitution ([`docs/memory/constitution.md`](docs/memory/constitution.md)), including Articles I-VI and post-cross-validation amendments A-D.

These scripts are designed to run both locally and in CI. The GitHub Actions workflow `validate-dependencies` triggers on every registry change, preventing merges that would violate system invariants. The `monthly-organ-audit` workflow performs a full system health check — examining every repo's documentation status, CI presence, dependency declarations, and constitutional compliance — and generates a Markdown report with JSON metrics suitable for automated dashboards.

The Platinum validation suite adds additional checks: CI workflow presence, CHANGELOG files, architectural decision records, badge rows, and implementation status fields. 228 checks pass across the full suite, giving high confidence that the system's quality claims are backed by automated verification rather than manual assertion.

---

## How to Use This Corpus

### For Human Readers

1. **Start with** [`00-c-master-summary.md`](docs/genesis/00-c-master-summary.md) for a 30-minute overview of the system's design
2. **Browse** [`registry-v2.json`](registry-v2.json) to see all 97 repos with their status, tiers, and documentation state
3. **Read the essays** at [public-process](https://organvm-v-logos.github.io/public-process/) for the meta-system narrative
4. **Reference** the numbered documents (`01`–`05`) in [`docs/planning/`](docs/planning/) for the original planning methodology

### For AI Agents

- **Claude Code:** Read [`CLAUDE.md`](CLAUDE.md) first — it provides full project context, key invariants, and document architecture
- **Gemini:** Read [`docs/agents/GEMINI.md`](docs/agents/GEMINI.md) for Gemini-specific onboarding
- **Any agent:** Read [`docs/agents/AGENTS.md`](docs/agents/AGENTS.md) for universal agent guidelines (commit style, testing, security)
- **Full file inventory:** [`docs/ANNOTATED-MANIFEST.md`](docs/ANNOTATED-MANIFEST.md) provides exhaustive per-file annotations

### Key Invariants

1. `registry-v2.json` is the single source of truth for all repo state
2. No back-edges in the dependency graph (I → II → III only)
3. All 8 organs are represented at launch
4. Documentation precedes deployment
5. Every README is a portfolio piece
6. Promotion is a state machine: LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED → ARCHIVED

---

## Why This System Exists

The eight-organ system began with a question: what happens when you apply the same rigor to organizing creative work that engineers apply to organizing code? Most creative portfolios are flat — a list of projects with screenshots and descriptions. The relationships between projects are implicit, the governance is invisible, and the organizational logic is whatever the creator happened to do most recently.

This system takes a different approach. The relationships between projects are explicit (declared dependencies in the registry), the governance is visible (promotion state machines, validation scripts, constitutional articles), and the organizational logic is itself a designed artifact (eight organs with distinct responsibilities and no back-edges). The meta-system isn't overhead on top of the creative work — it *is* the creative work, or at least the most interesting part of it.

The practical consequence is that this portfolio can answer questions that flat portfolios cannot: How do theory projects relate to commercial products? (Through declared dependency edges.) How do you maintain quality across 148 repos? (Through automated validation and documented standards.) How do you prevent different types of work from corrupting each other? (Through organ-level separation with GitHub organizations as the enforcement boundary.) How was ~6K+ words of documentation produced in nine days? (Through the AI-conductor model, documented transparently.)

For grant reviewers, the system demonstrates sustained creative practice with institutional ambition — not just individual projects but the infrastructure that connects them. For hiring managers, it demonstrates systems architecture, governance design, and the ability to ship at scale with quality. For fellow practitioners, it offers a reusable model for organizing creative work that goes beyond "put it all in one repo and hope for the best."

The system is open. The documentation is public. The methodology is documented. The mistakes are visible. That's the point.

---

## License

This work is licensed under the [Creative Commons Attribution-ShareAlike 4.0 International License](LICENSE) (CC BY-SA 4.0).

You are free to share and adapt this material for any purpose, including commercial, as long as you give appropriate credit and distribute derivative works under the same license.

---

## Author

**@4444j99** / **@4444J99**

This corpus operates on an AI-conductor model: human directs, AI generates volume, human reviews and refines. The meta-system — and the process of building it — is itself the primary portfolio artifact.

<!-- SYSTEM-NAV-START -->

---

<sub>[Portfolio](https://4444j99.github.io/portfolio/) · [System Directory](https://4444j99.github.io/portfolio/directory/) · [ORGAN Meta](https://meta-organvm.github.io/) · Part of the <a href="https://4444j99.github.io/portfolio/directory/">ORGANVM eight-organ system</a></sub>

<!-- SYSTEM-NAV-END -->
