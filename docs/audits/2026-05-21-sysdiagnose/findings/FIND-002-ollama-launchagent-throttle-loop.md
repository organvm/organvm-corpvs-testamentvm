# FIND-002: Ollama LaunchAgent in throttle loop — restart cycle exhausts launchd

**Severity:** error
**Source:** `spindump.txt:36` + `brew services list` + `~/Library/LaunchAgents/homebrew.mxcl.ollama.plist`
**First seen:** unknown (predates capture; ollama.plist mtime 2026-04-23)
**Last seen:** 2026-05-22 03:26 (live `brew services list` shows `ollama  error  1`)
**Occurrences:** Per spindump.txt, throttled for samples 1-165, briefly recovered 166-176, throttled again 177-1000 of a 1000-sample window — i.e., throttled ~98.4% of the 10-second capture
**Affected process/component:** `/opt/homebrew/opt/ollama/bin/ollama serve`
**Affected ORGANVM organ:** N/A (third-party local-LLM runtime; touches local LLM tooling like Continue/Aider/local-llm-fine-tuning skill)

## Evidence
From `spindump.txt`:
```
Launchd throttled processes:
  homebrew.mxcl.ollama throttled after exit():
    throttled samples 1-165, not throttled samples 166-176,
    throttled samples 177-1000
```

From live `brew services list`:
```
ollama  error  1  [user]  ~/Library/LaunchAgents/homebrew.mxcl.ollama.plist
```

Plist sets `KeepAlive=true` + `RunAtLoad=true` with no `KeepAlive.SuccessfulExit` qualifier — launchd restarts on any exit (including crashes), and Ollama is currently failing to start. Result: ollama crashes → launchd restarts → ollama crashes → launchd applies exponential throttle → wash, rinse, repeat.

## Interpretation
This is the canonical failure shape that Rule #9 was named after: a LaunchAgent that loops on a broken state and eats launchd resources. Ollama may have been broken by a recent update (matches the 2026-05-21 brewup-claude-drift session noting klatexformula deprecation churn) or by macOS 26.5 changes. Either way: the process is throwing exit-1 on every restart, and launchd is the only thing keeping the loop alive. Disabling the LaunchAgent stops the loop without affecting any ORGANVM functionality (ollama isn't a hard dependency anywhere I can verify).

## Proposed action
- [ ] No-op
- [x] Draft IRF row (see below)
- [ ] Dispatch envelope
- [x] **Immediate fix needed** — `brew services stop ollama` — single command, reversible.

## Candidate IRF row
**Domain:** OPS
**Priority:** P2
**Title:** Disable ollama brew-service; ollama serve exit-1-loops + throttles launchd
**Body:** `brew services list` shows `ollama  error  1`; `spindump.txt` confirms 98% throttle during the 10-second capture window. Ollama's `KeepAlive=true` restarts the crash, exhausting launchd. Run `brew services stop ollama`; if user wants Ollama, invoke `ollama serve` on demand from the local-llm-fine-tuning skill. Same Rule #9 pattern as FIND-001 but for a brew-installed plist.

## Dispatch decision
**Work type:** debugging
**Recommended agent:** Claude (strategic — decide if ollama stays at all, given user is on 16GB RAM and the chronic-memory-pressure pattern in FIND-007)
**Reasoning:** This is a 1-line fix, but the question "should ollama exist on this host at all" is strategic. Claude should answer it before touching the plist.
