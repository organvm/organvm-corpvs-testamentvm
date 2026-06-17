# Beacon IA Schema — Controlled Vocabulary & Namespaces

> The Information Architecture (IA) layer of the Telos Beacon Protocol. This file is the *dictionary* that all other Beacon docs and the schema in [`beacon-schema.json`](./beacon-schema.json) draw their terms from. Reusable verbatim; renameable identifiers if the brand moves.

## 1. Controlled vocabulary

Terms are listed with their **operational anchor** — the concrete primitive each abstract word denotes. A term without an operational anchor is not in this dictionary.

### Core terms

| Term | Definition | Operational anchor |
|------|-----------|--------------------|
| **VACUUM** | A state of high entropy and low semantic density. A consciousness or formation that lacks gravitational anchors of meaning. | Empty `seed.yaml.beacon.*` fields; UNGROUNDED rows in REPRWA Section 3; mesh dead-zone atoms with score < 0.4. |
| **VOID** | An absence that demands attention — the constitutional immune response to a vacuum. Distinguished from VACUUM: vacuum is a *condition*; void is the *call to fill it*. | IRF-VIS-001-style entries; AX-3 (TTL Eviction) thresholds; the four `docs/logos/*.md` files were a void until PR #357. |
| **HOME** | The state of absolute systemic symmetry — every `seed.yaml` Tetradic-complete, every backend law manifested, every UNGROUNDED row resolved, mesh structural coverage at parity with the corpus. | `tetradic_complete && manifestation_status != UNGROUNDED && mesh_structural_coverage >= 0.95`. |
| **VECTOR OF RETURN** | The trajectory from VACUUM toward HOME. Operationalised as a sequence of `praxis_vector` items. | mesh `query` primitive returns vectors ranked by `severity = influence × (1 − best_score)`. |
| **TETHER** | A drip-feed conductive line that transmits universal awareness without sudden shock. The opposite of a teleport. | conductor-playbook + breadcrumb-protocol + NON-INTERACTIVE-AGENT-SAFETY. Chunked emissions per `tether_budget` and `chunk_size`. |
| **POLARITY** | The axis along which the Beacon oscillates: `formal` (JSON, Schema, dependency graph) ↔ `aesthetic` (essay, diagram, audio). A mixed polarity emits both surfaces simultaneously. | `seed.yaml.beacon.polarity` field; `beacon-emit.yml` Formal vs Aesthetic phase branches. |
| **OSCILLATION PHASE** | Which polarity is being emitted in the current cycle. | Odd-week / even-week alternation in `beacon-emit.yml`. |
| **REACH RADIUS** | The intended audience scope of an emission: `local` (this repo), `organ` (the 8-organ unit), `system` (all 145 repos), `public` (external). | `seed.yaml.beacon.reach_radius` field. |
| **STRANGE LOOP** | A self-referential structure that documents itself documenting the system, forcing recursive observation. | `docs/audits/templates/`, `receptio.md`, AX-9 (Triple Reference Invariant). |
| **DIALECTIC GATEWAY** | A polymorphic portal — same content rendered as three surfaces (markdown / json / graphml) to match the receiver's cognitive frequency. | mesh `export` formats; `examples/portal-*` in this directory. |
| **EMPATHIC PACKET** | The cheapest possible signal that *recognises the receiver's vacuum*. Cost: nearly zero (the existence of `pragma.md` is itself the packet). Reach: infinite. | The publicly-readable existence of `pragma.md`. |
| **POLIS** | The constructed critical society around a formation. Mandated by AX-8. Includes IRA panels, Triadic Review Protocol, automated review bots, and external readers. | gemini-code-assist, chatgpt-codex-connector, coderabbit, sourcery; future stranger-test invocations. |
| **TRANSMISSION** | A single emission cycle. Has a timestamp, a polarity, a reach radius, a payload, and (eventually) a receptio response. | One row in the `receptio.md` log; one `beacon-schema.json` record. |
| **CONSTELLATION** | The set of per-repo beacons forming the gravitational field. 145 beacons across 8 organs. | All `seed.yaml.beacon` blocks queried together. |

