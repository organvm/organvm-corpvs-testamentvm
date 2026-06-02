# IRF P0 surface — snapshot

**Last check:** 2026-06-02T11:13:00Z
**Count:** 40 open P0 items (39 OPEN, 1 PARTIAL)

## Delta since prior snapshot
- Closed: IRF-VAC-001 (renamed to IRF-VAC-001a; original ID no longer in P0-open set)
- Opened: IRF-VAC-001a (PARTIAL — same underlying item as IRF-VAC-001, now advanced and relabelled)
- Status-changed: none (all other items remain OPEN)

## Per-domain rollup

| Domain | Open P0 count |
|--------|--------------|
| Session-Discovered | 12 |
| P0 (Research/SGO) | 11 |
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
| IRF-APP-087 | Session-Discovered | OPEN | 39 outreach messages prepared but 0 sent — pipeline warm-path unactivated. ADVANCED: triage complete (9 dead, 10 ready, 6 follow-ups). Still 0 sent. Human action required. |
| IRF-CRP-018 | Session-Discovered | OPEN | 3 modified-modified (`MM`) JSON config files: `~/.claude.json`, `~/.claude/settings.json`, `~/Library/Application Support/Claude/claude_desktop_config.json`. Drift undecidable mechanically — each requires independent human judgment. |
| IRF-III-026 | ORGAN-III | OPEN | VACUUM: public-record-data-scrapper has no payment flow. 526 tests, deployed on Netlify+Render, UCC-MCA lead generation. Zero revenue. Requires Stripe integration + 3-tier pricing. |
| IRF-III-027 | ORGAN-III | OPEN | VACUUM: content-engine--asset-amplifier (Cronus) has no payment flow. CF Pages + Cloudflare Workers + Neon PostgreSQL. Requires Stripe integration + freemium pricing. |
| IRF-III-035 | ORGAN-III | OPEN | VACUUM: sovereign-systems hub `quizFormUrl` is empty. `src/data/hub.config.ts:268`. Blocked on Maddie response for GHL form URL. GH#58. |
| IRF-III-047 | Session-Discovered | OPEN | Styx revenue gap — premortem completed. 20 failure modes identified. Revised plan: Week 1 (20 cold messages), Week 2 (calls), Week 3 (extract), Week 4 (invoice). GH#598. |
| IRF-INST-001 | Session-Discovered | OPEN | Apply to NLnet NGI0 Commons Fund — EUR 37,080 for Cvrsvs Honorvm. Draft complete. Next deadline: June 1, 2026 (may be missed). Requires human review pass + form submission. See IRF-INST-015. |
| IRF-INST-015 | Session-Discovered | OPEN | Human review pass on NLnet draft — read aloud, verify claims, check scoring criteria. Then submit web form at nlnet.nl/propose/. Deadline: June 1, 2026 12:00 CEST. |
| IRF-INST-016 | Session-Discovered | OPEN | Register ORCID — 5 minutes at orcid.org/register. Required for academic funders (Sloan, NSF). |
| IRF-OPS-014 | Operations | OPEN | Overreach Incident remediation — Stream D 17-commit push to hokage-chess origin/main without acolyte authorization. Decision: accept as live or rollback via force-with-lease. |
| IRF-OPS-021 | Operations | OPEN | README.md merge-conflict markers on main — `meta-organvm/organvm-corpvs-testamentvm/README.md` lines 14–23 and 312–318. Mechanical resolution: keep one copy, drop markers. |
| IRF-OPS-028 | Operations | OPEN | Word-count metric generator regression: `total_words_short` shows `~6K+` instead of `~404K+`. Cascading into 87+ files across 3 repos. Requires metrics generator repair + golden-set validation. |
| IRF-OPS-061 | Session-Discovered | OPEN | `organvm atoms pipeline --write` cadence slipped — atom registry 11 days stale at last audit (2026-05-21). Unifier protocol first principle violated. Durable cadence fix needed (hook/schedule/closeout ritual). |
| IRF-OPS-069 | Session-Discovered | OPEN | `domus-memory-sync` scope filter silently drops non-`.md` plan files. Description notes engine fix shipped 2026-05-22 but row not formally closed in IRF. Surface without interpretation. |
| IRF-PRT-027 | PERSONAL | OPEN | hokagechess.com domain registration (Cloudflare Registrar). Verified available 2026-04-25. Time-decay squatter risk. ~5-min checkout. |
| IRF-PRT-028 | PERSONAL | OPEN | hokage-chess landing page deploy to Vercel. Next.js 16 build ready. Depends on IRF-PRT-027 (domain) and IRF-PRT-060 (Kit API key). |
| IRF-PRT-060 | Session-Discovered | OPEN | Kit API key (PRT-030) gates Hokage L2 email funnel deploy. 60s user action. Silent since 2026-04-25. |
| IRF-PRT-061 | Session-Discovered | OPEN | hokagechess.com domain registration — verified AVAILABLE 2026-04-25. ~$15/yr Cloudflare or Namecheap. (Note: duplicates IRF-PRT-027 in substance.) |
| IRF-RES-003 | P0 (Research/SGO) | OPEN | Define "readiness" construct independently of its operationalization — convene expert panel. GH#343. |
| IRF-RES-004 | P0 (Research/SGO) | OPEN | Conduct factor analysis on the omega scorecard — EFA on all indicators across repo population. GH#340. |
| IRF-RES-006 | P0 (Research/SGO) | OPEN | Build a controlled vocabulary registry for domain terms — machine-readable mapping. GH#339. |
| IRF-RES-007 | P0 (Research/SGO) | OPEN | Make incompleteness visible in all governance verdicts — explicit scope statement in every verdict. GH#344. |
| IRF-RES-008 | P0 (Research/SGO) | OPEN | Formalize the IRA panel protocol — strengthen as Tarskian escape. GH#345. Human: external rater recruitment. |
| IRF-RES-009 | P0 (Research/SGO) | OPEN | Implement seed.yaml semantic accuracy tracking — machine-readable registry of properties not covered by validation. GH#346. |
| IRF-RES-010 | P0 (Research/SGO) | OPEN | Separate self-maintenance from self-improvement in governance — two distinct operational modes. GH#348. |
| IRF-RES-011 | P0 (Research/SGO) | OPEN | Establish hybrid topology principle as architectural law — codify inter-organ hierarchical flow. GH#341. |
| IRF-RES-012 | P0 (Research/SGO) | OPEN | Design governance artifacts as boundary objects — redesign seed.yaml, CLAUDE.md, governance-rules.json. GH#349. |
| IRF-RES-013 | P0 (Research/SGO) | OPEN | Implement temporal staging for governance validation — validate previous state using current state. GH#342. |
| IRF-RES-014 | P0 (Research/SGO) | OPEN | Implement context-specific governance norms — differentiate thresholds by organ, language, project type. GH#347. CONDITIONAL on RES-004. |
| IRF-SEC-002 | Security | OPEN | OpenAI API key exposed in public Docker image `cetaceang/openai-king` (507 pulls, live since Aug 2025). Action: rotate at platform.openai.com + audit + report image. |
| IRF-SEC-005 | Security | OPEN | Gmail app password not revoked. Label `gmail-app-pw-033526` grants IMAP/SMTP. 27+ days without revocation. Action: revoke at myaccount.google.com/apppasswords. |
| IRF-SYS-009 | Governance & Standards | OPEN | Gmail notification hygiene — Gmail filter + GitHub notification settings. Human action: 2 min at github.com/settings/notifications + Gmail. |
| IRF-SYS-011 | Session-Discovered | OPEN | GoDaddy domain `met4vers.io` EXPIRED — grace period active. Decision: renew or let expire. Requires GoDaddy account login. |
| IRF-SYS-087 | Governance & Standards | OPEN | UMFAS birth — compress corpus into the space. Reframed: birth = compression of 766K-word corpus into atomized self-contained units. GH#310. Blocker: IRF-SYS-085. |
| IRF-SYS-137 | Governance & Standards | OPEN | Gemini Takeout export still pending. Check takeout.google.com, download, place in my-knowledge-base/intake/canonical/sources/. Human action. |
| IRF-SYS-156 | Governance & Standards | OPEN | GitHub notification backlog — 4,115 total / 1,448 unread / 12 explicit-attention items. Triage ladder documented. Human + Agent action ~2-3h. |
| IRF-SYS-201 | Session-Discovered | OPEN | Conductor MCP operationally cold — fleet routing table empty despite Dispatch Protocol mandate. 4× live dispatch calls returned null. Options: register agents, manual-envelope generator, or amend CLAUDE.md. |
| IRF-TAX-VAC-001 | ORGAN-IV | OPEN | Execute cold-reading Stranger Test on personalized-storefront-render SKILL.md. Verification gate to graduate substrate. |
| IRF-THE-VAC-004 | ORGAN-I | OPEN | Implement corpus persona-extract in conversation-corpus-engine. Extract vocabulary/yearnings from session JSONLs. Highest compounding move. |
| IRF-VAC-001a | GitHub Issue Trail (Vacuum 1) | PARTIAL | Create tracking issue for SGO research programme on corpvs-testamentvm (13 papers, 74 tasks). PARTIAL: 3 arXiv issues created on praxis-perpetua (#28, #29, #30). Umbrella issue on corpvs-testamentvm still needed. |
