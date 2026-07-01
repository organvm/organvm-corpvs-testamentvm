# Audit: Stable Unit Notice Ownership & Governance Sync
**Date:** 2026-04-02
**Status:** DRAFT (Plotting & Tending)

## Objective
Identify and resolve mismatches between repository `seed.yaml` metadata and the canonical `registry-v2.json`. Ensure all "Stable units" (`GRADUATED` status) possess the required notice ownership metadata and `NOTICE` files.

## Background
According to the **Stable Units Protocol**, a unit is stable when its identity and interfaces are hardened. Transitioning to `GRADUATED` (Stable) requires:
1. Declared interface section.
2. Changelog practice.
3. **Ownership metadata** (Notice Ownership).
4. Branch protection intent.
5. Breaking change declaration.

## Governance Mismatch Report

### 1. public-record-data-scrapper (Flagship)
- **Registry Status:** `GRADUATED` (since 2026-02-28)
- **seed.yaml Status:** `PUBLIC_PROCESS` (v1.0)
- **Issues:**
    - Mismatch in promotion status.
    - Missing `ownership` block in `seed.yaml`.
    - Missing `NOTICE` file (recommended for graduated flagship).
    - License is currently MIT; check if transition to Apache-2.0 is desired for stronger patent protection as a "Stable deliverable."

### 2. classroom-rpg-aetheria (Standard)
- **Registry Status:** `GRADUATED`
- **seed.yaml Status:** `PUBLIC_PROCESS` (v1.0)
- **Issues:**
    - Mismatch in promotion status.
    - Missing `ownership` block.

### 3. general Audit of GRADUATED units
The following units are marked `GRADUATED` in `registry-v2.json` but may require tending to their `seed.yaml` (v1.1 upgrade + ownership):
- `organvm-iv-taxis/orchestration-start-here`
- `organvm-iii-ergon/commerce--meta`
- `4444J99/domus-semper-palingenesis`
- `meta-organvm/organvm-engine`
- `meta-organvm/praxis-perpetua`
- `organvm-i-theoria/conversation-corpus-engine`
- `organvm-vii-kerygma/kerygma-profiles`
- `organvm-vii-kerygma/distribution-strategy`
- `organvm-vii-kerygma/social-automation`
- `organvm-vii-kerygma/kerygma-pipeline`
- `organvm-vii-kerygma/announcement-templates`

## Proposed Tending Actions

### Phase 1: Metadata Hardening
- Upgrade `seed.yaml` to `schema_version: "1.1"`.
- Sync `promotion_status: GRADUATED`.
- Add `ownership` block:
  ```yaml
  ownership:
    lead: "[user]"
    collaborators: []
    ai_agents:
      - type: claude
        access: [read, edit, commit]
        scope: "maintenance"
  ```

### Phase 2: Notice Ownership (Legal)
- Add `NOTICE` file to root of `GRADUATED` repositories.
- Format for `NOTICE`:
  ```text
  ORGANVM System
  Copyright 2026 [user] / ORGANVM

  This product includes software developed as part of the ORGANVM
  meta-workspace (https://github.com/meta-organvm).
  ```

### Phase 3: Interface & Breaking Changes
- Ensure each repo has a `docs/INTERFACE.md` or a clear section in `README.md`.
- Explicitly define breaking change criteria in `seed.yaml` (future schema update).

## Verification Checklist
- [ ] `registry-v2.json` matches `seed.yaml` for all 126 repos.
- [ ] All `GRADUATED` units have `ownership` metadata.
- [ ] All `flagship` graduated units have a `NOTICE` file.
