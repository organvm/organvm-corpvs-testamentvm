# ADR-004: Registry as JSON, Not Database

## Status

Accepted

## Date

2026-02-09

## Context

The system needed a single source of truth for all 97 repositories — their organ membership, status, documentation state, and metadata. Three approaches were considered:

1. **Relational database** (PostgreSQL/SQLite): Rich querying, schema enforcement, but requires a runtime dependency and deployment infrastructure
2. **YAML files per repo**: Distributed, easy to edit, but no single view and hard to validate holistically
3. **Single JSON file**: Version-controlled, grep-able, no runtime dependency, atomic commits

The choice needed to support: CI/CD validation workflows, human review via `git diff`, machine parsing by orchestrator agents, and zero infrastructure cost.

## Decision

All repository metadata lives in `repo-registry.json` — a single flat JSON file at the repository root. Schema version 0.5 defines the structure:

- Top-level: `metadata` (schema version, timestamps), `organizations` (per-org config), `repositories` (array of repo entries)
- Each repo entry: `name`, `org`, `implementation_status`, `public`, `description`, `documentation_status`, `portfolio_relevance`
- ORGAN-III repos additionally carry `type` (SaaS/B2B/B2C/internal), `revenue_model`, and `revenue_status`
- `implementation_status` enum: ACTIVE | PROTOTYPE | SKELETON | DESIGN_ONLY | ARCHIVED

The file is validated by `scripts/praxis-validate.py` and CI workflows. Changes are atomic git commits with full diff visibility.

## Consequences

### Positive

- **Zero infrastructure**: No database server, no connection strings, no hosting cost
- **Full version history**: Every registry change is a git commit with diff, author, and timestamp
- **Grep-able**: `grep -c '"ACTIVE"' repo-registry.json` gives instant counts
- **CI-friendly**: Validation scripts run against the file without any runtime dependencies
- **Atomic updates**: A single commit updates the entire system state
- **Portable**: Copy one file and you have the complete system inventory

### Negative

- **No relational queries**: Cross-referencing (e.g., "all ORGAN-III repos with ACTIVE status and SaaS type") requires JSON parsing, not SQL
- **Merge conflicts**: Concurrent registry edits create git conflicts that must be resolved manually
- **Schema evolution is manual**: No migration framework — schema changes require updating the file and all consumers
- **File size grows linearly**: At 97 repos the file is manageable (~50KB); at 1,000 repos this approach would need reconsidering
- **No concurrent writes**: Single-writer assumption — if two workflows update the registry simultaneously, one will conflict

## References

- Registry file: `repo-registry.json`
- Validation: `scripts/praxis-validate.py`
- Schema history: v1 (archived in `docs/archive/`), v2 current (schema 0.5)
- ADR-009 for the VERITAS revenue field split that modified the schema
