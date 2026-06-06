#!/usr/bin/env python3
"""Deploy community health files to flagship repos missing them.

Deploys CONTRIBUTING.md, SECURITY.md, issue templates, PR template,
and (where needed) LICENSE to flagship repos in the organvm system.

Each CONTRIBUTING.md is customized per-repo with stack, setup instructions,
and project-specific contribution guidelines. SECURITY.md, issue templates,
and PR template follow a shared standard.

Usage:
    python3 scripts/deploy-flagship-health.py                # Deploy all missing files
    python3 scripts/deploy-flagship-health.py --dry-run      # Preview without deploying
    python3 scripts/deploy-flagship-health.py --repo NAME    # Deploy to one repo only
    python3 scripts/deploy-flagship-health.py --file TYPE    # Deploy one file type only
                                                             # (contributing, security, issues, pr, license)

Requires: gh CLI authenticated with push access to all target orgs.
"""

import argparse
import base64
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class FlagshipRepo:
    """A flagship repo and what it needs."""
    org: str
    repo: str
    default_branch: str
    stack: str
    description: str
    setup_instructions: str
    test_command: str
    code_style_notes: str
    missing: list[str] = field(default_factory=list)
    language: str = "Python"
    package_manager: str = ""
    monorepo: bool = False


# ---------------------------------------------------------------------------
# Flagship definitions
# ---------------------------------------------------------------------------

