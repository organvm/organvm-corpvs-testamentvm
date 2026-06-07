# Concordance — Governance ID Reference

**Created:** 2026-02-17
**Author:** @4444j99
**Status:** ACTIVE — Living document, updated as IDs are added or resolved
**Companions:** [`rolling-todo.md`](./rolling-todo.md) (active queue), [`operational-cadence.md`](./operational-cadence.md) (rhythm), [`there+back-again.md`](../strategy/there+back-again.md) (destination), [`sprint-catalog.md`](../strategy/sprint-catalog.md) (menu), [`e2g-ii-action-items.md`](../evaluation/e2g-ii-action-items.md) (audit trail)

---

> *Every governance document uses short IDs. This document resolves all of them in one place. When you encounter "X1" or "AP-3" or "#8" — look here.*

---

## How to Use

**In conversation:** Ask Claude "what's X1?" or "which items advance #8" — the CLAUDE.md invocation table teaches it to check here.

**In terminal:** `python3 scripts/invoke.py <ID>` resolves any ID to its definition, source, and related IDs.

```bash
python3 scripts/invoke.py X1                  # lookup single ID
python3 scripts/invoke.py X1 E3 AP-2          # lookup multiple IDs
python3 scripts/invoke.py --namespace todo     # list all TODO items
python3 scripts/invoke.py --namespace omega    # list all omega criteria
python3 scripts/invoke.py --tag INCOME         # filter by constraint tag
python3 scripts/invoke.py --search "stranger"  # full-text search across definitions
python3 scripts/invoke.py --list               # list all namespaces and counts
```

**ID pattern cheat sheet:**

| Pattern | Namespace | Example |
|---------|-----------|---------|
| `X\d` | P0 TODO items (hermetic seal breakers) | X1 |
| `E\d` | P1 TODO items (engagement) | E3 |
| `M\d-II` | P2 TODO items (quality) | M2-II |
| `S\d-II` | P3 TODO items (strategic) | S1-II |
| `G\d` | Setup guide TODO items | G2 |
| `#\d+` or bare 1–19 | Omega criteria | #8 |
| `H\d` | Horizons | H3 |
| `AP-\d` | Anti-patterns | AP-1 |
| `W\d-II`, `SP\d-II`, `BS\d-II`, `LC\d-II`, `BL\d-II`, `ET\d-II`, `LO\d-II` | E2G-II findings | W1-II |
| Two-digit `\d\d` or sprint name | Sprints | 29 / AUTOMATA |
| `IRF-XXX-NNN` | Index Rerum Faciendarum items | IRF-SYS-001 |
| `FORM-[A-Z]{3}-\d+` | Formation declarations | FORM-RES-001 |
| `INQ-YYYY-NNN` | SGO research commissions | INQ-2026-006 |
| `SGO-YYYY-RP-NNN` | SGO research papers | SGO-2026-RP-002 |
| `SGO-YYYY-SYN-NNN` | SGO synthesis papers | SGO-2026-SYN-02 |
| `SGO-YYYY-D-NNN` | SGO dissertations | SGO-2026-D-003 |
| `S-\w+` | Named session IDs (non-numeric) | S-CC-review |
| `DONE-NNN` | IRF completion entries | DONE-284 |
| `GH#NNN` | GitHub issue references (per-repo) | GH#5 (aerarium) |
| `ATM-X-NNN` | Formal atoms (system-system--system) | ATM-M-018 |
| `DOC-X-NN` | Document envelopes (system-system--system) | DOC-M-01 |
| `SOP-SS-XXX-NNN` | Standard operating procedures (system-system--system) | SOP-SS-ATM-001 |
| `ent_[A-F0-9]{5}` | Registry entities (system-system--system) | ent_534B8 |
| `rel_[A-F0-9]{5}` | Registry relationships (system-system--system) | rel_195AD |
| `evt_[A-F0-9]{5}` | Registry events (system-system--system) | evt_05C78 |
| `TRX-{trunk}[.{N}]` | Zettelkasten transcript IDs (post-flood) | TRX-CAS.2.1 |
| `TRX-C.NN` | Compiled specification IDs (post-flood) | TRX-C.07 |
| `T(X,Y)` X={S,C,P,I} Y={O,C,M,A} | Threshold topology cells (governance membrane) | T(S,O) |
| `classified_\w+` | Classified governance rules (threshold topology) | classified_logic_first_governance |
| `INT-NNN` | Contrib intent register (`4444J99/contrib` archaeology/INTENTS.md; distinct from the fossil scheme `INT-YYYY-MM-DD-NNN` below) | INT-052 |
| `DR-N[a]` | Contrib decision record (`4444J99/contrib` archaeology/ARCHAEOLOGY.md) | DR-1a |
| `AB-N` | Contrib abandoned-approaches register (`4444J99/contrib` archaeology/ARCHAEOLOGY.md) | AB-17 |
| `RD-N` | Contrib roadmap deltas (`4444J99/contrib`; distinct from a-i--skills research docs RD-001..006, see DONE-483) | RD-13 |

---

## Index Rerum Faciendarum (IRF)

Source: [`INST-INDEX-RERUM-FACIENDARUM.md`](../../INST-INDEX-RERUM-FACIENDARUM.md)

Universal work registry. 26 domain prefixes:

| Prefix | Domain | Scope |
|--------|--------|-------|
| IRF-SYS | System-wide governance & standards | Cross-organ |
| IRF-IDX | Index apparatus (companion indices) | Cross-organ |
| IRF-SKL | Skills & automation | ORGAN-IV |
| IRF-MON | Monitoring & auditing | META (vigiles) |
| IRF-CRP | Corpus | META (testamentvm) |
| IRF-SGO | Studium Generale ORGANVM | META (praxis-perpetua) |
| IRF-VIG | Vigiles Aeternae | META (vigiles) |
| IRF-TRV | Trivium / Dialectica | META (engine) |
| IRF-TST | Testament Protocol | META (engine) |
| IRF-OBJ | Object Lessons | ORGAN-II |
| IRF-LOG | Logos / Discourse | ORGAN-V |
| IRF-KOI | Koinonia / Community | ORGAN-VI |
| IRF-KER | Kerygma / Distribution | ORGAN-VII |
| IRF-PRT | Portfolio | PERSONAL |
| IRF-APP | Application Pipeline | PERSONAL |
| IRF-GEN | Generative Visuals | Cross-organ |
| IRF-IRA | Evaluative Authority / IRA | META + PERSONAL |
| IRF-ARC | Cross-organ architecture | Cross-organ |
| IRF-BLK | Blockchain & provenance | META (testament) |
| IRF-DOC | Documentation gaps | Cross-organ |
| IRF-VER | Verification debts | Cross-organ |
| IRF-RES | Research programme (71-task manifest) | META (praxis-perpetua) |
| IRF-CCE | Conversation Corpus Engine | ORGAN-I |
| IRF-HRM | Hermeneus intelligence layer | META (stakeholder-portal) |
| IRF-DOM | Domus Infrastructure | PERSONAL (domus) |
| IRF-OSS | Open-Source Contributions | Cross-organ |
| IRF-DWV | DWV Integration (rebrand) | Cross-organ |
| IRF-DSF | Dispersio Formalis (SPEC-022) | META (post-flood) |
| IRF-GRC | Gravitas Culturalis (SPEC-021) | META (post-flood) |
| IRF-LIQ | Liquid Constitutional Order (SPEC-019) | META (post-flood) |
| IRF-PSP | Petasum Super Petasum (governance orch.) | ORGAN-IV |
| IRF-VOX | Voice Governance | ORGAN-IV |
| IRF-CND | Conductor OS | ORGAN-IV |
| IRF-ATN | Agentic Titan (swarm architecture) | ORGAN-IV |
| IRF-PSG | Process Sequence Governance (SPEC-023) | META (post-flood) |
| IRF-AOR | A-Organism | META (a-organvm) |
| IRF-SEC | Security (credentials, incidents, billing) | META (custodia-securitatis) |
| IRF-OPS | Operations | Cross-organ |
| IRF-III | ORGAN-III (Ergon/Commerce) | ORGAN-III |

#### IRF-APP Items (Pipeline S33, 2026-03-23)

