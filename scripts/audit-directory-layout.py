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
README_VARIANTS = ["README.md", "README.rst", "README.txt", "readme.md", "README"]
LICENSE_VARIANTS = ["LICENSE", "LICENSE.md", "LICENSE.txt", "LICENSE.rst",
                    "COPYING", "COPYING.md", "LICENCE", "LICENCE.md"]
MAX_NESTING = 4  # package-relative; #26 §4 says "~3" — 4 (pkg/sub/sub/leaf) is within tolerance, 5+ is the smell
# known contrib/upstream clones — not our original work, forked into our orgs.
# Identity-based exemption (owner-based misses forks cloned into first-party orgs).
VENDORED_NAMES = {"fastmcp", "python-sdk", "openai-agents-contrib", "openai-agents",
                  "openai-python", "anthropic-sdk-python", "mcp"}
# first-party owners — repos whose origin is NOT one of these are vendored/forked
FIRST_PARTY_OWNERS = {"a-organvm", "4444j99", "meta-organvm", "organvm",
                      "organvm-i-theoria", "organvm-ii-poiesis", "organvm-iii-ergon",
                      "organvm-iv-taxis", "organvm-v-logos", "organvm-vi-koinonia",
                      "organvm-vii-kerygma", "ivviiviivvi"}


def has_any(repo: Path, names: list[str]) -> bool:
    return any((repo / n).exists() for n in names)


# files legitimately expected at root — NOT clutter (#10 mandates health/identity here)
_CANON_EXACT = {
    "readme.md", "readme.rst", "readme.txt", "readme", "license", "license.md",
    "license.txt", "copying", "changelog.md", "changelog", "contributing.md",
    "code_of_conduct.md", "security.md", "support.md", "maintainers.md",
    "governance.md", "codeowners", "claude.md", "agents.md", "gemini.md",
    "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
    "pnpm-workspace.yaml", "requirements.txt", "pyproject.toml", "setup.py",
    "setup.cfg", "uv.lock", "poetry.lock", "cargo.toml", "cargo.lock", "go.mod",
    "go.sum", "gemfile", "gemfile.lock", "dockerfile", "makefile", "components.json",
    "index.html", "next-env.d.ts", "app.json", "vercel.json", "render.yaml",
    "netlify.toml", "turbo.json", "nx.json", "instance.toml", "version",
    # organvm system declarations
    "ecosystem.yaml", "seed.yaml", "network-map.yaml",
}


def is_canonical_root(name: str) -> bool:
    n = name.lower()
    if n in _CANON_EXACT:
        return True
    # config/manifest/lock patterns expected at root
    if n.endswith((".config.js", ".config.ts", ".config.mjs", ".config.cjs",
                   ".config.json", ".config.yaml")):
        return True
    if n.startswith("tsconfig") and n.endswith(".json"):
        return True
    if n.startswith("docker-compose") or n.startswith(".env"):
        return True
    return False


def origin_owner(repo: Path) -> str | None:
    """Parse the origin remote owner from .git/config without shelling out."""
    cfg = repo / ".git" / "config"
    if not cfg.is_file():
        return None
    try:
        text = cfg.read_text(errors="ignore")
    except OSError:
        return None
    in_origin = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("[remote "):
            in_origin = 'origin"' in s
        elif in_origin and s.startswith("url"):
            url = s.split("=", 1)[1].strip()
            # git@github.com:OWNER/repo.git  OR  https://github.com/OWNER/repo
            if ":" in url and "@" in url:
                tail = url.split(":", 1)[1]
            else:
                tail = url.split("github.com/", 1)[-1]
            owner = tail.split("/", 1)[0] if "/" in tail else ""
            return owner.lower()
    return None


def is_vendored(repo: Path) -> bool:
    if repo.name.lower() in VENDORED_NAMES:
        return True
    owner = origin_owner(repo)
    return owner is not None and owner not in FIRST_PARTY_OWNERS


def is_archive(repo: Path) -> bool:
    n = repo.name.lower()
    return ".archive" in n or n.startswith(".archive") or "archived" in n


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


PRUNE_DIRS = {"node_modules", "__pycache__", ".venv", "venv", "dist", "build",
              ".next", ".nuxt", "target", ".gradle", "Pods", "vendor", "coverage",
              # native-mobile trees impose deep reverse-domain paths (framework-like)
              "android", "ios"}


def max_depth(base: Path, limit: int = 8) -> int:
    """Deepest directory depth under base (dirs only), capped for speed.

    Prunes build caches and native-mobile trees — their depth is tooling/framework
    imposed, not authored structure (#26 §4 framework exemption applies)."""
    best = 0
    for dirpath, dirnames, _ in os.walk(base):
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in PRUNE_DIRS]
        depth = len(Path(dirpath).relative_to(base).parts)
        best = max(best, depth)
        if best >= limit:
            break
    return best


