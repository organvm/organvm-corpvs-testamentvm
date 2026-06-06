# 12: Habitat Governance Lifecycle

**Date:** 2026-03-06
**Status:** ACTIVE — applies to all repos across 8 organs
**Derived from:** Styx full-breath audit (2026-03-06), structural integrity audit (2026-03-06), document 10 (repository standards), quarterly sustainability checklist
**Complements:** `10-repository-standards.md` (root hygiene), `11-specification-driven-development.md`, quarterly sustainability checklist

---

## 1. Philosophy: Ideas Find Their Habitat

The ORGANVM is not a filing system. It is a living topology — a constructed universe where ideas germinate, root, and grow.

An idea begins as abstraction. A thought, an intuition, an itch. It has no home yet and needs none. It might live in a journal, a voice memo, a conversation with an AI. This is the Theoria phase — pure potential.

The moment that abstraction touches material — a research session, a brainstorm document, a prototype, an AI chat that generates something surprising — the idea begins to take shape. It develops gravity. And the ORGANVM, if it is well-constructed, offers a natural habitat where that shaped idea can root itself without being forced into a box it doesn't fit.

Some ideas root in art (Poiesis). Some root in commerce (Ergon). Some turn out to be governance insights (Taxis) or community initiatives (Koinonia). The system doesn't decide in advance. The idea finds its organ the way a seed finds its soil — through affinity, not assignment.

**The governance artifacts described in this document are not bureaucratic overhead imposed from above.** They are the soil conditions that allow an organism to survive at each stage of its growth. A seedling doesn't need a security policy. A tree bearing fruit that strangers pay for does. The promotion ladder encodes this natural logic.

---

## 2. The Promotion Ladder as Growth Stages

Each stage of the promotion ladder corresponds to a phase of organic development. The governance requirements at each stage exist because the organism genuinely needs them to survive — not because a policy said so.

### Pre-LOCAL — The Materia Collider

Before an idea even becomes a LOCAL repo, it may exist in the **materia-collider** (`meta-organvm/materia-collider/`) — the pre-codified experimental space where ideas collide, contradict, and transform before earning a place in the organ system.

The collider is the dream-state counterpart to the wake-state organs. Nothing in it is canonical. Contradictions are encouraged. Ideas can be killed without ceremony. Its `bench/` directory has no naming conventions, no format requirements — it is the workshop bench covered in sawdust.

**What happens here:**
- Raw ideas enter from `intake/`, from conversations, from inversions of existing assumptions
- Collision protocols (inversion, dialectic, analogical, scale, temporal, archetypal) transform raw material
- The director observes what emerges. Some collisions produce nothing. Some produce a new particle — an idea ready to root.

**Who does what:**
- The **director** (human) senses what's missing, selects ideas for collision, and judges when something is ready to graduate
- **Specialists** (AI archetypes from the skill library or Agentic Titan) execute collision protocols and produce experimental results
- No specialist would surface the need for the collider itself — that perception lives at the system-design level, the director's level

**Graduation from the collider** happens three ways, simultaneously valid:
1. **Manual**: The director moves an idea to the right organ deliberately
2. **Directed**: The director signals readiness; a specialist produces the organ-appropriate artifact (seed.yaml, README, etc.)
3. **Organic**: During normal work, collider material naturally becomes code or docs in an organ — no formal graduation

An idea that graduates from the collider enters the promotion ladder at LOCAL. From there, the lifecycle below applies.

### LOCAL — The Seedling

The idea just sprouted. It might be a single file, a prototype, a half-formed repo. It barely has a name.

**What it needs to survive:**
- `seed.yaml` declaring organ membership and what it is
- `README.md` (even a paragraph)
- `.gitignore`
- A working git repo

**What it does NOT need:** Security policies, contributing guides, ADRs, CI pipelines, code of conduct. These would be premature. The organism is still figuring out what it is. Governance at this stage is overhead that slows experimentation.

**The habitat provides:** Freedom to pivot, rename, restructure, or die without ceremony. Most LOCALs never promote. That's healthy.

### CANDIDATE — The Sapling

