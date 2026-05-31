# IRF P0 surface — snapshot

**Last check:** 2026-05-31T11:13:00Z
**Count:** 40 open P0 items

## Delta since prior snapshot
- Closed: IRF-VAC-001 (ID renamed to IRF-VAC-001a — 3 of 4 arXiv sub-tasks created on praxis-perpetua; umbrella tracking issue on corpvs-testamentvm still needed)
- Opened: IRF-VAC-001a (PARTIAL — same underlying work item; 3 arXiv submission issues exist, corpvs umbrella issue remains to be created)
- Status-changed: IRF-VAC-001 OPEN → IRF-VAC-001a PARTIAL (via ID rename)

## Per-domain rollup

| Domain | Open P0 count |
|--------|--------------|
| Session-Discovered | 12 |
| P0 (Research / SGO) | 11 |
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
| IRF-APP-087 | Session-Discovered | OPEN | 39 outreach messages prepared but 0 sent — pipeline warm-path unactivated. 9 targets dead, 10 messages ready to send (3 personalized follow-ups + 7 LinkedIn connects), 6 follow-ups written. Still 0 sent. Human action required. |
| IRF-CRP-018 | Session-Discovered | OPEN | 3 modified-modified (`MM`) JSON config files: `~/.claude.json`, `~/.claude/settings.json`, `~/Library/Application Support/Claude/claude_desktop_config.json`. Source and runtime both modified; drift undecidable mechanically. Per-file user inspection required. |
| IRF-III-026 | ORGAN-III | OPEN | VACUUM: public-record-data-scrapper has no payment flow. 526 tests, deployed on Netlify+Render, UCC-MCA lead generation. Required: Stripe integration, 3-tier pricing page, sign-up flow. |
| IRF-III-027 | ORGAN-III | OPEN | VACUUM: content-engine--asset-amplifier (Cronus) has no payment flow. CF Pages + Cloudflare Workers + Neon PostgreSQL, 7 AI providers. Required: Stripe integration, free-tier gate, pricing page, sign-up flow. |
| IRF-III-035 | ORGAN-III | OPEN | VACUUM: sovereign-systems hub `quizFormUrl` is empty. `src/data/hub.config.ts:268` has `quizFormUrl: ''`. Maddie response required for GHL form URL. GH#58. |
| IRF-III-047 | Session-Discovered | OPEN | Styx revenue gap — premortem completed. 20 failure modes identified. Revised plan: Week 1 (20 cold messages), Week 2 (15-min calls), Week 3 (extract minimum artifact), Week 4 (send invoice). GH#598. |
| IRF-INST-001 | Session-Discovered | OPEN | Apply to NLnet NGI0 Commons Fund — EUR 37,080 for Cvrsvs Honorvm governance engine extraction. Draft complete. Deadline: June 1, 2026 12:00 CEST (13th call). REMAINING: human review pass + form submission. See IRF-INST-015. |
| IRF-INST-015 | Session-Discovered | OPEN | Human review pass on NLnet draft — read aloud, verify claims, check scoring criteria alignment. Then submit web form at nlnet.nl/propose/ selecting "NGI Zero Commons Fund." Deadline: June 1, 2026 12:00 CEST. |
| IRF-INST-016 | Session-Discovered | OPEN | Register ORCID — persistent researcher identifier. 5 minutes at orcid.org/register. Required for academic funders (Sloan, NSF). No excuse for delay. |
| IRF-OPS-014 | Operations | OPEN | Overreach Incident remediation — Stream D 17-commit push to hokage-chess origin/main without acolyte authorization. Push range `0a31116..7d29278` live on `4444J99/hokage-chess` main. Decision: accept or rollback via force-with-lease. |
| IRF-OPS-021 | Operations | OPEN | README.md merge-conflict markers on main — `meta-organvm/organvm-corpvs-testamentvm/README.md`. Lines 14–23 and 312–318. All three sides carry identical content; mechanical resolution. User decision required. |
| IRF-OPS-028 | Operations | OPEN | Word-count metric generator regression cascading into 87+ files across 3 repos. `total_words_short` reported as `~6K+` vs prior `~404K+/~766K+`. Fix requires source-walk on metrics generator + golden-set validation + bulk-update. |
| IRF-OPS-061 | Session-Discovered | OPEN | `organvm atoms pipeline --write` cadence slipped — atom registry was 11 days stale at audit time 2026-05-21. Unifier protocol violated; recent session content unrepresented. Durable cadence mechanism needs human decision (SessionStart hook, scheduled task, or closeout SKILL). |
| IRF-OPS-069 | Session-Discovered | OPEN | `domus-memory-sync` scope filter drops `*.mmd` plan files, causing Rule #2 violations. Fix shipped this session for `.mmd` but future extensions (`.d2`, `.puml`, `.drawio`) need a declarative extension list at top of script for true closure. |
| IRF-PRT-027 | PERSONAL | OPEN | hokagechess.com domain registration (Cloudflare Registrar). Verified available 2026-04-25. Required for hokage-chess landing page deploy. Time-decay squatter risk. ~5-min checkout. |
| IRF-PRT-028 | PERSONAL | OPEN | hokage-chess landing page deploy to Vercel. Repo `4444J99/hokage-chess` is private; Next.js 16 build ready. Depends on IRF-PRT-027 (domain) and IRF-PRT-030 (Kit API key). |
| IRF-PRT-060 | Session-Discovered | OPEN | Kit API key (PRT-030) gates Hokage L2 deploy. 60s user action; without it, email funnel L2 cannot ship. Silent since Apr 25. |
| IRF-PRT-061 | Session-Discovered | OPEN | hokagechess.com domain registration — verified AVAILABLE 2026-04-25. Time-decay risk: domain may be taken by squatter. Register today (~$15/yr Cloudflare or Namecheap). |
| IRF-RES-003 | P0 (Research / SGO) | OPEN | Define "readiness" construct independently of its operationalization — convene expert panel. GH#343 (commission INQ-2026-013, Wave 3). |
| IRF-RES-004 | P0 (Research / SGO) | OPEN | Conduct factor analysis on omega scorecard — EFA on all indicators; determine single vs. multiple latent factors. GH#340. |
| IRF-RES-006 | P0 (Research / SGO) | OPEN | Build a controlled vocabulary registry for domain terms — machine-readable synonym mapping; validate new names in CI. GH#339. |
| IRF-RES-007 | P0 (Research / SGO) | OPEN | Make incompleteness visible in all governance verdicts — every verdict must include explicit scope statement. GH#344. |
| IRF-RES-008 | P0 (Research / SGO) | OPEN | Formalize the IRA panel protocol — explicit guidance on semantic properties automated checks cannot assess. GH#345 (HUMAN — external rater recruitment required). |
| IRF-RES-009 | P0 (Research / SGO) | OPEN | Implement seed.yaml semantic accuracy tracking — registry of properties not covered by seed.yaml validation. GH#346. |
| IRF-RES-010 | P0 (Research / SGO) | OPEN | Separate self-maintenance from self-improvement in governance — two distinct operational modes with architectural enforcement. GH#348. |
| IRF-RES-011 | P0 (Research / SGO) | OPEN | Establish the hybrid topology principle as architectural law — codify inter-organ hierarchical / intra-organ rhizomatic connectivity. GH#341. |
| IRF-RES-012 | P0 (Research / SGO) | OPEN | Design governance artifacts as boundary objects — redesign seed.yaml, CLAUDE.md, governance-rules.json for human/machine/AI communities. GH#349. |
| IRF-RES-013 | P0 (Research / SGO) | OPEN | Implement temporal staging for governance validation — validate previous state using current state, never current using itself. GH#342. |
| IRF-RES-014 | P0 (Research / SGO) | OPEN | Implement context-specific governance norms — differentiate thresholds by organ, language, project type. GH#347 (CONDITIONAL on RES-004). |
| IRF-SEC-002 | Security | OPEN | OpenAI API key exposed in public Docker image `cetaceang/openai-king` (507 pulls, live since Aug 2025). Action: rotate at platform.openai.com, audit usage logs, report to Docker Hub. |
| IRF-SEC-005 | Security | OPEN | Gmail app password not revoked. Label `gmail-app-pw-033526` (created 2026-03-25) grants IMAP/SMTP to padavano.anthony@gmail.com. Action: revoke at myaccount.google.com/apppasswords. |
| IRF-SYS-009 | Governance & Standards | OPEN | Gmail notification hygiene — filter designed in S36. HUMAN ACTION NEEDED: (1) Create Gmail filter, (2) uncheck "Automatically watch repositories" in GitHub Settings, (3) set org routing to web-only. |
| IRF-SYS-011 | Session-Discovered | OPEN | GoDaddy domain `met4vers.io` EXPIRED — cancellation notice received. Grace period active. Decision needed: renew or let expire. Requires GoDaddy account login. |
| IRF-SYS-087 | Governance & Standards | OPEN | UMFAS birth — compress the corpus into the space. Reframed 2026-04-06: Birth = compression of 766K-word corpus into atomized self-contained units. Steps: full corpus inventory → atomization → directory exists containing everything. GH#310. |
| IRF-SYS-137 | Governance & Standards | OPEN | Gemini Takeout export still pending — HUMAN ACTION NEEDED. Google Takeout requested for Gemini conversation history but export not yet delivered/downloaded. Check takeout.google.com. |
| IRF-SYS-156 | Governance & Standards | OPEN | GitHub notification backlog — 4,115 total / 1,448 unread / 12 explicit-attention items at high risk of being lost in CI noise. Triage ladder documented. Human action: ~30 min bulk + ~1–2h explicit-12 triage. |
| IRF-SYS-201 | Session-Discovered | OPEN | Conductor MCP operationally cold despite Dispatch Protocol mandate — 4× `conductor_fleet_dispatch` calls returned `recommended_agent: null`. 5 bench-agent binaries installed but routing table empty. Fleet registration mechanism not yet discovered. |
| IRF-TAX-VAC-001 | ORGAN-IV | OPEN | Execute cold-reading Stranger Test on personalized-storefront-render SKILL.md. Verification gate to graduate substrate from "self-attested" to "verified." |
| IRF-THE-VAC-004 | ORGAN-I | OPEN | Implement corpus persona-extract in conversation-corpus-engine. Highest compounding move: extract vocabulary/yearnings from session JSONLs. |
| IRF-VAC-001a | GitHub Issue Trail (Vacuum 1) | PARTIAL | Create tracking issue for SGO research programme on corpvs-testamentvm (13 papers, 74 tasks, 3 arXiv packages, 4 governance declarations). PARTIAL: 3 arXiv submission issues created on praxis-perpetua (#28, #29, #30). Umbrella tracking issue on corpvs-testamentvm still needed. |
