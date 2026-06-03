# IRF P0 surface — snapshot

**Last check:** 2026-06-03T11:18:25Z
**Count:** 40 open P0 items

## Delta since prior snapshot
- Closed: IRF-VAC-001 (split into IRF-VAC-001a [P0] + IRF-VAC-001b [P1]; the parent ID no longer appears in the table)
- Opened: IRF-VAC-001a (P0 successor to IRF-VAC-001 — same SGO tracking issue task, now with explicit sub-ID)
- Status-changed: none

## Per-domain rollup

| Domain | Open P0 count |
|--------|--------------|
| Research | 11 |
| Governance & Standards | 6 |
| Operations | 5 |
| ORGAN-III | 4 |
| Personal | 4 |
| Institutional | 3 |
| Security | 2 |
| Applications | 1 |
| Corpus | 1 |
| ORGAN-IV | 1 |
| ORGAN-I | 1 |
| Vacuum / GitHub Issue Trail | 1 |

## Items

| ID | Domain | Status | Description |
|----|--------|--------|-------------|
| IRF-APP-087 | Applications | OPEN | 39 outreach messages prepared but 0 sent — pipeline warm-path unactivated. ADVANCED (S-every-frame-2026-04-23): Triage complete — 9 target dead (rejec... |
| IRF-CRP-018 | Corpus | OPEN | 3 modified-modified (`MM`) JSON config files: `~/.claude.json`, `~/.claude/settings.json`, `~/Library/Application Support/Claude/claude_desktop_config`... |
| IRF-III-026 | ORGAN-III | OPEN | VACUUM: public-record-data-scrapper has no payment flow. 526 tests, deployed on Netlify+Render, UCC-MCA lead generation. 17 deployed URLs, zero revenu... |
| IRF-III-027 | ORGAN-III | OPEN | VACUUM: content-engine--asset-amplifier (Cronus) has no payment flow. CF Pages + Cloudflare Workers + Neon PostgreSQL, 7 AI providers, zero marginal c... |
| IRF-III-035 | ORGAN-III | OPEN | VACUUM: sovereign-systems hub `quizFormUrl` is empty. `src/data/hub.config.ts:268` has `quizFormUrl: ''`. `QuizEmbed.astro` falls back to the local `/... |
| IRF-III-047 | ORGAN-III | OPEN | Styx revenue gap — premortem completed. 20 failure modes identified on "extract sellable artifact + get paid in 30 days" plan. Hidden assumption: inte... |
| IRF-INST-001 | Institutional | OPEN | Apply to NLnet NGI0 Commons Fund — EUR 37,080 for Cvrsvs Honorvm governance engine extraction. Web form at nlnet.nl/propose/. DRAFT COMPLETE (S38). Al... |
| IRF-INST-015 | Institutional | OPEN | Human review pass on NLnet draft — Read aloud, verify all claims, check scoring criteria alignment. Then submit web form at nlnet.nl/propose/ selectin... |
| IRF-INST-016 | Institutional | OPEN | Register ORCID — Persistent researcher identifier. Takes 5 minutes at orcid.org/register. Required for academic funders (Sloan, NSF). Referenced in "B... |
| IRF-OPS-014 | Operations | OPEN | Overreach Incident remediation — Stream D 17-commit push to hokage-chess origin/main without acolyte authorization. Acolyte deferred push decision to ... |
| IRF-OPS-021 | Operations | OPEN | README.md merge-conflict markers on main — `meta-organvm/organvm-corpvs-testamentvm/README.md`. Lines 14–23 and 312–318 contain unresolved diff3-style... |
| IRF-OPS-028 | Operations | OPEN | Word-count metric generator regression cascading into 87+ files across 3 repos. `total_words_short` metric reported as `~6K+` where previously `~404K+... |
| IRF-OPS-061 | Operations | OPEN | `organvm atoms pipeline --write` cadence has slipped — atom registry at `~/Code/organvm/organvm-corpvs-testamentvm/data/prompt-registry/prompt-atoms.j... |
| IRF-OPS-069 | Operations | OPEN | `domus-memory-sync` line 81 + line 100 scope filter accepts ONLY `*.md` files in `~/.claude/plans/`, silently dropping `*.mmd` (Mermaid sources) and ... |
| IRF-PRT-027 | Personal | OPEN | hokagechess.com domain registration (Cloudflare Registrar). Verified available 2026-04-25 via Verisign. Register through Cloudflare Registrar (at-cost... |
| IRF-PRT-028 | Personal | OPEN | hokage-chess landing page deploy to Vercel. Repo `4444J99/hokage-chess` is private; Next.js 16 build ready. Deploy to Vercel: connect GitHub repo, con... |
| IRF-PRT-060 | Personal | OPEN | Kit API key (PRT-030) gates Hokage L2 deploy. 60s user action; without it, email funnel L2 cannot ship. Escalate if delayed >7d (currently silent sinc... |
| IRF-PRT-061 | Personal | OPEN | hokagechess.com domain registration — verified AVAILABLE 2026-04-25. Time-decay risk: domain may be taken by squatter. No owner assigned. Register tod... |
| IRF-RES-003 | Research | OPEN | Define "readiness" construct independently of its operationalization — convene expert panel to define full domain of "repository readiness" independen... |
| IRF-RES-004 | Research | OPEN | Conduct factor analysis on the omega scorecard — perform EFA on all indicators across repo population; determine single vs. multiple latent factors. G... |
| IRF-RES-006 | Research | OPEN | Build a controlled vocabulary registry for domain terms — machine-readable mapping of canonical terms to synonyms; validate new names against vocabula... |
| IRF-RES-007 | Research | OPEN | Make incompleteness visible in all governance verdicts — every automated verdict must include explicit scope statement listing unverified semantic pro... |
| IRF-RES-008 | Research | OPEN | Formalize the IRA panel protocol — strengthen IRA panel as Tarskian escape; provide explicit guidance on semantic properties that automated checks can... |
| IRF-RES-009 | Research | OPEN | Implement seed.yaml semantic accuracy tracking — maintain machine-readable registry of properties not covered by seed.yaml validation; track gap betwe... |
| IRF-RES-010 | Research | OPEN | Separate self-maintenance from self-improvement in governance — build two distinct operational modes with architectural enforcement of the boundary. G... |
| IRF-RES-011 | Research | OPEN | Establish the hybrid topology principle as architectural law — codify inter-organ hierarchical flow and intra-organ rhizomatic connectivity as compres... |
| IRF-RES-012 | Research | OPEN | Design governance artifacts as boundary objects — redesign seed.yaml, CLAUDE.md, and governance-rules.json as boundary objects accommodating human, ma... |
| IRF-RES-013 | Research | OPEN | Implement temporal staging for governance validation — ensure governance always validates previous state using current state, never current state usin... |
| IRF-RES-014 | Research | OPEN | Implement context-specific governance norms — differentiate thresholds by organ, programming language, and project type; use expert-determined context... |
| IRF-SEC-002 | Security | OPEN | OpenAI API key exposed in public Docker image. Key found in `cetaceang/openai-king` (92MB, 507 pulls, live since Aug 2025). Responsible disclosure rec... |
| IRF-SEC-005 | Security | OPEN | Gmail app password not revoked in Google Account. Label `gmail-app-pw-033526` (created 2026-03-25) grants IMAP/SMTP to `padavano.anthony@gmail.com`. N... |
| IRF-SYS-009 | Governance & Standards | OPEN | Gmail notification hygiene — filter designed in S36: `from:notifications@github.com ("dependabot[bot]" OR "github-actions[bot]")` → Skip Inbox, Apply ... |
| IRF-SYS-011 | Governance & Standards | OPEN | GoDaddy domain `met4vers.io` EXPIRED — cancellation notice received. Domain expired Mar 29 (originally flagged as "parked" Mar 21). Grace period activ... |
| IRF-SYS-087 | Governance & Standards | OPEN | UMFAS birth — compress the corpus into the space. REFRAMED 2026-04-06: Birth is NOT empty dir + SEED.md. Birth is COMPRESSION: inventory all origin do... |
| IRF-SYS-137 | Governance & Standards | OPEN | Gemini Takeout export still pending — HUMAN ACTION NEEDED. Google Takeout requested for Gemini conversation history but export not yet delivered/downl... |
| IRF-SYS-156 | Governance & Standards | OPEN | GitHub notification backlog — 4,115 total / 1,448 unread / 12 explicit-attention items at high risk of being lost in CI noise. Quantified S-2026-04-25... |
| IRF-SYS-201 | Governance & Standards | OPEN | Conductor MCP operationally cold despite Dispatch Protocol mandate — `~/.claude/CLAUDE.md` mandates calling `conductor_fleet_dispatch` before BUILD-ph... |
| IRF-TAX-VAC-001 | ORGAN-IV | OPEN | Execute cold-reading Stranger Test on personalized-storefront-render SKILL.md. Verification gate to graduate substrate from "self-attested" to "verifi... |
| IRF-THE-VAC-004 | ORGAN-I | OPEN | Implement corpus persona-extract in conversation-corpus-engine. Highest compounding move: extract vocabulary/yearnings from session JSONLs. |
| IRF-VAC-001a | Vacuum / GitHub Issue Trail | OPEN | Create tracking issue for SGO research programme on corpvs-testamentvm (13 papers, 74 tasks, 3 arXiv packages, 4 governance declarations). PARTIAL — 3... |
