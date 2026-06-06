# 11: Specification-Driven Development (Skills Framework)

**Date:** 2026-02-10
**Status:** ACTIVE — defines the specification workflow for all Bronze Sprint and subsequent deliverables
**Derived from:** `speckit` skill (Specification-Driven Development toolkit)
**Complements:** `01-readme-audit-framework.md` (scoring rubric), `03-per-organ-readme-templates.md` (organ-specific templates), `08-canonical-action-plan.md` (canonical decisions and Bronze scope), `10-repository-standards.md` (repository standards)

---

## 1. Purpose & Scope

This document adapts **Specification-Driven Development (SDD)** from a code-generation methodology into the organvm documentation and governance context. The `speckit` skill was designed for software projects where specifications drive code. In this corpus, specifications drive **documentation, governance artifacts, and launch deliverables**.

The adaptation is structural, not cosmetic. Where speckit assumes the output is functions, APIs, and data models, organvm assumes the output is READMEs, registry updates, essays, and community health files. The workflow mechanics — specify, plan, execute against quality gates — transfer directly.

**Relationship to existing documents:**

| Document | Covers | This Document Adds |
|----------|--------|-------------------|
| `01` Audit Framework | README scoring rubric (0-100) | Specification workflow that precedes scoring |
| `03` README Templates | Organ-specific section structure | Feature-level specs that determine which template to apply |
| `08` Canonical Action Plan | Bronze Sprint scope and success criteria | Formal specification format for each Bronze deliverable |
| `10` Repository Standards | Root hygiene, badges, community health | Specification gates that validate standards compliance |
| [`docs/memory/constitution.md`](../memory/constitution.md) | Immutable project principles | Constitutional constraint checking during planning |

**When to reference this document:** When planning any new deliverable (README, essay, registry update, workflow). The specification should exist before the work begins. When evaluating completed work, use `01` (scoring) and `04` (checklists) instead.

---

## 2. The Documentation Power Inversion

### Traditional Documentation Workflow

In most projects, documentation follows implementation:

```
Code exists -> Someone writes a README -> README describes code -> README drifts from reality
```

The README is scaffolding around code. When code changes, the README lags. Documentation is always catching up.

### The organvm Inversion

In this corpus, the specification is truth; documentation is the generated output:

```
Specification exists -> README is generated to satisfy spec -> Registry is updated to match -> Quality gates validate compliance
```

This is the same "power inversion" that speckit applies to code, redirected at documentation deliverables. The specification defines what a README must contain, what registry fields must be populated, what cross-references must resolve — and the writing work implements those requirements.

### Why This Works for Documentation

The AI-conductor model (`CLAUDE.md` §AI-Conductor Workflow Model) means specifications are particularly powerful:

1. **AI generates volume.** A well-specified README requirement ("3,000+ words, 12 sections, working examples, score >=90 on `01` rubric") gives AI enough constraint to produce a quality first draft.
2. **Human reviews against spec.** The reviewer checks whether the spec is satisfied, not whether the README "looks good." This reduces subjective review fatigue (finding B7/SC-6 in `08`).
3. **Quality is measurable.** Every requirement in the spec is testable. "All cross-references resolved" is binary. "Score >=90" is numeric. There is no ambiguity about whether a deliverable is done.

### Concept Mapping

| speckit Concept | organvm Adaptation |
|-----------------|-------------------|
| Feature | Deliverable (README, essay, registry update, workflow) |
| User story | Stakeholder scenario (grant reviewer reads README, hiring manager checks portfolio) |
| Functional requirement | Documentation requirement (word count, sections, cross-references, registry fields) |
| API contract | Cross-reference contract (which repos link to which, dependency direction) |
| Data model | Registry schema (fields, types, validation rules) |
| Test | Quality gate (Registry, Portfolio, Dependency, Completeness) |
| Code generation | AI-assisted README/essay drafting |
| Deployment | Publication to GitHub (public visibility, org-level pinning) |

---

