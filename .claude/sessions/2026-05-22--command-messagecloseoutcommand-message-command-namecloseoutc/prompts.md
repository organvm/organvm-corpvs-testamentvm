# Session Prompts: 2026-05-22

**Session ID:** `a008c272-d082-4420-9343-4f0336f08fa5`
**Duration:** ~92 min
**Working directory:** `/Users/4jp/Code/organvm/organvm-corpvs-testamentvm`
**Prompts:** 52 human messages

---

### P1 — 2026-05-22 22:16:20

<command-message>closeout</command-message>
<command-name>/closeout</command-name>
<command-args>re:all-sessions; survey, cleanup, report:' ❯ double check all work; be the hall-monitor wanting oh so badly to catch someone breaking the rules;
The Index Rerum Faciendarum at meta-organvm/organvm-corpvs-testamentvm/INST-INDEX-RERUM-FACIENDARUM.md is the universal work registry (150 items, 19 domains, IRF-XXX-NNN
  IDs). On start: check for P0/P1 items in your working domain. During work: note completed or discovered IRF items. On close: update the IRF — move completed items to ##
  Completed, add new items to their domain section, update statistics. REQUIRED: propagate completions to ALL interested external indices — close GitHub issues, check omega
  scorecard impact, update inquiry-log.yaml if SGO work, update seed.yaml if capabilities changed, update CLAUDE.md if architecture changed, update concordance if new IDs
  introduced. Default is check-all-10-indices and skip inapplicable, not check-none. CLI: organvm irf list --priority P0 | organvm irf stats
❯ all the N/As suggest something imperative; it means their is a vacuum where something should be--research it, plan it, log it;
none-knowledge--N/A, no data, seed lacking--creates vacuum 
                                                                                      
  ❯ all the N/As suggest something imperative; it means their is a vacuum where    
  something should be--research it, plan it, log it;              
