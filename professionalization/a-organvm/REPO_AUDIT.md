# Track E Repo Audit: a-organvm

Issue: a-organvm/organvm-corpvs-testamentvm#488  
Audit date: 2026-06-18  
Doctrine: TRACK-E-PROFESSIONALIZATION-2026-06-11.md  
Packet used: STREAM-PROF-PACKET-2026-06-11.md. The requested 2026-06-12 packet was not present in session-meta.  
Scope: first rolling-scoreboard row for the current repository only.

## Scoreboard

| Metric | Count |
|---|---:|
| Repos audited | 1 |
| active | 1 |
| incubation | 0 |
| inquiry | 0 |
| archive | 0 |
| retired | 0 |
| professional | 0 |
| needs-polish | 1 |
| internal-only | 0 |
| archive verdict | 0 |

## Audit Rows

| Repo | Track B input | State | Surface verdict | Stranger-60s conclusion | Receipt |
|---|---|---|---|---|---|
| `a-organvm/organvm-corpvs-testamentvm` | `park` from activation audit #484 | `active` | `needs-polish` | This reads as a serious governance corpus and institutional control plane, but a stranger would notice stale public identity signals before trusting it as fully polished. | GH-488-PROF-2026-06-18-001 |

## a-organvm/organvm-corpvs-testamentvm

### Seven Questions

| Question | Answer |
|---|---|
| What is it? | The authoritative planning, governance, registry, audit, and knowledge corpus for the ORGANVM creative-institutional system. |
| Is it active? | Yes. The repo has current issue traffic, current soak-test data through 2026-06-18, and remains the production home for work registry, prompt registry, meta-documentation, and session-continuation artifacts. |
| Is it user-reachable? | Yes as a public GitHub documentation corpus and directory surface. It is not a packaged user application; "use" means navigate the corpus, run local audit scripts, and consult registry/governance artifacts. |
| Who owns it? | 4444J99 / a-organvm operationally; legacy repo-registry and docs still identify `meta-organvm` as the org alias/source. `.github/CODEOWNERS` names `@4444j99`. |
| What state is it in? | `active`. Track B parked it because it is not a shippable user product; Track E state remains active because it is a live corpus/control-plane artifact. |
| Why should it continue to exist? | It is the canonical control plane for registry truth, governance constraints, work tracking, prompt/session registries, and meta-system documentation consumed by the rest of the swarm. |
| What would a stranger think after 60 seconds? | This is substantial and intentionally governed, but the surface asks the reader to reconcile too many old names, stale counts, and mixed status/license signals. |

### 10-Second Identity Test

| Test | Result | Evidence |
|---|---|---|
| What is this? | Pass | README title and opening paragraph identify the eight-organ planning and governance corpus. |
| Who owns it? | Partial | CODEOWNERS exists, but README and registry split ownership between `a-organvm` current context and legacy `meta-organvm` links. |
| Why does it exist? | Pass | README purpose and Quick Navigation explain governance, registry, and corpus role. |
| Is it active? | Partial | Badges and README say active/launched, but `seed.yaml` still says `implementation_status: PRODUCTION` and `promotion_status: PUBLIC_PROCESS`; registry says `ACTIVE`/`GRADUATED`. |
| Can I use it? | Partial | Quick Navigation is useful, but there is no short "how to use this corpus today" path for non-build usage and scripts have no install/setup surface. |

### Surface Checklist

| Element | Status | Note |
|---|---|---|
| README | present, stale | Strong document, but stale repo counts and legacy org URLs reduce trust. |
| LICENSE | present, inconsistent | `LICENSE` is CC BY-SA 4.0; top badge also advertises MIT. |
| Screenshots | missing / low relevance | Not required for a documentation corpus, but no visual orientation surface exists. |
| Demo URL | partial | README links portfolio, directory, public-process, and ORGAN Meta; no single canonical public surface is marked as the live demo/entrypoint. |
| Installation | partial | Scripts exist, but there is no package setup or minimal local command path beyond scattered command references. |
| Status | present, inconsistent | Active/launched/status badges conflict with registry/seed terminology and Track B `park`. |
| Roadmap | present | README, docs/strategy, docs/operations, and IRF provide roadmap/work-queue surfaces. |
| Maintainer | partial | `.github/CODEOWNERS` names owner; README does not surface a maintainer line. |
| Contact | missing / partial | README footer links portfolio and system pages, but no explicit contact/support route is visible in the first surface. |

### Professionalization Findings

1. Canonical identity drift: current task and GitHub issue use `a-organvm`, while README, registry, locorum, seed, and badges still lean on `meta-organvm`.
2. Metric drift: README badges/opening mix 97, 148, and 149 repo counts; registry summary uses 148/145 language; a stranger cannot tell which count is current.
3. License drift: MIT badge and CC BY-SA license/badge coexist.
4. State drift: Track B `park`, repo-registry `ACTIVE`/`GRADUATED`, seed `PRODUCTION`/`PUBLIC_PROCESS`, and README `LAUNCHED` all describe different axes without a public reconciliation note.
5. Use-path gap: "not a source code repository" is clear, but there is no compact outsider path for what to do next if they want to use the corpus.

### Cursor

Last audited repo: `a-organvm/organvm-corpvs-testamentvm`  
Next suggested repo, adopting activation-audit #484 order: `a-organvm/public-record-data-scrapper`  
Failure notes: GitHub issue body was not available through local `gh`; issue #488 had no comments; session-meta did not contain the named 2026-06-12 PROF packet.
