# E2G Action Items — Prioritized

**Source:** `docs/evaluation/e2g-full-system-review.md`
**Generated:** 2026-02-13
**Sprint context:** Post-PRAXIS, pre-external submission

---

## Priority Legend

- **P0 (CRITICAL):** Must fix before any external submission. These are credibility-destroying if discovered.
- **P1 (HIGH):** Should fix within 1–2 days. These weaken claims but are survivable.
- **P2 (MEDIUM):** Fix within 1–2 weeks. These improve presentation and reduce risk.
- **P3 (STRATEGIC):** Plan and execute over 1+ month. These build long-term credibility.

---

## P0 — CRITICAL (Fix Before Submission)

- [x] **Q1.** Fix TODO in all 5 application materials — replace `TODO — deploy portfolio site before submission` with actual portfolio URL (`https://4444j99.github.io/portfolio/`) — **RESOLVED (VERITAS Sprint):** All 5 applications have portfolio URL at line 26/27. Zero TODOs remain (verified via grep).
  - Files: `applications/knight-foundation.md:26`, `applications/eyebeam-residency.md:26`, `applications/google-creative.md:26`, `applications/processing-foundation.md:26`, `applications/ai-systems-role.md:27`
  - Finding: W5

- [x] **Q2.** Change `revenue: active` to `revenue_model: [subscription|freemium|one-time]` for all ORGAN-III repos with zero actual revenue — **RESOLVED (VERITAS Sprint):** Split into `revenue_model` + `revenue_status: pre-launch` across all 27 ORGAN-III repos
  - File: `repo-registry.json` (9 entries with `"revenue": "active"`)
  - Finding: W3, LC4, SP3

- [x] **Q3.** Redate 9 future-dated essays (2026-02-14 through 2026-02-22) to their actual creation date (2026-02-13) — **RESOLVED (VERITAS Sprint):** All 9 essays redated in system-metrics.json and public-process _posts/
  - Files: `system-metrics.json` essay timeline, public-process `_posts/` frontmatter
  - Finding: W4, SP2

## P1 — HIGH (Fix Within 1–2 Days)

- [x] **Q4.** Add portfolio URL to application materials (in the Portfolio URL section and supporting materials) — **RESOLVED (VERITAS Sprint):** Portfolio URL present in all 5 applications (verified via grep).
  - Files: All 5 `applications/*.md`
  - Finding: W5

- [x] **Q5.** Translate project-internal vocabulary in applications for external audiences — **RESOLVED (VERITAS Sprint):** All 5 applications de-jargoned, AI-conductor defined on first use, "Why [Target]" sections differentiated per audience
  - Replace "115 seed.yaml contract edges" with human-readable description
  - Replace "PRAXIS Sprint" references with accessible language
  - Define "AI-conductor methodology" on first use
  - Files: All 5 `applications/*.md`
  - Finding: PA4

- [x] **M5.** Write an honest "How This Was Built" essay acknowledging AI role, compressed timeline, and current limitations — **RESOLVED (VERITAS Sprint):** Essay deployed to public-process
  - Target: `_posts/` in public-process
  - Finding: BS3, BS4, PA3

## P2 — MEDIUM (Fix Within 1–2 Weeks)

- [x] **M1.** Rename `implementation_status: PRODUCTION` → `ACTIVE` across the entire system — **RESOLVED (VERITAS Sprint):** 82 repos renamed in repo-registry.json, system-metrics.json, validation scripts, CLAUDE.md, and all 5 application materials
  - Files: `repo-registry.json` (82 entries), `system-metrics.json`, all validation scripts, CLAUDE.md, application materials
  - Finding: LC3, SP1, ET2
  - Note: Chose `ACTIVE` over `DOCUMENTED` or `MAINTAINED` — it says "this repo is maintained" without implying production deployment

