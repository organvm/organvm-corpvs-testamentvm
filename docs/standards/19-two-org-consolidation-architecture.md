# 19: Two-Org Consolidation Architecture

**Date:** 2026-05-27
**Status:** ACTIVE — describes the elevated topological form of the system; migration is multi-session
**Derived from:** Empirical org sprawl across 10 GitHub orgs; conductor decision to reduce GitHub topology while preserving the 8-organ epistemic taxonomy
**Complements:** `10-repository-standards.md`, `17-branch-governance.md`, `18-scheduled-process-contract.md`, `20-reusable-workflow-architecture.md`, `21-apps-surface-policy.md`, `22-essence-function-naming-convention.md`

---

## 1. The reduction

| Before | After |
|---|---|
| 10 GitHub orgs (4444J99 + a-organvm + meta-organvm + 7 organ orgs) | **2 GitHub orgs** (`${ORG_PERSONAL}` + `${ORG_SYSTEM}`) |
| 8-organ taxonomy mirrored at GitHub-org level (one org per organ) | 8-organ taxonomy preserved as `seed.yaml organ:` + GitHub topic + double-hyphen naming |
| ~30+ apps × 8–10 orgs = redundant installations | Apps installed **once per surviving org** (max 2 installations of each) |
| ~140 GH Actions cron entries scattered, ~70 of which are duplicate `stale.yml` × 40 repos | ~8 reusable workflows in `${ORG_SYSTEM_TEMPLATE}` called by every repo |
| Per-repo workflows are 60+ LOC files | Per-repo workflows are 5-line callers invoking reusables |
| ~14 routines fire on the busiest day across all surfaces | ≤15/day target met by construction |

The 8-organ system isn't reduced — its **topological mirror** is. Per Rule #34 ("merge into ideal form"), the elevated form preserves essential complexity (organ epistemology) and drops incidental complexity (GitHub-org-per-organ).

## 2. Where each layer lives

| Concern | Old location | Elevated location |
|---|---|---|
| Personal identity (4 repos) | `4444J99` org | **`${ORG_PERSONAL}` org** (unchanged) |
| System work (~148 repos) | Scattered across 8 organ orgs + a-organvm + meta-organvm | **`${ORG_SYSTEM}` org** (all repos transferred in) |
| Organ classification | GitHub org membership | `seed.yaml organ:` field + GitHub topic `organ-<n>-<name>` + repo naming `<organ>-<type>--<name>` |
| Governance corpus | `meta-organvm/organvm-corpvs-testamentvm` | `${ORG_SYSTEM}/organvm-corpvs-testamentvm` (existing redirects handle URL change) |
| Shared workflows | Per-repo duplicates (40× stale.yml, etc.) | **`${ORG_SYSTEM_TEMPLATE}/.github/workflows/`** reusables |
| Apps | Installed per-org × 8–10 | Installed on `${ORG_SYSTEM}` with `repository_selection: all` |
| Profile / org-level README | None | `${ORG_SYSTEM_TEMPLATE}/profile/README.md` — public face of the system |

## 3. The 8-organ taxonomy after consolidation

Each organ remains a distinct epistemological category. Implementation:

| Organ | Greek suffix | seed.yaml value | GitHub topic | Example repo name |
|---|---|---|---|---|
| I | `theoria` (θεωρία) | `organ: i-theoria` | `organ-i-theoria` | `recursive-engine--generative-entity` |
| II | `poiesis` (ποίησις) | `organ: ii-poiesis` | `organ-ii-poiesis` | `metasystem-master` |
| III | `ergon` (ἔργον) | `organ: iii-ergon` | `organ-iii-ergon` | `public-record-data-scrapper` |
| IV | `taxis` (τάξις) | `organ: iv-taxis` | `organ-iv-taxis` | `orchestration-start-here` |
| V | `logos` (λόγος) | `organ: v-logos` | `organ-v-logos` | `public-process` |
| VI | `koinonia` (κοινωνία) | `organ: vi-koinonia` | `organ-vi-koinonia` | (community repos) |
| VII | `kerygma` (κήρυγμα) | `organ: vii-kerygma` | `organ-vii-kerygma` | (distribution repos) |
| Meta | (umbrella) | `organ: meta` | `organ-meta` | `organvm-corpvs-testamentvm` |

Discovery query: `gh repo list ${ORG_SYSTEM} --json name,topics --jq '.[] | select(.topics | contains(["organ-iv-taxis"]))'` returns all ORGAN-IV repos.

## 4. Identity-layer reading order (4 steps for a stranger)