FLAGSHIPS: list[FlagshipRepo] = [
    FlagshipRepo(
        org="organvm-i-theoria",
        repo="recursive-engine--generative-entity",
        default_branch="main",
        stack="Python (recursive theory engine, symbolic systems)",
        description=(
            "RE:GE is a recursive theory engine that explores epistemological "
            "frameworks, identity systems, and ontological recursion through "
            "Python. It models self-referential symbolic structures as "
            "computational artifacts."
        ),
        setup_instructions="""\
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/recursive-engine--generative-entity.git
cd recursive-engine--generative-entity

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```""",
        test_command="pytest -v",
        code_style_notes=(
            "Follow PEP 8. Use type hints for function signatures. "
            "Add docstrings to public APIs. Maintain the ritual/mythic tone "
            "in documentation files."
        ),
        missing=["SECURITY.md", ".github/ISSUE_TEMPLATE/", ".github/PULL_REQUEST_TEMPLATE.md"],
        language="Python",
    ),
    FlagshipRepo(
        org="organvm-ii-poiesis",
        repo="metasystem-master",
        default_branch="master",
        stack="Node.js / HTML / CSS / JavaScript (digital temple, multimedia art)",
        description=(
            "Metasystem Master is a digital temple and multimedia art platform "
            "combining interactive web experiences, generative visuals, and "
            "audio synthesis. It serves as the creative flagship of the "
            "organvm art organ."
        ),
        setup_instructions="""\
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/metasystem-master.git
cd metasystem-master

# Install dependencies
npm install

# Start development server
npm run dev
```""",
        test_command="npm test",
        code_style_notes=(
            "Use `const` over `let`; avoid `var`. Keep JavaScript readable "
            "and well-commented. CSS follows BEM naming where applicable. "
            "HTML should be semantic and accessible."
        ),
        missing=["CONTRIBUTING.md", "SECURITY.md", ".github/PULL_REQUEST_TEMPLATE.md"],
        language="JavaScript",
        package_manager="npm",
    ),
    FlagshipRepo(
        org="organvm-iii-ergon",
        repo="life-my--midst--in",
        default_branch="master",
        stack="pnpm monorepo, Turborepo, Next.js 16, Fastify 5, Vitest 4, TypeScript 5.3",
        description=(
            "Life My Midst In is a full-stack application built as a pnpm "
            "monorepo with Turborepo orchestration. The frontend uses Next.js 16, "
            "the API layer runs Fastify 5, and the test suite uses Vitest 4. "
            "It features JWT authentication, RBAC, Stripe billing, and a "
            "PostgreSQL database (Neon)."
        ),
        setup_instructions="""\
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/life-my--midst--in.git
cd life-my--midst--in

# Install dependencies (pnpm required)
pnpm install

# Set up environment
cp .env.example .env.local
# Edit .env.local with your DATABASE_URL, JWT_SECRET, etc.

# Run database migrations
pnpm --filter api migrate

# Start all packages in development mode
pnpm dev
```""",
        test_command="pnpm test",
        code_style_notes=(
            "TypeScript strict mode is enforced. Use `const` over `let`. "
            "Prefer async/await over raw Promises. Use named exports. "
            "Follow the monorepo package boundaries — changes to shared "
            "packages should be tested across all consumers."
        ),
        missing=["CONTRIBUTING.md", "SECURITY.md"],
        language="TypeScript",
        package_manager="pnpm",
        monorepo=True,
    ),
    FlagshipRepo(
        org="organvm-iv-taxis",
        repo="orchestration-start-here",
        default_branch="main",
        stack="GitHub Actions workflows, Python scripts, YAML configuration",
        description=(
            "Orchestration Start Here is the governance hub of the organvm "
            "system. It contains GitHub Actions workflows for cross-org "
            "orchestration (promotion, distribution, dependency validation, "
            "registry health), Python automation scripts, and seed.yaml "
            "configuration for the system graph."
        ),
        setup_instructions="""\
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/orchestration-start-here.git
cd orchestration-start-here

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Validate workflows locally (optional, requires act)
# act -l
```""",
        test_command="python3 -m pytest tests/ -v",
        code_style_notes=(
            "Python follows PEP 8 with type hints. GitHub Actions workflows "
            "use consistent naming (kebab-case). YAML files should be "
            "well-commented. Scripts should handle errors gracefully and "
            "print clear status messages."
        ),
        missing=["CONTRIBUTING.md", "SECURITY.md", ".github/ISSUE_TEMPLATE/", ".github/PULL_REQUEST_TEMPLATE.md"],
        language="Python",
    ),
    FlagshipRepo(
        org="organvm-iv-taxis",
        repo="agentic-titan",
        default_branch="main",
        stack="Python (AI agent framework, LLM orchestration)",
        description=(
            "Agentic Titan is a Python-based AI agent framework for "
            "LLM orchestration. It provides abstractions for building "
            "autonomous agents that can coordinate tasks, manage context, "
            "and interact with external tools and APIs."
        ),
        setup_instructions="""\
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/agentic-titan.git
cd agentic-titan

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in development mode
pip install -e ".[dev]"
```""",
        test_command="pytest -v",
        code_style_notes=(
            "Follow PEP 8. Use type hints for all function signatures. "
            "Prefer dataclasses or Pydantic for data structures. "
            "Write docstrings for public APIs. Agent interfaces should "
            "be well-documented with usage examples."
        ),
        missing=["CONTRIBUTING.md", "SECURITY.md", ".github/ISSUE_TEMPLATE/", ".github/PULL_REQUEST_TEMPLATE.md"],
        language="Python",
    ),
    FlagshipRepo(
        org="meta-organvm",
        repo="organvm-engine",
        default_branch="main",
        stack="Python (system engine, registry validation, metrics)",
        description=(
            "Organvm Engine is the system engine for the organvm meta-org. "
            "It provides registry validation, metrics calculation, "
            "and system-level tooling that operates across all eight organs. "
            "It reads from repo-registry.json and coordinates cross-org operations."
        ),
        setup_instructions="""\
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/organvm-engine.git
cd organvm-engine

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```""",
        test_command="pytest -v",
        code_style_notes=(
            "Follow PEP 8. Use type hints. Prefer f-strings for formatting. "
            "Scripts should use argparse for CLI interfaces and print clear "
            "status messages. Handle API errors gracefully."
        ),
        missing=[
            "CONTRIBUTING.md", "SECURITY.md", "LICENSE",
            ".github/ISSUE_TEMPLATE/", ".github/PULL_REQUEST_TEMPLATE.md",
        ],
        language="Python",
    ),
    FlagshipRepo(
        org="organvm-v-logos",
        repo="public-process",
        default_branch="main",
        stack="Jekyll blog, Ruby, Markdown essays",
        description=(
            "Public Process is the essay publication platform for the organvm "
            "system. It is a Jekyll blog that hosts essays about building "
            "in public, creative systems, autonomous infrastructure, and "
            "the philosophy behind the eight-organ model. Essays are written "
            "in Markdown with YAML frontmatter."
        ),
        setup_instructions="""\
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/public-process.git
cd public-process

# Install Ruby dependencies
bundle install

# Serve locally
bundle exec jekyll serve

# Site available at http://localhost:4000
```""",
        test_command="bundle exec jekyll build --strict_front_matter",
        code_style_notes=(
            "Essays use Markdown with YAML frontmatter (title, date, categories, "
            "tags, excerpt). Follow the existing essay style: clear prose, "
            "specific examples, honest reflection. Filenames follow Jekyll "
            "convention: YYYY-MM-DD-slug.md in _posts/."
        ),
        missing=["CONTRIBUTING.md", "SECURITY.md", ".github/ISSUE_TEMPLATE/", ".github/PULL_REQUEST_TEMPLATE.md"],
        language="Ruby",
        package_manager="bundler",
    ),
]


