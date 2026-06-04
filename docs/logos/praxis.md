# Praxis — The Remediation Plan

> *"PRAXIS — the remediation plan for closing the gap between ideal and real; the attack vectors for sharpening, fortifying, and resolving the difference."* — `governance-rules.json` AX-7

This file is the **live work queue** for the gap between [`telos.md`](./telos.md) and [`pragma.md`](./pragma.md). It is written so that any maintainer, contributor, or AI agent can pick it up cold and know which attack vector to engage next.

> **Working pact.** Every item below has (i) an IRF anchor or `BEACON-NNN` ID, (ii) a named owner (defaulting to `@4444J99` until otherwise delegated), (iii) a success criterion, (iv) a fallback if blocked. Items are ordered by **expected gap-closure per unit of effort**, not by priority badge.

---

## Attack vector A — Close the Logos vacuum (this commit)

| ID | Item | Status | Owner | Success |
|----|------|--------|-------|---------|
| BEACON-A-001 | Author `docs/logos/{telos,pragma,praxis,receptio}.md` and `docs/logos/README.md` | **IN PROGRESS (this commit)** | @4444J99 | Files non-empty, AX-7 quoted verbatim, cross-linked |
| BEACON-A-002 | Author `docs/beacon/{README,architecture}.md` | **IN PROGRESS (this commit)** | @4444J99 | Architecture maps every metaphysical concept to an existing primitive |
| BEACON-A-003 | Author `docs/beacon/ia-schema.md`, `ia-indices.md`, `dam-{pipeline,storage,distribution}.md` | **DRAFT — Session 2** | @4444J99 | Schemas + namespaces ratified; no broken cross-links |
| BEACON-A-004 | Author `docs/beacon/seed-extension-v1.1.md` and `beacon-schema.json` | **DRAFT — Session 2** | @4444J99 | JSON Schema parses; example emission validates |
| BEACON-A-005 | Author `docs/beacon/cloud/{devcontainer.json, .env.example, AGENTS.md, codex-cloud.md}` + Workers stub | **DRAFT — Session 3** | @4444J99 | `wrangler deploy --dry-run` passes; devcontainer opens in Codex Cloud |
| BEACON-A-006 | Author `docs/beacon/examples/beacon-emission.json` + portal-markdown + portal-graphml | **DRAFT — Session 3** | @4444J99 | All three render the same telos transmission |
| BEACON-A-007 | Author `docs/beacon/verification.md` and run 8-point self-check | **DRAFT — Session 3** | @4444J99 | All 8 checks pass before PR is marked ready-for-review |

