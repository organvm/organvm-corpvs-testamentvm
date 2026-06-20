#!/usr/bin/env python3
"""Calculate system-wide metrics from repo-registry.json, sprint specs, and essays.

Thin wrapper around organvm_engine.metrics.calculator — delegates core computation
to the engine while adding corpus-specific features (sprint counts, essay API, etc.).

Usage:
    python3 scripts/calculate-metrics.py
    python3 scripts/calculate-metrics.py --registry repo-registry.json --output system-metrics.json
    python3 scripts/calculate-metrics.py --skip-essays   # offline mode
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from organvm_engine.metrics.calculator import (
    compute_metrics,
    format_word_count,
    write_metrics,
)

# ISOTOPE DISSOLUTION: Gate memory--remember G2 (CORPUS_SCRIPTS_DISSOLVED)
from organvm_engine.registry.loader import load_registry as _engine_load

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = ROOT / "repo-registry.json"
DEFAULT_OUTPUT = ROOT / "system-metrics.json"
SPRINTS_DIR = ROOT / "docs" / "specs" / "sprints"


def count_sprint_specs(sprints_dir: Path) -> tuple[int, list[str]]:
    """Count .md files in specs/sprints/ and return sorted names."""
    if not sprints_dir.is_dir():
        return 0, []
    specs = sorted(f.stem for f in sprints_dir.glob("*.md"))
    return len(specs), specs


def count_local_essays(workspace: Path) -> int:
    """Count essays from local public-process _posts/ directory."""
    posts_dir = workspace / "organvm-v-logos" / "public-process" / "_posts"
    if not posts_dir.is_dir():
        return -1
    essays = [f for f in posts_dir.iterdir() if f.is_file() and f.suffix in (".md", ".markdown", ".html")]
    return len(essays)


def fetch_essay_count_remote(skip: bool = False) -> int:
    """Get essay count from public-process _posts/ via gh API (fallback)."""
    if skip:
        return -1  # sentinel: caller should preserve existing value

    try:
        result = subprocess.run(
            ["gh", "api",
             "repos/organvm-v-logos/public-process/git/trees/HEAD?recursive=1",
             "--jq", '[.tree[] | select(.path | startswith("_posts/"))] | length'],
            capture_output=True, text=True, timeout=15,
        )
        if result.returncode == 0 and result.stdout.strip().isdigit():
            return int(result.stdout.strip())
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    print("  WARNING: Could not fetch essay count from GitHub API", file=sys.stderr)
    return -1


def fetch_essay_count(skip: bool = False, workspace: Path | None = None) -> int:
    """Get essay count: local _posts/ as primary source, GitHub API as fallback.

    Local counting is preferred because essays may exist locally before being
    pushed to the remote. The GitHub API only sees pushed content.
    """
    if skip:
        return -1

    # Primary: count from local filesystem
    if workspace:
        local_count = count_local_essays(workspace)
        if local_count > 0:
            # Validate against remote if available (informational only)
            remote_count = fetch_essay_count_remote(skip=False)
            if remote_count > 0 and remote_count != local_count:
                print(f"  NOTE: Local essays ({local_count}) != remote ({remote_count}) — "
                      f"{local_count - remote_count} unpushed", file=sys.stderr)
            return local_count

    # Fallback: GitHub API
    return fetch_essay_count_remote(skip=False)


def load_existing_essay_count(output_path: Path) -> int:
    """Fallback: read essay count from existing metrics if API was skipped."""
    if not output_path.exists():
        return 29  # known good default

    try:
        with open(output_path) as f:
            existing = json.load(f)
        return existing.get("computed", {}).get("published_essays", 29)
    except (json.JSONDecodeError, KeyError):
        return 29


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate system metrics")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY),
                        help="Path to repo-registry.json")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT),
                        help="Path for JSON metrics output")
    parser.add_argument("--skip-essays", action="store_true",
                        help="Skip GitHub API call for essay count")
    parser.add_argument("--workspace", default=None,
                        help="Workspace root for word counting (default: ~/Workspace)")
    parser.add_argument("--skip-words", action="store_true",
                        help="Skip word counting")
    args = parser.parse_args()

    registry_path = Path(args.registry)
    output_path = Path(args.output)

    # Load registry
    registry = _engine_load(registry_path)

    # Core metrics from engine
    workspace_raw = args.workspace or os.environ.get("ORGANVM_WORKSPACE_DIR")
    workspace = (
        Path(workspace_raw).expanduser().resolve() if workspace_raw
        else Path.home() / "Workspace"
    )

    workspace_arg = workspace if (not args.skip_words and workspace.is_dir()) else None
    computed = compute_metrics(registry, workspace=workspace_arg)

    # Corpus-specific: sprint specs
    sprint_count, sprint_names = count_sprint_specs(SPRINTS_DIR)
    computed["sprints_completed"] = sprint_count
    computed["sprint_names"] = sprint_names

    # Corpus-specific: essay count (local primary, GitHub API fallback)
    essay_count = fetch_essay_count(skip=args.skip_essays, workspace=workspace)
    if essay_count == -1:
        essay_count = load_existing_essay_count(output_path)
        print(f"  Using existing essay count: {essay_count}")
    computed["published_essays"] = essay_count

    # Write via engine
    write_metrics(computed, output_path)

    # Summary
    c = computed
    print(f"Metrics written to {output_path}")
    print(f"  Repos: {c['total_repos']} ({c['active_repos']} ACTIVE)")
    print(f"  Organs: {c['operational_organs']}/{c['total_organs']} operational")
    print(f"  CI: {c['ci_workflows']}")
    print(f"  Dependencies: {c['dependency_edges']} edges")
    print(f"  Essays: {c.get('published_essays', '?')}")
    print(f"  Sprints: {c.get('sprints_completed', '?')}")
    if "word_counts" in c:
        wc = c["word_counts"]
        tw, tw_num, tw_short = format_word_count(wc["total"])
        print(f"  Words: {tw_short} (readmes={wc['readmes']:,}, essays={wc['essays']:,}, "
              f"corpus={wc['corpus']:,}, profiles={wc['org_profiles']:,})")


if __name__ == "__main__":
    main()
