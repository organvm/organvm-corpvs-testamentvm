# Rolling TODO — Master Deferred Work Queue

**Created:** 2026-02-17
**Author:** @4444j99
**Status:** ACTIVE — Living document, reviewed weekly (Friday retrospective)
**Last reviewed:** 2026-02-18 (ERUPTIO staged: 7 submission scripts ready, deploy guide ready, Sponsors setup guide ready. Materials awaiting execution.)
**Companions:** [`operational-cadence.md`](./operational-cadence.md) (rhythm), [`there+back-again.md`](../strategy/there+back-again.md) (destination), [`sprint-catalog.md`](../strategy/sprint-catalog.md) (menu), [`e2g-ii-action-items.md`](../evaluation/e2g-ii-action-items.md) (audit trail), [`concordance.md`](./concordance.md) (ID lookup)
**Constitution:** [`docs/memory/constitution.md`](../memory/constitution.md) — Articles I-VI govern all specifications

---

> *The roadmap says **where we're going.** The catalog says **what we could do.** The cadence says **when we work.** This document says **what we're actually doing next.***

> **Benefits Cliff Awareness:** SNAP excludes lump-sum grants (safe).
> Medicaid threshold: $21,597/year. Essential Plan $0 premium to $39,125.
> Fair Fares hard cliff: $22,692/year.
> Call NYLAG (212-613-5000) before accepting any single grant >$5K.
> See [`docs/applications/10-funding-strategy.md`](../applications/10-funding-strategy.md) for full analysis.

---

## How to Use This Document

**When:** Every Friday during the Part I retrospective block (see [`operational-cadence.md`](./operational-cadence.md) Part I).

**What to do:**
1. Scan READY — can anything be knocked out this week?
2. Scan NEEDS TIME — schedule blocks for next week's deep work days
3. Check NEEDS INCOME / NEEDS EXTERNAL — has anything unblocked?
4. Move completed items to COMPLETED with a date
5. Add any new items discovered during the week
6. At monthly review (Week 4), archive completed items

**Constraint tags:**
- `[READY]` — No blockers. Just needs doing. Quick wins (<30 min).
- `[TIME]` — Needs a scheduled block (>30 min). No other blocker.
- `[INCOME]` — Requires spending money (hosting, subscriptions, paid tools).
- `[EXTERNAL]` — Waiting on someone or something outside your control.

**Item IDs** use the e2g-ii codes where they exist (X1, E2, M3-II, S1-II, etc.) and new codes (G1, G2, G3) for setup-guide items. This preserves provenance and makes cross-referencing painless.

---

## READY — No Blockers, Just Needs Doing

- [x] **X4.** Make first social media post — completed 2026-02-17 (HERMETICUM session: Mastodon + Discord via distribution pipeline, issue #45)
  - Source: [e2g-ii P0](../evaluation/e2g-ii-action-items.md) · Omega: feeds #7, #13
- [ ] **F1.** Activate GitHub Sponsors — STAGED 2026-02-18 (ERUPTIO: setup guide ready, tiers $5/$25/$100)
  - Source: [10-funding-strategy.md](../applications/10-funding-strategy.md) · Omega: feeds #9, #10
- [ ] **F2.** Apply for Fractured Atlas fiscal sponsorship (~30 min) — $10/mo, unlocks org-only grants (NEA, state arts councils)
  - Source: [10-funding-strategy.md](../applications/10-funding-strategy.md) · Omega: feeds #9
- [ ] **G2.** Configure Render deploy hook for life-my--midst--in — deploy service first (depends on X2), then copy deploy hook URL to `RENDER_DEPLOY_HOOK` secret
  - Render free tier costs $0, no credit card required
  - Enables auto-deploy on push to master
  - Source: [autonomous-setup-guide](./autonomous-setup-guide.md) §4

---

## NEEDS TIME — Schedule a Block

### This Week — URGENT DEADLINES

> **Non-negotiable rule from E2G-II:** No new named internal sprints until X1-X4 are complete.
> **Clarification:** Funding applications are external-facing (breaking the seal), not internal sprints.

- [ ] **F24.** Submit Watermill Center Summer Program application — STAGED 2026-02-18 (ERUPTIO: submission script ready, awaiting submission via SlideRoom)
  - URL: https://www.watermillcenter.org/summer/ (via SlideRoom) · Fit: 7/10
  - FREE: housing, food, materials, local transport, small travel stipend. 4 weeks on Long Island (Jul 5 - Aug 2, 2026).
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) · Residency agent

