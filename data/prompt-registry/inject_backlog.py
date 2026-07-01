#!/usr/bin/env python3
"""Inject 34 cross-audit backlog items as tracked atoms in prompt-atoms.json."""

import json
import subprocess
import sys
from pathlib import Path

REGISTRY_DIR = Path(__file__).parent
ATOMS_FILE = REGISTRY_DIR / "prompt-atoms.json"

BACKLOG_ITEMS = [
    {"id": "BACKLOG-001", "content": "Gmail app password revocation — burn exposed password in Google Account Security", "universes": ["security"], "date": "2026-04-17", "priority": "P0"},
    {"id": "BACKLOG-002", "content": "LegalZoom FL Annual Report — overdue since 2026-04-16", "universes": ["personal", "financial"], "date": "2026-04-16", "priority": "P0"},
    {"id": "BACKLOG-003", "content": "Tax filing — overdue since 2026-04-15", "universes": ["personal", "financial"], "date": "2026-04-15", "priority": "P0"},
    {"id": "BACKLOG-004", "content": "OpenAI API key rotation — exposed in Docker image", "universes": ["security"], "date": "2026-04-16", "priority": "P0"},
    {"id": "BACKLOG-005", "content": "Webhook secret to 1Password — terminal value 97231e...72cd", "universes": ["security", "persistence"], "date": "2026-04-16", "priority": "P0"},
    {"id": "BACKLOG-006", "content": "GoDaddy met4vers.io — grace period ending, cancellation notice sent, decision needed", "universes": ["personal", "naming"], "date": "2026-04-16", "priority": "P0"},
    {"id": "BACKLOG-007", "content": "Stripe integration — public-record-data-scrapper (IRF-III-026) — revenue blocker", "universes": ["organ-iii", "financial"], "date": "2026-04-17", "priority": "P0"},
    {"id": "BACKLOG-008", "content": "Stripe integration — content-engine/Cronus (IRF-III-027) — revenue blocker", "universes": ["organ-iii", "financial"], "date": "2026-04-17", "priority": "P0"},
    {"id": "BACKLOG-009", "content": "Architectural misalignment — sovereign-systems water-first vs spiral-first (IRF-III-029)", "universes": ["organ-iii"], "date": "2026-04-17", "priority": "P0"},
    {"id": "BACKLOG-010", "content": "6 domain registrations at Cloudflare — [user].dev, anthonypadavano.com/dev, organvm.dev/org/io ($51-$101/yr)", "universes": ["personal", "naming"], "date": "2026-04-16", "priority": "P1"},
    {"id": "BACKLOG-011", "content": "Codex 6-repo build — awaiting handoff approval (IRF-SYS-118)", "universes": ["meta"], "date": "2026-04-17", "priority": "P1"},
    {"id": "BACKLOG-012", "content": "5-PR corrective implementation — sovereign-systems homepage restructure, water page, quiz, spiral nodes, polish (IRF-III-031)", "universes": ["organ-iii"], "date": "2026-04-17", "priority": "P1"},
    {"id": "BACKLOG-013", "content": "65-want atomization — cartographical fossil record of Maddie's actual desires (IRF-III-030)", "universes": ["organ-iii"], "date": "2026-04-17", "priority": "P1"},
    {"id": "BACKLOG-014", "content": "Padavano booking/scheduling mechanism for consulting site (IRF-III-028)", "universes": ["organ-iii", "financial"], "date": "2026-04-17", "priority": "P1"},
    {"id": "BACKLOG-015", "content": "GCP billing payment — overdue", "universes": ["financial"], "date": "2026-04-16", "priority": "P1"},
    {"id": "BACKLOG-016", "content": "Wire new Gmail app password through 1Password + op read", "universes": ["security", "persistence"], "date": "2026-04-17", "priority": "P1"},
    {"id": "BACKLOG-017", "content": "Becka McKay thread — awaiting reply to Apr 17 boundary-setting message", "universes": ["relationships"], "date": "2026-04-17", "priority": "P1"},
    {"id": "BACKLOG-018", "content": "Portfolio migration — base path /portfolio to /, Cloudflare Pages, zero-downtime cutover (IRF-PRT-026)", "universes": ["personal"], "date": "2026-04-16", "priority": "P2"},
    {"id": "BACKLOG-019", "content": "Formal strata INSTANCE.toml — 3 additional locations unexecuted (IRF-SYS-117)", "universes": ["meta", "UNIVERSAL"], "date": "2026-04-17", "priority": "P2"},
    {"id": "BACKLOG-020", "content": "Layer 4 CPU tuning — LaunchAgent 6h→12h, nice 19 for CCE refresh", "universes": ["organ-i", "automation"], "date": "2026-04-16", "priority": "P2"},
    {"id": "BACKLOG-021", "content": "Gemini web API content acquisition — batchexecute RPC ID mapping", "universes": ["organ-i"], "date": "2026-04-16", "priority": "P2"},
    {"id": "BACKLOG-022", "content": "Soak pipeline zero system variables bug (IRF-SYS-116)", "universes": ["meta"], "date": "2026-04-17", "priority": "P2"},
    {"id": "BACKLOG-023", "content": "Universal routing law — implement routing-law.yaml in organvm-ontologia", "universes": ["meta", "UNIVERSAL"], "date": "2026-04-17", "priority": "P2"},
    {"id": "BACKLOG-024", "content": "Vercel project name — align to padavano (may still be victoroff-group or consilivm-simplex)", "universes": ["organ-iii"], "date": "2026-04-17", "priority": "P2"},
    {"id": "BACKLOG-025", "content": "Email triage system — 4-tier classifier, LaunchAgent automation", "universes": ["personal", "automation"], "date": "2026-04-17", "priority": "P1"},
    {"id": "BACKLOG-026", "content": "Santander overdraft", "universes": ["financial"], "date": "2026-04-16", "priority": "P3"},
    {"id": "BACKLOG-027", "content": "Nelnet forbearance", "universes": ["financial"], "date": "2026-04-16", "priority": "P3"},
    {"id": "BACKLOG-028", "content": "Zip Pay", "universes": ["financial"], "date": "2026-04-16", "priority": "P3"},
    {"id": "BACKLOG-029", "content": "Cash App", "universes": ["financial"], "date": "2026-04-16", "priority": "P3"},
    {"id": "BACKLOG-030", "content": "LinkedIn Premium cancel", "universes": ["financial"], "date": "2026-04-16", "priority": "P3"},
    {"id": "BACKLOG-031", "content": "CCE GitHub issues — create tracking issues for CPU throttling fix + Gemini adapter", "universes": ["organ-i"], "date": "2026-04-16", "priority": "P3"},
    {"id": "BACKLOG-032", "content": "CCE CLAUDE.md — document --throttle flag in CLI Command Tree", "universes": ["organ-i"], "date": "2026-04-16", "priority": "P3"},
    {"id": "BACKLOG-033", "content": "custodia-securitatis GitHub issue — governance tracking for new repo creation", "universes": ["security"], "date": "2026-04-16", "priority": "P3"},
    {"id": "BACKLOG-034", "content": "Plugin reload confirmation — verify /reload-plugins clears all 4 errors", "universes": ["personal"], "date": "2026-04-16", "priority": "P3"},
]


