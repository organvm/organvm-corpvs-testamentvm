# INST — Index Locorum

**Status:** ACTIVE
**Created:** 2026-03-23
**Authority:** META — System-wide reference instrument
**Purpose:** Canonical map of where everything lives — repos, directories, key files, URLs, infrastructure endpoints.

> *Index Locorum* — the classical index of places. In the ORGANVM system, "places" are repos, directories, files, URLs, and infrastructure endpoints. This is the second of four classical indices; see the Index Rerum Faciendarum for the complete apparatus.

### The Four Indices

| Index | Latin | Purpose | Status |
|-------|-------|---------|--------|
| **Index Rerum Faciendarum** | *Things to be done* | Universal work registry | `INST-INDEX-RERUM-FACIENDARUM.md` |
| **Index Locorum** | *Index of places* | Canonical map of where everything lives | **THIS DOCUMENT** |
| **Index Nominum** | *Index of names* | Registry of all named entities | `INST-INDEX-NOMINUM.md` (law built; census pending) |
| **Index Rerum** | *Index of things* | Ontological inventory of what exists | IRF-IDX-003 (planned) |

---

## Workspace Topology

`~/Workspace/` — the root. Not a git repo. Contains organ superproject directories, non-organ directories, and workspace-level metadata files.

### Organ Directories

Each organ directory is a **git superproject** tracking its repos as submodules. The directory name matches the GitHub org name.

| Directory | Organ | GitHub Org | Registry Repos | Local Repos | Domain |
|-----------|-------|-----------|---------------|-------------|--------|
| `organvm-i-theoria/` | I | `organvm-i-theoria` | 21 | 16 | Foundational theory, recursive engines, symbolic computing |
| `organvm-ii-poiesis/` | II | `organvm-ii-poiesis` | 32 | 8 | Generative art, performance systems, creative coding |
| `organvm-iii-ergon/` | III | `organvm-iii-ergon` | 29 | 7 | Commercial products, SaaS tools, developer utilities |
| `organvm-iv-taxis/` | IV | `organvm-iv-taxis` | 18 | 20 | Orchestration, governance, AI agents, skills |
| `organvm-v-logos/` | V | `organvm-v-logos` | 2 | 7 | Public discourse, essays, editorial, analytics |
| `organvm-vi-koinonia/` | VI | `organvm-vi-koinonia` | 6 | 6 | Community, reading groups, salons, learning |
| `organvm-vii-kerygma/` | VII | `organvm-vii-kerygma` | 4 | 7 | Marketing, POSSE distribution, announcements |
| `meta-organvm/` | META | `meta-organvm` | 12 | 19 | Cross-organ engine, schemas, dashboard, governance corpus |
| `4444J99/` | LIMINAL | `4444j99` | — | 5 | Personal projects: portfolio, artist site, dotfiles |

**Note:** Registry repos includes archived repos. Local repos count only non-hidden subdirectories present on disk.

### Non-Organ Directories

| Directory | Purpose | Git? |
|-----------|---------|------|
| `dwv/` | Digital Value Workspace — consilivm-simplex (Padavano consulting) + specvla-ergon--avditor-mvndi (Avditor Mvndi SaaS) | No (contains sub-repos) |
| `blender-mcp/` | Blender MCP integration addon (forked) | Yes |
| `gemini-cli-blender-extension/` | Gemini CLI Blender extension | Yes |
| `alchemia-ingestvm/` | Data staging area for ingestion pipeline (separate from META submodule) | No |
| `intake/` | Unsorted inbound material — docs, specs, code fragments, personal archives. Treat as untrusted. | No |

### Workspace-Level Files

| File | Purpose |
|------|---------|
| `workspace-manifest.json` | Maps all organ superprojects and non-organ directories (schema v1.0) |
| `CLAUDE.md` | AI agent context for the workspace root |
| `AGENTS.md` | Multi-agent context file |
| `GEMINI.md` | Gemini agent context file |
| `sync_interlinked_landing_pages.sh` | Cross-organ landing page sync script |

---

## Repositories by Organ

### META-ORGANVM — Meta (12 repos)

The meta-organ is a **git superproject**. Submodules are tracked in `.gitmodules`. `stakeholder-portal/` and `intake/` exist locally but are NOT submodules.

