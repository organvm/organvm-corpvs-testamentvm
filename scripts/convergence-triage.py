#!/usr/bin/env python3
"""CONVERGENCE Sprint Phase D: Triage provenance None-target entries.

Resolves 961 entries with org/None targets by routing to specific repos,
marking as already-deployed, or marking as not-deployable.
"""

import json
from pathlib import Path
from collections import Counter

PROVENANCE_PATH = Path(__file__).parent.parent / "provenance-registry.json"

# === ROUTING RULES ===

# ORGAN-IV staging files -> specific repos
ORGAN_IV_ROUTING = {
    "orchestrator-agents/": ("organvm-iv-taxis", "agentic-titan", "agents/"),
    "coordination-protocols/": ("organvm-iv-taxis", "orchestration-start-here", "docs/coordination/"),
    "flow-patterns/": ("organvm-iv-taxis", "orchestration-start-here", "docs/flow-patterns/"),
    "dreamcatcher/": ("organvm-iv-taxis", "agentic-titan", "src/dreamcatcher/"),
    "metasystem-manifest/": ("organvm-iv-taxis", "orchestration-start-here", "docs/metasystem/"),
    "seed-schema/": ("organvm-iv-taxis", "orchestration-start-here", "docs/seed-schema/"),
    "deploy-tooling/": ("organvm-iv-taxis", "orchestration-start-here", "scripts/deploy/"),
}

# ORGAN-VII None targets -> specific repos by content type
ORGAN_VII_ROUTING = {
    "calendar": ("organvm-vii-kerygma", "distribution-strategy", "docs/calendars/"),
    "export": ("organvm-vii-kerygma", "distribution-strategy", "docs/exports/"),
    "dashboard": ("organvm-vii-kerygma", "social-automation", "docs/dashboards/"),
    "reach": ("organvm-vii-kerygma", "distribution-strategy", "docs/reach/"),
    "analytics": ("organvm-vii-kerygma", "social-automation", "docs/analytics/"),
}

# ORGAN-II backup files -> specific repos
ORGAN_II_ROUTING = {
    "omni-dromenon-machina": ("organvm-ii-poiesis", "metasystem-master", "docs/archive/omni-backup/"),
}

# ORGAN-I unrouted -> default theory repos by keyword
ORGAN_I_KEYWORDS = {
    "recursive": ("organvm-i-theoria", "recursive-engine--generative-entity", "docs/theory/"),
    "epistemic": ("organvm-i-theoria", "auto-revision-epistemic-engine", "docs/research/"),
    "ontolog": ("organvm-i-theoria", "organon-noumenon--ontogenetic-morphe", "docs/research/"),
    "narratol": ("organvm-i-theoria", "narratological-algorithmic-lenses", "docs/research/"),
    "linguistic": ("organvm-i-theoria", "linguistic-atomization-framework", "docs/research/"),
    "governance": ("organvm-i-theoria", "system-governance-framework", "docs/"),
}

# Directories whose files are not deployable (personal/system files)
NOT_DEPLOYABLE_DIRS = {
    "OS-me",
    "cloudbase-mcp",
    "mcp-servers",
    ".Trash",
}

# organvm-pactvm files are likely already in corpvs-testamentvm
ALREADY_DEPLOYED_DIRS = {
    "organvm-pactvm/ingesting-organ-document-structure",
}


def classify_none_entry(source_path, entry):
    """Classify a None-target entry into deploy/already-deployed/not-deployable."""
    organ = entry.get("organ", "")
    path = Path(source_path)
    parts = path.parts

    # Find workspace-relative path
    workspace_idx = None
    for i, part in enumerate(parts):
        if part == "Workspace":
            workspace_idx = i
            break

    if workspace_idx is None:
        return "not-deployable", "outside-workspace", None

    rel_parts = parts[workspace_idx + 1:]
    project_dir = rel_parts[0] if rel_parts else ""
    rel_path = "/".join(rel_parts)

    # Check not-deployable directories
    if project_dir in NOT_DEPLOYABLE_DIRS:
        return "not-deployable", f"personal-system-files ({project_dir})", None

    # Check already-deployed directories
    for already_dir in ALREADY_DEPLOYED_DIRS:
        if rel_path.startswith(already_dir):
            return "already-deployed", "in-corpvs-testamentvm", None

    # organvm-pactvm parent files (not in ingesting subdir)
    if project_dir == "organvm-pactvm" and len(rel_parts) <= 2:
        return "deploy-parent", "parent-dir-material", ("meta-organvm", "organvm-corpvs-testamentvm")

    # ORGAN-IV staging directory routing
    if project_dir == "ORG-IV-orchestration-staging":
        for subdir, (org, repo, deploy_path) in ORGAN_IV_ROUTING.items():
            if any(part == subdir.rstrip("/") for part in rel_parts):
                return "deploy", f"staging->{repo}", (org, repo, deploy_path)
        # Default: route to orchestration-start-here
        return "deploy", "staging->orchestration-start-here", (
            "organvm-iv-taxis", "orchestration-start-here", "docs/staging/"
        )

    # ORGAN-VII routing by filename keywords
    if organ == "ORGAN-VII":
        filename_lower = path.name.lower()
        for keyword, (org, repo, deploy_path) in ORGAN_VII_ROUTING.items():
            if keyword in filename_lower or keyword in rel_path.lower():
                return "deploy", f"keyword->{repo}", (org, repo, deploy_path)
        # Default: distribution-strategy
        return "deploy", "default->distribution-strategy", (
            "organvm-vii-kerygma", "distribution-strategy", "docs/materials/"
        )

    # ORGAN-II backup routing
    if organ == "ORGAN-II":
        for dir_key, (org, repo, deploy_path) in ORGAN_II_ROUTING.items():
            if dir_key in rel_path:
                return "deploy", f"backup->{repo}", (org, repo, deploy_path)
        # Default: metasystem-master archive
        return "deploy", "default->metasystem-master", (
            "organvm-ii-poiesis", "metasystem-master", "docs/archive/provenance/"
        )

    # ORGAN-I keyword routing
    if organ == "ORGAN-I":
        filename_lower = path.name.lower()
        for keyword, (org, repo, deploy_path) in ORGAN_I_KEYWORDS.items():
            if keyword in filename_lower:
                return "deploy", f"keyword->{repo}", (org, repo, deploy_path)
        # Default: scalable-lore-expert (catch-all theory)
        return "deploy", "default->scalable-lore-expert", (
            "organvm-i-theoria", "scalable-lore-expert", "docs/theory/"
        )

    # ORGAN-V: route to public-process
    if organ == "ORGAN-V":
        return "deploy", "default->public-process", (
            "organvm-v-logos", "public-process", "docs/materials/"
        )

    # ORGAN-VI: route to adaptive-personal-syllabus
    if organ == "ORGAN-VI":
        return "deploy", "default->adaptive-personal-syllabus", (
            "organvm-vi-koinonia", "adaptive-personal-syllabus", "docs/materials/"
        )

    # ORGAN-III: route based on content
    if organ == "ORGAN-III":
        return "deploy", "default->misc-commerce", (
            "organvm-iii-ergon", "card-trade-social", "docs/materials/"
        )

    # Fallback
    return "not-deployable", "unclassifiable", None


