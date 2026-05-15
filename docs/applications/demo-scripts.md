# ORGANVM Demo Scripts

Three demonstration scenarios for external audiences — grant panels, residency
interviews, portfolio reviews, and conference presentations. Each is designed to
be performed live at a terminal or pre-recorded as a screencast.

**Prerequisites:** Activate the workspace venv (`source .venv/bin/activate` from
`meta-organvm/`). All commands are run from the `meta-organvm/` directory unless
otherwise noted.

**Last verified:** 2026-03-04

---

## Demo 1: "The Living System" (5 minutes)

**Audience:** Grant panels, portfolio reviewers, anyone evaluating system scope.
**Goal:** Establish that this is a real, operational system — not a spec document
or a folder of side projects. Show that 148 repositories across 8 organs are
running, monitored, and governed by a unified CLI.

### Script

#### Beat 1 — System Health (60 seconds)

```bash
organvm status
```

**Expected output:**

```
  ORGANVM System Pulse
  ══════════════════════════════════════════════════

  Organs (8/8 operational)
  ──────────────────────────────────────────────────
    ORGAN-I             20 repos  (Theory)
    ORGAN-II            30 repos  (Art)
    ORGAN-III           27 repos  (Commerce)
    ORGAN-IV             7 repos  (Orchestration)
    ORGAN-V              2 repos  (Public Process)
    ORGAN-VI             6 repos  (Community)
    ORGAN-VII            4 repos  (Marketing)
    META-ORGANVM         7 repos  (Meta)
    ────────────────────────────────────────
    Total              103 repos  (94 active)

  Soak Test (VIGILIA)
  ──────────────────────────────────────────────────
    Streak:    17/30 days  56%
    Remaining: 13 days

  Omega Score
  ──────────────────────────────────────────────────
    4/17 MET (23%), 3 in progress

  Infrastructure
  ──────────────────────────────────────────────────
    CI workflows:  94
    Dep edges:     43
```

**Talking points:**
- "This is the entire system in one command. Eight organs, 103 repositories, all
  managed by a single person using AI as a force multiplier."
- "The soak test is a 30-day stability trial — the system has to run
  autonomously with zero critical incidents. We are 17 days in."
- "92 active repos, each with CI, a `seed.yaml` automation contract, and a
  registry entry."

**Transition cue:** "That summary shows the heartbeat. Let me show you what the
system is actually working toward."

#### Beat 2 — Omega Scorecard (60 seconds)

```bash
organvm omega status
```

**Expected output:**

```
Omega Scorecard: 4/17 MET
────────────────────────────────────────────────────────────
  ▪ #1   30-day soak test passes (≤3 incidents)        IN_PROGRESS
  □ #2   Stranger test score ≥80%                      NOT_MET
  ▪ #3   Engagement baseline (30 days of data)         IN_PROGRESS
  □ #4   Runbooks validated by second operator         NOT_MET
  ■ #5   ≥1 application submitted                      MET
  ■ #6   AI-conductor essay published                  MET
  □ #7   ≥3 external feedback collected                NOT_MET
  ■ #8   ≥1 ORGAN-III product live                     MET
  □ #9   revenue_status: live for ≥1 entry             NOT_MET
  □ #10  MRR ≥ system operating costs                  NOT_MET
  □ #11  ≥2 salons/events with external participants   NOT_MET
  □ #12  ≥3 external contributions                     NOT_MET
  ■ #13  ≥1 organic inbound link                       MET
  □ #14  ≥1 recognition event                          NOT_MET
  □ #15  Portfolio updated with validation             NOT_MET
  □ #16  Bus factor >1 (validated)                     NOT_MET
  ▪ #17  System operates 30+ days autonomously         IN_PROGRESS
────────────────────────────────────────────────────────────
  4 MET, 3 IN PROGRESS, 10 NOT MET
```

**Talking points:**
- "Omega is the graduation protocol — 17 criteria the system must satisfy before
  it can be considered complete. This is not a checkbox exercise; these are
  externally verifiable conditions."
