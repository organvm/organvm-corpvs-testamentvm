# Emergency Procedures

**Purpose:** What to do when things break in the eight-organ system.
**Audience:** A competent developer responding to system issues with no prior context.
**Last updated:** 2026-02-16

---

## Severity Levels

| Level | Definition | Response time |
|-------|-----------|---------------|
| **SEV-1** | Registry corruption, dependency graph violation, billing overrun | Same day |
| **SEV-2** | CI failure cascade (>5 repos), workflow quota exhaustion | Within 48 hours |
| **SEV-3** | Individual repo CI failure, stale data, broken links | Next weekly check |

---

## Procedure 1: CI Failure Cascade (>5 Repos Failing)

**Symptoms:** Multiple repos show failing CI runs simultaneously. The soak test monitor reports `failing > 5`.

**Likely causes:**
- A shared dependency was updated with breaking changes (Dependabot batch)
- GitHub Actions service degradation
- A batch push triggered CI across many repos simultaneously

**Steps:**

1. **Assess scope:**
   ```bash
   # Check how many repos are failing
   python3 scripts/soak-test-monitor.py collect
   # Look at the CI section of the output
   ```

2. **Check GitHub status:**
   Visit https://www.githubstatus.com/ — if Actions is degraded, wait for resolution.

3. **Identify common cause:**
   ```bash
   # Look at failure details for recent runs
   gh run list --repo organvm-iv-taxis/orchestration-start-here --limit 5 --json conclusion,name,createdAt
   ```
   If multiple repos fail with the same error (e.g., "Node 18 deprecated"), the cause is environmental.

4. **If Dependabot batch:** Revert the problematic dependency update across affected repos. Or pin the version in the workflow files.

5. **If environmental:** Update the affected workflow files (e.g., bump Node version). The workflow specs are documented in `docs/implementation/github-actions-spec.md`.

---

## Procedure 2: Registry Corruption Recovery

**Symptoms:** `organ-audit.py` reports critical errors. `repo-registry.json` has invalid JSON, missing organs, or inconsistent data.

**Steps:**

1. **Don't panic.** The registry is version-controlled. Every change is in git history.

2. **Identify when corruption occurred:**
   ```bash
   cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm
   git log --oneline -20 -- repo-registry.json
   ```

3. **Restore from last known good state:**
   ```bash
   # Find the last commit where the audit passed
   # Then restore that version
   git show <good-commit>:repo-registry.json > repo-registry.json
   ```

4. **Validate the restored version:**
   ```bash
   python3 scripts/organ-audit.py \
       --registry repo-registry.json \
       --governance governance-rules.json \
       --output /tmp/recovery-audit.md
   ```

5. **If the corruption was from a script:** Check `scripts/` for recent changes. The most common cause is a batch update script that wrote partial data (e.g., interrupted during execution).

6. **Commit the fix:**
   ```bash
   git add repo-registry.json
   git commit -m "fix: restore registry from <good-commit> after corruption"
   git push origin main
   ```

---

## Procedure 3: Billing Overrun

**Context:** In February 2026, `organvm-i-theoria` hit 48,880 GitHub Actions minutes due to 14 cron workflows running across 149 repos. Three additional ORGAN-III cron workflows also contributed. Total: 17 cron workflows disabled.

**Symptoms:** GitHub sends billing alerts. Or you notice workflows are being queued but not running (quota exhaustion).

**Steps:**

1. **Identify which org is overrunning:**
   ```bash
   # Check each org's Actions usage
   for org in organvm-i-theoria organvm-ii-poiesis organvm-iii-ergon organvm-iv-taxis organvm-v-logos organvm-vi-koinonia organvm-vii-kerygma meta-organvm; do
       echo "--- $org ---"
       gh api "orgs/$org/settings/billing/actions" --jq '.total_minutes_used // "N/A"' 2>/dev/null || echo "  (no access or free plan)"
   done
   ```

2. **Identify expensive workflows:**
   ```bash
   # List workflows with recent runs for the overrunning org
   gh api "repos/<org>/<repo>/actions/runs?per_page=20" --jq '.workflow_runs[] | "\(.name) — \(.conclusion) — \(.run_started_at)"'
   ```

