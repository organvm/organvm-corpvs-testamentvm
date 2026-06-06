# 15: Three Pure Systems — Outer-Tier Repository Architecture

**Date:** 2026-05-09
**Status:** ACTIVE — applies to `meta-organvm/organvm-corpvs-testamentvm` first; pattern extends to all repos in the eight-organ ecosystem
**Derived from:** Implicit constraints in CLAUDE.md "Document Architecture" + "Artifact Routing" sections; user directive *"purely the docs ideal demands & any scripting or surface elsewhere in its own system of purely itself"*
**Complements:** `10-repository-standards.md` (root hygiene), `14-logos-documentation-layer.md` (inner-tier ontology for CORPUS)

---

## 1. Purpose & Scope

This document declares the **outer-tier ontology** under which every non-substrate file in a repository belongs to exactly one of three pure systems. The four-form logos ontology (TELOS / PRAGMA / PRAXIS / RECEPTIO / ALCHEMICAL-IO) defined in `14-logos-documentation-layer.md` is the **inner-tier** ontology that organizes one — and only one — of the three pure systems: CORPUS.

This doctrine resolves a category error that the system's documentation has tolerated implicitly: classifying executable scripts and public-facing surface assets in the *same vocabulary* as documentation produces an ontology that mixes kinds-of-being. The three-pure-systems doctrine restores discipline: **each system is purely itself, organized by its own internal logic, never reclassified by another system's vocabulary.**

---

## 2. The Two-Tier Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│  SUBSTRATE — required-by-tools, root-anchored, classified by no system │
│  (LICENSE, README.md, CLAUDE.md, .git/, .gitignore, hidden agent       │
│   integration dirs, .pre-commit-config.yaml, etc.)                     │
└──────────────────────────────────────────────────────────────────────┘
                                 ↓ supports ↓
   ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
   │     CORPUS       │   │     ENGINE       │   │     SURFACE      │
   │  (the docs)      │   │  (the scripts)   │   │  (the interface) │
   │                  │   │                  │   │                  │
   │ Inner ontology:  │   │ Inner taxonomy:  │   │ Inner taxonomy:  │
   │   TELOS          │   │   invocation     │   │   ci-workflow    │
   │   PRAGMA         │   │   generators     │   │   issue-form     │
   │   PRAXIS         │   │   audit          │   │   org-template   │
   │   RECEPTIO       │   │   convergence    │   │   portfolio      │
   │   ALCHEMICAL-IO  │   │   soak / health  │   │   blog           │
   │                  │   │   validators     │   │                  │
   └──────────────────┘   └──────────────────┘   └──────────────────┘
       pure docs              pure code            pure interface
   The corpus IS this     The corpus USES this   The corpus MEETS
                                                  the world via this
```

### 2.1 The Three Pure Systems

| System | Essence | Internal organizing principle | Vocabulary |
|---|---|---|---|
| **CORPUS** | The documentation; the repository's *narrative record*; what the repo IS | Four-form logos ontology per `14-logos-documentation-layer.md` | `telos`, `pragma`, `praxis`, `receptio`, `alchemical-io` |
| **ENGINE** | The executable machinery operating on the corpus; what the repo USES | Function-based taxonomy: invocation, generators, audit, convergence, soak/health, validators, deploy | `function`, `invoked_by`, `consumes`, `produces` |
| **SURFACE** | The public-facing interface; how the repo MEETS the world | Interface-type taxonomy: ci-workflow, issue-form, org-template, portfolio, blog | `interface_type`, `external_dependency`, `tool_locked` |

### 2.2 The SUBSTRATE Layer

SUBSTRATE is **not** a fourth pure system. It is the *ground* on which the three rest. A file is in SUBSTRATE *only* if its existence at that exact path is mandated by an external tool or convention, including:

- **VCS internals**: `.git/`
- **Tool-required root files**: `LICENSE`, `README.md`, `CLAUDE.md`, `.gitignore`, `.gitattributes`, `.editorconfig`, `.pre-commit-config.yaml`, `.gitleaks.toml`, `.nojekyll`
- **Per-agent integration scaffolding**: `.claude/`, `.gemini/`, `.serena/`, `.sops/`
- **Repo-meta navigation**: `DIRECTORY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `AGENTS.md`, `GEMINI.md`

A file that *could* live elsewhere but currently sits at root for organizational reasons (e.g., `essay-1-bootstrap-to-scale.md`) is **CORPUS-typed**, not SUBSTRATE — substrate is determined by external mandate, not by current placement.

---

## 3. Core Demands

### Demand 1 — Single-system membership
Every non-substrate file belongs to **exactly one** of CORPUS / ENGINE / SURFACE. Not zero. Not two. The classifier surfaces any orphan as `UNCLASSIFIED` (a defect to remediate).

