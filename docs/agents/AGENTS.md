# Repository Guidelines

Global policy: /Users/4jp/AGENTS.md applies and cannot be overridden.

## Project Structure & Module Organization
This repository is a documentation corpus for the ORGAN I–VII system, not an application codebase. Primary content lives under `docs/` as numbered planning artifacts (for example, `docs/genesis/00-c-master-summary.md`, `docs/planning/01-readme-audit-framework.md`, `docs/planning/05-risk-map-and-sequencing.md`). Active machine-readable state lives in `repo-registry.json` and `.config/organvm.config.json`. Environment templates are in `.config/organvm.env`, while `.config/organvm.env.local` is local-only. The `docs/archive/` directory contains superseded v1 files and should be treated as read-only historical reference.

## Build, Test, and Development Commands
There is no build pipeline; contribution quality comes from validation checks.

```bash
rg --files
```
List tracked project files quickly.

```bash
jq . repo-registry.json > /dev/null
python3 -m json.tool .config/organvm.config.json > /dev/null
```
Validate JSON syntax before committing.

```bash
rg -n "\[.*\]|TODO|TBD" *.md
```
Find unresolved placeholders in documentation.

## Coding Style & Naming Conventions
Use clear, professional Markdown with descriptive headings and short sections. Keep edits specific and avoid broad rewrites of unrelated docs. Follow existing filename patterns: numbered phase documents (`NN-name.md`), versioned artifacts (`*-v2.md`), and stable canonical references (`repo-registry.json`). For org/repo naming, preserve conventions in `.config/organvm.config.json`, including `[organ]-[type]--[specific-name]` (double dash separator).

## Testing Guidelines
Testing is documentation QA:
- Re-score README changes using the rubric in `01-readme-audit-framework.md`.
- Confirm links, examples, and cross-references are still accurate.
- When editing inventory/governance docs, ensure consistency with `repo-registry.json` as the source of truth.

## Commit & Pull Request Guidelines
This repository currently has no established commit history; use Conventional Commit style moving forward (for example, `docs: refine organ-ii README template`, `chore: update registry-v2 statuses`). Keep commits scoped to one document set or one data file. PRs should include: purpose, files changed, decisions made, and any follow-up work.

## Security & Configuration Tips
Do not commit secrets, personal tokens, or private org/account identifiers. Keep local overrides in `.config/organvm.env.local` only. Treat `docs/archive/` as immutable unless a maintainer explicitly requests archival correction.
