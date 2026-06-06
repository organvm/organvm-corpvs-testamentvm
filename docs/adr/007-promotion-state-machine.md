# ADR-007: Promotion State Machine

## Status

Accepted

## Date

2026-02-09

## Context

The eight-organ system needed a formal mechanism to govern when content moves between organs — particularly when internal work becomes externally visible. Without this, every repo would need ad-hoc decisions about "is this ready to show?" and there would be no consistent quality gate.

The core problem: ORGAN-I produces theory, ORGAN-II produces art, ORGAN-III produces products. How does a concept graduate from internal exploration to public-facing asset? And how does a repo move from skeleton to portfolio piece?

Two separate state machines were needed:
1. **Cross-organ promotion**: When work moves from one organ's domain to another's visibility layer
2. **Repository documentation status**: The quality tier of an individual repo's documentation

## Decision

### Cross-Organ Promotion States

```
LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED → ARCHIVED
```

- **LOCAL**: Work exists within its home organ only. No cross-references, no external visibility.
- **CANDIDATE**: Nominated for promotion. Meets minimum quality criteria. Under review.
- **PUBLIC_PROCESS**: Published via ORGAN-V (essays, case studies). Externally visible but not yet integrated into other organs.
- **GRADUATED**: Fully integrated. Referenced by downstream organs. Part of the system narrative.
- **ARCHIVED**: No longer actively promoted. Preserved for historical reference.

Transitions are governed by `promotion-recommender.yml` (monthly, 1st at 08:00 UTC), which evaluates repos against criteria: CI passing, README complete, tests present, documentation status ≥ ACTIVE.

### Repository Implementation Status

```
DESIGN_ONLY → SKELETON → PROTOTYPE → ACTIVE → ARCHIVED
```

This tracks the code maturity of each repo, independent of its promotion state. Stored in `repo-registry.json` as `implementation_status`.

## Consequences

### Positive

- **Quality gates are explicit**: No repo reaches external visibility without meeting defined criteria
- **Automated evaluation**: The promotion-recommender workflow checks criteria monthly without human intervention
- **Reversible**: Repos can be demoted or archived without special handling
- **Separation of concerns**: Documentation quality (implementation_status) is independent of cross-organ promotion status
- **Audit trail**: Every promotion is a registry commit with full diff

### Negative

- **Promotion latency**: Monthly evaluation means a repo ready on day 2 waits until day 30 for promotion consideration
- **Two state machines to track**: Cross-organ promotion and implementation status are related but distinct — this creates cognitive overhead
- **ARCHIVED is ambiguous**: It means different things in the two state machines (no longer promoted vs. no longer maintained)
- **Manual overrides needed**: The automated recommender catches obvious promotions but strategic demotions require human judgment

## References

- Promotion workflow: `promotion-recommender.yml` in orchestration-start-here
- Orchestration system: `docs/implementation/orchestration-system-v2.md` §Promotion Criteria
- VERITAS sprint renamed PRODUCTION→ACTIVE: `docs/specs/sprints/11-veritas.md`
- Registry: `repo-registry.json` (`implementation_status` field)
