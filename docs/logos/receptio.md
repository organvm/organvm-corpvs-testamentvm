# Receptio — `meta-organvm/organvm-corpvs-testamentvm`

> *Reception. The account of how the corpus has been received by the world or the constructed polis —*
> *AND the symmetric inversion: what the corpus attracts and absorbs from the contextual universe beyond itself.*

**Status:** Initial draft (filling the documented vacuum per `14-logos-documentation-layer.md`)
**Date:** 2026-05-09
**Counterpart files:** `telos.md` (idealized form), `pragma.md` (concrete state), `praxis.md` (remediation plan), `alchemical-io.md` (metabolic narrative)

---

## 1. Two Directions of Reception

Reception in this corpus is bidirectional. The corpus is read **and** the corpus reads.

| Direction | Question | Channels |
|---|---|---|
| Outward → polis | How is the corpus received by the world? | Public-process essays, applications, validation runs, citations, traffic |
| Inward ← contextual universe | What is the corpus open to absorbing? | Conversation corpora intake, fossil records, external frameworks, sibling-repo cross-pollination, scholarly references |

A corpus that is purely received but does not receive becomes a monument; a corpus that absorbs but is never read becomes a private library. The corpus's telos demands both.

## 2. Outward Reception (How the Corpus Has Been Received)

### 2.1 Public Process (ORGAN-V)
- **29 essays published** to `organvm-v-logos/public-process` (per Live System Variables, 2026-04-14).
- Essay extraction-from-corpus pipeline is mandated by `14-logos-documentation-layer.md` §5 but not yet automated; current essays are hand-extracted.
- The essays are the corpus's primary public-facing artifact; the corpus itself is read at one remove (most readers encounter the essays before they encounter `docs/genesis/00-c-master-summary.md`).

### 2.2 Validation Runs (Cross-AI Reception)
Located in `docs/validation-runs/`. The corpus has been read and critiqued by:
- **Codex CLI** runs (`docs/validation-runs/codex-cli/runs/<timestamp>/`)
- **Gemini CLI** runs (`docs/validation-runs/gemini-cli/`)
- **GitHub Copilot CLI** runs (`docs/validation-runs/github-copilot-cli/`)
- **Conversation Corpus Engine** (`docs/validation-runs/conversation-corpus-engine/2026-03-25-s37-runtime-snapshot/`)

These runs are how the corpus checks its own intelligibility against agents trained on different distributions. Disagreement between runs is a pragma signal.

### 2.3 Application Submissions (External-Org Reception)
Located in `docs/applications/`:
- Conference proposals (`conference-proposals/`)
- Grant cover letters (`cover-letters/`)
- Profile materials (`profiles/`)
- Submission packets (`submission-materials/`)

Each application is a probe into a specific external polis (a fellowship committee, a conference program, a foundation board). The corpus is received by these polises whether or not the submission succeeds; the rejection letters are themselves receptio.

### 2.4 Sprint Catalog and IRF Closures
- **33 sprints completed** (per Live System Variables); 76 catalogued
- **549 cross-organ links** between IRF entries and registry-v2 entries
- Closing an IRF entry is internal reception — the system received the work and acknowledged it as done

### 2.5 Investor Reception
`docs/pitch/` contains pitch materials. As of 2026-05-09 this is incipient; reception is mostly internal (pitch drafts circulating among collaborators, not external investors).

### 2.6 Internal Polis Reception
- 32,128 observations recorded (per Live System Variables)
- 121 active SOPs governing reception within the system
- Concordance lookups via `python3 scripts/invoke.py <ID>` — the corpus is read by its own agents using its own invocation system

## 3. Inward Reception (What the Corpus Absorbs from the Contextual Universe)

The corpus is not a closed system. It is **porous to its environment by design**, and its long-term coherence depends on continuous absorption. The intake channels below are real and operating today.

### 3.1 Conversation Corpora (Active Intake)
- **`data/corpora/`** — weekly conversation slices (e.g., `week-2026-04-19_to_2026-04-26/`)
- **`data/corpus/april-2026/`** — month-stamped rolling corpus
- **`data/atoms/`** + **`data/atoms/backlogs/`** — atomized prompt corpus (8,218 prompts → 31,649 atoms per `seed.yaml`)
- **`data/prompt-registry/`** — registered plan and session prompts

Each session that touches the corpus contributes new atoms. The intake is automated via post-commit hooks across all workspace repos (`breathing` clause in `seed.yaml`). The corpus *grows* by absorbing the conversations that produced it.

### 3.2 Fossil Records (Append-Only History)
- **`data/fossil/fossil-record.jsonl`** — appended by witness-hooks at session-close
- **`data/fossil/chronicle/`** — chronicle entries, finer granularity

Fossils are the corpus's involuntary absorption: every session leaves a trace whether or not the contributor intends to deposit one.

### 3.3 Pulse and Telemetry
- **`data/pulse/`** — system pulse data
- **`data/dashboard/`** — system-dashboard data feeds
- **`data/organism/`** — organism-state snapshots

These channels absorb *system state* into the corpus's self-knowledge. They are not human input; they are the corpus listening to its own metabolism.

