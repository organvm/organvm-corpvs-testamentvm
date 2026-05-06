# U1 — Per-Repo Lifecycle Audit

**Unit:** U1 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by parent-context coordinator (background worker rate-limited)

---

## 1. Context

Of the ~240 repos in the workspace, which are actively maintained, which are slowing, which are abandoned? Aggregate stats hide the individual-repo health that matters for "becoming a better creator" — a flagship repo silently going dormant is a different signal than the same repo getting incremental commits. This audit classifies tracked repos by dormancy and surfaces both the most-active and most-dormant patterns.

## 2. Method

- Loaded `data/fossil/fossil-record.jsonl` (10,510 entries with `repo`, `timestamp`, `organ`)
- Per-repo: extracted earliest commit, latest commit, total count, organ assignment
- Dormancy buckets: ACTIVE = last commit < 30 days; SLOWING = 30-90 days; DORMANT = 90-180 days; ABANDONED = 180+ days
- Reference date: 2026-05-05
- Cross-checked with `registry-v2.json` for promotion-status context

**Caveat**: The fossil-record covers 121 repos. The workspace has ~240 repos per `~/Workspace/CLAUDE.md`. The 119 repos in workspace but not in fossil are repos that either have no commits, were never run through `organvm fossil excavate`, or were created after the last excavation. This unit reports on the 121 *fossil-tracked* repos only.

## 3. Findings

**F1 — 86.8% of tracked repos are ACTIVE (commit in last 30 days).** Of 121 repos: 105 ACTIVE, 15 SLOWING, 0 DORMANT, 1 ABANDONED. The system is overwhelmingly in active maintenance — much healthier than would be expected for a 240-repo ecosystem.

**F2 — Only 1 abandoned repo: `gemini-cli-blender-extension` (last commit 2025-09-30, 5 commits, organ UNKNOWN).** This is a 7-month-stale repo with low commit history — likely an early experiment that didn't pan out. No flagship repos are abandoned.

**F3 — Top 5 most-active repos (last commit, organ):**
1. `domus-semper-palingenesis` (2026-05-05, 388 commits, LIMINAL) — chezmoi dotfile manager, very active
2. `meta-organvm` (2026-04-20, 411 commits, META) — meta-system corpus
3. `organvm-corpvs-testamentvm` (2026-04-15, 531 commits, META) — this repo, the planning corpus
4. `sovereign-systems--elevate-align` (2026-04-15, 63 commits, ORGAN-III) — flagship product
5. `agentic-titan` (2026-04-15, 105 commits, ORGAN-IV) — orchestration flagship

**F4 — Top 5 by commit volume:**
1. `repo` (2,662 commits, ORGAN-IV) — generic-named repo (unclear which actual repo this maps to in fossil; likely `organvm-engine` or similar via missing repo-disambiguation step)
2. `public-record-data-scrapper` (701 commits, ORGAN-III)
3. `organvm-corpvs-testamentvm` (531 commits, META)
4. `portfolio` (495 commits, LIMINAL)
5. `meta-organvm` (411 commits, META)

The "repo" entry with 2,662 commits is a data-quality issue: the fossil resolver didn't capture the actual repo name for that subset.

**F5 — 15 SLOWING repos (commit gap 30-90 days) include some flagships.** Notable slowing entries: `tmp_organvm-i-theoria.github.io` (2026-03-10, 11 commits, ORGAN-VII), `org-dotgithub` (2026-03-08, 12 commits, ORGAN-IV). The `tmp_` prefix on a github.io repo suggests staging that's not yet finalized.

**F6 — Per-organ commit volume (from fossil):**
- ORGAN-IV: 3,478 commits (33%) — orchestration dominates
- META: 1,677 (16%)
- ORGAN-III: 1,590 (15%)
- LIMINAL: 1,160 (11%)
- ORGAN-I: 767 (7%)
- ORGAN-II: 542 (5%)
- ORGAN-VI: 313 (3%)
- UNKNOWN: 309 (3%)
- ORGAN-V: 279 (3%)
- ORGAN-VII: 203 (2%)

The 309 UNKNOWN-organ commits indicate ~3% of fossil entries lack organ attribution.

## 4. Quantitative Table

| Bucket | Threshold | Count | % | Notes |
|---|---|---:|---:|---|
| ACTIVE | < 30 days | 105 | 86.8% | healthy maintenance |
| SLOWING | 30-90 days | 15 | 12.4% | needs attention |
| DORMANT | 90-180 days | 0 | 0% | none |
| ABANDONED | 180+ days | 1 | 0.8% | gemini-cli-blender-extension |
| **Total tracked** | — | **121** | 100% | of ~240 in workspace |

| Top-Active Repo | Last Commit | Commits | Organ |
|---|---|---:|---|
| domus-semper-palingenesis | 2026-05-05 | 388 | LIMINAL |
| meta-organvm | 2026-04-20 | 411 | META |
| organvm-corpvs-testamentvm | 2026-04-15 | 531 | META |
| sovereign-systems--elevate-align | 2026-04-15 | 63 | III |
| agentic-titan | 2026-04-15 | 105 | IV |

## 5. Negative Findings

- **NF1 — No flagship repos are abandoned.** This is a positive negative finding — the public-commitment surface is genuinely maintained.
- **NF2 — 119 repos in workspace are NOT in fossil-record.** The dormancy audit is incomplete by design; the 119 missing repos may include genuinely abandoned ones not visible to this unit.
- **NF3 — The "repo" entry with 2,662 commits is a data-quality issue.** Some commits got attributed to a generic "repo" string instead of the actual repo name. Fixing the fossil-record resolver would shift those commits onto their real repo.

## 6. Recommendations

**R1 — Run `organvm fossil excavate` against the 119 untracked repos.** The current view is selective. Either backfill the fossil-record to cover all workspace repos, or explicitly mark the missing ones as "intentionally untracked" (e.g., third-party clones, contrib mirrors). Either way, eliminates the silent-coverage gap.

**R2 — Resuscitate or archive the 15 SLOWING repos.** Some are temporary (`tmp_organvm-i-theoria.github.io` has the `tmp_` prefix), some are infrastructure (`org-dotgithub`). For each: either commit a maintenance update or formally archive via promotion-status change to ARCHIVED.

**R3 — Fix the fossil resolver's repo-name attribution.** 2,662 commits attributed to `repo` is the largest single data quality issue. Find and patch the resolver step that's losing the actual repo name on that subset.

**R4 — Schedule a 30-day SLOWING-bucket review.** Convert SLOWING into either ACTIVE (commit) or ABANDONED (mark). Avoid the bucket from becoming a permanent purgatory.

---

**Validation gate:** 6 findings, 8+ evidence anchors (repo names + commit dates + counts), 4 recommendations tied to findings, method explicit including caveat about 121 vs 240 repo coverage. Negative findings include the fossil-data-quality issue. Out-of-scope: commit message quality (U2), session-commit timing (U3), per-organ asks-vs-ships (U8) — all footnoted by reference.