3. **Disable cron-triggered workflows** (the most common cause):
   ```bash
   # For each offending repo, disable the workflow via GitHub API
   gh api "repos/<org>/<repo>/actions/workflows/<workflow_id>/disable" --method PUT
   ```

   Or edit the workflow file to remove the `schedule:` trigger:
   ```bash
   # Remove schedule trigger, keep workflow_dispatch for manual runs
   gh api "repos/<org>/<repo>/contents/.github/workflows/<file>.yml" \
       --jq '.content' | base64 -d
   # Edit and re-push with schedule lines removed
   ```

4. **Wait for billing cycle reset** (monthly). GitHub free plan includes 2,000 min/month; Pro includes 3,000 min/month.

5. **Document which workflows were disabled** in this corpus (update MEMORY.md or create an ADR in `docs/adr/`).

**Prevention:** Before enabling any cron workflow, estimate monthly minutes: `runs_per_month * avg_minutes_per_run * num_repos`. The ORGAN-I overrun was 14 crons * ~30 runs/month * ~2 min/run * 20 repos = ~16,800 min/month.

---

## Procedure 4: Dependency Graph Violation

**Symptoms:** `organ-audit.py` or `validate-dependencies` workflow reports back-edges or cycles.

**Context:** The core invariant is that data flows I -> II -> III only. ORGAN-III cannot depend on ORGAN-II, and ORGAN-II cannot depend on ORGAN-I. ORGAN-IV through Meta may reference any organ.

**Steps:**

1. **Identify the violation:**
   ```bash
   python3 scripts/organ-audit.py \
       --registry repo-registry.json \
       --governance governance-rules.json \
       --output /tmp/dep-audit.md
   ```
   Look for lines like: `Back-edge violation: organvm-iii-ergon/repo -> organvm-ii-poiesis/repo`

2. **Determine if the dependency is real or stale:**
   - Read the offending repo's `seed.yaml` (if it has one) or check the `dependencies` field in `repo-registry.json`
   - Often, back-edges were introduced during batch operations and don't reflect actual code dependencies

3. **Remove the offending dependency:**
   - Edit `repo-registry.json` to remove the dependency from the `dependencies` array
   - If the repo has a `seed.yaml`, update its `consumes` field too

4. **Re-validate:**
   ```bash
   python3 scripts/v4-dependency-validation.py
   ```

5. **If the dependency is genuinely needed:** This means the architecture has a design problem. Document it as an ADR in `docs/adr/` and discuss whether the repo should be moved to a different organ.

---

## Procedure 5: GitHub Actions Quota Exhaustion

**Symptoms:** Workflow runs are queued but never start. GitHub shows "You've exceeded your spending limit" or workflows show "Queued" indefinitely.

**Steps:**

1. **Confirm it's a quota issue** (not a GitHub outage):
   ```bash
   gh api "orgs/organvm-iv-taxis/settings/billing/actions" --jq '.total_minutes_used'
   ```

2. **Triage active workflows:**
   - Orchestration workflows (ORGAN-IV) are highest priority — keep these running
   - Individual repo CI is lowest priority — these can wait

3. **Cancel non-essential queued runs:**
   ```bash
   # List queued runs
   gh run list --repo <org>/<repo> --status queued --json databaseId,name
   # Cancel specific runs
   gh run cancel <run_id> --repo <org>/<repo>
   ```

4. **Disable non-critical cron workflows** until the billing cycle resets (see Procedure 3).

5. **Long-term:** Consider moving high-frequency CI to a self-hosted runner or reducing workflow triggers (e.g., only run on PRs, not every push).

---

## Quick Reference: Key Files

| What | Where |
|------|-------|
| Registry | `repo-registry.json` |
| Governance rules | `governance-rules.json` |
| Audit script | `scripts/organ-audit.py` |
| Dependency validator | `scripts/v4-dependency-validation.py` |
| Metrics dashboard | `scripts/praxis-metrics-dashboard.py` |
| Soak test monitor | `scripts/soak-test-monitor.py` |
| Orchestration workflows | `organvm-iv-taxis/orchestration-start-here/.github/workflows/` |
| GitHub Actions spec | `docs/implementation/github-actions-spec.md` |

---

## Escalation

If you encounter a situation not covered here:

1. Check `docs/implementation/orchestration-system-v2.md` for governance rules
2. Check git history for how similar issues were resolved in the past
3. Check the CLAUDE.md and MEMORY.md files in this repo for accumulated operational knowledge
4. If the issue affects external-facing assets (portfolio, essays), prioritize those fixes
