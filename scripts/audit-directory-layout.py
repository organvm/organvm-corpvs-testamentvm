#!/usr/bin/env python3
"""Conformance auditor for standard #26 (internal directory layout).

Encodes docs/standards/26-internal-directory-layout--monorepo-feature-organization.md
as executable checks. Scans git repos under given roots, scores each against #26,
and reports violations. This is the GENERATIVE universal-implementation mechanism:
the standard is the rule; every repo's conformance derives from running this.

Usage:
    audit-directory-layout.py [ROOT ...]        # human report
    audit-directory-layout.py --json [ROOT ...] # machine-readable
    audit-directory-layout.py --repo PATH       # single repo

Defaults to scanning ~/Workspace/* org dirs and a curated ~/Code set.
Read-only: never modifies a repo.
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path

HOME = Path.home()
TYPE_FOLDER_SMELLS = {"components", "services", "utils", "helpers", "hooks", "models"}
REQUIRED_ROOT = ["README.md", "LICENSE"]
MAX_NESTING = 3  # under src/, per #26 §4


def is_git_repo(p: Path) -> bool:
    return (p / ".git").exists()


def find_repos(roots: list[Path]) -> list[Path]:
    repos: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        if is_git_repo(root):
            repos.append(root)
            continue
        for child in sorted(root.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            if is_git_repo(child):
                repos.append(child)
            else:  # one more level (org-dir/repo)
                for gchild in sorted(child.iterdir()):
                    if gchild.is_dir() and is_git_repo(gchild):
                        repos.append(gchild)
    return repos


def max_depth(base: Path, limit: int = 8) -> int:
    """Deepest directory depth under base (dirs only), capped for speed."""
    best = 0
    for dirpath, dirnames, _ in os.walk(base):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d != "node_modules"]
        depth = len(Path(dirpath).relative_to(base).parts)
        best = max(best, depth)
        if best >= limit:
            break
    return best


def classify_layout(repo: Path) -> str:
    has_apps = (repo / "apps").is_dir()
    has_pkgs = (repo / "packages").is_dir() or (repo / "libs").is_dir()
    if has_apps and has_pkgs:
        return "monorepo"
    if (repo / "src").is_dir():
        return "src"
    # language-equivalent importable homes
    if (repo / "cmd").is_dir() or list(repo.glob("*.go")):
        return "go"
    if (repo / "crates").is_dir():
        return "rust-workspace"
    return "flat"


def audit_repo(repo: Path) -> dict:
    violations: list[str] = []
    notes: list[str] = []
    root_entries = [e for e in repo.iterdir() if not e.name.startswith(".")]
    root_files = [e for e in root_entries if e.is_file()]
    layout = classify_layout(repo)
    is_code = any((repo / m).exists() for m in
                  ("package.json", "pyproject.toml", "go.mod", "Cargo.toml", "setup.py"))

    # §2/§9 required root files
    for req in REQUIRED_ROOT:
        if not (repo / req).exists():
            violations.append(f"missing root {req}")

    # §8 root file-count trigger (>25 -> consolidate; #10 target <20 for code)
    if is_code and len(root_files) > 20:
        violations.append(f"root file count {len(root_files)} >20 (consolidate; §8)")

    # §2 importable code home for code repos
    if is_code and layout == "flat":
        notes.append("flat layout on a code repo — justify or move to src/ (§2)")

    # §4 type-folder smell as direct child of src/ or root
    for base in (repo, repo / "src"):
        if base.is_dir():
            smells = {d.name for d in base.iterdir() if d.is_dir()} & TYPE_FOLDER_SMELLS
            if smells:
                child_count = sum(1 for _ in (base).iterdir())
                if "components" in smells:
                    comp = base / "components"
                    n = sum(1 for _ in comp.iterdir()) if comp.is_dir() else 0
                    if n > 20:
                        violations.append(f"{comp.relative_to(repo)}/ has {n} entries >20 — switch to feature folders (§4/§8)")
                    else:
                        notes.append(f"type-folder(s) {sorted(smells)} under {base.name or '.'} — prefer feature folders (§4)")
                else:
                    notes.append(f"type-folder(s) {sorted(smells)} under {base.name or '.'} — prefer feature folders (§4)")

    # §4 nesting depth under src/
    src = repo / "src"
    if src.is_dir():
        d = max_depth(src)
        if d > MAX_NESTING:
            violations.append(f"src/ nesting depth {d} >{MAX_NESTING} (§4)")

    # §6 branch-per-environment smell (heuristic: env-named dirs are fine; can't see branches here)
    if (repo / "environments").is_dir() or (repo / "envs").is_dir() or (repo / "overlays").is_dir():
        notes.append("directory-per-environment present (§6 compliant)")

    score = max(0, 100 - 25 * len(violations) - 5 * len(notes))
    return {
        "repo": str(repo.relative_to(HOME)),
        "layout": layout,
        "is_code": is_code,
        "root_files": len(root_files),
        "violations": violations,
        "notes": notes,
        "score": score,
    }


def default_roots() -> list[Path]:
    roots = [HOME / "Workspace"]
    code = HOME / "Code"
    # curated code repos that are real projects (skip _underscore infra + archives)
    for name in ("agent-runtime", "speech-score-engine", "organvm",
                 "persona-fleet", "machina-mundi-canonici"):
        p = code / name
        if p.exists():
            roots.append(p)
    return roots


def main() -> int:
    args = sys.argv[1:]
    as_json = "--json" in args
    args = [a for a in args if a != "--json"]
    if args and args[0] == "--repo":
        repos = [Path(args[1]).expanduser()]
    elif args:
        repos = find_repos([Path(a).expanduser() for a in args])
    else:
        repos = find_repos(default_roots())

    results = [audit_repo(r) for r in repos]
    results.sort(key=lambda x: x["score"])

    if as_json:
        print(json.dumps(results, indent=2))
        return 0

    n = len(results)
    clean = sum(1 for r in results if not r["violations"])
    print(f"# Standard #26 conformance — {n} repos scanned\n")
    print(f"Clean (no violations): {clean}/{n}\n")
    for r in results:
        flag = "OK " if not r["violations"] else "!! "
        print(f"{flag}[{r['score']:3d}] {r['repo']}  ({r['layout']}, {r['root_files']} root files)")
        for v in r["violations"]:
            print(f"      ✗ {v}")
        for note in r["notes"][:3]:
            print(f"      · {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
