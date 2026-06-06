# 13. Organ Identity and Placement

*Standard 13 — Epistemic Membranes: Formalizing Organ & Repository Identity*

## 1. Philosophy

The ORGANVM system is built on the principle that **each organ is an epistemic domain** — a bounded region of concern with its own vocabulary, practices, and outputs. These boundaries are not administrative conveniences but structural necessities. When boundaries blur, the system loses its ability to reason about itself: dependency analysis becomes meaningless, governance rules fire on false targets, and the registry degenerates from a map of the world into a phonebook.

AX-2 (Epistemic Membranes) already enforces that cross-organ data flow must be *declared*. This standard extends that principle to the organs themselves: **what makes an organ an organ must be formalized, machine-readable, and auditable**.

The organ system exists at three scales:
- **Enterprise** (ORGANVM) — the whole system, one entity
- **Organization** (8 organs) — epistemic domains, each a GitHub org
- **Repository** (~113 repos) — individual units of work within organs

This document governs the middle scale: what defines each organization, and how repositories are assigned to the correct one.

## 2. The Organ Map

### ORGAN-I: Theoria (Theory)

**Purpose:** Foundational theory, epistemological frameworks, recursive engines, ontological systems, symbolic computing.

**What belongs here:** Pure conceptual structures — algorithms, engines, and frameworks that express ideas. The output is knowledge structures that other organs consume. A Theoria repo should be *about* an idea, not *for* a user.

**What does NOT belong here:**
- Repos with user-facing interfaces → ORGAN-II or ORGAN-III
- Repos that generate revenue → ORGAN-III
- Repos that orchestrate other repos → ORGAN-IV
- Documentation or essays → ORGAN-V

**Ambiguity resolution:** "Is this a theory or a product?" — if it has a `revenue_model`, it's a product. If it has an audience beyond other repos, it's art (II) or product (III). If it could exist as a paper, it's theory.

### ORGAN-II: Poiesis (Art)

**Purpose:** Generative art, performance systems, creative coding, experiential design.

**What belongs here:** Artifacts that transform ORGAN-I theory into aesthetic experience. Installations, performances, generative systems, creative tools. The output is something that can be *experienced*.

**What does NOT belong here:**
- Repos that generate revenue as products → ORGAN-III
- Pure frameworks with no artistic output → ORGAN-I
- Content distribution systems → ORGAN-VII

**Ambiguity resolution:** "Is this art or a product?" — if the primary intent is aesthetic/expressive, it's art even if it *could* make money. If it has a pricing page, it's a product.

### ORGAN-III: Ergon (Commerce)

**Purpose:** Commercial products, SaaS tools, developer utilities, B2B/B2C applications. The factory floor.

**What belongs here:** Anything with a revenue model or intended for market deployment. Every non-archived Ergon repo must declare `revenue_model` and should have CI configured (per OD-III Factory Gate).

**What does NOT belong here:**
- Pure theory → ORGAN-I
- Art → ORGAN-II
- System orchestration → ORGAN-IV
- Revenue model is `none` or `internal` with no customer intent → reassess

**Ambiguity resolution:** "Should community features inside a product stay in III?" — yes. The *product* is in III; community *infrastructure* is in VI. Products *feed* community via event edges.

### ORGAN-IV: Taxis (Orchestration)

**Purpose:** Orchestration, governance tooling, AI agent management, workflow routing, system coordination.

**What belongs here:** The conductor layer — repos that direct other organs but don't contain their domain logic. Agent behavior libraries, skills, interaction design, routing rules.

**What does NOT belong here:**
- Foundational theory → ORGAN-I
- Products → ORGAN-III
- Governance *data* (registry, schemas, rules) → META-ORGANVM

**Ambiguity resolution:** "AI skills library: I or IV?" — IV, because it orchestrates agent behavior. The *theory* behind skill design might be I, but the *library of actionable skills* is orchestration. "Conductor: IV or META?" — Conductor manages session flow (orchestration), not system data, so IV.

### ORGAN-V: Logos (Discourse)

**Purpose:** Public discourse, essays, building in public, editorial content. The observatory.

**What belongs here:** Written content for public consumption. Read-many-write-one: V observes all organs but produces only to its own domain.

**What does NOT belong here:**
- Internal governance docs → META/praxis-perpetua
- Content that generates revenue → ORGAN-III
- Content distribution → ORGAN-VII

**Ambiguity resolution:** "Blog posts about a product: III or V?" — V. The *product* is in III; the *essay about building it* is in V. The essay produces no cross-organ edges.

### ORGAN-VI: Koinonia (Community)

**Purpose:** Community infrastructure — salons, reading groups, learning cohorts, community taxonomy.