- [ ] **F3.** Submit Artadia NYC application ($15K unrestricted) — STAGED 2026-02-18 (ERUPTIO: submission script ready, awaiting submission via Submittable)
  - URL: https://artadia.org/award_schedule/new-york/ (Submittable) · Fit: 8/10
  - Source: [10-funding-strategy.md](../applications/10-funding-strategy.md) · Omega: #5, #9

- [ ] **F22.** Submit Doris Duke / Mozilla "Artists Make Technology Lab" ($150K) — STAGED 2026-02-18 (ERUPTIO: submission script ready, awaiting submission via Giving Data portal)
  - URL: https://www.dorisduke.org/grants/projects/artists-make-technology-lab · Fit: 7/10
  - **HIGHEST SINGLE AMOUNT IN PIPELINE.** Up to $150K. Governance-as-choreography framing.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 1 · Omega: #5, #9

- [ ] **F10.** Submit Prix Ars Electronica entry (EUR 10K + Golden Nica) — STAGED 2026-02-18 (ERUPTIO: submission script ready, awaiting submission via calls.ars.electronica.art)
  - URL: https://ars.electronica.art/prix/en/opencall/ · Fit: 8/10
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 1 · Omega: #5, #14

- [ ] **F11.** Submit S+T+ARTS Prize entry (EUR 20K) — STAGED 2026-02-18 (ERUPTIO: auto-qualifies via Prix Ars submission, awaiting Prix Ars submission)
  - URL: https://starts-prize.aec.at/en/open-call/ · Fit: 8/10
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 1 · Omega: #5, #14

- [ ] **X1.** Submit Google Creative Lab Five application — STAGED 2026-02-18 (ERUPTIO: submission script ready, awaiting submission via creativelab5.com)
  - Materials: `docs/applications/05-google-creative-lab-five-responses.md`
  - URL: https://www.creativelab5.com/ · Fit: 8/10
  - Source: [e2g-ii P0](../evaluation/e2g-ii-action-items.md) · Omega: #5, feeds #7

- [ ] **[EXPIRED] F4.** Research and submit NEH Summer Programs — **deadline Mar 6** (~2 hrs)
  - Credential-building. Evaluate eligibility before investing time.
  - Source: [10-funding-strategy.md](../applications/10-funding-strategy.md)

- [ ] **F12.** Apply PEN America Writers Aid (up to $3,500) — STAGED 2026-02-18 (ERUPTIO: submission script ready, awaiting submission via pen.org)
  - URL: https://pen.org/us-writers-aid-initiative/ · Fit: **9/10** — highest-fit emergency fund
  - Max 2 grants lifetime. Benefits cliff: SNAP-safe.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 1 · Omega: #5, #9

- [ ] **F13.** Submit Awesome Foundation NYC ($1K no strings) — monthly deadline (~30 min)
  - URL: https://www.awesomefoundation.org/en/chapters/nyc · Fit: 8/10
  - Zero restrictions, zero reporting. SNAP-safe.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 1

- [ ] **X2.** Deploy life-my--midst--in to Render — STAGED 2026-02-18 (ERUPTIO: deploy script + Neon DB ready, awaiting deployment)
  - Guide: `~/Workspace/organvm-iii-ergon/life-my--midst--in/DEPLOY.md`
  - Source: [e2g-ii P0](../evaluation/e2g-ii-action-items.md) · Omega: #8

