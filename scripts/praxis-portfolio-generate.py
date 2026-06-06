#!/usr/bin/env python3
"""PRAXIS Sprint Phase A: Portfolio site data generator.

Reads repo-registry.json and generates structured data for the Astro portfolio site.
Outputs:
  - site-data/landing.json      — Landing page metrics and overview
  - site-data/projects.json     — 19 curated project gallery entries
  - site-data/essays.json       — Essay index from public-process _posts/
  - site-data/graph.json        — Dependency graph data for D3.js visualization
  - site-data/about.json        — CV/about page data
  - site-data/design-tokens.json — Design tokens from taste.yaml (if available)
  - site-data/rss-meta.json     — RSS feed metadata

Usage:
    python3 scripts/praxis-portfolio-generate.py [--output-dir site-data]
"""

import argparse
import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent.parent / "repo-registry.json"
PROVENANCE_PATH = Path(__file__).parent.parent / "provenance-registry.json"

ORGAN_NAMES = {
    "ORGAN-I": ("Theory", "Theoria", "organvm-i-theoria"),
    "ORGAN-II": ("Art", "Poiesis", "organvm-ii-poiesis"),
    "ORGAN-III": ("Commerce", "Ergon", "organvm-iii-ergon"),
    "ORGAN-IV": ("Orchestration", "Taxis", "organvm-iv-taxis"),
    "ORGAN-V": ("Public Process", "Logos", "organvm-v-logos"),
    "ORGAN-VI": ("Community", "Koinonia", "organvm-vi-koinonia"),
    "ORGAN-VII": ("Marketing", "Kerygma", "organvm-vii-kerygma"),
    "META": ("Meta", "Meta", "meta-organvm"),
}

SPRINT_HISTORY = [
    {"name": "IGNITION", "date": "2026-02-09", "summary": "Org architecture — 8 GitHub orgs"},
    {"name": "PROPULSION", "date": "2026-02-10", "summary": "Bronze/Silver/Gold documentation sprints"},
    {"name": "ASCENSION", "date": "2026-02-10", "summary": "Micro-validation and integration"},
    {"name": "EXODUS", "date": "2026-02-11", "summary": "System launch — all 8 organs OPERATIONAL"},
    {"name": "PERFECTION", "date": "2026-02-11", "summary": "Gap-fill — 11 repos, 14 promotions"},
    {"name": "AUTONOMY", "date": "2026-02-12", "summary": "seed.yaml contracts, agents, workflows"},
    {"name": "GENESIS", "date": "2026-02-12", "summary": "7 new repos from local materials"},
    {"name": "ALCHEMIA", "date": "2026-02-12", "summary": "2,012 files inventoried, taste.yaml cascading"},
    {"name": "CONVERGENCE", "date": "2026-02-13", "summary": "82 ACTIVE, 7 ARCHIVED, zero gaps"},
    {"name": "PRAXIS", "date": "2026-02-13", "summary": "External impact — portfolio, distribution, revenue"},
    {"name": "VERITAS", "date": "2026-02-13", "summary": "Credibility hardening — PRODUCTION→ACTIVE, revenue split, essay dates"},
    {"name": "MANIFESTATIO", "date": "2026-02-14", "summary": "Re-audit (7x more code), 3 CI fixes, engagement baseline"},
    {"name": "ILLUSTRATIO", "date": "2026-02-14", "summary": "Portfolio polish — CMYK design, p5.js animations, LLM consultation"},
]


# ISOTOPE DISSOLUTION: Gate memory--remember G2 (CORPUS_SCRIPTS_DISSOLVED)
try:
    from organvm_engine.registry.loader import load_registry as _engine_load
except ImportError:
    _engine_load = None


