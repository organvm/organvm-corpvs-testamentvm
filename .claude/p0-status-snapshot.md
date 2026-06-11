# IRF P0 surface — snapshot

**Last check:** 2026-06-11T11:13:00Z
**Count:** 40 open P0 items

## Delta since prior snapshot
- Closed: IRF-SYS-201 (resolved by DONE-602: conductor fleet registry populated), IRF-VAC-001 (renamed/split to IRF-VAC-001a–d)
- Opened: IRF-APP-088 (6 dormant income opportunities from 2026-06-06 inbox triage), IRF-VAC-001a (SGO tracking issue — PARTIAL, replaces IRF-VAC-001)
- Status-changed: none

## Per-domain rollup

| Domain | Open P0 count |
|--------|--------------|
| Session-Discovered | 12 |
| P0 | 11 |
| Governance & Standards | 4 |
| ORGAN-III | 3 |
| Operations | 3 |
| PERSONAL | 2 |
| Security | 2 |
| GitHub Issue Trail (Vacuum 1) | 1 |
| ORGAN-I | 1 |
| ORGAN-IV | 1 |

## Items

| ID | Domain | Status | Description |
|----|--------|--------|-------------|
| IRF-APP-087 | Session-Discovered | OPEN | 39 outreach messages prepared but 0 sent — pipeline warm-path unactivated. 10 messages ready to send, still 0 sent. Human action required. |
| IRF-APP-088 | Session-Discovered | OPEN | Act on the 6 dormant income opportunities from 2026-06-06 inbox triage: Longo/Zapata depo reply in Drafts, contradictory Senator Lanza/NYS DOL drafts, Ross Townsend/Lawrence Harvey Rust InMail, 3 staffing re-engagements. |
| IRF-CRP-018 | Session-Discovered | OPEN | 3 modified-modified (MM) JSON config files: ~/.claude.json, ~/.claude/settings.json, ~/Library/Application Support/Claude/claude_desktop_config.json. Source and runtime both modified; drift undecidable mechanically. |
| IRF-III-026 | ORGAN-III | OPEN | VACUUM: public-record-data-scrapper has no payment flow. 526 tests, deployed on Netlify+Render, UCC-MCA lead generation, zero revenue. Requires Stripe integration + 3-tier pricing. |
| IRF-III-027 | ORGAN-III | OPEN | VACUUM: content-engine--asset-amplifier (Cronus) has no payment flow. CF Pages + Cloudflare Workers + Neon PostgreSQL, 7 AI providers, zero marginal cost. Requires Stripe integration + freemium pricing. |
| IRF-III-035 | ORGAN-III | OPEN | VACUUM: sovereign-systems hub quizFormUrl is empty. src/data/hub.config.ts:268 has quizFormUrl: ''. GH#58. |
| IRF-III-047 | Session-Discovered | OPEN | Styx revenue gap — premortem completed. 20 failure modes identified. Revised plan: Week 1 cold messages, Week 2 calls, Week 3 extract artifact, Week 4 invoice. GH#598. |
| IRF-INST-001 | Session-Discovered | OPEN | Apply to NLnet NGI0 Commons Fund — EUR 37,080 for Cvrsvs Honorvm governance engine extraction. Draft complete. Deadline was June 1, 2026 — check next call. |
| IRF-INST-015 | Session-Discovered | OPEN | Human review pass on NLnet draft — read aloud, verify all claims, check scoring criteria alignment. Then submit web form at nlnet.nl/propose/. |
| IRF-INST-016 | Session-Discovered | OPEN | Register ORCID — persistent researcher identifier. 5 minutes at orcid.org/register. Required for academic funders (Sloan, NSF). |
| IRF-OPS-014 | Operations | OPEN | Overreach Incident remediation — Stream D 17-commit push to hokage-chess origin/main without acolyte authorization. Decision needed: accept as live or rollback via force-with-lease. |
| IRF-OPS-021 | Operations | OPEN | README.md merge-conflict markers on main in meta-organvm/organvm-corpvs-testamentvm/README.md. Lines 14–23 and 312–318 contain unresolved diff3-style conflict markers. Corruption is live on main. |
| IRF-OPS-028 | Operations | OPEN | Word-count metric generator regression cascading into 87+ files across 3 repos. total_words_short reported as ~6K+ where previously ~404K+/~739K+/~766K+. All generator-cascaded commits blocked. |
| IRF-OPS-061 | Session-Discovered | OPEN | organvm atoms pipeline --write cadence has slipped — atom registry last modified 2026-05-10, 11+ days stale at audit time. Unifier protocol first principle violated. |
| IRF-OPS-069 | Session-Discovered | OPEN | domus-memory-sync line 81 + line 100 scope filter accepts ONLY *.md files, silently dropping *.mmd and other plan-class extensions. Rule #2 violation surfaced 2026-05-22. |
| IRF-PRT-027 | PERSONAL | OPEN | hokagechess.com domain registration (Cloudflare Registrar). Verified available 2026-04-25 via Verisign. Required for hokage-chess landing page deploy and brand identity. |
| IRF-PRT-028 | PERSONAL | OPEN | hokage-chess landing page deploy to Vercel. Repo 4444J99/hokage-chess is private; Next.js 16 build ready. Depends on IRF-PRT-027 (domain) and IRF-PRT-030 (Kit API key). |
| IRF-PRT-060 | Session-Discovered | OPEN | Kit API key (PRT-030) gates Hokage L2 deploy. 60s user action; without it, email funnel L2 cannot ship. Silent since Apr 25. |
| IRF-PRT-061 | Session-Discovered | OPEN | hokagechess.com domain registration — verified AVAILABLE 2026-04-25. Time-decay risk: domain may be taken by squatter. Register today (~$15/yr). |
| IRF-RES-003 | P0 | OPEN | Define "readiness" construct independently of its operationalization — convene expert panel. GH#343 (INQ-2026-013, Wave 3). |
| IRF-RES-004 | P0 | OPEN | Conduct factor analysis on the omega scorecard — perform EFA on all indicators across repo population. GH#340 (INQ-2026-013, Wave 1). |
| IRF-RES-006 | P0 | OPEN | Build a controlled vocabulary registry for domain terms — machine-readable mapping of canonical terms to synonyms. GH#339 (INQ-2026-013, Wave 1). |
| IRF-RES-007 | P0 | OPEN | Make incompleteness visible in all governance verdicts — every automated verdict must include explicit scope statement. GH#344 (INQ-2026-013, Wave 3). |
| IRF-RES-008 | P0 | OPEN | Formalize the IRA panel protocol — strengthen IRA panel as Tarskian escape. GH#345 (INQ-2026-013, Wave 4). |
| IRF-RES-009 | P0 | OPEN | Implement seed.yaml semantic accuracy tracking — machine-readable registry of properties not covered by seed.yaml validation. GH#346 (INQ-2026-013, Wave 4). |
| IRF-RES-010 | P0 | OPEN | Separate self-maintenance from self-improvement in governance — two distinct operational modes with architectural enforcement. GH#348 (INQ-2026-013, Wave 5). |
| IRF-RES-011 | P0 | OPEN | Establish the hybrid topology principle as architectural law — codify inter-organ hierarchical flow and intra-organ rhizomatic connectivity. GH#341 (INQ-2026-013, Wave 2). |
| IRF-RES-012 | P0 | OPEN | Design governance artifacts as boundary objects — redesign seed.yaml, CLAUDE.md, governance-rules.json as boundary objects. GH#349 (INQ-2026-013, Wave 5). |
| IRF-RES-013 | P0 | OPEN | Implement temporal staging for governance validation — always validate previous state using current schema. GH#342 (INQ-2026-013, Wave 2). |
| IRF-RES-014 | P0 | OPEN | Implement context-specific governance norms — differentiate thresholds by organ, language, and project type. GH#347 (INQ-2026-013, Wave 4; conditional on RES-004). |
| IRF-SEC-002 | Security | OPEN | OpenAI API key exposed in public Docker image cetaceang/openai-king (92MB, 507 pulls). Action: rotate at platform.openai.com, audit usage logs, report to Docker Hub. |
| IRF-SEC-005 | Security | OPEN | Gmail app password not revoked in Google Account. Revocation performed 2026-06-06 per memory record — pending one live verification at Google to close this row. |
| IRF-SYS-009 | Governance & Standards | OPEN | Gmail notification hygiene — filter designed in S36. HUMAN ACTION NEEDED: create Gmail filter, uncheck auto-watch repositories, set org routing to web-only. |
| IRF-SYS-011 | Session-Discovered | OPEN | GoDaddy domain met4vers.io EXPIRED — grace period active. Decision needed: renew or let expire. External blocker: requires GoDaddy account login. |
| IRF-SYS-087 | Governance & Standards | OPEN | UMFAS birth — compress the corpus into the space. Birth = compression: inventory → atomize → directory exists containing everything. Top-dir: organvm/{organvm, meta, taxis}. GH#310. |
| IRF-SYS-137 | Governance & Standards | OPEN | Gemini Takeout export still pending — HUMAN ACTION NEEDED. Check takeout.google.com for ready export, download, place in my-knowledge-base/intake/canonical/sources/. |
| IRF-SYS-156 | Governance & Standards | OPEN | GitHub notification backlog — 4,115 total / 1,448 unread / 12 explicit-attention items at risk of being lost in CI noise. Triage ladder: bulk-mark CI noise, address 12 explicit-attention items. |
| IRF-TAX-VAC-001 | ORGAN-IV | OPEN | Execute cold-reading Stranger Test on personalized-storefront-render SKILL.md. Verification gate to graduate substrate from "self-attested" to "verified." |
| IRF-THE-VAC-004 | ORGAN-I | OPEN | Implement corpus persona-extract in conversation-corpus-engine. Extract vocabulary/yearnings from session JSONLs. Highest compounding move. |
| IRF-VAC-001a | GitHub Issue Trail (Vacuum 1) | PARTIAL | Create tracking issue for SGO research programme on corpvs-testamentvm (13 papers, 74 tasks). 3 arXiv issues created on praxis-perpetua (#28–#30). Umbrella tracking issue on corpvs-testamentvm still needed. |
