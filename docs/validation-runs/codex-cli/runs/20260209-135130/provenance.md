# Provenance

- **Run ID:** `20260209-135130`
- **Generated at (UTC):** `2026-02-09T19:15:05Z`
- **Workspace root:** `~/Workspace/organvm-pactvm/ingesting-organ-document-structure`

## Tool Versions

- `codex`: `codex-cli 0.98.0`
- `gemini`: `0.27.3`
- `gh`: `gh version 2.86.0 (2026-01-21)`
- `copilot` (via gh): `0.0.361`

## Model Pins

- Codex: `gpt-5`
- Gemini: `gemini-3-pro-preview`
- Copilot: `gpt-5`

## Command Notes

1. Codex run required overriding local config key `model_reasoning_effort` from unsupported `xhigh` to `high`.
2. Gemini run required constraining extensions to `FileSearch` to avoid extension noise in stdout.
3. Copilot run required token isolation because the default classic `GH_TOKEN` was rejected by Copilot CLI in this environment.
4. Copilot run used `--disable-builtin-mcps` for stable headless execution.

## Integrity

- Input files and SHA256 values are recorded in `input-manifest.json`.
- Raw model outputs are preserved as `*.raw.md`.