1. `github.com/${ORG_PERSONAL}` — the human
2. `github.com/${ORG_SYSTEM}` — the work (org profile rendered from `${ORG_SYSTEM_TEMPLATE}/profile/README.md`)
3. `github.com/${ORG_SYSTEM}/organvm-corpvs-testamentvm` — the architecture (this corpus)
4. `<any-repo>/README.md` — convergent format per `10-repository-standards.md`

A stranger reads ≤4 surfaces to understand the system. The 8-organ taxonomy surfaces at step 2 (org-level README explains the 8 organs) and at step 4 (per-repo README declares its organ).

## 5. Migration arc (multi-session)

| Phase | Work | Risk | Sessions |
|---|---|---|---:|
| **0 — Architecture** | Standards docs 19–22 + env file extension + plan file | Low (planning) | 1 (this session) |
| **1 — Target org reserve** | `gh api -X POST /user/orgs` for `${ORG_SYSTEM}` bare name, OR keep `a-organvm` and document the choice in `.env.local` | Low | 1 (out-of-band) |
| **2 — Apps consolidation** | Install canonical 8 apps on `${ORG_SYSTEM}` with `repository_selection: all`; remove dormant apps from source orgs | Low | 1 |
| **3 — Reusable workflows** | Author 8 reusables in `${ORG_SYSTEM_TEMPLATE}/.github/workflows/`; convert per-repo workflows to callers | Medium (CI changes) | 2–3 |
| **4 — Class-(I) → Class-(III) migration** | Convert `${ROUTINE_COMMIT_SUMMARIZER}`, `${ROUTINE_REPO_WARDEN}` Phase B, `${ROUTINE_PR_CASCADE}` to server-side workflows (invokes Claude API via org secret `ANTHROPIC_API_KEY`) | Medium (API integration) | 2 |
| **5 — Repo transfer** | `gh repo transfer <source>/<repo> ${ORG_SYSTEM}` for each of ~28 repos not already in target; update `${REGISTRY_V2}`, topics, README badges | High (URL changes; existing redirects mitigate) | 3–6 weeks |
| **6 — Source org archival** | After each org drains: `gh repo archive` not delete (preserve history) | Low | 1 |
| **7 — Self-audit infrastructure** | Author `${ROUTINE_TOPOLOGY_WITNESS}`, `${ROUTINE_APPS_DORMANCY_WITNESS}`, `${ROUTINE_REUSABLE_COVERAGE_WITNESS}` as Class-(I) scheduled-tasks | Low | 1 |

Each phase has rollback. Each is incremental.

## 6. Per-class fire-count budget (post-migration)

| Class | Cap | Current | Post-migration target |
|---|---:|---:|---:|
| (I) Local-token | ≤4 daily-equivalent | 8 active (this session) | 4 (after migration of 3 to class-(III)) |
| (II) Local-RAM (Rule #55a) | ≤3 | 0 | 1 (`${LA_SUMMON_DAILY}`) + 2 reserved |
| (III) Server-side reusable | ~8 | ~140 scattered | 8 reusables in `${ORG_SYSTEM_TEMPLATE}` |
| (IV) Apps | ~8 per org | 30+ per org (redundant) | 8 in `${ORG_SYSTEM}` |
| **Total daily fires** | — | ~14+ | ~10–14 |

## 7. The env-file as identity declaration

Per `22-essence-function-naming-convention.md`, every name in this document references an env var from `${CORPVS_ROOT}/.config/organvm.env`. Renaming `a-organvm` → `organvm` is a one-line edit (`ORG_SYSTEM=organvm`); every downstream reference inherits.

The env file IS the system's identity declaration. The system is **parameterized over its own name**.

## 8. Open extensions

- **Topology witness** (`${ROUTINE_TOPOLOGY_WITNESS}`) — Class-(I) routine that asserts the invariant "only `${ORG_PERSONAL}` and `${ORG_SYSTEM}` exist as non-archived orgs accessible to the conductor"; flags any drift.
- **Per-machine override** via `${CORPVS_ROOT}/.config/organvm.env.local` (gitignored) — allows a fork or staging instance to use different org names without touching the canonical file.
- **9th organ extension** — adding `ORGAN_VIII=...` to the env file flows through the cascade; no other code changes needed.

## 9. Cross-references

- `${DOC_BRANCH_GOVERNANCE}` Section 8 (tier classification) becomes simpler with 2 orgs
- `${DOC_SCHEDULED_PROCESS_CONTRACT}` (Rule #55a) bounds Class-(II)
- `${DOC_REUSABLE_WORKFLOW_ARCHITECTURE}` (doc 20) details the Class-(III) reusables
- `${DOC_APPS_SURFACE_POLICY}` (doc 21) details the Class-(IV) slot rules
- `${DOC_NAMING_CONVENTION}` (doc 22) governs the essence-function naming used here
- `${CORPVS_ROOT}/.config/organvm.env` is the canonical name registry
