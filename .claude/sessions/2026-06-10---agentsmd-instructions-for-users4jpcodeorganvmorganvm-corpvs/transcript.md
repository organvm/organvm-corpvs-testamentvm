# Session Transcript: Codex — /Users/4jp/Code/organvm/organvm-corpvs-testamentvm

**Agent:** Codex (OpenAI)
**Session ID:** `019eb377-d378-7962-a1f4-755ac4f5e941`
**Working directory:** `/Users/4jp/Code/organvm/organvm-corpvs-testamentvm`
**Messages:** 2 (2 human, 0 assistant)

---

## [1] Human — 21:37:20

# AGENTS.md instructions for /Users/4jp/Code/organvm/organvm-corpvs-testamentvm

<INSTRUCTIONS>
<!-- Role: shim | Owner: domus-genoma | Source: dot_local/share/codex/AGENTS.md.tmpl | Redirects-to: ~/AGENTS.md | Manifest: ~/.config/ai-context/agent-instruction-surfaces.json -->

Global policy: /Users/4jp/AGENTS.md applies and cannot be overridden.

--- project-doc ---

<!-- ORGANVM:AUTO:START -->
## Agent Context (auto-generated — do not edit)

This repo participates in the **META-ORGANVM (Meta)** swarm.

### Active Subscriptions
- Event: `governance.updated` → Action: Update meta-system documentation
- Event: `health-audit.completed` → Action: Review system-wide audit findings

### Production Responsibilities
- **Produce** `meta-documentation` for ORGAN-IV
- **Produce** `research-tasks` for META-ORGANVM/organvm-engine, META-ORGANVM/praxis-perpetua
- **Produce** `work-registry` for ALL
- **Produce** `prompt-registry` for ALL
- **Produce** `session-continuation-prompts` for ALL

### External Dependencies
- **Consume** `orchestration-artifact` from `ORGAN-IV`

### Governance Constraints
- Adhere to unidirectional flow: I→II→III
- Never commit secrets or credentials

*Last synced: 2026-06-08T16:26:25Z*
<!-- ORGANVM:AUTO:END -->


Files called AGENTS.md commonly appear in many places inside a container - at "/", in "~", deep within git repositories, or in any other directory; their location is not limited to version-controlled folders.

Their purpose is to pass along human guidance to you, the agent. Such guidance can include coding standards, explanations of the project layout, steps for building or testing, and even wording that must accompany a GitHub pull-request description produced by the agent; all of it is to be followed.

Each AGENTS.md governs the entire directory that contains it and every child directory beneath that point. Whenever you change a file, you have to comply with every AGENTS.md whose scope covers that file. Naming conventions, stylistic rules and similar directives are restricted to the code that falls inside that scope unless the document explicitly states otherwise.

When two AGENTS.md files disagree, the one located deeper in the directory structure overrides the higher-level file, while instructions given directly in the prompt by the system, developer, or user outrank any AGENTS.md content.

</INSTRUCTIONS>
<environment_context>
  <cwd>/Users/4jp/Code/organvm/organvm-corpvs-testamentvm</cwd>
  <shell>zsh</shell>
  <current_date>2026-06-10</current_date>
  <timezone>America/New_York</timezone>
  <filesystem><workspace_roots><root>/Users/4jp/Code/organvm/organvm-corpvs-testamentvm</root></workspace_roots><permission_profile type="managed"><file_system type="restricted"><entry access="read"><special>:root</special></entry><entry access="write"><path>/Users/4jp/Code/organvm/organvm-corpvs-testamentvm</path></entry><entry access="write"><special>:slash_tmp</special></entry><entry access="write"><special>:tmpdir</special></entry><entry access="read"><path>/Users/4jp/Code/organvm/organvm-corpvs-testamentvm/.git</path></entry><entry access="read"><path>/Users/4jp/Code/organvm/organvm-corpvs-testamentvm/.agents</path></entry><entry access="read"><path>/Users/4jp/Code/organvm/organvm-corpvs-testamentvm/.codex</path></entry></file_system></permission_profile></filesystem>
</environment_context>

---

## [2] Human — 21:37:20

You are on branch fix/ingestion-source-paths (verify with git branch --show-current; if different, stop and report). Create the missing file data/prompt-registry/README.md — it is referenced by .gitignore line 35 ('see data/prompt-registry/README.md for regeneration commands') but was never written. Document the regeneration pipeline accurately by reading the docstrings/headers of these scripts in data/prompt-registry/: extract_all_prompts.py, atomize_prompts.py, snapshot_status_carryover.py, prioritize_atoms.py, generate_work_queue.py, route_atoms.py. README must cover: (1) pipeline order: backup (cp the 4 JSONs + INST-INDEX-PROMPTORUM.md to a dated .backup-* dir) → python3 snapshot_status_carryover.py → python3 extract_all_prompts.py → python3 atomize_prompts.py → apply status carry-over by (timestamp, sha1(content)) join → re-apply secret redaction (IRF-SEC-005, commits b08fb35/3423079/482408f) and grep-verify zero literal hits → python3 prioritize_atoms.py → python3 generate_work_queue.py → python3 route_atoms.py. (2) HAZARDS in a prominent section: extract+atomize are FULL REBUILDS that reset every status to UNREVIEWED and reassign sequential IDs; no script makes backups; rebuilding from raw transcripts re-introduces previously-redacted secrets; run steps sequentially only (16GB machine). (3) Which files are gitignored (all *.json in the dir) vs tracked (.py, .md). Style: terse, operational, no marketing prose. Then: git add data/prompt-registry/README.md && git commit -m 'docs(prompt-registry): add regeneration README (referenced by .gitignore but missing)'. Do NOT push. Do NOT modify any .json or any other file.

---
