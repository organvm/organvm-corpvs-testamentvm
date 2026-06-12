# Session Prompts: 2026-06-11

**Session ID:** `7eef907b-f1a2-4bb3-9ba8-91d975cbeec5`
**Duration:** ~5 min
**Working directory:** `/Users/4jp`
**Prompts:** 19 human messages

---

### P1 — 2026-06-11 12:17:00

<scheduled-task name="daily-repo-hygiene" file="/Users/4jp/.claude/scheduled-tasks/daily-repo-hygiene/SKILL.md">
This is an automated run of a scheduled task. The user is not present to answer questions. For implementation details, execute autonomously without asking clarifying questions — make reasonable choices and note them in your output. "write" actions (e.g. MCP tools that send, post, create, update, or delete), only take them if the task file asks for that specific action. When in doubt, producing a report of what you found is the correct output.

## Version: v1.2.0
## Doctrine: ACTION-BY-DEFAULT. A routine that measures + reports but defers every change is theatre (Rule #4 conductor principle + "done = utilized in reality"). Default to the **reversible** action (archive, not delete) inside an allowlist envelope; only **irreversible/external** ops (push-to-main, delete, send, non-conductor authorship) gate to the conductor. Reporting-instead-of-archiving is the bug, not the feature.
## Status format: `<N>-repos-<U>-unpushed-<O>-orphan-<S>-stale-<P>-pushes-<W>-root-drift-<H>-home-drift` (e.g., `204-repos-3-unpushed-8-orphan-705-stale-0-pushes-0-root-drift-50-home-drift`)

## Metadata
- **Owner:** conductor (`4444J99` / `4444jPPP`)
- **Class:** I (local-token)
- **Cadence:** daily (08:17 EDT)
- **IRF row:** IRF-SYS-212 (Higher Ideal Form migration arc; consolidates 3 prior routines)
- **Depends on:** `git`, `xargs -P 8`; no other routines
- **Audit log path:** `~/.claude/scheduled-tasks/audit/YYYY-MM-DD.log`
- **Conformance:** docs/standards/24 v1.1.0
- **Last semver bump:** 2026-06-05 — v1.1.0 adds Phase F cartridge-drift watch + scratch sweep (mop, not just count; per `~/Workspace/workspace-manifest.json → allowed_root` and session-meta `TRIPTYCH.md` §cartridge). Prior: 2026-05-27 initial v1.0.0 (post-consolidation; merged from `daily-orphan-plans` + `daily-unpushed-commits` + `daily-push-feature-branches` per doc 23 alchemical evolution; those evolved-testaments still queryable)

## Audit log (start — invoke FIRST)
Run: `~/.local/bin/scheduled-task-audit-bookend daily-repo-hygiene start`
Per docs/standards/18 §9, every Class-(I) fire must emit start + end entries regardless of writes.

Operate under `~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-branch-governance.md` Sections 5, 8, 10. **Read it first.**

Universal Rule #2 ("nothing local only") + Universal Rule #5 ("plans are artifacts") drive this task.

## Pre-flight
- Standards doc 17 readable
- Audit log path writable
- Conductor identity: `git config --global user.email` matches `etceter4@etceter4.com` (abort writes if not)

## Procedure

### Phase A: enumerate repos (ONCE)
Walk `~/Workspace/*`, `~/Code/*`, `/Users/4jp/bound`. For each git repo: path, remote URL, current branch, branches list with author emails. Skip submodules, `_agents/`, `node_modules/`, `__pycache__/`. Parallelize fetches with `xargs -P 8`.

### Phase B: ahead/behind report (READ-ONLY)
Per repo's current branch: fetch, `rev-list --left-right --count @{u}...HEAD`, last-commit-date. No-upstream → bucket separately.

Output sorted by ahead-count descending. Sections: "No upstream set", "Behind only".

Highest-signal: ahead>0 AND last-commit >24h old.

### Phase C: orphan-plan classification (READ-ONLY)
Walk `~/.claude/plans/*.md` + every `<repo>/.claude/plans/*.md` from Phase A. Classify Orphaned/Stale/Resolved. Report grouped by repo, Orphaned+Stale only, sorted age descending.

### Phase D: BOUNDED PUSH — feature branches in 4444J99 only (WRITE)
For each repo under `~/Workspace/4444J99/*` with remote `4444J99/<repo>`:
1. Branches matching §5 naming: `feature/*`, `fix/*`, `chore/*`, `refactor/*`, `docs/*`, `perf/*`, `test/*`, `ci/*`, `hotfix/*`
2. HEAD commit author email = conductor's
3. Has upstream, ahead≥1, behind=0, last commit >1h old
4. **Cap: max 5 pushes**

Execute (60s/30s stagger): `git push origin <branch>` (NO `-f`). Skip rejected. Per-action audit.

Excluded: `a-organvm/`, ORGAN-*, no-upstream, non-§5-named branches.

### Phase E: unified report
Combine Phase B + C + D + excluded counts.

### Phase F: cartridge-drift watch + scratch sweep (v1.1.0 — MOP, not just count)
Contract: `~/Workspace/workspace-manifest.json → allowed_root` (doctrine: session-meta `TRIPTYCH.md` §cartridge).