# ---------------------------------------------------------------------------
# Template generators
# ---------------------------------------------------------------------------

def generate_contributing(repo: FlagshipRepo) -> str:
    """Generate a repo-specific CONTRIBUTING.md."""
    monorepo_note = ""
    if repo.monorepo:
        monorepo_note = """
### Monorepo Structure

This project is a monorepo managed by Turborepo. Key packages:

- `packages/` — Shared libraries and utilities
- `apps/` — Deployable applications (web, API)

When making changes, consider which package is affected. Run tests across
all packages before submitting a PR to catch cross-package regressions:

```bash
pnpm test
pnpm build
```
"""

    prereqs = {
        "Python": "Python 3.11+",
        "JavaScript": "Node.js 20+ and npm",
        "TypeScript": "Node.js 20+ and pnpm 9+" if repo.package_manager == "pnpm" else "Node.js 20+",
        "Ruby": "Ruby 3.2+ and Bundler",
    }
    prereq = prereqs.get(repo.language, repo.language)

    return f"""# Contributing to {repo.repo}

Thank you for your interest in contributing to this project.

## Overview

{repo.description}

**Stack:** {repo.stack}

## Prerequisites

- Git
- {prereq}
- A GitHub account

## Development Setup

{repo.setup_instructions}

## How to Contribute

### Reporting Issues

- Use GitHub Issues for bug reports and feature requests
- Use the provided issue templates when available
- Include clear reproduction steps for bugs
- For documentation issues, specify which file and section

### Making Changes

1. **Fork** the repository on GitHub
2. **Clone** your fork locally
3. **Create a branch** for your change:
   ```bash
   git checkout -b feat/your-feature-name
   ```
4. **Make your changes** following the code style guidelines below
5. **Test** your changes:
   ```bash
   {repo.test_command}
   ```
6. **Commit** with a clear, imperative-mood message:
   ```bash
   git commit -m "add validation for edge case in parser"
   ```
7. **Push** your branch and open a Pull Request
{monorepo_note}
### Code Style

{repo.code_style_notes}

### Commit Messages

- Use imperative mood: "add feature" not "added feature"
- Keep the title under 72 characters
- Reference issue numbers when applicable: "fix auth bug (#42)"
- Keep commits atomic and focused on a single change

## Pull Request Process

1. Fill out the PR template with a description of your changes
2. Reference any related issues
3. Ensure all CI checks pass
4. Request review from a maintainer
5. Address review feedback promptly

PRs should be focused — one feature or fix per PR. Large changes should be
discussed in an issue first.

## Code of Conduct

Be respectful, constructive, and honest. This project is part of the
[organvm system](https://github.com/{repo.org}), which values transparency
and building in public. We follow the
[Contributor Covenant](https://www.contributor-covenant.org/).

## Questions?

Open an issue on this repository or start a discussion if discussions are
enabled. For system-wide questions, see
[orchestration-start-here](https://github.com/organvm-iv-taxis/orchestration-start-here).
"""


