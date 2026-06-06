# Cross-AI Logic-Check Prompts

**Purpose:** Three prompts designed for Codex, Gemini, and Copilot to validate the logic of this planning corpus against the Evaluation-to-Growth findings. Paste each prompt into the respective tool along with the specified documents.

**How to use:** Copy the prompt for each tool. Attach or paste the listed documents. Run it. Collect the structured output. Bring all three responses back for synthesis.

**Post-reconciliation note (2026-02-09):** These prompts reflect the reconciled state of the corpus. All TE budgets now reference `02` bottom-up sums (~4.4M TE Phase 1, ~6.5M TE grand total). The budget reconciliation, TE conversion (278 edits, 15 files, 4 agents), and Phase -1 (org architecture + config files) are all complete. The `06` evaluation includes four new findings discovered during reconciliation: C7 (systematic ~13% optimism), R6 (AI-conductor proof), B7 (coordination overhead ~5-10%), E7 (meta-lesson).

---

## ═══════════════════════════════════════════
## PROMPT 1: CODEX — Technical Feasibility
## ═══════════════════════════════════════════

**Attach these files in this order:**
1. `organvm.env` (in `.config/`) — Read first: the naming architecture (env-var template)
2. `organvm.config.json` (in `.config/`) — Read second: machine-readable org mapping
3. `repo-registry.json` (at root) — Read third: the central registry (source of truth for all repos)
4. `orchestration-system-v2.md` (in `docs/implementation/`) — Read fourth: governance rules and dependency model
5. `github-actions-spec.md` (in `docs/implementation/`) — Read fifth: the 5 workflows that consume the registry
6. `06-evaluation-to-growth-analysis.md` (in `docs/evaluation/`) — Read last: the independent evaluation you're validating

---

### Prompt

