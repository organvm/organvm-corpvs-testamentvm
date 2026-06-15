# Minimum Viable Operations

**Purpose:** What a second operator needs to do to keep the eight-organ system healthy.
**Audience:** A competent developer with GitHub experience but no prior knowledge of this system.
**Last updated:** 2026-02-16

---

## System Overview (60-Second Version)

The ORGANVM system is an eight-organ creative-institutional platform spanning 150 repositories across 8 GitHub organizations. It coordinates theory (ORGAN-I), art (ORGAN-II), commerce (ORGAN-III), orchestration (ORGAN-IV), public process (ORGAN-V), community (ORGAN-VI), marketing (ORGAN-VII), and meta-governance (Meta).

The system is **largely autonomous** — GitHub Actions workflows handle CI, dependency validation, essay monitoring, and distribution auditing. Your job as operator is to monitor, not to intervene.

**Source of truth:** `repo-registry.json` in `meta-organvm/organvm-corpvs-testamentvm`

---

## Daily Operations

**Required effort:** Zero (system is autonomous)

There is nothing you need to do daily. The following workflows run on their own:

| Workflow | Schedule | What it does |
|----------|----------|-------------|
| `essay-monitor.yml` | Daily 09:00 UTC | Detects new essays in public-process `_posts/` |
| CI workflows | On push | Run tests and linting per repo |

If you want to spot-check, glance at the GitHub Actions tab for `orchestration-start-here` to confirm runs are green.

---

## Weekly Operations

**Required effort:** ~15 minutes

### 1. Check Workflow Run History

```bash
# Quick check: are the orchestrator workflows green?
gh run list --repo organvm-iv-taxis/orchestration-start-here --limit 10
```

Look for:
- `orchestrator-agent` (runs Mon 07:00 UTC) — should show `completed / success`
- `validate-dependencies` (runs Mon 06:30 UTC) — should show `completed / success`
- `distribution-agent` (runs Wed 10:00 UTC) — should show `completed / success`

**If a workflow is failing:** See `emergency-procedures.md` for CI failure cascade response.

### 2. Review Dependabot PRs

```bash
# List open Dependabot PRs across key repos
gh pr list --repo organvm-iv-taxis/orchestration-start-here --author "dependabot[bot]" --state open
gh pr list --repo organvm-iv-taxis/agentic-titan --author "dependabot[bot]" --state open
```

For each open PR:
- Read the changelog summary
- If it's a patch/minor version bump with passing CI, merge it
- If it's a major version bump, review breaking changes before merging

---

## Monthly Operations

**Required effort:** ~1 hour

### 1. Run the Organ Audit

```bash
cd ~/Workspace/meta-organvm/organvm-corpvs-testamentvm

python3 scripts/organ-audit.py \
    --registry repo-registry.json \
    --governance governance-rules.json \
    --output audit-report.md \
    --metrics metrics.json \
    --github
```

This checks:
- Every organ has minimum repo count
- All repos have required fields
- No dependency graph violations (cycles, back-edges)
- No stale repos (>90 days without validation)
- README exists on GitHub for every repo

**Expected result:** `AUDIT PASSED` with zero critical alerts. Warnings are informational.

### 2. Review Engagement Trends

If the soak test monitor is running:

```bash
python3 scripts/soak-test-monitor.py report --days 30
```

Otherwise, manually check GitHub Insights for the top repos:
- `organvm-iv-taxis/orchestration-start-here`
- `organvm-v-logos/public-process`
- `organvm-i-theoria/recursive-engine--generative-entity`

Look for: traffic trends (views, clones), any new stars or forks.

### 3. Update System Metrics

```bash
python3 scripts/praxis-metrics-dashboard.py --output system-metrics.json
```

This regenerates the dashboard data used by the portfolio site. Commit and push if values have changed.

---

## Quarterly Operations

**Required effort:** ~2 hours

### Sustainability Checklist

Review each of these and note any concerns:

1. **Billing:** Check GitHub Actions usage across all 8 orgs. Historical overrun was in `organvm-i-theoria` (48,880 min in Feb 2026, caused by cron workflows — now disabled).
   ```bash
   # Check recent Actions usage (requires org admin)
   gh api orgs/organvm-i-theoria/settings/billing/actions --jq '.total_minutes_used'
   ```

2. **Dependency freshness:** Are any repos using deprecated libraries or outdated Node/Python versions?

3. **Registry accuracy:** Spot-check 5 random repos — does their `implementation_status` in the registry match reality?

4. **Essay cadence:** Has at least 1 essay been published in the last 90 days? (ORGAN-V health signal)

5. **Workflow drift:** Have any GitHub Actions workflow files been modified outside of this corpus? Check:
   ```bash
   gh api repos/organvm-iv-taxis/orchestration-start-here/commits?per_page=5 --jq '.[].commit.message'
   ```

---

## Key Contacts and Access

| Resource | Location |
|----------|----------|
| Registry (source of truth) | `meta-organvm/organvm-corpvs-testamentvm/repo-registry.json` |
| Governance rules | `meta-organvm/organvm-corpvs-testamentvm/governance-rules.json` |
| Orchestration workflows | `organvm-iv-taxis/orchestration-start-here/.github/workflows/` |
| Validation scripts | `meta-organvm/organvm-corpvs-testamentvm/scripts/` |
| Essays | `organvm-v-logos/public-process/_posts/` |
| Portfolio site | `4444J99/portfolio` (deploys to `4444j99.github.io/portfolio/`) |

**Authentication:** All `gh` CLI commands require GitHub authentication. The system uses HTTPS remotes with `gh auth` tokens. Org-wide tokens are stored in 1Password.

---

## What NOT to Do

- **Don't push directly to branch-protected repos** (e.g., `public-record-data-scrapper`) — use PRs
- **Don't push to archived repos** — they reject pushes by design
- **Don't re-enable disabled cron workflows** without checking billing first (see emergency procedures)
- **Don't modify `repo-registry.json` without running the audit afterward** — it's the single source of truth
- **Don't use `gh api` file-by-file pushes for bulk updates** — they create divergent remote commits. Use `git push` instead.
