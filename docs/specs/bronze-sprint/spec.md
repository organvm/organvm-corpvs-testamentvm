# Feature Specification: Bronze Sprint (Minimum Viable Launch)

**Created:** 2026-02-10
**Status:** Complete (2026-02-10)
**Closure:** All 34 validation items passed. 7 flagship READMEs deployed to GitHub. Registry updated. See [`checklists/requirements.md`](checklists/requirements.md) for full validation results.
**Source:** `08-canonical-action-plan.md` §3 (Bronze Sprint Definition)
**Constitution:** [`docs/memory/constitution.md`](../../memory/constitution.md) (all articles and amendments apply)
**TE Budget Band:** 1.1M-1.6M TE

## User Scenarios & Testing

### User Story 1 - Flagship READMEs (Priority: P1)

A grant reviewer visits the organvm GitHub organizations for the first time. They navigate to one flagship repo per organ and read the README. Within 30 seconds, they understand what the project does and why it matters. Within 5 minutes, they can assess whether this work merits funding consideration.

**Why this priority:** The flagship READMEs are the primary portfolio artifact. Without them, the eight-organ system is invisible to external audiences. Everything else (registry, essay, cross-references) supports these READMEs.

**Independent Test:** Can be validated by applying the `01` rubric to each flagship README. Each must score >=90/100 independently of whether other deliverables are complete.

**Acceptance Scenarios:**

1. **Given** a visitor lands on an ORGAN-I flagship repo, **When** they read the README hero section, **Then** they understand the theoretical contribution and its relationship to the eight-organ system within 30 seconds.
2. **Given** a visitor lands on an ORGAN-III flagship repo, **When** they read through the README, **Then** they find working installation instructions, usage examples, and business context (metrics, users, value proposition).
3. **Given** at least one flagship per organ I-V exists and VI-VII have stubs, **When** a reviewer navigates across all 8 orgs, **Then** they encounter a consistent README structure (hero section, badges, cross-references) that communicates a unified system.
4. **Given** a flagship README references another organ's repo, **When** the reviewer follows the cross-reference link, **Then** it resolves to a real, accessible page (no 404s, no TBD placeholders).

**Deliverable:** At least one fully documented flagship README per organ (I-V mandatory, VI-VII at minimum stubs). Specific repos determined by exploration, not pre-selected (per D-02).

**TE Budget:** 535K-750K TE (5-7 flagships x ~107K TE avg)

---

### User Story 2 - Registry Schema Hardening (Priority: P2)

An AI agent (or GitHub Actions workflow) reads `repo-registry.json` to determine the state of a repo. It finds all required fields populated with verified data, enabling automated dependency validation and audit reporting.

**Why this priority:** The registry is the machine-readable backbone. Without the 4 new fields (`dependencies[]`, `promotion_status`, `tier`, `last_validated`), Phase 2 automation is blocked. Schema hardening during Bronze prevents a retrofit later.

**Independent Test:** Can be validated by running `python3 -m json.tool repo-registry.json` (schema validity) and checking that all flagship repos have the 4 new fields populated with non-placeholder values.

**Acceptance Scenarios:**

1. **Given** `repo-registry.json` is loaded, **When** an agent queries a flagship repo entry, **Then** it finds `dependencies[]`, `promotion_status`, `tier`, and `last_validated` fields with verified values.
2. **Given** the registry schema includes `dependencies[]`, **When** an agent traverses dependencies for an ORGAN-III repo, **Then** no dependency path leads back to ORGAN-III (no back-edges, per Article II).
3. **Given** all flagship READMEs are drafted, **When** the registry is compared to repo reality, **Then** `documentation_status` and `tier` fields match actual state (no aspirational "100%" or "OPERATIONAL" for incomplete repos).

**Deliverable:** `repo-registry.json` gains 4 new fields. Data populated iteratively as flagships are written, locked after majority of flagships are drafted (per D-05).

**TE Budget:** 70K-88K TE

---

### User Story 3 - Process Essay (Priority: P3)

A hiring manager at an AI lab reads "How I Used 4 AI Agents to Cross-Validate an Eight-Organ System." They understand the methodology, see concrete examples from the cross-validation cycle, and recognize the meta-system narrative as evidence of systems thinking at organizational scale.

**Why this priority:** The process essay is the highest-value portfolio artifact per SC-5 (unanimous across all 6 validation responses). It transforms the planning corpus from internal documentation into a public-facing demonstration of the AI-conductor model. However, it requires material from completed flagships, making it dependent on P1 progress.

**Independent Test:** Can be validated by word count (4,000-5,000 words), structural completeness (introduction, methodology, per-agent findings, cross-validation synthesis, lessons learned), and the "Stranger Test" (would a stranger at an AI lab find this compelling?).

**Acceptance Scenarios:**