```
You are reviewing the technical architecture of a seven-organ creative-institutional system
that coordinates ~44 GitHub repositories across 7 GitHub organizations. An independent
evaluation has already been performed, and a subsequent budget reconciliation pass has been
completed. Your job is to validate or challenge the evaluation's technical findings, from
the perspective of someone who would actually implement this system.

READ THE ATTACHED FILES IN THIS ORDER:
1. organvm.env — the naming architecture (env-var template)
2. organvm.config.json — machine-readable org mapping
3. repo-registry.json — the central registry (source of truth for all repos)
4. orchestration-system-v2.md — governance rules and dependency model
5. github-actions-spec.md — the 5 workflows that consume the registry
6. 06-evaluation-to-growth-analysis.md — the independent evaluation you're validating

CONTEXT: One person is building this. The system uses env-var-based org naming
(organvm.env), a central JSON registry (repo-registry.json), governance rules
(orchestration-system-v2.md), and 5 GitHub Actions workflows (github-actions-spec.md).

COMPLETED SO FAR:
- Phase -1 (org naming architecture) is complete: organvm.env, organvm.config.json,
  organvm.env.local created.
- TE conversion: 278 edits across 15 active documents by 4 parallel AI agents.
- Budget reconciliation: all documents now agree on ~4.4M TE for Phase 1 and ~6.5M TE
  grand total.

THE EVALUATION FOUND:
1. The registry schema is underpowered — missing dependency, promotion_status, tier, and
   last_validated fields that the workflows need
2. Budget reconciliation revealed a systematic ~13% underestimate (C7): top-down estimates
   from 00-c consistently undercount compared to 02's bottom-up sums. The gap was ~500K TE
   for Phase 1 alone. This has been reconciled — all docs now use the 02 numbers — but
   the same optimism likely affects Phases 2-3.
3. The env-var architecture (organvm.env → organvm.env.local → organvm.config.json) is
   sound
4. The registry claims 60 repos but only contains 44
5. A Bronze/Silver/Gold tiered launch was proposed to replace the binary all-or-nothing gate
6. Coordination overhead between parallel AI streams is ~5-10% of total TE (B7): 4 agents
   working from different source documents produced divergent totals requiring human
   reconciliation. This pattern will recur during README writing.

YOUR TASK — answer each question with AGREE / DISAGREE / ADD:

1. REGISTRY SCHEMA
   a. Does the current repo-registry.json schema support the 5 workflows in
      github-actions-spec.md? If not, what specific fields are missing?
   b. The evaluation proposes adding: dependencies[], promotion_status enum, tier enum,
      documentation_status enum, last_validated timestamp. Is this the right set of fields?
      What would you add or remove?
   c. Can the registry realistically serve as the single source of truth for both human
      readers and automated workflows? Or should there be separate human-facing and
      machine-facing registries?

2. GITHUB ACTIONS VIABILITY
   a. Are the 5 specified workflows (validate-dependencies, monthly-organ-audit,
      promote-repo, publish-process, distribute-content) architecturally sound?
   b. Which workflows should be implemented first for maximum value with minimum effort?
   c. The evaluation says managing 4 parallel AI streams (Claude/Gemini/Codex/Copilot) for
      README writing is harder than doing it yourself. Agree or disagree? What's the
      realistic coordination model?

3. ENV-VAR ARCHITECTURE
   a. Is the organvm.env → organvm.env.local → organvm.config.json layering correct?
   b. Should the JSON config be generated FROM the env file, or should they be independent?
   c. Are there edge cases in the ${ORGAN_PREFIX}-${SUFFIX} naming scheme that could break
      GitHub org name constraints?

4. TIERED LAUNCH (Bronze/Silver/Gold)
   a. The evaluation proposes: Bronze = 5 flagship repos + registry (~1.5M TE), Silver = 15
      repos + essay (~3.0M TE), Gold = all 44 + workflows (~6.5M TE). Are these TE estimates
      realistic for a solo developer with AI assistance?
   b. From a technical standpoint, what's the minimum infrastructure needed for Bronze to
      be credible? (e.g., does it need working CI? A live registry endpoint? Working
      cross-references?)

5. BUDGET RECONCILIATION VALIDATION
   a. The reconciled Phase 1 budget is ~4.4M TE (from 02's bottom-up sums). The revised
      grand total is ~7.2M TE when applying the 13% correction to Phases 2-3 plus
      coordination overhead. Does this total seem realistic for the scope described?
   b. Should the ~13% correction from C7 be formally propagated to Phase 2 and Phase 3
      budgets in the planning documents? Or is it sufficient to note the risk?
   c. The coordination overhead (B7) of ~5-10% (~220-440K TE) is currently unbudgeted.
      Should it be added as an explicit line item, or absorbed into per-task estimates?

6. WHAT DID THE EVALUATION MISS?
   a. Are there technical risks not identified in the evaluation?
   b. What's the single most important technical decision to make before starting Phase 0?

FORMAT: Use the AGREE/DISAGREE/ADD structure for each sub-question. Keep responses
concrete and implementation-focused. No motivational language. If something won't work,
say so directly and explain why.
```

---

## ═══════════════════════════════════════════
## PROMPT 2: GEMINI — Strategic Reasoning
## ═══════════════════════════════════════════

**Attach these files in this order:**
1. `00-c-master-summary.md` (in `docs/genesis/`) — Read first: executive summary of the entire system
2. `parallel-launch-strategy.md` (in `docs/strategy/`) — Read second: strategic rationale for simultaneous launch
3. `implementation-package-v2.md` (in `docs/implementation/`) — Read third: the master execution plan with TE budgets and phases
4. `orchestration-system-v2.md` (in `docs/implementation/`) — Read fourth: governance model and dependency rules
5. `public-process-map-v2.md` (in `docs/implementation/`) — Read fifth: ORGAN-V content strategy and distribution plan
6. `06-evaluation-to-growth-analysis.md` (in `docs/evaluation/`) — Read last: the independent evaluation you're validating

---

### Prompt