The idea has taken enough shape to name. It has a `seed.yaml`, a real README, and someone (even just the creator) can explain what it does and why it exists. It may have working code or it may be a specification. Either way, it has committed to being *something*.

**What it needs to survive (in addition to LOCAL):**
- `CLAUDE.md` — AI agent context so automated tools can understand it
- `LICENSE` — even if provisional
- Dependency audit awareness (monthly `npm audit` or equivalent)
- Tags and description set on GitHub

**What it does NOT need yet:** Contributing guides (nobody else is contributing), security policies (nothing is deployed), ADRs (not enough decisions have been made to document). The organism is growing but not yet public-facing.

**The habitat provides:** Visibility within the system. The registry knows it exists. The quarterly checklist will spot-check it. But it's still mostly left alone to grow.

### PUBLIC_PROCESS — The Flowering Tree

The organism is visible to the world. It has a deployment, a CI pipeline, users or at least an audience. Other people can see it, interact with it, maybe contribute to it. This is where governance becomes essential — not as compliance, but as care for something that is now alive in a shared ecosystem.

**What it needs to survive (in addition to CANDIDATE):**

| Artifact | Purpose | Why Now |
|----------|---------|---------|
| `SECURITY.md` | Responsible disclosure policy | People can see (and attack) your deployed code |
| `CONTRIBUTING.md` | How to participate | Others may want to contribute or you need to onboard collaborators |
| `CODE_OF_CONDUCT.md` | Community standards | The project has a public identity now |
| `docs/adr/` (1+ ADRs) | Major architectural decisions documented | Decisions are hardening — record why before you forget |
| CI pipeline (`.github/workflows/`) | Automated quality gates | Too much surface area for manual checking |
| Quarterly E2G review | Health assessment | The organism is complex enough to develop hidden problems |
| `seed.yaml` `last_validated` current | Proof of recent audit | The system needs to know this organism was recently examined |

**For repos handling money or personal data** (ORGAN-III financial products):

| Artifact | Purpose | Why Now |
|----------|---------|---------|
| 2+ ADRs covering financial architecture | Document escrow model, payment flows | Money flows must be auditable and explainable |
| 2-reviewer policy for financial code | Prevent single-point errors in money handling | The blast radius of a financial bug is too high for solo review |
| Validation gates in CI | Automated invariant checking | Ledger integrity, no secrets in builds, no banned terminology |

**The habitat provides:** Structure that protects both the organism and its users. The quarterly sustainability checklist now actively monitors this repo. The organ-level governance policies apply. The system-wide registry tracks its health metrics.

### GRADUATED — The Mature Organism

Fully mature. External users depend on it. Revenue may flow through it. Breaking changes require migration plans. The organism has earned its place and now carries responsibility.

**What it needs to survive (in addition to PUBLIC_PROCESS):**

| Artifact | Purpose | Why Now |
|----------|---------|---------|
| External security audit (annual) | Independent verification | Self-assessment is insufficient for production systems others depend on |
| SLA documentation | Uptime and response commitments | Users are making decisions based on your reliability |
| Incident response runbook | How to handle outages and breaches | When things break at 2am, you need a playbook |
| Comprehensive ADR set | All major decisions documented | Institutional memory — the system must be understandable without its creator |
| Changelog / release notes | Communication to dependents | People need to know what changed and when |
| Penetration testing (for financial products) | Active adversarial testing | Passive scanning is insufficient for systems handling money |

**The habitat provides:** Full system integration. Dashboard visibility. Cross-organ event subscriptions active. Distribution pipeline (Kerygma) announces releases. Community (Koinonia) may host discussion groups around it.

### ARCHIVED — The Fossil Record

The organism has completed its lifecycle. It may have been superseded, pivoted into something else, or simply served its purpose. Archiving is not failure — it is completion.

**What remains:**
- README updated with archive notice and pointer to successor (if any)
- `seed.yaml` updated to `ARCHIVED`
- Code preserved as-is (read-only)
- No active CI, no security monitoring, no E2G reviews

**The habitat provides:** Respect. The organism's contributions to the system are recorded. Its ADRs and documentation remain searchable. It can be revived if conditions change.

---

## 3. Organ-Specific Adaptations