### Demand 2 — Vocabulary discipline
- **TELOS / PRAGMA / PRAXIS / RECEPTIO / ALCHEMICAL-IO** apply only inside CORPUS. They never appear as classifications for ENGINE or SURFACE files.
- **invocation / generators / audit / convergence / soak / validators / deploy** apply only inside ENGINE.
- **ci-workflow / issue-form / org-template / portfolio / blog** apply only inside SURFACE.

A `scripts/audit.py` is **not** PRAXIS — it is ENGINE / audit. A `.github/workflows/ci.yml` is **not** RECEPTIO — it is SURFACE / ci-workflow. Misapplication is a category error.

### Demand 3 — Each system describes itself in its own terms
- CORPUS publishes `docs/logos/{telos,pragma,praxis,receptio,alchemical-io}.md` per `14-logos-documentation-layer.md`.
- ENGINE publishes `scripts/README.md` (or equivalent) declaring its function-based internal taxonomy and per-script inventory.
- SURFACE publishes its self-description in its native territory (typically `.github/README.md` or a comparable interface-index doc).

The doctrine doc itself (this file) lives in CORPUS because it is a **demand the corpus makes of itself** — that is `TELOS` per the inner ontology.

### Demand 4 — Cross-system manifests are derived, never authored manually
Any artifact that classifies files across system boundaries is generated by an ENGINE script and lives in the territory it describes:
- `docs/logos/manifest.csv` (CORPUS-internal classification) — generated by `scripts/generate-logos-manifest.py`
- `scripts/manifest.csv` (ENGINE-internal classification) — generated by the same script's ENGINE pass
- `surface-manifest.csv` or similar (SURFACE-internal classification) — generated by the same script's SURFACE pass

No human authors a cross-system row; the classifier is the single source of truth for system-membership.

### Demand 5 — Substrate is acknowledged, not absorbed
SUBSTRATE files are listed in each system's manifest as `exempt=TRUE` with an `exempt_reason`, but are not classified by that system's internal vocabulary. `LICENSE` is not RECEPTIO; `.github/workflows/ci.yml` is **not** SUBSTRATE merely because GitHub mandates the path — the path is mandated, but the file is SURFACE / ci-workflow. SUBSTRATE is the smaller set: files whose *existence* and *path* are *both* externally mandated (`.gitignore`, `LICENSE`, `.git/`).

---

## 4. Path Assignment for `meta-organvm/organvm-corpvs-testamentvm`

The 21 top-level directories of this corpus partition cleanly into the four layers:

### CORPUS
`docs/`, `registry/`, `data/`, `ecosystem/`, `testament/`, `site-data/` (state telemetry consumed by docs), `essays/`, `applications/`, `specs/`, `_posts/` (TBD — see §5)
Plus root markdown not in SUBSTRATE: `INST-INDEX-LOCORUM.md`, `INST-INDEX-RERUM-FACIENDARUM.md`, `IRF-V3-SPEC.md`, `ONTOLOGY-V2-SKETCH.md`, `essay-1-…-essay-8.md`, `CAPTAINS-LOG.md`, plus all root JSON/YAML governance files (`organ-definitions.json`, `governance-rules.json`, `governance-config.yaml`, `governance-amendments.jsonl`, `metrics-targets.yaml`, `vars-targets.yaml`, `seed.yaml`, `task-manifest.yaml`, `system-metrics.json`, `system-snapshot.json`, `system-vars.json`, `workspace-manifest.json`, `provenance-registry.json`, `praxis-distribution-report.json`, `praxis-flagship-report.json`, `code-substance-report.json`, `ecosystem.yaml`, `repo-registry.json`).

### ENGINE
`scripts/`, `templates/`, `.config/` (env config consumed exclusively by scripts).

### SURFACE
`.github/`, `.github-template/`, `portfolio-site/`. (`_posts/` is candidate-SURFACE if it feeds a static-site renderer; pending §5.)