❯ there seemed to be a shit ton of issues as you proceeded--overwriting was not done correct? we only add? then the audit sorts it after, correct?                                      
❯ persistent memory MUST be local & remote simultaneously; if the physical manifestaion dies > soul persists;                                                                           
❯ [(local):(remote)={1:1}; correct? 
› if:dead[manifestion(physical)] > then:live[soul(persists)];
❯ so nothing was lost? if lost, recover immediatley; this is a rule that MUST be universally contextually applied;                                                                      
❯ commit[all] push[origin]; source returned improved onnwards+upwards;
❯ all has been added to universale context ? nothing
will be lost? ';</command-args>

### P2 — 2026-05-22 22:16:20

Base directory for this skill: /Users/4jp/.claude/skills/closeout

# /closeout — Session Close-Out Ritual

## When to invoke

- User explicitly says: `/closeout`, "close out", "wrap up", "end the session"
- Before any non-trivial `git push` (the close-out should precede the push)
- When the session has produced 3+ files, plans, or atoms and the user is signaling end

## Six-step protocol

### Step 1 — Inventory session outputs

Run, in parallel where possible:

```bash
# What files did this session create or modify?
git status --short

# What plans were authored in this session?
ls -t ~/.Codex/plans/*.md 2>/dev/null | head -10

# What's the current branch and where does it stand vs origin?
git branch --show-current
git log @{u}.. 2>/dev/null || echo "(no upstream tracking)"
```

Surface a brief inventory table to the user:
- N files modified, M created
- K plans authored this session
- L commits ahead of origin

### Step 2 — Walk back through plans

For each plan authored this session (filter `~/.Codex/plans/*.md` by mtime within session window):

For each plan, classify it as one of:
- **EXECUTED**: contains `DONE-NNN` reference. No action.
- **IN-PROGRESS**: contains `IRF-XXX-NNN` reference but no DONE-NNN. Update its frontmatter to confirm continued status.
- **ABANDONED**: no closure reference, no follow-on commits. Move to `~/.Codex/plans/abandoned/` with a brief abandonment-reason.

Ask the user for ambiguous cases. Do NOT bulk-classify without confirmation — the home-scope AGENTS.md rule "Atoms are permanent — never batch-close" applies to plans-as-artifacts too.

### Step 3 — Walk back through atoms (if applicable)

If `data/prompt-registry/prompt-atoms.json` was touched this session, identify atoms that were closed in this session and confirm their `status` field is updated.

If not (most sessions), skip.

### Step 4 — Verify git state

Cross-check:
- Working tree is clean (no uncommitted changes meant for this session)
- Local main is in sync with origin (or branch tracks correctly)
- No stray exports/temp files in workspace root (`ls /Users/4jp/Workspace/*.txt` should be empty)

If stray exports exist (the auto-named `2026-MM-DD-NNNNNN-this-session-being-continued-from-a-previous-c.txt` pattern), move them to `~/Documents/session-exports/` or delete if duplicative.

### Step 4.5 — Verify CLAUDE.md autogen freshness (hall-monitor gate)

If the active repo has a `CLAUDE.md` carrying `<!-- ORGANVM:AUTO:START -->` / `<!-- ORGANVM:AUTO:END -->` sentinels, run the gate:

```bash
~/.local/bin/claude-md-autogen-gate
```

If it exits non-zero, the autogen tail is older than 7 days. **Refuse to mark the session as DONE.** Refresh first:

```bash
organvm context sync --write     # autogen sections only
# or
organvm refresh                  # full 10-step pipeline
```

Then re-stage `CLAUDE.md` and commit (the `claude-md-autogen-freshness` pre-commit hook will re-verify), and re-run the gate.

Bypass only with explicit user authorization:

```bash
AUTOGEN_FRESHNESS_THRESHOLD_DAYS=999 ~/.local/bin/claude-md-autogen-gate
```

Pairs with the pre-commit hook (`claude-md-autogen-freshness`); together they catch staleness at both the commit boundary and the session boundary. Root-cause precedent: 32-day autogen-tail staleness traced on 2026-05-16 to `organvm refresh` step 6 soft-failing on `system-system--system: invalid tier 'sovereign'` (closed via schema + validator lockstep edit; see GH `4444J99/domus-semper-palingenesis#30`, IRF-DOM-048).

### Step 5 — Update active-handoff (if exists)

If `.conductor/active-handoff.md` exists in any active repo, update it with:
- What this session accomplished
- What's locked / not-yet-attempted
- What the next session should pick up

This is the cross-session continuity gate.

### Step 6 — Write CLOSEOUT_SUMMARY.md

Produce a session-close-out summary at `~/.Codex/plans/closeout-{date}.md` with:

```markdown
# Session Close-Out — {date}

## Outputs
- {N} files created, {M} modified
- {K} plans authored: {filenames}
- {L} commits made (SHAs): {sha-list}

## Closure marks
- EXECUTED plans (DONE-NNN refs): {list}
- IN-PROGRESS plans (IRF refs): {list}
- ABANDONED plans (moved): {list}

## Pending
- Uncommitted changes: {if any}
- Unpushed commits: {if any}
- Active handoff: {path if exists}

## Hand-off note for next session
{one-paragraph context for resumability}
```

## Rules to honor

- **Never batch-close atoms or plans without explicit user confirmation.** Per Universal Rule (memory rule #53): atoms are permanent, never batch-close.
- **Never delete plan files.** Move to `abandoned/` instead, preserving the history (per the plan-discipline section of the home AGENTS.md).
- **Never push as part of closeout** unless user has explicitly authorized push for this session. Closeout's job is to *prepare* for push, not perform it.
- **If the session produced no notable artifacts**, say so and exit cleanly. Closeout is fast on quiet sessions.

## Why this exists

Per `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md`:

> 90.4% of plans are ORPHANED. Of 427 plans in `~/.Codex/plans/`, 386 contain neither a DONE-NNN nor IRF reference. Only 20 (4.7%) are EXECUTED, 21 (4.9%) are IN-PROGRESS.

The orphan rate is a direct artifact of the absence of a close-out ritual. This skill is the ritual.

The cost of skipping is invisible bookkeeping debt: plans accumulate, atoms stay open against doctrine that already encodes them, the system can't programmatically answer "what was done?". The cost of doing it is ~3-5 minutes per session.

## Related

- `docs/evaluation/SELF-REVIEW-MASTER-2026-05-05.md` — Pathology #4: plan-author cadence vastly exceeds plan-execution cadence (21:1)
- `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md` — full data behind the 90.4% orphan rate
- Universal Rule #2: "Nothing local only" — close-out is what makes "nothing local only" achievable per session


ARGUMENTS: re:all-sessions; survey, cleanup, report:' ❯ double check all work; be the hall-monitor wanting oh so badly to catch someone breaking the rules;
The Index Rerum Faciendarum at meta-organvm/organvm-corpvs-testamentvm/INST-INDEX-RERUM-FACIENDARUM.md is the universal work registry (150 items, 19 domains, IRF-XXX-NNN
  IDs). On start: check for P0/P1 items in your working domain. During work: note completed or discovered IRF items. On close: update the IRF — move completed items to ##
  Completed, add new items to their domain section, update statistics. REQUIRED: propagate completions to ALL interested external indices — close GitHub issues, check omega
  scorecard impact, update inquiry-log.yaml if SGO work, update seed.yaml if capabilities changed, update CLAUDE.md if architecture changed, update concordance if new IDs
  introduced. Default is check-all-10-indices and skip inapplicable, not check-none. CLI: organvm irf list --priority P0 | organvm irf stats
❯ all the N/As suggest something imperative; it means their is a vacuum where something should be--research it, plan it, log it;
none-knowledge--N/A, no data, seed lacking--creates vacuum 
                                                                                      
  ❯ all the N/As suggest something imperative; it means their is a vacuum where    
  something should be--research it, plan it, log it;              
❯ there seemed to be a shit ton of issues as you proceeded--overwriting was not done correct? we only add? then the audit sorts it after, correct?                                      
❯ persistent memory MUST be local & remote simultaneously; if the physical manifestaion dies > soul persists;                                                                           
❯ [(local):(remote)={1:1}; correct? 
› if:dead[manifestion(physical)] > then:live[soul(persists)];
❯ so nothing was lost? if lost, recover immediatley; this is a rule that MUST be universally contextually applied;                                                                      
❯ commit[all] push[origin]; source returned improved onnwards+upwards;
❯ all has been added to universale context ? nothing
will be lost? ';

**Actions taken:**
- Bash: `git status --short && echo "---BRANCH---" && git branch --show-current && echo "---UPSTREAM---" && git log @{u}.. --onel...`
- Bash: `git diff INST-INDEX-RERUM-FACIENDARUM.md | head -100`
- Bash: `ls -lat ~/.claude/plans/*.md 2>/dev/null | head -10 && echo "---codex---" && ls -lat ~/.Codex/plans/*.md 2>/dev/null | h...`
- Bash: `echo "---corpvs---" && git status --short | wc -l && echo "---walking other repos for unpushed/uncommitted---" && for d ...`
- Bash: `cd ~/Code/organvm/my-knowledge-base && git status --short && echo "---" && git log --oneline -3`
- Bash: `cd ~/Code/organvm/a-i--skills.broken-xattr-2026-05-16 && git status --short 2>&1 | head -5 && echo "---" && ls -la .git/...`
- Bash: `echo "---walking ~/Workspace too---" && for d in ~/Workspace/*/; do if [ -d "$d/.git" ]; then cd "$d" 2>/dev/null; modif...`
- Bash: `cd ~/Workspace/session-meta && git status --short 2>&1 | head -20 && echo "---remote---" && git remote -v 2>&1 | head -3`
- Bash: `cd ~/Code/organvm/organvm-corpvs-testamentvm && git remote get-url origin && echo "---" && git fetch origin main 2>&1 | ...`
- Bash: `cd ~/Code/organvm/my-knowledge-base && ls -d .specstory .test-tmp atomized intake 2>&1 | head -10 && echo "---intake siz...`
- Bash: `cd ~/Code/organvm/my-knowledge-base && grep -E "^(intake|atomized|\.specstory|\.test-tmp)" .gitignore 2>/dev/null && ech...`
- Bash: `cat ~/.claude/plans/handoff-2026-05-22-remote-canonical-parity.md 2>/dev/null | head -80`
- Bash: `cd ~/Workspace/session-meta && git remote -v 2>&1 | head -3 && echo "---" && ls -la HEALTH-REPORT.md 2>&1 | head -2 && e...`
- Bash: `cd ~/Code/organvm/organvm-corpvs-testamentvm && git add INST-INDEX-RERUM-FACIENDARUM.md && git diff --cached --stat && e...`
- Bash: `cd ~/Code/organvm/organvm-corpvs-testamentvm && git log --oneline -3 && echo "---verify remote---" && git ls-remote orig...`
- Write `/Users/4jp/.claude/plans/closeout-2026-05-22-hall-monitor-cross-session-survey.md`

---

### P3 — 2026-05-22 22:28:22 (+12m)

all unique data survives present context upon exit?

**Actions taken:**
- Bash: `echo "=== 1. IRF commit on remote ===" && cd ~/Code/organvm/organvm-corpvs-testamentvm && git ls-remote origin main | he...`
- Bash: `echo "=== Closeout in chezmoi source? ===" && ls -la ~/Workspace/4444J99/domus-semper-palingenesis/private_dot_claude/pl...`
- Bash: `cd ~/Workspace/4444J99/domus-semper-palingenesis && echo "=== git status ===" && git status --short | head -10 && echo "...`
- Bash: `cd ~/Workspace/4444J99/domus-semper-palingenesis && echo "=== git log for closeout file ===" && git log --oneline -- pri...`

---

### P4 — 2026-05-22 22:37:55 (+9m)

re:current-cwd('~/Code/organvm/organvm-corpvs-testamentvm'); all unique data survives present context upon exit?

**Actions taken:**
- Bash: `cd ~/Code/organvm/organvm-corpvs-testamentvm && echo "=== 1. Working tree state ===" && git status --short && echo "(emp...`

---

### P5 — 2026-05-22 22:44:33 (+6m)

codify following process:' To build a decentralized architecture where raw logs are transformed into curated data products owned by business units, you need a Data Mesh Architecture powered by a Modern Data Stack (MDS).
------------------------------
## 1. The Architecture Blueprint
This architecture relies on a Medallion (Lakehouse) structure split across decentralized domains, tied together by a central governance plane.

[ RAW SOURCE ] ──► [ INGESTION ] ──► [ BRONZE ] ──► [ SILVER ] ──► [ GOLD ] ──► [ CONSUMPTION ]
 (Logs/DBs)         (Airbyte/Fivetran) (Raw Logs)    (Cleaned/Atomized) (Indexed/Products)  (BI/AI/Apps)
                                           │              │              │
                                           ▼              ▼              ▼
                                  ┌──────────────────────────────────────────────┐
                                  │      CENTRAL GOVERNANCE & CATALOG PLANE       │
                                  │    (Metadata, Frontmatter, Unique IDs, Access)│
                                  └──────────────────────────────────────────────┘

## Ingestion Layer

* Tools: Airbyte, Fivetran, or Apache Kafka (for streaming logs).
* Role: Extracts raw data from databases and application logs. Moves it to storage without modification.

## Storage & Compute Layer (The Lakehouse)

* Tools: Snowflake, Databricks, or AWS S3 with Apache Iceberg.
* Bronze Layer (Raw): Append-only storage of messy logs and raw DB dumps.
* Silver Layer (Enriched): Data is atomized, cleaned, deduplicated, and conformed to schema rules.
* Gold Layer (Curated Data Products): Data is aggregated, indexed, assigned unique IDs, and structured for domain consumption.

## Central Governance Plane (The Glue)

* Tools: dbt (Data Build Tool), Atlan, or Collibra.
* Role: Manages the frontmatter/metadata, data cataloging, lineage tracking, and row-level access control.

------------------------------
## 2. The Domain Process Cycle (The Lifecycle)
Every business domain follows a continuous 6-phase lifecycle to ingest raw data, transform it, and serve it to domain owners.

┌────────────────────────────────────────────────────────┐
│  1. INGEST  ──►  2. CLEAN  ──►  3. ATOMIZE & INDEX      │
└───────────────────────────┬────────────────────────────┘
                            ▼
┌────────────────────────────────────────────────────────┐
│  6. REFRESH ◄──  5. GOVERN ◄──  4. PUBLISH & DELIVER   │
└────────────────────────────────────────────────────────┘

## 1. Ingest (Raw Stage)

* Raw logs and database snapshots land in the domain's Bronze bucket.
* Data is immutable and retains its original messy structure.

## 2. Clean & Standardize (Silver Stage)

* Anomalies and null values are handled.
* Timestamps are normalized to a uniform timezone (e.g., UTC).
* Data types are strictly cast (e.g., strings to integers).

## 3. Atomize & Index (Gold Stage)

* Atomization: Monolithic log objects (like massive JSON blobs) are shredded into granular, single-purpose tables.
* Identification: A deterministic hashing algorithm (like MD5 or UUIDv5) generates permanent unique IDs across systems.
* Indexing: Cluster keys or indexes are applied for rapid query performance.

## 4. Publish & Deliver (The Product)

* Frontmatter Injection: dbt generates a schema.yml containing metadata, ownership tags, and column definitions.
* Delivery: The dataset is exposed as a secure view or shared table directly inside the Domain Owner's workspace.

## 5. Govern & Secure

* Role-Based Access Control (RBAC) ensures only authorized domain users can read the data.
* Data quality monitors (e.g., Great Expectations or dbt tests) run automatically to check for uniqueness and nulls.

## 6. Refresh & Iterate

* Orchestration tools (like Apache Airflow or Prefect) trigger the pipeline on a schedule (e.g., hourly) or via events.
* Domain owners provide feedback to data engineers to evolve the schema as business needs change.

------------------------------



 ';

**Actions taken:**
- Bash: `cd ~/Code/organvm/organvm-corpvs-testamentvm && ls docs/standards/ 2>&1 | head -20 && echo "---" && echo "next number?" ...`
- Write `/Users/4jp/Code/organvm/organvm-corpvs-testamentvm/docs/standards/16-data-mesh-medallion-architecture.md`
- ToolSearch
- EnterWorktree
- Write `/Users/4jp/Code/organvm/organvm-corpvs-testamentvm/.claude/worktrees/standard-16-data-mesh/docs/standards/16-data-mesh-medallion-architecture.md`
- Read `/Users/4jp/Code/organvm/organvm-corpvs-testamentvm/.claude/worktrees/standard-16-data-mesh/INST-INDEX-RERUM-FACIENDARUM.md`
- Bash: `grep -oE "IRF-SYS-[0-9]+" /Users/4jp/Code/organvm/organvm-corpvs-testamentvm/.claude/worktrees/standard-16-data-mesh/INS...`
- Bash: `grep -n "IRF-SYS-194" /Users/4jp/Code/organvm/organvm-corpvs-testamentvm/.claude/worktrees/standard-16-data-mesh/INST-IN...`
- Read `/Users/4jp/Code/organvm/organvm-corpvs-testamentvm/.claude/worktrees/standard-16-data-mesh/INST-INDEX-RERUM-FACIENDARUM.md`
- Edit `/Users/4jp/Code/organvm/organvm-corpvs-testamentvm/.claude/worktrees/standard-16-data-mesh/INST-INDEX-RERUM-FACIENDARUM.md`
- Bash: `git status --short && echo "---diff stat---" && git diff --stat && echo "---commit---" && git add docs/standards/16-data...`
- Bash: `cd /Users/4jp/Code/organvm/organvm-corpvs-testamentvm && echo "=== current branch in main checkout ===" && git branch --...`
- ToolSearch
- ExitWorktree
- ExitWorktree
- Bash: `echo "=== verify Standard 16 still in main ===" && git log --oneline -3 && echo "" && echo "=== verify file on disk ==="...`

---

### P6 — 2026-05-22 23:18:42 (+34m)

<command-message>personalized-storefront-render</command-message>
<command-name>/personalized-storefront-render</command-name>

### P7 — 2026-05-22 23:18:42

Base directory for this skill: /Users/4jp/.claude/skills/personalized-storefront-render

# Personalized Storefront Render — Substrate Skill

> Translate internal artifacts into client-facing surfaces in the client's domain language. Substrate, not bespoke build.

## When to invoke

- User asks for "a client-facing version of X" / "translate this for Rob/Maddie/<client>" / "ELI5 / TLDR of <internal doc>".
- User wants every internal artifact (or a class of them) to project to a client storefront.
- A new client is being onboarded and needs a personalized read-surface for ongoing work.
- A specific artifact is tagged with `audiences:` frontmatter and the storefront has not been regenerated.

## When NOT to invoke

- The artifact is governance/SOP/internal-only with no client surface (`audiences: [internal]` or unmtagged).
- The work is bespoke creative direction for a specific deliverable (use the relevant domain skill — Hokage bridge content, Spiral lineage substrate, etc.).
- The client surface already exists and is hand-curated outside this substrate (do not ingest after-the-fact; respect the existing artifact).

## Architecture (4 layers)

```
LAYER 0 — PERSONA CORPUS  (~/Documents/personas/)
  {id}.md          ← prose source-of-truth (untouched by this skill)
  {id}.lexicon.yaml ← machine-readable translation table (this skill consumes)

LAYER 1 — INTERNAL ARTIFACTS  (per client repo, /docs/**)
  Existing artifacts, optionally extended with YAML frontmatter:
  audiences[], tldr, strata, client_render_mode

LAYER 2 — TRANSLATION ENGINE  (this skill)
  Composes:
    Product Domain Engine (Phase 4 logos→pathos rendering)
    8-Strata Domain Ideal-Whole (gap-map / coverage detection)
    voice-enforcement (constitution check vs persona register)
    lexicon-substitution (forbidden-terms removal, analogy mapping, ELI5/TLDR shaping)
  Output: docs/storefront/_generated/<artifact>.<persona>.client.md
   then:  docs/storefront/_curated/<artifact>.<persona>.client.md  (after human ratify)

LAYER 3 — DEPLOY SURFACE  (per-repo, per-stack adapter)
  Hokage:  /storefront/[...slug] via Next.js → rob.<domain> (link-gated)
  Spiral:  /storefront/[...slug] via Astro → maddie.<domain> (link-gated)
  Future:  static adapter ships plain HTML
```

## Commands (CLI surface)

The skill is callable from any agent; the operator-facing form is the `organvm storefront` subcommand:

| Command | Purpose |
|---|---|
| `organvm storefront sync --repo <path>` | Walk source.globs, read audiences frontmatter, render per-persona drafts to `_generated/`. Idempotent. |
| `organvm storefront audit [--persona <id>] [--unmtagged]` | Report: lexicons stale (>90d behind prose), unmtagged client-relevant artifacts, orphan curated files (no source), forbidden-term hits in any draft. |
| `organvm storefront ratify <artifact-slug> [--persona <id>]` | Move `_generated/...client.md` → `_curated/...client.md` after human read. Records voice-scorer score in artifact metadata. |
| `organvm storefront status` | One-line: `<n> drafts unratified · <m> internal artifacts changed since last sync · <k> forbidden-term hits`. |
| `organvm storefront feedback add --persona <id> --note "..."` | Append client feedback to `~/Documents/personas/{id}.feedback.md` and create an `IRF.STO-FEEDBACK-*` item. |

Invocation by agents: prefer the skill protocol (this document) over re-implementing; call the CLI for actual rendering.

## Composition contract (what this skill does NOT duplicate)

This skill is a conductor. It **invokes** existing skills/tools rather than re-implementing them:

- **Product Domain Engine** — Phase 4 (rhetorical-mode rendering) is invoked for the logos→pathos transform when audience.register requires it.
- **domain-ideal-whole-substrate** — the 8-strata `internal-magnet` rules are read to determine which source globs are eligible for client projection. The `gap-map` stratum surfaces audit findings.
- **voice-enforcement** — the persona's `voice_constitution` field names a rule pack that voice-scorer uses to score every draft pre-ratify.
- **stranger-test-protocol** — the verification step "fresh agent identifies the persona's domain language without invoking PDE/ontology terms" comes from this protocol.

**Do not** re-implement what these skills already do. Substrate failure modes flow downstream from substrate violations.

## Substrate refuses to render orphans

Every storefront-rendered artifact MUST trace `bridge_to:` lineage to a real internal artifact. The substrate refuses to emit `_generated/*.client.md` for any input where:

- No source file exists at the path implied by the artifact frontmatter, OR
- `bridge_to:` references a domain handle not present in the persona's lexicon, OR
- `audiences[].id` references a persona without a `{id}.lexicon.yaml` file in `~/Documents/personas/`.

This rule prevents personalization theatre — making something *sound like* the persona without saying anything they would actually care about. Density-of-real-content is the gravity.

## Lifecycle (Universal Rule #6 — everything is a loop)

```
internal artifact created/updated
  → audiences frontmatter present? if no → skip (default [internal])
  → operator runs `organvm storefront sync` (on demand, no daemon — Universal Rule #55)
  → render pipeline emits _generated/<artifact>.<persona>.client.md per audience entry
  → voice-scorer scores draft against persona.voice_constitution
  → IRF auto-issues STO-DRAFT-* item per unratified draft
  → operator reads + ratifies → _curated/
  → repo-native build (npm run build for Next.js, etc.) ships /storefront/* routes
  → client receives URL; reads in their language
  → client feedback enters via mailto + `storefront feedback add` → STO-FEEDBACK-* IRF items
  → next sync regenerates from updated source + lexicon
```

No daemons. No LaunchAgents. Pre-push git hook in opt-in repos may warn (exit 0) when client-relevant files changed without a regenerate; the warning surfaces the exact `storefront sync` command to run.

## Phased rollout (substrate maturity)

| Slice | Scope | Status (2026-04-25) |
|---|---|---|
| 1 — Rob storefront | Schema, Rob lexicon, hokage-chess config, frontmatter on 1+ canonical artifact, hand-curated drafts | scaffolded; route + deploy deferred (hokage Next.js has breaking changes per AGENTS.md) |
| 2 — Maddie storefront | Astro adapter, Maddie lexicon, spiral config, frontmatter on 5 spiral artifacts | pending |
| 3 — Full substrate | Auto-draft generator, pre-push hook, IRF wiring, mailto backfeed, static adapter, `audit --unmtagged` baseline | pending |

## References

- **Plan**: `~/.claude/plans/2026-04-25-personalized-client-storefront-substrate.md`
- **Schema**: `~/Workspace/organvm/schema-definitions/schemas/storefront-v1.schema.json`
- **Canonical example**: `~/Workspace/organvm/schema-definitions/examples/storefront-frontmatter-rob.yaml`
- **First persona lexicon**: `~/Documents/personas/rob-bonavoglia.lexicon.yaml`
- **First repo opt-in**: `~/Workspace/4444J99/hokage-chess/storefront.config.yaml`
- **Sibling skills**: `product-domain-engine` (PDE Phase 4 invocation), `domain-ideal-whole-substrate` (8-strata gap-map), `voice-enforcement` (per-persona constitution checks)


### P8 — 2026-05-22 23:19:29

slash{'TLDR'};

### P9 — 2026-05-22 23:42:50 (+23m)

<command-message>closeout</command-message>
<command-name>/closeout</command-name>

### P10 — 2026-05-22 23:42:50

Base directory for this skill: /Users/4jp/.claude/skills/closeout

# /closeout — Session Close-Out Ritual

## When to invoke

- User explicitly says: `/closeout`, "close out", "wrap up", "end the session"
- Before any non-trivial `git push` (the close-out should precede the push)
- When the session has produced 3+ files, plans, or atoms and the user is signaling end

## Six-step protocol

### Step 1 — Inventory session outputs

Run, in parallel where possible:

```bash
# What files did this session create or modify?
git status --short

# What plans were authored in this session?
ls -t ~/.Codex/plans/*.md 2>/dev/null | head -10

# What's the current branch and where does it stand vs origin?
git branch --show-current
git log @{u}.. 2>/dev/null || echo "(no upstream tracking)"
```

Surface a brief inventory table to the user:
- N files modified, M created
- K plans authored this session
- L commits ahead of origin

### Step 2 — Walk back through plans

For each plan authored this session (filter `~/.Codex/plans/*.md` by mtime within session window):

For each plan, classify it as one of:
- **EXECUTED**: contains `DONE-NNN` reference. No action.
- **IN-PROGRESS**: contains `IRF-XXX-NNN` reference but no DONE-NNN. Update its frontmatter to confirm continued status.
- **ABANDONED**: no closure reference, no follow-on commits. Move to `~/.Codex/plans/abandoned/` with a brief abandonment-reason.

Ask the user for ambiguous cases. Do NOT bulk-classify without confirmation — the home-scope AGENTS.md rule "Atoms are permanent — never batch-close" applies to plans-as-artifacts too.

### Step 3 — Walk back through atoms (if applicable)

If `data/prompt-registry/prompt-atoms.json` was touched this session, identify atoms that were closed in this session and confirm their `status` field is updated.

If not (most sessions), skip.

### Step 4 — Verify git state

Cross-check:
- Working tree is clean (no uncommitted changes meant for this session)
- Local main is in sync with origin (or branch tracks correctly)
- No stray exports/temp files in workspace root (`ls /Users/4jp/Workspace/*.txt` should be empty)

If stray exports exist (the auto-named `2026-MM-DD-NNNNNN-this-session-being-continued-from-a-previous-c.txt` pattern), move them to `~/Documents/session-exports/` or delete if duplicative.

### Step 4.5 — Verify CLAUDE.md autogen freshness (hall-monitor gate)

If the active repo has a `CLAUDE.md` carrying `<!-- ORGANVM:AUTO:START -->` / `<!-- ORGANVM:AUTO:END -->` sentinels, run the gate:

```bash
~/.local/bin/claude-md-autogen-gate
```

If it exits non-zero, the autogen tail is older than 7 days. **Refuse to mark the session as DONE.** Refresh first:

```bash
organvm context sync --write     # autogen sections only
# or
organvm refresh                  # full 10-step pipeline
```

Then re-stage `CLAUDE.md` and commit (the `claude-md-autogen-freshness` pre-commit hook will re-verify), and re-run the gate.

Bypass only with explicit user authorization:

```bash
AUTOGEN_FRESHNESS_THRESHOLD_DAYS=999 ~/.local/bin/claude-md-autogen-gate
```

Pairs with the pre-commit hook (`claude-md-autogen-freshness`); together they catch staleness at both the commit boundary and the session boundary. Root-cause precedent: 32-day autogen-tail staleness traced on 2026-05-16 to `organvm refresh` step 6 soft-failing on `system-system--system: invalid tier 'sovereign'` (closed via schema + validator lockstep edit; see GH `4444J99/domus-semper-palingenesis#30`, IRF-DOM-048).

### Step 5 — Update active-handoff (if exists)

If `.conductor/active-handoff.md` exists in any active repo, update it with:
- What this session accomplished
- What's locked / not-yet-attempted
- What the next session should pick up

This is the cross-session continuity gate.

### Step 6 — Write CLOSEOUT_SUMMARY.md

Produce a session-close-out summary at `~/.Codex/plans/closeout-{date}.md` with:

```markdown
# Session Close-Out — {date}

## Outputs
- {N} files created, {M} modified
- {K} plans authored: {filenames}
- {L} commits made (SHAs): {sha-list}

## Closure marks
- EXECUTED plans (DONE-NNN refs): {list}
- IN-PROGRESS plans (IRF refs): {list}
- ABANDONED plans (moved): {list}

## Pending
- Uncommitted changes: {if any}
- Unpushed commits: {if any}
- Active handoff: {path if exists}

## Hand-off note for next session
{one-paragraph context for resumability}
```

## Rules to honor

- **Never batch-close atoms or plans without explicit user confirmation.** Per Universal Rule (memory rule #53): atoms are permanent, never batch-close.
- **Never delete plan files.** Move to `abandoned/` instead, preserving the history (per the plan-discipline section of the home AGENTS.md).
- **Never push as part of closeout** unless user has explicitly authorized push for this session. Closeout's job is to *prepare* for push, not perform it.
- **If the session produced no notable artifacts**, say so and exit cleanly. Closeout is fast on quiet sessions.

## Why this exists

Per `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md`:

> 90.4% of plans are ORPHANED. Of 427 plans in `~/.Codex/plans/`, 386 contain neither a DONE-NNN nor IRF reference. Only 20 (4.7%) are EXECUTED, 21 (4.9%) are IN-PROGRESS.

The orphan rate is a direct artifact of the absence of a close-out ritual. This skill is the ritual.

The cost of skipping is invisible bookkeeping debt: plans accumulate, atoms stay open against doctrine that already encodes them, the system can't programmatically answer "what was done?". The cost of doing it is ~3-5 minutes per session.

## Related

- `docs/evaluation/SELF-REVIEW-MASTER-2026-05-05.md` — Pathology #4: plan-author cadence vastly exceeds plan-execution cadence (21:1)
- `docs/evaluation/self-review-2026-05-05/stale-plans-and-orphan-commits.md` — full data behind the 90.4% orphan rate
- Universal Rule #2: "Nothing local only" — close-out is what makes "nothing local only" achievable per session


**Actions taken:**
- Bash: `echo "=== Step 1: inventory ===" && git status --short && echo "(clean)" && echo "" && echo "=== branch / parity ===" &&...`
- Bash: `echo "=== active-handoff content (first 40 lines) ===" && head -40 .conductor/active-handoff.md && echo "" && echo "=== ...`
- Write `/Users/4jp/.claude/plans/closeout-2026-05-22-standard-16-codification.md`
- Bash: `echo "=== chezmoi source now? ===" && ls -la ~/Workspace/4444J99/domus-semper-palingenesis/private_dot_claude/plans/clos...`
- Bash: `cd ~/Workspace/4444J99/domus-semper-palingenesis && chezmoi add ~/.claude/plans/closeout-2026-05-22-standard-16-codifica...`

---

---

## Prompt Summary

**Total prompts:** 10
**Session duration:** ~92 min
**Avg time between prompts:** ~9.2 min

### Prompt Categories (heuristic)

- **Directives** (implement/build/create/add/write): 5
- **Questions**: 6
- **Fixes** (fix/error/bug/broken/fail): 3
- **Reviews** (check/verify/review/audit): 5