def detect_framework(repo: Path) -> str | None:
    """Frameworks that IMPOSE directory structure (#26 §4 exemption).

    Their mandated nesting (e.g. Next.js src/app/<route>/...) and idiomatic
    type-folders (src/components/) are NOT violations.
    """
    if list(repo.glob("next.config.*")) or (repo / "next-env.d.ts").exists():
        return "nextjs"
    if list(repo.glob("svelte.config.*")):
        return "sveltekit"
    if list(repo.glob("nuxt.config.*")):
        return "nuxt"
    if list(repo.glob("remix.config.*")):
        return "remix"
    # expo / react-native — app.json at root or under src/* (monorepo)
    if (repo / "app.json").exists() or list(repo.glob("src/*/app.json")):
        return "expo"
    # NESTED framework apps in a monorepo: src/<thing>/next.config.* or src/<thing>/app/
    if list(repo.glob("src/*/next.config.*")) or list(repo.glob("src/*/app")):
        return "nextjs-monorepo"
    return None


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
    framework = detect_framework(repo)
    vendored = is_vendored(repo)
    archive = is_archive(repo)
    is_code = any((repo / m).exists() for m in
                  ("package.json", "pyproject.toml", "go.mod", "Cargo.toml", "setup.py"))

    # Vendored/forked or archived repos are EXEMPT from #26 (upstream owns their
    # structure/license; archives are frozen). Report, don't flag.
    if vendored or archive:
        kind = "vendored/fork" if vendored else "archive"
        return {
            "repo": str(repo.relative_to(HOME)), "layout": layout,
            "framework": framework, "is_code": is_code,
            "root_files": len(root_files), "violations": [],
            "notes": [f"EXEMPT ({kind}) — #26 does not apply"], "score": 100,
            "exempt": kind,
        }

    # §2/§9 required root files (variant-aware)
    if not has_any(repo, README_VARIANTS):
        violations.append("missing root README.md")
    if not has_any(repo, LICENSE_VARIANTS):
        violations.append("missing root LICENSE")

    # §8 root file-count: #26 §8 ACTION trigger is >25 (consolidate); #10 <20 is a
    # softer target -> advisory note in the 21-25 band. Declaration/data repos whose
    # files ARE the content (#10 §2 carve-out) are exempt: >10 root .yaml/.yml decls.
    yaml_decls = sum(1 for e in root_files if e.suffix.lower() in (".yaml", ".yml"))
    is_declaration_repo = yaml_decls > 10 and not (repo / "src").is_dir()
    # static multi-page site: PWA markers; its root .html pages ARE content (app structure)
    html_pages = sum(1 for e in root_files if e.suffix.lower() == ".html")
    is_static_site = (repo / "manifest.json").exists() and (repo / "sw.js").exists() and html_pages >= 2
    if is_static_site:
        notes.append(f"static multi-page site ({html_pages} root .html pages) — root .html is content")
    # Root clutter = DISCRETIONARY files only. #10 MANDATES health/identity files at root,
    # so counting them as "consolidate" clutter is self-contradictory. Standard manifests,
    # configs, framework entries and organvm declarations are also expected, not clutter.
    if is_code and not is_declaration_repo and not is_static_site:
        discretionary = [e for e in root_files if not is_canonical_root(e.name)]
        if len(discretionary) > 10:
            names = ", ".join(sorted(e.name for e in discretionary)[:6])
            violations.append(f"{len(discretionary)} discretionary root files >10 — relocate (§8): {names}…")
        elif len(discretionary) > 6:
            notes.append(f"{len(discretionary)} discretionary root files (>6; §8 watch)")
    elif is_declaration_repo:
        notes.append(f"declaration/data repo ({yaml_decls} root YAML decls) — #10 §2 content carve-out")

    # §2 importable code home for code repos
    if is_code and layout == "flat":
        notes.append("flat layout on a code repo — justify or move to src/ (§2)")

    # §4 type-folder smell as direct child of src/ or root
    for base in (repo, repo / "src"):
        if base.is_dir():
            smells = {d.name for d in base.iterdir() if d.is_dir()} & TYPE_FOLDER_SMELLS
            if smells:
                sum(1 for _ in (base).iterdir())
                if "components" in smells:
                    comp = base / "components"
                    # count DISTINCT flat components: exclude colocated tests/specs/stories
                    # (#26 §4 ENDORSES colocation) and exclude files already in subdirs.
                    flat = set()
                    if comp.is_dir():
                        for e in comp.iterdir():
                            if e.is_file() and e.suffix in (".tsx", ".ts", ".jsx", ".js", ".vue", ".svelte"):
                                stem = e.name
                                for marker in (".test.", ".spec.", ".stories."):
                                    if marker in stem:
                                        stem = None
                                        break
                                if stem and not stem.startswith("index."):
                                    flat.add(e.stem.split(".")[0])
                    n = len(flat)
                    # "~20" (§8): hard trigger when clearly exceeded (>25), advisory 21-25
                    if n > 25:
                        violations.append(f"{comp.relative_to(repo)}/ has {n} flat components >25 — switch to feature folders (§4/§8)")
                    elif n > 20:
                        notes.append(f"{comp.relative_to(repo)}/ has {n} flat components (~20 target; §4)")
                    elif not framework:
                        notes.append(f"type-folder(s) {sorted(smells)} under {base.name or '.'} — prefer feature folders (§4)")
                elif not framework:
                    notes.append(f"type-folder(s) {sorted(smells)} under {base.name or '.'} — prefer feature folders (§4)")

    # §4 nesting depth — measured from the PACKAGE root, not src/.
    # Python `src/<pkg>/...` legitimately spends one level on the package dir;
    # measuring from src/ over-penalizes it. Exempt framework-imposed routing.
    src = repo / "src"
    if src.is_dir() and not framework:
        subdirs = [d for d in src.iterdir() if d.is_dir() and not d.name.startswith(".")]
        base = subdirs[0] if len(subdirs) == 1 else src  # single package dir -> measure inside it
        d = max_depth(base)
        if d > MAX_NESTING:
            rel = base.relative_to(repo)
            violations.append(f"{rel}/ nesting depth {d} >{MAX_NESTING} (§4)")

    # §6 branch-per-environment smell (heuristic: env-named dirs are fine; can't see branches here)
    if (repo / "environments").is_dir() or (repo / "envs").is_dir() or (repo / "overlays").is_dir():
        notes.append("directory-per-environment present (§6 compliant)")

    score = max(0, 100 - 25 * len(violations) - 5 * len(notes))
    return {
        "repo": str(repo.relative_to(HOME)),
        "layout": layout,
        "framework": framework,
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
