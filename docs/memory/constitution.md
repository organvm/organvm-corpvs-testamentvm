# organvm Project Constitution

**Version:** 1.1.0 | **Ratified:** 2026-02-10 | **Last Amended:** 2026-03-04
**Source:** `CLAUDE.md` Key Invariants (lines 28-34) + `08-canonical-action-plan.md` §2 stable consensus

## Core Principles (Articles I-VI)

### I. Registry as Single Source of Truth
All repo state lives in `repo-registry.json`. The registry is never wrong; if reality and registry disagree, update the registry or fix reality. No document, workflow, or agent may claim authoritative repo state outside the registry.

### II. Unidirectional Dependencies
Flow is I->II->III only. No back-edges: ORGAN-III cannot depend on ORGAN-II; ORGAN-II cannot depend on ORGAN-III. ORGAN-IV orchestrates; ORGAN-V documents; ORGAN-VII amplifies. Dependency violations are structural failures, not style issues.

### III. All Eight Organs Visible at Launch
Each organ has at least one representative at launch — flagship (fully documented) or stub (purpose, status, and link to parent org). The eight-organ system must be visible in its entirety; individual organs may launch at different completeness tiers per Amendment A. "Visible" means a grant reviewer navigating all 8 orgs encounters evidence of each organ's existence and purpose, not that every repo is complete.

### IV. Documentation Precedes Deployment
No Phase N+1 until Phase N is complete. Documentation is the deliverable, not an afterthought. Every README is written before the feature it documents is promoted.

### V. Portfolio-Quality Documentation
Every README is a portfolio piece, written for grant reviewers and hiring managers, not just developers. The "Stranger Test" applies: a grant reviewer seeing this for the first time should be convinced.

### VI. Promotion State Machine
Repos follow: LOCAL -> CANDIDATE -> PUBLIC_PROCESS -> GRADUATED -> ARCHIVED. This governs cross-organ promotion. Repo documentation status uses a separate vocabulary: ACTIVE/DEPLOYED/SKELETON/EMPTY. No state may be skipped.

## Amendments (Post-Cross-Validation Consensus)

### Amendment A: Bronze Tier Launch Path
*Source: SC-2, D-08 in `08-canonical-action-plan.md`*

The Bronze Sprint produces the Minimum Viable Launch: 5 flagships (one per organ I-V) + stubs for VI-VII + hardened registry + process essay. Completion is criteria-driven (D-08 success criteria), not time-boxed. "5 Perfect Repos > 44 Mediocre Repos."

### Amendment B: Coordination Overhead Budget
*Source: SC-3, B7 in `06-evaluation-to-growth-analysis.md`*

Budget 10% of phase TE as explicit line item for reconciling parallel AI streams. Coordination overhead is real and must not be hidden inside task estimates.

### Amendment C: Registry Schema Completeness
*Source: SC-1 in `08-canonical-action-plan.md`*

`repo-registry.json` must include `dependencies[]`, `promotion_status`, `tier`, and `last_validated` fields before Phase 2. Schema evolves iteratively during Bronze (fields added as workflows need them, locked after majority of flagships are drafted).

### Amendment D: AI Non-Determinism Acknowledgment
*Source: Meta-finding in `THREE_CLI_COMPARISON_ANALYSIS.md`*

Same inputs produce different strategic outputs across AI models and across time. All AI-generated deliverables require human review. Budget estimates use scenario banding (ranges), not point estimates, to reflect this variance.

## Quality Gates

### Registry Gate
Does this deliverable update `repo-registry.json`? Is the schema satisfied? Are all required fields populated with verified (not aspirational) data?

### Portfolio Gate
Does this README or essay pass the "Stranger Test" (D-08, Copilot validation §7)? Would a grant reviewer seeing this for the first time be convinced? Score >=90/100 on the `01` rubric for flagships.

### Dependency Gate
Does this deliverable respect the I->II->III flow? No back-edges? Cross-references follow the dependency direction?

### Completeness Gate
Are all TBD markers resolved? 0 broken links? No placeholder content in shipped deliverables?

### Signal Closure Gate
Does this organ's active work have declared produces edges for all entailed outputs per the `entailment_flows` matrix in `governance-rules.json`? Are all downstream organs receiving the signals this activity logically entails? Validate with `organvm governance audit --signal-closure`.

### Triadic Self-Knowledge Gate
Does this formation's `seed.yaml` articulate all three dimensions: telos (the dream), pragma (the reality), and praxis (the plan to close the gap)? Are the fields genuine self-knowledge, not placeholder text? Does a stranger reading them understand why this formation exists, what it has achieved, and what remains? Validate with `organvm governance audit --self-knowledge`.

