# 08: Canonical Action Plan (Post-Cross-Validation)

**Date:** 2026-02-09
**Status:** CANONICAL — this document resolves all contradictions from the cross-validation cycle and defines the executable Bronze Sprint plan.
**Supersedes:** `07-cross-ai-logic-check-results.md` (executive verdict), selective aspects of `05-risk-map-and-sequencing.md` (timeline/sequencing), `implementation-package-v2.md` (Phase 1 scope — Bronze replaces all-at-once)
**Source intelligence:** 3 AI models (gpt-5, gemini-3-pro-preview, gpt-5) × 2 runs (Run A/B identical, Run C ~5.5 hours later), producing 6,004+ lines of validation analysis across `gemini-cli/`, `github-copilot-cli/`, `codex-cli/`

---

## 1. Resolved Decisions

Every contradiction surfaced by the cross-validation cycle has been resolved by human decision. Each entry states the contradiction, the resolution, and the reasoning.

### D-01: Budget Correction Propagation — DECIDED: Scenario Banding

**Contradiction:** Run A/B recommends preserving original TE figures with explanatory correction notes (~13% optimism, finding C7). Run C recommends formally updating all figures to a single corrected canonical baseline.

**Resolution:** Use scenario banding throughout all planning documents. Rather than picking a single number or preserving stale figures with notes, express budgets as ranges (e.g., "1.1M–1.6M TE for Bronze") that acknowledge the variance discovered through cross-validation. The band itself is the statement.

**Reasoning:** Banding is more honest than either alternative. It reflects the empirical finding that identical prompts produced different calibrations ~5.5 hours apart. A single number implies false precision; notes on original figures create cognitive overhead. The band communicates: "our best estimate falls in this range, and here's why."

