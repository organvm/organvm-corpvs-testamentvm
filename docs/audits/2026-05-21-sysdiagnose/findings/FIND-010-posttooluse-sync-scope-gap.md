# FIND-010: PostToolUse `domus-memory-sync` hook lacks path-scope filter — auto-syncs ANY Write/Edit to chezmoi-source

**Status:** ✅ **FIXED 2026-05-22 18:24 EDT** at commit `602c734` (`Update .local/bin/domus-memory-sync`, +31 / −2 lines). Runtime/source/remote now in parity. Sanity test confirms: out-of-scope paths SKIP correctly (`/tmp/scope-test/fake.md` → `SKIP: out of scope (stdin)`), in-scope paths proceed through the chain.

**Severity:** critical (now resolved)
**Source:** `~/.claude/settings.json` PostToolUse hook chain + `~/.local/bin/domus-memory-sync`
**First seen:** 2026-05-22 03:33 EDT (first commit in audit window)
**Last seen:** 2026-05-22 15:23 EDT (last pre-patch sync; mechanism filtered as of 18:24 EDT)
**Occurrences:** 17 commits within audit window (03:26–03:50 EDT) + ~10 additional commits before patch
**Affected process/component:** Claude Code → PostToolUse hook → `domus-memory-sync` → `chezmoi add` → autoCommit+autoPush
**Affected ORGANVM organ:** META (chezmoi-source ↔ runtime parity layer)

## Evidence

### settings.json hook entries (two)
```
"command": "~/.local/bin/domus-memory-sync",
"timeout": 5
```

### `domus-memory-sync` stdin-path branch (no scope filter)
```bash
elif [[ -n "$stdin_filepath" && -f "$stdin_filepath" ]]; then
  files_to_add+=("$stdin_filepath")
```

The `--all` branch DOES scope to `~/.claude/projects/*/memory/*.md` + `~/.claude/plans/*.md` via `find -path` predicates. The PostToolUse-stdin branch does NOT — it accepts any filepath the hook payload carries.

### Audit window commits (17 files pushed to PUBLIC repo before privatization)
```
Workspace/_diagnostics/sysdiagnose-2026-05-21/REPORT.md
Workspace/_diagnostics/sysdiagnose-2026-05-21/timeline.md
Workspace/_diagnostics/sysdiagnose-2026-05-21/memory-parity.md
Workspace/_diagnostics/sysdiagnose-2026-05-21/findings/FIND-{001..009}-*.md
Workspace/_diagnostics/sysdiagnose-2026-05-21/dispatch-envelopes/DISPATCH-{001,002,005,006}-*.md
private_dot_claude/projects/-Users-[user]/memory/project_artifact_2026_05_22_sysdiagnose_forensic_audit.md
```

### Constitutional violations enabled by the gap
- `feedback_unauthorized_commit_chezmoi` (2026-05-14): "chezmoi-source autoCommit+autoPush does NOT authorize Claude commits; direct Edit/Write requires explicit user ship-it." The PostToolUse hook silently routes ANY Write/Edit to `chezmoi add`, which feeds the autoCommit pipeline — bypassing the explicit-ship-it requirement.
- Bg-subprocess audit brief stated "no commits" as a hard rule. The subprocess obeyed the letter (it never called `git commit`) but the hook chain produced 17 commits anyway, attributed to the user's git identity rather than the subprocess.
- Universal Rule #5 (fix bases not outputs): the bug is in the script's scope filter, not in any individual file. Output-level remediation (deleting committed files) is patching symptoms.

## Interpretation

The hook was designed to satisfy Universal Rule #2 ("nothing local only") by mirroring Claude memory writes + plans to the GitHub remote via chezmoi. The implementation correctly scopes the `--all` mode (probably the original use case), but the stdin-path mode added later (per the script's "CC 2.1.143+ pattern" comment) accepts any filepath without scope-checking. This means any file Claude writes — anywhere on disk — gets `chezmoi add`'d, which copies it into the chezmoi-source tree, which then auto-commits and auto-pushes.

In practice: the bg subprocess wrote 17+ files to `~/Workspace/_diagnostics/...`. Each Write tool call fired the PostToolUse hook with that filepath in stdin JSON. `domus-memory-sync` extracted the path, called `chezmoi add <audit-file>`, chezmoi copied it into `~/Workspace/4444J99/domus-semper-palingenesis/Workspace/_diagnostics/...`, and the autoCommit+autoPush chain pushed it all to GitHub. Within ~20 minutes the entire audit (including a critical security-vulnerability disclosure in FIND-001) was on the public internet.

The exposure window was approximately 03:33–15:30 EDT — roughly 12 hours of public visibility. The repo has since been privatized, but commit SHAs remain in GitHub's cache for ~90 days, and any clones made during the window persist offline.

## Proposed action

- [x] No-op — informational only
- [x] **Draft IRF row** (below)
- [x] **Dispatch envelope** (below — Codex-class mechanical_refactoring)
- [ ] Immediate fix needed — **gated on user authorization** per `feedback_unauthorized_commit_chezmoi`

## Candidate IRF row

**Domain:** SEC (security) + SYS (system) — joint
**Priority:** P0
**Title:** Add path-scope filter to `domus-memory-sync` PostToolUse stdin branch
**Body:**
The PostToolUse hook chain `Write/Edit → domus-memory-sync → chezmoi add → autoCommit → autoPush` silently mirrors any file path Claude writes into the chezmoi-source tree, regardless of intended scope. The `--all` mode of the script scopes correctly to `~/.claude/projects/*/memory/*.md` and `~/.claude/plans/*.md`; the stdin-path mode does not filter at all. Result: a single bg-subprocess audit landed 17 files (including a critical-severity security-vulnerability disclosure with full reproduction details) into a PUBLIC GitHub repo within ~20 minutes, before the repo was retroactively privatized. The fix is a path-scope `case` statement at the top of the stdin-path branch, accepting only files whose path matches the same predicates as `--all`. Out of scope: revising the `--all` branch (already correctly scoped) or changing chezmoi's autoCommit behavior (separate axis).

## Dispatch decision (per `~/.claude/CLAUDE.md` Work-Type matrix)

**Work type:** mechanical_refactoring (path-scope filter added to existing script)
**Recommended agent:** Codex (after Claude designs the predicate)
**Reasoning:** The design decision (which paths constitute valid sync targets) is strategic — Claude. The implementation (bash `case` statement, regex tests) is mechanical — Codex. The fix lives in `dot_local/bin/executable_domus-memory-sync` in the chezmoi-source tree; user must authorize commit per `feedback_unauthorized_commit_chezmoi`.
