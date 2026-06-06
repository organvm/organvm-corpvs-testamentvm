# ADR-019: Rename `registry-v2.json` → `repo-registry.json` (Self-Describing Name)

## Status

Accepted

## Date

2026-06-06

## Context

The single source of truth for all repositories was historically named
`registry-v2.json`. The `-v2` suffix encodes *version lineage* (it succeeded an
earlier `registry.json`/v1 shape), not *function*. A reader encountering the
filename learns only that it is "the second version of a registry" — nothing
about what the registry indexes.

The canonical name must describe function, not history: this file is the
**portfolio repo registry** — the index of every repository across all organs,
their organ membership, status, dependency edges, and metadata. Version lineage
belongs in git history and the `metadata.schema_version` field inside the file,
not in the filename.

This is a **rename + reference-update wave only**. The file content is PROTECTED
and remains byte-identical (same blob hash) through the move.

## Decision

1. `registry-v2.json` is renamed to **`repo-registry.json`** via `git mv`
   (content untouched — verified byte-identical).
2. A relative symlink `registry-v2.json → repo-registry.json` is committed
   alongside it. Git tracks symlinks (mode `120000`), so **every existing
   reader that opens `registry-v2.json` keeps working** — no consumer breaks at
   cutover.
3. **All live code and live documentation** inside this repo are updated to
   reference `repo-registry.json` directly: `scripts/*.py`, `.github/workflows/*.yml`
   (including `push`/`pull_request` path-trigger filters), `.config/organvm.env`,
   standards, ADRs, specs, essays, READMEs, and indices.
4. **Historical and dated artifacts are left untouched** — session transcripts,
   prompt-registry snapshots, dated audit/closeout reports, validation-run
   captures, fossil records, and the provenance registry. These are records of
   what was true at their write-time; rewriting them would falsify the record
   (No-Deletion / alchemical-evolution principle, Standard 23).

## The Rule (for all new code)

> New code and new docs reference **`repo-registry.json`** only. The
> `registry-v2.json` symlink exists solely as a backward-compatibility breadcrumb
> for legacy readers; do not introduce new references to it.

## Consequences

### Positive

- **Self-describing**: the filename now states what the file *is* (the repo
  registry), not which version it happens to be.
- **Zero-break cutover**: the committed symlink keeps every legacy reader,
  external fetch fallback, and bookmark working during the transition.
- **Function over lineage**: aligns with Standard 22 (essence-function naming).

### Negative / Trade-offs

- A symlink remains at the old path. It is a deliberate breadcrumb, not drift;
  it can be retired in a future wave once no legacy reader resolves it.
- A future repo (`organvm-iv-taxis/orchestration-start-here`) that hosts a
  central-registry mirror must also adopt `repo-registry.json` for the
  `validate-dependencies.yml` central fetch to hit the new name directly; until
  then the workflow's local fallback resolves the renamed file.

## References

- ADR-004 (Registry as JSON, Not Database) — establishes the file's role
- Standard 22 (essence-function naming convention)
- Standard 23 (no-deletion principle / alchemical evolution)
- `.sops/registry-update-protocol.md` (safe-editing protocol for the registry)
