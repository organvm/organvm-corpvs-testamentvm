# Handoff Envelope — Stream Σ: DIWS Substrate Skill Build

**Target agent:** Codex
**Source agent:** Claude Opus 4.7 (1M context)
**Plan:** `~/.claude/plans/okay-so-now-harmonic-kettle.md` (Stream Σ)
**Status:** READY FOR DISPATCH (manual; conductor_fleet MCP not available in originating session)
**Created:** 2026-04-25

## Scope

Build the **Domain-Ideal-Whole Substrate (DIWS)** skill from existing plan v2.2. This is mechanical scaffolding work from a fully-designed spec — Codex's lane.

The skill is the **gating dependency** for the entire portfolio-unification workstream (parent plan). Without it: Stream Synthesis (n-way combinations doc) cannot run; Stream Ω cannot use the gap-map operator; PDE cannot ingest a domain substrate.

## Source spec (read FIRST, do NOT modify)

`~/.claude/plans/2026-04-25-domain-ideal-whole-substrate-design.md`

This plan is v2.2 (additive versioning). Read it in full. Its invariants govern your build.

## Build targets

Under `~/Workspace/a-i--skills/skills/project-management/domain-ideal-whole-substrate/`:

### Top-level
- `SKILL.md` — main contract (1 file, ~300-500 lines)
  - Front-matter: name / description / when-to-use / invariants
  - 8 strata named with their canonical questions/outputs
  - 4 operators named with their fire-conditions
  - Phase 0 + Phase 0.5 protocol
  - 5-phase use protocol (load → instantiate → operate → audit → contribute)
  - Cross-references to PDE + MSP

### references/
- `8-strata-spec.md` — ontology / lineage / constellation / gap-map / agent-fleet / production-stack / internal-magnet / external-contribution (one section per stratum, ~100-200 lines each)
- `4-operators-spec.md` — selfish-altruistic loop / magnetic membrane / portfolio operator (v2 + v2.1) / reflexive operator (v2.2)
- `portfolio-composition-map.md` — v3 deepening, cross-flow matrix per pair/triple/quad combination
- `diws-msp-mapping.md` — isomorphism between DIWS strata and MSP synthesis primitives (oscillator/filter/modulator)

### scripts/
- `audit-portfolio.sh` — Phase 0; globs `~/Workspace/` for engines, classifies into 3-tier taxonomy (domain-engines / meta-engines / consultant-engines), outputs `portfolio-reuse-map.md` to caller's CWD
- `portfolio-gap-audit.sh` — **the stretching rack**; Phase 0.5; runs gap-map operator across all DIWS instances simultaneously; outputs holes/fat report

### assets/
- `domain-ontology-template.md` — stratum 1 template
- `domain-lineage-template.md` — stratum 2 template
- `domain-constellation-template.yaml` — stratum 3 template (75-person constellation file format; copy schema from `~/Workspace/organvm/organvm-corpvs-testamentvm/docs/portfolio/parameter-matrix.md` for field shape)
- `domain-gap-map-template.md` — stratum 4 template
- `domain-agent-fleet-template.yaml` — stratum 5 template
- `domain-production-stack-template.md` — stratum 6 template
- `domain-attractor-template.md` — stratum 7 template
- `domain-contribution-charter-template.md` — stratum 8 template

### proof-instances/
- `chess/` — partial fill demonstrating chess domain (use Hokage Chess artifacts as input source: `~/Workspace/4444J99/hokage-chess/`)
- `wellness/` — partial fill (use Maddie/Elevate Align artifacts: `~/Workspace/<spiral-repo>/`)
- `education/` — partial fill (Jessica stub: `~/.claude/projects/-Users-[user]/memory/collaborator_jessica.md` is the only source; mark fields UNKNOWN per stub-fidelity)
- `voodoo/` — outlier validator (loads stratum 8 heavily); design-only, no real client

## Reused utilities (DO NOT REIMPLEMENT)

- `~/Workspace/a-i--skills/skills/project-management/product-domain-engine/scripts/domain-audit.sh` — DIWS Phase 0.5 calls this internally; do not duplicate audit logic
- `~/Workspace/a-i--skills/skills/creative/modular-synthesis-philosophy/SKILL.md` — DIWS references for cross-portfolio routing; mention but don't restate
- 75-person Constellation file format from `project_artifact_cross_pollination_master_diagnosis.md` — reuse field shape

## Constraints (HARD RULES)

- **Universal rule #2** — every artifact git-tracked AND pushed before stream closes
- **Universal rule #3** — plan v2.2 is sculpture; never overwrite. If you discover something requiring spec change, write `2026-04-25-domain-ideal-whole-substrate-design-v3.md` and reference v2.2; never edit v2.2
- **Universal rule #17** — no stubs, placeholders, TODOs, partial code; every file must be complete on first commit
- **Constitutional axiom #22** — triple-check before closing; never claim DONE without 2+ evidence sources
- **No LaunchAgents** (rule #55) — `audit-portfolio.sh` and `portfolio-gap-audit.sh` are on-demand only; no plist generation, no timer-based automation
- **No backwards compat** — DIWS is a NEW skill; do not add migration/compatibility code
- **Stranger test gate** — a fresh agent (no prior context) must be able to read SKILL.md alone and load the chess/wellness/education proof instances without needing references/ files

## Cross-verify protocol

When this work returns to Claude, the following MUST hold:

1. `SKILL.md` exists at the target path with valid front-matter
2. All 8 stratum templates exist in assets/ (one per stratum)
3. `scripts/audit-portfolio.sh` runs end-to-end via `bash audit-portfolio.sh` and produces a non-empty `portfolio-reuse-map.md` in CWD
4. `scripts/portfolio-gap-audit.sh` runs against the 4 active DIWS proof-instances (chess / wellness / education / voodoo) and produces a holes/fat report with ≥1 entry per axis per instance
5. Git commit + push to `~/Workspace/a-i--skills/` with message starting `feat(diws):`
6. Stranger test passes: a fresh Claude session reads SKILL.md and correctly identifies the 4 operators + 8 strata without prior plan context

If ANY of these fail: Claude will run `cross_verify` and request specific fixes before clearing the handoff.

## Out-of-scope (do NOT do)

- Do not build the synthesis layer (`portfolio-synthesis.md`) — that's a separate Claude-owned stream
- Do not write the 5 organvm CLIs (sessions audit, subatomic decompose, etc.) — that's Stream Τ's lane (separate envelope)
- Do not modify PDE skill or MSP skill — read-only references
- Do not modify `INST-INDEX-RERUM-FACIENDARUM.md` — IRF rows for this stream's outputs are added by Claude on cross-verify

## On completion

When all targets exist + cross-verify passes:
1. Write a session memory at `~/.claude/projects/-Users-[user]/memory/project_session_<id>_diws_skill_build.md` summarizing artifacts shipped
2. Add to `MEMORY.md` Active Artifacts: `[DIWS substrate skill]` entry
3. Notify Claude session by leaving handoff-completion marker at `~/Workspace/organvm/organvm-corpvs-testamentvm/docs/agents/2026-04-25-stream-sigma-COMPLETED.md` with commit SHA(s)

## Source plan

This envelope is generated from parent plan: `~/.claude/plans/okay-so-now-harmonic-kettle.md` (Stream Σ, lines under "D.2 Stream Σ — DIWS Substrate Skill Build").