1. **Given** the essay is draft-complete, **When** a reader with no prior context reads it, **Then** they understand the eight-organ model, the cross-validation methodology, and the AI-conductor workflow without referencing other documents.
2. **Given** the essay references specific flagship READMEs as examples, **When** the reader follows those links, **Then** the READMEs exist and demonstrate the quality described in the essay.
3. **Given** the essay describes the "Simulating Organizational Scale in Solo Practice" framing (per Gemini insight in `08` §7), **When** a reader assesses the claim, **Then** the 7 org structure and ~44 repos provide concrete evidence for the framing.

**Deliverable:** "How I Used 4 AI Agents to Cross-Validate an Eight-Organ System" (~4,000-5,000 words). Written iteratively as flagships provide material (per D-05).

**TE Budget:** 100K-120K TE

---

### User Story 4 - Cross-Reference Resolution (Priority: P4)

A technical reviewer clicks every link in every flagship README. Every link resolves. Every cross-organ reference points to a real, accessible page. No TBD markers remain in any shipped document.

**Why this priority:** Cross-reference integrity is the minimum quality bar for a portfolio that claims to be a coordinated system. A single broken link undermines the "orchestrated eight-organ architecture" narrative. This deliverable depends on P1 (all flagships must exist before cross-references can be fully resolved).

**Independent Test:** Can be validated by automated link checking (404 scan) and grep for `[TBD` markers across all flagship READMEs.

**Acceptance Scenarios:**

1. **Given** all flagship READMEs are drafted, **When** a link checker scans all flagship documents, **Then** 0 broken links are found.
2. **Given** the two-pass approach (SC-7) was used, **When** all `[TBD:org/repo#section]` placeholders from Pass 1 are audited, **Then** every placeholder has been resolved in Pass 2.
3. **Given** cross-references between organs, **When** the direction of each reference is checked, **Then** all references follow the I->II->III dependency flow (no back-edges, per Article II).

**Deliverable:** All inter-repo links validated. No TBD markers in shipped READMEs. Cross-references follow dependency direction.

**TE Budget:** 80K-100K TE

---

### Edge Cases

- What happens if a flagship candidate turns out to be a hollow shell during exploration? Reassign flagship status to the next-best repo in that organ (per D-02 exploration-first approach).
- What happens if an ORGAN-VI or ORGAN-VII repo has no code at all? Write a stub README (4 sections, 200+ words per D-07 Stub tier) that clearly communicates the organ's purpose and future plans.
- What happens if cross-references create a circular dependency between two organs? This violates Article II. Resolve by restructuring the reference to point to ORGAN-IV (orchestration) as the coordination hub.
- What happens if the process essay lacks sufficient material after 3 flagships? Continue writing flagships; the essay grows with each completed flagship (per D-05 iterative sequencing).

## Requirements

### Functional Requirements

- **FR-001:** System MUST produce at least one fully documented flagship README per organ I-V, with stubs for VI-VII
- **FR-002:** Each flagship README MUST score >=90/100 on the `01-readme-audit-framework.md` rubric
- **FR-003:** Each flagship README MUST follow the progressive disclosure pattern from `10-repository-standards.md` §3
- **FR-004:** Each flagship README MUST include organ-specific sections from `03-per-organ-readme-templates.md`
- **FR-005:** `repo-registry.json` MUST include `dependencies[]`, `promotion_status`, `tier`, and `last_validated` fields for all flagship repos
- **FR-006:** Registry data MUST match repo reality (no aspirational values)
- **FR-007:** Process essay MUST be 4,000-5,000 words covering cross-validation methodology
- **FR-008:** All cross-references between flagships MUST resolve (0 broken links)
- **FR-009:** No `[TBD` markers MUST remain in any shipped flagship README
- **FR-010:** All flagship READMEs MUST display organ membership badge per `10` §6

### Key Entities

- **Flagship README:** A fully documented (3,000+ words, 12 sections) README for a portfolio-critical repo. The primary output of the Bronze Sprint.
- **Registry Entry:** A JSON object in `repo-registry.json` representing one repo's canonical state. Source of truth per Article I.
- **Process Essay:** A 4,000-5,000 word public-facing essay documenting the AI-conductor methodology. Published to ORGAN-V.
- **Cross-Reference:** A link from one README to another repo's README or section. Must follow dependency direction per Article II.

## Success Criteria

Mapped directly from `08-canonical-action-plan.md` D-08. All must be true for Bronze to be declared complete.

### Measurable Outcomes

- **SC-001:** At least one fully documented flagship per organ (I-V mandatory, VI-VII at least stubs)
- **SC-002:** `repo-registry.json` schema includes `dependencies[]`, `promotion_status`, `tier`, `last_validated`
- **SC-003:** All flagship READMEs score >=90/100 on the `01` rubric
- **SC-004:** All cross-references between flagships are resolved (no TBD markers)
- **SC-005:** Process essay ("How I Used 4 AI Agents...") is draft-complete
- **SC-006:** 0 broken links across all flagship READMEs
- **SC-007:** Registry data matches reality for all flagships (no aspirational `100%` or `OPERATIONAL`)
