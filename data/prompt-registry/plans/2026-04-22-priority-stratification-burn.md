# Maximum Throughput Burn Session

**Date:** 2026-04-22 (continued)
**Context:** Priority stratification DONE. 7-dimension scoring engine built. 17,855 OPEN atoms surfaced. Similarity + verification engines built. Root causes fixed. Now: burn through the backlog at maximum throughput. User has ~40% CloudMax capacity remaining before morning reset — use it ALL.

## Completed This Session
- prioritize_atoms.py (7 dimensions including repetition)
- reopen_atoms.py, verify_done.py, similarity_engine.py, vacuum_radiation.py
- measure_implementation.py root cause fix (evidence recording)
- Corpus: 17,855 OPEN, 4,246 DONE, 2,498 CLOSED

## Burn Plan — Parallel Execution

### Stream 1: Fix agent-dispatch and re-fire fleet
- Fix Codex dispatch (needs `--skip-git-repo-check` or trusted dir)
- Fix Gemini dispatch (argument format issue)
- Fire top 5 Codex + top 10 Gemini items with corrected args

### Stream 2: Run measurement pipeline with evidence recording
- Re-run `measure_implementation.py` (now records evidence in `produced`)
- This will close atoms with git/IRF/GitHub evidence AND record WHY
- Then re-run prioritize + generate_work_queue + route

### Stream 3: Burn P0 OPEN atoms directly
- Work through the 88 P0 atoms
- For each: do the work, close the atom, generate vacuum atoms
- Focus on Claude-strategic items (governance rules, architecture)

### Stream 4: User's 3 priority items
- ATM-024599: Essay publication audit and restart
- ATM-024598: Captain's log reconstruction
- ATM-024597: Portfolio/client website unity analysis

### Stream 5: Deduplication pass
- The 2,658 copy groups (9,932 atoms) need canonical selection
- Build a dedup pass that keeps the most complete version of each group
- Close redundant copies → reduces OPEN count meaningfully

## Verification
- After each stream: re-run `python3 prioritize_atoms.py && python3 generate_work_queue.py`
- Track OPEN count reduction
- Commit every 30-45 minutes

**Repo:** `~/Workspace/organvm/organvm-corpvs-testamentvm/data/prompt-registry/`

---

## Phase 1: Build `prioritize_atoms.py`

New script that scores all 24,596 atoms on 6 dimensions, writes `priority` (P0-P3) and `priority_score` (0.0-1.0) back into `prompt-atoms.json`.

### Scoring Dimensions

| Dimension | Weight | Signal | Source |
|-----------|--------|--------|--------|
| Recency | 0.15 | Exponential decay: `exp(-days_old / 45)` | `atom.date` |
| Type urgency | 0.25 | correction=1.0, governance-rule=0.8, constraint=0.7, question=0.6, directive=0.5, implicit-signal=0.3, emotional/data/command=0.1 | `atom.type` |
| Universe criticality | 0.20 | security=1.0, personal=0.9, UNIVERSAL=0.8, meta=0.7, organ-iv=0.6, organ-i/ii/iii=0.5, unscoped=0.3 | `atom.universes` |
| Content specificity | 0.15 | File paths, repo names, tool names, command presence; penalize vague language | `atom.content` |
| Cross-reference density | 0.10 | Inverted keyword index — how many other atoms share keywords with this one | Computed corpus-wide |
| Completion trajectory | 0.15 | Universe completion rate: boost last-mile items (>60% DONE), boost neglected universes (<20% DONE) | Computed corpus-wide |

### P-Level Mapping

```
score >= 0.70 → P0 (critical — act now)
score >= 0.50 → P1 (high — this session or next)
score >= 0.30 → P2 (medium — this week)
score <  0.30 → P3 (low — backlog)
```

### Implementation

**File:** `data/prompt-registry/prioritize_atoms.py`

