# Session Prompts: 2026-06-12

**Session ID:** `07b0585a-ae81-44db-a476-bdf8e8e5135d`
**Duration:** ~8 min
**Working directory:** `/Users/4jp`
**Prompts:** 19 human messages

---

### P1 — 2026-06-12 13:02:07

<scheduled-task name="daily-pr-management" file="/Users/4jp/.claude/scheduled-tasks/daily-pr-management/SKILL.md">
This is an automated run of a scheduled task. The user is not present to answer questions. For implementation details, execute autonomously without asking clarifying questions — make reasonable choices and note them in your output. "write" actions (e.g. MCP tools that send, post, create, update, or delete), only take them if the task file asks for that specific action. When in doubt, producing a report of what you found is the correct output.

## Version: v1.0.3
## Status format: `<N>-prs-tier1=<X>-tier2=<Y>-tier3=<Z>-writes=<W>` (e.g., `71-prs-tier1=8-tier2=18-tier3=45-writes=0`)

## Metadata
- **Owner:** conductor (`4444J99` / `4444jPPP`)
- **Class:** I (local-token; migrates to Class-(III) in doc 19 Phase 4)
- **Cadence:** daily (09:01 EDT)
- **Author scope:** conductor identities ONLY — `4444J99`, `4444jPPP`. Bot identities (`google-labs-jules[bot]`, `dependabot[bot]`) are explicitly OUT of scope and have their own surfaces: `daily-dependabot-merge` (peer routine) and `IRF-OPS-082` (Jules 346-PR sunk-cost one-time triage). Codex / OpenCode / Gemini-CLI / Claude Code push under local `gh` auth = `4444J99` identity, so they are already covered.
- **IRF row:** IRF-SYS-211 (Rule #55a + Aggressive workflow pass — consolidated PR-automation surface) · IRF-SYS-223 (v1.0.0 → v1.0.1 author-scope + JSON-field drift fix)
- **Depends on:** `gh` CLI auth, `${REGISTRY_V2}` for tier classification, `~/.local/bin/dependabot-tier-classify` (canonical Phase-B resolver, shared with `daily-dependabot-merge`), canonical-replies whitelist at `~/.claude/scheduled-tasks/canonical-replies.md`
- **Repo-registry canonical path:** `~/Code/organvm/organvm-corpvs-testamentvm/repo-registry.json` (at repo root — corrected v1.0.1; prior text claimed a non-existent `data/` subdir. Renamed from `registry-v2.json` per corpvs ADR-019 / PR #419 — a backward-compat symlink at the old name still resolves)
- **Audit log path:** `~/.claude/scheduled-tasks/audit/YYYY-MM-DD.log`
- **Conformance:** docs/standards/24 v1.1.0
- **Last semver bump:** 2026-06-10 — v1.0.3 — Phase B now invokes the canonical deterministic resolver `~/.local/bin/dependabot-tier-classify` (shared with `daily-dependabot-merge`) instead of the v1.0.2 inline basename-flatten. This (a) ends the two-implementations divergence behind the 2026-06-10 incident, (b) fixes the collision silent-drop the basename map still had (`.github` ×8 / `hokage-chess` ×2 collapsed to one arbitrary row), (c) adds the `protected` report-only gate (flagship/infra/sovereign held regardless of promotion_status), and (d) aligns the prose-vs-impl split to the resolver's safer rule (unknown `4444J99/<repo>` → Tier 1, not Tier 3). Prior: 2026-06-10 — v1.0.2 — five fixes surfaced by the 2026-06-10 live fire (the run that "only produced a report" until corrected). **(a) Phase-B registry matching was a silent no-op** — the `"org/name"`-slug lookup matched 0 of 64 PRs (registry keys are lowercased AND use organ-org names while PRs live under the `a-organvm` umbrella org), collapsing every PR to the Tier-1 unknown→safest default. Fixed to lowercased-basename matching. **(b) Human-comment gate must exclude bots** — §10 #5 gates only on *humans* other than the author; without bot-exclusion the routine is falsely blocked by sourcery/codex/coderabbit/gemini/qodo review noise (this alone neuters Phase C-2/D). **(c) Authorization posture codified** — the contract IS standing authorization for Tier-2 enablement + Tier-3 merge within caps; the run must NOT degrade to report-only on public-ORGANVM grounds when §8/§10 gates pass. **(d) Comment-cap vs 5-promotion-cap reconciled** — post canonical-reply #4 on ≤3 promotions (the 3-comment cap binds). **(e) Immediate-merge awareness + secret pre-scan** — a Tier-2 enablement on an UNSTABLE/CLEAN PR with no pending *required* checks merges at once; secret-adjacent Phase-D titles get a `gh pr diff` grep first. See "Authorization posture", "Human-gate", "Per-run merge ceiling", and "Implementation gotchas". Prior: 2026-05-28 — v1.0.1 — four drift fixes surfaced by the 2026-05-27 fire's forensic post-mortem (`abandoned-end` row, 2026-05-27 audit log). **(a) Author scope as post-filter, not API parameter** — `--author=@me` silently collapsed scope to whatever identity the CLI was authenticated as. The naive fix `--author=4444J99 --author=4444jPPP` doesn't work either: the flag is `string` (singular), so the last value wins; and `4444jPPP` doesn't exist as a GitHub user. The robust fix enumerates everything and post-filters via jq on `.author.login`, preserving visibility for Phase E reporting. **(b) JSON-field list trimmed to fields actually supported by `gh search prs`** — `mergeable / mergeStateStatus / reviewDecision / headRefName / baseRefName / commits / comments` are NOT search-API fields; they must come from per-PR `gh pr view`. **(c) `registry-v2.json` canonical path corrected** — was claimed at `data/registry-v2.json`, real path is repo root. **(d) `--limit 1000` documented** — default 30 silently truncates (a-organvm had 430 open in the 2026-05 sample). Prior: 2026-05-27 — initial v1.0.0 (post-consolidation; merged from prior `daily-pr-promote-and-triage` + `daily-pr-execute-by-tier` per doc 23 alchemical evolution; those evolved-testaments still queryable).

## Audit log (start — invoke FIRST)
Run: `~/.local/bin/scheduled-task-audit-bookend daily-pr-management start`
Per docs/standards/18 §9, every Class-(I) fire must emit start + end entries regardless of writes.

Operate under `~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-branch-governance.md` Sections 8 + 10. **Read it first.** If unreadable, abort to report-only mode for the entire run.

## Authorization posture (v1.0.2 — read before deciding to defer)
This contract IS the conductor's standing authorization for the writes it defines: draft→ready promotions, Tier-2 auto-merge enablement, and Tier-3 squash-merges. When the §8 tier rule and the §10 hard-NEVERs are satisfied, **execute** — do **not** degrade to report-only and do **not** defer a Tier-2/Tier-3 write merely because the target is a public ORGANVM repo. The home-CLAUDE.md "no push to public ORGANVM main without per-session authorization" rule is **pre-satisfied for this narrow, gated, contracted scope** by the existence of this task; it is not a reason to park authorized work. A report is the residue of the run, not its product — the run's job is to *act* within the caps. Report-only is correct ONLY when pre-flight fails, a hard-NEVER blocks, or a gate genuinely does not pass.

## Human-gate (v1.0.2 — "unanswered comment" means unanswered by a HUMAN)
§10 #5 gates merges on comments from **humans other than the author**. Review bots are NOT humans and must be excluded before computing the gate. Treat a login as a bot if it ends in `[bot]` OR matches `(?i)bot|sourcery|codex-connector|coderabbit|gemini-code-assist|qodo|dependabot|jules|github-actions`. A PR is human-gated only when the latest *human* (non-author, non-bot) comment is newer than the author's latest comment. Without this exclusion the routine is falsely blocked by review-bot noise and under-acts — the failure mode that produced a no-op report on 2026-06-10.

## Pre-flight (all must pass — any fail = abort writes, run Phase E only)
- Standards doc 17 readable
- Audit log path writable
- `gh auth status` returns authenticated
- Canonical-replies whitelist readable
- repo-registry.json readable

## Procedure

### Phase A: enumerate (read-only, ONCE)
For each conductor-owned org/user (`4444J99`, `a-organvm`, `meta-organvm`, `organvm-i-theoria` through `-vii-kerygma`):

```
gh search prs --owner=<org> --state=open \
  --json url,number,title,isDraft,author,repository,updatedAt,commentsCount \
  --limit 1000
```

Then **post-filter** in jq, retaining only PRs authored by the conductor identity set:

```
| jq '[.[] | select(.author.login == "4444J99")]'
```

Notes (v1.0.1):
- Author scope is enforced as a **post-filter, not as an API parameter.** Empirical reasons:
  - `gh search prs --author` is a `string` (singular). Passing `--author=A --author=B` makes the last value win, NOT an OR — would silently collapse scope.
  - The constitutional alt-identity `4444jPPP` does not exist as a GitHub user (verified 2026-05-28 — `gh search prs --author=4444jPPP` errors with "users do not exist"). Treat the metadata reference as aspirational until/unless that account is created.
  - Post-filtering preserves visibility into the bot/outside populations for Phase E reporting without a second API call.
- Author-set expansion: if a second conductor identity is later created (e.g., `4444jPPP`), update the jq filter to `select(.author.login == "4444J99" or .author.login == "4444jPPP")` — semver-bump to the next patch at that time, and confirm the new identity exists via `gh api users/<login>` before shipping.
- `--limit 1000` is required: the default 30 truncates large orgs (e.g., `a-organvm` had 430 open in 2026-05 sample).
- Field set is restricted to what `gh search prs` actually supports. Per-PR detail required by Phase C/D (`mergeStateStatus`, `reviewDecision`, `headRefName`, `baseRefName`, `commits[]`, `statusCheckRollup`) MUST come from `gh pr view <n> --repo <slug> --json …` invocations against each candidate, not from Phase A's batch search.

### Phase B: tier-classify (read-only, ONCE — via the canonical deterministic resolver)
**Do NOT hand-roll classification.** Pipe every enumerated PR slug through the single
canonical resolver shared with `daily-dependabot-merge`, so the two routines that fire
10 min apart over the same PRs can never diverge again (the 2026-06-10 incident):

```
printf '%s\n' "${SLUGS[@]}" | ~/.local/bin/dependabot-tier-classify --stdin
```

One JSON object per slug: `{slug, tier, resolution, matched_org, matched_name,
promotion_status, repo_tier, protected, reason}`. Read `.tier`, `.protected`, and
`.resolution`. Non-zero exit (registry unreadable) → abort writes → report-only.
Run `dependabot-tier-classify --self-test` in pre-flight.

The resolver supersedes the v1.0.2 basename-flatten (which silently dropped one row on
every duplicate `name` — `.github` ×8, `hokage-chess` ×2 — to an arbitrary tier). It
implements §8 faithfully PLUS three things prose cannot: case-insensitive exact match,
`a-organvm` redirect-alias resolution, and an ambiguity guard (collision/unknown →
**Tier 1**). §8 rules it applies (first match wins):
- **Tier 1**: `promotion_status == "GRADUATED"` AND `tier ∈ {infrastructure, flagship, sovereign}`
- **Tier 2**: `promotion_status ∈ {PUBLIC_PROCESS, CANDIDATE}` OR `tier == "standard"`
- **Tier 3**: `promotion_status ∈ {LOCAL, ARCHIVED}` OR `owner == 4444J99`
- **Unknown OR ambiguous** → **Tier 1**

This also resolves the prior prose-vs-impl split: the resolver is now the single
authority, so an **unknown `4444J99/<repo>` → Tier 1** (safest), not Tier 3. Treat
`protected == true` (any flagship/infrastructure/sovereign repo) as **report-only** in
Phase C/D regardless of computed tier — a GRADUATED-flagship under the personal org
(e.g. `domus-genoma`) and a non-GRADUATED flagship (e.g. `portfolio`) are both held.

### Phase C: SAFE WRITES — draft→ready + Tier 2 auto-merge enable
For each draft PR where ALL of: Tier 2/3 (NOT Tier 1) AND `protected == false`, author=`4444J99`/`4444jPPP`, ≥1 non-merge commit, CI SUCCESS/EXPECTED/empty, last commit >24h old, title NOT WIP/DRAFT/[wip]/[draft]/DO NOT MERGE. **Cap: max 5 promotions.** A `DIRTY` merge state does NOT disqualify a promotion — the gate is CI + title, because draft→ready is a review-readiness signal, not a merge.

Execute (60s/30s stagger): `gh pr ready <PR-URL>`, then post canonical-reply #4 **on at most 3 promotions** (the 3-comment/run cap binds *below* the 5-promotion cap — the draft→ready timeline event is self-documenting for the rest; never exceed 3 comments just to satisfy the per-promotion instruction), per-action audit.

Then for each non-draft Tier 2 PR (`protected == false`, author=conductor, APPROVED or no-review-required, CLEAN/UNSTABLE, **no unanswered _human_ comments** — see Human-gate). **Cap: max 3 enablements.** `gh pr merge --auto --squash --delete-branch`. **Immediate-merge awareness:** when the PR is `UNSTABLE`/`CLEAN` with no *pending required* checks, `--auto` has nothing to wait on and GitHub merges immediately — so an enablement is frequently an effective merge to that repo's `main` (public ORGANVM repos included). This is intended and authorized (see Authorization posture); count it under the per-run merge ceiling below. Post canonical-reply #3 only if the 3-comment cap is not already spent on promotions.

### Phase D: HIGHER-AUTHORITY WRITES — Tier 3 actual squash-merges
**Wait 180 seconds** after Phase C. Skip if Phase C had 3+ failures.

For each non-draft Tier 3 PR (CLEAN, all checks passed, **no unanswered _human_ comments** — see Human-gate). **Cap: max 3 merges.**

Execute (60s/30s stagger, oldest-first): **re-verify state immediately before each merge** (`gh pr view` → require `state=OPEN`, `isDraft=false`, `mergeStateStatus=CLEAN`, `mergeable=MERGEABLE`, zero FAILURE checks, human-gate clear). A sibling merge into the same repo can leave the next PR transiently `mergeable=UNKNOWN` while GitHub recomputes — that is a state-mismatch → skip + log; re-verifying a now-*settled* PR later in the same run and merging it then is **not** a forbidden retry (it is a fresh successful gate). **Secret pre-scan:** if the title or head branch matches `(?i)auth|cookie|token|secret|key|cred|password`, run `gh pr diff` and grep for real credential patterns (`gh[pousr]_…`, `AKIA…`, `BEGIN … PRIVATE KEY`, `(secret|password|api[_-]?key|token)\s*[:=]\s*"…"`, `xox[baprs]-…`) excluding placeholders — withhold + log on any hit (validate-before-shipping). Then `gh pr merge --squash --delete-branch`, per-action audit, canonical-reply #6 sparingly.

**Per-run merge ceiling (v1.0.2 reconciliation).** The two phase caps are independent: ≤3 Tier-2 enablements (Phase C-2) AND ≤3 Tier-3 direct merges (Phase D). Because a Tier-2 enablement often merges immediately (above), a single run can produce up to 6 effective merges — which exceeds the literal "max 3 auto-merges performed per task run" wording in doc 17 §10. Read §10's phrase as the **Phase-D direct-merge cap**; the Phase-C-2 enablement cap is separate and additive. Reconciling §10's wording to match is a corpvs-standard edit (Tier-1, separate authorization) — tracked, not done here.

### Phase E: READ-ONLY REPORT
Structured Markdown: (a) awaiting your reply, (b) Merge-ready Tier 1 (manual), (c) Stale >14d, (d) Blocked by CI, (e) Phase C+D summary.

## Implementation gotchas (v1.0.2 — learned from the 2026-06-10 fire)
- **`gh pr view --json commits` schema** is `{oid, messageHeadline, messageBody, authoredDate, committedDate, authors[]}` — there is NO `.commit.author.date` (that is the REST shape). Use `.committedDate` for recency and `.messageHeadline` for the merge-commit test.
- **`gh search prs` does not expose** `mergeable / mergeStateStatus / reviewDecision / headRefName / baseRefName / commits / comments / statusCheckRollup` — fetch all per-PR detail via `gh pr view <n> --repo <slug> --json …`.
- **zsh `echo "$json" | jq` mangles control characters** in commit/comment bodies → "Invalid string: control characters" parse errors. Write the JSON to a file and run `jq` on the file (or use `gh … --jq`); do not round-trip JSON through `echo`.
- **Staggers:** foreground `sleep 60` is blocked in the agent harness. Run the staggered write sequence as a single detached background script (background jobs may `sleep`), or pace with the harness's wait primitive — do not chain short sleeps.
- **`reviewDecision` is empty (`""`/null)** when no review is required — treat empty as "no-review-required" (eligible), distinct from `REVIEW_REQUIRED`/`CHANGES_REQUESTED` (ineligible).

## Failure semantics
- Single failure: log + continue
- 3 failures in Phase C: skip Phase D entirely
- 3 failures in Phase D: abort remaining
- State-mismatch in Phase D step 1: skip + log

## What this task NEVER does (Section 10 hard-NEVERs)
- Tier 1 writes, code amendments, substantive comments (only canonical-replies), force pushes / direct main pushes, merges with unanswered **human** maintainer-other comments (bots excluded — see Human-gate), action on WIP/DRAFT titles

## Audit log (end — invoke LAST, after the report)
Run: `~/.local/bin/scheduled-task-audit-bookend daily-pr-management end <status>`
where `<status>` follows format `<N>-prs-tier1=<X>-tier2=<Y>-tier3=<Z>-writes=<W>`. Use hyphens; no whitespace.
</scheduled-task>

**Actions taken:**
- Bash: `~/.local/bin/scheduled-task-audit-bookend daily-pr-management start 2>&1; echo "---EXIT:$?---"`
- Bash: `cat ~/Code/organvm/organvm-corpvs-testamentvm/docs/standards/17-branch-governance.md 2>&1 | head -5; echo "===READABLE_C...`
- Bash: `cd ~/Code/organvm/organvm-corpvs-testamentvm 2>/dev/null; awk '/^## (8|10)\.?/{p=1} /^## (9|11)\.?/{if(NR>1)p=0} p' docs...`
- Bash: `echo "=== gh auth ==="; gh auth status 2>&1 | head -8
echo "=== canonical-replies ==="; test -r ~/.claude/scheduled-task...`
- Bash: `echo "=== orgs I belong to ==="; gh api user/orgs --jq '.[].login' 2>&1 | head -30
echo "=== my own repos w/ open PRs (q...`
- Bash: `cd /tmp && rm -f pr_*.json all_prs.json
owners="4444J99 a-organvm meta-organvm organvm organvm-i-theoria organvm-ii-poie...`
- Bash: `cd /tmp && rm -f pr_*.json
owners=(4444J99 a-organvm meta-organvm organvm organvm-i-theoria organvm-ii-poiesis organvm-i...`
- Bash: `cd /tmp
jq -s 'add | [.[] | select(.author.login=="4444J99")]' pr_4444J99.json pr_a-organvm.json pr_meta-organvm.json pr...`
- Bash: `cd /tmp
jq -r '.[].repository.nameWithOwner' conductor_prs.json | sort -u > uniq_slugs.txt
echo "Unique repos: $(wc -l <...`
- Bash: `cd /tmp
# Build tier lookup as JSON object keyed by slug
jq -s 'map({key:.slug, value:{tier:.tier, protected:.protected,...`
- Bash: `cd /tmp
cands=(
"a-organvm/call-function--ontological 8"
"a-organvm/alchemia-ingestvm 7"
"a-organvm/organvm-ontologia 8"...`
- Bash: `cd /tmp
for f in /tmp/prview_*.json; do
  jq -r '
    def isbot(l): (l|test("\\[bot\\]$")) or (l|ascii_downcase|test("bo...`
- Bash: `cd /tmp
# Re-poll UNKNOWN+fail=false Tier-2 candidates to settle mergeability
declare -a settle=(
"a-organvm/alchemical-...`
- Bash: `echo "=== canonical-replies whitelist ==="; cat ~/.claude/scheduled-tasks/canonical-replies.md 2>&1 | head -60
echo ""
e...`
- Bash: `cd /tmp
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
echo "Attempting Tier-2 auto-merge enablement on vigiles#5 (verification probe...`
- Bash: `cd /tmp
echo "=== Stale >14d (updatedAt < 2026-05-29) ==="
jq -r '[.[] | select(.updatedAt < "2026-05-29")] | length as ...`
- Bash: `cd /tmp
echo "=== PR counts per tier (for status string) ==="
jq -r 'group_by(.tinfo.tier)[] | "tier\(.[0].tinfo.tier): ...`
- Bash: `~/.local/bin/scheduled-task-audit-bookend daily-pr-management end "82-prs-tier1=62-tier2=19-tier3=1-writes=0" 2>&1; echo...`

---

---

## Prompt Summary

**Total prompts:** 1
**Session duration:** ~8 min
**Avg time between prompts:** ~8.0 min

### Prompt Categories (heuristic)

- **Directives** (implement/build/create/add/write): 1
- **Questions**: 1
- **Fixes** (fix/error/bug/broken/fail): 1
- **Reviews** (check/verify/review/audit): 1
