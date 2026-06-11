# Session Prompts: 2026-06-10

**Session ID:** `d7e08d8b-162e-41a3-b1a7-d088b2cbf0e6`
**Duration:** ~70 min
**Working directory:** `/Users/4jp`
**Prompts:** 14 human messages

---

### P1 — 2026-06-10 13:21:02

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
- Bash: `~/.local/bin/scheduled-task-audit-bookend daily-worktree-triage-and-cleanup start 2>&1; echo "---EXIT:$?---"`
- Bash: `sed -n '1,80p' ~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-branch-governance.md 2>&1 | tail -100; echo "...`
- Bash: `set -e
for root in "$HOME/Workspace" "$HOME/Code"; do
  [ -d "$root" ] || { echo "MISSING-ROOT: $root"; continue; }
  # ...`
- Bash: `> /tmp/wt_primary.txt; > /tmp/wt_linkfiles.txt
while IFS= read -r repo; do
  if [ -d "$repo/.git" ]; then echo "$repo" >...`
- Bash: `cat /private/tmp/claude-501/-Users-4jp/d7e08d8b-162e-41a3-b1a7-d088b2cbf0e6/tasks/bp5pqkmwr.output 2>/dev/null`
- Bash: `echo "primary repos (.git dir): $(wc -l < /tmp/wt_primary.txt)"
echo "linkfiles (.git file): $(wc -l < /tmp/wt_linkfiles...`
- Bash: `: > /tmp/wt_primary.txt; : > /tmp/wt_linkfiles.txt
while IFS= read -r repo; do
  if [ -d "$repo/.git" ]; then printf '%s...`
- Bash: `: > /tmp/wt_report.txt
multi=0
while IFS= read -r repo; do
  out=$(git -C "$repo" worktree list --porcelain 2>/dev/null)...`
- Bash: `cat /tmp/wt_report.txt`
- Bash: `now=$(date +%s)
printf '%-78s | %-7s | %-9s | %-8s | %s\n' "WORKTREE" "DIRTY" "UNPUSHED" "IDLEdays" "BUCKET"
# iterate r...`
- Bash: `now=$(date +%s)
safe=0; dirtyidle=0; active=0; retain=0; locked=0; prune=0; dirtycount=0; total=0
awk '/^##### REPO:/{fi...`
- Bash: `~/.local/bin/scheduled-task-audit-bookend daily-worktree-triage-and-cleanup end "221-repos-53-worktrees-0-removals-10-di...`

---

### P2 — 2026-06-10 14:31:53 (+70m)

<task-notification>
<task-id>bp5pqkmwr</task-id>
<tool-use-id>toolu_017FVG44FM2AuVTM4WNcZBpQ</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-4jp/d7e08d8b-162e-41a3-b1a7-d088b2cbf0e6/tasks/bp5pqkmwr.output</output-file>
<status>killed</status>
<summary>Background command "Split primaries from linkfile worktrees" was stopped</summary>
</task-notification>

---

## Prompt Summary

**Total prompts:** 2
**Session duration:** ~70 min
**Avg time between prompts:** ~35.0 min

### Prompt Categories (heuristic)

- **Directives** (implement/build/create/add/write): 1
- **Questions**: 0
- **Fixes** (fix/error/bug/broken/fail): 1
- **Reviews** (check/verify/review/audit): 1
