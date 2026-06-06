#!/usr/bin/env python3
"""
Workspace restructure: ~/world/realm/ → ~/Workspace/<org>/<repo>/

Moves organ-system repos from the 7-level ontological hierarchy into a flat
2-level structure that mirrors GitHub exactly.

Usage:
    python3 scripts/restructure-workspace.py                  # Dry run (default)
    python3 scripts/restructure-workspace.py --execute        # Execute all moves
    python3 scripts/restructure-workspace.py --rollback LOG   # Reverse from log file
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HOME = Path.home()
WORKSPACE = HOME / "Workspace"
WORLD_REALM = HOME / "world" / "realm"
SCRIPT_DIR = Path(__file__).parent
REGISTRY_PATH = SCRIPT_DIR.parent / "repo-registry.json"

ORG_DIRS = [
    "organvm-i-theoria",
    "organvm-ii-poiesis",
    "organvm-iii-ergon",
    "organvm-iv-taxis",
    "organvm-v-logos",
    "organvm-vi-koinonia",
    "organvm-vii-kerygma",
    "meta-organvm",
]

STALE_DIRS = [
    "4444j99-community",
    "4444j99-marketing",
    "4444j99-orchestration",
    "4444j99-organs",
]

# Explicit name mappings for content dirs where spelling differs
CONTENT_NAME_MAP = {
    "shared-remembrance-gateway": "shared-rememberance-gateway",  # registry → workspace (misspelled)
}


def normalize_name(github_name: str) -> str:
    """Normalize a GitHub repo name to match local directory naming."""
    return github_name.replace("--", "-").rstrip("-").lower()


def discover_world_repos() -> dict[str, Path]:
    """Find all git repos in ~/world/realm/, keyed by normalized name."""
    repos = {}
    for root, dirs, _files in os.walk(WORLD_REALM):
        if ".git" in dirs:
            path = Path(root)
            normalized = path.name.lower()
            repos[normalized] = path
            dirs.clear()  # don't recurse into .git subtrees
        # Also don't recurse into .git dirs themselves
        if ".git" in dirs:
            dirs.remove(".git")
    return repos


def discover_world_non_git_dirs() -> dict[str, Path]:
    """Find directories in ~/world/realm/ under repo/ level that lack .git."""
    dirs_found = {}
    for realm in WORLD_REALM.iterdir():
        if not realm.is_dir():
            continue
        for org_dir in (realm / "org").iterdir() if (realm / "org").is_dir() else []:
            repo_parent = org_dir / "repo"
            if not repo_parent.is_dir():
                continue
            for repo_dir in repo_parent.iterdir():
                if repo_dir.is_dir() and not (repo_dir / ".git").is_dir():
                    normalized = repo_dir.name.lower()
                    dirs_found[normalized] = repo_dir
    return dirs_found


def discover_workspace() -> tuple[dict[str, Path], dict[str, Path], list[Path]]:
    """Categorize ~/Workspace/ contents into git dirs, content dirs, and symlinks."""
    git_dirs = {}
    content_dirs = {}
    symlinks = []

    for item in WORKSPACE.iterdir():
        if item.is_symlink():
            symlinks.append(item)
        elif item.is_dir():
            name = item.name
            if (item / ".git").is_dir():
                git_dirs[name] = item
            else:
                content_dirs[name] = item

    return git_dirs, content_dirs, symlinks


# ISOTOPE DISSOLUTION: Gate memory--remember G2 (CORPUS_SCRIPTS_DISSOLVED)
try:
    from organvm_engine.registry.loader import load_registry as _engine_load
except ImportError:
    _engine_load = None


def load_registry() -> list[dict]:
    """Load all repos from repo-registry.json."""
    if _engine_load is not None:
        data = _engine_load(REGISTRY_PATH)
    else:
        with open(REGISTRY_PATH) as f:
            data = json.load(f)
    repos = []
    for organ_key, organ_data in data["organs"].items():
        for repo in organ_data["repositories"]:
            repos.append({
                "organ": organ_key,
                "org": repo["org"],
                "name": repo["name"],
                "status": repo.get("implementation_status", repo.get("status")),
            })
    return repos


def get_remote_url(repo_path: Path) -> str | None:
    """Get the current origin remote URL for a git repo."""
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def build_plan() -> dict:
    """Build the complete restructure plan."""
    registry = load_registry()
    world_repos = discover_world_repos()
    world_non_git = discover_world_non_git_dirs()
    ws_git, ws_content, ws_symlinks = discover_workspace()

    plan = {
        "create_dirs": [],
        "moves_world": [],       # git repos from ~/world/
        "moves_workspace": [],   # git dirs from ~/Workspace/
        "content_moves": [],     # non-git content dirs
        "merge_cases": [],       # agentic-titan-style: git + content
        "symlinks_remove": [],
        "dirs_remove": [],
        "remote_updates": [],    # populated after moves
        "corpus_move": None,
        "skipped": [],
    }

    # Step 1: org directories
    for org in ORG_DIRS:
        org_path = WORKSPACE / org
        if not org_path.exists():
            plan["create_dirs"].append(str(org_path))

    # Track which workspace items we plan to move (to avoid double-handling)
    ws_items_claimed = set()

    # Step 2-4: match registry repos to local sources
    for repo in registry:
        org = repo["org"]
        name = repo["name"]
        dest = WORKSPACE / org / name

        # Skip .github infra repos
        if name == ".github":
            plan["skipped"].append(f"{org}/{name} — infrastructure, skip")
            continue

        # Skip if destination already exists
        if dest.exists() and not dest.is_symlink():
            plan["skipped"].append(f"{org}/{name} — already at destination")
            continue

        normalized = normalize_name(name)
        found = False

        # --- Source 1: git repo in ~/world/ ---
        if normalized in world_repos:
            source = world_repos[normalized]
            remote_url = f"https://github.com/{org}/{name}.git"

            # Check for merge case: git repo in ~/world/ AND content dir in ~/Workspace/
            ws_content_name = None
            for candidate in [name, normalized, name.replace("--", "-")]:
                if candidate in ws_content and candidate not in ws_items_claimed:
                    ws_content_name = candidate
                    break

            if ws_content_name:
                # Merge case: move git repo first, then content into _local/
                plan["merge_cases"].append({
                    "git_source": str(source),
                    "content_source": str(ws_content[ws_content_name]),
                    "dest": str(dest),
                    "org": org,
                    "name": name,
                    "remote_url": remote_url,
                })
                ws_items_claimed.add(ws_content_name)
            else:
                plan["moves_world"].append({
                    "source": str(source),
                    "dest": str(dest),
                    "org": org,
                    "name": name,
                    "remote_url": remote_url,
                })
            found = True

        # --- Source 2: git dir in ~/Workspace/ ---
        if not found:
            for candidate in [name, normalized, name.replace("--", "-")]:
                if candidate in ws_git and candidate not in ws_items_claimed:
                    source = ws_git[candidate]
                    plan["moves_workspace"].append({
                        "source": str(source),
                        "dest": str(dest),
                        "org": org,
                        "name": name,
                        "remote_url": f"https://github.com/{org}/{name}.git",
                    })
                    ws_items_claimed.add(candidate)
                    found = True
                    break

        # --- Source 3: non-git content dir in ~/Workspace/ ---
        if not found:
            # Check direct name matches and spelling variants
            candidates = [name, normalized, name.replace("--", "-")]
            if name in CONTENT_NAME_MAP:
                candidates.append(CONTENT_NAME_MAP[name])

            for candidate in candidates:
                if candidate in ws_content and candidate not in ws_items_claimed:
                    plan["content_moves"].append({
                        "source": str(ws_content[candidate]),
                        "dest": str(dest),
                        "org": org,
                        "name": name,
                    })
                    ws_items_claimed.add(candidate)
                    found = True
                    break

        # --- Source 4: non-git dir in ~/world/ ---
        if not found:
            if normalized in world_non_git:
                source = world_non_git[normalized]
                plan["content_moves"].append({
                    "source": str(source),
                    "dest": str(dest),
                    "org": org,
                    "name": name,
                    "note": "non-git dir from ~/world/",
                })
                found = True

        if not found:
            plan["skipped"].append(f"{org}/{name} — no local clone found (remote-only)")

    # Step 5: symlinks pointing to ~/world/
    for link in ws_symlinks:
        target = str(os.readlink(link))
        if "/world/" in target:
            plan["symlinks_remove"].append(str(link))

    # Stale 4444j99-* directories
    for d in STALE_DIRS:
        path = WORKSPACE / d
        if path.exists():
            plan["dirs_remove"].append(str(path))

    # Step 7: corpus move
    corpus_src = WORKSPACE / "organvm-pactvm" / "ingesting-organ-document-structure"
    corpus_dest = WORKSPACE / "meta-organvm" / "organvm-corpvs-testamentvm"
    if corpus_src.exists() and not corpus_dest.exists():
        plan["corpus_move"] = {
            "source": str(corpus_src),
            "dest": str(corpus_dest),
            "remote_url": "https://github.com/meta-organvm/organvm-corpvs-testamentvm.git",
        }

    return plan


def print_plan(plan: dict) -> None:
    """Print a human-readable summary of the plan."""
    print("=" * 70)
    print("WORKSPACE RESTRUCTURE PLAN")
    print("=" * 70)

    if plan["create_dirs"]:
        print(f"\n📁 CREATE {len(plan['create_dirs'])} org directories:")
        for d in plan["create_dirs"]:
            print(f"   mkdir {d}")

    if plan["moves_world"]:
        print(f"\n📦 MOVE {len(plan['moves_world'])} git repos from ~/world/:")
        for m in plan["moves_world"]:
            src = m["source"].replace(str(HOME), "~")
            dst = m["dest"].replace(str(HOME), "~")
            print(f"   {src}")
            print(f"     → {dst}")

    if plan["moves_workspace"]:
        print(f"\n📦 MOVE {len(plan['moves_workspace'])} git repos within ~/Workspace/:")
        for m in plan["moves_workspace"]:
            src = m["source"].replace(str(HOME), "~")
            dst = m["dest"].replace(str(HOME), "~")
            print(f"   {src}")
            print(f"     → {dst}")

    if plan["merge_cases"]:
        print(f"\n🔀 MERGE {len(plan['merge_cases'])} repos (git + content dir):")
        for m in plan["merge_cases"]:
            git_src = m["git_source"].replace(str(HOME), "~")
            content_src = m["content_source"].replace(str(HOME), "~")
            dst = m["dest"].replace(str(HOME), "~")
            print(f"   git:     {git_src}")
            print(f"   content: {content_src}")
            print(f"     → {dst} (content → _local/)")

    if plan["content_moves"]:
        print(f"\n📄 MOVE {len(plan['content_moves'])} content dirs (non-git):")
        for m in plan["content_moves"]:
            src = m["source"].replace(str(HOME), "~")
            dst = m["dest"].replace(str(HOME), "~")
            note = m.get("note", "")
            print(f"   {src}")
            print(f"     → {dst}" + (f"  ({note})" if note else ""))

    if plan["symlinks_remove"]:
        print(f"\n🔗 REMOVE {len(plan['symlinks_remove'])} symlinks:")
        for s in plan["symlinks_remove"]:
            print(f"   rm {s.replace(str(HOME), '~')}")

    if plan["dirs_remove"]:
        print(f"\n🗑  REMOVE {len(plan['dirs_remove'])} stale directories:")
        for d in plan["dirs_remove"]:
            print(f"   rm -rf {d.replace(str(HOME), '~')}")

    if plan["corpus_move"]:
        c = plan["corpus_move"]
        print(f"\n📜 CORPUS MOVE:")
        print(f"   {c['source'].replace(str(HOME), '~')}")
        print(f"     → {c['dest'].replace(str(HOME), '~')}")

    total_moves = (
        len(plan["moves_world"])
        + len(plan["moves_workspace"])
        + len(plan["merge_cases"])
        + len(plan["content_moves"])
    )
    total_remotes = total_moves + (1 if plan["corpus_move"] else 0)

    if plan["skipped"]:
        print(f"\n⏭  SKIPPED {len(plan['skipped'])} repos:")
        for s in plan["skipped"]:
            print(f"   {s}")

    print(f"\n{'=' * 70}")
    print(f"SUMMARY: {total_moves} moves, {len(plan['symlinks_remove'])} symlinks removed, "
          f"{len(plan['dirs_remove'])} stale dirs removed, "
          f"{total_remotes} remote updates")
    print(f"{'=' * 70}")


def execute_plan(plan: dict) -> Path:
    """Execute the restructure plan. Returns path to rollback log."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_path = SCRIPT_DIR / f"restructure-log-{timestamp}.jsonl"
    errors = []

    def log_action(action: dict):
        with open(log_path, "a") as f:
            f.write(json.dumps(action) + "\n")

    print(f"\nRollback log: {log_path}")
    print()

    # Step 1: create org directories
    for d in plan["create_dirs"]:
        print(f"  mkdir -p {d}")
        Path(d).mkdir(parents=True, exist_ok=True)
        log_action({"action": "mkdir", "path": d})

    # Step 2: move git repos from ~/world/
    for m in plan["moves_world"]:
        src, dst = m["source"], m["dest"]
        print(f"  mv {Path(src).name} → {Path(dst).parent.name}/{Path(dst).name}")
        try:
            # Ensure parent exists
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dst)
            log_action({"action": "move", "source": src, "dest": dst})
        except Exception as e:
            msg = f"  ERROR moving {src}: {e}"
            print(msg)
            errors.append(msg)
            continue

        # Update remote
        _update_remote(dst, m["remote_url"], log_action)

    # Step 3: move git repos within ~/Workspace/
    for m in plan["moves_workspace"]:
        src, dst = m["source"], m["dest"]
        print(f"  mv {Path(src).name} → {Path(dst).parent.name}/{Path(dst).name}")
        try:
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dst)
            log_action({"action": "move", "source": src, "dest": dst})
        except Exception as e:
            msg = f"  ERROR moving {src}: {e}"
            print(msg)
            errors.append(msg)
            continue

        _update_remote(dst, m["remote_url"], log_action)

    # Merge cases (e.g. agentic-titan)
    for m in plan["merge_cases"]:
        git_src = m["git_source"]
        content_src = m["content_source"]
        dst = m["dest"]
        print(f"  merge {Path(git_src).name} + content → {Path(dst).parent.name}/{Path(dst).name}")
        try:
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            # Move git repo first
            shutil.move(git_src, dst)
            log_action({"action": "move", "source": git_src, "dest": dst})

            # Move content into _local/ subdirectory
            local_dir = Path(dst) / "_local"
            local_dir.mkdir(exist_ok=True)
            for item in Path(content_src).iterdir():
                if item.name.startswith("."):
                    continue  # skip hidden files
                item_dest = local_dir / item.name
                shutil.move(str(item), str(item_dest))
            # Remove the now-empty content dir
            try:
                shutil.rmtree(content_src)
            except Exception:
                # May have hidden files left; remove those too
                shutil.rmtree(content_src, ignore_errors=True)
            log_action({
                "action": "merge_content",
                "content_source": content_src,
                "local_dir": str(local_dir),
            })
        except Exception as e:
            msg = f"  ERROR merging {git_src}: {e}"
            print(msg)
            errors.append(msg)
            continue

        _update_remote(dst, m["remote_url"], log_action)

    # Step 4: content-only moves
    for m in plan["content_moves"]:
        src, dst = m["source"], m["dest"]
        print(f"  mv (content) {Path(src).name} → {Path(dst).parent.name}/{Path(dst).name}")
        try:
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dst)
            log_action({"action": "move_content", "source": src, "dest": dst})
        except Exception as e:
            msg = f"  ERROR moving content {src}: {e}"
            print(msg)
            errors.append(msg)

    # Step 5: remove symlinks (capture target before removing)
    for s in plan["symlinks_remove"]:
        print(f"  rm (symlink) {Path(s).name}")
        try:
            target = os.readlink(s) if os.path.islink(s) else "?"
            os.remove(s)
            log_action({"action": "remove_symlink", "path": s, "target": str(target)})
        except FileNotFoundError:
            print(f"    (already gone)")
        except Exception as e:
            msg = f"  ERROR removing symlink {s}: {e}"
            print(msg)
            errors.append(msg)

    # Remove stale directories
    for d in plan["dirs_remove"]:
        print(f"  rm -rf (stale) {Path(d).name}")
        try:
            shutil.rmtree(d)
            log_action({"action": "remove_dir", "path": d})
        except Exception as e:
            msg = f"  ERROR removing {d}: {e}"
            print(msg)
            errors.append(msg)

    # Step 7: corpus move
    if plan["corpus_move"]:
        c = plan["corpus_move"]
        src, dst = c["source"], c["dest"]
        print(f"  mv (corpus) → {Path(dst).parent.name}/{Path(dst).name}")
        try:
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dst)
            log_action({"action": "move", "source": src, "dest": dst})
        except Exception as e:
            msg = f"  ERROR moving corpus: {e}"
            print(msg)
            errors.append(msg)
            return log_path

        _update_remote(dst, c["remote_url"], log_action)

    print()
    if errors:
        print(f"COMPLETED with {len(errors)} errors:")
        for e in errors:
            print(f"  {e}")
    else:
        print("COMPLETED successfully — all moves executed.")

    print(f"Rollback log: {log_path}")
    return log_path