| Repo | Tier | Status | Public | GitHub |
|------|------|--------|--------|--------|
| `.github` | infrastructure | ACTIVE | Yes | `github.com/meta-organvm/.github` |
| `organvm-corpvs-testamentvm` | **flagship** | ACTIVE | Yes | `github.com/meta-organvm/organvm-corpvs-testamentvm` |
| `organvm-engine` | **flagship** | ACTIVE | Yes | `github.com/meta-organvm/organvm-engine` |
| `alchemia-ingestvm` | standard | ACTIVE | Yes | `github.com/meta-organvm/alchemia-ingestvm` |
| `schema-definitions` | standard | ACTIVE | Yes | `github.com/meta-organvm/schema-definitions` |
| `system-dashboard` | standard | ACTIVE | Yes | `github.com/meta-organvm/system-dashboard` |
| `organvm-mcp-server` | infrastructure | ACTIVE | Yes | `github.com/meta-organvm/organvm-mcp-server` |
| `praxis-perpetua` | standard | ACTIVE | No | `github.com/meta-organvm/praxis-perpetua` |
| `stakeholder-portal` | standard | ACTIVE | Yes | `github.com/meta-organvm/stakeholder-portal` |
| `materia-collider` | standard | ACTIVE | No | `github.com/meta-organvm/materia-collider` |
| `organvm-ontologia` | standard | ACTIVE | Yes | `github.com/meta-organvm/organvm-ontologia` |
| `vigiles-aeternae--agon-cosmogonicum` | standard | active | Yes | `github.com/meta-organvm/vigiles-aeternae--agon-cosmogonicum` |

**Local-only directories** (not in registry, exist on disk within `meta-organvm/`):
- `data/` — Shared data directory
- `docs/` — Superproject documentation
- `docs/validation-runs/` — Cross-AI validation artifacts and preserved runtime snapshots, including `conversation-corpus-engine/2026-03-25-s37-runtime-snapshot/`
- `tools/` — Cross-repo utility scripts (audit, secrets, sync)
- `organvm-theoria-knowledge-engine/` — Knowledge engine (local development)
- `post-flood/` — Post-flood recovery artifacts
- `topological-mythos/` — Topological mythos development
- `organvm-iii-ergon/` — ORGAN-III staging area
- `intake/` — Unsorted material (not a submodule)

### ORGAN-I — Theoria (21 repos)

| Repo | Tier | Status | Public | GitHub |
|------|------|--------|--------|--------|
| `recursive-engine--generative-entity` | **flagship** | ACTIVE | Yes | `github.com/organvm-i-theoria/recursive-engine--generative-entity` |
| `auto-revision-epistemic-engine` | standard | ACTIVE | Yes | `github.com/organvm-i-theoria/auto-revision-epistemic-engine` |
| `narratological-algorithmic-lenses` | standard | ACTIVE | Yes | `github.com/organvm-i-theoria/narratological-algorithmic-lenses` |
| `call-function--ontological` | standard | ACTIVE | Yes | `github.com/organvm-i-theoria/call-function--ontological` |
| `sema-metra--alchemica-mundi` | standard | ACTIVE | Yes | `github.com/organvm-i-theoria/sema-metra--alchemica-mundi` |
| `cognitive-archaelogy-tribunal` | standard | ACTIVE | No | `github.com/organvm-i-theoria/cognitive-archaelogy-tribunal` |
| `linguistic-atomization-framework` | standard | ACTIVE | Yes | `github.com/organvm-i-theoria/linguistic-atomization-framework` |
| `my-knowledge-base` | standard | ACTIVE | Yes | `github.com/organvm-i-theoria/my-knowledge-base` |
| `styx-behavioral-economics-theory` | standard | ACTIVE | Yes | `github.com/organvm-i-theoria/styx-behavioral-economics-theory` |
| `vigiles-aeternae--corpus-mythicum` | standard | active | Yes | `github.com/organvm-i-theoria/vigiles-aeternae--corpus-mythicum` |
| `.github` | infrastructure | ACTIVE | Yes | `github.com/organvm-i-theoria/.github` |
| `organon-noumenon--ontogenetic-morphe` | standard | ARCHIVED | Yes | `github.com/organvm-i-theoria/organon-noumenon--ontogenetic-morphe` |
| `a-recursive-root` | standard | ARCHIVED | Yes | `github.com/organvm-i-theoria/a-recursive-root` |
| `radix-recursiva-solve-coagula-redi` | standard | ARCHIVED | Yes | `github.com/organvm-i-theoria/radix-recursiva-solve-coagula-redi` |
| `nexus--babel-alexandria` | archive | ARCHIVED | Yes | `github.com/organvm-i-theoria/nexus--babel-alexandria` |
| `4-ivi374-F0Rivi4` | archive | ARCHIVED | Yes | `github.com/organvm-i-theoria/4-ivi374-F0Rivi4` |
| `cog-init-1-0-` | archive | ARCHIVED | Yes | `github.com/organvm-i-theoria/cog-init-1-0-` |
| `scalable-lore-expert` | standard | ARCHIVED | Yes | `github.com/organvm-i-theoria/scalable-lore-expert` |
| `meta-source--ledger-output` | standard | ARCHIVED | Yes | `github.com/organvm-i-theoria/meta-source--ledger-output` |
| `hierarchia-mundi` | standard | ARCHIVED | Yes | `github.com/organvm-i-theoria/hierarchia-mundi` |
| `studium-generale` | standard | ARCHIVED | No | `github.com/organvm-i-theoria/studium-generale` |

