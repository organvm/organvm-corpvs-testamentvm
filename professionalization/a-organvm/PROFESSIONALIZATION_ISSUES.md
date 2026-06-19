# Track E Professionalization Issues: a-organvm

Issue: a-organvm/organvm-corpvs-testamentvm#488  
Audit date: 2026-06-18  
Status: read-side ledger only. No README edits, PRs, releases, deploys, or issue closures were performed.

## Summary

| ID | Repo | Surface verdict | Priority | Issue |
|---|---|---|---|---|
| PROF-AORG-CORPVS-001 | `a-organvm/organvm-corpvs-testamentvm` | `needs-polish` | P0 | Canonical org and URL drift across `a-organvm` and `meta-organvm`. |
| PROF-AORG-CORPVS-002 | `a-organvm/organvm-corpvs-testamentvm` | `needs-polish` | P0 | Public metrics and repo counts are stale/inconsistent. |
| PROF-AORG-CORPVS-003 | `a-organvm/organvm-corpvs-testamentvm` | `needs-polish` | P1 | License surface advertises both MIT and CC BY-SA 4.0. |
| PROF-AORG-CORPVS-004 | `a-organvm/organvm-corpvs-testamentvm` | `needs-polish` | P1 | State terms are not reconciled for outsiders. |
| PROF-AORG-CORPVS-005 | `a-organvm/organvm-corpvs-testamentvm` | `needs-polish` | P2 | Maintainer/contact/use path is incomplete on the first public surface. |

## Issues

### PROF-AORG-CORPVS-001: Canonical org and URL drift

Surface verdict: `needs-polish`  
Recommended issue title: `PROFESSIONALIZATION: needs-polish - canonical org drift`  
Evidence: Current task and issue context use `a-organvm/organvm-corpvs-testamentvm`; README badges and links, `repo-registry.json`, `INST-INDEX-LOCORUM.md`, and `seed.yaml` still foreground `meta-organvm`.

Finding: A stranger cannot know whether `a-organvm` is the canonical home, a migration target, or an alias for the older meta-organvm namespace.

FORGE packet candidate:
- Decide and publish the canonical display string for the repo.
- Add one short canonical-location note to the README if redirects/aliases are intentional.
- Align `seed.yaml`, registry row, badges, and locorum references to that canonical statement.

### PROF-AORG-CORPVS-002: Public metrics and repo counts are stale/inconsistent

Surface verdict: `needs-polish`  
Recommended issue title: `PROFESSIONALIZATION: needs-polish - public metric drift`  
Evidence: README mixes 97, 148, and 149 repo claims; registry summary says total 148 while noting 145 registry entries.

Finding: The corpus advertises institutional scale, but contradictory counts make the scale look ungoverned.

FORGE packet candidate:
- Recompute current repo/org counts from the canonical registry.
- Replace all first-viewport README count claims with a single dated metric block.
- Leave historical counts only in timeline/history sections where dates are explicit.

### PROF-AORG-CORPVS-003: License surface advertises two licenses

Surface verdict: `needs-polish`  
Recommended issue title: `PROFESSIONALIZATION: needs-polish - license badge mismatch`  
Evidence: README top badge advertises MIT; the license file and later badge indicate CC BY-SA 4.0.

Finding: Licensing is a first-pass trust signal. Mixed licenses make reuse terms ambiguous.

FORGE packet candidate:
- Confirm intended license for corpus text, scripts, and generated data.
- Replace or split badges so text/data/code licensing is explicit.
- Add a short "Licensing" note if the repo intentionally uses multiple licenses.

### PROF-AORG-CORPVS-004: State terms are not reconciled for outsiders

Surface verdict: `needs-polish`  
Recommended issue title: `PROFESSIONALIZATION: needs-polish - state vocabulary reconciliation`  
Evidence: Track B says `park`; Track E assigns `active`; registry says `ACTIVE` and `GRADUATED`; `seed.yaml` says `PRODUCTION` and `PUBLIC_PROCESS`; README says `LAUNCHED` and active.

Finding: Each state can be legitimate on its own axis, but the first public surface does not explain the axes. A stranger may read `park` as abandoned even though the corpus is operationally active.

FORGE packet candidate:
- Add a small state-axis note to a governance/status surface, not necessarily the README first paragraph.
- Align seed metadata with current vocabulary or mark it as legacy.
- Cross-reference Track B activation state and Track E legibility state as separate axes.

### PROF-AORG-CORPVS-005: Maintainer/contact/use path is incomplete

Surface verdict: `needs-polish`  
Recommended issue title: `PROFESSIONALIZATION: needs-polish - maintainer contact and use path`  
Evidence: `.github/CODEOWNERS` names `@4444j99`; README footer links portfolio/system pages; CONTRIBUTING explains contribution workflow. No first-surface maintainer/contact line or compact "how to use this corpus" path is visible.

Finding: The corpus is navigable for an initiated operator, but an outsider still has to infer whether they should browse docs, run scripts, open issues, or start from a public site.

FORGE packet candidate:
- Add a maintainer/contact route to the first public surface or a clearly linked support file.
- Add a compact "Use this corpus" path: read, query registry, run audit command, open issue.
- Keep it factual and non-marketing; this is a governance corpus, not an app landing page.

## Issue Filing Note

No new GitHub `PROFESSIONALIZATION:` issue was opened from this session. The stream packet requires immediate duplicate search before filing; available tooling exposed issue comments but not issue search/list or the issue body. This ledger is the handoff artifact for a future duplicate-safe filing pass.
