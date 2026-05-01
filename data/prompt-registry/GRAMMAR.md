# Prompt Registry — Substrate Grammar

**Pairs with:** `INST-INDEX-PROMPTORUM.md` (this directory) — the auto-generated registry of every 4jp prompt (5,867+ prompts, 523+ sessions, dating to 2025-11-22, captured via SessionEnd hook at `~/.claude/hooks/session-prompt-capture.sh`).

**This file documents the macro→atom grammar that the registry serves.** The registry is what; this file is why and how. The registry is data; this file is the framework that makes the data legible — what to call a macro, how to decompose it, where atoms attach, which lenses derive, which surfaces render per audience.

**Parallel:** `INST-INDEX-RERUM-FACIENDARUM` (engineering work) and per-project `atomized-wants` documents (client/collaborator asks). Together those three are the same substrate viewed through different lenses.

**Seeded:** 2026-05-01, in response to the directive: "everything client asks (1 source containing macro dreams broken into layer upon layer below until a single unit defined) i prompt (1 source containing macro dreams broken into layer upon layer below until a single unit defined) is created and tracked against concrete iterations constantly tracking diff and spread."
**Purpose:** Name the substrate philosophy, the lens grammar, the audience-specific surfaces, and the diff/spread measurement intent that the existing automated registry implements but does not articulate.
**Scope:** Cross-repo. 4jp prompts span every organ + every project. This grammar applies universally; the registry collects universally.

---

## The substrate

Every input to the work has the same recursive shape:

```
MACRO DREAM
├── LAYER (named decomposition axis)
│   ├── LAYER
│   │   ├── ...
│   │   └── ATOM (single defined unit, testable, completable)
│   └── ATOM
└── LAYER → ATOM
```

A macro is decomposed until each leaf is an atom — small enough to verify, complete, or close in one motion. Atoms map outward to commits, renders, deployments. Two quantities are continuously measured:

- **DIFF** — the gap between an atom's intent and the rendered reality. The atom says X; what's deployed is Y; the diff is the delta.
- **SPREAD** — how a single macro fans out across many atoms across many files / commits / surfaces. Spread is the system's footprint of one dream.

The substrate is one. The views are many. Lenses derive views; the substrate stays canonical.

## Lenses

Four primary lenses generate views over the same substrate:

| Lens | Question answered | Derivation rule |
|---|---|---|
| **Was** | What were the atoms 4jp prompted on between dates X and Y? | Filter primary sources by date; group by macro lineage |
| **Is** | What's the live state of every atom? Which are claimed-done vs actually-rendered? | Cross-reference atom IDs against `git log` and deployed surfaces; compute diff |
| **Will** | What atoms are next, given current macro pressure? | Projected from open atoms × current pace × spread coefficient |
| **Should** | What atoms *ought* to exist that don't, given the macro? | Diff between decomposition completeness and atom inventory |

## Audiences and surfaces

Visual surfaces derive from the substrate per audience. Each surface filters and renders the substrate for one reader:

| Audience | Surface | What it foregrounds |
|---|---|---|
| 4jp (self) | full canonical view | every macro, every atom, all four lenses, raw diff + spread numbers |
| Maddie (or any client) | client-scoped subset | only atoms touching her stream; what's live vs pending; her open asks |
| Sub-agents | task-scoped slice | the macro + ancestor layers + sibling atoms relevant to the dispatched scope |
| Future selves | trajectory view | macro evolution over time; how a dream got refined; what was dropped and why |
| External advisor / verifier | evidence-anchored | every atom paired with its primary-source citation + verification status |

Surfaces are render-time artifacts. They don't replicate the substrate; they read from it.

## Primary sources

The raw substrate already lives in collected form. This index does not re-extract — it references.

| Source | Location | Collection cadence | Owner |
|---|---|---|---|
| Claude Code session prompts | `~/.claude/sessions/{YYYY-MM-DD--slug}/prompts.md` | per session, automatic | Claude Code runtime |
| Claude Code transcripts (full) | `~/.claude/sessions/{YYYY-MM-DD--slug}/transcript.md` | per session, automatic | Claude Code runtime |
| Codex CLI session exports | per-repo `.specstory/history/*.md` | per Codex session, automatic | SpecStory |
| Weekly assessed prompt corpus | `meta-organvm/organvm-corpvs-testamentvm/data/corpora/week-{YYYY-MM-DD}_to_{YYYY-MM-DD}/prompts-{raw,assessed}.jsonl` | weekly, manual via `organvm prompts narrate` | 4jp |
| Granular debug captures | `.specstory/debug/{uuid}/*.json` | per session, automatic | SpecStory |
| Per-session JSONL event stream | `~/.claude/sessions/{YYYY-MM-DD--slug}/session.jsonl` | per session, automatic | Claude Code runtime |

The sources are distributed but complete. The directive is not "collect more" — it is "decompose what's collected, render lenses."

## Tooling already in place

`organvm` CLI subcommands that operate on this substrate:

