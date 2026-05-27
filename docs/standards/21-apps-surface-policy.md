# 21: Apps Surface Policy

**Date:** 2026-05-27
**Status:** ACTIVE — governs GitHub Apps installation on `${ORG_PERSONAL}` and `${ORG_SYSTEM}`
**Derived from:** 2026-05-27 audit revealing 30+ apps installed across 10 orgs with massive duplication (5× Semgrep, 4× redundant AI review bots, 7× dormant AI coding agents)
**Complements:** `17-branch-governance.md`, `19-two-org-consolidation-architecture.md`, `22-essence-function-naming-convention.md`

---

## 1. Purpose & Scope

The 2-org topology (per doc 19) collapses the apps surface from "installed per-org × 8–10" to "installed once per surviving org." This document specifies the **8 canonical app slots** (Class-(IV) in the four-class scheduling taxonomy) and the criteria for occupancy.

## 2. The 8 canonical slots

Each slot serves a distinct concern. The slot's identity is what it IS (a SAST scanner, a deploy target); the vendor in the slot is what currently fills the role.

| Env var | Slot purpose | Default vendor | Why this slot exists |
|---|---|---|---|
| `${APP_PRIMARY_AGENT}` | The AI agent the conductor actually uses | `claude` | Daily work loop |
| `${APP_DEPENDENCY_SCANNER}` | Security alerts + version updates for dependencies | `dependabot` (GitHub native) | Already free; 21 open alerts on corpvs as of 2026-05-27 |
| `${APP_PR_REVIEWER}` | Single AI review on every PR | `coderabbitai` | Established; per audit, was active in `organvm-i-theoria` (7 comments / 7 days) |
| `${APP_SAST_SCANNER}` | Static analysis for security issues | `semgrep-app` | Single install (replaces 5 redundant date-suffixed org-namespaced installations) |
| `${APP_SECRET_SCANNER}` | Detect committed secrets | `gitguardian` OR GitHub Secret Scanning | Pick one — GitHub-native costs $0; gitguardian has richer dashboard |
| `${APP_DEPLOY_TARGET}` | Primary deploy target for the flagship sites | `vercel` | Portfolio is on Vercel-class hosting |
| `${APP_CI_BUILDER}` | External CI/build runner (if needed) | `google-cloud-build` | Only if actively used; can be empty slot |
| `${APP_PROJECT_TRACKER}` | Project management surface | `linear-code` | Only if Linear is part of the active workflow |

## 3. Dormancy criteria

Per audit, an app is **DORMANT** if it has 0 PRs / 0 comments / 0 check-runs across all repos in `${ORG_SYSTEM}` for 30+ days.

Dormancy criteria are codified for the future `${ROUTINE_APPS_DORMANCY_WITNESS}` scheduled task (Class-(I)) to enumerate weekly:

```bash
# Pseudo-code for the witness routine
for app in $(gh api /orgs/${ORG_SYSTEM}/installations --jq '.installations[].app_slug'); do
  pr_count=$(gh search prs --author "app/$app" --owner ${ORG_SYSTEM} --created ">=$(date -v-30d)" --json url | jq 'length')
  comment_count=$(gh search prs --commenter "app/$app" --owner ${ORG_SYSTEM} --updated ">=$(date -v-30d)" --json url | jq 'length')
  if [ $pr_count -eq 0 ] && [ $comment_count -eq 0 ]; then
    echo "DORMANT: $app"
  fi
done
```

The witness reports; the conductor decides whether to uninstall.

## 4. Apps marked for migration (per 2026-05-27 audit)

**KEEP** on `${ORG_SYSTEM}` (and re-install if needed post-migration):

```
claude                                  → ${APP_PRIMARY_AGENT}
dependabot (GitHub native)              → ${APP_DEPENDENCY_SCANNER}
coderabbitai                            → ${APP_PR_REVIEWER}
semgrep-app (single install)            → ${APP_SAST_SCANNER}
gitguardian                             → ${APP_SECRET_SCANNER}
vercel                                  → ${APP_DEPLOY_TARGET}
google-cloud-build                      → ${APP_CI_BUILDER} (if active)
linear-code                             → ${APP_PROJECT_TRACKER} (if active)
renovate                                → (optional, redundant with dependabot for many use cases)
```

