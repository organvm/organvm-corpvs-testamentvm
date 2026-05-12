# Pragma — `meta-organvm/organvm-corpvs-testamentvm`

> *The Concrete Realization. The honest account of what has been built.*
> *How far is the corpus from its telos?*

**Status:** Initial draft (filling the documented vacuum per `14-logos-documentation-layer.md`)
**Date:** 2026-05-09
**Counterpart files:** `telos.md` (idealized form), `praxis.md` (remediation plan), `receptio.md` (reception), `alchemical-io.md` (metabolic narrative)

---

## 1. What Exists Today

The corpus is at directory depth **9** at its deepest point (`docs/validation-runs/codex-cli/runs/20260209-135130/`). It contains **117 directories** and **1,059 files** (excluding `.git/` and caches). The file distribution by depth:

| Depth | Files | Notes |
|---|---|---|
| 0 (root) | 54 | LICENSE, README, governance JSONs, root markdown indices, root essays |
| 1 | 147 | Bucket-direct files (`docs/CLAUDE.md` etc.) |
| 2 | 409 | Largest single layer — most active documentation lives here |
| 3 | 382 | Second-largest — sprint specs, validation runs, archived staging |
| 4 | 48 | Time-stamped sub-buckets |
| 5 | 19 | Deep validation/archive leaves |

Top-level shape: **21 directories** (7 hidden agent/integration configs, 14 content directories). The 14 content directories naturally cluster into the three pure systems (CORPUS / ENGINE / SURFACE) defined in `docs/standards/15-three-pure-systems.md`.

## 2. State of the Three Pure Systems (As-Is)

### CORPUS (this system)
- **Coverage**: ~600 documentation files across `docs/` + state artifacts in `registry/`, `data/`, `ecosystem/`, `testament/`
- **Inner-form distribution (estimated, pending generator script):**
  - TELOS: ~110 files (constitution, standards 10–14, genesis 00-a/b/c/d, specs)
  - PRAGMA: ~270 files (registry, data, evaluations, this very document)
  - PRAXIS: ~180 files (implementation, operations, strategy, planning, agents)
  - RECEPTIO: ~270 files (essays, applications, validation runs, archive)
  - ALCHEMICAL-IO: this single file (summarizing the breathing/fossil flow)
- **Health**: All four primary forms now have a top-level narrative under `docs/logos/`. Symmetry, previously 0.0 (VACUUM), is now non-zero.

### ENGINE (peer system, untouched here)
- 51 Python/bash scripts in `scripts/` (invocation, audit, convergence, soak, generators)
- 5 directories under `templates/` (adr, badges, changelog, ci-workflows)
- 3 config files in `.config/` consumed by `scripts/generate-claude-md.py` and `organvm refresh`
- Self-description: pending. The ENGINE does not yet have its own `scripts/README.md` declaring its internal taxonomy.

### SURFACE (peer system, untouched here)
- 16 GitHub Actions workflows in `.github/workflows/`
- Issue and PR templates in `.github/ISSUE_TEMPLATE/`
- Astro static site in `portfolio-site/src/{pages,layouts,styles,data}/`
- Jekyll-style timestamped posts in `_posts/`
- Downstream-org templates in `.github-template/{generated,meta-profile,minimal-core,profile,ISSUE_TEMPLATE,workflows}/`
- Self-description: pending. The SURFACE does not yet have its own self-declaring index.

