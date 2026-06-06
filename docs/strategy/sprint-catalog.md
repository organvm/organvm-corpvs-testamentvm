# Sprint Catalog — Every Possible Sprint Beyond the 16

**Created:** 2026-02-16
**Author:** @4444j99 (AI-conductor model: human directs, AI generates, human reviews)
**Status:** REFERENCE — This document is a static inventory, not a living roadmap
**Companions:** [`there+back-again.md`](./there+back-again.md) (omega roadmap), [`operational-cadence.md`](../operations/operational-cadence.md) (daily/weekly rhythm), [`rolling-todo.md`](../operations/rolling-todo.md) (active queue)
**Constitution:** [`docs/memory/constitution.md`](../memory/constitution.md) — Articles I-VI govern all specifications

---

> *This catalog names everything that could be done. The operational cadence governs when — and whether — to do it. This is a menu; AP-1 says don't order everything at once.*

---

## How to Read This Document

This document is an **exhaustive inventory** of every sprint-worthy work package that could be executed across the eight-organ system. It is organized into 18 categories covering all 8 organs, all 5 horizons, and all 17 omega criteria.

**This document is NOT:**
- A backlog (there is no priority ordering within categories)
- A roadmap (see [`there+back-again.md`](./there+back-again.md) for that)
- A commitment (listing something here does not mean it will be done)
- A sprint plan (see [`operational-cadence.md`](../operations/operational-cadence.md) AP-1)

**This document IS:**
- A complete map of addressable work
- A reference for weekly planning sessions (operational cadence Part I, Friday retrospective)
- Evidence that the system's scope is understood and bounded
- A menu from which individual tasks are pulled into the weekly rhythm
- One leg of a governance quadrilateral: roadmap (destination) + cadence (rhythm) + catalog (menu) + rolling TODO (queue)

### Conventions

- **Sprint numbers** continue from the 16 construction sprints (01-IGNITION through 16-PLATINUM), starting at 17. Sprint specs for all 33 completed sprints live in `docs/specs/sprints/` with continuous numbering (01–33, no gaps). Sprints 17–33 are now complete (REMEDIUM, SYNCHRONIUM, CONCORDIA, TRIPARTITUM, SUBMISSIO, METRICUM, PUBLICATIO, CANON, INSPECTIO, PROPAGATIO, BETA-VITAE, RECOGNITIO, AUTOMATA, DISTRIBUTIO, FUNDAMEN, SENSORIA, OPERATIO). These numbers are for reference only — the operational cadence discourages named sprints in favor of weekly rhythm.
- **Catalog vs. execution numbering (17–23):** This catalog was written as a hypothetical inventory. When sprints 19–23 were actually executed, some took different names than what the catalog had assigned. The canonical sprint numbers and names are in `docs/specs/sprints/` — those are what actually happened. Catalog items that were displaced (never executed at their catalog number) are marked as unscheduled future work below. For sprints ≥24, catalog numbers are hypothetical references until executed.
- **Effort estimates** assume AI-conductor model (AI generates, human reviews). They are order-of-magnitude only.
- **Horizon mapping** uses H1–H5 from [`there+back-again.md`](./there+back-again.md):
  - **H1** — Prove It Works (Days 1–30)
  - **H2** — Validate Externally (Days 15–90)
  - **H3** — Generate Revenue (Days 30–180)
  - **H4** — Build Community (Days 60–365)
  - **H5** — Achieve Recognition (Days 90–730)
- **Omega criteria** are numbered #1–#17 per the omega roadmap's "Seventeen Omega Criteria" table.

---

## System State Snapshot (2026-02-16)

This catalog was generated against the following state. Numbers will drift; the catalog's structure remains valid.

| Metric | Value |
|--------|-------|
| Registry entries | 97 (87 ACTIVE, 10 ARCHIVED) |
| Repos not cloned locally | 0 (all 97 cloned; SYNCHRONIUM Sprint 18) |
| Deployed essays | 33 on remote (updated Sprint 23: PUBLICATIO) |
| Undeployed essay drafts | 0 ready to deploy (5 already-deployed drafts remain in `docs/essays/` as source copies) |
| ORGAN-III pre-launch | 15 repos with `revenue_status: pre-launch` |
| ORGAN-II zero-code repos | 10 repos with 0 code files |
| ORGAN-VI zero-code repos | 3/3 local repos have 0 code |
| ORGAN-VII zero-code repos | 3/3 local repos have 0 code |
| Failing workflows | None (phantom failures diagnosed; all workflows healthy) |
| Applications submitted | 0 of 13 tracked (9 READY, checklist created) |
| Stranger test | Protocol ready, not executed |
| Soak test | Day 1 of 30 |
| Revenue | $0 |
| Community events | 0 |
| External contributions | 0 |

---

## CATEGORY 1: INFRASTRUCTURE REPAIR

*Fix what's broken before building anything new.*

### Sprint 17: REMEDIUM (Remedy) — RESOLVED

**Fix failing orchestration workflows.** *(Resolved 2026-02-16: All workflows confirmed healthy.)*

Investigation revealed no actual failures:
- `essay-monitor` and `publish-process`: **Phantom failures** — push events triggering schedule-only workflows; latest real scheduled runs succeeded
- `ci.yml` (Python CI): **Already replaced** by Minimal CI; all 31 Minimal CI runs pass
- `validate-dependencies`: **Already fixed** — back-edges removed in CONVERGENCE; latest run passed
- `distribute-content`: 29/29 SKIPPED is **correct behavior** — waiting for `ready-to-distribute` label

No workflow code changes were needed. The "failing" signal was misleading — caused by push triggers on schedule-only workflows, which produce expected failures in GitHub's run history.

| Field | Value |
|-------|-------|
| Effort | ~1 hour (diagnosis only) |
| Horizon | H1 (Prove It Works) |
| Omega criteria | #1, #17 |
| Resolution | Diagnosed as phantom failures; no code changes required |

### Sprint 18: SYNCHRONIUM (Sync) — COMPLETE

**Clone all missing repos locally and sync workspace.** *(Completed 2026-02-16 as part of workspace restructure.)*

All 97 repos cloned to flat `~/Workspace/<org>/<repo>/` layout. 14 missing repos cloned, 8 `.github` org profiles cloned, public-process synced, 68 repos moved from legacy ~/world/ hierarchy, 39 symlinks removed, git remotes converted SSH→HTTPS. 29 GB freed.

| Field | Value |
|-------|-------|
| Effort | ~2 hours |
| Horizon | H1 (operational completeness) |
| Omega criteria | #17 (full local workspace) |
| Resolution | All repos cloned and workspace restructured to flat 2-level layout |

### Sprint 19: CONCORDIA (Registry Reconciliation) — COMPLETE

**Reconcile registry with actual GitHub state.** *(Executed as Sprint 19, 2026-02-16.)*

