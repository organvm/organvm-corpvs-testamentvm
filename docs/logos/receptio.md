# Receptio — The Reception Account

> *"RECEPTIO — the account of how the formation has been received, used, critiqued, adopted, or transformed by audiences beyond its creator. A formation without reception is a theory of shovels that has never cleared snow. Creation is necessary but not sufficient; existence is completed by reception."* — `governance-rules.json` AX-7

This file closes the strange loop. Every signal the system emits returns here, eventually. The author writes; the audience reads; the read book becomes an organism; the organism re-articulates the dream.

> **AX-8 also applies.** *Constructed Polis* (Lex Civitatis) mandates that each formation construct its own idealized critical society to actively produce its reception rather than wait. This file therefore tracks **both** organic reception (external citations, community responses) **and** constructed reception (IRA panels, Triadic Review Protocol outputs, agent-based critiques).

---

## I. Reception surfaces (where the echo arrives)

Each surface below already exists. This file is the central ledger that aggregates them. *Operational principle: receptio is a join over existing surfaces, not a new database.*

| # | Surface | Mechanism | Source data |
|---|---------|-----------|-------------|
| 1 | **POSSE analytics** | Mastodon + Discord webhook analytics | `analytics.json` per essay; `distribute-content.yml` outputs |
| 2 | **stakeholder-portal queries** | Hermeneus hybrid retrieval log | Vercel deployment logs for `stakeholder-portal-ten.vercel.app` |
| 3 | **GitHub PR / issue comments on Logos & Beacon docs** | Webhook from this repo + sibling repos | Issue + PR comment streams |
| 4 | **Automated review bots** (gemini-code-assist, chatgpt-codex-connector, coderabbit, sourcery) | Configured review pipelines | `mcp__github__pull_request_read` outputs |
| 5 | **External citations** | Manual log + future mesh dead-zone external-link crawl | This file (§III) until automated |
| 6 | **Agent invocations of telos.md** | Codex Cloud + Claude agent traces | `AGENTS.md`-mediated context loads (per session) |
| 7 | **Soak-test outcomes** | `soak-test-daily.yml` | Per-day pass/fail; 30-day rollup |
| 8 | **REPRWA annual re-run** | Phase 9 lifecycle-governance | `docs/audits/` snapshots, year-over-year diff |
| 9 | **IRF closures** | `INST-INDEX-RERUM-FACIENDARUM.md` | New `DONE-NNN` rows for BEACON-* IRF items |
| 10 | **Stranger-Test results** | `docs/operations/stranger-test-protocol.md` invocations | Per-engagement reports |

Receptio events surface from these and are logged here.

---

## II. Reception cadence