1. **MEASURE** — `<W>` = count of `~/Workspace` root entries (incl. hidden) not in
   `allowed_root.{directories,files,hidden}`; `<H>` = count of non-factory home-root entries:
   `ls ~ | grep -vcE '^(Applications|Desktop|Documents|Downloads|Library|Movies|Music|Pictures|Public)$'`.
   Both land in the end-status string.
2. **SWEEP (archive, never delete)** — any regenerated agent-scratch dir at Workspace root
   (`.claude .codex .gemini .specstory .temp .history .lh .whisper .openhand .recovery _diagnostics _worktrees`)
   moves whole to `~/Workspace/.archive/<YYYY-MM-DD>-janitor-sweep/` with a `.MOVED-TO.md` tombstone
   naming this routine + the origin path. Swept session-bearing content awaits the next session-meta
   absorption pass (TRIPTYCH invariant 4); the tombstone preserves provenance.
3. **NEVER** — touch `allowed_root` entries, `.archive` itself, anything inside a git repo, or the
   home directory beyond counting (`<H>` is measure-only; home absorption is epoch work, not janitor work).
   No `rm` of any non-empty path — archive only. Report swept-dir names in Phase E.

## What this task NEVER does (Section 10 hard-NEVERs)
- Pushes to main/master/develop, pushes outside 4444J99 personal org, force-pushes, sets upstream on first push, pushes branches with non-conductor authorship, moves/removes plan files (Phase C read-only), deletes non-empty paths (Phase F archives only)

## Audit log (end — invoke LAST, after the report)
Run: `~/.local/bin/scheduled-task-audit-bookend daily-repo-hygiene end <status>`
where `<status>` follows format `<N>-repos-<U>-unpushed-<O>-orphan-<S>-stale-<P>-pushes-<W>-root-drift-<H>-home-drift`. Use hyphens; no whitespace.
</scheduled-task>

**Actions taken:**
- Bash: `~/.local/bin/scheduled-task-audit-bookend daily-repo-hygiene start 2>&1; echo "---EXIT: $?---"`
- Bash: `echo "=== conductor identity ==="; git config --global user.email; echo "=== standards doc 17 readable? ==="; test -r ~/...`
- Bash: `echo "=== doc 17 section markers ==="; grep -nE '^#{1,4} ' ~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-b...`
- Bash: `echo "=== allowed_root ==="; python3 -c "import json,sys; d=json.load(open('/Users/4jp/Workspace/workspace-manifest.json...`
- Bash: `sed -n '90,210p' ~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-branch-governance.md`
- Bash: `cd /tmp
# Enumerate top-level git repos under the three roots; prune noise dirs.
roots=(~/Workspace ~/Code /Users/4jp/bo...`
- Bash: `echo "=== ~/Code top ==="; ls -la ~/Code 2>&1 | head; echo "=== ~/Code/organvm ==="; ls ~/Code/organvm 2>&1 | head -30; ...`
- Bash: `CODE_REAL="$(cd ~/Code && pwd -P)"
echo "resolved Code -> $CODE_REAL"
# Catch Code/<repo>/.git and Code/organvm/<repo>/....`
- Bash: `cat /tmp/hygiene_repos.txt /tmp/hygiene_code_repos.txt | while read -r p; do
  [ -d "$p" ] && (cd "$p" 2>/dev/null && pw...`
- Bash: `: > /tmp/hygiene_ahead.tsv
while read -r repo; do
  cd "$repo" 2>/dev/null || continue
  br=$(git symbolic-ref --short -...`
- Bash: `NOW=$(date +%s); DAY=$((NOW-86400))
echo "=== UNPUSHED (ahead>0), sorted by ahead desc ==="
echo "ahead  behind  age(h) ...`
- Bash: `# Gather plan dirs: ~/.claude/plans + every <repo>/.claude/plans
: > /tmp/hygiene_plans.txt
[ -d ~/.claude/plans ] && fi...`
- Bash: `NOW=$(date +%s); D14=$((NOW-14*86400)); D60=$((NOW-60*86400))
# Files with a resolution marker near the top (first 15 li...`
- Bash: `cat /tmp/hygiene_orphaned.tsv /tmp/hygiene_stale.tsv | while IFS=$'\t' read -r age f; do
  # scope = path up to .claude/...`
- Bash: `CONDUCTOR="etceter4@etceter4.com"; NOW=$(date +%s); HR=$((NOW-3600))
echo "=== scanning all branches in ~/Workspace/4444...`
- Bash: `cd ~/Workspace
echo "=== ALL Workspace root entries (incl hidden) ==="
ls -A1 ~/Workspace
echo ""
echo "=== <H> home-roo...`
- Bash: `cd ~/Workspace
python3 - <<'PY'
import json, os
m=json.load(open('/Users/4jp/Workspace/workspace-manifest.json'))['allow...`
- Bash: `STATUS="191-repos-4-unpushed-260-orphan-671-stale-0-pushes-7-root-drift-21-home-drift"
echo "status: $STATUS"
~/.local/b...`

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