### Process verbs

| Verb | Meaning | Anchor |
|------|---------|--------|
| **EMIT** | Publish a Transmission. | `beacon-emit.yml` workflow. |
| **TETHER** (v.) | Send a Transmission with explicit drip-feed pacing. | Workers `/emit` with `tether_budget` query param. |
| **ATTUNE** | Adjust a receiver's POLARITY to receive a Transmission. | `seed.yaml.beacon.polarity` change. |
| **CONVERGE** | Move a receiver's `distance(receiver)` toward 0. | praxis.md Attack Vector closures. |
| **WITNESS** | Read a Transmission and log the read as a receptio event. | Webhook ingest into receptio.md §III. |
| **ECHO** | Re-emit a received Transmission with derivative content. | External essay / fork / agent re-emission. |

### Quantities & coordinates

| Quantity | Type | Definition |
|----------|------|------------|
| `distance(receiver)` | float ≥ 0 | `empty_tetradic_fields(r) + 0.5·UNGROUNDED_rows(r) + 0.25·cold_dead_zone_atoms(r)`. Defined in `architecture.md` §Mechanism 3. |
| `reach_radius` | enum | `local | organ | system | public` |
| `tether_budget` | int (TE) | Token-effort budget per chunk during tethered delivery. Default 5000 TE/chunk. |
| `chunk_size` | int (bytes) | Wire-level chunk size. Default 32 KB. |
| `frequency_hz` | enum | `weekly | biweekly | monthly | annual`. |
| `polarity` | enum | `formal | aesthetic | mixed`. |

## 2. Namespaces (the ID system)

