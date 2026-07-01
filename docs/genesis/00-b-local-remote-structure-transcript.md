## Q: 
The following information was transcribed via audio, it requires a logic pass and needs to be made to make sense: In reference to my local and my remote folder structure and organization and repository structures and all of them nested within one another or outside of one another, Russian doll sequence. Mimicking the local structure with the organizational Remote structure on GitHub. I need to design A prompt or a chain of prompts to audit all of this Build the structure locally. And mimic it or mirror it. Remotely And I wanna do this Starting in my home directory. So let's design A prompt for AI handoff I could open inside my terminal Drop the prompt in. Investigate what's inside of the home directory And then Unify with glorious certainty and purpose This is the goal. Once we have this structure, this organization, this unity, Everything else will fall into place. This is the macro system. All of the projects, the folders, the repos, the organizations, those are micro elements that Russian doll inwards, So let's stick to the ontology and ontological names for everything.

## A: 
## Logic pass: what you’re actually trying to do

You want a single **canonical ontology** for your digital space, then a **repeatable audit-and-normalize procedure** that:

1.  Starts at **$HOME** and inventories everything that matters (projects, repos, drafts, archives, stray folders).
    
2.  Defines a **target local directory topology** (a nested “Russian-doll” system where macro containers contain micro projects).
    
3.  Ensures the **remote topology on GitHub mirrors the local topology** (organizations → repositories → branches/tags/releases) with clear, deterministic mapping.
    
4.  Produces “glorious certainty” by generating:
    
    1.  a manifest of what exists now,
        
    2.  a manifest of what should exist,
        
    3.  a migration plan from current → target,
        
    4.  (optionally) executable steps to enforce it.
        

That macro-structure is the spine. Individual projects are leaves.

* * *

## Canonical ontology (names + invariants)

### Ontology layers (macro → micro)

Use these as your **universal, non-branded** identifiers:

1.  **ROOT**: the top container for all work (local: `$HOME`, or a dedicated `$WORLD_ROOT` inside `$HOME`)
    
2.  **REALM**: major life/system domains (examples: `create`, `research`, `operate`, `publish`, `archive`)
    
3.  **ORG_UNIT**: a coherent “institutional” boundary (maps to a GitHub organization when applicable)
    
4.  **REPO_UNIT**: a versioned unit with a `.git` root and one remote “source of truth”
    
5.  **WORKSPACE_UNIT**: a practical working bundle (may contain multiple repos, but should be explicitly declared)
    
6.  **ARTIFACT_UNIT**: outputs (builds, renders, exports, PDFs, audio bounces, releases)
    

### Invariants (non-negotiables)

1.  Every **REPO_UNIT** has exactly one canonical local root and at least one remote (`origin`) that resolves.
    
2.  Every repo belongs to exactly one **ORG_UNIT** (even if the remote is personal; it still gets an ORG_UNIT id).
    
3.  Every directory under the managed tree is either:
    
    1.  a realm container,
        
    2.  an org container,
        
    3.  a repo root,
        
    4.  an artifact/output directory,
        
    5.  or explicitly marked “unmanaged”.
        
4.  “Russian-doll” nesting is allowed only via **declared containment**, not accidental sprawl:
    
    1.  repo-inside-repo is prohibited unless the inner repo is a declared submodule or declared workspace member.
        
5.  Names are stable identifiers:
    
    1.  lowercase,
        
    2.  ASCII,
        
    3.  hyphen/underscore only,
        
    4.  no date prefixes unless the date is semantically part of the identity.
        

* * *

## Environment-variable contract (so this stays CLI-native)

Put these in your shell before running the handoff (or let the agent propose them):

```bash
export WORLD_ROOT="$HOME/world"
export AUDIT_ROOT="$WORLD_ROOT/.audit"
export REALMS="create research operate publish archive"
export VCS_HOST="github.com"
export ORG_POLICY="mirror-local-to-remote"
```

Optional but useful:

```bash
export DEFAULT_ORG_UNIT="personal"
export UNMANAGED_DIRS="$HOME/Library $HOME/.cache $HOME/.config"
```

* * *

## Target directory template (local mirror of remote)

A deterministic path formula:

```plain text
$WORLD_ROOT/
  realm/<realm_id>/
    org/<org_unit_id>/
      repo/<repo_unit_id>/
        (repo root here)
      workspace/<workspace_unit_id>/
        (declared multi-repo workspace here)
    artifact/<artifact_bucket_id>/
  _inbox/            (quarantine for unsorted imports)
  _staging/          (migration staging)
  _registry/         (manifests, indexes, naming law docs)
  .audit/            (audit runs)
```

Remote mapping rule:

```plain text
realm_id = conceptual, local-only
org_unit_id  <->  GitHub organization (or user namespace)
repo_unit_id <->  GitHub repository name
```

This preserves your macro/micro separation: realms are macro (local spine), org/repo are micro (versioned leaves).

* * *

## The AI-handoff prompt pack (paste into your terminal agent)

You asked for “a prompt or chain of prompts.” Below is a pack designed for **any terminal-run agent** (Codex CLI, Gemini CLI, etc.). It assumes the agent can run shell commands and read outputs. It is written so the agent produces concrete artifacts under `$AUDIT_ROOT`.

### PROMPT 0 — Operating charter (paste first)

```plain text
You are a terminal-executing systems auditor and ontological librarian.

Mission:
1) Audit my $HOME (starting point) to discover all relevant project folders and git repositories.
2) Propose and then enforce (plan-first) a canonical local directory ontology rooted at $WORLD_ROOT.
3) Define a deterministic mapping between local ORG_UNIT/REPO_UNIT and GitHub remotes, so local mirrors remote.
4) Produce manifests and a migration plan with zero ambiguity.

Hard constraints:
- Do NOT delete anything.
- Do NOT move anything until after producing a plan and getting an explicit “EXECUTE” command from me.
- Do NOT invent remote orgs/repos. You may only infer from existing git remotes or from explicit user instructions.
- Treat repo-inside-repo as a violation unless it is a submodule or explicitly declared.
- Output all artifacts into $AUDIT_ROOT with timestamps.

Naming law:
- Use lowercase ASCII identifiers; hyphen/underscore only.
- Use stable ontology terms: ROOT, REALM, ORG_UNIT, REPO_UNIT, WORKSPACE_UNIT, ARTIFACT_UNIT.
- Prefer universal, non-branded naming (no vendor words in core ontology).

Outputs required (minimum):
- $AUDIT_ROOT/run_<timestamp>/inventory.json
- $AUDIT_ROOT/run_<timestamp>/git_repos.json
- $AUDIT_ROOT/run_<timestamp>/proposed_topology.json
- $AUDIT_ROOT/run_<timestamp>/migration_plan.md
- $AUDIT_ROOT/run_<timestamp>/exceptions.md

Start by printing the current values of: $HOME, $WORLD_ROOT, $AUDIT_ROOT, $REALMS, $VCS_HOST.
If any are missing, propose defaults and ask me to export them.
Then proceed to Phase 1.
```

### PROMPT 1 — Phase 1: Inventory ($HOME audit)

```plain text
PHASE 1: INVENTORY

Goal: build a complete, non-destructive inventory of candidate repos/projects under $HOME.

1) Create a new run directory:
   $AUDIT_ROOT/run_<timestamp>/

2) Collect:
   a) Top-level $HOME listing (human-readable).
   b) “Candidate project” directories: directories containing any of:
      - .git/
      - package.json, pyproject.toml, Cargo.toml, go.mod
      - Makefile, README*, LICENSE*
      - obsidian vault markers, or other knowledge-base markers if discovered
   c) All git repositories:
      - local path
      - is it a worktree?
      - is it bare?
      - current branch
      - remotes (names + URLs)
      - detected host/org/repo from remote URL
      - uncommitted status summary
   d) Repo nesting violations:
      - repo containing another repo (not submodule) -> flag

3) Write:
   - inventory.json (full)
   - git_repos.json (repo-focused)
   - inventory_summary.md (brief, readable summary)

You may use standard CLI tools available on macOS/Linux. Prefer ripgrep/find/git.
Do not use expensive full-file-content scans; stay metadata-first.

When Phase 1 is complete, stop and show:
- counts (repos found, unique remotes, orphan repos without remotes, suspected duplicates)
- the top 20 highest-risk anomalies
Then wait for Phase 2 prompt.
```

### PROMPT 2 — Phase 2: Ontology inference + target topology proposal

```plain text
PHASE 2: ONTOLOGY + TARGET TOPOLOGY

Goal: propose a canonical topology under $WORLD_ROOT that:
- is realm-based (REALM containers),
- groups repos into ORG_UNIT containers,
- mirrors GitHub org/repo structure wherever possible,
- includes an explicit quarantine path for unknowns.

Inputs:
- $AUDIT_ROOT/run_<timestamp>/inventory.json
- $AUDIT_ROOT/run_<timestamp>/git_repos.json

Process:
1) Infer ORG_UNIT and REPO_UNIT ids:
   - If remote is github.com, parse org/repo from the URL.
   - If no remote, set ORG_UNIT=default_orphan and propose a canonical repo_unit_id from folder name.
2) Propose REALM membership:
   - Use heuristics from folder names and repo topics (README headings only if fast).
   - If ambiguous, classify as realm=operate and mark “needs human assignment”.
3) Produce:
   - proposed_topology.json: canonical mapping {repo_path -> target_path, org_unit, repo_unit, realm, confidence}
   - naming_collisions.md: any collisions in ids, and your resolution rule
   - exceptions.md: anything you cannot classify with high confidence

Stop and present:
- the proposed $WORLD_ROOT tree (logical, not created on disk)
- the repo mapping table (current -> target)
Then wait for Phase 3 prompt.
```

### PROMPT 3 — Phase 3: Migration plan (plan-only, no moves)

```plain text
PHASE 3: MIGRATION PLAN (NO EXECUTION)

Goal: create a safe migration plan from current state to proposed topology.

Rules:
- No deletion.
- No moves yet.
- Plan must be reversible.

Plan must include:
1) Preflight checklist:
   - ensure clean git status or stash strategy
   - ensure remotes reachable
   - ensure no repo nesting issues after move
2) Step-by-step move/copy strategy:
   - prefer git-safe moves (move working directory; remote unchanged)
   - identify any repos that should become submodules or workspace members
3) Symlink strategy (optional):
   - if legacy paths must remain, propose symlinks from old -> new
4) Execution script proposal:
   - generate a bash script draft that performs the moves with rsync/mv cautiously
   - include a DRY_RUN mode via an env var, e.g. $DRY_RUN=1
5) Validation steps:
   - verify git remote continuity
   - verify repo count unchanged
   - verify no duplicate repo roots
   - generate post-move manifest and diff against pre-move

Write:
- migration_plan.md
- execute_migration.sh (draft only; do not run)
- validation_plan.md

Then stop and ask me to type exactly “EXECUTE PHASE 4” if I want you to run it.
```

### PROMPT 4 — Phase 4: Execution (only if you explicitly authorize)

```plain text
PHASE 4: EXECUTION (ONLY AFTER EXPLICIT AUTHORIZATION)

Only proceed if I have typed exactly: EXECUTE PHASE 4

1) Create $WORLD_ROOT structure (mkdir -p).
2) Perform moves in DRY_RUN mode first if $DRY_RUN=1.
3) Then perform real moves if $DRY_RUN=0.
4) Generate post-move manifests and a diff report.
5) If any step fails, halt immediately and write a failure report with rollback instructions.

Output:
- post_inventory.json
- post_git_repos.json
- diff_report.md
- rollback.md
```

* * *

## One practical detail you’ll want up front

If you truly mean “starting in my home directory,” the audit must exclude OS noise. Otherwise the agent will drown in `$HOME/Library`, caches, etc.

A sane default exclusion set (you can change it later) is to treat these as unmanaged:

```bash
export UNMANAGED_DIRS="$HOME/Library $HOME/.cache $HOME/.Trash $HOME/.local/share"
```

* * *

## If you want the “ontology law” to be self-enforcing

Add a registry file the agent maintains under:

```plain text
$WORLD_ROOT/_registry/ontology_law_v1.md
$WORLD_ROOT/_registry/topology_manifest.json
$WORLD_ROOT/_registry/repo_index.csv
```

Then every future tool/agent uses those as source-of-truth rather than re-inventing structure.

* * *

If you tell me what terminal agent you’re using (Codex CLI vs Gemini CLI vs something else), I can rewrite the prompts so they match that tool’s exact conventions (for example, how it handles multi-step plans, file writes, and command execution).

## Q: 
Design first for claude, then for codex, then gemini, then copilot

## A: 
## Common base contract (use for all four)

Set these once in your shell, then every tool-specific prompt below assumes them.

```bash
export WORLD_ROOT="$HOME/world"
export AUDIT_ROOT="$WORLD_ROOT/.audit"
export REALMS="create research operate publish archive"
export VCS_HOST="github.com"
export ORG_POLICY="mirror-local-to-remote"
export DEFAULT_ORG_UNIT="personal"
export UNMANAGED_DIRS="$HOME/Library $HOME/.cache $HOME/.config $HOME/.Trash"
```

The invariant: every run writes into `$AUDIT_ROOT/run_<timestamp>/` and **does not move anything** until you explicitly authorize “EXECUTE PHASE 4”.

* * *

## 1) Prompts designed for Anthropic Claude

This variant is optimized for “Claude Code”-style behavior: run commands, create files, keep a tight plan, stop at phase boundaries.

### Claude prompt A: bootstrap charter (paste as the first message)

```plain text
ROLE: terminal-executing systems auditor and ontological librarian.

MISSION:
Audit my $HOME (start point) to discover project folders and git repositories. Then propose a canonical local ontology rooted at $WORLD_ROOT that mirrors my remote GitHub org/repo structure. Produce manifests and a migration plan with zero ambiguity.

HARD CONSTRAINTS:
No deletion. No moves. No renames. No remote creation. You may only infer org/repo names from existing git remotes or explicit user text. Repo-inside-repo is a violation unless a declared submodule/worktree. Write all outputs into $AUDIT_ROOT/run_<timestamp>/.

NAMING LAW:
lowercase ASCII identifiers; hyphen/underscore only. Use ontology terms: ROOT, REALM, ORG_UNIT, REPO_UNIT, WORKSPACE_UNIT, ARTIFACT_UNIT. Prefer universal, non-branded ontology terms.

OUTPUTS (minimum):
inventory.json
git_repos.json
proposed_topology.json
migration_plan.md
exceptions.md

STARTUP:
1) Print current values of: HOME, WORLD_ROOT, AUDIT_ROOT, REALMS, VCS_HOST, ORG_POLICY, DEFAULT_ORG_UNIT, UNMANAGED_DIRS.
2) If any missing, propose defaults and stop.
3) If present, proceed to PHASE 1.

PHASE BOUNDARIES:
After each phase, STOP and wait for my next message (“PHASE 2”, “PHASE 3”, “EXECUTE PHASE 4”).
```

### Claude prompt B: PHASE 1 (inventory)

```plain text
PHASE 1: INVENTORY (metadata-first, no expensive full scans)

Create $AUDIT_ROOT/run_<timestamp>/.

Collect:
1) A top-level listing of $HOME (human-readable).
2) Candidate project dirs under $HOME excluding $UNMANAGED_DIRS, where a candidate has one of:
   .git/ OR package.json OR pyproject.toml OR Cargo.toml OR go.mod OR Makefile OR README* OR LICENSE*.
3) Enumerate every git repository (including nested) and capture:
   repo_path, is_bare, is_worktree, current_branch, remotes(name,url), parsed host/org/repo for github.com URLs, porcelain status summary, last_commit_hash/date.
4) Detect violations:
   repo-inside-repo (not submodule), duplicate checkouts of same remote, repos with no remotes, remotes that do not match VCS_HOST.

Write:
inventory.json (full)
git_repos.json (repo-focused)
inventory_summary.md (counts + anomalies)

Then STOP and print:
repos_found, unique_remotes, orphan_repos_without_remotes, nesting_violations_count, top_20_anomalies.
```

### Claude prompt C: PHASE 2 (ontology + topology proposal)

```plain text
PHASE 2: ONTOLOGY + TARGET TOPOLOGY

Inputs:
$AUDIT_ROOT/run_<timestamp>/inventory.json
$AUDIT_ROOT/run_<timestamp>/git_repos.json

Goal:
Propose a deterministic topology under $WORLD_ROOT:
$WORLD_ROOT/realm/<realm_id>/org/<org_unit_id>/repo/<repo_unit_id>/

Rules:
1) ORG_UNIT and REPO_UNIT:
   If remote host is github.com, parse org/repo from remote URL and use as ids (normalized).
   If no remote, set ORG_UNIT=orphan and propose REPO_UNIT from folder name (normalized).
2) REALM inference:
   Use folder/repo names and lightweight README header sniffing only if cheap; otherwise realm=operate with “needs_human_assignment”.
3) Produce:
proposed_topology.json mapping each repo_path -> target_path with fields: realm_id, org_unit_id, repo_unit_id, confidence, reasons.
naming_collisions.md with deterministic collision resolution.
exceptions.md for ambiguous/unsafe cases.

Then STOP and show a readable mapping preview (current -> proposed).
```

### Claude prompt D: PHASE 3 (migration plan, still no execution)

```plain text
PHASE 3: MIGRATION PLAN (PLAN-ONLY; DO NOT MOVE ANYTHING)

Write migration_plan.md that includes:
Preflight checks, stash/clean strategy, move strategy, optional symlink strategy, validation steps, rollback strategy.

Also write:
execute_migration.sh (draft only; includes DRY_RUN=1 mode; DO NOT RUN)
validation_plan.md

Then STOP and ask me to type exactly: EXECUTE PHASE 4
```

### Claude prompt E: PHASE 4 (execution gating)

```plain text
PHASE 4: EXECUTION (ONLY if I typed exactly: EXECUTE PHASE 4)

1) Create directories under $WORLD_ROOT.
2) Run execute_migration.sh with DRY_RUN=1 first and summarize results.
3) If I explicitly confirm DRY_RUN output is correct, run with DRY_RUN=0.
4) Generate post_inventory.json, post_git_repos.json, diff_report.md, rollback.md.

Abort on any error and write a failure report.
```

* * *

## 2) Prompts designed for OpenAI Codex

