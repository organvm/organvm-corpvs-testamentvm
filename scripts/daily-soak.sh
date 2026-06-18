#!/usr/bin/env bash
set -euo pipefail

# Daily soak test snapshot collector
# Runs soak-test-monitor.py collect, commits, and pushes the result.
# Designed to be called by launchd (com.4jp.organvm.soak-snapshot.plist).

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$HOME/System/Logs"
LOG_FILE="$LOG_DIR/soak-snapshot.log"
DATE="$(date +%Y-%m-%d)"

mkdir -p "$LOG_DIR"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

log "=== Soak snapshot starting for $DATE ==="

cd "$REPO_DIR"

# Pull latest to avoid conflicts
git pull --rebase --quiet >> "$LOG_FILE" 2>&1 || log "WARN: git pull failed, continuing"

# Run the collector
if /opt/homebrew/bin/python3 scripts/soak-test-monitor.py collect >> "$LOG_FILE" 2>&1; then
  log "Snapshot collected successfully"
else
  log "WARN: Snapshot collection had issues (exit code $?), committing anyway"
fi

# Temporal staging (IRF-RES-013): validate the previous state under current rules.
# Informational and non-blocking — staging only the prior snapshot, so it must run
# with --before today's date. Surfaces rule drift; never aborts the soak.
if /opt/homebrew/bin/python3 scripts/temporal-staging-validator.py check --before "$DATE" >> "$LOG_FILE" 2>&1; then
  log "Temporal staging check passed (previous state valid under current rules)"
else
  log "WARN: Temporal staging detected rule drift — see report"
fi

SNAPSHOT_FILE="data/soak-test/daily-${DATE}.json"
TEMPORAL_REPORT="data/soak-test/temporal-staging-latest.json"

if [[ -f "$SNAPSHOT_FILE" ]]; then
  git add "$SNAPSHOT_FILE"
  [[ -f "$TEMPORAL_REPORT" ]] && git add "$TEMPORAL_REPORT"
  if git diff --cached --quiet; then
    log "No changes to commit (snapshot already existed)"
  else
    git commit -m "chore(soak): daily snapshot $DATE" >> "$LOG_FILE" 2>&1
    git push >> "$LOG_FILE" 2>&1 || log "WARN: git push failed"
    log "Snapshot committed and pushed"
  fi
else
  log "ERROR: Snapshot file not created: $SNAPSHOT_FILE"
fi

log "=== Soak snapshot complete ==="
