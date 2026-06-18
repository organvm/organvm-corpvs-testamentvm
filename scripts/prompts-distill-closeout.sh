#!/usr/bin/env bash
# prompts-distill-closeout.sh — leak-safe wrapper for Session Review Protocol step 4.
#
# Resolves IRF-DST-004 / GH#352 (with IRF-SYS-241 leak-safety).
#
# PROBLEM
#   The auto-generated Session Review Protocol tells operators to run
#       organvm prompts distill --dry-run
#   at closeout. But `distill` defaults to reading <atoms-dir>/clipboard-prompts.json,
#   and nothing generates that file by default. Its real precursor,
#   `organvm prompts clipboard`, writes a DIFFERENT filename
#   (ai-prompts-clipboard-export.json) to an UNSAFE, CWD-relative default location.
#   So the documented bare command always fails with "Input file not found,"
#   producing a blocked closeout check with no first-class precondition — and running
#   `clipboard` naively can deposit ~1100 personal prompts (multi-MB) into a tracked repo.
#
# FIX
#   Chain the two commands with explicit, ALIGNED I/O paths routed through a PRIVATE,
#   untracked cache (~/.cache/organvm-heartbeat) — the same route the daily heartbeat
#   uses (DONE-566). This NEVER writes clipboard data into this repo. It also degrades
#   gracefully: if the CLI or the clipboard precondition is unavailable, it prints a
#   machine-readable status and exits 0, so closeout stays informational and never
#   hard-blocks a session.
#
# USAGE
#   bash scripts/prompts-distill-closeout.sh            # dry-run (default)
#   bash scripts/prompts-distill-closeout.sh --write    # emit the coverage report
#
# ENV
#   ORGANVM_CLOSEOUT_CACHE   override the private cache dir (default ~/.cache/organvm-heartbeat)

# Note: NO `set -e` — we deliberately control exit codes so the closeout never aborts a
# session on a missing precondition.
set -uo pipefail

MODE="--dry-run"
if [[ "${1:-}" == "--write" ]]; then
  MODE="--write"
fi

# PRIVATE cache — never git- nor chezmoi-tracked. Personal clipboard data lives only here.
CACHE_DIR="${ORGANVM_CLOSEOUT_CACHE:-$HOME/.cache/organvm-heartbeat}"
EXPORT_FILE="$CACHE_DIR/ai-prompts-clipboard-export.json"   # clipboard's native filename
DISTILL_INPUT="$CACHE_DIR/clipboard-prompts.json"           # the filename distill expects

status() { printf '[prompts-distill-closeout] %s\n' "$*"; }

# Precondition 1: the CLI must be installed.
if ! command -v organvm >/dev/null 2>&1; then
  status "PRECONDITION_UNMET: organvm CLI not found on PATH — skipping distill (closeout informational only)."
  exit 0
fi

mkdir -p "$CACHE_DIR"

# Step A — export clipboard prompts to the PRIVATE cache (never the repo).
status "Generating clipboard export → $CACHE_DIR (private, untracked)"
if ! organvm prompts clipboard --output-dir "$CACHE_DIR" >/dev/null 2>&1; then
  status "PRECONDITION_UNMET: 'organvm prompts clipboard' failed (no clipboard history?) — skipping distill."
  exit 0
fi

# Step B — align the filename distill reads to the file clipboard wrote.
if [[ -f "$EXPORT_FILE" ]]; then
  cp -f "$EXPORT_FILE" "$DISTILL_INPUT"
else
  # Fall back to the most recent JSON the clipboard command produced.
  found="$(ls -t "$CACHE_DIR"/*.json 2>/dev/null | head -1)"
  if [[ -z "$found" ]]; then
    status "PRECONDITION_UNMET: clipboard produced no JSON export in $CACHE_DIR — skipping distill."
    exit 0
  fi
  cp -f "$found" "$DISTILL_INPUT"
fi

# Step C — run distill against the aligned, private input.
status "Running: organvm prompts distill --input <cache>/clipboard-prompts.json $MODE"
organvm prompts distill --input "$DISTILL_INPUT" "$MODE"
rc=$?
if [[ $rc -ne 0 ]]; then
  status "distill exited $rc"
fi
exit $rc
