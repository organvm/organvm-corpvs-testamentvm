# Contributing to the ORGAN System Planning Corpus

Thank you for your interest in contributing to this documentation corpus. This repository contains planning, governance, and implementation strategy documents for the eight-organ creative-institutional system.

## Scope

This is a **documentation-only repository**. There is no runtime code. Contributions involve editing markdown documents, JSON registry files, and YAML workflow specifications.

## How to Contribute

### Corrections

If you find factual errors, broken cross-references, or outdated information:

1. Open an issue describing the error and its location (file + section).
2. If you'd like to fix it yourself, fork the repo and submit a PR.

### Suggestions

For structural changes, new documents, or strategic adjustments:

1. Open an issue with the `suggestion` label.
2. Describe the proposed change and its rationale.
3. Reference any existing documents that would be affected.

### Editorial Standards

- Follow the existing document naming conventions (`NN-TITLE.md` for numbered docs).
- Maintain consistency with the reading order and document layers described in `CLAUDE.md`.
- Cross-reference related documents using relative links.
- When modifying `repo-registry.json`, preserve the existing JSON schema exactly.
- Do not modify files in the `archive/` directory — it is frozen.

### Commit Messages

- Use imperative mood, under 72 characters for the title line.
- Reference the document(s) changed (e.g., `Update repo-registry.json: add repo X to ORGAN-III`).

## Review Process

All PRs are reviewed by the project owner (@4444j99). Documentation changes are evaluated for:

- Factual accuracy
- Consistency with the eight-organ model
- Alignment with the parallel launch strategy
- Portfolio-quality language (grant reviewers and hiring managers are the audience)

## Questions

Open an issue with the `question` label.
