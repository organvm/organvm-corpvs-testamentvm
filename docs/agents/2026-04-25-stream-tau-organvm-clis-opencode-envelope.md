# Handoff Envelope — Stream Τ: Organvm CLI Tooling Build

**Target agent:** OpenCode
**Source agent:** Claude Opus 4.7 (1M context)
**Plan:** `~/.claude/plans/okay-so-now-harmonic-kettle.md` (Stream Τ)
**Status:** READY FOR DISPATCH (manual; conductor_fleet MCP not available in originating session)
**Created:** 2026-04-25

## Scope

Build 5 missing organvm CLIs + 1 pre-commit hook. These tools were identified as gaps during the 72h dark-matter audit (`docs/portfolio/dark-matter-inventory.md`). Without them: future 72h sweeps remain manual, sister-relay propagation continues to leak stale state, DONE-ID collisions stay possible.

This is well-scoped infrastructure CLI work — OpenCode's lane.

## Source context (read FIRST)

- `~/.claude/plans/okay-so-now-harmonic-kettle.md` — Stream Τ section (D.3)
- `~/Workspace/organvm/organvm-corpvs-testamentvm/docs/portfolio/dark-matter-inventory.md` — the 25 items the tools must surface
- `~/Workspace/organvm/organvm-corpvs-testamentvm/data/done-id-counter.json` — counter file the hook protects
- Existing organvm CLI source location (verify on entry): probably `~/Workspace/organvm/organvm-corpvs-testamentvm/cli/` or `~/Workspace/organvm-iv-taxis/<some-repo>/cli/` — discover via `which organvm` and follow the symlink

## Build targets

### CLI 1: `organvm sessions audit`

```
organvm sessions audit --since <duration>
```

**Inputs:** duration string (e.g. `72h`, `7d`, `30d`)
**Reads:**
- All `~/.claude/projects/-Users-[user]/memory/project_session_*.md` files; filter by mtime within window
- `~/Workspace/organvm/organvm-corpvs-testamentvm/INST-INDEX-RERUM-FACIENDARUM.md` (text grep for session names)
- `~/Workspace/organvm/organvm-corpvs-testamentvm/data/fossil/fossil-record.jsonl` (JSONL filter by date)
- Git log of relevant repos (use `gh repo list` for known repos)

**Outputs:**
- Table: session_id | memory_file | irf_rows | fossil_entries | git_commits | triple_ref_status
- triple_ref_status = OK if memory + IRF + (git OR fossil) all present; STALE if memory only

**Acceptance:** Running `organvm sessions audit --since 72h` on 2026-04-25 returns the 10 session memories listed in `dark-matter-inventory.md` with correct status flags.

### CLI 2: `organvm subatomic decompose`

```
organvm subatomic decompose <session-id-or-memory-file>
```

**Inputs:** session ID (e.g. `S-2026-04-25-v5-materia`) or path to a `project_session_*.md` file
**Reads:** the memory file + git log of repos referenced in it
**Algorithm:** parse the memory's narrative breaks (## headers, "**Then**", commit-count groupings). For each segment, propose a sub-atom as a candidate DONE-N entry with: title, description, source-commit, parent-session.
**Output:** YAML to stdout with proposed sub-atoms, NOT auto-claimed; human/Claude reviews before claiming DONE-IDs.

**Acceptance:** Running against `project_session_2026-04-25_v5_materia_physics.md` returns ≥10 sub-atom candidates (predicted 11 in dark-matter-inventory.md).

### CLI 3: `organvm memory triangulate`

```
organvm memory triangulate --since <duration> [--strict]
```

**Inputs:** duration window
**Reads:** all memory files + IRF + fossil-record.jsonl + recent git logs across known repos + open GitHub issues (`gh issue list --state all --search "created:>=<date>"`)
**Algorithm:** for each entity (work item, person, project), count reference locations. Report items with <3 references (single-location risk). Universal rule #2 + axiom #23 enforcement.
**Output:** Table by entity_id with reference counts and missing locations.