### SUBSTRATE
`.git/`, `.claude/`, `.gemini/`, `.serena/`, `.sops/`, `LICENSE`, `README.md`, `CLAUDE.md`, `DIRECTORY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `AGENTS.md`, `GEMINI.md`, `.gitignore`, `.gitattributes`, `.editorconfig`, `.pre-commit-config.yaml`, `.gitleaks.toml`, `.nojekyll`.

---

## 5. Edge Cases and Open Decisions

### 5.1 `_posts/`
Jekyll convention places posts under `_posts/`, but the repo also contains `.nojekyll` disabling Jekyll. If `_posts/` content is ingested by `portfolio-site/` (Astro), the directory is SURFACE / blog. If `_posts/` is residual or moved to ingestion-by-CORPUS, it is RECEPTIO. **Resolution required**; pending IRF entry under IRF-OPS.

### 5.2 `templates/`
Templates are consumed by ENGINE scripts to generate per-repo artifacts. They are themselves not executable, but they are ENGINE-machinery (input to generators). Classifying as ENGINE for now; any template that becomes a *displayed* artifact (e.g., a portfolio template) graduates to SURFACE.

### 5.3 `site-data/`
Currently classified as CORPUS / PRAGMA (state-of-the-corpus telemetry) because it is human-readable JSON describing system state. If a future site-data file is consumed *only* by the static-site build, it becomes SURFACE.

### 5.4 `.github-template/`
The downstream-template directory is SURFACE because it propagates SURFACE-typed files (org profiles, issue templates, workflows) to other repos. Even though it lives at root, its contents are interface-shaped.

### 5.5 Root JSON/YAML
The 19+ root JSON/YAML files (`repo-registry.json`, `organ-definitions.json`, etc.) are CORPUS / PRAGMA — they are the corpus's machine-readable self-knowledge. They are *not* SUBSTRATE despite living at root, because they are not externally mandated to be there in name or location.

---

## 6. Enforcement

| Mechanism | Where | When |
|---|---|---|
| Inner-ontology generator | `scripts/generate-logos-manifest.py` (deferred to follow-up PR) | Pre-commit and on-demand |
| ENGINE self-description | `scripts/README.md` (pending) | Hand-authored; updated when new functions are added |
| SURFACE self-description | `.github/README.md` (pending) | Hand-authored; updated when new interfaces are added |
| Cross-system orphan check | CI workflow (deferred) | On every PR; fails if any non-substrate file is `UNCLASSIFIED` |
| Doctrine self-citation | This file | Updated when category boundaries are revised; revisions require constitutional review |

---

## 7. Migration Path for Other Repos

The pattern established here for `organvm-corpvs-testamentvm` rolls outward in three waves:

1. **Wave 1 (this PR)** — Establish the doctrine and the CORPUS-side instantiation in this repo. Demonstrate that the inner-tier logos files honor the standard.
2. **Wave 2** — ENGINE and SURFACE self-descriptions for this repo (follow-up PRs scoped to those territories).
3. **Wave 3** — Roll the doctrine to other meta-organvm flagship repos, then organ flagships, then long-tail repos. The IRF tracks each repo's adoption status.

---

## 8. Relationship to Inner Logos Standard

This standard does **not** replace `14-logos-documentation-layer.md`. The inner-tier logos standard remains in force for CORPUS. This standard adds the outer-tier separation that scopes inner-tier vocabulary to its proper system.

A repo cannot satisfy `14` without `15`: applying the four-form logos vocabulary to a `scripts/` directory would violate Demand 2. A repo cannot satisfy `15` without `14`: declaring CORPUS as a pure system without its inner ontology leaves the corpus undefined internally.

The two standards are **co-required**.

---

## 9. Open IRF Entries Generated by This Doctrine

- **IRF-DOC-XXX**: Migrate `seed.yaml` to schema v1.2 (adds machine-readable telos/pragma/praxis/receptio summaries)
- **IRF-OPS-XXX**: Resolve `_posts/` system-membership (CORPUS or SURFACE)
- **IRF-OPS-XXX**: Author `scripts/README.md` (ENGINE self-description)
- **IRF-OPS-XXX**: Author SURFACE self-description (location TBD: `.github/README.md` may be reserved for org-profile rendering)
- **IRF-OPS-XXX**: Implement `scripts/generate-system-manifests.py` and CI orphan check
- **IRF-DOC-XXX**: Roll three-pure-systems doctrine to next meta-organvm flagship

---

## Appendix: Worked Examples

| File | System | Inner classification | Why |
|---|---|---|---|
| `docs/memory/constitution.md` | CORPUS | TELOS / memory | The repo's immutable principles |
| `repo-registry.json` | CORPUS | PRAGMA / root-singleton | Authoritative state-of-the-corpus |
| `docs/strategy/sprint-catalog.md` | CORPUS | PRAXIS / strategy | Documentation about action |
| `docs/validation-runs/codex-cli/runs/20260209-135130/result.json` | CORPUS | RECEPTIO / validation-runs | External-AI reception of the corpus |
| `data/fossil/fossil-record.jsonl` | CORPUS | ALCHEMICAL-IO / fossil | Metabolic flow record |
| `scripts/invoke.py` | ENGINE | invocation | Lookup utility |
| `scripts/generate-claude-md.py` | ENGINE | generators | Refresh auto-gen zone |
| `scripts/organ-audit.py` | ENGINE | audit | Per-organ state inspection |
| `templates/adr/template.md` | ENGINE | generators (input) | Consumed by generator scripts |
| `.github/workflows/ci.yml` | SURFACE | ci-workflow | GitHub Actions runner |
| `.github/ISSUE_TEMPLATE/bug.md` | SURFACE | issue-form | GitHub issue UI |
| `.github-template/profile/README.md` | SURFACE | org-template | Downstream-org propagation |
| `portfolio-site/src/pages/index.astro` | SURFACE | portfolio | Astro public site |
| `LICENSE` | SUBSTRATE | — | Externally mandated by license discovery |
| `.gitignore` | SUBSTRATE | — | Required by git |
| `CLAUDE.md` | SUBSTRATE | — | Required by Claude Code agent |
