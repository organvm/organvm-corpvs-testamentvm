#!/usr/bin/env python3
"""CONVERGENCE Sprint Phase B: Deploy provenance materials to 7 DESIGN_ONLY repos.

Reads provenance-registry.json, finds files classified to each DESIGN_ONLY repo,
reads them from the local filesystem, and deploys via GitHub Contents API (gh CLI).
Marks entries as deployed in the provenance registry.
"""

import json
import subprocess
import base64
import time
import sys
from pathlib import Path

PROVENANCE_PATH = Path(__file__).parent.parent / "provenance-registry.json"
REGISTRY_PATH = Path(__file__).parent.parent / "repo-registry.json"

# 7 DESIGN_ONLY repos and their deploy path mappings
DEPLOY_TARGETS = {
    "organvm-vi-koinonia/adaptive-personal-syllabus": {
        "deploy_root": "docs/",
        "description": "Curriculum, modules, and wing materials",
    },
    "organvm-ii-poiesis/universal-waveform-explorer": {
        "deploy_root": "docs/synthwave/",
        "description": "Synthwave and waveform exploration materials",
    },
    "organvm-ii-poiesis/life-betterment-simulation": {
        "deploy_root": "docs/design/",
        "description": "Simulation design documents",
    },
    "organvm-iii-ergon/hokage-chess": {
        "deploy_root": "docs/strategy/",
        "description": "Strategy and game design documents",
    },
    "organvm-iii-ergon/card-trade-social": {
        "deploy_root": "docs/design/",
        "description": "Card trading platform design docs",
    },
    "organvm-ii-poiesis/shared-remembrance-gateway": {
        "deploy_root": "docs/",
        "description": "Shared remembrance project docs",
    },
    "organvm-i-theoria/scalable-lore-expert": {
        "deploy_root": "docs/",
        "description": "Lore expert theory documents",
    },
}

# File extensions to skip (binary, generated, or irrelevant)
SKIP_EXTENSIONS = {
    ".DS_Store", ".pyc", ".pyo", ".o", ".so", ".dylib",
    ".lock", ".log", ".tmp", ".swp",
}

SKIP_FILENAMES = {
    ".DS_Store", "Thumbs.db", ".dbxignore", "npm-install.log",
    "package-lock.json", "node_modules",
}


def gh_api_put(org, repo, path, content_bytes, message, branch=None):
    """Create or update a file via GitHub Contents API using stdin for large payloads."""
    endpoint = f"/repos/{org}/{repo}/contents/{path}"

    # Check for existing file SHA
    sha_result = subprocess.run(
        ["gh", "api", "-X", "GET", endpoint],
        capture_output=True, text=True,
    )
    sha = None
    if sha_result.returncode == 0:
        try:
            existing = json.loads(sha_result.stdout)
            sha = existing.get("sha")
        except json.JSONDecodeError:
            pass

    b64_content = base64.b64encode(content_bytes).decode("utf-8")

    payload = {
        "message": message,
        "content": b64_content,
    }
    if sha:
        payload["sha"] = sha
    if branch:
        payload["branch"] = branch

    # Use --input - for ARG_MAX safety
    result = subprocess.run(
        ["gh", "api", "-X", "PUT", endpoint, "--input", "-"],
        input=json.dumps(payload),
        capture_output=True, text=True,
    )

    if result.returncode != 0:
        err = result.stderr.strip()[:200]
        print(f"    FAIL {path}: {err}")
        return False
    return True