- "Four are met: a submitted application, a published essay on AI-conductor
  methodology, a live product, and organic external recognition."
- "Three more are in progress, including the 30-day soak test. Ten remain open.
  The system is honest about what it has not achieved."

**Transition cue:** "What kind of products does this system produce? Let me show
you the commercial arm."

#### Beat 3 — Product Inventory (60 seconds)

```bash
organvm registry list --organ ORGAN-III
```

**Expected output (abbreviated):**

```
  Name                                    Organ       Status    Tier
  ────────────────────────────────────────────────────────────────────
  classroom-rpg-aetheria                ORGAN-III   ACTIVE    standard
  gamified-coach-interface              ORGAN-III   ACTIVE    standard
  trade-perpetual-future                ORGAN-III   ACTIVE    standard
  public-record-data-scrapper           ORGAN-III   ACTIVE    flagship
  search-local--happy-hour              ORGAN-III   ACTIVE    standard
  the-invisible-ledger                  ORGAN-III   ACTIVE    standard
  ...
  25 repo(s)
```

**Talking points:**
- "ORGAN-III is the commercial arm — 27 repositories ranging from a flagship
  50-state public records platform to social apps, game engines, and developer
  tools."
- "12 of these are live and deployed — you can visit them right now."
- "Each has a `seed.yaml` declaring its dependencies, event subscriptions, and
  automation triggers. This is not a portfolio of side projects — it is a
  managed product catalog."

**Transition cue:** "Are these just repos, or do they have live deployments?"

#### Beat 4 — Live Deployments (60 seconds)

Navigate to deployed URLs. Open a browser or use `curl -sI` to prove liveness.

```bash
# Flagship ORGAN-III product
curl -sI https://public-record-data-scrapper.netlify.app | head -3

# ORGAN-V essay platform
curl -sI https://public-process.netlify.app | head -3

# ORGAN-VI community hub
curl -sI https://community-hub-8p8t.onrender.com | head -3
```

**Expected output (per URL):**

```
HTTP/2 200
...
```

**Talking points:**
- "Three different organs, three live deployments. The flagship product, the
  essay platform, and the community hub."
- "These are not mockups. HTTP 200 — they are running."
- "Across ORGAN-III alone, there are deployments on Netlify, Cloudflare Pages,
  GitHub Pages, and Render."

**Deployed URLs to have ready for browser demo:**

| Product | URL |
|---------|-----|
| Public Record Data Scrapper (ORGAN-III flagship) | https://public-record-data-scrapper.netlify.app |
| Gamified Coach Interface | https://gamified-coach-interface.pages.dev |
| The Actual News | https://the-actual-news.pages.dev |
| Hokage Chess | https://organvm-iii-ergon.github.io/hokage-chess/ |
| Public Process essays (ORGAN-V) | https://public-process.netlify.app |
| Community Hub (ORGAN-VI) | https://community-hub-8p8t.onrender.com |
| A-MAVS-OLEVM (ORGAN-II art) | https://etceter4.netlify.app |

**Transition cue:** "That is the surface. Let me show you how all of this is
actually governed."

#### Beat 5 — Governance Audit (60 seconds)

```bash
organvm governance audit
```

**Expected output (abbreviated):**

```
Governance Audit Report
========================================

WARNINGS (24):
  ORGAN-I/.github: no CI workflow
  ORGAN-I/.github: not platinum (missing CHANGELOG/ADRs)
  ORGAN-II/chthon-oneiros: not platinum (missing CHANGELOG/ADRs)
  ...

INFO (1):
  Dependency graph: 43 edges, 10 cross-organ directions

Result: PASS
```

**Talking points:**
- "The governance audit checks every repo against the system's own rules — CI
  presence, platinum status, dependency compliance."
- "24 warnings, zero violations. The warnings are infrastructure repos and
  archive entries that intentionally have relaxed requirements."
- "Result: PASS. The system polices itself."

**Closing line:** "This is not a portfolio. It is an operational institution with
103 repositories, 94 CI pipelines, 8 organs, and a 17-criteria graduation
protocol — run by one person with AI as the conductor."

---