**Local-only** (on disk, not in registry):
- `atomic-substrata/` — Atomic substrata project
- `conversation-corpus-engine/` — Conversation corpus processing engine
- `conversation-corpus-site/` — Conversation corpus web presentation
- `scale-threshold-emergence/` — Scale threshold emergence research

### ORGAN-II — Poiesis (32 repos)

| Repo | Tier | Status | Public | GitHub |
|------|------|--------|--------|--------|
| `metasystem-master` | **flagship** | ACTIVE | Yes | `github.com/organvm-ii-poiesis/metasystem-master` |
| `a-mavs-olevm` | **flagship** | ACTIVE | Yes | `github.com/organvm-ii-poiesis/a-mavs-olevm` |
| `chthon-oneiros` | standard | ACTIVE | Yes | `github.com/organvm-ii-poiesis/chthon-oneiros` |
| `krypto-velamen` | standard | ACTIVE | Yes | `github.com/organvm-ii-poiesis/krypto-velamen` |
| `alchemical-synthesizer` | standard | ACTIVE | Yes | `github.com/organvm-ii-poiesis/alchemical-synthesizer` |
| `ivi374ivi027-05` | standard | ACTIVE | Yes | `github.com/organvm-ii-poiesis/ivi374ivi027-05` |
| `styx-behavioral-art` | standard | ACTIVE | Yes | `github.com/organvm-ii-poiesis/styx-behavioral-art` |
| `vigiles-aeternae--theatrum-mundi` | standard | active | Yes | `github.com/organvm-ii-poiesis/vigiles-aeternae--theatrum-mundi` |
| `.github` | infrastructure | ACTIVE | Yes | `github.com/organvm-ii-poiesis/.github` |
| `core-engine` | archive | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/core-engine` |
| `performance-sdk` | archive | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/performance-sdk` |
| `example-generative-music` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/example-generative-music` |
| `example-choreographic-interface` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/example-choreographic-interface` |
| `showcase-portfolio` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/showcase-portfolio` |
| `archive-past-works` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/archive-past-works` |
| `case-studies-methodology` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/case-studies-methodology` |
| `learning-resources` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/learning-resources` |
| `example-generative-visual` | archive | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/example-generative-visual` |
| `example-interactive-installation` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/example-interactive-installation` |
| `example-ai-collaboration` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/example-ai-collaboration` |
| `docs` | archive | ARCHIVED | No | `github.com/organvm-ii-poiesis/docs` |
| `a-i-council--coliseum` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/a-i-council--coliseum` |
| `artist-toolkit-and-templates` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/artist-toolkit-and-templates` |
| `client-sdk` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/client-sdk` |
| `academic-publication` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/academic-publication` |
| `example-theatre-dialogue` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/example-theatre-dialogue` |
| `audio-synthesis-bridge` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/audio-synthesis-bridge` |
| `art-from--auto-revision-epistemic-engine` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/art-from--auto-revision-epistemic-engine` |
| `art-from--narratological-algorithmic-lenses` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/art-from--narratological-algorithmic-lenses` |
| `life-betterment-simulation` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/life-betterment-simulation` |
| `universal-waveform-explorer` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/universal-waveform-explorer` |
| `shared-remembrance-gateway` | standard | ARCHIVED | Yes | `github.com/organvm-ii-poiesis/shared-remembrance-gateway` |

### ORGAN-III — Ergon (29 repos)

| Repo | Tier | Status | Public | GitHub |
|------|------|--------|--------|--------|
| `public-record-data-scrapper` | **flagship** | DEPLOYED | Yes | `github.com/organvm-iii-ergon/public-record-data-scrapper` |
| `content-engine--asset-amplifier` | standard | SKELETON | Yes | `github.com/organvm-iii-ergon/content-engine--asset-amplifier` |
| `peer-audited--behavioral-blockchain` | **flagship** | ACTIVE | Yes | `github.com/organvm-iii-ergon/peer-audited--behavioral-blockchain` |
| `classroom-rpg-aetheria` | standard | DEPLOYED | Yes | `github.com/organvm-iii-ergon/classroom-rpg-aetheria` |
| `the-actual-news` | standard | DEPLOYED | Yes | `github.com/organvm-iii-ergon/the-actual-news` |
| `life-my--midst--in` | standard | ACTIVE | Yes | `github.com/organvm-iii-ergon/life-my--midst--in` |
| `commerce--meta` | standard | ACTIVE | No | `github.com/organvm-iii-ergon/commerce--meta` |
| `styx-behavioral-commerce` | standard | ACTIVE | No | `github.com/organvm-iii-ergon/styx-behavioral-commerce` |
| `.github` | infrastructure | ACTIVE | Yes | `github.com/organvm-iii-ergon/.github` |
| `growth-auditor` | — | — | — | local only |
| `gamified-coach-interface` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/gamified-coach-interface` |
| `trade-perpetual-future` | standard | ARCHIVED | No | `github.com/organvm-iii-ergon/trade-perpetual-future` |
| `fetch-familiar-friends` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/fetch-familiar-friends` |
| `sovereign-ecosystem--real-estate-luxury` | standard | ARCHIVED | No | `github.com/organvm-iii-ergon/sovereign-ecosystem--real-estate-luxury` |
| `search-local--happy-hour` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/search-local--happy-hour` |
| `multi-camera--livestream--framework` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/multi-camera--livestream--framework` |
| `universal-mail--automation` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/universal-mail--automation` |
| `mirror-mirror` | standard | ARCHIVED | No | `github.com/organvm-iii-ergon/mirror-mirror` |
| `the-invisible-ledger` | standard | ARCHIVED | No | `github.com/organvm-iii-ergon/the-invisible-ledger` |
| `enterprise-plugin` | archive | ARCHIVED | No | `github.com/organvm-iii-ergon/enterprise-plugin` |
| `virgil-training-overlay` | archive | ARCHIVED | Yes | `github.com/organvm-iii-ergon/virgil-training-overlay` |
| `tab-bookmark-manager` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/tab-bookmark-manager` |
| `a-i-chat--exporter` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/a-i-chat--exporter` |
| `your-fit-tailored` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/your-fit-tailored` |
| `my-block-warfare` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/my-block-warfare` |
| `my--father-mother` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/my--father-mother` |
| `card-trade-social` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/card-trade-social` |
| `hokage-chess` | standard | ARCHIVED | Yes | `github.com/organvm-iii-ergon/hokage-chess` |
| `anon-hookup-now` | standard | ARCHIVED | No | `github.com/organvm-iii-ergon/anon-hookup-now` |
| `render-second-amendment` | archive | ARCHIVED | No | `github.com/organvm-iii-ergon/render-second-amendment` |
| `select-or-left-or-right-or` | standard | ARCHIVED | No | `github.com/organvm-iii-ergon/select-or-left-or-right-or` |

