# 18: Scheduled-Process Contract

**Date:** 2026-05-27
**Status:** ACTIVE — applies to all conductor-authored long-running processes (LaunchAgents, cron, foreground daemons) across all machines
**Derived from:** Universal Rule #55 (strict ban) + #55a (additive amendment); empirical history of LaunchAgent incidents (Jupyter P0, sysdiagnose jetsam kills, CCE-throttle attempts)
**Complements:** `17-branch-governance.md` (the analogous contract for GitHub-state writes by scheduled tasks); `INST-INDEX-RERUM-FACIENDARUM.md` (where IRF rows for new processes get filed before activation)

---

## 1. Purpose & Scope

Universal Rule #55 (strict): *No LaunchAgents — every incident froze/broke the machine. On-demand CLI only. HARD RULE.*

The strict rule was distilled from real incidents. It is also empirically wrong about scope: the conductor's machine runs 8 third-party LaunchAgents without issue (Backblaze, Google Updater×2, MS Edge, OpenAI, iMazing, Anthropic ShipIt, `homebrew.mxcl.atuin`). The rule's intent was always **"no unbounded conductor processes"**, not **"no `launchd` jobs of any kind."**

This document codifies the amendment (Rule #55a): scheduled / long-running processes are PERMITTED if they satisfy the **(a)-(e) contract** below; otherwise the strict #55 ban applies.

This document IS the durable authorization for the `launchd-contract-wrap` tool and any conductor-authored LaunchAgent/cron entry. Without it, scheduled processes default to forbidden.

---

## 2. The (a)-(e) contract

Every conductor-authored long-running process MUST satisfy all five conditions. Missing one = forbidden under strict #55.

### (a) Hard wall-clock cap

**Why:** Runaway processes consume RAM/CPU/process-slots; on a 16GB-RAM Beta-OS machine, this loses the jetsam lottery for an unrelated process. The Jupyter P0 incident: an unbounded Jupyter kernel that ran for hours.

**LaunchAgent form:** wrap command in `timeout <N>`; reinforce at launchd level with `ExitTimeOut: <N+10>` + `AbandonProcessGroup: false`.

**Cron form:** wrap command in `timeout <N>`; cron has no native equivalent to `ExitTimeOut`.

**Default cap:** 300 seconds (5 min). Longer caps require justification in the IRF row.

### (b) Resource bounds

**Why:** Even bounded processes can degrade interactive responsiveness if they run at default priority on a memory-constrained machine. The sysdiagnose audit revealed 3 jetsam kills in 36h on a day with multiple default-priority background tasks.

**LaunchAgent form:**
- `ProcessType: Background` (signals to launchd that the process is non-interactive; affects jetsam priority)
- `Nice ≥ 5` (lower CPU priority; default is 0)
- `LowPriorityIO: true` (deprioritize I/O scheduling)

**Cron form:** `nice -n 5 <command>` and `ionice -c 3 <command>` (Linux); macOS cron uses `nice` only.

### (c) Kill-switch on consecutive failures

**Why:** A misbehaving process that fails every minute is worse than one that fails once; cumulative resource pressure compounds. Need a built-in self-disable for unattended failure modes.

**LaunchAgent form:** wrapper script maintains a counter at `~/.local/share/conductor-launchd/failures/<name>.count`. On N consecutive failures (default N=3), wrapper touches a sentinel at `~/.local/share/conductor-launchd/disabled/<name>.disabled`. Sentinel-presence causes subsequent runs to no-op-and-exit (the wrapper checks first). `ThrottleInterval: 60` at launchd level prevents launchd's own rapid-restart from compounding the issue.

**Cron form:** wrapper script does the same sentinel-touch logic. Cron has no `ThrottleInterval`; rely on wrapper.

**Reset:** `rm <sentinel> && echo 0 > <counter>` after the conductor fixes the underlying issue.

### (d) Audit trail

**Why:** When an unattended process misbehaves at 3am, the conductor needs to know what happened without forensics. The corpus's existing audit-log primitive (TSV at `~/.claude/scheduled-tasks/audit/YYYY-MM-DD.log`) already serves scheduled-tasks MCP entries; extend it to LaunchAgents/cron.

**Format:** TSV with columns: `<ISO-timestamp>\t<process-name>\t-\t-\t<action>\t<status>`. Actions: `run`, `skip`, `kill-switch-triggered`. Statuses: `success`, `failure-rc-N`, `timeout-killed-Ns`, `kill-switch-active`, `N-consecutive-failures`.

**Path:** `~/.claude/scheduled-tasks/audit/YYYY-MM-DD.log` — same path as scheduled-tasks MCP entries. Rotates daily by file-per-day; no log-rotation infrastructure needed.

### (e) Pre-registered IRF row

**Why:** A LaunchAgent that no one remembers adding is exactly the class of mystery process the original Rule #55 was preventing. Forcing an IRF row before activation ensures triple-reference (Rule #23) is satisfied: the process exists in (1) plist + wrapper, (2) audit log entries, (3) IRF row with stated purpose and closure options.

**Form:** New IRF row in `INST-INDEX-RERUM-FACIENDARUM.md`, P-class as appropriate, stating:
- What the process does
- Why it can't be on-demand CLI (justify departure from strict #55)
- Closure options (when can this be retired?)
- Activation timestamp + LaunchAgent label

**Enforcement:** the `launchd-contract-wrap` tool prints `(e) IRF row: CONDUCTOR RESPONSIBILITY` and does NOT auto-install. The conductor invokes `launchctl bootstrap` manually after filing the row.

---

## 3. Authoring tool: `launchd-contract-wrap`

The CLI `~/.local/bin/launchd-contract-wrap` (shipped in domus `dot_local/bin/`) generates compliant artifacts.

```bash
launchd-contract-wrap <name> <cmd-abs-path> <cron-or-interval> [max-runtime-sec] [nice]
```

Output:
- `~/Library/LaunchAgents/com.conductor.<name>.plist` — the plist
- `~/.local/share/conductor-launchd/wrappers/<name>.sh` — the wrapper (enforces a/b/c/d)
- State dirs for counter + sentinel

The tool **validates the plist with `plutil -lint`** before exiting. It does NOT install. It prints the `launchctl bootstrap` command for the conductor to run AFTER filing the IRF row.

Constraints enforced by the tool:
- `name` must be lowercase kebab-case (matches `^[a-z0-9-]+$`)
- `cmd` must exist and be executable
- `max-runtime` must be > 0
- `nice` must be ≥ 5
- Cron form supports only `* | <integer>` per field (no ranges/lists — launchd limitation)

---

## 4. Exemptions

The contract applies to **conductor-authored** processes only. The following are EXEMPT:

- **Apple system LaunchAgents/LaunchDaemons** (`/System/Library/`, Apple-signed) — Apple's responsibility, not conductor's failure class.
- **Vendor auto-updaters** (Google Updater, MS Edge Updater, Anthropic ShipIt, OpenAI Atlas update-helper, iMazing, Backblaze) — third-party-signed, sandboxed by their vendors, well-bounded by design.
- **Homebrew services** (`brew services start <pkg>`) — `homebrew.mxcl.<pkg>.plist` files are part of the package-manager affordance; the package author is responsible for bounds. Exception: if a Homebrew service misbehaves on this machine, treat it as a Rule #55 violation and migrate it to `launchd-contract-wrap` (which adds the conductor's own bounds).

The `monthly-launchagent-audit` scheduled task classifies into three buckets:
- **VIOLATION** — conductor-authored, missing one or more of (a)-(e). Recommend immediate `launchctl bootout` + IRF row.
- **EXEMPT** — third-party-signed per the above list. Count only.
- **COMPLIANT** — conductor-authored, all (a)-(e) satisfied (label starts with `com.conductor.`, wrapper present, IRF row exists for the label). Count + sample.

---

## 5. Migration path from existing cron / scheduled-tasks

When migrating an existing user-cron entry or scheduled-tasks MCP task to a LaunchAgent (e.g., because it needs sleep-wake-aware firing):

1. **File the IRF row first** (e). Without it, the migration is forbidden.
2. **Run `launchd-contract-wrap`** with the target command and schedule.
3. **Review the generated plist + wrapper.** Verify (a)-(d) bounds match the use case.
4. **Activate**: `launchctl bootstrap gui/$(id -u) <plist>` then `launchctl enable gui/$(id -u)/<label>`.
5. **Remove the original**: edit `crontab -e` to delete the cron entry, OR `update_scheduled_task` with `enabled: false` for the MCP task.
6. **Verify**: wait for the next scheduled fire, then check `~/.claude/scheduled-tasks/audit/<date>.log` for the entry.

If any of (a)-(e) are not satisfiable for a given use case, the migration is forbidden — keep the original (cron / MCP) form, or accept that the work runs only when its triggering surface is active.

---

## 6. Reverting the amendment

If the (a)-(e) contract proves insufficient — e.g., if a future incident shows that even bounded LaunchAgents cause cascading failures — Rule #55a is RETIRED (not the contract itself, but its scope-relaxation effect). The original Rule #55 strict ban remains in force.

The retirement signal: any P0 incident traceable to a LaunchAgent that satisfied (a)-(e) at the time of incident. The IRF row for that incident must explicitly call out which contract condition was inadequate, so the contract can be tightened rather than abandoned.

---

## 9. Audit-log universal applicability (extends (d) from LaunchAgent-only to all Class-(I) routines)

**Codified 2026-05-27** following the 2026-05-26 defect inventory which revealed that 7 of 8 active scheduled-tasks-MCP routines did not write to the audit log on every fire (only `monthly-launchagent-audit` did, because it explicitly cited Rule #55a (d)).

The original Rule #55a (d) applies to LaunchAgents. This section extends the same discipline to every Class-(I) routine (scheduled-tasks-MCP entries + any future fire-on-cadence work in the conductor's local-token surface).

### The invariant

**Every Class-(I) fire MUST write start + end entries to `~/.claude/scheduled-tasks/audit/YYYY-MM-DD.log` regardless of whether the routine performs any writes.**

Rationale: the audit log is the **canonical fire registry**. Absence of an entry means defect (the routine forgot to log), not no-fire. Without this invariant, the `lastRunAt` MCP field becomes the only fire-tracking surface — and that field doesn't survive task retirement or MCP-tool changes the way an append-only TSV does.

### The bookend pattern (mechanical implementation)

Two invocations per fire, top and bottom of every SKILL.md prompt:

```bash
# Phase 0 (top of prompt):
~/.local/bin/scheduled-task-audit-bookend <task-id> start

# … main routine work …

# Phase Final (bottom of prompt):
~/.local/bin/scheduled-task-audit-bookend <task-id> end <one-line-status>
```

The shim `~/.local/bin/scheduled-task-audit-bookend` (shipped 2026-05-27, source at `${DOMUS_ROOT}/dot_local/bin/executable_scheduled-task-audit-bookend`) handles:
- TSV formatting with UTC timestamp
- Per-day log rotation
- Tab-stripping in status strings (safety)
- Never-fail-parent semantics (audit-log write should never block the routine)

### Status format (the `<one-line-status>` parameter)

- **Hyphen-separated** (no whitespace, no tabs) — the audit log is TSV
- **Summarize the fire's headline finding** — what would a human want to see if reading `tail -1 audit/<date>.log`?
- **Embed counts where relevant** — `204-repos-3-unpushed-0-pushes`, `71-prs-0-writes`, `8-orphan-705-stale`
- **Use `no-X` form for null findings** — `no-drift`, `no-orphans-no-stale`, `no-violations`
- **Use `key=value` form for multi-metric** — `compliant=2-exempt=8-violation=0`

### Per-action audit writes preserved

The existing per-action audit writes from Rule #55a (d) and standards doc 17 § 10 continue to apply. Bookend `start`/`end` are the **outer envelope**; per-action writes are inner detail. Example timeline for a fire with 2 writes:

```
2026-05-27T13:00:42Z  daily-pr-management  -  -  start  -
2026-05-27T13:01:15Z  daily-pr-management  portfolio  84  draft-to-ready  success
2026-05-27T13:02:30Z  daily-pr-management  domus  142  auto-merge-enable  success
2026-05-27T13:08:55Z  daily-pr-management  -  -  end  71-prs-tier2=2-promotions=1-merges=1
```

### Per-routine status conventions (canonical examples)

| Routine | Status format |
|---|---|
| `daily-hook-drift` | `no-drift` OR `drift-detected-<event-types>` |
| `daily-repo-hygiene` | `<N>-repos-<U>-unpushed-<O>-orphan-<S>-stale-<P>-pushes` |
| `daily-pr-management` | `<N>-prs-tier1=<X>-tier2=<Y>-tier3=<Z>-writes=<W>` |
| `daily-worktree-triage-and-cleanup` | `<R>-repos-<W>-worktrees-<C>-removals-<D>-dirty-<L>-locked` |
| `daily-code-review` | `<N>-commits-summarized-<R>-repos` OR `no-commits-since-yesterday` |
| `weekly-irf-aging` | `<R>-rows-<A>-aging-<S>-shipped-<O>-overdue` |
| `weekly-sibling-scope-drift` | `<S>-scopes-<C>-cross-3plus-<P>-promotion-candidates` |
| `monthly-launchagent-audit` | `compliant=<C>-exempt=<E>-violation=<V>` |

### Defect-detection by the invariant

A future `weekly-audit-log-coverage-witness` Class-(I) routine (to be authored) can grep the audit log to verify: for every active scheduled task, every expected-firing date has exactly one `start` + one `end` entry. Missing pairs = routine-defect; mismatched counts (start without end, or vice versa) = mid-fire failure.

This closes the loop: the audit-log invariant is itself audited by a routine that writes to the audit log.

---

## 7. Cross-references

- **Universal Rule #55** (strict ban): `dot_config/ai-context/universal-rules.md.tmpl` line 65 (domus)
- **Universal Rule #55a** (amendment): immediately following #55 in the same file
- **`launchd-contract-wrap`**: `dot_local/bin/executable_launchd-contract-wrap` (domus)
- **`monthly-launchagent-audit`** scheduled task: `~/.claude/scheduled-tasks/monthly-launchagent-audit/SKILL.md` — updated 2026-05-27 to use the three-bucket classification from Section 4
- **Audit log path**: `~/.claude/scheduled-tasks/audit/YYYY-MM-DD.log` — same primitive used by scheduled-tasks MCP per `17-branch-governance.md` Section 10
- **Empirical incident memory** (the original ban motivation):
  - `~/.claude/projects/-Users-[user]/memory/project_artifact_2026_05_22_four_roots_audit.md` (Jupyter LaunchAgent P0)
  - `~/.claude/projects/-Users-[user]/memory/project_artifact_2026_05_22_sysdiagnose_forensic_audit.md` (jetsam kills)
  - `~/.claude/projects/-Users-[user]/memory/feedback_no_launchagents.md` (referenced from domus CLAUDE.md "LaunchAgents (macOS) — REMOVED" section)

---

## 8. Open extensions (future, not blocking)

- **Daily `daily-launchagent-contract-check` task** — granular daily check that the conductor's LaunchAgents are firing within their (a)-(c) bounds. Currently the monthly audit suffices for enumeration; the daily check would surface "this process keeps timing out but the kill-switch hasn't triggered yet" earlier.
- **`launchd-contract-wrap` --dry-run flag** — emit the artifacts to a tmp dir for review without touching `~/Library/LaunchAgents/`.
- **Cron-side contract wrapper** — analogous CLI for `crontab` entries. The cron use case is smaller (no sleep-wake awareness) but the wrapper would still enforce (a)+(c)+(d) for cron entries that exist for portability reasons.