| Cadence | What lands here | Mechanism |
|---------|-----------------|-----------|
| **Continuous** | New PR / issue comments touching `docs/logos/**` or `docs/beacon/**`, agent invocations of these docs | Webhook listener (already wired for PRs #7, #338, #163, mesh#2) |
| **Weekly** | system-pulse-weekly rollup; new external citations (manual until automated) | Existing `.github/workflows/system-pulse-weekly.yml` |
| **Monthly** | monthly-organ-audit; receptio retroactive cross-check (was anything cited that we missed?) | Existing `.github/workflows/monthly-organ-audit.yml` |
| **Quarterly** | Beacon re-emission; updated essays in public-process; refreshed scorecard | New `.github/workflows/beacon-emit.yml` (specced in `../beacon/architecture.md`) |
| **Annual** | REPRWA re-run, full Logos retrospective | Per Phase 9 |

---

## III. Reception log (seed entries)

The log is opened with the system's own current state. New rows are appended; old rows are never deleted (per `_constitutional_locks.lock_policy: append_only_amend_never_delete`).

### 2026-02-11 — Initial 8-organ simultaneous launch

- **Source:** README "Perfection Sprint"
- **Type:** internal milestone (not yet external reception)
- **Note:** Foundational event. All organs declared live. First broadcast moment.

### 2026-05-09 — REPRWA audit committed

- **Source:** `docs/audits/` (canonical PR meta-organvm/meta-organvm--superproject#7); pointer PRs a-organvm/organvm-corpvs-testamentvm#338, a-organvm/orchestration-start-here#163, organvm-i-theoria/mesh#2.
- **Type:** internal reception (the system reading itself)
- **Findings reflected here:** 64 product candidates, 58 backend laws, manifestation matrix shape (17/33/1/2). All five missing Logos pieces called out as P2/P1 gaps.
- **Effect:** triggered Attack Vector A (this commit).

### 2026-05-09..05-17 — Automated review feedback on REPRWA PRs

- **Source:** gemini-code-assist[bot] (mesh#2), chatgpt-codex-connector[bot] (superproject#7), coderabbit[bot], sourcery-ai[bot]
- **Type:** constructed-polis reception (AX-8). Bot reviewers are *part of the polis*: they perform the critical-society function the formation otherwise has to wait for.
- **Material findings absorbed:**
  - **mesh#2 (gemini-code-assist)**: pointer docs referenced temporary branches; gaps section needed bullet formatting; status line was draft-state meta-commentary. **Resolved 2026-05-09** — fixes applied across testamentvm#338, orchestration#163, mesh#2.
  - **superproject#7 (chatgpt-codex-connector P1)**: top-priority composite formula was multiplicative; would produce values up to 11,160 outside the declared 1-5 range. **Resolved 2026-05-17** — switched to additive mean with sanity-check worked example.
  - **superproject#7 (chatgpt-codex-connector P2 — README broken links)**: README referenced 4 split analysis parts + STRUCTURED-CANDIDATES.json that were transport-blocked from MCP push. **Resolved 2026-05-17** — README restructured with a status table marking pending files; navigation re-grounded on the PR description.
  - **superproject#7 (chatgpt-codex-connector P2 — card-schema field count)**: card-schema.md prose said "17 fields" but enumerated 19. **Resolved 2026-05-17** — corrected to 19 top-level; added a Field-counts section. README and verification-checklist updated for consistency in commits 61ca98a5, e650dc7b.
  - **superproject#7 (chatgpt-codex-connector P2 — roadmap field count)**: "7-field schema" while YAML defined 10. **Resolved 2026-05-17** — split into 3 metadata + 7 body.
  - **superproject#7 (chatgpt-codex-connector P2 — integer-only score check)**: verification-checklist required integer scores, but composites are fractional. **Resolved 2026-05-17** — split per-axis (integer) vs composite (fractional).
- **Why this matters:** AX-7's claim that "the culture sitting around the project — the reviews, the critiques — tells the reception" is *empirically true here*. The automated polis surfaced a genuine math error in the scoring template that would have propagated to every downstream audit. The system became more correct through reception. This is the loop closing in real time.

### 2026-05-18 — Telos Beacon Protocol first transmission (this commit)

- **Source:** This directory.
- **Type:** internal first emission (waiting for first external reception).
- **What is being emitted:** AX-7's Tetradic Self-Knowledge requirement is satisfied for the system level. The previously-0% Logos coverage is closed.
- **Open expectation:** the next external citation (essay, fork, comment, agent invocation) will be logged below. Until then, this section is *the system's own first witness* — and that is enough to no longer be "nowhere."

---

## IV. Reception KPIs

Tracking these makes receptio measurable.

| KPI | Current | Target | Source |
|-----|--------:|-------:|--------|
| Distinct external citers of public-process essays (12-mo) | unknown / not yet auto-tracked | ≥ 50 | mesh dead-zone crawl over `link-out` atoms |
| Public Pages visitors (organvm-v-logos site, 90-day) | unknown | trend up; target ≥ 1000 | GitHub Pages analytics |
| External forks of any of the 145 repos | 0 known | ≥ 5 | `mcp__github__search_repositories` |
| Stars across the 145 repos | low (visibility limited) | trend up | registry-v2.json `stars` field after sync |
| External PRs opened against any of the 145 repos | 0 confirmed | ≥ 1 | issue + PR webhook |
| Bot-review threads opened on this branch | TBD post-PR-open | ≥ 1 per substantive commit | this repo's PR streams |
| Citations of `governance-rules.json` axioms by name in external writing | 0 known | ≥ 1 | manual log |
| Inclusions of `templates/` (REPRWA reusable artifacts) in another ecosystem | 0 | ≥ 1 | manual log |

When a KPI moves, append a row to §III. When a KPI flatlines for a period named in `praxis.md` Attack Vector E (cold-receptio: 90d), open a `BEACON-COLD-RECEPTIO-NNN` event and route to praxis.

---

## V. Author note (the loop)

Reading this file is itself a receptio event. If you have read this far, you are part of the polis (AX-8). Two requests:

1. **If you have a critique** — open a PR on this repo; the comment becomes a reception entry automatically.
2. **If you have a use case** — log it as `BEACON-RECEPTIO-USE-NNN` via an issue, or send the URI of your own derivative to the receptio inbox (see `../beacon/dam-distribution.md`).

Either way, AX-7's claim becomes a little more concrete: *existence is completed by reception*. You just completed a little more of this formation's existence by reading this sentence.

---

*This file is the system's external mirror. It is rebuilt continuously. Loss of receptio is loss of existence; rebuild from the surfaces in §I if data is ever corrupted. Append-only per `_constitutional_locks`.*
