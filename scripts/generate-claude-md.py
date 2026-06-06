#!/usr/bin/env python3
"""Generate CLAUDE.md files for repos that don't have one yet.

Reads repo-registry.json, fetches each repo's README and directory tree via
GitHub API, then generates a tiered CLAUDE.md appropriate to the repo's
type and significance.

Tiers:
  - flagship:      Full context (architecture, key files, build, test, conventions)
  - standard-code: Medium context (what it does, key dirs, build/test)
  - standard-doc:  Light context (what it contains, navigation)

Usage:
    python3 scripts/generate-claude-md.py                  # dry-run
    python3 scripts/generate-claude-md.py --push           # push via gh api
    python3 scripts/generate-claude-md.py --only ORG/REPO  # single repo
    python3 scripts/generate-claude-md.py --list-missing   # just show missing
"""

import argparse
import base64
import json
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "repo-registry.json"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# ── Organ metadata ──────────────────────────────────────────
ORGAN_MAP = {
    "ORGAN-I":      ("I",    "Theory",        "theoria",    "organvm-i-theoria"),
    "ORGAN-II":     ("II",   "Art",           "poiesis",    "organvm-ii-poiesis"),
    "ORGAN-III":    ("III",  "Commerce",      "ergon",      "organvm-iii-ergon"),
    "ORGAN-IV":     ("IV",   "Orchestration", "taxis",      "organvm-iv-taxis"),
    "ORGAN-V":      ("V",    "Public Process","logos",      "organvm-v-logos"),
    "ORGAN-VI":     ("VI",   "Community",     "koinonia",   "organvm-vi-koinonia"),
    "ORGAN-VII":    ("VII",  "Marketing",     "kerygma",    "organvm-vii-kerygma"),
    "META-ORGANVM": ("Meta", "Meta",          "meta-organvm", "meta-organvm"),
}

# Flagship repos get the richest CLAUDE.md
FLAGSHIPS = {
    "recursive-engine--generative-entity",
    "metasystem-master",
    "a-mavs-olevm",
    "public-record-data-scrapper",
    "life-my--midst--in",
    "orchestration-start-here",
    "agentic-titan",
    "organvm-engine",
    "public-process",
}

# File extensions that indicate code repos (vs doc/art repos)
CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".rs", ".go", ".java",
    ".rb", ".php", ".c", ".cpp", ".h", ".swift", ".kt",
    ".vue", ".svelte", ".astro",
}

# ── GitHub API helpers ──────────────────────────────────────

def gh_api(endpoint, method="GET", jq=None):
    """Call gh api and return stdout. Returns None on error."""
    cmd = ["gh", "api", endpoint]
    if method != "GET":
        cmd.extend(["-X", method])
    if jq:
        cmd.extend(["--jq", jq])
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def get_readme(org, repo):
    """Fetch decoded README content."""
    raw = gh_api(f"repos/{org}/{repo}/readme", jq=".content")
    if not raw:
        return ""
    try:
        return base64.b64decode(raw).decode("utf-8", errors="replace")
    except Exception:
        return ""


def get_tree(org, repo, depth=2):
    """Fetch directory tree (top-level + one level deep for key dirs)."""
    contents = gh_api(f"repos/{org}/{repo}/contents", jq='[.[] | {name, type}]')
    if not contents:
        return []
    try:
        items = json.loads(contents)
    except json.JSONDecodeError:
        return []

    tree = []
    for item in items:
        name = item.get("name", "")
        itype = item.get("type", "")
        tree.append({"name": name, "type": itype, "children": []})

        # Go one level deeper for key directories
        if itype == "dir" and name in ("src", "lib", "packages", "apps", "tests", "test",
                                        "scripts", "docs", "components", "pages", "api",
                                        "server", "client", "core", "config"):
            sub = gh_api(f"repos/{org}/{repo}/contents/{name}", jq='[.[] | {name, type}]')
            if sub:
                try:
                    children = json.loads(sub)
                    tree[-1]["children"] = [c.get("name", "") for c in children[:20]]
                except json.JSONDecodeError:
                    pass
    return tree


def get_languages(org, repo):
    """Fetch language breakdown."""
    raw = gh_api(f"repos/{org}/{repo}/languages")
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def get_default_branch(org, repo):
    """Get the default branch name."""
    raw = gh_api(f"repos/{org}/{repo}", jq=".default_branch")
    return raw or "main"