## Demo 2: "The Conductor Model" (10 minutes)

**Audience:** Technical reviewers, AI practitioners, engineering managers,
conference audiences interested in human-AI collaboration.
**Goal:** Show how the AI-conductor workflow operates: seed.yaml contracts,
governance enforcement, automated metrics, and the essay publishing pipeline.

### Script

#### Beat 1 — The seed.yaml Contract System (2 minutes)

Start by showing what a seed.yaml looks like — the automation contract every
repo must carry.

```bash
cat ~/Workspace/organvm-i-theoria/recursive-engine--generative-entity/seed.yaml
```

**Expected output:**

```yaml
schema_version: "1.0"
organ: I
organ_name: Theory
repo: recursive-engine--generative-entity
org: organvm-i-theoria

metadata:
  implementation_status: ACTIVE
  tier: flagship
  promotion_status: PUBLIC_PROCESS
  last_validated: "2026-02-11"
  generated: "2026-02-17"
  sprint: "SENSORIA"
  language: python

agents:
  - name: ci
    trigger: on_push
    workflow: .github/workflows/ci-python.yml
    description: "Continuous integration pipeline"

produces:
  - type: theory
    description: "Epistemological frameworks, recursive engines, ontological systems"

consumes: []

subscriptions:
  - event: governance.updated
    source: ORGAN-IV
    action: Check compliance with updated governance rules
  - event: health-audit.completed
    source: ORGAN-IV
    action: Review audit findings for this repo
```

**Talking points:**
- "Every repo in the system carries a `seed.yaml`. This is its contract — it
  declares which organ it belongs to, what it produces, what it consumes, and
  what events it subscribes to."
- "This is the flagship of ORGAN-I: RE:GE, a symbolic operating system for
  myth, identity, and recursive systems. 1,254 tests, 85% coverage, pure Python."
- "The `produces` field declares that it outputs theory. The `subscriptions`
  field says it reacts to governance updates from ORGAN-IV."
- "There is no implicit wiring. Every connection in this system is declared in a
  `seed.yaml` and validated by the engine."

**Transition cue:** "What happens when the system validates all these contracts
at once?"

```bash
organvm seed validate 2>&1 | head -25
```

**Expected output (abbreviated):**

```
  PASS meta-organvm/.github
  PASS meta-organvm/alchemia-ingestvm
  PASS meta-organvm/organvm-corpvs-testamentvm
  PASS meta-organvm/organvm-engine
  ...
  110 seeds found, 107 PASS, 3 FAIL
```

**Talking points:**
- "110 seed files across the workspace. 107 pass. The 3 failures are archived
  repos with legacy YAML formatting — the system does not sweep problems under
  the rug."
- "Each PASS means: the seed declares a valid organ, has required metadata
  fields, and declares its agents, produces, and consumes edges correctly."

**Transition cue:** "Seeds declare connections. But who enforces that those
connections are legal?"

#### Beat 2 — Governance Rules Enforcement (2 minutes)

```bash
organvm governance check-deps
```

**Expected output:**

```
Dependency Graph Validation
────────────────────────────────────────
  Total edges: 43
  Missing targets: 7
  Self-dependencies: 0
  Back-edges: 0
  Cycles: 0

  Cross-organ directions:
    organvm-ii-poiesis -> organvm-i-theoria: 3
    organvm-iv-taxis -> organvm-i-theoria: 2
    organvm-v-logos -> organvm-i-theoria: 1
    organvm-v-logos -> organvm-ii-poiesis: 1
    organvm-v-logos -> organvm-iii-ergon: 1
    organvm-v-logos -> organvm-iv-taxis: 1
    ...

  Violations:
    Missing target: organvm-vi-koinonia/community-hub -> koinonia-db
    ...

  Result: FAIL
```

**Talking points:**
- "62 dependency edges across the system. Zero back-edges. Zero cycles. The
  unidirectional flow — I to II to III — is not aspirational. It is enforced."
- "The core rule: theory flows to art, art informs products. No back-edges.
  ORGAN-IV orchestrates everything. ORGAN-V observes. ORGAN-VII distributes."
