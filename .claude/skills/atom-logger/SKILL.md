---
name: atom-logger
description: Append structured work atom records for completed, modified, discovered, or deferred work. Use after a meaningful unit of work needs IRF-anchored session logging.
---

# atom-logger

You append **work-atom records** to the prompt registry. An atom is one self-contained unit of work — granular enough that future sessions can grep for it and large enough that it represents a deliverable, not a keystroke.

## When to invoke

Use this skill:
- After closing an IRF item (kind=`closed`)
- After creating a new artifact (kind=`created`)
- After modifying an existing artifact in a non-trivial way (kind=`modified`)
- After discovering a new work item that wasn't in the handoff (kind=`discovered`)
- After explicitly deciding to defer something (kind=`deferred`)

Do **not** use for noise — line edits, formatting fixes, exploratory reads. Atoms must be readable as a session's deliverables, not as a keystroke log.

## How it works

The plugin builds a JSON record with:
- `atom_id` — derived SHA-1 prefix from the canonical payload
- `irf_id` — the IRF entry this atom anchors against
- `session_id` — the session producing the atom
- `title` — one-line description
- `kind` — one of {`created`, `modified`, `closed`, `discovered`, `deferred`}
- `tags` — freeform list
- `created_at` — UTC ISO-8601 timestamp

It appends one JSON line to `data/atoms/atomized-tasks.jsonl`.

## Invocation

```
python3 scripts/organ-cli.py plugin run atom-logger \
    --irf IRF-SYS-184 \
    --session S-2026-05-19-pick-abc \
    --title "Implement 4 meta-plugins" \
    --kind closed \
    --tags python skills plugins
```

Useful flags:
- `--dry-run` — print the atom to stdout but do not append
- `--target PATH` — override the default sink

## Discipline

- **One atom per deliverable.** Resist "summary atoms" that bundle multiple deliverables; future searches lose precision.
- **Always anchor to an IRF ID.** An atom without an IRF anchor is a free-floating work unit and is invisible to the governance machinery.
- **Run `triple-reference-tracker` first** if you're unsure whether the IRF anchor is well-formed.

## Composing with other meta-plugins

- Typically the **terminal** plugin in the meta-plugin chain — runs after the work is done
- Output is consumed by `vacuum-radar` (for next-session orientation) and downstream metrics
- Repeated logging from the same session produces a session log; final entry should be `kind=closed` anchored to the session's handoff IRF

See `IRF-SYS-184` for the full plugin ecosystem design.
