#!/usr/bin/env python3
"""Plan Task Reality Check — verify plan-derived tasks against filesystem reality.

Builds a filename index of ~/Workspace/ once (skipping node_modules, .git, __pycache__),
then batch-checks all tasks from atomized-tasks.jsonl against it.

Verification strategies:
  1. Source plan in .archive/ -> archived_moot
  2. Source plan file existence check
  3. files_touched field -> direct path check
  4. raw_text file path extraction (regex + backtick paths)
  5. Repo/project directory existence
  6. delete_file tasks -> success = absence
  7. create_file tasks -> success = presence
  8. Title-based backtick path extraction

Output: plan-tasks-triaged.jsonl (same directory as input).
"""

import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

WORKSPACE = Path.home() / "Workspace"
ATOMS_DIR = WORKSPACE / "organvm" / "organvm-corpvs-testamentvm" / "data" / "atoms"
INPUT_FILE = ATOMS_DIR / "atomized-tasks.jsonl"
OUTPUT_FILE = ATOMS_DIR / "plan-tasks-triaged.jsonl"

SKIP_DIRS = {
    "node_modules",
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".next",
    ".turbo",
    "dist",
    ".tox",
    ".eggs",
}

# File extensions that signal a real file path
FILE_EXTENSIONS = {
    "py", "ts", "tsx", "js", "jsx", "json", "yaml", "yml", "toml", "md",
    "sh", "zsh", "tmpl", "bats", "css", "html", "plist", "conf", "cfg",
    "txt", "lock", "sql", "rs", "go", "lua", "vim", "ini", "env", "xml",
    "svg", "png", "jpg", "wasm", "rb", "rake", "gemspec", "swift",
    "jsonl", "csv", "nix", "tf", "hcl", "dockerfile",
}

# ---------------------------------------------------------------------------
# Phase 1: Build filesystem index
# ---------------------------------------------------------------------------


def build_file_index(root: Path) -> tuple[set[str], set[str], set[str]]:
    """Walk ~/Workspace/ and return three indexes:
    - all_files: set of relative paths from Workspace root
    - all_dirs: set of relative directory paths
    - basenames: set of all filenames (for fuzzy matching)
    """
    all_files: set[str] = set()
    all_dirs: set[str] = set()
    basenames: set[str] = set()

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skipped directories in-place
        dirnames[:] = [
            d
            for d in dirnames
            if d not in SKIP_DIRS and not d.endswith(".egg-info")
        ]

        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir != ".":
            all_dirs.add(rel_dir)

        for fname in filenames:
            rel_path = os.path.join(rel_dir, fname) if rel_dir != "." else fname
            all_files.add(rel_path)
            basenames.add(fname)

    return all_files, all_dirs, basenames


# ---------------------------------------------------------------------------
# Phase 2: Extract verifiable signals from tasks
# ---------------------------------------------------------------------------

# Pattern 1: Paths with extensions (e.g., src/foo/bar.py)
FILE_PATH_RE = re.compile(
    r"(?:^|[\s`|\"'(\[{,])("
    r"(?:~/Workspace/)?"
    r"(?:[\w.@-]+/)+"
    r"[\w.@-]+"
    r"\.(?:" + "|".join(FILE_EXTENSIONS) + ")"
    r")(?:[\s`|\"'),;:\]}]|$)",
    re.IGNORECASE,
)

# Pattern 2: Backtick-enclosed paths (e.g., `foo/bar.py` or `dot_config/zsh/15-env.zsh.tmpl`)
BACKTICK_PATH_RE = re.compile(
    r"`("
    r"(?:[\w.@~/-]+/)+"  # at least one dir separator
    r"[\w.@-]+"
    r"(?:\.[\w]+)?"  # optional extension
    r")`"
)

# Pattern 3: Standalone filenames with extensions in backticks (e.g., `ignition.sh`)
BACKTICK_FILE_RE = re.compile(
    r"`([\w.-]+\.(?:" + "|".join(FILE_EXTENSIONS) + "))`",
    re.IGNORECASE,
)


