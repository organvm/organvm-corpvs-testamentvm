> **Canonical location:** `praxis-perpetua/standards/SOP--pitch-deck-rollout.md`. This file is a reference copy retained for local context.

# SOP: Pitch Deck Generation & Rollout

**Created:** 2026-03-04
**Author:** @4444j99 (AI-conductor model: human directs, AI generates, human reviews)
**Status:** ACTIVE — Living document, updated as process evolves
**Companions:** [`key-workflows.md`](./key-workflows.md) (procedures), [`operational-cadence.md`](./operational-cadence.md) (rhythm), [`minimum-viable-operations.md`](./minimum-viable-operations.md) (maintenance)
**Precedent:** `organvm-iii-ergon/peer-audited--behavioral-blockchain` — first bespoke implementation
**Toolchain:** `organvm-engine` pitch CLI (`meta-organvm/organvm-engine/src/organvm_engine/pitchdeck/`)

---

> *Every repo in the ecosystem deserves a pitch — a single-page artifact that answers "what is this, why does it exist, and why should I care?" This SOP governs how pitch decks are created, maintained, and deployed across all 8 organs.*

---

## Table of Contents

1. [Purpose & Scope](#1-purpose--scope)
2. [Pitch Deck Tiers](#2-pitch-deck-tiers)
3. [Phase 1 — Readiness Audit](#3-phase-1--readiness-audit)
4. [Phase 2 — README Section Standardization](#4-phase-2--readme-section-standardization)
5. [Phase 3 — pitch.yaml Authoring](#5-phase-3--pitchyaml-authoring)
6. [Phase 4 — Auto-Generation](#6-phase-4--auto-generation)
7. [Phase 5 — Bespoke Deck Development](#7-phase-5--bespoke-deck-development)
8. [Phase 6 — Deployment & Hosting](#8-phase-6--deployment--hosting)
9. [Phase 7 — CI/CD Integration](#9-phase-7--cicd-integration)
10. [Phase 8 — Quality Gates & Review](#10-phase-8--quality-gates--review)
11. [Phase 9 — External Submission Pipeline](#11-phase-9--external-submission-pipeline)
12. [Organ-Specific Guidelines](#12-organ-specific-guidelines)
13. [Maintenance & Sync Cadence](#13-maintenance--sync-cadence)
14. [Rollout Sequence & Priority Matrix](#14-rollout-sequence--priority-matrix)
15. [Decision Trees](#15-decision-trees)
16. [Appendices](#16-appendices)

---

## 1. Purpose & Scope

### What this SOP does

This procedure governs the creation, deployment, and maintenance of pitch decks for every eligible repository across the ORGANVM ecosystem. A pitch deck is a **single-page web artifact** (hosted via GitHub Pages) that presents a project's purpose, problem space, solution, and positioning within the organ system.

The ecosystem uses a **two-track system**:
- **Auto-generated** — the `organvm-engine` pitch CLI produces single-file HTML decks from structured data (README, seed.yaml, registry, pitch.yaml), themed per-organ.
- **Bespoke** — hand-crafted SPAs with custom code, animations, and narrative for repos that warrant the investment.

### When to run it

| Trigger | Description |
|---------|-------------|
| **New repo onboarding** | When a repo is added to the registry and has at least a README |
| **Promotion to PUBLIC_PROCESS** | When a repo's promotion status advances — it now faces external audiences |
| **Pre-launch / Pre-fundraise** | Before public launch or investor outreach for commercial products |
| **Quarterly sync** | Part of the monthly review cycle (see [`operational-cadence.md`](./operational-cadence.md)) |
| **README major edit** | When a repo's Problem/Solution/Features sections are substantially rewritten |
| **Organ aesthetic update** | When `organ-aesthetic.yaml` or `themes.py` palettes change |

### What it applies to

Any repo in any organ, subject to the exclusion rules in [Section 2](#2-pitch-deck-tiers). The procedure is **organ-agnostic** — the same phases apply whether the repo is a theoretical engine (ORGAN-I), a generative art system (ORGAN-II), a commercial product (ORGAN-III), or an orchestration tool (ORGAN-IV). The **organ-specific** section ([Section 12](#12-organ-specific-guidelines)) provides per-organ tone, palette, and narrative guidance.

---

## 2. Pitch Deck Tiers

Every repo is classified into one of four tiers. The tier determines tooling, effort, and review process.

### Tier 0: Excluded (No Pitch Deck)

**Criteria:** Any of:
- `infrastructure` tier in seed.yaml
- `ARCHIVED` promotion status
- Governance-only repos with no user-facing product or tool
- `.github` org config repos

**Action:** Skipped during sync. No `docs/pitch/` directory created.

### Tier 1: Auto-Generated (Default)

**Criteria:** Any `standard` or `flagship` tier repo with at least a description in registry or README.
**Expected volume:** ~70% of eligible repos.
**Tooling:** `organvm-engine pitch generate <repo>`
**Output:** Single-file HTML at `docs/pitch/index.html` (~60-80KB)
**Sections:** Hero, Problem, Solution, Features, Architecture, [Market (ORGAN-III only)], Positioning, CTA
**Theme:** Organ palette resolved from `themes.py`
**Animation:** Single procedural hero canvas (organ-specific generative pattern)
**Review:** Automated CI checks (link integrity, section completeness, marker presence)
**Maintenance:** Re-generated on sync runs

### Tier 2: Enhanced Auto-Generated (pitch.yaml Override)

**Criteria:** Repos needing richer content than README alone — custom taglines, curated problem cards, explicit market positioning, or hand-picked CTA links.
**Expected volume:** ~15-20% of eligible repos.
**Tooling:** Same CLI; reads `pitch.yaml` for content overrides (highest priority in data assembly)
**Output:** Same single-file HTML, but with curated content
**Review:** Human review of pitch.yaml content
**Maintenance:** pitch.yaml edited manually; HTML re-generated on sync

### Tier 3: Bespoke (Custom Application)

**Criteria:** Any of:
- Flagship tier with active fundraising or investor audience
- The pitch deck doubles as an interactive product demo
- Narrative complexity requires > 7 sections or custom visualizations
- External audience (press, partners, accelerators) beyond GitHub visitors

**Expected volume:** 3-5 repos ecosystem-wide.
**Tooling:** Custom build pipeline per repo (Vite/React, Next.js static export, etc.)
**Output:** Custom SPA in `docs/` or `docs/pitch/`
**Review:** Full code review + narrative review (two reviewers: technical + content)
**Maintenance:** Manual; must be registered in `BESPOKE_REPOS` set and `seed.yaml`

---

## 3. Phase 1 — Readiness Audit

Before generating pitch decks for a repo (or batch of repos), verify data readiness.

### 3.1 Registry entry

```bash
cd ~/Workspace/meta-organvm
source .venv/bin/activate
python -m organvm_engine registry stats
```

Verify the target repo(s) have:
- [ ] Entry in `repo-registry.json`
- [ ] `tier`, `org`, `tech_stack` fields populated
- [ ] ORGAN-III repos: `revenue_model` and `revenue_status` present

### 3.2 seed.yaml

- [ ] `seed.yaml` exists in repo root
- [ ] Fields present: `organ`, `tier`, `promotion_status`
- [ ] `produces`/`consumes` edges declared (if repo has inter-organ dependencies)

### 3.3 organ-aesthetic.yaml

- [ ] Organ directory has `.github/organ-aesthetic.yaml`
- [ ] Palette for this organ exists in `themes.py` (`ORGAN_PALETTES` dict)

### 3.4 Engine health

```bash
python -m organvm_engine pitch generate --repo <target-repo> --dry-run
```

- [ ] Dry run completes without import errors
- [ ] Output reports expected action (generated, bespoke skip, or error with clear message)

### 3.5 GitHub Pages eligibility

- [ ] Repo has (or can create) a `docs/` directory
- [ ] GitHub Pages can be enabled (source: `docs/` on default branch)
- [ ] No existing `docs/pitch/index.html` that would be unintentionally clobbered

---

## 4. Phase 2 — README Section Standardization

The auto-generator extracts content from README `##` and `###` headings. Headings are normalized to lowercase for matching.

### 4.1 Required sections (all repos)

```markdown
## What This Is
[1-2 paragraphs. First sentence auto-extracted as tagline if pitch.yaml doesn't override.]

## Problem
[3-4 bullet points or 1-2 paragraphs. Bold text before em-dash becomes card title.]

- **Pain Point One** — Quantified statement with citation if available
- **Pain Point Two** — Another dimension of the problem
- **Pain Point Three** — The "aha" insight

## Solution
[1-2 paragraphs describing the approach. First paragraph extracted for the Solution section.]

## Key Features
[Bulleted list, max 6 items. Bold text becomes feature card title.]

- **Feature A** — Benefit-oriented description
- **Feature B** — Benefit-oriented description

## Architecture
[1-2 paragraphs. Tech keywords auto-extracted as badges.]
```

### 4.2 Recognized section aliases

The parser searches for these alternate heading names (all equivalent):

| Canonical | Aliases |
|-----------|---------|
| `## Problem` | `## The Problem`, `## Motivation`, `## Why` |
| `## Solution` | `## The Solution`, `## Approach`, `## How It Works`, `## Overview` |
| `## Key Features` | `## Features`, `## Capabilities` |
| `## Architecture` | `## Technical Architecture`, `## Design`, `## Stack` |
| `## Market` | `## Business Model`, `## Revenue`, `## Pricing` *(ORGAN-III only)* |

### 4.3 Section writing guidelines

**Problem section:**
- Lead with a quantified pain point (cite source if possible)
- 3 cards max — each independently compelling
- Use bold title + em-dash + explanation for best auto-extraction
- Write for a non-technical stakeholder

**Solution section:**
- First sentence = the "elevator pitch" (this becomes the deck tagline)
- Explain mechanism, not just outcome
- Reference the problem by name to close the narrative loop

**Features section:**
- Action-oriented titles: "Peer Auditing", not "Auditing Module"
- Each maps to a user benefit, not a technical implementation detail
- 4-6 items; auto-generator truncates at 6

**Architecture section:**
- Lead with tech stack as comma-separated keywords (extracted as badges)
- Follow with 1-2 sentences on design philosophy
- Mention deployment target if applicable

### 4.4 Audit script

```bash
python -m organvm_engine pitch audit-readmes [--organ III] [--fix-suggestions]
```

Output reports per-section status: `[OK]`, `[WEAK]` (present but thin), `[MISSING]`.

---

## 5. Phase 3 — pitch.yaml Authoring

For repos needing richer content than README provides (Tier 2), create `pitch.yaml` in the repo root. This file has **highest priority** in the data assembly chain: `pitch.yaml > seed.yaml > registry > README`.

### 5.1 Schema

```yaml
# pitch.yaml — Pitch deck content overrides
display_name: "Human-Readable Name"          # Override auto-humanized name
tagline: "One-line hook (< 120 chars)"       # Hero subtitle
description: >                               # 1-3 sentences, meta description
  Concise project description.

problem:                                     # 1-3 problem cards
  - title: "Pain Point"
    text: "Quantified statement"

solution: >                                  # 1-2 paragraphs
  How the project addresses the problem.

features:                                    # 1-6 feature cards
  - title: "Feature Name"
    text: "Benefit-oriented description"

architecture: >                              # 1-2 paragraphs
  Technical design and philosophy.

tech_stack:                                  # Technology names (rendered as badges)
  - PostgreSQL
  - Redis
  - React

# ORGAN-III only
market: >                                    # Market description
  TAM/SAM/SOM and go-to-market strategy.
revenue_model: "SaaS + Platform Fee"
revenue_status: "Pre-Revenue"

# Links (CTA section)
github_url: "https://github.com/org/repo"
docs_url: ""
demo_url: ""

# Bespoke configuration (Tier 3 only)
pitch:
  type: bespoke                              # enum: auto | bespoke
  path: src/pitch                            # Source directory
  build_cmd: "cd src/pitch && npm run build" # Build command
  output_dir: docs/pitch                     # Output directory
```

### 5.2 When to create pitch.yaml

| Scenario | Action |
|----------|--------|
| README has good content but tagline needs polish | Minimal pitch.yaml (`tagline` + `display_name` only) |
| README is thin or missing key sections | Full pitch.yaml with all content fields |
| Product has specific investor/stakeholder messaging | Curated problem/solution/features |
| Product has a live demo URL | Add `demo_url` |
| README content is accurate but wrong tone for pitch | Override with pitch.yaml |

### 5.3 Validation

```bash
python -m organvm_engine pitch validate <repo>
# Checks: YAML syntax, field types, tagline length, URL reachability
```

---

## 6. Phase 4 — Auto-Generation

### 6.1 Dry run

Always dry-run before writing files.

```bash
# Single repo
python -m organvm_engine pitch generate --repo <name> --dry-run

# All repos in an organ
python -m organvm_engine pitch sync --organ ORGAN-III --dry-run

# Full ecosystem
python -m organvm_engine pitch sync --dry-run
```

### 6.2 Review dry run output

Verify for each organ:
- [ ] **Generated count** matches expected (total repos minus excluded/bespoke)
- [ ] **Bespoke list** includes all known bespoke repos
- [ ] **Skipped list** shows correct reasons (`tier=infrastructure`, `tier=archive`, `directory not found`)
- [ ] **Error count** is 0

### 6.3 Single-repo test

Before batch generation, test one repo per organ:

```bash
python -m organvm_engine pitch generate --repo <name>
open ~/Workspace/<organ-dir>/<repo>/docs/pitch/index.html
```

Verify:
- [ ] HTML renders in browser
- [ ] Organ palette applied (correct accent color, heading font)
- [ ] Navigation dots functional
- [ ] All sections have content (no "Under Construction" placeholders)
- [ ] CTA links resolve
- [ ] Responsive at 375px, 768px, 1024px
- [ ] `prefers-reduced-motion` disables animations

### 6.4 Batch generation

```bash
# By organ (recommended — review in batches)
python -m organvm_engine pitch sync --organ ORGAN-I
python -m organvm_engine pitch sync --organ ORGAN-II
python -m organvm_engine pitch sync --organ ORGAN-III
# ... etc.

# By tier
python -m organvm_engine pitch sync --tier flagship
python -m organvm_engine pitch sync --tier standard
```

### 6.5 Post-generation verification

```bash
# Count generated files
find ~/Workspace -path "*/docs/pitch/index.html" | wc -l

# Verify all auto-generated contain the marker
find ~/Workspace -path "*/docs/pitch/index.html" -exec grep -L "ORGANVM:PITCH:AUTO" {} \;
# (Should list only bespoke decks)

# Check file sizes (expect 40-80KB each)
find ~/Workspace -path "*/docs/pitch/index.html" -exec ls -lh {} \;
```

---

## 7. Phase 5 — Bespoke Deck Development

### 7.1 Eligibility criteria

A repo qualifies for bespoke when **any** of these apply:
1. Flagship tier with active fundraising
2. The pitch deck doubles as interactive product demo
3. Complex narrative requiring > 7 sections or custom visualizations
4. External audience (investors, press, partners, accelerators)

### 7.2 Bespoke narrative template

Adapt this structure to the project's domain. Not all slides are required for every organ — commercial products (ORGAN-III) need the full set; theory/creative repos may omit business slides.

| Slide | Purpose | Required | ORGAN-III Addition |
|-------|---------|----------|-------------------|
| 1 | **Hero** — title, tagline, 2-3 anchor stats | Yes | — |
| 2 | **Problem** — quantified pain points | Yes | — |
| 3 | **Solution** — core mechanism | Yes | — |
| 4 | **Differentiation** — what makes this unique | Yes | — |
| 5 | **Risk Mitigation** — legal, technical, or market risks | Recommended | — |
| 6 | **Market** — TAM/SAM/SOM, go-to-market | ORGAN-III | Required |
| 7 | **Competitive Landscape** — positioning | ORGAN-III | Required |
| 8 | **Business Model** — revenue, unit economics | ORGAN-III | Required |
| 9 | **Platform Economics** — cost structure at scale | ORGAN-III | Recommended |
| 10 | **Technical Stack** — architecture credibility | Recommended | — |
| 11 | **Team / Capability Proof** | Recommended | — |
| 12 | **CTA** — the ask, milestones, urgency | Yes | — |

Non-commercial organs may replace slides 6-9 with:
- **Impact / Reach** — who this serves and how many
- **Integration Points** — how it connects to other organs
- **Roadmap** — what's next

### 7.3 Recommended technical patterns

These patterns were validated in the first bespoke implementation and should be adopted as defaults for future bespoke decks:

**Architecture:**
- React 18 + Vite + TypeScript strict mode
- Tailwind CSS with CSS custom properties for organ theming
- p5.js for procedural animations (optional — CSS-only is also valid)
- Single `slides.ts` data file defining all content (separates data from rendering)

**Content type system:**
- `stat` — Grid of value/label/source cards
- `bullets` — Title + bullet list
- `callout` — Emphasis box with title + body
- `flow` — Sequential steps with arrows
- `columns` — 2-3 column titled lists

**Expandable sections per slide (recommended):**
- **ELI5** — Plain-language explanation for non-expert audience
- **Tough Questions** — 2-3 anticipated objections with answers (investor-grade depth)

**Animation patterns:**
- All visuals procedural (no raster images) — reduces bundle, enables responsiveness
- IntersectionObserver gates animation instances to viewport proximity (lazy loading)
- All entrance animations via CSS `[data-reveal]` attributes, not imperative JS
- Staggered delays: `transitionDelay: ${i * 0.12}s` for cinematic reveals
- Must respect `prefers-reduced-motion`

**Build config:**
- `base: './'` — relative paths for GitHub Pages subdirectory hosting
- `outDir: docs/pitch` (or `docs/` if pitch is the primary docs output)
- `emptyOutDir` set appropriately to avoid clobbering sibling content

### 7.4 Registration

When a bespoke deck is created:

1. **Add to `BESPOKE_REPOS`** in `meta-organvm/organvm-engine/src/organvm_engine/pitchdeck/sync.py`
2. **Add to `seed.yaml`:**
   ```yaml
   pitch:
     type: bespoke
     path: src/pitch
     build_cmd: "cd src/pitch && npm run build"
     output_dir: docs/pitch
   ```
3. **Verify** the output HTML does **not** contain the `PITCH_MARKER` comment (this prevents auto-gen from ever overwriting it)
4. **Commit** registration changes to both the repo and the engine

### 7.5 Constants handling

Bespoke decks that reference domain constants (behavioral coefficients, financial thresholds, market figures, etc.) must choose a sync strategy:

| Approach | When to Use |
|----------|-------------|
| **Copy constants into pitch data file** | Pitch is standalone, constants change rarely. Add a CI drift-check script. |
| **Import from shared package** | Pitch is part of a monorepo build pipeline. Constants always in sync. |
| **CI sync script** | Constants change frequently. Script diffs pitch values against source of truth. |

---

## 8. Phase 6 — Deployment & Hosting

### 8.1 GitHub Pages configuration

1. Repo Settings > Pages
2. Source: **Deploy from a branch**
3. Branch: `main` (or default), directory: `/docs`

### 8.2 Output path convention

| Deck Type | Output Path | URL |
|-----------|------------|-----|
| Auto-generated | `docs/pitch/index.html` | `/{repo}/pitch/` |
| Bespoke (subdirectory) | `docs/pitch/index.html` | `/{repo}/pitch/` |
| Bespoke (root) | `docs/index.html` | `/{repo}/` |
| Bespoke (alt path) | `docs/pitch-deck/index.html` | `/{repo}/pitch-deck/` |

**Rule:** If `docs/index.html` already exists for other purposes (API docs, planning, etc.), use the `docs/pitch/` subdirectory. The root-docs pattern is only appropriate when the pitch IS the primary docs output.

### 8.3 Deployment verification checklist

- [ ] URL loads without 404
- [ ] All assets load (no 404s in DevTools Network tab)
- [ ] Navigation dots track scroll
- [ ] Hero section renders (animation + title + badge)
- [ ] CTA links resolve
- [ ] Responsive at 375px, 768px, 1024px
- [ ] `prefers-reduced-motion` respected
- [ ] Page title and meta description correct
- [ ] Lighthouse accessibility score > 90

---

## 9. Phase 7 — CI/CD Integration

### 9.1 Per-repo CI (auto-generated decks)

Add to the repo's GitHub Actions workflow:

```yaml
pitch-deck:
  runs-on: ubuntu-latest
  if: github.ref == 'refs/heads/main'
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with: { python-version: '3.12' }
    - name: Install organvm-engine
      run: pip install organvm-engine
    - name: Generate pitch deck
      run: organvm-engine pitch generate --repo ${{ github.event.repository.name }}
    - name: Verify output
      run: |
        test -f docs/pitch/index.html
        grep -q "ORGANVM:PITCH:AUTO" docs/pitch/index.html
    - name: Commit if changed
      run: |
        git diff --quiet docs/pitch/ || {
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/pitch/
          git commit -m "chore: regenerate pitch deck [skip ci]"
          git push
        }
```

### 9.2 Per-repo CI (bespoke decks)

```yaml
pitch-deck:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with: { node-version: '20' }
    - name: Install & build
      run: cd src/pitch && npm ci && npm run build
    - name: Verify output
      run: test -f docs/pitch/index.html || test -f docs/index.html
```

Bespoke output is **not** auto-committed — it's managed manually or by the repo's existing CD pipeline.

### 9.3 Ecosystem-wide sync (meta-organvm)

```yaml
# .github/workflows/pitch-sync.yml
name: Pitch Deck Sync
on:
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6 AM UTC
  workflow_dispatch:
    inputs:
      organ: { description: 'Organ to sync (empty=all)', required: false }
      dry_run: { description: 'Dry run only', type: boolean, default: true }
```

### 9.4 Compliance gate (ORGAN-III repos with regulated terminology)

For repos with terminology compliance concerns, integrate a gatekeeper scan on pitch output:

```bash
scripts/gatekeeper-scan.sh docs/pitch/index.html
```

Ensure no prohibited vocabulary (gambling terminology, etc.) appears in production output.

---

## 10. Phase 8 — Quality Gates & Review

### 10.1 Auto-generated checks

| Check | Pass Criteria |
|-------|---------------|
| HTML validity | 0 errors (W3C validator or `html-validate`) |
| Link integrity | All links resolve 200/301 (`lychee` or `linkchecker`) |
| Accessibility | Lighthouse score >= 90 |
| Content completeness | All sections have non-placeholder content |
| File size | < 100KB |
| Marker present | `ORGANVM:PITCH:AUTO` in output |
| Organ palette | Accent color matches organ theme |

### 10.2 Bespoke checks (in addition to above)

| Check | Pass Criteria |
|-------|---------------|
| Build succeeds | `npm run build` exits 0 |
| TypeScript | `tsc --noEmit` passes |
| Bundle size | < 500KB gzipped |
| Narrative coherence | Problem → Solution → Proof arc complete (human review) |
| Animation performance | 60 FPS on mid-range device |
| Mobile responsive | Usable at 375px width |
| Reduced motion | All animations disabled under `prefers-reduced-motion` |
| Constants accuracy | Values match source of truth (CI drift check) |

### 10.3 Review workflow

**Auto-generated (Tier 1-2):**
1. Run `pitch generate --dry-run`, inspect output
2. If pitch.yaml was modified, submit PR with pitch.yaml changes
3. Reviewer checks content accuracy and tone
4. Merge triggers auto-regeneration

**Bespoke (Tier 3):**
1. Feature branch `feat/pitch-deck`
2. Full implementation
3. PR includes: scroll-through screenshots/GIF, narrative review notes, Lighthouse report
4. Two reviewers: one technical (code), one narrative (content)
5. Merge deploys via GitHub Pages

---

## 11. Phase 9 — External Submission Pipeline

### 11.1 Pitch deck → submission script

The pitch deck is the **internal** artifact. For external submissions (investors, press, accelerators), adapt via the submission scripts in `meta-organvm/organvm-corpvs-testamentvm/docs/applications/submission-scripts/`.

```
Pitch Deck (internal) → Submission Script (external) → Target Platform
```

### 11.2 Conversion process

1. Extract key metrics and narrative from the pitch deck
2. Adapt tone to target audience (VC vs. press vs. accelerator vs. enterprise)
3. Strip internal terminology (organ references, promotion status)
4. Add platform-specific formatting (word limits, required sections)
5. Store submission at `<repo>/docs/submissions/<target>-<date>.md`

### 11.3 PPTX export (bespoke only)

For offline sharing:
1. Browser print-to-PDF as baseline
2. PowerPoint conversion via `pptxgenjs` or manual
3. Store at `<repo>/docs/pitch/pitch--<project-slug>-deck.pptx`

---

## 12. Organ-Specific Guidelines

Each organ has a distinct visual and narrative identity. The auto-generator applies these automatically via `themes.py`; bespoke decks must conform manually.

### Palette & Typography

| Organ | Accent | Background | Heading Font | Badge Color |
|-------|--------|------------|-------------|-------------|
| **I** Theoria | `#6366f1` indigo | `#0c0f1a` | Palatino, serif | `#6366f1` |
| **II** Poiesis | `#e94560` crimson | `#120a1e` | Georgia, serif | `#e94560` |
| **III** Ergon | `#3b82f6` blue | `#0a0f1e` | System sans-serif | `#3b82f6` |
| **IV** Taxis | `#22c55e` green | `#0a0f0a` | SF Mono, monospace | `#22c55e` |
| **V** Logos | `#f59e0b` amber | `#14100a` | Georgia, serif | `#f59e0b` |
| **VI** Koinonia | `#d97706` orange | `#140f0a` | Georgia, serif | `#d97706` |
| **VII** Kerygma | `#ef4444` red | `#14081a` | System sans-serif | `#ef4444` |
| **META** | `#e94560` crimson | `#0f0f23` | Georgia, serif | `#e94560` |

### Tone & Narrative Guidance

| Organ | Tone | Problem Framing | Solution Framing | CTA Language |
|-------|------|----------------|-----------------|-------------|
| **I** | Academic, philosophical, dense | Knowledge gaps, methodological limitations | Formal systems, recursive engines | "Explore the Engine" / "Read the Theory" |
| **II** | Evocative, sensory, artistic | Creative limitations, tool gaps | Performance systems, generative engines | "Experience It" / "Watch" |
| **III** | Crisp, action-oriented, data-backed | Market pain, economic inefficiency | Product mechanism, competitive advantage | "Try It" / "Request Demo" / "Invest" |
| **IV** | System-level, precise | Coordination failures, governance gaps | Automation, orchestration patterns | "View the Pipeline" |
| **V** | Discursive, analytical | Information gaps, discourse failures | Publication, curation, editorial voice | "Read" / "Subscribe" |
| **VI** | Warm, inclusive | Isolation, access barriers | Gathering spaces, learning circles | "Join" / "Attend" |
| **VII** | Direct, broadcast, minimal | Reach limitations, platform dependency | POSSE automation, syndication | "Syndicate" / "Follow" |
| **META** | Authoritative, transparent | Governance complexity, system coherence | Registry, seed contracts, dashboards | "Explore the System" |

### Market Section

**Only rendered for ORGAN-III** repos. All other organs omit slides 6-9 from the bespoke template and the Market section from auto-generated decks. Non-commercial organs should emphasize impact, integration, and roadmap instead.

---

## 13. Maintenance & Sync Cadence

### 13.1 Triggers

| Event | Scope | Action |
|-------|-------|--------|
| Weekly (Monday 6AM UTC) | All auto-generated | `pitch sync` via CI |
| `seed.yaml` change | Affected repo | `pitch generate <repo>` via CI |
| README edit (Problem/Solution/Features/Architecture) | Affected repo | `pitch generate <repo>` via CI |
| `pitch.yaml` change | Affected repo | `pitch generate <repo>` via CI |
| Registry update | All affected repos | `pitch sync` via CI |
| `organ-aesthetic.yaml` change | All repos in that organ | `pitch sync --organ <N>` |
| Manual | Any | Local CLI |

### 13.2 Staleness detection

The sync engine can compare the auto-generated timestamp (embedded in the `PITCH_MARKER` comment) against source file modification times. A deck is stale if any of `README.md`, `seed.yaml`, or `pitch.yaml` is newer than the generated output.

### 13.3 Version tracking

Every auto-generated deck contains:
```html
<!-- ORGANVM:PITCH:AUTO v{VERSION} generated {ISO-TIMESTAMP} -->
```

Bump `PITCH_VERSION` in `pitchdeck/__init__.py` when:
- Template structure changes (sections added/removed)
- CSS/JS changes affecting rendering
- Hero animation changes

### 13.4 Archival

When a repo moves to `ARCHIVED`:
- Pitch deck **retained** but excluded from future syncs
- Add an "Archived" banner if desired
- Remove from `BESPOKE_REPOS` if applicable; add to `ARCHIVED_BESPOKE`

---

## 14. Rollout Sequence & Priority Matrix

### 14.1 Wave plan

| Wave | Scope | Tier | Notes |
|------|-------|------|-------|
| **0** | First bespoke precedent (done) | Bespoke | Audit + this SOP |
| **1** | ORGAN-III PUBLIC_PROCESS repos | Auto + pitch.yaml | Highest external visibility |
| **2** | ORGAN-I, ORGAN-II | Auto | Theory + creative |
| **3** | ORGAN-IV, ORGAN-V, META | Auto | Orchestration + discourse + governance |
| **4** | ORGAN-VI, ORGAN-VII | Auto | Community + distribution |
| **5** | Additional bespoke candidates | Bespoke | Flagship repos across organs |
| **6** | CANDIDATE/LOCAL repos | Auto | Minimal decks for early-stage repos |
| **7** | CI/CD integration + weekly sync | Maintenance | Full pipeline operational |

### 14.2 Priority within each wave

1. `PUBLIC_PROCESS` > `CANDIDATE` > `LOCAL`
2. `flagship` > `standard`
3. Repos with rich READMEs first
4. Repos with live deployments first
5. Recently active repos over stale ones

### 14.3 Effort per tier

| Tier | Per-Repo Effort |
|------|-----------------|
| 0 (excluded) | 0 |
| 1 (auto, no overrides) | 15-30 min (README audit + generate) |
| 2 (auto + pitch.yaml) | 1-2 hours (README audit + pitch.yaml authoring + review) |
| 3 (bespoke) | 2-5 days (SPA development + narrative design + review) |

---

## 15. Decision Trees

### Does this repo get a pitch deck?

```
tier = "infrastructure" OR "archive"?
  YES → Tier 0 (no deck)
  NO  ↓
promotion_status = "LOCAL" with no README?
  YES → Not yet — revisit on promotion
  NO  ↓
Has at least a description in registry or README?
  YES → Gets a pitch deck → proceed to next tree
  NO  → Write minimal README first, then generate
```

### Auto-generated or bespoke?

```
Flagship with active fundraising?
  YES → Bespoke (Tier 3)
  NO  ↓
Pitch doubles as interactive product demo?
  YES → Bespoke (Tier 3)
  NO  ↓
Narrative needs > 7 sections or custom animations?
  YES → Bespoke (Tier 3)
  NO  ↓
README has rich Problem/Solution/Features content?
  YES → Tier 1 (auto, no overrides)
  NO  ↓
Can pitch.yaml fill the gaps?
  YES → Tier 2 (auto + pitch.yaml)
  NO  → Standardize README first → Tier 1
```

### Where does the output go?

```
Does docs/index.html already exist for other content?
  YES → docs/pitch/index.html
  NO  ↓
Is this a bespoke deck that IS the primary docs output?
  YES → docs/index.html
  NO  → docs/pitch/index.html (default)
```

---

## 16. Appendices

### A. Data Assembly Priority Chain

```
pitch.yaml  →  seed.yaml  →  repo-registry.json  →  README.md
 (highest)                                         (lowest)
```

Each source fills only the fields that higher-priority sources left empty. A repo with only registry data still produces a valid (minimal) deck.

### B. CLI Quick Reference

```bash
# Single repo
python -m organvm_engine pitch generate --repo <name> [--dry-run]

# Organ batch
python -m organvm_engine pitch sync --organ ORGAN-III [--dry-run]

# Tier batch
python -m organvm_engine pitch sync --tier flagship [--dry-run]

# Full ecosystem
python -m organvm_engine pitch sync [--dry-run]

# README audit
python -m organvm_engine pitch audit-readmes [--organ III]

# Validate pitch.yaml
python -m organvm_engine pitch validate <repo>
```

### C. File Checklist

**All eligible repos:**
- [ ] `README.md` with standard sections
- [ ] `seed.yaml` with organ, tier, promotion_status
- [ ] `docs/pitch/index.html` (generated or bespoke output)

**Tier 2 additions:**
- [ ] `pitch.yaml` in repo root

**Tier 3 additions:**
- [ ] Pitch source directory (e.g., `src/pitch/`)
- [ ] Build script in `package.json`
- [ ] `seed.yaml` with `pitch.type: bespoke`
- [ ] Entry in `BESPOKE_REPOS` set in `sync.py`

### D. Bespoke Detection Logic

```python
# sync.py — _is_bespoke()
# A file is bespoke if it exists but does NOT contain PITCH_MARKER.
# Auto-generated files always contain the marker.
# Bespoke files never do (they're hand-authored).
```

### E. Glossary

| Term | Definition |
|------|-----------|
| **PITCH_MARKER** | HTML comment identifying auto-generated decks; absence = bespoke |
| **pitch.yaml** | Per-repo content override (highest priority in data assembly) |
| **seed.yaml** | Per-repo contract: organ, tier, edges, promotion status |
| **organ-aesthetic.yaml** | Per-organ visual identity (palette, typography, tone) |
| **taste.yaml** | Base aesthetic standard (Tufte, Dieter Rams) |
| **Tier 0-3** | Pitch deck classification (excluded / auto / enhanced auto / bespoke) |

---

*This SOP is organ-agnostic and repo-agnostic. Each repo's unique pitch content lives in its own README, seed.yaml, and pitch.yaml — not in this document. This document governs the process, not the content.*