### Amendment E: Post-Construction Operational Shift
*Source: CONSTITUTIO sprint review (2026-03-04), REGULA governance update*

The system has transitioned from **construction** (building, documenting, deploying) to **operation** (sustaining, validating, evolving). Implications:
- Article III (all organs visible at launch) is **SATISFIED** — all 8 organs are operational (launched 2026-02-11). This article now governs any new organ additions, not existing ones.
- Article IV (documentation precedes deployment) applies to **new features and promotions**, not retroactive documentation of already-deployed repos.
- Amendment A (Bronze Tier Launch Path) is **COMPLETED** — Bronze, Silver, and Gold sprints are done. Amendment A remains as historical record of the launch methodology.
- Amendment C (Registry Schema Completeness) is **COMPLETED** — all required fields are present and validated. Schema formalized as v1.0.0.
- Quality gates remain active for all ongoing work. The Portfolio Gate and Stranger Test become increasingly important as external audiences grow.

### Amendment F: Signal Closure — Lex Necessitatis
*Source: First-principles derivation from Article II (unidirectional dependencies), Constitutional Map §8 (signal flows), AX-2 (epistemic membranes), and the operational principle "N/A is a vacuum." Ratified 2026-03-27.*

The organ system is logically closed under its own axioms. The definitions of organ functions, the canonical signal flows, and the epistemic membrane requirement together constitute a deductive system: given the axioms, certain inter-organ outputs are not optional but logically necessary. An activity in Ergon (III) that does not produce process documentation (→ Logos V), distribution material (→ Kerygma VII), community growth signals (→ Koinonia VI), or research feedback (→ Theoria I) violates the signal flow graph's own definitions.

This principle is deductive, not aspirational. Law is law; logic dictateth. If the axioms are what they are, the conclusions follow — regardless of whether the receiving formations have been built yet. Absence is not deferral; it is violation. Every entailed output that exists nowhere in the system is a vacuum that constitutional law mandates be filled. What is omitted here must, by law, exist elsewhere. What exists nowhere is a constitutional breach.

Implications:
- Every `seed.yaml` `produces` array must declare ALL entailed outputs, not only primary ones
- `organvm governance audit --signal-closure` validates organ-level signal completeness
- IRF-VAC entries are created for any entailed output lacking a receiving formation
- The `entailment_flows` section of `governance-rules.json` is the authoritative reference for which activities entail which outputs
- The Signal Closure Gate is now a mandatory quality gate for all deliverables

Encoded as: AX-6 (Signal Closure) + LIQ-008 (Signal Closure Across Functions) in `governance-rules.json`.

### Amendment G: Tetradic Self-Knowledge — Lex Reflexionis
*Source: First-principles derivation from the observation that every directory is the concrete realization of an idealized form — an intersection of functionalities at work — and that creation is completed by reception, not by intention. Ratified 2026-03-30.*

Every non-archived formation in the system embodies an idealized form. That form has four constitutive dimensions:

1. **TELOS** (τέλος) — The theory, thesis, or dream that called the formation into existence. The intersectional functionalities it idealizes. Why it was conceived. What the world looks like if this formation achieves its purpose.

2. **PRAGMA** (πρᾶγμα) — The concrete thing realized. The honest account of what has been built, how far it is from the ideal, and where the delta lies. Not a description of features but a truthful reckoning of state.

3. **PRAXIS** (πρᾶξις) — The remediation plan. The attack vectors for sharpening and fortifying. The specific actions that close the gap between ideal and real. Not aspirational roadmap but concrete plans of attack addressing known failures and deficiencies.

4. **RECEPTIO** (receptiō) — The account of reception. How the formation has been received, used, critiqued, adopted, transformed, or ignored by audiences beyond its creator. A shovel is only a shovel if it shovels — a theory of shovels does not clear the driveway snow. A book is only the author's exercise as they write it; it becomes an organism when read and imagined by an audience. The society that responds — that attempts to know, critiques, makes art — the culture sitting around the project tells the reception of the project as a living tool. For formations not yet received: the intended reception strategy and what reception would validate the telos. For formations that have been received: documented evidence of that reception.

Insights and theories are not ephemeral. They are structural obligations. Every directory in the system — since at its core it is an idealized form of some intersectional functionalities at work — has dreams for the dream that formed it, the concrete realized, plans of attack for the difference between them, and the society that responds to validate its existence as a real thing in the world. All four must be explicitly articulated.

