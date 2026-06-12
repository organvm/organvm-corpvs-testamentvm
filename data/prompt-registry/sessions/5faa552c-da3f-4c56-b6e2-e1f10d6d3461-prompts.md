# Session Prompts: 2026-06-12

**Session ID:** `5faa552c-da3f-4c56-b6e2-e1f10d6d3461`
**Duration:** ~5 min
**Working directory:** `/Users/4jp`
**Prompts:** 15 human messages

---

### P1 — 2026-06-12 13:22:37

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
- Bash: `~/.local/bin/scheduled-task-audit-bookend daily-worktree-triage-and-cleanup start`
- Bash: `sed -n '1,80p' ~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-branch-governance.md 2>/dev/null | grep -n -A...`
- Bash: `awk '/^## 10\./{f=1} f{print} /^## 11\./{if(f)exit}' ~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-branch-...`
- Bash: `LOG_DIR=~/.claude/scheduled-tasks/audit
mkdir -p "$LOG_DIR" 2>/dev/null
if [ -w "$LOG_DIR" ]; then echo "PREFLIGHT: audi...`
- Bash: `# Discover git repos under ~/Workspace and ~/Code (skip _agents, node_modules, __pycache__)
# A git repo has a .git dir/...`
- Bash: `# More thorough repo discovery with prune (faster, deeper) — skip heavy/irrelevant dirs
: > /tmp/wt_repos.txt
for base i...`
- Bash: `cd /tmp
# Dedupe to real repos via common-dir; collect secondary worktrees with full status.
: > /tmp/wt_report.tsv
: > ...`
- Bash: `: > /tmp/wt_secondaries.tsv   # repo \t wt_path \t branch \t locked \t prunable
repos_with_secondaries=0
total_secondary...`
- Bash: `cut -f2 /tmp/wt_secondaries.tsv | sort -u > /tmp/wt_paths.txt
echo "UNIQUE SECONDARY WORKTREE PATHS: $(wc -l < /tmp/wt_p...`
- Bash: `awk -F'\t' '
BEGIN{ sc=0; di=0; lk=0; act=0; sp=0; excl=0 }
{
  path=$1; owner=$2; locked=$4; dirty=$5; unpushed=$6; idl...`
- Bash: `awk -F'\t' '
BEGIN{ sc=0; di=0; sp=0; act=0; ri=0; excl=0 }
{
  path=$1; owner=$2; locked=$4; dirty=$5; unpushed=$6; idl...`
- Bash: `for repo in \
  "/Users/4jp/Workspace/limen-work/conversation-corpus-engine" \
  "/Users/4jp/Code/organvm/organvm-engine...`
- Bash: `awk -F'\t' '
$0 ~ /STALE-PRUNABLE/ { next }
$2=="." { next }   # exclude submodule
{ if($5=="yes") d++; if($4=="yes") l+...`
- Bash: `~/.local/bin/scheduled-task-audit-bookend daily-worktree-triage-and-cleanup end 301-repos-62-worktrees-0-removals-11-dir...`

---

---

## Prompt Summary

**Total prompts:** 1
**Session duration:** ~5 min
**Avg time between prompts:** ~5.0 min

### Prompt Categories (heuristic)

- **Directives** (implement/build/create/add/write): 1
- **Questions**: 0
- **Fixes** (fix/error/bug/broken/fail): 1
- **Reviews** (check/verify/review/audit): 1
