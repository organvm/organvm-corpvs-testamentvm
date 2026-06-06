#!/usr/bin/env python3
"""PRAXIS Sprint Phase B: Flagship repo code substance audit.

Queries GitHub API for each flagship/key repo to assess:
  - Lines of code (non-docs, non-config)
  - Test file count and test function count
  - CI workflow status (passing/failing/none)
  - Real code vs skeleton classification
  - Demo/example directory presence

Usage:
    python3 scripts/praxis-flagship-audit.py [--output praxis-flagship-report.json]
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent.parent / "repo-registry.json"

# Flagship targets from PRAXIS plan (prioritized by portfolio impact)
FLAGSHIP_TARGETS = [
    {
        "org": "organvm-i-theoria",
        "repo": "recursive-engine--generative-entity",
        "organ": "I",
        "language": "Python",
        "plan": "Add comprehensive tests, docs, demo notebook",
    },
    {
        "org": "organvm-i-theoria",
        "repo": "auto-revision-epistemic-engine",
        "organ": "I",
        "language": "Python",
        "plan": "Add API, tests, usage examples",
    },
    {
        "org": "organvm-ii-poiesis",
        "repo": "metasystem-master",
        "organ": "II",
        "language": "Python",
        "plan": "Add integration tests, demo mode",
    },
    {
        "org": "organvm-ii-poiesis",
        "repo": "example-generative-music",
        "organ": "II",
        "language": "TypeScript",
        "plan": "Web Audio API generative music engine with live demo",
    },
    {
        "org": "organvm-iii-ergon",
        "repo": "gamified-coach-interface",
        "organ": "III",
        "language": "TypeScript",
        "plan": "Next.js coaching app skeleton with working UI",
    },
    {
        "org": "organvm-iii-ergon",
        "repo": "classroom-rpg-aetheria",
        "organ": "III",
        "language": "TypeScript",
        "plan": "Game engine core with playable demo",
    },
    {
        "org": "organvm-iv-taxis",
        "repo": "agentic-titan",
        "organ": "IV",
        "language": "Python",
        "plan": "Working orchestration agent with real dispatch",
    },
    {
        "org": "organvm-v-logos",
        "repo": "public-process",
        "organ": "V",
        "language": "Jekyll",
        "plan": "Ensure Jekyll builds cleanly, add search, improve navigation",
    },
]

# Code file extensions (non-config, non-docs)
CODE_EXTENSIONS = {
    "Python": {".py"},
    "TypeScript": {".ts", ".tsx", ".js", ".jsx"},
    "Jekyll": {".rb", ".html", ".scss", ".css", ".js"},
}

# Test file patterns
TEST_PATTERNS = {
    "Python": ["test_", "_test.py", "tests/", "spec_"],
    "TypeScript": [".test.", ".spec.", "__tests__/", "tests/"],
    "Jekyll": ["_spec.", "test"],
}


def gh_api(endpoint, jq_filter=None):
    """Call GitHub API via gh CLI."""
    cmd = ["gh", "api", endpoint]
    if jq_filter:
        cmd.extend(["--jq", jq_filter])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return None, result.stderr.strip()
    return result.stdout.strip(), None


def audit_repo(org, repo, language):
    """Audit a single repo for code substance."""
    full = f"{org}/{repo}"
    report = {
        "org": org,
        "repo": repo,
        "language": language,
        "audited": datetime.now(timezone.utc).isoformat(),
    }

    # 1. Get file tree
    tree_data, err = gh_api(
        f"repos/{full}/git/trees/HEAD?recursive=1",
        "[.tree[] | .path]"
    )
    if err:
        report["error"] = f"Could not fetch tree: {err}"
        report["classification"] = "ERROR"
        return report

    try:
        paths = json.loads(tree_data)
    except (json.JSONDecodeError, TypeError):
        report["error"] = "Could not parse tree response"
        report["classification"] = "ERROR"
        return report

    # 2. Classify files
    code_exts = CODE_EXTENSIONS.get(language, set())
    test_pats = TEST_PATTERNS.get(language, [])

    code_files = []
    test_files = []
    doc_files = []
    config_files = []
    demo_files = []
    total_files = len(paths)

    # Collect all code extensions across all languages for multi-language detection
    all_code_exts = set()
    for exts in CODE_EXTENSIONS.values():
        all_code_exts.update(exts)

    for p in paths:
        lower = p.lower()
        ext = "." + p.rsplit(".", 1)[-1] if "." in p else ""

        # Skip truly hidden directories (not .github or .ci which contain real code)
        code_dotdirs = {".github", ".ci"}
        if any(seg.startswith(".") for seg in p.split("/") if seg not in code_dotdirs):
            config_files.append(p)
            continue

        # Demo/example detection (tag only, doesn't skip)
        if any(d in lower for d in ["demo/", "examples/", "example/", "notebooks/", "demo."]):
            demo_files.append(p)

        # Test detection — code extension + test pattern
        is_test = any(pat in lower for pat in test_pats)
        if is_test and ext in code_exts:
            test_files.append(p)
            continue

        # Code detection — check BEFORE docs/config to avoid misclassifying
        # .py files in docs/ directories or .ci/ scripts as non-code
        if ext in code_exts:
            code_files.append(p)
            continue

        # Doc detection — only for doc-specific extensions or docs/ with non-code files
        if ext in {".md", ".txt", ".rst", ".adoc"}:
            doc_files.append(p)
            continue
        if lower.startswith("docs/") and ext not in all_code_exts:
            doc_files.append(p)
            continue

        # Config detection
        if ext in {".yml", ".yaml", ".toml", ".json", ".cfg", ".ini", ".lock"}:
            config_files.append(p)
            continue

    # 3. Check for src/ directory
    has_src = any(p.startswith("src/") for p in paths)
    has_lib = any(p.startswith("lib/") for p in paths)
    has_app = any(p.startswith("app/") for p in paths)
    has_package = any(p.startswith("packages/") for p in paths)

    # 4. Check CI status
    ci_data, ci_err = gh_api(
        f"repos/{full}/actions/runs?per_page=1",
        ".workflow_runs[0] | {status, conclusion, name, created_at}"
    )
    ci_status = None
    if ci_data and ci_data != "null":
        try:
            ci_status = json.loads(ci_data)
        except json.JSONDecodeError:
            pass

    # 5. Check for package.json / pyproject.toml (real project indicators)
    has_package_json = "package.json" in paths
    has_pyproject = "pyproject.toml" in paths or "setup.py" in paths
    has_cargo = "Cargo.toml" in paths
    has_gemfile = "Gemfile" in paths

    # 6. Classify
    code_count = len(code_files)
    test_count = len(test_files)

    if code_count >= 20 and test_count >= 5:
        classification = "SUBSTANTIAL"
    elif code_count >= 10 or (code_count >= 5 and test_count >= 1):
        classification = "PARTIAL"
    elif code_count >= 1:
        classification = "MINIMAL"
    else:
        classification = "SKELETON"

    report.update({
        "total_files": total_files,
        "code_files": len(code_files),
        "test_files": len(test_files),
        "doc_files": len(doc_files),
        "config_files": len(config_files),
        "demo_files": len(demo_files),
        "has_src_dir": has_src,
        "has_lib_dir": has_lib,
        "has_app_dir": has_app,
        "has_package_dir": has_package,
        "has_build_manifest": has_package_json or has_pyproject or has_cargo or has_gemfile,
        "ci_latest": ci_status,
        "classification": classification,
        "code_file_list": code_files[:20],  # First 20 for reference
        "test_file_list": test_files[:10],
    })

    return report


def main():
    parser = argparse.ArgumentParser(description="Audit flagship repo code substance")
    parser.add_argument("--output", default="praxis-flagship-report.json",
                        help="Output JSON report path")
    parser.add_argument("--all-repos", action="store_true",
                        help="Audit ALL non-archived repos, not just flagships")
    args = parser.parse_args()

    print("=" * 60)
    print("PRAXIS Sprint Phase B — Flagship Code Substance Audit")
    print("=" * 60)

    targets = FLAGSHIP_TARGETS

    if args.all_repos:
        with open(REGISTRY_PATH) as f:
            reg = json.load(f)
        targets = []
        for organ_key, organ_data in reg["organs"].items():
            for repo in organ_data.get("repositories", []):
                if repo.get("implementation_status") == "ARCHIVED":
                    continue
                if repo["name"] == ".github":
                    continue
                lang = "Python"
                ci = repo.get("ci_workflow") or ""
                if "typescript" in ci:
                    lang = "TypeScript"
                elif "python" in ci:
                    lang = "Python"
                elif "mixed" in ci:
                    lang = "Python"  # mixed repos get Python detection + TS counted separately
                targets.append({
                    "org": repo.get("org", ""),
                    "repo": repo["name"],
                    "organ": organ_key.replace("ORGAN-", "").replace("META-ORGANVM", "Meta"),
                    "language": lang,
                    "plan": "",
                })

    reports = []
    classifications = {"SUBSTANTIAL": 0, "PARTIAL": 0, "MINIMAL": 0, "SKELETON": 0, "ERROR": 0}

    for i, target in enumerate(targets, 1):
        full = f"{target['org']}/{target['repo']}"
        print(f"\n[{i}/{len(targets)}] Auditing {full}")
        report = audit_repo(target["org"], target["repo"], target["language"])
        report["organ"] = target.get("organ", "")
        report["vivification_plan"] = target.get("plan", "")

        cls = report.get("classification", "ERROR")
        classifications[cls] = classifications.get(cls, 0) + 1

        status_icon = {
            "SUBSTANTIAL": "+",
            "PARTIAL": "~",
            "MINIMAL": "-",
            "SKELETON": "!",
            "ERROR": "X",
        }.get(cls, "?")

        print(f"  [{status_icon}] {cls}: {report.get('code_files', 0)} code, "
              f"{report.get('test_files', 0)} test, "
              f"{report.get('total_files', 0)} total")

        reports.append(report)

    # Summary
    print(f"\n{'=' * 60}")
    print("FLAGSHIP AUDIT SUMMARY")
    print(f"{'=' * 60}")
    for cls, count in sorted(classifications.items()):
        if count > 0:
            print(f"  {cls}: {count}")

    substantial = classifications.get("SUBSTANTIAL", 0)
    total = len(reports)
    print(f"\n  Vivification needed: {total - substantial} of {total} repos")

    output_data = {
        "audit_date": datetime.now(timezone.utc).isoformat(),
        "sprint": "PRAXIS",
        "phase": "B",
        "total_audited": total,
        "classifications": classifications,
        "repos": reports,
    }

    output_path = Path(args.output)
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=2)
        f.write("\n")

    print(f"\n  Report: {output_path}")


if __name__ == "__main__":
    main()
