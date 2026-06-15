# 28: The Ossuary Pattern — Reabsorbing Archived Repos into ORGAN-I

**Date:** 2026-06-15
**Status:** ACTIVE — governs the terminal transition of the promotion state machine
**Derived from:** Four-branch synthesis report §VI.2 ("failure recycling" gap); Session 8738e514 (strategic lifecycle analysis)
**Complements:** `docs/adr/007-promotion-state-machine.md`, `23-no-deletion-principle--alchemical-evolution.md`, `27-logos-bypass-feedback-routing.md`
**Resolves:** GH#99

---

## 1. The principle

**Dead products are quarries, not graves.** When a product reaches the end of its commercial life (GRADUATED → ARCHIVED), the theoretical primitives, algorithms, and structural patterns embedded in it are *harvested* and routed back into ORGAN-I as raw material. Named after the architectural ossuary — the chamber where bones are stored not to be forgotten but to be kept available — the pattern adds a constructive after-life to archival.

This is a direct expression of the **No-Deletion Principle** (`23-...`): ARCHIVED is not an end-state, it is `TRANSMUTED-TO-TESTAMENT`. The Ossuary pattern names what the testament is *for*.

## 2. The problem: the state machine ended at ARCHIVED

The promotion state machine (ADR-007) runs `LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED → ARCHIVED`. ARCHIVED was terminal. A product that failed in the market took its embedded intellectual work to the grave with it: the clever scheduling algorithm, the ontology that the domain forced it to discover, the structural pattern that only became visible under real load. That work was paid for (in tokens, in time, in market exposure) and then discarded.

Meanwhile ORGAN-I — the source of primitives — is perpetually hungry for raw material. The asymmetry is absurd: the system throws away exactly the kind of hard-won, reality-tested insight that Theory most needs, at exactly the moment it becomes free.

## 3. The solution: ARCHIVED → REABSORBED

The Ossuary pattern adds a transition *parallel to* ARCHIVED rather than after it (ARCHIVED remains a valid resting state per No-Deletion; REABSORBED records that a harvest occurred).

```
                                   ┌─────────────┐
GRADUATED ──► ARCHIVED ────────────► (testament) │
                  │                 └─────────────┘
                  │ harvest
                  ▼
            ┌───────────┐   Logos Bypass (std 27)   ┌──────────┐
            │  OSSUARY   │ ───── intake/market/ ────►│ ORGAN-I  │
            │ (harvest   │                           │  intake  │
            │  template) │                           └──────────┘
            └───────────┘
              status: REABSORBED
```

Crucially, **the harvested material does not flow directly from the ARCHIVED ORGAN-III repo into an ORGAN-I repo** — that would be a back-edge. It flows through the **Logos Bypass** (`27-logos-bypass-feedback-routing.md`): the harvest is written up, staged in `intake/market/`, and autonomously ingested by ORGAN-I. The acyclic graph is preserved.

## 4. The harvest template

When a repo enters ARCHIVED, the conductor (or an agent) produces a **harvest record** — a single markdown artifact extracting reusable value:

```markdown
# Ossuary Harvest: <repo-name>

**Archived:** <date>  ·  **Org:** <organ-iii-org>  ·  **Cause of death:** <reason>

## Theoretical primitives recovered
- <primitive>: <where it lived in the code, why it generalizes>

## Algorithms / patterns recovered
- <algorithm>: <what problem it solved, what it assumed>

## Empirical constants & findings
- <constant/finding>: <what reality taught that the theory did not predict>
  (route via Logos Bypass — see std 27 §5 for the lambda=1.955 archetype)

## Routing
- Staged at: intake/market/<date>-ossuary-<repo>.md
- Candidate ORGAN-I consumers: <repo(s)>
- Provenance: this harvest derives from ORGAN-III/<repo>@<sha>
```

The harvest record is the bone catalogue. ORGAN-I decides, on its own schedule, which bones become new primitives.

## 5. Schema consideration: `reabsorption_status`

A new optional field is proposed for the `registry-v2.json` repo schema, to be added when the first repo is actually harvested (additive, per No-Deletion):

| Field | Values | Meaning |
|-------|--------|---------|
| `reabsorption_status` | `null` \| `HARVEST_PENDING` \| `HARVESTED` \| `REABSORBED` | Tracks whether an ARCHIVED repo's value has been extracted and whether ORGAN-I has ingested it |
| `reabsorption_provenance` | `[ {into: "organvm-i-.../<repo>", artifact: "<path>"} ]` | Which ORGAN-I work derives from this dead product (forward-traceable lineage) |

This is a **schema consideration**, not yet a schema change: no repo is ARCHIVED-and-harvested today (the corpus has no GRADUATED→ARCHIVED ORGAN-III repos as of 2026-06-15), so adding the columns now would be speculative. The fields are specified here so that the moment the first product dies, the vocabulary already exists.

## 6. Provenance: tracing ORGAN-I work back to ORGAN-III failure

The pattern's most valuable long-run output is a **forward-traceable lineage**: "this theoretical primitive in ORGAN-I exists because *that* product failed and we harvested what it learned." `reabsorption_provenance` records the edge in the *documentation* layer (not the dependency graph), so the system can answer "what did we learn from our dead?" — a question most institutions cannot answer at all.

## 7. Test on one archived repo

There is currently **no GRADUATED→ARCHIVED ORGAN-III repo** to test against (verified against `repo-registry.json`, 2026-06-15: all ORGAN-III repos are LOCAL/DEVELOPMENT/DEPLOYED/GRADUATED, none ARCHIVED). The test deliverable is therefore specified as a **dry-run** against the nearest analogue and is tracked as a follow-up:

- **Dry-run target:** the first ORGAN-III product to be archived after a BETA sprint (GH#12–#24) concludes without market traction.
- **Acceptance for the live test:** a harvest record exists, is staged in `intake/market/`, and at least one `reabsorption_provenance` edge is recorded.

This contingency is logged in the IRF so the test fires automatically when the precondition is met, rather than being silently dropped.

## 8. Acceptance criteria

- [x] Ossuary pattern documented as an ACTIVE standard (this file). — GH#99 deliverable 1
- [x] `reabsorption_status` schema field specified for registry-v2 (§5). — GH#99 deliverable 2
- [~] Test on one archived repo — **deferred with cause**: no ARCHIVED ORGAN-III repo exists yet; dry-run target and live-test acceptance specified (§7) and logged to IRF. — GH#99 deliverable 3

## 9. Cross-references

- **ADR-007** (`docs/adr/007-promotion-state-machine.md`) — the state machine this transition extends.
- **`23-no-deletion-principle--alchemical-evolution.md`** — ARCHIVED as `TRANSMUTED-TO-TESTAMENT`; this pattern is what the testament feeds.
- **`27-logos-bypass-feedback-routing.md`** — the non-back-edge channel the harvest travels.
