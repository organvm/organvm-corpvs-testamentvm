# FIND-009: voice-scorer venv shebang stale after Workspace → Code migration

**Severity:** info
**Source:** discovered during audit close — attempt to invoke `voice-scorer` CLI for REPORT.md scoring
**First seen:** 2026-05-20 (skills-path migration date per `[[feedback_skills_path_coordination]]`)
**Last seen:** 2026-05-22 03:30 (live invocation failure during this audit)
**Occurrences:** 1 — but represents a structural class of drift (see Interpretation)
**Affected process/component:** `~/Code/organvm/vox--architectura-gubernatio/.venv/bin/voice-scorer`
**Affected ORGANVM organ:** ORGAN-IV adjacent (governance / voice-scorer wraps voice-enforcement skill)

## Evidence
```
$ ~/Code/organvm/vox--architectura-gubernatio/.venv/bin/voice-scorer score REPORT.md
(eval): bad interpreter: ~/Workspace/organvm/vox--architectura-gubernatio/.venv/bin/python3.14: no such file or directory

$ head -1 ~/Code/organvm/vox--architectura-gubernatio/.venv/bin/voice-scorer
#!~/Workspace/organvm/vox--architectura-gubernatio/.venv/bin/python3.14

$ ls ~/Code/organvm/vox--architectura-gubernatio/.venv/bin/python*
python  python3  python3.14   # all present — only the script shebang points at the old path
```

The `.venv` directory was created when the repo lived at `~/Workspace/organvm/vox--architectura-gubernatio/`. The repo moved to `~/Code/organvm/...` per the 2026-05-20 skills-path coordination (memory entry `[[feedback_skills_path_coordination]]`, IRF-OPS-059). The CLI script's shebang was baked into the wheel at install time and never refreshed. The MCP path works (uses Python imports, no shebang involved) — only direct CLI invocation breaks.

## Interpretation
Third sibling of the `[[feedback_path_anchored_fix_class]]` pattern: when a literal path is hardcoded across multiple consumers and the underlying location moves, downstream artifacts break in subtle ways. Prior incidents:
- 2026-05-10 — `.git` loss in `a-i--skills`
- 2026-05-16 — broken xattr after move
- 2026-05-20 — chezmoi-template + 3 sibling consumers hardcoded `Workspace/organvm/a-i--skills` (fixed via `code_root` in `.chezmoidata.toml`)

This is the same class but for a *venv shebang* baked at install time — not text-find-and-replaceable, requires recreation. Fix: `cd ~/Code/organvm/vox--architectura-gubernatio && rm -rf .venv && uv venv && uv pip install -e .` (or equivalent for whatever package manager created the venv). This will rewrite the shebang to the current path.

Severity is info, not error, because the MCP path works — voice-enforcement skill continues to function for in-Claude-Code use. CLI users (humans, CI, `voice-scorer check <dir>` batch operations) will hit the broken-shebang error.

## Proposed action
- [x] No-op (documented — fix is one command at user convenience)
- [x] Draft IRF row (see below)
- [ ] Dispatch envelope (could be Codex, but it's a one-command fix for the user)
- [ ] Immediate fix needed

## Candidate IRF row
**Domain:** OPS
**Priority:** P2
**Title:** Recreate voice-scorer venv after Workspace → Code repo migration
**Body:** `~/Code/organvm/vox--architectura-gubernatio/.venv/bin/voice-scorer` has shebang `#!~/Workspace/organvm/vox--architectura-gubernatio/.venv/bin/python3.14` (old path). Direct CLI invocation fails; MCP path works. Fix: `rm -rf ~/Code/organvm/vox--architectura-gubernatio/.venv && cd ~/Code/organvm/vox--architectura-gubernatio && uv venv && uv pip install -e .`. Sibling of IRF-OPS-059 (skills-path coordination). Also instructs `[[feedback_path_anchored_fix_class]]`: scan all `~/Code/organvm/**/.venv/bin/*` shebangs for stale `~/Workspace/organvm/` paths.

## Dispatch decision
**Work type:** mechanical_refactoring
**Recommended agent:** Codex (one-command fix + audit scan)
**Reasoning:** Mechanical and well-scoped; perfect fit for Codex per the Work-Type matrix.