def extract_file_refs(text: str) -> list[str]:
    """Extract file path references from text (raw_text + title)."""
    refs = set()

    for pattern in [FILE_PATH_RE, BACKTICK_PATH_RE]:
        for match in pattern.finditer(text):
            path = match.group(1)
            path = path.replace("~/Workspace/", "")
            # Skip things that are clearly not paths
            if path.startswith("http") or path.startswith("git@"):
                continue
            refs.add(path)

    for match in BACKTICK_FILE_RE.finditer(text):
        fname = match.group(1)
        if not fname.startswith("http"):
            refs.add(fname)

    return list(refs)


def resolve_repo_dir(task: dict) -> Optional[str]:
    """Try to find the workspace directory for a task's project from slug or source."""
    project = task.get("project", {})
    slug = project.get("slug", "")
    source_file = task.get("source", {}).get("file", "")

    # Strategy 1: from slug (e.g., "organvm/essay-pipeline/.claude/plans")
    if slug and "/" in slug and not slug.startswith("_"):
        parts = slug.split("/")
        if len(parts) >= 2:
            candidate = f"{parts[0]}/{parts[1]}"
            if not candidate.startswith("."):
                return candidate

    # Strategy 2: from source file path
    if source_file and "/" in source_file:
        parts = source_file.split("/")
        if len(parts) >= 2 and not parts[0].endswith(".md"):
            return f"{parts[0]}/{parts[1]}"

    return None


def is_archived_source(task: dict) -> bool:
    """Check if the task originates from an archived plan."""
    source_file = task.get("source", {}).get("file", "")
    slug = task.get("project", {}).get("slug", "")

    return (
        source_file.startswith(".archive/")
        or slug.startswith(".archive/")
        or "/archive/" in source_file.lower()
    )


# ---------------------------------------------------------------------------
# Phase 3: Verification logic
# ---------------------------------------------------------------------------


def check_file_exists(
    file_path: str, all_files: set[str], basenames: set[str]
) -> tuple[bool, str]:
    """Check if a file reference exists in the workspace."""
    if file_path in all_files:
        return True, "direct_match"

    basename = os.path.basename(file_path)
    if basename in basenames:
        return True, "basename_match"

    return False, "not_found"


def check_dir_exists(dir_path: str, all_dirs: set[str]) -> bool:
    """Check if a directory exists in the workspace index."""
    if dir_path in all_dirs:
        return True
    for d in all_dirs:
        if d.endswith("/" + dir_path):
            return True
    return False


def gather_all_refs(task: dict) -> list[str]:
    """Gather all file references from a task (files_touched + raw_text + title)."""
    refs = []

    # From files_touched
    for ft in task.get("files_touched", []):
        path = ft.get("path", "")
        if path:
            refs.append(path)

    # From raw_text
    refs.extend(extract_file_refs(task.get("raw_text", "")))

    # From title
    refs.extend(extract_file_refs(task.get("title", "")))

    # Deduplicate while preserving order
    seen = set()
    unique = []
    for r in refs:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    return unique


def check_delete_task(
    task: dict,
    all_files: set[str],
    all_dirs: set[str],
    basenames: set[str],
) -> tuple[str, str]:
    """For delete tasks: success = target is gone."""
    refs = gather_all_refs(task)
    if not refs:
        return "unverifiable", "no_target_paths_found"

    for ref in refs:
        exists, _ = check_file_exists(ref, all_files, basenames)
        if exists:
            return "verified_open", "delete_targets_still_exist"

    return "verified_complete", "delete_targets_absent"


def check_create_task(
    task: dict,
    all_files: set[str],
    all_dirs: set[str],
    basenames: set[str],
) -> tuple[str, str]:
    """For create_file tasks: success = file exists."""
    refs = gather_all_refs(task)
    if not refs:
        return "unverifiable", "no_target_paths_found"

    found = sum(1 for r in refs if check_file_exists(r, all_files, basenames)[0])
    if found > 0:
        return "verified_complete", f"created_files_exist ({found}/{len(refs)})"
    return "verified_open", "created_files_not_found"