def push_file(org, repo, path, content, message, branch=None):
    """Push a file via gh api PUT."""
    b64 = base64.b64encode(content.encode()).decode()

    # Check if file exists (get SHA for update)
    existing = gh_api(f"repos/{org}/{repo}/contents/{path}", jq=".sha")

    payload = {
        "message": message,
        "content": b64,
    }
    if branch:
        payload["branch"] = branch
    if existing:
        payload["sha"] = existing

    payload_json = json.dumps(payload)
    cmd = [
        "gh", "api", f"repos/{org}/{repo}/contents/{path}",
        "-X", "PUT", "--input", "-"
    ]
    result = subprocess.run(cmd, input=payload_json, capture_output=True, text=True, timeout=30)
    return result.returncode == 0


# ── CLAUDE.md Generation ───────────────────────────────────

def detect_repo_type(tree, languages):
    """Determine if this is a code repo, doc repo, or art repo."""
    code_dirs = {"src", "lib", "packages", "apps", "server", "client", "api", "core", "components"}
    doc_dirs = {"docs", "_posts", "content", "articles", "posts"}

    has_code_dir = any(item["name"] in code_dirs for item in tree if item["type"] == "dir")
    has_doc_dir = any(item["name"] in doc_dirs for item in tree if item["type"] == "dir")

    code_bytes = sum(v for k, v in languages.items()
                     if k.lower() not in ("markdown", "html", "css", "scss", "dockerfile"))
    total_bytes = sum(languages.values()) if languages else 1

    if code_bytes / max(total_bytes, 1) > 0.3 or has_code_dir:
        return "code"
    elif has_doc_dir:
        return "doc"
    else:
        return "mixed"


def format_tree_section(tree):
    """Format directory tree as markdown."""
    lines = ["```"]
    for item in sorted(tree, key=lambda x: (x["type"] != "dir", x["name"])):
        prefix = "📁" if item["type"] == "dir" else "📄"
        lines.append(f"{prefix} {item['name']}/") if item["type"] == "dir" else lines.append(f"  {item['name']}")
        for child in item.get("children", [])[:10]:
            lines.append(f"    {child}")
        if len(item.get("children", [])) > 10:
            lines.append(f"    ... ({len(item['children'])} items)")
    lines.append("```")
    return "\n".join(lines)


def extract_description(readme):
    """Extract first meaningful paragraph from README."""
    lines = readme.split("\n")
    collecting = False
    paragraph = []

    for line in lines:
        stripped = line.strip()

        # Skip badges, images, links-only lines
        if stripped.startswith("![") or stripped.startswith("[![") or stripped.startswith("<img"):
            continue
        if stripped.startswith("#"):
            if collecting and paragraph:
                break
            collecting = True
            continue
        if not stripped:
            if collecting and paragraph:
                break
            continue
        if collecting or not any(line.startswith(c) for c in ("#", "!", "<", "[")):
            paragraph.append(stripped)
            collecting = True

    return " ".join(paragraph[:5]) if paragraph else ""


def detect_build_system(tree):
    """Detect build/package system from files present."""
    files = {item["name"] for item in tree}
    systems = []

    if "package.json" in files:
        if "pnpm-lock.yaml" in files or "pnpm-workspace.yaml" in files:
            systems.append("pnpm")
        elif "yarn.lock" in files:
            systems.append("yarn")
        else:
            systems.append("npm")
    if "pyproject.toml" in files or "setup.py" in files:
        systems.append("Python (pip/setuptools)")
    if "Cargo.toml" in files:
        systems.append("Rust (cargo)")
    if "go.mod" in files:
        systems.append("Go")
    if "Gemfile" in files:
        systems.append("Ruby (bundler)")
    if "Makefile" in files or "makefile" in files:
        systems.append("Make")
    if "Dockerfile" in files or "docker-compose.yml" in files:
        systems.append("Docker")
    if "turbo.json" in files:
        systems.append("Turborepo")

    return systems


def detect_test_framework(tree, languages):
    """Detect testing setup."""
    files = {item["name"] for item in tree}
    dirs = {item["name"] for item in tree if item["type"] == "dir"}

    frameworks = []
    if "vitest.config.ts" in files or "vitest.config.js" in files:
        frameworks.append("Vitest")
    if "jest.config.js" in files or "jest.config.ts" in files:
        frameworks.append("Jest")
    if "pytest.ini" in files or "conftest.py" in files:
        frameworks.append("pytest")
    if any(d in dirs for d in ("tests", "test", "__tests__", "spec")):
        if not frameworks:
            if "Python" in languages:
                frameworks.append("pytest (likely)")
            elif any(lang in languages for lang in ("TypeScript", "JavaScript")):
                frameworks.append("Node test runner (likely)")

    return frameworks