Registry reconciliation: 6 orphan repos registered (91→97), render-second-amendment deleted locally (14 GB freed), 2 LFS checkout failures fixed, seed.yaml audit (38/86 = 44% coverage).

| Field | Value |
|-------|-------|
| Effort | ~2 hours |
| Horizon | H1 (registry integrity) |
| Omega criteria | Constitution Article I (registry is never wrong) |
| Resolution | Registry reconciled with GitHub — 97 entries, all verified |

### MEMORIA (Memory Correction) — COMPLETE *(unscheduled)*

**Fix stale data across corpus documents.** *(Completed 2026-02-16 as part of Sprint 20 TRIPARTITUM. Originally catalog item 19, displaced by CONCORDIA.)*

13 files updated with ~70 edits: all active documents now reflect 97 repos, 87 ACTIVE, 7 ARCHIVED, correct org counts, and ACTIVE terminology (not PRODUCTION). Includes CLAUDE.md, README.md, application materials, omega roadmap, operational docs, and evaluation docs.

| Field | Value |
|-------|-------|
| Effort | ~1.5 hours |
| Horizon | H1 (data integrity) |
| Omega criteria | Constitution Article I (registry is never wrong) |
| Resolution | All 13 active documents reconciled with repo-registry.json |

### Sprint 31: FUNDAMEN (Foundation) — **COMPLETE** (2026-02-17)

**Infrastructure hardening for Organs V/VI/VII/Meta.** *(Executed as Sprint 31, 2026-02-17.)*

Synced 6 stale local repos (ORGAN-VI/VII), added README/CI/seed.yaml to alchemia-ingestvm (last repo without README), added real HTTP POST logic to social-automation (Mastodon + Discord via urllib.request), enhanced test coverage across all 4 prototype repos (60→85+ tests).

| Field | Value |
|-------|-------|
| Effort | ~2 hours |
| Horizon | H1 (infrastructure integrity) |
| Omega criteria | #1 (system stability), #17 (CI health) |
| Resolution | All 97 repos have READMEs, 0 stale locals, ORGAN-VI/VII have real implementations |

### Sprint 32: SENSORIA (Perception) — **COMPLETE** (2026-02-17)

**Autonomous perception layer — full seed.yaml coverage, stale-detection, metrics hardening.** *(Executed as Sprint 32, 2026-02-17.)*

Gave the system a sensory layer: fixed stale system-metrics.json (29→32 sprints), deployed seed.yaml to all 41 missing repos (50%→100% coverage), wrote stale-detector.py + weekly workflow to autonomously detect metric drift, fixed propagation false-positives in concordance.md.

| Field | Value |
|-------|-------|
| Effort | ~2 hours |
| Horizon | H1 (autonomous infrastructure) |
| Omega criteria | #1 (system stability), #6 (system architecture) |
| Resolution | 100% seed.yaml coverage, stale-detection autonomous, metrics current |

---

## CATEGORY 2: DOCUMENTATION COMPLETION

*Fill the gaps in the historical and architectural record.*

### Sprint 20: TRIPARTITUM (Three-Part Sprint) — COMPLETE

**Combined REMEDIUM + MEMORIA + ANNOTATIO into a single execution sprint.** *(Executed as Sprint 20, 2026-02-16.)*

Three work streams in one sprint: (1) stale metrics corrected across 13 files (~70 edits), (2) 19 retrospective sprint specs written in `docs/specs/sprints/`, (3) all active docs aligned with repo-registry.json. Each spec follows a consistent template: Objective, Delivered, Key Decisions, Metrics Delta, Lessons.

| Field | Value |
|-------|-------|
| Effort | ~3 hours |
| Horizon | H1 (data integrity), H2 (evidence for applications), H5 (methodological authority) |
| Omega criteria | #6, #14, Constitution Article I |
| Resolution | 19 specs written, 13 documents updated, all docs aligned with registry |

### ANNOTATIO (Annotation) — COMPLETE *(unscheduled)*

**Write sprint specs for all completed sprints.** *(Completed 2026-02-16 as part of Sprint 20 TRIPARTITUM. Originally catalog item 20, displaced by TRIPARTITUM.)*

19 retrospective specs written in `docs/specs/sprints/`: Gap-Fill, Platinum, Sprints 1–14 (IGNITION through OPERATIO), and Sprints 17–19 (REMEDIUM, SYNCHRONIUM, CONCORDIA). Each spec follows a consistent template: Objective, Delivered, Key Decisions, Metrics Delta, Lessons.

| Field | Value |
|-------|-------|
| Effort | ~1.5 hours (template + 19 specs) |
| Horizon | H2 (evidence for applications), H5 (methodological authority) |
| Omega criteria | #6, #14 (methodology documentation) |
| Resolution | 19 specs in `docs/specs/sprints/`, plus 20-tripartitum.md for this sprint itself |

### DECISIO (Decision Records) *(unscheduled)*

**Write ADRs for all major architectural decisions.**

- Only 2 ADRs exist (001-initial-architecture, 002-integration-patterns)
- Missing ADRs: organ naming scheme, registry schema design, promotion state machine, dependency direction rule (I→II→III), essay dating policy, revenue field split (VERITAS), PRODUCTION→ACTIVE rename, SKELETON handling, cross-org dispatch architecture, AI-conductor methodology, soak test design, billing guardrails

