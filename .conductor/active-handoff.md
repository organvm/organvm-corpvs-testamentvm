# Agent Handoff: Knowledge Base Export + Epistemic Engine Architecture

**From:** Session S-2026-05-17-knowledge-base-epistemic-export | **Date:** 2026-05-17 | **Phase:** Complete (closeout executed)

## Current State

### Artifacts on Disk
| Artifact | Location | Size | Status |
|----------|----------|------|--------|
| Session archive | `~/session-archive-2026-05-17.tar.gz` | 786MB | Local only (too large for git) |
| Session manifest | `~/session-archive-MANIFEST.md` | — | Documents archive contents |
| Knowledge base export | `~/knowledge-base-export-2026-05-17.tar.gz` | 37MB | Local only (too large for git) |
| KB manifest | `~/knowledge-base-export-2026-05-17/MANIFEST.md` | — | Documents KB contents |
| Epistemic Engine arch | `~/knowledge-base-export-2026-05-17/conversation-context-llm-knowledge-bases.md` | — | Inside KB archive |
| Closeout summary | `data/closeout-S-2026-05-17-knowledge-base-epistemic-export.md` | 6.3K | Git-tracked, pushed |

### Git State (corpvs-testamentvm)
- Branch: `main`, clean, in sync with `origin/main`
- Latest commit: `3c73cd3` (chore autogen refresh)
- 5 commits pushed this session

### Cloned Repos (shallow, depth=1)
- `a-organvm/my-knowledge-base` → `/Users/4jp/Workspace/a-organvm/my-knowledge-base`
- `organvm-i-theoria/linguistic-atomization-framework` → `/Users/4jp/Code/organvm-i-theoria/`
- `organvm-i-theoria/nexus--babel-alexandria` → `/Users/4jp/Code/organvm-i-theoria/`

## Completed Work