def generate_claude_md(org, repo, organ_key, repo_meta, readme, tree, languages, branch):
    """Generate CLAUDE.md content."""
    name = repo_meta.get("name", repo)
    description = repo_meta.get("description", "") or extract_description(readme)
    status = repo_meta.get("implementation_status", repo_meta.get("status", "ACTIVE"))
    portfolio_relevance = repo_meta.get("portfolio_relevance", "MEDIUM")
    is_flagship = repo in FLAGSHIPS

    organ_num, organ_name, _, _ = ORGAN_MAP.get(organ_key, ("?", "Unknown", "", ""))
    repo_type = detect_repo_type(tree, languages)
    build_systems = detect_build_system(tree)
    test_frameworks = detect_test_framework(tree, languages)

    # Primary languages (by bytes, top 3)
    sorted_langs = sorted(languages.items(), key=lambda x: -x[1])[:3]
    lang_str = ", ".join(f"{k}" for k, v in sorted_langs) if sorted_langs else "Not detected"

    sections = []

    # Header
    sections.append(f"# CLAUDE.md — {name}\n")
    sections.append(f"**ORGAN {organ_num}** ({organ_name}) · `{org}/{repo}`")
    sections.append(f"**Status:** {status} · **Branch:** `{branch}`")
    sections.append("")

    # What This Repo Is
    sections.append("## What This Repo Is\n")
    if description:
        sections.append(description)
    sections.append("")

    # Languages & Stack
    if languages:
        sections.append("## Stack\n")
        sections.append(f"**Languages:** {lang_str}")
        if build_systems:
            sections.append(f"**Build:** {', '.join(build_systems)}")
        if test_frameworks:
            sections.append(f"**Testing:** {', '.join(test_frameworks)}")
        sections.append("")

    # Directory Structure (for code repos and flagships)
    if tree and (repo_type == "code" or is_flagship):
        sections.append("## Directory Structure\n")
        sections.append(format_tree_section(tree))
        sections.append("")

    # Key Files (for code repos)
    if repo_type == "code" or is_flagship:
        key_files = []
        file_names = {item["name"] for item in tree}
        if "README.md" in file_names:
            key_files.append("- `README.md` — Project documentation")
        if "package.json" in file_names:
            key_files.append("- `package.json` — Dependencies and scripts")
        if "pyproject.toml" in file_names:
            key_files.append("- `pyproject.toml` — Python project config")
        if "seed.yaml" in file_names:
            key_files.append("- `seed.yaml` — ORGANVM orchestration metadata")
        if any(item["name"] in ("src", "lib", "core") and item["type"] == "dir" for item in tree):
            src_dir = next(item["name"] for item in tree
                         if item["name"] in ("src", "lib", "core") and item["type"] == "dir")
            key_files.append(f"- `{src_dir}/` — Main source code")
        if any(item["name"] in ("tests", "test", "__tests__") and item["type"] == "dir" for item in tree):
            test_dir = next(item["name"] for item in tree
                          if item["name"] in ("tests", "test", "__tests__") and item["type"] == "dir")
            key_files.append(f"- `{test_dir}/` — Test suite")

        if key_files:
            sections.append("## Key Files\n")
            sections.append("\n".join(key_files))
            sections.append("")

    # Development (for code repos)
    if build_systems and (repo_type == "code" or is_flagship):
        sections.append("## Development\n")
        if "pnpm" in build_systems:
            sections.append("```bash")
            sections.append("pnpm install    # Install dependencies")
            sections.append("pnpm build      # Build all packages")
            sections.append("pnpm test       # Run tests")
            sections.append("pnpm dev        # Start development server")
            sections.append("```")
        elif "npm" in build_systems:
            sections.append("```bash")
            sections.append("npm install     # Install dependencies")
            sections.append("npm run build   # Build")
            sections.append("npm test        # Run tests")
            sections.append("```")
        elif "Python (pip/setuptools)" in build_systems:
            sections.append("```bash")
            sections.append("pip install -e .    # Install in development mode")
            sections.append("pytest              # Run tests")
            sections.append("```")
        elif "Ruby (bundler)" in build_systems:
            sections.append("```bash")
            sections.append("bundle install  # Install dependencies")
            sections.append("bundle exec jekyll serve  # Local server (if Jekyll)")
            sections.append("```")
        elif "Rust (cargo)" in build_systems:
            sections.append("```bash")
            sections.append("cargo build     # Build")
            sections.append("cargo test      # Run tests")
            sections.append("```")
        sections.append("")

    # ORGANVM Context
    sections.append("## ORGANVM Context\n")
    sections.append(f"This repository is part of the **ORGANVM** eight-organ creative-institutional system.")
    sections.append(f"It belongs to **ORGAN {organ_num} ({organ_name})** under the `{org}` GitHub organization.")
    sections.append("")

    deps = repo_meta.get("dependencies", [])
    if deps:
        sections.append("**Dependencies:**")
        for dep in deps:
            if isinstance(dep, str):
                sections.append(f"- {dep}")
            elif isinstance(dep, dict):
                sections.append(f"- {dep.get('name', dep.get('repo', 'unknown'))}")
        sections.append("")

    # Registry reference
    sections.append(f"**Registry:** [`repo-registry.json`](https://github.com/meta-organvm/organvm-corpvs-testamentvm/blob/main/repo-registry.json)")
    sections.append(f"**Corpus:** [`organvm-corpvs-testamentvm`](https://github.com/meta-organvm/organvm-corpvs-testamentvm)")
    sections.append("")

    return "\n".join(sections)