def check_modify_task(
    task: dict,
    all_files: set[str],
    all_dirs: set[str],
    basenames: set[str],
) -> tuple[str, str]:
    """For modify_file/configure: target file must exist to be actionable."""
    refs = gather_all_refs(task)
    if not refs:
        return "unverifiable", "no_target_paths_found"

    found = sum(1 for r in refs if check_file_exists(r, all_files, basenames)[0])
    if found == 0:
        return "verified_open", "target_files_missing"
    # File exists but content change unverifiable
    return "unverifiable", "target_exists_content_unverifiable"


def check_generic_file_refs(
    task: dict,
    all_files: set[str],
    basenames: set[str],
) -> tuple[Optional[str], Optional[str]]:
    """For any task type, check if referenced files exist as a signal."""
    refs = gather_all_refs(task)
    if not refs:
        return None, None

    found = sum(1 for r in refs if check_file_exists(r, all_files, basenames)[0])
    if found > 0:
        return "likely_complete", f"referenced_files_exist ({found}/{len(refs)})"
    return None, None


def check_repo_dir(task: dict, all_dirs: set[str]) -> tuple[Optional[str], Optional[str]]:
    """Check if the task's repo directory exists."""
    repo_dir = resolve_repo_dir(task)
    if not repo_dir:
        return None, None

    if check_dir_exists(repo_dir, all_dirs):
        return None, None  # Exists, not conclusive

    # Check if archived
    repo_name = repo_dir.split("/")[-1] if "/" in repo_dir else repo_dir
    for d in all_dirs:
        if repo_name in d and ".archive" in d:
            return "archived_moot", f"repo_archived ({repo_dir})"

    return "verified_open", f"repo_dir_missing ({repo_dir})"


def check_source_plan(task: dict, all_files: set[str]) -> Optional[bool]:
    """Check if the plan file that generated this task still exists in the workspace."""
    source = task.get("source", {}).get("file", "")
    if not source or source.endswith(".md") and "/" not in source:
        # Bare filename, can't locate reliably
        return None
    return source in all_files


# ---------------------------------------------------------------------------
# Top-level verification dispatchers
# ---------------------------------------------------------------------------


def verify_completed_task(
    task: dict,
    all_files: set[str],
    all_dirs: set[str],
    basenames: set[str],
) -> tuple[str, str]:
    """Verify a task already marked as completed."""
    task_type = task.get("task_type", "")

    # Archived source -> trust the completion
    if is_archived_source(task):
        return "confirmed_complete", "completed_and_archived"

    if task_type == "delete_file":
        status, reason = check_delete_task(task, all_files, all_dirs, basenames)
        if status == "verified_complete":
            return "confirmed_complete", reason
        elif status == "verified_open":
            return "disputed_completion", reason
        return "unverifiable_completion", reason

    elif task_type == "create_file":
        status, reason = check_create_task(task, all_files, all_dirs, basenames)
        if status == "verified_complete":
            return "confirmed_complete", reason
        elif status == "verified_open":
            return "disputed_completion", reason
        return "unverifiable_completion", reason

    elif task_type in ("modify_file", "configure"):
        refs = gather_all_refs(task)
        if refs:
            found = sum(
                1 for r in refs if check_file_exists(r, all_files, basenames)[0]
            )
            if found > 0:
                return "confirmed_complete", f"target_files_present ({found}/{len(refs)})"
        return "unverifiable_completion", "no_file_evidence"

    # For non-file tasks, check repo health
    repo_status, repo_reason = check_repo_dir(task, all_dirs)
    if repo_status == "verified_open":
        return "disputed_completion", repo_reason
    if repo_status == "archived_moot":
        return "confirmed_complete", "completed_and_repo_archived"

    # Check if source plan exists (completed task with existing plan = trust it)
    plan_exists = check_source_plan(task, all_files)
    if plan_exists is True:
        return "confirmed_complete", "source_plan_exists_trusting_status"
    if plan_exists is False:
        return "unverifiable_completion", "source_plan_missing"

    return "unverifiable_completion", "no_filesystem_evidence"


