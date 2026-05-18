# Pragma — The Honest Account

> *"PRAGMA — the honest account of what has been concretely realized; the delta between the dream and the thing built."* — `governance-rules.json` AX-7

This is the system's **soil**. It is not the Bad Side of the dream; it is the substrate the dream actually grows in. Pragma is written without ornament because ornamenting pragma makes the dream blind.

> *Confidence note.* Numbers below are taken from two sources: (a) the REPRWA audit committed on branch `claude/repo-world-analysis-NNyj1` in this repo (`docs/audits/`), and (b) `registry-v2.json` at HEAD. Any drift is reconciled in `praxis.md` and routed to receptio as `BEACON-DRIFT-NNN`.

---

## I. Scale of the formation

- **Repositories tracked:** 145 across 8 GitHub organizations, registered in `registry-v2.json` (v1.2.0 schema).
- **Organs:** 8 — Theoria, Poiesis, Ergon, Taxis, Logos, Koinonia, Kerygma, Meta.
- **Launch:** all 8 organs operational since 2026-02-11.
- **Dependency edges declared:** 115 system-wide via `seed.yaml.produces/consumes`. 62 of those are intra-graph and validated for acyclicity by `validate-dependencies.yml`.
- **Governance rules:** v3.0. 4 master/derived natural laws (LEX-I through LEX-IV), 9 axioms (AX-1 through AX-9), 29 dictums (RR-1 through RR-9+), 8 amendments (A-A through A-H).
- **Workflows:** 16 GitHub Actions workflows in this repo alone (143 across the 8 orgs).
- **Scripts:** 51 Python/shell validation scripts.
- **Sprints completed:** 33 (numbered 01–33). The system was bootstrapped through a 76-sprint catalog organized in 18 categories.
- **Documentation surface:** ~404K+ words across 7 layered strata (genesis, planning, strategy, implementation, evaluation, standards, operations) plus archive.
- **AI-Conductor token budget:** ~6.5M TE for the full corpus across all phases.

This is the *built* substrate. It is real. It runs.

---

## II. The honest manifestation matrix

The REPRWA audit (`docs/audits/`) catalogued **58 backend laws** and classified each by its public/visible manifestation status:

| Manifestation status | Count | Meaning |
|----------------------|------:|---------|
| **PRESENT** | 17 | Publicly visible, branded, productized, or discoverable as a counterpart to the backend law. |
| **PARTIAL** | 33 | Backend law has some surface, but the surface is internal (issue comments, log files, in-repo docs) rather than public, branded, discoverable, or productized. |
| **MISSING** | 1 | No visible counterpart anywhere. |
| **UNGROUNDED** | 2 | Visible artifact is referenced but its backend law is unclear. |