### ORGAN-IV — Taxis (18 repos)

| Repo | Tier | Status | Public | GitHub |
|------|------|--------|--------|--------|
| `orchestration-start-here` | **flagship** | ACTIVE | Yes | `github.com/organvm-iv-taxis/orchestration-start-here` |
| `agentic-titan` | **flagship** | ACTIVE | Yes | `github.com/organvm-iv-taxis/agentic-titan` |
| `tool-interaction-design` | **flagship** | ACTIVE | Yes | `github.com/organvm-iv-taxis/tool-interaction-design` |
| `petasum-super-petasum` | standard | ACTIVE | Yes | `github.com/organvm-iv-taxis/petasum-super-petasum` |
| `universal-node-network` | standard | ACTIVE | Yes | `github.com/organvm-iv-taxis/universal-node-network` |
| `agent--claude-smith` | standard | ACTIVE | Yes | `github.com/organvm-iv-taxis/agent--claude-smith` |
| `a-i--skills` | standard | ACTIVE | Yes | `github.com/organvm-iv-taxis/a-i--skills` |
| `system-governance-framework` | standard | ACTIVE | No | `github.com/organvm-iv-taxis/system-governance-framework` |
| `reverse-engine-recursive-run` | standard | ACTIVE | Yes | `github.com/organvm-iv-taxis/reverse-engine-recursive-run` |
| `collective-persona-operations` | standard | ACTIVE | Yes | `github.com/organvm-iv-taxis/collective-persona-operations` |
| `.github` | infrastructure | ACTIVE | Yes | `github.com/organvm-iv-taxis/.github` |
| `contrib--adenhq-hive` | contrib | ACTIVE | Yes | `github.com/organvm-iv-taxis/contrib--adenhq-hive` |
| `contrib--ipqwery-ipapi-py` | standard | LOCAL | No | local only |
| `contrib--primeinc-github-stars` | standard | LOCAL | No | local only |
| `contrib--temporal-sdk-python` | standard | LOCAL | No | local only |
| `contrib--dbt-mcp` | standard | LOCAL | No | local only |
| `contrib--langchain-langgraph` | standard | LOCAL | No | local only |
| `contrib--anthropic-skills` | standard | LOCAL | No | local only |

**Local-only** (on disk, not in registry):
- `org-dotgithub/` — Org-level `.github` config staging
- `research/` — Orchestration research
- `tools/` — Organ-level tooling