def load_registry():
    if _engine_load is not None:
        return _engine_load(REGISTRY_PATH)
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def generate_landing(registry):
    """Generate landing page metrics and overview."""
    all_repos = []
    organ_summaries = []
    for organ_key, organ_data in registry["organs"].items():
        repos = organ_data.get("repositories", [])
        all_repos.extend(repos)
        names = ORGAN_NAMES.get(organ_key, (organ_key, organ_key, ""))
        organ_summaries.append({
            "key": organ_key,
            "name": names[0],
            "greek": names[1],
            "org": names[2],
            "repo_count": len(repos),
            "status": organ_data.get("launch_status", "UNKNOWN"),
            "description": organ_data.get("description", ""),
        })

    status_counts = defaultdict(int)
    for r in all_repos:
        status_counts[r.get("implementation_status", "UNKNOWN")] += 1

    dep_count = sum(len(r.get("dependencies", [])) for r in all_repos)
    ci_count = sum(1 for r in all_repos if r.get("ci_workflow"))

    return {
        "title": "ORGANVM — Eight-Organ Creative-Institutional System",
        "tagline": "A living system of 8 organs coordinating theory, art, commerce, orchestration, public process, community, marketing, and governance.",
        "metrics": {
            "total_repos": len(all_repos),
            "active_repos": status_counts.get("ACTIVE", 0),
            "archived_repos": status_counts.get("ARCHIVED", 0),
            "dependency_edges": dep_count,
            "ci_workflows": ci_count,
            "operational_organs": sum(1 for o in organ_summaries if o["status"] == "OPERATIONAL"),
            "sprints_completed": len(SPRINT_HISTORY),
        },
        "organs": organ_summaries,
        "sprint_history": SPRINT_HISTORY,
        "generated": datetime.now(timezone.utc).isoformat(),
    }


def generate_projects(registry):
    """Generate curated project gallery (flagships + CRITICAL relevance)."""
    projects = []
    for organ_key, organ_data in registry["organs"].items():
        names = ORGAN_NAMES.get(organ_key, (organ_key, organ_key, ""))
        for repo in organ_data.get("repositories", []):
            relevance = repo.get("portfolio_relevance", "")
            tier = repo.get("tier", "")
            impl_status = repo.get("implementation_status", "")

            if impl_status == "ARCHIVED":
                continue

            is_curated = tier == "flagship" or "CRITICAL" in relevance
            if not is_curated:
                continue

            org = repo.get("org", names[2])
            projects.append({
                "name": repo["name"],
                "org": org,
                "organ": organ_key,
                "organ_name": names[0],
                "url": f"https://github.com/{org}/{repo['name']}",
                "description": repo.get("description", ""),
                "portfolio_relevance": relevance,
                "tier": tier,
                "implementation_status": impl_status,
                "ci_workflow": repo.get("ci_workflow"),
                "dependencies": repo.get("dependencies", []),
                "promotion_status": repo.get("promotion_status", ""),
            })

    return {
        "total_curated": len(projects),
        "projects": projects,
        "generated": datetime.now(timezone.utc).isoformat(),
    }


