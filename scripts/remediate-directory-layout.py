#!/usr/bin/env python3
"""Remediation engine for standard #26 — closes the SAFE class of gaps.

Inverse of audit-directory-layout.py. For each first-party repo missing a
README or LICENSE, generates the appropriate file (honest stub README; MIT or
CC-BY-SA-4.0 per #10 license policy) and commits it on the repo's current branch.

ADDITIVE ONLY: never moves, deletes, or overwrites an existing file. Structural
debt (root>20, components>20, nesting>3) is OUT of scope here — those move files
and require per-repo build verification; tend to them by hand.

Usage:
    remediate-directory-layout.py            # dry-run (prints planned actions)
    remediate-directory-layout.py --apply    # write + commit (no push)
"""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

HOME = Path.home()
GAP = HOME / "Code/organvm/organvm-corpvs-testamentvm/docs/research/2026-05-29-layout-conformance.json"
YEAR = 2026
HOLDER = "[name redacted] (@4444J99) / ORGANVM"

CODE_MANIFESTS = ("package.json", "pyproject.toml", "go.mod", "Cargo.toml", "setup.py")

MIT = """MIT License

Copyright (c) {year} {holder}

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

CC = """Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

Copyright (c) {year} {holder}

This work is licensed under the Creative Commons Attribution-ShareAlike 4.0
International License. You are free to share and adapt the material for any
purpose, even commercially, under the following terms: you must give
appropriate credit and distribute your contributions under the same license.

Full license text: https://creativecommons.org/licenses/by-sa/4.0/legalcode
Summary: https://creativecommons.org/licenses/by-sa/4.0/
"""


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def is_code(repo: Path) -> bool:
    return any((repo / m).exists() for m in CODE_MANIFESTS)


def describe(repo: Path) -> str | None:
    """Honest one-line description from manifests — never fabricated."""
    pj = repo / "package.json"
    if pj.exists():
        try:
            d = json.loads(pj.read_text())
            if d.get("description"):
                return d["description"].strip()
        except Exception:
            pass
    pp = repo / "pyproject.toml"
    if pp.exists():
        for line in pp.read_text(errors="ignore").splitlines():
            s = line.strip()
            if s.startswith("description"):
                return s.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def title_of(repo: Path) -> str:
    return repo.name.replace("--", " — ").replace("-", " ").title()


def gen_readme(repo: Path) -> str:
    desc = describe(repo)
    hook = f"> {desc}" if desc else "> _Part of the ORGANVM system. One-line purpose pending curation._"
    return (
        f"# {title_of(repo)}\n\n"
        f"{hook}\n\n"
        f"## Status\n\n"
        f"Active. See `CLAUDE.md` for working context where present.\n\n"
        f"## Context\n\n"
        f"Member repository of the ORGANVM eight-organ system. Repository "
        f"standards: `organvm-corpvs-testamentvm/docs/standards/10-repository-standards.md` "
        f"and `26-internal-directory-layout--monorepo-feature-organization.md`.\n"
    )


def main() -> int:
    apply = "--apply" in sys.argv
    data = json.loads(GAP.read_text())
    actions: list[tuple[Path, list[str], str]] = []

    for r in data:
        if r.get("exempt") or not r["violations"]:
            continue
        repo = HOME / r["repo"]
        if not (repo / ".git").exists():
            continue
        need_readme = any("README" in v for v in r["violations"])
        need_license = any("LICENSE" in v for v in r["violations"])
        made: list[str] = []
        if need_readme and not any((repo / n).exists() for n in
                                   ("README.md", "README.rst", "README.txt", "README")):
            made.append("README.md")
        if need_license and not any((repo / n).exists() for n in
                                    ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING")):
            made.append("LICENSE")
        if made:
            lic = "MIT" if is_code(repo) else "CC-BY-SA-4.0"
            actions.append((repo, made, lic))

    print(f"{'APPLY' if apply else 'DRY-RUN'}: {len(actions)} repos to remediate (README/LICENSE only)\n")
    done = 0
    for repo, made, lic in actions:
        label = f"{repo.relative_to(HOME)}  +{','.join(made)}" + (f" [{lic}]" if "LICENSE" in made else "")
        print(("  ✓ " if apply else "  · ") + label)
        if not apply:
            continue
        for f in made:
            if f == "README.md":
                (repo / "README.md").write_text(gen_readme(repo))
            elif f == "LICENSE":
                tmpl = MIT if lic == "MIT" else CC
                (repo / "LICENSE").write_text(tmpl.format(year=YEAR, holder=HOLDER))
        rc, _ = run(["git", "add"] + made, repo)
        msg = (f"Close #26 gap: add {' + '.join(made)}\n\n"
               f"Standard #26 root-hygiene conformance (additive; no files moved).\n\n"
               f"Co-Authored-By: Claude Opus 4.8 (1M context) <[email redacted]>")
        rc, out = run(["git", "commit", "-q", "-m", msg], repo)
        if rc == 0:
            done += 1
        else:
            print(f"      ! commit failed: {out[:120]}")
    if apply:
        print(f"\nCommitted in {done}/{len(actions)} repos (local; push separately).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