### This Month (Feb 17 – Mar 18)

- [ ] **[EXPIRED] F14.** Apply Bread Loaf Writers' Conference scholarship ($4,440 value) — **deadline Mar 15** (~2 hrs)
  - URL: https://www.middlebury.edu/writers-conferences/writers-conference · Fit: 7/10
  - Participant Scholarship covers tuition/room/board. Nonfiction track. MFA + 41 essays is strong.
  - 10 days, August 12-22, 2026 in Middlebury, VT. Not income (scholarship covers program costs).
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 2

- [ ] **[EXPIRED] E3.** Submit Google Creative Fellowship application — **deadline March 18, 2026**
  - URL: https://creativefellowship.google/ · Materials ready · Fit: 7/10
  - Source: [e2g-ii P1](../evaluation/e2g-ii-action-items.md) · Omega: #5, feeds #14

- [x] **X3.** Submit 9 job applications — completed 2026-03-19 (Anthropic, Coinbase, Temporal, Cursor, Datadog, Deepgram, Perplexity, Railway, Render)
  - Cover letters: `docs/applications/cover-letters/`
  - Source: [e2g-ii P0](../evaluation/e2g-ii-action-items.md) · Omega: #5, feeds #7

- [ ] **W1.** Pitch Noema Magazine (pays $1/word = ~$3K/essay) — rolling, **pitch this month**
  - Contact: pitches@noemamag.com
  - Pitch: "I built a 150-repo creative system orchestrated by AI — here's what it reveals about solo creative production."
  - Benefits cliff: Writing income is earned (counts toward SNAP $1,580/mo threshold). One per quarter = safe.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 5

- [ ] **W2.** Submit to Gay & Lesbian Review ($250/feature) — rolling
  - URL: https://glreview.org/writers-guidelines/ · Fit: 9/10
  - Direct LGBTQ+ identity match. Essay practice perfectly suited. Immediate income pathway.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 2