- "The 7 missing targets are newly wired community repos referencing targets not
  yet registered. The system does not let this slide — it reports FAIL until
  those targets exist."
- "This is what AI-conductor means: the human designs the rules, the AI applies
  them at scale, and the machine catches violations the human would miss."

**Transition cue:** "Rules are half the story. The other half is knowing what
breaks when something changes."

```bash
organvm governance impact recursive-engine--generative-entity
```

**Expected output:**

```
Impact Analysis for: recursive-engine--generative-entity
  18 repositories affected:
    - metasystem-master
    - cognitive-archaelogy-tribunal
    - public-process
    - agentic-titan
    - performance-sdk
    ...

  Propagation Path:
      ↳ metasystem-master
      ↳ cognitive-archaelogy-tribunal
      ↳ public-process
      ↳ reverse-engine-recursive-run
      ↳ agentic-titan
        ↳ docs
        ↳ performance-sdk
        ↳ agent--claude-smith
          ↳ a-i--skills
```

**Talking points:**
- "Before touching the flagship, you ask: what breaks? 18 repositories are
  affected — across ORGAN-I, ORGAN-II, ORGAN-IV, and ORGAN-V."
- "The blast radius is not guesswork. The engine traces the dependency graph and
  shows every downstream consumer."
- "This is how you govern 103 repos with one person: you make the machine tell
  you what breaks before you break it."

**Transition cue:** "Governance catches violations. But who maintains the
numbers?"

#### Beat 3 — Automated Metrics Pipeline (2 minutes)

```bash
organvm metrics calculate
```

**Expected output:**

```
Metrics written to .../organvm-corpvs-testamentvm/system-metrics.json
  Repos: 103 (92 ACTIVE)
  Organs: 8/8 operational
  CI: 94
  Dependencies: 43 edges
  Words: 841K+ (readmes=278,373, essays=142,281, corpus=414,198, profiles=6,031)
```

**Talking points:**
- "One command computes the entire system's metrics: repo count, CI coverage,
  dependency edges, word count across all documentation."
- "404,000+ words of documentation. 278K in READMEs alone. All generated through
  the AI-conductor model — AI writes, human reviews and edits."
- "These numbers are not manually tracked. They are computed from the actual
  workspace state every time you run the command."

Now show that metrics propagate into documentation files:

```bash
organvm metrics refresh --dry-run 2>&1 | head -15
```

**Expected output:**

```
DRY RUN — no files will be modified
  Would update: organvm-corpvs-testamentvm/docs/genesis/00-c-master-summary.md
  Would update: organvm-corpvs-testamentvm/registry-v2.json
  ...
```

**Talking points:**
- "The `refresh` command calculates metrics and then propagates them into every
  document that references system numbers — the master summary, the registry,
  the README files."
- "No manual find-and-replace. One command updates every occurrence of
  '103 repositories' or '~404K+ words' across the entire corpus."
- "This is the conductor model in action: the system maintains its own
  documentation."

**Transition cue:** "The final piece of the conductor model is the public
record."

#### Beat 4 — The Essay Publishing Pipeline (2 minutes)

```bash
organvm registry show public-process
```

**Expected output:**

```
  public-process
  ────────────────────────────────────────
  Organ:       ORGAN-V
  description:        Essays, case studies, methodology documentation, RSS feed,
                      newsletter integration
  portfolio_relevance:CRITICAL - Primary narrative layer describing all 8 organs
  launch_content:     Essay 1: How We Orchestrate Eight Organs Across ~44
                      GitHub Repositories, Essay 2: Theory + Commerce + Art...
  deployment_url:     https://public-process.netlify.app
```

**Talking points:**
- "ORGAN-V is the public disclosure layer. Everything the system does is
  documented in essays deployed to this Netlify site."
- "There are 29 meta-system essays plus 4 additional essays — over 404,000+ words
  of published writing about methodology, governance, and creative systems."
- "The essay topics come from the implementation plan. Each essay is specified
  in a sprint, generated via the conductor model, reviewed, and deployed."

