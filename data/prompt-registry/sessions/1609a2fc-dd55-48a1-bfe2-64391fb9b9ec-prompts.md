# Session Prompts: 2026-06-04

**Session ID:** `1609a2fc-dd55-48a1-bfe2-64391fb9b9ec`
**Duration:** ~8 min
**Working directory:** `~/Code/euro-trip-2026`
**Prompts:** 23 human messages

---

### P1 — 2026-06-04 11:24:50

git-parity check and closeout

**Actions taken:**
- Skill

---

### P2 — 2026-06-04 11:25:01

Base directory for this skill: ~/.claude/skills/closeout

# /closeout — Session Close-Out Ritual

## When to invoke

- User explicitly says: `/closeout`, "close out", "wrap up", "end the session"
- Before any non-trivial `git push` (the close-out should precede the push)
- When the session has produced 3+ files, plans, or atoms and the user is signaling end

## Six-step protocol

### Step 1 — Inventory session outputs

Run, in parallel where possible:

```bash
# What files did this session create or modify?
git status --short

# What plans were authored in this session?
ls -t ~/.Codex/plans/*.md 2>/dev/null | head -10

# What's the current branch and where does it stand vs origin?
git branch --show-current
git log @{u}.. 2>/dev/null || echo "(no upstream tracking)"
```

Surface a brief inventory table to the user:
- N files modified, M created
- K plans authored this session
- L commits ahead of origin

### Step 2 — Walk back through plans

For each plan authored this session (filter `~/.Codex/plans/*.md` by mtime within session window):

For each plan, classify it as one of:
- **EXECUTED**: contains `DONE-NNN` reference. No action.
- **IN-PROGRESS**: contains `IRF-XXX-NNN` reference but no DONE-NNN. Update its frontmatter to confirm continued status.
- **ABANDONED**: no closure reference, no follow-on commits. Move to `~/.Codex/plans/abandoned/` with a brief abandonment-reason.

Ask the user for ambiguous cases. Do NOT bulk-classify without confirmation — the home-scope AGENTS.md rule "Atoms are permanent — never batch-close" applies to plans-as-artifacts too.

### Step 3 — Walk back through atoms (if applicable)

If `data/prompt-registry/prompt-atoms.json` was touched this session, identify atoms that were closed in this session and confirm their `status` field is updated.

If not (most sessions), skip.

### Step 4 — Verify git state

Cross-check:
- Working tree is clean (no uncommitted changes meant for this session)
- Local main is in sync with origin (or branch tracks correctly)
- No stray exports/temp files in workspace root (`ls ~/Workspace/*.txt` should be empty)

If stray exports exist (the auto-named `2026-MM-DD-NNNNNN-this-session-being-continued-from-a-previous-c.txt` pattern), move them to `~/Documents/session-exports/` or delete if duplicative.

### Step 4.5 — Verify CLAUDE.md autogen freshness (hall-monitor gate)

If the active repo has a `CLAUDE.md` carrying `<!-- ORGANVM:AUTO:START -->` / `<!-- ORGANVM:AUTO:END -->` sentinels, run the gate:

```bash
~/.local/bin/claude-md-autogen-gate
```

If it exits non-zero, the autogen tail is older than 7 days. **Refuse to mark the session as DONE.** Refresh first:

```bash
organvm context sync --write     # autogen sections only
# or
organvm refresh                  # full 10-step pipeline
```

Then re-stage `CLAUDE.md` and commit (the `claude-md-autogen-freshness` pre-commit hook will re-verify), and re-run the gate.

Bypass only with explicit user authorization:

```bash
AUTOGEN_FRESHNESS_THRESHOLD_DAYS=999 ~/.local/bin/claude-md-autogen-gate
```

Pairs with the pre-commit hook (`claude-md-autogen-freshness`); together they catch staleness at both the commit boundary and the session boundary. Root-cause precedent: 32-day autogen-tail staleness traced on 2026-05-16 to `organvm refresh` step 6 soft-failing on `system-system--system: invalid tier 'sovereign'` (closed via schema + validator lockstep edit; see GH `4444J99/domus-semper-palingenesis#30`, IRF-DOM-048).