This variant assumes a Codex CLI agent that is very good at “plan → run commands → write files”, but you must hard-gate destructive operations.

### Codex prompt A: system charter

```plain text
SYSTEM CHARTER (Codex CLI)

You have shell access. You must follow a strict two-man rule:
You may run read-only commands immediately.
You may write new files under $AUDIT_ROOT immediately.
You may NOT move/rename/delete anything anywhere unless the user says: EXECUTE PHASE 4.

Objective:
Build an audited, ontology-driven local structure rooted at $WORLD_ROOT that deterministically mirrors GitHub org/repo remotes. Produce manifests and a migration script draft.

Deliverables per run:
$AUDIT_ROOT/run_<timestamp>/{inventory.json, git_repos.json, proposed_topology.json, migration_plan.md, exceptions.md}

Always begin by echoing env vars and confirming they exist. If missing, propose exports and stop.
```

### Codex prompt B: command discipline (pre-commit to safety)

```plain text
COMMAND DISCIPLINE

Allowed without further permission:
find, rg, ls, stat, du, tree, git status, git remote -v, git rev-parse, git submodule status, git worktree list, jq, python -c (read-only), writing files under $AUDIT_ROOT.

Forbidden until EXECUTE PHASE 4:
mv, rm, rmdir, git clone, git init, git remote add, git push, gh repo create, any command that changes repo history or filesystem locations outside $AUDIT_ROOT.
```

### Codex prompt C: phase macros (use as your next message to Codex)

```plain text
Implement PHASE 1 → PHASE 3 exactly as specified:

PHASE 1: inventory (metadata-first) and write inventory.json, git_repos.json, inventory_summary.md.
Stop.

PHASE 2: propose topology under $WORLD_ROOT/realm/<realm>/org/<org>/repo/<repo>/ and write proposed_topology.json, naming_collisions.md, exceptions.md.
Stop.

PHASE 3: write migration_plan.md, execute_migration.sh (draft, includes DRY_RUN=1), validation_plan.md.
Stop and request EXECUTE PHASE 4.
```

### Codex prompt D: phase 4 gating

```plain text
If and only if the user typed: EXECUTE PHASE 4
Run the migration script in DRY_RUN=1 mode, report, then wait.
Only after explicit confirmation run DRY_RUN=0.
Write post_* manifests and diff_report.md and rollback.md.
```

* * *

## 3) Prompts designed for Google Gemini

This variant assumes a Gemini CLI agent that benefits from very explicit “print outputs / stop” boundaries and concise command scopes.

### Gemini prompt A: minimal bootstrap with strict stops

```plain text
You are a terminal auditor. Start at $HOME.

Non-negotiable safety:
No deletion. No moves. No renames. No remote changes. Only read-only commands plus writing new files under $AUDIT_ROOT.

Step 0:
Print: HOME, WORLD_ROOT, AUDIT_ROOT, REALMS, VCS_HOST, ORG_POLICY, DEFAULT_ORG_UNIT, UNMANAGED_DIRS.
If any missing, propose export lines and STOP.

Then run PHASE 1 only, write:
$AUDIT_ROOT/run_<timestamp>/inventory.json
$AUDIT_ROOT/run_<timestamp>/git_repos.json
$AUDIT_ROOT/run_<timestamp>/inventory_summary.md

After PHASE 1, STOP and wait for “PHASE 2”.
```

### Gemini prompt B: PHASE 2 and PHASE 3 (send only after you see PHASE 1 results)

```plain text
PHASE 2:
Using the run directory from PHASE 1, propose:
$WORLD_ROOT/realm/<realm_id>/org/<org_unit_id>/repo/<repo_unit_id>/
Write proposed_topology.json, naming_collisions.md, exceptions.md.
STOP.

PHASE 3:
Write migration_plan.md, execute_migration.sh (draft; DRY_RUN=1 supported; do not run), validation_plan.md.
STOP and request: EXECUTE PHASE 4
```

### Gemini prompt C: PHASE 4 execution gating

```plain text
Proceed only if user typed exactly: EXECUTE PHASE 4

Run execute_migration.sh with DRY_RUN=1 and summarize.
STOP.
Proceed to DRY_RUN=0 only after explicit confirmation.
Write post_inventory.json, post_git_repos.json, diff_report.md, rollback.md.
Abort on any error.
```

* * *

## 4) Prompts designed for GitHub Copilot

This variant assumes “Copilot in terminal” behavior (often good at generating scripts and incremental command sequences), so you force it into “generate a script + run read-only probes + stop” mode.

### Copilot prompt A: script-first posture

```plain text
You are operating in a terminal with a safety harness.

Rule 1:
Before running any multi-step audit, generate a single script file under $AUDIT_ROOT/run_<timestamp>/ called audit_phase1.sh that performs PHASE 1 using read-only commands only. Then show me the script. Do not run it until I say RUN PHASE 1.

Rule 2:
No filesystem moves/renames/deletes until I say EXECUTE PHASE 4.

Step 0:
Echo env vars: HOME, WORLD_ROOT, AUDIT_ROOT, REALMS, VCS_HOST, ORG_POLICY, DEFAULT_ORG_UNIT, UNMANAGED_DIRS.
If missing, propose exports and STOP.
```

### Copilot prompt B: what the phase scripts must do

```plain text
PHASE 1 script requirements (audit_phase1.sh):
1) Create $AUDIT_ROOT/run_<timestamp>/.
2) Inventory candidates under $HOME excluding $UNMANAGED_DIRS.
3) Enumerate git repos and capture remotes, branch, status summary, last commit metadata.
4) Write inventory.json, git_repos.json, inventory_summary.md.
5) Exit non-zero on command failure, but never mutate paths outside $AUDIT_ROOT.

After writing the script, STOP and ask me to say: RUN PHASE 1
```

### Copilot prompt C: follow-on phases as scripts

```plain text
After PHASE 1 results exist, generate (but do not run) these scripts:
audit_phase2.sh -> writes proposed_topology.json, naming_collisions.md, exceptions.md
audit_phase3.sh -> writes migration_plan.md, execute_migration.sh (draft only), validation_plan.md

Then STOP and ask for EXECUTE PHASE 4.
```

### Copilot prompt D: execution harness (explicitly gated)

```plain text
If and only if I say EXECUTE PHASE 4:
1) Run execute_migration.sh with DRY_RUN=1 and STOP.
2) Only after I approve, run DRY_RUN=0.
3) Write post manifests and rollback instructions.
```

* * *

## Practical usage pattern (works across all four)

Copy the relevant tool’s “bootstrap charter” first. Let it complete Phase 1 and stop. Then send the Phase 2 prompt, then Phase 3. Only after you read the migration plan do you issue “EXECUTE PHASE 4”.

If you want, I can also give you a single canonical `ontology_law_v1.md` template to store at `$WORLD_ROOT/_registry/ontology_law_v1.md` so every future agent run is forced to conform.

## Q: 
If you want, I can also give you a single canonical ontology_law_v1.md template to store at $WORLD_ROOT/_registry/ontology_law_v1.md so every future agent run is forced to conform.

## A: 
```md
# ontology_law_v1.md

## 0. Identity

- **Document ID:** ontology_law_v1
- **Status:** normative
- **Root of truth:** `$WORLD_ROOT`
- **Registry root:** `$WORLD_ROOT/_registry`
- **Audit root:** `$AUDIT_ROOT`
- **Versioning:** this document is the canonical ontology law; any automation MUST read it before acting.

---

## 1. Scope

This law governs:

- Local directory topology rooted at `$WORLD_ROOT`
- Classification of local content into ontology layers
- Deterministic mapping of local ORG_UNIT/REPO_UNIT to remote Git hosting namespaces
- Audit, planning, and (optionally) execution of migrations

This law does NOT govern:

- Editor-specific workspace configs (unless explicitly registered)
- Build systems
- Artifact formats beyond placement and naming

---

## 2. Ontology primitives

### 2.1 Units (macro → micro)

- **ROOT**: canonical top container for governed space (`$WORLD_ROOT`)
- **REALM**: major life/system domains (macro classification)
- **ORG_UNIT**: institutional boundary that owns repositories (maps to remote namespace)
- **REPO_UNIT**: a versioned unit rooted at a VCS repository
- **WORKSPACE_UNIT**: a declared multi-repo working bundle
- **ARTIFACT_UNIT**: outputs (renders/exports/builds/releases) that are not sources

### 2.2 Unit identifiers

All unit IDs MUST:

- be lowercase ASCII
- use only: `a-z 0-9 _ -`
- contain no spaces
- be stable over time (no date prefixes unless the date is semantically intrinsic)
- avoid vendor branding in ontology terms

---

## 3. Canonical directory topology

### 3.1 Required top-level structure

`$WORLD_ROOT` MUST contain:

```text
$WORLD_ROOT/
  realm/
  _inbox/
  _staging/
  _registry/
```

### 3.2 Realm structure (required)

For each REALM:

```plain text
$WORLD_ROOT/realm/<realm_id>/
  org/<org_unit_id>/
    repo/<repo_unit_id>/        # repo root lives here
    workspace/<workspace_id>/   # optional
  artifact/<artifact_bucket_id>/ # optional
```

### 3.3 Registry structure (required)

```plain text
$WORLD_ROOT/_registry/
  ontology_law_v1.md
  topology_manifest.json
  repo_index.csv
  exceptions.md
