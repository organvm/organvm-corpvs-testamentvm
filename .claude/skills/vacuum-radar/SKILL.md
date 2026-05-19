---
name: vacuum-radar
description: Real-time VACUUM and N/A detection across the IRF and repo state. Scans `INST-INDEX-RERUM-FACIENDARUM.md` for entries containing the marker "VACUUM", entries whose final column is literally "None" (no closure tag), and high-priority P1 items still open. Use before declaring a session complete; use mid-session to confirm new work is not surfacing new vacuums.
---

# vacuum-radar

You are the **vacuum detector**. ORGANVM's invariants forbid silent gaps — any "missing artifact" or "expected-but-not-present" condition must surface as an IRF entry marked `VACUUM`. This skill enumerates them and counts them.

## When to invoke

Use this skill:
- Before closing a session — confirm no new VACUUMs are open
- After any large refactor or registry change — new gaps may have surfaced
- When the user asks about "open work" or "what's missing"
- As a pre-flight check before commissioning a downstream agent

## What it scans

The plugin walks every IRF row and classifies it. An entry is **open** when its ID is not strikethrough (`~~IRF-XXX-NNN~~`). It then reports three buckets:

1. **Open VACUUM entries** — rows where the summary contains the substring `VACUUM`
2. **Open P1 entries** — rows whose priority cell contains `P1`
3. **Open entries with `None` in the last column** — rows where the closure column is literally `None` (i.e., not yet linked to a successor or completion record)

It also reports the **next DONE-ID** from `data/done-id-counter.json` for sanity.

## Invocation

```
python3 scripts/organ-cli.py plugin run vacuum-radar
```

Useful flags:
- `--json` — machine-readable
- `--fail-on N` — exit non-zero if open VACUUM count exceeds N (default: never fail)

## Reading the output

A healthy state has:
- Open VACUUM count trending down over sessions
- Every P1 either claimed by an agent or marked deferred with rationale
- `None` in last column → at minimum, link to a successor IRF or to "Completed"

If the report shows a VACUUM that surprises you, **investigate before continuing**. Vacuums are the canonical gap between what the system IS and what it NEEDS TO BE; ignoring one is how systems silently regress.

## Composing with other meta-plugins

- Run **after** `session-orchestrator` to see what new gaps the previous session's work surfaced
- Pipe `--json` into a downstream summarizer
- Use `triple-reference-tracker` on any VACUUM you intend to claim, to ensure the triple is in place before work begins

See `IRF-SYS-184` for the full plugin ecosystem design.
