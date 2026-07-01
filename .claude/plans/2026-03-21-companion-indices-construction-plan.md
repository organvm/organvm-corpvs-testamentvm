# Companion Indices Construction Plan

**IRF items:** IRF-IDX-001, IRF-IDX-002, IRF-IDX-003, IRF-IDX-004
**Priority:** P1 (all three content indices) + P2 (CLI tooling)
**Date:** 2026-03-21
**Blockers:** None. All data sources exist. Pattern exists (INST-INDEX-RERUM-FACIENDARUM.md).

---

## Why These Exist

The four-index apparatus is a classical scholarly reference system:
- **Locorum** (places): WHERE things are
- **Nominum** (names): WHAT things are called
- **Rerum** (things): WHAT things ARE
- **Rerum Faciendarum** (things to be done): WHAT REMAINS — **already built**

The first three are reference instruments. The fourth is a governance instrument. Together they provide complete navigability of a 117-repo, 8-organ system.

---

## 1. INST-INDEX-LOCORUM.md (IRF-IDX-001)

**Purpose:** Canonical map of where everything lives.

### Data Sources (all verified to exist)

| Source | Location | Yields |
|--------|----------|--------|
| registry-v2.json | organvm-corpvs-testamentvm/ | 118 repos with org, name, status |
| Deployment URLs | registry-v2.json `deployment_url` fields | 21 live URLs (netlify, pages.dev, github.io, vercel) |
| GitHub organizations | 8 orgs | organvm-i-theoria through meta-organvm |
| seed.yaml files | 74/117 repos | produces/consumes edges, artifact paths |
| Vercel projects | vercel.com dashboard | stakeholder-portal, portfolio |
| Neon databases | console.neon.tech | small-fog-61557376 (Hermeneus DB) |
| Cloudflare | pages.dev deployments | gamified-coach-interface, the-actual-news, turfsynth |
| MCP servers | ~/Workspace/mcp-servers/ | filesystem, memory, sequential-thinking |
| API routes | Hermeneus concordance | 7 routes documented |
| CLI entry points | pyproject.toml files | organvm, alchemia, ontologia, cce, organvm-dashboard, organvm-mcp, organvm-validate |

### Proposed Structure

```markdown
# INST — Index Locorum
## GitHub Organizations (8)
  Table: org name, URL, repo count, organ
## Repositories (118)
  Table per organ: repo name, org, URL, deployment URL, status
## Deployment Targets (21+)
  Table: URL, platform (Vercel/Netlify/Cloudflare/GitHub Pages), repo, status
## Infrastructure Endpoints
  ### Databases: Neon (Hermeneus), local Postgres
  ### MCP Servers: filesystem, memory, sequential-thinking
  ### API Routes: 7 Hermeneus routes (from concordance)
## CLI Entry Points (7)
  Table: command, package, pyproject.toml location
## Key Files
  Table: registry-v2.json, governance-rules.json, system-metrics.json, VISION.md, etc.
```

### Generation Command

```bash
# Manual first pass, then automate via IRF-IDX-004:
organvm registry list --json | python3 -c "..." > sections/repos.md
organvm seed discover | ... > sections/seeds.md
grep -roh 'https://.*\.\(app\|io\|dev\|com\)' registry-v2.json | sort -u > sections/urls.md
```

**Estimated size:** ~400 lines. **Effort:** 1 session.

---

## 2. INST-INDEX-NOMINUM.md (IRF-IDX-002)

**Purpose:** Registry of all named entities.

### Data Sources (all verified to exist)

| Source | Location | Yields |
|--------|----------|--------|
| Organs | organvm-engine organ_config.py | 8 organs with Greek names |
| Repos | registry-v2.json | 118 repos with display_name |
| CLI tools | pyproject.toml [project.scripts] | 7 CLI commands |
| Agent personas | Hermeneus personas.ts | hermeneus, advisor |
| Vigiles regimes | vigiles-aeternae engine | 22 regimes |
| Watcher orders | vigiles-aeternae engine | 8 orders |
| SPECs | organvm-corpvs-testamentvm/specs/ | 22 SPEC-*.md files |
| SOPs | praxis-perpetua/standards/ | 57 SOP files |
| Dissertations | inquiry-log.yaml | 3: D-001 (Precision Pipeline), D-002 (Evaluative Authority), D-003 (Everything Change) |
| Faculties | inquiry-log.yaml | applied-systems, governance, meta-cognition, + others |
| Named protocols | governance docs | Testament, Descent, Membrane, Styx |
| People | governance docs | Chris (the Provost), Anthony (operator) |
| IRF namespaces | concordance.md | 21 namespaces (SYS, IDX, SKL, MON, CRP, SGO, VIG, TRV, TST, OBJ, KER, PRT, APP, GEN, IRA, ARC, BLK, DOC, VER, RES, HRM) |
| Ontologia entities | ~/.organvm/ontologia | 1836 entities (1712 modules, 8 organs, 116 repos) |

### Proposed Structure

