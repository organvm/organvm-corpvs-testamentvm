# Conference Talk Abstracts

**Created:** 2026-03-04 (Sprint 66: ORATIO)
**Source:** covenant-ark.md, evidence-portfolio.md, existing proposals in conference-proposals/
**Purpose:** Three polished, submission-ready 300-word abstracts for 2026-2027 conference CFPs
**Status:** READY FOR SUBMISSION

---

## Talk 1: The AI-Conductor Model: Building Institutional-Scale Systems Solo

### Abstract (300 words)

What happens when you treat an AI not as a replacement for a developer, but as an orchestra responding to a conductor?

In three weeks, working solo, I built a 113-repository system spanning 8 GitHub organizations -- 739K+ words of documentation, 49 published essays, 4,015+ automated tests, 104 CI/CD workflows -- all governed by a formal promotion state machine, validated dependency graph, and machine-readable registry. The effort metric was not hours but tokens expended: 6.5 million of them, budgeted and tracked across 33+ named sprints the way a film production tracks shooting days.

This talk introduces the AI-conductor methodology: a structured approach where the human provides architectural vision, governance design, and editorial judgment while the AI generates volume at institutional scale. The model has three phases -- direct, generate, review -- and three failure modes I discovered the hard way: hallucinated code examples that pass CI but do nothing, generic phrasing that makes every README indistinguishable, and the VERITAS sprint where I found nine honest-to-god lies in my own AI-generated data and had to build an entire audit framework in response.

The governance layer is what makes it work. A single JSON registry tracks all 113 repositories. A dependency graph enforces unidirectional flow between organs with 62 dependency edges and zero back-edge violations. A five-state promotion pipeline (LOCAL through ARCHIVED) ensures nothing goes public until it meets quality gates. Six JSON schemas validate every data contract. A 32-day zero-incident soak test has verified autonomous operation. Without these structures, AI-generated volume is just AI-generated noise.

This is not a talk about prompt engineering. It is a talk about organizational design -- about how one person can operate at institutional scale by treating AI as infrastructure rather than intelligence. I will share the actual architecture decision records, the billing disasters (48,880 minutes of CI in one month), the metrics, and the methodology you can steal.

### Target Venues

- **Strange Loop** (St. Louis) -- systems thinking, software architecture, programming paradigms
- **XOXO** (Portland) -- independent creators, art+tech, solo practice sustainability

### Speaker Bio

Systems artist and auteur-producer. Creator of the ORGANVM eight-organ system: 113 repositories across 8 GitHub organizations coordinating theory, generative art, commercial products, governance, public process, community, and marketing through automated governance. 49 published essays, 33+ development sprints, 739K+ words of documentation, 4,015+ automated tests, 27 constitutional specs grounded in 130 peer-reviewed sources. 18 years professional experience spanning creative systems design, college instruction (11 years, 2,000+ students at 8+ institutions), multimedia production, and construction project management. MFA Creative Writing (FAU), Meta Full-Stack Developer certification. NYC-based.

### Technical Requirements

- Screen sharing / HDMI output for slides
- No audio required (no live demos with sound)
- Ideal format: 30 min talk + 10 min Q&A
- Adaptable to: lightning talk (10 min), workshop (90 min with hands-on TE budgeting exercise)

### Companion Materials