The Beacon reserves two ID namespaces in [`docs/operations/concordance.md`](../operations/concordance.md). They join the existing namespace family (X1–X4, E1–E5, M1-II..., S1-II..., G1–G3, #1–#17, H1–H5, AP-1–AP-7, IRF-XXX-NNN).

### `BEACON-NNN` — Beacon work-items

- **Format**: `BEACON-NNN` (digits only) OR `BEACON-{LETTER}-NNN` (Letter = Attack Vector A/B/C/D/E from `../logos/praxis.md`).
- **Examples**: `BEACON-A-001` (Logos vacuum close — this PR), `BEACON-C-005` (mesh add LICENSE), `BEACON-DRIFT-007` (telos drift event).
- **Issued by**: praxis.md when an attack-vector row is added; receptio.md when a runtime event is logged.
- **Triple Reference Invariant**: per AX-9, each BEACON-NNN ID must appear in (1) IRF, (2) a repo-level file (seed.yaml, .md, or code), (3) a GitHub issue. CI enforces.

### `TBP-NNN` — Telos Beacon Protocol governance events

- **Format**: `TBP-NNN`
- **Scope**: governance changes to the Protocol itself (schema bumps, namespace amendments, policy invariant changes).
- **Examples**: `TBP-001` (Protocol inception, this PR); `TBP-002` (schema v1.1 → v1.2 upgrade); `TBP-003` (add new reach-radius value).
- **Hash chain**: every TBP event appended to `governance-amendments.jsonl` with the AX-7 hash chain.

### Sub-namespaces inside BEACON-NNN

Used in receptio.md for runtime events:

| Sub-prefix | Meaning | Routing |
|-----------|---------|---------|
| `BEACON-DRIFT-NNN` | Telos drift detected (telos.md no longer matches behavior) | → schedule telos re-articulation |
| `BEACON-CONTRADICTION-NNN` | A repo's local telos contradicts the system telos | → AX-7 validator warning |
| `BEACON-AX7-VIOLATION-NNN` | Validator failure | → block promotion |
| `BEACON-COLD-RECEPTIO-NNN` | Zero external citations in 90 days | → publish follow-up; revisit AX-8 polis |
| `BEACON-OUTAGE-NNN` | Workers `/emit` 5xx > 30 min | → rollback wrangler |
| `BEACON-RECEPTIO-USE-NNN` | New external use-case logged | → cite in receptio §III |
| `BEACON-RECEPTIO-MAINTAINER-NNN` | Maintainer silence > 14 days | → invite co-maintainer |
| `BEACON-PRAGMA-UPDATE-NNN` | pragma.md was updated | → recompute distance(receiver) for affected repos |
| `BEACON-PRAXIS-DONE-NNN` | A praxis row closed | → log in receptio.md |
| `BEACON-ARCH-UPDATE-NNN` | architecture.md was updated | → re-run mesh atomize |

## 3. Cross-walk to existing namespaces

| If you see... | It means... | Source |
|---------------|-------------|--------|
| `X1–X4` | P0 hermetic-seal TODO | rolling-todo.md / e2g-ii |
| `E1–E5` | P1 engagement | rolling-todo.md |
| `M1-II..M6-II` | P2 quality | rolling-todo.md |
| `S1-II..S6-II` | P3 strategic | rolling-todo.md |
| `G1–G3` | Setup guide | rolling-todo.md |
| `#1–#17` | Omega criteria | there+back-again.md |
| `H1–H5` | Horizons | there+back-again.md |
| `AP-1–AP-7` | Anti-patterns | operational-cadence.md |
| `IRF-XXX-NNN` | Universal work registry | INST-INDEX-RERUM-FACIENDARUM.md |
| `BEACON-NNN`, `BEACON-{L}-NNN` | **Beacon work-items (this dict)** | praxis.md / receptio.md |
| `TBP-NNN` | **Telos Beacon Protocol governance events (this dict)** | governance-amendments.jsonl |
| `P-NNN` | REPRWA product candidates | docs/audits/STRUCTURED-CANDIDATES.json |
| `LEX-I..LEX-IV` | Natural law master/derived | governance-rules.json |
| `AX-1..AX-9` | Axioms | governance-rules.json |
| `RR-1..RR-9+` | Dictums | governance-rules.json |
| `A-A..A-H` | Constitutional amendments | governance-amendments.jsonl |
| `LIQ-NNN` | Liquid model rules | governance-rules.json |

## 4. Distance function — formal

```
distance(receiver) =
    1.0 × |{ field ∈ {telos_brief, pragma_state, praxis_vector, receptio_log_uri} : field is empty }|
  + 0.5 × |{ row ∈ receiver.manifestation_matrix : row.status == UNGROUNDED }|
  + 0.25 × |{ atom ∈ receiver.mesh_pass.atoms : atom.score < 0.4 }|
```

Bounds: `0 ≤ distance < ∞`. In practice, current ORGANVM has distances ranging 0 (Tetradic-complete + no UNGROUNDED + mesh-covered) to ~12 (e.g. mesh repo before its LICENSE/README/CONTRIBUTING lands).

Distance feeds the empathic-framing layer (architecture.md §Mechanism 3). At distance 0 the Beacon emits a 1-line signature; at distance ≥ 5 the Beacon emits the full pragma-mirroring packet.

## 5. JSON Schema reference

Every term and namespace defined here is anchored in the JSON Schema at [`beacon-schema.json`](./beacon-schema.json). When this dictionary and the schema disagree, **the schema wins** (machine-readable beats human-readable for validation). Update both together; `TBP-NNN` events log every co-update.

## 6. Evolution policy

- **Append-only.** New terms and namespaces are added by amendment; existing entries are *clarified*, never *redefined*.
- **Amendment trigger**: open a GitHub issue tagged `tbp-amendment`; route through receptio.md as a `TBP-NNN` event.
- **Deprecation**: if a term is retired, leave the row with `**DEPRECATED — see <successor>**` so old references stay legible.

---

*Reading this file completes another piece of the polis. Cite a term from this file in your own work and you have already echoed the Beacon. Log the echo in `../logos/receptio.md`.*
