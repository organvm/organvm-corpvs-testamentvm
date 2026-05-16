# Portfolio Brief: The Eight-Organ System

**For:** All application tracks (art-tech grants, residencies, selective employment, consulting)
**Updated:** 2026-02-18
**Status:** LAUNCHED — all 8 organs OPERATIONAL
**Funding strategy:** [10-funding-strategy.md](./10-funding-strategy.md) — benefits cliff, deadline sequencing, identity positions
**Canonical identity, metrics, and text blocks:** [00-covenant-ark.md](./00-covenant-ark.md) — single source of truth for all application materials

---

## One-Paragraph Summary

I designed and implemented an eight-organ orchestration system that coordinates 148 repositories across 8 GitHub organizations — spanning theory, generative art, commercial products, governance, public process, community, and marketing. The system includes a machine-readable registry, automated dependency validation, a formal promotion state machine (LOCAL -> CANDIDATE -> PUBLIC_PROCESS -> GRADUATED -> ARCHIVED), and 11 GitHub Actions workflows for autonomous governance. It is fully documented at ~6K+ words and validated by automated scripts that check every repository for CI/CD, documentation, dependency integrity, and constitutional compliance.

---

## System at a Glance

| Dimension | Value |
|-----------|-------|
| Total repositories | 148 |
| GitHub organizations | 8 |
| Documentation | ~6K+ words |
| CI/CD coverage | 82+ repos with workflows |
| Validation scripts | 5 automated, all passing |
| Meta-system essays | 41 published (~150K words) |
| Dependency edges | 62, all validated |
| Back-edge violations | 0 |
| Circular dependencies | 0 |
| Implementation status | 92 ACTIVE, 54 ARCHIVED |

---

## The Eight Organs

| # | Organ | Domain | Repos | What It Demonstrates |
|---|-------|--------|-------|----------------------|
| I | Theoria | Theory & epistemology | 20 | Intellectual depth, foundational thinking, recursive systems |
| II | Poiesis | Generative art & performance | 30 | Creative systems design, artistic infrastructure |
| III | Ergon | Commerce & products | 27 | Product-market thinking, revenue generation, deployment |
| IV | Taxis | Orchestration & governance | 7 | Systems architecture, governance design, organizational capacity |
| V | Logos | Public process & essays | 2 | Transparency, thought leadership, building in public |
| VI | Koinonia | Community | 4 | Collaborative infrastructure, community contribution |
| VII | Kerygma | Marketing & distribution | 4 | Audience building, POSSE automation, content strategy |
| VIII | Meta | Umbrella coordination | 3 | Cross-system integration, meta-documentation |

---

## Key Technical Achievements

### Orchestration Architecture
- **Central registry** (`registry-v2.json`): Single source of truth for all 100 repos — status, dependencies, documentation, tier, promotion state
- **Dependency validation**: Automated checks enforce no back-edges in I->II->III chain, no circular dependencies, transitive depth <= 4
- **Promotion state machine**: Formal governance pipeline (LOCAL -> CANDIDATE -> PUBLIC_PROCESS -> GRADUATED -> ARCHIVED) with automated workflows

### Automation Stack
- **5 GitHub Actions workflows**: validate-dependencies, monthly-organ-audit, promote-repo, publish-process, distribute-content
- **Organ audit script**: Full system health check across all 8 organs with Markdown report + JSON metrics
- **POSSE distribution**: Automated content distribution to Mastodon, Discord, newsletter

### Flagship Projects
- **recursive-engine--generative-entity** (ORGAN-I): Symbolic operating system — 1,254 tests, 85% coverage, 21 organ handlers
- **agentic-titan** (ORGAN-IV): Multi-agent orchestration framework — 1,095 tests, 18 development phases
- **metasystem-master** (ORGAN-II): Generative art meta-system, the creative engine connecting theory to practice
- **life-my--midst--in** (ORGAN-III): Interactive identity/CV platform with Inverted Interview paradigm, feature-complete, selected for beta (Sprint 25 INSPECTIO assessment)

