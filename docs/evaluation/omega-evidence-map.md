# Omega Evidence Map

**Created:** 2026-02-17
**Author:** @4444j99 (AI-conductor model: human directs, AI generates, human reviews)
**Status:** LIVING DOCUMENT — reviewed monthly at omega checklist review
**Companions:** [`there+back-again.md`](../strategy/there+back-again.md) (criteria definitions), [`rolling-todo.md`](../operations/rolling-todo.md) (active queue), [`operational-cadence.md`](../operations/operational-cadence.md) (review rhythm)
**Constitution:** [`docs/memory/constitution.md`](../memory/constitution.md) — Articles I-VI govern all specifications

---

> *The roadmap defines the criteria. This document tracks the proof. Each entry answers: "What evidence exists that this criterion is met or progressing?"*

---

## GitHub Tracking

All omega criteria and remaining sprints are tracked as GitHub issues on [`meta-organvm/organvm-corpvs-testamentvm`](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues).

| Omega Criteria | Issue | Sprint Issues |
|----------------|-------|---------------|
| #1, #3, #17 (soak) | [#1](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/1) | [#45](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/45) VIGILIA, [#46](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/46) VIGILIA-II |
| #2, #4, #16 (stranger test) | [#2](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/2) | [#26](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/26) PEREGRINUS |
| #7 (feedback) | [#3](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/3) | [#28](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/28) TESTIMONIUM |
| #9, #10 (revenue) | [#4](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/4) | [#25](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/25) MERCATURA |
| #11 (salons) | [#5](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/5) | [#29](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/29) CONVIVIUM, [#30](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/30) CONVIVIUM-II |
| #12 (contributions) | [#6](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/6) | [#31](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/31) HOSPITIUM, [#32](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/32) FORUM |
| #14 (recognition) | [#7](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/7) | [#27](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/27) PETITIO, [#47](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/47) ORATIO |
| #15 (portfolio) | [#8](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/8) | [#36](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/36) RENOVATIO |