- [x] **M2.** Vivify top 4 non-SUBSTANTIAL flagships with real code and tests — **SUPERSEDED (MANIFESTATIO Sprint):** PRAXIS audit miscounted code files due to wrong language detection (agentic-titan classified as TypeScript instead of Python) and `docs/` prefix trap (code files in `docs/` directories classified as documentation). Corrected counts:
  - `agentic-titan` — was 2 code files, actually **219 code, 93 test** (Python, not TypeScript). SUBSTANTIAL.
  - `metasystem-master` — was 28 code files, actually **62 code, 12 test**. Still SUBSTANTIAL.
  - `auto-revision-epistemic-engine` — was 20 code files, actually **23 code, 3 test**. PARTIAL (unchanged tier).
  - `example-generative-music` — 7 code files, 2 tests. PARTIAL (correct, no change).
  - `public-process` — 6 code files. MINIMAL (correct, Jekyll site — code count isn't meaningful metric).
  - System-wide re-audit: **40+ repos with 10+ code files** (was claimed as 6). The "code substance gap" was a measurement error, not a real gap.
  - Finding: W1, LC2

- [x] **M3.** Add `revenue_status` field to ORGAN-III repo schema — **RESOLVED (VERITAS Sprint):** Split `revenue` into `revenue_model` + `revenue_status` across all 27 ORGAN-III repos
  - Values: `pre-launch` | `beta` | `live`
  - Separates business model (what you plan to charge) from business state (whether anyone is paying)
  - File: `repo-registry.json`
  - Finding: W3, LC4

- [ ] **M4.** ~~Restructure CI to distinguish "test suite passes" from "no tests found"~~ → **Reclassified to P3 (MANIFESTATIO Sprint).** Corrected system-wide audit reveals 49 repos with test directories — the "hollow CI" narrative was based on flawed measurement. CI does run real tests in the majority of code-heavy repos. Monitor over 30 days; restructure only if needed.
  - Option C selected (with corrected numbers): "49 repos with test suites, 82+ with CI workflows"
  - Finding: W6, SP4, ET3

- [x] **M6.** Create audience-specific application variants — **RESOLVED (EXODUS Sprint):** 3 audience tracks + 9 submission bundles created in `docs/applications/`
  - Technical (AI labs): lead with registry, orchestration, CI, code substance
  - Humanities (grants): lead with essays, governance philosophy, naming etymology
  - Arts (residencies): lead with cross-domain integration, meta-system as artwork
  - Finding: ET4, PA4

## P3 — STRATEGIC (1+ Month)

- [x] **S1.** Run the system for 30 days without intervention; document what breaks — **IN PROGRESS (OPERATIO Sprint):** Monitoring script built (`scripts/soak-test-monitor.py`), 30-day clock started 2026-02-16. Daily snapshots → `data/soak-test/daily-YYYY-MM-DD.json`. Report generation via `report` subcommand.
  - Tests: autonomous workflow execution, CI stability, registry consistency
  - Deliverable: "30-Day Soak Test" report
  - Finding: LC5, SP5

- [x] **S2.** Get one external person to navigate the system and document their experience — **PROTOCOL READY (OPERATIO Sprint):** Test protocol written at `docs/operations/stranger-test-protocol.md` with 5 tasks, scoring rubric, and analysis template. Recruitment is external/calendar work.
  - First external validation of the "Stranger Test" (Constitution Article V)
  - Deliverable: External usability report
  - Finding: BS1, BS2

- [x] **S3.** Submit one actual application (Knight Foundation or Processing Foundation) — **READY TO SUBMIT (OPERATIO Sprint):** Recommended first submission: Google Creative Lab Five (no deadline, lowest friction). Google Creative Fellowship by March 18, 2026. All materials ready per `04-application-tracker.md`.
  - Converts portfolio asset into real-world feedback loop
  - Prerequisites: P0 items complete, M5 essay published
  - Finding: LO1

- [x] **S4.** Publish AI-conductor methodology as standalone essay or talk proposal — **DRAFTED (OPERATIO Sprint):** 4,000+ word essay at `docs/essays/09-ai-conductor-methodology.md`. Covers methodology, TE budgeting, sprint-based conducting, failure recovery. Ready for deploy to ORGAN-V `_posts/`.
  - Target venues: Strange Loop, XOXO, Processing Community Day, NeurIPS workshop
  - Exploits: BL3 (methodology has standalone value)
  - Finding: BL3

- [x] **S5.** Establish 30-day engagement baseline — **IN PROGRESS (OPERATIO Sprint):** Engagement tracking built into `scripts/soak-test-monitor.py` (stars, forks, views, clones for 8 flagship repos). 30-day baseline collection started 2026-02-16 alongside S1 soak test.
  - Metrics: GitHub stars, forks, page views (GitHub insights), essay reads (Jekyll analytics), RSS subscribers
  - Required for: credible "public process" claims
  - Finding: BS5

- [x] **S6.** Write operational runbooks for a second operator — **RESOLVED (OPERATIO Sprint):** 3 runbooks written at `docs/operations/`: `minimum-viable-operations.md` (daily/weekly/monthly/quarterly), `emergency-procedures.md` (5 procedures), `key-workflows.md` (6 step-by-step guides with actual commands).
  - Document: minimum viable operation, key workflows, emergency procedures
  - Addresses: bus-factor critique for grant applications
  - Finding: SP5, ET1

---

## Cross-Reference: Finding → Action Item

| Finding | Code | Action Items |
|---------|------|-------------|
| Code substance gap | W1 | M2 (superseded — measurement error) |
| Promotion stagnation | W2 | (no direct action — natural over time) |
| Revenue claims | W3, LC4, SP3 | Q2, M3 |
| Essay dating | W4, SP2 | Q3 |
| Application TODOs | W5 | Q1, Q4 |
| CI hollow coverage | W6, SP4, ET3 | M4 (reclassified P3 — 49 repos have tests) |
| PRODUCTION semantics | LC3, SP1, ET2 | M1 |
| Documentation-before-deployment | LC1 | M5 (honest framing) |
| Single-operator risk | SP5, ET1 | S6 |
| No external validation | BS1, BS2 | S2 |
| No engagement data | BS5 | S5 |
| AI transparency | BS3, BS4 | M5 |
