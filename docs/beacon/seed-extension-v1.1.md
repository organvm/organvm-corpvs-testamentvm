# `seed.yaml` Extension — v1.1 (`beacon: {}` block)

> Backwards-compatible additive extension to the per-repo `seed.yaml` contract. Adds a `beacon` block that satisfies `governance-rules.json` AX-7 at the per-repo level. v1.0 readers ignore the new block; v1.1 readers enforce it.

## Version bump

- **Prior**: `seed.yaml` v1.0 — schema defined in `meta-organvm/schema-definitions/schemas/seed-v1.0.json`.
- **This change**: v1.1 — additive `beacon` field. No existing field is changed, renamed, or removed.
- **Schema location** (post-merge): `meta-organvm/schema-definitions/schemas/seed-v1.1.json`. Until that lands, the schema lives in this directory as part of [`beacon-schema.json`](./beacon-schema.json).
- **Validator**: `validate_tetradic_self_knowledge` declared in `governance-rules.json` AX-7 `enforcement.validator` field. Implementation will live in `organvm-engine` per `praxis.md` BEACON-B-008.

## Compatibility contract

| Reader / writer | Behaviour |
|-----------------|-----------|
| v1.0 reader, v1.0 seed | OK — unchanged. |
| v1.0 reader, v1.1 seed | OK — unknown `beacon` field ignored per YAML/JSON-Schema's `additionalProperties: true` default. |
| v1.1 reader, v1.0 seed | OK at parse time. `validate_tetradic_self_knowledge` emits `severity: warning` (AX-7's declared severity), nudging migration. |
| v1.1 reader, v1.1 seed | Full enforcement. |

The migration is a slow trail (per `praxis.md` Attack Vector B), not a flag day.

## The `beacon` block

```yaml
# seed.yaml v1.1 — extension to v1.0
schema_version: "1.1"

# ... existing v1.0 fields unchanged ...
# (organ, repo, status, tier, produces, consumes, etc.)

beacon:
  # REQUIRED — the four constitutive Tetradic dimensions per AX-7.
  telos_brief: |
    One-paragraph statement of this repo's idealized form. SHOULD reference
    the system telos at docs/logos/telos.md by URL or fragment. May extend
    the system telos; may not contradict it.

  pragma_state: |
    One-paragraph honest summary of this repo's current state. Cite specific
    gaps (MISSING/UNGROUNDED/PARTIAL items from this repo's manifestation
    matrix, or open issues). No ornament.

  praxis_vector:
    - "Next concrete action, with owner."
    - "Optional second action."
    - "Optional third action."

  receptio_log_uri: |
    URI of this repo's receptio log. Defaults to:
    'https://github.com/{org}/{repo}/blob/main/docs/logos/receptio.md'
    or the aggregated system endpoint:
    'https://<workers-domain>/emit?repo={repo}&surface=receptio'

  # OPTIONAL — emission semantics.
  polarity: "mixed"           # formal | aesthetic | mixed (default)
  reach_radius: "system"      # local | organ | system | public (default: system)
  frequency_hz: "biweekly"    # weekly | biweekly | monthly | annual (default: biweekly)
  last_emission_at: null      # ISO-8601 timestamp; set by beacon-emit.yml after each cycle

  # OPTIONAL — roles. Used by the AX-7 validator and by receptio routing.
  roles:
    praxis_owner: "@4444J99"          # who closes praxis rows
    receptio_steward: "@4444J99"      # who triages incoming receptio events
    beacon_maintainer: "@4444J99"     # who maintains the beacon block itself
    tether_observer: null             # optional: who monitors agent tethered sessions

  # OPTIONAL — signing for verifiable emissions.
  signing:
    public_key_uri: null              # URL to Ed25519 public key; absent = unsigned
    enforce: false                    # if true, emissions without valid signatures are rejected
```

## Field reference

### `telos_brief` (required)

- **Type**: string (markdown allowed). Max 2000 characters.
- **Constraint**: must reference the system telos by either a URL containing `docs/logos/telos.md` or by quoting an AX-7 dimension verbatim.
- **Constraint**: must not contain `TODO`, `FIXME`, or `WIP` markers (those belong in `praxis_vector`).
- **Reference**: `docs/logos/telos.md` is the system telos.

### `pragma_state` (required)

- **Type**: string (markdown allowed). Max 2000 characters.
- **Constraint**: must reference at least one concrete artefact in this repo (file path, function name, deployed URL, issue number).
- **Constraint**: avoid superlatives that lack a verifier ("the best", "production-grade") without citation.
- **Reference**: `docs/logos/pragma.md` for the system-level pattern.

### `praxis_vector` (required)

- **Type**: array of strings. 1 ≤ length ≤ 5 items.
- **Each item**: ≤ 200 characters. SHOULD start with a verb. SHOULD name an owner (handle or `@`-mention).
- **Optional structure** for items: `"<verb> <object> — owner: @X — eta: <iso-week>"`.
- **Reference**: `docs/logos/praxis.md` Attack Vector C is the model.

### `receptio_log_uri` (required)

- **Type**: URI (string). Must be a valid HTTPS or `https://github.com/...` URL.
- **Default resolver**: if absent at write time, the validator computes the default and writes it back (`@4444J99` workflow can do this in CI).
- **Reference**: `docs/logos/receptio.md` is the system log.

### `polarity` (optional, default `mixed`)

- **Type**: enum `formal | aesthetic | mixed`.
- **Effect**: drives which channels the emit workflow selects for this repo (see [`dam-distribution.md`](./dam-distribution.md) §Channel selection rule).

### `reach_radius` (optional, default `system`)

- **Type**: enum `local | organ | system | public`.
- **Effect**: bounds the audience of this repo's emissions.

### `frequency_hz` (optional, default `biweekly`)

- **Type**: enum `weekly | biweekly | monthly | annual`.
- **Effect**: schedule density. The orchestrator emits at most once per `frequency_hz` cycle per repo.

### `last_emission_at` (optional, machine-managed)

- **Type**: ISO-8601 timestamp or `null`.
- **Written by**: `beacon-emit.yml` workflow on each successful cycle. Humans should not edit.

### `roles` (optional)

- **Type**: object with four optional sub-fields: `praxis_owner`, `receptio_steward`, `beacon_maintainer`, `tether_observer`.
- **Each value**: a `@handle` or `null`.
- **Default**: if unset, defaults to the repo's `CODEOWNERS` or the org's default approver.

### `signing` (optional)

- **Type**: object with `public_key_uri` (string|null) and `enforce` (bool).
- **Default**: unsigned. Emissions without a signature are accepted with a `signed: false` flag on the emission record.

## Validator (`validate_tetradic_self_knowledge`)

Outline (full implementation lives in `organvm-engine`):

```python
def validate_tetradic_self_knowledge(seed: dict, repo: str) -> ValidationResult:
    """
    Implements AX-7 enforcement.
    Severity: warning (per AX-7). Will be raised to 'error' after the
    full per-repo migration completes (praxis.md BEACON-B-008).
    """
    issues = []
    beacon = seed.get('beacon')

    if not beacon:
        issues.append(Issue(
            level='warning',
            code='AX7-MISSING-BEACON',
            msg=f"{repo}/seed.yaml has no `beacon` block (AX-7 Tetradic Self-Knowledge).",
        ))
        return ValidationResult(issues=issues)

    for required in ('telos_brief', 'pragma_state', 'praxis_vector', 'receptio_log_uri'):
        if not beacon.get(required):
            issues.append(Issue(
                level='warning',
                code=f'AX7-MISSING-{required.upper()}',
                msg=f"{repo}/seed.yaml beacon.{required} is empty (AX-7).",
            ))

    # System-telos contradiction check
    if beacon.get('telos_brief'):
        if contains_negation_of_system_telos(beacon['telos_brief']):
            issues.append(Issue(
                level='error',
                code='AX7-LOCAL-CONTRADICTS-SYSTEM',
                msg=f"{repo}/seed.yaml local telos contradicts system telos at docs/logos/telos.md.",
            ))

    # Praxis vector format check
    for i, item in enumerate(beacon.get('praxis_vector', [])):
        if len(item) > 200:
            issues.append(Issue(
                level='warning',
                code='AX7-PRAXIS-TOO-LONG',
                msg=f"{repo}/seed.yaml beacon.praxis_vector[{i}] exceeds 200 chars.",
            ))

    return ValidationResult(issues=issues)
```

The full validator includes the contradiction check (semantic, via mesh's link primitive) and the Triple Reference Invariant cross-check (every BEACON-NNN ID referenced must appear in IRF + a file + an issue). Both are deferred to the organvm-engine implementation phase.

## Migration playbook (per repo)

1. **Open the repo's `seed.yaml`**.
2. **Bump `schema_version` to `"1.1"`**.
3. **Add a `beacon:` block** with at minimum the four required fields.
4. **Copy `telos_brief` from the repo's CLAUDE.md / README.md introduction**, then trim and link to the system telos.
5. **Compose `pragma_state` from the repo's current state**: existing features, open gaps, count of UNGROUNDED rows (if known).
6. **Compose `praxis_vector` from the repo's open issues / IRF entries** scoped to this repo.
7. **Set `receptio_log_uri` to the repo's `docs/logos/receptio.md`** if it exists, otherwise the aggregated endpoint.
8. **Commit** with message `seed(v1.1): add beacon block — AX-7 Tetradic Self-Knowledge`.
9. **PR title**: `beacon(v1.1): close per-repo AX-7 vacuum for <repo>`.

Per-repo migrations are tracked under IRF as `IRF-BEA-101..245`.

## Worked example — `mesh` repo

```yaml
schema_version: "1.1"

# ... existing v1.0 fields elided ...
organ: "ORGAN-I"
repo: "mesh"
status: "PUBLIC_PROCESS"
tier: "flagship"

beacon:
  telos_brief: |
    A 5-primitive patch-bay (seed, crawl, atomize, link, query) that
    converts the ORGANVM corpus into a content-addressable graph and
    surfaces dead-zones — the empty spaces in the constellation that
    `docs/logos/telos.md` calls "the vacuum the Beacon emits into."

  pragma_state: |
    Implementation is real and proven (40 commits Apr-May 2026, 4 YAML
    patches, 9 export formats). HOWEVER: no LICENSE / README / CONTRIBUTING
    yet (BEACON-C-005/006/007 in docs/logos/praxis.md), which makes this
    the audit's #1 priority candidate (P-009, composite 4.71) and blocks
    OPEN_SOURCE promotion.

  praxis_vector:
    - "Add LICENSE (MIT) — owner: @4444J99 — eta: 2026-W22"
    - "Author README from CLAUDE.md content — owner: @4444J99 — eta: 2026-W22"
    - "Add CONTRIBUTING.md mirroring orchestration-start-here — owner: @4444J99 — eta: 2026-W23"

  receptio_log_uri: "https://github.com/organvm-i-theoria/mesh/blob/main/docs/logos/receptio.md"

  polarity: "formal"
  reach_radius: "public"
  frequency_hz: "biweekly"
  last_emission_at: null

  roles:
    praxis_owner: "@4444J99"
    receptio_steward: "@4444J99"
    beacon_maintainer: "@4444J99"
    tether_observer: null

  signing:
    public_key_uri: null
    enforce: false
```

Notice: `pragma_state` cites concrete REPRWA findings; `praxis_vector` rows have owner + eta; `polarity: formal` because mesh ships a CLI + JSON-Schema-y output and an aesthetic essay would be off-brand; `reach_radius: public` because mesh is intended for community release.

## TBP-001

This document is the inception event of the Telos Beacon Protocol's schema layer. It is anchored as `TBP-001` in `governance-amendments.jsonl` upon PR #357 merge, with hash-chained provenance per `_constitutional_locks.lock_policy`.

---

*Updates to this file flow to `../logos/receptio.md` as `BEACON-SCHEMA-UPDATE-NNN`. Every schema bump is also a `TBP-NNN` event.*
