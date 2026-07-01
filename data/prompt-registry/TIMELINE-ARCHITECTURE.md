# Timeline-Rooted Prompt Graph — Architecture

**Created:** 2026-05-05
**Origin:** User directive — *"Every prompt needs to be put on a timeline. Each prompt's atomic unit within needs mapping on multi-directions and possibilities. Then, tracked with what's currently implemented in another pillar, and then an ideal form of what it should be."*
**Status:** Seed structure built (Pipeline B); data-layer addition needed for praxis branches; viewer functional

---

## The architecture

```
TIMELINE (root, chronological τ-axis)
  │
  └─ PROMPT (inception event at τ=0)
       │  - timestamp, session_id, thread_id, agent
       │  - prompt_text (the inception)
       │
       └─ ATOMIC UNIT (σ=1 decomposition — task derived from prompt)
            │  - task_id, title, status, type
            │  - project_organ, project_repo, tags
            │
            ├─→ PRAXIS branches (multi-directional possibilities)
            │     - alternative realizations / branches not yet committed
            │     - currently EMPTY in data — field needs adding
            │
            ├─→ PRAGMA pointers (current implementation)
            │     - shared_refs: file paths in repos
            │     - shared_tags: technology/concept tags
            │     - jaccard: similarity score
            │
            └─→ TELOS pointer (ideal form)
                  - form_id, label
                  - completeness, materialization counts
                  - verified_done / answered / total facets
```

In substrate vocabulary: this is a slice across the **τ-axis** (time) of the **(POV-tetrad × σ-axis)** chart from `~/.claude/CLAUDE.md`. The prompt is the **inception event** at the σ=0 / τ=0 origin; the atomic unit is the σ=1 decomposition; the three gravitational pillars are the **POV-tetrad legs** (telos / pragma / praxis), with **receptio** (reception/feedback) closing the loop in user follow-up.

---

## Substrates that compose into the architecture

The data already exists (Pipeline B in `data/atoms/`):

| File | Records | Role |
|---|---:|---|
| `data/atoms/annotated-prompts.jsonl` | 4,247 | Prompts (inception events) — Claude only |
| `data/atoms/prompt-atoms.jsonl` | 11,980 | Multi-source prompts (ChatGPT, Claude, etc.) — wider time range, back to 2022 |
| `data/atoms/atomized-tasks.jsonl` | 10,647 | Tasks (atomic units) decomposed from plans |
| `data/atoms/atom-links.jsonl` | 16,239 | task ↔ prompt linkages with Jaccard + shared file refs |
| `data/atoms/ideal-forms.jsonl` | 515 | Ideal forms (telos pillar) with materialization counts |
| `data/atoms/form-gap-analysis.jsonl` | 10 | Top-form materialization evidence (file paths in repos) |
| `data/atoms/intention-trajectories.jsonl` | 113 | Trajectory clusters (theme over time) |

The connective tissue: `atom-links.jsonl` already encodes pragma pointers (file references) and similarity scores. `ideal-forms.jsonl` already encodes telos data. **What was missing was the timeline-rooted assembly that pulls them into one queryable structure.**

---

## The two pipelines (and why they don't join cleanly)

The system has *two parallel atom registries*:

**Pipeline A (`prompt-atoms.json`, 73 MB, 24,599 atoms)** — uses `ATM-NNNNNN` / `PRM-NNNNN` IDs. This is the canonical atom registry used by INSIGHTS-FULL-HISTORY-2026-05-05.md. Time range: 2025-11 → 2026-04.

**Pipeline B (`data/atoms/*.jsonl`, multiple files)** — uses hex-hash IDs (`task_id: 045e4d521c4d`, `prompt_id: 359b00a22c67`). Has Jaccard linkages, multi-source prompts, ideal-forms, and goes back to 2022.

The two pipelines do not have a foreign-key bridge today. They are parallel views of the same underlying corpus, computed differently. The current `timeline-graph.py` build uses Pipeline B because Pipeline B has the linkage data already computed.

**Open question for the architect:** unify under one identity scheme, or keep both and add a translation layer?

