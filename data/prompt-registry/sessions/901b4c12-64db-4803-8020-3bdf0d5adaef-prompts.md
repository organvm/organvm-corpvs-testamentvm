# Session Prompts: 2026-06-12

**Session ID:** `901b4c12-64db-4803-8020-3bdf0d5adaef`
**Duration:** ~2 min
**Working directory:** `/Users/4jp`
**Prompts:** 8 human messages

---

### P1 — 2026-06-12 12:03:27

<scheduled-task name="daily-hook-drift" file="/Users/4jp/.claude/scheduled-tasks/daily-hook-drift/SKILL.md">
This is an automated run of a scheduled task. The user is not present to answer questions. For implementation details, execute autonomously without asking clarifying questions — make reasonable choices and note them in your output. "write" actions (e.g. MCP tools that send, post, create, update, or delete), only take them if the task file asks for that specific action. When in doubt, producing a report of what you found is the correct output.

## Version: v2.4.0
## Status format: `no-drift` | `drift-detected-<agent>[-<agent>...]` | `error-<reason>`

## Metadata
- **Owner:** conductor (`4444J99` / `4444jPPP`)
- **Class:** I (local-token)
- **Cadence:** daily (08:03 EDT)
- **IRF row:** IRF-SYS-210 (deployed-only hook violation pattern — this routine is mitigation (a))
- **Depends on:** `~/.local/bin/check-agent-hooks-drift` shim, chezmoi runtime, python3 ≥3.11 (tomllib stdlib)
- **Audit log path:** `~/.claude/scheduled-tasks/audit/YYYY-MM-DD.log`
- **Conformance:** docs/standards/24 v1.1.0
- **Last semver bump:** 2026-06-10 — v2.4.0 (MINOR — "act, don't just report", per conductor *"a report is only a fraction of any battle"*): (1) NEW `check-agent-hooks-drift --discover` mode probes a `DISCOVERY_CANDIDATES` watchlist for **coverage gaps** — chezmoi-managed surfaces carrying a real hook/mcp block but absent from `SURFACE_MATRIX` (emits `COVERAGE-GAP=…`, exit 3). This is the structural fix for blind spots: a normal run can only check what's in the matrix, so an unlisted surface (claude-desktop, claude-json) was invisible. On its very first run `--discover` found `claude-json` (`~/.claude.json` `.mcpServers`, managed via `modify_` merge, verified in-sync) → promoted into `SURFACE_MATRIX` (now 6 checked surfaces). (2) Procedure rewritten from "report each diff" into explicit phases **discover → check → act → self-heal**, with auto-fix wired to divergence DIRECTION (was prose-only "posture", never operationalized). (3) Autonomy split: unattended cron self-heals SAFE target-only `chezmoi apply` (directions #1/#3) automatically but opens-PR-without-merge for any source/coverage change; interactive runs may merge on request. (4) shim footer + help updated; detector stays read-only (Rule #6), remediation is the caller's.
  - prior: 2026-06-10 — v2.3.0 (MINOR: appended `claude-desktop` row to `SURFACE_MATRIX` — `~/Library/Application Support/Claude/claude_desktop_config.json` `.mcpServers`, a chezmoi-managed `modify_` template surface that no row had ever pointed at, so the routine was blind to it. The 2026-06-10 run discovered live drift on it the moment it was checked: 3 MCP servers (filesystem, sequential-thinking, memory) pinned `/opt/homebrew/bin/npx` on disk vs canonical `~/.local/share/npm/bin/npx` in source — direction #3, reconciled target-only via `chezmoi apply`. Coverage 4→5 checked surfaces. Validated: spaced path is `IFS='|' read`-safe and all functional `$path` uses are quoted. Discovery sweep also confirmed `~/.cline` + `~/.copilot` are empty husks (no hook surface yet) and `~/.gemini/antigravity-cli` is an app-runtime store like Goose/Zed — none trackable today.)
  - prior: 2026-06-05 — v2.2.0 (de-hardcode the coverage matrix: new `check-agent-hooks-drift --matrix` emits the table from live `SURFACE_MATRIX` + chezmoi state, state *derived* not hand-labelled; SKILL.md table is now an `AUTOGEN:coverage-matrix` block the daily routine regenerates each run so it self-heals instead of drifting — root-cause fix for the v2.0.x/v2.1.0 hand-edit churn, per the conductor directive "no hardcoded information — all dynamic & auto-updating")
  - prior: 2026-06-05 — v2.1.0 (coverage matrix corrected to deployed reality after PR #59 was finally `chezmoi apply`'d: 7 rows; `gemini-mcp` retargeted `settings.json`→`mcp-server-enablement.json`; `cursor-mcp` + `continue` rows added; symlink realpath-resolution now deployed so symlinked agent homes — `~/.gemini`, `~/.codex`, `~/.cursor` — stop falsely reporting "unmanaged"; `codex` + `opencode-mcp` reclassified dormant→**excluded-by-design** per `.chezmoiignore` `be960d4`; **auto-fix posture flipped `never`→`always` (worktree→PR→merge)** per standing policy `feedback_always_auto_fix_via_worktree_pr`)
  - prior: 2026-06-05 — v2.0.1 (PATCH from a parallel session: reclassified `opencode-mcp` active→excluded after `be960d4` `.chezmoiignore`'d `opencode.json`. Correct observation but pre-#59 framing — superseded by v2.1.0, which deployed the merged shim and found the true root cause was a stale deployed shim, not a 5-surface ceiling. Intent folded forward.)
  - prior: 2026-05-27 — v2.0.0 (BREAKING: scope expanded Claude-only → multi-agent; status vocabulary changed from `drift-detected-<event-types>` to `drift-detected-<agent>[-<agent>...]`; old `check-claude-hooks-drift` retained as deprecation wrapper, removal target 2026-08-27)

## Coverage matrix

Surfaces are declared once, in the shim's `SURFACE_MATRIX` array (one `agent|path|kind|filter` row each — adding an agent is a one-line append **there**, never here). A surface is only *checkable* if it has a chezmoi source-of-truth to diff against; app-rewritten configs are deliberately `.chezmoiignore`'d and correctly skipped as "unmanaged" every run.

**The table below is auto-generated — do not hand-edit it.** It is produced by `check-agent-hooks-drift --matrix`, which *derives* every row's state from live chezmoi facts rather than carrying a hand-typed label: `checked` = chezmoi renders source for it; `excluded-by-design` = its (realpath-resolved) target is `.chezmoiignore`'d; `dormant` = neither (not yet `chezmoi add`-ed); `absent` = deployed file missing. The daily routine regenerates this block every run (see "Procedure" → "Self-heal the coverage matrix"), so it cannot silently lie the way the hand-maintained v2.0.x/v2.1.0 matrices did — that drift is the entire reason this generator exists. Refresh on demand with `check-agent-hooks-drift --matrix`; the human *why* (gemini retarget, symlink realpath, exclusion rationale) lives in the prose below the block, which the generator never touches.

<!-- AUTOGEN:coverage-matrix START — regenerated by `check-agent-hooks-drift --matrix`; do not hand-edit between these markers -->
| Agent | Deployed path | Hook block | Extractor | State |
|---|---|---|---|---|
| `claude` | `~/.claude/settings.json` | `.hooks` | `jq` | ✅ checked |
| `codex` | `~/.codex/config.toml` | `.notify` | `toml-jq` | ⛔ excluded-by-design — app-rewritten; `.chezmoiignore`'d |
| `gemini-mcp` | `~/.gemini/mcp-server-enablement.json` | `.` | `jq` | ✅ checked |
| `gemini-pol` | `~/.gemini/policies/housekeeping.json` | `.` | `jq` | ✅ checked |
| `opencode-mcp` | `~/.config/opencode/opencode.json` | `.mcp` | `jq` | ⛔ excluded-by-design — app-rewritten; `.chezmoiignore`'d |
| `cursor-mcp` | `~/.cursor/mcp.json` | `.mcpServers` | `jq` | ✅ checked |
| `continue` | `~/.continue/config.yaml` | `.mcpServers` | `yaml-jq` | ⏸ dormant — auto-activates on `chezmoi add` |
| `claude-desktop` | `~/Library/Application Support/Claude/claude_desktop_config.json` | `.mcpServers` | `jq` | ✅ checked |
| `claude-json` | `~/.claude.json` | `.mcpServers` | `jq` | ✅ checked |

_Auto-generated by `check-agent-hooks-drift --matrix` — do not hand-edit; the daily-hook-drift routine regenerates this block._
<!-- AUTOGEN:coverage-matrix END -->

**The "unmanaged" count is expected, not a regression.** Excluded-by-design rows (`codex`, `opencode-mcp`) are app-owned configs that the owning app rewrites at runtime (auth state, UI prefs, hook trust-hashes, extension flags). Managing them in chezmoi re-asserts a stale source every `apply` and fights the app → perpetual benign drift. Per the de-hardcode #6 decision (`be960d4`), the runtime file is canonical for app state; the durable user-intent skeleton lives in git history. These rows are **kept** (not deleted) so they auto-reactivate if an app ever stops self-rewriting. For Gemini, the tracked hand-authored surface is `mcp-server-enablement.json` (not the app-rewritten `settings.json`).

**Symlink resolution.** Several agent homes are chezmoi-managed *symlinks* (`~/.gemini`, `~/.codex`, `~/.cursor` → `~/.local/share/...`). `chezmoi cat` cannot resolve through its own managed symlinks, so the shim realpath-resolves the deployed path before reading source. Without this (the pre-PR-#59 deployed shim), every symlinked agent silently reported "unmanaged" even when fully tracked — exactly the false negative that pinned coverage at 1 surface on the 2026-06-05 run until the merged shim was finally `chezmoi apply`'d.

**Dormant rows auto-activate** when their config is onboarded via `chezmoi add <path>` — no SKILL.md edit needed; the `chezmoi cat` probe returns content from that point and the row begins reporting.

**Surfaces explicitly NOT covered** (out of scope):
- Plugin-scoped `~/.claude/plugins/*/hooks.json` files — LOCAL-ONLY by plugin design, no chezmoi source to diff against. Universal Rule #2 inversion; tracked separately.
- Zed (`~/.config/zed/settings.json`): JSONC; regex comment-stripping would corrupt `//` inside string values. Needs a real JSONC parser.
- Goose (`~/.config/goose/config.yaml`): `.chezmoiignore`'d as app-runtime-owned; no stable hand-authored surface to diff.

## Audit log (start — invoke FIRST)
Run: `~/.local/bin/scheduled-task-audit-bookend daily-hook-drift start`
Per docs/standards/18 §9, every Class-(I) fire must emit start + end entries regardless of writes.

## Procedure

Every run executes four phases **in order: discover → check → act → self-heal**. A report is where the work STARTS, not where it ends — every finding below routes to a concrete action. The shim emits its canonical status on the final line of stdout as `STATUS=<payload>`; capture it for the end bookend.

**Autonomy depends on who is running it** (this is the v2.4.0 policy — "self-heal safe, PR the rest"):
- **Unattended (daily cron, no human present):** auto-apply the SAFE fixes (target-only `chezmoi apply` — directions #1/#3 below); for anything that mutates chezmoi SOURCE or adds coverage, open a worktree→PR but **DO NOT auto-merge** — leave it ready for conductor review. Never merge unattended.
- **Interactive (conductor present):** may carry any fix through to merge on request.

### Phase 1 — Discover coverage gaps (every run)

Run `check-agent-hooks-drift --discover`.
- **exit 0** — no gaps; every managed agent surface is already in `SURFACE_MATRIX`. Continue.
- **exit 3** — one or more `COVERAGE-GAP=agent|path|kind|filter` lines on stdout. Each is a chezmoi-**managed** surface carrying a real hook/mcp block that **no matrix row checks** — a blind spot (exactly how `claude-desktop` and `claude-json` each went unchecked). For each gap:
  1. Confirm it is sound: not `.chezmoiignore`'d, target block stable (not a perpetually app-rewritten key), and `--matrix` would classify it `checked`.
  2. Append the `agent|path|kind|filter` row to `SURFACE_MATRIX` in the shim source, regenerate the AUTOGEN matrix (Phase 4), and open a worktree→PR. **Do not auto-merge unattended.**
  - A `present-unmanaged` or `present-managed-empty` stderr note is **not** a gap (no source to diff / no block to check) — no action; it is informational only.

### Phase 2 — Check for drift

Run `check-agent-hooks-drift` (no args = all matrix agents; `--only=a,b` for a subset).
- **exit 0** (`STATUS=no-drift`) — report one line (`no drift across N agent surfaces`); go to Phase 4.
- **exit 1** (`STATUS=drift-detected-<agent>…`) — the shim wrote a per-agent unified diff to stderr. For each drifted agent, name the semantic drift, then **act per Phase 3**:
  - `claude` — which hook event types diverged (PreToolUse, PostToolUse, SessionStart, SessionEnd, UserPromptSubmit, Stop, PreCompact, Notification)
  - `codex` — whether the notify command path or trigger event changed
  - `gemini-mcp` / `opencode-mcp` / `cursor-mcp` / `continue` / `claude-desktop` / `claude-json` — which MCP server entries were added/removed/edited
  - `gemini-pol` — which policy section(s) drifted
- **exit 2** (`STATUS=error-<reason>`) — internal error. Report which agent's extraction failed and which tool was missing/malformed. No fix.

### Phase 3 — Act on drift, by divergence direction

**NON-NEGOTIABLE first: scan every diff for secrets** before any commit/push (app configs carry live tokens — codex `Authorization`, `bearer_token_env_var`). A detected secret is a hard stop: surface for rotation, never commit it, never route around the credential gate.

Then classify each drift by comparing the deployed block against the chezmoi-rendered source, and fix:

1. **Deployed strayed from canonical source** (source is correct; an app or hand-edit moved the deployed file). The common case — e.g. Claude Desktop rewriting `npx` paths. **Fix = `chezmoi apply --force <deployed-path>`** (target-only; no source mutation, no PR). **Auto-run, including unattended.** Re-run the check to confirm clean.
2. **Deployed is intentionally ahead of source** (a deliberate deployed-file edit that SHOULD become canonical). **Fix = lift into source:** worktree, `chezmoi add -S <worktree> <deployed-path>` (or `chezmoi edit`), regenerate any AUTOGEN, scan for secrets, commit, **open a PR — do NOT auto-merge unattended** (conductor reviews). Interactive: merge on request, then `chezmoi apply`.
3. **Source ahead of deployed** (a merged source change was never applied). The shim shows this indirectly as stale behavior. **Fix = `chezmoi apply <deployed-path>`** (target-only). **Auto-run, including unattended.**

Direction is a judgment call: if the chezmoi source was committed within the drift window, treat as #1/#3 (source canonical, re-apply). If the deployed change looks intentional and newer, treat as #2 and **escalate via PR rather than clobbering it**. For `excluded-by-design` rows reporting drift: that should not happen (they're unmanaged) — the `.chezmoiignore` entry was likely removed; investigate, don't blindly fix.

### Phase 4 — Self-heal the coverage matrix (every run)

The coverage table in this file is **generated**, not maintained. Regenerate it so the doc can never drift from runtime reality:

1. Capture live state: `check-agent-hooks-drift --matrix`.
2. Splice that output into this SKILL.md between the `<!-- AUTOGEN:coverage-matrix START … -->` and `<!-- AUTOGEN:coverage-matrix END -->` markers — anchor on the line-start `<!--` markers, **not** a bare `AUTOGEN` match (this prose mentions the marker names; an unanchored match grabs the wrong region). Replace everything between them; touch nothing outside.
3. If the deployed SKILL.md changed as a result, that is divergence-direction #2 — lift it to source via the Phase 3 PR flow (no auto-merge unattended). If unchanged, do nothing.

This makes the matrix self-correcting: a new `SURFACE_MATRIX` row, or any change in chezmoi management state (a `chezmoi add`, a new `.chezmoiignore` line), shows up in the table on the next run with no hand-editing. Never hand-edit the rows between the markers — the next regeneration overwrites them, and until then they look authoritative while lying.

## Backward compatibility

`~/.local/bin/check-claude-hooks-drift` is preserved as a deprecated thin wrapper that delegates to `check-agent-hooks-drift --only=claude`. It emits a deprecation warning to stderr on every invocation. Removal target: **2026-08-27** (one quarterly cycle). External callers should migrate.

## What this task NEVER does
- **Commits a secret.** Scan every diff before pushing; app configs carry live tokens (e.g. codex `config.toml` `Authorization` headers). A detected secret is a hard stop — surface for rotation, never commit it, never work around a credential gate.
- **Merges a source/coverage PR unattended.** On the daily cron run, source-mutating fixes (new matrix rows, direction-#2 lifts, matrix-regen) open a PR and STOP for conductor review. Auto-merge only happens interactively, on request. (Target-only `chezmoi apply` self-heals — directions #1/#3 — are exempt: they touch no source.)
- Force-pushes, or pushes source changes outside a PR (worktree→PR only).
- Re-asserts an `.chezmoiignore`'d app-rewritten config back into management (that fight is settled — `be960d4`).
- Touches plugin-scoped `~/.claude/plugins/*/hooks.json` files (out of scope; no source-of-truth).
- Files IRF rows (auto-fix routes through PRs, not the IRF ledger).

(This task **acts**, it doesn't just report — see "Procedure" Phases 1–4 above. v2.1.0 retired the old read-only rule; v2.4.0 split autonomy by attended/unattended and added discovery.)

## Audit log (end — invoke LAST, after the report)
Run: `~/.local/bin/scheduled-task-audit-bookend daily-hook-drift end <status>`
where `<status>` is the verbatim payload of the `STATUS=…` line emitted by `check-agent-hooks-drift`. Use hyphens; no whitespace.

Status string examples:
- `daily-hook-drift end no-drift`
- `daily-hook-drift end drift-detected-codex`
- `daily-hook-drift end drift-detected-claude-gemini-mcp`
- `daily-hook-drift end drift-detected-claude-codex-gemini-mcp-gemini-pol-opencode-mcp` (full-fleet drift)
- `daily-hook-drift end error-missing-tool-python3`
- `daily-hook-drift end error-extraction-failed-codex`
</scheduled-task>

**Actions taken:**
- Bash: `~/.local/bin/scheduled-task-audit-bookend daily-hook-drift start 2>&1; echo "---EXIT:$?---"`
- Bash: `command -v check-agent-hooks-drift && echo "---" && ~/.local/bin/check-agent-hooks-drift --discover 2>&1; echo "---EXIT:...`
- Bash: `~/.local/bin/check-agent-hooks-drift 2>&1; echo "---EXIT:$?---"`
- Bash: `~/.local/bin/check-agent-hooks-drift --matrix 2>&1; echo "---EXIT:$?---"`
- Bash: `SKILL=~/.claude/scheduled-tasks/daily-hook-drift/SKILL.md
# Extract the current AUTOGEN block (between the markers) and ...`
- Bash: `SKILL=~/.claude/scheduled-tasks/daily-hook-drift/SKILL.md
# Anchor on line-START markers (^<!--) so the in-prose backtic...`
- Bash: `~/.local/bin/scheduled-task-audit-bookend daily-hook-drift end no-drift 2>&1; echo "---EXIT:$?---"`

---

---

## Prompt Summary

**Total prompts:** 1
**Session duration:** ~2 min
**Avg time between prompts:** ~2.0 min

### Prompt Categories (heuristic)

- **Directives** (implement/build/create/add/write): 1
- **Questions**: 0
- **Fixes** (fix/error/bug/broken/fail): 1
- **Reviews** (check/verify/review/audit): 1
