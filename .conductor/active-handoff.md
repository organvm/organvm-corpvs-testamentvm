# Agent Handoff: Prompt-Registry Re-Ingestion (staged, not yet run)

**From:** Session a80496a1 (Claude, session-meta scope) | **Date:** 2026-06-10 | **Phase:** BUILD staged — interrupted by closeout before the extract run

**Full campaign handoff (fleet state, spend limit, resume map):** `~/bound/findings/2026-06-10-cross-agent-handoff.md` (bound @ `47331cc`). This file covers only the corpus-repo lane.

## Current State
- Branch `fix/ingestion-source-paths` @ `3c9c68a`, pushed, in sync. Contains: SPECSTORY_DIRS repointed to 5 verified post-cutover homes + `snapshot_status_carryover.py`.
- `data/prompt-registry/status-carryover.json` written (3.8MB, 23,710 content-keyed entries; gitignored). Status counts at snapshot: OPEN 14898 / DONE 6361 / ARCHIVED 2012 / CLOSED-NAV 1316 / CLOSED-COMMAND 12 (24,599 atoms).
- Rollback backup intact: `data/prompt-registry/.backup-2026-06-10/` (137MB).
- **Re-ingestion has NOT run.** Registry stale since 2026-04-22.
- Jules session `16163121062509222885` dispatched (2026-06-10 ~22:45 ET) to implement `harvest_opencode()` + `harvest_gemini()` in `extract_all_prompts.py` (verified store schemas inline in the envelope; see bound `findings/2026-06-10-{opencode,gemini}-store-schema.md`). Land it before or after the first re-run — the pipeline can re-run cheaply once it lands.
- Working tree carries OTHER sessions' modifications (AGENTS.md, CLAUDE.md, GEMINI.md, IRF, omega-evidence-map, repo-registry.json) — not this session's; do not sweep-commit.

## Next Actions (SEQUENTIAL — 16GB jetsam machine, never two heavy steps at once)
1. `python3 data/prompt-registry/extract_all_prompts.py` (full rebuild, wholesale overwrite by design).
2. `python3 data/prompt-registry/atomize_prompts.py`.
3. Write + run an apply-carryover script (does not exist yet): join on `"{timestamp}|{sha1(content)}"` against `status-carryover.json`; restore status/produced/priority/priority_score.
4. **Re-redact (IRF-SEC-005, MANDATORY):** rebuilds re-introduce the burned Gmail app-password from raw transcripts. Patterns live in corpus redaction commits `b08fb35` / `3423079` / `482408f`. grep-verify ZERO literals before committing anything.
5. Caches: `prioritize_atoms.py` → `generate_work_queue.py` → `route_atoms.py`.
6. Verify: registry ≥5867 prompts, max timestamp ≈2026-06-10, DONE=6361 / ARCHIVED=2012 preserved. Commit only tracked `.md` derivatives (registry/atoms JSONs are gitignored).

## Risks & Warnings
- `prompt-atoms.json` is a protected file — the rebuild pipeline is the ONLY sanctioned wholesale writer; everything else does targeted edits.
- If the run dies mid-pipeline, restore from `.backup-2026-06-10/` before retrying.
- Claude subagent fan-out is unavailable (monthly spend limit hit 2026-06-10); this pipeline is pure-local CPU and unaffected.