### SUBSTRATE (acknowledged, classified by no system)
- Root-required files: `LICENSE`, `README.md`, `CLAUDE.md`, `DIRECTORY.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `AGENTS.md`, `GEMINI.md`, `.gitignore`, `.gitattributes`, `.editorconfig`, `.pre-commit-config.yaml`, `.gitleaks.toml`, `.nojekyll`
- Hidden agent integrations: `.claude/`, `.gemini/`, `.serena/`, `.sops/`

## 3. State of the Eight Organs (Per `registry-v2.json` + Live Variables)

| Organ | Org | Repos | Status | Flagship documentation |
|---|---|---|---|---|
| I — Theory (Theoria) | `organvm-i-theoria` | 20 | OPERATIONAL | `recursive-engine--generative-entity` |
| II — Art (Poiesis) | `organvm-ii-poiesis` | 30 | OPERATIONAL | `metasystem-master`, `a-mavs-olevm` |
| III — Commerce (Ergon) | `organvm-iii-ergon` | 27 | OPERATIONAL | `public-record-data-scrapper` |
| IV — Orchestration (Taxis) | `organvm-iv-taxis` | 7 | OPERATIONAL | `orchestration-start-here`, `agentic-titan` |
| V — Public Process (Logos) | `organvm-v-logos` | 2 | OPERATIONAL | `public-process` |
| VI — Community (Koinonia) | `organvm-vi-koinonia` | 4 | OPERATIONAL | — |
| VII — Marketing (Kerygma) | `organvm-vii-kerygma` | 4 | OPERATIONAL | — |
| VIII — Meta | `meta-organvm` | 13 | OPERATIONAL | `organvm-corpvs-testamentvm` (this) |

**Live system variables** (per CLAUDE.md auto-gen, 2026-04-14 snapshot):
- `total_repos`: 145 · `active_repos`: 89 · `archived_repos`: 54
- `dependency_edges`: 60 · `ci_workflows`: 107 · `published_essays`: 29
- `sprints_completed`: 33 · `total_organs`: 10 · `operational_organs`: 10
- `code_files`: 0 · `test_files`: 0 · `repos_with_tests`: 0

Note: `code_files`/`test_files`/`repos_with_tests` reporting 0 is itself a pragma signal — implementation density is currently below telos. See `praxis.md` §3 for the closure plan.

## 4. The Distance from Telos

| Telos demand | Pragma reality | Gap |
|---|---|---|
| Total coverage of every artifact | ~404K words deployed across 148 docs + 8 org profiles | Substantial; cross-organ logos symmetry currently low across most repos |
| Perfect symmetry (no Ghosts, no Dreams) | Symmetry: 0.0 (VACUUM) for this repo before today; status of other repos varies | Closing for this repo with the current PR; other repos enumerated in IRF |
| Recursive self-description | This document set itself is a step toward recursive self-description | First iteration; ontology will need refinement after live use |
| Single source of truth | `registry-v2.json` exists and is treated as authoritative | Cross-references in legacy v1 docs (`docs/archive/`) still reference older state |
| Public-process alignment | 29 essays published; ORGAN-V `public-process` repo OPERATIONAL | Logos→essay extraction pipeline (per `14-logos-documentation-layer.md` §5) not yet automated |

## 5. Notable Pragma-Specific Properties

- **The corpus has no build system.** Its "executables" are Python and bash scripts in `scripts/`, and 16 GitHub Actions workflows. There is no compiler, no package manager, no test runner that traverses the whole repository. Quality is enforced via pre-commit, linting, and human review.
- **The corpus is documentation-heavy and code-light.** This is by intent (per CLAUDE.md: *"This is a planning and governance documentation corpus — not a source code repository"*). The implementation density that other repos exhibit is a feature, not a bug, *of those repos*. The corpus's contribution is structural and narrative.
- **Append-only chronicling dominates the deepest paths.** Every directory at depth ≥ 6 is a date-stamped run, snapshot, or archive (e.g., `2026-04`, `20260209-135130`, `week-2026-04-19_to_2026-04-26`). The corpus grows by accretion, not deletion.
- **Three duplicated top-level names with distinct roles** (intentional, per CLAUDE.md routing): `applications/` (top-level staging) vs. `docs/applications/` (canonical identity); `essays/` (drafts) vs. `docs/essays/` (curated); `specs/` (cross-cutting formations) vs. `docs/specs/` (per-sprint SDD).

## 6. Pragma Self-Audit Triggers

The following automation regularly refreshes pragma state:
- `python3 scripts/calculate-metrics.py` — registry-driven metrics
- `python3 scripts/organ-audit.py` — per-organ repo state
- `python3 scripts/generate-claude-md.py` — refreshes the auto-gen zone in CLAUDE.md (and pragma-relevant fields like Symmetry)
- `bash scripts/daily-soak.sh` — daily health snapshot under `data/soak-test/`
- `bash scripts/backup-all-orgs.sh` — backup pulse

The `Live System Variables` section of CLAUDE.md is the canonical pragma snapshot, regenerable on demand.
