# Plan: Universal Repository Directory-Structure Standard

**Date:** 2026-05-29
**Scope:** organvm-corpvs-testamentvm (standards corpus) + downstream 148-repo rollout
**Trigger:** Conductor pasted an external research report ("Repository Directory Structure: Universal Principles…") and directed: *"review and implement universally; exploring, planning, implementing and then verify."*
**Phase model:** EXPLORE ✅ → PLAN (this doc) → IMPLEMENT → VERIFY

---

## 1. What the conductor asked

Do all five of: **(t)** treat-as-spec & restructure a repo, **(e)** evaluate/critique, **(v)** voice/quality pass, **(s)** save durably, **(f)** fact-check — **then** review and implement the principles **universally**, across explore→plan→implement→verify.

## 2. EXPLORE findings (verified against disk, not memory)

- **Not greenfield.** A repository standard already exists: `docs/standards/10-repository-standards.md` (14,990 B, 2026-02-09). 25 numbered standards docs total.
- `#10` covers **root hygiene · README tiers · community-health · badges · curation/visibility**. It is **nearly silent on internal layout** — exactly the research doc's strength.
- **No substantive conflict** with `21-apps-surface-policy.md` — that doc governs *GitHub Apps (bots)*, not `apps/` monorepo dirs. (Terminology-collision risk only — must disambiguate.)
- **Two reconciliations required** vs. existing corpus:
  - Research recommends **Diátaxis** for `docs/`; corpus runs the **Logos tetrad** (doc `#14`). Different layers — coexist, don't replace.
  - Research recommends generic **short lowercase names**; corpus enforces **`[organ]-[type]--[name]` essence-function** (doc `#22`). Corpus convention wins inside the organ system.
- `registry-v2.json` (repo root) is the machine-readable source of truth → the substrate to drive any universal sweep.

## 3. Fact-check verdicts (f)

- **Google "2B LOC / 86 TB / 9M files" — CONFIRMED** (CACM 2016, Potvin & Levenberg; corroborated 2015 reporting). Keep the doc's Jan-2015-snapshot caveat.
- **Octoverse "3× profile visits" — UNVERIFIABLE.** Targeted searches failed to surface it. Recommendation: cut or downgrade to "anecdotal," do not cite Octoverse as primary.

## 4. Evaluation summary (e)

Accuracy strong; one empirical claim unverifiable; minor coherence flaw (conflates the orthogonal `src/`-vs-flat and `apps/`-split axes); ~70% directly adoptable, ~30% needs reconciliation vs `#14/#16/#22`. Full rubric in session response.

## 5. The scope fork — "implement universally" has two senses

- **(A) Codify-and-enforce (governance sense).** Author additive standard `#26` (internal layout) complementing `#10`; reconcile Diátaxis↔Logos and naming↔`#22`; update `#10` compliance checklist + `github-repository-standards` skill; (optionally) a `build-contract`-style lint. **Safe, reversible (git), in-scope, IS the universal artifact in a governance system.** → DO NOW.
- **(B) Physically restructure N repos.** Rewrite directory layouts to conform. **Irreversible-ish, outward-facing, per-repo push auth, multi-session.** → Requires explicit authorization + a **pilot** before any sweep (research doc itself recommends pilot-then-rollout).

## 6. IMPLEMENT plan

1. **(s)** Save research doc → `docs/research/2026-05-29-repository-directory-structure-conventions.md` with provenance header + fact-check + eval editorial note.
2. **(A)** Author `docs/standards/26-internal-directory-layout--monorepo-feature-organization.md` (additive; cross-refs `#10/#14/#16/#21/#22`; disambiguates apps/ vs Apps-surface; reconciles Diátaxis↔Logos; precedence appendix).
3. **(A)** Add cross-reference pointer in `#10` appendix (single additive line — no rewrite, honors no-deletion `#23`).
4. **(t / B-pilot)** Restructure ONE pilot repo to conform + VERIFY → template for sweep. **Awaiting conductor: which repo + push authorization.**
5. **(v)** Voice pass on the research doc / standard only if it's headed for publication — offer, don't assume.

## 7. VERIFY plan

- Standard `#26` lints clean against `build-contract --check` (naming/ratio).
- Pilot repo: `git status` clean, tests pass (if any), structure matches `#26`, README/health intact, pushed with parity 0/0.
- registry-v2.json entry for pilot annotated with conformance.

## 8. Authorization gates (held)

- Push to `a-organvm/organvm-corpvs-testamentvm` (public ORGANVM) — **needs per-session conductor auth.**
- Any physical repo restructure (B) — **needs explicit go + pilot-repo selection.**

## 9. Closure

Closes on: `#26` committed + pushed, `#10` cross-ref added, research doc saved, pilot restructured+verified+pushed, registry annotated. File DONE-NNN + IRF row at closeout.

---

## STATUS: EXECUTED (2026-05-29)

All planned work complete + propagated.

- **Standard `#26`** authored + `#10` cross-linked; research doc saved (`docs/research/2026-05-29-repository-directory-structure-conventions.md`, restored to full fidelity).
- **Generative mechanism** built: `scripts/audit-directory-layout.py` (+ `remediate-`, `declutter-`), calibrated to `#26`'s actual text.
- **Fleet sweep: 63 → 0 violations** (103 clean, 4 exempt). 46 repos README/LICENSE; 9 decluttered; `classroom-rpg-aetheria` 46-component migration `tsc`-verified (0 regression).
- **Propagated:** corpvs commits `09e76ed → 7d0f07e` pushed; 43 fleet repos pushed; PRs classroom-rpg #131, stakeholder-portal #55; 6 active repos held (commits safe-local).
- **Evidence:** ledger `docs/research/2026-05-29-layout-tech-debt-ledger.md`; closeout `.claude/plans/2026-05-29-closeout-universal-layout-sweep.md`.

No DONE-NNN allocated (cross-org fleet work, not a single corpvs IRF item); closure evidenced by the zero-violation report + push parity above.



## Index-line detail folded in from MEMORY.md (2026-06-01 trim)

- corpvs main was empirically UNPROTECTED (HTTP 404) — the push-auth ceremony guards nothing there, yet the harness classifier still gated it once on ambiguous consent.
- The earlier `growth-auditor` violation count was a colocated-test counting artifact (not real layout debt); the auditor was recalibrated to #26's actual text: discretionary-only root-clutter, distinct-component count, framework/native/cache pruning, vendored/declaration/static-site carve-outs.
- 6 repos HELD per "unless active currently": 5 active feature branches carrying others' WIP + digital-income rebase-conflict — commits left safe-local, not pushed.
