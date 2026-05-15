# Conference Talk Outlines

**Created:** 2026-03-04 (Sprint 67: PRAELECTIO)
**Source:** conference-abstracts.md, conference-proposals/, evidence-portfolio.md
**Purpose:** Slide-by-slide outlines for three 30-minute conference talks
**Status:** DRAFT — ready for rehearsal

---

## Talk 1: The AI-Conductor Model: Building Institutional-Scale Systems Solo

**Format:** 30 minutes + 10 min Q&A
**Target venues:** Strange Loop, XOXO

### Slide-by-Slide Outline

**SECTION 1: THE PROBLEM (5 min)**

**Slide 1 — Title Slide**
- Title: "The AI-Conductor Model: Building Institutional-Scale Systems Solo"
- Subtitle: "What happens when AI is the orchestra and you are the conductor?"
- Name, handle, date
- Visual: conductor silhouette with code streaming from baton

**Slide 2 — The Scale Problem**
- "Institutional scale demands institutional labor"
- Documentation, governance, CI/CD, distribution, community — all need dedicated teams
- Show a list of roles: tech writer, DevOps engineer, PM, marketing, community manager
- Punchline: what if one person needs to fill all of them?

**Slide 3 — The Usual Answer**
- "Just hire someone" / "Just raise funding" / "Just reduce scope"
- Why none of these work for bootstrapped creative practice
- The gap between what one person can write and what a system needs
- A 3,000-word README takes 4-6 hours to write well. You have 113 repos.

**Slide 4 — What I Actually Built**
- 113 repositories, 8 GitHub organizations, 3 weeks
- ~404K+ words of documentation
- 49 published essays
- 4,015+ automated tests, 104 CI/CD workflows
- 6 JSON schemas, 16 ADRs
- Visual: the eight-organ diagram

**SECTION 2: THE MODEL (8 min)**

**Slide 5 — The Metaphor: Conductor, Not Replacement**
- AI is not replacing the developer — it is the orchestra
- The conductor does not play every instrument but controls every sound
- Three phases: DIRECT, GENERATE, REVIEW
- Visual: orchestral diagram with the three phases labeled

**Slide 6 — Phase 1: DIRECT**
- Human provides: architecture, governance design, editorial judgment, quality gates
- Specification-driven development: every deliverable has a spec.md before generation begins
- Example: the four-document governance quadrilateral (roadmap + cadence + catalog + todo)
- "You cannot conduct an orchestra without a score"

**Slide 7 — Phase 2: GENERATE**
- AI generates volume at institutional scale
- Effort metric: Tokens-Expended (TE), not human-hours
- Total budget: ~6.5M TE across 33 sprints
- Token arithmetic: 3,000-word README = ~72K TE (including revisions and validation)
- Live example: generating a README in 15 minutes of human review time

**Slide 8 — Phase 3: REVIEW**
- Human strategic review: accuracy, positioning, voice, portfolio quality
- AI validation: template compliance, link checking, cross-reference verification
- "Every README is a portfolio piece" — written for grant reviewers and hiring managers
- The edit ratio: how much human intervention each generation pass requires

**Slide 9 — TE Budget Model**
- Show the per-task TE table:
  - README REWRITE: ~72K TE
  - README POPULATE: ~88K TE
  - Essay (4,000-5,000 words): ~120K TE
  - Validation pass: ~15K TE
- Phase budgets: Phase 1 = ~4.4M, Phase 2 = ~1.0M, Phase 3 = ~1.1M
- "Tokens are the shooting days of AI-augmented production"

**SECTION 3: THE GOVERNANCE LAYER (7 min)**

**Slide 10 — Why Volume Without Governance = Noise**
- AI can generate 100 READMEs. Without structure, you get 100 indistinguishable documents.
- The governance layer is what transforms volume into a system
- "The registry is more important than any individual repo"

**Slide 11 — Registry-as-JSON**
- `registry-v2.json`: single source of truth for all 113 repos
- Keyed by organ, each containing array of repo objects
- Fields: name, org, status, tier, promotion_status, ci_workflow, revenue_model
- Demo moment: show the actual registry file, scroll through it