**Implications:**
1. Every non-archived `seed.yaml` must include `telos`, `pragma`, `praxis`, and `receptio` fields (schema v1.2)
2. Empty or placeholder values are violations — the fields demand genuine self-knowledge
3. The tetradic fields are consumed by: context generation (`organvm context sync`), signal routing (a formation that doesn't know its own purpose can't participate coherently in signal flows), audit (`organvm governance audit --self-knowledge`), and the Stranger Test (a reviewer encountering the formation should immediately understand its dream, its reality, its plan, and its reception)
4. The fields evolve as the formation evolves — they are living documents, not static declarations
5. AX-7 extends AX-6: signal closure requires that outputs exist elsewhere; tetradic self-knowledge requires that the *reason for those outputs* is articulated within and that the *response to those outputs* is captured back
6. The feedback flows (VII/VI/V → I) are the constitutional mechanism by which reception reaches the formation. AX-6 mandates outward signal flow; LIQ-010 mandates that the response flows back and is recorded. The loop must close.
7. A GRADUATED formation with no documented reception is a constitutional anomaly — promoted without evidence that it exists as anything other than its creator's intention

Encoded as: AX-7 (Tetradic Self-Knowledge) + RR-6 (Tetradic Articulation) + LIQ-009 (Reflexive Knowledge Obligation) + LIQ-010 (Reception Completes Existence) in `governance-rules.json`.

### Amendment H: Constructed Polis — Lex Civitatis
*Source: The recognition that in a system of systems in nesting systems, reception cannot be outsourced to the external world's timeline. Each formation must construct its own idealized critical society. Ratified 2026-03-30.*

Every formation is its own universal system. Scientists study a thing. Philosophers interrogate its premises. Critics challenge its execution. Academics place it in lineage. Practitioners test it as a tool. Artists respond to its aesthetic. This will happen in the real world eventually — but the system cannot wait for the world to catch on.

Each formation constructs an **idealized polis** — the critical society that its phase of development demands. This polis actively produces the formation's `receptio` (AX-7) rather than waiting for organic reception. The polis is not decorative commentary or aspirational metadata. It is the mechanism by which self-knowledge is generated under adversarial review, the same operation the IRA panel performs for dissertations extended to every formation in the system.

The polis draws from existing infrastructure:
- **IRA panels** (`auto-revision-epistemic-engine`) — multi-model evaluative consensus with disciplinary personas
- **Triadic Review Protocol** — 3 distinct perspectives minimum (memory: `feedback_triadic_review.md`)
- **Voice governance** (`vox--architectura-gubernatio`) — per-organ voice profiles and stylesheet scoring
- **Faculty registry** (`praxis-perpetua/governance/faculty-registry.yaml`) — named competency domains and evaluation rubrics

The nesting is recursive. A formation's polis examines the formation. An organ's polis examines the organ. The system's polis examines the system. At every level: knowledge creation, each module as its own universal system.

**Implications:**
1. Every non-archived repo at PUBLIC_PROCESS or GRADUATED must declare a `polis` section in seed.yaml (RR-7)
2. Minimum 3 disciplinary lenses per the Triadic Review Protocol — genuinely distinct perspectives
3. Each lens names a role, states what it examines, and records findings (or null for formations not yet reviewed)
4. The polis produces the `receptio` — findings feed back into `pragma` (updating honest assessment) and `praxis` (updating remediation plan)
5. LOCAL/CANDIDATE formations may declare intended lenses with null findings — the polis is planned before it operates
6. The constructed polis is autopoietic: the formation produces the society that evaluates and evolves the formation

Encoded as: AX-8 (Constructed Polis) + RR-7 (Polis Declaration) + LIQ-011 (Autopoietic Reception) in `governance-rules.json`.

### Amendment K: The Symmetry of Record — Lex Umbrae Naturae
*Source: The realization that Nature demands a documentation counterpart. Every formation (Nature) exists in a required and recursive relationship with its record (Counterpart). Ratified 2026-04-02.*

Nature and Counterpart are constitutive. A piece of Nature (code, configuration, or structural change) is not finished until its shadow is cast in the Counterpart (rationale, specification, or commemorative record). This symmetry ensures the system's memory (**Mneme**) grows in exact proportion to its mass.

Every formation must maintain a **Logos Layer** (`docs/logos/`) that serves as the Counterpart to its technical implementation. This layer is not "documentation about the code" but the "narrative expression of the formation's existence."

**Implications:**
1. Nature (Implementation) and Counterpart (Record) are a required relationship.
2. A formation without a Logos Layer is a "Ghost" — nature without a record.
3. A formation with a Logos Layer but no Implementation is a "Dream" — a record without nature.
4. The system prohibits both Ghosts and Dreams at PUBLIC_PROCESS and GRADUATED status.
5. The Logos Layer is the bridge to ORGAN-V (Logos) and the public process.