| Field | Value |
|-------|-------|
| Effort | ~6–8 hours (12–15 ADRs) |
| Horizon | H1 (operational maturity), H5 (shows rigorous engineering) |
| Omega criteria | #16 (bus factor — ADRs help second operators understand decisions) |
| Tracking | [Issue #10](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/10) |

### CANON (Canon Cleanup) — COMPLETE *(unscheduled)*

**Reconcile stale documentation with current reality.** *(Executed as Sprint 24, 2026-02-16. Originally catalog item 22, displaced by METRICUM.)*

Catalog numbering reconciliation (this file), historical document headers added to 4 implementation-era documents. See Sprint 24 spec for details.

| Field | Value |
|-------|-------|
| Effort | ~1 hour |
| Horizon | H1 (documentation integrity) |
| Omega criteria | #2 (stranger test — stale docs confuse strangers) |
| Resolution | Catalog reconciled, 4 historical headers added, sprint spec written |

---

## CATEGORY 3: CONTENT & PUBLISHING

*Deploy essays, activate distribution, build the audience.*

### Sprint 22: METRICUM (Metrics) — COMPLETE

**Build metrics variable system for the corpus.** *(Executed as Sprint 22, 2026-02-16.)*

Metrics variable system: `calculate-metrics.py` computes live counts from registry + GitHub API, `metrics-variables.json` stores them, `propagate-metrics.py` finds and replaces stale values across all active documents. Ensures metrics consistency without manual updates.

| Field | Value |
|-------|-------|
| Effort | ~2 hours |
| Horizon | H1 (data integrity), H2 (accurate application materials) |
| Omega criteria | Constitution Article I (registry is never wrong) |
| Resolution | 3 scripts + JSON store deployed, metrics propagated across 20+ files |

### Sprint 23: PUBLICATIO (Publication) — COMPLETE

**Deploy remaining essay drafts and write new essays.** *(Completed 2026-02-16.)*

4 essays deployed (29→33): 1 existing draft (promotions-in-practice) + 3 new essays (how-to-think-about-autonomous-systems, why-the-organ-model-separates-commerce-from-theory, governance-frameworks-for-artists). Metrics propagated across 18 files.

| Field | Value |
|-------|-------|
| Effort | ~3 hours |
| Horizon | H2 (#6, #7), H5 (#14) |
| Omega criteria | #6 (AI-conductor essay — already deployed), feeds #14 |
| Resolution | 33 essays deployed, ~398K+ total words |

### Sprint 24: DISTRIBUTIO (Distribution Infrastructure) — **COMPLETE** (2026-02-17)

**Set up and activate POSSE distribution channels.** *(Executed as Sprint 30, 2026-02-17.)*

Backfill distribution workflow created (3/week drip-feed of 35-essay backlog), essay-monitor enhanced with frontmatter extraction, distribute-content upgraded with rich metadata parsing (excerpt, tags-as-hashtags, essay URLs). All social posts now use actual essay content instead of slug-derived titles and issue URLs. See Sprint 30 spec for details.

| Field | Value |
|-------|-------|
| Effort | ~2 hours (AI-conductor model) |
| Horizon | H4 (#13 organic inbound links), H5 (#14 recognition) |
| Omega criteria | #13 (organic inbound link requires distribution first) |
| Resolution | Backfill pipeline active, 3 essays/week, ~12 weeks to complete backlog |

### Sprint 25: RSS-AUTOMATIO (RSS & Newsletter)

**Set up automated content distribution.**

- Verify Jekyll RSS feed works on public-process
- Set up email newsletter (Ghost, Buttondown, or similar)
- Connect essay publishing to automatic newsletter sends

| Field | Value |
|-------|-------|
| Effort | ~2–4 hours |
| Horizon | H4 (distribution network) |
| Omega criteria | #13 |
| Tracking | [Issue #11](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/11) |

---

## CATEGORY 4: PRODUCT & REVENUE (ORGAN-III)

*Each ORGAN-III pre-launch product is a potential beta sprint. Sorted by code substance (descending).*

> **Note (Sprint 25):** The INSPECTIO assessment (`docs/implementation/organ-iii-beta-assessment.md`) evaluated the top 5 repos and recommends life-my--midst--in as the first beta product. See the product brief at `docs/implementation/organ-iii-beta-brief.md`.

### Sprint 26: BETA-UNIVERSALIS (Universal Mail Automation Beta)

**Ship `universal-mail--automation` — 1,272 code files, highest code substance.**

- Assess feature completeness, deployment readiness
- Deploy to a domain, basic UI
- Create user onboarding flow
- Revenue model: subscription

| Field | Value |
|-------|-------|
| Effort | ~20–40 hours depending on state |
| Horizon | H3 (#8, #9, #10) |
| Omega criteria | #8 (product live), #9 (revenue_status: live), #10 (MRR) |
| Tracking | [Issue #12](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/12) |

### Sprint 27: BETA-VITAE (Life-My-Midst-In Beta) — **COMPLETE** (2026-02-16)

**Ship `life-my--midst--in` — 1,694 code files.** *(Completed 2026-02-16.)*

DB provisioned on Neon (44 tables, seeded). 3 migration bugs fixed (016_settings PK expression, 002_masks missing column, seed ordering). Auth prefix bug fixed. render.yaml duplicate-services-key fixed. DEPLOY.md written. Render Blueprint ready for one-click deploy. 2 essays deployed (#34 product update, #35 sprint retrospective). 291 tests pass, 7/7 packages build.

| Field | Value |
|-------|-------|
| Effort | ~20–40 hours |
| Horizon | H3 |
| Resolution | Neon DB live, 44 tables, DEPLOY.md + render.yaml ready, 2 essays deployed (33→35) |

### Sprint 28: BETA-SCRAPPER (Public Record Data Scrapper Beta)

**Ship `public-record-data-scrapper` — 497 code files, omega roadmap's recommended first candidate.**

- Branch-protected (requires PRs)
- Revenue model: subscription
- Highest portfolio relevance in ORGAN-III

| Field | Value |
|-------|-------|
| Effort | ~20–40 hours |
| Horizon | H3 (#8, #9, #10) |
| Omega criteria | #8, #9, #10 |
| Tracking | [Issue #13](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/13) |

### Sprint 29: BETA-AETHERIA (Classroom RPG Aetheria Beta)

**Ship `classroom-rpg-aetheria` — 211 code files.**

- Revenue model: subscription
- Strong case study documentation

| Field | Value |
| Tracking | [Issue #14](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/14) |
|-------|-------|
| Effort | ~15–30 hours |
| Horizon | H3 |

### Sprint 30: BETA-FAMILIARIS (Fetch Familiar Friends Beta)

**Ship `fetch-familiar-friends` — 188 code files.**

- Revenue model: freemium
- Cron workflow disabled during ILLUSTRATIO

| Field | Value |
| Tracking | [Issue #15](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/15) |
|-------|-------|
| Effort | ~15–30 hours |
| Horizon | H3 |

### Sprint 31: BETA-IMPERIUM (Sovereign Ecosystem Real Estate Beta)

**Ship `sovereign-ecosystem--real-estate-luxury` — 145 code files.**

- Revenue model: subscription

| Field | Value |
| Tracking | [Issue #16](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/16) |
|-------|-------|
| Effort | ~15–30 hours |
| Horizon | H3 |

### Sprint 32: BETA-BELLUM (My Block Warfare Beta)

**Ship `my-block-warfare` — 118 code files.**

- Revenue model: freemium

| Field | Value |
| Tracking | [Issue #17](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/17) |
|-------|-------|
| Effort | ~15–30 hours |
| Horizon | H3 |

### Sprint 33: BETA-FUTURUM (Trade Perpetual Future Beta)

**Ship `trade-perpetual-future` — 104 code files.**

- Revenue model: subscription
- Financial product — extra regulatory/compliance considerations

| Field | Value |
| Tracking | [Issue #18](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/18) |
|-------|-------|
| Effort | ~20–40 hours (compliance adds overhead) |
| Horizon | H3 |

### Sprint 34: BETA-CONVIVIUM (Search Local Happy Hour Beta)

**Ship `search-local--happy-hour` — 78 code files.**

- Revenue model: freemium

| Field | Value |
| Tracking | [Issue #19](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/19) |
|-------|-------|
| Effort | ~10–20 hours |
| Horizon | H3 |

### Sprint 35: BETA-LUDUS (Gamified Coach Interface Beta)

**Ship `gamified-coach-interface` — 44 code files.**

- Revenue model: subscription

| Field | Value |
| Tracking | [Issue #20](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/20) |
|-------|-------|
| Effort | ~10–20 hours |
| Horizon | H3 |

### Sprint 36: BETA-NUNTIUS (The Actual News Beta)

**Ship `the-actual-news` — 15 code files.**

- Revenue model: subscription
- Minimal code substance — may need significant development

| Field | Value |
| Tracking | [Issue #21](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/21) |
|-------|-------|
| Effort | ~30–50 hours |
| Horizon | H3 |

### Sprint 37: BETA-VESTIS (Your Fit Tailored Beta)

**Ship `your-fit-tailored` — 6 code files.**

- Revenue model: subscription
- Very little code — essentially needs to be built from scratch

| Field | Value |
| Tracking | [Issue #22](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/22) |
|-------|-------|
| Effort | ~40–60 hours |
| Horizon | H3 |

### Sprint 38: BETA-PATER (My Father Mother Beta)

**Ship `my--father-mother` — 3 code files.**

- Revenue model: one-time purchase
- Essentially empty — needs full build

| Field | Value |
| Tracking | [Issue #23](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/23) |
|-------|-------|
| Effort | ~40–60 hours |
| Horizon | H3 |

### Sprint 39: BETA-CAMERA (Multi-Camera Livestream Beta)

**Ship `multi-camera--livestream--framework` — 0 code files (local).**

- Revenue model: subscription
- Empty locally — may have code on remote

| Field | Value |
| Tracking | [Issue #24](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/24) |
|-------|-------|
| Effort | ~50–80 hours |
| Horizon | H3 |

### Sprint 40: MERCATURA (Payment Integration)

**Integrate payment processing across the first beta product.**

- Stripe or equivalent setup
- Pricing page, terms of service, privacy policy
- Change `revenue_status` from `pre-launch` → `beta` → `live`
- First dollar milestone

| Field | Value |
| Tracking | [Issue #25](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/25) |
|-------|-------|
| Effort | ~8–16 hours per product |
| Horizon | H3 (#9, #10) |
| Omega criteria | #9 (revenue_status: live), #10 (MRR ≥ operating costs) |

---

## CATEGORY 5: EXTERNAL VALIDATION

*Submit the system to external audiences.*

### Sprint 41 → Sprint 21: SUBMISSIO (Application Blitz) — COMPLETE

**Verify application metrics and create submission checklist.** *(Prep executed as Sprint 21, 2026-02-16. Actual submissions are human work tracked in `docs/applications/08-submission-checklist.md`.)*

All 9 bundles verified with current metrics — 97 repos, 398K+ words, 33 essays. Submission checklist created. Human form-filling is the remaining step (not AI-conductor work).

- 7 job applications with verified cover letters (Anthropic ×2, OpenAI, Together AI, HuggingFace, Cohere, Runway)
- Google Creative Lab Five (no deadline, ready now)
- Google Creative Fellowship (March 18, 2026 deadline — page shows "Coming soon!" as of Feb 16)

| Field | Value |
|-------|-------|
| Effort | ~1 hour (verification + checklist) |
| Horizon | H2 (#5, #7) |
| Omega criteria | #5 (≥1 application submitted), feeds #7 (external feedback) |
| Resolution | Prep complete 2026-02-16 — metrics verified, checklist created. Human submissions pending. |

### Sprint 42: PEREGRINUS (Stranger Test Execution)

**Recruit participant and execute the stranger test.**

- Find 1 qualifying participant (competent developer, no prior exposure)
- Administer 5-task protocol from `stranger-test-protocol.md`
- Score results against rubric
- Document findings and fix identified issues

| Field | Value |
| Tracking | [Issue #26](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/26) |
|-------|-------|
| Effort | ~4–8 hours (recruitment + administration + analysis) |
| Horizon | H1 (#2), H2 (#7) |
| Omega criteria | #2 (stranger test ≥80%), feeds #4 (runbook validation), #16 (bus factor) |

### Sprint 43: PETITIO (Grant Applications)

**Write and submit grant applications for upcoming deadlines.**

- Eyebeam "Speculating on Plurality" (Spring 2026, TBA)
- Processing Foundation Fellowship (~April–May 2026)
- Knight Foundation Art+Tech (June 20, 2026 — verify geographic eligibility first)
- NEA GAP 2 (July 9, 2026 — requires fiscal sponsor)
- Creative Capital, MAP Fund, Rhizome as alternatives

| Field | Value |
| Tracking | [Issue #27](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/27) |
|-------|-------|
| Effort | ~8–16 hours per application × 4–6 applications |
| Horizon | H2 (#5, #7), H5 (#14) |
| Omega criteria | #5, #7, #14 (recognition through grant award) |

### Sprint 44: TESTIMONIUM (Feedback Collection)

**Systematically collect external feedback on the system.**

- Structure feedback templates for different audiences (developers, artists, grant reviewers)
- Reach out to 5–10 people for structured reviews
- Compile feedback synthesis document

| Field | Value |
| Tracking | [Issue #28](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/28) |
|-------|-------|
| Effort | ~6–10 hours |
| Horizon | H2 (#7) |
| Omega criteria | #7 (≥3 pieces of external feedback) |

---

## CATEGORY 6: COMMUNITY (ORGAN-VI)

*Build the community infrastructure and host events.*

### Sprint 45: CONVIVIUM (First Salon)

**Plan and host the first ORGAN-VI salon or reading group.**

- All 3 local ORGAN-VI repos have 0 code — purely organizational
- Choose format: reading group (lower barrier) vs. salon (more ambitious)
- Select topic, recruit 3–5 participants, set date
- Host the event, document it

| Field | Value |
| Tracking | [Issue #29](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/29) |
|-------|-------|
| Effort | ~8–12 hours (planning + hosting + documentation) |
| Horizon | H4 (#11) |
| Omega criteria | #11 (≥2 salons with external participants — this is the first) |

### Sprint 46: CONVIVIUM-II (Second Salon)

**Host a second salon to meet the omega criterion.**

- Different topic or format from the first
- Iterate on lessons from Sprint 45

| Field | Value |
| Tracking | [Issue #30](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/30) |
|-------|-------|
| Effort | ~6–10 hours |
| Horizon | H4 (#11) |
| Omega criteria | #11 (≥2 requires two events) |

### Sprint 47: HOSPITIUM (Contributor Onboarding)

**Prepare the system for external contributors.**

- Write system-wide CONTRIBUTING.md guide
- Create "good first issues" across 3–5 repos
- Tag issues with appropriate labels
- Write contributor onboarding documentation
- Community guidelines / code of conduct review

| Field | Value |
| Tracking | [Issue #31](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/31) |
|-------|-------|
| Effort | ~4–8 hours |
| Horizon | H4 (#12) |
| Omega criteria | #12 (≥3 external contributions — this creates the pathway) |

### Sprint 48: FORUM (Community Infrastructure)

**Build community communication infrastructure.**

- Set up Discord server (or choose platform)
- Create channels mapped to organs
- Write channel descriptions and pinned messages
- Invite initial community members

| Field | Value |
| Tracking | [Issue #32](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/32) |
|-------|-------|
| Effort | ~4–6 hours |
| Horizon | H4 (#12, #13) |

---

## CATEGORY 7: CREATIVE WORK (ORGAN-I / ORGAN-II)

*Advance the theory and art the system was built to protect.*

### Sprint 49: THEORIA (Theory Development)

**Advance ORGAN-I theoretical work.**

- `recursive-engine--generative-entity` (997 code files) — extend the framework
- `organon-noumenon--ontogenetic-morphe` (1,551 code files) — develop the ontology
- `narratological-algorithmic-lenses` (4,743 code files) — advance the methodology
- Write new theory that produces citable artifacts

| Field | Value |
| Tracking | [Issue #33](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/33) |
|-------|-------|
| Effort | ~20–40 hours (ongoing creative work, not a fixed deliverable) |
| Horizon | H5 (#14 — intellectual contribution) |
| Omega criteria | #14 (recognition through citation or adoption) |

### Sprint 50: VIVIFICATIO (Vivify Empty ORGAN-II Repos)

**Add real creative code to ORGAN-II repos that are ACTIVE but empty.**

- 10 repos with 0 code files: artist-toolkit-and-templates, client-sdk, academic-publication, life-betterment-simulation, universal-waveform-explorer, shared-remembrance-gateway, chthon-oneiros, krypto-velamen, card-trade-social (ORGAN-III but 0 code)
- 5 repos with 1–7 code files: example-generative-music (5), example-choreographic-interface (3), example-theatre-dialogue (3), audio-synthesis-bridge (7), example-generative-visual (2, ARCHIVED)
- These are ACTIVE in the registry but have no code substance — the VERITAS honesty standard questions this

| Field | Value |
| Tracking | [Issue #34](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/34) |
|-------|-------|
| Effort | ~4–8 hours per repo × 15 repos = ~60–120 hours total |
| Horizon | H1 (registry honesty), H4 (creative artifacts attract community) |
| Omega criteria | Constitution Article I (registry accuracy) |

### Sprint 51: POIESIS (Create Art)

**Actually make creative work using ORGAN-II infrastructure.**

- Generative music compositions
- Interactive installations
- Performance scripts
- Choreographic interfaces
- AI collaboration pieces

| Field | Value |
| Tracking | [Issue #35](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/35) |
|-------|-------|
| Effort | Unbounded (this is the ongoing creative practice the system protects) |
| Horizon | H4 (creative artifacts), H5 (recognition through art) |
| Omega criteria | #14 (intellectual/creative contribution) |

---

## CATEGORY 8: PORTFOLIO & PRESENTATION

*Update how the system presents itself to external audiences.*

### Sprint 52: RENOVATIO (Portfolio Refresh)

**Update portfolio site with current state.**

- 19 curated projects — are they still current?
- Add OPERATIO Sprint outcomes (soak test, runbooks)
- Update system metrics (may be stale since ILLUSTRATIO)
- Ensure all project links resolve

| Field | Value |
| Tracking | [Issue #36](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/36) |
|-------|-------|
| Effort | ~2–4 hours |
| Horizon | H2 (#15), H5 |
| Omega criteria | #15 (portfolio updated with external validation) |

### Sprint 53: DEMONSTRATIO (Demo Creation)

**Create demonstrations for external audiences.**

- Record system walkthrough video (for grant applications)
- Build interactive demo for portfolio site
- Create "3-minute pitch" materials
- Screenshot gallery of key repos and workflows

| Field | Value |
| Tracking | [Issue #37](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/37) |
|-------|-------|
| Effort | ~8–16 hours |
| Horizon | H2, H5 |
| Omega criteria | Strengthens #5, #14 |

### Sprint 54: CURRICULO (Resume/CV Update)

**Update application materials with post-construction evidence.**

- Resume page at portfolio site may need updates
- Add soak test results, essay count, code audit numbers
- Update narrative to reflect validation phase

| Field | Value |
| Tracking | [Issue #38](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/38) |
|-------|-------|
| Effort | ~2–3 hours |
| Horizon | H2 |

---

## CATEGORY 9: QUALITY & TESTING

*Strengthen the system's empirical foundations.*

### Sprint 55: PROBATIO (Test Infrastructure)

**Improve CI/test coverage across the system.**

- Address M4 (distinguish "tests pass" from "no tests found")
- Audit which repos run real tests vs. structural-only CI
- Add meaningful tests to key ORGAN-III product repos
- Target: every repo with 10+ code files should have real test execution in CI

| Field | Value |
| Tracking | [Issue #39](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/39) |
|-------|-------|
| Effort | ~12–24 hours |
| Horizon | H1 (system integrity) |
| Omega criteria | #1 (soak test — CI health is a soak test signal) |

### Sprint 56: SECURITAS (Security Audit)

**Security audit across all repos.**

- Review CodeQL findings (CodeQL runs on orchestration-start-here)
- Check for exposed secrets, vulnerable dependencies
- Update all Dependabot PRs across system
- Review security policies (SECURITY.md files)

| Field | Value |
| Tracking | [Issue #40](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/40) |
|-------|-------|
| Effort | ~8–16 hours |
| Horizon | H1 |

### Sprint 57: ACCESSIBILITAS (Accessibility)

**Accessibility audit of public-facing properties.**

- Portfolio site accessibility review (WCAG 2.1 AA)
- Public-process Jekyll site accessibility
- ORGAN-III product accessibility (when products ship)

| Field | Value |
| Tracking | [Issue #41](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/41) |
|-------|-------|
| Effort | ~4–8 hours per property |
| Horizon | H4 (community inclusivity) |

---

## CATEGORY 10: AUTOMATION & TOOLING

*Build tools that reduce operator dependency.*

### Sprint 58: INSTRUMENTUM (Developer Tooling) — **COMPLETE** (2026-02-17)

**Build CLI tools for common operations.** *(Executed as part of Sprint 33 OPERATIO batch, 2026-02-17.)*

Unified `scripts/organ-cli.py` with 8 subcommands: registry show/validate/update, metrics refresh, invoke, soak status, deploy essay, pulse. Registry validator checks required fields, status enums, ORGAN-III revenue fields, and dependency back-edges.

| Field | Value |
|-------|-------|
| Effort | ~30 min (AI-conductor) |
| Horizon | H1 (operational maturity) |
| Omega criteria | #16 (bus factor — tools reduce operator dependency) |
| Resolution | organ-cli.py deployed with 8 subcommands, stdlib-only |

### Sprint 59: AUTOMATIA (Pipeline Automation) — **COMPLETE** (2026-02-17)

**Automate manual workflows.** *(Essay auto-deploy executed as part of Sprint 33 OPERATIO batch, 2026-02-17.)*

Essay auto-deploy pipeline: `scripts/essay-deploy.py` scans docs/essays/ for ready essays, compares against remote _posts/, pushes via gh API. `.github/workflows/essay-deploy.yml` triggers on push when essays change. Closes the last manual step in the essay lifecycle.

| Field | Value |
|-------|-------|
| Effort | ~30 min (AI-conductor) |
| Horizon | H1 (#17 autonomous operation), H4 (distribution) |
| Omega criteria | #17 (30+ days without intervention) |
| Resolution | Essay lifecycle fully autonomous: author → detect → distribute |

### Sprint 60: OBSERVATIO (Monitoring Dashboard) — **COMPLETE** (2026-02-17)

**Build system health dashboard.** *(Executed as part of Sprint 33 OPERATIO batch, 2026-02-17.)*

Static HTML dashboard (`scripts/generate-dashboard.py`) reads soak-test snapshots and system-metrics.json, generates self-contained HTML with inline SVG charts. CMYK design, VIGILIA progress bar, organ distribution, validation/CI/engagement trends. Integrated into system-pulse-weekly.yml.

| Field | Value |
|-------|-------|
| Effort | ~30 min (AI-conductor) |
| Horizon | H1 (operational visibility) |
| Resolution | data/dashboard/index.html generated weekly, committed alongside pulse report |

---

## CATEGORY 11: GOVERNANCE & SCHEMA

*Evolve the system's self-governance mechanisms.*

### Sprint 61: CONSTITUTIO (Constitutional Review)

**Review and potentially amend the constitution.**

- Are Articles I–VI still serving the system?
- Do Amendments A–D need updates based on post-construction reality?
- Should new articles be added (community governance, revenue policy)?

| Field | Value |
| Tracking | [Issue #42](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/42) |
|-------|-------|
| Effort | ~4–6 hours |
| Horizon | H1 (governance maturity) |
| Omega criteria | Supports all criteria through governance clarity |

### Sprint 62: SCHEMA-EVOLUTIO (Registry Schema v1.0)

**Evolve registry from schema v0.5 to v1.0.**

- Add community metrics fields (stars, forks, contributors)
- Add engagement data fields
- Add revenue tracking fields (current MRR, lifetime revenue)
- Add soak test health status per repo
- Formalize schema with JSON Schema validation

| Field | Value |
| Tracking | [Issue #43](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/43) |
|-------|-------|
| Effort | ~8–12 hours |
| Horizon | H1, H3 |

### Sprint 63: REGULA (Governance Rules Update)

**Update governance-rules.json for post-construction era.**

- Review promotion criteria (still relevant?)
- Add revenue governance rules for ORGAN-III
- Add community governance rules for ORGAN-VI
- Update dependency validation rules if needed

| Field | Value |
| Tracking | [Issue #44](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/44) |
|-------|-------|
| Effort | ~4–6 hours |
| Horizon | H1 |

---

## CATEGORY 12: SOAK TEST & MONITORING

*Validate autonomous operation empirically.*

### Sprint 64: VIGILIA (30-Day Soak Test Completion)

**Complete the soak test and generate the report.**

- Mostly passive (30 calendar days of data collection)
- Active work: ensure daily snapshots run, investigate any incidents
- Generate the 30-day report at conclusion
- Document all incidents with post-mortems

| Field | Value |
| Tracking | [Issue #45](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/45) |
|-------|-------|
| Effort | ~2–4 hours active (over 30 days) + ~2 hours for report |
| Horizon | H1 (#1, #3, #17) |
| Omega criteria | #1 (soak test passes), #3 (engagement baseline), #17 (autonomous operation) |

### Sprint 65: VIGILIA-II (Extended Soak Test)

**If the 30-day soak test reveals issues, run a remediation + re-test cycle.**

- Fix issues found in Sprint 64
- Run a second 30-day cycle
- Compare results

| Field | Value |
| Tracking | [Issue #46](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/46) |
|-------|-------|
| Effort | ~4–8 hours active + 30 calendar days |
| Horizon | H1 |
| Contingent on | Sprint 64 results |

---

## CATEGORY 13: CONFERENCES & TALKS

*Build authority through public speaking.*

### Sprint 66: ORATIO (Conference Proposals)

**Write and submit conference talk proposals.**

- Strange Loop, XOXO, Processing Community Day, NeurIPS workshop
- Write abstract, bio, talk outline for each

| Field | Value |
| Tracking | [Issue #47](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/47) |
|-------|-------|
| Effort | ~4–6 hours per proposal × 3–4 proposals |
| Horizon | H5 (#14) |
| Omega criteria | #14 (recognition through invited talk) |

### Sprint 67: PRAELECTIO (Talk Preparation)

**Prepare actual conference presentation.**

- Write full talk (30–45 min)
- Create slides/visual materials
- Practice delivery

| Field | Value |
| Tracking | [Issue #48](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/48) |
|-------|-------|
| Effort | ~16–24 hours |
| Horizon | H5 |
| Contingent on | Sprint 66 acceptance |

---

## CATEGORY 14: PARTNERSHIPS & NETWORKING

*Connect the system to the broader ecosystem.*

### Sprint 68: FOEDUS (Partnership Outreach)

**Identify and contact potential institutional partners.**

- Academic departments using related methodologies
- Other practitioners with similar multi-repo architectures
- Art-tech organizations (Rhizome, Eyebeam network, Processing community)
- AI labs with open-source mandates (for methodology adoption)

| Field | Value |
| Tracking | [Issue #49](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/49) |
|-------|-------|
| Effort | ~8–12 hours |
| Horizon | H4 (#12, #13), H5 (#14) |
| Omega criteria | #12 (external contributions), #14 (recognition) |

### Sprint 69: MENTORIA (Mentorship Network)

**Build mentorship connections for the organ model.**

- Connect with practitioners in overlapping fields
- Offer the AI-conductor methodology for adoption/feedback
- Participate in relevant communities as contributor (not just broadcaster)

| Field | Value |
| Tracking | [Issue #50](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/50) |
|-------|-------|
| Effort | ~4–8 hours (ongoing) |
| Horizon | H4, H5 |

---

## CATEGORY 15: LEGAL & COMPLIANCE

*Legal prerequisites for revenue and community.*

### Sprint 70: IUSTITIA (Legal Foundation)

**Legal infrastructure for revenue-generating products.**

- Terms of Service for ORGAN-III products
- Privacy Policy (required for any product collecting data)
- Review LICENSE files across all repos (are they appropriate?)
- GDPR/CCPA compliance assessment for any product with users

| Field | Value |
| Tracking | [Issue #51](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/51) |
|-------|-------|
| Effort | ~8–16 hours |
| Horizon | H3 (prerequisite for revenue) |
| Omega criteria | Prerequisite for #8, #9 |

### Sprint 71: PROPRIETAS (IP Protection)

**Intellectual property documentation.**

- Document the organ model as a methodology (for citation protection)
- Ensure AI-conductor methodology is properly attributed
- Review any third-party code dependencies for license compliance

| Field | Value |
| Tracking | [Issue #52](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/52) |
|-------|-------|
| Effort | ~4–8 hours |
| Horizon | H5 |

---

## CATEGORY 16: DESIGN & UX

*Visual and navigational quality across public surfaces.*

### Sprint 72: FORMA (Design System Extension)

**Extend CMYK design system to products.**

- Create shared design tokens (colors, typography, spacing)
- Build component library for ORGAN-III products
- Apply consistent design language across public-facing properties

| Field | Value |
| Tracking | [Issue #53](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/53) |
|-------|-------|
| Effort | ~12–20 hours |
| Horizon | H3 (product quality), H4 (brand recognition) |

### Sprint 73: NAVIGATIO (Navigation/UX Improvement)

**Improve system navigation for external users.**

- Based on stranger test results (Sprint 42)
- Improve org profile READMEs for discoverability
- Create a "system map" or visual navigation aid
- Improve cross-references between repos

| Field | Value |
| Tracking | [Issue #54](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/54) |
|-------|-------|
| Effort | ~8–12 hours |
| Horizon | H2, H4 |
| Contingent on | Sprint 42 results |

---

## CATEGORY 17: DATA & ANALYTICS

*Measure what matters.*

### Sprint 74: ANALYTICA (Analytics Setup)

**Set up proper analytics beyond GitHub Insights.**

- Plausible/Fathom for portfolio site (privacy-respecting)
- Jekyll analytics for public-process
- Social media analytics tracking
- Define key metrics and tracking cadence

| Field | Value |
| Tracking | [Issue #55](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/55) |
|-------|-------|
| Effort | ~4–8 hours |
| Horizon | H1 (#3 engagement baseline), H4 |

### Sprint 75: DOSSIER (Evidence Portfolio)

**Compile evidence portfolio for applications.**

- Screenshots of green CI runs
- Soak test data visualizations
- Engagement trend charts
- Code substance statistics
- Before/after comparisons

| Field | Value |
| Tracking | [Issue #56](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/56) |
|-------|-------|
| Effort | ~4–6 hours |
| Horizon | H2 (#5, #7) |

---

## CATEGORY 18: BACKUP & RESILIENCE

*Ensure the system survives adverse events.*

### Sprint 76: PRAESIDIUM (Backup & DR)

**Backup and disaster recovery infrastructure.**

- Verify all repos are backed up (Backblaze already runs)
- Document recovery procedures
- Test recovery from repo deletion scenario
- Archive critical data outside GitHub

| Field | Value |
| Tracking | [Issue #57](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/57) |
|-------|-------|
| Effort | ~4–8 hours |
| Horizon | H1 (operational maturity) |

---

## APPENDIX A: Sprint Count by Category

| # | Category | Sprints | Notes |
|---|----------|---------|-------|
| 1 | Infrastructure Repair | 4 | 17 REMEDIUM, 18 SYNCHRONIUM, 19 CONCORDIA + MEMORIA (unscheduled) |
| 2 | Documentation Completion | 3 | 20 TRIPARTITUM + ANNOTATIO (unscheduled), DECISIO (unscheduled), CANON (unscheduled, executed as Sprint 24) |
| 3 | Content & Publishing | 4 | 22 METRICUM, 23 PUBLICATIO, 24–25 (DISTRIBUTIO, RSS-AUTOMATIO) |
| 4 | Product & Revenue (ORGAN-III) | 15 | 26–40 |
| 5 | External Validation | 4 | 41/21 SUBMISSIO, 42–44 |
| 6 | Community (ORGAN-VI) | 4 | 45–48 |
| 7 | Creative Work (ORGAN-I/II) | 3 | 49–51 |
| 8 | Portfolio & Presentation | 3 | 52–54 |
| 9 | Quality & Testing | 3 | 55–57 |
| 10 | Automation & Tooling | 3 | 58–60 |
| 11 | Governance & Schema | 3 | 61–63 |
| 12 | Soak Test & Monitoring | 2 | 64–65 |
| 13 | Conferences & Talks | 2 | 66–67 |
| 14 | Partnerships & Networking | 2 | 68–69 |
| 15 | Legal & Compliance | 2 | 70–71 |
| 16 | Design & UX | 2 | 72–73 |
| 17 | Data & Analytics | 2 | 74–75 |
| 18 | Backup & Resilience | 1 | 76 |
| | **TOTAL** | **~60** | Completed: 17–33 (17 sprints). Remaining: hypothetical catalog items. |

---

## APPENDIX B: Omega Criteria → Sprint Mapping

Every omega criterion maps to at least one sprint. The 17 criteria are from [`there+back-again.md`](./there+back-again.md) § "The Seventeen Omega Criteria."

| # | Criterion | Required Sprints | Tracking | Notes |
|---|-----------|-----------------|----------|-------|
| 1 | 30-day soak test passes | ~~17 (REMEDIUM)~~, 64 (VIGILIA) | [Omega #1](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/1) | Soak test in progress (17/30 days) |
| 2 | Stranger test ≥80% | 42 (PEREGRINUS), 73 (NAVIGATIO) | [Omega #2](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/2) | Test first, fix second |
| 3 | Engagement baseline established | 64 (VIGILIA), 74 (ANALYTICA) | [Omega #1](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/1) | Passive collection + analytics |
| 4 | Runbooks validated | 42 (PEREGRINUS) | [Omega #2](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/2) | Stranger test validates runbooks |
| 5 | ≥1 application submitted | 41 (SUBMISSIO) | **MET** | Doris Duke / Mozilla AMT submitted 2026-02-24 |
| 6 | AI-conductor essay published | **ALREADY MET** | **MET** | Deployed 2026-02-11 |
| 7 | ≥3 external feedback | 41 (SUBMISSIO), 44 (TESTIMONIUM) | [Omega #3](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/3) | Applications produce feedback |
| 8 | ≥1 ORGAN-III product live | 27 BETA-VITAE (life-my--midst--in) | **MET** | 12 products deployed 2026-02-28 |
| 9 | `revenue_status: live` for ≥1 entry | 40 (MERCATURA) | [Omega #4](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/4) | Requires Stripe integration |
| 10 | MRR ≥ system operating costs | 40 (MERCATURA) | [Omega #4](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/4) | Requires payment integration |
| 11 | ≥2 salons with external participants | 45 (CONVIVIUM), 46 (CONVIVIUM-II) | [Omega #5](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/5) | Two separate events |
| 12 | ≥3 external contributions | 47 (HOSPITIUM), 48 (FORUM) | [Omega #6](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/6) | Create pathway, then attract |
| 13 | ≥1 organic inbound link | 24 (DISTRIBUTIO), 68 (FOEDUS) | **MET** | LobeHub organic indexing 2026-02-28 |
| 14 | ≥1 recognition event | 43 (PETITIO), 66 (ORATIO), 68 (FOEDUS) | [Omega #7](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/7) | Multiple vectors |
| 15 | Portfolio updated with validation | 52 (RENOVATIO) | [Omega #8](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/8) | Quick update |
| 16 | Bus factor >1 | 42 (PEREGRINUS), 58 (INSTRUMENTUM) | [Omega #2](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/2) | Test + tools |
| 17 | 30+ days autonomous operation | ~~17 (REMEDIUM)~~, 64 (VIGILIA) | [Omega #1](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/1) | Soak test clock running (17/30) |

---

## APPENDIX C: Organ Coverage

Every organ is addressed by at least one sprint.

| Organ | Primary Sprints | Coverage |
|-------|----------------|----------|
| I (Theoria) | 49 (THEORIA) | Theory development |
| II (Poiesis) | 50 (VIVIFICATIO), 51 (POIESIS) | Code substance + creative output |
| III (Ergon) | 26–40 (14 BETA sprints + MERCATURA) | Product shipping + revenue |
| IV (Taxis) | 17 (REMEDIUM), 58–60 (tooling), 61–63 (governance) | Infrastructure + governance |
| V (Logos) | 23 (PUBLICATIO), 24–25 (distribution) | Essays + POSSE |
| VI (Koinonia) | 45–48 (community sprints) | Salons + contributors |
| VII (Kerygma) | 24 (DISTRIBUTIO), 66–67 (conferences) | Distribution + talks |
| Meta | 19–20, 22, 24 (documentation + metrics), 61–63 (governance) | Corpus + registry |

---

## APPENDIX D: Critical Path to Omega (Minimum Sprint Set)

If the goal is reaching omega with minimum sprint count, these 12 sprints form the critical path. They cover all 17 omega criteria with the fewest work packages:

| Order | Sprint | Covers Criteria | Calendar Dependency |
|-------|--------|----------------|---------------------|
| ~~1~~ | ~~**17 REMEDIUM**~~ | ~~#1, #17~~ | **COMPLETE** — workflows confirmed healthy |
| ~~2~~ | ~~**41/21 SUBMISSIO**~~ | ~~#5, #7~~ | **COMPLETE** — prep executed as Sprint 21; human submissions pending |
| 3 | **42 PEREGRINUS** | #2, #4, #16 | Validates H1 claims |
| ~~4~~ | ~~**27 BETA-VITAE**~~ | ~~#8~~ | **COMPLETE** — DB provisioned (44 tables on Neon), 3 migration bugs fixed, auth bug fixed, DEPLOY.md written, Render Blueprint ready |
| 5 | **40 MERCATURA** | #9, #10 | Requires deployed beta product (life-my--midst--in) |
| 6 | **64 VIGILIA** | #1, #3, #17 | 30 calendar days (passive) — clock started 2026-02-16 |
| 7 | **24 DISTRIBUTIO** | #13 | Creates inbound surface area |
| 8 | **45 CONVIVIUM** | #11 (partial) | First salon |
| 9 | **46 CONVIVIUM-II** | #11 (complete) | Second salon |
| 10 | **47 HOSPITIUM** | #12 | Enables external contributions |
| 11 | **52 RENOVATIO** | #15 | Quick portfolio update |
| 12 | **43 PETITIO** | #14 | Grant application for recognition |

**Already met:** #6 (AI-conductor essay published 2026-02-11), #1/#17 prerequisites (REMEDIUM — workflows healthy), #5/#7 prerequisites (SUBMISSIO — prep complete, human submissions pending), #8 prerequisites (BETA-VITAE — DB provisioned, deployment ready)

**Omega scorecard (post-AMPLIFICATIO, Sprint 33):** 1/17 MET (#6), 8 IN PROGRESS (#1, #3, #5, #8, #12, #14, #16, #17), 8 NOT STARTED (#2, #4, #7, #9, #10, #11, #13, #15). The 3 new IN PROGRESS criteria (#12, #14, #16) were advanced by AMPLIFICATIO artifacts (CONTRIBUTING.md, conference proposals, 14 ADRs). All 8 NOT STARTED criteria require external contact or money.

**Remaining critical path:** 8 sprints (42→40→64→24→45→46→47→52→43), plus **immediate human actions** (submit applications, deploy product, first social post) that advance criteria #5, #8, #13 without requiring named sprints.

**E2G-II priority reordering:** The critical path sequence should be reordered to front-load external contact:
1. **IMMEDIATE (human actions):** Submit Creative Lab Five (#5), deploy life-my--midst--in (#8), first social media post (feeds #13)
2. **Sprint 29 DISTRIBUTIO** — essay and content distribution (#13) — **COMPLETE**
3. **Sprint 31 FUNDAMEN** — infrastructure hardening for V/VI/VII/Meta (#1, #17) — **COMPLETE**
4. **Sprint 32 SENSORIA** — autonomous perception layer, 100% seed.yaml, stale-detection (#1, #6) — **COMPLETE**
5. **Sprint 33 PEREGRINUS** — stranger test + runbook validation (#2, #4, #16)
5. **Sprint 33 MERCATURA** — payment integration (#9, #10)
6. **Sprint 34 RENOVATIO** — portfolio refresh (#15)
7. **Sprint 35 CONVIVIUM** — first salon (#11 partial)
7. **VIGILIA** — passive, completes ~March 18 (#1, #3, #17)
8. Remaining: CONVIVIUM-II (#11 complete), HOSPITIUM (#12), PETITIO (#14)

**Note on critical path vs. cadence:** The critical path identifies the minimum set. The operational cadence (`operational-cadence.md`) determines how these are sequenced into weekly rhythm. They are pulled from this catalog as individual tasks, not executed as named sprints — per AP-1.

---

## APPENDIX E: Effort Summary

| Category | Min Hours | Max Hours |
|----------|-----------|-----------|
| Infrastructure Repair | 4 | 8 |
| Documentation Completion | 18 | 26 |
| Content & Publishing | 20 | 40 |
| Product & Revenue | 303 | 578 |
| External Validation | 24 | 44 |
| Community | 22 | 36 |
| Creative Work | 84 | 168 |
| Portfolio & Presentation | 12 | 23 |
| Quality & Testing | 24 | 48 |
| Automation & Tooling | 28 | 56 |
| Governance & Schema | 16 | 24 |
| Soak Test & Monitoring | 6 | 12 |
| Conferences & Talks | 28 | 42 |
| Partnerships & Networking | 12 | 20 |
| Legal & Compliance | 12 | 24 |
| Design & UX | 20 | 32 |
| Data & Analytics | 8 | 14 |
| Backup & Resilience | 4 | 8 |
| **TOTAL** | **~645** | **~1,203** |

The full catalog represents roughly 645–1,203 hours of AI-conductor effort. The critical path (Appendix D, 12 sprints) represents roughly 120–250 hours. Neither number includes calendar-time dependencies (e.g., the 30-day soak test clock, grant deadlines, salon scheduling).