```markdown
# INST — Index Nominum
## Organs (8)
  Table: key, Greek name, English name, domain, GitHub org
## Repositories (118)
  Table: name, display_name, organ, tier, status
## CLI Tools (7)
  Table: command, package, description
## Agent Personas (2+)
  Table: id, display_name, role, requires_auth
## Governance Entities
  ### Vigiles Regimes (22) — table: name, scope, trigger
  ### Watcher Orders (8) — table: name, jurisdiction
  ### Named Protocols (4) — Testament, Descent, Membrane, Styx
## Specifications (22)
  Table: SPEC-NNN, title, status, location
## Standard Operating Procedures (57+)
  Table: SOP name, scope, phase, location
## Research Programme
  ### Dissertations (3): D-001, D-002, D-003
  ### Faculties: governance, applied-systems, meta-cognition, ...
  ### Papers (13): SGO-2026-RP-*, SGO-2026-SYN-*
## People
  Chris (the Provost), [name redacted] (operator/creator)
## IRF Namespaces (21)
  Table: prefix, domain, item count
```

**Estimated size:** ~600 lines. **Effort:** 1–2 sessions.

---

## 3. INST-INDEX-RERUM.md (IRF-IDX-003)

**Purpose:** Ontological inventory of what exists.

### Data Sources (all verified to exist)

| Source | Location | Yields |
|--------|----------|--------|
| Ontologia | ~/.organvm/ontologia | 1836 entities with UIDs, types, states |
| seed.yaml produces/consumes | 74 seed files | artifact declarations with types |
| File extensions | `organvm registry` code_files metric | 23,121 code files |
| Test files | `organvm registry` test_files metric | 4,337 test files |
| Artifact types | seed.yaml `type` fields | web-application, api-endpoint, python-package, CLI, etc. |
| Governance artifacts | specs/, sops/, regimes/ | YAML spec, markdown SOP, regime definition |
| Testament chain | chain.jsonl | 146 produced artifacts across 14 types |
| Research artifacts | inquiry-log.yaml | dissertations, papers, bibliographies |

### Proposed Structure

```markdown
# INST — Index Rerum
## Artifact Type Taxonomy
  Table: type, count, examples, produced_by
## By State
  ### Implemented — artifacts with code, tests, deployment
  ### Specified — SPEC documents without full implementation
  ### Planned — IRF items without spec or code
## By Relationship
  ### Produces/Consumes Graph — from seed.yaml edges (55 dependency edges)
  ### depends_on — from registry dependencies
  ### references — from cross-document citations
## By Provenance
  ### Session Attribution — which session created what (S1–S28)
  ### Commit Attribution — significant commits with their artifacts
## Testament Artifacts (146)
  Table: modality, count (visual: 129, statistical: 7, schematic: 5, ...)
## Code Inventory
  ### By Language — .ts, .py, .md, .yaml, .json
  ### By Function — src/, tests/, scripts/, docs/
```

**Estimated size:** ~500 lines. **Effort:** 1–2 sessions.

---

## 4. IRF-IDX-004 — CLI Generation Tooling

**Purpose:** `organvm index generate locorum|nominum|rerum` to auto-generate indices from live data.

### Architecture

```
organvm index generate locorum
  → reads: registry-v2.json, seed.yaml files, Vercel API, .env files
  → writes: INST-INDEX-LOCORUM.md

organvm index generate nominum
  → reads: registry-v2.json, organ_config.py, vigiles engine, specs/, sops/, inquiry-log.yaml
  → writes: INST-INDEX-NOMINUM.md

organvm index generate rerum
  → reads: ontologia store, seed.yaml edges, testament chain, git log
  → writes: INST-INDEX-RERUM.md
```

**Implementation:** New module `organvm_engine/cli/index.py` with three subcommands. Pattern: existing `organvm context sync` which reads registry + seeds and generates markdown.

**Effort:** 1 session after the manual indices exist as templates.

---

## Execution Order

1. **Locorum first** — simplest (mostly URLs and paths), provides the "where" for Nominum and Rerum to reference
2. **Nominum second** — names are stable, provides vocabulary for Rerum
3. **Rerum third** — most complex (relationships, states), benefits from Locorum + Nominum existing
4. **CLI tooling last** — automates regeneration once manual versions prove the structure

---

## S28 Hermeneus Seed Data (queue for inclusion)

When building each index, these S28 artifacts must be included:

**Locorum:**
- `/api/health/llm` — LLM provider health endpoint
- `/api/cron/ingest` — Ingestion health endpoint
- `stakeholder-portal-ten.vercel.app` — Hermeneus production URL
- Neon DB: `small-fog-61557376`, branch `main`

**Nominum:**
- `Hermeneus` — display name for stakeholder-portal
- `IRF-HRM-*` — namespace (8 items)
- `provider cascade` — architectural pattern
- `ad-injection stripping` — quality governance pattern

**Rerum:**
- `provider-cascade` (type: architectural-pattern, state: implemented, provenance: S28)
- `sse-streaming` (type: feature, state: implemented, provenance: S28)
- `stale-context-detection` (type: feature, state: implemented, provenance: S28)
- `hermeneus-intelligence-ui` (type: web-application, state: deployed, URL: stakeholder-portal-ten.vercel.app)