---

## Build & view tooling

The seed implementation is at `scripts/timeline-graph.py`:

```bash
# Assemble the timeline-graph
python3 scripts/timeline-graph.py build
#   → writes data/prompt-registry/timeline-graph.jsonl

# View the most recent 20 prompts (with at least one linked task)
python3 scripts/timeline-graph.py view

# View a specific prompt by ID prefix
python3 scripts/timeline-graph.py view --prompt-id f1effca7

# View prompts since a date
python3 scripts/timeline-graph.py view --since 2026-04-01 --limit 50
```

The viewer renders each prompt as a markdown record with:
- Timeline anchor (timestamp)
- Inception (prompt text excerpt)
- Atomic units (each linked task)
- For each atomic unit: PRAGMA, TELOS, PRAXIS sections

---

## Coverage status (as of 2026-05-05)

| Layer | Coverage | Notes |
|---|---:|---|
| Prompts on timeline | 4,247 | from annotated-prompts.jsonl |
| Prompts with linked tasks | 280 (6.6%) | atom-links coverage is sparse |
| Tasks with PRAGMA file refs | 92 (0.6%) | most links share tags but not file refs |
| Tasks with TELOS pointer | 234 (1.4%) | conservative tag-overlap matching |
| Tasks with PRAXIS branches | 0 (0%) | data-layer field doesn't exist yet |

Coverage is sparse because:
1. Most atom-links have shared *tags* (`python`, `mcp`, `astro`) but not shared *file refs* (specific paths). The pragma pointer becomes a tag-pointer rather than a file-pointer.
2. Telos matching is one-direction-only (task→form via tag overlap). Bidirectional matching with form-keyword expansion would raise this substantially.
3. Praxis branches require generating *alternative realizations* per task. This is an LLM-synthesis task, not a data-layer derivation.

---

## What "complete" looks like

The architecture is fully realized when:

1. **Identity-bridging**: Pipeline A (`ATM-NNNNNN`) ↔ Pipeline B (`task_id` hash) have a translation table. One query returns the same atom regardless of identity scheme used.
2. **Pragma coverage > 50%**: most tasks have at least one shared file reference (not just shared tags). Achieved by either (a) widening the linkage threshold, or (b) re-computing atom-links with stricter file-anchored similarity.
3. **Telos coverage > 80%**: most tasks map to at least one ideal form. Achieved by switching from tag-overlap to embedding-similarity matching against form labels.
4. **Praxis branches present**: each task has 1-5 alternative-realization branches. Achieved by an LLM pass that, for each task, proposes branches based on the task description + the broader context.
5. **Receptio loop closed**: when a task is materialized, the materialization-evidence is recorded as a backlink (form-gap-analysis style) so future queries see "this prompt produced X via path Y".

---

## Recommended next moves

In priority order:

1. **Run `python3 scripts/timeline-graph.py build`** to produce the seed `timeline-graph.jsonl`. Spot-check it.
2. **Add a `praxis_branches` field to atomized-tasks.jsonl** as an empty list. Set up an LLM-pass routine that fills it in for top-priority tasks.
3. **Build the identity bridge between Pipeline A and Pipeline B.** Without this, ATM atoms don't appear in the timeline, even though they're the canonical registry.
4. **Migrate to embedding-based telos matching** to raise telos-pointer coverage from 1.4% to 80%+.
5. **Rendering surface**: extend the viewer to produce a static HTML timeline (one page per month, each prompt as an expandable card showing its three pillars). The markdown viewer is functional; HTML would be discoverable.

---

## Cross-references

- `docs/evaluation/SELF-REVIEW-MASTER-2026-05-05.md` — Self-review master synthesis (Pathology 1: traceability broken)
- `docs/evaluation/INSIGHTS-FULL-HISTORY-2026-05-05.md` — Aggregate longitudinal report
- `~/.claude/CLAUDE.md` — substrate vocabulary anchor (POV-tetrad, σ-axis, τ-axis)
- `scripts/timeline-graph.py` — implementation
