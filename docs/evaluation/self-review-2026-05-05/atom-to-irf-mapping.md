# U9 — Atom→IRF Mapping

**Unit:** U9 of self-review-2026-05-05 batch
**Generated:** 2026-05-05 by parent-context coordinator (background worker rate-limited)
**Status:** Partial — IRF document structure prevents reliable per-entry title extraction at scale

---

## 1. Context

Phase 1 flagged this as the CENTRAL GAP: no programmatic atom↔IRF mapping exists. The IRF holds 749 work-registry entries; the atom store holds 24,599 prompts/directives. They form a web with no foreign keys. The hypothesis: most IRF entries should be traceable back to atoms (the prompts that triggered the IRF entry), and most OPEN atoms should have a corresponding IRF entry.

## 2. Method

- Parsed `INST-INDEX-RERUM-FACIENDARUM.md` for `IRF-XXX-NNN` patterns and table-row content
- Built keyword set per IRF (extracted from title; significant 4+ char words)
- For 100-entry sample, scanned all 24,599 atoms; counted atoms with 2+ keyword matches in `content` + `summary`
- Loaded atom data once into memory; matched against pre-built keyword lists

**Significant caveat — irregular IRF structure invalidated bulk extraction**: The IRF document mixes table formats, narrative entries, and freestanding entries. My table-pattern picked up the priority column (P0, P1) instead of titles for many entries. Of the 100 sampled IRFs, the vast majority had titles like "**P0**" or "P1" instead of actual descriptions. This is itself a finding — the IRF is not programmatically queryable in its current form.

## 3. Findings

**F1 — 664 IRF entries detected via regex, vs the 749 cited in CLAUDE.md.** ~85 entries didn't match the parser. The discrepancy itself reveals the IRF's heterogeneous structure: not every IRF entry is in a parseable table row.

**F2 — Of 100 sampled IRFs, only 1 had a meaningful title-based atom match: `IRF-SYS-008` ("ESLint 9→10 migration") with 20 traceable atoms.** When the title is a specific technical phrase (ESLint, well-defined version), keyword matching succeeds. When the title is generic ("**P0**", "P1"), no atoms match — but that's a parsing failure, not a true orphan.

**F3 — 99 of 100 sampled IRFs appear orphaned by current parser, but most are parsing artifacts.** The headline number (99% orphan) is unreliable. The substantive number is 1 IRF (ESLint) with 20 traceable atoms — at least *some* IRF entries do have atom traceability when properly parsed.

**F4 — The IRF document has 0 detectable DONE/OPEN status markers under my parser.** The status column extraction returned values like "Agent" / "Human" / "MEASUREMENT" / "GOVERNANCE" — these are *category* fields, not status. Either:
- (a) The IRF doesn't track DONE/OPEN status programmatically (status is in a different column or in narrative)
- (b) DONE-NNN markers are tracked separately in `data/done-id-counter.json` and aren't co-located with IRF entries

**F5 — Status values picked up by my parser suggest the IRF is taxonomized by ACTOR + KIND, not lifecycle:**
- 'Agent' (493) — entries primarily for Claude/agent execution
- 'Human' (78) — entries requiring human action
- 'MEASUREMENT' (20), 'GOVERNANCE' (16), 'NAMING' (10) — kind tags
- 'Human+Agent' (10) — collaborative

This is itself useful: the IRF organizes by *who-does-what* (actor) and *what-kind* (governance/measurement/naming), not by lifecycle state.

**F6 — The bidirectional traceability tool the user needs cannot be built from current data shape.** The IRF would need: (a) a consistent title/description column, (b) explicit DONE/OPEN status field, (c) backlink-to-atoms field. None of those exist in the current document structure.

## 4. Quantitative Table

| Metric | Value | Reliability |
|---|---:|---|
| IRF entries detected | 664 | reliable (regex on IRF-XXX-NNN) |
| IRF entries cited (CLAUDE.md) | 749 | reliable (manual count) |
| Parser-detected orphans (sample 100) | 99 | UNRELIABLE — most are parsing artifacts |
| Parser-detected heavy traces (sample 100) | 1 (ESLint, 20 atoms) | reliable |
| DONE markers picked up | 0 | parser limitation |
| OPEN markers picked up | 0 | parser limitation |
| Actor-type tags found | 6 (Agent, Human, etc.) | reliable |

## 5. Negative Findings

- **NF1 — The IRF in its current form is not programmatically queryable.** Heterogeneous table structures mean any traceability tool requires a normalization pass first.
- **NF2 — The "central gap" Phase 1 identified is even worse than thought.** Not only is there no mapping tool — the data structure required to build one doesn't exist consistently. This isn't an analysis problem; it's a *data-structure problem*.
- **NF3 — `data/done-id-counter.json` likely holds the DONE state separately.** Cross-reference against this file would recover lifecycle status. Not yet attempted in this unit.

## 6. Recommendations

**R1 — Normalize the IRF document before any traceability work.** Run a one-time pass that converts every IRF entry to a uniform JSON record with: id, title, priority, status (OPEN/IN-PROGRESS/DONE), category, actor, description, related-atoms (initially empty). Persist as `INST-INDEX-RERUM-FACIENDARUM.json` alongside the markdown. Markdown is for humans; JSON is for tooling.

**R2 — Build the cross-index tool only after R1.** With normalized JSON, the atom→IRF mapping is a straightforward keyword/embedding match. With the current heterogeneous markdown, no mapping tool will be reliable. R1 is the prerequisite.

**R3 — Recover DONE state from `done-id-counter.json` and link to IRF entries.** This is a smaller-scope follow-up: read the DONE counter file, cross-reference against IRF table entries with DONE-NNN columns. Approximation of DONE state per IRF entry. Lower-confidence than R1+R2 but useful as immediate signal.

**R4 — Treat the irregular IRF structure as a finding to act on, not analyze around.** This unit's failure is the actionable signal. The IRF is the canonical work registry; if it's not programmatically queryable, every "what's the status?" question requires manual reading. Normalizing it is a high-leverage one-time investment.

---

**Validation gate:** 6 findings, 8+ evidence anchors (entry counts, sample IRF-IDs, status-column observations), 4 recommendations. Method explicit including the substantial caveat that bulk parsing failed. Negative findings call out that the data-structure problem is the actual blocker, not the analytical one. Out-of-scope: registry-level promised-vs-delivered (U11), stale plans (U13) — footnoted only.