| ID | Description | Priority | Refs |
|----|-------------|----------|------|
| IRF-APP-001 | Collect 3+ months v2 outcome data for D-001 | P2 | INQ-2026-001 |
| IRF-APP-002 | Register content-engine--asset-amplifier in registry + GitHub | P1 | GH#272 |
| IRF-APP-003 | Scrapper Phase 1 for Tony Carbone (coverage dashboard + health monitoring) | P1 | GH#230 |
| IRF-APP-004 | Content engine MVP build (partnership with Lefler) | P2 | GH#274 |
| IRF-APP-005 | Follow-up tracking (Tony + Scott responses) | P1 | GH#275 |
| ~~IRF-APP-006~~ | ~~GitHub issues for APP-002/003/004/005~~ — DONE (issues done, repo creation pending) | ~~P1~~ | GH#272-275 |
| IRF-APP-007 | ~~Omega scorecard consulting pivot evidence~~ — DONE | ~~P2~~ | Omega #5,7,9,13,14 |
| ~~IRF-APP-008~~ | ~~Inquiry log D-001 evidence~~ — DONE-184 | ~~P1~~ | INQ-2026-001 |
| IRF-APP-009 | Testament milestone (part a DONE, parts b/c pending IRF-APP-002) | P2 | MILESTONE-2026-002 |
| ~~IRF-APP-010~~ | ~~Index Locorum update~~ — DONE-185 | ~~P1~~ | INST-INDEX-LOCORUM |
| IRF-APP-011 | Omega #19 network density from content-engine repo | P2 | Omega #19 |

#### IRF-SYS Items (Session Close-Out Audit)

| ID | Description | Priority | Refs |
|----|-------------|----------|------|
| IRF-SYS-044 | Fix hanging `organvm session review` / `organvm session plans` commands in large repos | P1 | GH#70 |
| IRF-SYS-045 | Fix `organvm irf stats` undercounting tail-appended items | P1 | GH#71 |
| IRF-SYS-195 | Standard 16 (Data Mesh + Medallion Architecture) codified — adoption work tracking row | P2 | `docs/standards/16-data-mesh-medallion-architecture.md` |
| IRF-SYS-196 | Claude Code `CronCreate(durable: true)` silently ignored — no `~/.claude/scheduled_tasks.json` written, `CronList` reports session-only regardless of flag | P3 | `~/.claude/plans/2026-05-22-session-tldr-recall-system.md` |
| IRF-SYS-197 | BSD-crontab Rule-#9 adjudication captured — wrapper pre-staged at `~/.local/bin/session-tldr-cron-wrapper`, not installed | P3 | Decision-pending |

*191 additional IRF-SYS items (SYS-046 through SYS-194 + SYS-198+) in full IRF — this concordance section is curated, not exhaustive (per known undercounting in IRF-SYS-045 and curation precedent in IRF-DOM footer below).*

#### IRF-OPS Items (Operations)

| ID | Description | Priority | Refs |
|----|-------------|----------|------|
| IRF-OPS-093 | Session export persistence vacuum — `organvm session export` can write durable-looking closeout markdown into non-git workspace paths | P2 | GH#429 |

#### IRF-DOM Items (Domus Infrastructure, S29+)