**Slide 12 — Dependency Graph & Promotion Pipeline**
- Unidirectional flow: Theory (I) -> Art (II) -> Commerce (III)
- 50 validated cross-organ edges, 0 circular dependencies, 0 back-edge violations
- Five-state promotion: LOCAL -> CANDIDATE -> PUBLIC_PROCESS -> GRADUATED -> ARCHIVED
- Current pipeline: 4 GRADUATED, 29 PUBLIC_PROCESS, 55 CANDIDATE, 6 LOCAL, 54 ARCHIVED
- Visual: the dependency DAG with organ labels

**Slide 13 — Six JSON Schemas**
- registry-v2, seed-v1, governance-rules, dispatch-payload, soak-test, system-metrics
- All at v1.0.0, validated against all live data
- Machine-readable contracts prevent drift as the system scales
- "Schema validation is the immune system"

**SECTION 4: THE FAILURE MODES (5 min)**

**Slide 14 — Failure Mode 1: Hallucinated Code**
- AI-generated README with code examples that look correct, pass CI, but do nothing
- Discovery: manual review during Silver Sprint found plausible-looking but non-functional examples
- Fix: specification-driven templates that require working import paths and test coverage

**Slide 15 — Failure Mode 2: Generic Phrasing**
- When AI writes 60 READMEs in a sprint, they start sounding identical
- "This project provides a robust, scalable solution for..." x60
- Fix: organ-aesthetic.yaml files defining distinct voice per organ
- The VERITAS sprint: found 9 factual errors (lies) in AI-generated data, built audit framework

**Slide 16 — Failure Mode 3: Billing Disasters**
- 48,880 minutes of GitHub Actions CI in one month
- Free tier: 2,000 minutes/month. Overage: real money.
- Solution: disabled 17 workflows, implemented billing guardrails (ADR documented)
- "Automated governance is great until it automates your credit card"

**SECTION 5: THE EVIDENCE (5 min)**

**Slide 17 — The Numbers**
- 33 completed sprints (IGNITION through OPERATIO) in 3 weeks of calendar time
- 12 ORGAN-III products deployed across Netlify/Render
- 32-day zero-incident soak test COMPLETE
- Omega scorecard: 8/17 criteria met
- Custom CLI with 23 command groups, MCP server with 88 tools
- Stakeholder portal LIVE

**Slide 18 — What You Can Steal**
- The AI-conductor model is methodology, not tooling — works with any AI provider
- Three things to adopt today:
  1. Measure effort in tokens, not hours
  2. Build governance before you build features
  3. Treat every document as a portfolio piece
- Open-source governance corpus: github.com/meta-organvm/organvm-corpvs-testamentvm