**Sources:** `gemini-cli/validation_synthesis.md` (C1-C5), `codex-cli/runs/20260209-135130/three_run_comparison_report.md` (contradiction matrix), `github-copilot-cli/00-MANIFEST-AND-INDEX.md` (decision #3)

---

### D-02: Bronze Flagship Selection — DECIDED: Defer to Exploration

**Contradiction:** Run A/B recommends 5 flagships (one per organ I–V) + 2 stretch goals. Run C recommends 7 required flagships. Both runs pre-select specific repos based on `repo-registry.json` portfolio_relevance and current scores.

**Resolution:** Do not pre-select flagship repos. Full repo exploration and README draft attempts will reveal which repos are genuinely showcase-ready and which need more work than their scores suggest. The flagship list emerges from doing the work, not from planning documents.

**Reasoning:** Pre-selection based on registry scores (which are themselves estimates) risks committing to repos that turn out to be hollow shells or committing away from repos that turn out to be surprisingly strong. The 8 unregistered repos in ORGAN-I haven't even been classified yet. Let the work speak.

**What IS decided:** Bronze tier requires at minimum one fully documented flagship per organ (I–V mandatory, VI–VII at least stubs). The specific repos are TBD pending exploration.

**Sources:** `gemini-cli/copilot_validation_response.md` (flagship selection §1a), `codex-cli/runs/20260209-135130/copilot_validation_response.md` (7 CRITICAL repos), `gemini-cli/validation_synthesis.md` (D1 flagship disagreement)

---

### D-03: Bronze TE Baseline — DECIDED: Band 1.1M–1.6M TE

**Contradiction:** Run A/B estimates ~1.1M TE for Bronze (aggressive, assumes tight execution). Run C estimates ~1.5M TE (includes iteration buffer and coordination overhead). The gap is ~36%.

**Resolution:** Plan at ~1.5M TE. Report as band: 1.1M–1.6M TE. The lower bound represents optimistic single-pass execution; the upper bound includes the 10% coordination overhead, discovery contingency, and 2–3 revision cycles per flagship.

**Band components:**
- Flagship READMEs (5–7 × ~107K TE avg): 535K–750K TE
- Registry schema work: ~88K TE
- Process essay: ~120K TE
- Cross-reference resolution pass: ~100K TE
- Coordination overhead (10%): ~84K–106K TE
- Discovery contingency: ~100K–200K TE
- **Total: ~1,027K–1,364K TE** (round to 1.1M–1.6M band)

**Sources:** `gemini-cli/copilot_validation_response.md` (§2d Bronze feasibility), `codex-cli/runs/20260209-135130/copilot_validation_response.md` (Bronze ~1.5M), `github-copilot-cli/THREE_CLI_COMPARISON_ANALYSIS.md` (Divergence 3)

---

### D-04: Portfolio Narrative Lead — DECIDED: Meta-System First

**Contradiction:** Run A/B recommends leading with shipped production systems (aetheria, coach, etc.) and positioning meta-documentation as supporting evidence. Run C recommends leading with the AI-conductor methodology and orchestration complexity, using products as proof of concept.

**Resolution:** Lead with meta-system. The seven-organ orchestration model, the env-var-first architecture, the cross-AI validation methodology, and the AI-conductor workflow are the differentiating story. Production systems (ORGAN-III repos) serve as evidence that the methodology produces real output.

**Narrative order:**
1. "I designed a seven-organ system to coordinate ~44 repos across 7 GitHub orgs"
2. "I used 4 AI agents in parallel to validate and refine the architecture"
3. "Here are the deployed products that this system produces" (aetheria, coach, etc.)
4. "Here's how I document the process transparently" (ORGAN-V essays)

**Context-dependent override:** For grant applications, production evidence may need to come first (funders want to see tangible output). The canonical order above is for AI hiring and residency contexts.

**Sources:** `gemini-cli/gemini_validation_response.md` (portfolio positioning), `codex-cli/runs/20260209-135130/gemini_validation_response.md` ("Simulating Organizational Scale" framing), `github-copilot-cli/THREE_CLI_COMPARISON_ANALYSIS.md` (Divergence 2)

---

### D-05: Registry & Essay Sequencing — DECIDED: Iterative Both

**Contradiction:** Run C recommends completing registry schema and process essay BEFORE starting flagship READMEs (infrastructure-first). Run A/B recommends building registry and essay alongside flagship writing (agile/iterative).

**Resolution:** Iterative approach. Registry schema hardening and essay writing happen alongside flagship README work, not as sequential prerequisites. Writing flagships will reveal what the registry actually needs (not aspirational schema design). The essay grows as the work provides material to document.

**Practical sequence:**
- **Ongoing:** Registry schema evolves as flagships are written (add fields when workflows need them)
- **Ongoing:** Process essay accumulates material as each flagship is completed
- **Milestone:** Registry schema locked after majority of flagships are drafted (not before)
- **Milestone:** Process essay published when it has enough concrete examples (not on a calendar date)

**Reasoning:** Infrastructure-first assumes you know what the infrastructure needs before you've done the work. The cross-validation itself demonstrated that plans change when you do the actual work (Run A/B vs Run C). Iterative sequencing respects this reality.

**Sources:** `gemini-cli/copilot_validation_response.md` (§5b registry timing), `codex-cli/runs/20260209-135130/copilot_validation_response.md` (registry before first flagship), `github-copilot-cli/THREE_CLI_COMPARISON_ANALYSIS.md` (Divergence 4)

---

### D-06: Framework Productization — DECIDED: Yes, Phase 2

**Contradiction:** Run A/B considers framework productization (extracting `organvm` as a reusable open-source tool) a post-launch activity. Run C elevates it to a medium-priority parallel work stream beginning in Phase 2.

**Resolution:** Begin framework extraction in Phase 2. The `organvm.env` / `organvm.config.json` architecture is already designed for reusability (Phase -1 delivered this). Phase 2 validation work is the natural time to extract the framework: you're already testing the system's governance rules, and extraction forces you to articulate what's general vs. what's instance-specific.

**What this means:**
- Phase 1 (Bronze): No framework extraction work. Focus on flagships.
- Phase 2 (Validation): Extract the organvm template as a separate repository. Document what's framework vs. what's instance.
- Phase 3 (Launch): Framework repo is part of the launch portfolio.

**Sources:** `codex-cli/runs/20260209-135130/gemini_validation_response.md` (productization recommendation), `gemini-cli/gemini_validation_response.md` (framework as product)

---

### D-07: Tiered Repo Classification — DECIDED: Defer to Exploration

**Contradiction:** The cross-validation produced multiple attempts at classifying all 44 repos into tiers (Flagship/Standard/Stub/Archive) based on registry data. Run A/B and Run C disagree on specific assignments.

**Resolution:** Defer all tier assignments. Define the tier criteria (what makes a repo Flagship vs. Standard vs. Stub vs. Archive) but do not assign repos to tiers until full exploration and README draft attempts reveal their actual state.

**Tier criteria (framework only):**

| Tier | Criteria | README Target | TE Budget |
|------|----------|---------------|-----------|
| **Flagship** | Deployed/substantial, CRITICAL portfolio relevance, demonstrates organ's core function | 3,000+ words, 12 sections, working examples | ~107K–180K TE |
| **Standard** | Active development, HIGH/MEDIUM relevance, contributes to organ completeness | 1,000+ words, 8 sections | ~50K–88K TE |
| **Stub** | Placeholder or early-stage, MEDIUM/OPTIONAL relevance | 200+ words, 4 sections (purpose, status, links, author) | ~12K–24K TE |
| **Archive** | Empty, abandoned, or merged elsewhere; INTERNAL/no relevance | Archive notice + redirect | ~8K–12K TE |

**Sources:** `gemini-cli/copilot_validation_response.md` (§4a template tiers), `codex-cli/runs/20260209-135130/copilot_validation_response.md` (archive/populate split)

---

### D-08: Bronze Sprint Timeline — DECIDED: Success Criteria, Not Sprint Count

**Contradiction:** Run A/B implies 2 sprints for Bronze. Run C implies 3. The original plan (`roadmap-there-and-back-again.md`) allocates 2 sprints for all of Phase 1 (~4.4M TE), which is far larger than Bronze scope.

**Resolution:** Do not fix a sprint count. Define success criteria for Bronze completion and let the work determine pace. Premature timeline commitments create pressure to cut quality — exactly the failure mode the Bronze tier was designed to prevent.

**Bronze success criteria (all must be true):**
- [ ] At least one fully documented flagship per organ (I–V mandatory, VI–VII at least stubs)
- [ ] `repo-registry.json` schema includes `dependencies[]`, `promotion_status`, `tier`, `last_validated`
- [ ] All flagship READMEs score ≥90/100 on the `01-readme-audit-framework.md` rubric
- [ ] All cross-references between flagships are resolved (no TBD markers)
- [ ] Process essay ("How I Used 4 AI Agents...") is draft-complete
- [ ] 0 broken links across all flagship READMEs
- [ ] Registry data matches reality for all flagships (no aspirational `100%` or `OPERATIONAL`)

**Sources:** `gemini-cli/validation_synthesis.md` (Bronze definition), `codex-cli/runs/20260209-135130/validation_synthesis.md` (Bronze scope), all three comparison reports

---

## 2. Stable Consensus (No Resolution Needed)

These findings were consistent across all 3 AI models and both validation runs. They are canonical.

| # | Finding | Action | Source |
|---|---------|--------|--------|
| SC-1 | Registry schema is blocking | Add `dependencies[]`, `promotion_status`, `tier`, `last_validated` fields. Adopt JSON Schema + CI lint. | All 6 validation responses |
| SC-2 | Bronze tier is MVL | Scope Phase 1 to flagships + registry + essay, not all 44 repos. | `validation_synthesis.md` (both runs) |
| SC-3 | Coordination overhead is real | Budget 10% of phase TE as explicit line item for reconciling parallel AI streams. | `validation_synthesis.md` (both runs), finding B7 |
| SC-4 | TE budgets are realistic | Use `02-repo-inventory-audit.md` bottom-up sums as baseline, apply scenario banding. | `copilot_validation_response.md` (both runs) |
| SC-5 | Process essay is highest priority | "How I Used 4 AI Agents to Cross-Validate a Seven-Organ System" — write iteratively alongside flagships. | All 6 validation responses |
| SC-6 | Human review is pacing constraint | Batch reviews in 5-repo chunks. Flagship reviews when cognition is fresh. AI-assisted fact-checking. | `copilot_validation_response.md` (Run A/B §7b) |
| SC-7 | Cross-references need two-pass approach | Write READMEs with `[TBD:org/repo#section]` placeholders; resolve in dedicated pass after drafts exist. | `copilot_validation_response.md` (Run A/B §3) |
| SC-8 | Templates must be tiered | Flagship (12 sections), Standard (8 sections), Stub (4 sections). One-size-fits-all fails. | `copilot_validation_response.md` (both runs §4) |

---

## 3. Bronze Sprint Definition

### Scope

The Bronze Sprint produces the **Minimum Viable Launch (MVL)**: enough fully documented repos to demonstrate all seven organs, supported by a hardened registry and a process essay.

**Deliverables:**
1. **Flagship READMEs** — At least one per organ (I–V mandatory, VI–VII at minimum stubs). Specific repos TBD after exploration.
2. **Registry schema hardening** — `repo-registry.json` gains `dependencies[]`, `promotion_status`, `tier`, `last_validated` fields. Data populated iteratively as flagships are written.
3. **Process essay** — "How I Used 4 AI Agents to Cross-Validate a Seven-Organ System" (~4,000–5,000 words). Written iteratively as flagships provide material.
4. **Cross-reference resolution** — All inter-repo links validated. No TBD markers in shipped READMEs.

### TE Budget

**Band: 1.1M–1.6M TE**

| Line Item | Low Estimate | High Estimate |
|-----------|-------------|---------------|
| Flagship READMEs (5–7) | 535K TE | 750K TE |
| Registry schema work | 70K TE | 88K TE |
| Process essay | 100K TE | 120K TE |
| Cross-reference pass | 80K TE | 100K TE |
| Coordination overhead (10%) | 79K TE | 106K TE |
| Discovery contingency | 100K TE | 200K TE |
| **Total** | **~964K TE** | **~1,364K TE** |

Rounded band: **1.0M–1.4M TE** (conservative round: **1.1M–1.6M TE** including margin)

### Timeline

No fixed sprint count. Work continues until success criteria (§1, D-08) are met. Pace is governed by human review capacity (~3–4 hours/day of concentrated review) and discovery during exploration.

### Success Criteria

See D-08 above. All 7 checkboxes must be satisfied before Bronze is declared complete.

---

## 4. Tiered Repo Classification

**Status: DEFERRED** (per D-07)

Tier criteria are defined in D-07 (Flagship/Standard/Stub/Archive with word counts, section counts, and TE ranges). Specific repo assignments will emerge from full exploration and README draft attempts.

**What happens during exploration:**
1. Visit each of the 44 registered repos + 8 unregistered ORGAN-I repos + 14 local repos
2. Assess actual code state, README state, and portfolio potential
3. Assign preliminary tiers based on reality, not registry aspirations
4. Adjust flagship selections based on what's genuinely showcase-ready

**Expected output:** An updated version of the `02-repo-inventory-audit.md` table with tier assignments, replacing the current REWRITE/REVISE/POPULATE/ARCHIVE columns with Flagship/Standard/Stub/Archive.

---

## 5. Sequencing

### Resolved: Iterative, Not Sequential

The infrastructure-first vs. narrative-first tension is resolved by doing both iteratively. No phase gates between registry work, essay writing, and flagship READMEs.

**Practical execution pattern:**

```
EXPLORATION PHASE (no fixed duration):
  │
  ├── Explore all repos across all 7 organs
  ├── Draft README attempts reveal tier assignments
  ├── Registry schema evolves based on what workflows need
  │
  └── Output: Tier assignments, flagship selections, revised TE estimates
      │
BRONZE EXECUTION (criteria-driven, not time-boxed):
  │
  ├── Write flagship READMEs (parallel across organs)
  │     ├── Each flagship informs registry data
  │     ├── Each flagship provides essay material
  │     └── Cross-references use TBD placeholders
  │
  ├── Registry hardening (iterative)
  │     ├── Schema fields added as needed
  │     └── Data populated alongside README writing
  │
  ├── Process essay (accumulative)
  │     ├── Material gathered from each completed flagship
  │     └── Draft grows organically, published when substantial
  │
  └── Cross-reference resolution (final pass)
        ├── All TBD markers resolved
        ├── All links validated (404 check)
        └── Human review of inter-organ narrative coherence
```

**Writing order within organs** (respects dependency flow I→II→III, no back-edges):
- ORGAN-I flagships first (establishes vocabulary)
- ORGAN-II/III in parallel (they're independent of each other)
- ORGAN-IV/V last (they synthesize everything, have most cross-references)
- ORGAN-VI/VII stubs can happen anytime

---

## 6. What NOT to Do (Rejected by Cross-Validation Consensus)

These items were explicitly rejected or deprioritized by all three AI models and/or both validation runs:

| Rejected Item | Why | Source |
|---------------|-----|--------|
| All-at-once binary launch gate | Unanimously rejected. Bronze tier replaces it. | All validation responses |
| Monthly governance audits at launch | Quarterly is sufficient. Monthly creates overhead with no audience. | `gemini-cli/gemini_validation_response.md` |
| POSSE automation at launch | Premature. No audience exists to distribute to. Manual distribution first. | `codex-cli/runs/20260209-135130/gemini_validation_response.md` |
| Promotion ceremony process | Governance without software is overhead. Implement when repos actually need promotion. | `gemini-cli/validation_synthesis.md` (C6 critique) |
| NSF Convergence Accelerator application | Timeline misaligned. Frame grants as sustainability funding, not seed funding. | `codex-cli/runs/20260209-135130/gemini_validation_response.md` |
| Holly Herndon / Lieberman / Kogan comparisons | Too aspirational for current portfolio state. Demonstrate first, compare later. | `codex-cli/runs/20260209-135130/gemini_validation_response.md` |
| Pre-selecting flagships from planning data | Registry scores are estimates. Let exploration reveal actual repo quality. | Human decision D-02 |
| Fixed sprint timeline | Premature commitment creates quality pressure. Criteria-driven completion instead. | Human decision D-08 |

---

## 7. Unique Insights Worth Preserving

These emerged from specific models or runs and are valuable even though they're not consensus items.

### From Codex (Technical Lens)
- **Machine-first registry:** The registry should have a JSON Schema that CI can lint on every PR. Not just "source of truth" but "machine-validatable source of truth." (`codex-cli/runs/20260209-135130/codex_validation_response.md`)
- **Minimal repo object:** Codex proposed a concrete schema with 15+ fields (id, full_name, organ, stage, launch_tier, documentation_status, last_validated_at, ci_status, topics, dependencies, promotion_status, promotion_targets, promotion_history, process_doc_ref, essay_refs, analytics_key). Use as reference when hardening. (`codex-cli/runs/20260209-135130/codex_validation_response.md`)

### From Gemini (Strategic Lens)
- **"Simulating Organizational Scale in Solo Practice":** This framing — a solo practitioner simulating the coordination complexity of a 50-person org — is the most compelling portfolio narrative. Use it in the process essay. (`codex-cli/runs/20260209-135130/gemini_validation_response.md`)
- **"System Design Journal":** Curate the planning documents themselves into a narrative. The corpus IS the portfolio piece, not just the READMEs it produces. (`codex-cli/runs/20260209-135130/gemini_validation_response.md`)
- **Knight Foundation is the right first grant target.** Frame as sustainability (not seed). Lead with governance methodology. Knight's Art + Tech Expansion Fund explicitly funds "long-term digital capacity" — the evaluation criteria are organizational capacity, sustainability, and long-term vision. Frame the application as: "Building the infrastructure to support a future community around autonomous creative systems." Audience size is NOT a blocker for this fund. (`gemini-cli/gemini_validation_response.md`)
- **12 deployed commercial products as lead talking point.** The portfolio undersells production work. Gemini identified that 12 deployed products (aetheria, coach, etc.) are more impressive to funders and hiring managers than the orchestration system itself. Revised pitch: *"Over the past [X years], I've built 12 deployed commercial products spanning education, coaching, real estate, and media. To coordinate this work, I developed organvm: a 7-organ orchestration framework."* Lead with deployed systems, show organvm as operational infrastructure (not aspirational planning). (`gemini-cli/gemini_validation_response.md`, `gemini-cli/validation_synthesis.md` S3)
- **Better practitioner comparables.** Instead of Holly Herndon / Lieberman / Kogan (rejected in §6), use: (1) **Julian Oliver** — artist-engineer, infrastructure focus, governance protocols; (2) **Nicky Case** — systems thinking, educational tools, documentation-first transparent process; (3) **Hundred Rabbits** (Devine Lu Linvega & Rekka Bellum) — small-scale sustainable creative infrastructure, extensive documentation. These comparables match the current portfolio state rather than aspirational positioning. (`gemini-cli/gemini_validation_response.md`, `gemini-cli/validation_synthesis.md` S2)

### From Copilot (Execution Lens)
- **Human review fatigue after repo 15–20.** The most dangerous failure mode is cognitive, not technical. Batch reviews in 5-repo chunks, prioritize flagships early when cognition is fresh. (`gemini-cli/copilot_validation_response.md` §7b)
- **Self-review 4-step process ("Stranger Test"):** (1) AI validation pass (template compliance, links, code syntax), (2) Human review (facts, narrative, portfolio positioning), (3) Time-delayed re-review (24–48 hours, applying the "Stranger Test": "If I were a grant reviewer seeing this for the first time, would this convince me?"), (4) AI cross-check (second opinion). Estimated cost: ~5K TE automated + ~12K TE AI cross-check per repo; ~15–20 min human review per flagship, ~10 min per standard. (`gemini-cli/copilot_validation_response.md` §4c, `github-copilot-cli/analysis_differences_report.md`)
- **Archive-vs-populate split for ORGAN-II:** Archive 4 generic placeholders (example-generative-visual, example-interactive-installation, example-ai-collaboration, docs-core-system). Populate 4 portfolio-critical repos (showcase-portfolio, archive-past-works, case-studies-methodology, example-generative-music). (`gemini-cli/copilot_validation_response.md` §1b)

### From Cross-Run Comparison (Meta-Findings)
- **AI validation is non-deterministic for strategy.** Same prompts, ~5.5 hours apart, produced different strategic recommendations while core technical findings remained stable. This is itself a portfolio-worthy finding. (`github-copilot-cli/THREE_CLI_COMPARISON_ANALYSIS.md`)
- **Model provenance matters.** Run C used gpt-5 and gemini-3-pro-preview. Run A/B model pins were not recorded. Future validation runs should always record model versions. (`codex-cli/runs/20260209-135130/provenance.md`)

### Audience-Dependent Narrative Switching

D-04 says "meta-system first" for hiring. §7 notes "12 deployed products" as lead talking point for funders. These are audience-dependent, not contradictory:

| Audience | Lead With | Evidence | Close With |
|----------|-----------|----------|------------|
| AI hiring / residencies | Meta-system orchestration (D-04) | 12 deployed products | Cross-AI validation methodology |
| Grant applications | 12 deployed products + metrics | organvm as operational infrastructure | Process essay as sustainability evidence |
| Academic / research | Cross-AI validation findings | Org architecture as methodology | Theory repos as intellectual contribution |

---

## 8. Supersedes

This document supersedes or updates the following:

| Document | What Changes |
|----------|-------------|
| `07-cross-ai-logic-check-results.md` | **Superseded.** The "Bronze Sprint" action plan in §Action Plan is replaced by this document's §3. The 5-flagship selection is replaced by exploration-first approach (D-02). |
| `05-risk-map-and-sequencing.md` | **Partially superseded.** The daily breakdown schedule (Mon–Sun) is obsolete — replaced by criteria-driven completion (D-08). Risk assessment (R1–R7) remains valid. |
| `implementation-package-v2.md` | **Partially superseded.** Phase 1 scope is now Bronze (§3), not all 44 repos. Per-task TE estimates (§1.3–1.8) remain valid reference points but are now expressed as bands. |
| `parallel-launch-strategy.md` | **Reframed.** "All 7 organs must launch simultaneously" is preserved but reinterpreted: each organ needs at least ONE flagship at launch, not ALL repos in each organ. |
| `roadmap-there-and-back-again.md` | **Extended.** Phase 0 gains this canonical plan as a deliverable. The Phase 1 description should reference Bronze scope. |
| `gemini_vs_copilot_comparison.md` | **Consumed.** Findings are incorporated into §1 and §2 above. |
| `triptych_comparison_report.md` | **Consumed.** Findings are incorporated into §1 and §7 above. |
| `three_run_comparison_report.md` (both root and codex-cli) | **Consumed.** D-01 through D-05 are resolved in §1 above. |

---

## 9. Provenance

### Cross-Validation Runs

| Run | Directory | Models | Timestamp |
|-----|-----------|--------|-----------|
| A | `gemini-cli/` | Not recorded | ~2026-02-09T13:51 UTC (estimated) |
| B | `github-copilot-cli/` | Same as A (byte-identical) | Same as A |
| C | `codex-cli/runs/20260209-135130/` | Codex: gpt-5, Gemini: gemini-3-pro-preview, Copilot: gpt-5 | 2026-02-09T19:15:05 UTC |

### Decision Authority

All D-register resolutions (D-01 through D-08) were made by the human owner (@4444j99 / @4444J99) on 2026-02-09, informed by the cross-validation intelligence but not bound by any single AI recommendation.

### Synthesis Agent

This document was produced by Claude Opus 4.6, synthesizing the outputs of gpt-5 (Codex, Copilot) and gemini-3-pro-preview (Gemini) validation runs. The synthesis itself is a demonstration of the AI-conductor model: multiple AI systems generate analysis, a coordinating AI synthesizes, and the human decides.

---

## 10. Deferred Technical Items (Phase 2+)

The cross-validation surfaced several technical risks and implementation details that are out of scope for the Bronze Sprint but should be addressed in Phase 2 or Phase 3. They are recorded here to prevent knowledge loss.

### T1: GitHub API Rate Limits

**Source:** `gemini-cli/codex_validation_response.md`, `gemini-cli/validation_synthesis.md`, `gemini-cli/analysis_differences_report.md`

The automation layer (`github-actions-spec.md`) assumes unlimited API calls. GitHub Actions has rate limits of 1,000 requests/hour for authenticated requests. The `monthly-organ-audit.yml` workflow scanning 44 repos × multiple checks per repo could hit these limits.

**Mitigation (Phase 2):** Implement exponential backoff and caching in all audit workflows. Consider splitting the monthly audit into per-organ runs staggered across the month.

### T2: Registry Schema Migration Script

**Source:** `gemini-cli/codex_validation_response.md`, `gemini-cli/validation_synthesis.md`, `gemini-cli/analysis_differences_report.md`

No migration strategy exists for moving from the current `repo-registry.json` schema to the enhanced schema (with `dependencies[]`, `promotion_status`, `tier`, `last_validated`). 44 repos already have entries in the current schema.

**Mitigation (Phase 2):** Write `migrate-registry-v2-to-v3.py` script before making schema changes. Script should validate all existing data, add new fields with sensible defaults, and produce a diff for human review.

### T3: Naming Collision Risk (Global GitHub Namespace)

**Source:** `gemini-cli/codex_validation_response.md`, `gemini-cli/validation_synthesis.md`

GitHub org names are a global namespace. If someone else already owns a target org name (e.g., `organvm-i-theoria`), the rename/creation fails silently.

**Status:** Largely mitigated by Phase -1 completion (2026-02-09), which successfully created/renamed all 7 orgs. Retained here as a contingency note: if org names ever need to change, run `check-org-availability.sh` (recommended by Codex) to pre-validate.

### T4: Secret/PAT Sprawl Across 7 Orgs

**Source:** `gemini-cli/analysis_differences_report.md`, `gemini-cli/gemini_vs_copilot_comparison.md`, `gemini-cli/triptych_comparison_report.md`

Managing PATs and API keys across 7 distinct GitHub organizations and 44 repos creates operational complexity and security risk. Only Gemini identified this as a concern.

**Mitigation (Phase 2):** Define an org-level secret management strategy. The `ORCHESTRATION_PAT` in `organvm.env` should be a single fine-grained PAT with minimal scopes, rotated on a schedule, and documented in the governance model.

### T5: `sync-registry-with-reality.yml` Workflow

**Source:** `gemini-cli/codex_validation_response.md`, `gemini-cli/validation_synthesis.md`

Codex recommended a workflow that audits actual GitHub state against registry claims — discovering repos not in the registry, detecting deleted repos, and validating org membership. This was ranked as the #2 priority workflow (after `validate-dependencies`), recommended to run weekly.

**Mitigation (Phase 2/3):** Add `sync-registry-with-reality.yml` to the CI/CD specification in `github-actions-spec.md`. Implement after the registry schema is locked (D-05 milestone).

---

## 11. Consistency Propagation Checklist

This section tracks whether each superseded document has been updated with back-references and content corrections per the E2G coherence pass (`09-corpus-coherence-review.md`).

### Back-Reference Banners
- [x] `parallel-launch-strategy.md` — banner added (2026-02-09)
- [x] `orchestration-system-v2.md` — banner added (2026-02-09)
- [x] `implementation-package-v2.md` — banner added (2026-02-09)
- [x] `public-process-map-v2.md` — banner added (2026-02-09)
- [x] `roadmap-there-and-back-again.md` — banner added (2026-02-09)

### Content Corrections
- [x] Rejected comparables (Herndon/Lieberman/Kogan → Oliver/Case/Hundred Rabbits) — propagated to 5 files
- [x] NSF Convergence Accelerator — removed from target lists, annotated in pitch paragraphs across 5 files
- [x] Repo count (60+ → ~44) — corrected in 5 files + registry
- [x] Launch criteria (rigid per-organ → exploration-first) — corrected in `orchestration-system-v2.md` (in `docs/implementation/`)
- [x] Audit cadence (monthly → quarterly) — corrected in `orchestration-system-v2.md` (in `docs/implementation/`)
- [x] Timeline (Week 3-4 → criteria-driven) — corrected in `public-process-map-v2.md` (in `docs/implementation/`)

### Narrative Coherence
- [x] Audience-dependent narrative switching table added to §7
- [x] D-04 (meta-system first) reconciled with §7 (12 deployed products)

### Audit Trail
- [x] `09-corpus-coherence-review.md` created with full E2G analysis and edit manifest
