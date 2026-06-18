#!/usr/bin/env python3
"""Shared governance validators — the single source of truth for rule-based checks.

These functions are *pure with respect to time*: given a registry state and a set
of governance rules, they return the same verdict regardless of when they run. That
property is what makes temporal staging possible (IRF-RES-013): the *same* current
validator can be applied to a *previous* state to expose rule drift.

Extracted from soak-test-monitor.py so that both the daily collector and the
temporal-staging validator call identical logic. If these checks were duplicated,
the two validators could disagree — which would defeat the entire purpose of
validating previous-state-with-current-rules.

Consumed by:
  - scripts/soak-test-monitor.py        (current-state collection)
  - scripts/temporal-staging-validator.py  (previous-state, current-rules check)
"""

import hashlib
import json
from collections import defaultdict

# The canonical eight organs (ORGAN I-VII + Meta).
EXPECTED_ORGANS = [f"ORGAN-{n}" for n in ["I", "II", "III", "IV", "V", "VI", "VII"]] + ["META-ORGANVM"]

# Fields every repo must carry for registry integrity.
REQUIRED_REPO_FIELDS = ("name", "org", "implementation_status", "documentation_status")

# Generative flow I->II->III; lower number must never depend on higher (no back-edge).
ORGAN_LEVELS = {
    "organvm-i-theoria": 1,
    "organvm-ii-poiesis": 2,
    "organvm-iii-ergon": 3,
}
RESTRICTED_LEVELS = {1, 2, 3}


def build_repo_map(registry: dict) -> tuple[dict, list]:
    """Build repo lookup and flat list from registry organs."""
    repo_map = {}
    all_repos = []
    for organ_key, organ_data in registry.get("organs", {}).items():
        for repo in organ_data.get("repositories", []):
            key = f"{repo['org']}/{repo['name']}"
            repo["_organ_key"] = organ_key
            repo_map[key] = repo
            all_repos.append(repo)
    return repo_map, all_repos


def validate_registry(registry: dict) -> dict:
    """Check registry integrity: required fields, organ completeness."""
    issues = []
    _, all_repos = build_repo_map(registry)

    for organ in EXPECTED_ORGANS:
        if organ not in registry.get("organs", {}):
            issues.append(f"Missing organ: {organ}")

    for repo in all_repos:
        key = f"{repo.get('org', '?')}/{repo.get('name', '?')}"
        for field in REQUIRED_REPO_FIELDS:
            if not repo.get(field):
                issues.append(f"{key}: missing field '{field}'")

    return {
        "total_repos": len(all_repos),
        "issues": issues,
        "pass": len(issues) == 0,
    }


def validate_dependencies(registry: dict, governance: dict) -> dict:
    """Check dependency graph: no cycles, no back-edges, depth within limits."""
    repo_map, all_repos = build_repo_map(registry)

    deps = []
    for repo in all_repos:
        key = f"{repo['org']}/{repo['name']}"
        for dep in repo.get("dependencies", []):
            deps.append((key, dep))

    # Back-edge check: within the restricted I/II/III flow, a lower level may
    # not depend on a higher level.
    back_edges = []
    for from_key, to_key in deps:
        from_level = ORGAN_LEVELS.get(from_key.split("/")[0])
        to_level = ORGAN_LEVELS.get(to_key.split("/")[0])
        if from_level and to_level and from_level in RESTRICTED_LEVELS and to_level in RESTRICTED_LEVELS:
            if from_level < to_level:
                back_edges.append(f"{from_key} -> {to_key}")

    # Cycle check (DFS).
    adj = defaultdict(list)
    for f, t in deps:
        adj[f].append(t)

    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(lambda: WHITE)
    cycles = []

    def dfs(node, path):
        color[node] = GRAY
        path.append(node)
        for neighbor in adj[node]:
            if color[neighbor] == GRAY:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
            elif color[neighbor] == WHITE:
                dfs(neighbor, path)
        path.pop()
        color[node] = BLACK

    for node in list(repo_map.keys()):
        if color[node] == WHITE:
            dfs(node, [])

    # Depth check.
    max_depth = governance.get("dependency_rules", {}).get("max_transitive_depth", 4)

    def measure_depth(node, visited=None):
        if visited is None:
            visited = set()
        if node in visited:
            return 0
        visited.add(node)
        if not adj[node]:
            return 0
        return 1 + max(measure_depth(n, visited) for n in adj[node])

    deepest = 0
    for node in repo_map:
        d = measure_depth(node)
        if d > deepest:
            deepest = d

    return {
        "total_edges": len(deps),
        "back_edges": back_edges,
        "cycles": [" -> ".join(c) for c in cycles],
        "max_depth": deepest,
        "depth_limit": max_depth,
        "pass": len(back_edges) == 0 and len(cycles) == 0 and deepest <= max_depth,
    }


# --- Temporal staging support (IRF-RES-013) ---

def _digest(obj) -> str:
    """Stable sha256 over canonicalized JSON — order-independent, whitespace-free."""
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def project_state(registry: dict, governance: dict) -> dict:
    """Freeze the validation-relevant projection of current state into a capsule.

    The capsule must contain *everything* the rule-based validators consume — and
    nothing time-relative (no staleness, no CI, no engagement). A future run
    reconstructs a registry from this capsule and re-validates it under whatever
    rules are then current. This is the object-tier snapshot in the Tarskian sense.
    """
    repo_map, all_repos = build_repo_map(registry)
    repos = []
    for repo in all_repos:
        repos.append({
            "org": repo.get("org"),
            "name": repo.get("name"),
            "organ_key": repo.get("_organ_key"),
            "implementation_status": repo.get("implementation_status"),
            "documentation_status": repo.get("documentation_status"),
            "dependencies": list(repo.get("dependencies", [])),
        })
    return {
        "schema": 1,
        "registry_digest": _digest({k: v for k, v in registry.items()}),
        "governance_version": governance.get("version"),
        "governance_digest": _digest(governance.get("dependency_rules", {})),
        "organs_present": sorted(registry.get("organs", {}).keys()),
        "repo_count": len(all_repos),
        "repos": repos,
    }


def reconstruct_registry(capsule: dict) -> dict:
    """Rebuild a registry-shaped dict from a frozen state capsule.

    The result is structurally compatible with build_repo_map / validate_registry /
    validate_dependencies, so the *current* validators run against it unchanged.
    """
    organs: dict = {}
    # Preserve organ keys that were present even if they hold no repos, so the
    # "missing organ" check sees exactly what the snapshot saw.
    for organ_key in capsule.get("organs_present", []):
        organs.setdefault(organ_key, {"repositories": []})
    for repo in capsule.get("repos", []):
        organ_key = repo.get("organ_key") or "UNKNOWN"
        organs.setdefault(organ_key, {"repositories": []})
        organs[organ_key]["repositories"].append({
            "org": repo.get("org"),
            "name": repo.get("name"),
            "implementation_status": repo.get("implementation_status"),
            "documentation_status": repo.get("documentation_status"),
            "dependencies": list(repo.get("dependencies", [])),
        })
    return {"organs": organs}