The lifecycle above is universal. Each organ adds its own requirements based on its nature:

### ORGAN-III (Commerce / Ergon)

Commerce repos that handle money, PII, or have paying users add:

- **Code review policy** with tiered reviewer requirements (see `commerce--meta/governance/policies/code-review-policy.md`)
- **Security audit cadence** — quarterly E2G, monthly dependency audits, annual external pentest post-beta (see `commerce--meta/governance/policies/security-audit-cadence.md`)
- **Linguistic compliance** — for products distributed via app stores or payment processors, vocabulary scanning in CI
- **Financial ADRs** — escrow model, payment flows, and ledger integrity must be documented before PUBLIC_PROCESS

### ORGAN-I (Theoria)

Theory repos that contain research or personal archives add:
- **Data sensitivity classification** — mark files containing personal data
- **SHA-pinned GitHub Actions** — org policy for supply chain security

### ORGAN-II (Poiesis)

Creative repos add:
- **License clarity** — CC BY-SA or CC BY-NC-SA for creative works vs. MIT for code
- **Attribution requirements** — for collaborative or remix-based works

### Other Organs

Organs IV-VII follow the universal lifecycle. Organ-specific additions are documented in each organ's `CLAUDE.md` and, where they exist, in the organ's governance directory.

---

## 4. The SOP: Equipping a Repo at Promotion Time

When a repo is ready to promote from one stage to the next, use this checklist to ensure it has the habitat conditions it needs. This is not a gate to pass — it is a garden to tend.

### LOCAL → CANDIDATE

- [ ] `seed.yaml` exists with correct organ, tier, and `promotion_status: CANDIDATE`
- [ ] `README.md` explains what this is and why it exists
- [ ] `.gitignore` is language-appropriate
- [ ] `LICENSE` selected (see doc 10 §2.3)
- [ ] `CLAUDE.md` provides AI agent context
- [ ] GitHub repo has description and topics set
- [ ] Run `npm audit` / `pip audit` — no critical vulnerabilities

### CANDIDATE → PUBLIC_PROCESS

- [ ] `SECURITY.md` with disclosure policy and scope
- [ ] `CONTRIBUTING.md` with setup, PR process, and test requirements
- [ ] `CODE_OF_CONDUCT.md` (Contributor Covenant v2.1 + domain-specific additions)
- [ ] At least 1 ADR documenting the most significant architectural decision
- [ ] CI pipeline running: build + test + lint minimum
- [ ] `seed.yaml` updated: `promotion_status: PUBLIC_PROCESS`, `last_validated` current
- [ ] First E2G review completed and filed in `docs/planning/`
- [ ] **If financial/PII**: 2+ ADRs, validation gates in CI, 2-reviewer policy documented

### PUBLIC_PROCESS → GRADUATED

- [ ] All PUBLIC_PROCESS requirements satisfied
- [ ] ADR set covers all major architectural decisions (aim for 3+)
- [ ] External security audit scheduled or completed (financial products)
- [ ] SLA documented (even if informal — "best effort" is a valid SLA for solo operator)
- [ ] Incident response notes exist (even a paragraph in SECURITY.md)
- [ ] Changelog or release notes established
- [ ] `seed.yaml` updated: `promotion_status: GRADUATED`

### Any → ARCHIVED

- [ ] README updated with archive notice
- [ ] Pointer to successor repo (if applicable)
- [ ] `seed.yaml` updated: `promotion_status: ARCHIVED`
- [ ] CI disabled or reduced to prevent false-alarm noise
- [ ] Final commit message: `chore: archive — {reason}`

---

## 5. Relationship to Other Documents

| Document | Relationship |
|----------|-------------|
| `10-repository-standards.md` | Defines root hygiene (what files belong at root). This document defines *when* each file becomes necessary. |
| `11-specification-driven-development.md` | Defines the spec-first workflow. This document defines the governance wrapper around specs as they mature. |
| Quarterly sustainability checklist | Operational audit for the whole system. This document defines what each repo should have *before* the quarterly audit checks it. |
| Organ-level governance policies | Organ-specific requirements (e.g., ORGAN-III code review policy). This document provides the universal frame; organs add specifics. |
| `seed.yaml` | Per-repo contract. This document defines what `promotion_status` transitions require. |
| `meta-organvm/materia-collider/` | The pre-codified space upstream of the promotion ladder. Ideas graduate from the collider into LOCAL. |
| `organvm-iv-taxis/agentic-titan/` | The execution engine (22 archetypes, 9 topologies) that processes collider output into organ-ready artifacts. |