## 3. The Three Commands (Adapted)

The speckit skill defines three commands that form a pipeline: specify -> plan -> tasks. In the organvm context, these become documentation-specific workflows.

### `/speckit.specify` -> Define the Deliverable

**Original purpose:** Create a feature specification from a natural language description.

**Adapted purpose:** Create a deliverable specification from the planning corpus. The input is not a feature description but a planning document reference (e.g., "08 §3 Bronze Sprint, deliverable 1: Flagship READMEs").

**Output:**
- `docs/specs/{deliverable-name}/spec.md` — deliverable specification with stakeholder scenarios, documentation requirements, and success criteria
- `docs/specs/{deliverable-name}/checklists/requirements.md` — quality validation checklist

**Process (adapted):**
1. Identify the deliverable from the planning corpus (`08`, `02`, registry)
2. Determine the tier (Flagship/Standard/Stub/Archive per D-07)
3. Generate stakeholder scenarios with prioritized stories (P1 = grant reviewer, P2 = hiring manager, P3 = community contributor)
4. Define documentation requirements (FR-001, FR-002, etc.) mapped to `01` rubric dimensions and `10` standards
5. Create measurable success criteria from D-08 checkboxes
6. Validate against [`docs/memory/constitution.md`](../memory/constitution.md) quality gates
7. Flag ambiguities (max 3 `[NEEDS CLARIFICATION]` markers)

**Key adaptation:** speckit says "avoid HOW (no tech stack, APIs, code structure)." For organvm, the equivalent is: "avoid specific prose (no draft text, no README content). Specify what the README must achieve, not what it must say."

### `/speckit.plan` -> Design the Approach

**Original purpose:** Create an implementation plan with technology decisions.

**Adapted purpose:** Create a documentation plan with template selection, cross-reference mapping, and registry update strategy.

**Output:**
- `docs/specs/{deliverable-name}/plan.md` — documentation plan with template selection and writing strategy
- `docs/specs/{deliverable-name}/research.md` — repo exploration findings (actual code state, current README state, portfolio potential)

**Process (adapted):**
1. Load deliverable specification and project constitution
2. Determine template from `03` (organ-specific) and tier from D-07
3. Run constitution check (evaluate quality gates)
4. Research phase: explore the actual repo (code state, existing docs, dependencies)
5. Map cross-references: which other repos will this README link to? Do those READMEs exist yet?
6. Plan registry updates: what fields will change in `repo-registry.json`?
7. Re-evaluate constitution compliance post-design

**Constitution Gates (adapted for documentation):**
- **Registry Gate:** Does the plan include registry updates? Are new fields justified?
- **Portfolio Gate:** Does the writing strategy target the "Stranger Test"?
- **Dependency Gate:** Do planned cross-references respect I->II->III flow?
- **Completeness Gate:** Will all TBD markers be resolvable given current corpus state?

### `/speckit.tasks` -> Generate the Work Items

**Original purpose:** Generate an executable task list from the implementation plan.

**Adapted purpose:** Generate a documentation task list organized by stakeholder story, with dependency ordering and parallelization markers.

**Output:**
- `docs/specs/{deliverable-name}/tasks.md` — dependency-ordered task list

**Task format:** `[ID] [P?] [Story] Description`
- `[P]` = Can run in parallel (different repos, no cross-reference dependencies)
- `[Story]` = Which stakeholder scenario (SS1, SS2, SS3)

**Phase structure (adapted):**
1. **Setup:** Template selection, registry schema check, cross-reference inventory
2. **Foundation:** Repo exploration, current-state assessment, tier assignment
3. **Stakeholder Stories:** README writing in priority order (P1 flagship first, then P2, P3)
4. **Polish:** Cross-reference resolution, link validation, registry finalization

---

## 4. Project Constitution

The project constitution lives at [`docs/memory/constitution.md`](../memory/constitution.md) and defines immutable architectural principles. When any `/speckit.plan` equivalent is run, the constitution is loaded and validated against.