```
1. Load prompt-atoms.json (all 24,596 atoms)
2. Compute corpus-wide aggregates:
   a. Universe completion rates (% DONE per universe)
   b. Inverted keyword index (keyword → set of atom_ids)
   c. Cross-reference counts per atom
3. Score each atom:
   a. Recency: exp(-days_old / 45)
   b. Type urgency: lookup table
   c. Universe criticality: max(criticality for each universe)
   d. Content specificity: regex-based feature detection
   e. Cross-reference density: normalized count from inverted index
   f. Completion trajectory: boost function based on universe completion rate
   g. Composite: weighted sum → priority_score (0.0-1.0)
   h. Map to P0-P3
4. Write priority + priority_score back into each atom in prompt-atoms.json
5. Print distribution: how many P0, P1, P2, P3 per status (DONE/OPEN/CLOSED-*)
```

**Keyword extraction:** Reuse the domain-filtered approach from `measure_implementation.py` — strip stopwords, lowercase, split on non-alpha. Already proven on this corpus.

**Performance:** 24,596 atoms, inverted index is O(n*k) where k = avg keywords per atom (~20). Cross-reference density is O(n*k) via index lookup. Total: <10 seconds.

### Modifications to Existing Scripts

**`generate_work_queue.py`** — Replace `parse_priority()` (lines 20-45):
- Read `priority` field from atom (computed by prioritize_atoms.py)
- Fall back to old type-based mapping if `priority` field is absent
- Sort by `priority` then `priority_score` descending within each P-level

**`route_atoms.py`** — Add priority to dispatch output:
- Include `priority` and `priority_score` in each dispatched atom
- Sort within each target by priority (P0 first)

**`open-atoms-cache.json`** — Add `priority_score` field alongside existing `priority` field.

---

## Phase 2: Dispatch Fleet

After prioritization runs, fire Codex and Gemini atoms:

1. Re-run `generate_work_queue.py` and `route_atoms.py` with new priorities
2. Read the 8 Codex items and 21 Gemini items from `dispatch-queue.json`
3. Fire via `agent-dispatch` CLI (parallel — all at once)

---

## Phase 3: Burn Top-Priority OPEN Atoms

With the queue sorted by real priority:

1. Pull the top P0/P1 OPEN atoms
2. Work through Claude-strategic items directly
3. After completing work, run measurement pipeline:
   ```bash
   cd data/prompt-registry
   python3 measure_implementation.py
   python3 prioritize_atoms.py      # re-score after status changes
   python3 generate_work_queue.py
   python3 route_atoms.py
   ```

---

## Critical Files

| File | Action |
|------|--------|
| `data/prompt-registry/prioritize_atoms.py` | **CREATE** — main scoring engine |
| `data/prompt-registry/generate_work_queue.py` | **MODIFY** — use computed priority |
| `data/prompt-registry/route_atoms.py` | **MODIFY** — include priority in dispatch |
| `data/prompt-registry/prompt-atoms.json` | **MODIFIED BY SCRIPT** — adds priority fields |
| `data/prompt-registry/open-atoms-cache.json` | **MODIFIED BY SCRIPT** — updated cache |

## Reusable Code

- Keyword extraction: `measure_implementation.py` lines ~100-135 (domain-filtered tokenizer)
- Atom loading pattern: `generate_work_queue.py` lines 72-78
- Truncation utility: `generate_work_queue.py` lines 63-68

## Verification

1. Run `python3 prioritize_atoms.py` — should complete in <15 seconds, print distribution
2. Verify P0 atoms make sense: security items, corrections, recent governance rules
3. Verify P3 atoms make sense: old implicit-signals, vague directives, well-covered universes
4. Run `python3 generate_work_queue.py` — WORK-QUEUE.md should show P0 items first
5. Run `python3 route_atoms.py` — DISPATCH-QUEUE.md should show priorities within each target
6. Spot-check: compare 5 atoms manually against scoring formula

## Plan Persistence

Copy this plan to `organvm-corpvs-testamentvm/data/prompt-registry/plans/` after exiting plan mode, per plan file discipline.