**The dominant category is PARTIAL.** This is the system's central honesty: most of its laws have *some* body, but the body is private. The Beacon's job (and the praxis layer's job) is to convert PARTIAL → PRESENT.

The PARTIAL count of 33 is the operational definition of the *vacuum* the Beacon emits into.

---

## III. Vacuums named explicitly

Specific gaps surfaced by REPRWA and other audits, listed without ornament:

1. **The Logos layer was empty.** Until this commit, `docs/logos/telos.md`, `pragma.md`, `praxis.md`, `receptio.md` were all referenced (by `CLAUDE.md`, `GEMINI.md`, AX-7) but did not exist. Coverage: 0% → 100% with this delivery.
2. **`governance-thresholds.json` semantics are opaque.** T-series origins, radii (down/up/lateral), and wave classifications exist as values but are not narrated. Effect: governance is enforceable but unexplainable.
3. **`organvm` CLI is referenced but not visibly implemented** in `scripts/`. Effect: AGENTS-style docs talk to a tool that may not exist.
4. **Index Nominum and Index Rerum are planned but not built.** Index Locorum and IRF exist. Two of four classical indices are vacuums.
5. **`mesh` repo has no LICENSE / README / CONTRIBUTING.** Effect: IP status unclear; community use blocked; the audit's #1 priority candidate (P-009, composite 4.71) cannot ship beyond BUILD_NOW.
6. **`organvm-v-logos/public-process` "Logos" doc layer is GHOST (symmetry: 0.5).** Counterpart to governance logic is partially missing in the public-process essays.
7. **`praxis-perpetua` provenance is uneven.** 766K+ words; per-fragment authorship not always traceable.
8. **`Amendment H (Temporal Manifestation)`** is constitutional but cryptographic-philosophical in tone, not practically explained.
9. **`dreamcatcher` subsystem** is referenced in `src/` of orchestration-start-here; role unclear from public surface.
10. **`contrib_engine` income-weighting algorithm** is referenced; coefficients not visible.
11. **Test claims are partially unverified.** CLAUDE.md cites "240 passing tests" but tests/ directory structure is undocumented in the public surface.
12. **Cocoon map is 1/11 instantiated.** TRIPTYCH.md describes 11 biological mechanisms; only `skeletal_define.py` has a function. 36 gate contracts declared, ~10% implemented.
13. **stakeholder-portal not submoduled.** Lives locally; invisible to the superproject pointer system.
14. **`intake/` graveyard** in the superproject: ~2GB ingested, not exited. Material absorbed without being alchemized.
15. **Isotope proliferation.** Registry-loading is reimplemented 7× across 6 repos. Organ-mapping in 3 places. Same code, different locations.
16. **Single-maintainer concentration.** @4444J99 is the single approval gate across all four core repos. High bus factor risk.
17. **AI-Conductor formal specification** is extensively narrated across 33+ essays but has not been distilled into one canonical specification doc.

These are not failures. They are the *honest delta* between the dream of telos.md and the thing built. AX-7 names this: "the honest account of what has been concretely realized."

---

## IV. What the system definitely is

To balance the vacuum list:

- It is **constitutional**. Governance is testable: v3.0 axioms enforced via CI (`validate-dependencies.yml`, monthly-organ-audit, promote-repo). Amendments appended to a hash-chained log.
- It is **launched**. All 8 organs operational since 2026-02-11. Cross-organ dispatch live. Promotion state machine running.
- It is **already public-process**. ~33 essays totaling ~130K+ words on the Jekyll site. POSSE distribution active to Mastodon + Discord.
- It is **agent-operable**. organvm-mcp-server exposes 16 tools across 5 groups. AGENTS.md and CLAUDE.md auto-generated. Dialect identity classifiable.
- It is **audited**. REPRWA itself ran end-to-end against the four core repos in May 2026; outputs in `docs/audits/` (canonical PR meta-organvm/meta-organvm--superproject#7).
- It is **provenanced**. `action_ledger` records atomic actions with cycle detection and bidirectional provenance. AI-generation explicitly tagged.
- It is **maintained**. soak-test-daily, monthly-organ-audit, ecosystem-coverage-audit, ecosystem-staleness-weekly, system-pulse-weekly, stale-detector-weekly all run.
- It is **funded-in-part**. `cvrsvs-honorvm` is NLnet-funded. `aerarium--res-publica` is the institutional/fiscal-sponsorship wrapper.

---

## V. The delta in one paragraph

The delta between the dream (telos.md) and the thing built is **mostly visibility, not capability**. The infrastructure to be a Multidimensional Lighthouse exists — registries, schemas, validators, distribution, atomization, dead-zone detection, MCP bridges, design tokens, governance hash chains. What is missing is the *visible, branded, public manifestation* of each of these as a recognizable component of the Beacon. 33 of 58 backend laws need their public face. The Logos directory (this one) is the first such face; the per-repo `seed.yaml.beacon` field (specified in `../beacon/seed-extension-v1.1.md`) is the next.

The work named in [`praxis.md`](./praxis.md) is the closure of that delta.

---

*This file is updated whenever (a) the REPRWA audit re-runs, or (b) any of the 17 named vacuums closes or opens, or (c) the underlying counts in §I change by >5%. Every update is logged in receptio as `BEACON-PRAGMA-UPDATE-NNN`.*