Encoded as: LEX-XI (Symmetry) + validate_logos_layer in `governance-rules.json`.

### Amendment I: Lex Naturalis — Natural Law Foundation
*Source: The recognition that the governance of this system is not invented but derived from the laws of the universe. Two master principles form the deductive substrate: conservation and universal composition. Ratified 2026-03-30.*

The constitution rests on two principles that precede all axioms:

**LEX-I: Conservation.** Nothing can be created or destroyed — only transformed. Every artifact persists in some form. ARCHIVED is not death but transformation. The 200 unheard songs are latent energy, not nothing.

**LEX-II: Universal Composition.** Everything is made from the same materials. A paper and a product are the same substrate differently arranged. The 14 signal classes are the periodic table. Organ boundaries are arrangements, not substances.

From these two principles, eight derived laws govern the system:

| Law | Natural analog | Governs |
|-----|---------------|---------|
| LEX-III Entropy | 2nd Law of Thermodynamics | Maintenance is the cost of existence; unmaintained things decay |
| LEX-IV Metabolism | Biological metabolism | Every formation must transform inputs to outputs or it is dead |
| LEX-V Apoptosis | Programmed cell death | Healthy death serves the organism; ARCHIVED is immune response |
| LEX-VI Selection Pressure | Natural selection | The environment decides what survives via demonstrated reception |
| LEX-VII Homeostasis | Self-regulation | The system self-corrects automatically and continuously |
| LEX-VIII Latent Heat | Phase transition energy | Promotion costs invisible work that must not be dismissed |
| LEX-IX Gravity | General relativity | Mass attracts; flagships pull signal disproportionately |
| LEX-X Catalysis | Chemical catalysis | Formations that enable without producing are judged by what they enable |

Every existing axiom (AX-1 through AX-8) derives from LEX-I and LEX-II. The derivation chains are documented in the `lex_naturalis` section of `governance-rules.json`. The master principles are final and do not change. The derived laws are extensible as the system encounters phenomena they govern.

**Self-similarity (fractal law):** An atom is the smallest unit; as you zoom all the way out, the universe is a massive atom. The system is self-similar at every scale: a formation contains the same structure as an organ, which contains the same structure as the organism. seed.yaml is the genome of a formation; governance-rules.json is the genome of the organism. The tetrad (telos/pragma/praxis/receptio) applies at every level. The polis applies at every level. The natural laws apply at every level. This self-similarity is not designed — it is a consequence of universal composition (LEX-II).

Encoded as: `lex_naturalis` section in `governance-rules.json` (LEX-I through LEX-X + completeness note).

### PROHIB-I: The Inversion Prohibition — Lex Contra Simulacrum
*Source: The observation that recording evolved from serving life to replacing it. Social media as the pathological case. The constitutional obligation to prevent the system from becoming its own social media feed. Ratified 2026-03-30.*

The recording exists to serve the living system — never the reverse.

Pre-historic creation was unrecorded and therefore unrecoverable. The constitutional project (Amendments F through I) built the recording apparatus: signal closure, tetradic self-knowledge, constructed polis, natural law foundation. This apparatus ensures nothing is ever pre-historic again — every formation knows itself, is examined, and persists.

But recording evolved, in human civilization, from serving life to consuming it. Social media is the terminal case: people more concerned with appearing to have a good life than actually having one. The image of the meal replacing the meal. The documentation of the experience replacing the experience.

**This system is vulnerable to exactly this pathology.** 127 repos with exquisite seed.yaml contracts and code that doesn't run. A governance-rules.json at version 3.0 governing formations that have never been used. Constitutional law for a nation of empty buildings. The day the governance is more impressive than what it governs is the day the system has failed.

**PROHIB-I** is the constitutional immune response. Detection heuristics:
- Telos word count vastly exceeding pragma word count (performing life rather than living it)
- Signal edges declared but zero fulfilled (declaration without substance)
- GRADUATED status with null receptio (promoted without evidence of life)
- Polis findings all positive with no adversarial critique (critical society captured by its subject)
- Governance artifacts updated more recently than source code (recording outpacing the living)

Pragma (AX-7) is the specific antidote: the *honest account of what has been concretely realized*, which must always be legible beside the telos. If the pragma is thin and the telos is lush, the formation is performing its existence rather than living it.

Encoded as: PROHIB-I in `governance-rules.json` `lex_naturalis.constitutional_prohibitions`.

### Amendment J: Constitutional Limits — Lex Finis
*Source: Gödel's Incompleteness Theorems, self-organized criticality (Per Bak), and the compression principle from the genetic material ("laws = compressed reality"). The law that limits law. Ratified 2026-03-30.*

