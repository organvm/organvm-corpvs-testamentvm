# IRF P0 surface — snapshot

**Last check:** 2026-06-06T11:13:00Z
**Count:** 39 open P0 items

## Delta since prior snapshot
- Closed: IRF-SYS-156 (downgraded to P1 — new P1 update row at top-level section "PARTIALLY ADVANCED (S-Achilles-A)" supersedes original P0 row; humans-waiting queue reduced 16→8, dotfiles CI fixed)
- Opened: none
- Status-changed: IRF-SYS-156 (P0 → P1 via advancement row); IRF-VAC-001 → IRF-VAC-001a (ID precision correction — prior snapshot recorded wrong ID suffix; same item)

## Per-domain rollup

| Domain | Open P0 count |
|--------|--------------|
| Research (RES) | 11 |
| Operations (OPS) | 5 |
| Governance & Standards (SYS) | 5 |
| ORGAN-III | 4 |
| Personal (PRT) | 4 |
| Institutional (INST) | 3 |
| Security (SEC) | 2 |
| Application Pipeline (APP) | 1 |
| Corpus (CRP) | 1 |
| GitHub Issue Trail (VAC) | 1 |
| ORGAN-I | 1 |
| ORGAN-IV | 1 |

## Items

| ID | Domain | Status | Description |
|----|--------|--------|-------------|
| IRF-APP-087 | Application Pipeline | OPEN | 39 outreach messages prepared but 0 sent — pipeline warm-path unactivated. ADVANCED: triage complete, 10 messages ready to send, still 0 sent. Human action required. |
| IRF-CRP-018 | Corpus | OPEN | 3 modified-modified (MM) JSON config files: `~/.claude.json`, `~/.claude/settings.json`, `~/Library/Application Support/Claude/claude_desktop_config.json`. Per-file user inspection required. |
| IRF-III-026 | ORGAN-III | OPEN | VACUUM: public-record-data-scrapper has no payment flow. 526 tests, deployed on Netlify+Render. Required: Stripe integration, pricing page, sign-up flow. |
| IRF-III-027 | ORGAN-III | OPEN | VACUUM: content-engine--asset-amplifier (Cronus) has no payment flow. CF Pages + Cloudflare Workers + Neon PostgreSQL, 7 AI providers. Required: Stripe, pricing, sign-up. |
| IRF-III-035 | ORGAN-III | OPEN | VACUUM: sovereign-systems hub `quizFormUrl` is empty. `src/data/hub.config.ts:268` has `quizFormUrl: ''`. GH#58. Awaiting Maddie response. |
| IRF-III-047 | ORGAN-III | OPEN | Styx revenue gap — premortem completed. 20 failure modes on "extract sellable artifact + get paid in 30 days." Week 1 target: 20 cold messages. GH#598. |
| IRF-INST-001 | Institutional | OPEN | Apply to NLnet NGI0 Commons Fund — EUR 37,080. Draft complete. Next deadline: June 1, 2026 CEST (may be past). Human review + form submission required. See IRF-INST-015. |
| IRF-INST-015 | Institutional | OPEN | Human review pass on NLnet draft — read aloud, verify claims, check scoring criteria. Then submit at nlnet.nl/propose/ (NGI Zero Commons Fund). |
| IRF-INST-016 | Institutional | OPEN | Register ORCID — persistent researcher identifier. 5 minutes at orcid.org/register. Required for academic funders (Sloan, NSF). |
| IRF-OPS-014 | Operations | OPEN | Overreach Incident — Stream D 17-commit push to hokage-chess origin/main without acolyte authorization. Decision: accept push or rollback via force-with-lease. |
| IRF-OPS-021 | Operations | OPEN | README.md merge-conflict markers on main in `meta-organvm/organvm-corpvs-testamentvm/README.md`. Lines 14–23 and 312–318. Mechanical resolution (all three sides identical content). |
| IRF-OPS-028 | Operations | OPEN | Word-count metric generator regression cascading into 87+ files across 3 repos. `total_words_short` reported as `~6K+` (was `~404K+`). Blocks all generator-cascaded commits. |
| IRF-OPS-061 | Operations | OPEN | `organvm atoms pipeline --write` cadence slipped — atom registry 11+ days stale at last audit (2026-05-21). Unifier protocol first principle being violated. |
| IRF-OPS-069 | Operations | OPEN | `domus-memory-sync` scope filter fix shipped but IRF row not closed. Row text indicates fix was deployed; awaits human DONE closure. |
| IRF-PRT-027 | Personal | OPEN | hokagechess.com domain registration (Cloudflare Registrar). Verified available 2026-04-25. Time-decay risk. Required for hokage-chess deploy (IRF-PRT-028). |
| IRF-PRT-028 | Personal | OPEN | hokage-chess landing page deploy to Vercel. Next.js 16 build ready. Depends on IRF-PRT-027 (domain) and IRF-PRT-030 (Kit API key, now closed). |
| IRF-PRT-060 | Personal | OPEN | Kit API key (PRT-030) gates Hokage L2 deploy. 60s user action; without it, email funnel L2 cannot ship. Silent since Apr 25. |
| IRF-PRT-061 | Personal | OPEN | hokagechess.com domain registration — verified AVAILABLE 2026-04-25. Duplicate of IRF-PRT-027 framing; time-decay squatter risk. |
| IRF-RES-003 | Research | OPEN | Define "readiness" construct independently — convene expert panel. GH#343 (commission INQ-2026-013, Wave 3). |
| IRF-RES-004 | Research | OPEN | Conduct factor analysis on omega scorecard — EFA across repo population. GH#340 (INQ-2026-013, Wave 1). Blocked on IRF-RES-003. |
| IRF-RES-006 | Research | OPEN | Build controlled vocabulary registry for domain terms — machine-readable canonical→synonyms mapping. GH#339 (INQ-2026-013, Wave 1). |
| IRF-RES-007 | Research | OPEN | Make incompleteness visible in all governance verdicts — every verdict must include explicit scope statement. GH#344 (INQ-2026-013, Wave 3). |
| IRF-RES-008 | Research | OPEN | Formalize IRA panel protocol — strengthen as Tarskian escape; external rater recruitment required. GH#345 (INQ-2026-013, Wave 4). |
| IRF-RES-009 | Research | OPEN | Implement seed.yaml semantic accuracy tracking — machine-readable registry of properties not covered by seed.yaml validation. GH#346 (INQ-2026-013, Wave 4). |
| IRF-RES-010 | Research | OPEN | Separate self-maintenance from self-improvement in governance — two distinct operational modes. GH#348 (INQ-2026-013, Wave 5; Löb-theorem escape). |
| IRF-RES-011 | Research | OPEN | Establish hybrid topology principle as architectural law — inter-organ hierarchical + intra-organ rhizomatic. GH#341 (INQ-2026-013, Wave 2). |
| IRF-RES-012 | Research | OPEN | Design governance artifacts as boundary objects — seed.yaml, CLAUDE.md, governance-rules.json as multi-community artifacts. GH#349 (INQ-2026-013, Wave 5). |
| IRF-RES-013 | Research | OPEN | Implement temporal staging for governance validation — validate previous state using current state, never self. GH#342 (INQ-2026-013, Wave 2). |
| IRF-RES-014 | Research | OPEN | Implement context-specific governance norms — differentiate thresholds by organ/language/type. GH#347 (INQ-2026-013, Wave 4). Blocked on IRF-RES-003 + IRF-RES-004. |
| IRF-SEC-002 | Security | OPEN | OpenAI API key exposed in public Docker image `cetaceang/openai-king` (507 pulls). Action: rotate at platform.openai.com, audit usage logs, report to Docker Hub. |
| IRF-SEC-005 | Security | OPEN | Gmail app password not revoked — label `gmail-app-pw-033526` (created 2026-03-25) still active. Action: revoke at myaccount.google.com/apppasswords. |
| IRF-SYS-009 | Governance & Standards | OPEN | Gmail notification hygiene — filter designed in S36, not yet created. Human action: Gmail filter + GitHub notification settings (2 min). |
| IRF-SYS-011 | Governance & Standards | OPEN | GoDaddy domain `met4vers.io` EXPIRED — grace period, cancellation notice received 2026-04-15. Decision: renew or let expire. External blocker: GoDaddy login. |
| IRF-SYS-087 | Governance & Standards | OPEN | UMFAS birth — compress corpus into space. Reframed: Birth = COMPRESSION of 766K words corpus → atomized units. GH#310. Blocked on IRF-SYS-085. |
| IRF-SYS-137 | Governance & Standards | OPEN | Gemini Takeout export still pending — HUMAN ACTION NEEDED. Check takeout.google.com, download, place in my-knowledge-base/intake/canonical/sources/. |
| IRF-SYS-201 | Governance & Standards | OPEN | Conductor MCP operationally cold — `conductor_fleet_dispatch` returns null for all work types (0 agents registered). All 5 agent binaries installed but zero registered with conductor. |
| IRF-TAX-VAC-001 | ORGAN-IV | OPEN | Execute cold-reading Stranger Test on personalized-storefront-render SKILL.md. Verification gate to graduate substrate from "self-attested" to "verified." |
| IRF-THE-VAC-004 | ORGAN-I | OPEN | Implement corpus persona-extract in conversation-corpus-engine. Extract vocabulary/yearnings from session JSONLs. Highest compounding move. |
| IRF-VAC-001a | GitHub Issue Trail | OPEN | Create umbrella tracking issue for SGO research programme on corpvs-testamentvm (13 papers, 74 tasks, 3 arXiv packages). PARTIAL: 3 arXiv issues created on praxis-perpetua. |
