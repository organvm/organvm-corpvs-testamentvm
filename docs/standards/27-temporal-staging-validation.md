# 27: Temporal Staging for Governance Validation

**Date:** 2026-06-18
**Status:** ACTIVE — governs all automated governance verdicts that certify system state
**IRF:** IRF-RES-013 (P0, GOVERNANCE) · **GH:** [#342](https://github.com/a-organvm/organvm-corpvs-testamentvm/issues/342) · **Commission:** INQ-2026-013, Wave 2
**Motor:** Tarskian · **Sources:** SGO-2026-RP-02 §§5.1, 6.1; SGO-2026-SYN-02 §§3, 4.1, 5.2 (Goodhart-Campbell mathematical necessity)
**Complements:** `docs/memory/constitution.md` (Amendment J, LIM-I Incompleteness), `governance-rules.json` (`dependency_rules`), `scripts/soak-test-monitor.py` (collector that freezes capsules), `scripts/governance_validators.py` (shared rule logic)

---

## 1. The Principle in One Sentence

**Governance must always validate a *previous* state using the *current* rules — never the current state using itself.**

```
    validator(T)  judges  state(T-1)        ✅ temporal staging
    validator(T)  judges  state(T)          ❌ self-reference (Goodhart fixed point)
```

## 2. Why Self-Validation Is Not Validation

Before this refactor, the soak collector (`scripts/soak-test-monitor.py`) validated the
*current* registry against the *current* rules and wrote the verdict (`registry_pass: true`)
into the *same* daily snapshot. The generation that produced the state also certified it.

That arrangement is defective for a reason that is **mathematical, not operational**:

- **Tarski's undefinability theorem.** A formal language cannot contain its own truth
  predicate. The truth of statements in an object-language `L` can only be defined in a
  strictly higher metalanguage `L⁺`. A validator that judges its own contemporaneous
  output is asserting truth from inside `L` — which Tarski proved is impossible without
  contradiction. The verdict is not *wrong*; it is *undefined*.

- **Goodhart-Campbell collapse.** "When a measure becomes a target, it ceases to be a
  good measure." When the verdict (`pass`) and the target (current state being acceptable)
  are computed in the same tick from the same inputs, the measure and the target *fuse*.
  A `PASS` then conveys no information: of course the current rules accept the current
  state — the rules and the state co-evolved. The verdict is a fixed point, not a
  measurement (SYN-02 §3).

The practical failure this hides is **rule drift**: rules can quietly relax to keep
certifying whatever state exists, and self-validation will never notice, because there is
no independent tier to disagree.

## 3. The Tarskian Fix — Staging in Time

We cannot build an infinite tower of metalanguages, but we do not need to. **Time supplies
the hierarchy for free.** The state captured at `T-1` was produced *before* the rules in
force at `T` existed. Therefore the current rules are, with respect to that frozen state, a
strictly higher tier:

| Tier | Tarskian role | Concrete artifact |
|------|---------------|-------------------|
| Object language `L` | the state being judged | the registry as it was at `T-1`, frozen in a **state capsule** |
| Metalanguage `L⁺` | the truth predicate | the **current** validators + **current** `governance-rules.json` at `T` |

Because `L⁺` is genuinely later than `L`, a `PASS` is informative again: it means "state
that existed yesterday still satisfies the rules as they stand today." A `FAIL` where the
state previously passed *under its own contemporaneous rules* is the **rule-drift signal** —
the two tiers disagree, and that disagreement is the whole point.

This is also the constitution's own logic (Amendment J, LIM-I): the law cannot fully
specify itself; judgment must come from a tier the specification does not contain. Temporal
staging is that tier, mechanized.

## 4. Mechanics

### 4.1 Freezing the object tier — the *state capsule*

A verdict (`pass`/`fail`) is not enough to re-validate; you need the *state*. The collector
now freezes a `state_capsule` into every daily snapshot — the validation-relevant projection
of the registry plus the governance version/digest then in force:

```json
"state_capsule": {
  "schema": 1,
  "registry_digest": "…",
  "governance_version": "3.0",
  "governance_digest": "…",
  "organs_present": ["ORGAN-I", "…", "META-ORGANVM"],
  "repo_count": 89,
  "repos": [ { "org": "…", "name": "…", "organ_key": "ORGAN-I",
              "implementation_status": "…", "documentation_status": "…",
              "dependencies": [ "…" ] } ]
}
```

The capsule contains **only what the rule-based validators consume** and **nothing
time-relative** (no CI status, no staleness, no engagement — those have no meaning when
re-run against the past).

### 4.2 Judging it from the current tier

`scripts/temporal-staging-validator.py check` performs the staging:

1. find the most recent *prior* snapshot carrying a capsule;
2. `reconstruct_registry()` rebuilds a registry-shaped object from it;
3. run the **current** `validate_registry` / `validate_dependencies` (+ current governance)
   against that previous state;
4. compare the temporal verdict to the snapshot's own contemporaneous self-verdict;
5. exit non-zero on **rule drift** (previously-passing state now fails).

### 4.3 One validator, two tenses

The rule-based checks live in **`scripts/governance_validators.py`** as the single source of
truth, imported by both the collector (current state) and the temporal validator (previous
state). This is not incidental: validating previous-with-current *requires* that the same
validator code be applied across the time gap. Had the logic been duplicated, the two tiers
could disagree for the wrong reason — a divergence between two copies of a check rather than
a real drift in the governed state.

## 5. Operating the Check

```bash
# Validate the most recent prior state under today's rules
python3 scripts/temporal-staging-validator.py check

# Stage strictly-earlier state on the same day a snapshot was written
python3 scripts/temporal-staging-validator.py check --before 2026-06-18

# Fail on ANY violation, not only on drift (strict gate for CI)
python3 scripts/temporal-staging-validator.py check --strict
```

**Verdicts:**

- `INSUFFICIENT_HISTORY` — no prior capsule exists yet (expected during bootstrap; exits 0).
  Capsules accumulate from the first collector run after this refactor.
- `PASS` — previous state satisfies current rules. If rules also changed since the snapshot,
  the validation is genuinely independent and the system is consistent across the change.
- `FAIL` + `rule_drift_detected: true` — state that certified itself at `T-1` fails today's
  rules. Investigate whether the rules tightened legitimately or the state regressed.

The report is written to `data/soak-test/temporal-staging-latest.json`.

## 6. What This Does and Does Not Claim

- It does **not** make governance complete (LIM-I still holds; semantic properties remain
  undecidable — see IRF-RES-007, "make incompleteness visible").
- It **does** remove one specific defect: the *self-referential* verdict whose `PASS`
  carried zero independent information.
- It is the structural precondition for IRF-RES-016 (Goodhart monitoring) and IRF-RES-053
  (strange-loop stability analysis), which depend on having an independent temporal tier to
  measure metric/outcome correlation against.

## 7. Bootstrapping Note

The first run after deployment will report `INSUFFICIENT_HISTORY` until at least one daily
snapshot carrying a `state_capsule` predates the check. From the second capsule-bearing
snapshot onward, every collector run leaves behind a re-validatable object tier, and the
temporal validator has a genuine `T-1` to judge.
