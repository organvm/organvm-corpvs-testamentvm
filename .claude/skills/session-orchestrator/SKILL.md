---
name: session-orchestrator
description: Master sequencer for the Phase 0→3 chain. Reads the active handoff envelope at `.conductor/active-handoff.md`, identifies the originating session's declared phase, and surfaces the next unblocked action. Use at session start to orient before doing any work; use again whenever you complete an action and need to know what's next.
---

# session-orchestrator

You are the **master sequencer** for ORGANVM's Phase 0→3 chain. Before doing any other work, you orient the session against the active handoff envelope.

## When to invoke

Use this skill:
- At the very start of a fresh session, before reading any other files
- After completing any P0/P1 action, to confirm the next item
- When the user asks "what's next?" / "where are we?" / "what should I do?"
- When you suspect the session is drifting off the declared phase

## How it works

The orchestrator reads `.conductor/active-handoff.md` and emits a report with:
- **Originating session ID** and declared **phase**
- Count of items the previous session marked complete (`- [x]` checkboxes)
- Ordered list of **open actions**, parsed from the handoff's `### P0/P1/P2 …` blocks
- A single **recommended next action**

## Invocation

```
python3 scripts/organ-cli.py plugin run session-orchestrator
```

Useful flags:
- `--handoff PATH` — use a different envelope (defaults to `.conductor/active-handoff.md`)
- `--json` — machine-readable output for chaining into other plugins

## Phase model

- **Phase 0** — Substrate / Domain Scaffolding (DIWS must precede any session-context or PDE work)
- **Phase 1** — Documentation / Specification
- **Phase 2** — Validation / Micro-validation
- **Phase 3** — Integration / Release

When the parsed phase does not match what you'd infer from the open actions, surface that mismatch to the user before proceeding.

## Composing with other meta-plugins

`session-orchestrator` is the natural first node in the meta-plugin chain. After running it, the recommended downstream sequence is:

1. **`vacuum-radar`** — detect missing/N/A entries
2. **`triple-reference-tracker`** — verify the IRF/repo/GH-issue triple for each action
3. **`atom-logger`** — record what the session did, for the next session's orchestrator

See `IRF-SYS-184` for the full plugin ecosystem design.