### ORGAN-V — Logos (2 registered + 5 local)

| Repo | Tier | Status | Public | GitHub |
|------|------|--------|--------|--------|
| `public-process` | **flagship** | ACTIVE | Yes | `github.com/organvm-v-logos/public-process` |
| `.github` | infrastructure | ACTIVE | Yes | `github.com/organvm-v-logos/.github` |

**Local-only** (on disk, not in registry — protected branch repos requiring PR + review):
- `analytics-engine/` — Analytics engine (protected branch)
- `editorial-standards/` — Editorial standards (protected branch)
- `essay-pipeline/` — Essay publishing pipeline (protected branch)
- `reading-observatory/` — Reading observatory (protected branch)
- `docs/` — Organ-level documentation
- `tools/` — Organ-level tooling

### ORGAN-VI — Koinonia (6 repos)

| Repo | Tier | Status | Public | GitHub |
|------|------|--------|--------|--------|
| `community-hub` | **flagship** | ACTIVE | Yes | `github.com/organvm-vi-koinonia/community-hub` |
| `koinonia-db` | standard | ACTIVE | Yes | `github.com/organvm-vi-koinonia/koinonia-db` |
| `adaptive-personal-syllabus` | standard | ACTIVE | Yes | `github.com/organvm-vi-koinonia/adaptive-personal-syllabus` |
| `salon-archive` | standard | ACTIVE | No | `github.com/organvm-vi-koinonia/salon-archive` |
| `reading-group-curriculum` | standard | ACTIVE | No | `github.com/organvm-vi-koinonia/reading-group-curriculum` |
| `.github` | infrastructure | ACTIVE | Yes | `github.com/organvm-vi-koinonia/.github` |

**Local-only:**
- `tools/` — Organ-level tooling

### ORGAN-VII — Kerygma (4 repos)

| Repo | Tier | Status | Public | GitHub |
|------|------|--------|--------|--------|
| `distribution-strategy` | standard | ACTIVE | Yes | `github.com/organvm-vii-kerygma/distribution-strategy` |
| `social-automation` | standard | ACTIVE | No | `github.com/organvm-vii-kerygma/social-automation` |
| `.github` | infrastructure | ACTIVE | Yes | `github.com/organvm-vii-kerygma/.github` |
| `announcement-templates` | archive | ARCHIVED | No | `github.com/organvm-vii-kerygma/announcement-templates` |

**Local-only:**
- `kerygma-pipeline/` — Distribution pipeline
- `kerygma-profiles/` — Platform profile configs
- `tmp_organvm-i-theoria.github.io/` — Temporary GitHub Pages staging
- `tools/` — Organ-level tooling

### LIMINAL — 4444J99 (personal, 5 repos)

| Repo | Purpose | Local Path |
|------|---------|------------|
| `4444J99` | Profile README | `4444J99/4444J99/` |
| `portfolio` | Personal portfolio site | `4444J99/portfolio/` |
| `domus-semper-palingenesis` | Dotfiles + environment (chezmoi) | `4444J99/domus-semper-palingenesis/` |
| `application-pipeline` | Application materials pipeline | `4444J99/application-pipeline/` (memory backup at `.claude/memory/`) |
| `victoroff-group` | Victoroff Group project | `4444J99/victoroff-group/` |
| `intake` | Personal intake/staging | `4444J99/intake/` |

---

## Key Files

### System-Wide Governance Artifacts

| File | Location | Purpose |
|------|----------|---------|
| `repo-registry.json` | `meta-organvm/organvm-corpvs-testamentvm/` | Single source of truth for all 124 repos across 8 organs. **PROTECTED: never overwrite wholesale.** |
| `governance-rules.json` | `meta-organvm/organvm-corpvs-testamentvm/` | Dependency rules and promotion constraints. **PROTECTED.** |
| `system-metrics.json` | `meta-organvm/organvm-corpvs-testamentvm/` | Computed system metrics. **PROTECTED.** |
| `governance-config.yaml` | `meta-organvm/organvm-corpvs-testamentvm/` | Governance configuration |
| `organ-definitions.json` | `meta-organvm/organvm-corpvs-testamentvm/` | Organ identity definitions |
| `metrics-targets.yaml` | `meta-organvm/organvm-corpvs-testamentvm/` | Metrics targets and thresholds |
| `vars-targets.yaml` | `meta-organvm/organvm-corpvs-testamentvm/` | Variable resolution targets |
| `workspace-manifest.json` | `~/Workspace/` | Maps all organ superprojects and non-organ directories |

### Index Apparatus