**UNINSTALL** (dormant per 7-day audit; safe to remove during migration):

```
chatgpt-codex-connector    (0 PRs in user's orgs)
chatgptbot                 (0 PRs in user's orgs)
gemini-code-assist         (0 PRs in user's orgs)
google-ai-studio           (assumed dormant)
google-labs-jules          (0 PRs in user's orgs — globally active on others' repos)
komment-ai                 (0 comments)
oz-by-warp                 (assumed dormant)
cursor                     (IDE-level, not org-level)
codacy-production          (redundant with semgrep + GitHub Code Scanning)
trunk-io                   (redundant with semgrep)
socket-security            (redundant with dependabot + gitguardian)
agentic-search             (assumed dormant)
llamapreview               (1 comment in audit window; drop in favor of coderabbit)
sourcery-ai                (audited active in 2 orgs; drop in favor of coderabbit)
qodo-free-for-open-source-projects  (drop in favor of coderabbit)
ivviiviivvi-semgrep-code-011226     (redundant Semgrep instance)
labores-crux-semgrep-011226         (redundant Semgrep instance)
omni-dromenon-semgrep-code-011226   (redundant Semgrep instance)
semgrep-code-ivviiviivvi            (redundant Semgrep instance — same as semgrep-app)
meta-organvm-cross-org              (custom; review whether still needed in 2-org topology)
docker                              (review if actively integrated)
```

That's ~21 apps to uninstall, ~9 to keep — net of the 8 canonical slots + 1 optional (renovate).

## 5. Apps that violate Section 2's "one slot per concern" rule

**3 PR review bots active simultaneously in organvm-i-theoria** (per audit: coderabbit=7, llama=6, sourcery=5 in 7 days). Per Universal Rule #29 ("never make the human look stupid"), a public PR with 3 AI bots dog-piling reduces credibility. Consolidation: keep one (`${APP_PR_REVIEWER}` = coderabbitai); uninstall the other two.

**5 Semgrep installations.** Single canonical install (`semgrep-app` at `${ORG_SYSTEM}` org level with `repository_selection: all`) replaces them all.

**6 AI coding agents installed.** Per audit, only `claude` is active in your orgs. Keep `${APP_PRIMARY_AGENT}=claude`; uninstall jules, codex, chatgpt, gemini, cursor, oz unless explicit decision to revive any.

## 6. New-app onboarding rule

Before installing a new app on `${ORG_SYSTEM}` or `${ORG_PERSONAL}`:

1. Identify which slot it fills (one of the 8 in Section 2, or propose adding a 9th slot)
2. If the slot is occupied, decide whether to swap vendors (uninstall current, install new) or skip
3. If it's a NEW slot, propose an env-var name (e.g., `APP_<PURPOSE>=<vendor>`) and add to `${CORPVS_ROOT}/.config/organvm.env`
4. Document the decision in IRF with the rationale
5. Install with `repository_selection: all` so it applies uniformly

Never install an app "to try it out" without slot-decision — that's how the 30+ accretion happened.

## 7. The `${ROUTINE_APPS_DORMANCY_WITNESS}` task (future)

Add to `${SCHED_TASKS_ROOT}/` as Class-(I) weekly routine. The witness:
- Enumerates installed apps via `gh api /orgs/<org>/installations`
- For each, counts 30-day activity (PRs, comments, check-runs)
- Classifies: ACTIVE (≥1 activity), DORMANT (0), or UNKNOWN
- Reports DORMANT list for conductor review

Not part of this session's autonomous landings; documented for Phase 7 of the doc-19 migration arc.

## 8. Cross-references

- `${DOC_TWO_ORG_ARCHITECTURE}` — the topology this policy assumes
- `${DOC_BRANCH_GOVERNANCE}` — apps interact with branch protection; coderabbit + dependabot may auto-merge per tier
- `${DOC_NAMING_CONVENTION}` — env-var slot naming follows essence-function
- Phase 2 of the migration arc (per doc 19 Section 5) is the work that lands this policy