- [x] **E5.** Write "Construction Addiction" essay (#36) — completed 2026-02-17 (HERMETICUM session: ~2600 words, auto-deploys via essay-deploy pipeline)
  - Source: [e2g-ii P1](../evaluation/e2g-ii-action-items.md) · Omega: #6

- [ ] **G1.** Set up LinkedIn developer token (~30 min, OAuth flow) — enables automated LinkedIn distribution
  - Source: [autonomous-setup-guide](./autonomous-setup-guide.md) §5

### Next 1-3 Months (Deadline-Sequenced)

- [ ] **F6.** Submit Fire Island Artist Residency — **deadline Apr 1** (~2 hrs, SlideRoom)
  - LGBTQ+ emerging visual artist. Stipend + housing. Fit: 7/10
  - Source: [10-funding-strategy.md](../applications/10-funding-strategy.md) · Omega: #5

- [ ] **F15.** Submit NLnet NGI Zero Commons Fund (EUR 5K-50K) — **deadline Apr 1** (~3 hrs)
  - URL: https://nlnet.nl/commonsfund/ · Fit: 7/10
  - Funds open-source infrastructure for the commons. Registry, seed.yaml, orchestration patterns are genuine contributions.
  - Benefits cliff: International grant, lump-sum. SNAP-safe.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 3

- [ ] **F5.** Submit Creative Capital 2027 application ($50K) — portal opens Mar 2, **deadline Apr 2, 3pm ET** (~4-6 hrs)
  - HIGHEST-FIT TARGET (9/10). 6 short questions, 500-word project description, work samples.
  - Identity position: Systems Artist — "adventurous and imaginative" interdisciplinary work.
  - Benefits cliff: $50K exceeds Medicaid → Essential Plan ($0 premium). Call NYLAG before accepting.
  - Source: [10-funding-strategy.md](../applications/10-funding-strategy.md) · Omega: #5, #9

- [ ] **F16.** Submit ZKM Rauschenberg Residencies application (3-month Germany) — **deadline Apr 12** (~2 hrs)
  - URL: https://zkm.de/en/open-call-rauschenberg-residencies-202627 · Fit: 8/10
  - Submit single PDF to image@zkm.de. 3 places only. Oct-Dec 2026 in Karlsruhe.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 3

- [ ] **F17.** Submit WFF Housing Stability Grant ($30K over 3 years) — **deadline Apr 14, 5pm ET** (~4 hrs)
  - URL: https://www.nyfa.org/awards-grants/wff-housing-stability-grant-for-artists/ · Fit: **9/10**
  - **HIGHEST-VALUE NYC opportunity.** $12K yr 1, $10K yr 2, $8K yr 3. NYC 5+ years, AGI ≤$75K, housing-precarious.
  - **Action first:** Confirm digital/generative art eligibility with NYFA (visual artist requirement).
  - Benefits cliff: $12K yr 1 + $12K adjunct = $24K → exceeds Medicaid. Call NYLAG.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 3 · Omega: #5, #9

- [ ] **F7.** Submit Rauschenberg Cycle 36 ($5K) — **opens Apr 14, closes May 12** (~1 hr)
  - Emergency grant for digital/electronic arts. Quick application. SNAP-safe.
  - Source: [10-funding-strategy.md](../applications/10-funding-strategy.md)

- [ ] **F8.** Submit Spencer Foundation Small Research ($50K) — **deadline Apr 15, noon CT** (~4 hrs)
  - Education research focus. Identity position: Educator.
  - Source: [10-funding-strategy.md](../applications/10-funding-strategy.md) · Omega: #5

- [ ] **F18.** Submit Whiting Creative Nonfiction Grant ($40K) — **~Apr 2026** (~4 hrs)
  - URL: https://www.whiting.org/writers/creative-nonfiction-grant · Fit: 8/10
  - Writers completing book-length nonfiction. The 404K+ word corpus IS a book-in-progress.
  - Benefits cliff: $40K exceeds Medicaid → Essential Plan. Call NYLAG.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 3

- [ ] **F9.** Submit Processing Foundation Fellowship ($10K) — **~Apr-May** (~3 hrs)
  - Infrastructure contribution. Governance toolkit as deliverable. Fit: 6/10
  - Source: [10-funding-strategy.md](../applications/10-funding-strategy.md) · Omega: #5

- [ ] **F19.** Submit Warhol Arts Writers Grant ($15K-$50K) — **opens May 1** (~4 hrs)
  - URL: https://www.artswriters.org · Fit: 7/10
  - Articles, books, short-form writing about contemporary visual art. 41 essays = strong portfolio.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 3

- [ ] **F20.** Submit Headlands Center residency (fully funded) — **window Apr 1-Jun 1** (~3 hrs)
  - Fit: **9/10**. Airfare, meals, housing, $1K/mo stipend. 4-10 weeks, Sausalito CA.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 4

- [ ] **F21.** Submit Recurse Center application (free, Brooklyn) — rolling (~2 hrs)
  - URL: https://www.recurse.com/ · Fit: **9/10**
  - Free, no cost. 6-12 weeks in Brooklyn. Self-directed programming retreat. Perfect fit.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 4

- [ ] **W3.** Pitch Logic Magazine ($1,200-$2K/essay) — rolling, themed issues
  - URL: https://logicmag.io · Fit: 8/10
  - Pitch: "Governance as Artistic Medium" — technology criticism angle.
  - Source: [11-funding-research-exhaustive.md](../applications/11-funding-research-exhaustive.md) Part 5

- [ ] **M1-II.** Recruit and run first stranger test — protocol at `docs/operations/stranger-test-protocol.md`
  - 1 participant, 5 tasks, scoring rubric
  - Source: [e2g-ii P2](../evaluation/e2g-ii-action-items.md) · Omega: #2, #4, #16
  - Recommended sprint: 30 PEREGRINUS

- [ ] **M3-II.** Refresh portfolio with post-construction evidence — 33 sprints, omega scorecard, live product
  - Site: `4444j99.github.io/portfolio/`
  - **Partial:** RENOVATIO updated all 5 data JSON files (97 repos, 94 ACTIVE, 33 sprints, 41 essays). Omega scorecard page added (pre-validation maturation session). Remaining: visual verification after deploy, push portfolio changes.
  - Source: [e2g-ii P2](../evaluation/e2g-ii-action-items.md) · Omega: #15

- [ ] **M6-II.** CI restructure — make CI fail when no tests, require explicit `skip_tests: true`
  - 17 disabled cron workflows remain disabled (Sprint 12 ILLUSTRATIO)
  - Source: [e2g-ii P2](../evaluation/e2g-ii-action-items.md), carried from E2G-I M4

- [x] **M9-II.** Fix fetch-familiar-friends CI — completed 2026-02-17 (downgraded `@types/react-dom` from ^19.2.3 to ^18.3.5 to match runtime React 18.2.0, closes #200)
  - Source: AMPLIFICATIO CI investigation · Omega: #1, #17

- [x] **M10-II.** Fix life-my--midst--in CI — completed 2026-02-17 (downgraded ESLint ^10.0.0 to ^9.39.2, added design-system vitest.config.ts with 20% thresholds, closes #91)
  - Source: AMPLIFICATIO CI investigation · Omega: #1, #8, #17

- [x] **M7-II.** Registry cleanup: 3 repos archived on GitHub but marked ACTIVE — nexus--babel-alexandria-, 4-ivi374-F0Rivi4, cog-init-1-0- — completed 2026-02-17 (RENOVATIO: all 3 archived in registry, ACTIVE 90→87, ARCHIVED 7→10)
  - Source: Sprint 32 SENSORIA findings

- [x] **M8-II.** Resolve 5 ghost repos — completed 2026-02-17 (RENOVATIO: all 5 exist on GitHub and are active; "ghost" was false alarm from missing local clones, not missing remotes)
  - Source: Sprint 32 SENSORIA findings

- [x] **S1-II.** Complete 30-day soak test and generate report — completed 2026-03-18 (32/30 days, 0 incidents)
  - Command: `python3 scripts/soak-test-monitor.py report --days 30`
  - Source: [e2g-ii P3](../evaluation/e2g-ii-action-items.md) · Omega: #1, #17

- [ ] **S4-II.** Write 2 planned essays (from Sprint 23 PUBLICATIO backlog)
  - ~~"constraint-alchemy-workshop"~~ — completed 2026-02-17 (essay #37, ~2400 words)
  - "performance-platform-methodology" (target Wed Mar 18)
  - Source: [e2g-ii P3](../evaluation/e2g-ii-action-items.md)

- [ ] **S6-II.** Pursue conference talk or workshop proposal — AI-conductor methodology talk
  - Venues: Strange Loop, XOXO, Processing Community Day
  - **Partial:** 2 talk proposals drafted (AMPLIFICATIO) — `docs/applications/conference-proposals/ai-conductor-talk.md` and `constraint-alchemy-talk.md`. Remaining: submit when CFPs open.
  - Source: [e2g-ii P3](../evaluation/e2g-ii-action-items.md) · Omega: #14

---

## NEEDS INCOME — Requires Spending Money

- [ ] **G3.** Ghost newsletter hosting (~$9/mo or self-host) — enables email distribution channel
  - Source: [autonomous-setup-guide](./autonomous-setup-guide.md) §6

- [ ] **M2-II.** Stripe payment integration for life-my--midst--in — connect real Stripe test keys
  - Mock fallback already in codebase
  - Source: [e2g-ii P2](../evaluation/e2g-ii-action-items.md) · Omega: #9, #10
  - Recommended sprint: 31 MERCATURA

- [ ] **M5-II.** Set up monitoring/alerting for life-my--midst--in — Sentry error tracking + uptime monitoring
  - Required before claiming "product live" credibly
  - Source: [e2g-ii P2](../evaluation/e2g-ii-action-items.md)

---

## NEEDS EXTERNAL — Waiting on Someone or Something Else

- [ ] **S2-II.** Host first salon (ORGAN-VI community event) — need ≥2 external participants
  - Source: [e2g-ii P3](../evaluation/e2g-ii-action-items.md) · Omega: #11
  - Recommended sprint: 33 CONVIVIUM

- [ ] **S3-II.** Create contribution pathway for external contributors — need community activity first
  - CONTRIBUTING.md templates, good-first-issue labels, onboarding docs
  - **Partial:** CONTRIBUTING.md written (corpvs-testamentvm root), 5 good-first-issues created across 150 repos (AMPLIFICATIO). Remaining: first external contribution, community onboarding docs.
  - Source: [e2g-ii P3](../evaluation/e2g-ii-action-items.md) · Omega: #12
  - Recommended sprint: Catalog item 47 HOSPITIUM

- [ ] **S5-II.** Investigate universal-mail--automation as second product candidate
  - Sprint 25 INSPECTIO recommended INVESTIGATE status
  - Source: [e2g-ii P3](../evaluation/e2g-ii-action-items.md)

---

## COMPLETED — Done Since Last Review

> Move items here with a completion date. Archive monthly.

- [x] **E1.** Refresh operational cadence Part IV — completed 2026-02-16 (Sprint 28 RECOGNITIO)
  - Source: [e2g-ii P1](../evaluation/e2g-ii-action-items.md)
- [x] **E2.** Enable non-dry-run soak test monitoring — completed 2026-02-17 (workflow configured without --dry-run, first cron run 2026-02-18 08:00 UTC)
  - Source: [e2g-ii P1](../evaluation/e2g-ii-action-items.md) · Omega: #1, #3, #17
- [x] **E4.** Deploy essay drafts #34 and #35 — completed 2026-02-16 (Sprint 27 BETA-VITAE)
  - Source: [e2g-ii P1](../evaluation/e2g-ii-action-items.md) · Omega: #6
- [x] **X4.** Make first social media post — completed 2026-02-17 (HERMETICUM: Mastodon + Discord, distribution issue #45)
  - Source: [e2g-ii P0](../evaluation/e2g-ii-action-items.md) · Omega: feeds #7, #13
- [x] **E5.** Write "Construction Addiction" essay (#36) — completed 2026-02-17 (HERMETICUM: ~2600 words, SP2-II→narrative)
  - Source: [e2g-ii P1](../evaluation/e2g-ii-action-items.md) · Omega: #6
- [x] **M4-II.** Improve seed.yaml coverage from 44% to 100% — completed 2026-02-17 (Sprint 32 SENSORIA — 82/82 eligible repos)
  - Source: [e2g-ii P2](../evaluation/e2g-ii-action-items.md)
- [x] **M7-II.** Registry cleanup: 3 archived-on-GitHub repos marked ACTIVE — completed 2026-02-17 (RENOVATIO: ACTIVE 90→87, ARCHIVED 7→10)
  - Source: Sprint 32 SENSORIA findings
- [x] **M8-II.** Resolve 5 ghost repos — completed 2026-02-17 (all 5 exist on GitHub; "ghost" was false alarm from missing local clones)
  - Source: Sprint 32 SENSORIA findings
- [x] **M9-II.** Fix fetch-familiar-friends CI — completed 2026-02-17 (@types/react-dom v19→v18, closes #200)
  - Source: AMPLIFICATIO CI investigation
- [x] **M10-II.** Fix life-my--midst--in CI — completed 2026-02-17 (ESLint 10→9.x, design-system coverage 75%→20%, closes #91)
  - Source: AMPLIFICATIO CI investigation
- [x] **S1-II.** Complete 30-day soak test — completed 2026-03-18 (32/30 days, 0 incidents)
  - Source: [e2g-ii P3](../evaluation/e2g-ii-action-items.md) · Omega: #1, #17
- [x] **X3.** Submit 9 job applications — completed 2026-03-19 (Anthropic, Coinbase, Temporal, Cursor, Datadog, Deepgram, Perplexity, Railway, Render)
  - Source: [e2g-ii P0](../evaluation/e2g-ii-action-items.md) · Omega: #5, feeds #7

---

## Archive

> Items moved from COMPLETED at monthly review, with date range.

*No archived items yet.*

---

## Provenance Summary

| Source Document | Items Drawn | Coverage |
|----------------|-------------|----------|
| [`e2g-ii-action-items.md`](../evaluation/e2g-ii-action-items.md) | 20 of 21 (E1, E2, E4, M4-II, S1-II, X3 completed) | 100% of open items |
| [`autonomous-setup-guide.md`](./autonomous-setup-guide.md) | 3 of 3 PENDING/OPTIONAL | 100% |
| [`10-funding-strategy.md`](../applications/10-funding-strategy.md) | 9 items (F1-F9) | Funding strategy rewrite |
| [`11-funding-research-exhaustive.md`](../applications/11-funding-research-exhaustive.md) | 15 items (F10-F21, W1-W3) | Exhaustive research integration |
| [`operational-cadence.md`](./operational-cadence.md) Part IV | Subsumed by e2g-ii items | Cross-referenced |
| [`sprint-catalog.md`](../strategy/sprint-catalog.md) | Referenced via recommended sprints | Menu, not queue |
| Sprint 32 SENSORIA findings | 2 new items (M7-II, M8-II) | Registry anomalies |
| AMPLIFICATIO CI investigation | 2 new items (M9-II, M10-II) | Deferred CI fixes |

**Total items:** 54 (2 READY, 32 TIME, 3 INCOME, 3 EXTERNAL, 14 COMPLETED) — 9 of the READY/TIME items are STAGED (materials ready, awaiting submission/execution). 3 TIME items expired (F4 Mar 6, F14 Mar 15, E3 Mar 18).
**Late agent integration (2026-02-17):** F22 (Doris Duke $150K, Mar 2) from creative tech agent. F24 (Watermill Center, **Feb 18 TOMORROW**) from residency agent — free housing/food, Long Island, 7/10 fit.
**Research integration (2026-02-17):** 15 new items from exhaustive funding research — 12 funding (F10-F21) + 3 writing income (W1-W3). Key additions: Prix Ars Electronica (Mar 4), S+T+ARTS (Mar 4), PEN America (rolling), WFF Housing ($30K/3yr), Whiting ($40K), Headlands (9/10), Recurse Center (9/10), premium writing income (Noema, Logic, GLR).
**Strategy rewrite (2026-02-17):** 9 funding items added (F1-F9). Benefits cliff note added. NEEDS TIME reordered by deadline urgency (F3 Artadia Mar 1 → F9 Processing ~Apr-May). Funding submissions classified as external-facing (compatible with P0 hermetic seal rule).
**ERUPTIO session (2026-02-18):** 9 items staged (materials prepared, not yet submitted) — X1 (CL5 script), X2 (deploy guide), F1 (Sponsors setup guide), F3 (Artadia script), F10 (Prix Ars script), F11 (S+T+ARTS script), F12 (PEN America script), F22 (Doris Duke script), F24 (Watermill script). Submission scripts clipboard-ready; execution awaiting human action.
**Previous session:** Late agent integration + research integration (2026-02-17) — 200+ opportunities researched across 5 domains, top targets added to queue

---

*This document was created on 2026-02-17 as the fourth governance document, completing the quadrilateral: roadmap (destination) + catalog (menu) + cadence (rhythm) + rolling TODO (queue). Review weekly at Friday retrospective. Items that persist for 3+ months without progress should be reassessed — they may belong in the catalog's unscheduled list rather than the active queue.*