| File | Location | Purpose |
|------|----------|---------|
| `INST-INDEX-RERUM-FACIENDARUM.md` | `meta-organvm/organvm-corpvs-testamentvm/` | Universal work registry (IRF) |
| `INST-INDEX-LOCORUM.md` | `meta-organvm/organvm-corpvs-testamentvm/` | This document — canonical place map |
| `INST-AMMOI.md` | `meta-organvm/organvm-corpvs-testamentvm/specs/` | System density instrument |
| `INST-ERA.md` | `meta-organvm/organvm-corpvs-testamentvm/specs/` | Event + resource alignment |
| `INST-EVENT-SPINE.md` | `meta-organvm/organvm-corpvs-testamentvm/specs/` | Event spine definition |
| `INST-FORMATION.md` | `meta-organvm/organvm-corpvs-testamentvm/specs/` | Formation instrument |
| `INST-GRAPH-INDICES.md` | `meta-organvm/organvm-corpvs-testamentvm/specs/` | Graph indices |
| `INST-HEARTBEAT.md` | `meta-organvm/organvm-corpvs-testamentvm/specs/` | System heartbeat |
| `INST-TAXONOMY.md` | `meta-organvm/organvm-corpvs-testamentvm/specs/` | Taxonomy instrument |
| `INST-TEMPORAL-METRICS.md` | `meta-organvm/organvm-corpvs-testamentvm/specs/` | Temporal metrics |
| `INST-VARIABLE-RESOLUTION.md` | `meta-organvm/organvm-corpvs-testamentvm/specs/` | Variable resolution rules |

### Specifications (SPEC-000 through SPEC-018)

All in `meta-organvm/organvm-corpvs-testamentvm/specs/`. 21 specification documents covering system architecture, contracts, and formal methods.

### Per-Repo Contracts

| File | Purpose |
|------|---------|
| `seed.yaml` | Automation contract — organ, tier, produces/consumes edges, event subscriptions |
| `CLAUDE.md` | Claude Code agent context (auto-generated by `organvm context sync`) |
| `AGENTS.md` | Multi-agent context file |
| `GEMINI.md` | Gemini agent context file |
| `ecosystem.yaml` | Platform/delivery ecosystem status |

### Essays (Governance Corpus)

All in `meta-organvm/organvm-corpvs-testamentvm/`:

| File | Topic |
|------|-------|
| `essay-1-bootstrap-to-scale.md` | Bootstrap to scale methodology |
| `essay-2-aesthetic-nervous-system.md` | Aesthetic nervous system |
| `essay-3-seed-contracts.md` | Seed contract architecture |
| `essay-4-provenance-as-practice.md` | Provenance as practice |
| `essay-5-archive-paradox.md` | The archive paradox |
| `essay-6-dependency-graph.md` | Dependency graph governance |
| `essay-7-the-convergence.md` | The convergence |
| `essay-8-recursive-proof.md` | Recursive proof |

Additional essays in `docs/essays/`.

### Dotfiles (Chezmoi Source)

Source directory: `~/Workspace/4444J99/domus-semper-palingenesis/`
Deploys to: `$HOME/`

| Source File | Deploys To | Purpose |
|-------------|------------|---------|
| `dot_zshenv` | `~/.zshenv` | XDG dirs, ORGANVM env vars, HISTFILE |
| `dot_config/zsh/` | `~/.config/zsh/` | Full zsh config (ZDOTDIR) |
| `dot_config/git/config.tmpl` | `~/.config/git/config` | Git identity, SSH signing, delta |
| `dot_config/private_op/secrets.zsh` | `~/.config/op/secrets.zsh` | 1Password secret loading |
| `modify_dot_claude.json.tmpl` | `~/.claude.json` | Claude Code MCP config (merge mode) |
| `private_dot_claude/CLAUDE.md.tmpl` | `~/.claude/CLAUDE.md` | Global Claude instructions |
| `dot_local/bin/executable_domus` | `~/.local/bin/domus` | Main system management CLI |

---

## Infrastructure Endpoints

### Deployed Services

| Service | URL | Platform | Purpose |
|---------|-----|----------|---------|
| Hermeneus (Stakeholder Portal) | `stakeholder-portal-ten.vercel.app` | Vercel | AI intelligence portal — repo browser + chat |
| ORGANVM Portfolio Site | — | Astro (static) | Portfolio-facing governance corpus presentation |
| System Dashboard | `localhost:8000` | FastAPI (local) | Health, registry browser, dependency graph, soak monitoring, omega scorecard |
| Object Lessons | `object-lessons.pages.dev` | Cloudflare Pages | Film studies site |

### GitHub Organizations