```
You are a strategic advisor reviewing a creative practitioner's plan to launch a
seven-organ system of ~44 GitHub repositories across 7 organizations. The system spans
theory, art, commerce, orchestration, public writing, community, and marketing. The
practitioner is solo and targets grants (Knight Foundation, Mellon, NSF), AI hiring
(Anthropic, OpenAI), and residencies (Eyebeam, Somerset House) as audiences.

An independent evaluation has been performed, followed by a budget reconciliation pass
that closed a ~500K TE gap across all planning documents. Your job is to assess the
STRATEGIC logic — not the technical implementation.

READ THE ATTACHED FILES IN THIS ORDER:
1. 00-c-master-summary.md — executive summary of the entire system
2. parallel-launch-strategy.md — strategic rationale for simultaneous launch
3. implementation-package-v2.md — master execution plan with TE budgets and phases
4. orchestration-system-v2.md — governance model and dependency rules
5. public-process-map-v2.md — ORGAN-V content strategy and distribution plan
6. 06-evaluation-to-growth-analysis.md — the independent evaluation you're validating

COMPLETED SO FAR:
- Phase -1 (org naming architecture): DONE. Config files created.
- TE conversion: DONE. 278 edits across 15 files by 4 parallel AI agents.
- Budget reconciliation: DONE. ~500K gap closed; all docs now agree on ~4.4M TE Phase 1,
  ~6.5M TE grand total.

THE EVALUATION FOUND:
1. The "meta-system as portfolio asset" positioning relies on analogy to Holly Herndon, Zach
   Lieberman, Gene Kogan — but no evidence that THIS system would be evaluated similarly
2. The urgency framing ("Why Now? 2026 funding landscape") is motivational, not strategic —
   grant cycles don't compress to 2-week sprints
3. The planning corpus itself may be the most impressive artifact — more portfolio-ready
   than the system it describes
4. A Bronze/Silver/Gold tiered launch was proposed: Bronze (5 flagships, ~1.5M TE), Silver (15
   repos + essay, ~3.0M TE), Gold (all 44 + workflows, ~6.5M TE). Revised grand total with
   13% correction + overhead: ~7.2M TE.
5. The TE conversion proved the AI-conductor model works at scale: 278 edits by 4 parallel
   agents in a single session (R6). The process itself — coordinating multiple AI agents,
   discovering budget discrepancies, reconciling across 15 files — is stronger portfolio
   evidence than any individual README.
6. The governance model is overengineered for solo operation (~300K+ TE/month maintenance)
7. The honest narrative ("what I learned building this") is more compelling than the polished
   one ("here is my perfect system")

YOUR TASK — answer each question with AGREE / DISAGREE / ADD:

1. PORTFOLIO POSITIONING
   a. Is "meta-system documentation as primary portfolio asset" a credible strategy for
      grants and hiring in 2026? Or is it too abstract for evaluators who want to see
      shipped products?
   b. The evaluation says the planning corpus is more impressive than the system. Should the
      practitioner literally submit the planning documents as part of grant applications?
   c. For AI hiring specifically (Anthropic, OpenAI): does a 7-organ documentation system
      demonstrate "production-ready thinking"? Or does it look like over-architecture without
      production evidence?

2. GRANT STRATEGY
   a. Which of these is the strongest grant angle: (i) the framework as reusable
      infrastructure for creative practitioners, (ii) the implementation as a case study in
      solo creative practice, (iii) the meta-documentation as evidence of organizational
      capacity?
   b. Is Knight Foundation's "Art + Tech Expansion Fund" a realistic target for this
      project? What about NSF Convergence Accelerator?
   c. The evaluation notes no existing audience (no followers, no email list, no community).
      Does this undermine the grant positioning? How critical is demonstrated audience for
      these funders?

3. THE BRONZE/SILVER/GOLD APPROACH
   a. Does tiered launch make strategic sense for the stated audiences? Or does it signal
      "work in progress" when evaluators want to see "complete"?
   b. What's the minimum that needs to exist for a credible grant application? For a job
      application?
   c. The evaluation proposes "launch Bronze, iterate to Silver, Gold is 3-6 months." Is this
      sequencing strategically sound? Should anything be reordered?

4. NARRATIVE STRATEGY
   a. The evaluation suggests the honest essay — "I Tried to Launch 44 Repos at Once" —
      is more compelling than the polished pitch. Agree? Is vulnerability an asset or
      liability for the target audiences?
   b. The TE conversion itself produced a process narrative more portfolio-ready than any
      README: "How 4 AI Agents Edited 278 Values Across 15 Documents (And What Went Wrong)."
      Should the practitioner prioritize writing THIS process essay over the flagship
      READMEs? Is the AI-conductor narrative the strongest card to lead with?
   c. Should ORGAN-V (public writing) be the FIRST thing to launch, since essays position
      the entire system? Or should it wait until the repos it describes are ready?
   d. The practitioner names Holly Herndon, Zach Lieberman, Gene Kogan as comparables.
      Are these the right references? Who else should be in the comparison set?

5. WHAT DID THE EVALUATION MISS?
   a. Are there strategic opportunities not identified?
   b. What's the strongest counterargument to the evaluation's overall conclusion?
   c. If you had to advise this practitioner on the single most impactful thing to do in
      the next sprint, what would it be?

FORMAT: Use the AGREE/DISAGREE/ADD structure for each sub-question. Be direct about what
will and won't work. Provide specific recommendations, not general encouragement. If the
strategy has a fatal flaw, name it.
```