def main():
    import argparse
    parser = argparse.ArgumentParser(description="CONVERGENCE Phase D: Triage provenance")
    parser.add_argument("--dry-run", action="store_true", help="Preview without modifying")
    parser.add_argument("--stats-only", action="store_true", help="Only show statistics")
    args = parser.parse_args()

    with open(PROVENANCE_PATH) as f:
        provenance = json.load(f)

    source_map = provenance["source_to_repo"]

    # Find all None-target entries
    none_entries = {
        path: entry for path, entry in source_map.items()
        if "/None" in entry.get("target", "")
    }

    print(f"Total provenance entries: {len(source_map)}")
    print(f"None-target entries: {len(none_entries)}")
    print()

    # Classify each entry
    triage_results = {
        "deploy": [],
        "deploy-parent": [],
        "already-deployed": [],
        "not-deployable": [],
    }
    reason_counts = Counter()
    target_repo_counts = Counter()

    for source_path, entry in none_entries.items():
        category, reason, route_info = classify_none_entry(source_path, entry)
        triage_results[category].append((source_path, entry, reason, route_info))
        reason_counts[reason] += 1
        if route_info and len(route_info) >= 2:
            target_repo_counts[f"{route_info[0]}/{route_info[1]}"] += 1

    # Print statistics
    print("=== TRIAGE RESULTS ===")
    for category, entries in sorted(triage_results.items()):
        print(f"\n{category}: {len(entries)} entries")
    print()

    print("=== REASON BREAKDOWN ===")
    for reason, count in reason_counts.most_common():
        print(f"  {reason}: {count}")
    print()

    if target_repo_counts:
        print("=== TARGET REPO DISTRIBUTION ===")
        for repo, count in target_repo_counts.most_common():
            print(f"  {repo}: {count}")
        print()

    if args.stats_only:
        return

    # Apply triage decisions
    modified = 0
    for category, entries in triage_results.items():
        for source_path, entry, reason, route_info in entries:
            entry["triage"] = category
            entry["triage_reason"] = reason

            if category == "deploy" and route_info:
                org, repo = route_info[0], route_info[1]
                entry["target"] = f"{org}/{repo}"
                if len(route_info) >= 3:
                    entry["deploy_path"] = route_info[2]
            elif category == "deploy-parent" and route_info:
                org, repo = route_info
                entry["target"] = f"{org}/{repo}"
            elif category == "already-deployed":
                entry["triage_note"] = "File already exists in corpvs-testamentvm"
            elif category == "not-deployable":
                entry["triage_note"] = f"Not repo material: {reason}"

            modified += 1

    if args.dry_run:
        print(f"\n[DRY RUN] Would modify {modified} entries in provenance-registry.json")
        # Show sample entries per category
        for category, entries in triage_results.items():
            if entries:
                print(f"\n  Sample {category}:")
                for source_path, _, reason, route_info in entries[:3]:
                    print(f"    {Path(source_path).name}: {reason} -> {route_info}")
    else:
        # Update provenance totals
        none_remaining = sum(
            1 for entry in source_map.values()
            if "/None" in entry.get("target", "") and "triage" not in entry
        )
        provenance["triage_summary"] = {
            "total_triaged": modified,
            "deploy": len(triage_results["deploy"]),
            "deploy_parent": len(triage_results["deploy-parent"]),
            "already_deployed": len(triage_results["already-deployed"]),
            "not_deployable": len(triage_results["not-deployable"]),
            "none_remaining": none_remaining,
        }

        with open(PROVENANCE_PATH, "w") as f:
            json.dump(provenance, f, indent=2)
        print(f"\nProvenance registry updated: {modified} entries triaged.")
        print(f"None-target entries remaining: {none_remaining}")


if __name__ == "__main__":
    main()