def main():
    atoms = json.loads(ATOMS_FILE.read_text(encoding="utf-8"))

    # Check for existing backlog atoms (idempotency)
    existing_ids = {a["atom_id"] for a in atoms}
    if "BACKLOG-001" in existing_ids:
        print("Backlog items already injected. Skipping.")
        return

    new_atoms = []
    for item in BACKLOG_ITEMS:
        new_atoms.append({
            "atom_id": item["id"],
            "parent_prompt_id": "",
            "type": "directive",
            "content": f"[{item['priority']}] {item['content']}",
            "summary": f"[{item['priority']}] {item['content'][:120]}",
            "universes": item["universes"],
            "status": "OPEN",
            "produced": [],
            "source": "cross-audit-2026-04-18",
            "date": item["date"],
            "timestamp": "",
            "response_summary": "",
        })

    atoms.extend(new_atoms)
    ATOMS_FILE.write_text(json.dumps(atoms, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Injected {len(new_atoms)} backlog items into prompt-atoms.json")
    print(f"Total atoms: {len(atoms)}")

    # Re-run measurement
    print("\nRe-running measurement engine...")
    subprocess.run([sys.executable, str(REGISTRY_DIR / "measure_implementation.py")], cwd=str(REGISTRY_DIR))


if __name__ == "__main__":
    main()
