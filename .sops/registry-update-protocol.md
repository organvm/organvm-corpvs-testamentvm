---
sop: true
name: registry-update-protocol
scope: repo
phase: any
triggers:
  - context:registry-edit
complements: []
overrides: null
---
# Registry Update Protocol

## Purpose

Defines safe editing practices for `repo-registry.json`, the 2,200+ line single source of truth for all repos.

## Procedure

1. **Never overwrite wholesale.** Read existing content and apply targeted edits
2. **Use the CLI**: `organvm registry update <repo> <field> <value>` for single-field changes
3. **Validate after editing**: `organvm registry validate`
4. **Guard rail**: `save_registry()` refuses to write < 50 repos to the production path
5. **Tests must use `tmp_path`** or explicit fixture paths for file-writing operations

## Verification

- `organvm registry validate` exits 0
- `git diff organvm-corpvs-testamentvm/repo-registry.json` shows only intended changes
- No test writes to the production registry path
