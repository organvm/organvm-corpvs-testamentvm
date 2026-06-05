# Session Prompts: 2026-06-04

**Session ID:** `e36b8ddd-d20e-44f0-8d8b-b30cc40ecc83`
**Duration:** ~10 min
**Working directory:** `/Users/4jp`
**Prompts:** 11 human messages

---

### P1 — 2026-06-04 13:22:28

<scheduled-task name="daily-worktree-triage-and-cleanup" file="/Users/4jp/.claude/scheduled-tasks/daily-worktree-triage-and-cleanup/SKILL.md">
This is an automated run of a scheduled task. The user is not present to answer questions. For implementation details, execute autonomously without asking clarifying questions — make reasonable choices and note them in your output. "write" actions (e.g. MCP tools that send, post, create, update, or delete), only take them if the task file asks for that specific action. When in doubt, producing a report of what you found is the correct output.

## Version: v1.0.0
## Status format: `<R>-repos-<W>-worktrees-<C>-removals-<D>-dirty-<L>-locked` (e.g., `176-repos-2-worktrees-0-removals-0-dirty-0-locked`)

## Metadata
- **Owner:** conductor (`4444J99` / `4444jPPP`)
- **Class:** I (local-token)
- **Cadence:** daily (09:22 EDT)
- **IRF row:** IRF-SYS-212 (Higher Ideal Form migration; worktree-housekeeping is part of repo-hygiene infrastructure)
- **Depends on:** `git worktree list` across repos; no other routines
- **Audit log path:** `~/.claude/scheduled-tasks/audit/YYYY-MM-DD.log`
- **Conformance:** docs/standards/24 v1.1.0
- **Last semver bump:** 2026-05-27 — initial v1.0.0 (bookend + canonical-form discipline applied)

## Audit log (start — invoke FIRST)
Run: `~/.local/bin/scheduled-task-audit-bookend daily-worktree-triage-and-cleanup start`
Per docs/standards/18 §9, every Class-(I) fire must emit start + end entries regardless of writes.

Operate under `~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-branch-governance.md` Section 10. **Read it first.** Hard NEVERs apply: no force-removes of dirty trees, no operations on locked worktrees, no touching the primary worktree.

## Context (why this task exists)
Per `~/.claude/projects/-Users-4jp/memory/project_session_2026_05_23_worktree_housekeeping_enforcement_disposition.md` and `feedback_chezmoi_add_during_rebase_race.md`, worktrees accumulate: cross-session sibling worktrees, forgotten experimental branches, locked worktrees from abandoned rebases.

## Pre-flight
- Standards doc 17 readable
- Audit log path writable

## Procedure

### Phase A: enumerate (read-only)
For every git repo under `~/Workspace/*` and `~/Code/*` (skip `_agents/`, `node_modules/`, `__pycache__`): `git -C <repo> worktree list --porcelain`.

**Skip the primary worktree.** For each secondary worktree, collect: path, branch, last-mtime, locked status, uncommitted (status --porcelain), unpushed (rev-list @{u}..HEAD --count).

### Phase B: classify
| Bucket | Criteria |
|---|---|
| **SAFE-CLEAN** | No uncommitted, no unpushed, idle >7 days, NOT locked |
| **DIRTY-IDLE** | Has uncommitted OR unpushed, idle >14 days |
| **LOCKED** | Marked locked by git (rebase or explicit) |
| **ACTIVE** | Modified within 24h |
| **STALE-PRUNABLE** | Registered path does not exist on disk (`git worktree list` shows `prunable`) |

### Phase C: SAFE-CLEAN cleanup
For each SAFE-CLEAN worktree:
- **Per-run cap: max 5 removals**
- Execute: `git -C <parent-repo> worktree remove <wt-path>` (NO `--force`)
- Per-action audit: `<ISO>\tdaily-worktree-triage-and-cleanup\t<parent-repo>\t<wt-path>\tworktree-remove\tsuccess|failure|locked-mid-flight`

### Phase D: report
- SAFE-CLEAN removals performed
- DIRTY-IDLE — conductor decision required
- LOCKED — recommend `git worktree unlock <path>` after confirming no in-flight rebase
- STALE-PRUNABLE — recommend `git worktree prune` per parent-repo (branch refs preserved per doc 23 alchemical evolution)
- ACTIVE — count only

## What this task NEVER does
- Force-removes dirty trees, force-removes worktrees with unpushed commits, touches primary worktree, operates on locked worktrees autonomously

## Audit log (end — invoke LAST, after the report)
Run: `~/.local/bin/scheduled-task-audit-bookend daily-worktree-triage-and-cleanup end <status>`
where `<status>` follows format `<R>-repos-<W>-worktrees-<C>-removals-<D>-dirty-<L>-locked`. Use hyphens; no whitespace.
</scheduled-task>

**Actions taken:**
- Bash: `~/.local/bin/scheduled-task-audit-bookend daily-worktree-triage-and-cleanup start 2>&1; echo "---EXIT: $?---"`
- Bash: `cat ~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-branch-governance.md 2>&1 | sed -n '1,50p' | head -5; ec...`
- Bash: `cd ~
# Find all git repos under Workspace and Code, skipping noise dirs. A repo has a .git entry at its root.
# Search t...`
- Bash: `cd ~
> /tmp/wt_findings.txt
secondary_repos=0
total_secondary_wt=0
while IFS= read -r repo; do
  [ -d "$repo/.git" ] || ...`
- Bash: `while kill -0 $(pgrep -f 'worktree list --porcelain' | head -1) 2>/dev/null; do sleep 1; done 2>/dev/null
sleep 1
echo "...`
- Read `/private/tmp/claude-501/claude-501/-Users-4jp/e36b8ddd-d20e-44f0-8d8b-b30cc40ecc83/tasks/bk8gb46uw.output`
- Bash: `sleep 20; echo "=== current output ==="; cat /private/tmp/claude-501/claude-501/-Users-4jp/e36b8ddd-d20e-44f0-8d8b-b30cc...`
- Bash: `echo "=== interim findings ==="; cat /tmp/wt_findings.txt 2>/dev/null; echo "=== running git procs ==="; ps aux | grep -...`
- Bash: `echo "=== actual git processes (any) ==="; ps -eo pid,etime,command | grep -w git | grep -v grep | head -20
echo "=== ba...`
- Bash: `cd ~
# kill any lingering background loop from before
pkill -f 'wt_repos.txt' 2>/dev/null
GTIMEOUT=$(command -v gtimeout...`

---

---

## Prompt Summary

**Total prompts:** 1
**Session duration:** ~10 min
**Avg time between prompts:** ~10.0 min

### Prompt Categories (heuristic)

- **Directives** (implement/build/create/add/write): 1
- **Questions**: 0
- **Fixes** (fix/error/bug/broken/fail): 1
- **Reviews** (check/verify/review/audit): 1