---

## ═══════════════════════════════════════════
## PROMPT 3: COPILOT — Repo-Level Execution
## ═══════════════════════════════════════════

**Attach these files in this order:**
1. `01-readme-audit-framework.md` (in `docs/planning/`) — Read first: the scoring rubric (0-100) for README quality
2. `02-repo-inventory-audit.md` (in `docs/planning/`) — Read second: per-repo inventory with current scores and TE budgets
3. `03-per-organ-readme-templates.md` (in `docs/planning/`) — Read third: the 12-section README template
4. `05-risk-map-and-sequencing.md` (in `docs/planning/`) — Read fourth: risk identification and writing sequence
5. `repo-registry.json` (at root) — Read fifth: the actual repo data (names, orgs, status, relevance)
6. `06-evaluation-to-growth-analysis.md` (in `docs/evaluation/`) — Read last: the independent evaluation you're validating

---

### Prompt

```
You are reviewing the execution plan for documenting ~44 GitHub repositories across 7
organizations. The repositories span theory frameworks, generative art tools, commercial
products, orchestration infrastructure, public essays, community spaces, and marketing
distribution. One person is doing all the work, with AI assistance.

An independent evaluation has been performed, followed by a budget reconciliation that
aligned all planning documents. Your job is to assess the EXECUTION feasibility — the
actual repo-by-repo writing and validation work.

READ THE ATTACHED FILES IN THIS ORDER:
1. 01-readme-audit-framework.md — the scoring rubric (0-100) for README quality
2. 02-repo-inventory-audit.md — per-repo inventory with current scores and TE budgets
3. 03-per-organ-readme-templates.md — the 12-section README template
4. 05-risk-map-and-sequencing.md — risk identification and writing sequence
5. repo-registry.json — the actual repo data (names, orgs, status, relevance)
6. 06-evaluation-to-growth-analysis.md — the independent evaluation you're validating

COMPLETED SO FAR:
- TE conversion: DONE. 278 edits across 15 files by 4 parallel AI agents.
- Budget reconciliation: DONE. TE budgets validated and reconciled: organ totals from 02
  are authoritative (~4.4M TE Phase 1, ~6.5M TE grand total). The reconciliation closed a
  ~500K TE gap between top-down (00-c) and bottom-up (02) estimates.
- Phase -1: DONE. Org naming architecture created.

THE EVALUATION FOUND:
1. The corpus claims 60 repos but only 44 exist in the registry; 16 are placeholders
2. TE budgets validated and reconciled: organ totals from 02 are authoritative (~4.4M TE
   Phase 1). The reconciliation revealed a systematic ~13% underestimate (C7) in top-down
   planning — ORGAN-I was ~660K planned vs ~850K actual, ORGAN-II was ~850K planned vs
   ~1,110K actual. The gap is largest for POPULATE tasks (~110-180K TE per repo vs ~72K TE
   assumed for typical rewrites).
3. TE budgets validated: 3000-word README ≈ ~72K TE per generation cycle; human review
   (~15 min/repo) is the actual throughput constraint
4. Templates (03) specify 12 sections per README — good structure but infeasible for all 44
5. A Bronze/Silver/Gold tier system was proposed: Flagship (5-7 repos, 3000+ words),
   Standard (15-20, 1000 words), Stub (10-15, 200 words), Archived (5-8, notice only)
6. Cross-references between READMEs create a chicken-and-egg problem during simultaneous
   writing
7. Coordination overhead between parallel AI streams (B7) adds ~5-10% (~220-440K TE) to
   Phase 1. This is currently unbudgeted.

THE REGISTRY (repo-registry.json) CONTAINS THESE REPOS. Your task is to work with the
actual data.

YOUR TASK — answer each question with AGREE / DISAGREE / ADD:

1. FLAGSHIP SELECTION
   a. Based on the registry data (portfolio_relevance, documentation_status, organ), which
      5-7 repos should be flagships? List them by name with reasoning.
   b. The evaluation says ORGAN-II has 4 empty repos that should be archived. Which
      specific repos (from registry data) should be archived vs populated?
   c. Are there any repos currently marked LOW relevance that should actually be flagships?
      Any marked CRITICAL that don't deserve it?

2. WRITING EFFORT ESTIMATION
   a. For a 3000-word technical README with 12 sections, installation instructions, working
      examples, and cross-references — what's a realistic TE estimate per repo, assuming
      AI assistance for first drafts and human editing? The corpus says ~72K TE for rewrites
      and ~88-180K TE for populating from scratch. Validate these ranges.
   b. For a 1000-word standard README — same question.
   c. For a 200-word stub — same question.
   d. Given your estimates: is Bronze (5-7 flagships in ~1.5M TE) realistic? What about Silver
      (15 repos + 1 essay in ~3.0M TE)?

3. CROSS-REFERENCE PROBLEM
   a. The evaluation identifies a chicken-and-egg problem: READMEs cross-reference each
      other, but they're being written simultaneously. What's the practical solution?
   b. Should cross-references be added in a separate pass after all READMEs exist? Or can
      they be written as placeholders first?
   c. Which repos have the MOST cross-references (based on organ relationships) and should
      therefore be written last?

4. TEMPLATE APPLICABILITY
   a. The 12-section template in document 03 was designed for all repos. Which sections are
      essential for flagships, which for standard, and which can be dropped for stubs?
   b. Should ORGAN-I (theory) repos use the same template as ORGAN-III (commerce) repos?
      What organ-specific adjustments are needed?
   c. The validation checklist (04) requires peer review. The evaluation notes this is
      impossible for a solo operator. What's the most effective self-review process?

5. SEQUENCING
   a. The risk map (05) suggests doing ORGAN-I first, then ORGAN-II, then ORGAN-III. The
      evaluation says this sequential work contradicts "parallel launch." What's the optimal
      writing order for the 5-7 flagships?
   b. Should the registry be fixed BEFORE or AFTER writing the first flagship READMEs?
   c. When during this process should the first ORGAN-V essay be written?

6. RECONCILIATION AND OVERHEAD
   a. The reconciliation pass itself consumed coordination overhead not in the original
      budget. How should future phases account for this? Should reconciliation passes be
      budgeted as explicit line items (e.g., ~5-10% of phase TE)?
   b. The ~13% optimism gap (C7) was found comparing top-down vs bottom-up estimates.
      For execution planning, should the practitioner use the bottom-up (02) numbers plus
      an explicit overhead buffer? Or re-estimate from scratch?

7. WHAT DID THE EVALUATION MISS?
   a. Are there execution risks in the repo data that the evaluation didn't catch?
   b. What's the most likely failure mode when a solo developer starts writing READMEs
      across 7 organs?
   c. If the practitioner can only complete 3 repos total in the next sprint, which 3
      should they be?

FORMAT: Use the AGREE/DISAGREE/ADD structure for each sub-question. Reference specific
repo names from the registry where relevant. Be concrete about TE estimates — no ranges
wider than 2x (e.g., "~50K-88K TE" is fine, "~12K-180K TE" is not). If a plan element is
unrealistic, say so and provide an alternative.
```

---

## Using the Results

When you return with all three responses, the synthesis process is:

1. **Consensus items** — Where all 3 tools agree with the evaluation, those findings are confirmed
2. **Disagreements** — Where a tool disagrees, examine its reasoning; this is where the evaluation may need revision
3. **Additions** — New insights from each tool's perspective that the evaluation missed
4. **Meta-findings** — The reconciliation process itself is data. Note where the AIs validate or challenge the new findings (C7's ~13% optimism, R6's AI-conductor proof, B7's coordination overhead). These meta-findings test whether the evaluation's self-analysis holds up under external scrutiny.
5. **Action conflicts** — Where tools recommend contradictory actions, those require a human decision

The goal is not to get three tools to agree with each other — it's to use their different perspectives (technical / strategic / execution) to stress-test the evaluation before acting on it.