**What belongs here:** Repos that serve a community of people. Receives events from products (III) and theory (I) to build community around them.

**What does NOT belong here:**
- Products that monetize community → ORGAN-III
- Content broadcasting → ORGAN-VII
- Internal coordination → ORGAN-IV

### ORGAN-VII: Kerygma (Distribution)

**Purpose:** POSSE distribution, social automation, announcement pipelines. Pure consumer.

**What belongs here:** One-way broadcasting. Takes content from V and announcements from other organs, syndicates to external platforms. **Must not have `produces` edges** (per OD-VII).

**What does NOT belong here:**
- Original content production → ORGAN-V
- Community interaction → ORGAN-VI
- Products → ORGAN-III

### META-ORGANVM: Meta

**Purpose:** The structural substrate. System registry, JSON schemas, core engine, governance corpus, process SOPs, dashboard, MCP server, ingestion pipeline.

**What belongs here:** Infrastructure required for the organ system to function. Changes here propagate system-wide.

**What does NOT belong here:**
- Agent orchestration → ORGAN-IV
- Products → ORGAN-III
- Public content → ORGAN-V
- Theory consumed by II/III → ORGAN-I

**Ambiguity resolution:** "Engine: META or I?" — the engine that *manages the system* is META. Engines that express *theories consumed by other organs* are I.

## 3. Placement Decision Tree

```
START: You have a new repo. Where does it go?

Q1: Does it generate revenue (or intend to)?
  YES → ORGAN-III (Ergon)
  NO → Q2

Q2: Does it orchestrate other repos or manage AI agents?
  YES → ORGAN-IV (Taxis)
  NO → Q3

Q3: Is it system infrastructure (registry, schemas, engine, dashboard)?
  YES → META-ORGANVM
  NO → Q4

Q4: Is it pure theory / framework / knowledge structure?
  YES → Q4a: Does it produce aesthetic/experiential artifacts?
    YES → ORGAN-II (Poiesis)
    NO → ORGAN-I (Theoria)
  NO → Q5

Q5: Is it public content (essays, editorial)?
  YES → ORGAN-V (Logos)
  NO → Q6

Q6: Is it community infrastructure?
  YES → ORGAN-VI (Koinonia)
  NO → Q7

Q7: Does it distribute content to external platforms?
  YES → ORGAN-VII (Kerygma)
  NO → Revisit Q1-Q6 or consult this document's ambiguity resolutions.
```

## 4. Boundary Disputes

| Repo | Current Organ | Dispute | Resolution |
|------|---------------|---------|------------|
| `a-i--skills` | ORGAN-IV | Knowledge-like, could be I | IV — orchestrates agent behavior |
| `tool-interaction-design` (contains Conductor) | ORGAN-IV | Conductor could be META infrastructure | IV — session flow is orchestration, not data |
| `portfolio-site` (inside corpus) | META (as sub-dir) | Full Astro app inside governance corpus | Should be extracted as independent repo |
| `organvm-engine` modules at scale | META | Some modules have >10 files | Acceptable for a core engine; monitor growth |

## 5. The Drift Audit Process

### Running the audit

```bash
# Full audit — all repos with affinity scores
organvm governance placement

# Single repo check with recommendations
organvm governance placement --repo <name>

# Only flagged repos
organvm governance placement --audit

# Machine-readable
organvm governance placement --json
```

### Running excavation

```bash
# Full excavation — all buried entities
organvm governance excavate

# Filter by type
organvm governance excavate --type sub_package

# Cross-organ family report
organvm governance excavate --families

# Machine-readable
organvm governance excavate --json
```

### Interpreting results

**Placement scores** (0-100):
- 70+: Well-placed, no action needed
- 50-69: Questionable — review inclusion/exclusion criteria
- <50: Misplaced — investigate and consider moving

**Excavation severities:**
- `info`: Noteworthy but not actionable (e.g., cross-organ families)
- `warning`: Should be reviewed and potentially remediated
- `critical`: Immediate action needed (e.g., sub-package with its own CI)

### Remediation

Moving a repo between organs:
1. Run `organvm governance placement --repo <name>` to confirm misplacement
2. Update `repo-registry.json` — move repo to the correct organ's array
3. Update `seed.yaml` — change `organ` field
4. Update GitHub — transfer repo to the correct org
5. Re-run `organvm governance placement --audit` to verify

## 6. References

- **organ-definitions.json** — Machine-readable organ identity definitions (source of truth for placement criteria)
- **AX-5 Organ Placement** — The dictum that enforces this standard
- **AX-2 Epistemic Membranes** — Cross-organ data flow must be declared
- **Doc 12 (Habitat Governance Lifecycle)** — Promotion stages within an organ
- **Doc 10 (Repository Standards)** — Root hygiene and README standards
