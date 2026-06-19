# README Coverage Audit — 26 Repositories Missing READMEs

**Task:** LIMEN-094 — Audit 26 missing READMEs across 148 repos
**Issue:** [a-organvm/organvm-corpvs-testamentvm#387](https://github.com/a-organvm/organvm-corpvs-testamentvm/issues/387)
**Audit date:** 2026-06-18 (re-audit of a 2026-06-01 "Jules-ready batch" finding)
**Auditor:** Agent (LIMEN dispatch, worktree `limen-094-dd6f`)
**IRF entry:** IRF-SYS-256
**Predecessor:** IRF-SYS-055 (RESOLVED, 2026-04-02) — *"VACUUM: 29 repositories missing READMEs at GRADUATED status."*
**Source of truth:** `repo-registry.json` (schema v1.2.0)

---

## 1. Executive Summary

Of the **149 repository entries** in `repo-registry.json`, **122 carry a deployed README**
(`documentation_status` = `DEPLOYED` ×115 or `FLAGSHIP README DEPLOYED` ×7) and **27 do not**.
Exactly one of those 27 — `local/_portal` — is a local-only repo never pushed to GitHub, so
**across the 148 GitHub repos, 26 lack a deployed README**. This reconciles to the count in the
2026-06-01 audit that opened issue #387.

The audit's central finding is **not** that 26 repos are derelict. When the 26 are classified by
*why* they lack a deployed README, only **8 are genuine content gaps** that need an authored README.
The remaining 18 are accounted for by design:

| Class | Count | Nature | Action |
|-------|------:|--------|--------|
| **A — Compliant by design** | 12 | Org-profile `.github` repos (8) + intentional redirect stubs (4) | None / definitional |
| **B — Forks (inherit upstream README)** | 6 | `contrib--*` forks of external projects | Light contribution-context addendum |
| **C — Genuine content gaps** | 8 | SKELETON / MINIMAL / IN_PROGRESS first-party repos | **Author or expand README** |

The "26 missing" headline is therefore **largely a classification artifact of a presence-only scan**.
The actionable core is the 8 Class-C repos — of which **5 are public** (portfolio-visible) and should
be prioritized.

**Trend:** 29 missing (IRF-SYS-055, 2026-04-02) → 26 missing (this audit, 2026-06) — net 3 closed in ~2 months.

---

## 2. Scope & Methodology

### 2.1 What was audited
All repository entries in `repo-registry.json`, the system's single source of truth (CLAUDE.md
Invariant #1). Each entry carries a `documentation_status` field whose enum in practice is
`DEPLOYED | FLAGSHIP README DEPLOYED | INFRASTRUCTURE | SKELETON | MINIMAL | ACTIVE |
ARCHIVED — REDIRECT… | IN_PROGRESS`. A repo is treated as **lacking a deployed README** when its
status is anything other than `DEPLOYED` or `FLAGSHIP README DEPLOYED`.

### 2.2 Environment constraint (important)
This audit was executed inside a sandboxed LIMEN dispatch worktree with **no network egress** —
`gh`, `WebFetch`, and outbound HTTP were unavailable, and the live org clones under
`~/Workspace/<org>/` were outside the permitted working directory. **The audit is therefore
registry-based, not a live `git ls-files` of each GitHub repo.** This is sufficient to enumerate and
classify the 26, because the registry's `documentation_status` is the field the original 2026-06-01
audit also wrote against. It is **not** sufficient to detect *registry-vs-reality drift* (a repo
marked `DEPLOYED` whose `README.md` was since deleted on GitHub). §6 gives the exact command to run
that live cross-check when network is available; it should be run before this finding is closed.

### 2.3 Why registry status and live presence can disagree
`documentation_status` is a *planning-time claim*. A presence-only scan (`README.md` exists Y/N) and
this status field can diverge in both directions:
- **False positive of the scan:** `.github` repos and redirect stubs *have* a `README.md` on GitHub
  but are not "authored repo READMEs" — a naive scan that only checks status≠DEPLOYED flags them.
- **False negative of the registry:** a repo marked `DEPLOYED` whose README was later removed would
  pass this audit but fail a live scan. Only §6 catches this.

---

## 3. The Reconciliation Arithmetic

```
repo-registry.json entries carrying documentation_status ......... 149
  ├─ DEPLOYED .................................................... 115  ─┐ have README
  └─ FLAGSHIP README DEPLOYED ......................................  7  ─┘  (122)
  ── non-deployed ................................................. 27
        INFRASTRUCTURE (.github org-profile repos) ................  8
        ARCHIVED — REDIRECT TO metasystem-master ..................  4
        SKELETON ..................................................  5
        MINIMAL / minimal .........................................  3
        ACTIVE (contrib--* forks) .................................  6
        IN_PROGRESS ...............................................  1
  ── of the 27 non-deployed, local-only (not a GitHub repo) ....... -1   (local/_portal, SKELETON)
  ════════════════════════════════════════════════════════════════════
  GitHub repos missing a deployed README .......................... 26   ← matches issue #387
```

---

## 4. Findings — The 26 Repositories

Legend: **Class A** = compliant by design · **Class B** = fork (upstream README) · **Class C** = genuine gap

| # | Repo | Org | Registry status | Public | Class | Note |
|--:|------|-----|-----------------|:------:|:-----:|------|
| 1 | `.github` | organvm-i-theoria | INFRASTRUCTURE | ✓ | A | Org-profile / community-health repo |
| 2 | `.github` | organvm-ii-poiesis | INFRASTRUCTURE | ✓ | A | Org-profile / community-health repo |
| 3 | `.github` | organvm-iii-ergon | INFRASTRUCTURE | ✓ | A | Org-profile / community-health repo |
| 4 | `.github` | organvm-iv-taxis | INFRASTRUCTURE | ✓ | A | Org-profile / community-health repo |
| 5 | `.github` | organvm-v-logos | INFRASTRUCTURE | ✓ | A | Org-profile / community-health repo |
| 6 | `.github` | organvm-vi-koinonia | INFRASTRUCTURE | ✓ | A | Org-profile / community-health repo |
| 7 | `.github` | organvm-vii-kerygma | INFRASTRUCTURE | ✓ | A | Org-profile / community-health repo |
| 8 | `.github` | meta-organvm | INFRASTRUCTURE | ✓ | A | Org-profile / community-health repo |
| 9 | `core-engine` | organvm-ii-poiesis | ARCHIVED — REDIRECT | ✓ | A | Intentional redirect stub → `metasystem-master` |
| 10 | `performance-sdk` | organvm-ii-poiesis | ARCHIVED — REDIRECT | ✓ | A | Intentional redirect stub → `metasystem-master` |
| 11 | `example-generative-visual` | organvm-ii-poiesis | ARCHIVED — REDIRECT | ✓ | A | Intentional redirect stub → `metasystem-master` |
| 12 | `docs` | organvm-ii-poiesis | ARCHIVED — REDIRECT | ✗ | A | Intentional redirect stub → `metasystem-master` |
| 13 | `vigiles-aeternae--corpus-mythicum` | organvm-i-theoria | SKELETON | ✓ | **C** | Mythological research corpus; Vigiles ORGAN-I expression |
| 14 | `vigiles-aeternae--theatrum-mundi` | organvm-ii-poiesis | SKELETON | ✓ | **C** | Creative multiverse / RPG; Vigiles ORGAN-II expression |
| 15 | `vigiles-aeternae--agon-cosmogonicum` | meta-organvm | SKELETON | ✓ | **C** | Mythological governance sim; Vigiles franchise hub |
| 16 | `content-engine--asset-amplifier` | organvm-iii-ergon | SKELETON | ✓ | **C** | ORGAN-III commerce product skeleton (DONE-181 seed) |
| 17 | `render-second-amendment` | organvm-iii-ergon | MINIMAL | ✗ | **C** | ORGAN-III; minimal README |
| 18 | `materia-collider` | meta-organvm | MINIMAL | ✗ | **C** | Dissolution sink for 53 boilerplate repos (ORGAN-RESET) |
| 19 | `cvrsvs-honorvm` | meta-organvm | minimal | ✓ | **C** | Meta repo; minimal README |
| 20 | `hokage-chess` | 4444j99 | IN_PROGRESS | ✗ | **C** | Client engagement (Rob Bonavoglia); PERSONAL — see §5.3 |
| 21 | `contrib--ipqwery-ipapi-py` | organvm-iv-taxis | ACTIVE (fork) | ✗ | B | OSS-contribution fork; retains upstream README |
| 22 | `contrib--primeinc-github-stars` | organvm-iv-taxis | ACTIVE (fork) | ✗ | B | OSS-contribution fork; retains upstream README |
| 23 | `contrib--temporal-sdk-python` | organvm-iv-taxis | ACTIVE (fork) | ✗ | B | OSS-contribution fork; retains upstream README |
| 24 | `contrib--dbt-mcp` | organvm-iv-taxis | ACTIVE (fork) | ✗ | B | OSS-contribution fork; retains upstream README |
| 25 | `contrib--langchain-langgraph` | organvm-iv-taxis | ACTIVE (fork) | ✗ | B | OSS-contribution fork; retains upstream README |
| 26 | `contrib--anthropic-skills` | organvm-iv-taxis | ACTIVE (fork) | ✗ | B | OSS-contribution fork; retains upstream README |

> **Excluded (local-only, not among the 148 GitHub repos):** `local/_portal` (SKELETON). It is the
> 27th non-deployed entry; it is omitted from the GitHub-repo count of 26. It should still receive a
> README before it is pushed to a remote.

---

## 5. Remediation Classes

### 5.1 Class A — Compliant by design (12 repos) — *no README authoring required*
- **8 × `.github` org-profile repos.** A `.github` repo's "README" is the **org profile** rendered on
  the organization landing page (community-health inheritance — CLAUDE.md notes health files are
  "inherited org-wide via 8 `.github` repos"). These are infrastructure, not portfolio repos. A
  presence-only scan flags them only because their `documentation_status` is `INFRASTRUCTURE`, not
  `DEPLOYED`. **Recommendation:** confirm each org profile renders (§6 live check), then treat as
  out-of-scope for the README audit. Optionally add an `INFRASTRUCTURE` carve-out to the audit query
  so future runs don't re-flag them.
- **4 × redirect stubs** (`core-engine`, `performance-sdk`, `example-generative-visual`, `docs` in
  `organvm-ii-poiesis`). These were deliberately archived and point readers to `metasystem-master`.
  Their READMEs *exist* as redirect notices. **Recommendation:** none — this is the intended terminal
  state for an archived-redirect repo.

### 5.2 Class B — Forks inheriting upstream README (6 repos) — *light touch*
The `contrib--*` repos under `organvm-iv-taxis` are **forks of external open-source projects** created
to stage upstream contributions (e.g. the grafana/k6 work in IRF-OSS-042). A fork retains the
upstream project's README, so a strict "no README" scan would *not* flag these — they appear here only
because their `documentation_status` is `ACTIVE` (fork is live) rather than `DEPLOYED` (ORGANVM README
authored). **Recommendation:** do **not** overwrite the upstream README. Where useful, add a short
`CONTRIBUTING-ORGANVM.md` or a top-of-README ORGANVM banner explaining the fork's purpose and the
contribution status, then set `documentation_status` to a fork-aware value. Low priority; private repos.

### 5.3 Class C — Genuine content gaps (8 repos) — *the actionable batch*
These are first-party ORGANVM repos that genuinely need an authored or expanded README. This is the
"Jules-ready batch" the issue refers to.

| Repo | Status | Public | Priority | Rationale |
|------|--------|:------:|:--------:|-----------|
| `vigiles-aeternae--corpus-mythicum` | SKELETON | ✓ | **P1** | Public, portfolio-visible; flagship-adjacent Vigiles franchise |
| `vigiles-aeternae--theatrum-mundi` | SKELETON | ✓ | **P1** | Public; Vigiles franchise ORGAN-II expression |
| `vigiles-aeternae--agon-cosmogonicum` | SKELETON | ✓ | **P1** | Public; Vigiles franchise **hub**, sibling of this corpus in meta-organvm |
| `content-engine--asset-amplifier` | SKELETON | ✓ | **P1** | Public ORGAN-III commerce product; has a seeded skeleton (DONE-181) to expand |
| `cvrsvs-honorvm` | minimal | ✓ | **P2** | Public meta repo; expand minimal README |
| `render-second-amendment` | MINIMAL | ✗ | **P2** | Private ORGAN-III; expand minimal README |
| `materia-collider` | MINIMAL | ✗ | **P2** | Private; the dissolution sink for 53 boilerplate repos — README should document its role as the absorption zone |
| `hokage-chess` | IN_PROGRESS | ✗ | **P3** | Client engagement (PERSONAL); a portfolio README may be inappropriate — confirm client/visibility intent before authoring |

**Priority rule applied:** public repos outrank private (portfolio visibility, CLAUDE.md Invariant #5
— "every README is a portfolio piece"). The **5 public Class-C repos** are the highest-value targets;
the 3 private repos follow; `hokage-chess` is gated on a client/visibility decision.

---

## 6. Live-Verification Appendix (run before closing #387)

This audit is registry-based. To confirm against live GitHub state and catch any registry-vs-reality
drift (a `DEPLOYED` repo whose README was deleted), run — from an environment with `gh` and network —
a presence check across all repos. Example sketch:

```bash
# For each repo in repo-registry.json, check whether README.md exists on the default branch.
python3 - <<'PY'
import json, subprocess
reg = json.load(open('repo-registry.json'))
for organ in reg['organs'].values():
    for r in organ.get('repositories', []):
        slug = f"{r['org']}/{r['name']}"
        rc = subprocess.run(
            ['gh','api',f'repos/{slug}/contents/README.md','--silent'],
            capture_output=True)
        present = rc.returncode == 0
        claimed = r.get('documentation_status','')
        deployed = claimed in ('DEPLOYED','FLAGSHIP README DEPLOYED')
        if present != deployed:
            print(f"DRIFT  {slug:60s} live={'README' if present else 'NONE':6s}  registry={claimed}")
PY
```

Any line printed is **drift** that this sandboxed audit could not see. Reconcile `documentation_status`
to live state, then re-run the §3 arithmetic.

---

## 7. Recommendations

1. **Dispatch the Class-C batch (8 repos, 5 public first).** This is the genuine work. Each is a
   `README POPULATE`/`README REVISE` task (≈88K/50K TE per CLAUDE.md). Suitable for Jules dispatch
   (SPEC-024 cyclic dispatch) since the gap list is now explicit.
2. **Do not "fix" Class A or B by overwriting READMEs.** The `.github` profiles and redirect stubs are
   correct as-is; the `contrib--*` forks must keep their upstream README. Forcing a generated README
   here would *degrade* state and violate the no-back-edges / fork-integrity conventions.
3. **Tighten the audit definition.** A future README audit should subtract `INFRASTRUCTURE` and
   `ARCHIVED — REDIRECT*` classes up front and treat forks separately, so the headline number reflects
   *authorable* gaps (8), not presence-scan artifacts (26). Consider a registry field like
   `readme_audit_class: {authored|profile|redirect|fork-inherited|n-a}`.
4. **Run §6 before closing #387.** Registry-based enumeration is necessary but not sufficient; the live
   cross-check is what certifies the count and catches silent drift.
5. **Give `local/_portal` a README before it is pushed** (the excluded 27th entry).

---

## 8. Linkage

- **GitHub issue:** [a-organvm/organvm-corpvs-testamentvm#387](https://github.com/a-organvm/organvm-corpvs-testamentvm/issues/387)
- **IRF entry:** IRF-SYS-256 (this audit) — see `INST-INDEX-RERUM-FACIENDARUM.md`
- **Predecessor:** IRF-SYS-055 (RESOLVED 2026-04-02) — the prior "29 repositories missing READMEs at GRADUATED status" vacuum
- **Related:** IRF-SYS-053 (108 repos fail Logos symmetry), IRF-CND-018 / IRF-CND-030 (specific repos needing identity docs)
- **Methodology:** CLAUDE.md Invariants #1 (registry source of truth) & #5 (README as portfolio piece); SOP `document-audit-feature-extraction`
- **Source of truth:** `repo-registry.json` (schema v1.2.0)
