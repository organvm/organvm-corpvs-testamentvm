# IRF P0 surface — snapshot

**Last check:** 2026-05-25T11:14:27Z
**Count:** 39 open P0 items

## Delta since prior snapshot
- Closed: none
- Opened: none
- Status-changed: none

> Bootstrap run — no prior snapshot existed. All 39 items treated as current state.

## Items
| ID | Domain | Status | Description |
|----|--------|--------|-------------|
| IRF-APP-087 | APP | OPEN | 39 outreach messages prepared but 0 sent — pipeline warm-path unactivated. Human action required. |
| IRF-CRP-018 | CRP | OPEN | 3 modified-modified (`MM`) JSON config files: `~/.claude.json`, `~/.claude/settings.json`, `~/Library/Application Support/Claude/claude_desktop_config.json`. Source and runtime both modified; drift undecidable mechanically. |
| IRF-III-026 | III | OPEN | VACUUM: public-record-data-scrapper has no payment flow. 526 tests, deployed, zero revenue. Stripe integration + pricing page + sign-up flow needed. |
| IRF-III-027 | III | OPEN | VACUUM: content-engine--asset-amplifier (Cronus) has no payment flow. CF Pages + Workers + Neon PostgreSQL, 7 AI providers, zero marginal cost on Ollama. Stripe + pricing needed. |
| IRF-III-035 | III | OPEN | VACUUM: sovereign-systems hub `quizFormUrl` is empty. `src/data/hub.config.ts:268` — Maddie intended GHL form URL. GH#58. |
| IRF-III-047 | III | OPEN | Styx revenue gap — premortem completed. 20 failure modes. Revised plan: Week 1 cold messages → Week 4 invoice. GH#598. |
| IRF-INST-001 | INST | OPEN | Apply to NLnet NGI0 Commons Fund — EUR 37,080. Deadline June 1, 2026. Draft complete, stats updated. Human review pass + form submission remaining. |
| IRF-INST-015 | INST | OPEN | Human review pass on NLnet draft — read aloud, verify claims, submit at nlnet.nl/propose/. Draft at aerarium--res-publica/applications/nlnet-ngi0-commons-2026/draft.md. |
| IRF-INST-016 | INST | OPEN | Register ORCID — 5 minutes at orcid.org/register. Required for academic funders (Sloan, NSF). |
| IRF-OPS-014 | OPS | OPEN | Overreach Incident remediation — unauthorized 17-commit push to hokage-chess origin/main. Decision needed: accept or rollback via --force-with-lease. |
| IRF-OPS-021 | OPS | OPEN | README.md merge-conflict markers on main — `meta-organvm/organvm-corpvs-testamentvm/README.md` lines 14–23 and 312–318. Mechanical resolution: keep one copy, drop markers. |
| IRF-OPS-028 | OPS | OPEN | Word-count metric generator regression — `total_words_short` reports `~6K+` vs correct `~404K+`/`~739K+`/`~766K+`. Cascading into 87+ files. Generator fix needed before any metric-dependent commits. |
| IRF-OPS-061 | OPS | OPEN | `organvm atoms pipeline --write` cadence slipped — atom registry 11 days stale at 2026-05-21 audit. Unifier surface blind to recent session content. |
| IRF-OPS-069 | OPS | OPEN | `domus-memory-sync` scope filter silently drops `.mmd` (Mermaid) files — only `.md` accepted. Causes Rule #2 violations for plan-class non-markdown artifacts. |
| IRF-PRT-027 | PRT | OPEN | hokagechess.com domain registration (Cloudflare Registrar). Verified available 2026-04-25. Register before squatters move. ~$15/yr. |
| IRF-PRT-028 | PRT | OPEN | hokage-chess landing page deploy to Vercel. Next.js 16 build ready. Depends on IRF-PRT-027 (domain) and IRF-PRT-030 (Kit API key). |
| IRF-PRT-060 | PRT | OPEN | Kit API key (PRT-030) gates Hokage L2 deploy. 60-second user action. Silent since Apr 25. |
| IRF-PRT-061 | PRT | OPEN | hokagechess.com domain registration — verified AVAILABLE 2026-04-25. Time-decay squatter risk. ~$15/yr via Cloudflare or Namecheap. |
| IRF-RES-003 | RES | OPEN | Define "readiness" construct independently of its operationalization — expert panel required. GH#343 (INQ-2026-013, Wave 3). |
| IRF-RES-004 | RES | OPEN | Conduct factor analysis on the omega scorecard — EFA on all indicators across repo population. GH#340 (INQ-2026-013, Wave 1). |
| IRF-RES-006 | RES | OPEN | Build controlled vocabulary registry for domain terms — machine-readable mapping, CI validation. GH#339 (INQ-2026-013, Wave 1). |
| IRF-RES-007 | RES | OPEN | Make incompleteness visible in all governance verdicts — explicit scope statement per verdict. GH#344 (INQ-2026-013, Wave 3). |
| IRF-RES-008 | RES | OPEN | Formalize IRA panel protocol — Tarskian escape; external rater recruitment required. GH#345 (INQ-2026-013, Wave 4). |
| IRF-RES-009 | RES | OPEN | Implement seed.yaml semantic accuracy tracking — registry of properties not covered by validation. GH#346 (INQ-2026-013, Wave 4). |
| IRF-RES-010 | RES | OPEN | Separate self-maintenance from self-improvement in governance — two distinct operational modes. GH#348 (INQ-2026-013, Wave 5). |
| IRF-RES-011 | RES | OPEN | Establish hybrid topology principle as architectural law — codify inter/intra-organ flow. GH#341 (INQ-2026-013, Wave 2). |
| IRF-RES-012 | RES | OPEN | Design governance artifacts as boundary objects — redesign seed.yaml, CLAUDE.md, governance-rules.json. GH#349 (INQ-2026-013, Wave 5). |
| IRF-RES-013 | RES | OPEN | Implement temporal staging for governance validation — validate previous state using current state. GH#342 (INQ-2026-013, Wave 2). |
| IRF-RES-014 | RES | OPEN | Implement context-specific governance norms — differentiate thresholds by organ/language/type. GH#347 (INQ-2026-013, Wave 4; conditional on RES-004). |
| IRF-SEC-002 | SEC | OPEN | OpenAI API key exposed in public Docker image `cetaceang/openai-king` (507 pulls, live since Aug 2025). Rotate at platform.openai.com, audit logs, report to Docker Hub. |
| IRF-SEC-005 | SEC | OPEN | Gmail app password `gmail-app-pw-033526` not revoked. 27+ days since creation. Revoke at myaccount.google.com/apppasswords. |
| IRF-SYS-009 | SYS | OPEN | Gmail notification hygiene — Gmail filter + GitHub notification settings. HUMAN ACTION NEEDED. ~2 min at github.com/settings/notifications + Gmail. |
| IRF-SYS-011 | SYS | OPEN | GoDaddy domain `met4vers.io` EXPIRED — grace period, cancellation notice 2026-04-15. Renew or let expire decision required. |
| IRF-SYS-087 | SYS | OPEN | UMFAS birth — compress corpus into the space (766K words, 160 docs, 269 plans). GH#310. |
| IRF-SYS-137 | SYS | OPEN | Gemini Takeout export still pending — HUMAN ACTION NEEDED. Check takeout.google.com, download, place in my-knowledge-base/intake/canonical/sources/. |
| IRF-SYS-156 | SYS | OPEN | GitHub notification backlog — 4,115 total / 1,448 unread / 12 explicit-attention items at risk. Triage ladder: bulk-mark CI noise, address 12 humans-waiting. |
| IRF-SYS-201 | SYS | OPEN | Conductor MCP operationally cold — fleet routing table empty. 4× dispatch calls returned null. 5 agent binaries installed but zero registered. GH routing manual. |
| IRF-TAX-VAC-001 | TAX-VAC | OPEN | Execute cold-reading Stranger Test on personalized-storefront-render SKILL.md — verification gate to graduate from self-attested to verified. |
| IRF-THE-VAC-004 | THE-VAC | OPEN | Implement corpus persona-extract in conversation-corpus-engine — extract vocabulary/yearnings from session JSONLs. Highest compounding move. |