def generate_security(repo: FlagshipRepo) -> str:
    """Generate a standard SECURITY.md."""
    return f"""# Security Policy

## Reporting Security Vulnerabilities

**Please do not report security vulnerabilities through public GitHub issues,
discussions, or pull requests.**

Instead, please use [GitHub Security Advisories](https://github.com/{repo.org}/{repo.repo}/security/advisories/new)
to report vulnerabilities privately. This allows us to assess the risk and
prepare a fix before public disclosure.

If you are unable to use Security Advisories, you may email security concerns
to the repository maintainer directly.

### What to Include

Please include as much of the following information as possible:

- The type of issue (e.g., injection, authentication bypass, data exposure)
- Full paths of source file(s) related to the issue
- The location of the affected source code (tag/branch/commit or direct URL)
- Any special configuration required to reproduce the issue
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

This information helps us triage and resolve the report quickly.

## Response Timeline

- **Acknowledgment:** Within 48 hours of receiving a report
- **Assessment:** Within 1 week of acknowledgment
- **Resolution:** Depends on severity; critical issues are prioritized

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest  | Yes       |

## Security Best Practices for Contributors

1. **Never commit secrets** — API keys, passwords, tokens, or credentials
2. **Validate all inputs** — Sanitize user-supplied data
3. **Keep dependencies updated** — Review and apply security patches promptly
4. **Use HTTPS** — All external resources should be loaded over HTTPS
5. **Follow least privilege** — Request only the permissions you need

## Acknowledgments

We appreciate responsible disclosure and will credit reporters (with permission)
in our release notes.
"""


def generate_bug_report_template() -> str:
    """Generate a bug report issue template."""
    return """---
name: Bug Report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

## Description

A clear and concise description of what the bug is.

## Steps to Reproduce

1. Go to '...'
2. Run '...'
3. See error

## Expected Behavior

A clear and concise description of what you expected to happen.

## Actual Behavior

A clear and concise description of what actually happened.

## Screenshots / Logs

If applicable, add screenshots or error logs to help explain the problem.

## Environment

- OS: [e.g., macOS 15, Ubuntu 24.04, Windows 11]
- Runtime: [e.g., Python 3.12, Node.js 22, Ruby 3.3]
- Browser (if applicable): [e.g., Chrome 130, Firefox 133]

## Additional Context

Add any other context about the problem here.
"""


def generate_feature_request_template() -> str:
    """Generate a feature request issue template."""
    return """---
name: Feature Request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

## Problem Statement

A clear and concise description of the problem or limitation. Example: "I'm always frustrated when [...]"

## Proposed Solution

A clear and concise description of what you want to happen.

## Alternatives Considered

A clear and concise description of any alternative solutions or features you've considered.

## Additional Context

Add any other context, mockups, or screenshots about the feature request here.

## Implementation Notes

If you have ideas about how this could be implemented, share them here.
"""


def generate_pr_template() -> str:
    """Generate a pull request template."""
    return """## Summary

<!-- What does this PR do? Why is it needed? -->

## Changes

<!-- List the key changes made in this PR -->

-

## Related Issues

<!-- Link related issues: Fixes #123, Relates to #456 -->

## Testing

<!-- How did you test these changes? -->

- [ ] Existing tests pass
- [ ] New tests added (if applicable)
- [ ] Manual testing performed

## Checklist

- [ ] Code follows the project's style guidelines
- [ ] Self-review completed
- [ ] Documentation updated (if applicable)
- [ ] No secrets or credentials included
"""