| Command | Operation |
|---|---|
| `organvm prompts narrate` | Extract, classify, and thread prompts into narrative arcs |
| `organvm prompts clipboard` | Extract from Paste.app clipboard history |
| `organvm prompts audit` | Pipeline data audit (noise, completion, linking quality) |
| `organvm prompts distill` | Distill clipboard prompts into operational patterns + SOP coverage |
| `organvm atoms link` | Link atomized tasks to annotated prompts by content similarity |
| `organvm atoms pipeline` | Full atomization (atomize → narrate → link → index) |
| `organvm atoms reconcile` | Cross-reference atoms against git history to detect completed work |
| `organvm atoms fanout` | Fan out atom data to per-organ rollup JSON |
| `organvm irf list` | Engineering work registry by priority |

The directive aligns these into one substrate-with-lenses view. No new core tooling required for the seed; new tooling needed for **per-audience visual surfaces** (deferred — design before code).

## Macro entry format

```markdown
### M-XXX: <macro title>

**Stated:** <YYYY-MM-DD> <where stated — session ID, commit, doc>
**Surface intent:** <one-line goal>
**Status:** <conceiving | decomposing | atomizing | partly-iterated | resolved | abandoned>

#### Layers
- **L1.** <decomposition axis name>
  - **L2.** <sub-axis>
    - **A-XXX.NN** <atom — testable single unit> → <iteration anchor: commit hash | doc path | session ID | "pending">

#### Iterations
| Date | Type | Anchor | Diff observed |
|---|---|---|---|
| ... | commit | <hash> | <atom intent vs rendered delta> |
| ... | doc | <path> | ... |

#### Spread
- Files touched: <count>
- Commits to date: <count>
- Surfaces affected: <list>
- Macro fan-out coefficient: <atoms / commits>
```

## Seed entries

### M-001: Build the Sovereign Systems Spiral artifact

**Stated:** 2026-04-01 in `sovereign-systems--elevate-align/docs/handoff-maddie-spiral-path-2026-04-01.md` (intake handoff). Reinforced across ~30 days of iteration.
**Surface intent:** A 13-node 3D spiral that reads as Maddie's brand identity at first glance and routes visitors to her four pillars on click.
**Status:** partly-iterated (Round 7 in progress as of 2026-05-01)

**Layers (sketch — fuller decomposition deferred to follow-up session):**
- L1. Architecture (node count, phases, data shape)
  - A-001.01 13-node lock-in → commit `9ded399` (2026-04-04)
  - A-001.02 Phase-pillar mapping → commit `a2553ce` (2026-04-20)
- L1. Geometry (3D shape, motion, dimensionality)
  - A-001.03 Three.js helix realignment → commit `7fb3308` (2026-04-21)
  - A-001.04 Per-node sacred symbol geometry → commit `b8d105b` (2026-04-25)
  - A-001.05 Sacred-geometry-primitives wiring (procedural per-node) → pending (Track A3 in plan)
- L1. Color (palette, contrast, identity per node)
  - A-001.06 Chakra spectrum interpolation → commit `02c90a2` (2026-04-25)
  - A-001.07 Chakra-default + hybrid vessel ship → commit `070b98d` (2026-04-30)
- L1. Vessel mode (mesh × particle blend)
  - A-001.08 Four-mode A/B (invisible/visible/refracted-star/hybrid) → commit `9baed08` (2026-04-29)
  - A-001.09 Hybrid particle opacity tune (Track A1) → commit `251f698` (2026-05-01)

**Iterations:** 56 spiral-relevant commits Apr 19 → May 1. Full timeline at `sovereign-systems--elevate-align/docs/timelines/2026-05-01-spiral-evolution-timeline.md`.

**Spread:** ~10 files in `src/components/spiral/` + `src/data/`; 56 commits; 4 visual modes; 13 procedural geometries; cross-references to atomized-wants W-005, W-006, W-066.

### M-002: Establish substrate / lens / surface pattern

**Stated:** 2026-05-01 in this Claude Code session. The directive that produced this very file.
**Surface intent:** Every prompt 4jp authors flows into a canonical substrate; views derive via lenses; visual surfaces render per audience; diff and spread measure continuously.
**Status:** conceiving (this seed is the first artifact)

**Layers:**
- L1. Substrate definition
  - A-002.01 Name the substrate, its philosophy, lens grammar → this file
  - A-002.02 Catalogue primary sources → this file (table above)
  - A-002.03 Catalogue existing tooling → this file (table above)
- L1. Decomposition format
  - A-002.04 Macro entry template → this file
  - A-002.05 Atom ID scheme + iteration anchor types → A-NNN.NN scheme defined; anchor types listed
- L1. Lenses
  - A-002.06 Was / Is / Will / Should derivation rules → defined above
- L1. Audiences and surfaces
  - A-002.07 Surface inventory per audience → defined above
  - A-002.08 Surface implementations (visual artifacts) → pending