**Acceptance:** Running `organvm memory triangulate --since 72h` on 2026-04-25 returns ≥25 single-location entries (the dark-matter inventory items, since they're now 2/3 in IRF + memory but missing from git/GH for some).

### CLI 4: `organvm relay draft`

```
organvm relay draft <relay-file>
```

**Inputs:** path to a sister-agent relay file (typically a markdown HANDOFF doc)
**Reads:** the relay's claims (file paths, commit SHAs, DONE-IDs, status assertions)
**Algorithm:** for each claim, verify against current disk state (file exists? commit in git log? DONE-ID in counter? status matches IRF?). Reject relay if >0% staleness.
**Output:** Diff-style report — each claim CONFIRMED / STALE / DROP, with evidence per claim.

**Acceptance:** Running on a deliberately-stale relay file returns the correct staleness diagnosis.

### CLI 5: `organvm atoms pipeline --verify`

```
organvm atoms pipeline --verify
```

**Inputs:** none (operates on full corpus)
**Reads:** done-id-counter.json + IRF + fossil-record.jsonl + git logs + handoff envelopes
**Algorithm:** for every DONE-NNN in the counter, verify: matching commit (git log search), matching IRF row (text search), matching memory entry (file search), matching handoff if applicable.
**Output:** Table of broken DONE-IDs with what's missing.

**Acceptance:** Returns 0 broken entries on clean state; introduces a deliberate orphan DONE-N and verifies detection.

### Pre-commit hook: done-id-counter.json collision guard

**Path:** `~/Workspace/4444J99/domus-semper-palingenesis/private_dot_claude/hooks/check-done-id-counter.sh` (deployed to `~/.claude/hooks/` via chezmoi)

OR repo-local: `~/Workspace/organvm/organvm-corpvs-testamentvm/.git/hooks/pre-commit` (or `.pre-commit-hooks.yaml` if pre-commit framework already in use — investigate first; per existing pre-commit output in corpvs, the framework IS in use).

**Algorithm:** before commit, if `data/done-id-counter.json` is being modified:
1. Pull latest remote counter file (read-only fetch)
2. If remote `next_id` > local `next_id` → BLOCK commit, instruct: "Remote has higher counter; pull --rebase first"
3. If remote `next_id` == local before edit → allow
4. If local `next_id` < remote `next_id` → BLOCK with message about mid-edit collision

**Acceptance:** Deliberately introduce a stale counter (manually decrement next_id) → hook blocks. Clean state → hook passes.

## Reused utilities (DO NOT REIMPLEMENT)

- existing `organvm` CLI framework (Click? Typer? — discover on entry)
- existing chezmoi hook deployment patterns (other hooks in `private_dot_claude/hooks/`)
- existing IRF parsing if any (`scripts/invoke.py` per corpvs CLAUDE.md)

## Constraints (HARD RULES)

- **Universal rule #17** — no stubs; complete CLIs only
- **Universal rule #55 (No LaunchAgents)** — every CLI is on-demand only; do NOT add `crontab` entries, `launchd` plists, or any timer-based execution; if a feature seems to need scheduling, surface as a manual `organvm cron suggest` output for the user to schedule themselves
- **Constitutional axiom #22** — every CLI ships with at least one self-test that exercises the happy path
- **Universal rule #2** — final commit pushed to remote
- **No mocking the database** (per dotfiles feedback memory `feedback_no_mock_db.md` if exists) — integration tests against real corpvs data, not fixtures
- **Pre-commit hook MUST NOT bypass via --no-verify in tests** — that's a corner-case bug

## Cross-verify protocol

When this work returns to Claude:

1. All 5 CLIs invocable with `--help`; help text matches spec above
2. CLI 1 returns exactly the 10 session memories in dark-matter-inventory.md when run with `--since 72h` from 2026-04-25 baseline (use `git log` to set artificial date if needed)
3. CLI 2 produces ≥10 sub-atoms for V5 materia session
4. CLI 3 produces the expected single-location set
5. CLI 4 detects stale claim correctly on test relay
6. CLI 5 detects orphan DONE-N correctly
7. Pre-commit hook blocks deliberate collision; allows clean update
8. Git commits + pushes to relevant repos (corpvs for CLIs, dotfiles for hook)

## Out-of-scope (do NOT do)

- Do not build the DIWS skill (Stream Σ, separate envelope)
- Do not run the actual 72h atomization sweep (Stream Ω, Claude lane)
- Do not modify the IRF directly — Claude handles IRF row updates on cross-verify
- Do not change `done-id-counter.json` schema — append-only protections, no migrations

## On completion

1. Session memory at `~/.claude/projects/-Users-[user]/memory/project_session_<id>_organvm_clis.md`
2. Add to `MEMORY.md` Active Artifacts: `[Organvm CLI fleet]` entry
3. Handoff-completion marker at `~/Workspace/organvm/organvm-corpvs-testamentvm/docs/agents/2026-04-25-stream-tau-COMPLETED.md` with commit SHAs

## Source plan

This envelope is generated from parent plan: `~/.claude/plans/okay-so-now-harmonic-kettle.md` (Stream Τ, lines under "D.3 Stream Τ — Tooling Layer").
