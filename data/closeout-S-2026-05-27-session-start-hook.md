# Closeout: S-2026-05-27 — SessionStart Orientation Hook (workspace--superproject)

**Session:** wire a permanent SessionStart hook for Claude Code on the web in the superproject
**Date:** 2026-05-27 | **Phase:** Complete | **Repo:** `4444J99/workspace--superproject`
**Branch:** `claude/issue-discovery-reporting-C5ZPZ` | **PR:** #4 (draft)

## Scope

Author and permanently wire a `SessionStart` hook so every Claude Code on the web session
in the superproject (a) has the `federation-graph` runtime dependency installed and (b) is
oriented to the IRF with P0/P1 items surfaced for triage. Then follow ORGANVM closeout +
cross-agent-handoff protocols.

## Completed Work

- [x] `.claude/hooks/session-start.sh` — web-gated (`CLAUDE_CODE_REMOTE`), synchronous,
      fail-soft. Installs `pyyaml`; read-only shallow-clones the IRF into `.irf-cache/`
      (30s timeout, `GIT_TERMINAL_PROMPT=0`) and surfaces P0/P1 lines; flags `.irf/outbox/`
      deltas. All inputs env-overridable (`IRF_REMOTE`/`IRF_FILE`/`IRF_CACHE`).
- [x] `.claude/settings.json` — registers the hook under `hooks.SessionStart`.
- [x] `.gitignore` — the superproject is whitelist-based (`*` then re-include);
      `.claude/hooks/`, `.claude/settings.json`, and `.irf/outbox/**` were being silently
      ignored. Added whitelist entries so they are actually tracked. `.irf-cache/` stays
      ignored (runtime artifact).
- [x] `CLAUDE.md` — documented the hook + the `.irf/outbox` propagation contract
      (completion-logging checklist item #9).
- [x] `.irf/outbox/` — queued this closeout, the cross-agent handoff, the IRF delta, and a
      README describing the propagation contract (checklist item #1, via the outbox).
- [x] Draft PR #4 opened against `main`.

## Validation Evidence

| Check | Result |
|-------|--------|
| `json.load(.claude/settings.json)` | valid JSON |
| `CLAUDE_CODE_REMOTE=true ./.claude/hooks/session-start.sh` | exit 0; pyyaml installed; IRF synced; P0/P1 surfaced |
| `python3 -m py_compile scripts/federation-graph.py scripts/test_federation_graph.py` | clean |
| `python3 scripts/test_federation_graph.py` | 14/14 passing |
| `git check-ignore` | hook + settings + outbox now tracked; `.irf-cache/` still ignored |

## Key Decisions

| Decision | Rationale |
|----------|-----------|
| Synchronous (not async) hook | First iteration per session-start-hook skill; guarantees deps before the agent loop runs. Switch to async only if startup latency matters. |
| Fail-soft, no `set -e` | The IRF clone depends on network/scope that may be absent; a hook must never block or fail a session. Every step is guarded and degrades to a printed note. |
| Whitelist `.claude/hooks` + `settings.json` + `.irf/outbox` in `.gitignore` | The repo's `*`-then-re-include `.gitignore` was silently ignoring them — without this the hook would not persist ("wire it permanently"). |
| Queue completions in `.irf/outbox/` rather than editing the IRF | This repo's MCP scope is the `4444J99` org only; the canonical IRF is in `a-organvm`. The hook's own documented mechanism is the protocol-correct path. |

## What's Locked / Not Attempted

- **Canonical IRF / `.conductor/active-handoff.md` / corpus `data/closeout-*`** — in
  `a-organvm/organvm-corpvs-testamentvm`, out of this session's repo scope. Deltas queued in
  `.irf/outbox/` for a write-scoped session.
- **The surfaced P0 items** (e.g. IRF-SYS-087 UMFAS birth) — system-wide governance work,
  not in scope for this hook-wiring session.
- **Async hook mode** — deliberately not enabled.

## Follow-up Items

1. A write-scoped session should propagate `.irf/outbox/` per `.irf/outbox/README.md`, then
   clear the queue.
2. Once PR #4 merges to `main`, all future web sessions in the superproject use the hook.
3. Consider an analogous SessionStart hook for the `portfolio/` submodule (npm deps) if web
   sessions operate there directly.