### Articles (from CLAUDE.md Key Invariants)

| Article | Principle | Gate Implication |
|---------|-----------|-----------------|
| I | Registry as Single Source of Truth | Every deliverable that changes repo state must update `repo-registry.json` |
| II | Unidirectional Dependencies | Cross-references must flow I->II->III; no back-edges |
| III | All Eight Organs at Launch | Bronze Sprint must produce at least one flagship per organ I-V |
| IV | Documentation Precedes Deployment | Specification must exist before writing begins |
| V | Portfolio-Quality Documentation | Every README passes the "Stranger Test" |
| VI | Promotion State Machine | Repo status changes follow LOCAL->CANDIDATE->PUBLIC_PROCESS->GRADUATED->ARCHIVED |

### Amendments (from post-cross-validation consensus)

| Amendment | Addition | Gate Implication |
|-----------|----------|-----------------|
| A | Bronze Tier Launch Path | Scope to flagships + registry + essay; criteria-driven completion |
| B | Coordination Overhead Budget | 10% TE allocation for cross-deliverable reconciliation |
| C | Registry Schema Completeness | `dependencies[]`, `promotion_status`, `tier`, `last_validated` required |
| D | AI Non-Determinism | Budget estimates use scenario banding; human review mandatory |

### When the Constitution Applies

The constitution applies to **planning and specification**, not to individual writing decisions. A README author choosing between two phrasings does not need to check the constitution. A planner deciding which repos to write READMEs for does.

Specifically, the constitution is checked:
- When creating a new specification (`/speckit.specify`)
- When creating a documentation plan (`/speckit.plan`)
- When declaring a deliverable complete (all four quality gates)
- When proposing changes to the planning corpus itself

---

## 5. Specification Workflow

### When to Use SDD vs. Existing Templates

The planning toolkit (`01`-`05`, `08`, `10`) and SDD serve different purposes:

| Situation | Use |
|-----------|-----|
| Writing a single README for a known repo | `03` template directly (SDD is overhead for a single well-defined deliverable) |
| Scoring an existing README | `01` rubric |
| Validating a completed README | `04` checklist |
| Planning a multi-deliverable sprint (e.g., Bronze) | SDD specification first, then templates for individual READMEs |
| Planning a new essay or process document | SDD specification (essays don't have templates in `03`) |
| Hardening the registry schema | SDD specification (registry work is cross-cutting, not per-repo) |
| Resolving cross-references across multiple repos | SDD specification (cross-cutting coordination task) |

### Integration with Existing Planning Toolkit

```
08-canonical-action-plan (scope + success criteria)
  |
  v
11-specification-driven-development (this document: methodology)
  |
  v
docs/specs/{deliverable}/spec.md (deliverable specification)
  |
  v
docs/specs/{deliverable}/plan.md (documentation plan)
  |                           |
  v                           v
03 templates (README writing)  repo-registry.json (state updates)
  |                           |
  v                           v
04 checklists (validation)    01 rubric (scoring)
  |
  v
10 standards (compliance)
```

The specification sits between the canonical plan (`08`) and the execution tools (`01`-`05`, `10`). It translates strategic decisions into testable requirements for individual deliverables.

### The Two-Pass Writing Pattern

SDD reinforces the two-pass approach established in SC-7 (`08` §2):

**Pass 1 (Draft):** Write READMEs with `[TBD:org/repo#section]` placeholders for unresolvable cross-references. The specification tracks which placeholders exist and what they need.

**Pass 2 (Resolution):** After all flagship drafts exist, resolve all TBD markers in a dedicated cross-reference pass. The specification's Completeness Gate enforces zero remaining placeholders.

---

## 6. Tier-Aware Specifications

Not every repo needs the same specification depth. The tier system from D-07 (`08` §1) determines how much specification work precedes the writing work.

### Specification Depth by Tier

| Tier | Spec Depth | Spec Contents | Writing Process |
|------|-----------|---------------|-----------------|
| **Flagship** | Full specification | All 4 spec sections (scenarios, requirements, success criteria, entities) + constitution check + cross-reference map | Full SDD pipeline: specify -> plan -> tasks -> write -> validate |
| **Standard** | Light specification | Requirements + success criteria only (no full scenarios) | Abbreviated: requirements -> template -> write -> validate |
| **Stub** | No specification | Direct from `03` template (4 sections: purpose, status, links, author) | Template -> write -> quick check |
| **Archive** | No specification | Archive notice + redirect | One-step write |

### Flagship Specification Requirements

A Flagship spec must include:

1. **Stakeholder scenarios (3 minimum):**
   - P1: Grant reviewer evaluating portfolio (what convinces them?)
   - P2: Hiring manager assessing technical depth (what demonstrates capability?)
   - P3: Community contributor deciding to engage (what's the on-ramp?)

2. **Documentation requirements (mapped to `01` rubric):**
   - Existence & Accessibility (0-20): title, ToC, formatting, navigation
   - Content Completeness (0-40): problem statement, installation, examples, dependencies, contributing
   - Accuracy & Currency (0-20): valid links, working code, current docs
   - Portfolio Relevance (0-20): why exists, system connection, value prop, evidence

3. **Success criteria (mapped to D-08):**
   - Score >=90/100 on `01` rubric
   - 0 broken links
   - All cross-references resolved
   - Registry data matches reality

4. **Cross-reference map:**
   - Which repos does this README link to?
   - Which repos link back to this one?
   - Are all targets available (or do TBD placeholders need to be tracked)?

### Standard Specification Requirements

A Standard spec needs only:

1. Documentation requirements (abbreviated: word count, required sections, badge minimums)
2. Success criteria (score >=70/100 on `01` rubric, 0 broken links)

---

## 7. Precedence & Integration

This document is **Layer 1 (Phase 1 Planning)** in the document architecture, numbered `11` to continue the `01`-`10` sequence.

### Precedence Rules

- For README *scoring*, defer to `01-readme-audit-framework.md`
- For README *content structure*, defer to `03-per-organ-readme-templates.md`
- For README *validation*, defer to `04-per-organ-validation-checklists.md`
- For tier *classification criteria*, defer to `08-canonical-action-plan.md` D-07
- For repo *root hygiene, badges, community health*, defer to `10-repository-standards.md`
- For *specification methodology, quality gates, constitution, and spec workflow*, **this document is authoritative**
- For *immutable project principles*, defer to [`docs/memory/constitution.md`](../memory/constitution.md)

### Document Interactions

| This Document Section | Interacts With | How |
|----------------------|----------------|-----|
| §2 Power Inversion | `CLAUDE.md` AI-Conductor Model | Extends the AI-conductor pattern to specification-first workflow |
| §3 Three Commands | `speckit` skill SKILL.md | Adapts the three commands for documentation context |
| §4 Constitution | [`docs/memory/constitution.md`](../memory/constitution.md) | References the constitution; constitution is the source of truth |
| §5 Workflow | `01`-`05`, `08`, `10` | Defines where SDD fits in the existing planning toolkit |
| §6 Tier-Aware Specs | `08` D-07 | Maps tier criteria to specification depth |
| §7 Precedence | All planning docs | Establishes non-overlapping authority boundaries |

### What This Document Does NOT Cover

- **Specific Bronze Sprint deliverables.** Those live in [`docs/specs/bronze-sprint/spec.md`](../specs/bronze-sprint/spec.md).
- **The canonical action plan.** That's `08-canonical-action-plan.md`.
- **Repository-level standards.** That's `10-repository-standards.md`.
- **Essay content strategy.** That's [`public-process-map-v2.md`](../implementation/public-process-map-v2.md).
- **Execution timeline.** That's [`roadmap-there-and-back-again.md`](../strategy/roadmap-there-and-back-again.md).

This document defines the *methodology* for specifying deliverables. The deliverables themselves live in `docs/specs/`.
