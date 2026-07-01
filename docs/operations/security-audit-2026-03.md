# Security Audit Report — March 2026

**Sprint 56: SECURITAS**
**Date:** 2026-03-04
**Scope:** All 7 submodules in `meta-organvm/` superproject
**Auditor:** AI-assisted (Claude Code)

---

## Executive Summary

The meta-organvm codebase demonstrates good foundational security hygiene: no known CVEs in third-party dependencies, consistent use of `yaml.safe_load()`, no `subprocess` or `eval()` calls in source code, and no plaintext `http://` URLs. However, one **CRITICAL** finding requires immediate action: real GitHub App credentials are committed to the superproject in `.env.example`. Five additional medium/low-priority findings are documented below.

**Overall Risk Assessment: MEDIUM** (one critical credential exposure, otherwise low risk)

---

## Findings

### CRITICAL

#### C-1: Real credentials committed in `.env.example`

**File:** `~/Workspace/meta-organvm/.env.example` (tracked in superproject git)
**Commit:** `d9db3fd` ("docs: github app configuration and 1password credential references")

The file contains:
- `GITHUB_APP_ID=2958047` (real app ID)
- `GITHUB_APP_CLIENT_ID=Iv23liN5op3fxVRtJgAp` (real client ID)
- `GITHUB_WEBHOOK_SECRET=ea504da70f6cc2cd73c47b63330fd61d3e812374f4a43a4126d698ba13bc1b2f` (real webhook secret)

Even though the private key is correctly deferred to 1Password (`op read ...`), the webhook secret is a full 256-bit HMAC secret that could allow webhook spoofing if exposed. The client ID is public-ish but the webhook secret is not.

**Impact:** An attacker with access to the git history can craft spoofed GitHub webhook payloads.

**Remediation:**
1. Rotate the webhook secret immediately in GitHub App settings.
2. Replace real values in `.env.example` with placeholders: `GITHUB_WEBHOOK_SECRET=<retrieve-from-1password>`.
3. Use `git filter-repo` or BFG Repo Cleaner to purge the secret from git history, or accept that the old secret is burned (rotation is sufficient if the repo is private).

---

### MEDIUM

#### M-1: No Dependabot configured on 5 of 7 submodules

Only `.github/` (the org-level community health repo) has a `dependabot.yml` — and it only covers `github-actions`, not pip/Python dependencies.

**Missing Dependabot:** organvm-engine, organvm-mcp-server, alchemia-ingestvm, system-dashboard, schema-definitions.

**Impact:** Vulnerable transitive dependencies will not trigger automated PRs.

**Remediation:** Add `dependabot.yml` to each submodule with:
```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
```

#### M-2: No `.env` entry in any `.gitignore`

None of the submodule `.gitignore` files explicitly exclude `.env` files. The superproject uses an allowlist pattern (`*` then `!specific-files`) which implicitly blocks `.env`, but submodules use a standard blocklist pattern and omit `.env`.

**Impact:** A developer creating a `.env` file inside a submodule could accidentally commit it.

**Remediation:** Add `.env` and `.env.local` to the `.gitignore` of each submodule.

#### M-3: GitHub Actions workflows lack `permissions` blocks

All 5 CI workflows (`organvm-engine`, `organvm-mcp-server`, `alchemia-ingestvm`, `system-dashboard`, `schema-definitions`) run without explicit `permissions:` declarations.

**Impact:** Workflows inherit the repository's default token permissions, which may be broader than needed (especially `contents: write` or `packages: write`).

**Remediation:** Add least-privilege `permissions:` block to each workflow:
```yaml
permissions:
  contents: read
```

#### M-4: Loose dependency version pinning

All subprojects use minimum-version-only pins (e.g., `pyyaml>=6.0`, `fastapi>=0.104`). No lockfile (`requirements.lock`, `pip-compile` output) is committed.

**Impact:** Builds are not reproducible. A compromised or buggy new release of any dependency will be automatically pulled on next install.

**Remediation:**
- Generate `requirements.lock` files using `pip-compile` (from `pip-tools`).
- Pin exact versions in lockfiles while keeping loose pins in `pyproject.toml`.
- Add lockfile regeneration to CI.