# ── Main ────────────────────────────────────────────────────

# ISOTOPE DISSOLUTION: Gate memory--remember G2 (CORPUS_SCRIPTS_DISSOLVED)
try:
    from organvm_engine.registry.loader import load_registry as _engine_load
except ImportError:
    _engine_load = None


def load_registry():
    """Load and parse repo-registry.json."""
    if _engine_load is not None:
        return _engine_load(REGISTRY)
    with open(REGISTRY) as f:
        return json.load(f)


def iter_repos(registry):
    """Yield (organ_key, org, repo_name, repo_meta) for each non-archived repo."""
    for organ_key, organ in registry["organs"].items():
        for repo in organ.get("repositories", []):
            status = repo.get("implementation_status", repo.get("status", ""))
            name = repo.get("name", "")
            org = repo.get("org", "")
            if status == "ARCHIVED" or name == ".github":
                continue
            yield organ_key, org, name, repo


def main():
    parser = argparse.ArgumentParser(description="Generate CLAUDE.md for repos missing one")
    parser.add_argument("--push", action="store_true", help="Push via gh api")
    parser.add_argument("--only", type=str, help="Only process ORG/REPO")
    parser.add_argument("--list-missing", action="store_true", help="Just list missing repos")
    parser.add_argument("--staging-dir", type=str, default=None,
                        help="Write generated files to this directory instead of pushing")
    args = parser.parse_args()

    registry = load_registry()
    missing = []
    generated = []
    errors = []

    # Phase 1: Find missing repos
    print("Scanning repos for CLAUDE.md...\n")
    for organ_key, org, name, repo_meta in iter_repos(registry):
        full = f"{org}/{name}"
        if args.only and full != args.only:
            continue

        existing = gh_api(f"repos/{org}/{name}/contents/CLAUDE.md", jq=".sha")
        if existing:
            continue
        missing.append((organ_key, org, name, repo_meta))

    print(f"Found {len(missing)} repos missing CLAUDE.md\n")

    if args.list_missing:
        for _, org, name, _ in sorted(missing, key=lambda x: f"{x[1]}/{x[2]}"):
            print(f"  {org}/{name}")
        return

    # Phase 2: Generate and optionally push
    for i, (organ_key, org, name, repo_meta) in enumerate(missing, 1):
        full = f"{org}/{name}"
        print(f"[{i}/{len(missing)}] {full}...", end=" ", flush=True)

        try:
            readme = get_readme(org, name)
            tree = get_tree(org, name)
            languages = get_languages(org, name)
            branch = get_default_branch(org, name)

            content = generate_claude_md(org, name, organ_key, repo_meta,
                                         readme, tree, languages, branch)

            if args.staging_dir:
                staging = Path(args.staging_dir)
                staging.mkdir(parents=True, exist_ok=True)
                out_path = staging / f"{org}__{name}__CLAUDE.md"
                out_path.write_text(content)
                print(f"staged → {out_path.name}")
                generated.append(full)
            elif args.push:
                ok = push_file(org, name, "CLAUDE.md", content,
                              "docs: add CLAUDE.md for AI-augmented workflow context",
                              branch)
                if ok:
                    print("✓ pushed")
                    generated.append(full)
                else:
                    print("✗ push failed")
                    errors.append(full)
            else:
                print(f"generated ({len(content)} chars)")
                generated.append(full)

        except Exception as e:
            print(f"✗ error: {e}")
            errors.append(full)

    # Summary
    print(f"\n{'─' * 50}")
    print(f"Generated: {len(generated)}")
    print(f"Errors:    {len(errors)}")
    if errors:
        print("\nFailed repos:")
        for e in errors:
            print(f"  {e}")


if __name__ == "__main__":
    main()
