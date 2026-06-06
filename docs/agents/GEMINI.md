# GEMINI.md - ORGAN I–VII System Context

This repository is a **planning and governance documentation corpus** for the ORGAN I–VII system. It contains the complete architecture, audit, and implementation strategy for an eight-organ creative-institutional system coordinating ~44 GitHub repositories across 8 GitHub organizations.

## 🏛️ Project Overview

The ORGAN I–VII system is designed to protect distinct modes of work (theory, art, commerce, community) from collapsing into each other while presenting the entire meta-system as a primary portfolio asset. The project follows an **AI-conductor model**, where humans direct and refine while AI generates volume (documentation, outlines, etc.).

**Owner:** @4444j99 / @4444J99
**Launch:** Criteria-driven (per D-08 in `08-canonical-action-plan.md`)
**Implementation Status:** Parallel All-Organs Deployment (v2.0)

## 🫀 The Eight-Organ Model

| Organ | Domain | GitHub Organization | Etymology |
|-------|--------|---------------------|-----------|
| **ORGAN-I** | Theory | `organvm-i-theoria` | θεωρία (contemplation) |
| **ORGAN-II** | Art | `organvm-ii-poiesis` | ποποίησις (creation) |
| **ORGAN-III** | Commerce | `organvm-iii-ergon` | ἔργον (work/product) |
| **ORGAN-IV** | Orchestration | `organvm-iv-taxis` | τάξις (arrangement) |
| **ORGAN-V** | Public Process | `organvm-v-logos` | λόγος (word/reason) |
| **ORGAN-VI** | Community | `organvm-vi-koinonia` | κοινωνία (communion) |
| **ORGAN-VII** | Marketing | `organvm-vii-kerygma` | κήρυγμα (proclamation) |

## 📐 Key Invariants

1.  **`repo-registry.json` is the Single Source of Truth**: All repository states and relationships must be defined here.
2.  **Unidirectional Dependency Flow**: Flow is strictly **I → II → III**. Back-edges are prohibited (e.g., ORGAN-III cannot depend on ORGAN-II).
3.  **Parallel Launch**: All 8 organs are represented and operational at launch day.
4.  **Documentation-First**: No Phase 2 (Validation) until Phase 1 (Documentation) is complete.
5.  **Every README is a Portfolio Piece**: Documentation is written for external visibility (grant reviewers, research labs, residencies).
6.  **Promotion State Machine**: Repos move through `LOCAL → CANDIDATE → PUBLIC_PROCESS → GRADUATED → ARCHIVED`.

## 📁 Project Structure

Primary content lives as numbered planning artifacts at the top level.

*   **Layer 0 (Genesis):** `00-a` through `00-c` — Conversational source material and audit foundations.
*   **Layer 1 (Planning):** `01` through `05` — Sequential planning toolkit (rubrics, templates, checklists, risk map).
*   **Layer 2 (Strategy):** `parallel-launch-strategy.md`, `phase-1-execution-index.md`.
*   **Layer 3 (v2 Active):** Active implementation specs (`repo-registry.json`, `docs/implementation/orchestration-system-v2.md`, `docs/implementation/github-actions-spec.md`).
*   **`docs/archive/`**: Superseded v1 documents (read-only reference).

## 🛠️ Maintenance & Validation

### Critical Files
*   **`repo-registry.json`**: Canonical registry of all 44+ repos.
*   **`.config/organvm.config.json`**: Organ metadata and naming conventions.
*   **`CLAUDE.md`**: Detailed implementation guide for AI agents.
*   **`01-readme-audit-framework.md`**: The scoring rubric (0-100) for documentation quality.

### Useful Commands
This project has no build pipeline; quality is maintained via documentation QA.

*   **Validate JSON Syntax**:
    ```bash
    jq . repo-registry.json > /dev/null
    python3 -m json.tool .config/organvm.config.json > /dev/null
    ```
*   **Find Unresolved Placeholders**:
    ```bash
    rg -n "\[.*\]|TODO|TBD" *.md
    ```
*   **List Project Files**:
    ```bash
    rg --files
    ```

## 🧠 AI-Conductor Workflow

When working in this repo, agents should prioritize **architectural reasoning** and **systemic coherence**. Every change to a repository's status or a project's roadmap must be reflected in `repo-registry.json`. Effort is measured in **TE (Tokens-Expended)** budgets rather than human-hours.

Refer to `docs/ANNOTATED-MANIFEST.md` for a document-by-document breakdown of the corpus.