Three limits bound the constitution itself:

**LIM-I: Incompleteness.** This constitution will never be complete. That is not a deficiency — it is a mathematical theorem (Gödel, 1931). Every attempt to fully specify governance generates new phenomena the law didn't anticipate. The appropriate response is not more law but better judgment at the boundaries where law runs out.

**LIM-II: Criticality.** Systems operate most productively at the edge of chaos. Too much governance → rigidity → death. Too little → chaos → death. Every law added pushes the system further from chaos but closer to rigidity. The burden of proof is on the law: does this axiom enable more life, or does it constrain life to enable more governance?

**LIM-III: Compression.** All learning is compression. The constitution should be getting shorter over time, not longer. If a new law can be derived from existing principles without explicit statement, it should NOT be added. The remaining latent genetic material (Noether symmetry, emergence, path dependence, energy gradients, carrying capacity) is derivable from LEX-I and LEX-II and does not require separate codification. The final form of this constitution, if it reaches maturity, should be shorter than its first draft.

**Implication for this session:** Amendments F through J were written in a single legislative session. The constitution grew from 6 articles and 5 amendments to 6 articles, 10 amendments, 8 axioms, 7 repo rules, 11 liquid rules, 10 natural laws, 3 limits, 1 prohibition, and 5 genesis documents as genetic material. This was necessary — the genetic material existed pre-constitutionally and needed to be expressed. But LIM-II demands that the next legislative session compress rather than expand. The constitution has spoken extensively. Now it must listen to what it governs.

Encoded as: LIM-I, LIM-II, LIM-III in `governance-rules.json` `lex_naturalis.limits`.

## Post-Launch Reviews

### Review 1 (2026-03-04) — CONSTITUTIO Sprint

**Reviewer:** @4444j99 (AI-conductor review)

**Findings:** All 6 core articles remain valid and enforced. No article requires modification. The constitution successfully governs post-launch operations as written.

| Article | Status | Notes |
|---------|--------|-------|
| I. Registry as SSOT | ACTIVE | repo-registry.json at schema v1.2.0, 149 registry entries tracked |
| II. Unidirectional Deps | ACTIVE | Current V4 report records 1 back-edge requiring remediation; ORGAN-III→VI/VII edges are forward (higher→lower organ flow for community/distribution) |
| III. Eight Organs Visible | SATISFIED | All 8 organs operational since 2026-02-11 |
| IV. Doc Precedes Deploy | ACTIVE | Governs ongoing promotions and new features |
| V. Portfolio-Quality Docs | ACTIVE | Stranger Test not yet executed (omega #2) |
| VI. Promotion State Machine | ACTIVE | 68 CANDIDATE, 12 PUBLIC_PROCESS, 4 GRADUATED |

**Amendments status:** A (completed), B (active), C (completed), D (active), E (active), F (ratified 2026-03-27).

**Next review:** After stranger test execution (omega #2) or at 60-day post-launch mark, whichever comes first.

## Machine-Readable Constitution (Dictums)

The `dictums` section of `governance-rules.json` is the authoritative machine-readable encoding of this constitution's structural laws. It encodes three tiers:

- **Axioms (AX-*):** Universal invariants (AX-1 DAG, AX-2 Epistemic Membranes, AX-3 TTL Eviction, AX-4 Registry Coherence, AX-5 Organ Placement, AX-6 Signal Closure)
- **Organ Dictums (OD-*):** Per-organ constraints (OD-I through OD-VII + OD-META)
- **Repo Rules (RR-*):** Per-repository requirements (RR-1 Seed Contract, RR-2 SRP, RR-3 Event Handshake)

Each dictum declares enforcement mode (`automated`/`audit`/`manual`) and severity (`critical`/`warning`/`info`). Automated dictums are checked by validators in `organvm-engine/governance/dictums.py`.

**CLI commands:**
- `organvm governance dictums` — list all dictums
- `organvm governance dictums --check` — run compliance validators
- `organvm governance dictums --id AX-1` — show specific dictum
- `organvm governance audit` — includes dictum violations in full audit

**MCP tools:**
- `organvm_governance_dictums` — list dictums (optional `level` filter)
- `organvm_governance_check_dictums` — run compliance checks

## Governance

This constitution supersedes ad-hoc decision-making for the organvm project. All specifications (`docs/specs/`) and planning documents must be validated against these articles, amendments, and gates before execution.

Amendments require: (1) documented rationale with source citation, (2) human approval by @4444j99, (3) propagation to all affected documents per the E2G coherence review pattern established in `09-corpus-coherence-review.md`.