- [x] Exported session archive (811 plans, 906 project memories, 21,908 files total)
- [x] Exported knowledge base (1,463 .md files across 7 repos)
- [x] Designed Epistemic Engine 5-node architecture (Intake → Compiler → Workbench → Oracle/Factory → Maintainer)
- [x] Designed plugin ecosystem (3-layer: 4 meta-plugins + ~160 existing skills + gap-fillers)
- [x] Defined gain staging rules for plugin chain
- [x] Updated IRF with 5 items (2 completions, 3 new)
- [x] Created 3 GitHub issues (#353, #354, #355)
- [x] Claimed DONE-533, DONE-534
- [x] Executed hall-monitor closeout (all violations found and fixed)
- [x] Committed and pushed all work

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| 3-layer plugin architecture (meta-plugins + existing skills + gap-fillers) | ~160 skills already exist; build only the 4 orchestrators that don't exist yet |
| DIWS as Phase 0 substrate | Domain scaffolding must precede any session context or PDE work |
| Compressed tar.gz for exports | Disk at 52% (11GB free); exports too large for git, must be portable |
| Epistemic Engine = product, not scripts | User explicitly requested "incredible new product instead of a hacky collection of scripts" |
| Gain staging rules for plugin chain | Prevent context clipping and maintain truth fidelity across the chain |
| IRF canonical path = Code/organvm | `meta-organvm` path identified as vacuum (IRF-SYS-185 filed) |

## Critical Context

### Epistemic Engine Architecture (5 Nodes)
1. **Intake Node** — Web Clipper (browser extension normalizes web to Markdown) + Ingest Watcher (local daemon monitors raw/ directory)
2. **Compiler** — Incremental Indexing (LLM reads raw doc → summary → index card) + Ontology Mapping + Semantic Linking (autonomous backlinks)
3. **Workbench** — Obsidian as human-readable glass + Agentic CLI (commission research, not just search)
4. **Oracle & Factory** — Multi-Modal Output (Markdown essay, matplotlib chart, Marp slideshow) + Recursive Feedback Loop
5. **Maintainer** — Health Checks (contradictions, dead links, thin concepts) + Gap Imputation (web search to fill gaps)

### Plugin Ecosystem (4 Priority Meta-Plugins)
1. **session-orchestrator** — Master sequencer for Phase 0→3 chain
2. **vacuum-radar** — Real-time N/A detection during session
3. **triple-reference-tracker** — Enforce IRF+repo+GH issue during work
4. **atom-logger** — Log work units to prompt registry

### User Workflow (the product to build)
Raw data ingest → LLM-compiled wiki → Obsidian IDE → Q&A/output → recursive filing → autonomous linting. User rarely writes/edits manually; the LLM is the domain maintainer.

### Constraints
- macOS 26 ARM64, 16GB RAM — avoid parallel process spawning
- No LaunchAgents (HARD RULE) — on-demand CLI only
- Docker Desktop quit — native binary or Docker Compose only
- chezmoi governs dotfiles — fix bases, not outputs
- local:remote = 1:1 — nothing local only

## Next Actions

### P1 — Immediate (zero dependencies)
1. **IRF-THE-033:** Formalize Epistemic Engine product spec
   - Define MVP scope (which of 5 nodes first?)
   - Identify existing tools that map to each component
   - Write spec in `organvm-corpvs-testamentvm` or new repo

2. **IRF-SYS-184:** Implement 4 priority meta-plugins
   - Start with `session-orchestrator` (master sequencer)
   - Then `vacuum-radar` (real-time N/A detection)
   - Then `triple-reference-tracker` (enforce triple reference)
   - Then `atom-logger` (log to prompt registry)
   - Each should be an opencode skill or Claude Code skill

### P2 — Deferred (not blocked)
3. **IRF-SYS-185:** Fix IRF missing from meta-organvm
   - Decision needed: symlink vs copy vs document canonical location
   - Low effort, low urgency

### Ongoing — From Existing Active Handoff
4. **my-knowledge-base active-handoff.md** — Gemini theory work (T1–T10) still pending
   - T1: SOP Master Index
   - T2: UMFAS Monad Merge Decision
   - T3: Phase 5 Apple Notes Adapter
   - T4: Knowledge Graph Confidence Propagation
   - T5: Embedding Model Benchmark Expansion
   - T6: Theory-to-Concrete Handoff Governance
   - T7: Prompt Atomization Second-Pass Triage
   - T8–T10: Optional theory-substrate specs

## Risks & Warnings

- **Disk space:** 52% used (11GB free). Full 31GB report export blocked until external drive/cloud.
- **IRF vacuum:** IRF exists at `Code/organvm/organvm-corpvs-testamentvm/` but NOT at `meta-organvm/organvm-corpvs-testamentvm/`. Sessions operating from meta-organvm cannot access IRF.
- **Plugin design ≠ implementation:** The 4 meta-plugins are designed but not built. Next agent must not re-design; they must implement.
- **Epistemic Engine scope risk:** 5-node architecture is ambitious. MVP should be 1-2 nodes max.
- **16GB RAM constraint:** Max 4-6 concurrent agents. Do not spawn many parallel processes.
- **Shallow clones:** 3 repos cloned with depth=1. Full history not available locally.

## Conflict Zones

| Path | Rule |
|------|------|
| `INST-INDEX-RERUM-FACIENDARUM.md` | Read before write; never overwrite wholesale; append-only for new items |
| `data/done-id-counter.json` | Claim next ID atomically; increment after claim |
| `data/prompt-registry/prompt-atoms.json` | Targeted edits only; never replace wholesale |
| `.conductor/active-handoff.md` | Update, don't replace; preserve existing scope sections |

## Recovery Protocol

If next session finds state mismatch:
1. Check `git log` in corpvs-testamentvm for commits since `3c73cd3`
2. Verify archives still exist at `~/session-archive-2026-05-17.tar.gz` and `~/knowledge-base-export-2026-05-17.tar.gz`
3. Check GitHub issues #353, #354, #355 for any updates
4. Re-read IRF to confirm DONE-533, DONE-534 are logged

*— end envelope —*
---

## Addendum: 2026-05-21 — Four-Runtime Protocol Alignment (Claude session)

**Scope:** Orthogonal to the 2026-05-17 KB-export work above. Triggered by Codex SessionStart printout showing `NEON_API_KEY for MCP server 'Neon' is empty` and the user's reframe: "design ideal interactive ecosystem; not Claude only."

**Plans authored this session (both IN-PROGRESS, no DONE-NNN):**

| Plan | Path | Status |
|---|---|---|
| Four-runtime interactive ecosystem alignment | ~/.claude/plans/2026-05-21-four-runtime-interactive-ecosystem-alignment.md | IN-PROGRESS |
| Agent integration protocols past/present/potential | ~/.claude/plans/2026-05-21-agent-integration-protocols-past-present-potential.md | IN-PROGRESS |

**Key finding (the structural reframe):** Original three-layer plan (Secrets · MCP · Hooks) is incomplete. Honest decomposition is five layers: L1 Secrets, L2 Agent↔tool (MCP), L3 Hooks, L4 Editor↔agent (ACP — new), L5 Agent↔agent (A2A — new). Four runtimes participate in different subsets depending on driver/driven role.

**Files NOT modified:** INST-INDEX-RERUM-FACIENDARUM.md, prompt-atoms.json, registry-v2.json, this repo's working tree.

**Recovery for next session resuming this scope:**
1. Read four-runtime-interactive-ecosystem-alignment.md (the design).
2. Then agent-integration-protocols-past-present-potential.md (the research that reframed it).
3. User has NOT approved Phase 1 BUILD; do not implement until edge-priority decision is made.

*— end 2026-05-21 addendum —*

## Resolution received 2026-05-21 (supersedes prior "Phase 1 NOT approved" line above)

**Edge-priority answer (user, 2026-05-21):** All five layers — L1 Secrets · L2 MCP · L3 Hooks · L4 ACP · L5 A2A — are in scope, phased over multiple quarters. The three-of-four collapse from the closeout applies: Phase 0a (NEON_API_KEY injection trace), Phase 0e (per-runtime ACP audit), Phase 0f (conductor↔A2A reconciliation) are all UNFROZEN.

**Neon-fate answer (user, 2026-05-21, verbatim):** "notate, research all lanes, arrive at elevated plain" — do NOT collapse to vestigial (delete) or wanted (1Password wire) yet. Instead: document each runtime's current secret-handling, research per-lane mechanisms (Codex `bearer_token_env_var`, Claude's untraced injection, Gemini's settings.json, OpenCode's per-server env block), then synthesize at higher altitude. Phase 1a is gated on this research, not on a binary fix.