---

## 6. Business Habitats — When a Repo Becomes an Organism

Some repos — particularly in ORGAN-III — grow beyond code into something resembling a full business organism. They develop their own governance, research, legal analysis, infrastructure, and operational departments. This is not a violation of the ORGANVM model. It is the natural consequence of a product maturing.

A **business habitat** is a repo that has organically accumulated the limbs of a venture:

- **Product code** (application source, tests, CI)
- **Research** (competitor analysis, market studies, academic grounding)
- **Legal** (regulatory analysis, compliance strategy, IP considerations)
- **Infrastructure** (Terraform, deployment configs, monitoring)
- **Governance** (ADRs, validation gates, review policies)
- **Agent departments** (specialist AI contexts for different operational functions)

### 6.1 The Seven Departments

Extracted from the Styx (`peer-audited--behavioral-blockchain`) pattern, a mature business habitat may develop specialist agent departments in `.claude/agents/`:

| Department | Scope | Example Artifacts |
|-----------|-------|-------------------|
| **Enterprise** | B2B sales, partnerships, integration strategy | Enterprise playbooks, partnership templates |
| **Product** | Feature roadmap, UX research, backlog management | Product briefs, user stories, prioritization |
| **Growth** | Marketing, distribution, user acquisition | Growth experiments, channel strategy |
| **Support** | Customer success, documentation, onboarding | Support runbooks, FAQ, escalation paths |
| **Operations** | Deployment, monitoring, incident response | Runbooks, SLAs, monitoring dashboards |
| **Finance** | Revenue model, pricing, billing integration | Pricing analysis, unit economics, forecasts |
| **Legal** | Compliance, terms of service, regulatory strategy | Regulatory briefs, compliance checklists |

These departments are **repo-scoped agent contexts** — they help AI assistants understand the operational context when working in each domain. They do NOT replace organ-level or system-level governance.

### 6.2 Directory Anatomy of a Business Habitat

```
REPO LAYER (the habitat)
├── src/                      # Application code + co-located tests
├── docs/
│   ├── planning/             # E2G reports, timelines, blocked handoffs
│   ├── adr/                  # Architecture Decision Records
│   ├── research/             # Product research, competitor analysis
│   ├── thesis/               # Academic grounding (if applicable)
│   ├── legal/                # Product-specific legal analysis
│   └── architecture/         # System specs, feasibility studies
├── scripts/
│   ├── validation/           # Quality gates (run in CI)
│   └── smoke/                # Deployment verification
├── infra/terraform/          # Infrastructure as Code
├── .github/workflows/        # CI/CD pipelines
├── .claude/agents/           # Department-specific agent contexts
├── CONTRIBUTING.md           # Contribution guidelines
├── SECURITY.md               # Security policy
├── CODE_OF_CONDUCT.md        # Community standards
├── seed.yaml                 # Automation contract
└── Makefile                  # Build/test/dev commands
```

### 6.3 What Lives Where — The Four-Layer Rule

The ORGANVM model has four governance layers. A business habitat generates artifacts at multiple layers, and each artifact must land at the correct one:

| Layer | Governance Owner | What Belongs Here |
|-------|-----------------|-------------------|
| **Repo** | Code, tests, product docs, agent contexts | Everything specific to this product: source, tests, research, legal analysis, ADRs, `.claude/agents/`, IaC, validation scripts |
| **Organ** | Cross-repo policies, shared governance | Policies that apply to ALL repos in the organ: code review policy, security audit cadence, legal templates, financial frameworks |
| **System** | Registry, schemas, dependency graph, standards | System-wide truth: `repo-registry.json`, cross-organ standards (this document), system metrics |
| **Orchestration** | Workflows, agents, skills | Cross-organ automation: promotion workflows, distribution pipelines, skill library |