Open in browser:

```bash
open https://public-process.netlify.app
```

**Talking points:**
- "This is the live site. RSS feed, newsletter-ready, each essay 3,000-5,000
  words."
- "Essay #6 — 'AI-Conductor Essay' — is the one that satisfies omega criterion
  #6. It is about this exact methodology."

**Transition cue:** "Now let me show you the pitch deck system that ties all
of this together."

#### Beat 5 — Pitch Deck Generation (2 minutes)

```bash
organvm pitch sync --help
```

**Expected output:**

```
usage: organvm pitch sync [-h] [--organ ORGAN] [--dry-run]
```

**Talking points:**
- "The pitch command generates HTML pitch decks for every repo in the system.
  83 decks were generated in a single sprint."
- "Each deck pulls from the registry entry, the seed.yaml, and the README to
  create a consistent presentation."
- "This is the final link: theory to art to product to essay to pitch deck.
  The conductor model generates the entire pipeline."

Show the upcoming deadlines to demonstrate operational cadence:

```bash
organvm deadlines
```

**Expected output:**

```
  Upcoming Deadlines (next 30 days)
  ════════════════════════════════════════════════════════════
  ID         Date           Days     Urgency      Description
  ────────────────────────────────────────────────────────────
  F4          2026-03-06       2d    THIS WEEK    Research and submit NEH...
  F14         2026-03-15      11d    SOON         Apply Bread Loaf Writers...
  E3          2026-03-18      14d    SOON         Submit Google Creative...
  ...
  6 deadline(s) shown (13 total)
```

**Talking points:**
- "The system tracks application deadlines. 13 total, 6 within the next 30
  days."
- "Each deadline has a concordance ID — F4, F14, E3 — that maps to a full
  specification in the governance corpus."
- "This is an institution, not a person. Institutions have calendars, deadlines,
  and accountability."

**Closing line:** "The conductor model is human direction, AI execution, machine
verification. The human designs the architecture and reviews the output. The AI
generates 404,000+ words of documentation, 94 CI pipelines, and 83 pitch decks.
The machine enforces 62 dependency edges, 17 graduation criteria, and a 30-day
soak test."

---

## Demo 3: "From Theory to Product" (15 minutes)

**Audience:** Residency interviews, academic panels, anyone evaluating the
creative-institutional model as a whole. This is the comprehensive demo that
traces a single intellectual thread from abstract epistemological theory through
generative art to a deployed commercial product with revenue readiness.

### Script

#### Beat 1 — The Theory Layer (3 minutes)

Start with the system overview, then zoom into a specific ORGAN-I repo.

```bash
organvm status
```

**Talking point (brief):** "Eight organs. 103 repos. Let me show you how a
single idea flows through this system."

```bash
organvm registry show auto-revision-epistemic-engine
```

**Expected output:**

```
  auto-revision-epistemic-engine
  ────────────────────────────────────────
  Organ:       ORGAN-I
  org:                organvm-i-theoria
  status:             ACTIVE
  description:        Self-governing orchestration framework with 8 phases,
                      4 human review gates, BLAKE3 audit chain, and ethical
                      axiom enforcement
  promotion_status:   PUBLIC_PROCESS
  tier:               standard
  ci_workflow:        ci-python.yml
  platinum_status:    True
  promotion_obligations: target_name: art-from--auto-revision-epistemic-engine
                         status: FULFILLED
```

**Talking points:**
- "ORGAN-I is the theory layer. This repo implements a self-governing
  orchestration framework — a system that manages its own revision process."
- "It has 8 phases, 4 human review gates, a BLAKE3 cryptographic audit chain,
  and ethical axiom enforcement."
- "Notice `promotion_obligations`: when this theory repo reached PUBLIC_PROCESS
  status, it triggered a contractual obligation to create an art derivative in
  ORGAN-II. That obligation is FULFILLED."
- "This is the institutional model: theory does not exist for its own sake. It
  must produce art."

**Transition cue:** "The obligation was fulfilled. Let me show you what it
produced."

#### Beat 2 — The Art Derivative (3 minutes)

