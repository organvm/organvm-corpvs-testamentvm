# Contributing to the ORGANVM System

Thank you for your interest in contributing. This document explains how the eight-organ system works and how to find your way in.

## System Overview

The organvm system is an eight-organ creative-institutional system spanning 149 registry entries across the organ/meta GitHub organizations plus personal/local entries:

| Organ | Domain | Organization | What's Here |
|-------|--------|-------------|-------------|
| I | Theory | [organvm-i-theoria](https://github.com/organvm-i-theoria) | Epistemological frameworks, recursive engines, ontological systems |
| II | Art | [organvm-ii-poiesis](https://github.com/organvm-ii-poiesis) | Generative art, interactive systems, performance frameworks |
| III | Commerce | [organvm-iii-ergon](https://github.com/organvm-iii-ergon) | Products, deployed systems, customer-facing tools |
| IV | Orchestration | [organvm-iv-taxis](https://github.com/organvm-iv-taxis) | Governance, routing, system coordination |
| V | Public Process | [organvm-v-logos](https://github.com/organvm-v-logos) | Essays, building in public, process documentation |
| VI | Community | [organvm-vi-koinonia](https://github.com/organvm-vi-koinonia) | Community infrastructure, reading groups, collaborative spaces |
| VII | Marketing | [organvm-vii-kerygma](https://github.com/organvm-vii-kerygma) | Content distribution, announcements, POSSE automation |
| Meta | Umbrella | [meta-organvm](https://github.com/meta-organvm) | Planning corpus, registry, governance docs |

## How to Contribute

### Types of Contributions

**Code**: Bug fixes, features, performance improvements, tests. Most code lives in Organs I-III.

**Documentation**: README improvements, tutorial additions, typo fixes. Every repo in the system has a README. If you find one that's unclear, that's a contribution opportunity.

**Essays**: Opinion pieces, case studies, tutorials, retrospectives. Published via ORGAN-V ([public-process](https://github.com/organvm-v-logos/public-process)).

**Feedback**: Open an issue on any repo describing what confused you, what's broken, or what could be improved. Honest feedback from outside the system is the most valuable contribution.

### Workflow

1. **Find a repo**: Browse the organizations above or look for issues labeled `good-first-issue`
2. **Fork the repo**: Standard GitHub fork workflow
3. **Create a branch**: Use descriptive branch names (`fix/auth-middleware-bug`, `feat/add-p5js-template`)
4. **Make your changes**: Follow the coding conventions in the repo's README or CLAUDE.md
5. **Open a PR**: Reference any related issues. Describe what you changed and why.

### Code Standards

- Write clear, readable code over clever code
- Use descriptive names for variables, functions, and classes
- Include tests for new functionality
- Follow PEP 8 for Python, strict TypeScript for TS/JS
- Comments explain "why", not "what"

### Commit Messages

- Use imperative mood: "fix bug" not "fixed bug"
- Keep the title under 72 characters
- Reference issue numbers when applicable

## Entry Points

If you're looking for where to start, these repos are good first-contribution targets:

1. **[example-choreographic-interface](https://github.com/organvm-ii-poiesis/example-choreographic-interface)** — Choreographic interfaces and gesture-driven art. Add gesture recognition examples.
2. **[example-generative-music](https://github.com/organvm-ii-poiesis/example-generative-music)** — Generative music examples. Add a new synthesis approach or audio example.
3. **[reading-group-curriculum](https://github.com/organvm-vi-koinonia/reading-group-curriculum)** — Reading group curricula. Suggest a reading list or discussion guide.
4. **[social-automation](https://github.com/organvm-vii-kerygma/social-automation)** — Social media automation for POSSE distribution. Add announcement templates.
5. **[orchestration-start-here](https://github.com/organvm-iv-taxis/orchestration-start-here)** — System orchestration. Document workflow triggers or improve existing docs.

## Architecture Decisions

Major architectural decisions are documented in ADRs (Architecture Decision Records) in `docs/adr/`. If you're wondering *why* something works the way it does, start there. See [ADR-006](docs/adr/006-ai-conductor-methodology.md) for the AI-conductor methodology that shapes how documentation is produced in this system.

## Code of Conduct

Be respectful, constructive, and honest. This system values transparency — it's built in public — and that ethos extends to all interactions. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).

## Questions?

Open an issue on any repo, or start a discussion in [orchestration-start-here](https://github.com/organvm-iv-taxis/orchestration-start-here/discussions) (if discussions are enabled).