- Essay: "The AI-Conductor Model" (public-process essay #9, published 2026-02-12)
- Full governance corpus: [organvm-corpvs-testamentvm](https://github.com/meta-organvm/organvm-corpvs-testamentvm)
- 16 Architecture Decision Records (open source)
- Evidence portfolio with verifiable metrics: [evidence-portfolio.md](https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/docs/applications/evidence-portfolio.md)
- Sprint catalog documenting all 33 completed sprints

---

## Talk 2: Constraint Alchemy: From Zero Budget to 113 Repositories

### Abstract (300 words)

No budget. No team. No runway. These are the constraints I started with when I built an eight-organ creative system that now spans 113 repositories, 8 GitHub organizations, and ~404K+ words of documentation -- all on free-tier hosting, with zero employees, in three weeks of calendar time.

Constraint alchemy is not motivational thinking. It is a structured methodology with five techniques I developed and documented across 33 sprints: inverse design (build from the constraint, not despite it -- "no database budget" becomes "registry-as-JSON"), temporal compression (deadlines as creative accelerants -- 33+ sprints in three weeks through AI-conductor methodology), minimum viable governance (the four-document quadrilateral that prevents chaos without creating bureaucracy), autonomous amplification (systems that generate their own content and distribution pipeline), and portfolio-as-proof (process documentation IS the primary deliverable -- 49 essays about building the system ARE the system's output).

I will walk through the actual decisions. Why a single JSON file beats a database when you have 113 repos and zero infrastructure budget. Why disabling 17 GitHub Actions workflows saved the system after a billing disaster of 48,880 CI minutes. Why publishing honest revenue numbers (all zeros) built more credibility with grant reviewers than inflated projections. Why I run a formal promotion state machine, six validated JSON schemas, and a constitutional governance framework grounded in 27 specs backed by 130 peer-reviewed sources -- for a project with exactly one contributor.

The answer to that last question is the core of the talk: constraints do not just shape what you build. They shape what you become. The governance structures I designed to survive zero-budget, zero-team conditions turned out to be more interesting than any individual artifact the system produced. The constraint became the medium. The limitation became the architecture.

I will provide the full constraint-to-decision-to-architecture pipeline, with templates you can apply to your own constrained creative practice.

### Target Venues

- **XOXO** (Portland) -- independent creators, sustainability, bootstrapping
- **IndieWebCamp** -- independent web, self-hosted infrastructure, POSSE philosophy
- **Eyebeam** (NYC) -- art+tech, institutional critique, systems as creative medium

### Speaker Bio

Systems artist and auteur-producer. Creator of the ORGANVM eight-organ system: 113 repositories across 8 GitHub organizations, built with zero budget, zero team, and a methodology that transmutes constraints into architecture. 49 published essays document the creative process -- including the failures, billing disasters, and course corrections -- in real time. 4,015+ automated tests, 104 CI/CD workflows, 8/17 omega maturity criteria met. 18 years professional experience across creative systems design, college instruction (2,000+ students), and multimedia production. MFA Creative Writing. NYC-based.

### Technical Requirements

- Screen sharing / HDMI output for slides
- No audio required
- Ideal format: 30 min talk + 10 min Q&A
- Adaptable to: workshop (2 hrs with hands-on constraint mapping exercise), lightning talk (10 min)

### Companion Materials

- Essay: "Constraint Alchemy: How Limitations Become Creative Fuel" (published 2026-02-17)
- Architecture Decision Records ADR-001 through ADR-016 (open source)
- Full governance corpus: [organvm-corpvs-testamentvm](https://github.com/meta-organvm/organvm-corpvs-testamentvm)
- Evidence portfolio with verifiable metrics: [evidence-portfolio.md](https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/docs/applications/evidence-portfolio.md)
- Sprint catalog with all 33 completed sprints: constraint-to-architecture traceability

---

## Talk 3: Eight Organs: Creative Practice as Systems Architecture

### Abstract (300 words)

What happens when you model creative practice as a distributed system?

Most artists work in one domain. Most software architects build one product. I built eight organs -- Theory, Art, Commerce, Orchestration, Public Process, Community, Marketing, and Meta-governance -- as a single coordinated system with 113 repositories, enforced dependency rules, and a formal promotion pipeline. The result is not a portfolio. It is an organism, and the architecture decisions that shape it are indistinguishable from the artistic decisions.

The eight-organ model is a dependency graph. Theory (ORGAN-I) produces frameworks that Art (ORGAN-II) consumes and transforms into generative works. Art produces artifacts that Commerce (ORGAN-III) packages into products. The flow is unidirectional: I to II to III, enforced by automated validation with zero back-edge violations across 62 dependency edges. Orchestration (ORGAN-IV) coordinates everything. Public Process (ORGAN-V) observes and documents. Community (ORGAN-VI) and Marketing (ORGAN-VII) distribute. Meta (ORGAN-VIII) governs the governors.

Each organ has its own aesthetic identity (defined in organ-aesthetic.yaml), its own CI/CD workflows, its own promotion criteria. A generative art system in ORGAN-II and a SaaS product in ORGAN-III share the same governance infrastructure, the same registry, the same promotion state machine -- but express entirely different creative intentions through the same architectural constraints. The promotion pipeline (LOCAL, CANDIDATE, PUBLIC_PROCESS, GRADUATED, ARCHIVED) applies equally to a philosophical framework and a commercial web scraper.

This is systems architecture as creative practice. The dependency graph is a compositional constraint, like a harmonic rule in music: it does not limit what you can create -- it shapes what wants to emerge. I will demonstrate the full pipeline from a theoretical concept in ORGAN-I through its transformation into generative art in ORGAN-II and commercial product in ORGAN-III, showing how the architecture itself is the creative methodology.

### Target Venues

- **Processing Community Day** -- creative coding, educational tools, open-source art infrastructure
- **Eyebeam** (NYC) -- art+tech, institutional critique, systems art

### Speaker Bio

Systems artist and auteur-producer working at the intersection of creative infrastructure, governance design, and AI-augmented methodology. Creator of the ORGANVM eight-organ system: 113 repositories across 8 GitHub organizations coordinating theory, generative art, commercial products, governance, public process, community, and marketing through automated governance and a formal promotion state machine. 49 published essays document the creative process in real time. 8/17 omega maturity criteria met, 32-day zero-incident soak test complete. Reference points: Julian Oliver's critical engineering, Nicky Case's Explorable Explanations, Hundred Rabbits' radical transparency. MFA Creative Writing. NYC-based.

### Technical Requirements

- Screen sharing / HDMI output for slides
- Audio helpful but not required (optional: short generative art demo from ORGAN-II repos)
- Ideal format: 30 min talk + 10 min Q&A
- Adaptable to: 45 min deep-dive (with live dependency graph walkthrough), workshop (2 hrs with organ-model design exercise)

### Companion Materials

- Full governance corpus: [organvm-corpvs-testamentvm](https://github.com/meta-organvm/organvm-corpvs-testamentvm)
- Interactive portfolio with generative art: [4444j99.github.io/portfolio](https://4444j99.github.io/portfolio/)
- Public Process essays (49 published): [organvm-v-logos.github.io/public-process](https://organvm-v-logos.github.io/public-process/)
- System dashboard with dependency graph visualization
- Evidence portfolio: [evidence-portfolio.md](https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/docs/applications/evidence-portfolio.md)
- Organ-aesthetic.yaml files defining visual identity cascades per organ

---

## Target Conference CFP Windows (Estimated)

| Conference | Location | Typical CFP Window | Talk Fit |
|------------|----------|-------------------|----------|
| Strange Loop | St. Louis, MO | Apr-Jun (fall conf) | Talk 1 |
| XOXO | Portland, OR | Spring (fall conf) | Talk 1, Talk 2 |
| Processing Community Day | Global/distributed | Varies by chapter, typically spring | Talk 3 |
| IndieWebCamp | Multiple cities | Rolling / event-specific | Talk 2 |
| Eyebeam | New York, NY | Spring open call (varies) | Talk 2, Talk 3 |

## Cross-Reference

- Existing detailed proposals: `conference-proposals/ai-conductor-talk.md`, `conference-proposals/constraint-alchemy-talk.md`
- Canonical identity and metrics: `00-covenant-ark.md`
- Evidence portfolio: `evidence-portfolio.md`
- Application tracker: `04-application-tracker.md`