def generate_essays():
    """Fetch essay index from public-process repo."""
    result = subprocess.run(
        ["gh", "api", "repos/organvm-v-logos/public-process/git/trees/HEAD?recursive=1",
         "--jq", '[.tree[] | select(.path | startswith("_posts/")) | .path]'],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print(f"  WARNING: Could not fetch essays from GitHub API: {result.stderr.strip()}")
        return {"essays": [], "total": 0, "error": "API query failed"}

    paths = json.loads(result.stdout.strip())
    essays = []
    for path in sorted(paths):
        filename = path.replace("_posts/", "")
        # Parse Jekyll filename: YYYY-MM-DD-slug.md
        parts = filename.split("-", 3)
        if len(parts) >= 4:
            date = f"{parts[0]}-{parts[1]}-{parts[2]}"
            slug = parts[3].replace(".md", "").replace(".markdown", "")
            title = slug.replace("-", " ").title()
        else:
            date = ""
            slug = filename.replace(".md", "")
            title = slug.replace("-", " ").title()

        essays.append({
            "path": path,
            "filename": filename,
            "date": date,
            "slug": slug,
            "title": title,
            "url": f"https://organvm-v-logos.github.io/public-process/{date.replace('-', '/')}/{slug}/",
        })

    return {
        "total": len(essays),
        "essays": sorted(essays, key=lambda e: e.get("date", ""), reverse=True),
        "feed_url": "https://organvm-v-logos.github.io/public-process/feed.xml",
        "site_url": "https://organvm-v-logos.github.io/public-process/",
        "generated": datetime.now(timezone.utc).isoformat(),
    }


def generate_graph(registry):
    """Generate dependency graph data for D3.js visualization."""
    nodes = []
    edges = []
    node_ids = set()

    for organ_key, organ_data in registry["organs"].items():
        names = ORGAN_NAMES.get(organ_key, (organ_key, organ_key, ""))
        for repo in organ_data.get("repositories", []):
            if repo.get("implementation_status") == "ARCHIVED":
                continue
            org = repo.get("org", names[2])
            node_id = f"{org}/{repo['name']}"
            node_ids.add(node_id)
            nodes.append({
                "id": node_id,
                "name": repo["name"],
                "organ": organ_key,
                "organ_name": names[0],
                "tier": repo.get("tier", "standard"),
                "status": repo.get("implementation_status", "UNKNOWN"),
            })

    for organ_key, organ_data in registry["organs"].items():
        names = ORGAN_NAMES.get(organ_key, (organ_key, organ_key, ""))
        for repo in organ_data.get("repositories", []):
            if repo.get("implementation_status") == "ARCHIVED":
                continue
            org = repo.get("org", names[2])
            source = f"{org}/{repo['name']}"
            for dep in repo.get("dependencies", []):
                if dep in node_ids:
                    edges.append({"source": source, "target": dep})

    return {
        "nodes": nodes,
        "edges": edges,
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "generated": datetime.now(timezone.utc).isoformat(),
    }


def generate_about(registry):
    """Generate about/CV page data."""
    summary = registry.get("summary", {})
    meta_note = registry.get("meta_system_portfolio_note", {})

    return {
        "system_name": "ORGANVM",
        "subtitle": "Eight-Organ Creative-Institutional System",
        "owner": "@4444j99 / @4444J99",
        "launch_date": registry.get("launch_date", "2026-02-11"),
        "system_summary": summary.get("portfolio_strength", ""),
        "strategic_context": meta_note.get("context", ""),
        "supporting_evidence": meta_note.get("supporting_evidence", ""),
        "strategic_opportunity": meta_note.get("strategic_opportunity", ""),
        "application_targets": [
            {
                "category": "AI Systems Engineering",
                "description": "Orchestration capacity, architectural reasoning, multi-agent systems",
            },
            {
                "category": "Creative/Technical Grants",
                "description": "NSF, NEA, Mellon, Knight Foundation — infrastructure as art",
            },
            {
                "category": "Technology Residencies",
                "description": "Eyebeam, Recurse Center — equitable systems, community infrastructure",
            },
            {
                "category": "Fellowships",
                "description": "Processing Foundation, Google Creative — artist-engineer hybrid",
            },
        ],
        "generated": datetime.now(timezone.utc).isoformat(),
    }


def generate_rss_meta(registry):
    """Generate RSS feed metadata."""
    return {
        "title": "ORGANVM — Public Process",
        "description": "Essays on building an eight-organ creative-institutional system in public.",
        "link": "https://organvm-v-logos.github.io/public-process/",
        "feed_url": "https://organvm-v-logos.github.io/public-process/feed.xml",
        "language": "en-US",
        "author": "ORGANVM",
        "generated": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Generate portfolio site data from registry")
    parser.add_argument("--output-dir", default="site-data", help="Output directory for generated JSON")
    args = parser.parse_args()

    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("PRAXIS Sprint Phase A — Portfolio Data Generation")
    print("=" * 60)

    registry = load_registry()

    generators = [
        ("landing.json", "Landing page", generate_landing, (registry,)),
        ("projects.json", "Project gallery", generate_projects, (registry,)),
        ("essays.json", "Essay index", generate_essays, ()),
        ("graph.json", "Dependency graph", generate_graph, (registry,)),
        ("about.json", "About/CV page", generate_about, (registry,)),
        ("rss-meta.json", "RSS metadata", generate_rss_meta, (registry,)),
    ]

    for filename, label, gen_fn, gen_args in generators:
        print(f"\n[GEN] {label} → {output / filename}")
        try:
            data = gen_fn(*gen_args)
            with open(output / filename, "w") as f:
                json.dump(data, f, indent=2)
                f.write("\n")

            # Print summary stats
            if isinstance(data, dict):
                for key in ("total_curated", "total", "total_nodes", "total_edges", "metrics"):
                    if key in data:
                        val = data[key]
                        if isinstance(val, dict):
                            for k, v in val.items():
                                print(f"  {k}: {v}")
                        else:
                            print(f"  {key}: {val}")
            print(f"  OK")
        except Exception as e:
            print(f"  ERROR: {e}")

    print(f"\n{'=' * 60}")
    print(f"Generated {len(generators)} files in {output}/")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