```bash
organvm registry show art-from--auto-revision-epistemic-engine
```

**Expected output:**

```
  art-from--auto-revision-epistemic-engine
  ────────────────────────────────────────
  Organ:       ORGAN-II
  org:                organvm-ii-poiesis
  status:             ACTIVE
  description:        Interactive visualization of self-governing orchestration
                      — governance as performance art
  dependencies:       organvm-i-theoria/auto-revision-epistemic-engine
  promotion_status:   CANDIDATE
  tier:               standard
  ci_workflow:        ci-python.yml
  platinum_status:    True
```

**Talking points:**
- "The naming convention makes the lineage explicit:
  `art-from--auto-revision-epistemic-engine`. Double-hyphen separates function
  from source."
- "This is an interactive visualization — it turns the governance framework
  into performance art. The 8 phases, the review gates, the audit chain all
  become visual and sonic material."
- "Note the `dependencies` field: it points back to the ORGAN-I source. This
  edge is enforced. You cannot create an ORGAN-II repo without declaring where
  the theory came from."
- "Status: CANDIDATE. It has CI, platinum status, and is moving toward
  PUBLIC_PROCESS — following the same state machine as its parent."

Now show a second theory-to-art pair to establish the pattern:

```bash
organvm registry show narratological-algorithmic-lenses
```

**Expected output (abbreviated):**

```
  narratological-algorithmic-lenses
  ────────────────────────────────────────
  Organ:       ORGAN-I
  description:        14 narratological studies x 92 algorithms — formalizing
                      narrative principles from Aristotle to Pixar as executable
                      code
  promotion_obligations: target: art-from--narratological-algorithmic-lenses
                         status: FULFILLED
```

```bash
organvm registry show art-from--narratological-algorithmic-lenses
```

**Expected output (abbreviated):**

```
  art-from--narratological-algorithmic-lenses
  ───────────────────────────────────────────
  Organ:       ORGAN-II
  description:        Interactive web experience exploring narrative structures
                      via visual algorithmic lenses
  dependencies:       organvm-i-theoria/narratological-algorithmic-lenses
```

**Talking points:**
- "Same pattern. 14 narratological studies and 92 algorithms in ORGAN-I become
  an interactive web experience in ORGAN-II."
- "This is not incidental. The naming convention, the promotion obligation, and
  the dependency declaration are system-level contracts that every repo follows."

**Transition cue:** "Theory produces art. Now let me show you how the dependency
graph connects all of this."

#### Beat 3 — The Seed Graph (2 minutes)

```bash
organvm seed graph
```

**Expected output:**

```
Seed Graph: 110 repos, 13 edges

Produces/Consumes edges:
  organvm-i-theoria/auto-revision-epistemic-engine
    --[dependency]--> organvm-ii-poiesis/art-from--auto-revision-epistemic-engine
  organvm-i-theoria/narratological-algorithmic-lenses
    --[dependency]--> organvm-ii-poiesis/art-from--narratological-algorithmic-lenses
  organvm-iii-ergon/public-record-data-scrapper
    --[dependency]--> organvm-v-logos/public-process
  organvm-iv-taxis/agentic-titan
    --[dependency]--> organvm-v-logos/public-process
  organvm-vi-koinonia/koinonia-db
    --[package]--> organvm-vi-koinonia/adaptive-personal-syllabus
  ...
```

**Talking points:**
- "110 repos, 13 declared edges. Every connection is explicit in a `seed.yaml`
  file — there are no implicit dependencies."
- "The I-to-II flow is visible: theory to art. The III-to-V flow shows products
  feeding the public-process essay platform."
- "The direction is enforced. I to II to III. No back-edges allowed. ORGAN-IV
  orchestrates. ORGAN-V observes. ORGAN-VII distributes."

Validate the graph structure:

```bash
organvm governance check-deps
```

**Talking points:**
- "Zero back-edges, zero cycles, zero self-dependencies. The unidirectional
  flow is mathematically verified, not just documented."
- "7 missing targets are in ORGAN-VI and ORGAN-VII — newly wired community and
  distribution repos. The system does not pass itself when edges are incomplete."