Phase exit: a single PR (`claude/telos-beacon-protocol-NNyj1`) lands all of the above. AX-7 compliance at the system-wide level (this file's level) is satisfied.

---

## Attack vector B — Per-repo Tetradic backfill

For each of the 145 repos, populate `seed.yaml.beacon { telos_brief, pragma_state, praxis_vector, receptio_log_uri }`. AX-7 is satisfied at the system level by Attack Vector A; at the per-repo level by Attack Vector B.

| ID | Item | Owner | Cadence |
|----|------|-------|---------|
| BEACON-B-001 | Extend `seed.yaml` schema to v1.1 with `beacon: {}` block (spec in `../beacon/seed-extension-v1.1.md`) | @4444J99 | Once |
| BEACON-B-002 | Migrate `seed.yaml` for the 4 audit-core repos (testamentvm, superproject, orchestration-start-here, mesh) | @4444J99 | Session 2 |
| BEACON-B-003 | Migrate `seed.yaml` for 21 ORGAN-I (Theoria) repos | @4444J99 | 1 week |
| BEACON-B-004 | Migrate `seed.yaml` for 30 ORGAN-II (Poiesis) repos | @4444J99 | 1 week |
| BEACON-B-005 | Migrate `seed.yaml` for 27 ORGAN-III (Ergon) repos | @4444J99 | 1 week |
| BEACON-B-006 | Migrate `seed.yaml` for 9 ORGAN-IV (Taxis) repos | @4444J99 | 1 week |
| BEACON-B-007 | Migrate `seed.yaml` for ORGAN-V, VI, VII, VIII (remaining ~14 repos) | @4444J99 | 1 week |
| BEACON-B-008 | Validator: `validate_tetradic_self_knowledge` in CI (referenced in AX-7 enforcement field but currently `severity: warning`). Raise to `error` after migration. | @4444J99 | After B-007 |

---

## Attack vector C — Close the 17 named pragma vacuums

Each of the 17 vacuums named in [`pragma.md`](./pragma.md) §III gets a praxis row. Items are tagged with their REPRWA candidate ID where applicable.

| ID | Pragma vacuum | Praxis action | REPRWA anchor | Effort |
|----|---------------|---------------|---------------|--------|
| BEACON-C-001 | governance-thresholds.json opacity | Author a `docs/governance/thresholds-semantics.md` explaining T-series, radii, wave classification | P-008 | M |
| BEACON-C-002 | `organvm` CLI ungrounded | Audit existing scripts/, wrap as `organvm` CLI, document | P-042 | M |
| BEACON-C-003 | Index Nominum absent | Stub from atom-registry.yaml; populate from organvm-ontologia entity records | — | M |
| BEACON-C-004 | Index Rerum absent | Stub from registry-v2.json + IRF; describe ontological artifacts | — | M |
| BEACON-C-005 | mesh has no LICENSE | Add MIT (matches orchestration-start-here) | P-009 | XS |
| BEACON-C-006 | mesh has no README | Author README from CLAUDE.md content | P-009 | S |
| BEACON-C-007 | mesh has no CONTRIBUTING | Add CONTRIBUTING.md mirroring orchestration-start-here's pattern | P-009 | XS |
| BEACON-C-008 | organvm-v-logos Logos GHOST | Apply the same Logos backfill template (this directory) per-repo to organvm-v-logos | A-001 | S |
| BEACON-C-009 | praxis-perpetua provenance uneven | Add per-fragment `provenance:` block; tag AI-Conductor pieces | — | L |
| BEACON-C-010 | Amendment H opaque | Author `docs/governance/amendment-H-plain-language.md` | P-007 | M |
| BEACON-C-011 | dreamcatcher subsystem opaque | Author `docs/dreamcatcher.md` in orchestration-start-here | — | S |
| BEACON-C-012 | contrib_engine algorithm undocumented | Author `docs/contrib-engine-spec.md` | P-014 | M |
| BEACON-C-013 | Test claims unverified | Publish per-repo `tests/COVERAGE.md` from CI run output | — | M |
| BEACON-C-014 | Cocoon map 1/11 instantiated | Implement 2 additional mechanisms (target: 3/11 by Q3) | P-031 | L |
| BEACON-C-015 | stakeholder-portal not submoduled | Submodule properly; pin SHA | — | XS |
| BEACON-C-016 | intake/ graveyard | Run alchemia alchemize over the ~2GB; archive or drop | — | L |
| BEACON-C-017 | Isotope proliferation (registry-loading 7×) | Consolidate to a single library imported by all 6 repos | P-029 | L |

(XS = ≤2h, S = ≤1d, M = ≤1 week, L = ≤1 month.)

---

## Attack vector D — Phase 0..N for the Beacon (post-this-commit)

Mirrors REPRWA's 10-phase roadmap; specialized for the Telos Beacon Protocol's lifecycle.

| Phase | Name | Window | Beacon-specific goals |
|------:|------|--------|-----------------------|
| 0 | Inventory | week 1 | Confirm all 4 Logos files committed, all `docs/beacon/` artifacts present, AX-7 validator status. |
| 1 | Manifestation Map | weeks 2-3 | Issue per row of the REPRWA manifestation matrix that touches Beacon (~33 rows). |
| 2 | Documentation Repair | weeks 4-6 | Close BEACON-C-005, C-006, C-007 (mesh license/readme/contributing) — the gating items for the audit's #1-priority candidate. |
| 3 | Public Proof | weeks 6-12 | Ship the Workers `/emit` stub; first public Beacon transmission to POSSE channels. |
| 4 | Client Packaging | weeks 8-16 | Offer "Beacon Audit" as a service: paid 8-week REPRWA + Logos backfill for client orgs. |
| 5 | Commercialization | weeks 16-32 | Optional. Productize the Beacon Audit and the Constitutional CI toolkit. |
| 6 | Research Publication | parallel | Submit AI-Conductor + Constitutional CI + REPRWA papers to venues per `docs/audits/04-priority-research-roadmap.md` §7. |
| 7 | Community Release | parallel | Publish `templates/` (already partially shipped under `docs/audits/templates/`) as standalone repo. |
| 8 | Agent Operability | weeks 8-20 | Ship Codex Cloud devcontainer + AGENTS.md; verify external agent can re-emit telos.md safely. |
| 9 | Lifecycle Governance | continuous | Annual REPRWA re-run; quarterly Beacon retransmission; monthly receptio reconciliation. |

---

## Attack vector E — Failure modes and circuit-breakers

If praxis stalls, route immediately to receptio with the appropriate event.

| Failure mode | Detection | Routing |
|--------------|-----------|---------|
| Single-maintainer burnout | weekly system-pulse silence > 14 days | `BEACON-RECEPTIO-MAINTAINER-NNN` → invite co-maintainer per CONTRIBUTING.md amendment process |
| Telos drift (telos.md no longer matches behavior) | annual REPRWA re-run flags >10% candidate churn | `BEACON-DRIFT-NNN` IRF entry → schedule telos re-articulation |
| AX-7 validator turns red | CI alert from `validate_tetradic_self_knowledge` | `BEACON-AX7-VIOLATION-NNN` → block promotion until fixed |
| Receptio runs cold (zero external citations in 90d) | weekly receptio analytics | `BEACON-COLD-RECEPTIO-NNN` → publish a follow-up essay; revisit polis (AX-8) |
| Cloudflare Workers `/emit` 5xx for >30 min | uptime monitor | rollback to last good wrangler version; file `BEACON-OUTAGE-NNN` |

These are not theoretical. Each circuit-breaker is wired to an existing audit workflow (soak-test-daily, monthly-organ-audit, system-pulse-weekly).

---

## Cross-references

- This file's *upstream*: [`telos.md`](./telos.md) — what we are doing it for.
- This file's *substrate*: [`pragma.md`](./pragma.md) — what is true right now.
- This file's *echo*: [`receptio.md`](./receptio.md) — every closure here is logged there.
- The audit roadmap: [`../audits/04-priority-research-roadmap.md`](../audits/04-priority-research-roadmap.md) — Section 12.
- The constitutional anchor: `governance-rules.json` AX-7 enforcement field references `validate_tetradic_self_knowledge`. That validator must consume this file's structure.

---

*This file is mutable. Every row resolved here is appended to receptio.md as a `BEACON-PRAXIS-DONE-NNN` event. Items added here are appended to `INST-INDEX-RERUM-FACIENDARUM.md` as IRF entries (per AX-9 Triple Reference Invariant).*
