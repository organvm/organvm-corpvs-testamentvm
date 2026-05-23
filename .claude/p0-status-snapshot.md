# IRF P0 surface — snapshot

**Last check:** 2026-05-23T11:13:00Z
**Count:** 42 open P0 items

## Delta since prior snapshot
- Closed: none
- Opened: all 42 (bootstrap — no prior snapshot)
- Status-changed: none

## Per-domain rollup
| Domain | Count |
|--------|-------|
| RES (Research Programme) | 11 |
| SYS (Systems/Infrastructure) | 6 |
| OPS (Operations) | 5 |
| SEC (Security) | 4 |
| III (ORGAN-III Commerce) | 4 |
| PRT (Projects/Portfolio) | 4 |
| INST (Institutional/Grants) | 3 |
| THE (Theory) | 1 |
| TAX (Taxis/Orchestration) | 1 |
| VAC (Vacuum) | 1 |
| APP (Applications/Outreach) | 1 |
| CRP (Corpus/Personal) | 1 |
| **Total** | **42** |

## Items
| ID | Domain | Status | Description |
|----|--------|--------|-------------|
| IRF-APP-087 | APP | OPEN (ADVANCED) | 39 outreach messages prepared but 0 sent — pipeline warm-path unactivated |
| IRF-CRP-018 | CRP | OPEN | 3 modified-modified (MM) JSON config files: ~/.claude.json, ~/.claude/settings.json, ~/Library/Application Support/Claude/claude_desktop_config.json — drift undecidable mechanically |
| IRF-III-026 | III | OPEN | VACUUM: public-record-data-scrapper has no payment flow (526 tests, deployed, zero revenue) |
| IRF-III-027 | III | OPEN | VACUUM: content-engine--asset-amplifier (Cronus) has no payment flow (CF Pages + Workers, zero marginal cost on Ollama) |
| IRF-III-035 | III | OPEN | VACUUM: sovereign-systems hub quizFormUrl is empty (src/data/hub.config.ts:268, GH#58) |
| IRF-III-047 | III | OPEN | Styx revenue gap — premortem completed (20 failure modes), revised plan written (GH#598) |
| IRF-INST-001 | INST | OPEN (ADVANCED) | Apply to NLnet NGI0 Commons Fund — EUR 37,080 for Cvrsvs Honorvm; human review + form submission by June 1, 2026 |
| IRF-INST-015 | INST | OPEN | Human review pass on NLnet draft — read aloud, verify claims, submit web form (nlnet.nl/propose/) |
| IRF-INST-016 | INST | OPEN | Register ORCID — 5 minutes at orcid.org/register; required for academic funders |
| IRF-OPS-014 | OPS | OPEN | Overreach Incident remediation — Stream D 17-commit push to hokage-chess origin/main without acolyte authorization; decision: accept or rollback |
| IRF-OPS-021 | OPS | OPEN | README.md merge-conflict markers on main — meta-organvm/organvm-corpvs-testamentvm/README.md lines 14–23 and 312–318 |
| IRF-OPS-028 | OPS | OPEN | Word-count metric generator regression cascading into 87+ files across 3 repos (total_words_short reported ~6K+ vs prior ~766K+) |
| IRF-OPS-061 | OPS | OPEN | organvm atoms pipeline cadence slipped — prompt-atoms.json 11 days stale as of 2026-05-21 audit |
| IRF-OPS-069 | OPS | OPEN | domus-memory-sync line 81+100 scope filter drops *.mmd files — fix shipped in session but IRF row not formally closed |
| IRF-PRT-027 | PRT | OPEN | hokagechess.com domain registration (Cloudflare Registrar, verified available 2026-04-25) |
| IRF-PRT-028 | PRT | OPEN | hokage-chess landing page deploy to Vercel (Next.js 16 build ready, depends on IRF-PRT-027) |
| IRF-PRT-060 | PRT | OPEN | Kit API key (PRT-030) gates Hokage L2 deploy — 60s user action; silent since Apr 25 |
| IRF-PRT-061 | PRT | OPEN | hokagechess.com domain registration — verified AVAILABLE 2026-04-25, time-decay risk |
| IRF-RES-003 | RES | OPEN | Define "readiness" construct independently of its operationalization — expert panel (GH#343) |
| IRF-RES-004 | RES | OPEN | Conduct factor analysis on omega scorecard — EFA on all indicators (GH#340) |
| IRF-RES-006 | RES | OPEN | Build controlled vocabulary registry for domain terms — machine-readable term→synonym mapping (GH#339) |
| IRF-RES-007 | RES | OPEN | Make incompleteness visible in all governance verdicts — explicit scope statement per verdict (GH#344) |
| IRF-RES-008 | RES | OPEN | Formalize IRA panel protocol — Tarskian escape; external rater recruitment required (GH#345) |
| IRF-RES-009 | RES | OPEN | Implement seed.yaml semantic accuracy tracking — registry of properties not covered by validation (GH#346) |
| IRF-RES-010 | RES | OPEN | Separate self-maintenance from self-improvement in governance — two distinct operational modes (GH#348) |
| IRF-RES-011 | RES | OPEN | Establish hybrid topology principle as architectural law — inter-organ hierarchical / intra-organ rhizomatic (GH#341) |
| IRF-RES-012 | RES | OPEN | Design governance artifacts as boundary objects — seed.yaml, CLAUDE.md, governance-rules.json (GH#349) |
| IRF-RES-013 | RES | OPEN | Implement temporal staging for governance validation — Goodhart-Campbell necessity (GH#342) |
| IRF-RES-014 | RES | OPEN | Implement context-specific governance norms — differentiate thresholds by organ/language/project type (GH#347) |
| IRF-SEC-002 | SEC | OPEN | OpenAI API key exposed in public Docker image cetaceang/openai-king (92MB, 507 pulls) — rotate at platform.openai.com |
| IRF-SEC-005 | SEC | OPEN | Gmail app password not revoked (label gmail-app-pw-033526, created 2026-03-25, 27+ days unrevoked) |
| IRF-SEC-011 | SEC | OPEN (gated: human rotation) | VACUUM-SEALED: pre-existing credential leak in pushed history of public repo; sealed memo at ~/.claude/projects/.../sealed_pat_leak_2026-05-10.md |
| IRF-SEC-012 | SEC | OPEN (gated: precondition for Phase B) | Token rotation gate for repo-consolidation Phase B — token in use holds admin:enterprise, 15 days unactioned |
| IRF-SYS-009 | SYS | OPEN | Gmail notification hygiene — filter designed S36, HUMAN ACTION NEEDED: create Gmail filter + GitHub notification settings |
| IRF-SYS-011 | SYS | OPEN | GoDaddy domain met4vers.io EXPIRED — grace period; decision: renew or let expire |
| IRF-SYS-087 | SYS | OPEN | UMFAS birth — compress 766K words corpus into atomized space (GH#310) |
| IRF-SYS-137 | SYS | OPEN | Gemini Takeout export still pending — check takeout.google.com, download, place in my-knowledge-base/intake/ |
| IRF-SYS-156 | SYS | OPEN | GitHub notification backlog — 4,115 total / 1,448 unread / 12 explicit-attention items at risk |
| IRF-SYS-201 | SYS | OPEN | Conductor MCP operationally cold — fleet routing table empty despite Dispatch Protocol mandate; 4× live reproduction |
| IRF-TAX-VAC-001 | TAX | OPEN | Execute cold-reading Stranger Test on personalized-storefront-render SKILL.md |
| IRF-THE-VAC-004 | THE | OPEN | Implement corpus persona-extract in conversation-corpus-engine (vocabulary/yearnings from session JSONLs) |
| IRF-VAC-001a | VAC | PARTIAL | Create tracking issue for SGO research programme on corpvs-testamentvm (umbrella issue still needed) |