**What unfreezes for next session:** Phase 0 investigation (read-only; trace + audit + reconcile) plus the multi-lane Neon-handling notation. Phase 1 BUILD remains gated on the synthesis output, not on a fresh user decision.

*— end resolution block —*

---

# Agent Handoff: Hall-Monitor Cascade + Artifact Routing

**From:** Session 2026-05-22 Claude hall-monitor + artifact routing | **Date:** 2026-05-22 21:00 EDT | **Phase:** Complete (closeout executing)

## Current State

### Artifacts on Disk (this session's contributions)

| Artifact | Location | Status |
|---|---|---|
| docs/audits/2026-05-22-four-roots-private-bin-opt-usr.md | corpvs | Pushed `eba90cc` |
| docs/audits/2026-05-21-sysdiagnose/ (REPORT.md + findings/ + dispatch-envelopes/ + 4 companions) | corpvs | Pushed `eba90cc` |
| docs/governance/directory-taxonomy-touch-policy.html | corpvs | Pushed `eba90cc` |
| IRF-OPS-066 (routing precedent) + IRF-OPS-067 (additive correction) | corpvs/INST-INDEX-RERUM-FACIENDARUM.md | Pushed `8410240` |
| Memory: feedback_four_layer_classification_check.md | chezmoi-runtime + source | Pushed `c052f93` |
| Memory: feedback_reflog_as_hidden_actor_forensic.md | chezmoi-runtime + source | Pushed `7ab5066` |
| Memory: project_artifact_2026_05_22_outside_git_artifact_routing.md | chezmoi-runtime + source | Pushed `5d50695` |
| Memory: project_session_2026_05_22_hall_monitor_artifact_routing.md | chezmoi-runtime + source | Pushed `52887a4` |
| MEMORY.md index (4 new pointers added) | chezmoi-runtime + source | Pushed `f4f1411` |

### Git State

- corpvs: `main` at `8410240`, **1:1 parity** with origin
- domus-semper-palingenesis: `master` at `6534e1d+`, **1:1 parity** with origin (continued sibling auto-commits expected)
- a-i--skills: `main` at `3e6a249`, **1:1 parity** (untouched this session)

## Completed Work