def generate_mit_license() -> str:
    """Generate an MIT LICENSE file."""
    return """MIT License

Copyright (c) 2026 organvm

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


# ---------------------------------------------------------------------------
# GitHub API helpers
# ---------------------------------------------------------------------------

def file_exists_on_github(org: str, repo: str, path: str) -> tuple[bool, str | None]:
    """Check if a file exists on GitHub. Returns (exists, sha_or_none)."""
    result = subprocess.run(
        ["gh", "api", f"repos/{org}/{repo}/contents/{path}"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return False, None
    try:
        data = json.loads(result.stdout)
        if isinstance(data, dict) and "sha" in data:
            return True, data["sha"]
        # Directory listing (array) — directory exists
        if isinstance(data, list):
            return True, None
    except json.JSONDecodeError:
        pass
    return False, None


def deploy_file(
    org: str,
    repo: str,
    path: str,
    content: str,
    message: str,
    branch: str,
    *,
    dry_run: bool = False,
    overwrite: bool = False,
) -> str:
    """Deploy a file to a GitHub repo via the contents API.

    Returns "deployed", "skipped", or "failed".
    """
    exists, sha = file_exists_on_github(org, repo, path)

    if exists and not overwrite:
        print(f"  SKIP {path} (already exists)")
        return "skipped"

    if dry_run:
        print(f"  DRY-RUN would deploy {path} ({len(content)} bytes)")
        return "deployed"

    b64_content = base64.b64encode(content.encode("utf-8")).decode("utf-8")

    payload: dict = {
        "message": message,
        "content": b64_content,
        "branch": branch,
    }
    if exists and sha:
        payload["sha"] = sha

    # Use --input - for ARG_MAX safety (base64 can be large)
    result = subprocess.run(
        ["gh", "api", "-X", "PUT",
         f"repos/{org}/{repo}/contents/{path}",
         "--input", "-"],
        input=json.dumps(payload),
        capture_output=True, text=True,
    )

    if result.returncode != 0:
        err = result.stderr.strip()[:300]
        if '"sha"' in err or "does not match" in err:
            print(f"  FAIL {path}: SHA mismatch (file changed remotely)")
        else:
            print(f"  FAIL {path}: {err}")
        return "failed"

    print(f"  OK   {path}")
    return "deployed"


# ---------------------------------------------------------------------------
# Deployment orchestration
# ---------------------------------------------------------------------------

def _should_deploy(
    file_type: str,
    file_filter: str | None,
    missing: list[str],
    missing_key: str,
) -> bool:
    """Decide whether to deploy a file type based on filter and missing list."""
    # If a filter is set, only deploy that type
    if file_filter and file_filter != file_type:
        return False

    # Check if this file type is in the repo's missing list
    for m in missing:
        if missing_key.rstrip("/") in m.rstrip("/"):
            return True

    return False


def deploy_repo_health_files(
    repo: FlagshipRepo,
    *,
    dry_run: bool = False,
    file_filter: str | None = None,
) -> dict[str, int]:
    """Deploy all missing health files to one flagship repo.

    Returns counts: {"deployed": N, "skipped": N, "failed": N}
    """
    counts = {"deployed": 0, "skipped": 0, "failed": 0}
    org = repo.org
    name = repo.repo
    branch = repo.default_branch

    print(f"\n{'='*60}")
    print(f"  {org}/{name} (branch: {branch})")
    print(f"{'='*60}")

    # Build the file deployment plan
    plan: list[tuple[str, str, str]] = []  # (path, content, commit_message)

    # CONTRIBUTING.md
    if _should_deploy("contributing", file_filter, repo.missing, "CONTRIBUTING.md"):
        plan.append((
            "CONTRIBUTING.md",
            generate_contributing(repo),
            f"docs: add CONTRIBUTING.md with {repo.language} development guide",
        ))

    # SECURITY.md
    if _should_deploy("security", file_filter, repo.missing, "SECURITY.md"):
        plan.append((
            "SECURITY.md",
            generate_security(repo),
            "docs: add SECURITY.md with vulnerability reporting policy",
        ))

    # LICENSE (only for repos that need it)
    if _should_deploy("license", file_filter, repo.missing, "LICENSE"):
        plan.append((
            "LICENSE",
            generate_mit_license(),
            "docs: add MIT LICENSE",
        ))

    # Issue templates
    if _should_deploy("issues", file_filter, repo.missing, ".github/ISSUE_TEMPLATE/"):
        plan.append((
            ".github/ISSUE_TEMPLATE/bug_report.md",
            generate_bug_report_template(),
            "docs: add bug report issue template",
        ))
        plan.append((
            ".github/ISSUE_TEMPLATE/feature_request.md",
            generate_feature_request_template(),
            "docs: add feature request issue template",
        ))

    # PR template
    if _should_deploy("pr", file_filter, repo.missing, ".github/PULL_REQUEST_TEMPLATE.md"):
        plan.append((
            ".github/PULL_REQUEST_TEMPLATE.md",
            generate_pr_template(),
            "docs: add pull request template",
        ))

    if not plan:
        print("  Nothing to deploy for this repo.")
        return counts

    # Deploy each file
    for path, content, message in plan:
        result = deploy_file(
            org, name, path, content, message, branch, dry_run=dry_run,
        )
        counts[result] += 1

        # Rate-limit: 0.5s between API calls to avoid secondary rate limits
        if not dry_run:
            time.sleep(0.5)

    return counts


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Deploy community health files to flagship repos",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be deployed without making changes",
    )
    parser.add_argument(
        "--repo",
        type=str,
        default=None,
        help="Deploy to a single repo only (match by repo name, e.g. 'agentic-titan')",
    )
    parser.add_argument(
        "--file",
        type=str,
        choices=["contributing", "security", "issues", "pr", "license"],
        default=None,
        help="Deploy only one file type",
    )
    args = parser.parse_args()

    # Verify gh CLI is available and authenticated
    result = subprocess.run(
        ["gh", "auth", "status"], capture_output=True, text=True,
    )
    if result.returncode != 0:
        print("ERROR: gh CLI is not authenticated. Run 'gh auth login' first.",
              file=sys.stderr)
        sys.exit(1)

    print("Flagship Health File Deployment")
    print("=" * 60)
    if args.dry_run:
        print("MODE: DRY RUN (no changes will be made)")
    if args.repo:
        print(f"FILTER: repo={args.repo}")
    if args.file:
        print(f"FILTER: file={args.file}")

    # Filter repos if --repo is specified
    targets = FLAGSHIPS
    if args.repo:
        targets = [r for r in FLAGSHIPS if args.repo in r.repo]
        if not targets:
            print(f"\nERROR: No flagship repo matches '{args.repo}'",
                  file=sys.stderr)
            print("Available repos:", file=sys.stderr)
            for r in FLAGSHIPS:
                print(f"  - {r.org}/{r.repo}", file=sys.stderr)
            sys.exit(1)

    # Deploy to each target repo
    totals = {"deployed": 0, "skipped": 0, "failed": 0}
    for repo in targets:
        counts = deploy_repo_health_files(
            repo, dry_run=args.dry_run, file_filter=args.file,
        )
        for k in totals:
            totals[k] += counts[k]

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"  Deployed: {totals['deployed']}")
    print(f"  Skipped:  {totals['skipped']}")
    print(f"  Failed:   {totals['failed']}")

    if totals["failed"] > 0:
        print("\nSome deployments failed. Check the output above for details.")
        sys.exit(1)
    elif totals["deployed"] == 0 and totals["skipped"] > 0:
        print("\nAll files already exist. Nothing to deploy.")
    else:
        print("\nAll deployments completed successfully.")


if __name__ == "__main__":
    main()
