# 10: Repository Standards (Skills Framework)

**Date:** 2026-02-09
**Status:** ACTIVE — applies to all ~44 repos across 8 GitHub organizations
**Derived from:** Three documentation skills (`github-repository-standards`, `github-repo-curator`, `github-profile-architect`)
**Complements:** `01-readme-audit-framework.md` (scoring rubric), `03-per-organ-readme-templates.md` (organ-specific templates), `04-per-organ-validation-checklists.md` (validation checklists), `08-canonical-action-plan.md` D-07 (tiered classification)

---

## 1. Purpose & Scope

This document defines **repository-level standards** enforced across all eight organs of the organvm system. It synthesizes three documentation skills into a single reference:

- **Root Hygiene** — what files and directories belong at root, and what doesn't (from `github-repository-standards`)
- **Curation & Visibility** — how repos are classified, tagged, and presented (from `github-repo-curator`)
- **Profile Integration** — how individual repos contribute to org-level branding (from `github-profile-architect`)

**Relationship to existing documents:**

| Document | Covers | This Document Adds |
|----------|--------|-------------------|
| `01` Audit Framework | README scoring rubric (0–100) | Root hygiene, community health files, badge standards |
| `03` README Templates | Organ-specific README sections | Progressive disclosure pattern, hero section standard, badge ordering |
| `04` Validation Checklists | Per-organ QA checklists | Cross-cutting compliance checklist for root hygiene + community health |
| `08` D-07 Tiered Classification | Flagship/Standard/Stub/Archive criteria | Per-tier README depth requirements, badge minimums, visibility rules |

**When to reference this document:** Before creating or auditing any repository in the eight-organ system. The standards here apply universally; organ-specific adaptations live in `03` and `04`.

---

## 2. Root Hygiene Standard

The repository root is a lobby. It signals architectural maturity at a glance. Implementation details belong in subdirectories.

### Required Root Files

Every repo, regardless of tier, must have these files at root:

| File | Purpose | Notes |
|------|---------|-------|
| `README.md` | Human entry point | Depth varies by tier (see §3) |
| `LICENSE` | Legal terms | See §2.3 for license selection |
| `.gitignore` | VCS exclusion rules | Language/framework appropriate |
| `CLAUDE.md` | AI agent context | Project-specific guidance for Claude Code |

### Required Directories

| Directory | When Required | Contents |
|-----------|---------------|----------|
| `.github/` | All repos | Community health files, issue templates, PR template, workflows |
| `docs/` | Repos with documentation beyond README | ADRs, API specs, guides |
| `src/` or equivalent | Code repos | Source code (language-appropriate: `src/`, `lib/`, `pkg/`) |

### The `.config/` Strategy

Tool configuration files (ESLint, Prettier, Docker, etc.) clutter the root. Where tooling supports it, move configs to `.config/`:

```
.config/
├── eslint.config.js
├── prettier.config.js
└── docker/
    └── Dockerfile
```

Update `package.json` scripts or tool CLI flags to reference the new paths. Not all tools support this — use pragmatism over purity.

### Root File Count Target

- **Code repos:** Target <20 files at root. If root exceeds 20, audit for relocation candidates.
- **Documentation repos:** Flexible — this planning corpus has 30+ root documents by design. The "lobby" metaphor applies to code repos; documentation repos are more like libraries where the files *are* the content.

### License Selection Guide

| Repo Type | Recommended License | Rationale |
|-----------|-------------------|-----------|
| Source code (libraries, tools) | MIT | Maximum adoption, minimal friction |
| SaaS/commercial (ORGAN-III) | MIT or proprietary | Depends on business model |
| Documentation/planning | CC BY-SA 4.0 | Attribution + share-alike for written works |
| Art/creative (ORGAN-II) | CC BY-SA 4.0 or CC BY-NC-SA 4.0 | Protects creative work; NC variant for commercial protection |
| Infrastructure/governance (ORGAN-IV) | MIT | Encourages framework adoption |

---

## 3. README Standard

The README is a conversion funnel. It moves the reader from "What is this?" to engagement in under 30 seconds.

### Progressive Disclosure Pattern

Every README follows the same information architecture, scaled by tier:

1. **Hero Section** (visible without scrolling)
   - Project title
   - Badge row (see §6)
   - One-line hook (what this is, in one sentence)
   - Quick start or navigation link

2. **Value Section** (why this exists)
   - Problem statement or motivation
   - What the project does differently

3. **Action Section** (how to use it)
   - Installation / getting started
   - Usage examples
   - Documentation links

4. **Context Section** (where this fits)
   - Cross-references to related repos/organs
   - Contributing guidelines
   - License and author

### Tiered README Depth

Aligned with `08-canonical-action-plan.md` D-07 tier criteria:

| Tier | Sections | Word Target | Required Sections |
|------|----------|-------------|-------------------|
| **Flagship** | 12 | 3,000+ words | All 4 disclosure layers + organ-specific sections from `03` templates |
| **Standard** | 8 | 1,000+ words | Hero + Value + Action + Context (condensed) |
| **Stub** | 4 | 200+ words | Title + purpose + status + links to parent organ |
| **Archive** | 2 | 50+ words | Archive notice + redirect to successor/parent |

### Hero Section Pattern

```markdown
# Project Name

[![Status](badge)][link] [![License](badge)][link] [![Organ](badge)][link]

> One-line hook: what this project is and why it matters.

[Quick Start](#quick-start) | [Documentation](#documentation) | [Contributing](#contributing)
```

The hero section is the most important real estate in the README. It must communicate purpose without requiring the reader to scroll.

### Cross-References

Use the `03-per-organ-readme-templates.md` templates for organ-specific section requirements. This document defines the *pattern*; `03` defines the *content* per organ type.

During the Bronze Sprint, use `[TBD:org/repo#section]` placeholders for cross-references that can't yet be resolved. These are resolved in a dedicated cross-reference pass after all flagship drafts exist (per SC-7 in `08`).

---

## 4. Community Health Files

The `.github/` directory contains files that GitHub surfaces in the repository UI (security policy, contributing guidelines, etc.) and automation workflows.

### Required Files (All Repos)

| File | Purpose | Tier Requirement |
|------|---------|-----------------|
| `CONTRIBUTING.md` | How to contribute | All tiers except Archive |
| `SECURITY.md` | Vulnerability reporting | All tiers except Archive |
| `CODE_OF_CONDUCT.md` | Community standards | All tiers except Archive |
| `PULL_REQUEST_TEMPLATE.md` | PR checklist | Flagship and Standard tiers |
| `ISSUE_TEMPLATE/` | Structured issue forms | Flagship and Standard tiers |

### SECURITY.md Pattern

For repos that are documentation-only or non-deployed:

```markdown
# Security Policy

## Reporting a Vulnerability

If you discover a security issue, please email [security contact]
rather than opening a public issue.

## Scope

This repository contains [documentation/planning materials/source code].
[Adjust scope description per repo type.]
```

For deployed code repos (ORGAN-III), include supported versions and response timeline.

### CONTRIBUTING.md Pattern

Adapt per repo type:
- **Code repos:** Fork → branch → PR workflow, development setup, testing requirements
- **Documentation repos:** Correction process, suggestion process, editorial standards
- **Art repos (ORGAN-II):** Collaboration guidelines, attribution requirements, exhibition context

### Issue Templates

Minimum two templates per repo:
1. **Bug report / Document correction** — structured problem reporting
2. **Feature request / Planning suggestion** — structured improvement proposals

Use GitHub's YAML-based issue forms where possible for structured input.

### CODE_OF_CONDUCT.md

Use [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) as the standard across all repos. Customize the enforcement contact per org.

---

## 5. Curation & Visibility Strategy

### Visibility Decision Matrix

Every repo must have an explicit visibility decision recorded in `repo-registry.json`:

| Visibility | Criteria | Action |
|------------|----------|--------|
| **Public** | Portfolio-worthy, demonstrates organ function, contributes to external narrative | Default for Flagship and Standard tiers |
| **Private** | Valuable but not showcase-ready, client work, infrastructure internals | Standard tier repos during development; promote to Public when ready |
| **Archive** | Completed, abandoned, or merged elsewhere; retains reference value | Archive tier repos; set GitHub "archived" flag |
| **Delete** | Truly obsolete, redundant, or empty with no recovery value | Only after explicit human decision; never automated |

### Topics/Tags Taxonomy

Every repo receives a consistent set of GitHub topics for discoverability:

**Required topics (all repos):**
1. **Organ tag:** `organ-i`, `organ-ii`, `organ-iii`, `organ-iv`, `organ-v`, `organ-vi`, `organ-vii`
2. **Domain tag:** `theory`, `art`, `commerce`, `orchestration`, `public-process`, `community`, `marketing`
3. **Type tag:** `saas`, `b2b`, `b2c`, `library`, `tool`, `documentation`, `governance`, `creative`, `community-space`
4. **Status tag:** `active`, `deployed`, `skeleton`, `archived`, `experimental`

**Optional topics:**
- Technology tags: `typescript`, `python`, `rust`, etc.
- Framework tags: `nextjs`, `react`, `fastapi`, etc.
- The `organvm` tag on all repos for system-wide search

### Pinned Repository Strategy

Each GitHub org can pin up to 6 repositories. Pin selection criteria:

1. **Flagship repo** — the most impressive/complete in the org (always pinned)
2. **Most relevant to portfolio narrative** — supports the organ's story
3. **Active development** — shows the org is alive
4. **Demonstrates range** — different technologies or approaches within the organ
5. **Collaborative work** — if applicable, shows teamwork
6. **Infrastructure/governance** — shows architectural maturity (especially for ORGAN-IV)