| Org | URL | Organ |
|-----|-----|-------|
| `organvm-i-theoria` | `github.com/organvm-i-theoria` | I — Theoria |
| `organvm-ii-poiesis` | `github.com/organvm-ii-poiesis` | II — Poiesis |
| `organvm-iii-ergon` | `github.com/organvm-iii-ergon` | III — Ergon |
| `organvm-iv-taxis` | `github.com/organvm-iv-taxis` | IV — Taxis |
| `organvm-v-logos` | `github.com/organvm-v-logos` | V — Logos |
| `organvm-vi-koinonia` | `github.com/organvm-vi-koinonia` | VI — Koinonia |
| `organvm-vii-kerygma` | `github.com/organvm-vii-kerygma` | VII — Kerygma |
| `meta-organvm` | `github.com/meta-organvm` | META |
| `4444j99` / `4444J99` | `github.com/4444J99` | LIMINAL (personal) |

**Legacy org aliases** (local remotes may still reference):
- `ivviiviivvi` -> `organvm-i-theoria`
- `omni-dromenon-machina` -> `organvm-ii-poiesis`
- `labores-profani-crux` -> `organvm-iii-ergon`

### MCP Servers

| Server | Location | Purpose |
|--------|----------|---------|
| ORGANVM MCP | `meta-organvm/organvm-mcp-server/` | System graph exposure (16 tools, 5 groups) via stdio |
| Filesystem MCP | `~/Workspace/mcp-servers/` | Local filesystem access (scoped to workspace) |
| Memory MCP | `~/Workspace/mcp-servers/` | Persistent memory graph |
| Sequential Thinking MCP | `~/Workspace/mcp-servers/` | Structured reasoning |
| Blender MCP | `~/Workspace/blender-mcp/` | Blender integration |

MCP LaunchAgent: `~/Library/LaunchAgents/com.4jp.mcp.servers.plist`

### Local Services (LaunchAgents)

All deployed to `~/Library/LaunchAgents/`:

| Agent | Plist | Purpose |
|-------|-------|---------|
| MCP Servers | `com.4jp.mcp.servers.plist` | MCP server auto-start on login |
| MCP Environment | `com.4jp.env.mcp.plist` | Set MCP environment variables via launchctl |
| System Dashboard | `com.4jp.organvm.dashboard.plist` | ORGANVM dashboard auto-start |
| Soak Snapshot | `com.4jp.organvm.soak-snapshot.plist` | Daily soak test snapshots |
| System Pulse | `com.4jp.organvm.pulse.plist` | System pulse monitoring |
| Cloudflared | `com.4jp.cloudflared.organvm.plist` | Cloudflare tunnel for ORGANVM |
| Daily Health | `com.4jp.pipeline.daily-health.plist` | Daily health pipeline |
| Daily Monitor | `com.4jp.pipeline.daily-monitor.plist` | Daily monitoring pipeline |
| Daily Deferred | `com.4jp.pipeline.daily-deferred.plist` | Deferred task processing |
| Biweekly Agent | `com.4jp.pipeline.agent-biweekly.plist` | Biweekly agent pipeline |
| Calendar Refresh | `com.4jp.pipeline.calendar-refresh.plist` | Calendar data refresh |
| Weekly Backup | `com.4jp.pipeline.weekly-backup.plist` | Weekly backup pipeline |
| Weekly Briefing | `com.4jp.pipeline.weekly-briefing.plist` | Weekly briefing generation |
| Gmail Labeler | `com.user.gmail_labeler.plist` | Gmail label automation (disabled) |
| Mail Automation | `com.user.mail_automation.plist` | Mail automation (disabled) |

---

## Data Directories

All within `meta-organvm/organvm-corpvs-testamentvm/data/`:

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `fossil/` | Archaeological record | `fossil-record.jsonl` (9,445 commits), `chronicle/` |
| `atoms/` | Atomized tasks, prompt links, per-organ rollups | `atomized-tasks.jsonl`, `atom-links.jsonl`, `annotated-prompts.jsonl`, `plan-index.json` |
| `soak-test/` | Daily soak test snapshots | `daily-YYYY-MM-DD.json` series |
| `dashboard/` | Dashboard static assets | `index.html` |
| `index/` | Deep index data | `deep-index.json` |
| `omega/` | Omega scorecard snapshots | `omega-status-YYYY-MM-DD.json` series |
| `organism/` | System organism snapshots | `system-organism-YYYY-MM-DD.json` |
| `pulse/` | Weekly pulse reports | `weekly-YYYY-MM-DD.md` series |

### Additional Data Locations

| Directory | Purpose |
|-----------|---------|
| `meta-organvm/organvm-corpvs-testamentvm/ecosystem/` | Ecosystem snapshots and pillar DNA |
| `meta-organvm/organvm-corpvs-testamentvm/registry/` | Registry-related data |
| `meta-organvm/organvm-corpvs-testamentvm/site-data/` | Portfolio site data files |
| `meta-organvm/organvm-corpvs-testamentvm/sops/` | Standard operating procedures |
| `meta-organvm/organvm-corpvs-testamentvm/testament/` | Testament records |
| `~/Workspace/alchemia-ingestvm/` | Ingestion pipeline staging data |
| `~/Workspace/intake/` | Unsorted inbound material |