---

### LOW

#### L-1: Google Docs OAuth token stored without restricted permissions

**File:** `alchemia-ingestvm/src/alchemia/channels/google_docs.py`

The OAuth2 token is written to `~/.config/alchemia/google_token.json` via `TOKEN_PATH.write_text(creds.to_json())` without setting restrictive file permissions (e.g., `chmod 600`).

**Impact:** On shared systems, other users could read the token file.

**Current state:** The config directory does not currently exist (no Google Docs integration is active), so this is theoretical.

**Remediation:** After writing the token, set permissions:
```python
import os
TOKEN_PATH.write_text(creds.to_json())
os.chmod(TOKEN_PATH, 0o600)
```

---

## Positive Findings (No Issues)

| Check | Result |
|-------|--------|
| **pip-audit (CVE scan)** | No known vulnerabilities in 45+ installed packages (PyYAML 6.0.3, FastAPI 0.129.0, Jinja2 3.1.6, cryptography 46.0.5, etc.) |
| **YAML deserialization** | All 12 `yaml.load` calls across all submodules use `yaml.safe_load()` — no unsafe deserialization |
| **Shell injection** | Zero uses of `subprocess`, `os.system()`, `eval()`, or `exec()` in any source code |
| **Pickle deserialization** | No `pickle.load()` usage found |
| **HTTP URLs** | No plaintext `http://` URLs in any `.py`, `.yaml`, or `.json` source files |
| **Schema validation** | All 3 schema examples pass validation (dispatch, registry, seed) |
| **Secrets in source code** | No hardcoded API keys, passwords, or tokens in Python/YAML source (the `.env.example` issue is in a config file, not source) |
| **`shell=True`** | Not used anywhere in the codebase |

---

## Dependency Inventory

| Package | Version | Notes |
|---------|---------|-------|
| PyYAML | 6.0.3 | Current, safe_load only |
| FastAPI | 0.129.0 | Current |
| Jinja2 | 3.1.6 | Current, autoescaping assumed |
| cryptography | 46.0.5 | Current |
| Pydantic | 2.12.5 | Current |
| mcp | 1.26.0 | Current |
| jsonschema | 4.26.0 | Current |
| httpx | 0.28.1 | Current |

---

## Recommendations Summary

| Priority | Finding | Action | Effort |
|----------|---------|--------|--------|
| **CRITICAL** | C-1: Webhook secret in `.env.example` | Rotate secret, replace with placeholder, scrub history | 30 min |
| **MEDIUM** | M-1: No Dependabot on submodules | Add `dependabot.yml` to 5 repos | 15 min |
| **MEDIUM** | M-2: No `.env` in gitignore | Add `.env` to each submodule `.gitignore` | 10 min |
| **MEDIUM** | M-3: No CI permissions blocks | Add `permissions: contents: read` | 10 min |
| **MEDIUM** | M-4: No dependency lockfiles | Generate `requirements.lock` with pip-compile | 45 min |
| **LOW** | L-1: Token file permissions | Add `os.chmod(path, 0o600)` after write | 5 min |

**Total estimated remediation effort:** ~2 hours

---

## Methodology

1. **CVE scanning:** `pip-audit` against installed venv (45+ packages)
2. **Secret detection:** Regex search for `password`, `secret`, `api_key`, `token` across all `.py`, `.yaml`, `.json` source files, excluding test/example/schema/template contexts
3. **Dependency configuration:** Checked all submodules for `dependabot.yml`
4. **Schema validation:** Ran `validate.py --all-examples` against canonical JSON Schemas
5. **URL audit:** Searched for plaintext `http://` URLs across all source files
6. **Code safety patterns:** Searched for `eval()`, `exec()`, `subprocess`, `os.system()`, `pickle.load()`, `yaml.load()` (unsafe), `shell=True`
7. **Gitignore audit:** Verified `.env` coverage across all submodules
8. **CI hardening:** Checked for `permissions:` blocks in GitHub Actions workflows
9. **Dependency pinning:** Reviewed `pyproject.toml` dependency specifications

---

*Next audit recommended: 2026-06-01 (quarterly cadence)*
