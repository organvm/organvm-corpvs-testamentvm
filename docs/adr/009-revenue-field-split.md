# ADR-009: Revenue Field Split (VERITAS)

## Status

Accepted

## Date

2026-02-13

## Context

In repo-registry.json schema v0.4, ORGAN-III repositories had a single `revenue` field that conflated two distinct concepts:

1. **Revenue model** — *how* the product intends to generate revenue (subscription, freemium, one-time purchase, advertising, etc.)
2. **Revenue status** — *whether* the product is currently generating revenue (none, pre-revenue, generating, profitable)

A repo like `life-my--midst--in` had `revenue: "subscription"`, which implied it was *currently* earning subscription revenue — it wasn't. It had a subscription *model* but zero actual revenue. This conflation was dishonest and would mislead anyone reading the registry (grant reviewers, hiring managers, potential collaborators).

The VERITAS sprint (Sprint 11) was explicitly focused on honesty corrections across the system.

## Decision

Split the single `revenue` field into two fields for all 24 ORGAN-III repositories:

- **`revenue_model`**: The intended revenue mechanism (e.g., `subscription`, `freemium`, `one-time`, `advertising`, `internal`, `none`)
- **`revenue_status`**: The current revenue reality (e.g., `none`, `pre-revenue`, `beta`, `generating`, `profitable`)

This follows the principle: **separate intent from reality**. A product can have a clear revenue model (`subscription`) while honestly reporting that it currently generates no revenue (`none`).

The schema version was bumped to v0.5 to reflect this breaking change. The validation script `praxis-validate.py` was updated to require both fields for ORGAN-III repos.

## Consequences

### Positive

- **Honesty**: The registry accurately represents both intention and reality
- **Queryable**: Scripts can filter "repos with revenue models but no revenue" for prioritization
- **Credibility**: External readers see honest self-assessment, not inflated claims
- **Actionable**: The `revenue_status: none` designation makes it clear which products need monetization work

### Negative

- **Schema breaking change**: All consumers of repo-registry.json needed updates (validation scripts, dashboard generators, metric calculators)
- **24 repos updated**: Every ORGAN-III entry required manual review and split
- **Complexity increase**: Two fields instead of one — more to maintain and validate
- **No revenue anywhere**: After the split, all 24 ORGAN-III repos showed `revenue_status: none` — an uncomfortable truth, but an honest one

## References

- VERITAS sprint: `docs/specs/sprints/11-veritas.md`
- Registry: `repo-registry.json` (schema v0.5)
- Validation: `scripts/praxis-validate.py`
- Constitution Article I (Honesty): `docs/memory/constitution.md`