def _update_remote(repo_path: str, target_url: str, log_fn) -> None:
    """Update git remote origin to the target HTTPS URL."""
    if not Path(repo_path).joinpath(".git").is_dir():
        return
    current = get_remote_url(Path(repo_path))
    if current and current != target_url:
        try:
            subprocess.run(
                ["git", "-C", repo_path, "remote", "set-url", "origin", target_url],
                capture_output=True, text=True, timeout=5,
            )
            log_fn({
                "action": "remote_update",
                "path": repo_path,
                "old_url": current,
                "new_url": target_url,
            })
            print(f"    remote: {current} → {target_url}")
        except Exception as e:
            print(f"    WARNING: failed to update remote for {repo_path}: {e}")


def rollback(log_path: str) -> None:
    """Reverse moves from a rollback log file."""
    actions = []
    with open(log_path) as f:
        for line in f:
            actions.append(json.loads(line))

    # Reverse in order
    for action in reversed(actions):
        if action["action"] == "move":
            src, dst = action["dest"], action["source"]
            print(f"  rollback: {src} → {dst}")
            Path(dst).parent.mkdir(parents=True, exist_ok=True)
            shutil.move(src, dst)
        elif action["action"] == "remote_update":
            old_url = action["old_url"]
            path = action["path"]
            print(f"  rollback remote: {path} → {old_url}")
            subprocess.run(
                ["git", "-C", path, "remote", "set-url", "origin", old_url],
                capture_output=True, text=True, timeout=5,
            )
        elif action["action"] == "remove_symlink":
            target = action.get("target")
            path = action["path"]
            if target and target != "?":
                print(f"  rollback symlink: {path} → {target}")
                os.symlink(target, path)
        elif action["action"] == "mkdir":
            path = action["path"]
            if Path(path).exists() and not any(Path(path).iterdir()):
                print(f"  rollback: rmdir {path}")
                Path(path).rmdir()

    print("Rollback complete.")


def main():
    parser = argparse.ArgumentParser(description="Restructure workspace directories")
    parser.add_argument("--execute", action="store_true", help="Execute the plan (default: dry run)")
    parser.add_argument("--rollback", metavar="LOG", help="Rollback from a log file")
    args = parser.parse_args()

    if args.rollback:
        rollback(args.rollback)
        return

    plan = build_plan()
    print_plan(plan)

    if not args.execute:
        print("\nDRY RUN — no changes made. Use --execute to apply.")
        return

    print("\nEXECUTING...")
    log_path = execute_plan(plan)
    print(f"\nDone. Log at: {log_path}")


if __name__ == "__main__":
    main()