- [x] Hall-monitor cascade audit across 3 load-bearing git repos
- [x] Identified 3 candidate Rule-#2 violations (routed to corpvs/docs/)
- [x] Discovered recursive own-violation of [[verification-precedes-classification]] (4 hrs old at time of violation)
- [x] Codified [[four-layer-classification-check]] amendment
- [x] Codified [[reflog-as-hidden-actor-forensic]] as forensic instrument for sibling-actor activity
- [x] Filed IRF-OPS-066 (precedent) + IRF-OPS-067 (additive correction)
- [x] Reconciled chezmoi drift caused by MOVE operations (converted to COPY + chezmoi add)
- [x] Two-layer preservation established for all 3 originally-flagged artifacts (chezmoi byte-mirror + corpvs governance home)

## Key Decisions

| Decision | Rationale |
|---|---|
| Move 2 files + symlink 1 back, copy sysdiagnose outputs | Symmetric "minimum access-pattern disruption" per artifact nature |
| Reconcile chezmoi drift via `chezmoi add` (not `chezmoi apply`) | Runtime version was user's latest editing; source should follow |
| Additive correction via IRF-OPS-067 (not edit OPS-066) | Honors [[feedback-additive-only-policy]] — corrections accumulate as new rows |
| docs/audits/YYYY-MM-DD-<topic>/ as new convention | docs/evaluation/ reserved for ongoing scoring; docs/audits/ for point-in-time inspections |
| 813 MB sysdiagnose raw bundle stays at ~/Workspace/_diagnostics/ | Git is wrong-medium for kernel evidence dumps; only narrative mirror at corpvs |

## Critical Context for Next Session

### The recursive-violation lesson is the meta-finding

[[feedback-verification-precedes-classification]] was authored at 15:20 today. By 19:45 the same session violated it. **A feedback memory's mere existence does not prevent its violation by the agent who authored it** — the verification step has to be operationalized into the *action protocol*, not left as a passive rule. IRF-OPS-067 + [[four-layer-classification-check]] operationalize this with a concrete four-bullet checklist.

### Four-layer Rule-#2 check (next session: use this)

Before classifying any file as "outside-git" / "Rule-#2 violating", check ALL four layers:
1. Direct `.git` ancestry (walk from file path upward)
2. `chezmoi managed | grep <file>` — chezmoi-source is its own pushed git repo
3. Sibling dotfile managers (yadm, dotbot, stow)
4. Per-tool config-sync surfaces (Codex `~/.codex/config.toml`, etc.)

Single-layer audit is the most common decay mode. Caught me this session.

### Pre-existing chezmoi drift NOT addressed (sibling-session territory)

- 7 DA: `.claude/plans/2026-04-22-*.md` (source has, runtime deleted)
- 1 DA: `seed.yaml` (intentional user trashing per IRF-OPS-040; restore would undo decision)
- 5 MM: settings.json, MEMORY.md, claude_desktop_config.json, FIND-010-posttooluse-sync-scope-gap.md
- 1 R: validate-no-hardcoded-paths.sh
- 1 M: GEMINI.md (runtime-only)

Surface for user / next session.

### Hook gap discovered

The PostToolUse `domus-memory-sync` hook fires on Write but NOT Edit. Sibling session already filed `reference_domus_memory_sync_modify_blind_spot.md` documenting. Workaround: after Edit on a memory file, manually run `chezmoi add <runtime-path>`.

## What's Locked / Not-Yet-Attempted

- The 470 OPEN IRF items (12 P0, 147 P1) — the broad vacuum field, untouched this session
- The 4 engine N/A vacuums (Edges/Tensions/Clusters=0, Δ24h/Δ7d=n/a, Inference=0%, sprint_names erased) — pre-existing, not addressed
- Per-file reconciliation of pre-existing chezmoi drift — requires per-file user decisions

## Pointers

- Closeout: `~/.Codex/plans/closeout-2026-05-22-hall-monitor-artifact-routing.md`
- Session memory: `[[2026-05-22-hall-monitor-artifact-routing]]`
- IRF rows shipped: IRF-OPS-066, IRF-OPS-067

---

## 2026-05-22 — Onslaught Synthesis + Hall-Monitor Cycle (session 704ff1f1)

**Closed via:** `~/.claude/plans/closeout-2026-05-22-onslaught-synthesis-hall-monitor.md`