def get_default_branch(org, repo):
    """Get the default branch of a repo."""
    result = subprocess.run(
        ["gh", "api", f"/repos/{org}/{repo}", "--jq", ".default_branch"],
        capture_output=True, text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return "main"


def is_repo_archived(org, repo):
    """Check if a repo is archived on GitHub."""
    result = subprocess.run(
        ["gh", "api", f"/repos/{org}/{repo}", "--jq", ".archived"],
        capture_output=True, text=True,
    )
    return result.returncode == 0 and result.stdout.strip() == "true"


def compute_deploy_path(source_path, target_key, deploy_root):
    """Compute the deployment path within the target repo.

    Preserves subdirectory structure relative to the project root.
    """
    source = Path(source_path)
    filename = source.name

    # Try to preserve some directory structure from the source
    # e.g., ~/Workspace/ProjectX/subdir/file.md -> docs/subdir/file.md
    parts = source.parts
    # Find the project directory (child of Workspace)
    workspace_idx = None
    for i, part in enumerate(parts):
        if part == "Workspace":
            workspace_idx = i
            break

    if workspace_idx is not None and workspace_idx + 2 < len(parts):
        # Path relative to the project dir
        rel_parts = parts[workspace_idx + 2:]  # skip Workspace/ProjectDir
        rel_path = "/".join(rel_parts)
        return f"{deploy_root}{rel_path}"

    return f"{deploy_root}{filename}"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="CONVERGENCE Phase B: Deploy materials")
    parser.add_argument("--dry-run", action="store_true", help="Preview without deploying")
    parser.add_argument("--repo", type=str, help="Deploy to specific repo (org/repo)")
    parser.add_argument("--limit", type=int, default=0, help="Limit files per repo (0=all)")
    args = parser.parse_args()

    # Load provenance registry
    with open(PROVENANCE_PATH) as f:
        provenance = json.load(f)

    source_map = provenance["source_to_repo"]

    # Group files by target repo
    repo_files = {}
    for source_path, entry in source_map.items():
        target = entry.get("target", "")
        if target in DEPLOY_TARGETS:
            if target not in repo_files:
                repo_files[target] = []
            repo_files[target].append((source_path, entry))

    if args.repo:
        if args.repo not in repo_files:
            print(f"No provenance files found for {args.repo}")
            print(f"Available targets: {list(repo_files.keys())}")
            sys.exit(1)
        repo_files = {args.repo: repo_files[args.repo]}

    total_deployed = 0
    total_failed = 0
    total_skipped = 0

    for target_key, files in sorted(repo_files.items()):
        org, repo = target_key.split("/")
        config = DEPLOY_TARGETS[target_key]
        deploy_root = config["deploy_root"]

        print(f"\n{'='*60}")
        print(f"Target: {target_key} ({len(files)} files)")
        print(f"Deploy root: {deploy_root}")
        print(f"Description: {config['description']}")

        if not args.dry_run:
            # Check if repo is archived
            if is_repo_archived(org, repo):
                print("  SKIP: repo is archived on GitHub")
                total_skipped += len(files)
                continue

            branch = get_default_branch(org, repo)
            print(f"  Branch: {branch}")
        else:
            branch = "main"

        deployed_count = 0
        for i, (source_path, entry) in enumerate(files):
            if args.limit and i >= args.limit:
                print(f"  ... (limit reached, {len(files) - args.limit} more)")
                break

            source = Path(source_path)

            # Skip irrelevant files
            if source.name in SKIP_FILENAMES or source.suffix in SKIP_EXTENSIONS:
                print(f"  SKIP {source.name} (excluded pattern)")
                total_skipped += 1
                continue

            # Check file exists locally
            if not source.exists():
                print(f"  SKIP {source.name} (not found locally)")
                total_skipped += 1
                continue

            deploy_path = compute_deploy_path(source_path, target_key, deploy_root)
            message = f"docs: deploy {source.name} from provenance (CONVERGENCE Sprint)"

            if args.dry_run:
                print(f"  [{i+1}/{len(files)}] Would deploy: {source.name} -> {deploy_path}")
                deployed_count += 1
            else:
                print(f"  [{i+1}/{len(files)}] {source.name} -> {deploy_path}...", end=" ", flush=True)
                try:
                    content = source.read_bytes()
                    if gh_api_put(org, repo, deploy_path, content, message, branch):
                        print("OK")
                        # Mark as deployed in provenance
                        entry["deployed"] = True
                        entry["deployed_path"] = f"{org}/{repo}/{deploy_path}"
                        deployed_count += 1
                        total_deployed += 1
                    else:
                        total_failed += 1
                except Exception as e:
                    print(f"ERROR: {e}")
                    total_failed += 1

                # Rate limit
                time.sleep(1)

        print(f"  Result: {deployed_count}/{len(files)} deployed")

    # Save updated provenance registry
    if not args.dry_run and total_deployed > 0:
        with open(PROVENANCE_PATH, "w") as f:
            json.dump(provenance, f, indent=2)
        print(f"\nProvenance registry updated with {total_deployed} deployment records.")

    print(f"\n{'='*60}")
    print(f"SUMMARY: {total_deployed} deployed, {total_failed} failed, {total_skipped} skipped")


if __name__ == "__main__":
    main()
