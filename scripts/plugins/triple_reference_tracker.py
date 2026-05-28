#!/usr/bin/env python3
"""triple-reference-tracker — enforce IRF + repo + GH issue triple per work atom.

For each IRF ID supplied, verify:
  1. The IRF entry exists in `INST-INDEX-RERUM-FACIENDARUM.md`
  2. The repo reference is present (defaults to `a-organvm/organvm-corpvs-testamentvm`)
  3. A GH-issue reference (`GH#NNN` or `#NNN`) is present in the IRF row

Fails closed: exit non-zero if any of the three is missing for any input ID.

Usage:
    organ-cli plugin triple-reference-tracker IRF-THE-033
    organ-cli plugin triple-reference-tracker IRF-THE-033 IRF-SYS-184 IRF-SYS-185
    organ-cli plugin triple-reference-tracker IRF-THE-033 --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
IRF_FILE = ROOT / "INST-INDEX-RERUM-FACIENDARUM.md"
DEFAULT_REPO = "a-organvm/organvm-corpvs-testamentvm"


@dataclass
class TripleCheck:
    irf_id: str
    irf_present: bool
    repo_present: bool
    gh_issue: str | None
    row_excerpt: str
    verdict: str  # "OK" | "MISSING" | "NOT_FOUND"


def _find_row(irf_id: str, irf_text: str) -> str | None:
    pattern = re.compile(rf"^\|\s*~?~?{re.escape(irf_id)}~?~?\s*\|.*$", re.MULTILINE)
    m = pattern.search(irf_text)
    return m.group(0) if m else None


def _check(irf_id: str, irf_text: str, repo: str) -> TripleCheck:
    row = _find_row(irf_id, irf_text)
    if not row:
        return TripleCheck(
            irf_id=irf_id,
            irf_present=False,
            repo_present=False,
            gh_issue=None,
            row_excerpt="",
            verdict="NOT_FOUND",
        )
    repo_present = repo in row or repo.split("/")[1] in row
    gh_match = re.search(r"GH#?(\d+)|#(\d{3,})\b", row)
    gh_issue = None
    if gh_match:
        gh_issue = gh_match.group(1) or gh_match.group(2)
    verdict = "OK" if (repo_present and gh_issue) else "MISSING"
    excerpt = (row[:240] + "…") if len(row) > 240 else row
    return TripleCheck(
        irf_id=irf_id,
        irf_present=True,
        repo_present=repo_present,
        gh_issue=gh_issue,
        row_excerpt=excerpt,
        verdict=verdict,
    )


def _emit_markdown(checks: list[TripleCheck], repo: str) -> str:
    lines = [
        "# Triple Reference Tracker Report",
        "",
        f"- **Default repo:** `{repo}`",
        f"- **Checked IDs:** {len(checks)}",
        "",
        "| IRF ID | In IRF? | Repo? | GH Issue | Verdict |",
        "|---|---|---|---|---|",
    ]
    for c in checks:
        lines.append(
            f"| {c.irf_id} "
            f"| {'✓' if c.irf_present else '✗'} "
            f"| {'✓' if c.repo_present else '✗'} "
            f"| {c.gh_issue or '—'} "
            f"| {c.verdict} |"
        )
    lines.append("")
    return "\n".join(lines)


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="organ-cli plugin triple-reference-tracker")
    parser.add_argument("irf_ids", nargs="+", help="one or more IRF IDs (e.g. IRF-THE-033)")
    parser.add_argument("--repo", default=DEFAULT_REPO,
                        help="repo slug to require in the row (default: %(default)s)")
    parser.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    args = parser.parse_args(argv)

    if not IRF_FILE.exists():
        print(f"ERROR: IRF not found at {IRF_FILE}", file=sys.stderr)
        return 2

    irf_text = IRF_FILE.read_text()
    checks = [_check(i, irf_text, args.repo) for i in args.irf_ids]

    if args.json:
        print(json.dumps([asdict(c) for c in checks], indent=2))
    else:
        print(_emit_markdown(checks, args.repo))

    return 0 if all(c.verdict == "OK" for c in checks) else 1


if __name__ == "__main__":
    sys.exit(run())