Review pinned repos quarterly as part of the monthly audit cycle defined in [`orchestration-system-v2.md`](../implementation/orchestration-system-v2.md).

---

## 6. Badge & Shield Standards

Badges provide at-a-glance metadata. They must be consistent, meaningful, and not overwhelming.

### Style Convention

All badges use **`flat-square`** style from [shields.io](https://shields.io) for visual consistency across the system:

```markdown
![Badge](https://img.shields.io/badge/label-message-color?style=flat-square)
```

### Badge Ordering Convention

Badges appear in this order in the README hero section:

1. **Status badges** — build status, CI/CD, deployment status
2. **Metadata badges** — version, license, organ membership
3. **Social badges** — stars, forks (only on repos with external traction)
4. **Activity badges** — last commit, open issues (optional)

### Per-Organ Badge Color Scheme

| Organ | Color | Hex | Rationale |
|-------|-------|-----|-----------|
| I (Theory) | Deep Blue | `#1a237e` | Depth, intellect |
| II (Art) | Purple | `#6a1b9a` | Creativity, expression |
| III (Commerce) | Green | `#2e7d32` | Growth, commerce |
| IV (Orchestration) | Orange | `#e65100` | Coordination, alertness |
| V (Public Process) | Teal | `#00695c` | Transparency, openness |
| VI (Community) | Warm Red | `#c62828` | Connection, gathering |
| VII (Marketing) | Gold | `#f9a825` | Visibility, amplification |

### Required Badges by Tier

| Tier | Minimum Badges | Required Types |
|------|---------------|----------------|
| **Flagship** | 4+ | License + Organ + Status + at least 1 metadata |
| **Standard** | 2+ | License + Organ |
| **Stub** | 1 | Organ membership |
| **Archive** | 1 | Archive status notice |

### Organ Membership Badge

Every repo displays its organ membership:

```markdown
![ORGAN-I: Theory](https://img.shields.io/badge/ORGAN--I-Theory-1a237e?style=flat-square)
```

---

## 7. Compliance Checklist

Quick-reference checklist for validating any repo against these standards. Use alongside the organ-specific checklists in `04-per-organ-validation-checklists.md`.

### Root Hygiene
- [ ] `README.md` exists and matches tier depth requirement
- [ ] `LICENSE` exists and matches repo type recommendation
- [ ] `.gitignore` exists and is appropriate for the project
- [ ] `CLAUDE.md` exists with project-specific guidance
- [ ] Root file count is reasonable (<20 for code repos)
- [ ] Tool configs relocated to `.config/` where supported

### Community Health
- [ ] `.github/CONTRIBUTING.md` exists (except Archive tier)
- [ ] `.github/SECURITY.md` exists (except Archive tier)
- [ ] `.github/CODE_OF_CONDUCT.md` exists (except Archive tier)
- [ ] `.github/PULL_REQUEST_TEMPLATE.md` exists (Flagship/Standard)
- [ ] `.github/ISSUE_TEMPLATE/` contains at least 2 templates (Flagship/Standard)

### README Quality
- [ ] Hero section: title + badges + one-line hook + navigation
- [ ] Progressive disclosure: can understand purpose in <30 seconds
- [ ] Badge style is `flat-square`
- [ ] Badge order follows convention: Status → Metadata → Social → Activity
- [ ] Cross-references use correct format (no broken links, TBD markers resolved)
- [ ] Scores ≥90/100 on `01` rubric (Flagship) or ≥70/100 (Standard)

### Visibility & Curation
- [ ] Visibility decision recorded in `repo-registry.json`
- [ ] GitHub topics set: organ tag + domain tag + type tag + status tag
- [ ] Repository description filled in on GitHub
- [ ] Pinned repos reviewed (if this is a flagship)

### Organ-Specific
- [ ] Organ-specific sections from `03` template are present
- [ ] Organ-specific validation from `04` checklist passes
- [ ] Cross-organ references follow dependency rules (no back-edges)

---

## Appendix: Relationship to Existing Standards Documents

This document is **Layer 1 (Phase 1 Planning)** in the document architecture, numbered `10` to follow the existing `01`–`08` sequence. It introduces no contradictions with existing documents — it adds coverage for root hygiene, community health, curation, and badges that the existing `01`–`05` planning toolkit does not address.

**Precedence rules:**
- For README *scoring*, defer to `01-readme-audit-framework.md`
- For README *content*, defer to `03-per-organ-readme-templates.md`
- For README *validation*, defer to `04-per-organ-validation-checklists.md`
- For tier *classification*, defer to `08-canonical-action-plan.md` D-07
- For root hygiene, community health, badges, visibility, and curation, **this document is authoritative**
- For *internal* directory layout (src/-vs-flat, monorepo `apps/`+`packages/`, feature-vs-type organization, doc taxonomy, nesting, environments), defer to `26-internal-directory-layout--monorepo-feature-organization.md` (added 2026-05-29)