### Step 5 — Update active-handoff (if exists)

If `.conductor/active-handoff.md` exists in any active repo, update it with:
- What this session accomplished
- What's locked / not-yet-attempted
- What the next session should pick up

This is the cross-session continuity gate.

### Step 6 — Write CLOSEOUT_SUMMARY.md

**Destination depends on session scope:**
- **Project-scoped session** (work is bound to a single repo): write to `<repo>/.<tool>/plans/YYYY-MM-DD-closeout-{slug}.md`. The convention varies per tool: `.codex/` for Codex sessions, `.claude/` for Claude, etc. **Check whether the chosen plans directory is gitignored or tracked** — `git check-ignore -v <path>` answers it cleanly. Tracked directory means Step 7 applies.
- **Cross-project / home-scoped session**: write to `~/.<tool>/plans/YYYY-MM-DD-closeout-{slug}.md`. Chezmoi sync (if active) handles persistence; Step 7 does not apply.

Produce a session-close-out summary with:

```markdown
# Session Close-Out — {date}

## Outputs
- {N} files created, {M} modified
- {K} plans authored: {filenames}
- {L} commits made (SHAs): {sha-list}

## Closure marks
- EXECUTED plans (DONE-NNN refs): {list}
- IN-PROGRESS plans (IRF refs): {list}
- ABANDONED plans (moved): {list}

## Pending
- Uncommitted changes: {if any}
- Unpushed commits: {if any}
- Active handoff: {path if exists}

## Hand-off note for next session
{one-paragraph context for resumability}
```

### Step 7 — Stage tracked artifacts and propose a commit message

This step exists to close the gap that Step 4's "working tree is clean" check exposes whenever Step 5 or Step 6 wrote into a tracked directory. Without it, the closeout itself creates the orphan-plan state the skill was built to prevent — every closeout-summary-as-untracked-file is one more entry against the 90.4% orphan rate.

**Decision tree:**

1. **Were any Step 5/6 artifacts written to a tracked directory of the active repo?**
   `git status --short <artifact-path>` reports `??` (untracked) for tracked-directory-new-file. If so, continue. Otherwise (gitignored destination, home-scoped only), skip Step 7 entirely.

2. **Stage the artifacts:** `git add <artifact-paths>`. Do NOT use `git add -A` — stage only the specific closeout/handoff files, never sweep up unrelated working-tree changes (this aligns with the home-scope rule against `git add -A`).

3. **Propose a commit message** (do NOT commit yet — closeout's authority ends at staging; the conductor performs the commit):

   ```
   docs(plans): closeout + handoff for YYYY-MM-DD session

   Closeout summary at .<tool>/plans/YYYY-MM-DD-closeout-{slug}.md.
   Active-handoff updated at .conductor/active-handoff.md (if tracked).
   Cross-agent handoff at .<tool>/plans/YYYY-MM-DD-handoff-{slug}.md (if produced).
   ```

   Surface this message verbatim to the conductor with the exact `git commit && git push` invocation. The conductor lands it (or routes through their PR workflow — see Rules).

4. **Re-run Step 4's verification** after staging. `git status` should now show the artifacts as staged-not-untracked. The "working tree is clean" attestation in the final closeout summary is then literally true (modulo the staged artifacts, which are the closeout's intentional output, not stray state).

**Why "stage but don't commit":** This honors the existing "never push as part of closeout" rule. Staging is a local-only operation — no network, no remote mutation, no surprise pushes. It preserves the closeout's role as *preparing* for push without performing it, while removing the orphan-plan generation pathway.

## Rules to honor