- L1. Diff and spread
  - A-002.09 Measurement cadence (on-demand CLI / hook / session-end) → pending wiring
  - A-002.10 Threshold definitions for "drift" → pending

**Iterations:** seed only.

**Spread:** 1 file (this one). To be extended.

### M-003: Migrate Maddie's water funnel from snapshot to canonical surface

**Stated:** 2026-05-01 mid-session via universal mandates M1 (multi-citation) and M2 (no hardcoded dynamic data) plus today's bottle-pricing + bottled-water-education + fluoride-bug asks.
**Surface intent:** Every dynamic value in the water funnel (prices, contaminant thresholds, affiliate URLs, brand claims) lives in external config with cited provenance.
**Status:** decomposing

**Layers (high-level):**
- L1. Externalize dynamic data (M2)
  - A-003.01 BottledWaterCost array → JSON config (Track B)
  - A-003.02 FilterTier priceRange + affiliateUrl → JSON config (Track B + E merged)
  - A-003.03 EWG contaminant→effects map → JSON config or KV (deferred)
- L1. Citation discipline (M1)
  - A-003.04 Bottled-water claims (pH, sodium, cost) → ≥2 sources per claim (Track C)
  - A-003.05 Fluoride filter recommendation → ≥2 sources
  - A-003.06 Existing claims audit → backlog
- L1. EWG fluoride coverage (W-069)
  - A-003.07 Three-state data-source banner → commit `c778f48` (2026-05-01)
  - A-003.08 Fluoride in client fallback → commit `c778f48` (2026-05-01)
  - A-003.09 Route migration `functions/` → `src/pages/api/` → held on Maddie's badge state
  - A-003.10 "Common contaminants checked but not detected" sub-list → held on Maddie evidence

**Iterations:** 2 commits to date (today).
**Spread:** `src/data/hydration.config.ts`, `src/components/HydrationNode.astro`, `functions/api/water-report.ts`, `src/content/branches/`, `src/data/citations.ts` — 5+ files projected.

## Maintenance

| Cadence | What runs | What it produces |
|---|---|---|
| Per session | `~/.claude/sessions/{...}/prompts.md` written automatically | Raw 4jp prompts for that session |
| Per Codex session | `.specstory/history/*.md` written automatically | Raw 4jp prompts in repo context |
| Weekly | `organvm prompts narrate` | Threaded narrative arcs across the week |
| Weekly | `organvm prompts audit` | Pipeline health (noise, linking quality) |
| Weekly | `organvm prompts distill` | Operational patterns + SOP coverage |
| Per session-end | `organvm session review --latest` | Session summary, plan cross-ref |
| On-demand | `organvm atoms reconcile` | Atom claims vs git history |
| On-demand | `organvm atoms fanout` | Per-organ rollup of atoms |
| On macro stated | Hand-add macro entry to this file | New M-NNN root + initial layer sketch |
| On atom completed | Hand-update iteration anchor in this file | Atom moves from `pending` → commit hash |

## Cross-references

- `INST-INDEX-RERUM-FACIENDARUM.md` — engineering work registry. Atoms in this index that produce engineering work cross-reference IRF IDs (e.g., `IRF-OPS-017`).
- `INST-INDEX-LOCORUM.md` — canonical map of system locations.
- `INST-INDEX-NOMINUM.md` — registry of names.
- Per-project `atomized-wants` documents (e.g., `sovereign-systems--elevate-align/docs/client-decisions/2026-04-17-atomized-wants.md`) — client/collaborator asks. W-IDs in those docs cross-reference atoms here when the work is 4jp-driven decomposition of a client want.
- `IRF-V3-SPEC.md` — spec for the IRF schema; the macro-entry format above is informed by this lineage.
- `ONTOLOGY-V2-SKETCH.md` — workspace ontology sketch.

## Open questions for next session

1. **Atom ID collision policy.** Currently A-NNN.NN with macro-prefix scoping. Cross-macro ID space needs governance to prevent collisions when multiple macros decompose into the same atom (a single atom can be a leaf of two macros).
2. **Visual surfaces.** Per-audience renders are stated above but not built. The mandate says "visual representations, one for each audience of interest." Surface-construction tooling is the gap to fill next.
3. **Diff/spread cadence wiring.** The cadence table is aspirational; PreToolUse / PostToolUse hooks haven't been wired. The user's "all above" answer suggests CLI + hook + session-end + visual together — that's a multi-step build.
4. **Substrate-rolled-up view.** The user's "all above" for location implies per-project + workspace-meta + rolled-up. Per-project echoes already exist (Claude Code session prompts.md); workspace-meta is this file; the rolled-up view (substrate-of-substrates) is unmodeled.

## Status

This file is a SEED. The substrate philosophy is named. Three macros are sketched. Lenses, audiences, sources, tooling, format, cross-references are documented. What's missing is the steady-state extension cadence and the visual surfaces. Both are to be built incrementally; this file is the canonical entry point that names the system.