def verify_pending_task(
    task: dict,
    all_files: set[str],
    all_dirs: set[str],
    basenames: set[str],
) -> tuple[str, str]:
    """Check if a pending task is actually already done, moot, or legitimately open."""
    task_type = task.get("task_type", "")

    # Gate 0: archived source -> moot regardless
    if is_archived_source(task):
        return "archived_moot", "plan_in_archive"

    # Gate 1: repo/project directory check
    repo_status, repo_reason = check_repo_dir(task, all_dirs)
    if repo_status == "archived_moot":
        return "archived_moot", repo_reason
    if repo_status == "verified_open":
        return "verified_open", repo_reason

    # Gate 2: type-specific checks
    if task_type == "delete_file":
        return check_delete_task(task, all_files, all_dirs, basenames)

    elif task_type == "create_file":
        return check_create_task(task, all_files, all_dirs, basenames)

    elif task_type in ("modify_file", "configure"):
        status, reason = check_modify_task(task, all_files, all_dirs, basenames)
        if status != "unverifiable":
            return status, reason
        # Fall through to generic checks

    elif task_type == "write_test":
        refs = gather_all_refs(task)
        test_refs = [
            r
            for r in refs
            if "test" in r.lower() or ".bats" in r or "spec" in r.lower()
        ]
        if test_refs:
            found = sum(
                1 for r in test_refs if check_file_exists(r, all_files, basenames)[0]
            )
            if found > 0:
                return "likely_complete", f"test_files_exist ({found}/{len(test_refs)})"

    elif task_type == "document":
        refs = gather_all_refs(task)
        doc_refs = [r for r in refs if r.endswith(".md") or r.endswith(".rst")]
        if doc_refs:
            found = sum(
                1 for r in doc_refs if check_file_exists(r, all_files, basenames)[0]
            )
            if found > 0:
                return "likely_complete", f"doc_files_exist ({found}/{len(doc_refs)})"

    elif task_type == "deploy":
        refs = gather_all_refs(task)
        if refs:
            found = sum(
                1 for r in refs if check_file_exists(r, all_files, basenames)[0]
            )
            if found > 0:
                return "likely_complete", f"deploy_artifacts_exist ({found}/{len(refs)})"

    # Gate 3: generic file reference check (for any type including 'generic')
    file_status, file_reason = check_generic_file_refs(task, all_files, basenames)
    if file_status:
        return file_status, file_reason

    # Gate 4: source plan existence
    plan_exists = check_source_plan(task, all_files)
    if plan_exists is False:
        # Plan file gone = likely the work was done and cleaned up, or project restructured
        return "unverifiable", "source_plan_missing"

    return "unverifiable", "no_filesystem_signal"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print("=" * 70)
    print("Plan Task Reality Check")
    print("=" * 70)

    # Phase 1: Build index
    print(f"\n[1/3] Building filesystem index of {WORKSPACE} ...")
    t0 = time.time()
    all_files, all_dirs, basenames = build_file_index(WORKSPACE)
    dt = time.time() - t0
    print(f"  Indexed {len(all_files):,} files, {len(all_dirs):,} dirs in {dt:.1f}s")
    print(f"  Unique basenames: {len(basenames):,}")

    # Phase 2: Load tasks
    print(f"\n[2/3] Loading tasks from {INPUT_FILE.name} ...")
    tasks = []
    with open(INPUT_FILE) as f:
        for line in f:
            line = line.strip()
            if line:
                tasks.append(json.loads(line))
    print(f"  Loaded {len(tasks):,} tasks")

    # Phase 3: Verify each task
    print("\n[3/3] Verifying tasks against filesystem ...")
    t0 = time.time()

    stats: dict[str, int] = {}
    original_status_counts: dict[str, int] = {}

    results = []
    for task in tasks:
        original_status = task.get("status", "pending")
        original_status_counts[original_status] = (
            original_status_counts.get(original_status, 0) + 1
        )

        if original_status == "completed":
            new_status, reason = verify_completed_task(
                task, all_files, all_dirs, basenames
            )
        else:
            new_status, reason = verify_pending_task(
                task, all_files, all_dirs, basenames
            )

        stats[new_status] = stats.get(new_status, 0) + 1

        out = dict(task)
        out["triage"] = {
            "original_status": original_status,
            "verified_status": new_status,
            "reason": reason,
        }
        results.append(out)

    dt = time.time() - t0
    print(f"  Verified {len(results):,} tasks in {dt:.1f}s")

    # Write output
    print(f"\n  Writing {OUTPUT_FILE.name} ...")
    with open(OUTPUT_FILE, "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"  Written: {OUTPUT_FILE}")

    # Print results
    total = len(tasks)

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print("\nOriginal status distribution:")
    for k, v in sorted(original_status_counts.items(), key=lambda x: -x[1]):
        print(f"  {k:>25s}: {v:>6,} ({100 * v / total:5.1f}%)")

    print("\nVerified status distribution:")
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        print(f"  {k:>25s}: {v:>6,} ({100 * v / total:5.1f}%)")

    # Category aggregation
    actually_done = (
        stats.get("verified_complete", 0)
        + stats.get("confirmed_complete", 0)
        + stats.get("likely_complete", 0)
    )
    actually_open = stats.get("verified_open", 0)
    archived = stats.get("archived_moot", 0)
    disputed = stats.get("disputed_completion", 0)
    unverifiable_total = stats.get("unverifiable", 0) + stats.get(
        "unverifiable_completion", 0
    )

    print(f"\n{'=' * 50}")
    print("  SUMMARY")
    print(f"{'=' * 50}")
    print(
        f"  {'Verified COMPLETE':>25s}: {actually_done:>6,} ({100 * actually_done / total:5.1f}%)"
    )
    print(
        f"  {'Verified OPEN':>25s}: {actually_open:>6,} ({100 * actually_open / total:5.1f}%)"
    )
    print(
        f"  {'Archived / moot':>25s}: {archived:>6,} ({100 * archived / total:5.1f}%)"
    )
    print(
        f"  {'Disputed completions':>25s}: {disputed:>6,} ({100 * disputed / total:5.1f}%)"
    )
    print(
        f"  {'Unable to verify':>25s}: {unverifiable_total:>6,} ({100 * unverifiable_total / total:5.1f}%)"
    )
    print(f"{'=' * 50}")
    print(f"  {'TOTAL':>25s}: {total:>6,}")

    # Status change analysis
    orig_complete = original_status_counts.get("completed", 0)
    orig_pending = original_status_counts.get("pending", 0)
    newly_done = stats.get("verified_complete", 0) + stats.get("likely_complete", 0)

    print(f"\n{'=' * 50}")
    print("  STATUS CHANGES")
    print(f"{'=' * 50}")
    print(
        f"  Was 'completed' ({orig_complete:,}):"
    )
    print(
        f"    confirmed:  {stats.get('confirmed_complete', 0):,}"
    )
    print(
        f"    disputed:   {disputed:,}"
    )
    print(
        f"    unverified: {stats.get('unverifiable_completion', 0):,}"
    )
    print(
        f"  Was 'pending' ({orig_pending:,}):"
    )
    print(
        f"    now done:       {newly_done:,}"
    )
    print(
        f"    archived/moot:  {archived:,}"
    )
    print(
        f"    confirmed open: {actually_open:,}"
    )
    print(
        f"    unverifiable:   {stats.get('unverifiable', 0):,}"
    )
    net_pending = orig_pending - newly_done - archived - actually_open
    print(
        "\n  Net unresolved (pending - done - archived - confirmed_open):"
    )
    print(
        f"    {net_pending:,} tasks still in limbo"
    )
    real_backlog = actually_open + stats.get("unverifiable", 0)
    print(
        "  True backlog (confirmed_open + unverifiable):"
    )
    print(
        f"    {real_backlog:,} tasks"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