**Substrate shipped:**
- Synthesis plan: `~/.claude/plans/2026-05-22-onslaught-collected-sibling-sessions.md` (25 clusters from 18 sibling close-outs)
- 14 IRF rows: OPS-070..079 + CRP-015..018 (corpvs `046a57f` → `8bd59cf`, row count 866 → 880)
- GH issue: #361 (14-checkbox tracking, V3 remediation per CLAUDE.md propagation requirement)
- 2 memory entries: `feedback_self_catch_synthesis_own_pattern.md`, `project_session_onslaught_sudoers_role.md`

**Hall-monitor outcome:** 3 violations (V1 sibling-stranded, V2 Edit→chezmoi-add asymmetry firing on own synthesis output, V3 GH-issue vacuum). All 3 remediated same-session. Self-catch rate 2/3 reflexive, 1/3 user-surfaced.

**N/A atomization:** 3 indices terminal-N/A with reason, 1 was a real vacuum (V3 GH issue, closed).

**Parity (per-repo):**
- domus chezmoi-source: `bc3907e` == origin/master, 1:1
- corpvs: `8bd59cf` == origin/main, 1:1

**What's locked / not-yet-attempted:**
- 4 first-wave executables named in synthesis (C8 rebase-merge rm, C9 INDEX regenerator, C10 hook deploy, C19 atuin orphan) — await new authorization
- P2 user-gated batch (CRP-015..018 + OPS-077) — needs user decision
- Codex/Gemini dispatch envelopes for IRF-OPS-074/075 — not generated this turn
- GH#361 14 checkboxes — close as individual IRF rows complete

**Next session pickup:** the synthesis is the lens; execution is downstream. Start at the first-wave executables list or surface the P2 batch for user decision.

---

## 2026-05-27 — Code Review → Generator Fixes → PR Backlog Triage (Claude session)

**Closed via:** `data/closeout-S-2026-05-27-code-review-pr-triage.md`

**What shipped to `main`:**
- **#364** (`97fc6fa`) — 8 fixes to pulse/dashboard generators (`system-pulse-generator.py`, `generate-dashboard.py`, `soak-test-monitor.py`) + regenerated artifacts. Fixes: hardcoded `/8` organ denominator → `total_organs`; CI breakdown now shows billing-locked (sums to total_checked); prototype-repo reconciliation; `n/a` instead of `?` for absent word/file metrics; clamped soak-day caption; palette cycling so all 10 organs render; metrics-driven Organs stat; META-ORGANVM added to registry validation.
- **#367** (`39c5d1e`) — shell-injection remediation in `promote-repo.yml` (all `${{ }}` moved out of run/script bodies into `env:`). Re-applied cleanly because **#278 had no merge base** with main.
- **#351** (`06a57b1`) — astro 5→6 (build verified green).

**In flight:**
- **#372** — GitHub Actions version bumps (github-script v8→v9, pages actions v4→v5, fetch-metadata v2→v3) re-applied cleanly because **#324 was corrupted** (stale May-1 base, committed `<<<<<<< HEAD` marker). Includes shellcheck cleanups (SC2129/SC2034) to satisfy the #370 actionlint guard. Awaiting actionlint re-run; merge when green.

**Closed without merge (superseded):** #278 → #367, #324 → #372.

**Key decisions:**
| Decision | Rationale |
|----------|-----------|
| Re-apply divergent branches rather than force-merge | #278/#324 had no merge base / committed conflict markers; clean re-apply on current main is the only safe path |
| Merge astro major on build-green | portfolio-site build is the real safety gate for a framework major |
| Clear shellcheck findings, don't weaken the actionlint guard | #370's guard is a deliberate shell-injection control |

**What's locked / not attempted:**
- 8 draft PRs (#356, #357, #358, #359, #360, #362, #363, #365) — other sessions' WIP; not merged/closed.
- #338, #335 — other workstreams.
- ~100+ open IRF/governance issues incl. DECISION items (#300, #301) — need the owner.

**Follow-up (discovered, NOT done):**
1. **Security (same class as #367):** `distribute-content.yml` still has inline `${{ steps.metadata.outputs.excerpt/issue_url }}` in a `run:` block (the `TITLE` vector was removed in #372). Move EXCERPT/ISSUE_URL to `env:` and audit remaining workflows.
2. `system-pulse-weekly.yml:39` SC2086 (info) — latent; surfaces on any PR touching that file.

**Next session pickup:** merge #372 when green; then the distribute-content.yml env-hardening follow-up; then the draft/issue backlog per owner direction.

*— end 2026-05-27 section —*
