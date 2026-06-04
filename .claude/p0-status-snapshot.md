# IRF P0 surface — snapshot

**Last check:** 2026-06-04T11:13:00Z
**Count:** 42 open P0 items

## Delta since prior snapshot
- Closed: IRF-VAC-001 (ID renamed/split to IRF-VAC-001a in current IRF)
- Opened: IRF-SEC-011, IRF-SEC-012, IRF-VAC-001a
- Status-changed: none

> **Parser note:** IRF-SEC-011 and IRF-SEC-012 were present in the IRF on the prior run date (2026-05-27) but were missed by the prior snapshot's parser, which did not handle the `**P0 (gated: ...)**` bold-qualified priority format. They are surfaced here for the first time; they are NOT newly filed rows. IRF-VAC-001a is the P0 continuation of the former IRF-VAC-001 (the original item was split into IRF-VAC-001a through IRF-VAC-001d; only `a` carries P0 priority).

## Per-domain rollup

| Domain | Open P0 count |
|--------|--------------|
| Research Programme (P0 Foundational) | 11 |
| Session-Discovered Items | 12 |
| Security | 4 |
| Governance & Standards | 4 |
| Operations | 3 |
| ORGAN-III (Commerce / Ergon) | 3 |
| PERSONAL / Portfolio | 2 |
| ORGAN-I (Theoria) | 1 |
| ORGAN-IV (Governance Orchestration) | 1 |
| GitHub Issue Trail (Vacuum) | 1 |

## Items

| ID | Domain | Status | Description |
|----|--------|--------|-------------|
| IRF-APP-087 | Session-Discovered | OPEN | 39 outreach messages prepared but 0 sent — pipeline warm-path unactivated |
| IRF-CRP-018 | Session-Discovered | OPEN | 3 modified-modified (`MM`) JSON config files requiring independent human judgment |
| IRF-III-026 | ORGAN-III — Ergon | OPEN | VACUUM: public-record-data-scrapper has no payment flow (526 tests, live on Netlify+Render) |
| IRF-III-027 | ORGAN-III — Ergon | OPEN | VACUUM: content-engine--asset-amplifier (Cronus) has no payment flow |
| IRF-III-035 | ORGAN-III — Ergon | OPEN | VACUUM: sovereign-systems hub `quizFormUrl` is empty (`src/data/hub.config.ts:268`) |
| IRF-III-047 | Session-Discovered | OPEN | Styx revenue gap — premortem completed, 20 failure modes identified |
| IRF-INST-001 | Session-Discovered | OPEN | Apply to NLnet NGI0 Commons Fund — EUR 37,080 for Cvrsvs Honorvm governance engine extraction |
| IRF-INST-015 | Session-Discovered | OPEN | Human review pass on NLnet draft — read aloud, verify claims, check scoring criteria |
| IRF-INST-016 | Session-Discovered | OPEN | Register ORCID — persistent researcher identifier, 5 min at orcid.org/register |
| IRF-OPS-014 | Operations | OPEN | Overreach Incident remediation — 17-commit push to hokage-chess origin/main without authorization |
| IRF-OPS-021 | Operations | OPEN | README.md merge-conflict markers on main in `meta-organvm/organvm-corpvs-testamentvm/README.md` |
| IRF-OPS-028 | Operations | OPEN | Word-count metric generator regression cascading into 87+ files across 3 repos |
| IRF-OPS-061 | Session-Discovered | OPEN | `organvm atoms pipeline --write` cadence slipped — atom registry stale |
| IRF-OPS-069 | Session-Discovered | OPEN | `domus-memory-sync` scope filter silently drops non-`.md` files |
| IRF-PRT-027 | PERSONAL — Portfolio | OPEN | hokagechess.com domain registration (Cloudflare Registrar) — verified available 2026-04-25 |
| IRF-PRT-028 | PERSONAL — Portfolio | OPEN | hokage-chess landing page deploy to Vercel (Next.js 16 build ready) |
| IRF-PRT-060 | Session-Discovered | OPEN | Kit API key gates Hokage L2 deploy — 60s user action |
| IRF-PRT-061 | Session-Discovered | OPEN | hokagechess.com domain registration — time-decay risk of squatter |
| IRF-RES-003 | P0 — Foundational | OPEN | Define "readiness" construct independently of its operationalization |
| IRF-RES-004 | P0 — Foundational | OPEN | Conduct factor analysis on the omega scorecard (EFA across repo population) |
| IRF-RES-006 | P0 — Foundational | OPEN | Build a controlled vocabulary registry for domain terms |
| IRF-RES-007 | P0 — Foundational | OPEN | Make incompleteness visible in all governance verdicts |
| IRF-RES-008 | P0 — Foundational | OPEN | Formalize the IRA panel protocol (Tarskian escape) |
| IRF-RES-009 | P0 — Foundational | OPEN | Implement seed.yaml semantic accuracy tracking |
| IRF-RES-010 | P0 — Foundational | OPEN | Separate self-maintenance from self-improvement in governance |
| IRF-RES-011 | P0 — Foundational | OPEN | Establish the hybrid topology principle as architectural law |
| IRF-RES-012 | P0 — Foundational | OPEN | Design governance artifacts as boundary objects (seed.yaml, CLAUDE.md, governance-rules.json) |
| IRF-RES-013 | P0 — Foundational | OPEN | Implement temporal staging for governance validation |
| IRF-RES-014 | P0 — Foundational | OPEN | Implement context-specific governance norms (by organ, language, project type) |
| IRF-SEC-002 | Security | OPEN | OpenAI API key exposed in public Docker image (`cetaceang/openai-king`, 507 pulls) |
| IRF-SEC-005 | Security | OPEN | Gmail app password not revoked in Google Account (label `gmail-app-pw-033526`) |
| IRF-SEC-011 | Security | OPEN | VACUUM-SEALED: pre-existing credential leak in pushed history of this public repo — rotation required before disclosure |
| IRF-SEC-012 | Security | OPEN | Token rotation gate for repo-consolidation Phase B — stale token with admin:enterprise scope |
| IRF-SYS-009 | Governance & Standards | OPEN | Gmail notification hygiene — GitHub Actions / Dependabot notification filter |
| IRF-SYS-011 | Session-Discovered | OPEN | GoDaddy domain `met4vers.io` EXPIRED — cancellation notice received |
| IRF-SYS-087 | Governance & Standards | OPEN | UMFAS birth — compress the corpus into the space (REFRAMED 2026-04-06) |
| IRF-SYS-137 | Governance & Standards | OPEN | Gemini Takeout export still pending — HUMAN ACTION NEEDED |
| IRF-SYS-156 | Governance & Standards | OPEN | GitHub notification backlog — 4,115 total / 1,448 unread / 12 explicit-attention items |
| IRF-SYS-201 | Session-Discovered | OPEN | Conductor MCP operationally cold despite Dispatch Protocol mandate |
| IRF-TAX-VAC-001 | ORGAN-IV — Governance Orchestration | OPEN | Execute cold-reading Stranger Test on personalized-storefront-render SKILL.md |
| IRF-THE-VAC-004 | ORGAN-I — Theoria | OPEN | Implement corpus persona-extract in conversation-corpus-engine |
| IRF-VAC-001a | GitHub Issue Trail (Vacuum 1) | OPEN | Create tracking issue for SGO research programme on corpvs-testamentvm (PARTIAL — 3 arXiv issues created) |