---

## Positioning by Track

### Art-Tech Grants (PRIMARY TRACK — highest fit)
**Evidence:** ORGAN-V essays (41 published, ~6K+ words) + machine-readable registry documenting 5 years of sustained organizational capacity + 33 named development sprints. **Demonstrates:** The ORGANVM system AS a creative work — governance-as-art, process-as-product, sustained practice at institutional scale. **Targets:** Creative Capital (9/10), Artadia NYC (8/10), Spencer Foundation (6/10).

### Residencies & Fellowships
**Evidence:** 100 repos assembled into a coherent system through editorial vision, documented in real-time across 42 essays — the creative process itself rendered as the product. **Demonstrates:** Systemic creative practice, solo production at institutional scale, AI-augmented methodology, documentation as primary artistic output. **Targets:** Google Creative Lab (8/10), Fire Island (7/10), Eyebeam (7/10), Processing Foundation (6/10).

### Consulting & Freelance
**Evidence:** The 148-repo system IS the credential. AI orchestration, documentation, workshop facilitation. **Demonstrates:** $100-125/hr market rate for AI orchestration consulting. 100+ courses taught, 2,000+ students, ~6K+ words of documentation. **Rate floor:** $100/hr (corrected from $60/hr per market research).

### Selective Employment (deprioritized)
**Evidence:** ORGAN-IV orchestration architecture, registry-as-truth design, governance trade-offs encoded in governance-rules.json, agentic-titan (1,095 tests across 18 phases). **Demonstrates:** Production-ready systems thinking, architectural reasoning, autonomous system design, test-driven development at scale. **Targets:** Together AI (6/10), HuggingFace (5/10). Engineering roles are competitive reaches from a non-traditional background — apply selectively.

---

## Evidence Links

| Asset | URL |
|-------|-----|
| Central Registry | `github.com/meta-organvm/organvm-corpvs-testamentvm/registry-v2.json` |
| Orchestration Hub | `github.com/organvm-iv-taxis/orchestration-start-here` |
| Public Process | `github.com/organvm-v-logos/public-process` |
| Governance Spec | `github.com/meta-organvm/organvm-corpvs-testamentvm/docs/implementation/orchestration-system-v2.md` |
| CI/CD Spec | `github.com/meta-organvm/organvm-corpvs-testamentvm/docs/implementation/github-actions-spec.md` |

---

## Process as Product

The eight-organ system makes the creative process itself visible, governable, and reproducible. The 42 essays aren't marketing — they're the creative process rendered into prose. The governance rules aren't bureaucracy — they're generative constraints that shape what the system can become. The registry isn't just metadata — it's the editorial arrangement that turns 97 individual repos into a coherent body of work.

This is the thesis: **the process of creation IS the product.** Grant reviewers see sustained organizational capacity. Residency evaluators see a documented creative methodology. Engineering hiring managers see production-grade systems thinking. Same evidence, same system — the framing shifts, but the work is one thing.

## The Method

The system was built using AI tools as compositional instruments — the architectural vision, governance design, and editorial judgment are the creative work; AI provides execution capacity. The system design that turns 100 repos into a coordinated organism instead of a pile of code is what distinguishes this from either pure engineering or pure art.

Solo production at full intensity: not isolation as limitation, but as the only way to maintain a singular vision across theory, art, commerce, governance, public process, community, and marketing. Five years of construction, 33 named sprints, 6,200+ words — built alone because the work required it.

## Who This Is For

| Audience | What They See |
|----------|--------------|
| Art-tech grant programs | A living creative work: governance-as-art, 5+ years sustained practice, the system IS the artwork |
| Residencies & fellowships | A documented creative methodology: the process of creation as artistic practice |
| Consulting clients | Demonstrated AI orchestration at scale: 100 repos, autonomous governance, ~6K+ words of documentation |
| Selective employment | Production-grade systems thinking: governance, orchestration, autonomous infrastructure |
| Collaborators | A system designed to scale: community infrastructure, public documentation, reusable patterns |
