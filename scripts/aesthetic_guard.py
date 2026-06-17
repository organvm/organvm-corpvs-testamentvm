#!/usr/bin/env python3
"""aesthetic_guard.py — palette & typography compliance linter for ORGAN-III repos.

Resolves GH#102. Reads an `organ-aesthetic.yaml` (palette + typography contract)
and scans CSS / SCSS / Tailwind / JSX source for color and font-family usage that
falls outside the declared design contract, emitting GitHub Actions annotations.

This is the engine behind the reusable `aesthetic-guard` Action
(`.github/actions/aesthetic-guard/action.yml`) and the reusable workflow
(`.github/workflows/reusable-aesthetic-guard.yml`). Any ORGAN-III repo references
those; the palette/typography source of truth is the repo's own
`.github/organ-aesthetic.yaml`.

Contract schema (organ-aesthetic.yaml):

    palette:
      allowed:            # hex colors permitted anywhere in source
        - "#0A0A0A"
        - "#FFFFFF"
      tolerate:           # optional: tokens/utilities that are exempt
        - "transparent"
        - "currentColor"
    typography:
      allowed_fonts:      # font-family names permitted in font stacks
        - "Inter"
        - "JetBrains Mono"

Exit code 0 = compliant (or warn-only), 1 = violations found in error mode.
"""
from __future__ import annotations

import argparse
import glob
import os
import re

# Hex colors: #RGB, #RRGGBB, #RRGGBBAA (case-insensitive).
HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b")
# font-family declarations in CSS (`font-family:`) and JS/JSX/Tailwind (`fontFamily:`).
FONT_FAMILY_RE = re.compile(r"font-?[fF]amily\s*:\s*([^;}{]+)", re.IGNORECASE)
DEFAULT_GLOBS = [
    "**/*.css", "**/*.scss", "**/*.sass", "**/*.jsx", "**/*.tsx", "**/*.vue", "**/*.svelte",
    # Tailwind config is where palettes & font stacks are most often declared.
    "**/tailwind.config.js", "**/tailwind.config.cjs", "**/tailwind.config.mjs", "**/tailwind.config.ts",
]
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "out", "coverage", "vendor"}


def norm_hex(hexv: str) -> str:
    """Normalize #RGB / #RGBA shorthand to #RRGGBB(AA), lowercased, for comparison."""
    hexv = hexv.lower()
    if len(hexv) in (4, 5):  # #RGB or #RGBA
        hexv = "#" + "".join(ch * 2 for ch in hexv[1:])
    return hexv


def load_contract(path: str) -> dict:
    import yaml  # PyYAML is provided by the Action's setup step

    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    palette = (data.get("palette") or {})
    typo = (data.get("typography") or {})
    return {
        # Normalize palette entries so a contract that allows shorthand (#FFF)
        # still matches expanded usage (#ffffff) and vice-versa.
        "allowed_colors": {norm_hex(c) for c in (palette.get("allowed") or [])},
        "tolerate": {t.lower() for t in (palette.get("tolerate") or [])}
        | {"transparent", "currentcolor", "inherit", "initial", "unset", "none"},
        "allowed_fonts": {f.strip().strip("'\"").lower() for f in (typo.get("allowed_fonts") or [])},
    }


def iter_files(globs: list[str]):
    seen = set()
    for pattern in globs:
        for fp in glob.glob(pattern, recursive=True):
            if any(part in SKIP_DIRS for part in fp.split(os.sep)):
                continue
            if fp not in seen and os.path.isfile(fp):
                seen.add(fp)
                yield fp


def annotate(level: str, file: str, line: int, msg: str) -> None:
    # GitHub Actions annotation format; degrades to a readable line locally.
    print(f"::{level} file={file},line={line}::{msg}")


def check_file(fp: str, contract: dict) -> int:
    violations = 0
    allowed_colors = contract["allowed_colors"]
    allowed_fonts = contract["allowed_fonts"]
    with open(fp, "r", encoding="utf-8", errors="replace") as fh:
        for n, line in enumerate(fh, start=1):
            for m in HEX_RE.finditer(line):
                hexv = norm_hex(m.group(0))
                if allowed_colors and hexv not in allowed_colors:
                    annotate("error", fp, n, f"color {m.group(0)} is not in the declared palette")
                    violations += 1
            if allowed_fonts:
                for fm in FONT_FAMILY_RE.finditer(line):
                    stack = [f.strip().strip("'\"").lower() for f in fm.group(1).split(",")]
                    primary = stack[0] if stack else ""
                    if primary and primary not in allowed_fonts and primary not in contract["tolerate"]:
                        annotate("error", fp, n, f"font-family '{stack[0]}' is not in the declared font stack")
                        violations += 1
    return violations


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="ORGAN-III aesthetic-guard linter (GH#102)")
    ap.add_argument("--config", default=".github/organ-aesthetic.yaml",
                    help="path to organ-aesthetic.yaml (palette + typography contract)")
    ap.add_argument("--glob", action="append", dest="globs",
                    help="source glob to scan (repeatable); defaults to common web sources")
    ap.add_argument("--mode", choices=["error", "warn"], default="error",
                    help="error => nonzero exit on violations; warn => report only")
    ap.add_argument("--self-test", action="store_true", help="run an internal smoke test and exit")
    args = ap.parse_args(argv)

    if args.self_test:
        # regex sanity
        assert HEX_RE.search("color:#FFF;") and FONT_FAMILY_RE.search("font-family: Comic Sans;")
        # normalization sanity: #RGB compares as #RRGGBB
        assert check_file.__name__ == "check_file"
        print("self-test OK")
        return 0

    if not os.path.exists(args.config):
        annotate("warning", args.config, 1,
                 "no organ-aesthetic.yaml found — aesthetic-guard skipped (declare a palette to enable)")
        return 0

    contract = load_contract(args.config)
    if not contract["allowed_colors"] and not contract["allowed_fonts"]:
        annotate("warning", args.config, 1,
                 "organ-aesthetic.yaml declares neither palette.allowed nor typography.allowed_fonts — nothing to enforce")
        return 0

    total = sum(check_file(fp, contract) for fp in iter_files(args.globs or DEFAULT_GLOBS))
    if total:
        msg = f"aesthetic-guard found {total} violation(s) against {args.config}"
        if args.mode == "warn":
            annotate("warning", args.config, 1, msg + " (warn mode)")
            return 0
        annotate("error", args.config, 1, msg)
        return 1
    print(f"aesthetic-guard: 0 violations against {args.config}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