**Transition cue:** "The graph connects theory to art. Now let me follow the
path all the way to a deployed product."

#### Beat 4 — The Deployed Product (3 minutes)

```bash
organvm registry show public-record-data-scrapper
```

**Expected output:**

```
  public-record-data-scrapper
  ────────────────────────────────────────
  Organ:       ORGAN-III
  org:                organvm-iii-ergon
  status:             DEPLOYED
  description:        50-state UCC public records aggregation platform. Live
                      Vercel deployment, tiered B2B subscriptions, Terraform AWS
                      infrastructure, 60+ collection agents, 2,055 tests.
  promotion_status:   PUBLIC_PROCESS
  tier:               flagship
  ci_workflow:        ci-typescript.yml
  platinum_status:    True
  revenue_model:      subscription
  revenue_status:     pre-launch
  deployment_url:     https://public-record-data-scrapper.netlify.app
```

**Talking points:**
- "ORGAN-III is the commercial arm. The flagship is a 50-state public records
  platform — B2B, subscription model, 60+ data collection agents, 2,055 tests."
- "It has a live deployment, CI, and platinum status. It is at PUBLIC_PROCESS —
  the same promotion level as the ORGAN-I theory repos."
- "The governance patterns from ORGAN-I — self-governing phases, audit chains —
  directly informed how this product manages its own collection pipeline."

Show the seed.yaml to demonstrate the contract system:

```bash
cat ~/Workspace/organvm-iii-ergon/public-record-data-scrapper/seed.yaml
```

**Expected output (abbreviated):**

```yaml
organ: III
organ_name: Commerce
repo: public-record-data-scrapper
metadata:
  implementation_status: PRODUCTION
  tier: flagship
produces:
  - type: dependency
    description: Consumed by organvm-v-logos/public-process
    consumers: [organvm-v-logos/public-process]
subscriptions:
  - event: governance.updated
    source: ORGAN-IV
  - event: health-audit.completed
    source: ORGAN-IV
```

**Talking points:**
- "The product declares what it produces — its output feeds the public-process
  essay platform in ORGAN-V."
- "It subscribes to governance updates from ORGAN-IV. When governance rules
  change, this product knows it needs to check compliance."
- "This is a commercial product that is embedded in an institutional
  architecture. It does not stand alone — it participates in the system."

Open in browser:

```bash
open https://public-record-data-scrapper.netlify.app
```

**Transition cue:** "This product is live but pre-revenue. Let me show you the
revenue readiness picture."

#### Beat 5 — Revenue Readiness Status (2 minutes)

```bash
organvm omega status 2>&1 | grep -E "(#8|#9|#10)"
```

**Expected output:**

```
  ■ #8   ≥1 ORGAN-III product live                     MET
  □ #9   revenue_status: live for ≥1 entry             NOT_MET
  □ #10  MRR ≥ system operating costs                  NOT_MET
```

**Talking points:**
- "Omega criterion #8 is MET — at least one ORGAN-III product is live. There
  are actually 12 live deployments."
- "Criterion #9 — live revenue — is NOT MET. The system is honest: $0 MRR.
  Revenue status across ORGAN-III is pre-launch."
- "Criterion #10 — MRR covering operating costs — is also NOT MET. The system
  does not pretend to be revenue-positive."

Show the revenue model breakdown:

```bash
organvm registry show gamified-coach-interface | grep -E "(revenue|deployment)"
```

**Expected output:**

```
  revenue_model:      subscription
  revenue_status:     pre-launch
  deployment_url:     https://gamified-coach-interface.pages.dev
```

```bash
organvm registry show search-local--happy-hour | grep -E "(revenue|deployment)"
```

**Expected output:**

```
  revenue_model:      freemium
  revenue_status:     pre-launch
  deployment_url:     https://search-local-happy-hour.netlify.app
```

**Talking points:**
- "Across ORGAN-III, there are subscription products, freemium products, and
  one-time purchase products. All pre-launch."
