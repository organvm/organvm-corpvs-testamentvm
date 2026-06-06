# How I Used 4 AI Agents to Cross-Validate an Eight-Organ System

[![ORGAN-V: Public Process](https://img.shields.io/badge/ORGAN--V-Public%20Process-00695c?style=flat-square)](https://github.com/organvm-v-logos)
[![Status](https://img.shields.io/badge/status-draft--in--progress-yellow?style=flat-square)]()
[![License](https://img.shields.io/badge/license-CC%20BY--SA%204.0-blue?style=flat-square)](LICENSE)

> Building in public: the methodology, cross-validation cycle, and lessons learned from coordinating ~79 repositories across 8 GitHub organizations using AI agents as an ensemble of specialized reviewers.

[Introduction](#introduction) | [The Eight-Organ Model](#the-eight-organ-model) | [Methodology](#methodology) | [The Cross-Validation Cycle](#the-cross-validation-cycle) | [Per-Agent Findings](#per-agent-findings) | [Synthesis](#synthesis) | [Simulating Organizational Scale](#simulating-organizational-scale-in-solo-practice) | [Lessons Learned](#lessons-learned) | [Cross-References](#cross-references)

---

## Introduction

This essay documents the process of building and launching an eight-organ creative-institutional system — a coordinated architecture of ~79 GitHub repositories across 8 organizations — using AI agents not as code generators but as **specialized reviewers in a cross-validation ensemble**.

The conventional narrative about AI-assisted development focuses on code generation: write a prompt, get a function. This project demonstrates a different model. Four AI agents (Claude, Gemini, ChatGPT, Copilot) were given the same planning corpus and asked to independently evaluate the system architecture, identify risks, and propose execution strategies. Their responses were then cross-validated against each other to produce a canonical action plan that no single agent — and no single human — could have produced alone.

The result is not just a set of repositories. It is evidence that **AI agents can serve as an organizational simulation** — providing the diversity of perspective, constructive disagreement, and systematic review that would normally require a team of 4-6 specialists.

This essay is itself an ORGAN-V artifact: a public-process document that makes the methodology visible, inspectable, and reproducible.

---

## The Eight-Organ Model

The system organizes creative and institutional work into eight specialized organs, each with its own GitHub organization:

| Organ | Domain | Organization | Function |
|-------|--------|-------------|----------|
| **I** | Theory | [organvm-i-theoria](https://github.com/organvm-i-theoria) | Epistemological frameworks, recursive engines, ontological systems |
| **II** | Art | [organvm-ii-poiesis](https://github.com/organvm-ii-poiesis) | Generative art, performance systems, experiential computing |
| **III** | Commerce | [organvm-iii-ergon](https://github.com/organvm-iii-ergon) | SaaS products, B2B tools, commercial applications |
| **IV** | Orchestration | [organvm-iv-taxis](https://github.com/organvm-iv-taxis) | Multi-agent governance, routing, coordination frameworks |
| **V** | Public Process | [organvm-v-logos](https://github.com/organvm-v-logos) | Essays, methodology documentation, building in public |
| **VI** | Community | [organvm-vi-koinonia](https://github.com/organvm-vi-koinonia) | Salons, reading groups, collaborative encounters |
| **VII** | Marketing | [organvm-vii-kerygma](https://github.com/organvm-vii-kerygma) | POSSE distribution, announcements, brand presence |
| **VIII** | Meta | [meta-organvm](https://github.com/meta-organvm) | Umbrella organization coordinating all seven organs |

The model enforces **unidirectional dependencies**: Theory (I) informs Art (II) which informs Commerce (III). No organ depends on a downstream organ. Orchestration (IV) coordinates across organs without creating circular dependencies. This constraint is not bureaucratic — it is an architectural invariant that prevents the system from becoming a tangled dependency graph.

The naming uses Greek ontological suffixes (*theoria*, *poiesis*, *ergon*, *taxis*, *logos*, *koinonia*, *kerygma*) to signal that the organ system is not arbitrary categorization but a structured ontology of creative-institutional functions.

---

## Methodology

### The AI-Conductor Model

The project operates on what we call the **AI-conductor model**: the human directs, AI generates volume, the human reviews and refines. This is distinct from both "AI writes everything" and "human writes everything with AI suggestions."

In practice, the model works as follows:

1. **Human defines the architecture** — organ boundaries, dependency rules, quality standards, success criteria
2. **AI agents generate candidate implementations** — README drafts, registry schemas, workflow specifications, risk analyses
3. **Human reviews against specification** — not "does this look good?" but "does this satisfy the measurable requirements?"
4. **AI agents cross-validate** — each agent reviews the others' output, flagging disagreements and blind spots
5. **Human resolves conflicts** — when agents disagree, the human makes the final call using the constitution as the tiebreaker

This model is particularly powerful for documentation-heavy projects where the primary output is prose, structure, and architectural coherence — exactly the domain where AI excels at generating volume and where humans excel at ensuring accuracy and voice.

### The Cross-Validation Protocol

Four AI agents were given identical input: the complete planning corpus (12 documents, ~50,000 words) plus specific evaluation prompts. Each agent independently produced:

1. A risk assessment (what could go wrong)
2. A priority ranking (what matters most)
3. A scope recommendation (what to include in minimum viable launch)
4. A sequencing proposal (what order to execute)

The responses were then compared across all four agents to identify:
- **Stable consensus** (all 4 agree) — these became canonical decisions
- **Majority positions** (3 of 4 agree) — adopted with noted dissent
- **Split opinions** (2-2 or no majority) — flagged for human resolution
- **Unique insights** (only 1 agent raised) — preserved if valuable, even if not consensus

---

## The Cross-Validation Cycle

### Round 1: Independent Evaluation

Three AI agents — Codex (gpt-5), Gemini (gemini-3-pro-preview), and Copilot (gpt-5) — were given the same planning corpus (12 documents, ~50,000 words) and asked to independently evaluate the system. A fourth agent (Claude Opus 4.6) served as the synthesizing coordinator. The evaluation ran in two waves: Runs A/B (simultaneously to Gemini CLI and GitHub Copilot CLI) and Run C (~5.5 hours later to Codex CLI). This timing gap was itself a finding — the same prompts produced different strategic recommendations across time, while core technical assessments remained stable.

Each agent received three prompts:
1. **Validate the other two agents' analysis** — each agent reviewed the other models' outputs and flagged disagreements
2. **Identify the single highest-priority risk** — forcing prioritization, not just enumeration
3. **Propose a concrete execution plan** — not abstract recommendations but sequenced, budgeted action items

The results filled 6,004+ lines of analysis across three CLI output directories (`gemini-cli/`, `github-copilot-cli/`, `codex-cli/`), producing raw material that would have taken a human reviewer weeks to assemble independently.

### Round 2: Cross-Agent Review

The cross-agent review surfaced four categories of findings, documented exhaustively in `07-cross-ai-logic-check-results.md`:

**Unanimous consensus (all 3 models agree):**
- The registry schema was blocking — missing `dependencies[]` and `promotion_status` fields that the planned GitHub Actions workflows required
- The binary "all-at-once" launch gate was the critical risk — 44 repos at 100% readiness simultaneously was a guarantee of indefinite delay
- Coordination overhead of ~10% for managing parallel AI streams was real and must be budgeted
- The `organvm.env` → `organvm.config.json` architecture was production-grade

**Key disagreements:**
- **Launch order:** Codex recommended automating `validate-dependencies` first; Gemini recommended launching ORGAN-V first to build audience; Copilot recommended writing flagships first regardless of organ
- **Registry as artifact:** Codex saw it as a build output; Gemini as a manual submission file; Copilot as a prerequisite for writing
- **Portfolio lead asset:** Codex championed automation workflows; Gemini championed narrative essays; Copilot championed working code

These disagreements were the most valuable output of the entire cross-validation. They forced explicit decisions (D-01 through D-08 in the canonical action plan) on questions that a single-agent workflow would have resolved implicitly — and potentially incorrectly.

### Round 3: Canonical Action Plan

The cross-validation cycle produced the canonical action plan (`08-canonical-action-plan.md`), which contains:
- **8 D-register decisions** — deferred decisions resolved through cross-validation
- **8 stable consensus items** — points where all agents agreed
- **The Bronze Sprint definition** — minimum viable launch scope determined by cross-validation rather than arbitrary sprint planning

---

## Per-Agent Findings

### Claude (Anthropic) — Synthesis & Constitutional Design

Claude served as the synthesizing agent — not generating independent validation responses, but coordinating the outputs of the other three agents into a coherent canonical plan. This role is itself a finding: the AI-conductor model benefits from separating *generation* (multiple independent agents) from *synthesis* (a single coordinating agent).

Claude's specific contributions:
- **D-register methodology:** The 8 deferred decisions (D-01 through D-08) were structured using a constitutional approach — each decision explicitly states the contradiction, the resolution, and the reasoning. This format emerged from Claude's tendency to formalize disagreements as resolvable propositions rather than unresolved tensions.
- **Specification-driven development (SDD):** The Bronze Sprint specification (`docs/specs/bronze-sprint/spec.md`) follows an SDD pipeline (`specify → plan → tasks → write → validate`) that was designed through Claude's workflow. Each flagship README was written against measurable success criteria, not subjective quality judgments.
- **Criteria-driven completion (D-08):** The decision to abandon fixed sprint timelines in favor of 7 measurable success criteria was a direct output of the synthesis process. Claude identified that both Run A/B and Run C were trying to estimate *time* when what mattered was *state* — the system is done when the criteria are met, regardless of how long that takes.

### Gemini (Google) — Strategic Framing

Gemini provided the most valuable single insight of the entire cross-validation: the **"Simulating Organizational Scale in Solo Practice"** framing that became this essay's central thesis.

Gemini's specific contributions:
- **Organizational simulation thesis:** Gemini was the only agent to explicitly articulate that the eight-organ structure is not organizational cosplay but a genuine methodology for imposing coordination discipline at scale. This reframing transformed the portfolio narrative from "I organized my repos" to "I demonstrated a reproducible protocol for solo practitioners to achieve organizational-quality output."
- **System Design Journal:** Gemini recommended curating the planning documents themselves as a narrative asset — the 50,000-word planning corpus IS the portfolio piece, not just the READMEs it produces.
- **Grant strategy:** Gemini identified the Knight Foundation Art + Tech Expansion Fund as the right first target, noting that the fund explicitly evaluates "long-term digital capacity" and "organizational sustainability" — criteria the eight-organ system was designed to demonstrate.
- **Practitioner comparables:** Gemini replaced aspirational comparisons (Holly Herndon, Casey Reas) with grounded ones: Julian Oliver (artist-engineer with governance focus), Nicky Case (documentation-first transparent process), Hundred Rabbits (small-scale sustainable creative infrastructure). These match the portfolio's current state.

### ChatGPT / Codex (OpenAI) — Technical Validation

Codex (running gpt-5) brought the strongest technical lens, treating the system as an engineering artifact to be stress-tested.

Codex's specific contributions:
- **Registry as machine-validatable artifact:** Codex proposed that the registry should have a JSON Schema that CI can lint on every PR — not just "source of truth" but "machine-checkable source of truth." This became the foundation for the registry hardening work.
- **Minimal repo object schema:** Codex proposed a concrete 15+ field schema (id, full_name, organ, stage, launch_tier, documentation_status, last_validated_at, ci_status, topics, dependencies, promotion_status, promotion_targets, promotion_history, process_doc_ref, essay_refs, analytics_key) that served as the reference for the `repo-registry.json` schema evolution.
- **`validate-dependencies` as priority workflow:** Codex identified dependency validation as the most valuable automation — the single workflow that, if broken, would invalidate the entire unidirectional dependency guarantee (Article II of the constitution).
- **AI validation non-determinism:** The ~5.5 hour gap between Run A/B and Run C produced different strategic recommendations from the same model. Codex surfaced this as a meta-finding: AI validation is non-deterministic for strategic questions while remaining stable for technical assessments. This is itself a publishable insight.

### Copilot (GitHub) — Execution Pragmatism

Copilot brought the most pragmatic perspective, focused on what could actually be shipped rather than what should ideally exist.

Copilot's specific contributions:
- **Tiered template system (SC-8):** Copilot identified that a one-size-fits-all README template would fail. Flagships need 12 sections (3,000+ words), Standards need 8 sections (1,000+ words), Stubs need 4 sections (200+ words). This became the D-07 tier criteria.
- **Archive-vs-populate split for ORGAN-II:** Copilot diagnosed that 7 of ORGAN-II's 16 repos were monorepo duplicates of `metasystem-master` and should be archived, not documented. This saved an estimated ~350K TE of wasted README writing on repos that contained redundant code.
- **Two-pass cross-reference strategy (SC-7):** Copilot recommended writing READMEs with `[TBD:org/repo#section]` placeholders and resolving all cross-references in a dedicated final pass — preventing circular dependency deadlocks where README A needs a link to README B which isn't written yet.
- **Human review fatigue warning:** Copilot identified cognitive fatigue after reviewing 15-20 repos as the most dangerous failure mode — not technical but psychological. The recommendation: batch reviews in 5-repo chunks, prioritize flagships when cognition is fresh, use the 4-step "Stranger Test" (AI validation → human review → time-delayed re-review → AI cross-check).

---

## Synthesis: From Disagreement to Decision

The cross-validation's most powerful output was not any single agent's recommendation. It was the **pattern of disagreement** across agents that forced decisions the human conductor would not otherwise have made.

### The 8 D-Register Decisions

The canonical action plan (`08-canonical-action-plan.md`) distills the cross-validation into 8 explicitly resolved decisions:

| Decision | Question | Resolution |
|----------|----------|------------|
| **D-01** | How to handle budget calibration differences across runs? | Scenario banding — express budgets as ranges, not point estimates |
| **D-02** | Which repos should be flagships? | Defer to exploration — let the work reveal showcase-readiness |
| **D-03** | What's the Bronze Sprint TE budget? | Band: 1.1M–1.6M TE |
| **D-04** | What leads the portfolio narrative? | Meta-system first (for hiring); deployed products first (for grants) |
| **D-05** | Registry and essay before or during flagship writing? | Iterative — both evolve alongside flagships |
| **D-06** | When to extract the framework as a reusable tool? | Phase 2, not Phase 1 |
| **D-07** | How to classify all repos into tiers? | Define criteria now, assign later during exploration |
| **D-08** | Fixed sprint timeline or success criteria? | Criteria-driven — 7 checkboxes define "done," not a calendar date |

Each decision has a documented contradiction (what the agents disagreed about), a resolution (what the human decided), and reasoning (why). This audit trail is itself evidence of the organizational simulation: real organizations produce decision logs. Solo practitioners rarely do.

### What the Agents Couldn't Do

The cross-validation protocol has clear limits. AI agents excelled at:
- Identifying structural risks (missing registry fields, dependency cycles)
- Proposing alternative execution orders
- Stress-testing budget estimates against internal consistency
- Surfacing framing insights (the "Simulating Organizational Scale" thesis)

AI agents failed at:
- Assessing actual repository quality (only exploration revealed the ORGAN-II monorepo duplication)
- Predicting human cognitive constraints (Copilot's fatigue warning was insightful but abstract — the real experience of fatigue shaped the batching decisions)
- Resolving value conflicts (D-04, whether to lead with meta-system or shipped products, required human judgment about audience and context)

This asymmetry is the AI-conductor model's core design: AI generates breadth, humans provide depth. The conductor doesn't write every note — but every note exists because the conductor decided it should.

---

## Simulating Organizational Scale in Solo Practice

This is the essay's central thesis, identified through cross-validation (specifically, a unique insight from Gemini that the other three agents had not articulated):

**A solo practitioner managing 8 GitHub organizations and ~79 repositories is not pretending to be a large organization. They are *simulating organizational scale* — using the eight-organ structure to impose the same coordination discipline, dependency management, and quality accountability that a multi-team organization would require.**

The simulation is not metaphorical. It is structural:
- **Unidirectional dependencies** prevent the same coupling problems that plague real organizations
- **The registry as single source of truth** provides the same canonical state management that an enterprise would need
- **Quality gates** (registry, portfolio, dependency, completeness) enforce the same standards a review board would
- **Cross-validation by 4 AI agents** provides the same diversity of perspective a cross-functional team would bring

The difference is that a solo practitioner can move faster — there are no meeting calendars, no consensus-seeking delays, no organizational politics. The AI-conductor model preserves the *benefits* of organizational scale (rigor, accountability, diverse review) while eliminating the *costs* (coordination overhead, political friction, consensus paralysis).

This framing is not just a portfolio pitch. It is a genuine methodological contribution: a demonstrated protocol for how solo practitioners can achieve organizational-quality output using AI agents as specialized team members.

### The Evidence: Four Flagships as Proof of Concept

Each organ's flagship repository demonstrates a different dimension of the organizational simulation:

**ORGAN-I: RE:GE — Recursive Engine** (`recursive-engine--generative-entity`)
A symbolic operating system for myth, identity, ritual, and recursive systems. 452KB of pure Python, 1,254 tests at 85% coverage, 21 organ handlers implementing a ritual syntax DSL with bridges to Obsidian, Git, and Max/MSP. RE:GE demonstrates *theoretical depth* — the kind of foundational thinking that an R&D division would produce. The vocabulary it establishes (recursive identity, symbolic grounding, organ-handler architecture) propagates downstream to ORGAN-II and ORGAN-IV, exactly as the dependency model predicts.

**ORGAN-II: Omni-Dromenon Engine** (`metasystem-master`)
A canonical monorepo consolidating 12 separate git repositories into a unified real-time performance system. The core engine implements weighted voting, consensus mechanisms, parameter buses, genre presets, and an organ flow manifest — infrastructure for audience-responsive generative art. This demonstrates *artistic implementation* — not art as decoration, but art as engineering discipline. The monorepo consolidation itself mirrors the organizational simulation: bringing disparate creative projects under a single governance model.

**ORGAN-III: Public Record Data Scrapper** (`public-record-data-scrapper`)
A 50-state UCC public records aggregation platform. Live Vercel deployment, tiered B2B subscriptions, 2,055 tests, Terraform AWS infrastructure, 60+ collection agents spanning state Secretary of State offices, 19 server services, 9 database migrations, 5 integrations (Twilio, SendGrid, Plaid, ACH, AWS S3). This demonstrates *commercial viability* — the system produces revenue-generating products, not just portfolio pieces. The 4-tier pricing model (Free/Starter/Professional/Enterprise) evidences product-market thinking.

**ORGAN-IV: Agentic Titan** (`agentic-titan`)
A polymorphic agent swarm architecture with 6 topologies (hierarchical, mesh, broadcast, pipeline, consensus, hybrid), 1,095+ tests across 18 categories (adversarial, chaos, e2e, integration, performance, MCP, Ray), 22 agent archetypes, and model-agnostic routing across OpenAI, Anthropic, and local providers. This demonstrates *orchestration capacity* — the ability to coordinate complex multi-agent systems with production safety guarantees. The Omega Closure quality program (100% test coverage, zero-tolerance failure modes) mirrors the governance rigor the eight-organ system itself demands.

Together, these four flagships span theory → art → commerce → orchestration — the full I→II→III→IV dependency chain. No single repository would demonstrate organizational capacity. The four together, governed by a registry, coordinated by dependency rules, and documented through a public process, constitute evidence that a solo practitioner can produce organizational-scale output.

---

## Lessons Learned

### What Worked

1. **Cross-validation over consensus-seeking.** Asking 4 agents to independently evaluate the same corpus, then comparing their responses, produced better results than asking any single agent to iteratively refine a plan. The disagreements were the most valuable output.

2. **Constitutional constraints.** Defining immutable principles (Articles I-VI) before beginning execution prevented scope creep and provided a tiebreaker for contested decisions.

3. **Deferred decisions.** The D-register (8 deferred decisions) acknowledged uncertainty explicitly rather than forcing premature choices. Decisions were resolved when enough information existed, not when the sprint plan demanded them.

4. **Criteria-driven completion.** The Bronze Sprint is not time-boxed — it is criteria-boxed. Seven measurable success criteria define "done," not a calendar date. This prevents both premature declaration of victory and indefinite scope expansion.

### What Didn't Work (or Required Adjustment)

1. **Pre-selecting flagships from registry data.** The original cross-validation (Run A/B) pre-selected 5 flagship repos based on registry scores. This was overridden by D-02 ("Defer to Exploration") — and correctly so. Exploration revealed that ORGAN-II had 7 monorepo duplicates that would have wasted ~350K TE if documented individually. The `metasystem-master` repo, which became the ORGAN-II flagship, was not in any pre-selection list.

2. **Sequential phase gates.** The initial plan (`implementation-package-v2.md`) specified strict sequential phases: complete all documentation before any validation, complete all validation before any integration. The cross-validation unanimously rejected this. Iterative execution — writing flagships while evolving the registry while accumulating essay material — proved far more productive than the sequential plan suggested.

3. **Uniform README templates.** The planning corpus assumed a single README template for all repos. Copilot correctly identified that flagships (3,000+ words, 12 sections) and stubs (200+ words, 4 sections) need fundamentally different templates. The tiered template system (D-07) was a direct correction.

4. **AI validation non-determinism.** The ~5.5 hour gap between Run A/B and Run C produced materially different strategic recommendations from identical prompts. This means any cross-validation protocol must account for temporal variance — running validation once is insufficient. Multiple runs at different times provide a more robust signal.

5. **Aspirational registry data.** Several registry entries listed repos as "DEPLOYED" or "OPERATIONAL" that turned out to be skeleton code or empty scaffolds on actual inspection. The exploration phase corrected these systematically, but the lesson is clear: registry data that hasn't been validated against reality is not data — it's aspiration.

### What We'd Do Differently

1. **Explore before planning.** The 50,000-word planning corpus was written before any repo exploration occurred. If we started again, we would explore all repos first, *then* write planning documents informed by actual state. The exploration phase corrected many planning assumptions — but only because we built it into the process.

2. **Record model versions from the start.** Run A/B did not record which model versions were used. Run C did (gpt-5, gemini-3-pro-preview). All future validation runs should include full provenance: model version, timestamp, prompt hash, and input corpus hash.

3. **Budget for discovery overhead.** The Bronze Sprint budget included a "discovery contingency" (100K-200K TE) at the insistence of the cross-validation. This turned out to be essential — monorepo discovery in ORGAN-II, visibility corrections across multiple organs, and tier re-assignments all consumed contingency budget. Future sprints should maintain this cushion.

4. **Start with the process essay, not finish with it.** The essay was planned as a post-hoc deliverable. In practice, writing it alongside the flagships created a feedback loop: each flagship provided material, and the essay's narrative requirements shaped how flagships were written. Starting the essay earlier — even as a structural outline — would have accelerated both.

---

## Conclusion: A Protocol, Not a Product

This essay has documented a specific protocol: how a solo practitioner used four AI agents as a cross-validation ensemble to build, launch, and document an eight-organ creative-institutional system coordinating 79 repositories across 8 GitHub organizations.

The protocol is reproducible. The inputs are: a planning corpus, a set of evaluation prompts, multiple AI agents with different architectural biases, and a human conductor who resolves disagreements by making explicit, documented decisions. The outputs are: a set of canonical decisions, a tiered classification of all system components, and a collection of flagship documentation that no single agent could have produced alone.

What makes this a methodological contribution rather than a project report is the claim at its center: **AI agents can serve as an organizational simulation.** The four agents provided the diversity of perspective, the constructive disagreement, and the systematic review that an organization would. The human conductor provided the judgment, the voice, and the final authority that no AI can. Neither alone would have produced this system. Together, they demonstrated that the boundary between "solo practitioner" and "organization" is a question of methodology, not headcount.

The eight-organ system itself is evidence. The registry with 79 entries, each validated against reality. The dependency graph with no back-edges. The four flagship READMEs, each scoring above 90/100 on a measurable rubric. The constitution with immutable articles and post-cross-validation amendments. These are not the artifacts of a solo coder organizing their repos. They are the artifacts of an organizational simulation running at speed — with AI agents providing the scale and a human providing the direction.

The system is live. The process is public. The methodology is documented. What comes next is execution: Silver Sprint (15 Standard READMEs), Gold Sprint (full system validation), and the framework extraction that turns this specific implementation into a reusable protocol for anyone who wants to simulate organizational scale in solo practice.

---

## Cross-References

### Source Documents

| Document | Role in This Essay |
|----------|-------------------|
| [08-canonical-action-plan.md](https://github.com/organvm-v-logos/public-process) | The canonical output of the cross-validation cycle |
| [07-cross-ai-logic-check-results.md](https://github.com/organvm-v-logos/public-process) | Raw cross-validation results from all 4 agents |
| [repo-registry.json](https://github.com/organvm-v-logos/public-process) | Machine-readable source of truth for all 79 repos |

### Flagship READMEs (Evidence Base)

| Organ | Flagship | What It Demonstrates |
|-------|----------|---------------------|
| I | [RE:GE - Recursive Engine](https://github.com/organvm-i-theoria/recursive-engine--generative-entity) | Theoretical depth: 21-organ symbolic operating system with 1,254 tests |
| II | [Omni-Dromenon Engine](https://github.com/organvm-ii-poiesis/metasystem-master) | Artistic implementation: canonical monorepo consolidating 12 separate projects |
| III | [Public Record Data Scrapper](https://github.com/organvm-iii-ergon/public-record-data-scrapper) | Commercial viability: live deployment, B2B subscriptions, 2,055 tests |
| IV | [Agentic Titan](https://github.com/organvm-iv-taxis/agentic-titan) | Orchestration capacity: 6 topologies, 1,095+ tests, model-agnostic |

### System Links

- [meta-organvm](https://github.com/meta-organvm) — Umbrella organization
- [organvm-v-logos](https://github.com/organvm-v-logos) — This organ's home

---

**Organization:** [organvm-v-logos](https://github.com/organvm-v-logos)
**System:** [organvm eight-organ system](https://github.com/meta-organvm)
**Author:** [@4444J99](https://github.com/4444J99)

*Status: Draft complete. All TBD markers resolved from flagship material.*
*Last updated: 2026-02-10*
