# Intellectual Property Reference — ORGANVM System

**Version:** 1.0.0 | **Date:** 2026-03-04
**Scope:** All repositories across the 8-organ system (~103 repos, 8 GitHub organizations)
**Author:** @4444j99

This document is a reference summary, not a legal contract. Each repository's LICENSE file is the authoritative source for that repository's licensing terms.

---

## 1. Licensing Overview

The ORGANVM system uses a dual-license model:

| Content Type | License | Applies To |
|---|---|---|
| Source code | **MIT License** | All code repositories (organvm-engine, system-dashboard, alchemia-ingestvm, ORGAN-I through ORGAN-VII code repos, etc.) |
| Documentation corpus | **CC BY-SA 4.0** (Creative Commons Attribution-ShareAlike 4.0 International) | organvm-corpvs-testamentvm (planning docs, essays, governance corpus, ~410K+ words) |

Every repository contains a LICENSE file at its root. The copyright holder is listed as either `4444J99` or `organvm` depending on the GitHub organization. Individual repo LICENSE files are the authoritative source; this document summarizes the pattern.

## 2. Original Work Declaration

All source code, documentation, architectural designs, governance frameworks, and creative content across the ORGANVM system are original works by @4444j99, except where explicitly attributed otherwise. This includes:

- The eight-organ architectural model (Theoria, Poiesis, Ergon, Taxis, Logos, Koinonia, Kerygma, Meta)
- The promotion state machine (LOCAL, CANDIDATE, PUBLIC_PROCESS, GRADUATED, ARCHIVED)
- The repo-registry.json schema and governance-rules.json specification
- All 6 canonical JSON schemas in schema-definitions
- The organvm-engine CLI and its 12 command groups
- The MCP server implementation and its 16 tools
- The governance corpus (~410K+ words of planning, strategy, and process documentation)
- All generative art systems, performance frameworks, and creative coding projects in ORGAN-II

Where third-party code, algorithms, or ideas are incorporated, attribution is provided in the relevant repository's README, CHANGELOG, or inline comments.

## 3. AI-Generated Content Disclosure

The ORGANVM system is built using an **AI-conductor model**, as documented in the project constitution (Amendment D) and the public-process essay series. This means:

- **Human directs**: All architectural decisions, strategic direction, creative vision, and quality standards are set by the human author (@4444j99)
- **AI generates volume**: Large Language Models (primarily Claude by Anthropic) are used to generate initial drafts of documentation, code scaffolding, and boilerplate
- **Human reviews and refines**: All AI-generated output undergoes human review for accuracy, voice, and fitness for purpose

Effort is measured in Tokens-Expended (TE), not human-hours, reflecting this methodology. The total system budget is approximately 6.5M TE.

This disclosure is made voluntarily in the interest of transparency. The AI-conductor model is a documented methodology, not a limitation on the originality or copyright status of the resulting works. The human author retains full creative control and responsibility for all published content.

## 4. Third-Party Dependencies

All repositories declare their dependencies explicitly:

| Stack | Dependency File | Package Registry |
|---|---|---|
| Python | `pyproject.toml` (`[project.dependencies]`) | PyPI |
| TypeScript/JavaScript | `package.json` (`dependencies`, `devDependencies`) | npm |
| Rust | `Cargo.toml` | crates.io |

All third-party dependencies are open-source packages with compatible licenses (MIT, Apache-2.0, BSD, ISC, or similar permissive licenses). No proprietary or copyleft-incompatible dependencies are used in MIT-licensed code repositories.

Dependency trees can be audited using standard tooling (`pip list`, `npm ls`, `cargo tree`).

## 5. Trademark and Naming

The following names and conventions are used consistently across the system but are **not registered trademarks**:

- **ORGANVM** — the system name (Latin-styled spelling)
- **Organ numbering** — the I through VII + Meta designation scheme
- **Greek domain names** — Theoria, Poiesis, Ergon, Taxis, Logos, Koinonia, Kerygma
- **Double-hyphen convention** — single hyphen separates words, double hyphen separates function from descriptor (e.g., `recursive-engine--generative-entity`)
- **Sprint naming** — Latin/Greek sprint names (IGNITION, PROPULSIO MAXIMA, CONSTITUTIO, PROPRIETAS, etc.)

These names are used as identifiers within the system and its documentation. No trademark registration has been filed. Third parties referencing the ORGANVM system should use these names accurately and with attribution.

## 6. Data Privacy

The ORGANVM system itself — the engine, dashboard, MCP server, governance corpus, and orchestration layer — **does not collect, store, or process any user data**. It is an internal tooling and governance system.

Individual deployed products in ORGAN-III (commercial applications) may collect user data as needed for their function. Each deployed product maintains its own privacy policy appropriate to its use case. Those privacy policies are the responsibility of the individual product, not of the ORGANVM meta-system.

The `intake/` directory in the workspace contains unsorted inbound material that may include personal data archives. This content is local-only, never committed to public repositories, and is not part of any deployed system.

## 7. Export and Compliance

The ORGANVM system contains no export-controlled technology, encryption implementations, or dual-use items subject to EAR, ITAR, or equivalent regulations. The system consists of:

- Documentation and governance tooling
- Web applications and developer utilities
- Generative art and creative coding projects
- Standard open-source software dependencies

No component requires an export license for distribution.

---

*This document is maintained in `organvm-corpvs-testamentvm/docs/legal/intellectual-property.md` and is licensed under CC BY-SA 4.0 along with the rest of the governance corpus.*
