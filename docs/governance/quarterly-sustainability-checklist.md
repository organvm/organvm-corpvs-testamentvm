# Quarterly Sustainability Checklist

**Purpose:** Minimal viable audit for solo operator maintenance of 97 repos across 8 orgs
**Cadence:** Quarterly (Q2 2026 is first execution)
**Estimated effort:** 1-2 hours per quarter
**Source:** Doc 11 Priority 4 recommendation; simplified from `orchestration-system-v2.md` monthly spec

---

## Pre-Audit

- [ ] Note the date and quarter (e.g., "Q2 2026 — 2026-04-15")
- [ ] Confirm `repo-registry.json` is the working copy (not stale)

## 1. Registry Currency Check

- [ ] Run `python scripts/v3-registry-reconciliation.py` — confirm 0 missing repos, 0 extra repos
- [ ] Check for new repos created on GitHub not in registry: `gh api orgs/ORGNAME/repos --jq '.[].name'` for each org
- [ ] Verify `total_repos` count matches actual registry entries
- [ ] Spot-check 3 random repos: does GitHub description match registry description?

## 2. Broken Link Sweep

- [ ] Run `python scripts/v1-v2-link-tbd-audit.py` — note any new broken links
- [ ] Fix broken system links (highest priority)
- [ ] Triage external broken links (may be temporary outages)

## 3. Dependency Validation

- [ ] Run `python scripts/v4-dependency-validation.py` — confirm 0 violations
- [ ] Check for new dependencies added since last quarter

## 4. Constitution Gate Check

- [ ] Run `python scripts/v5-v6-constitution-organ-checks.py` — all 8 organs should PASS
- [ ] If any organ fails, investigate and fix before proceeding

## 5. CI Workflow Health

- [ ] Run the system-wide CI health query across all 8 orgs:
  ```bash
  for ORG in organvm-i-theoria organvm-ii-poiesis organvm-iii-ergon organvm-iv-taxis organvm-v-logos organvm-vi-koinonia organvm-vii-kerygma meta-organvm; do
    echo "=== $ORG ==="
    gh repo list "$ORG" --json name --jq '.[].name' | while read REPO; do
      RESULT=$(gh run list --repo "$ORG/$REPO" --limit 1 --json conclusion --jq '.[0].conclusion' 2>/dev/null)
      [ -n "$RESULT" ] && echo "  $REPO: $RESULT"
    done
  done
  ```
- [ ] Calculate CI pass rate: `passing / (passing + failing)` — target ≥ 95%
- [ ] For any failing repos: check if failure is a real code issue vs. stale workflow
- [ ] Verify `monthly-organ-audit.yml` has run at least once since last quarter
- [ ] Check for GitHub Actions deprecation warnings (Node.js version, action versions)
- [ ] ORGAN-I repos: verify all actions remain SHA-pinned (org policy requirement)

## 6. Content Freshness

- [ ] Are any essays outdated by project changes? (e.g., if a repo was archived that an essay references)
- [ ] Are flagship README word counts still ≥ 3,000? (spot-check 2-3)
- [ ] Has any flagship repo's code changed significantly without README update?

## 7. Promotion Obligation Status

- [ ] Query registry for `promotion_obligations` with `status: "PENDING"`:
  ```
  python3 -c "import json; [print(f'{r[\"org\"]}/{r[\"name\"]}: {o}') for org in json.load(open('repo-registry.json'))['organs'].values() for r in org['repositories'] for o in r.get('promotion_obligations', []) if o['status'] == 'PENDING']"
  ```
- [ ] For each PENDING obligation: is it still relevant? Should it be started, deferred, or cancelled?

## 8. Implementation Status Drift

- [ ] Run the implementation status distribution comparison:
  ```bash
  python3 -c "
  import json
  reg = json.load(open('repo-registry.json'))
  dist = reg.get('implementation_status_distribution', {})
  print('Current distribution:')
  for status, count in sorted(dist.items()):
      print(f'  {status}: {count}')
  print(f'  Total: {sum(dist.values())}')
  # Compare with previous quarter (update these baselines each quarter)
  baseline = {'ACTIVE': 90, 'ARCHIVED': 7}
  print('\\nDrift from baseline:')
  for status in sorted(set(list(dist.keys()) + list(baseline.keys()))):
      curr = dist.get(status, 0)
      prev = baseline.get(status, 0)
      delta = curr - prev
      arrow = '↑' if delta > 0 else '↓' if delta < 0 else '='
      print(f'  {status}: {prev} → {curr} ({arrow}{abs(delta)})')
  "
  ```
- [ ] Verify implementation status distribution matches expectations (87 ACTIVE, 10 ARCHIVED baseline)
- [ ] Have any ACTIVE repos degraded (dependencies outdated, tests failing)?
- [ ] Are the highest-portfolio-relevance repos maintaining code substance?

## Post-Audit

- [ ] Update `last_validated` dates in registry for any repos checked in detail
- [ ] Record audit results (pass/fail per section) in a dated entry below
- [ ] If critical issues found, create tracking items (registry notes or GitHub issues)

---

## Audit Log

| Quarter | Date | Operator | Result | Notes |
|---------|------|----------|--------|-------|
| Q2 2026 | TBD | @4444j99 | — | First quarterly audit |

---

## Scope Boundary

This checklist is intentionally minimal. It replaces the full monthly audit specification in `orchestration-system-v2.md` with a quarterly cadence appropriate for solo operation. If the project gains contributors, revisit the monthly spec.

Items explicitly excluded from this checklist (defer to when relevant):
- POSSE distribution metrics (no audience to measure yet)
- Community engagement tracking (ORGAN-VI not yet active)
- Framework extraction progress (deferred per D-06)
- Security audit of dependencies (add when code repos mature)
