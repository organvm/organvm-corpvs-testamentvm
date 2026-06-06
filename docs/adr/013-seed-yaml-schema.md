# ADR-013: Seed.yaml Schema and Autonomous Discovery

## Status

Accepted

## Date

2026-02-13

## Context

The orchestrator-agent workflow needs to build a system graph — understanding how 97 repos relate to each other, what each repo produces and consumes, and which autonomous agents operate within each repo. This information was originally scattered across READMEs, registry entries, and tribal knowledge.

The system needed a **self-describing metadata format** that:
1. Lives in each repo (not centralized) — so repos can be discovered independently
2. Declares what the repo produces and consumes (for dependency graph construction)
3. Describes autonomous agents operating within the repo (for the orchestrator to coordinate)
4. Is machine-parseable but human-editable (YAML, not binary)
5. Can be deployed to all 82 eligible repos without manual customization per repo

## Decision

### Schema: seed.yaml v1.0

Every non-archived, non-.github repo contains a `seed.yaml` at its root with this schema:

```yaml
schema_version: "1.0"
organ: "ORGAN-N"
org: "organvm-n-suffix"
repo: "repo-name"
metadata:
  status: "ACTIVE"
  type: "library|application|documentation|..."
agents: []  # List of autonomous agents in this repo
produces:
  - type: "artifact-type"
    description: "What this repo outputs"
consumes:
  - type: "artifact-type"
    from: "source-repo-or-organ"
    description: "What this repo needs"
subscriptions:
  - event: "event-type"
    source: "source-repo"
```

### Deployment Strategy

- `scripts/generate-seed-yaml.py` generates seed.yaml files for all eligible repos using repo-registry.json as the source
- During SENSORIA sprint, deployed to 41 repos that were missing seed.yaml (50%→100% coverage)
- For repos without specific cross-repo dependencies, organ-level produces/consumes are used (e.g., "ORGAN-II produces creative-artifact, consumes theory from ORGAN-I")

### Consumer: Orchestrator Agent

The `orchestrator-agent.yml` workflow (Mon 07:00 UTC) clones all seed.yaml files across the system and builds a unified dependency graph. This graph feeds into the system-pulse-weekly report and dashboard.

## Consequences

### Positive

- **Self-describing repos**: Each repo declares its own interfaces without relying on central registry alone
- **Autonomous discovery**: New repos are automatically discovered when their seed.yaml appears
- **Decentralized truth**: The registry knows *about* repos; seed.yaml knows *within* repos — complementary views
- **100% coverage**: All 82 eligible repos have seed.yaml (achieved Sprint 32 SENSORIA)
- **Machine-readable**: Orchestrator agents can parse YAML natively without custom parsing logic

### Negative

- **Dual source of truth risk**: seed.yaml and repo-registry.json can drift. The registry is authoritative; seed.yaml is declarative.
- **Generic organ-level declarations**: 34 repos with no specific cross-repo dependencies got organ-level produces/consumes — accurate but not granular
- **Maintenance burden**: seed.yaml files must be updated when repos change their interfaces
- **Schema evolution**: Changing the seed.yaml schema requires updating 82 files across 8 orgs — a batch operation

## References

- Generator: `scripts/generate-seed-yaml.py`
- Orchestrator consumer: `orchestrator-agent.yml` in orchestration-start-here
- SENSORIA sprint (100% deployment): `docs/specs/sprints/32-sensoria.md`
- Schema definition: seed.yaml files across all repos (self-documenting)
