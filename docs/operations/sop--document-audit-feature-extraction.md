# SOP: Document Audit & Feature Extraction v2.0

**Created:** 2026-03-04 (v1), **Revised:** 2026-03-06 (v2.0)
**Author:** @4444j99 (AI-conductor model: human directs, AI generates, human reviews)
**Status:** ACTIVE — Living document, updated as process evolves
**Companions:** [`key-workflows.md`](./key-workflows.md) (procedures), [`operational-cadence.md`](./operational-cadence.md) (rhythm), [`minimum-viable-operations.md`](./minimum-viable-operations.md) (maintenance)
**Constitution:** [`docs/memory/constitution.md`](../memory/constitution.md) — Articles I-VI govern all specifications
**Supersedes:** v1.0 (archived at `archive/2026-03/sop--document-audit-feature-extraction-v1.md`)

---

> *Every project accumulates documentation that contains product ideas nobody has tracked. This SOP turns that latent value into actionable GitHub issues, systematically and repeatably.*

---

## Table of Contents

1. [Purpose & Scope](#1-purpose--scope)
2. [Prerequisites](#2-prerequisites)
3. [Phase 0 — Scope & Classify](#3-phase-0--scope--classify)
4. [Phase 1 — Inventory & Triage](#4-phase-1--inventory--triage)
5. [Phase 2 — Exhaustive Read & Extraction](#5-phase-2--exhaustive-read--extraction)
6. [Phase 3 — Completeness Proof](#6-phase-3--completeness-proof)
7. [Phase 4 — Deduplication & Tension Resolution](#7-phase-4--deduplication--tension-resolution)
8. [Phase 5 — Synthesis](#8-phase-5--synthesis)
9. [Phase 6 — Issue Creation](#9-phase-6--issue-creation)
10. [Phase 7 — Post-Audit Artifacts](#10-phase-7--post-audit-artifacts)
11. [Light Mode (Corpora <= 10 Documents)](#11-light-mode-corpora--10-documents)
12. [Appendices](#12-appendices)

---

## 1. Purpose & Scope

### What this SOP does

This procedure takes a documentation corpus — a single repo's `docs/` directory, a flat collection of AI chat transcripts, a multi-repo research archive, or any other structured set of documents — and produces a complete set of GitHub issues. One for every product idea, feature concept, architectural suggestion, or behavioral insight buried in the documentation. The audit is **exhaustive**: every document is read word-for-word, not skimmed or summarized.

v2.0 adds a **mandatory completeness proof** (Phase 3) to verify that the reading pass captured at least 80% of extractable content, **antagonistic tension detection** to surface places where documents disagree, and a **synthesis phase** to identify strategic themes that no single issue captures.

### When to run it

| Trigger | Description |
|---------|-------------|
| **New repo onboarding** | When a repo first enters the system with existing documentation |
| **Major doc additions** | When a bulk import of research, brainstorm transcripts, or external references lands in a repo |
| **Quarterly review** | Part of the Week 4 monthly review cycle (see [`operational-cadence.md`](./operational-cadence.md), Part II, Week 4) |
| **Pre-beta audit** | Before a product enters private or public beta, to ensure nothing in the docs was forgotten |
| **Post-mortem** | After a failed launch or missed deadline, to capture lessons from planning docs |

### What it applies to

Any corpus in any organ containing documentation with untracked product or feature ideas. This includes:
- Standard `docs/` directories (research, brainstorm, legal, architecture, planning)
- `specs/` directories (RFCs, ADRs, technical specifications)
- `design/` directories (design documents, wireframes with annotations)
- Root-level markdown files (README, CONTRIBUTING, ARCHITECTURE)
- External reference libraries (books, papers, articles in `docs/research/reference-library/`)
- **AI chat transcripts** (Perplexity, ChatGPT, Claude — conversation logs with research output)
- **Flat file collections** (no subdirectory structure — requires thematic cohort reading order)
- **Multi-repo corpora** (documents whose issues route to different repositories)

The procedure is organ-agnostic. It works identically for ORGAN-I theory repos, ORGAN-II creative repos, ORGAN-III products, ORGAN-IV orchestration, and ORGAN-V editorial repos. Adapt the issue labels, routing, and terminology to the organ's domain.

### Version history

| Version | Date | Empirical basis | Key changes |
|---------|------|-----------------|-------------|
| v1.0 | 2026-03-04 | Styx/ORGAN-III: 52 authored docs, 74 issues, single repo | 5-phase architecture |
| v2.0 | 2026-03-06 | + ORGAN-IV: 16 AI transcripts, 73 issues across 150 repos | 8-phase architecture, completeness proof, tension detection, synthesis, multi-repo routing, coverage thresholds |

---

## 2. Prerequisites

### Required artifacts

| Artifact | Required? | Purpose |
|----------|-----------|---------|
| `FEATURE-BACKLOG.md` (or equivalent) | Recommended | Deduplication target — avoids creating issues for already-tracked features. If it doesn't exist, the audit will create one as an output artifact. |
| `MANIFEST.md` (or equivalent) | Recommended | Document index with stable IDs. If it doesn't exist, Phase 1 builds one. |
| `seed.yaml` | Required | Confirms organ membership, tier, and promotion status. Determines label taxonomy. |
| Project `CLAUDE.md` | Required | Provides project context, architecture, conventions. Read before starting. |

### Required tools

| Tool | Purpose | Install |
|------|---------|---------|
| `gh` CLI | GitHub issue creation, label management, issue listing | `brew install gh` + `gh auth login` |
| Claude Code (or manual) | Exhaustive document reading and extraction | Already available in this context |
| `pandoc` | Format conversion (epub -> plain text, docx -> markdown) | `brew install pandoc` |
| Calibre (optional) | AZW3/MOBI -> EPUB conversion (Amazon DRM-free only) | `brew install --cask calibre` |

### Required access

- GitHub repo write access (push to default branch)
- GitHub issue creation permissions **on all target repos** (critical for multi-repo audits)
- Read access to all files in the documentation corpus

### Pre-audit checklist

Before starting the audit, complete these steps in order:

- [ ] Read the project's `CLAUDE.md` (root level and `docs/CLAUDE.md` if it exists)
- [ ] Read `seed.yaml` — note organ, tier, promotion status
- [ ] Inventory all open GitHub issues on **every target repo**: `gh issue list --repo <org>/<repo> --state open --limit 500`
- [ ] Read `FEATURE-BACKLOG.md` if it exists — note all `F-*` IDs and their statuses
- [ ] Read `MANIFEST.md` if it exists — note all `DOC-*` IDs
- [ ] Confirm label taxonomy exists on each target repo (create labels if needed — see [Phase 6](#9-phase-6--issue-creation))
- [ ] Verify issues are enabled on all target repos (see [Appendix G](#appendix-g-multi-repo-routing-guide) for disabled-issues handling)

---

## 3. Phase 0 — Scope & Classify

**Goal:** Determine WHAT the corpus is before reading it. Misclassification cascades into under-extraction — a chat transcript read with authored-doc heuristics will miss 30-50% of its content.

**Time estimate:** ~15 minutes

### Step 1: Declare scope

| Dimension | Options |
|-----------|---------|
| **Repo topology** | `single-repo` / `multi-repo` / `cross-organ` |
| **Trigger** | `onboarding` / `quarterly` / `pre-beta` / `post-mortem` / `bulk-import` |
| **Corpus location** | Path(s) to documentation root(s) |

### Step 2: Classify document types

For each document in the corpus, assign a type. Each type selects a different extraction heuristic set (see [Appendix F](#appendix-f-document-type-heuristics)):

| Type | Description | Heuristic set |
|------|-------------|---------------|
| `authored` | Original prose written by humans (research, brainstorm, planning) | v1 heuristics ("We could...", "Future work", "Risk: ...") |
| `transcript` | AI chat transcripts (Perplexity, ChatGPT, Claude) | Numbered lists, named tools, "strategic gap", statistical claims, roadmaps |
| `reference` | External books, papers, articles | Chapter summaries, framework applications, case studies |
| `rfc-adr` | RFCs, ADRs, technical specifications | "Consequences", rejected alternatives, open questions |
| `code-wiki` | Code comments, wiki pages, README roadmap sections | TODO/FIXME, deprecated patterns, roadmap sections |

### Step 3: Build routing table (multi-repo only)

If the audit will create issues across multiple repos, define the routing table upfront:

```markdown
| Category | Target Repo | Labels |
|----------|-------------|--------|
| governance | orchestration-start-here | governance, research-derived |
| agent-architecture | agent--claude-smith | agent-architecture, research-derived |
| safety-protocol | petasum-super-petasum | safety-protocol, research-derived |
| orchestration | agentic-titan | orchestration, research-derived |
```

**Disabled-issues handling:** If any target repo has issues disabled, document the redirect repo and apply a `routed-from:<original-repo>` label. See [Appendix G](#appendix-g-multi-repo-routing-guide).

### Step 4: Plan agent allocation

Agent count scales by corpus size AND document density:

| Corpus size | Recommended agents | Notes |
|-------------|-------------------|-------|
| 1-5 docs | 1 agent | Single pass, no parallelization needed |
| 5-15 docs | 1-2 agents | Split by cohort if thematically distinct |
| 15-40 docs | 2-3 agents | Thematic cohort split |
| 40-100 docs | 3-5 agents | Folder-based or cohort-based split |
| 100+ docs | 5 max | Sequential cohort batches; do not exceed 5 concurrent on 16GB RAM |

**Density adjustment:** If >30% of documents are flagged high-density in Phase 1, add one agent.

### Phase 0 output

A scope declaration document containing: repo topology, trigger, document type classifications, routing table (if multi-repo), and agent allocation plan.

---

## 4. Phase 1 — Inventory & Triage

**Goal:** Build a complete map of every document in the corpus before reading anything. Determine the reading order.

**Time estimate:** ~15-30 minutes

### Step 1: List all documentation files

```bash
cd <repo-root>
find docs/ -type f | sort
```

Or with Claude Code:
```
Glob: docs/**/*
```

### Step 2: Classify by format

Create a working inventory. For each file, record:

| Field | Description |
|-------|-------------|
| **Path** | Relative path from repo root |
| **Format** | `markdown`, `pdf`, `epub`, `azw3`, `txt`, `docx`, `pptx`, `binary`, `asset` |
| **Readable?** | Yes / Needs conversion / Unreadable |
| **Category** | `research`, `brainstorm`, `legal`, `architecture`, `planning`, `pitch`, `reference`, `governance`, `transcript`, `asset` |
| **Size** | Approximate word count or line count |
| **Document type** | From Phase 0 classification: `authored`, `transcript`, `reference`, `rfc-adr`, `code-wiki` |
| **Density flag** | `normal` or `high-density` (>15 extractable items per 100 lines — see estimation guidance below) |
| **Source cluster** | Cluster ID if document shares a prompt, topic, or generation session with other docs |

### Step 3: Determine reading order

**Decision tree:**

1. **If the corpus has meaningful subdirectories** (brainstorm/, research/, legal/, etc.): use folder-based order (v1 default)
   - Brainstorm -> Research -> Legal -> Architecture -> Planning -> Reference library
2. **If the corpus is flat or mixed** (all files in one directory, or no thematic folder structure): use thematic cohort order
   - Group documents into 3-5 cohorts by topic/theme
   - Read each cohort as a unit to preserve thematic context
   - Within each cohort, read chronologically or by complexity (simple -> complex)

### Step 4: Identify source clusters

Documents that share the same prompt, topic, or generation session should be grouped as a **source cluster**. Within a cluster, expect 30-50% content overlap. Mark clusters for aggressive deduplication in Phase 4.

Examples of clusters:
- Three ChatGPT conversations on the same topic from different dates
- A Perplexity deep-research output and a Claude summary of the same question
- Multiple drafts of the same document

### Step 5: Estimate density

Quick density estimation per document:

```
density = (estimated extractable items) / (line count / 100)
```

If density > 15 items per 100 lines: flag as `high-density`. These documents get a within-Phase-2 second read.

### Step 6: Convert unreadable formats

For each file that needs conversion:

```bash
# EPUB -> plain text
pandoc -f epub -t plain "docs/research/reference-library/author--title.epub" \
  -o "/tmp/author--title.txt"

# DOCX -> markdown
pandoc -f docx -t markdown "docs/planning/roadmap.docx" \
  -o "/tmp/roadmap.md"

# PDF -> plain text (pandoc, best-effort)
pandoc -f pdf -t plain "docs/pitch/deck.pdf" \
  -o "/tmp/deck.txt"

# AZW3 -> EPUB -> plain text (requires Calibre)
ebook-convert "docs/research/reference-library/author--title.azw3" \
  "/tmp/author--title.epub"
pandoc -f epub -t plain "/tmp/author--title.epub" \
  -o "/tmp/author--title.txt"
```

**Note conversion failures.** Some formats (DRM-protected files, scanned PDFs without OCR, proprietary binary formats) cannot be converted. Record these as gaps in the audit summary.

### Step 7: Build the document manifest

If no `MANIFEST.md` exists, create one:

```markdown
# Project Manifest: Annotated Document Index

**Version**: 1.0.0
**Project**: <project-name>
**Document Count**: <N> entries
**Generated**: <YYYY-MM-DD>

---

## Cohort 1: <Cohort Name>

| ID | File | Type | Density | Cluster | Tags | Annotation |
|----|------|------|---------|---------|------|------------|
| DOC-RES-01 | `docs/research/topic-name.md` | authored | normal | — | #research | Brief description |
| DOC-CND-01 | `research/transcript-01.md` | transcript | high | C1 | #conductor | Brief description |
```

Assign stable `DOC-*` IDs using the pattern `DOC-{CATEGORY}-{NN}`:
- `DOC-RES-*` — Research
- `DOC-BRN-*` — Brainstorm
- `DOC-LEG-*` — Legal
- `DOC-ARC-*` — Architecture
- `DOC-PLN-*` — Planning
- `DOC-PIT-*` — Pitch
- `DOC-REF-*` — Reference library (external sources)
- `DOC-GOV-*` — Governance
- `DOC-CND-*` — AI chat transcripts (conductor sessions)
- `DOC-SAF-*` — Safety / compliance
- `DOC-TLG-*` — Tooling

### Phase 1 output

A complete `MANIFEST.md` showing every file with its DOC-ID, format, readability status, category, document type, density flag, cohort assignment, and source cluster ID. This is the roadmap for Phase 2.

---

## 5. Phase 2 — Exhaustive Read & Extraction

**Goal:** Read every document word-for-word and extract every actionable idea.

**Time estimate:** ~1-3 hours (scales with corpus size and density)

### The cardinal rule

**Read every word.** Do not skim. Do not summarize from headings. Do not skip sections that "look like boilerplate." The most valuable feature ideas are often buried in parenthetical remarks, footnotes, section transitions, or "future work" paragraphs that a skimmer would miss.

### Reading order

Use the order determined in Phase 1:

- **Folder-based** (if meaningful subdirs): Brainstorm -> Research -> Legal -> Architecture -> Planning -> Reference library
- **Thematic cohort** (if flat/mixed): Process each cohort as a unit, maintaining thematic context

### Extraction format

For each idea extracted, record:

```markdown
### [EXT-NNN] Extraction Title

- **Source**: `docs/research/filename.md`, Section "Section Name" (or page N for books)
- **Quote/Paraphrase**: Verbatim quote or close paraphrase of the relevant passage
- **Idea**: What product feature, behavioral mechanism, or architectural change this implies
- **Category**: `core-mechanics` | `ux` | `compliance` | `behavioral-science` | `infrastructure` | `business-model` | `security` | `social` | `mobile` | `b2b` | `governance` | `orchestration` | `safety-protocol` | `tooling` | etc.
- **Target repo**: (multi-repo only) Which repo this issue belongs in
```

### Extraction heuristics

Select the heuristic set matching each document's type from Phase 0. The full tables are in [Appendix F](#appendix-f-document-type-heuristics). Summary:

**Authored docs** (v1 heuristics):

| Signal | Example | Likely extraction |
|--------|---------|-------------------|
| "We could..." / "We should..." / "Consider..." | "We could add a spectator mode" | Feature idea |
| "The research shows..." / "Studies indicate..." | "Loss aversion coefficient is 1.955" | Behavioral constant or algorithm parameter |
| "Legal requirement" / "Must comply with..." | "Must verify age 18+ before staking" | Compliance feature |
| "Not yet implemented" / "Future work" / "Phase 2+" | "Phase 2: PvP lobbies" | Backlog item |
| Architectural diagrams with unbuilt components | "Oracle Network (planned)" | Infrastructure feature |
| Competitor analysis gaps | "Competitor X doesn't offer Y" | Differentiator feature |
| User journey steps without code | "User receives push notification" | Missing implementation |
| "Risk: ..." / "Mitigation: ..." | "Risk: users fabricate proofs" | Security feature |

**AI chat transcripts** (v2 additions):

| Signal | Example | Likely extraction |
|--------|---------|-------------------|
| Numbered lists with actionable items | "1. Deploy ollama, 2. Configure routing" | Implementation steps -> feature |
| Named tools or services | "Use CodeRabbit for automated review" | Tooling integration |
| "Strategic gap" / "missing" / "blind spot" | "No sensitivity-based routing exists" | Infrastructure gap |
| Statistical claims with citations | "METR finds 48% of AI code has issues" | Risk metric or threshold |
| Roadmap or phase structure | "Phase 1: local, Phase 2: hybrid" | Backlog sequencing |
| Consensus across multiple AI responses | 3/3 engines recommend the same approach | High-confidence feature |
| "Should" / "must" / "critical" language | "Must implement human-in-the-loop" | Safety requirement |

### Density-aware reading

Documents flagged `high-density` in Phase 1 get a **within-Phase-2 second read**. After the initial read, re-read the document looking specifically for items missed on the first pass. This is not the completeness proof (Phase 3) — it's a targeted second pass for documents known to be dense.

### Coverage self-estimate

After reading each document, the reading agent must estimate coverage:

```
DOC-RES-01: ~25 extractable items found, estimated ~30 total → ~83% coverage
DOC-CND-03: ~8 extractable items found, estimated ~20 total → ~40% coverage ← RE-READ
```

**If self-estimated coverage < 70%: immediately re-read within Phase 2.** Do not wait for Phase 3.

### Parallelization (Claude Code)

For large corpora, parallelize reads using Claude Code agents per the Phase 0 allocation plan:

```
Agent 1 (Cohort 1 — Process Discipline):
  "Read every file in this cohort word-for-word. Use the AI chat transcript
   heuristics from the SOP. For each product idea, feature concept, or
   architectural suggestion, extract it with: source file, section, verbatim
   quote, categorized idea, and target repo. Output as a numbered list.
   After reading each document, estimate coverage (items found / estimated total)."

Agent 2 (Cohort 2 — Safety & Data Sovereignty):
  [same instructions, different cohort]
```

**Constraint:** On 16GB RAM systems, limit to 5 concurrent agents. Each agent produces its own extraction list; merge in Phase 4.

### Phase 2 output

A consolidated extraction list organized by cohort or folder. Each extraction has a unique `EXT-NNN` ID, source citation, verbatim quote, categorized idea, target repo (if multi-repo), and per-document coverage estimates.

---

## 6. Phase 3 — Completeness Proof

**Goal:** Verify that Phase 2 captured the corpus's extractable content above threshold. This is the single most important v2 addition — without it, expect ~30% of content to be missed.

**Time estimate:** ~1-2 hours

**This phase is a mandatory gate. The audit cannot proceed to Phase 4 until the gate criteria are met.**

### Why this phase exists

The ORGAN-IV execution (16 AI chat transcripts) demonstrated that a single reading pass — even a careful one — achieves only ~70% coverage. The completeness proof caught:
- 74 obvious gaps (items the first reader should have caught)
- 110 non-obvious gaps (cross-document inferences)
- 8 antagonistic tensions (where documents disagree) — 0 caught in first pass
- 5 under-extracted documents (below 60% coverage)

### Step 1: Assign fresh agents

The completeness proof **must** be performed by agents who did NOT read the documents in Phase 2. Fresh eyes catch different things. If Phase 2 used agents 1-3, assign agents 4-5 (or new agents) for Phase 3.

For Light Mode (<=10 docs): the same agent can perform the completeness proof if it explicitly re-reads with an adversarial "what did I miss?" framing.

### Step 2: Line-by-line re-read

Fresh agents re-read every document line-by-line, producing a coverage table:

```markdown
| DOC-ID | Document | Total Items | Covered | Coverage % | Gap Count |
|--------|----------|-------------|---------|------------|-----------|
| DOC-CND-01 | conductor-session-01.md | 42 | 35 | 83% | 7 |
| DOC-CND-02 | conductor-session-02.md | 38 | 30 | 79% | 8 |
| DOC-SAF-04 | safety-protocols.md | 55 | 28 | 51% | 27 |
```

### Step 3: Classify gaps

Each gap gets one of these codes (from [Appendix H](#appendix-h-completeness-proof-methodology)):

| Code | Meaning | Action |
|------|---------|--------|
| **S** (Surface) | Obvious item the Phase 2 reader should have caught | Create new extraction |
| **R** (Refinement) | Existing extraction needs additional detail | Amend existing EXT-NNN |
| **P** (Pattern) | Cross-document pattern not visible from single doc | Create synthesis theme (Phase 5) |
| **A** (Antagonist) | Contradicts or tensions with another extraction | Add to tension register |
| **L** (Low-value) | Extractable but too granular for a standalone issue | Note in audit summary, skip |
| **N** (Non-obvious) | Requires domain expertise or cross-reference to spot | Document for future review |

### Step 4: Detect antagonistic tensions

Systematically identify where documents **disagree**. For each tension:

```markdown
### Tension T-NN: <Title>

- **Pole A**: [Document X] says "..."
- **Pole B**: [Document Y] says "..."
- **Classification**: COMPLEMENTARY / CONTEXT-DEPENDENT / TEMPORAL / DATA-QUALITY-ISSUE / NUANCED / UNRESOLVED
- **Resolution**: (deferred to Phase 4)
```

Tension classifications:
| Type | Meaning |
|------|---------|
| **COMPLEMENTARY** | Both poles are correct in different dimensions |
| **CONTEXT-DEPENDENT** | Each pole is correct in its specific context |
| **TEMPORAL** | One pole supersedes the other chronologically |
| **DATA-QUALITY-ISSUE** | One pole cites unreliable or misinterpreted data |
| **NUANCED** | The truth lies between the poles |
| **UNRESOLVED** | Genuine disagreement requiring human decision |

### Step 5: Gate check

**GATE CRITERIA — all three must pass:**

1. **Overall coverage >= 80%** (total items covered / total items identified)
2. **No document below 50% coverage** without a documented justification (e.g., "DOC-REF-03 is a 400-page textbook; 45% coverage is acceptable because the remaining content is not product-relevant")
3. **All antagonistic tensions identified and classified**

**If the gate fails:**
1. Return to Phase 2 for targeted re-extraction of under-covered documents
2. Re-run Phase 3 coverage check on the remediated documents only (not the full corpus)
3. Repeat until gate passes

### Phase 3 output

1. **Completeness proof document**: coverage table, gap register with codes, methodology notes
2. **Antagonistic tension register**: all tensions with Pole A, Pole B, classification
3. **Remediation extractions**: new EXT-NNN entries from gaps classified as S (Surface) or R (Refinement)
4. **Gate pass/fail declaration** with numbers

---

## 7. Phase 4 — Deduplication & Tension Resolution

**Goal:** Eliminate duplicates, resolve tensions, and classify each extraction for action.

**Time estimate:** ~1-2 hours

### Input

This phase operates on the **full extraction set**: Phase 2 originals + Phase 3 remediation extractions.

### Cross-reference targets

Every extraction must be checked against three sources:

#### 1. Feature backlog (`FEATURE-BACKLOG.md`)

If the project has an existing feature backlog with `F-*` IDs:
- Search for each extraction's keywords in the backlog
- If an `F-*` entry covers the same idea: **SKIP** (already tracked)
- If an `F-*` entry partially covers it: **ENHANCE** (note the `F-*` ID for cross-reference in the issue)

#### 2. Open GitHub issues

```bash
# List all open issues with titles (on each target repo)
gh issue list --repo <org>/<repo> --state open --limit 500 --json number,title

# Search for a specific keyword
gh issue list --repo <org>/<repo> --search "keyword" --state open
```

- If an open issue covers the same idea: **SKIP**
- If an open issue partially overlaps: **ENHANCE** (reference the issue number)

#### 3. Codebase (implemented but untracked)

```bash
# Search for feature keywords in source code
grep -r "keyword" src/ --include="*.ts" --include="*.tsx" -l
```

Or with Claude Code:
```
Grep: pattern="keyword" path="src/"
```

- If the feature is already implemented with tests: **SKIP** (optionally create a documentation issue)
- If partially implemented: **ENHANCE** (note the existing code paths)

### Source-cluster deduplication

Documents in the same source cluster (identified in Phase 1) get **aggressive merge**. Expect 30-50% overlap within clusters. When two extractions from the same cluster describe the same idea:
1. Merge into a single candidate
2. Keep the most detailed version as primary
3. Note all source documents

### Cross-document merge

Multiple documents often describe the same idea from different angles. When two or more extractions from different documents (not the same cluster) describe the same feature:
1. Merge them into a single candidate
2. List all source documents in the merged entry
3. Choose the most specific/detailed description as the primary
4. Retain unique details from each source as supplementary requirements

### Tension resolution

For each antagonistic tension from Phase 3:

1. **Determine resolution type** (using the classifications from Phase 3)
2. **Write a resolution statement** explaining how both poles relate
3. **Decide on issue action**:
   - COMPLEMENTARY: Create one issue that incorporates both perspectives
   - CONTEXT-DEPENDENT: Create one issue noting when each approach applies
   - TEMPORAL: Use the most recent position; note historical context
   - DATA-QUALITY-ISSUE: Use the well-sourced position; note the data quality concern
   - NUANCED: Create one issue with the synthesized position
   - UNRESOLVED: Create one issue flagged for human decision, presenting both poles

### Classification output

Each extraction gets one of four labels:

| Label | Action | Reason |
|-------|--------|--------|
| **SKIP** | Do nothing | Already tracked in backlog, open issue, or implemented code |
| **ENHANCE** | Update existing issue or backlog entry | Partially tracked — new details from this extraction add value |
| **CREATE** | New GitHub issue | Genuinely new idea not tracked anywhere |
| **TENSION** | New GitHub issue with both poles | Antagonistic tension requiring explicit resolution in the issue body |

### Phase 4 output

A deduplicated candidate list where each entry is classified as SKIP, ENHANCE, CREATE, or TENSION, with cross-references to existing tracking (issue numbers, `F-*` IDs, code paths), routing assignments (if multi-repo), and resolved tension register.

---

## 8. Phase 5 — Synthesis

**Goal:** Identify emergent strategic themes that no single issue captures. This phase produced the most strategically valuable output in both execution runs.

**Time estimate:** ~30-60 minutes

### Step 1: Identify cross-cutting themes

A cross-cutting theme spans **3+ documents or 2+ repos**. It represents a convergent pattern — multiple independent sources pointing in the same direction.

For each theme, document:

```markdown
### Theme N: <Theme Name>

**Sources**: DOC-CND-01, DOC-CND-05, DOC-SAF-02, DOC-TLG-03
**Repos touched**: orchestration-start-here, agentic-titan

**Convergence**: What pattern emerges when these documents are read together?

**Strategic implication**: What does this mean for the project/organ/system?

**Recommended action**: What should be built, changed, or investigated?
```

### Step 2: Map theme dependencies

```markdown
| Theme | Requires | Enables | Conflicts |
|-------|----------|---------|-----------|
| Local-first inference | Hardware budget | Sensitivity routing | Cloud-first scaling |
| Process-as-product | Session protocol | Writing Vault | Rapid iteration |
```

### Step 3: Integrate tensions as a theme

If Phase 3 found antagonistic tensions, compile them into a named theme:

```markdown
### Theme N: Antagonistic Tensions

The corpus contains N competing positions that cannot be mechanically resolved.
These represent genuine design decisions requiring human judgment.

| Tension | Pole A | Pole B | Resolution |
|---------|--------|--------|------------|
| T-01: ... | ... | ... | COMPLEMENTARY: ... |
```

### Step 4: Compile statistical/risk data appendix (if applicable)

If the corpus contains statistical claims, research findings, or risk data:

```markdown
### Appendix A: Risk Data

| Finding | Source | Statistic | Implication |
|---------|--------|-----------|-------------|
| AI code quality | METR study | 48% of AI code has issues | Mandatory review gates |
```

### Step 5: Produce recommended execution order

Based on theme dependencies, suggest an implementation sequence:

```markdown
## Recommended Execution Order

1. **Foundation**: Theme A (no dependencies, enables B and C)
2. **Infrastructure**: Theme B (requires A, enables D)
3. **Application**: Theme C (requires A), Theme D (requires B)
4. **Optimization**: Theme E (requires C and D)
```

### Phase 5 output

A synthesis document containing:
1. Named cross-cutting themes with source citations
2. Theme dependency map
3. Antagonistic tensions as a named theme
4. Statistical/risk data appendix (if applicable)
5. Recommended execution order

---

## 9. Phase 6 — Issue Creation

**Goal:** Create one GitHub issue per CREATE/TENSION candidate, update existing issues for ENHANCE candidates.

**Time estimate:** ~1-3 hours (scales with issue count)

### Label taxonomy

Before creating issues, ensure each target repo has these labels (create any that are missing):

```bash
# Core labels (every repo)
gh label create "enhancement" --description "New feature or request" --color "a2eeef" --repo <org>/<repo>
gh label create "documentation" --description "Documentation improvements" --color "0075ca" --repo <org>/<repo>
gh label create "research-derived" --description "Issue created from document audit" --color "c5def5" --repo <org>/<repo>

# Domain labels (adapt to project — examples)
gh label create "behavioral-science" --description "Behavioral economics and psychology" --color "d4c5f9" --repo <org>/<repo>
gh label create "compliance" --description "Legal and regulatory requirements" --color "e4e669" --repo <org>/<repo>
gh label create "ux" --description "User experience and interface" --color "7057ff" --repo <org>/<repo>
gh label create "infrastructure" --description "Backend, DevOps, architecture" --color "f9d0c4" --repo <org>/<repo>
gh label create "security" --description "Security features and hardening" --color "b60205" --repo <org>/<repo>
gh label create "governance" --description "Governance and process" --color "006b75" --repo <org>/<repo>
gh label create "safety-protocol" --description "Safety guardrails and protocols" --color "d93f0b" --repo <org>/<repo>
```

### Issue title format

```
feat: {descriptive title in lowercase}
```

Examples:
- `feat: add spectator mode for public contract viewing`
- `feat: implement sensitivity-based routing for confidential content`
- `feat: integrate CodeRabbit for automated code review`

### Issue body template

Every issue must use this structured template:

````markdown
## Source

- **Document(s)**: `docs/research/filename.md` (Section "X"), `docs/brainstorm/filename.md`
- **Author(s)**: Original document author(s) if known
- **Extraction ID(s)**: EXT-042, EXT-067 (merged)
- **Audit**: Document Audit v2.0, <YYYY-MM-DD>

## Problem

What gap, opportunity, or user need does this address? 2-3 sentences max.

## Proposed Feature

1. **Requirement 1**: Description
2. **Requirement 2**: Description
3. **Requirement 3**: Description

### Design sketch (if applicable)

Brief architectural notes, API shape, or UI behavior.

## Tensions (if applicable)

If this issue involves or resolves an antagonistic tension:

- **Pole A**: [Source] — Position
- **Pole B**: [Source] — Position
- **Resolution**: Classification + explanation

## Cross-References

- **Backlog**: F-CATEGORY-NN (if partially tracked)
- **Related issues**: #42, #67 (if related but not duplicate)
- **Code paths**: `src/api/services/module/file.ts` (if partially implemented)
- **Synthesis theme**: Theme N — <name> (if part of a cross-cutting theme)
- **External**: Link to research paper, competitor, or standard (if applicable)

## Labels

`enhancement`, `research-derived`, `domain-label`
````

### Issue creation rate

**Create issues sequentially with >= 2 second delay between API calls.** The GitHub API returns 502 errors under rapid-fire issue creation. This was learned from the ORGAN-IV execution where batch creation caused failures.

```bash
# Pattern for sequential creation with delay
gh issue create --repo <org>/<repo> --title "feat: ..." --body "..." --label "enhancement" --label "research-derived"
sleep 2
gh issue create --repo <org>/<repo> --title "feat: ..." --body "..." --label "enhancement" --label "research-derived"
```

### Batch creation strategy

Create issues in **thematic groups**, not in document order. This produces coherent issue clusters:

1. Group all CREATE/TENSION candidates by category
2. Within each group, sort by priority (P0 before P1, P1 before P2)
3. Create all issues in one group before moving to the next
4. Between groups, update the running tally

### Running tally

Maintain a running count during creation. For multi-repo audits, track by **target repo** (not by folder):

```
Repo: orchestration-start-here  — 28 issues created (#82-#109)
Repo: agentic-titan             — 17 issues created (#8-#24)
Repo: petasum-super-petasum     — 13 issues created (#119-#131)
Repo: agent--claude-smith       — 3 issues created (#14-#16)
─────────────────────────────────────────────────────────
Total: 59 issues created across 150 repos
```

For single-repo audits, track by category or folder:

```
Category: behavioral-science  — 15 issues created (#46-#60)
Category: ux                  — 12 issues created (#61-#72)
Category: compliance          — 8 issues created (#73-#80)
─────────────────────────────────────────────────────────
Total: 35 issues created
```

### ENHANCE workflow

For ENHANCE candidates (existing issues that need supplementary detail):

```bash
gh issue comment <issue-number> \
  --repo <org>/<repo> \
  --body "$(cat <<'EOF'
## Additional Context from Document Audit

**Source**: `docs/research/filename.md`, Section "X"
**Audit**: Document Audit v2.0, <YYYY-MM-DD>
**Completeness proof provenance**: This addition was identified during the Phase 3 completeness proof as a gap in the original extraction.

**New detail**: Description of what this extraction adds to the existing issue.
EOF
)"
```

### Phase 6 output

All CREATE/TENSION candidates have been filed as GitHub issues. All ENHANCE candidates have been commented on existing issues. The running tally is complete.

---

## 10. Phase 7 — Post-Audit Artifacts

**Goal:** Update project metadata, leave a clean audit trail, and file SOP improvement recommendations.

**Time estimate:** ~30-60 minutes

### Step 1: Update FEATURE-BACKLOG.md

If the project uses a feature backlog with `F-*` IDs:

1. Add new `F-*` entries for each created issue
2. Set status to `NOT_STARTED`
3. Add source citations (backreferencing doc filenames)
4. Update the executive summary counts
5. Update the source-to-feature reverse mapping table (if one exists)

If the project does not have a feature backlog, create one. At minimum, include:
- Feature ID (`F-{CATEGORY}-{NN}`)
- Title
- Status (`IMPLEMENTED`, `PARTIAL`, `STUB`, `NOT_STARTED`)
- Priority (`P0`, `P1`, `P2`, `P3`)
- Source document(s)
- GitHub issue number
- Target repo (if multi-repo)

### Step 2: Update MANIFEST.md

If new documents were discovered or created during the audit:

1. Assign `DOC-*` IDs to any new files
2. Add entries to the appropriate category/cohort table
3. Update the document count in the header
4. Update the version number

### Step 3: Create SYLLABUS.md

Select the variant based on the corpus content (see [Appendix I](#appendix-i-syllabus-variants)):

| Variant | When to use | Focus |
|---------|-------------|-------|
| **Academic** | Reference library contains books, papers, articles | Author — Title — Key takeaway |
| **Tooling** | Corpus references tools, services, frameworks | Tool — Purpose — Integration status |
| **Mixed** | Both academic and tooling references | Separate sections for each |
| **None** | No external references in corpus | Skip this step |

Place in `docs/research/reference-library/SYLLABUS.md`, `research/SYLLABUS.md`, or equivalent.

### Step 4: Commit synthesis and completeness proof

Ensure these Phase 3 and Phase 5 artifacts are committed:

- Synthesis document (from Phase 5)
- Completeness proof (from Phase 3)

### Step 5: Write the audit summary with retrospective

Create a summary file documenting what was done:

```markdown
# Document Audit Summary

**Date**: YYYY-MM-DD
**Repo**: <org>/<repo> (or "multi-repo: repo1, repo2, repo3")
**Auditor**: @username (with Claude Code)
**SOP version**: v2.0

## Scope
- Corpus location: <path>
- Document types: authored (N), transcript (N), reference (N), rfc-adr (N), code-wiki (N)
- Documents read: N (of M total files)
- Formats converted: epub (N), pdf (N), azw3 (N)
- Conversion failures: <list any>
- Source clusters: N clusters identified
- Agent allocation: N agents used

## Completeness Proof
- Overall coverage: N% (gate threshold: 80%)
- Documents below 50%: N (with justifications)
- Antagonistic tensions found: N
- Remediation extractions: N

## Results
- Raw extractions: N
- After deduplication: N candidates
  - SKIP (already tracked): N
  - ENHANCE (updated existing): N
  - CREATE (new issues): N
  - TENSION (tension issues): N

## Issues Created
- Total: N across M repos
- By repo:
  - repo1: N issues (#first-#last)
  - repo2: N issues (#first-#last)
- By category:
  - category1: N
  - category2: N

## Synthesis
- Cross-cutting themes identified: N
- Key themes: <list>

## Gaps
- Unreadable files: <list>
- Documents with no actionable extractions: <list>
- Areas needing further research: <list>

## Artifacts Updated
- [ ] FEATURE-BACKLOG.md — N new entries added
- [ ] MANIFEST.md — N new documents indexed
- [ ] SYLLABUS.md — created/updated (variant: academic/tooling/mixed)
- [ ] Synthesis document — N themes
- [ ] Completeness proof — N% coverage
- [ ] This summary committed

## Retrospective

### What worked well
- <observation>

### What didn't work
- <observation>

### Timing accuracy
- Phase 0: estimated Xm, actual Ym
- Phase 1: estimated Xm, actual Ym
- ...

### SOP amendment recommendations
- <recommendation with rationale>
```

Place this summary alongside the audit artifacts (e.g., `research/audit-summary--YYYY-MM-DD.md` or `docs/planning/audit-summary--YYYY-MM-DD.md`).

### Step 6: File SOP amendments

If the retrospective identifies improvements to this SOP:

1. Create a file `docs/operations/sop-amendments/<YYYY-MM-DD>-<slug>.md` in the corpus testamentvm repo
2. Describe the amendment: what to change, why, and evidence
3. The SOP maintainer reviews and incorporates in the next revision

### Step 7: Commit and push

```bash
git add docs/FEATURE-BACKLOG.md docs/MANIFEST.md docs/research/reference-library/SYLLABUS.md
git add docs/planning/audit-summary--YYYY-MM-DD.md  # if created
git add research/synthesis--*.md research/audit-completeness-proof--*.md  # if separate location
git commit -m "docs: complete document audit — N issues created across M repos

SOP v2.0 execution. N documents audited, N% coverage (completeness proof).
N cross-cutting themes, N antagonistic tensions resolved."
git push origin <branch>
```

---

## 11. Light Mode (Corpora <= 10 Documents)

For small corpora, phases collapse to reduce ceremony while maintaining the same deliverables:

### Collapsed structure

| Full mode | Light mode | Change |
|-----------|------------|--------|
| Phase 0 + Phase 1 | **Combined inventory** (~10 min) | Single step: scope, classify, and inventory together |
| Phase 2 + Phase 3 | **Read with built-in proof** (~1-2 hrs) | Same agent re-reads adversarially with explicit "what did I miss?" pass. No separate agent needed. Coverage self-check still required. |
| Phase 4 + Phase 5 | **Dedup & synthesize** (~30-60 min) | Deduplication and theme identification in one pass |
| Phase 6 | **Create issues** (unchanged) | Issue creation is mechanical — no shortcuts |
| Phase 7 | **Artifacts** (unchanged) | Artifacts are structural — no shortcuts |

### Light mode gate criteria

The same thresholds apply:
- Overall coverage >= 80%
- No document below 50% without justification
- All tensions identified

The difference is that a single agent can satisfy these by doing an explicit second pass, rather than requiring fresh agents.

### When NOT to use light mode

- Corpus has > 10 documents (even if some are short)
- Documents are high-density (> 15 items per 100 lines average)
- Multi-repo routing is needed (the routing table justifies a full Phase 0)
- Previous audit of similar corpus found significant completeness gaps

---

## 12. Appendices

### Appendix A: Format Conversion Reference

| Source Format | Target | Command | Notes |
|---------------|--------|---------|-------|
| EPUB | Plain text | `pandoc -f epub -t plain input.epub -o output.txt` | Best for prose books. Preserves chapter structure. |
| EPUB | Markdown | `pandoc -f epub -t markdown input.epub -o output.md` | Preserves formatting, headers, emphasis. |
| PDF | Plain text | `pandoc -f pdf -t plain input.pdf -o output.txt` | Works for text-based PDFs. Fails on scanned/image PDFs. |
| PDF (scanned) | Plain text | `tesseract input.pdf output -l eng pdf` | Requires `brew install tesseract`. Quality varies. |
| DOCX | Markdown | `pandoc -f docx -t markdown input.docx -o output.md` | Excellent conversion quality. |
| AZW3 | EPUB | `ebook-convert input.azw3 output.epub` | Requires Calibre. DRM-free only. |
| PPTX | Markdown | `pandoc -f pptx -t markdown input.pptx -o output.md` | Extracts text from slides; loses layout. |
| HTML | Markdown | `pandoc -f html -t markdown input.html -o output.md` | Good for saved web pages. |

**When conversion fails:**
1. Note the file in the audit summary under "Gaps"
2. Record what format it is and why conversion failed (DRM, scanned image, corrupted)
3. If the content is important, consider manual transcription or OCR alternatives
4. Do not skip the file silently — every gap must be documented

### Appendix B: Issue Body Template (Copy-Paste)

````markdown
## Source

- **Document(s)**: `docs/category/filename.md` (Section "X")
- **Author(s)**:
- **Extraction ID(s)**: EXT-NNN
- **Audit**: Document Audit v2.0, <YYYY-MM-DD>

## Problem

[What gap or opportunity this addresses]

## Proposed Feature

1. **Requirement**: [Description]
2. **Requirement**: [Description]

## Tensions

*(Remove this section if no tensions apply)*

- **Pole A**: [Source] — Position
- **Pole B**: [Source] — Position
- **Resolution**: [Type] — Explanation

## Cross-References

- **Backlog**: F-CATEGORY-NN
- **Related issues**: #N
- **Code paths**: `src/path/to/file.ts`
- **Synthesis theme**: Theme N — <name>
````

### Appendix C: Claude Code Agent Guide

For corpora with 15+ documents, use parallel Claude Code agents to read documents simultaneously.

**Agent allocation by corpus characteristics:**

| Corpus | Documents | Density | Recommended |
|--------|-----------|---------|-------------|
| Small, low-density | 5-15 | Normal | 1-2 agents |
| Small, high-density | 5-15 | High (>30% flagged) | 2-3 agents |
| Medium | 15-40 | Any | 2-3 agents (thematic cohort split) |
| Large, folder-based | 40-100 | Any | 3-5 agents (folder split) |
| Large, flat | 40-100 | Any | 3-5 agents (cohort split) |
| Very large | 100+ | Any | 5 agents max, sequential cohort batches |

**Agent prompt template:**

```
"Read every file in [cohort/folder] word-for-word. Use the [authored/transcript/reference/rfc-adr]
 extraction heuristics from the SOP. For each product idea, feature concept, or architectural
 suggestion, extract it with:
 - Source file and section
 - Verbatim quote or close paraphrase
 - Categorized idea
 - Target repo (if multi-repo)
 Output as a numbered extraction list (EXT-NNN format).
 After reading each document, estimate your coverage:
 'DOC-XX-NN: ~N items found, estimated ~M total, ~X% coverage'"
```

**Constraints:**
- Maximum 5 concurrent agents on 16GB RAM systems
- Each agent should output a structured extraction list, not prose
- Merge agent outputs in Phase 4 (deduplication) — expect 10-30% overlap between agents reading related docs
- Source-cluster documents should be assigned to the SAME agent (reduces cross-agent dedup burden)
- If an agent's output is truncated, split its assignment across two agents

### Appendix D: Adapting for Non-`docs/` Repos

Not all repos organize documentation under `docs/`. Here's how to apply this SOP to alternative structures:

| Structure | Where to look | Adaptation |
|-----------|---------------|------------|
| **RFC directory** (`rfcs/` or `rfc/`) | Each RFC is a self-contained proposal. Treat each RFC as a brainstorm document. | Extract unimplemented proposals, rejected alternatives worth revisiting, and open questions. Use `rfc-adr` heuristics. |
| **ADR directory** (`adr/` or `docs/adr/`) | Architecture Decision Records. | Focus on "Consequences" and "Alternatives Considered" sections — rejected alternatives often contain feature ideas. Use `rfc-adr` heuristics. |
| **Design docs** (`design/` or `docs/design/`) | Detailed feature specifications. | Cross-reference each design against codebase to find unimplemented sections. Use `authored` heuristics. |
| **Wiki** (GitHub Wiki) | Clone locally: `git clone <repo>.wiki.git` | Treat wiki pages as brainstorm documents. Wikis often contain undocumented feature discussions. Use `code-wiki` heuristics. |
| **Issue comments** | `gh api repos/<org>/<repo>/issues/<n>/comments` | For repos where design happens in issues, audit closed issue threads for unextracted ideas. |
| **PR descriptions** | `gh pr list --state merged --limit 100 --json title,body` | Large PRs sometimes describe features that were partially implemented or deferred. |
| **README sections** | Root `README.md`, "Roadmap" or "Future" sections | Often contains aspirational feature lists that were never tracked as issues. |
| **AI chat logs** | `research/`, `intake/`, `.specstory/` | AI conversation transcripts. Use `transcript` heuristics. Apply source clustering. |

### Appendix E: Cross-Reference to Governance

This SOP exists within the governance framework of the eight-organ system. Key connections:

| Document | Relationship |
|----------|-------------|
| [`docs/memory/constitution.md`](../memory/constitution.md) | Articles I-VI govern all specifications including this SOP. Article III (dependency flow) constrains which organs can produce features for which. |
| [`governance-rules.json`](../../governance-rules.json) | Defines promotion state machine and dependency edges. When creating issues, respect the organ's tier and promotion status from `seed.yaml`. |
| [`key-workflows.md`](./key-workflows.md) | Workflow #7 references this SOP. After completing an audit, use Workflow #1 (Update the Registry) if repo metadata changed. |
| [`operational-cadence.md`](./operational-cadence.md) | Document audits fit into the Week 4 (Review + Maintenance) cycle of the monthly cadence. Audits for ORGAN-III products align with Tuesday/Thursday product days. |
| [`minimum-viable-operations.md`](./minimum-viable-operations.md) | If the audit reveals system maintenance issues (broken links, missing CI, stale configs), log them through MVO procedures rather than creating feature issues. |
| [`concordance.md`](./concordance.md) | Use the concordance for ID format lookups (DOC-*, F-*, EXT-*) and cross-organ reference resolution. |

### Appendix F: Document Type Heuristics

#### F.1: Authored Documents

Standard prose written by humans — research memos, brainstorm notes, planning docs, architecture descriptions.

| Signal | Example | Likely extraction |
|--------|---------|-------------------|
| "We could..." / "We should..." / "Consider..." | "We could add a spectator mode" | Feature idea |
| "The research shows..." / "Studies indicate..." | "Loss aversion coefficient is 1.955" | Behavioral constant or parameter |
| "Legal requirement" / "Must comply with..." | "Must verify age 18+ before staking" | Compliance feature |
| "Not yet implemented" / "Future work" / "Phase 2+" | "Phase 2: PvP lobbies" | Backlog item |
| Architectural diagrams with unbuilt components | "Oracle Network (planned)" | Infrastructure feature |
| Competitor analysis gaps | "Competitor X doesn't offer Y" | Differentiator feature |
| User journey steps without code | "User receives push notification" | Missing implementation |
| "Risk: ..." / "Mitigation: ..." | "Risk: users fabricate proofs" | Security feature |
| Parenthetical asides and footnotes | "(this could also handle offline mode)" | Hidden feature idea |
| Section transitions with forward references | "which we'll address when we build the dashboard" | Untracked dependency |

#### F.2: AI Chat Transcripts

Conversation logs from AI assistants (Perplexity, ChatGPT, Claude). High density, often repetitive across sessions.

| Signal | Example | Likely extraction |
|--------|---------|-------------------|
| Numbered/bulleted actionable lists | "1. Deploy ollama, 2. Configure routing" | Implementation steps -> feature |
| Named tools, services, or frameworks | "Use CodeRabbit for automated review" | Tooling integration |
| "Strategic gap" / "missing" / "blind spot" | "No sensitivity-based routing exists" | Infrastructure gap |
| Statistical claims with citations | "METR finds 48% of AI code has issues" | Risk metric or threshold |
| Roadmap or phase structure | "Phase 1: local, Phase 2: hybrid" | Backlog sequencing |
| Consensus across AI responses | 3/3 engines recommend the same | High-confidence feature |
| "Should" / "must" / "critical" language | "Must implement human-in-the-loop" | Safety requirement |
| Comparison tables | "| Tool | Pros | Cons |" | Evaluation criteria |
| Explicit recommendations sections | "Recommendations: ..." | Direct feature candidates |
| Warnings or caveats | "Warning: without X, Y will fail" | Prerequisite feature |

**Transcript-specific guidance:**
- AI responses often front-load the most important items — but bury second-order insights deep in numbered lists (items 8-15). Read the full list.
- When the same question was asked of multiple AIs, cross-reference answers. Agreement = high confidence. Disagreement = tension.
- AI responses may hallucinate citations or statistics. Flag statistical claims for verification but still extract the underlying feature idea.

#### F.3: Reference Books & Papers

External academic or professional publications consumed as part of project research.

| Signal | Example | Likely extraction |
|--------|---------|-------------------|
| Chapter summaries with implications | "This framework suggests that..." | Theoretical grounding for feature |
| Case studies with parallels | "Company X solved this by..." | Implementation pattern |
| Framework definitions | "The 4-layer trust model consists of..." | Architecture template |
| Empirical findings | "Users preferred X over Y by 73%" | Design decision evidence |
| Cited limitations | "This approach fails when..." | Edge case to handle |
| "Further research needed" sections | "Open questions include..." | Research backlog item |
| Bibliography entries of interest | Referenced work not yet in library | SYLLABUS candidate |

#### F.4: RFCs and ADRs

Formal proposals and architectural decision records.

| Signal | Example | Likely extraction |
|--------|---------|-------------------|
| "Consequences" sections | "This means we must also..." | Implied feature requirement |
| "Alternatives Considered" / "Rejected" | "We considered X but chose Y because..." | Revisitable alternative |
| "Open Questions" | "TBD: how to handle offline mode" | Unresolved feature |
| "Status: Draft" or "Status: Proposed" | Entire RFC content | Unimplemented proposal |
| Migration paths | "To migrate from current state..." | Migration feature |
| "Non-goals" sections | "Explicitly not: real-time sync" | Future feature candidate |
| Decision date vs implementation date gap | RFC from 6 months ago, no code | Stalled feature |

#### F.5: Code and Wiki

Source code comments, GitHub wiki pages, README roadmap sections.

| Signal | Example | Likely extraction |
|--------|---------|-------------------|
| `TODO` / `FIXME` / `HACK` comments | `// TODO: add retry logic` | Missing implementation |
| `@deprecated` annotations | `@deprecated Use newMethod instead` | Migration needed |
| Disabled/commented-out code blocks | `// if (featureFlag) { ... }` | Planned feature |
| README "Roadmap" sections | "- [ ] Add OAuth support" | Tracked but not implemented |
| Wiki discussion pages | "We discussed adding X and decided..." | Decision + possible feature |
| Configuration with unused options | `# EXPERIMENTAL_FEATURE=false` | Hidden feature flag |

### Appendix G: Multi-Repo Routing Guide

When an audit produces issues that belong in different repositories, use this guide.

#### Routing table template

```markdown
## Issue Routing Table

**Audit scope**: <corpus description>
**Default repo**: <org>/<repo> (issues that don't match a specific category)

| Category | Target Repo | Labels | Notes |
|----------|-------------|--------|-------|
| governance | org/orchestration-start-here | governance, research-derived | Process and policy issues |
| agent-architecture | org/agent--claude-smith | agent-architecture, research-derived | Claude agent features |
| safety-protocol | org/petasum-super-petasum | safety-protocol, research-derived | Safety and guardrails |
| orchestration | org/agentic-titan | orchestration, research-derived | Multi-agent framework |
| *default* | org/orchestration-start-here | research-derived | Anything not matching above |
```

#### Disabled-issues handling

If a target repo has GitHub Issues disabled:

1. Route issues to the nearest parent/umbrella repo that does have issues enabled
2. Apply a `routed-from:<original-repo>` label to maintain provenance
3. Document the redirect in the routing table

```bash
# Check if issues are enabled
gh repo view <org>/<repo> --json hasIssuesEnabled -q '.hasIssuesEnabled'
```

#### Cross-organ routing rules

When documents reference features that span organs, respect the dependency flow:

- ORGAN-I/II/III features: route to the specific organ's repo
- ORGAN-IV orchestration features: route to `orchestration-start-here` or `agentic-titan`
- ORGAN-V documentation features: route to the ORGAN-V repo
- Cross-organ features: route to `orchestration-start-here` (ORGAN-IV is the orchestrator)

#### Label creation for new repos

```bash
# Minimal label set for a new target repo
for label in "enhancement" "documentation" "research-derived"; do
  gh label create "$label" --repo <org>/<repo> 2>/dev/null || true
done
```

### Appendix H: Completeness Proof Methodology

#### Coverage calculation

```
coverage = (items covered by existing extractions) / (total extractable items identified by fresh reader)
```

Where:
- **Items covered** = extractions from Phase 2 + extractions from Phase 2 re-reads
- **Total extractable items** = all items the fresh Phase 3 reader identifies as extractable

The fresh reader should err on the side of inclusion — if something *might* be extractable, count it. This keeps the coverage metric conservative.

#### Gap classification scheme

| Code | Name | Meaning | Typical action |
|------|------|---------|---------------|
| S | Surface | Obvious item missed in first pass | Create new EXT-NNN |
| R | Refinement | Existing extraction incomplete | Amend existing EXT-NNN |
| P | Pattern | Cross-document pattern | Feed to Phase 5 (synthesis) |
| A | Antagonist | Contradicts another extraction | Add to tension register |
| L | Low-value | Too granular for standalone issue | Note in audit summary |
| N | Non-obvious | Requires domain expertise to spot | Document for future review |

#### Tension detection protocol

For each document pair (D_i, D_j) where i != j:

1. Compare claims, recommendations, and assertions
2. If D_i says X and D_j says NOT-X (or a conflicting Y): record as tension
3. Classify using the 6-type schema (COMPLEMENTARY, CONTEXT-DEPENDENT, TEMPORAL, DATA-QUALITY-ISSUE, NUANCED, UNRESOLVED)

**Common tension patterns:**
- "Use cloud APIs for speed" vs. "Keep all data local for privacy"
- "Automate everything" vs. "Human review is essential"
- "Move fast" vs. "Be careful with safety"
- Newer document contradicts older document's assumption
- Different AI engines give conflicting recommendations on the same question

#### Gate criteria (formal)

```
PASS if:
  overall_coverage >= 0.80
  AND for_all(doc in corpus):
    doc.coverage >= 0.50 OR doc.has_justification == true
  AND tension_register.is_complete == true

FAIL otherwise → return to Phase 2, re-extract, re-check
```

### Appendix I: SYLLABUS Variants

#### I.1: Academic Variant

For corpora containing books, papers, and academic references.

```markdown
# Reference Syllabus: <Project Name>

## Core Reading (directly informs product design)

1. **Author — Title** (format). Key takeaway: one-sentence product implication.
   - Issues derived: #N, #M
   - Framework applied: <name>
2. ...

## Supplementary Reading (broader context)

1. **Author — Title** (format). Relevance: ...
2. ...

## Recommended Further Reading (not yet in library)

1. **Author — Title**. Why: fills gap in <area>.
2. ...
```

#### I.2: Tooling Variant

For corpora containing tool evaluations, service comparisons, and framework recommendations.

```markdown
# Tool & Methodology Reference: <Project Name>

## Integrated Tools (currently in use or planned)

| Tool | Purpose | Status | Issues |
|------|---------|--------|--------|
| CodeRabbit | Automated code review | Planned | #N |
| ollama | Local LLM inference | Not installed | #M |

## Evaluated Tools (considered but not adopted)

| Tool | Purpose | Why not | Revisit? |
|------|---------|---------|----------|
| ... | ... | ... | Yes/No |

## Methodologies & Frameworks

| Name | Source | Application | Issues |
|------|--------|-------------|--------|
| Frame/Shape/Build/Prove | DOC-CND-01 | Task lifecycle | #N |

## People & Organizations Referenced

| Name | Context | Relevance |
|------|---------|-----------|
| ... | ... | ... |
```

#### I.3: Mixed Variant

Combine sections from both Academic and Tooling variants. Use when the corpus contains both types.

### Appendix J: Retrospective Template

File this as part of the audit summary (Phase 7, Step 5) or as a standalone document.

```markdown
# Audit Retrospective: <Project/Corpus Name>

**Date**: YYYY-MM-DD
**Auditor**: @username
**SOP version used**: v2.0

## What worked well

- <Observation with specific example>
- <Observation>

## What didn't work

- <Observation with specific example>
- <Observation>

## Timing accuracy

| Phase | Estimated | Actual | Delta | Notes |
|-------|-----------|--------|-------|-------|
| Phase 0 | 15m | — | — | |
| Phase 1 | 15-30m | — | — | |
| Phase 2 | 1-3h | — | — | |
| Phase 3 | 1-2h | — | — | |
| Phase 4 | 1-2h | — | — | |
| Phase 5 | 30-60m | — | — | |
| Phase 6 | 1-3h | — | — | |
| Phase 7 | 30-60m | — | — | |
| **Total** | **~6-12h** | — | — | |

## Coverage analysis

- Initial Phase 2 coverage: N%
- Post-Phase 3 coverage: N%
- Delta: +N% (N new extractions from completeness proof)
- Was the completeness proof worth the time investment? Yes/No — because...

## SOP amendment recommendations

### Amendment 1: <Title>

**What to change**: <specific section or instruction>
**Why**: <evidence from this execution>
**Proposed text**: <draft wording>

### Amendment 2: ...

## Notes for next execution

- <Anything the next auditor should know>
```

---

## Quick Reference Card

```
+==============================================================+
|  DOCUMENT AUDIT & FEATURE EXTRACTION v2.0 -- QUICK REF       |
+==============================================================+
|                                                               |
|  PHASE 0: SCOPE & CLASSIFY                                   |
|  [ ] Determine scope (single/multi-repo)                     |
|  [ ] Classify document types -> select heuristics            |
|  [ ] Build routing table (if multi-repo)                     |
|  [ ] Plan agent allocation (size x density)                  |
|                                                               |
|  PHASE 1: INVENTORY & TRIAGE                                 |
|  [ ] List all files, classify format + readability           |
|  [ ] Assign thematic cohorts OR folder order                 |
|  [ ] Cluster shared-prompt/shared-topic docs                 |
|  [ ] Flag high-density docs for double-read                  |
|  [ ] Build MANIFEST.md                                       |
|                                                               |
|  PHASE 2: READ & EXTRACT                                     |
|  [ ] Read EVERY document word-for-word                       |
|  [ ] Use type-specific heuristics (Appendix F)               |
|  [ ] Double-read high-density flagged docs                   |
|  [ ] Self-estimate coverage per document                     |
|  [ ] Re-read any doc below 70% coverage                     |
|                                                               |
|  * PHASE 3: COMPLETENESS PROOF (mandatory gate) *            |
|  [ ] Fresh agents re-read all docs adversarially             |
|  [ ] Coverage table per document                             |
|  [ ] Detect antagonistic tensions between docs               |
|  [ ] GATE: >=80% overall, >=50% per-doc, all tensions IDed  |
|  [ ] If gate fails -> return to Phase 2 for re-extraction    |
|                                                               |
|  PHASE 4: DEDUP & TENSION RESOLUTION                         |
|  [ ] Cross-ref: backlog + issues + codebase                  |
|  [ ] Merge source-cluster overlaps (30-50% expected)         |
|  [ ] Classify: SKIP / ENHANCE / CREATE / TENSION             |
|  [ ] Resolve each tension with classification                |
|                                                               |
|  PHASE 5: SYNTHESIS                                          |
|  [ ] Identify cross-cutting themes (3+ docs or 2+ repos)    |
|  [ ] Map theme dependencies + execution order                |
|  [ ] Integrate tensions as a named theme                     |
|  [ ] Compile risk data appendix (if applicable)              |
|                                                               |
|  PHASE 6: CREATE ISSUES                                      |
|  [ ] Route by Phase 0 routing table                          |
|  [ ] Sequential creation (>=2s delay)                        |
|  [ ] Include tensions in issue body where relevant           |
|  [ ] Batch by category, maintain running tally               |
|                                                               |
|  PHASE 7: POST-AUDIT ARTIFACTS                               |
|  [ ] MANIFEST.md, FEATURE-BACKLOG.md, SYLLABUS.md (variant) |
|  [ ] Synthesis document + completeness proof                 |
|  [ ] Audit summary with retrospective                        |
|  [ ] File SOP amendment recommendations                      |
|  [ ] Commit + push                                           |
|                                                               |
|  GATE THRESHOLDS                                             |
|  Overall coverage: >=80%    Per-document floor: >=50%        |
|  All antagonistic tensions: identified + classified          |
|                                                               |
|  LIGHT MODE (<= 10 docs)                                    |
|  Phase 0+1 merge | Phase 2+3 same agent | Phase 4+5 merge   |
|  Phase 6+7 unchanged | Same gate thresholds                  |
|                                                               |
|  COMMANDS                                                    |
|  gh issue list --repo O/R --state open --limit 500           |
|  gh issue create --repo O/R --title "feat: ..." --body "..." |
|  gh issue comment N --repo O/R --body "..."                  |
|  pandoc -f epub -t plain in.epub -o out.txt                  |
|  pandoc -f pdf -t plain in.pdf -o out.txt                    |
|  sleep 2  # between issue creation calls                     |
|                                                               |
+==============================================================+
```

---

*This SOP was derived from two executions:*

1. *Styx/ORGAN-III (`peer-audited--behavioral-blockchain`): 52 authored docs across 6 folders, 74 issues (#46-#119), single repo, 2026-03-04. Established the 5-phase v1 architecture.*

2. *ORGAN-IV (`organvm-iv-taxis`): 16 AI chat transcripts in 4 thematic cohorts, 73 issues across 150 repos (orchestration-start-here, agentic-titan, petasum-super-petasum, agent--claude-smith), 2026-03-06. Exposed structural gaps: 70% first-pass coverage, 8 undetected tensions, 5 under-extracted documents, ad-hoc multi-repo routing. Motivated the v2 revision with completeness proof, tension detection, synthesis, and universal document type support.*

*The procedure is codified for reuse across all ~111 repos in the eight-organ system.*
