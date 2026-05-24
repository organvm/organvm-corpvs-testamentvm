# IRF P0 surface — snapshot

**Last check:** 2026-05-24T11:13:00Z
**Count:** 41 open P0 items

> **Parser note:** The IRF internal statistics table reports "P0 | 14" (stale, CLI-parser bug per IRF-OPS-017 — parser misses bolded `**P0**` cells). Actual count from raw grep: 41. This discrepancy is itself a P0-adjacent signal.

## Delta since prior snapshot
- Closed: none (bootstrap — no prior snapshot)
- Opened: all 41 (first run)
- Status-changed: none (bootstrap)

## Items
| ID | Domain | Status | Description |
|----|--------|--------|-------------|
| IRF-APP-087 | APP | OPEN | 39 outreach messages prepared but 0 sent — pipeline warm-path unactivated |
| IRF-CRP-018 | CRP | OPEN | 3 modified-modified (MM) JSON config files: ~/.claude.json, ~/.claude/settings.json, claude_desktop_config.json — source/runtime drift undecidable |
| IRF-III-026 | III | OPEN | VACUUM: public-record-data-scrapper has no payment flow (526 tests, deployed, zero revenue) |
| IRF-III-027 | III | OPEN | VACUUM: content-engine--asset-amplifier (Cronus) has no payment flow |
| IRF-III-035 | III | OPEN | VACUUM: sovereign-systems hub `quizFormUrl` is empty — awaiting Maddie response |
| IRF-III-047 | III | OPEN | Styx revenue gap — premortem completed, 20 failure modes identified, plan ready, execution pending |
| IRF-INST-015 | INST | OPEN | Human review pass on NLnet draft before submission (deadline: April 1, 2026 12:00 CEST) |
| IRF-INST-016 | INST | OPEN | Register ORCID — persistent researcher identifier, 5-min action |
| IRF-OPS-014 | OPS | OPEN | Overreach Incident remediation — Stream D 17-commit push to hokage-chess without authorization |
| IRF-OPS-021 | OPS | OPEN | README.md merge-conflict markers live on main (lines 14–23, 312–318) |
| IRF-OPS-028 | OPS | OPEN | Word-count metric generator regression — total_words cascading ~6K+ (was ~739K+) across 87+ files |
| IRF-OPS-061 | OPS | OPEN | atom pipeline cadence slipped — prompt-atoms.json 11+ days stale (last modified 2026-05-10) |
| IRF-OPS-069 | OPS | OPEN | domus-memory-sync *.mmd scope filter missing — row self-reports fix shipped but not officially DONE |
| IRF-PRT-027 | PRT | OPEN | hokagechess.com domain registration (Cloudflare Registrar, ~$15/yr) |
| IRF-PRT-028 | PRT | OPEN | hokage-chess landing page deploy to Vercel (blocked on IRF-PRT-027 domain) |
| IRF-PRT-060 | PRT | OPEN | Kit API key gates Hokage L2 deploy — 60s user action, silent since Apr 25 |
| IRF-PRT-061 | PRT | OPEN | hokagechess.com domain registration — verified available 2026-04-25, squatter risk (dup of IRF-PRT-027) |
| IRF-RES-003 | RES | OPEN | Define "readiness" construct independently of its operationalization — expert panel needed |
| IRF-RES-004 | RES | OPEN | Conduct factor analysis on the omega scorecard (INQ-2026-013 Wave 1) |
| IRF-RES-006 | RES | OPEN | Build controlled vocabulary registry for domain terms (INQ-2026-013 Wave 1) |
| IRF-RES-007 | RES | OPEN | Make incompleteness visible in all governance verdicts (INQ-2026-013 Wave 3) |
| IRF-RES-008 | RES | OPEN | Formalize the IRA panel protocol — Tarskian escape for semantic properties (INQ-2026-013 Wave 4) |
| IRF-RES-009 | RES | OPEN | Implement seed.yaml semantic accuracy tracking (INQ-2026-013 Wave 4) |
| IRF-RES-010 | RES | OPEN | Separate self-maintenance from self-improvement in governance — Löb-theorem escape (INQ-2026-013 Wave 5) |
| IRF-RES-011 | RES | OPEN | Establish hybrid topology principle as architectural law (INQ-2026-013 Wave 2) |
| IRF-RES-012 | RES | OPEN | Design governance artifacts as boundary objects — seed.yaml, CLAUDE.md, governance-rules.json (INQ-2026-013 Wave 5) |
| IRF-RES-013 | RES | OPEN | Implement temporal staging for governance validation — Goodhart-Campbell (INQ-2026-013 Wave 2) |
| IRF-RES-014 | RES | OPEN | Implement context-specific governance norms (INQ-2026-013 Wave 4, conditional on RES-004) |
| IRF-SEC-002 | SEC | OPEN | OpenAI API key exposed in public Docker image cetaceang/openai-king (507 pulls) — rotate + report |
| IRF-SEC-005 | SEC | OPEN | Gmail app password not revoked — 27+ days (label gmail-app-pw-033526) |
| IRF-SEC-011 | SEC | OPEN | VACUUM-SEALED: pre-existing credential leak in pushed history of public repo — gated on human rotation |
| IRF-SEC-012 | SEC | OPEN | Token rotation gate for repo-consolidation Phase B — stale token with admin:enterprise scope |
| IRF-SYS-009 | SYS | OPEN | Gmail notification hygiene — filter designed, HUMAN ACTION NEEDED to create |
| IRF-SYS-011 | SYS | OPEN | GoDaddy domain met4vers.io EXPIRED — decision needed (renew or let expire) |
| IRF-SYS-087 | SYS | OPEN | UMFAS birth — compress corpus into the space (reframed: compression, not empty dir) |
| IRF-SYS-137 | SYS | OPEN | Gemini Takeout export still pending — blocks full corpus ingestion |
| IRF-SYS-156 | SYS | OPEN | GitHub notification backlog — 4,115 total / 1,448 unread / 12 explicit-attention items |
| IRF-SYS-201 | SYS | OPEN | Conductor MCP operationally cold — fleet routing table empty despite Dispatch Protocol mandate |
| IRF-TAX-VAC-001 | TAX | OPEN | Execute cold-reading Stranger Test on personalized-storefront-render SKILL.md |
| IRF-THE-VAC-004 | THE | OPEN | Implement corpus persona-extract in conversation-corpus-engine |
| IRF-VAC-001a | VAC | PARTIAL | Create tracking issue for SGO research programme — 3 arXiv issues created, umbrella issue still needed |

## Per-Domain Rollup
| Domain | Open P0 Count |
|--------|--------------|
| APP | 1 |
| CRP | 1 |
| III | 4 |
| INST | 2 |
| OPS | 5 |
| PRT | 4 |
| RES | 11 |
| SEC | 4 |
| SYS | 6 |
| TAX | 1 |
| THE | 1 |
| VAC | 1 |
| **TOTAL** | **41** |