**Decision tree for artifact placement:**

1. Does it apply only to this product? → **Repo layer**
2. Does it apply to all repos in this organ? → **Organ layer** (e.g., `commerce--meta/governance/`)
3. Does it define a system-wide standard or truth? → **System layer** (e.g., `organvm-corpvs-testamentvm/`)
4. Does it automate cross-organ coordination? → **Orchestration layer** (e.g., `organvm-iv-taxis/`)

### 6.4 Flagship Promotion Triggers

A repo should be promoted from `standard` to `flagship` tier when it exhibits **three or more** of the following:

| Signal | Threshold | Rationale |
|--------|-----------|-----------|
| Test count | 200+ tests | Indicates production-grade quality investment |
| Documentation volume | 50+ doc files | Indicates mature product thinking beyond code |
| CI workflows | 5+ workflows | Indicates operational sophistication |
| Validation gates | 3+ automated gates | Indicates self-enforcing quality standards |
| Revenue integration | Stripe/payment processor connected | Indicates commercial viability |
| Infrastructure as Code | Terraform/Pulumi present | Indicates deployment maturity |
| Agent departments | 3+ specialist contexts | Indicates operational breadth beyond solo development |
| Academic grounding | Formal proofs or published research | Indicates intellectual depth unique in the system |

When promoting, update both:
- `seed.yaml`: `tier: flagship`
- `repo-registry.json`: `"tier": "flagship"`, `"portfolio_relevance": "CRITICAL - ..."`, `"documentation_status": "DEPLOYED"` or `"FLAGSHIP README DEPLOYED"`

### 6.5 Registry Requirements for Business Habitats

When a repo becomes a business habitat, its registry entry should include:

- `"type"`: One of `SaaS`, `B2B`, `B2C`, `internal`
- `"revenue_model"`: How it makes money (`subscription`, `commission`, `freemium`, `one-time`, `none`)
- `"revenue_status"`: Current state (`pre-revenue`, `pre-launch`, `beta`, `live`, `n/a`)
- `"tier": "flagship"`: Business habitats are by definition flagship-tier
- `"portfolio_relevance": "CRITICAL"`: Products with this level of development are always portfolio-critical

### 6.6 Cross-Organ Signals in seed.yaml

A business habitat's `seed.yaml` should declare its full produce/consume graph:

```yaml
produces:
  - type: product
    description: "What this product is and does"
  - type: community_signal
    description: "Product milestones generate community events"
    consumers: [organvm-vi-koinonia/community-hub]
  - type: distribution_signal
    description: "Product updates trigger POSSE distribution"
    consumers: [organvm-vii-kerygma/social-automation]

consumes:
  - type: governance-rules
    source: ORGAN-IV
    description: "Operations follow governance policies"
```

This ensures the orchestration layer (ORGAN-IV) can route events correctly and the dependency graph reflects reality.

---

## 7. Case Study: Styx (peer-audited--behavioral-blockchain)

Styx is the first repo in the ORGANVM system to organically grow into a full business habitat. Registered 2026-03-06 after a structural integrity audit revealed it had been operating outside the registry despite 159 commits and 499+ tests.

**What Styx has:**
- 499+ tests (most tested repo in the system)
- 147 documentation files across 6 subdirectories
- 7 CI workflows including blocked-handoff governance
- 8 validation gates + 8 smoke scripts
- A formal academic thesis with 9 theorem proofs
- 50+ research documents (competitor analysis, market studies)
- 7 specialist agent departments (enterprise, product, growth, support, ops, finance, legal)
- Terraform infrastructure as Code
- 30 structured GitHub issues with blocked-handoff governance

**Governance layer placement (all correct):**
- Product code, tests, research, legal, thesis, ADRs, agent departments → **repo layer**
- Code review policy, security audit cadence → **organ layer** (`commerce--meta/governance/`)
- Registry entry, this standard → **system layer** (`organvm-corpvs-testamentvm/`)

**Lesson:** The system didn't break. The system just didn't know Styx existed. Registration + tier promotion + pattern codification resolved all governance gaps without moving a single file.