### 3.4 Sibling-Repo Cross-Pollination
Per CLAUDE.md "Siblings in Meta": `.github`, `alchemia-ingestvm`, `schema-definitions`, `organvm-engine`, `system-dashboard`, `organvm-mcp-server`, `praxis-perpetua`, `stakeholder-portal`, `materia-collider`, `organvm-ontologia`, `vigiles-aeternae--agon-cosmogonicum`, `cvrsvs-honorvm`.

The corpus consumes from `ORGAN-IV` (orchestration-artifact) and produces to `ORGAN-IV`, `META-ORGANVM/organvm-engine`, `META-ORGANVM/praxis-perpetua`, and `ALL` (per the auto-gen Edges section of CLAUDE.md). Each producer–consumer edge is a channel through which contextual material flows in and out.

The dialect-identity scan (`organvm trivium scan META <OTHER>`) is an explicit absorption tool: it identifies translation pathways between this corpus's vocabulary and a sibling's vocabulary, surfacing absorbable concepts.

### 3.5 Scholarly and Intellectual Lineages (Open Absorption Channels)
The corpus already cites, but is open to deeper absorption from, the following bodies of thought:
- **Aristotelian causation** (the four-form ontology — telos / pragma / praxis / receptio is a tetradic compression of Aristotle's final, material, efficient, formal causes; see `docs/genesis/01-artistic-triforce-creative-ontology.md`)
- **Autopoiesis** (Maturana & Varela; the recursive self-production frame implicit in ORGAN-I's Recursive Engine)
- **Cybernetics** (second-order in particular — von Foerster, Pask; the "system observing its own observing" matches the corpus's recursive self-description)
- **Knowledge commons governance** (Ostrom's design principles; relevant to ORGAN-VI Koinonia)
- **AI-alignment scholarship** (Anthropic constitutional methods, recursive reward modeling — relevant to the AI-conductor model)
- **Archival science** (Cook, Schwartz on archives as active sites; relevant to `docs/archive/` discipline)
- **Liturgical and constitutional traditions** (the ORGANVM vocabulary draws on Greek and Latin canonical forms — telos, pragma, praxis, receptio, logos, koinonia, kerygma, theoria, poiesis, ergon, taxis — these are not ornament; they are inherited governance technology)

The corpus does not yet have a `docs/logos/bibliography.md`; this is a candidate IRF entry under IRF-DOC.

### 3.6 Outside-Tooling Absorption
The corpus integrates with external tools as absorption surfaces:
- **HuggingFace Hub** (per MCP server `mcp__875c6b6b...__hf_hub_query`) — model and dataset discovery; arxiv references via tag system
- **GitHub MCP server** — issue, PR, repo metadata absorption from the broader GitHub ecosystem
- **Anthropic Claude API** — the very generation that produces this document; the corpus absorbs Claude's training distribution every time it asks a question
- **Notion / Calendar / Drive integrations** (per the loaded MCP tool list) — administrative and scheduling context

## 4. The Discipline of Absorption

Pure absorption is not a virtue; *disciplined* absorption is. The corpus enforces three rules:

1. **Provenance.** Every absorbed artifact carries its source. `provenance-registry.json` tracks origin for absorbed material; un-attributable absorption is a defect.
2. **Routing.** Absorbed material lands in the correct system: documents into CORPUS, code/scripts into ENGINE, surface assets into SURFACE. CLAUDE.md's "Artifact Routing" decision tree (Q1/Q2/Q2b/Q3) governs this.
3. **Triage.** Unsorted absorbed material lands in `~/Workspace/intake/` (per CLAUDE.md Q3) and is triaged later. The corpus does not commit raw absorption directly to its trunk.

A future enforcement: a CI check that flags any commit to `docs/` containing material whose provenance chain is broken or whose routing is wrong.

## 5. The Ghost-Vacuum That This Document Closes

Per CLAUDE.md auto-gen prior to today: **Status: MISSING | Symmetry: 0.0 (VACUUM)**.

The vacuum existed because, while the corpus exhaustively *received* (29 essays published, 33 sprints closed, 32,128 observations recorded, 8,218 prompts atomized), it had not *narrated its reception*. The pragma was rich; the receptio was empty. This document, plus the four siblings in `docs/logos/`, ends that asymmetry.

Subsequent revisions of this file will track:
- New essays published to ORGAN-V
- Cross-AI validation runs producing notable agreement or disagreement
- Application outcomes (acceptance, rejection, silence — all are receptio)
- Sibling-repo absorption events that reshape the corpus's vocabulary
- New scholarly lineages absorbed into the bibliography (when one exists)

## 6. Reception's Ongoing Demand

If the corpus is to fulfill its telos, it must remain porous in both directions: continuously *read* by an expanding polis, and continuously *reading* an expanding contextual universe. Any closure of either direction — over-curation that excludes new readers, or insularity that excludes new sources — is a defect to be tracked in `pragma.md` and remediated via `praxis.md`.

The asymptotic posture: the corpus is a *living interface* between the eight-organ system and everything else.