- "The revenue infrastructure is in the registry — model, status, deployment URL.
  When any of these go live with paying users, the system will automatically
  detect it and update omega criterion #9."
- "The path is clear: deployed, instrumented, waiting for first revenue."

**Transition cue:** "Revenue is the destination. Let me show you the full
promotion pipeline that gets repos there."

#### Beat 6 — The Promotion State Machine (2 minutes)

```bash
organvm governance promote public-record-data-scrapper GRADUATED
```

**Expected output:**

```
  PUBLIC_PROCESS -> GRADUATED
  Transition is valid. Use 'organvm registry update' to apply.
```

**Talking points:**
- "The promotion state machine: LOCAL, CANDIDATE, PUBLIC_PROCESS, GRADUATED,
  ARCHIVED. You cannot skip states."
- "The flagship product is eligible for graduation — it has CI, platinum status,
  and active implementation. The transition is valid."
- "But graduation is not applied until the omega scorecard passes. The system
  holds itself to the full 17-criteria standard."

Show blast radius for the flagship:

```bash
organvm governance impact public-record-data-scrapper
```

**Expected output:**

```
Impact Analysis for: public-record-data-scrapper
  1 repositories affected:
    - public-process

  Propagation Path:
      ↳ public-process
```

Contrast with the ORGAN-I flagship:

```bash
organvm governance impact recursive-engine--generative-entity
```

**Expected output:**

```
Impact Analysis for: recursive-engine--generative-entity
  18 repositories affected:
    - metasystem-master
    - agentic-titan
    - public-process
    ...

  Propagation Path:
      ↳ metasystem-master
      ↳ agentic-titan
        ↳ agent--claude-smith
          ↳ a-i--skills
```

**Talking points:**
- "The ORGAN-III flagship affects 1 downstream consumer. The ORGAN-I flagship
  affects 18."
- "This makes structural sense: theory is foundational, products are terminal.
  Theory changes cascade. Product changes are contained."
- "The system knows this. The blast radius is computed, not estimated."

**Closing line:** "From theory to art to product — with enforced dependency
flow, machine-verified governance, contractual promotion obligations, live
deployments, and honest revenue reporting. This is not a collection of
projects. It is an institutional architecture where every edge is declared,
every transition is verified, and every number is computed from the actual
system state."

---

## Recording Notes

**Terminal setup:** Use a clean terminal with a dark background and a monospace
font at 16pt or larger. Set the window to 100 columns wide. Disable shell
prompt decorations that add noise. Consider iTerm2 with a minimal profile.

**Pacing:** Pause 2-3 seconds after each command output before speaking. Let
the audience read. Do not narrate the output line by line — summarize and
interpret. For the 15-minute demo, you have room to breathe between beats.

**Tone:** Calm, factual, understated. Let the numbers speak. Avoid superlatives.
The system's scale and rigor are self-evident when you show the actual output.
When the system reports NOT_MET or FAIL, do not apologize — say "the system is
honest about what it has not achieved."

**Fallback:** If a command produces unexpected output (e.g., new warnings since
last run), acknowledge it: "The system found something new — that is the point.
It does not run on cached results."

**Browser prep:** Have the deployed URLs pre-loaded in browser tabs for quick
switching during Beats 4 and 5 of Demo 3. The HTTP status checks via `curl`
are the proof; the browser is the visual payoff.

**Combined versions:**
- **7-minute version:** Demo 1 (5 min) + closing line from Demo 2
- **15-minute version:** Demo 1 (5 min) + Demo 2 (10 min) — comprehensive
  operational picture
- **30-minute version:** All three demos back to back, with audience Q&A after
  each. Use Demo 1 as the hook, Demo 2 as the methodology, Demo 3 as the
  narrative arc. End with the blast radius comparison.

**Pre-flight checklist:**
1. `source .venv/bin/activate` from `meta-organvm/`
2. Run `organvm status` once to verify the CLI is working
3. Verify internet connectivity for `curl` and browser demos
4. Close unrelated terminal tabs and browser windows
5. Set terminal font size to 16pt+
6. Disable notifications and Do Not Disturb