**Slide 19 — Resources & Links**
- Essay: "The AI-Conductor Model" (public-process essay #9)
- 16 Architecture Decision Records (open source)
- Evidence portfolio with verifiable metrics
- Sprint catalog documenting all 33+ completed sprints
- QR code to the governance corpus

**Slide 20 — Q&A Slide**
- "The AI-conductor model is not about prompt engineering. It is about organizational design."
- Contact info, handles, links
- "Questions?"

### Key Demo Moments

1. **Slide 11:** Open `registry-v2.json` in an editor — scroll through the 113 repos to show real scale. Show a single repo entry with all its fields.
2. **Slide 12:** Show the `organvm` CLI running `organvm registry list --organ ORGAN-I` — live listing of repos with their promotion states.
3. **Slide 7:** Show a terminal with a TE budget calculation — the token arithmetic for generating a README (input tokens + output tokens + revision iterations).
4. **Slide 17:** Run `organvm metrics calculate` or show the system dashboard at localhost:8000 — the omega scorecard in real time.

### Audience Takeaways

1. AI-as-infrastructure is a different paradigm from AI-as-assistant — it requires governance, not just prompts.
2. Token-based effort measurement (TE) is a practical replacement for hour-based estimation in AI-augmented workflows.
3. Governance structures (registries, state machines, dependency graphs) are the difference between AI-generated volume and AI-generated noise.
4. The failure modes of AI-augmented development are predictable, documentable, and solvable — hallucinated code, generic voice, and billing overruns.
5. One person CAN operate at institutional scale, but only with institutional-grade governance infrastructure.

---

## Talk 2: Constraint Alchemy: From Zero Budget to 113 Repositories

**Format:** 30 minutes + 10 min Q&A
**Target venues:** XOXO, IndieWebCamp, Eyebeam

### Slide-by-Slide Outline

**SECTION 1: THE CONSTRAINTS (5 min)**

**Slide 1 — Title Slide**
- Title: "Constraint Alchemy: From Zero Budget to 113 Repositories"
- Subtitle: "How limitations become architecture"
- Name, handle, date
- Visual: alchemical transformation symbol (lead -> gold)

**Slide 2 — Three Constraints**
- $0 budget — GitHub Free tier, no paid services, no database, no cloud compute
- 0 team members — solo operator, every role is yours
- Self-imposed deadline — D-08 launch criterion, 33 sprints in 3 weeks
- "These are the constraints that kill most projects. I decided to build from them."

**Slide 3 — Why These Constraints Are Common**
- Independent artists, solo developers, bootstrapped founders all face these
- The usual advice: "reduce scope" / "find a co-founder" / "apply for funding first"
- The problem with that advice: it treats constraints as obstacles, not materials
- "What if the constraint IS the architecture?"

**Slide 4 — What Emerged**
- 113 repositories, 8 GitHub organizations
- 739K+ words of documentation, 49 published essays
- 4,015+ tests, 104 CI/CD workflows, 6 JSON schemas
- Constitutional governance framework with 6 articles + 5 amendments
- All on free-tier infrastructure, zero employees, three weeks of calendar time

**SECTION 2: FIVE TECHNIQUES (12 min)**

**Slide 5 — Technique 1: Inverse Design**
- Build FROM the constraint, not DESPITE it
- "No database budget" does not mean "find a cheaper database"
- It means: "What if the entire system runs on a single JSON file?"
- `registry-v2.json`: 2,400+ lines, 113 repos, zero infrastructure cost
- Demo moment: show the registry file — a JSON file that IS the database
- "The constraint eliminated an entire class of operational complexity"

**Slide 6 — Technique 2: Temporal Compression**
- Deadlines as creative accelerants, not stress generators
- 33 named sprints in 3 weeks through AI-conductor methodology
- Each sprint has a Latin name, a spec.md, a checklist, and a TE budget
- Example sprint timeline: IGNITION (day 1) through OPERATIO (day 21)
- "Film productions budget shooting days. I budget tokens."

**Slide 7 — Technique 3: Minimum Viable Governance**
- The governance quadrilateral: 4 documents that prevent chaos without creating bureaucracy
  1. Roadmap (`there+back-again.md`) — 17 omega criteria across 5 horizons
  2. Sprint catalog — 76 named sprints across 18 categories
  3. Operational cadence — 7 anti-patterns to avoid
  4. Rolling TODO — prioritized work queue with invocation IDs
- "Governance is not bureaucracy. Governance is what lets you sleep at night."

**Slide 8 — Technique 4: Autonomous Amplification**
- Systems that generate their own content and distribution pipeline
- Essay published -> essay-monitor detects -> POSSE distribution fires -> social channels update
- 49 essays published with automated cross-posting
- 23 kerygma profiles mapping products to distribution channels
- "The system amplifies itself — I just conduct"

**Slide 9 — Technique 5: Portfolio-as-Proof**
- Process documentation IS the primary deliverable
- The 49 essays about building the system ARE the system's most visible output
- Grant reviewers and hiring managers see methodology, not just artifacts
- The governance corpus (~404K+ words) is evidence of capability
- "Documenting the building is building"

**SECTION 3: THE DECISIONS (8 min)**

**Slide 10 — ADR Tour: Architecture Decisions Under Constraint**
- 16 Architecture Decision Records, each tracing a constraint to a decision
- ADR format: context -> constraint -> decision -> consequences
- Walk through 3 representative ADRs:
  - Why JSON over database (cost constraint -> zero-infra design)
  - Why 8 orgs instead of 1 monorepo (governance constraint -> isolation)
  - Why Latin sprint names (identity constraint -> memorable, unique, searchable)

**Slide 11 — The Billing Disaster**
- 48,880 minutes of GitHub Actions CI in one month
- Free tier limit: 2,000 minutes. That is a 24x overage.
- Root cause: 104 workflows running on every push across 148 repos
- Decision: disabled 17 non-critical workflows, added billing guardrails
- "Constraints you forget about come back as invoices"

**Slide 12 — Revenue Honesty**
- Revenue status across all 28 ORGAN-III products: zero
- Published openly in registry, evidence portfolio, grant applications
- Counterintuitive result: honest zeros built MORE credibility with reviewers than projected numbers
- Omega criterion #9 (revenue live) and #10 (MRR >= costs) — transparently unmet
- "Honesty about constraints is itself a constraint technique"

**Slide 13 — The VERITAS Sprint**
- Sprint 23: found 9 factual errors in AI-generated data
- Lies in documentation: inflated numbers, future-dated achievements, phantom features
- Response: built an entire audit framework — validation scripts, cross-reference checks
- 5 validation scripts now run in CI against all data contracts
- "When your orchestra plays wrong notes, you do not fire the musicians. You fix the score."

**SECTION 4: WHAT YOU CAN TAKE HOME (5 min)**

**Slide 14 — The Constraint-to-Architecture Pipeline**
- Step 1: Name the constraint explicitly (not "limited resources" — "$0 and 1 person")
- Step 2: Invert it (what does the constraint make POSSIBLE, not impossible?)
- Step 3: Design from the inversion (the architecture IS the constraint)
- Step 4: Document the decision (ADR format: context, constraint, decision, consequences)
- Step 5: Validate the decision survived contact with reality

**Slide 15 — Three Questions for Your Constraints**
1. "What class of problems does this constraint ELIMINATE?" (no database = no database operations)
2. "What would I build if this constraint were permanent?" (not a workaround — a design)
3. "Is this constraint honest?" (if you are hiding revenue numbers, the constraint is dishonesty)

**Slide 16 — The Deeper Point**
- "Constraints do not just shape what you build. They shape what you become."
- The governance structures designed for zero-budget survival are MORE interesting than the artifacts
- The constraint became the medium. The limitation became the architecture.
- This talk is itself a constraint artifact: 30 minutes, one speaker, no live demos with sound

**Slide 17 — Resources**
- Essay: "Constraint Alchemy: How Limitations Become Creative Fuel" (published 2026-02-17)
- ADRs 001-016 (open source)
- Full governance corpus with all 33 sprint specs
- Evidence portfolio with verifiable metrics
- QR code to github.com/meta-organvm/organvm-corpvs-testamentvm

**Slide 18 — Q&A Slide**
- "The constraint is the medium. The limitation is the architecture."
- Contact info, handles, links
- "Questions?"

### Key Demo Moments

1. **Slide 5:** Open `registry-v2.json` and show it as the "database" — a single JSON file serving the function of an entire data layer. Scroll to show scale (2,400+ lines, 113 repos).
2. **Slide 7:** Show the four governance quadrilateral documents side by side in split panes — roadmap, catalog, cadence, rolling TODO.
3. **Slide 10:** Open an actual ADR file and walk through the constraint -> decision -> consequences format.
4. **Slide 13:** Run `organvm registry validate` to show the validation scripts catching errors in real time.

### Audience Takeaways

1. Constraints are design materials, not obstacles — "inverse design" means building FROM the constraint, not around it.
2. The constraint-to-architecture pipeline (name, invert, design, document, validate) is a repeatable methodology you can apply to any constrained creative practice.
3. Minimum viable governance (four documents) prevents chaos without creating bureaucracy — you do not need enterprise tooling to operate at scale.
4. Honest documentation of failures and constraints (billing disasters, revenue zeros, AI-generated lies) builds more credibility than polished success stories.
5. "Portfolio-as-proof" turns process documentation into the deliverable itself — the building is the art.

---

## Talk 3: Eight Organs: Creative Practice as Systems Architecture

**Format:** 30 minutes + 10 min Q&A
**Target venues:** Processing Community Day, Eyebeam

### Slide-by-Slide Outline

**SECTION 1: THE QUESTION (4 min)**

**Slide 1 — Title Slide**
- Title: "Eight Organs: Creative Practice as Systems Architecture"
- Subtitle: "What happens when you model creative practice as a distributed system?"
- Name, handle, date
- Visual: eight-organ diagram with flowing connections

**Slide 2 — The Premise**
- Most artists work in one domain. Most architects build one product.
- What if you designed creative practice as a distributed system with formal dependencies?
- Not a portfolio of projects — an organism with organs
- "The architecture decisions that shape it are indistinguishable from the artistic decisions"

**Slide 3 — Reference Points**
- Julian Oliver's Critical Engineering Manifesto — engineering as critical practice
- Nicky Case's Explorable Explanations — systems thinking as creative medium
- Hundred Rabbits' radical transparency — process documentation as art
- Sol LeWitt's wall drawings — instruction-based art, system as work
- "I am not the first to treat systems as medium. I may be the first to run 113 repos to do it."

**SECTION 2: THE EIGHT ORGANS (10 min)**

**Slide 4 — The Organ Map**
- Full diagram showing all 8 organs with names, domains, and repo counts:
  - I: Theoria (Theory) — 20 repos — epistemology, recursion, ontology
  - II: Poiesis (Art) — 31 repos — generative art, performance, experiential
  - III: Ergon (Commerce) — 28 repos — SaaS, B2B, B2C products
  - IV: Taxis (Orchestration) — 7 repos — governance, routing, AI agents
  - V: Logos (Discourse) — 6 repos — essays, public process, analytics
  - VI: Koinonia (Community) — 6 repos — salons, reading groups, learning
  - VII: Kerygma (Distribution) — 6 repos — POSSE, social automation
  - VIII: Meta — 8 repos — governance of governors, schemas, dashboard

**Slide 5 — The Dependency Graph**
- Unidirectional flow: I -> II -> III (enforced, zero violations)
- IV orchestrates all organs
- V observes (read-many, write-one)
- VII is pure consumer (receives, never produces upstream)
- VIII governs the governors
- 50 validated cross-organ edges, 0 circular dependencies
- Visual: DAG with color-coded organs and edge arrows
- "This is a compositional constraint, like a harmonic rule in music"

**Slide 6 — Organ I: Theoria (Theory)**
- Epistemological frameworks, recursive engines, symbolic computing
- Flagship: recursive-engine--generative-entity
- Produces: theoretical frameworks, ontological schemas, recursive patterns
- These are not academic papers — they are executable specifications
- "Theory is the root note of every chord the system plays"

**Slide 7 — Organ II: Poiesis (Art)**
- Generative art, performance systems, creative coding, experiential media
- Flagships: metasystem-master, a-mavs-olevm
- Consumes theoretical frameworks from ORGAN-I, transforms them into artworks
- Demo moment: show a generative art piece from ORGAN-II repos
- "Art is what theory looks like when it encounters a canvas"

**Slide 8 — Organ III: Ergon (Commerce)**
- 28 SaaS, B2B, and B2C products
- 12 deployed across Netlify/Render
- Revenue status: honestly zero (documented)
- Consumes art and frameworks, packages them as products
- "Commerce is not a betrayal of art. It is the third transformation."

**Slide 9 — Organs IV-VII: The Infrastructure**
- IV (Taxis): orchestration, governance rules, AI agent skills, dependency validation
- V (Logos): 49 published essays documenting the building process in real time
- VI (Koinonia): community infrastructure — salons, reading groups, taxonomy
- VII (Kerygma): POSSE distribution pipeline, 23 kerygma profiles
- "These organs do not make things. They make the making possible."

**Slide 10 — Organ VIII: Meta**
- The governance corpus (~404K+ words), the registry, the schemas
- Custom CLI (`organvm` — 23 command groups)
- MCP server (88 tools) exposing the system graph to AI sessions
- System dashboard with dependency visualization
- "Meta governs the governors. It is the organ that watches all other organs."

**SECTION 3: THE ARCHITECTURE AS ART (8 min)**

**Slide 11 — organ-aesthetic.yaml: Identity Cascades**
- Each organ has a defined aesthetic identity: palette, typography, tone, layout patterns
- Visual identity is a first-class architectural concern, not an afterthought
- Show two organ-aesthetic.yaml files side by side — Theory (austere, monospace) vs Art (vibrant, fluid)
- "The dependency graph shapes what emerges. The aesthetic.yaml shapes how it looks."

**Slide 12 — Promotion as Curation**
- Five-state pipeline: LOCAL -> CANDIDATE -> PUBLIC_PROCESS -> GRADUATED -> ARCHIVED
- Current state: 4 GRADUATED, 29 PUBLIC_PROCESS, 55 CANDIDATE, 6 LOCAL, 54 ARCHIVED
- The same pipeline applies to a philosophical framework AND a commercial web scraper
- Promotion criteria: CI workflow + platinum status + active implementation
- "Curation is not just selection. It is a state machine."

**Slide 13 — Seed.yaml: The Automation Contract**
- Every repo has a `seed.yaml` declaring organ membership, tier, edges, event subscriptions
- Machine-readable dependency graph built from seed files
- The system can validate its own structural integrity
- Demo moment: show `organvm seed graph` — the full cross-organ dependency visualization

**Slide 14 — The Pipeline: Theory to Art to Product**
- Walk through one complete transformation:
  - ORGAN-I: recursive-engine--generative-entity produces a recursive pattern framework
  - ORGAN-II: metasystem-master consumes it, generates visual artworks
  - ORGAN-III: a product packages the generative output for end users
  - ORGAN-V: an essay documents the transformation
  - ORGAN-VII: distribution pipeline pushes the essay to social channels
- "The dependency graph is the creative process. Following the edges IS the methodology."

**SECTION 4: SYSTEMS AS MEDIUM (8 min)**

**Slide 15 — Architecture Decisions ARE Artistic Decisions**
- Why 8 organs instead of 5 or 12? (the number creates a specific compositional space)
- Why unidirectional flow? (constraint as harmonic rule — limits generate surprise)
- Why Latin names? (language creates identity, identity creates commitment)
- Why publish revenue zeros? (transparency is an aesthetic choice)
- "Every ADR is also a manifesto"

**Slide 16 — The Dependency Graph as Compositional Constraint**
- Musical analogy: harmonic rules do not limit composition — they enable it
- The I->II->III flow means Theory must be complete before Art can transform it
- This is not a limitation — it is a generative principle
- Zero back-edge violations is not just engineering discipline — it is artistic discipline
- "The constraint shapes what WANTS to emerge"

**Slide 17 — What This Is Not**
- Not a portfolio (portfolios are collections; this is an organism)
- Not a monorepo (103 independent repos with formal governance)
- Not a framework (you cannot install it; you can only study and adapt the model)
- Not finished (omega scorecard: 8/17 criteria met — the system is alive and growing)
- "It is a creative practice that happens to look like systems architecture"

**Slide 18 — The Organ Model as Creative Methodology**
- You do not need 113 repos — you need the thinking behind them
- Design your practice as organs with dependencies, not projects in a folder
- Ask: what produces, what transforms, what distributes, what governs?
- The four questions that define any creative system:
  1. Where does raw material enter? (ORGAN-I)
  2. Where does transformation happen? (ORGAN-II)
  3. Where does value exit? (ORGAN-III)
  4. What keeps it honest? (ORGAN-VIII)

**Slide 19 — Resources**
- Full governance corpus: github.com/meta-organvm/organvm-corpvs-testamentvm
- Interactive portfolio with generative art: 4444j99.github.io/portfolio/
- 49 Public Process essays: organvm-v-logos.github.io/public-process/
- Evidence portfolio with verifiable metrics
- QR code to the governance corpus

**Slide 20 — Q&A Slide**
- "Systems architecture is creative practice. Creative practice is systems architecture."
- Contact info, handles, links
- "Questions?"

### Key Demo Moments

1. **Slide 5:** Run `organvm seed graph` or show the system dashboard dependency graph — the full DAG with all 50 edges, color-coded by organ.
2. **Slide 7:** Show a running generative art piece from an ORGAN-II repo (if audio is available) or a screenshot/recording of one.
3. **Slide 11:** Show two `organ-aesthetic.yaml` files side by side — contrast the visual identity definitions between Theory and Art organs.
4. **Slide 13:** Run `organvm seed validate` — show the system verifying its own structural integrity across 148 repos.
5. **Slide 14:** Walk through the dependency graph in the dashboard, clicking from ORGAN-I -> ORGAN-II -> ORGAN-III to trace one transformation pipeline.

### Audience Takeaways

1. Creative practice can be modeled as a distributed system with formal dependencies — the architecture IS the artistic methodology.
2. Unidirectional dependency flow (Theory -> Art -> Commerce) is a compositional constraint, not an engineering limitation — like harmonic rules in music, it shapes what emerges.
3. The same governance infrastructure (registries, promotion pipelines, schema validation) applies equally to philosophical frameworks and commercial products.
4. The four-question model (where does material enter, where does transformation happen, where does value exit, what keeps it honest) can structure any creative practice, at any scale.
5. Treating systems architecture as medium — not just tooling — opens a creative space where every ADR is also a manifesto and every dependency edge is also an artistic decision.

---

## Cross-Talk Reference: Shared Metrics

These metrics appear across all three talks and should be kept consistent. Source: evidence-portfolio.md.

| Metric | Value | Source |
|--------|-------|--------|
| Total repositories | 148 | registry-v2.json |
| GitHub organizations | 8 | registry-v2.json |
| Documentation volume | ~404K+ words | system metrics |
| Published essays | 29 | ORGAN-V public-process |
| Automated tests | 4,015+ | CI aggregation |
| CI/CD workflows | 107+ | registry-v2.json |
| JSON schemas | 6 (all v1.0.0) | schema-definitions |
| ADRs | 16 | docs/adr/ |
| Completed sprints | 33 | sprint catalog |
| Cross-organ edges | 50 (0 violations) | seed graph |
| Promotion: GRADUATED | 4 | registry |
| Promotion: PUBLIC_PROCESS | 29 | registry |
| Promotion: CANDIDATE | 55 | registry |
| Products deployed | 12 | Netlify/Render |
| Total TE budget | ~6.5M tokens | implementation-package-v2 |
| CI billing incident | 48,880 minutes | ADR |
| Omega scorecard | 8/17 met | omega evidence map |
| CLI command groups | 23 | organvm-engine |
| MCP server tools | 88 | organvm-mcp-server |
| Kerygma profiles | 23 | ORGAN-VII |

## Adaptation Notes

### Lightning Talk (10 min)
- Use slides 1, 4, 5-6 (model), 10 (governance), 14-15 (failure), 18 (takeaways) from Talk 1
- Focus on the conductor metaphor and one failure mode
- End with the three things to adopt today

### Workshop (90-120 min)
- Talk 1 workshop: TE budgeting exercise — participants estimate token costs for their own projects
- Talk 2 workshop: constraint mapping — participants name their constraints, apply inverse design
- Talk 3 workshop: organ model design — participants sketch their practice as organs with dependencies

### Panel / Fireside Chat
- Lead with the VERITAS sprint story (finding lies in your own AI-generated data)
- Revenue honesty angle plays well in indie/bootstrap contexts
- The "governance for one person" paradox generates good discussion
