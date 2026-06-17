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

Scope & limitations (by design — this is a lightweight heuristic, not an AST/CSS
engine): it checks hex-literal colors and font declarations — CSS `font-family`,
JS/JSX `fontFamily`, Tailwind theme objects, and CSS custom-property font tokens
(`--font-*`). It does NOT:
  - resolve Tailwind *utility classes* (`bg-red-500`, `text-sky-600`) against the
    palette — that requires encoding Tailwind's theme and is false-positive-prone;
    use `eslint-plugin-tailwindcss` with a restricted theme for that.
  - parse the CSS `font:` *shorthand* (`font: 16px 'X', sans-serif`) — isolating
    the family from size/weight/line-height reliably needs a real CSS parser.
The guard validates the *declared* contract/tokens and the common explicit
font-family forms, not every possible CSS/Tailwind authoring style. For
exhaustive enforcement, pair it with stylelint / eslint-plugin-tailwindcss in the
consumer's own CI.

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
# CSS custom-property font-token DEFINITIONS, e.g. `--font-body: 'Inter', sans-serif;`
# (captures the property name and value so size/weight tokens can be excluded).
CSS_FONT_VAR_DEF_RE = re.compile(r"(--[\w-]*font[\w-]*)\s*:\s*([^;}{]+)", re.IGNORECASE)
DEFAULT_GLOBS = [
    "**/*.css", "**/*.scss", "**/*.sass",
    "**/*.js", "**/*.ts", "**/*.jsx", "**/*.tsx", "**/*.vue", "**/*.svelte",
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


def primary_fonts(value: str) -> list[str]:
    """Primary font of each stack in a font-family value (lowercased).

    Handles CSS lists (`Inter, sans-serif`), quoted names (`'Comic Sans', serif`),
    JS arrays (`['OffContract', 'serif']`), and Tailwind object bodies
    (` sans: ['A','B'], display: ['OffContract'] `) — taking the FIRST entry of
    each array/stack so legitimate fallbacks (ui-sans-serif, system-ui) are not
    falsely flagged.
    """
    value = value.strip()
    arrays = re.findall(r"\[([^\]]*)\]", value)
    if arrays:
        out = []
        for arr in arrays:
            toks = re.findall(r"""['"]([^'"]+)['"]""", arr)
            if toks:
                out.append(toks[0].strip().lower())
        if out:
            return out
    quoted = re.findall(r"""['"]([^'"]+)['"]""", value)
    if quoted:
        # A quoted token may itself be a CSS stack, e.g. 'Inter, sans-serif' (common
        # in JSX inline styles) — take the primary family before the first comma.
        return [quoted[0].split(",")[0].strip().lower()]
    first = value.split(",")[0].strip().strip("{}").strip().lower()
    return [first] if first else []


def check_file(fp: str, contract: dict) -> int:
    violations = 0
    allowed_colors = contract["allowed_colors"]
    allowed_fonts = contract["allowed_fonts"]
    tolerate = contract["tolerate"]
    with open(fp, "r", encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()

    def check_fonts(names: list[str], ln: int) -> None:
        nonlocal violations
        for name in names:
            # Skip CSS custom properties / design tokens (e.g. var(--font-body)):
            # the real stack lives in the token definition, which is validated where
            # it is declared, not at each use site.
            if name.startswith("var(") or name.startswith("--"):
                continue
            if name and name not in allowed_fonts and name not in tolerate:
                annotate("error", fp, ln, f"font-family '{name}' is not in the declared font stack")
                violations += 1

    for n, line in enumerate(lines, start=1):
        for m in HEX_RE.finditer(line):
            hexv = norm_hex(m.group(0))
            if allowed_colors and hexv not in allowed_colors:
                annotate("error", fp, n, f"color {m.group(0)} is not in the declared palette")
                violations += 1
        if allowed_fonts:
            for fm in FONT_FAMILY_RE.finditer(line):
                val = fm.group(1).strip()
                if val and not val.startswith("{"):  # object form handled below
                    check_fonts(primary_fonts(val), n)
            # CSS custom-property font-token definitions (--font-body: 'X', y;).
            # Only treat as a font stack when the name says "family" or the value
            # looks like a stack (quote/comma) — so --font-size/-weight are ignored.
            for vm in CSS_FONT_VAR_DEF_RE.finditer(line):
                var_name, var_val = vm.group(1).lower(), vm.group(2).strip()
                # Treat as a font stack only when the name says "family" or the value
                # carries a quoted family. A bare comma is NOT a trigger — size tokens
                # like `--font-size-fluid: clamp(1rem, 2vw, 2rem)` contain commas but
                # declare no font family. Also skip values that are CSS functions.
                looks_func = "(" in var_val
                if (("family" in var_name) or "'" in var_val or '"' in var_val) and not looks_func:
                    check_fonts(primary_fonts(var_val), n)
    # Object form (Tailwind theme): fontFamily: { sans: [...], ... } — single or
    # multi-line. Scanned over the whole file so the value past `{` is examined.
    if allowed_fonts:
        text = "".join(lines)
        for m in re.finditer(r"font-?[fF]amily\s*:\s*\{(.*?)\}", text, re.DOTALL):
            ln = text[: m.start()].count("\n") + 1
            check_fonts(primary_fonts(m.group(1)), ln)
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
        assert HEX_RE.search("color:#FFF;") and FONT_FAMILY_RE.search("font-family: Comic Sans;")
        assert norm_hex("#FFF") == "#ffffff"  # shorthand normalizes
        # primary-font extraction across CSS / quoted / array / Tailwind-object forms
        assert primary_fonts("Inter, sans-serif") == ["inter"]
        assert primary_fonts("'Comic Sans', serif") == ["comic sans"]
        assert primary_fonts("'Inter, sans-serif'") == ["inter"]  # quoted CSS stack (JSX inline)
        assert primary_fonts("['OffContract', 'serif']") == ["offcontract"]
        assert primary_fonts(" sans: ['Inter','ui-sans'], display: ['OffContract'] ") == ["inter", "offcontract"]
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