---

## Document Architecture (Corpus)

Within `meta-organvm/organvm-corpvs-testamentvm/docs/`:

| Directory | Layer | Purpose |
|-----------|-------|---------|
| `genesis/` | 0 | Conversational source material and audit transcripts |
| `planning/` | 1 | Phase 1 planning toolkit (scoring, inventory, templates, checklists, risk) |
| `strategy/` | 2 | Roadmap, execution indices, sprint catalog (76 named sprints) |
| `implementation/` | 3 | v2 execution specs, orchestration, public process, GitHub Actions |
| `standards/` | — | Repository standards, SDD methodology |
| `operations/` | — | Rolling TODO, operational cadence, concordance, key workflows |
| `evaluation/` | — | Reviews, evaluations, assessments |
| `governance/` | — | Governance documents |
| `applications/` | — | Application materials (canonical source of truth for identity/metrics) |
| `essays/` | — | Essay drafts and working documents |
| `agents/` | — | Agent-specific context and configuration |
| `memory/` | — | Constitution, persistent context |
| `legal/` | — | Legal documents |
| `specs/` | — | Sprint specifications (`docs/specs/<sprint>/`) |
| `adr/` | — | Architecture Decision Records |
| `archive/` | — | Frozen v1 documents (do not modify) |
| `pitch/` | — | Pitch materials |
| `sop--ira-grade-norming.md` | — | IRA grade norming SOP |

---

## CLI Tools

| Tool | Location | Invocation | Purpose |
|------|----------|------------|---------|
| `organvm` | `meta-organvm/organvm-engine/` | `organvm <command>` | Unified CLI: 23 command groups for registry, governance, seeds, metrics, git, omega |
| `alchemia` | `meta-organvm/alchemia-ingestvm/` | `alchemia <subcommand>` | Material ingestion pipeline |
| `organvm-dashboard` | `meta-organvm/system-dashboard/` | `organvm-dashboard` | FastAPI dashboard server |
| `organvm-mcp` | `meta-organvm/organvm-mcp-server/` | `organvm-mcp` | MCP server (stdio) |
| `ontologia` | `meta-organvm/organvm-ontologia/` | `ontologia` | Adaptive structural registry |
| `domus` | `~/Workspace/4444J99/domus-semper-palingenesis/dot_local/bin/` | `domus <subcommand>` | System management (apply, maintain, packages, doctor) |
| `invoke.py` | `meta-organvm/organvm-corpvs-testamentvm/scripts/` | `python3 scripts/invoke.py <ID>` | Invocation symbol lookup |

---

## Environment Variables

### Set by `~/.zshenv` (universal)

| Variable | Value | Purpose |
|----------|-------|---------|
| `XDG_CONFIG_HOME` | `~/.config` | XDG base directory |
| `XDG_DATA_HOME` | `~/.local/share` | XDG data directory |
| `XDG_STATE_HOME` | `~/.local/state` | XDG state directory |
| `XDG_CACHE_HOME` | `~/.cache` | XDG cache directory |
| `ZDOTDIR` | `~/.config/zsh` | Zsh config location |
| `ORGANVM_WORKSPACE_DIR` | `~/Workspace` | Workspace root |
| `ORGANVM_CORPUS_DIR` | `~/Workspace/meta-organvm/organvm-corpvs-testamentvm` | Corpus root |
| `ORG_I` through `ORG_META` | `organvm-i-theoria` ... `meta-organvm` | Organ org mapping |
| `ORG_LIMINAL` | `4444j99` | Personal org |
| `GITHUB_PRIMARY` / `GITHUB_SECONDARY` | — | GitHub account identifiers |

### Set by `~/.config/zsh/15-env.zsh`

| Variable | Value | Purpose |
|----------|-------|---------|
| `DOMUS_ROOT` | `~/domus-semper-palingenesis` | Chezmoi source (stable identifier) |
| `AGENTS_ROOT` / `AGENTS_BIN` / `AGENTS_CACHE` / `AGENTS_STATE` / `AGENTS_LOG` | — | Agent infrastructure paths |
| `WORKSPACE_ROOT` | `$DOMUS_ROOT/projects` | Workspace root (domus context) |

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total repos in registry | 124 |
| Active repos | 62 |
| Archived repos | 53 |
| GitHub organizations | 9 (8 organ + 1 personal) |
| Operational organs | 8 |
| LaunchAgents deployed | 15 (13 active + 2 disabled) |
| INST documents | 11 |
| SPEC documents | 21 |
| System essays | 8+ |
| Total documented words | 741K+ |

---

*Last updated: 2026-03-23*