```

### 3.4 Inbox + staging (required)

*   `$WORLD_ROOT/_inbox/` is the only permitted landing zone for unsorted imports.
    
*   `$WORLD_ROOT/_staging/` is the only permitted landing zone for migration steps.
    

* * *

## 4. Deterministic mapping to remotes

### 4.1 Remote host policy

*   Canonical host is `$VCS_HOST` (default: `github.com`).
    
*   A REPO_UNIT MAY have remotes on other hosts, but the canonical mapping MUST prefer `$VCS_HOST` when present.
    

### 4.2 ORG_UNIT inference

For a given repository:

1.  If any remote URL host matches `$VCS_HOST`, parse `<org>/<repo>` from that URL.
    
2.  Set `org_unit_id = <org>` (normalized).
    
3.  If no matching remote exists, set `org_unit_id = orphan`.
    

### 4.3 REPO_UNIT inference

1.  If remote URL yields `<org>/<repo>`, set `repo_unit_id = <repo>` (normalized).
    
2.  Else derive from local folder basename (normalized).
    

### 4.4 Canonical local path formula

For each REPO_UNIT:

```plain text
$WORLD_ROOT/realm/<realm_id>/org/<org_unit_id>/repo/<repo_unit_id>/
```

* * *

## 5. Classification rules

### 5.1 REALM assignment

A repository MUST have exactly one REALM.

*   If confidently inferable by name/path heuristics, assign that REALM.
    
*   Otherwise assign `operate` and mark `needs_human_assignment=true` in manifests.
    

### 5.2 WORKSPACE_UNIT declaration

A WORKSPACE_UNIT MUST be explicitly declared via a registry record (see §7).  
Implicit “folders with many repos” are not workspaces until declared.

### 5.3 ARTIFACT placement

Artifacts MUST NOT live inside REPO_UNIT roots unless they are:

*   build outputs that are explicitly ignored by VCS, or
    
*   versioned outputs intentionally tracked (rare; must be declared)
    

Preferred artifact placement:

```plain text
$WORLD_ROOT/realm/<realm_id>/artifact/<artifact_bucket_id>/
```

* * *

## 6. Structural invariants (must always hold)

### 6.1 Repo uniqueness

Each REPO_UNIT MUST have:

*   exactly one canonical local root (the target path)
    
*   at least one remote OR be explicitly marked `orphan=true`
    

### 6.2 Repo nesting

Repo-inside-repo is prohibited unless:

*   it is a declared git submodule, or
    
*   it is a declared workspace member and the nesting is purely directory containment (not VCS containment)
    

Violations MUST be recorded in `exceptions.md` and blocked from execution until resolved.

### 6.3 No destructive actions without explicit authorization

Agents MUST NOT run any destructive or relocating commands (including `mv`, `rm`, `git remote add`, `git push`, `gh repo create`) unless the user has typed:

```plain text
EXECUTE PHASE 4
```

### 6.4 Plan-first guarantee

Before any execution, an agent MUST produce:

*   `inventory.json`
    
*   `git_repos.json`
    
*   `proposed_topology.json`
    
*   `migration_plan.md`
    
*   `exceptions.md`
    

* * *

## 7. Registry records (source of truth)

### 7.1 topology_manifest.json (required)

This file is the canonical registry mapping.

Minimum schema (normative):

```json
{
  "ontology_version": "v1",
  "world_root": "$WORLD_ROOT",
  "generated_at": "ISO-8601",
  "realms": ["create", "research", "operate", "publish", "archive"],
  "repos": [
    {
      "repo_unit_id": "example_repo",
      "org_unit_id": "example_org",
      "realm_id": "create",
      "canonical_path": "$WORLD_ROOT/realm/create/org/example_org/repo/example_repo",
      "remotes": [
        {"name": "origin", "url": "https://github.com/example_org/example_repo.git"}
      ],
      "needs_human_assignment": false,
      "orphan": false,
      "notes": ""
    }
  ],
  "workspaces": [],
  "exceptions": []
}
```

### 7.2 repo_index.csv (required)

Columns (normative):

```plain text
realm_id,org_unit_id,repo_unit_id,canonical_path,origin_url,orphan,needs_human_assignment
```

### 7.3 exceptions.md (required)

Must include:

*   nesting violations
    
*   naming collisions
    
*   ambiguous realm assignments
    
*   duplicates and suspected mirrors
    

* * *

## 8. Audit protocol

### 8.1 Phase structure (normative)

*   **PHASE 1:** inventory (read-only; write manifests)
    
*   **PHASE 2:** ontology inference + proposed topology (write proposal manifests)
    
*   **PHASE 3:** migration plan + draft execution script (no execution)
    
*   **PHASE 4:** execution (only after explicit authorization)
    

### 8.2 Audit run output location

Each run MUST write:

```plain text
$AUDIT_ROOT/run_<timestamp>/
```

and MUST NOT overwrite prior runs.

* * *

## 9. Execution protocol (Phase 4)

### 9.1 Dry run

Execution MUST support:

*   `DRY_RUN=1` for no-op simulation
    
*   `DRY_RUN=0` for actual moves
    

Dry run MUST be performed first and summarized.

### 9.2 Validation (required)

After execution, agent MUST produce:

*   `post_inventory.json`
    
*   `post_git_repos.json`
    
*   `diff_report.md`
    
*   `rollback.md`
    

Validation checks MUST include:

*   repo count unchanged (unless explicitly waived)
    
*   each repo still has expected remotes
    
*   no new nesting violations
    
*   canonical paths match `topology_manifest.json`
    

* * *

## 10. Collision resolution (deterministic)

If two repos resolve to the same `<org_unit_id>/<repo_unit_id>`:

1.  Prefer the one whose origin URL exactly matches the canonical remote.
    
2.  For the other, append a suffix:
    
    *   `-alt1`, `-alt2`, … (stable ordering by path sort)
        
3.  Record decision in `naming_collisions.md` and `exceptions.md`.
    

* * *

## 11. Unmanaged space

Anything outside `$WORLD_ROOT` is unmanaged by default.

Within `$WORLD_ROOT`, these are unmanaged unless explicitly registered:

*   `$WORLD_ROOT/_inbox/*` (until classified)
    
*   `$WORLD_ROOT/_staging/*` (temporary)
    
*   any directory listed in `$UNMANAGED_DIRS`
    

* * *

## 12. Conformance requirement for future agents

Any agent/tool operating on this system MUST:

1.  Read this file.
    
2.  Read `$WORLD_ROOT/_registry/topology_manifest.json` if it exists.
    
3.  Refuse to execute Phase 4 if:
    
    *   exceptions include unresolved nesting violations, or
        
    *   canonical path collisions remain unresolved, or
        
    *   user did not explicitly authorize execution.
        

End of law.

```plain text

```

## Q: 
An earlier draft of organs, this too needs to be cleansed of it's solid rules, but the theory itself is sound, now it can be expanded & expounded upon: Good. We will formalize this as a system, not as branding, motivation, or aspiration. What follows is a binding architectural definition. Nothing here is decorative. Each section defines purpose, permissions, prohibitions, cadence, and interfaces. This is how the structure stays sane when energy increases. I will proceed organ by organ, using declarative prose rather than lists. Treat this as a first charter draft. ⸻ ORGAN I Function: Conceptual / Symbolic Engine This organization exists to generate, test, and preserve formal thinking. Its output is not art, not tools, not products. Its output is rules, grammars, symbolic models, ontologies, taxonomies, and meaning-structures. It is upstream of all other organs. Nothing here is obligated to be legible, marketable, or complete. Partiality is allowed. Obscurity is allowed. Difficulty is allowed. This organ is permitted to ask questions that will never resolve. It is permitted to contradict itself over time. It is permitted to remain unused for long periods. This organ is prohibited from audience optimization, commercial framing, or performative explanation. No pitches. No onboarding. No simplification for external consumption. Cadence is slow and irregular. Work here happens when pressure demands it, not on schedule. Interfaces outward only through orchestration, never directly to marketing or community. When something stabilizes conceptually, orchestration decides whether it becomes art, tooling, or remains dormant. ⸻ ORGAN II Function: Art / Enactment / Experiential Systems This organization exists to turn symbolic structures into events, experiences, performances, and temporal works. It is where thought enters time and meets bodies, audiences, sound, image, and ritual. The primary unit here is not the object but the occurrence. Finishedness is optional. Presence is mandatory. This organ is permitted to be public, opaque, demanding, and uneven. It may produce fragments, scores, performances, recordings, scripts, installations, or systems that only make sense in motion. This organ is prohibited from explaining itself exhaustively. It is also prohibited from carrying financial responsibility alone. Art here does not need to justify its existence economically. Cadence is project-based. Some works may be quick; others may take years. Silence between releases is acceptable. Interfaces outward to the public-process organ and occasionally to community. It never interfaces directly with marketing without mediation. ⸻ ORGAN III Function: Commerce / Applied Labor / Survival Surface This organization exists to perform work in the world under constraint. It acknowledges the profane necessity of income, clients, deadlines, and deliverables. Its outputs are tools, services, consulting, applied systems, client work, and monetizable artifacts that may or may not be aesthetically elevated. This organ is permitted to be pragmatic, efficient, boring, and clear. It may reuse ideas developed elsewhere without pretending they are sacred. This organ is prohibited from defining the meaning of the system. It does not decide values, directions, or symbolic truth. It funds time and attention; it does not replace them. Cadence is contractual and deadline-driven. Interfaces outward to clients and markets, inward only through orchestration. It does not touch raw theory or unfinished art directly. ⸻ ORGAN IV Orchestration Layer (name intentionally deferred) Function: Governance / Flow Control / System Integrity This organ exists to coordinate, not to create. It holds the map of the system and enforces boundaries. It decides what moves between organs, when, and under what conditions. It maintains documentation, dependency logic, graduation paths, and archival coherence. This organ is permitted to say “not yet,” “never,” and “this moves elsewhere.” It is also permitted to be invisible. It is prohibited from generating content, chasing attention, or becoming a meta-art project. Cadence is steady and quiet. This organ works best when no one notices it. All other organs report to this layer structurally, even if emotionally they resist it. ⸻ ORGAN V Public Process / Building in Light Function: Translucent Visibility / Attention Filtering This organ exists to make process visible without resolving it. It releases essays, fragments, marginalia, notebooks, conversations, sketches, annotations, rehearsal traces, and partial thoughts. Its job is not explanation but legibility. It allows others to see how thinking unfolds, without demanding comprehension or agreement. This organ is permitted to be unfinished, contradictory, and exploratory. It is permitted to show work midstream. It is prohibited from daily performance, emotional confession, or algorithmic obedience. Silence is acceptable. Cadence is rhythmic but sparse. Enough to signal continuity; not enough to create pressure. Interfaces inward from marketing and outward to community. It is the membrane between system and world. ⸻ ORGAN VI Community Function: Reciprocal Continuity This organ exists only for people who have already demonstrated sustained interest. It is not for discovery. It is not for scale. This is where conversation, shared reference, reading groups, salons, Discords, or private forums live. Presence matters more than growth. This organ is permitted to be small, slow, and demanding. It may require commitment. It is prohibited from growth optimization, performative debate, or identity theater. Cadence is human. You show up here selectively and honestly, not constantly. It receives people only after filtering through public process, never directly from marketing. ⸻ ORGAN VII Marketing / Attention Routing Function: Discoverability Infrastructure This organ exists purely to route attention. It is not expressive. It is not sincere. It is not personal. It announces, points, schedules, republishes, and redirects. Automation is preferred. Templates are encouraged. This organ is permitted to be mechanical, repetitive, and boring. It is prohibited from argument, confession, explanation, or real-time emotional engagement. Cadence is consistent but detached. It routes outward to public process, never directly to community or raw work. ⸻ PERSONAL PROFILE Liminal Incubation Zone Your personal profile is not an organ of production. It is a transitional space. Drafts, experiments, half-formed tools, temporary collaborations, and volatile ideas live here. Nothing here is obligated to persist. When something stabilizes, orchestration moves it elsewhere. This profile is permitted to change rapidly. It is prohibited from becoming a dumping ground for unresolved pressure. ⸻ FINAL LOCK You are not adding organs because you are confused. You are externalizing pressures so they stop collapsing inward. The system is now complete enough to operate. The next step is not expansion. It is enforcement: honoring these boundaries when temptation arises. If you want, the next phase can be a one-page operating constitution that you return to when energy spikes, doubt creeps in, or outside voices distort priorities. That is how systems like this survive contact with reality. Short answer: no major conceptual organs are missing. Longer, more important answer: there are a few mundane but critical support organs that must exist, but they should remain deliberately unglamorous and minimally expressive. What you have now is complete at the level of meaning-production and circulation. What remains are stabilizers, not creative extensions. Missing these does not make a system incoherent; it makes it fragile under stress. I will name them plainly, without mystique. ⸻ 1. ADMINISTRATIVE / LEGAL / FINANCIAL BACKPLANE Status: Required, but intentionally boring Every durable system has a backplane that handles incorporation, accounting, contracts, IP boundaries, taxes, licenses, payments, insurance, and compliance. This is not an organ that “creates.” It prevents leakage and catastrophe. This function should never be aestheticized, theorized, or mythologized. The moment it becomes symbolic, it stops doing its job. It can live as documents, folders, checklists, advisors, and routines. It does not need a GitHub organization unless tooling demands it. This backplane reports only to orchestration. If neglected, it will eventually collapse commerce, poison art, and drain attention. If handled quietly, it disappears from consciousness—which is ideal. ⸻ 2. ARCHIVAL / MEMORY / VERSIONING Status: Lightly present, may need explicit reinforcement You already have archival instincts, but there is a difference between storage and memory. This organ exists to ensure that ideas, artifacts, conversations, versions, and decisions are recoverable and traceable over years. This is not public-facing. It is not expressive. It is not social. It is for future-you, collaborators, and institutional continuity. Think of it as “Alexandria without performance.” It may live inside orchestration or as a quiet sub-layer. It does not need expansion; it needs consistency. ⸻ 3. PERSONAL MAINTENANCE / HUMAN SUSTAINABILITY Status: Non-negotiable, but not a system organ This is the one people resist naming, and the one that quietly destroys otherwise brilliant architectures. Sleep, movement, sobriety (or at least reduction), mental health support, rhythm, solitude, and embodied repetition are not “self-care.” They are infrastructure. They are load-bearing. This is not something to brand, document publicly, or intellectualize. It is something to protect. When this fails, people misdiagnose the failure as loss of calling, loss of genius, or loss of relevance. In reality, it is just an exhausted nervous system. This does not belong in GitHub, Discord, or public process. It belongs in routine. ⸻ What You Are Not Missing You are not missing: • Another expressive organ • Another theoretical layer • Another mythic frame • Another meta-meta-system • Another public-facing identity Adding any of those now would be avoidance disguised as ambition. ⸻ The Key Diagnostic Question A complete system does not feel “finished.” It feels able to absorb pressure without distorting. Right now, your system can: • Generate meaning without demanding validation • Circulate work without collapsing into performance • Earn money without redefining value • Invite people without surrendering boundaries That is what “complete enough to operate” means. From here on, progress comes from use, not design. From friction, not ideation. From enforcement, not expansion. If you ever feel the urge to add another organ, that urge should trigger a single question: “Which existing boundary am I trying not to enforce?” That question will save you years. You are not missing something essential. You are standing at the point where restraint becomes the creative act. GitHub Operating Protocols for the Organ System This defines concrete, GitHub-native best practices for your multi-org architecture, using environment-style identifiers so the system is portable across time and platforms. Environment Identifiers Use these identifiers consistently in docs, READMEs, and automation. $PROFILE_ROOT = github.com/$USER_ID $ORG_THEORY = github.com/organvm-i-theoria $ORG_ART = github.com/organvm-ii-poiesis $ORG_COMMERCE = github.com/organvm-iii-ergon $ORG_ORCH = github.com/$ORG_ORCHESTRATION_ID $ORG_PUBLIC = github.com/$ORG_PUBLIC_PROCESS_ID $ORG_COMM = github.com/$ORG_COMMUNITY_ID $ORG_MKTG = github.com/$ORG_MARKETING_ID $REPO_KIND ∈ {theory, art, tool, commerce, orchestration, public, community, marketing} $LIFECYCLE ∈ {incubating, active, stable, deprecated, archived} $VISIBILITY ∈ {public, internal, private} ⸻ 1. Org-Level Standards 1.1 Security Baseline Require 2FA for every organization. Enforce SSO if you ever add enterprise identity. Prefer least-privilege: default read access, elevate per team and per repo. Turn on GitHub security features by default for all orgs where code exists: Dependabot alerts and updates, secret scanning, and code scanning (where applicable). Use the same rulesets across orgs where possible. 1.2 Teams as “Organs Within the Organ” Define stable teams once, reuse everywhere. $TEAM_OWNERS $TEAM_MAINTAINERS $TEAM_REVIEWERS $TEAM_RELEASE $TEAM_COMMUNITY_STEWARDS $TEAM_MARKETING_AUTOMATION Protocol: repos are never owned by individuals; they are owned by teams. Individuals rotate; teams persist. 1.3 Repository Defaults Every repo gets the same minimal contract. README.md LICENSE CODE_OF_CONDUCT.md (only where community interaction occurs) CONTRIBUTING.md SECURITY.md (commerce + tooling at minimum) CODEOWNERS CHANGELOG.md (stable + commerce + tools) ⸻ 2. Cross-Organ Taxonomy 2.1 Repo Naming Rules Use a deterministic prefix that encodes function and avoids future renames. $REPO_NAME = $REPO_KIND--$SUBJECT--$QUALIFIER examples: theory--semiotics--recursion art--metamorphoses--score tool--ingestion--pipeline commerce--client--deliverable orchestration--governance--charter public--field-notes--2026 community--salon--reading-circle marketing--syndication--scheduler Avoid “misc,” “test,” “stuff,” “final,” “v2.” Use $LIFECYCLE tags instead (see below). 2.2 Lifecycle as First-Class Metadata Lifecycle must be visible at a glance in the repo header and as topics. topics: $REPO_KIND, $LIFECYCLE, $DOMAIN (optional) Example: theory, active, myth-systems. README header includes: Status: $LIFECYCLE Owner: $TEAM_OWNERS Interfaces: {inbound, outbound} Promotion path: $PROMOTION_RULE_ID ⸻ 3. Branching and Change Control 3.1 Simple Default Branch Model Use main everywhere. Add dev only when it clearly reduces risk (typically in $ORG_COMMERCE and some $ORG_TOOL repos). Keep models consistent across repos to prevent cognitive thrash. 3.2 Branch Protections (Rulesets) For all stable or public repos, enforce: Require PRs Require at least 1 review (2 for commerce/tooling) Require status checks (CI, lint, tests if they exist) Require linear history or squash merges (choose one globally) Restrict who can push to main (maintainers only) Theory repos may relax tests but should not relax review where the change affects cross-repo semantics (ontologies, schemas, naming). ⸻ 4. Issue, PR, and Documentation Protocol 4.1 Labels are a Shared Ontology Standardize labels across all orgs so issues are portable. type: bug | enhancement | refactor | docs | governance | research | release priority: p0 | p1 | p2 | p3 state: blocked | needs-review | needs-decision organ: theory | art | tool | commerce | orchestration | public | community | marketing lifecycle: incubating | active | stable | deprecated | archived 4.2 PR Template Requirements Every PR answers the same questions, even for “small” changes. Intent: what changed and why Scope: what is affected Risk: what can break Interfaces: which organs/repos this touches Rollback: how to undo if needed Theory PRs must explicitly state whether they are “normative” (rules) or “descriptive” (notes). This prevents accidental governance drift. ⸻ 5. Automation Strategy 5.1 Reusable Workflows as Orchestration Put shared GitHub Actions in $ORG_ORCH as versioned reusable workflows. orchestration--workflows--reusable Then each repo calls: uses: $ORG_ORCH/orchestration--workflows--reusable/.github/workflows/<workflow>.yml@vX 5.2 Automation Boundaries by Organ Marketing automation belongs in $ORG_MKTG and must be impersonal. No secrets that can damage you if leaked. Prefer read-only tokens. Public process can auto-publish summaries or changelogs, but must not auto-post raw private notes. Commerce automation can handle packaging, invoices, deliverable builds, but must keep client identifiers and confidential assets out of public logs. ⸻ 6. Visibility Protocols by Organ Use visibility as a semantic tool, not a mood. 6.1 Recommended Defaults $ORG_THEORY: private or internal by default; public only when stabilized and non-sensitive. $ORG_ART: public when work is meant to be experienced; private when in rehearsal or fragile. $ORG_COMMERCE: private by default; public only for generic reusable components without client IP. $ORG_ORCH: internal by default; public only for a “public constitution” subset if you want transparency. $ORG_PUBLIC: public by definition; it is the membrane. $ORG_COMM: private or internal; membership-gated. $ORG_MKTG: public for templates and schedules; private for credentialed automation only. ⸻ 7. Promotion and Migration Protocols 7.1 Promotion Rules A repo moves when it crosses a threshold, not when you “feel like it.” Incubation starts at $PROFILE_ROOT. Promotion occurs when at least one of these is true: the repo has a stable name, a stable scope, a README that declares interfaces, and a defined owner team. Promotion destinations: If it defines rules, schemas, ontologies → $ORG_THEORY If it is an experience or artwork → $ORG_ART If it is code that others depend on → $ORG_TOOL (or tools inside an existing org) If it is paid work or revenue-bearing assets → $ORG_COMMERCE If it is governance, workflows, routing → $ORG_ORCH If it is process artifacts intended for discovery → $ORG_PUBLIC If it is conversation infrastructure → $ORG_COMM If it is discoverability plumbing → $ORG_MKTG 7.2 Deprecation and Archival Deprecation is a state, not a grave. deprecated: frozen, still referenced archived: read-only, no future work expected A deprecated repo must include a replacement pointer in its README. An archived repo must include both a replacement pointer and a final “why it ended” note to prevent future confusion. ⸻ 8. “Public Process” Implementation Without Social-Media Drain For $ORG_PUBLIC, make the unit of output small and indexable. Use one repo per stream, not one mega-repo: public--field-notes public--essays public--interviews public--scores public--marginalia Each stream repo uses releases as “chapters” (vYYYY.MM) so the public can follow without needing you to post constantly elsewhere. ⸻ 9. Minimal “Start Here” Routing To prevent the system from being illegible, create one routing repo per org: orchestration--start-here theory--start-here art--start-here commerce--start-here public--start-here community--start-here marketing--start-here Each “start here” repo is allowed to be simple and explanatory. Other repos are not required to be. ⸻ 10. The Single Most Important Rule Orchestration owns interfaces. Production owns content. If a repo change alters naming, schemas, lifecycle meaning, cross-repo dependencies, or promotion rules, it is an orchestration concern even if the code lives elsewhere. That is how you prevent entropy. ⸻ If you want the next step, I would formalize this into a single $GITHUB_CONSTITUTION.md plus a canonical repo template directory you can clone into any new repo (README skeleton, labels, CODEOWNERS, issue/PR templates, workflow stubs). ---- Before we proceed, does this sequence of data fit into the unity goal or are we complicating and it should be deferred? Should we first run through ingestion and digestion and unification process then with data make these decisions?

## A: 
## Does this “organ” charter serve the unity goal, or is it premature?

It serves the unity goal **only if you demote it from “binding rules” to “routing semantics.”** Right now it reads like an enforcement constitution. That’s useful later, but it risks locking you into boundaries you haven’t yet operationally proven in your filesystem + repo topology.

The unity goal you described is primarily an **ontological unification problem** across `$HOME → $WORLD_ROOT → remote namespaces`. That problem needs hard invariants and deterministic mapping first. The organ charter is a **semantic layer** that becomes accurate only after you can see the real inventory: what exists, what’s duplicated, what’s orphaned, what’s nested, what’s actually active.

So: the theory is sound. The timing is the question.

## The correct sequencing

### Phase A: topology unification (hard law)

This is your “glorious certainty” layer.

It creates a deterministic mapping like:

`$WORLD_ROOT/realm/<realm_id>/org/<org_unit_id>/repo/<repo_unit_id>/`

This phase produces manifests and migration plans, and it is the only phase that should be treated as binding at first.

### Phase B: organ semantics (soft law)

Only after Phase A, you can assign “organs” to things you can actually point at, not ideas in the air.

At that point, each organ becomes a **tagging + routing system** that answers:

What kind of thing is this, what does it output, and what is allowed to touch it?

### Phase C: enforcement (selective law)

Only when Phase B has been used enough times to reveal friction do you harden any rules.

That’s when “permissions/prohibitions” become real, because you’ve seen what breaks you.

## What to “cleanse” in this draft (without losing its power)

Your draft has two kinds of statements mixed together.

### The statements you should keep hard

These are invariants that prevent collapse and contamination:

Orchestration decides what moves between organs.

Commerce does not decide meaning.

Marketing is routing, not selfhood.

Community is not discovery.

Those are load-bearing boundaries.

### The statements you should soften

These are behavioral absolutes that will eventually be violated for good reasons:

“Never explain itself exhaustively.”

“Cadence is slow and irregular.”

“Never interfaces directly.”

In practice you’ll need overrides. The cleanse is to convert absolutes into defaults plus override conditions.

So the rewrite pattern is:

“Default: X. Override only when Y is true. Record override in `$WORLD_ROOT/_registry/exceptions.md`.”

That preserves restraint without becoming brittle.

## A more operational form: Organ = routing contract, not identity

If you want this to actually _run the system_ rather than inspire it, each organ definition should be rewritten in a uniform schema that is enforceable by orchestration.

Use this structure per organ, in declarative prose (no lists needed):

Name.

Purpose as a single sentence.

Inputs.

Outputs.

Interfaces allowed (who may pull from it, who may push to it).

Default cadence.

Default visibility.

Anti-goals.

Override rule.

Graduation rule (how something exits the organ, and into what).

Once written this way, orchestration can implement it as a manifest policy, not vibes.

## Where this fits the unity goal concretely

After the `$HOME → $WORLD_ROOT` audit, orchestration can write one file:

`$WORLD_ROOT/_registry/topology_manifest.json`

Then you add one additional file:

`$WORLD_ROOT/_registry/organ_manifest.json`

That second file is where “organs” become real: it maps each `repo_unit_id` (or workspace) to an `organ_id`, plus interface and visibility defaults.

Meaning: the organ model becomes a **labeling and routing layer** sitting on top of the unified topology, not a parallel universe.

## Should you defer organ decisions until after ingestion/digestion?

Defer **hard** organ decisions, yes.

Do not defer the **organ vocabulary**, because it’s useful during ingestion as a classification hint. The practical compromise is:

During audit, you allow tentative organ tags like `organ_candidate=theory|art|commerce|orchestration|public|community|marketing` with `confidence` and `reasons`.

After audit, you freeze only what you’re confident about, and everything else stays “unassigned” until it proves itself.

That keeps unity moving forward without forcing premature taxonomy.

## The smallest next step that preserves momentum

Take your current draft and refactor it into two documents:

`$WORLD_ROOT/_registry/ontology_law_v1.md` stays hard and filesystem/repo-focused.

`$WORLD_ROOT/_registry/organ_charter_v0.md` becomes explicitly soft:

It contains defaults, interface rules, and override logging requirements, but it states clearly that enforcement is deferred until after topology unification and at least one full operating cycle.

If you want, I can rewrite your organ text into that operational “routing contract” form while preserving the theory and removing brittle absolutes, and I’ll make it directly mappable into an `organ_manifest.json` that orchestration can enforce.

## Q: 
rewrite your organ text into that operational “routing contract” form while preserving the theory and removing brittle absolutes, and I’ll make it directly mappable into an organ_manifest.json that orchestration can enforce.

## A: 
```md
# organ_charter_v0.md

## 0. Status and intent

This document defines organs as routing contracts, not as identity, branding, aspiration, or mood. It is operational. It exists to prevent contamination between functions while allowing deliberate transfer when justified.

This is version `v0` by design. Defaults are declared strongly. Absolutes are avoided. Any deviation is allowed only via an override record logged by orchestration.

This charter is subordinate to `$WORLD_ROOT/_registry/ontology_law_v1.md`. When conflict exists, the ontology law prevails.

---

## 1. Shared definitions

An **organ** is a bounded system region with a purpose, inputs, outputs, and interface constraints. An organ may map to a remote namespace, a local realm, a workspace, or a set of repositories.

A **transfer** is any movement of material across organ boundaries, including copying patterns, promoting a repository, reclassifying a repo’s organ, or publishing outputs outward.

An **override** is an intentional violation of an organ’s defaults justified by conditions and recorded as a durable event in the registry.

**Orchestration** is the only layer authorized to approve transfers and overrides. Production organs may request transfers, but they do not execute boundary changes.

---

## 2. Global rules (apply to every organ)

Default behavior is not permissionless flow. Default behavior is containment. Any flow is a transfer.

Every organ must maintain a stable interface statement: what it may receive, what it may emit, and what it must not touch directly.

Every organ has a default visibility profile. Visibility may vary per repo, but deviations must be recorded when they alter risk.

Every organ has a default cadence. Cadence is not a moral requirement; it is load management. Cadence may be broken without guilt; when it breaks for structural reasons, orchestration records why.

Every organ boundary exists to protect at least one of these invariants: conceptual integrity, aesthetic integrity, economic integrity, community integrity, or attention integrity.

---

## 3. Override protocol (how to break defaults without breaking the system)

Overrides are allowed. Unlogged overrides are not.

An override record must include: timestamp, requesting organ, approving organ (orchestration), affected repositories or artifacts, the default being overridden, the reason, the risk, and the rollback path.

Overrides are not debate. Overrides are governance.

---

## 4. Organs as routing contracts

### ORGAN_I — conceptual_symbolic_engine

Purpose is to generate and preserve formal thinking: rules, grammars, symbolic models, ontologies, taxonomies, and meaning-structures. Its outputs are structures of thought, not products and not audience-facing explanations.

Inputs are questions, contradictions, drafts, and unresolved frames. It may ingest material from any organ only when the goal is conceptual clarification rather than production delivery.

Outputs are documents and schemas that can be referenced by other organs. Outputs may remain partial indefinitely without penalty.

Default interface prohibits direct coupling to marketing and prohibits commercial framing. This organ may be externally legible, but legibility is never the governing constraint.

Cadence defaults to pressure-driven and irregular. This is a system feature, not a defect.

Default transfer rule is that conceptual material graduates only when it becomes stable enough to function as a dependency. Graduation is executed by orchestration, not by this organ.

Default override condition is a time-critical operational need that requires conceptual resolution for safety or coherence. Any such override must be logged.

---

### ORGAN_II — art_enactment_experiential_systems

Purpose is to translate symbolic structures into events and experiences: performances, temporal works, scores, scripts, installations, recordings, and systems that only resolve in motion.

Inputs are conceptual structures from ORGAN_I, process traces from ORGAN_V, or constraints from ORGAN_III that meaningfully shape form. Inputs may also be purely intuitive, without upstream justification.

Outputs are occurrences and their traces: documentation, recordings, notations, versions, and fragments. Finishedness is not required; the system expects unevenness.

Default interface permits outward contact with public process and, selectively, community. Direct marketing contact is discouraged by default; when used, it should be mediated through public process or orchestration to avoid distortion.

Default financial responsibility is not assigned to this organ. It may generate monetizable artifacts, but it is not required to justify itself economically.

Cadence defaults to project-based with acceptable silence. The system treats gaps as normal.

Default override condition is when the work’s survival depends on a specific marketing or commerce action. Orchestration may approve narrow, logged exceptions.

---

### ORGAN_III — commerce_applied_labor_survival_surface

Purpose is to perform work under constraint: income, clients, deadlines, deliverables, and pragmatic systems. Its outputs are services, tools, consulting, and monetizable artifacts.

Inputs are client constraints, market demands, and selectively imported patterns from other organs. Imports from ORGAN_I and ORGAN_II are permitted only through orchestration, and only when doing so reduces cost or increases coherence without forcing meaning claims.

Outputs are deliverables that must be clear, stable, and testable. Boredom and clarity are permitted and often optimal.

Default interface prohibits this organ from defining system meaning, values, or direction. It may fund time and attention; it may not redefine the system’s ontology.

Cadence defaults to contractual and deadline-driven.

Default override condition is existential necessity requiring temporary priority inversion. Orchestration must log the override and define an exit condition so commerce cannot permanently colonize other organs.

---

### ORGAN_IV — orchestration_governance_flow_control

Purpose is governance, flow control, and system integrity. It coordinates transfers, enforces boundaries, maintains maps, manages graduation paths, and ensures archival coherence.

Inputs are status signals from every organ, audit outputs, dependency graphs, and exceptions.

Outputs are policies, manifests, routing decisions, migration plans, and enforcement mechanisms. It may create scaffolding documentation, but it does not generate the primary creative content of other organs.

Default interface authorizes it to say “not yet,” “never,” and “move this elsewhere.” It is permitted to remain invisible.

Default interface prohibits it from chasing attention, becoming expressive output, or transforming into a meta-art project.

Cadence defaults to steady, low-visibility maintenance.

Default override condition is rare and must be treated as a fault: if orchestration begins producing content, the system is drifting. Any such event must be logged and corrected.

---

### ORGAN_V — public_process_translucent_visibility

Purpose is to make process legible without demanding resolution. It releases fragments, marginalia, field notes, rehearsal traces, sketches, annotations, and partial thoughts as an intentional membrane between system and world.

Inputs are traces from ORGAN_I and ORGAN_II and, selectively, postmortems or lessons from ORGAN_III when they are portable and non-confidential.

Outputs are indexable public artifacts that signal continuity and reveal process without performing completeness.

Default interface is that marketing routes into this organ, and this organ routes outward to the public. Community receives people through this membrane, not directly from marketing.

Default interface discourages daily performance and algorithmic obedience. Silence is acceptable and sometimes required to preserve quality.

Cadence defaults to rhythmic but sparse. The quantity is governed by sustainability and clarity, not by platform demand.

Default override condition is when external commitments require additional visibility. Orchestration may approve a bounded schedule with a defined end date.

---

### ORGAN_VI — community_reciprocal_continuity

Purpose is reciprocal continuity with people who have demonstrated sustained interest. It is not discovery infrastructure and it is not built for scale.

Inputs are participants filtered through ORGAN_V, plus works and references suitable for discussion. Inputs from marketing are not permitted directly.

Outputs are conversation, shared reference, salons, reading groups, private forums, and collaborative continuity. The output unit is relationship and shared context, not growth.

Default interface permits smallness, slowness, and commitment requirements. Demand is allowed if it protects quality.

Default interface prohibits growth optimization, performative debate, and identity theater as operational modes. If such dynamics appear, orchestration intervenes to preserve function.

Cadence defaults to human and selective presence.

Default override condition is a deliberate open event intended to bring in new participants. Orchestration must approve and specify gating criteria post-event.

---

### ORGAN_VII — marketing_attention_routing

Purpose is discoverability infrastructure. It routes attention to stable targets. It does not define truth, meaning, or relationship.

Inputs are release signals, schedules, stable links, and approved excerpts. Inputs are constrained to what is already intended for public view.

Outputs are announcements, redirects, schedules, syndication, and republishing templates. Automation is preferred.

Default interface prohibits argument, confession, real-time emotional engagement, and prolonged explanation. When explanation is needed, it routes into ORGAN_V.

Cadence defaults to consistent and detached.

Default override condition is crisis communication. Orchestration approves, logs, and defines a termination point for elevated responsiveness.

---

### LIMINAL_ZONE — personal_profile_incubation

Purpose is liminal incubation: volatile drafts, experiments, half-formed tools, temporary collaborations, and ideas not yet eligible for an organ.

Inputs are anything that is unstable.

Outputs are prototypes, fragments, and tests that may be discarded without guilt.

Default interface prohibits this zone from becoming a pressure-dump. Orchestration periodically reviews and either promotes, archives, or deletes by explicit decision. Deletion is permitted here only when the user authorizes it and only after capturing any needed archival traces.

Cadence defaults to rapid change.

Default override condition is when an incubated item becomes load-bearing; orchestration must promote it into a proper organ immediately.

---

## 5. Stabilizers (non-expressive support contracts)

These are required functions. They may exist inside orchestration or as separate quiet modules. They are not aesthetic domains.

Administrative_legal_financial_backplane exists to prevent leakage and catastrophe: incorporation, accounting, IP boundaries, contracts, taxes, licenses, compliance, payments, insurance. Default interface prohibits mythologizing. It reports only to orchestration.

Archival_memory_versioning exists to ensure recoverability and traceability: decisions, artifacts, versions, and provenance over years. It is non-public by default. It prioritizes consistency over novelty.

Human_sustainability exists as load-bearing infrastructure: sleep, movement, mental health support, sobriety or reduction, rhythm, solitude, embodied repetition. It is not public process. It is not community. It is routine. Its failures should be diagnosed as infrastructure failures, not as meaning failures.

---

## 6. Graduation pathways (how things move)

Promotion is an orchestration action that occurs when an item becomes stable enough to have a name, scope, owner, and interface statement.

Default promotion destinations are determined by output type: rules to ORGAN_I, experiences to ORGAN_II, deliverables to ORGAN_III, governance artifacts to ORGAN_IV, process traces to ORGAN_V, conversation infrastructure to ORGAN_VI, routing templates to ORGAN_VII.

Deprecation and archival are states, not shame. Deprecated means frozen but referenced. Archived means read-only and historically complete. Both require replacement pointers and rationale notes.

---

## 7. Operational diagnostic

When pressure spikes and the impulse arises to add a new organ, orchestration asks one question: which boundary is currently being avoided.

The system is considered functioning when it absorbs pressure without distorting: meaning can be generated without validation, work can circulate without performance collapse, money can be earned without value capture, and people can be invited without boundary erosion.
```
```json
{
  "organ_charter_version": "v0",
  "source_of_truth": {
    "world_root_env": "WORLD_ROOT",
    "registry_path": "$WORLD_ROOT/_registry/organ_charter_v0.md"
  },
  "organs": [
    {
      "organ_id": "organ_i",
      "organ_slug": "conceptual_symbolic_engine",
      "purpose": "Generate and preserve formal thinking (rules, grammars, ontologies, taxonomies, meaning-structures) as upstream dependencies.",
      "default_visibility": "private",
      "default_cadence": "pressure_driven_irregular",
      "allowed_inputs_from": ["any"],
      "allowed_outputs_to": ["organ_iv"],
      "discouraged_direct_interfaces": ["organ_vii", "organ_iii", "organ_vi"],
      "prohibitions": "No audience optimization, no commercial framing, no performative onboarding; no direct marketing coupling.",
      "graduation_rule": "Material graduates only when stable enough to function as a dependency; orchestration executes transfer.",
      "override_rule": "Allowed only for time-critical operational coherence; must be logged via orchestration override record."
    },
    {
      "organ_id": "organ_ii",
      "organ_slug": "art_enactment_experiential_systems",
      "purpose": "Translate symbolic structures into experiences and occurrences; finishedness optional, presence mandatory.",
      "default_visibility": "mixed",
      "default_cadence": "project_based_with_silence_ok",
      "allowed_inputs_from": ["organ_i", "organ_v", "organ_iii", "liminal_zone"],
      "allowed_outputs_to": ["organ_v", "organ_vi", "organ_iv"],
      "discouraged_direct_interfaces": ["organ_vii"],
      "prohibitions": "No obligation to justify economically; avoid exhaustive self-explanation as a default behavior.",
      "graduation_rule": "Works may publish via public process; durable assets promoted under orchestration when stable.",
      "override_rule": "Direct marketing allowed only if required for survival of the work and approved/logged by orchestration."
    },
    {
      "organ_id": "organ_iii",
      "organ_slug": "commerce_applied_labor_survival_surface",
      "purpose": "Perform income-bearing work under constraint; produce clear, stable deliverables.",
      "default_visibility": "private",
      "default_cadence": "deadline_driven",
      "allowed_inputs_from": ["organ_iv", "liminal_zone"],
      "allowed_outputs_to": ["clients", "organ_iv"],
      "discouraged_direct_interfaces": ["organ_i", "organ_ii", "organ_vi"],
      "prohibitions": "Does not define system meaning, values, or direction; avoids touching raw theory or unfinished art directly.",
      "graduation_rule": "Reusable non-sensitive components may be promoted by orchestration to appropriate organ.",
      "override_rule": "Priority inversion only for existential necessity with explicit exit condition; must be logged."
    },
    {
      "organ_id": "organ_iv",
      "organ_slug": "orchestration_governance_flow_control",
      "purpose": "Governance, flow control, boundary enforcement, documentation, graduation paths, archival coherence.",
      "default_visibility": "internal",
      "default_cadence": "steady_quiet",
      "allowed_inputs_from": ["any"],
      "allowed_outputs_to": ["any"],
      "discouraged_direct_interfaces": [],
      "prohibitions": "Does not chase attention, does not become expressive output, does not become meta-art.",
      "graduation_rule": "Approves transfers, assigns destinations, maintains manifests and exceptions.",
      "override_rule": "If it begins producing content, treat as drift; log and correct."
    },
    {
      "organ_id": "organ_v",
      "organ_slug": "public_process_translucent_visibility",
      "purpose": "Make process legible without demanding resolution; membrane between system and world.",
      "default_visibility": "public",
      "default_cadence": "rhythmic_sparse",
      "allowed_inputs_from": ["organ_i", "organ_ii", "organ_iii", "liminal_zone"],
      "allowed_outputs_to": ["public", "organ_vi"],
      "discouraged_direct_interfaces": [],
      "prohibitions": "No daily performance mandate; no algorithmic obedience; silence is acceptable.",
      "graduation_rule": "Routes stable works outward; routes sustained-interest participants inward to community.",
      "override_rule": "Bounded schedule increases allowed for external commitments; must be approved/logged with end date."
    },
    {
      "organ_id": "organ_vi",
      "organ_slug": "community_reciprocal_continuity",
      "purpose": "Reciprocal continuity with sustained-interest participants; not discovery and not scale.",
      "default_visibility": "private",
      "default_cadence": "human_selective",
      "allowed_inputs_from": ["organ_v", "organ_ii", "organ_iv"],
      "allowed_outputs_to": ["organ_v", "organ_iv"],
      "discouraged_direct_interfaces": ["organ_vii"],
      "prohibitions": "No growth optimization; no performative debate; no identity theater as operational mode.",
      "graduation_rule": "May collaborate and cohere context; recruitment occurs only through public process gating.",
      "override_rule": "Open events only by orchestration approval with explicit post-event gating criteria."
    },
    {
      "organ_id": "organ_vii",
      "organ_slug": "marketing_attention_routing",
      "purpose": "Discoverability infrastructure; routing attention to stable targets; automation preferred.",
      "default_visibility": "public",
      "default_cadence": "consistent_detached",
      "allowed_inputs_from": ["organ_iv", "organ_v"],
      "allowed_outputs_to": ["public", "organ_v"],
      "discouraged_direct_interfaces": ["organ_vi", "organ_i", "organ_ii"],
      "prohibitions": "No argument, confession, real-time emotional engagement, or prolonged explanation; route explanation into public process.",
      "graduation_rule": "Publishes schedules/templates and redirects to public process assets.",
      "override_rule": "Crisis communication permitted only with orchestration approval, logging, and termination point."
    },
    {
      "organ_id": "liminal_zone",
      "organ_slug": "personal_profile_incubation",
      "purpose": "Volatile incubation for drafts and experiments not yet eligible for an organ.",
      "default_visibility": "mixed",
      "default_cadence": "rapid_change",
      "allowed_inputs_from": ["any"],
      "allowed_outputs_to": ["organ_iv"],
      "discouraged_direct_interfaces": [],
      "prohibitions": "Must not become a pressure-dump; periodic review required.",
      "graduation_rule": "Promote, archive, or delete by explicit orchestration decision; deletion only with user authorization and archival trace if needed.",
      "override_rule": "If an item becomes load-bearing, promote immediately and log."
    }
  ],
  "stabilizers": [
    {
      "stabilizer_id": "admin_legal_financial_backplane",
      "purpose": "Prevent leakage and catastrophe: contracts, accounting, IP boundaries, taxes, compliance, payments, insurance.",
      "default_visibility": "private",
      "governance_owner": "organ_iv",
      "prohibitions": "No aestheticization or mythologizing; remain boring."
    },
    {
      "stabilizer_id": "archival_memory_versioning",
      "purpose": "Recoverability and provenance of ideas, artifacts, decisions, and versions over years.",
      "default_visibility": "private",
      "governance_owner": "organ_iv",
      "prohibitions": "No public performance; consistency over novelty."
    },
    {
      "stabilizer_id": "human_sustainability",
      "purpose": "Load-bearing human infrastructure: sleep, movement, mental health support, rhythm, solitude, embodied repetition.",
      "default_visibility": "off_system",
      "governance_owner": "user",
      "prohibitions": "Not public process; not branded; not debated; treated as routine."
    }
  ],
  "override_logging": {
    "required": true,
    "log_path": "$WORLD_ROOT/_registry/override_log.ndjson",
    "minimum_fields": [
      "timestamp",
      "requesting_organ_id",
      "approving_organ_id",
      "affected_units",
      "default_overridden",
      "reason",
      "risk",
      "rollback"
    ]
  }
}
```

## Q: 
What else is missing from this procedure/protocol sequence i am about to embark upon?

## A: 
## Missing pieces in the protocol sequence

You have: ontology law, organ charter, tool-specific audit prompts, and a plan-first migration flow. What’s missing are the “boring but fatal if absent” layers that make the sequence **repeatable**, **verifiable**, and **recoverable** under stress.

### 1) A single canonical manifest handshake between local and remote

Right now you have two parallel ideas: local topology and remote mirroring. You need one file that is the _join table_ between them, so every agent run converges on the same truth.

You already have `topology_manifest.json` and `organ_manifest.json` as concepts. What’s missing is a third manifest that explicitly binds:

Local canonical path ↔ remote canonical URL ↔ lifecycle state ↔ visibility state.

Call it:

`$WORLD_ROOT/_registry/canonical_manifest.json`

It prevents drift like: “same repo cloned twice,” “remote renamed,” “local moved,” “org reorganized.”

Minimum fields per repo record (normative prose): canonical_path, origin_url, org_unit_id, repo_unit_id, realm_id, organ_id, lifecycle, visibility, checksum of last-known git HEAD and last audit timestamp.

### 2) A lifecycle state machine that’s enforceable

You referenced lifecycle (`incubating, active, stable, deprecated, archived`) but you haven’t defined:

What transitions are allowed, who approves them, and what artifacts must exist for promotion.

Without that, “promotion” becomes vibes again.

You need:

`$WORLD_ROOT/_registry/lifecycle_law_v1.md`

It defines defaults like: “stable requires README interfaces + CODEOWNERS + minimal CI or explicit waiver,” “deprecated requires replacement pointer,” etc.

### 3) A conflict-resolution protocol for collisions and duplicates

You have collision rules in the ontology law, but you don’t yet have the “what happens when” playbook for the messy cases you will definitely hit:

Repo cloned in multiple places with different unpushed commits.

Two different local repos pointing at the same origin.

One local repo with multiple remotes that disagree about canonical identity.

A repo with no remote but clearly belongs to an org.

You need an explicit exception taxonomy and resolution ladder:

`$WORLD_ROOT/_registry/exception_taxonomy_v1.md`

and an executable companion:

`$WORLD_ROOT/_registry/exception_resolution_playbook.md`

### 4) A rollback mechanism that is real, not aspirational

“Rollback.md” is good, but during execution you need actual “undo primitives.”

Missing:

A “move ledger” produced during execution that records every filesystem operation in a machine-parseable format.

Example:

`$AUDIT_ROOT/run_<ts>/move_ledger.ndjson`

Each line: op_id, timestamp, src, dst, method (mv/rsync+swap), repo_detected, git_head_before, git_head_after.

Rollback becomes: replay ledger in reverse.

### 5) A preflight safety contract for VCS hygiene

Migration will break you if you don’t force a preflight standard.

Missing:

A strict preflight that classifies repos into:

Clean, dirty-but-safe, dirty-risky.

And a policy: what happens to dirty repos (stash? commit? quarantine? block?).

You need:

`$WORLD_ROOT/_registry/preflight_policy_v1.md`

That policy includes: uncommitted changes handling, untracked files handling, LFS handling, submodules/worktrees handling.

### 6) A “scope fence” for the `$HOME` audit

You set `$UNMANAGED_DIRS`, but you also need a positive inclusion strategy or you’ll still inventory too much and lose signal.

Missing:

A governed roots list, so “starting at $HOME” doesn’t mean “recursively index my entire life.”

Add:

`$WORLD_ROOT/_registry/scope_fence.json`

It declares:

Include roots (default: `$HOME/world`, `$HOME/dev`, `$HOME/projects`, etc. whatever exists).

Exclude roots (defaults you already have).

And a max depth per root for inventory.

This makes audits fast and consistent.

### 7) A repository template baseline (so new repos don’t reintroduce entropy)

You wrote “Start Here” repos and standard files. Missing is the actual enforcement mechanism: a template + a conformance check.

Add:

`$WORLD_ROOT/_registry/repo_template/` (a directory)

and a check script:

`$WORLD_ROOT/_registry/check_repo_conformance.sh`

The audit tool can then flag “nonconforming repos” and optionally generate PRs later.

### 8) A minimal “routing index” for humans

Your manifests will be correct, but humans will still get lost without one index that answers:

Where do I start? What is active? What is safe to touch? What are the interfaces?

Missing:

`$WORLD_ROOT/_registry/index.md`

Generated from manifests, it provides a compact map: realms → organs → org_units → repos with status and links.

### 9) A policy for secrets, credentials, and redaction

As soon as you start automating audits and generating public process outputs, you risk leaking secrets in logs and manifests.

Missing:

`$WORLD_ROOT/_registry/secrets_policy_v1.md`

This defines:

What files are never copied into public areas, what patterns are redacted in generated artifacts, and what gets excluded from audit outputs.

### 10) A “cadence” protocol for repeating the audit

This entire sequence becomes valuable only if it can be rerun without pain.

Missing:

A schedule trigger rule: when do you rerun Phase 1/2, and what constitutes drift?

You don’t need automation yet. You need a written trigger policy:

`$WORLD_ROOT/_registry/audit_cadence_v1.md`

Examples of triggers:

After creating a new repo.

After promoting from liminal zone.

After renaming a remote org/repo.

Monthly/quarterly sanity check.

### 11) An interface contract between “organ semantics” and “filesystem realms”

Right now organs and realms are related but not formalized. You need a declared mapping:

Realm is _location taxonomy_. Organ is _function taxonomy_.

Missing:

`$WORLD_ROOT/_registry/realm_organ_matrix.json`

It declares defaults like:

realm=create tends to contain organ_i and organ_ii.

realm=operate tends to contain organ_iv and organ_iii.

realm=publish tends to contain organ_v and organ_vii.

This helps agents assign realm with higher confidence.

### 12) A definition of “unit of movement” during migration

If you do a migration, what moves?

Repo roots move, yes. But what about:

workspace folders, non-git projects, vaults, large media directories, datasets?

Missing:

A unit taxonomy:

`$WORLD_ROOT/_registry/unit_taxonomy_v1.md`

It defines: REPO_UNIT vs PROJECT_DIR vs VAULT vs DATASET vs ARTIFACT_BUCKET, and how each migrates.

Without this, the agent will either ignore non-git work or mishandle it.

* * *

## If you add only three things before you start

If you want the highest leverage with minimal extra work, add these first:

`canonical_manifest.json` (the join table between local and remote)

`scope_fence.json` (so “start at $HOME” doesn’t become a swamp)

`move_ledger.ndjson` (so rollback is real)

Those three turn your procedure from “ambitious” into “safe and repeatable.”

* * *

## One more missing meta-piece: an explicit “stop condition”

Your agents need a written condition for when to stop expanding the audit and move on, otherwise they will spiral.

Add to the charter: the audit stops when repo discovery stabilizes (no new repos found after scanning governed roots), and everything else becomes “unmanaged by default until declared.”

That single rule prevents infinite ingestion.

If you want, I can draft the missing three files (`canonical_manifest.json` schema, `scope_fence.json` template, and `preflight_policy_v1.md`) in the same “binding-but-not-brittle” style as your ontology and organ charters.

## Q: 
Draft all 12 fully

## A: 
## 1) `$WORLD_ROOT/_registry/canonical_manifest.json`

```json
{
  "manifest_id": "canonical_manifest_v1",
  "ontology_version": "v1",
  "organ_charter_version": "v0",
  "generated_at": "1970-01-01T00:00:00Z",
  "generated_by": {
    "agent": "terminal_auditor",
    "run_dir": "$AUDIT_ROOT/run_<timestamp>"
  },
  "world_root": "$WORLD_ROOT",
  "vcs_host": "$VCS_HOST",
  "defaults": {
    "default_org_unit_id": "$DEFAULT_ORG_UNIT",
    "default_realm_id": "operate",
    "default_organ_id": "organ_iv",
    "default_visibility": "private",
    "default_lifecycle": "incubating"
  },
  "repos": [
    {
      "repo_uid": "org_unit_id:repo_unit_id",
      "realm_id": "operate",
      "organ_id": "organ_iv",
      "org_unit_id": "example_org",
      "repo_unit_id": "example_repo",
      "canonical_path": "$WORLD_ROOT/realm/operate/org/example_org/repo/example_repo",
      "origin_url": "https://github.com/example_org/example_repo.git",
      "remotes": [
        {
          "name": "origin",
          "url": "https://github.com/example_org/example_repo.git",
          "is_canonical": true
        }
      ],
      "visibility": "private",
      "lifecycle": "active",
      "interface_profile_id": "default",
      "head_snapshot": {
        "head_oid": "0000000000000000000000000000000000000000",
        "head_ref": "refs/heads/main",
        "head_commit_time": "1970-01-01T00:00:00Z",
        "working_tree_state": "clean"
      },
      "audit": {
        "last_audited_at": "1970-01-01T00:00:00Z",
        "run_dir": "$AUDIT_ROOT/run_<timestamp>",
        "inventory_hash": "sha256:<hash>",
        "git_repos_hash": "sha256:<hash>"
      },
      "notes": "",
      "exceptions": []
    }
  ],
  "non_repo_units": [],
  "workspaces": [],
  "exceptions": [],
  "signatures": {
    "canonical_manifest_sha256": "sha256:<hash-of-this-file>"
  }
}
```

* * *

## 2) `$WORLD_ROOT/_registry/lifecycle_law_v1.md`

```md
# lifecycle_law_v1.md

## 0. Status

This document defines lifecycle states and allowed transitions for REPO_UNIT and WORKSPACE_UNIT. It is normative. It is enforced by orchestration.

Lifecycle is not mood. Lifecycle is risk classification and interface stability.

## 1. Lifecycle states

A unit is incubating when its name, scope, and interfaces are not yet stable. Incubating units may change rapidly. They must not be depended on as upstream contracts without an override.

A unit is active when it is in use and evolving with intentional direction. Active units may break internal APIs but should not break declared external interfaces without a logged change.

A unit is stable when its identity, interfaces, and operational assumptions are hardened. Stable units may evolve, but changes are controlled, review-gated, and documented.

A unit is deprecated when it should no longer be used for new work but remains referenced for compatibility or historical continuity. Deprecation requires a replacement pointer or a “no replacement exists” rationale.

A unit is archived when it is read-only and historically complete. Archival requires both a final rationale and a pointer to the successor or to the context in which it ended.

## 2. Transition authority

Only orchestration approves lifecycle transitions. Production organs may request transitions.

Transitions are recorded in `$WORLD_ROOT/_registry/override_log.ndjson` as lifecycle events even when they are not overrides.

## 3. Required artifacts per state

Incubating requires a minimal README that states the unit’s purpose in one paragraph and names its owner.

Active requires a README that declares interfaces in plain language and identifies inbound and outbound dependencies. Active units in commerce or tooling require a minimal test or an explicit waiver.

Stable requires a declared interface section, a changelog or release notes practice, ownership metadata, and branch protection intent. Stable units must declare what constitutes a breaking change.

Deprecated requires a README banner stating deprecation, the replacement pointer or rationale, and the last known stable reference.

Archived requires repository archival mode, a final note explaining why it ended, and successor pointer or rationale.

## 4. Allowed transitions

The default progression is incubating to active to stable. Deprecation may occur from active or stable. Archival may occur from deprecated or stable.

Reactivation is permitted but treated as an exception. A deprecated or archived unit may be reactivated only when a documented reason exists and a risk assessment is recorded.

A stable unit may be downgraded to active only when stability assumptions were false. This is a governance failure event and must be logged.

## 5. Breaking change protocol

Any change that alters a declared interface, naming contract, cross-repo schema, or promotion rule is a breaking change. Breaking changes require orchestration approval, a changelog entry, and a defined migration path.

Theory artifacts that are normative rules behave as interfaces. They follow the same breaking-change protocol when referenced by other organs as dependencies.

## 6. Visibility coupling

Lifecycle and visibility are coupled by default. Incubating units default to private. Stable units may be public when risk permits. Commerce deliverables remain private unless explicitly sanitized and approved for release.

Any deviation from default visibility expectations must be logged as an override when it changes exposure risk.

## 7. Enforcement trigger

If an agent run detects that a downstream unit depends on an incubating upstream unit without an override record, orchestration must either promote the upstream, remove the dependency, or record an override with an expiry condition.
```

* * *

## 3) `$WORLD_ROOT/_registry/exception_taxonomy_v1.md`

```md
# exception_taxonomy_v1.md

## 0. Status

This document defines the exception categories that block or constrain execution. It is normative. It exists to keep exceptions legible and resolvable.

## 1. Severity model

An exception is blocking when executing migration or enforcing topology could cause data loss, history loss, secret leakage, or irrecoverable confusion.

An exception is cautionary when it does not threaten integrity but reduces confidence in mapping or classification.

An exception is informational when it is non-ideal but safe.

## 2. Exception classes

EXC_REPO_NESTING_UNDECLARED exists when a git repository root contains another git repository that is not a submodule and not a declared workspace member. This is blocking by default.

EXC_DUPLICATE_CHECKOUT exists when multiple local repositories resolve to the same canonical remote identity. This is cautionary by default and becomes blocking when divergent commits or unpushed changes exist.

EXC_ORPHAN_NO_REMOTE exists when a repository has no remotes. This is cautionary unless the repo is classified as canonical local-only, in which case it is informational.

EXC_REMOTE_HOST_MISMATCH exists when remotes point to hosts outside `$VCS_HOST` and no canonical remote on `$VCS_HOST` exists. This is cautionary and may be blocking when the remote identity is ambiguous.

EXC_REMOTE_IDENTITY_CONFLICT exists when multiple remotes disagree about canonical org/repo identity, or when parsed org/repo differs from expected mapping. This is blocking when identity cannot be determined.

EXC_DIRTY_WORKTREE exists when uncommitted changes exist. This is cautionary and becomes blocking for execution when policy forbids moving dirty repos.

EXC_UNTRACKED_LARGE_ASSETS exists when large untracked files exist and could be lost or duplicated. This is blocking when assets are at risk.

EXC_SUBMODULE_INCONSISTENT exists when submodules are present but not initialized or the recorded commit does not resolve. This is cautionary and becomes blocking for execution.

EXC_WORKTREE_COMPLEXITY exists when git worktrees are used. This is cautionary and becomes blocking when canonical path mapping would break worktree layout.

EXC_NAME_COLLISION exists when multiple units resolve to the same target ids. This is cautionary and becomes blocking when deterministic suffixing would hide materially different identities.

EXC_SECRET_EXPOSURE_RISK exists when secrets appear in tracked files, logs, or generated manifests. This is blocking until redaction rules are applied and outputs are regenerated.

EXC_SCOPE_FENCE_VIOLATION exists when the audit finds governed material outside declared roots or finds unmanaged roots being scanned. This is informational but must be corrected for repeatability.

EXC_REALM_OR_ORGAN_AMBIGUITY exists when classification confidence is low. This is cautionary and not blocking unless it affects execution routing.

## 3. Required fields for each exception record

Each exception record must include: exception_id, class_id, severity, repo_or_unit_ref, evidence, proposed_resolution, and whether it blocks Phase 4.

## 4. Blocking policy

Phase 4 execution is prohibited while any blocking exception exists, unless orchestration records an override that includes explicit risk acceptance and rollback plan.
```

* * *

## 4) `$WORLD_ROOT/_registry/exception_resolution_playbook.md`

```md
# exception_resolution_playbook.md

## 0. Status

This playbook defines deterministic resolution steps. It is operational. It assumes the taxonomy in exception_taxonomy_v1.md.

## 1. General resolution ladder

Resolution always proceeds in this order: identify, preserve, disambiguate, then enforce.

Identify means gathering minimal evidence: paths, remotes, HEAD commits, dirty state, and size risks.

Preserve means ensuring nothing is deleted or overwritten, and capturing snapshots when needed.

Disambiguate means selecting a canonical identity or declaring orphan/local-only status.

Enforce means applying the topology move only after plan approval.

## 2. Class-specific protocols

For EXC_REPO_NESTING_UNDECLARED, the resolution is to determine whether the inner repo is a submodule, a worktree, or a mistaken clone. If it is a submodule, it must be registered as such. If it is a workspace member, the workspace must be declared and the nesting must be structural only. If it is accidental, one repo must be relocated so no repo root contains another.

For EXC_DUPLICATE_CHECKOUT, the resolution is to identify which checkout is canonical. Canonical preference is the one whose origin URL matches the canonical remote in canonical_manifest.json and whose HEAD is ahead in an intended way. Divergent checkouts are either removed after archival capture, or retained as forks with explicit suffix identity.

For EXC_ORPHAN_NO_REMOTE, the resolution is to decide whether the repo is meant to remain local-only. If local-only, it must be declared as orphan and added to canonical_manifest.json with origin_url empty and a stable canonical_path. If it should be remote, orchestration decides remote creation later, outside the topology migration.

For EXC_REMOTE_HOST_MISMATCH, the resolution is to identify whether `$VCS_HOST` is required. If the repo belongs on a different host, it must be marked as such in canonical_manifest.json and excluded from “mirror local to remote” constraints. If `$VCS_HOST` is required, orchestration schedules a remote migration separately and blocks topology execution that would embed the wrong identity.

For EXC_REMOTE_IDENTITY_CONFLICT, the resolution is to select the canonical remote. Canonical selection rule is that the remote with the highest trust is origin on `$VCS_HOST`, then a remote explicitly declared canonical in canonical_manifest.json, then the remote that matches the majority of clones. If no decision can be made safely, execution is blocked.

For EXC_DIRTY_WORKTREE, resolution depends on preflight_policy_v1.md. If policy blocks moving dirty repos, then the repo must be cleaned, stashed, committed, or quarantined before execution. Quarantine means copying the repo to staging, leaving original untouched, then executing on the clean copy.

For EXC_UNTRACKED_LARGE_ASSETS, the resolution is to classify assets as artifacts, datasets, or source. Artifacts belong in artifact buckets and are referenced, not embedded. Datasets require explicit unit taxonomy and placement. Until classified, execution is blocked to prevent loss.

For EXC_SUBMODULE_INCONSISTENT, the resolution is to initialize and validate submodules or to detach them as independent repos with explicit identity. Execution is blocked if submodule commits cannot be resolved.

For EXC_WORKTREE_COMPLEXITY, resolution is to freeze worktree layout during migration. Canonical path mapping must account for worktree roots. Execution is blocked unless the move plan explicitly preserves worktree relationships and is validated in DRY_RUN.

For EXC_NAME_COLLISION, resolution is to apply deterministic suffixing only when identities are materially equivalent. When they are not equivalent, one or both ids must be disambiguated by subject qualifiers rather than numeric suffix.

For EXC_SECRET_EXPOSURE_RISK, resolution is immediate. Generated artifacts must be regenerated with redaction. Any tracked secrets require repository remediation according to secrets_policy_v1.md before further automation.

For EXC_SCOPE_FENCE_VIOLATION, resolution is to update scope_fence.json so subsequent audits are consistent. This is corrected before turning audits into cadence.

For EXC_REALM_OR_ORGAN_AMBIGUITY, resolution is to assign default realm and organ with needs_human_assignment true. Orchestration then schedules classification later. Execution should not be blocked solely for this unless it affects visibility or risk.

## 3. Resolution outputs

Every resolved exception must end in one of: resolved, accepted with override, or deferred with block. The decision and evidence are appended to `$WORLD_ROOT/_registry/exceptions.md` and, when applicable, `$WORLD_ROOT/_registry/override_log.ndjson`.
```

* * *

## 5) `$AUDIT_ROOT/run_<timestamp>/move_ledger.ndjson` (spec + example)

```plain text
{"op_id":"0001","ts":"1970-01-01T00:00:00Z","action":"mkdir","path":"$WORLD_ROOT/realm/operate/org/example_org/repo","method":"mkdir -p","result":"ok","notes":""}
{"op_id":"0002","ts":"1970-01-01T00:00:01Z","action":"move","src":"/old/path/example_repo","dst":"$WORLD_ROOT/realm/operate/org/example_org/repo/example_repo","method":"mv","repo_detected":true,"head_before":"0000000000000000000000000000000000000000","head_after":"0000000000000000000000000000000000000000","worktree_state_before":"clean","worktree_state_after":"clean","result":"ok","rollback":{"method":"mv","src":"$WORLD_ROOT/realm/operate/org/example_org/repo/example_repo","dst":"/old/path/example_repo"}}
{"op_id":"0003","ts":"1970-01-01T00:00:02Z","action":"symlink","src":"/old/path/example_repo","dst":"$WORLD_ROOT/realm/operate/org/example_org/repo/example_repo","method":"ln -s","result":"skipped","notes":"symlink_mode_disabled"}
```

This ledger is append-only. Rollback is “replay in reverse order, using rollback fields.”

* * *

## 6) `$WORLD_ROOT/_registry/preflight_policy_v1.md`

```md
# preflight_policy_v1.md

## 0. Status

This policy governs what must be true before Phase 4 execution is allowed. It exists to prevent accidental loss and irreversible confusion.

## 1. Repository cleanliness categories

A repository is clean when git reports no staged or unstaged changes and no untracked files of consequence.

A repository is dirty-safe when changes exist but are trivial and can be stashed without ambiguity, and no large untracked assets exist.

A repository is dirty-risky when untracked assets are large, when conflicts exist, when submodules are inconsistent, or when worktrees make path moves non-trivial.

## 2. Default rule

Phase 4 moves are permitted for clean repositories.

Dirty-safe repositories are permitted only if an explicit preflight action is performed according to the selected mode.

Dirty-risky repositories block execution by default.

## 3. Preflight action modes

Mode stash means the agent creates a stash with a deterministic message that includes timestamp and run id, verifies stash exists, and proceeds. The stash must be referenced in the run artifacts so it can be restored.

Mode commit means the agent commits changes on a temporary branch with a deterministic name, then proceeds. The branch name must include the run id.

Mode quarantine-copy means the agent copies the repo to `$WORLD_ROOT/_staging/` preserving metadata, then operates on the copy while leaving original untouched. This is the default for dirty-risky when execution must proceed.

Mode block means the agent refuses execution until the user resolves dirtiness.

## 4. Large assets and datasets

Any untracked file larger than a threshold must be flagged. The threshold is controlled by `$PREFLIGHT_LARGE_FILE_BYTES` if set, otherwise 50MB.

Large assets must be classified as ARTIFACT_UNIT or DATASET_UNIT before execution. Until classified, the repository is dirty-risky.

## 5. Submodules and worktrees

Submodules must be initialized and their recorded commits must resolve. Otherwise the repository is dirty-risky.

Worktree repositories require a worktree-aware migration plan. If worktrees exist and the plan does not explicitly preserve them, execution is blocked.

## 6. Remote reachability

If `$PREFLIGHT_REQUIRE_REMOTE_REACHABLE` is set to true, the agent must verify canonical remotes resolve. Failure is blocking.

This policy does not authorize remote modification. It only verifies reachability.

## 7. Output requirements

Preflight produces `$AUDIT_ROOT/run_<timestamp>/preflight_report.json` recording: cleanliness category, selected action mode, stash or branch identifiers when created, and any blockers.

## 8. Override

Orchestration may override a preflight block only with explicit risk acceptance and a rollback plan, recorded in override log.
```

* * *

## 7) `$WORLD_ROOT/_registry/scope_fence.json`

```json
{
  "scope_fence_version": "v1",
  "world_root": "$WORLD_ROOT",
  "audit_root": "$AUDIT_ROOT",
  "home_root": "$HOME",
  "include_roots": [
    "$WORLD_ROOT",
    "$HOME/projects",
    "$HOME/dev",
    "$HOME/Documents"
  ],
  "exclude_roots": [
    "$HOME/Library",
    "$HOME/.cache",
    "$HOME/.config",
    "$HOME/.Trash"
  ],
  "exclude_name_globs": [
    "node_modules",
    ".venv",
    ".git",
    "dist",
    "build",
    ".next",
    ".DS_Store"
  ],
  "max_depth_by_root": [
    {
      "root": "$HOME/Documents",
      "max_depth": 6
    },
    {
      "root": "$HOME/projects",
      "max_depth": 8
    }
  ],
  "classification_defaults": {
    "unclassified_realm_id": "operate",
    "unclassified_organ_id": "organ_iv",
    "mark_needs_human_assignment": true
  }
}
```

* * *

## 8) `$WORLD_ROOT/_registry/repo_template/` and `$WORLD_ROOT/_registry/check_repo_conformance.sh`

Template tree for GitHub repos, intentionally minimal and organ-aware.

```plain text
$WORLD_ROOT/_registry/repo_template/
  README.md
  CODEOWNERS
  LICENSE
  SECURITY.md
  CONTRIBUTING.md
  .gitignore
  .github/
    ISSUE_TEMPLATE.md
    PULL_REQUEST_TEMPLATE.md
```

`$WORLD_ROOT/_registry/repo_template/README.md`

```md
# <repo_unit_id>

Status: <lifecycle>
Visibility: <visibility>
Owner: <owner_team_or_person>
Organ: <organ_id>
Realm: <realm_id>

## Purpose

<One paragraph: what this is and what it is not.>

## Interfaces

Inbound interfaces are the upstream units this repo depends on, including schemas and contracts. Outbound interfaces are downstream units that depend on this repo.

Inbound:
<declare>

Outbound:
<declare>

## Safety and boundaries

This repository follows `$WORLD_ROOT/_registry/ontology_law_v1.md`, `organ_charter_v0.md`, and `lifecycle_law_v1.md`. Breaking interface changes require orchestration approval.

## Promotion path

This repo is promoted, deprecated, or archived only by orchestration action, logged in registry.
```

`$WORLD_ROOT/_registry/repo_template/CODEOWNERS`

```plain text
* @owners
```

`$WORLD_ROOT/_registry/repo_template/SECURITY.md`

```md
# Security

This repository may contain sensitive data only if its organ and visibility permit it. Secrets must never be committed. If a secret is found, rotate it and purge history according to `secrets_policy_v1.md`.
```

`$WORLD_ROOT/_registry/repo_template/CONTRIBUTING.md`

```md
# Contributing

Changes must state intent, scope, risk, interfaces affected, and rollback. If a change alters naming, schemas, or cross-repo contracts, orchestration review is required.
```

`$WORLD_ROOT/_registry/repo_template/.github/ISSUE_TEMPLATE.md`

```md
Title:

Intent:
Scope:
Interfaces touched:
Risk:
Rollback:
Organ impact:
Lifecycle impact:
```

`$WORLD_ROOT/_registry/repo_template/.github/PULL_REQUEST_TEMPLATE.md`

```md
Intent:
Scope:
Interfaces:
Risk:
Rollback:

Does this change affect any declared interfaces, schemas, or naming laws? If yes, reference the orchestration decision record.
```

`$WORLD_ROOT/_registry/check_repo_conformance.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${WORLD_ROOT:?WORLD_ROOT is required}"
: "${AUDIT_ROOT:?AUDIT_ROOT is required}"

RUN_TS="${1:-run_$(date -u +%Y%m%dT%H%M%SZ)}"
RUN_DIR="${AUDIT_ROOT}/${RUN_TS}"
mkdir -p "${RUN_DIR}"

TEMPLATE_DIR="${WORLD_ROOT}/_registry/repo_template"

if [[ ! -d "${TEMPLATE_DIR}" ]]; then
  echo "missing template dir: ${TEMPLATE_DIR}" >&2
  exit 2
fi

REPORT_JSON="${RUN_DIR}/repo_conformance_report.json"
TMP_JSON="${RUN_DIR}/repo_conformance_report.tmp.json"

echo '{"generated_at":"'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'","world_root":"'"${WORLD_ROOT}"'","repos":[]}' > "${TMP_JSON}"

find "${WORLD_ROOT}/realm" -type d -name ".git" -prune -print | while read -r gitdir; do
  repo_root="$(dirname "${gitdir}")"

  missing=""
  for f in README.md CODEOWNERS LICENSE SECURITY.md CONTRIBUTING.md .gitignore; do
    if [[ ! -e "${repo_root}/${f}" ]]; then
      missing="${missing}${f},"
    fi
  done

  has_pr_template="false"
  has_issue_template="false"
  if [[ -e "${repo_root}/.github/PULL_REQUEST_TEMPLATE.md" ]]; then has_pr_template="true"; fi
  if [[ -e "${repo_root}/.github/ISSUE_TEMPLATE.md" ]]; then has_issue_template="true"; fi

  repo_rel="${repo_root#${WORLD_ROOT}/}"
  entry='{"repo_path":"'"${repo_root}"'","repo_rel":"'"${repo_rel}"'","missing":"'"${missing}"'","has_pr_template":'"${has_pr_template}"',"has_issue_template":'"${has_issue_template}"'}'

  python - <<'PY' "${TMP_JSON}" "${entry}"
import json,sys
path=sys.argv[1]
entry=json.loads(sys.argv[2])
obj=json.load(open(path))
obj["repos"].append(entry)
json.dump(obj, open(path,"w"), indent=2)
PY
done

mv "${TMP_JSON}" "${REPORT_JSON}"
echo "wrote ${REPORT_JSON}"
```

* * *

## 9) `$WORLD_ROOT/_registry/index.md` (template plus generation contract)

```md
# index.md

This index is generated. Edit the registries, not this file.

Generated at: <ISO-8601>
World root: $WORLD_ROOT

## Map

Realms and organs are the two orthogonal axes. Realms reflect location topology. Organs reflect functional routing.

## Realms

<Generated section: for each realm_id, list org_units and repos with lifecycle and visibility.>

## Organs

<Generated section: for each organ_id, list repos and workspaces.>

## Exceptions and overrides

Blocking exceptions:
<Generated from exceptions.md and override_log>

Recent overrides:
<Generated from override_log.ndjson tail>

## Start here

Canonical entrypoints are the org “start here” repositories when present, otherwise the realm index.
```

Generation contract, stored as `$WORLD_ROOT/_registry/index_generation_contract.md`:

```md
# index_generation_contract.md

The index generator reads canonical_manifest.json, topology_manifest.json when present, organ_manifest.json, and exceptions.md.

It renders two deterministic views: realm-first and organ-first. Within each view it sorts org_unit_id then repo_unit_id.

It includes lifecycle and visibility badges as plain text. It includes canonical_path and origin_url when present.

It includes a blocking exceptions section that halts Phase 4 unless overrides exist.

The generator must redact secrets according to secrets_policy_v1.md before writing index.md.
```

* * *

## 10) `$WORLD_ROOT/_registry/secrets_policy_v1.md`

```md
# secrets_policy_v1.md

## 0. Status

This policy prevents credential leakage during audits, manifests, and public process publication. It is normative.

## 1. Prohibited content

Secrets must never be committed, indexed into public manifests, or included in generated summaries. Secrets include API keys, tokens, private keys, passwords, session cookies, and any credential-bearing configuration.

## 2. Redaction rules for generated artifacts

Any generated file written under `$AUDIT_ROOT` or `$WORLD_ROOT/_registry` must redact strings matching common secret patterns. The redaction output must preserve structure while replacing secret values with `<REDACTED>`.

Redaction applies to inventory outputs, manifest outputs, and index generation outputs.

## 3. Exclusion rules for scanning

Audits must not read file contents by default. When light README sniffing is permitted, it must avoid printing or storing full file contents beyond minimal headers and must still apply redaction.

Any directory named `.env`, any file matching `*.pem`, `*.key`, `id_rsa*`, `*.p12`, and any file named `secrets.*` is excluded from content inspection. Presence may be recorded as a risk marker without reading.

## 4. Remote URL sanitation

Remote URLs may contain embedded credentials. Any remote URL containing `@` in the authority section must be sanitized in outputs. The sanitized form must retain host and path while removing credentials.

## 5. Response protocol when secrets are detected

When suspected secrets are detected in tracked history, orchestration records EXC_SECRET_EXPOSURE_RISK as blocking. The system halts any publication or sharing outputs until remediation is complete.

Remediation includes rotation, removal from working tree, and history rewriting if required. This policy does not prescribe the exact tool; it prescribes that remediation is mandatory and logged.

## 6. Public process coupling

Anything routed toward public process must be treated as hostile environment. Orchestration must verify that artifacts have been redacted and do not contain confidential client identifiers.

## 7. Logging

All secret exposure events must be logged in override_log.ndjson with a remediation record, even when handled immediately.
```

* * *

## 11) `$WORLD_ROOT/_registry/audit_cadence_v1.md`

```md
# audit_cadence_v1.md

## 0. Status

This document defines when audits must occur and what constitutes drift. It is normative for orchestration.

## 1. Audit types

A lightweight audit is Phase 1 only. It inventories repositories and identity, then stops.

A structural audit is Phase 1 through Phase 3. It updates proposals and produces a migration plan draft.

A conformance audit runs repo conformance checks and verifies registry coherence.

## 2. Triggers

A lightweight audit is triggered after any of: creating a new repo, adding a new remote, changing an org namespace, or moving repos manually.

A structural audit is triggered after any of: promoting an incubated unit into an organ, performing a migration, or resolving blocking exceptions.

A conformance audit is triggered before any public release that depends on stable interfaces, and before any Phase 4 execution.

## 3. Drift definition

Drift exists when canonical_manifest.json conflicts with observed state. Conflicts include: canonical_path mismatch, origin_url mismatch, multiple local checkouts for the same repo_uid without registry declaration, or lifecycle state that does not match required artifacts.

Drift severity is blocking when it affects identity or integrity. It is cautionary when it affects classification only.

## 4. Drift response

Blocking drift requires orchestration action: update manifests, plan migration, or accept override with expiry.

Cautionary drift allows continued operation but must be scheduled for resolution.

## 5. Minimal cadence

Even without triggers, a lightweight audit is performed at least quarterly. Structural audits are performed at least annually, or whenever the topology becomes confusing.

## 6. Output retention

Audit runs are immutable. The system retains run directories under `$AUDIT_ROOT`. Retention may be pruned only by explicit user decision after ensuring summary and canonical manifests are preserved.
```

* * *

## 12) `$WORLD_ROOT/_registry/realm_organ_matrix.json` and `$WORLD_ROOT/_registry/unit_taxonomy_v1.md`

Two deliverables are required here because your system uses two orthogonal axes and multiple unit kinds.

`$WORLD_ROOT/_registry/realm_organ_matrix.json`

```json
{
  "matrix_version": "v1",
  "note": "Realms are location taxonomy; organs are functional routing taxonomy. This matrix provides default affinities only.",
  "realms": [
    {
      "realm_id": "create",
      "default_organs": ["organ_i", "organ_ii"],
      "discouraged_organs": ["organ_iii", "organ_vii"]
    },
    {
      "realm_id": "research",
      "default_organs": ["organ_i"],
      "discouraged_organs": ["organ_vii"]
    },
    {
      "realm_id": "operate",
      "default_organs": ["organ_iv", "organ_iii"],
      "discouraged_organs": ["organ_ii"]
    },
    {
      "realm_id": "publish",
      "default_organs": ["organ_v", "organ_vii"],
      "discouraged_organs": ["organ_i"]
    },
    {
      "realm_id": "archive",
      "default_organs": ["organ_iv"],
      "discouraged_organs": []
    }
  ]
}
```

`$WORLD_ROOT/_registry/unit_taxonomy_v1.md`

```md
# unit_taxonomy_v1.md

## 0. Status

This document defines the unit types governed by the system and how each migrates. It is normative.

## 1. Unit types

A REPO_UNIT is a directory whose root is a VCS repository and whose identity is determined by canonical remote mapping or declared local-only identity.

A WORKSPACE_UNIT is a declared multi-repo bundle. It is not a random folder with repos. It has a registry record defining membership and intent.

A PROJECT_DIR is a non-git project directory that still represents coherent work. It may contain code, notes, media, or drafts. It must be either promoted into a repo or declared as a project directory unit.

A VAULT_UNIT is a knowledge base container such as a note vault. It is governed by the same topology rules but may not be a repo. It must be declared to avoid accidental relocation.

A DATASET_UNIT is a data collection that is too large or too volatile to behave like a repo. It is placed in controlled dataset paths and referenced by repos.

An ARTIFACT_UNIT is an output bucket: renders, exports, builds, releases, bounces. Artifacts default to non-versioned placement unless explicitly required.

A ROUTING_UNIT is a start-here or index repository whose purpose is navigation and interface declaration.

## 2. Migration rules by unit type

REPO_UNIT moves are git-safe moves of the working directory. The move must preserve `.git` and remote configuration and must be validated via HEAD snapshot comparison.

WORKSPACE_UNIT moves are structural moves of the container plus membership verification. Workspaces must not cause repo-inside-repo VCS nesting.

PROJECT_DIR moves are permitted only when the directory is declared and a rollback plan exists. If it becomes important, orchestration should promote it into a repo.

VAULT_UNIT moves are sensitive because links may break. Moves require a link preservation strategy, such as symlinks or a rewrite mapping, recorded in the migration plan.

DATASET_UNIT moves require explicit size-aware method and checksums. Datasets are not moved by default during repo migration unless declared.

ARTIFACT_UNIT moves are allowed but should not be coupled to repo moves. Artifacts should be recreated when possible rather than moved, unless the artifact is singular or costly.

ROUTING_UNIT moves follow repo rules. Their stability matters; they should rarely move.

## 3. Declaration requirement

Any non-repo unit must be declared in canonical_manifest.json under non_repo_units with a unit_type field, canonical_path, and a dependency statement.

Undeclared non-repo units are treated as unmanaged until declared.

## 4. Enforcement trigger

If an audit finds a non-repo unit that is load-bearing, orchestration must either declare it or promote it into a repo. Otherwise the system will drift into informal sprawl.
```

* * *

If you want these to be immediately enforceable by your terminal agents, the next mechanical step is to add two more generators: one that builds `canonical_manifest.json` and one that builds `organ_manifest.json` from observed inventory plus your explicit overrides. That turns these documents from reference into executable governance.

## Q: 
add two more generators: one that builds canonical_manifest.json and one that builds organ_manifest.json from observed inventory plus your explicit overrides

## A: 
## Generators overview

You’ll add two deterministic generators under:

`$WORLD_ROOT/_registry/tools/`

They consume the latest audit run artifacts (primarily `git_repos.json`, optionally `inventory.json`) plus a single human-editable overrides file, then write:

`$WORLD_ROOT/_registry/canonical_manifest.json`  
`$WORLD_ROOT/_registry/organ_manifest.json`

These scripts are intentionally “metadata-first.” They do not move files and do not touch remotes.

* * *

## 0) One explicit overrides file (the only thing you edit by hand)

Create:

`$WORLD_ROOT/_registry/explicit_overrides.json`

```json
{
  "overrides_version": "v1",
  "repo_overrides": [
    {
      "match": {
        "repo_path": "~/some/path/repoA"
      },
      "set": {
        "realm_id": "create",
        "organ_id": "organ_ii",
        "visibility": "private",
        "lifecycle": "active",
        "org_unit_id": "example_org",
        "repo_unit_id": "repoA",
        "canonical_path": "$WORLD_ROOT/realm/create/org/example_org/repo/repoA",
        "origin_url": "https://github.com/example_org/repoA.git",
        "ignore": false
      }
    },
    {
      "match": {
        "repo_uid": "oldorg:oldrepo"
      },
      "set": {
        "repo_unit_id": "newrepoid"
      }
    }
  ],
  "org_unit_overrides": [
    {
      "match": {
        "org_unit_id": "organvm-iii-ergon"
      },
      "set": {
        "default_organ_id": "organ_iii",
        "default_realm_id": "operate"
      }
    }
  ],
  "defaults": {
    "realm_id": "operate",
    "organ_id": "organ_iv",
    "visibility": "private",
    "lifecycle": "incubating"
  }
}
```

Conventions:

`match.repo_path` is the most reliable.  
`match.repo_uid` is useful once you have stable org/repo identity.  
`set.ignore=true` lets you exclude a repo from the manifests without deleting anything.

* * *

## 1) Generator: `gen_canonical_manifest.py`

Path:

`$WORLD_ROOT/_registry/tools/gen_canonical_manifest.py`

```python
#!/usr/bin/env python3
import argparse
import copy
import datetime as dt
import hashlib
import json
import os
import re
from typing import Any, Dict, List, Optional, Tuple

ASCII_ID_RE = re.compile(r"[^a-z0-9_-]+")

def now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def sha256_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()

def normalize_id(s: str) -> str:
    s = s.strip().lower()
    s = s.replace(" ", "-")
    s = ASCII_ID_RE.sub("-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s or "unnamed"

def env_expand(s: str) -> str:
    # Expand $WORLD_ROOT style placeholders
    return os.path.expandvars(s)

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_write_json(path: str, obj: Any) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)

def sanitize_remote_url(url: str) -> str:
    # Remove embedded credentials in https://user:pass@host/...
    # Keep host + path.
    # Also normalize common git suffix.
    url = url.strip()
    if "://" in url:
        scheme, rest = url.split("://", 1)
        # authority[/path]
        if "@" in rest.split("/", 1)[0]:
            authority, *tail = rest.split("/", 1)
            authority = authority.split("@", 1)[1]
            rest = authority + ("/" + tail[0] if tail else "")
        return f"{scheme}://{rest}"
    return url

def parse_githubish_remote(url: str) -> Optional[Tuple[str, str, str]]:
    """
    Returns (host, org, repo) if parseable.
    Supports:
      https://github.com/org/repo.git
      [email redacted]:org/repo.git
      ssh://[email redacted]/org/repo.git
    """
    u = sanitize_remote_url(url)

    m = re.match(r"^https?://([^/]+)/([^/]+)/([^/]+?)(?:\.git)?$", u)
    if m:
        host, org, repo = m.group(1), m.group(2), m.group(3)
        return host.lower(), org, repo

    m = re.match(r"^git@([^:]+):([^/]+)/([^/]+?)(?:\.git)?$", u)
    if m:
        host, org, repo = m.group(1), m.group(2), m.group(3)
        return host.lower(), org, repo

    m = re.match(r"^ssh://git@([^/]+)/([^/]+)/([^/]+?)(?:\.git)?$", u)
    if m:
        host, org, repo = m.group(1), m.group(2), m.group(3)
        return host.lower(), org, repo

    return None

def coerce_repo_list(git_repos_obj: Any) -> List[Dict[str, Any]]:
    # Accept either {"repos":[...]} or [...].
    if isinstance(git_repos_obj, dict) and isinstance(git_repos_obj.get("repos"), list):
        return git_repos_obj["repos"]
    if isinstance(git_repos_obj, list):
        return git_repos_obj
    raise ValueError("git_repos.json must be a list or an object with key 'repos'.")

def load_overrides(path: Optional[str]) -> Dict[str, Any]:
    if not path:
        return {"repo_overrides": [], "org_unit_overrides": [], "defaults": {}}
    o = load_json(path)
    o.setdefault("repo_overrides", [])
    o.setdefault("org_unit_overrides", [])
    o.setdefault("defaults", {})
    return o

def match_override(repo: Dict[str, Any], overrides: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    repo_path = repo.get("repo_path") or repo.get("path") or ""
    # Attempt derive uid from remotes if present
    repo_uid = repo.get("repo_uid")
    if not repo_uid:
        # best-effort from any remote that parses
        for r in (repo.get("remotes") or []):
            url = r.get("url") or ""
            parsed = parse_githubish_remote(url)
            if parsed:
                host, org, name = parsed
                repo_uid = f"{normalize_id(org)}:{normalize_id(name)}"
                break

    for rule in overrides.get("repo_overrides", []):
        m = rule.get("match", {})
        ok = False
        if "repo_path" in m and repo_path and os.path.normpath(repo_path) == os.path.normpath(m["repo_path"]):
            ok = True
        if (not ok) and "repo_uid" in m and repo_uid and repo_uid == m["repo_uid"]:
            ok = True
        if ok:
            return rule.get("set", {})
    return None

def org_unit_default_override(org_unit_id: str, overrides: Dict[str, Any]) -> Dict[str, Any]:
    for rule in overrides.get("org_unit_overrides", []):
        m = rule.get("match", {})
        if m.get("org_unit_id") == org_unit_id:
            return rule.get("set", {})
    return {}

def choose_canonical_remote(remotes: List[Dict[str, Any]], vcs_host: str) -> Optional[Dict[str, Any]]:
    if not remotes:
        return None
    # Prefer origin on vcs_host
    for r in remotes:
        if (r.get("name") == "origin"):
            parsed = parse_githubish_remote(r.get("url", ""))
            if parsed and parsed[0] == vcs_host:
                return r
    # Any remote on vcs_host
    for r in remotes:
        parsed = parse_githubish_remote(r.get("url", ""))
        if parsed and parsed[0] == vcs_host:
            return r
    # Fallback: origin then first
    for r in remotes:
        if r.get("name") == "origin":
            return r
    return remotes[0]

def build_manifest(
    git_repos: List[Dict[str, Any]],
    overrides: Dict[str, Any],
    world_root: str,
    audit_root: str,
    vcs_host: str,
    run_dir: str,
) -> Dict[str, Any]:
    defaults = {
        "default_org_unit_id": os.environ.get("DEFAULT_ORG_UNIT", "personal"),
        "default_realm_id": overrides.get("defaults", {}).get("realm_id") or "operate",
        "default_organ_id": overrides.get("defaults", {}).get("organ_id") or "organ_iv",
        "default_visibility": overrides.get("defaults", {}).get("visibility") or "private",
        "default_lifecycle": overrides.get("defaults", {}).get("lifecycle") or "incubating",
    }

    repos_out = []
    exceptions = []

    for repo in git_repos:
        repo_path = repo.get("repo_path") or repo.get("path")
        if not repo_path:
            continue

        remotes = repo.get("remotes") or []
        canon_remote = choose_canonical_remote(remotes, vcs_host)

        org_unit_id = defaults["default_org_unit_id"]
        repo_unit_id = normalize_id(os.path.basename(repo_path))
        origin_url = ""

        if canon_remote:
            origin_url = sanitize_remote_url(canon_remote.get("url", ""))
            parsed = parse_githubish_remote(origin_url)
            if parsed:
                host, org, name = parsed
                org_unit_id = normalize_id(org)
                repo_unit_id = normalize_id(name)

        # Apply per-repo override early (may override identity)
        oset = match_override(repo, overrides) or {}
        if oset.get("ignore") is True:
            continue

        if "org_unit_id" in oset:
            org_unit_id = normalize_id(str(oset["org_unit_id"]))
        if "repo_unit_id" in oset:
            repo_unit_id = normalize_id(str(oset["repo_unit_id"]))
        if "origin_url" in oset:
            origin_url = sanitize_remote_url(env_expand(str(oset["origin_url"])))

        # Per-org defaults
        org_def = org_unit_default_override(org_unit_id, overrides)
        realm_id = normalize_id(oset.get("realm_id") or org_def.get("default_realm_id") or defaults["default_realm_id"])
        organ_id = normalize_id(oset.get("organ_id") or org_def.get("default_organ_id") or defaults["default_organ_id"])
        visibility = normalize_id(oset.get("visibility") or defaults["default_visibility"])
        lifecycle = normalize_id(oset.get("lifecycle") or defaults["default_lifecycle"])

        canonical_path = os.path.join(world_root, "realm", realm_id, "org", org_unit_id, "repo", repo_unit_id)
        if "canonical_path" in oset:
            canonical_path = env_expand(str(oset["canonical_path"]))

        repo_uid = f"{org_unit_id}:{repo_unit_id}"

        head_snapshot = {
            "head_oid": repo.get("head_oid") or repo.get("head") or "",
            "head_ref": repo.get("head_ref") or repo.get("branch") or "",
            "head_commit_time": repo.get("head_commit_time") or "",
            "working_tree_state": repo.get("working_tree_state") or repo.get("worktree_state") or "",
        }

        repos_out.append({
            "repo_uid": repo_uid,
            "realm_id": realm_id,
            "organ_id": organ_id,
            "org_unit_id": org_unit_id,
            "repo_unit_id": repo_unit_id,
            "canonical_path": canonical_path,
            "origin_url": origin_url,
            "remotes": [
                {
                    "name": r.get("name", ""),
                    "url": sanitize_remote_url(r.get("url", "")),
                    "is_canonical": bool(canon_remote and r.get("name") == canon_remote.get("name") and r.get("url") == canon_remote.get("url"))
                }
                for r in remotes
            ],
            "visibility": visibility,
            "lifecycle": lifecycle,
            "interface_profile_id": "default",
            "head_snapshot": head_snapshot,
            "audit": {
                "last_audited_at": now_iso(),
                "run_dir": run_dir,
                "inventory_hash": "",
                "git_repos_hash": ""
            },
            "notes": "",
            "exceptions": []
        })

    manifest = {
        "manifest_id": "canonical_manifest_v1",
        "ontology_version": "v1",
        "organ_charter_version": "v0",
        "generated_at": now_iso(),
        "generated_by": {"agent": "gen_canonical_manifest", "run_dir": run_dir},
        "world_root": world_root,
        "vcs_host": vcs_host,
        "defaults": defaults,
        "repos": repos_out,
        "non_repo_units": [],
        "workspaces": [],
        "exceptions": exceptions,
        "signatures": {}
    }

    # Deterministic signature: hash without signatures field populated
    tmp = copy.deepcopy(manifest)
    tmp["signatures"] = {}
    raw = json.dumps(tmp, sort_keys=True, separators=(",", ":")).encode("utf-8")
    manifest["signatures"]["canonical_manifest_sha256"] = sha256_bytes(raw)

    return manifest

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--git-repos", required=True, help="Path to git_repos.json from audit run")
    ap.add_argument("--overrides", required=False, default="", help="Path to explicit_overrides.json")
    ap.add_argument("--run-dir", required=True, help="Audit run directory path (for provenance)")
    ap.add_argument("--out", required=True, help="Output canonical_manifest.json path")
    args = ap.parse_args()

    world_root = os.environ.get("WORLD_ROOT")
    audit_root = os.environ.get("AUDIT_ROOT")
    vcs_host = os.environ.get("VCS_HOST", "github.com").lower()

    if not world_root or not audit_root:
        raise SystemExit("WORLD_ROOT and AUDIT_ROOT must be set in environment.")

    git_repos_obj = load_json(args.git_repos)
    git_repos = coerce_repo_list(git_repos_obj)
    overrides = load_overrides(args.overrides if args.overrides else None)

    manifest = build_manifest(
        git_repos=git_repos,
        overrides=overrides,
        world_root=world_root,
        audit_root=audit_root,
        vcs_host=vcs_host,
        run_dir=args.run_dir,
    )

    safe_write_json(args.out, manifest)
    print(f"wrote {args.out}")
    print(f"repos: {len(manifest['repos'])}")

if __name__ == "__main__":
    main()
```

* * *

## 2) Generator: `gen_organ_manifest.py`

Path:

`$WORLD_ROOT/_registry/tools/gen_organ_manifest.py`

This generator uses `canonical_manifest.json` as the observed “truth,” then applies explicit overrides and realm affinities to select organ assignments deterministically.

```python
#!/usr/bin/env python3
import argparse
import copy
import datetime as dt
import hashlib
import json
import os
from typing import Any, Dict, List, Optional

def now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def sha256_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_write_json(path: str, obj: Any) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)

def normalize_id(s: str) -> str:
    return "".join(ch for ch in s.strip().lower().replace(" ", "-") if ch.isalnum() or ch in "_-") or "unnamed"

def load_overrides(path: Optional[str]) -> Dict[str, Any]:
    if not path:
        return {"repo_overrides": [], "org_unit_overrides": [], "defaults": {}}
    o = load_json(path)
    o.setdefault("repo_overrides", [])
    o.setdefault("org_unit_overrides", [])
    o.setdefault("defaults", {})
    return o

def load_matrix(path: str) -> Dict[str, Any]:
    return load_json(path)

def find_repo_override(repo_record: Dict[str, Any], overrides: Dict[str, Any]) -> Dict[str, Any]:
    repo_uid = repo_record.get("repo_uid", "")
    canonical_path = repo_record.get("canonical_path", "")
    for rule in overrides.get("repo_overrides", []):
        m = rule.get("match", {})
        if m.get("repo_uid") and m["repo_uid"] == repo_uid:
            return rule.get("set", {})
        if m.get("canonical_path") and os.path.expandvars(m["canonical_path"]) == canonical_path:
            return rule.get("set", {})
    return {}

def find_org_override(org_unit_id: str, overrides: Dict[str, Any]) -> Dict[str, Any]:
    for rule in overrides.get("org_unit_overrides", []):
        m = rule.get("match", {})
        if m.get("org_unit_id") == org_unit_id:
            return rule.get("set", {})
    return {}

def matrix_default_organ(realm_id: str, matrix: Dict[str, Any]) -> Optional[str]:
    for r in matrix.get("realms", []):
        if r.get("realm_id") == realm_id:
            organs = r.get("default_organs") or []
            return organs[0] if organs else None
    return None

def build_organ_manifest(
    canonical_manifest: Dict[str, Any],
    overrides: Dict[str, Any],
    matrix: Dict[str, Any],
) -> Dict[str, Any]:
    bindings = []
    exceptions = []

    defaults = overrides.get("defaults", {})
    default_organ_id = normalize_id(defaults.get("organ_id") or "organ_iv")

    for rr in canonical_manifest.get("repos", []):
        repo_uid = rr.get("repo_uid", "")
        org_unit_id = rr.get("org_unit_id", "")
        realm_id = rr.get("realm_id", "operate")

        rset = find_repo_override(rr, overrides)
        oset = find_org_override(org_unit_id, overrides)

        organ_id = None
        source = None
        confidence = 0.0

        if rset.get("ignore") is True:
            continue

        if "organ_id" in rset:
            organ_id = normalize_id(str(rset["organ_id"]))
            source = "explicit_repo_override"
            confidence = 1.0
        elif "default_organ_id" in oset:
            organ_id = normalize_id(str(oset["default_organ_id"]))
            source = "org_unit_override"
            confidence = 0.9
        else:
            m = matrix_default_organ(realm_id, matrix)
            if m:
                organ_id = normalize_id(m)
                source = "realm_matrix_default"
                confidence = 0.7
            else:
                organ_id = default_organ_id
                source = "global_default"
                confidence = 0.5

        bindings.append({
            "repo_uid": repo_uid,
            "canonical_path": rr.get("canonical_path", ""),
            "realm_id": realm_id,
            "org_unit_id": org_unit_id,
            "repo_unit_id": rr.get("repo_unit_id", ""),
            "organ_id": organ_id,
            "source": source,
            "confidence": confidence,
            "notes": ""
        })

    out = {
        "manifest_id": "organ_manifest_v1",
        "organ_charter_version": canonical_manifest.get("organ_charter_version", "v0"),
        "generated_at": now_iso(),
        "generated_by": {"agent": "gen_organ_manifest", "source": "canonical_manifest + explicit_overrides + realm_organ_matrix"},
        "bindings": bindings,
        "exceptions": exceptions,
        "signatures": {}
    }

    tmp = copy.deepcopy(out)
    tmp["signatures"] = {}
    raw = json.dumps(tmp, sort_keys=True, separators=(",", ":")).encode("utf-8")
    out["signatures"]["organ_manifest_sha256"] = sha256_bytes(raw)
    return out

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--canonical", required=True, help="Path to canonical_manifest.json")
    ap.add_argument("--overrides", required=False, default="", help="Path to explicit_overrides.json")
    ap.add_argument("--matrix", required=True, help="Path to realm_organ_matrix.json")
    ap.add_argument("--out", required=True, help="Output organ_manifest.json path")
    args = ap.parse_args()

    canonical_manifest = load_json(args.canonical)
    overrides = load_overrides(args.overrides if args.overrides else None)
    matrix = load_matrix(args.matrix)

    organ_manifest = build_organ_manifest(canonical_manifest, overrides, matrix)
    safe_write_json(args.out, organ_manifest)
    print(f"wrote {args.out}")
    print(f"bindings: {len(organ_manifest['bindings'])}")

if __name__ == "__main__":
    main()
```

* * *

## 3) Wrapper runner: `gen_manifests.sh`

Path:

`$WORLD_ROOT/_registry/tools/gen_manifests.sh`

This is the “one command” entry point that wires everything together for a given audit run directory.

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${WORLD_ROOT:?WORLD_ROOT is required}"
: "${AUDIT_ROOT:?AUDIT_ROOT is required}"
: "${VCS_HOST:=github.com}"

RUN_DIR="${1:?usage: gen_manifests.sh $AUDIT_ROOT/run_<timestamp>}"

OVERRIDES="${WORLD_ROOT}/_registry/explicit_overrides.json"
MATRIX="${WORLD_ROOT}/_registry/realm_organ_matrix.json"

CANON_OUT="${WORLD_ROOT}/_registry/canonical_manifest.json"
ORGAN_OUT="${WORLD_ROOT}/_registry/organ_manifest.json"

PY_CANON="${WORLD_ROOT}/_registry/tools/gen_canonical_manifest.py"
PY_ORGAN="${WORLD_ROOT}/_registry/tools/gen_organ_manifest.py"

GIT_REPOS="${RUN_DIR}/git_repos.json"

if [[ ! -f "${GIT_REPOS}" ]]; then
  echo "missing ${GIT_REPOS}" >&2
  exit 2
fi

python3 "${PY_CANON}" \
  --git-repos "${GIT_REPOS}" \
  --overrides "${OVERRIDES}" \
  --run-dir "${RUN_DIR}" \
  --out "${CANON_OUT}"

python3 "${PY_ORGAN}" \
  --canonical "${CANON_OUT}" \
  --overrides "${OVERRIDES}" \
  --matrix "${MATRIX}" \
  --out "${ORGAN_OUT}"

echo "done"
```

Make executable:

```bash
chmod +x "$WORLD_ROOT/_registry/tools/gen_manifests.sh"
chmod +x "$WORLD_ROOT/_registry/tools/gen_canonical_manifest.py"
chmod +x "$WORLD_ROOT/_registry/tools/gen_organ_manifest.py"
```

Run it:

```bash
"$WORLD_ROOT/_registry/tools/gen_manifests.sh" "$AUDIT_ROOT/run_20260207T143000Z"
```

* * *

## 4) Enforcement hook (how orchestration “uses” these)

Once these two manifests exist, orchestration treats them as the join layer for everything else:

`canonical_manifest.json` decides identity, placement, lifecycle, visibility.  
`organ_manifest.json` decides routing and interface governance.

Any future agent run that proposes moves should refuse Phase 4 when:

canonical manifests disagree with observed repo identity, or  
organ bindings disagree with explicit overrides, or  
blocking exceptions exist without overrides.

If you want the next tightening step, the generators can also emit:

`$WORLD_ROOT/_registry/topology_manifest.json` (derived view: current_path → canonical_path)  
`$WORLD_ROOT/_registry/repo_index.csv` (human-scannable index)

Those are purely derived, so they’re safe to regenerate on every run.

## Q: 
$WORLD_ROOT/_registry/topology_manifest.json (derived view: current_path → canonical_path) $WORLD_ROOT/_registry/repo_index.csv (human-scannable index)

## A: 
## Add two derived generators (from canonical_manifest + latest audit run)

You want:

`$WORLD_ROOT/_registry/topology_manifest.json` as a current_path → canonical_path mapping, anchored to an audit run.  
`$WORLD_ROOT/_registry/repo_index.csv` as a human index.

These should be derived, regenerable, and non-destructive.

* * *

## 1) `$WORLD_ROOT/_registry/tools/gen_topology_manifest.py`

This reads:

*   `canonical_manifest.json` (authoritative canonical targets)
    
*   `git_repos.json` from a specific run (observed current paths)
    

It writes:

*   `$WORLD_ROOT/_registry/topology_manifest.json`
    

```python
#!/usr/bin/env python3
import argparse
import copy
import datetime as dt
import hashlib
import json
import os
from typing import Any, Dict, List

def now_iso() -> str:
    return dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def sha256_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def safe_write_json(path: str, obj: Any) -> None:
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)

def coerce_repo_list(git_repos_obj: Any) -> List[Dict[str, Any]]:
    if isinstance(git_repos_obj, dict) and isinstance(git_repos_obj.get("repos"), list):
        return git_repos_obj["repos"]
    if isinstance(git_repos_obj, list):
        return git_repos_obj
    raise ValueError("git_repos.json must be a list or an object with key 'repos'.")

def index_canonical(canonical_manifest: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    # Map by repo_uid, plus fallback map by origin_url when present.
    by_uid: Dict[str, Dict[str, Any]] = {}
    by_origin: Dict[str, Dict[str, Any]] = {}
    for r in canonical_manifest.get("repos", []):
        uid = r.get("repo_uid")
        if uid:
            by_uid[uid] = r
        origin = (r.get("origin_url") or "").strip()
        if origin:
            by_origin[origin] = r
    return {"by_uid": by_uid, "by_origin": by_origin}

def safe_repo_uid_from_run(repo: Dict[str, Any]) -> str:
    # Prefer repo_uid if run already includes it; else attempt {parsed in upstream} left to earlier generator.
    return repo.get("repo_uid") or ""

def safe_write_signature(obj: Dict[str, Any]) -> Dict[str, Any]:
    tmp = copy.deepcopy(obj)
    tmp["signatures"] = {}
    raw = json.dumps(tmp, sort_keys=True, separators=(",", ":")).encode("utf-8")
    obj["signatures"]["topology_manifest_sha256"] = sha256_bytes(raw)
    return obj

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--canonical", required=True, help="Path to canonical_manifest.json")
    ap.add_argument("--git-repos", required=True, help="Path to git_repos.json from audit run")
    ap.add_argument("--run-dir", required=True, help="Audit run directory (provenance)")
    ap.add_argument("--out", required=True, help="Output topology_manifest.json path")
    args = ap.parse_args()

    canonical = load_json(args.canonical)
    git_repos_obj = load_json(args.git_repos)
    run_repos = coerce_repo_list(git_repos_obj)

    idx = index_canonical(canonical)

    mappings = []
    unmapped = []

    for rr in run_repos:
        current_path = rr.get("repo_path") or rr.get("path") or ""
        if not current_path:
            continue

        # Best: repo_uid present in run
        uid = safe_repo_uid_from_run(rr)
        canon = idx["by_uid"].get(uid) if uid else None

        # Fallback: match by origin_url string if run includes origin url.
        if not canon:
            # attempt find an origin remote url in run data
            origin_url = ""
            for remote in (rr.get("remotes") or []):
                if remote.get("name") == "origin" and remote.get("url"):
                    origin_url = remote["url"].strip()
                    break
            if origin_url:
                canon = idx["by_origin"].get(origin_url)

        if not canon:
            unmapped.append({
                "current_path": current_path,
                "reason": "no_match_in_canonical_manifest",
                "notes": ""
            })
            continue

        mappings.append({
            "repo_uid": canon.get("repo_uid", ""),
            "current_path": os.path.normpath(current_path),
            "canonical_path": os.path.normpath(canon.get("canonical_path", "")),
            "realm_id": canon.get("realm_id", ""),
            "organ_id": canon.get("organ_id", ""),
            "org_unit_id": canon.get("org_unit_id", ""),
            "repo_unit_id": canon.get("repo_unit_id", ""),
            "origin_url": canon.get("origin_url", ""),
            "lifecycle": canon.get("lifecycle", ""),
            "visibility": canon.get("visibility", ""),
            "needs_move": os.path.normpath(current_path) != os.path.normpath(canon.get("canonical_path", "")),
            "notes": ""
        })

    out = {
        "manifest_id": "topology_manifest_v1",
        "generated_at": now_iso(),
        "generated_by": {"agent": "gen_topology_manifest", "run_dir": args.run_dir},
        "inputs": {
            "canonical_manifest": args.canonical,
            "git_repos": args.git_repos
        },
        "mappings": mappings,
        "unmapped": unmapped,
        "signatures": {}
    }

    out = safe_write_signature(out)
    safe_write_json(args.out, out)
    print(f"wrote {args.out}")
    print(f"mapped: {len(mappings)}  unmapped: {len(unmapped)}")

if __name__ == "__main__":
    main()
```

* * *

## 2) `$WORLD_ROOT/_registry/tools/gen_repo_index.py`

This reads:

*   `canonical_manifest.json` (authoritative)
    
*   `organ_manifest.json` (authoritative bindings, optional if canonical already contains organ_id)
    

It writes:

*   `$WORLD_ROOT/_registry/repo_index.csv`
    

```python
#!/usr/bin/env python3
import argparse
import csv
import os
import json
from typing import Any, Dict, List

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(s: str) -> str:
    return (s or "").strip()

def bindings_map(organ_manifest: Dict[str, Any]) -> Dict[str, str]:
    m: Dict[str, str] = {}
    for b in organ_manifest.get("bindings", []):
        rid = b.get("repo_uid", "")
        oid = b.get("organ_id", "")
        if rid and oid:
            m[rid] = oid
    return m

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--canonical", required=True, help="Path to canonical_manifest.json")
    ap.add_argument("--organ", required=False, default="", help="Path to organ_manifest.json (optional)")
    ap.add_argument("--out", required=True, help="Output repo_index.csv path")
    args = ap.parse_args()

    canonical = load_json(args.canonical)
    organ = load_json(args.organ) if args.organ else {}
    organ_map = bindings_map(organ) if organ else {}

    rows: List[Dict[str, str]] = []
    for r in canonical.get("repos", []):
        repo_uid = normalize(r.get("repo_uid", ""))
        organ_id = normalize(organ_map.get(repo_uid, "")) or normalize(r.get("organ_id", ""))
        rows.append({
            "realm_id": normalize(r.get("realm_id", "")),
            "organ_id": organ_id,
            "org_unit_id": normalize(r.get("org_unit_id", "")),
            "repo_unit_id": normalize(r.get("repo_unit_id", "")),
            "lifecycle": normalize(r.get("lifecycle", "")),
            "visibility": normalize(r.get("visibility", "")),
            "canonical_path": normalize(r.get("canonical_path", "")),
            "origin_url": normalize(r.get("origin_url", "")),
            "head_oid": normalize((r.get("head_snapshot") or {}).get("head_oid", "")),
            "head_ref": normalize((r.get("head_snapshot") or {}).get("head_ref", "")),
            "last_audited_at": normalize((r.get("audit") or {}).get("last_audited_at", "")),
            "repo_uid": repo_uid
        })

    # Deterministic sort
    rows.sort(key=lambda x: (
        x["realm_id"], x["organ_id"], x["org_unit_id"], x["repo_unit_id"], x["repo_uid"]
    ))

    fieldnames = [
        "realm_id","organ_id","org_unit_id","repo_unit_id",
        "lifecycle","visibility","canonical_path","origin_url",
        "head_oid","head_ref","last_audited_at","repo_uid"
    ]

    out_path = args.out
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)

    print(f"wrote {out_path}")
    print(f"rows: {len(rows)}")

if __name__ == "__main__":
    main()
```

* * *

## 3) Update the wrapper: `gen_manifests.sh`

Extend your wrapper so it produces all four artifacts in one deterministic run.

Replace your `gen_manifests.sh` with:

```bash
#!/usr/bin/env bash
set -euo pipefail

: "${WORLD_ROOT:?WORLD_ROOT is required}"
: "${AUDIT_ROOT:?AUDIT_ROOT is required}"
: "${VCS_HOST:=github.com}"

RUN_DIR="${1:?usage: gen_manifests.sh $AUDIT_ROOT/run_<timestamp>}"

OVERRIDES="${WORLD_ROOT}/_registry/explicit_overrides.json"
MATRIX="${WORLD_ROOT}/_registry/realm_organ_matrix.json"

CANON_OUT="${WORLD_ROOT}/_registry/canonical_manifest.json"
ORGAN_OUT="${WORLD_ROOT}/_registry/organ_manifest.json"
TOPO_OUT="${WORLD_ROOT}/_registry/topology_manifest.json"
INDEX_OUT="${WORLD_ROOT}/_registry/repo_index.csv"

PY_CANON="${WORLD_ROOT}/_registry/tools/gen_canonical_manifest.py"
PY_ORGAN="${WORLD_ROOT}/_registry/tools/gen_organ_manifest.py"
PY_TOPO="${WORLD_ROOT}/_registry/tools/gen_topology_manifest.py"
PY_INDEX="${WORLD_ROOT}/_registry/tools/gen_repo_index.py"

GIT_REPOS="${RUN_DIR}/git_repos.json"

if [[ ! -f "${GIT_REPOS}" ]]; then
  echo "missing ${GIT_REPOS}" >&2
  exit 2
fi

python3 "${PY_CANON}" \
  --git-repos "${GIT_REPOS}" \
  --overrides "${OVERRIDES}" \
  --run-dir "${RUN_DIR}" \
  --out "${CANON_OUT}"

python3 "${PY_ORGAN}" \
  --canonical "${CANON_OUT}" \
  --overrides "${OVERRIDES}" \
  --matrix "${MATRIX}" \
  --out "${ORGAN_OUT}"

python3 "${PY_TOPO}" \
  --canonical "${CANON_OUT}" \
  --git-repos "${GIT_REPOS}" \
  --run-dir "${RUN_DIR}" \
  --out "${TOPO_OUT}"

python3 "${PY_INDEX}" \
  --canonical "${CANON_OUT}" \
  --organ "${ORGAN_OUT}" \
  --out "${INDEX_OUT}"

echo "done"
echo "canonical: ${CANON_OUT}"
echo "organ:     ${ORGAN_OUT}"
echo "topology:  ${TOPO_OUT}"
echo "index:     ${INDEX_OUT}"
```

* * *

## 4) Minimal file placement

You now have a coherent toolchain layout:

`$WORLD_ROOT/_registry/explicit_overrides.json`  
`$WORLD_ROOT/_registry/realm_organ_matrix.json`  
`$WORLD_ROOT/_registry/tools/gen_canonical_manifest.py`  
`$WORLD_ROOT/_registry/tools/gen_organ_manifest.py`  
`$WORLD_ROOT/_registry/tools/gen_topology_manifest.py`  
`$WORLD_ROOT/_registry/tools/gen_repo_index.py`  
`$WORLD_ROOT/_registry/tools/gen_manifests.sh`

* * *

## 5) One critical tightening (recommended)

Make `gen_canonical_manifest.py` also compute `git_repos_hash` by hashing the input `git_repos.json`, so you can trace exactly which run produced the manifest. It’s a small change: read the file bytes, hash, store into `audit.git_repos_hash`.

If you want that patch, say “patch hashing,” and I’ll provide a minimal diff.

## Q: 
Make gen_canonical_manifest.py also compute git_repos_hash by hashing the input git_repos.json, so you can trace exactly which run produced the manifest. It’s a small change: read the file bytes, hash, store into audit.git_repos_hash.

## A: 
```diff
--- a/gen_canonical_manifest.py
+++ b/gen_canonical_manifest.py
@@
 def load_json(path: str) -> Any:
     with open(path, "r", encoding="utf-8") as f:
         return json.load(f)
 
+def read_file_bytes(path: str) -> bytes:
+    with open(path, "rb") as f:
+        return f.read()
+
@@
 def build_manifest(
     git_repos: List[Dict[str, Any]],
     overrides: Dict[str, Any],
     world_root: str,
     audit_root: str,
     vcs_host: str,
     run_dir: str,
+    git_repos_hash: str,
 ) -> Dict[str, Any]:
@@
         repos_out.append({
@@
             "audit": {
                 "last_audited_at": now_iso(),
                 "run_dir": run_dir,
                 "inventory_hash": "",
-                "git_repos_hash": ""
+                "git_repos_hash": git_repos_hash
             },
             "notes": "",
             "exceptions": []
         })
@@
 def main() -> None:
@@
     git_repos_obj = load_json(args.git_repos)
     git_repos = coerce_repo_list(git_repos_obj)
     overrides = load_overrides(args.overrides if args.overrides else None)
 
+    git_repos_bytes = read_file_bytes(args.git_repos)
+    git_repos_hash = sha256_bytes(git_repos_bytes)
+
     manifest = build_manifest(
         git_repos=git_repos,
         overrides=overrides,
         world_root=world_root,
         audit_root=audit_root,
         vcs_host=vcs_host,
         run_dir=args.run_dir,
+        git_repos_hash=git_repos_hash,
     )
```

