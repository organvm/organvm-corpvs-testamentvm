---
name: triple-reference-tracker
description: Enforce the IRF + repo + GH-issue triple reference for any work atom. Given one or more IRF IDs, verifies that the IRF entry exists, that the repo reference is present, and that a GitHub issue reference (e.g. `GH#353` or `#353`) is in the row. Fails closed — use before starting work on any item to ensure the audit trail is in place.
---

# triple-reference-tracker

You enforce ORGANVM's **triple reference protocol**: every active work atom must be discoverable via three independent paths — the IRF entry, the repo file/commit, and the GitHub issue.

This is not bureaucratic. It is what prevents the system from silently losing track of work in flight. If one of the three is missing, the work is illegible to two-thirds of the audit surfaces.

## When to invoke

Use this skill:
- Before starting work on any IRF item, to confirm the triple is in place
- Before closing a session, to confirm every claimed-DONE has all three references
- When reviewing another agent's session, to verify they honored the protocol
- During CI-equivalent checks for new IRF entries

## How it works

For each IRF ID supplied, the plugin:

1. Searches `INST-INDEX-RERUM-FACIENDARUM.md` for the row
2. Checks the row contains the default repo slug `a-organvm/organvm-corpvs-testamentvm` (or `--repo` override)
3. Looks for `GH#NNN` or `#NNN` pattern in the row
4. Emits a verdict: **OK** (all three) / **MISSING** (one or more missing) / **NOT_FOUND** (no row)

Exit code is **non-zero** if any input ID is not `OK`. This is intentional: triple-reference failure should halt downstream work, not warn.

## Invocation

```
python3 scripts/organ-cli.py plugin run triple-reference-tracker IRF-THE-033
python3 scripts/organ-cli.py plugin run triple-reference-tracker IRF-THE-033 IRF-SYS-184 IRF-SYS-185
python3 scripts/organ-cli.py plugin run triple-reference-tracker IRF-THE-033 --json
python3 scripts/organ-cli.py plugin run triple-reference-tracker IRF-FOO-001 --repo other-org/other-repo
```

## Handling a MISSING verdict

When the verdict is **MISSING**, do not proceed with the work. Instead:

1. If the GH issue is missing — file one (or locate the existing one and append the link to the IRF row)
2. If the repo is missing — add the repo slug to the IRF row's source-column
3. Re-run the tracker to confirm verdict is now **OK**

When the verdict is **NOT_FOUND**, the user has likely typoed the IRF ID; surface this to them rather than silently treating absence as "no work needed."

## Composing with other meta-plugins

- Run **after** `vacuum-radar` on any VACUUM you intend to claim
- Run **before** `atom-logger` — only well-anchored atoms should be logged

See `IRF-SYS-184` for the full plugin ecosystem design.
