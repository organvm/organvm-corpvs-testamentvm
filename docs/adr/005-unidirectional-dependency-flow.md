# ADR-005: Unidirectional Dependency Flow (I→II→III)

## Status

Accepted

## Date

2026-02-09

## Context

With 97 repositories across 8 organs, uncontrolled cross-dependencies would create a tangled graph where changing one repo could break any other. The system needed a dependency model that:

1. Prevents circular dependencies (no cycles in the build/deploy graph)
2. Enables independent testing and deployment per organ
3. Makes the information flow explicit and auditable
4. Scales without combinatorial explosion of integration tests

The core tension: ORGAN-III (Commerce) products often *use* ORGAN-I (Theory) frameworks, and ORGAN-II (Art) projects often *embody* ORGAN-I concepts. But if III can depend on II, and II on I, and I on III, the entire system becomes a monolith.

## Decision

The dependency graph is a **strict DAG (Directed Acyclic Graph)** with unidirectional flow:

```
ORGAN-I (Theory) → ORGAN-II (Art) → ORGAN-III (Commerce)
```

**Rules:**
- ORGAN-I repos may depend on nothing (foundational layer)
- ORGAN-II repos may depend on ORGAN-I repos (art embodies theory)
- ORGAN-III repos may depend on ORGAN-I or ORGAN-II repos (products use frameworks and art)
- **No back-edges**: ORGAN-III cannot depend on ORGAN-II; ORGAN-II cannot depend on ORGAN-III; ORGAN-I cannot depend on II or III
- ORGAN-IV (Orchestration) has read access to all organs but owns no production code
- ORGAN-V/VI/VII consume outputs but do not create code dependencies

Dependencies are declared in `repo-registry.json` and validated by `validate-dependencies.yml` (runs weekly + on registry push). The workflow checks for cycles, back-edges, and maximum depth.

## Consequences

### Positive

- **Independent deployment**: Each organ can be built, tested, and deployed without the others
- **Clear information flow**: Theory produces concepts → Art realizes them → Commerce packages them for users
- **Reduced blast radius**: A breaking change in ORGAN-III cannot cascade to ORGAN-I or II
- **Audit trail**: The DAG is machine-validated — back-edges are caught in CI before merge
- **Conceptual clarity**: The dependency direction mirrors the creative process (think → make → ship)

### Negative

- **Code duplication**: If ORGAN-I and ORGAN-III both need a utility, it cannot live in III and be imported by I — it must be duplicated or extracted to I
- **Constrains organic development**: Sometimes a commerce product naturally produces a theoretical insight — the dependency rule prevents formalizing this as a code dependency
- **Graph maintenance overhead**: Every new cross-repo dependency must be declared and validated
- **Two back-edges found and fixed** during MANIFESTATIO sprint — the rule is easy to violate accidentally

## References

- Dependency validation: `validate-dependencies.yml` in orchestration-start-here
- Orchestration design: `docs/implementation/orchestration-system-v2.md`
- Back-edge fixes: Sprint 13 MANIFESTATIO (`docs/specs/sprints/13-manifestatio.md`)
- Registry: `repo-registry.json` (dependencies declared per-repo)