| ID | Description | Priority | Refs |
|----|-------------|----------|------|
| ~~IRF-DOM-001~~ | ~~Create seed.yaml~~ — DONE | ~~P1~~ | S29 |
| ~~IRF-DOM-002~~ | ~~Add domus to repo-registry.json (PERSONAL section)~~ — DONE (S-domus-vacuum) | ~~P0~~ | S29, #19 |
| ~~IRF-DOM-003~~ | ~~Emit testament events for domus~~ — DONE (S-domus-vacuum) | ~~P1~~ | DOM-002 |
| ~~IRF-DOM-004~~ | ~~Register IRF-DOM in concordance + omega xrefs~~ — DONE (S-domus-vacuum) | ~~P2~~ | S29 |
| IRF-DOM-005 | Create GitHub issues for domus testing gaps (5 areas) | P1 | S29, S32 |
| IRF-DOM-006 | Add domus to omega evidence map (#1, #16, #17, #19) | P1 | S29, DOM-002 |
| IRF-DOM-010 | Create Brewfile for domus — bootstrap missing tool tracking | P1 | S35, GH#4 |
| IRF-DOM-016 | Omega #17 evidence gap — cloud storage incident unreported | P1 | S35, DOM-006 |
| IRF-DOM-021 | CLAUDE.md missing project board URL | P1 | S-domus-board |
| IRF-DOM-022 | OpenClaw security: 3B model + web tools, no sandbox | P1 | S43, GH#52 |
| IRF-DOM-023 | lefthook global ghost — blocks git push system-wide | P1 | S43, GH#51 |
| IRF-DOM-047 | Global pre-commit hook `@: unbound variable` zero-arg failure | P1 | S-2026-04-29, GH#29 |
| ~~IRF-DOM-027~~ | ~~Remove dead serena fork MCP~~ — DONE (S-mcp-remediation) | ~~P1~~ | Completed |
| ~~IRF-DOM-029~~ | ~~Voice-scorer MCP non-functional~~ — DONE (S-domus-vacuum) | ~~P1~~ | Completed |
| ~~IRF-DOM-030~~ | ~~Conductor MCP untested~~ — DONE (S-domus-vacuum) | ~~P1~~ | Completed |
| ~~IRF-DOM-029 (renumbered)~~ | ~~Persist Claude session transcripts remotely~~ — DONE (DONE-373, S-domus-2026-04-15). `organvm session archive` command built + LaunchAgent every 30 min. | ~~P1~~ | Completed |
| IRF-DOM-031 | `~/.claude/settings.json` not tracked by chezmoi — persistence vacuum. Partially fixed: `private_dot_claude/settings.json.tmpl` restored with `{{ .chezmoi.homeDir }}` vars + PreToolUse if-guards + plugin cleanup. GH#26. | P1 | S-2026-04-16, GH#26 |

*18 additional P2/P3 items (DOM-007 through DOM-028) in full IRF.*

**Omega cross-references (domus → criteria):**

| Criterion | Domus role |
|-----------|-----------|
| #1 (30-day soak) | autoCommit/autoPush provides continuous deployment evidence |
| #16 (bus factor) | chezmoi bootstrap recreates operator environment on any machine; `settings.json.tmpl` now tracked (S-2026-04-16, was local-only) |
| #17 (autonomous ops) | 50ms shell startup, self-heal daemon, zero-error boot (S32 rewrite); silent SSH clone failure of plugin marketplace exposed infra resilience gap (S-2026-04-16, IRF-DOM-031) |
| #19 (network density) | 4 produces edges (env-config, agent-infra, secrets, claude-code-config) consumed by ALL organs |

#### Testament Milestones

| ID | Description | Date | Refs |
|----|-------------|------|------|
| MILESTONE-2026-001 | SGO Research Programme inaugural milestone | 2026-03-23 | INQ-2026-004 |
| MILESTONE-2026-002 | First inbound commercial engagement via GitHub public process | 2026-03-23 | IRF-APP-009, Omega #13,#9 |

#### Named Entities (Pipeline S33)

| Name | Type | Context |
|------|------|---------|
| `content-engine--asset-amplifier` | Repo (ORGAN-III, SKELETON) | AI content repurposing platform, Padavano+Lefler partnership |
| | INQ-2026-009 | SGO Research Commission | Autopoietic Identity Refinement: Multi-Modal Brand Metabolism and Inquiry-Driven Alignment Scoring |
| Tony Carbone | External contact | Managing Partner, Alternative Funding Group, MCA client |
| Scott Lefler | External contact | Owner, Lefler.Design, build-sell partnership |
| Alexis C. | External contact | Managing Director/Owner, Tony's business partner |
| Alternative Funding Group | Organization | MCA lender, altfunding.com, Ft. Lauderdale FL |
| Lefler Design | Organization | Premium motion design studio, lefler.design |

#### IRF-HRM Items (S28, 2026-03-21)

| ID | Description | Priority | Refs |
|----|-------------|----------|------|
| IRF-HRM-001 | Repo rename coordination (stakeholder-portal → hermeneus) | P1 | GH#28 |
| ~~IRF-HRM-002~~ | ~~Registry entry update~~ — DONE-185 | ~~P1~~ | Completed S28 |
| ~~IRF-HRM-003~~ | ~~Concordance registration~~ — DONE-186 | ~~P1~~ | Completed S28 |
| IRF-HRM-004 | Custom domain (hermeneus.organvm.io) | P2 | — |
| ~~IRF-HRM-005~~ | ~~Testament cascade~~ — DONE-187 | ~~P1~~ | Completed S28 |
| IRF-HRM-006 | Omega #9 stranger-test Hermeneus for polish validation | P2 | Omega |
| IRF-HRM-007 | Streaming markdown rendering fix (heading concatenation) | P2 | — |
| IRF-HRM-008 | Full re-ingestion with retry logic | P2 | — |

#### IRF-CCE Items (S33/S37/S38/S39)

| ID | Description | Priority | Refs |
|----|-------------|----------|------|
| IRF-CCE-014 | Record S33 CCE testament events once testament tooling path is usable | P1 | GH#11 |
| IRF-CCE-015 | Ratify OM-MEM-001 in the omega scorecard via criterion-authoring path | P1 | GH#14 |
| ~~IRF-CCE-016~~ | ~~Claude adapter parity with ChatGPT~~ — DONE-232 | ~~P2~~ | `conversation-corpus-engine@3fa116f` |
| ~~IRF-CCE-017~~ | ~~Dedicated tests for remaining module blind spots~~ — DONE-233 | ~~P2~~ | `conversation-corpus-engine@3fa116f` |
| ~~IRF-CCE-018~~ | ~~Semantic/title-overlap triage expansion~~ — DONE-234 | ~~P2~~ | `conversation-corpus-engine@3fa116f` |
| IRF-CCE-019 | Migrate historical federated review IDs away from slug-collision ambiguity | P1 | GH#13 |
| IRF-CCE-020 | Record S37 CCE testament events for review-assist/operator expansion | P2 | GH#12 |
| ~~IRF-CCE-021~~ | ~~ChatGPT local-session adapter + Chrome fallback~~ — DONE-295 | ~~P1~~ | `conversation-corpus-engine@cf97add..8fe770b` |
| ~~IRF-CCE-022~~ | ~~ChatGPT incremental sync + state persistence~~ — DONE-296 | ~~P1~~ | `conversation-corpus-engine@8fe770b` |
| ~~IRF-CCE-023~~ | ~~Post Office project registry lifecycle~~ — DONE-297 | ~~P1~~ | `conversation-corpus-engine@3d86009` |
| ~~IRF-CCE-024~~ | ~~Claude delta-sync adapter~~ — DONE-298 | ~~P1~~ | `conversation-corpus-engine@3d86009` |
| ~~IRF-CCE-025~~ | ~~Multi-provider refresh + LaunchAgent~~ — DONE-299 | ~~P1~~ | `conversation-corpus-engine@3d86009` + domus plist |
| IRF-CCE-026 | ChatGPT API scope degradation (633→4 conversations visible) | P1 | External blocker |
| IRF-CCE-027 | Post Office discover endpoint uses wrong API (gizmos ≠ Projects) | P2 | Blocked by CCE-026 |
| ~~IRF-CCE-028~~ | ~~Devise handoff documents for 6 open GH issues~~ — DONE-301 | ~~P1~~ | `conversation-corpus-engine@593c60d` |
| IRF-CCE-029 | Testament vacuum: S38/S39/S40 have no testament files | P2 | GH#17 |
| ~~IRF-CCE-030~~ | ~~S40 code committed in S41 close-out~~ — DONE-302 | ~~P2~~ | `conversation-corpus-engine@593c60d` |
| IRF-CCE-031 | CCE has no inquiry-log.yaml (SGO research vacuum) | P2 | GH#18 |
| IRF-CCE-032 | Omega format specimen missing from GH#14 handoff | P2 | GH#19 |
| IRF-CCE-033 | Execute CCE commercial architecture (H1: PyPI, MCP, landing page) | P1 | GH#20 |
| ~~IRF-CCE-034~~ | ~~GH issues missing for CCE-029/031/032/033~~ — DONE-S41-CLOSURE | ~~P2~~ | GH#17-24 created |
| IRF-CCE-035 | Omega evidence map: note commercial spec for #9/#10 | P2 | GH#21 |
| IRF-CCE-036 | seed.yaml planned produces edges (3 ORGAN-III vehicles) | P2 | GH#22 |
| IRF-CCE-037 | S41 testament gap — vacuum now spans S38-S41 (4 sessions) | P2 | GH#17 (combined with CCE-029) |
| IRF-CCE-038 | Cross-repo commercial awareness (CCE ↔ application-pipeline) | P2 | GH#23 |
| IRF-CCE-039 | Implementation plan not derived from commercial spec | P2 | GH#24 |

#### IRF-III Items (Commerce / Product Launch)

| ID | Description | Priority | Refs |
|----|-------------|----------|------|
| IRF-III-059 | the-actual-news canonical launch cutover vacuum: custom domain, public identity, hosted provider URLs, and strict deployed launch proof | P1 | `a-organvm/organvm-corpvs-testamentvm#21`, `a-organvm/the-actual-news` `.codex/plans/2026-06-07-actual-news-persistence-audit.md` |

#### Hermeneus API Routes (S28, 2026-03-21)

| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| `/api/chat` | POST | Rate-limited | AI chat with hybrid retrieval + provider cascade |
| `/api/health/llm` | GET | Public | Probes all LLM providers, reports latency + status |
| `/api/cron/ingest` | GET/POST | CRON_SECRET | Ingestion health metrics + staleness analysis |
| `/api/cron/maintenance` | POST | CRON_SECRET | Maintenance cycle with connectors + alerts |
| `/api/feedback` | POST | Public | User feedback on chat responses |
| `/api/admin/intel` | GET/POST | Session/Token | Admin scorecard + alerts |
| `/api/admin/session` | POST | Token | Admin session management |

Priority tiers: **P0** (now), **P1** (soon), **P2** (growth), **P3** (horizon).

---

## Formation IDs

Source: formation contracts in repo roots, especially `formation.yaml`.

| ID | Type | Host | Definition | Source |
|----|------|------|------------|--------|
| FORM-RES-001 | RESERVOIR | ORGAN-I (secondary: META-ORGANVM) | `conversation-corpus-site` — preserves, indexes, federates, and serves accumulated conversation knowledge across providers and organs. First registered reservoir formation in the post-flood order. | `organvm-i-theoria/conversation-corpus-site/formation.yaml` |

---

## SGO Research IDs

Source: [`inquiry-log.yaml`](../../../praxis-perpetua/commissions/inquiry-log.yaml), [`RESEARCH-REGISTRY.yaml`](../../../praxis-perpetua/research/sgo-2026-formalization-of-knowledge/RESEARCH-REGISTRY.yaml)

Three ID namespaces govern the SGO academic pipeline:

| Prefix | Namespace | Source | Example |
|--------|-----------|--------|---------|
| `INQ-YYYY-NNN` | Research commissions (all organs) | `inquiry-log.yaml` | INQ-2026-006 (The Formalization Programme) |
| `SGO-YYYY-D-NNN` | Dissertations | `inquiry-log.yaml` | SGO-2026-D-003 (Object Lessons) |
| `SGO-YYYY-RP-NNN` | Research papers (phase 1-2) | `RESEARCH-REGISTRY.yaml` | SGO-2026-RP-002 (Impossibility Landscape) |
| `SGO-YYYY-SYN-NNN` | Synthesis papers (phase 3-4) | `RESEARCH-REGISTRY.yaml` | SGO-2026-SYN-02 (Governance Impossibility) |

Active commissions: INQ-2026-001 through INQ-2026-009. The Formalization Programme (INQ-2026-006) contains 7 research papers (RP-001 through RP-007), 5 synthesis papers (SYN-01 through SYN-05), and 1 capstone.

---

## TODO Items

Source: [`rolling-todo.md`](./rolling-todo.md), [`e2g-ii-action-items.md`](../evaluation/e2g-ii-action-items.md)

### P0 — Break the Hermetic Seal

| ID | Definition | Constraint | Omega | Status |
|----|-----------|------------|-------|--------|
| X1 | Submit Google Creative Lab Five application | TIME | #5, feeds #7 | OPEN |
| X2 | Deploy life-my--midst--in to Render | TIME | #8 | OPEN |
| X3 | Submit 2 job applications (Together AI, HuggingFace) | TIME | #5, feeds #7 | OPEN |
| X4 | Make first social media post | READY | feeds #7, #13 | COMPLETED (2026-02-17) |

### P1 — Strengthen External Engagement

| ID | Definition | Constraint | Omega | Status |
|----|-----------|------------|-------|--------|
| E1 | Refresh operational cadence Part IV | — | — | COMPLETED (2026-02-16) |
| E2 | Enable non-dry-run soak test monitoring | TIME | #1, #3, #17 | COMPLETED (2026-02-17) |
| E3 | Submit Google Creative Fellowship (deadline Mar 18) | TIME | #5, feeds #14 | OPEN |
| E4 | Deploy essay drafts #34 and #35 | READY | #6 | COMPLETED (2026-02-16) |
| E5 | Write "Construction Addiction" essay (#36) | TIME | #6 | COMPLETED (2026-02-17) |

### P2 — System Quality

| ID | Definition | Constraint | Omega | Status |
|----|-----------|------------|-------|--------|
| M1-II | Recruit and run first stranger test | TIME | #2, #4, #16 | OPEN |
| M2-II | Stripe payment integration for life-my--midst--in | INCOME | #9, #10 | OPEN |
| M3-II | Refresh portfolio with post-construction evidence | TIME | #15 | OPEN |
| M4-II | Improve seed.yaml coverage 44% → 100% | TIME | — | COMPLETED (2026-02-17) |
| M5-II | Set up monitoring/alerting for life-my--midst--in | INCOME | — | OPEN |
| M6-II | CI restructure — fail on no tests | TIME | — | OPEN |

### P3 — Strategic

| ID | Definition | Constraint | Omega | Status |
|----|-----------|------------|-------|--------|
| S1-II | Complete 30-day soak test and generate report | TIME | #1, #17 | OPEN |
| S2-II | Host first salon (ORGAN-VI community event) | EXTERNAL | #11 | OPEN |
| S3-II | Create contribution pathway for external contributors | EXTERNAL | #12 | OPEN |
| S4-II | Write 2 planned essays (constraint-alchemy, performance-platform) | TIME | — | OPEN |
| S5-II | Investigate universal-mail--automation as 2nd product | EXTERNAL | — | OPEN |
| S6-II | Pursue conference talk or workshop proposal | TIME | #14 | OPEN |

### Setup Guide Items

| ID | Definition | Constraint | Omega | Status |
|----|-----------|------------|-------|--------|
| G1 | Set up LinkedIn developer token (OAuth flow) | TIME | — | OPEN |
| G2 | Render hosting for life-my--midst--in (deploy hook) | INCOME | — | OPEN |
| G3 | Ghost newsletter hosting (~$9/mo or self-host) | INCOME | — | OPEN |

---

## Omega Criteria

Source: [`there+back-again.md`](../strategy/there+back-again.md) §"The Nineteen Omega Criteria"

Constitutional amendment (2026-03-20): Old #9 (revenue_status: live) and #10 (MRR ≥ costs) replaced with craft-first criteria. Revenue follows traffic follows quality follows craft. Amendment (2026-03-21): #19 added — Network Testament health.

| # | Criterion | Horizon | Measurement | Status |
|---|-----------|---------|-------------|--------|
| 1 | 30-day soak test passes (≤3 critical incidents) | H1 | Soak test report | NOT MET |
| 2 | Stranger test score ≥80% | H1 | Test protocol results | NOT MET |
| 3 | Engagement baseline established (30 days of data) | H1 | Engagement report | NOT MET |
| 4 | Runbooks validated by second operator | H1 | Validation log | NOT MET |
| 5 | ≥1 application submitted | H2 | Application tracker | MET (2026-02-24) |
| 6 | AI-conductor essay published | H2 | Public-process URL | MET (2026-02-11) |
| 7 | ≥3 pieces of external feedback collected | H2 | Feedback synthesis doc | NOT MET |
| 8 | ≥1 ORGAN-III product live | H3 | Product URL + user count | MET (2026-02-28) |
| 9 | ≥3 products at stranger-ready polish | H3 | Stranger test per product (UI, docs, onboarding) | NOT MET |
| 10 | ≥100 unique visitors/month (organic discovery) | H3 | Analytics across portfolio + portal + products | NOT MET |
| 11 | ≥2 salons/events held with external participants | H4 | Event records | NOT MET |
| 12 | ≥3 external contributions to the system | H4 | GitHub activity | NOT MET |
| 13 | ≥1 organic inbound link from external site | H4 | Analytics | MET (2026-02-28) |
| 14 | ≥1 recognition event (grant, citation, invitation, or adoption) | H5 | Evidence URL | NOT MET |
| 15 | Portfolio updated with external validation | H5 | Portfolio site | MET (2026-03-19) |
| 16 | Bus factor >1 (validated, not just documented) | H1+H4 | Second operator log | NOT MET |
| 17 | System operates 30+ days without primary operator intervention | H1 | Soak test data | NOT MET |
| 18 | First organic revenue (inquiry → payment) | H5 | Payment record from organic discovery | NOT MET |
| 19 | Network Testament health (density + engagement + milestones) | H3 | network_density ≥ 0.5, engagement_velocity > 0, ≥1 milestone | NOT MET |

**Scorecard:** 5/19 MET (#5 application submitted 2026-02-24, #6 AI-conductor essay 2026-02-11, #8 12 products deployed 2026-02-28, #13 LobeHub organic inbound links 2026-02-28, #15 portfolio validation page 2026-03-19). #18 gated behind #9 + #10 (craft → traffic → revenue). #19 auto-assessed from network maps, engagement ledger, and milestone files.

---

## Horizons

Source: [`there+back-again.md`](../strategy/there+back-again.md) §"Five Parallel Horizons"

| ID | Name | Timeline | Focus | Feeds |
|----|------|----------|-------|-------|
| H1 | Prove It Works | Days 1–30 | Soak test, stranger test, runbooks, engagement baseline | H2, H4, H5 |
| H2 | Validate Externally | Days 15–90 | Applications, AI-conductor essay, external feedback | H3, H4, H5 |
| H3 | Generate Revenue | Days 30–180 | Ship ORGAN-III product, payment integration, first dollar | H4, H5 |
| H4 | Build Community | Days 60–365 | Salons, external contributors, organic readership | H5 |
| H5 | Achieve Recognition | Days 90–730 | Grants, citations, invitations, adoption | H4 (loop) |

**Critical path:** H1 → H2 → H3/H4 → H5

---

## Anti-Patterns

Source: [`operational-cadence.md`](./operational-cadence.md) Part VI

| ID | Name | Test Question |
|----|------|---------------|
| AP-1 | Don't Start Another Named Sprint | Am I building the system or using the system? |
| AP-2 | Don't Update the Registry Unless Something Actually Changed | Did something change in the real world (GitHub), or am I updating paperwork? |
| AP-3 | Don't Write More Documentation About Writing Documentation | Is this document for an external audience, or am I explaining the system to myself? |
| AP-4 | Don't Optimize Workflows That Are Already Passing | Is this workflow failing, or am I making it more elegant? |
| AP-5 | Don't Redesign the Portfolio When No One Has Seen It Yet | Has an external person given me feedback that motivates this change? |
| AP-6 | Don't Add Repos to Fill Perceived Gaps | Do I have code written that needs a home, or am I creating a home for code I haven't written? |
| AP-7 | Don't Confuse Motion With Progress | Does this advance an omega criterion, or does it make my dashboard look better? |

---

## E2G-II Findings

Source: [`e2g-ii-action-items.md`](../evaluation/e2g-ii-action-items.md) §"Cross-Reference: Finding → Action Item"

### Warnings (W)

| ID | Finding | Action Items |
|----|---------|-------------|
| W1-II | Zero external contact | X1, X2, X3, X4 |
| W2-II | Construction addiction unbroken | E5 |
| W3-II | Operational cadence stale | E1 (COMPLETED) |
| W4-II | Soak test nominal only | E2, S1-II |
| W5-II | Essay drafts not deployed | E4 |
| W6-II | Application materials expiring | X1, X3, E3 |

### Shatter Points (SP)

| ID | Finding | Action Items |
|----|---------|-------------|
| SP1-II | Hermetic seal shatter point | X1, X2, X3, X4 (all P0) |
| SP2-II | Construction addiction self-diagnosed | E5 |
| SP3-II | Day-count acceleration | All P0 items (urgency) |
| SP4-II | Beta product decay risk | X2, M5-II |

### Blind Spots (BS)

| ID | Finding | Action Items |
|----|---------|-------------|
| BS2-II | Self-assessment selection bias | M1-II (stranger test) |
| BS5-II | No social media presence | X4 |

### Latent Contradictions (LC)

| ID | Finding | Action Items |
|----|---------|-------------|
| LC1-II | Building in public but sealed | X4 (social media) |
| LC2-II | Construction addiction self-diagnosed | E5 |
| LC3-II | Ready but not submitted | X1, X3 |
| LC4-II | Beta-ready not deployed | X2 |

### Bright Lines (BL)

| ID | Finding | Action Items |
|----|---------|-------------|
| BL1-II | Omega scorecard as portfolio piece | M3-II (portfolio refresh) |
| BL3-II | Construction addiction essay value | E5 |

### Other (ET, LO)

| ID | Finding | Action Items |
|----|---------|-------------|
| ET2-II | Portfolio needs post-construction evidence | M3-II |
| ET3-II | Job applications need submission | X3 |
| LO3-II | Payment integration needed | M2-II |

---

## Sprints

Source: [`docs/specs/sprints/`](../specs/sprints/) (spec files), [`there+back-again.md`](../strategy/there+back-again.md) Appendix D (historical summary)

| # | Name | Date | Focus | Status |
|---|------|------|-------|--------|
| 01 | IGNITION | 2026-02-12 | Essay volume (21 essays, ~88K words) | COMPLETED |
| 02 | PROPULSION | 2026-02-12 | Batch promotion (17 repos PROTOTYPE→ACTIVE) | COMPLETED |
| 03 | ASCENSION | 2026-02-12 | More promotions (+12, +2 new repos) | COMPLETED |
| 04 | EXODUS | 2026-02-12 | Application prep (9 bundles, 66 ACTIVE) | COMPLETED |
| 05 | PERFECTION | 2026-02-12 | Portfolio expansion (20 projects) | COMPLETED |
| 06 | AUTONOMY | 2026-02-13 | Autonomous governance (seed.yaml, orchestrator) | COMPLETED |
| 07 | GENESIS | 2026-02-13 | Cross-org wiring (dispatch-receiver, CROSS_ORG_TOKEN) | COMPLETED |
| 08 | ALCHEMIA | 2026-02-13 | Orphan resolution (34 repos got produces/consumes) | COMPLETED |
| 09 | CONVERGENCE | 2026-02-13 | Graph validation (2 back-edge fixes) | COMPLETED |
| 10 | PRAXIS | 2026-02-13 | Audit + validation (E2G review) | COMPLETED |
| 11 | VERITAS | 2026-02-13 | Honesty corrections (PRODUCTION→ACTIVE, revenue split) | COMPLETED |
| 12 | ILLUSTRATIO | 2026-02-14 | Portfolio redesign (CMYK + Jost + p5.js) | COMPLETED |
| 13 | MANIFESTATIO | 2026-02-14 | Re-audit (3,586 code files, 7x previous) | COMPLETED |
| 14 | OPERATIO | 2026-02-16 | Operational readiness (soak test, runbooks) | COMPLETED |
| 15 | GAP-FILL | 2026-02-11 | Coverage gaps (+11 repos, +14 READMEs, 270K words) | COMPLETED |
| 16 | PLATINUM | 2026-02-11 | CI standardization (CI + CHANGELOG + ADR) | COMPLETED |
| 17 | REMEDIUM | 2026-02-16 | Workflow repair (phantom failures diagnosed) | COMPLETED |
| 18 | SYNCHRONIUM | 2026-02-16 | Workspace sync (missing repos cloned) | COMPLETED |
| 19 | CONCORDIA | 2026-02-16 | Registry reconciliation (91→97 repos) | COMPLETED |
| 20 | TRIPARTITUM | 2026-02-16 | Combined REMEDIUM+MEMORIA+ANNOTATIO (19 specs, 13 docs) | COMPLETED |
| 21 | SUBMISSIO | 2026-02-16 | Application verification (9 bundles verified) | COMPLETED |
| 22 | METRICUM | 2026-02-16 | Metrics variable system (calculate→store→propagate) | COMPLETED |
| 23 | PUBLICATIO | 2026-02-16 | Essay deployment (4 essays, 29→33) | COMPLETED |
| 24 | CANON | 2026-02-16 | Catalog reconciliation (4 numbering fixes) | COMPLETED |
| 25 | INSPECTIO | 2026-02-16 | Product assessment (life-my--midst--in selected) | COMPLETED |
| 26 | PROPAGATIO | 2026-02-16 | Findings propagation (fit scores, roadmap extended) | COMPLETED |
| 27 | BETA-VITAE | 2026-02-16 | Beta deployment prep (44 tables, 3 migration fixes) | COMPLETED |
| 28 | RECOGNITIO | 2026-02-17 | E2G-II review (omega scorecard 1/17) | COMPLETED |
| 29 | AUTOMATA | 2026-02-17 | Autonomous systems activation (3 cron workflows) | COMPLETED |
| 30 | DISTRIBUTIO | 2026-02-17 | Essay distribution pipeline (backfill, metadata) | COMPLETED |
| 31 | FUNDAMEN | 2026-02-17 | Infrastructure hardening V/VI/VII/Meta (85+ tests) | COMPLETED |
| 32 | SENSORIA | 2026-02-17 | Perception layer (100% seed.yaml, stale-detection) | COMPLETED |
| 33 | OPERATIO | 2026-02-17 | Autonomous operations batch (CLI, dashboard, essay-deploy) | COMPLETED |

---

## Cross-Reference: Omega ← TODO

Which TODO items advance which omega criteria. Items with no omega link are quality/maintenance work.

| Omega | Criterion | TODO Items |
|-------|-----------|------------|
| #1 | Soak test passes | E2, S1-II |
| #2 | Stranger test ≥80% | M1-II |
| #3 | Engagement baseline | E2 |
| #4 | Runbooks validated | M1-II |
| #5 | ≥1 application submitted | X1, X3, E3 |
| #6 | AI-conductor essay published | E4, E5 (MET via earlier deploy) |
| #7 | ≥3 external feedback | X1, X3, X4 (feeds) |
| #8 | ≥1 product live | X2 |
| #9 | ≥3 products at stranger-ready polish | M1-II (stranger test per product) |
| #10 | ≥100 unique visitors/month | — (requires analytics setup) |
| #11 | ≥2 salons/events | S2-II |
| #12 | ≥3 external contributions | S3-II |
| #13 | ≥1 organic inbound link | X4 (feeds) |
| #14 | ≥1 recognition event | E3, S6-II |
| #15 | Portfolio updated | M3-II |
| #16 | Bus factor >1 | M1-II |
| #17 | 30+ days autonomous | E2, S1-II |
| #18 | First organic revenue | M2-II (gated behind #9 + #10) |
| #19 | Network Testament health | — (auto-assessed from network maps) |

**Unlinked TODO items** (quality/infrastructure, no direct omega advancement): M4-II (seed.yaml), M5-II (monitoring), M6-II (CI restructure), S4-II (essays backlog), S5-II (second product investigation), G1 (LinkedIn token), G2 (Render hosting), G3 (Ghost newsletter).

---

## Institutional IDs

Source: `aerarium--res-publica/` — institutional wing. Package identities, grant application IDs, entity formation tracking.

| ID | Type | Definition | Source |
|----|------|------------|--------|
| `cvrsvs-honorvm` | Package | Extracted governance engine — promotion state machine, dependency DAG validator, seed contract parser. PyPI: `cvrsvs-honorvm`. License: Apache 2.0. Named after Roman *cursus honorum* (sequential order of public offices). ORGANVM orthography: V for U. | S38, `aerarium--res-publica/applications/nlnet-ngi0-commons-2026/draft.md` |
| `IRF-INST-NNN` | IRF domain | Institutional strategy work items (entity formation, grants, donor infrastructure). 18 items as of S38. | `INST-INDEX-RERUM-FACIENDARUM.md` |
| `NLnet-NGI0-2026` | Application | NLnet NGI0 Commons Fund application for Cvrsvs Honorvm. EUR 37,080, 11 milestones. Deadline: 2026-04-01 12:00 CEST. | `aerarium--res-publica/applications/nlnet-ngi0-commons-2026/draft.md` |

---

## A-Organism Embodiment IDs

Source: `a-organvm/` — embodiment vocabulary introduced during S47 second-function work.

| ID | Type | Definition | Source |
|----|------|------------|--------|
| `CIR-001` | Function ID | `circulatory_route.py` — the organism's second embodiment/function. Computes routes, signal attractions, and structural defects across gate contracts to assess circulation. | `a-organvm/RELAY.md`, `a-organvm/circulatory_route.py` |
| `SIG-002` | Signal type | `CONTRACT` — a declared behavioral agreement between organism functions. Added to `signal-graph.yaml` during S47. | `a-organvm/RELAY.md`, `a-organvm/signal-graph.yaml` |
| `SIG-003` | Signal type | `STATE` — the current configuration of the organism's elements at a point in time. Added to `signal-graph.yaml` during S47. | `a-organvm/RELAY.md`, `a-organvm/signal-graph.yaml` |
| `GEN-002` | Naming rule | Canonical names use `--` (double hyphen); Python module filenames map canonical `--` to `_` when rendered on disk. | `a-organvm/pyproject.toml`, `a-organvm/circulatory_route.py` |

---

## Named Code Entities

Source: `organvm-engine/src/organvm_engine/` — key classes by domain module. ~200 total classes across 28 modules.

| Module | Key Classes | Description |
|--------|-------------|-------------|
| `atoms/` | `AtomLink`, `PipelineResult`, `ReconcileResult`, `TaskVerdict`, `OrganRollup` | Atomization pipeline: Jaccard linking, reconciliation, per-organ fanout |
| `audit/` | `Finding`, `Severity`, `LayerReport`, `InfrastructureAuditReport` | Multi-layer infrastructure audit with severity-tagged findings |
| `ci/` | `CheckStatus`, `RepoCompliance`, `InfraAuditReport`, `CITriageReport`, `ScaffoldResult` | CI health triage, compliance auditing, workflow scaffolding |
| `content/` | `ContentPost`, `ContentSignal`, `CadenceReport` | Content reading, signal extraction, publishing cadence |
| `coordination/` | `WorkClaim`, `ClaimConflict`, `AgentPhase`, `ToolCheckout` | Multi-agent claims registry, lifecycle phases, tool concurrency |
| `deadlines/` | `Deadline` | Parsed deadline with date, omega links |
| `debt/` | `DebtItem` | Technical debt scanner items |
| `dispatch/` | `WebhookReceiver`, `DispatchReceipt`, `FormalVerificationError` | Event routing, webhook reception, idempotency |
| `distill/` | `OperationalPattern`, `PatternMatch`, `CoverageEntry` | Pattern taxonomy, prompt matching, SOP coverage |
| `events/` | `EventType`, `EventRecord`, `EventSpine` | Central event bus for system-wide event routing |
| `governance/` | `MultiplexGraph`, `DependencyResult`, `ImpactReport`, `SanctionEngine`, `EraTracker`, `FeedbackLoopInventory`, `TemporalGraph`, `Formation`, `PlacementAudit`, `DictumReport`, `ConformanceResult` | Dependency graph, state machine, sanctions, eras, feedback loops, placement, interrogation |
| `indexer/` | `Component`, `RepoIndex`, `SystemIndex`, `BridgeResult` | Repo component indexing, system-wide index, ontologia bridge |
| `irf/` | `IRFItem` | Parsed IRF work item with priority, domain, status |
| `ledger/` | `AnchorRecord`, `ChainVerificationResult`, `ChainIndex`, `EventTier` | Git-anchored ledger, chain verification, segment rotation |
| `metrics/` | `GateResult`, `RepoProgress`, `SystemOrganism`, `PropagationResult`, `HeartbeatReport`, `ConsilienceReport`, `LintReport` | Gate evaluation, organism health, propagation, consilience |
| `network/` | `MirrorEntry`, `NetworkMap`, `EngagementEntry` | External mirror tracking, engagement ledger |
| `omega/` | `OmegaScorecard`, `OmegaCriterion`, `SoakStreak`, `NetworkTestamentResult`, `Phase` | 19-criterion scorecard, soak analysis, network testament, phases |
| `ontologia/` | `RegistrySensor`, `SoakSensor`, `CISensor`, `PromotionSensor` | Data sensors feeding ontologia entity system |
| `ontology/` | `Relation`, `UnifiedRelationStore`, `Capability`, `CapabilityRegistry`, `EntityCategory` | Entity relations, capabilities, taxonomy |
| `paths.py` | `PathConfig` | Foundation: canonical workspace/corpus/soak path resolution |
| `pitchdeck/` | `PitchTheme`, `PitchDeckData` | Pitch deck rendering data and themes |
| `plans/` | `AtomicTask`, `PlanParser`, `PlanIndex`, `PlanOverlap`, `PlanSprawl` | Plan atomization, indexing, overlap detection, hygiene |
| `prompts/` | `AnnotatedPrompt`, `RawPrompt`, `NarrateResult`, `ClipboardPrompt` | Prompt extraction, classification, narrative threading, clipboard |
| `pulse/` | `AMMOI`, `PulseSnapshot`, `Advisory`, `SystemMood`, `MoodReading`, `NerveBundle`, `FlowProfile`, `DensityProfile` | Real-time system pulse: density, mood, advisories, flow |
| `registry/` | `ValidationResult`, `RegistryStats` | Registry validation and aggregate statistics |
| `seed/` | `SeedGraph`, `SignalGraph`, `SignalPort`, `SignalEdge` | Seed discovery, produces/consumes graph, signal routing |
| `session/` | `SessionMeta`, `SessionExport`, `AgentSession`, `SessionDebrief`, `PlanFile` | Multi-agent session parsing, export, debrief |
| `sop/` | `SOPEntry`, `AuditResult` | SOP/METADOC discovery and inventory audit |
| `testament/` | `TestamentArtifact`, `CatalogSummary`, `AestheticProfile`, `RenderResult`, `OrganOutputProfile`, `SonicTestament` | Testament artifacts, aesthetic profiles, multi-modal rendering |
| `trivium/` | `Dialect`, `DialectProfile`, `Correspondence`, `TranslationPair`, `TranslationEvidence` | Organ dialects, cross-organ correspondence, translation |
| `verification/` | `DispatchLedger`, `DispatchContract`, `VerificationReport`, `TemporalResult` | Dispatch idempotency, contract verification, model checking |

---

## Event Types

Source: `organvm-engine/src/organvm_engine/events/` — `EventType` enum values emitted by engine modules.

### Fossil & Testament Events (S34, 2026-03-23)

| Event Type | Emitter | Description |
|------------|---------|-------------|
| `ARCHITECTURE_CHANGED` | `testament/` | Emitted when new modules, types, or enums are added to the engine |
| `SCORECARD_EXPANDED` | `testament/` | Emitted when omega criteria count changes |
| `VOCABULARY_EXPANDED` | `testament/` | Emitted when new event types or governance IDs are introduced |
| `EPOCH_CLOSED` | `fossil/` | Emitted by fossil bridge when a geological epoch ends |
| `INTENTION_BORN` | `fossil/` | Emitted by fossil bridge when a unique prompt is captured (uniqueness > 0.9) |
| `DRIFT_DETECTED` | `fossil/` | Emitted by fossil bridge when intention-reality convergence < 0.3 |

---

## CLI Commands

Source: `organvm-engine/src/organvm_engine/cli/` — command groups registered under the `organvm` entry point.

### Fossil Commands (S34, 2026-03-23)

| Command | Description |
|---------|-------------|
| `organvm fossil excavate` | Crawl git history, classify commits by Jungian archetype, produce fossil-record.jsonl |
| `organvm fossil chronicle` | Generate Jungian-voiced epoch narratives from fossil data |
| `organvm fossil intentions` | Extract and browse unique prompt intentions |
| `organvm fossil drift` | Analyze intention-reality divergence |
| `organvm fossil epochs` | List all declared geological epochs |
| `organvm fossil stratum` | Query the fossil record by organ/archetype |
| `organvm fossil witness install` | Install post-commit hooks for real-time capture |
| `organvm fossil witness status` | Show witness coverage across workspace |
| `organvm fossil witness record` | Record a single witnessed commit (called by hook) |

### Taxonomy Commands (S34, 2026-03-23)

| Command | Description |
|---------|-------------|
| `organvm taxonomy classify` | Classify repos by functional heuristic |
| `organvm taxonomy audit` | Audit functional classification coverage |

### Testament Commands (S34, 2026-03-23)

| Command | Description |
|---------|-------------|
| `organvm testament record-session` | Record architecture events from git diff range |

### CCE Commands (S33, 2026-03-24)

Source: `conversation-corpus-engine/src/conversation_corpus_engine/cli.py` — entry point `cce`.

| Command | Description |
|---------|-------------|
| `cce corpus list \| register` | Manage corpus registry |
| `cce federation build` | Materialize cross-corpus federated indices |
| `cce provider discover \| readiness \| import \| bootstrap-eval \| refresh` | Provider lifecycle |
| `cce evaluation run` | Run regression gate evaluation |
| `cce review queue \| history \| resolve \| triage` | Federated review queue + auto-triage |
| `cce policy show \| replay \| stage \| review \| apply \| rollback` | Promotion threshold governance |
| `cce candidate show \| history \| stage \| review \| promote \| rollback` | Corpus candidate workflow |
| `cce schema list \| show \| validate` | Inspect/validate 8 JSON schema contracts |
| `cce surface manifest \| context \| bundle` | Meta/MCP-facing surface exports |
| `cce source-policy show \| set \| history` | Per-provider source authority |
| `cce source freshness` | Source staleness check |
| `cce dashboard` | Operator-facing health summary |
| `cce migration seed-from-staging` | Bootstrap registry from legacy staging root |

### CCE Triage Policies (S33, 2026-03-24)

| Policy | Type | Decision | Description |
|--------|------|----------|-------------|
| `exact-cross-corpus` | All | accept | Same local ID across different corpora |
| `slug-match` | family/action/unresolved-merge | accept | Same title slug, different UUID suffix |
| `prefix-entity-alias` | entity-alias | accept | One entity ID is prefix of other (cross-corpus) |
| `noise-entity` | entity-alias | reject | Numeric/null/boolean entity tokens |
| `short-entity` | entity-alias | reject | Entity ID too short to be meaningful |
| `contradiction-defer` | contradiction | defer | Contradictions require human review |

### CCE Artifact Types (S33, 2026-03-24)

| Artifact | Schema | Location |
|----------|--------|----------|
| `import-audit.json` | (unschematized) | `{corpus}/corpus/import-audit.json` |
| `near-duplicates.json` | (unschematized) | `{corpus}/corpus/near-duplicates.json` |
| `dashboard-payload` | (JSON via `--json`) | `cce dashboard --json` output |
| `triage-plan` | (JSON via `--json`) | `cce review triage --json` output |

### CCE Providers (S33, 2026-03-24)

| Provider | Adapter Type | Discovery Mode |
|----------|-------------|----------------|
| `chatgpt` | chatgpt-export | chatgpt-bundle |
| `claude` | claude-export | claude-bundle |
| `gemini` | gemini-export | document-export |
| `grok` | grok-export | document-export |
| `perplexity` | perplexity-export | document-export |
| `copilot` | copilot-export | document-export |
| `deepseek` | deepseek-export | document-export |
| `mistral` | mistral-export | document-export |

### Omega Proposals (S33, 2026-03-24)

| ID | Text | Status |
|----|------|--------|
| `OM-MEM-001` | Memory infrastructure demonstrates closed-loop autopoiesis — ≥1 session transcript completes ingest→normalize→evaluate→federate→surface→consume lifecycle | Proposed, evidence demonstrated, awaiting formal amendment |

---

## URI Schemes

| Scheme | Format | Example | Purpose |
|--------|--------|---------|---------|
| `fossil://` | `fossil://{type}/{id}` | `fossil://epoch/EPOCH-007`, `fossil://intention/INT-2026-03-21-001` | Reference scheme for fossil record entities |

---

## MCP Tools

Source: `organvm-mcp-server/src/organvm_mcp/` — tools exposed via MCP stdio protocol.

| Tool | Description |
|------|-------------|
| `organvm_query_registry` | Query registry by organ/status/tier |
| `organvm_get_repo` | Get full repo entry |
| `organvm_list_organs` | List all organs with repo counts |
| `organvm_get_seed` | Get seed.yaml for a repo |
| `organvm_find_edges` | Find produces/consumes edges |
| `organvm_get_event_contract` | Get event contract for a repo |
| `organvm_list_events` | List all registered events |
| `organvm_trace_dependencies` | Trace dependency chain |
| `organvm_check_dependency` | Check if a dependency edge is valid |
| `organvm_get_dependency_graph` | Get full dependency graph |
| `organvm_system_health` | System health summary |
| `organvm_omega_status` | Omega scorecard status |
| `organvm_ci_health` | CI health across organs |
| `organvm_upcoming_deadlines` | Upcoming deadlines |
| `organvm_pitch_status` | Pitch deck status |
| `organvm_get_context` | Cross-repo awareness context |
| `organvm_irf_query` | Query the IRF from agent sessions |

---

*This concordance was last updated on 2026-03-31. It should be updated when TODO items are completed, new IDs are created, or omega criteria change status. The `scripts/invoke.py` CLI tool parses this file directly — keep the markdown table format consistent.*

---

## Fieldwork Intelligence System (added S-fieldwork-mvp, 2026-03-31)

Layer 1 of 4-layer process intelligence system. Captures observations from contribution workflows.

### Enums

| Enum | Values | Location |
|------|--------|----------|
| `ObservationCategory` | merge_protocol, review_culture, ci_architecture, repo_layout, tooling, contributor_experience, communication_style, governance, documentation, security_posture (10) | `contrib_engine/schemas.py` |
| `SpectrumLevel` | AVOID=-2, CAUTION=-1, NOTE=0, STUDY=+1, ABSORB=+2 (IntEnum — first in codebase) | `contrib_engine/schemas.py` |
| `StrategicTag` | shatterpoint, missing_shield, friction_point, fortress, competitive_edge, competitive_gap (6) | `contrib_engine/schemas.py` |
| `ObservationSource` | pr_submission, review_response, ci_run, repo_exploration, phase_transition, automated (6) | `contrib_engine/schemas.py` |

### Models

| Model | Fields | Location |
|-------|--------|----------|
| `FieldObservation` | id, workspace, timestamp, category, signal, spectrum, strategic, source, evidence, scored_by, related_absorption_ids, atom_id | `contrib_engine/schemas.py` |
| `FieldworkIndex` | generated, observations + by_workspace(), by_category(), by_spectrum() | `contrib_engine/schemas.py` |

### CLI Commands

| Command | Description |
|---------|-------------|
| `fieldwork record` | Append observation to stream. Flags: --workspace, --category, --signal, --spectrum, --source, --evidence, --strategic, --scored-by |
| `fieldwork show` | Display observations. Filters: --workspace, --category, --min-spectrum |

### Data Files

| File | Pattern | Location |
|------|---------|----------|
| `fieldwork.yaml` | Append-only observation stream (rotation at 500 planned) | `contrib_engine/data/fieldwork.yaml` |

### ID Format

| Pattern | Example | Description |
|---------|---------|-------------|
| `fo-{workspace_short}-{MMDD}-{seq:03d}` | `fo-dbt-mcp-0330-001` | Strips `contrib--` prefix, sequential per workspace+date |

### Session IDs

| ID | Session | Date |
|----|---------|------|
| `S-fieldwork-mvp` | Fieldwork Layer 1 MVP + seed.yaml P0 fix + health audit | 2026-03-31 |
| `S52` | 72h Reconciliation Plotting and Tending (116 unresolved) | 2026-04-02 |

### IRF Items

| ID | Title |
|----|-------|
| `IRF-OSS-022` | Fieldwork implementation (Layer 1 done, Layers 2-4 remain) |
| `IRF-OSS-027` | TypeScript dead code archive |
| `IRF-OSS-028` | Workflow execution audit |
| `IRF-OSS-029` | Render CLI subcommand |
| `IRF-OSS-030` | Unused imports cleanup |
| `IRF-OSS-031` | capabilities.py test file |
| `IRF-AOR-009` | Define Cultvra (Logos) Layer |
| `IRF-SYS-050` | Workspace Ontology v2 Refinement |
| `IRF-APP-080` | Productize Application Pipeline |
| `IRF-OSS-042` | System-wide Action Ledger |
| `IRF-OSS-043` | IRF Instrument v3 (Endless Box) |
| `IRF-SYS-051` | Stable Unit Notice Ownership Audit |

### Sessions

| ID | Description |
|----|-------------|
| `S52` | 72h Reconciliation Plotting |
| `S-2026-04-02` | Governance Audit & Notice Ownership Tending |

---

## Conductor Fleet Dispatch (added S-dispatch, 2026-03-30)

System-wide cognitive service dispatch — routes tasks to AI agents by work type.

### Concepts

| Term | Definition | Location |
|------|-----------|----------|
| `cognitive-service-dispatch` | Produces edge: the dispatch capability as a system artifact | `tool-interaction-design/seed.yaml` |
| `work_types.yaml` | Taxonomy of 8 cognitive work types with class hierarchy | `tool-interaction-design/conductor/work_types.yaml` |
| `cognitive_class` | Hierarchy: `strategic > tactical > mechanical`. Agents have `max_cognitive_class` restrictions | `fleet.yaml` restrictions block |
| `TaskDispatcher` | Classifies work descriptions and routes to constrained agents via `FleetRouter` | `conductor/task_dispatcher.py` |
| `GuardrailedHandoffBrief` | Extended handoff envelope with `constraints_locked`, `files_locked`, `work_completed`, `conventions`, `verification_required` | `conductor/fleet_handoff.py` |
| `CrossVerifier` | Verifies agent output against handoff constraints (locked files, never-touch patterns, convention drift) | `conductor/cross_verify.py` |
| `active-handoff.md` | Canonical file receiving agents read on session start. Written/cleared by dispatch lifecycle | `.conductor/active-handoff.md` |

### MCP Tools

| Tool | Description |
|------|-------------|
| `conductor_fleet_dispatch` | Classify work and route to best-fit agent. Returns ranked agents with exclusion reasons |
| `conductor_fleet_guardrailed_handoff` | Generate constraint-carrying envelope for agent handoff. Auto-writes active-handoff.md |
| `conductor_fleet_cross_verify` | Verify agent output against handoff constraints. Auto-clears active-handoff.md on pass |

### Session IDs

| ID | Session | Date |
|----|---------|------|
| `S-dispatch` | Cognitive Service Dispatch design + implementation + fleet execution | 2026-03-30 |

### Inquiry

| ID | Title |
|----|-------|
| `INQ-2026-010` | The Fleet Protocol — task-to-agent routing with guardrailed handoff |

---

## TRX — Zettelkasten Transcript IDs

Source: [`post-flood/archive_original/.zettel-index.yaml`](../../../post-flood/archive_original/.zettel-index.yaml)
Validator: [`post-flood/archive_original/validate-zettelkasten.py`](../../../post-flood/archive_original/validate-zettelkasten.py)
Created: S-Zettelkasten (2026-04-13)

| Pattern | Scope | Count |
|---------|-------|-------|
| `TRX-{CAS\|TDR\|VSA\|HIS\|NSC}` | 5 trunk transcripts | 5 |
| `TRX-{trunk}.{N}[.{N}]` | Branch transcripts (up to depth 3) | 13 |
| `TRX-C.{01-10}` | Compiled specifications | 10 |

### Trunk Codes

| Code | Full Name | QA Own | Children |
|------|-----------|--------|----------|
| CAS | Commit Assessment Summary | 18 | CAS.1, CAS.2 |
| TDR | Top-Down Refinement Pipeline | 5 | TDR.1, TDR.2 |
| VSA | Virtual System Architecture | 2 | VSA.1 |
| HIS | Hierarchical Index Structures | 3 | — |
| NSC | Name and Structure Changes | 4 | — |

---

## Threshold Topology IDs

Source: [`governance-thresholds.json`](../../../../organvm-iv-taxis/orchestration-start-here/governance-thresholds.json)
Documentation: [`threshold-topology.md`](../../../../organvm-iv-taxis/orchestration-start-here/docs/threshold-topology.md)
Created: S-threshold (2026-04-06)
IRF: IRF-SYS-092, GH#152

Two-axis governance membrane: Scope (SUBSTRATE/CONTROL/PRODUCTION/INTERFACE) x Depth (ORGANISM/COMPOUND/MOLECULE/ATOM) = 16 threshold cells. Each cell carries radius and permeability.

### Threshold Cells (16)

| ID | Scope | Depth | Local Rules | Permeability (D/U/L) |
|----|-------|-------|-------------|---------------------|
| T(S,O) | SUBSTRATE | ORGANISM | art_I, art_III, amend_H | 1.0/0.0/1.0 |
| T(S,C) | SUBSTRATE | COMPOUND | art_VI, amend_A | 1.0/0.3/1.0 |
| T(S,M) | SUBSTRATE | MOLECULE | amend_C | 0.8/0.3/0.8 |
| T(S,A) | SUBSTRATE | ATOM | classified_seed_schema_conformance | 0.0/0.2/0.5 |
| T(C,O) | CONTROL | ORGANISM | amend_B, amend_D, classified_logic_first_governance | 0.9/0.1/0.8 |
| T(C,C) | CONTROL | COMPOUND | art_II, art_IV, rule_promote_to_art, rule_promote_to_commerce, wip_limits | 0.8/0.2/0.7 |
| T(C,M) | CONTROL | MOLECULE | amend_E, amend_F, amend_G | 0.7/0.2/0.5 |
| T(C,A) | CONTROL | ATOM | classified_action_ledger_emission, classified_ci_workflow_enforcement, classified_non_interactive_agent_safety | 0.0/0.2/0.3 |
| T(P,O) | PRODUCTION | ORGANISM | *(empty — governed by CONTROL Art. II)* | 0.8/0.1/0.3 |
| T(P,C) | PRODUCTION | COMPOUND | art_V | 0.7/0.2/0.3 |
| T(P,M) | PRODUCTION | MOLECULE | classified_production_repo_conventions | 0.6/0.2/0.2 |
| T(P,A) | PRODUCTION | ATOM | *(empty — no file-level production governance yet)* | 0.0/0.2/0.1 |
| T(I,O) | INTERFACE | ORGANISM | classified_interface_read_many_write_one | 0.8/0.1/0.3 |
| T(I,C) | INTERFACE | COMPOUND | classified_editorial_governance, classified_organ_aesthetic_identity | 0.7/0.2/0.3 |
| T(I,M) | INTERFACE | MOLECULE | classified_frontmatter_schema_validation | 0.6/0.2/0.2 |
| T(I,A) | INTERFACE | ATOM | classified_essay_file_constraints | 0.0/0.2/0.1 |

### Classified Governance Rules (11)

Informal operational conventions made visible during threshold classification (Waves 2-3).

| ID | Cell | Description |
|----|------|-------------|
| classified_seed_schema_conformance | T(S,A) | seed.yaml must conform to schema |
| classified_logic_first_governance | T(C,O) | Logic precedes ceremony in orchestration |
| classified_action_ledger_emission | T(C,A) | Every action emits a ledger entry |
| classified_ci_workflow_enforcement | T(C,A) | CI workflows enforced at atomic granularity |
| classified_non_interactive_agent_safety | T(C,A) | Non-interactive agents operate with safety constraints |
| classified_production_repo_conventions | T(P,M) | Production repos follow naming/structure conventions |
| classified_interface_read_many_write_one | T(I,O) | Interface organs read from many, write to one |
| classified_editorial_governance | T(I,C) | Editorial standards at organ compound level |
| classified_organ_aesthetic_identity | T(I,C) | Each organ maintains aesthetic identity |
| classified_frontmatter_schema_validation | T(I,M) | Frontmatter validated against schema per-repo |
| classified_essay_file_constraints | T(I,A) | Essay files follow format constraints |