- **Never batch-close atoms or plans without explicit user confirmation.** Per Universal Rule (memory rule #53): atoms are permanent, never batch-close.
- **Never delete plan files.** Move to `abandoned/` instead, preserving the history (per the plan-discipline section of the home AGENTS.md).
- **Never push as part of closeout** unless user has explicitly authorized push for this session. Closeout's job is to *prepare* for push, not perform it.
- **If the session produced no notable artifacts**, say so and exit cleanly. Closeout is fast on quiet sessions.

## Why this exists

Per `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md`:

> 90.4% of plans are ORPHANED. Of 427 plans in `~/.Codex/plans/`, 386 contain neither a DONE-NNN nor IRF reference. Only 20 (4.7%) are EXECUTED, 21 (4.9%) are IN-PROGRESS.

The orphan rate is a direct artifact of the absence of a close-out ritual. This skill is the ritual.

The cost of skipping is invisible bookkeeping debt: plans accumulate, atoms stay open against doctrine that already encodes them, the system can't programmatically answer "what was done?". The cost of doing it is ~3-5 minutes per session.

## Related

- `docs/evaluation/SELF-REVIEW-MASTER-2026-05-05.md` — Pathology #4: plan-author cadence vastly exceeds plan-execution cadence (21:1)
- `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md` — full data behind the 90.4% orphan rate
- Universal Rule #2: "Nothing local only" — close-out is what makes "nothing local only" achievable per session


ARGUMENTS: git-parity check and closeout

**Actions taken:**
- Bash: `git -C ~/Code/euro-trip-2026 status --short && echo "---branch---" && git -C ~/Code/euro-trip-2026 bra...`
- Bash: `ls -t ~/.Codex/plans/*.md 2>/dev/null | head -10`
- Bash: `find .claude/sessions -type f | head -20 && echo "---ignore-check---" && git check-ignore -v .claude/sessions/ 2>/dev/nu...`
- Bash: `ls ~/Workspace/*.txt 2>/dev/null || echo "(no stray exports in ~/Workspace)" && echo "---claude-plans-dir---" &...`
- AskUserQuestion
- Bash: `echo "=== PROTOCOL: global gitignore ===" && git config --get core.excludesfile && cat "$(git config --get core.excludes...`
- Bash: `echo "=== PRECEDENT: sibling repos with .claude/sessions ===" && for d in ~/Code/*/ ~/Workspace/*/; do...`
- Bash: `git -C ~/Workspace/4444J99 check-ignore -v .claude/sessions && echo "---" && cat ~/Workspace/4444J99/....`
- Bash: `printf '.claude/sessions/\n' >> .gitignore && git check-ignore -v .claude/sessions/ && git status --short`
- Write `~/Code/euro-trip-2026/.claude/plans/2026-06-04-closeout-git-parity-check.md`
- Bash: `git add .gitignore .claude/plans/2026-06-04-closeout-git-parity-check.md && git status --short && echo "---" && git diff...`

---

### P3 — 2026-06-04 11:30:19 (+5m)

commit and push

**Actions taken:**
- Bash: `git commit -m "docs(plans): closeout + git-parity fix for 2026-06-04 session

Closeout summary at .claude/plans/2026-06-...`
- Bash: `git status -sb && git log --oneline -1 @{u}`

---

### P4 — 2026-06-04 11:31:29 (+1m)

<command-message>closeout</command-message>
<command-name>/closeout</command-name>

### P5 — 2026-06-04 11:31:29

Base directory for this skill: ~/.claude/skills/closeout

# /closeout — Session Close-Out Ritual

## When to invoke

- User explicitly says: `/closeout`, "close out", "wrap up", "end the session"
- Before any non-trivial `git push` (the close-out should precede the push)
- When the session has produced 3+ files, plans, or atoms and the user is signaling end

## Six-step protocol

### Step 1 — Inventory session outputs

Run, in parallel where possible:

```bash
# What files did this session create or modify?
git status --short

# What plans were authored in this session?
ls -t ~/.Codex/plans/*.md 2>/dev/null | head -10

# What's the current branch and where does it stand vs origin?
git branch --show-current
git log @{u}.. 2>/dev/null || echo "(no upstream tracking)"
```

Surface a brief inventory table to the user:
- N files modified, M created
- K plans authored this session
- L commits ahead of origin

### Step 2 — Walk back through plans

For each plan authored this session (filter `~/.Codex/plans/*.md` by mtime within session window):

For each plan, classify it as one of:
- **EXECUTED**: contains `DONE-NNN` reference. No action.
- **IN-PROGRESS**: contains `IRF-XXX-NNN` reference but no DONE-NNN. Update its frontmatter to confirm continued status.
- **ABANDONED**: no closure reference, no follow-on commits. Move to `~/.Codex/plans/abandoned/` with a brief abandonment-reason.

Ask the user for ambiguous cases. Do NOT bulk-classify without confirmation — the home-scope AGENTS.md rule "Atoms are permanent — never batch-close" applies to plans-as-artifacts too.

### Step 3 — Walk back through atoms (if applicable)

If `data/prompt-registry/prompt-atoms.json` was touched this session, identify atoms that were closed in this session and confirm their `status` field is updated.

If not (most sessions), skip.

### Step 4 — Verify git state

Cross-check:
- Working tree is clean (no uncommitted changes meant for this session)
- Local main is in sync with origin (or branch tracks correctly)
- No stray exports/temp files in workspace root (`ls ~/Workspace/*.txt` should be empty)

If stray exports exist (the auto-named `2026-MM-DD-NNNNNN-this-session-being-continued-from-a-previous-c.txt` pattern), move them to `~/Documents/session-exports/` or delete if duplicative.

### Step 4.5 — Verify CLAUDE.md autogen freshness (hall-monitor gate)

If the active repo has a `CLAUDE.md` carrying `<!-- ORGANVM:AUTO:START -->` / `<!-- ORGANVM:AUTO:END -->` sentinels, run the gate:

```bash
~/.local/bin/claude-md-autogen-gate
```

If it exits non-zero, the autogen tail is older than 7 days. **Refuse to mark the session as DONE.** Refresh first:

```bash
organvm context sync --write     # autogen sections only
# or
organvm refresh                  # full 10-step pipeline
```

Then re-stage `CLAUDE.md` and commit (the `claude-md-autogen-freshness` pre-commit hook will re-verify), and re-run the gate.

Bypass only with explicit user authorization:

```bash
AUTOGEN_FRESHNESS_THRESHOLD_DAYS=999 ~/.local/bin/claude-md-autogen-gate
```

Pairs with the pre-commit hook (`claude-md-autogen-freshness`); together they catch staleness at both the commit boundary and the session boundary. Root-cause precedent: 32-day autogen-tail staleness traced on 2026-05-16 to `organvm refresh` step 6 soft-failing on `system-system--system: invalid tier 'sovereign'` (closed via schema + validator lockstep edit; see GH `4444J99/domus-semper-palingenesis#30`, IRF-DOM-048).

### Step 5 — Update active-handoff (if exists)

If `.conductor/active-handoff.md` exists in any active repo, update it with:
- What this session accomplished
- What's locked / not-yet-attempted
- What the next session should pick up

This is the cross-session continuity gate.

### Step 6 — Write CLOSEOUT_SUMMARY.md

**Destination depends on session scope:**
- **Project-scoped session** (work is bound to a single repo): write to `<repo>/.<tool>/plans/YYYY-MM-DD-closeout-{slug}.md`. The convention varies per tool: `.codex/` for Codex sessions, `.claude/` for Claude, etc. **Check whether the chosen plans directory is gitignored or tracked** — `git check-ignore -v <path>` answers it cleanly. Tracked directory means Step 7 applies.
- **Cross-project / home-scoped session**: write to `~/.<tool>/plans/YYYY-MM-DD-closeout-{slug}.md`. Chezmoi sync (if active) handles persistence; Step 7 does not apply.

Produce a session-close-out summary with:

```markdown
# Session Close-Out — {date}

## Outputs
- {N} files created, {M} modified
- {K} plans authored: {filenames}
- {L} commits made (SHAs): {sha-list}

## Closure marks
- EXECUTED plans (DONE-NNN refs): {list}
- IN-PROGRESS plans (IRF refs): {list}
- ABANDONED plans (moved): {list}

## Pending
- Uncommitted changes: {if any}
- Unpushed commits: {if any}
- Active handoff: {path if exists}

## Hand-off note for next session
{one-paragraph context for resumability}
```

### Step 7 — Stage tracked artifacts and propose a commit message

This step exists to close the gap that Step 4's "working tree is clean" check exposes whenever Step 5 or Step 6 wrote into a tracked directory. Without it, the closeout itself creates the orphan-plan state the skill was built to prevent — every closeout-summary-as-untracked-file is one more entry against the 90.4% orphan rate.

**Decision tree:**

1. **Were any Step 5/6 artifacts written to a tracked directory of the active repo?**
   `git status --short <artifact-path>` reports `??` (untracked) for tracked-directory-new-file. If so, continue. Otherwise (gitignored destination, home-scoped only), skip Step 7 entirely.

2. **Stage the artifacts:** `git add <artifact-paths>`. Do NOT use `git add -A` — stage only the specific closeout/handoff files, never sweep up unrelated working-tree changes (this aligns with the home-scope rule against `git add -A`).

3. **Propose a commit message** (do NOT commit yet — closeout's authority ends at staging; the conductor performs the commit):

   ```
   docs(plans): closeout + handoff for YYYY-MM-DD session

   Closeout summary at .<tool>/plans/YYYY-MM-DD-closeout-{slug}.md.
   Active-handoff updated at .conductor/active-handoff.md (if tracked).
   Cross-agent handoff at .<tool>/plans/YYYY-MM-DD-handoff-{slug}.md (if produced).
   ```

   Surface this message verbatim to the conductor with the exact `git commit && git push` invocation. The conductor lands it (or routes through their PR workflow — see Rules).

4. **Re-run Step 4's verification** after staging. `git status` should now show the artifacts as staged-not-untracked. The "working tree is clean" attestation in the final closeout summary is then literally true (modulo the staged artifacts, which are the closeout's intentional output, not stray state).

**Why "stage but don't commit":** This honors the existing "never push as part of closeout" rule. Staging is a local-only operation — no network, no remote mutation, no surprise pushes. It preserves the closeout's role as *preparing* for push without performing it, while removing the orphan-plan generation pathway.

## Rules to honor

- **Never batch-close atoms or plans without explicit user confirmation.** Per Universal Rule (memory rule #53): atoms are permanent, never batch-close.
- **Never delete plan files.** Move to `abandoned/` instead, preserving the history (per the plan-discipline section of the home AGENTS.md).
- **Never push as part of closeout** unless user has explicitly authorized push for this session. Closeout's job is to *prepare* for push, not perform it.
- **If the session produced no notable artifacts**, say so and exit cleanly. Closeout is fast on quiet sessions.

## Why this exists

Per `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md`:

> 90.4% of plans are ORPHANED. Of 427 plans in `~/.Codex/plans/`, 386 contain neither a DONE-NNN nor IRF reference. Only 20 (4.7%) are EXECUTED, 21 (4.9%) are IN-PROGRESS.

The orphan rate is a direct artifact of the absence of a close-out ritual. This skill is the ritual.

The cost of skipping is invisible bookkeeping debt: plans accumulate, atoms stay open against doctrine that already encodes them, the system can't programmatically answer "what was done?". The cost of doing it is ~3-5 minutes per session.

## Related

- `docs/evaluation/SELF-REVIEW-MASTER-2026-05-05.md` — Pathology #4: plan-author cadence vastly exceeds plan-execution cadence (21:1)
- `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md` — full data behind the 90.4% orphan rate
- Universal Rule #2: "Nothing local only" — close-out is what makes "nothing local only" achievable per session


**Actions taken:**
- Bash: `git status -sb && git log --oneline -1 && ls ~/Workspace/*.txt 2>/dev/null || echo "(no stray exports)"`

---

### P6 — 2026-06-04 11:32:10

<local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>

### P7 — 2026-06-04 11:32:10

<command-name>/exit</command-name>
            <command-message>exit</command-message>
            <command-args></command-args>

### P8 — 2026-06-04 11:32:10

<local-command-stdout>See ya!</local-command-stdout>

---

## Prompt Summary

**Total prompts:** 8
**Session duration:** ~8 min
**Avg time between prompts:** ~1.0 min

### Prompt Categories (heuristic)

- **Directives** (implement/build/create/add/write): 2
- **Questions**: 2
- **Fixes** (fix/error/bug/broken/fail): 2
- **Reviews** (check/verify/review/audit): 3
