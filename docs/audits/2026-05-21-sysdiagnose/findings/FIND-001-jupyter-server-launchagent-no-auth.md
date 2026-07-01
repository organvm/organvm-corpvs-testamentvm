# FIND-001: Jupyter Server LaunchAgent — unauthenticated code execution on port 8888

**Severity:** critical
**Source:** `~/Library/LaunchAgents/com.jupyter.server.plist` (created 2026-05-17)
**First seen:** 2026-05-17 21:27 (plist mtime)
**Last seen:** 2026-05-22 03:26 (live ps shows PID 1016 running with these args)
**Occurrences:** Persistent — KeepAlive=true, RunAtLoad=true
**Affected process/component:** `~/.local/share/uv/tools/jupyter-core/bin/jupyter-server`
**Affected ORGANVM organ:** infrastructure (jupyter MCP server depends on this)

## Evidence

Plist content:
```xml
<key>ProgramArguments</key>
<array>
    <string>~/.local/share/uv/tools/jupyter-core/bin/jupyter-server</string>
    <string>--no-browser</string>
    <string>--port=8888</string>
    <string>--IdentityProvider.token=</string>            <!-- EMPTY TOKEN -->
    <string>--ServerApp.allow_origin=*</string>          <!-- WILDCARD CORS -->
    <string>--ServerApp.disable_check_xsrf=True</string> <!-- XSRF DISABLED -->
</array>
<key>RunAtLoad</key><true/>
<key>KeepAlive</key><true/>
```

Live confirmation:
```
[user]  1016  0.1  0.2 435393024  39488  ??  S  1:01AM  0:03.80
  ~/.local/share/uv/tools/jupyter-core/bin/python
  jupyter-server --no-browser --port=8888
  --IdentityProvider.token=
  --ServerApp.allow_origin=*
  --ServerApp.disable_check_xsrf=True
```

Capture-time correlation: `top.txt` shows PID 68290 (then-active jupyter-server) as the parent of ~50 sleeping `python3.11` workers, each a Jupyter kernel that was never reaped — uniform 57M resident, 14 threads. This is a leak compounded by the auth issue.

## Interpretation

This is the highest-severity finding in the audit. Three independent ways this is dangerous:

1. **Rule #9 violation (constitutional).** The user's accumulated rule #55 says *"No LaunchAgents — every incident froze/broke the machine. On-demand CLI only. HARD RULE."* This plist creates an always-on, always-restarted process that the user did not author intentionally as durable infrastructure — it was likely created to back the `jupyter` MCP server but should be on-demand or a `brew services`-style optional surface, not a `KeepAlive` LaunchAgent.
2. **Critical security exposure.** With `--IdentityProvider.token=` (empty), `--ServerApp.allow_origin=*`, and `--ServerApp.disable_check_xsrf=True`, port 8888 accepts arbitrary code execution from any origin with no authentication. Even if firewalled from the LAN, a malicious web page in any browser tab on this machine can issue `fetch('http://localhost:8888/api/kernels', { method: 'POST', ... })` and execute Python with the user's permissions. DNS rebinding bypasses any same-origin protection.
3. **Resource leak.** The capture-time process snapshot shows ~50 zombie `ipykernel_launcher` children that have outlived their MCP sessions. Each holds 57M resident — ~2.8 GB of dead Python kernels accumulating into the chronic memory pressure documented in FIND-007.

## Proposed action
- [ ] No-op
- [x] Draft IRF row (see below)
- [x] Dispatch envelope (see below)
- [x] **Immediate fix needed** — at minimum: `launchctl unload ~/Library/LaunchAgents/com.jupyter.server.plist && mv ~/Library/LaunchAgents/com.jupyter.server.plist ~/Library/LaunchAgents/.disabled-com.jupyter.server.plist`. Audit cannot perform this; it's a destructive action outside read-only scope.

## Candidate IRF row
**Domain:** SEC
**Priority:** P0
**Title:** Replace KeepAlive Jupyter LaunchAgent with on-demand model; add auth token
**Body:** `com.jupyter.server.plist` runs jupyter-server on port 8888 with no token, wildcard CORS, and XSRF disabled — arbitrary local-code-execution exposure via any browser tab on the host. Also violates Universal Rule #9 (no LaunchAgents). Replace with either (a) `brew services start jupyter` invoked on-demand from MCP server startup, or (b) an `organvm jupyter start` CLI subcommand. In either case, generate a per-session token, bind to `127.0.0.1` only, and re-enable XSRF. The ~50 leaked ipykernel children at capture time confirm the LaunchAgent is also a slow resource leak.

## Dispatch decision (per ~/.claude/CLAUDE.md Work-Type matrix)
**Work type:** debugging + architecture
**Recommended agent:** Claude (strategic — auth model + on-demand vs always-on architecture decision)
**Reasoning:** Security architecture and Rule #9 remediation. The plist removal is mechanical (Codex-class) but the replacement-design decision is strategic. Dispatch envelope below for the mechanical follow-up after Claude designs the replacement.