Scorecard code fix: [`organvm-engine#1`](https://github.com/meta-organvm/organvm-engine/issues/1) — sync `_KNOWN_MET` to include #8 and #13.

---

## Summary

| Status | Count | Criteria |
|--------|-------|----------|
| MET | 9 | #1, #3, #5, #6, #8, #13, #15, #17, #19 |
| IN PROGRESS | 3 | #10, #12, #20 |
| NOT MET | 8 | #2, #4, #7, #9, #11, #14, #16, #18 |

**Latest rolling issue run (2026-06-18):**
- Local completion artifact: `data/omega/rolling-issue-2026-06-18.json`
- Pinned scorecard source: `data/omega/omega-status-2026-05-26.json` (9/20 MET, 3 IN_PROGRESS, 8 NOT_MET)
- Live soak source: `data/soak-test/daily-2026-06-18.json` (registry PASS, dependency PASS, 0 CI failures, 11 billing-locked repos)
- Generated soak report: `data/soak-test/report.md` (2026-05-19 to 2026-06-18)
- Delivery gate: `gh auth status` failed locally because the `4444J99` token is invalid; no remote comment could be posted.
- Delta gate: no criterion-status change from the issue context headline (`Omega scorecard 2026-06-14 -- 9/20 MET`), so the scheduler contract would not post a new rolling-issue comment even with valid auth.

**By Horizon:**

| Horizon | Timeline | Met | In Progress | Not Met |
|---------|----------|-----|-------------|---------|
| H1: Prove It Works | Days 1-30 | 3 (#1, #3, #17) | 0 | 2 (#2, #4) |
| H2: Validate Externally | Days 15-90 | 2 (#5, #6) | 0 | 1 (#7) |
| H3: Generate Revenue / Traffic | Days 30-180 | 2 (#8, #19) | 2 (#10, #20) | 1 (#9) |
| H4: Build Community | Days 60-365 | 1 (#13) | 1 (#12) | 1 (#11) |
| H5: Achieve Recognition | Days 90-730 | 1 (#15) | 0 | 2 (#14, #18) |
| Cross-horizon | H1+H4 | 0 | 0 | 1 (#16) |

---

## Criteria Detail

### H1: Prove It Works

---

#### #1: 30-Day Soak Test Passes (<=3 critical incidents) — MET (2026-03-18)

**Criterion:** Soak test report shows <=3 critical incidents over 30 consecutive days.

**Status:** **MET.** Pinned scorecard source reports 99/30 days with **0 critical incidents** as of 2026-05-25. Local live soak now extends through 2026-06-18 with registry PASS, dependency PASS, 0 CI failures, and 11 billing-locked repos in the latest snapshot. S1-II marked completed 2026-03-18. Soak data collection continues autonomously.

**Date met:** 2026-03-18 (27 days unrecognized — declared in Reconciliation Sprint 2026-04-14).

**Domus evidence (2026-04-14):** Domus Semper Palingenesis (registered PERSONAL 2026-04-13) provides the operator environment sustaining soak infrastructure. 50ms shell startup and zero-error boot (S32 rewrite) is foundational to the autonomous collection pipeline.

**Incident (2026-04-17→2026-04-18, S-cleanup-2026-04-18):** 1Password 8 Squirrel auto-updater failure at 2026-04-17 03:41 AM left `op-ssh-sign` binary missing. Git commit signing broken for >24 hours. chezmoi autoCommit+autoPush silently failed during window (commits blocked by missing signing binary). Discovered and fixed 2026-04-18 via `brew install --cask 1password`. Root cause: Electron auto-update on macOS 26 beta stripped binary without writing replacement. **Impact:** Autonomous propagation (#17 evidence) was false during failure window. Incident count: 0→1 (still within <=3 threshold). IRF-DOM-035.

**Previous status:** Data collection running since 2026-02-16. First real (non-dry-run) snapshot collected 2026-02-17. Daily cron at 08:00 UTC auto-collects and commits snapshots.

**Evidence:**
- Data: `data/soak-test/daily-*.json`
- Workflow: `.github/workflows/soak-test-daily.yml`
- Script: `scripts/soak-test-monitor.py`

**Current Data (2026-06-18 snapshot):**
- Registry validation: PASS (0 issues)
- Dependency validation: PASS (0 violations)
- CI: 60 checked, 0 failing, 49 unknown, 11 billing-locked
- Engagement: 0 stars, 0 forks in tracked top-repo aggregate
- Archive: 122 snapshots from 2026-02-16 through 2026-06-18; one known gap on 2026-05-26 after the criterion had already been met

**AMPLIFICATIO update (2026-02-17):** 4 CI fixes pushed (universal-waveform-explorer, shared-remembrance-gateway, hokage-chess, a-i-chat--exporter), improving soak signal quality from 55/74 (74%) to 67/72 (93.1%).

**Post-AMPLIFICATIO maturation (2026-02-17):** M9-II (fetch-familiar-friends: @types/react-dom v19→v18) and M10-II (life-my--midst--in: ESLint 10→9.x, design-system coverage 75%→20%) pushed. Expected CI: ~69/72 (95.8%) pending workflow runs. Only ORGAN-I billing lock failures remain as known issues.

**Vercel triage session (2026-03-23):** CI signal quality fix for stakeholder-portal — Release Drafter false failures on all PRs eliminated (was setting invalid `targetCommitish`), CI job name mismatch fixed (`quality`→`test` to match branch protection), unblocking all PR merges. Branch protection had been silently broken, preventing any PR from merging. Also: specvla-ergon--avditor-mvndi `build-and-test` unblocked via rebase + lint fix.

**Gap:** None for the launch criterion. Ongoing monitoring still records billing-locked ORGAN-I repos as a separate CI signal-quality constraint.

**Rolling TODO:** S1-II

**Tracking:** [Omega issue #1](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/1), [Sprint 64 VIGILIA #45](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/45)

---

#### #2: Stranger Test Score >=80% — NOT MET

**Criterion:** An uninvolved person navigates the system, scores >=80% on the test protocol.

**Status:** Protocol written, no participant recruited.

**Evidence:**
- Protocol: `docs/operations/stranger-test-protocol.md`

**Gap:** Needs 1 external participant who has never seen the system. Cannot be self-tested.

**Blocker:** EXTERNAL — requires human participant

**Rolling TODO:** M1-II

**Tracking:** [Omega issue #2](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/2), [Sprint 42 PEREGRINUS #26](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/26)

---

#### #3: Engagement Baseline Established (30 days of data) — MET (2026-03-18)

**Criterion:** 30 consecutive days of engagement metrics (stars, forks, views, clones) collected.

**Status:** **MET.** Pinned scorecard source reports 99 days of engagement data as of 2026-05-25. Soak test daily snapshots continue to include engagement metrics for 8 flagship repos; the latest local snapshot is 2026-06-18.

**Evidence:**
- Data: `data/soak-test/daily-*.json` → `engagement` section
- Baseline (2026-02-17): 5 total stars, 3 total forks, views distributed across 8 repos
- Latest live snapshot: `data/soak-test/daily-2026-06-18.json`

**Current Engagement Aggregate (2026-06-18):**
- Total stars: 0
- Total forks: 0
- Tracked top repos: 8

**Gap:** None for the baseline-data criterion. Positive external engagement is tracked separately by #7, #10, #13, and #14.

**Date met:** 2026-03-18

**Rolling TODO:** E2 (completed — soak test now collecting real data)

**Tracking:** [Omega issue #1](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/1), [Sprint 74 ANALYTICA #55](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/55)

---

#### #4: Runbooks Validated by Second Operator — NOT MET

**Criterion:** A second operator successfully follows the runbooks to perform system operations.

**Status:** Runbooks exist in `docs/operations/` (operational-cadence, autonomous-setup-guide). Not yet validated by anyone other than the author.

**Evidence:**
- Runbooks: `docs/operations/operational-cadence.md`, `docs/operations/autonomous-setup-guide.md`
- CLI: `scripts/organ-cli.py` (8 subcommands for system operations)

**Gap:** Needs a second human operator to attempt the procedures and log results.

**Blocker:** EXTERNAL — requires second person

**Rolling TODO:** M1-II (combined with stranger test — same participant could validate both)

**Tracking:** [Omega issue #2](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/2), [Sprint 42 PEREGRINUS #26](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/26)

---

### H2: Validate Externally

---

#### #5: >=1 Application Submitted — MET

**Criterion:** At least one grant/job/fellowship application has been submitted using the system as evidence.

**Status:** Application submitted 2026-02-24 (PROPULSIO MAXIMA Sprint).

**Evidence:**
- X1 materials: `docs/applications/05-google-creative-lab-five-responses.md`
- X3 cover letters: `docs/applications/cover-letters/`
- E3 script: `docs/applications/e3-google-creative-fellowship-submission.md` (deadline March 18)
- Supporting evidence: 41 published essays (~140K+ words), 14 ADRs, CONTRIBUTING.md, 100+ repos across 8 orgs
- 2 conference proposals drafted (AMPLIFICATIO): AI-conductor talk + constraint-alchemy workshop

**Gap:** None — criterion met.

**Date met:** 2026-02-24

---

#### #6: AI-Conductor Essay Published — MET

**Criterion:** An essay about the AI-conductor methodology has been published on the public-process site.

**Status:** Multiple essays published that document the AI-conductor methodology.

**Evidence:**
- Essay #32: "Building Autonomous Creative Systems" — guide covering the full methodology
- Essay #33: "Governance for Artists" — guide on the governance layer
- Essay #36: "Construction Addiction" — retrospective on the build process
- Essay #37: "Constraint Alchemy Workshop" — workshop format for the methodology
- Essay #39: "Performance Platform Methodology" — platform design methodology
- Essay #40: "Twelve Decisions" — ADR-based methodology narrative
- Total: 41 essays published, ~140K+ words, all at `organvm-v-logos/public-process/_posts/`
- Site URL: accessible via GitHub Pages

**Date met:** 2026-02-16 (essay #32 deployed). Strengthened substantially by essays #36-40 (HERMETICUM + AMPLIFICATIO sessions).

---

#### #7: >=3 Pieces of External Feedback Collected — NOT MET

**Criterion:** At least 3 pieces of feedback from people outside the system have been collected and synthesized.

**Status:** No external feedback collected yet. First social media posts made 2026-02-17 (Mastodon + Discord), but no responses received.

**Evidence:** None yet.

**Gap:** Requires external interaction. Potential sources: application reviewers (after #5), social media responses, stranger test participant, salon attendees.

**Blocker:** EXTERNAL — requires other humans to engage with the system

**Rolling TODO:** Fed by X1, X4, M1-II

**Tracking:** [Omega issue #3](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/3), [Sprint 44 TESTIMONIUM #28](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/28)

---

### H3: Generate Revenue

---

#### #8: >=1 ORGAN-III Product Live — MET

**Criterion:** At least one commercial product from ORGAN-III is deployed and accessible to users.

**Status:** 12 products deployed across Netlify and Render, all returning HTTP 200. Far exceeds the ≥1 requirement.

**Evidence:**

*Render (full-stack):*
- `life-my--midst--in` — https://inmidst-web.onrender.com (web) + https://inmidst-api.onrender.com (API)
- `public-record-data-scrapper` — https://ucc-mca-api.onrender.com (API backend)
- `community-hub` (ORGAN-VI) — https://community-hub-8p8t.onrender.com

*Netlify (static SPAs):*
- `fetch-familiar-friends` — https://fetch-familiar-friends.netlify.app
- `classroom-rpg-aetheria` — https://classroom-rpg-aetheria.netlify.app
- `trade-perpetual-future` — https://trade-perpetual-future.netlify.app
- `search-local--happy-hour` — https://search-local-happy-hour.netlify.app
- `public-record-data-scrapper` — https://public-record-data-scrapper.netlify.app (frontend)
- `mirror-mirror` — https://mirror-mirror-app.netlify.app
- `sovereign-ecosystem--real-estate-luxury` — https://sovereign-ecosystem.netlify.app
- `the-invisible-ledger` — https://the-invisible-ledger.netlify.app
- `a-mavs-olevm` (ORGAN-II) — https://etceter4.netlify.app
- `public-process` (ORGAN-V) — https://public-process.netlify.app
- `portfolio` (4444J99) — https://4444j99-portfolio.netlify.app

All seed.yaml files updated with deployment_url. Registry-v2.json updated.

**Gap:** None — massively exceeded.

**Blocker:** None

**Date met:** 2026-02-24 (life-my--midst--in initial deploy), strengthened 2026-02-28 (12 total products live)

**Rolling TODO:** X2

---

#### #9: >=3 ORGAN-III Products at Stranger-Ready Polish — NOT MET

**Criterion:** At least 3 ORGAN-III products pass the per-product stranger test (UI functional, docs clear, onboarding complete, zero rough edges for a first-time visitor).

**Status:** 12 products are live (far exceeding the ≥1 from #8), but stranger-ready polish has not been validated for any of them.

**Constitutional note:** This criterion was revised from "revenue_status: live for ≥1 registry entry." The constitutional amendment establishes the sequencing: craft (#9) → traffic (#10) → inquiry → revenue (#18). Revenue is an outcome, not a feature to bolt on.

**Evidence:**
- 12 products deployed: `data/omega/omega-status-2026-05-26.json` (criterion #8 evidence)
- Per-product polish: no stranger-test-per-product records exist yet

**Gap:** Requires per-product stranger-test execution for at least 3 candidates.

**Blocker:** INTERNAL — craft/QA work; no external dependency

**Rolling TODO:** M2-II (repurposed from Stripe integration → polish validation)

**Tracking:** [Omega issue #4](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/4), [Sprint 40 MERCATURA #25](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/25)

---

#### #10: >=100 Unique Visitors/Month (Organic Discovery) — IN PROGRESS

**Criterion:** At least 100 unique visitors per month across portfolio + portal + products, arriving organically (not solicited).

**Status:** Plausible Analytics installed on portfolio (4444j99.github.io/portfolio/). Visitor threshold not yet reached as of 2026-05-26.

**Constitutional note:** This criterion was revised from "MRR ≥ system operating costs." The new sequencing: craft (#9) → traffic (#10) → inquiry → revenue (#18). Traffic is the gate between polish and organic revenue.

**Evidence:**
- Plausible Analytics script: in portfolio `Layout.astro` since 2026-04
- Visitor count: requires authenticated dashboard access (UNVERIFIABLE-FROM-CLOUD)

**Gap:** Organic traffic takes calendar time and distribution. More instrumentation is not the constraint — craft polish (#9) and active distribution are.

**Blocker:** TIME + EXTERNAL (organic discovery); unblocked only after #9 is met

**Rolling TODO:** Downstream of #9

**Tracking:** [Omega issue #4](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/4)

---

### H4: Build Community

---

#### #11: >=2 Salons/Events with External Participants — NOT MET

**Criterion:** At least 2 community events (salons, reading groups, workshops) held with external participants.

**Status:** No events held. ORGAN-VI community infrastructure exists but is empty.

**Evidence:**
- ORGAN-VI `community-hub` promoted to PUBLIC_PROCESS and live with a real scheduled event (inaugural salon), advancing infrastructure for community events.

**Gap:** Requires recruiting participants and organizing events. Depends on some external visibility (#5, #13) to attract participants.

**Blocker:** EXTERNAL — needs participants

**Rolling TODO:** S2-II

**Tracking:** [Omega issue #5](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/5), [Sprint 45 CONVIVIUM #29](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/29), [Sprint 46 CONVIVIUM-II #30](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/30)

---

#### #12: >=3 External Contributions — IN PROGRESS

**Criterion:** At least 3 contributions from external people to the system (PRs, issues, feedback, content).

**Status:** Contribution pathway created (AMPLIFICATIO session, 2026-02-17). Infrastructure exists for external contributors. No external contributions received yet.

**Evidence:**
- CONTRIBUTING.md: Written and deployed to corpvs-testamentvm root (AMPLIFICATIO)
- Good-first-issues: 5 created across 5 repos (AMPLIFICATIO) — accessible entry points for newcomers
- Distribution pipeline: Active since 2026-02-17, pushing content to Mastodon + Discord (creates awareness)
- 40 published essays provide discoverability surface area

**Gap:** Requires actual external contributions. Infrastructure is in place (contribution pathway + entry points + distribution), but no external contributors have engaged yet.

**Blocker:** EXTERNAL — needs community discovery and engagement

**Rolling TODO:** S3-II

**Tracking:** [Omega issue #6](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/6), [Sprint 47 HOSPITIUM #31](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/31), [Sprint 48 FORUM #32](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/32)

---

#### #13: >=1 Organic Inbound Link — MET

**Criterion:** At least 1 external website links to any part of the system without being solicited.

**Status:** LobeHub Skills Marketplace (lobehub.com) has organically indexed and published skills from `organvm-iv-taxis/a-i--skills`, creating permanent external links to the ORGANVM ecosystem.

**Evidence:**
- https://lobehub.com/skills/organvm-iv-taxis-a-i-skills-theme-factory — links to `github.com/organvm-iv-taxis/a-i--skills`, published under `organvm-iv-taxis` author
- https://lobehub.com/pl/skills/organvm-iv-taxis-a-i-skills-continuous-learning-agent — same repo linkback
- These are organic — LobeHub indexed the repo content automatically without manual submission
- Verified 2026-02-28: page exists, contains full skill documentation, links back to GitHub org

**Gap:** None — criterion met.

**Date met:** Discovered 2026-02-28 (pages likely indexed earlier)

---

### H5: Achieve Recognition

---

#### #14: >=1 Recognition Event — NOT MET

**Criterion:** At least one external recognition: grant award, academic citation, conference invitation, or adoption by another system.

**Status:** **NOT MET.** 2 conference proposals drafted and submission-ready (AMPLIFICATIO, 2026-02-17). E3 (Google Creative Fellowship, deadline March 18) submission script prepared. No recognition has been received yet.

**Evidence:**
- Conference proposals: `docs/applications/conference-proposals/ai-conductor-talk.md` and `constraint-alchemy-talk.md` (AMPLIFICATIO)
- E3 submission script: `docs/applications/e3-google-creative-fellowship-submission.md` (deadline March 18)
- 14 ADRs demonstrate methodological rigor suitable for academic/conference citation
- 40 published essays provide citable body of work

**Gap:** Proposals drafted but not yet submitted (CFP windows needed). E3 prepared but not submitted. Actual recognition requires external review and acceptance.

**Blocker:** TIME (submit proposals when CFPs open) + EXTERNAL (acceptance decisions)

**Rolling TODO:** S6-II, E3

**Tracking:** [Omega issue #7](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/7), [Sprint 43 PETITIO #27](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/27), [Sprint 66 ORATIO #47](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/47)

---

#### #15: Portfolio Updated with External Validation — MET (2026-03-19)

**Criterion:** Portfolio site reflects external validation (testimonials, acceptance letters, user counts, press).

**Status:** **MET.** Validation page live at `4444j99.github.io/portfolio/validation/` since 2026-03-19. Confirmed in `data/omega/omega-status-2026-05-26.json`. This document previously showed NOT STARTED — corrected 2026-06-15.

**Date met:** 2026-03-19

**Evidence:**
- Validation page: `4444j99.github.io/portfolio/validation/` (UNVERIFIABLE-FROM-CLOUD; confirmed per omega JSON)
- Portfolio URL: `4444j99.github.io/portfolio/`
- Data files: `portfolio-site/src/data/*.json`, `site-data/*.json`

**Gap:** None — criterion met.

**Tracking:** [Omega issue #8](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/8), [Sprint 52 RENOVATIO #36](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/36)

---

### Cross-Horizon

---

#### #16: Bus Factor >1 (Validated) — NOT MET

**Criterion:** A second operator can maintain the system using existing documentation. Validated, not just documented.

**Status:** **NOT MET.** Documentation substantially strengthened (AMPLIFICATIO, 2026-02-17). 14 ADRs now document key architectural decisions. Comprehensive runbooks, CLI, and autonomous setup guide exist. No second operator has attempted maintenance.

**Evidence:**
- ADRs: 14 decision records in `docs/adr/` (003-014, covering naming/registry/DAG/AI-conductor/promotion/dating/revenue/dispatch/soak/billing/seed.yaml/numbering) — AMPLIFICATIO
- CONTRIBUTING.md: External contributor onboarding guide — AMPLIFICATIO
- Runbooks: `docs/operations/operational-cadence.md`
- Setup guide: `docs/operations/autonomous-setup-guide.md`
- CLI: `scripts/organ-cli.py` (8 subcommands for system operations)
- Autonomous workflows: 12 cron workflows across 2 repos (self-operating)
- Invocation system: `scripts/invoke.py` + `docs/operations/concordance.md` (100+ ID entries)

**Domus evidence (2026-04-14):** chezmoi bootstrap enables full environment reproduction: `chezmoi init --apply 4444j99/domus-semper-palingenesis`. A new machine inherits shell config, tool setup, agent infrastructure, MCP server configuration, and 1Password secret refs. The S32 rewrite (50ms startup, zero-error boot) means the bootstrapped environment is immediately operational.

**Gap:** Needs a real person to attempt system operation and log the results. Documentation is now comprehensive enough for the test — the constraint is participant recruitment, not documentation gaps.

**Blocker:** EXTERNAL — requires second person (potentially same as #2 and #4)

**Rolling TODO:** M1-II (shares participant with stranger test)

**Tracking:** [Omega issue #2](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/2), [Sprint 42 PEREGRINUS #26](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/26)

---

#### #17: System Operates 30+ Days Without Operator Intervention — MET (2026-03-18)

**Criterion:** The autonomous system runs for 30+ consecutive days without the primary operator needing to intervene.

**Status:** **MET.** Pinned scorecard source reports 99/30 days as of 2026-05-25; the local soak archive now extends through 2026-06-18. The 30-day threshold passed on 2026-03-18. Scheduled workflows continue to run without human per-task routing.

**Date met:** 2026-03-18 (27 days unrecognized — declared in Reconciliation Sprint 2026-04-14).

**Domus evidence (2026-04-14):** Domus self-heal daemon monitors and restores the operator environment without human intervention. The S32 rewrite eliminated all error-path boot failures. chezmoi autoCommit+autoPush ensures environment changes propagate to remote without manual git operations.

**Incident (2026-04-17→2026-04-18, S-cleanup-2026-04-18):** 1Password 8 auto-update failure broke git commit signing for >24 hours. chezmoi autoCommit was silently failing — environment changes were NOT propagating to remote during this window. The "without human intervention" claim was technically violated (manual `brew install --cask 1password` required to restore). Self-heal daemon did NOT detect or recover from this failure. Pattern matches IRF-DOM-017 (silent failure, no alerting). Does not reset 30-day clock (criterion already MET at 58+ days), but documents a resilience gap in the autonomous pipeline. IRF-DOM-035.

**Previous status:** Autonomous systems activated (AUTOMATA sprint, 2026-02-17). 11+ workflows configured with daily/weekly/monthly schedules. First real autonomous data collected 2026-02-17.

**Evidence:**
- Autonomous schedule: 12 cron workflows across 2 repos
- Workflow list: soak-test-daily, essay-monitor, metrics-refresh, orchestrator-agent, backfill-distribution, distribution-agent, stale-detector-weekly, system-pulse-weekly, promotion-recommender, essay-deploy, auto-deploy
- Data: `data/soak-test/daily-*.json` (tracks system operation without intervention)

**Current autonomous operation:**
- Essay distribution: Active (backfill-distribution running Mon/Wed/Fri)
- Metrics: Auto-refreshed weekly (Mon 06:00 UTC)
- Health monitoring: Daily soak test (08:00 UTC) + weekly stale detector (Tue 06:00 UTC)
- Pulse reports: Weekly (Sun 12:00 UTC)
- Latest local soak: `data/soak-test/daily-2026-06-18.json`

**AMPLIFICATIO update (2026-02-17):** 4 CI fixes pushed, improving autonomous signal quality (CI pass rate: 55/74 → 67/72, 93.1%).

**Post-AMPLIFICATIO maturation (2026-02-17):** M9-II and M10-II CI fixes pushed. Expected: ~69/72 (95.8%). Only ORGAN-I billing lock failures remain. Note: CI fixes count as infrastructure maintenance, not system intervention — the autonomous workflows continue operating regardless of individual repo CI status.

**Gap:** None for the 30-day launch criterion. The known 2026-04-17→2026-04-18 signing incident remains a resilience follow-up, but it did not reset the already-met criterion.

**S-dispatch evidence (2026-03-30):** Cognitive Service Dispatch system enables multi-agent autonomous operation — 4-stream fleet dispatch (Perplexity, Gemini, OpenCode, Claude) executed with handoff envelopes carrying constraints between agents. Extends autonomous operation model: the system can now dispatch mechanical work to worker-bee agents while Claude handles strategic work, without human per-task routing.

**Rolling TODO:** S1-II

**Tracking:** [Omega issue #1](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/1), [Sprint 64 VIGILIA #45](https://github.com/meta-organvm/organvm-corpvs-testamentvm/issues/45)

---

#### #18: First Organic Revenue (Inquiry → Payment) — NOT MET

*Horizon: H5*

**Criterion:** A first payment received from someone who discovered the work organically — not through a solicited pitch.

**Status:** No revenue. Gated behind #9 (stranger-ready polish) and #10 (organic traffic). Neither prerequisite is met.

**Constitutional note:** Revenue is the final outcome of the craft → traffic → inquiry → payment chain. It should not be targeted directly before #9 and #10 are proven.

**Evidence:** None.

**Gap:** Unblock #9 first (polish 3 products), then #10 (organic traffic), then create conditions for inbound inquiry.

**Blocker:** Depends on #9 and #10

---

#### #19: Network Testament Health (Density + Engagement + Milestones) — MET (2026-02-28)

*Horizon: H3*

**Criterion:** `network_density >= 0.5`, `engagement_velocity > 0`, `>=1 milestone` met simultaneously.

**Status:** **MET.** Confirmed in `data/omega/omega-status-2026-05-26.json`.

**Date met:** 2026-02-28 (discovered during Deployment Sprint).

**Evidence:**
- density = 1.00 (target ≥0.5) ✓
- engagement_velocity = 0.03 (target >0) ✓
- milestones = 3 (target ≥1) ✓
- maps = 2, mirrors = 5
- Source: `data/omega/omega-status-2026-05-26.json` (criterion #19, `auto: true`)
- Sigma-E tool state UNVERIFIABLE-FROM-CLOUD

**Gap:** None — criterion met.

---

#### #20: Formal Validation (Sigma-E ≥80% FORMAL Derivations) — IN PROGRESS

*Horizon: H3*

**Criterion:** ≥80% of sigma-E derivations reach FORMAL formalization level, validating system integrity (SPEC-025 Predicate 7 IMMUTABILITY).

**Status:** 14/24 derivations at FORMAL level = **58%**. Target is ≥80% (requires ≥20/24). Gap: 6 more derivations must reach FORMAL.

**Evidence:**
- Source: `data/omega/omega-status-2026-05-26.json` (criterion #20, `auto: true`, value "14/24 derivations at FORMAL level (58%)")
- Sigma-E adjudicatory layer runs locally (UNVERIFIABLE-FROM-CLOUD)

**Gap:** 6 derivations below FORMAL threshold. Requires sigma-E formal adjudication work.

**Blocker:** INTERNAL — sigma-E tooling work

---

## Critical Path to Omega

The fastest path through the criteria follows the horizon dependency chain:

```
H1 (#1, #3, #17) ──DONE──→ H1 complete (3/3 MET)
  ↓
H2 (#5, #6) ──DONE──→ H2 partially complete (2/3; #7 needs external feedback)
  ↓
H3 (#9) ──polish 3 products──→ unlocks #10 (organic traffic)
     (#8, #19 already MET; #20 IN PROGRESS)
          ↓
H4 (#13 MET; #12 IN PROGRESS; #11 needs events)
          ↓
H5 (#15 MET; #14 needs recognition; #18 needs #9+#10 first)
```

**What blocks omega is not engineering.** H1 is fully MET (3/3: #1, #3, #17). The 8 NOT MET criteria are blocked by: external humans (5: #2, #4, #7, #11, #16), craft gate (#9 — polish 3 products), dependency chain (#18 ← #9+#10), and recognition (#14).

**The one thing that accelerates everything:** Polish 3 products to stranger-ready (#9). This unblocks organic traffic (#10), which unblocks revenue (#18), and provides concrete evidence for recognition (#14) and external feedback (#7).

---

## Revision Log

| Date | Change | Reason |
|------|--------|--------|
| 2026-02-17 | Initial creation | Pre-validation maturation session |
| 2026-02-17 | AMPLIFICATIO evidence update — #12, #14, #16 flipped NOT STARTED → IN PROGRESS; #1, #5, #6, #17 evidence strengthened; summary 1/5/11 → 1/8/8; organic link check (#13) negative | Post-AMPLIFICATIO maturation |
| 2026-02-24 | System-Wide Activation Sprint — #8 flipped IN PROGRESS → MET (life-my--midst--in deployed on Render); ORGAN-VI promoted to PUBLIC_PROCESS; first real salon event created; summary 1/8/8 → 2/7/8 | System-Wide Activation Sprint |
| 2026-02-28 | Deployment Sprint — #5 flipped IN PROGRESS → MET (application submitted 02-24); #8 evidence massively expanded (12 products live across Netlify/Render); #13 flipped NOT STARTED → MET (LobeHub organic indexing of ORGAN-IV skills discovered); summary 2/7/8 → 4/6/7 | Full Deployment Sprint |
| 2026-03-04 | GitHub issue tracking — 58 issues created across organvm-engine (1) and organvm-corpvs-testamentvm (57). 9 omega tracking issues + 48 sprint issues + 1 scorecard code fix. Tracking links added to all 17 criteria entries in this document. | Issue codification session |
| 2026-04-14 | **Reconciliation Sprint** — #1 and #17 flipped IN PROGRESS → MET (both passed 2026-03-18, 27 days of unrecognized progress). Domus evidence added to #1, #16, #17, #19. Summary 7/2/10 → 9/0/10. H1 now fully MET (3/3). Registry grew 129→146 (mass registration + portfolio). | System-Wide Reconciliation Sprint |
| 2026-06-15 | **Omega scorecard sync** — Reconciled against `data/omega/omega-status-2026-05-26.json`. (1) #9 revised: "revenue_status: live" → "≥3 products at stranger-ready polish"; (2) #10 revised: "MRR ≥ costs" → "≥100 unique visitors/month"; (3) #15 corrected: NOT STARTED → MET (validation page live since 2026-03-19); (4) Sections for #18, #19, #20 added (previously absent); (5) Summary 9/0/10 (19 criteria) → 9/3/8 (20 criteria); (6) By Horizon and Critical Path updated. | omega-scorecard agent first run ([a-organvm/organvm-corpvs-testamentvm#490](https://github.com/a-organvm/organvm-corpvs-testamentvm/issues/490)) |
| 2026-06-18 | **Omega rolling issue handoff** — Recorded local completion artifact `data/omega/rolling-issue-2026-06-18.json`. Scorecard unchanged from 2026-06-14 issue context at 9/20 MET (3 IN_PROGRESS, 8 NOT_MET); live soak advanced to `data/soak-test/daily-2026-06-18.json` and `data/soak-test/report.md` regenerated for 2026-05-19 to 2026-06-18. Remote issue write blocked by invalid local `gh` token, and the scheduler delta gate would post no comment because criterion statuses did not change. Stale criterion detail text and headings normalized to match the pinned scorecard. | GH #490 local completion pass |
