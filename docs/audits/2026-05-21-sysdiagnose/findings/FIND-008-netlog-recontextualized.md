# FIND-008: Netlog "healthy idle window" reframed — entry into memory-pressure cascade

**Severity:** info
**Source:** `~/Downloads/claude-netlog-2026-05-20T02-50-07-463Z.json` + unified log slice 2026-05-19 22:49–22:51 + `JetsamEvent-2026-05-19-230502.ips`
**First seen:** 2026-05-19 22:50:07 (netlog start)
**Last seen:** 2026-05-19 23:05:02 (jetsam fired 14 min 55 sec later)
**Occurrences:** 1 corroboration
**Affected process/component:** Claude.app (netlog) → bztransmit (jetsam victim) — different processes; chained context
**Affected ORGANVM organ:** N/A

## Evidence

**Phase 1 netlog framing** (per plan file):
> Window: 18.2 seconds, 2026-05-19 22:50 EDT. Endpoints contacted: one — `browser-intake-us5-datadoghq.com`. Verdict: healthy idle window. No standalone forensic signal.

**Unified-log query for `process == "Claude"` during 22:49–22:51**: zero matches. Confirms Claude.app was indeed idle.

**However**, `JetsamEvent-2026-05-19-230502.ips` shows that **at 23:05:02 — 14 min 55 sec after the netlog quiet window** — jetsam fired with `"largestProcess": "bztransmit"` (Backblaze backup transmit). The host was in memory pressure during the netlog window; Claude.app's calmness was likely *not* an absence of work but a signal that Claude was already swapped out / inactive / suppressed by jetsam-adjacent pressure.

`memoryStatus` from that JetsamEvent shows free=15854 pages (≈248 MB), with anonymous=209439 pages (≈3.3 GB) and compressor running active (477552 pages). This is the same chronic-pressure pattern documented in FIND-005.

## Interpretation
The netlog's "no standalone forensic signal" verdict is correct in isolation but **misleading in context**. The 18-second quiet window was not an idle moment in steady-state — it was the entry to a memory-pressure cascade that culminated in a kernel-jetsam kill within 15 minutes. For future forensic audits: a thin netlog in isolation should prompt a unified-log cross-check on a wider window, not be dismissed as "nothing burning."

This is also a **method finding**: the Phase 1 brief's classification of the netlog as auxiliary was right, but the corroboration step it specified (slice unified log for the same window) was the load-bearing operation. Carrying it out changed the conclusion.

## Proposed action
- [x] No-op (methodological note for the report)
- [x] Draft IRF row (see below)
- [ ] Dispatch envelope
- [ ] Immediate fix needed

## Candidate IRF row
**Domain:** DOC
**Priority:** P3
**Title:** Document "thin netlog ≠ healthy idle" — cross-reference jetsam/swap state
**Body:** Phase 1 of the 2026-05-22 sysdiagnose audit framed the 2026-05-19 22:50 netlog as a "healthy idle window." Cross-reference to JetsamEvent-2026-05-19-230502 shows a jetsam kill 15 min later. Future-proof: in netlog-driven triage, always cross-check unified-log + jetsam events on a ±30-min window before concluding "nothing burning." File this under audit methodology (a-i--skills `forensic-audit` skill if one is later created).

## Dispatch decision
**Work type:** N/A
**Recommended agent:** N/A
**Reasoning:** Methodological note; lives in REPORT.md and the IRF row.
