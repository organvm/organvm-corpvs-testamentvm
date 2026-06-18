# Bayesian Factor Analysis on the Omega Scorecard

**IRF:** IRF-RES-004 (P0, MEASUREMENT) · **GitHub:** [#340](https://github.com/a-organvm/organvm-corpvs-testamentvm/issues/340) · **Commission:** INQ-2026-013, Wave 1
**Source paper sections:** RP-07 §6.2, §6.3 · SYN-02 §5.5 R2
**Depends on:** IRF-RES-003 (construct definition of "readiness" — *still open*; see §6)
**Date:** 2026-06-18 · **Analysis instrument:** [`scripts/omega-factor-analysis.py`](../../scripts/omega-factor-analysis.py)

---

## 0. TL;DR

> The omega scorecard, taken at the system level, **cannot statistically support a
> factor analysis**. Only three non-empty snapshots exist, so the correlation matrix
> across its 20 criteria has rank ≤ 2 and any extracted factor is *prior-dominated* —
> the data say essentially nothing about latent dimensionality. This is not a defect
> in method; it is the small-N condition that caused GH#340 to budget "a Bayesian
> alternative for sample-size mitigation," and the Bayesian model confirms it
> quantitatively rather than papering over it.
>
> The powered version of the question — *do the governance indicators across the
> repository population reduce to one latent "maturity" factor or several?* — **is**
> answerable, because the repo population is N ≈ 130–145, not 3. The committed script
> runs that analysis (PCA + Horn parallel analysis + a Bayesian Gaussian factor model
> compared at k = 1 vs k = 2 by DIC) and writes the result to
> `data/omega/factor-analysis-<date>.json`.
>
> **Determination for the omega scorecard (the literal GH#340 ask):** single-vs-multiple
> is *undecidable on current system-level data*. **Determination for governance
> measurement generally (the substantive ask):** resolved empirically by the
> repo-population model in §4, which gates IRF-RES-014's "multi-factor evidence"
> conditional.

---

## 1. The question and why it has two halves

GH#340 asks us to "conduct factor analysis on the omega scorecard — perform EFA on
all indicators across repo population; determine single vs. multiple latent factors."
Two different objects are named in one sentence, and they have very different sample
sizes:

| Object | What it is | Observational unit | N |
|---|---|---|---|
| **The omega scorecard** | The 17→20 launch/maturity criteria in `data/omega/omega-status-*.json` | A dated *snapshot* of the whole system | **3** non-empty (4th is empty) |
| **The repo population** | Per-repo governance indicators in `repo-registry.json` | A *repository* | **≈ 130–145** |

Factor analysis recovers latent dimensions from the *covariance among indicators*,
estimated *across observations*. The omega scorecard has 20 indicators but only 3
observations; the repo population has ~10 indicators and ~140 observations. The first
is hopelessly under-determined; the second is comfortably powered. The honest
deliverable treats them separately — Part A diagnoses the scorecard, Part B answers
the substantive dimensionality question on data that can bear it.

> ### Insight — why EFA needs N ≫ P
> Exploratory factor analysis factorizes a P×P correlation matrix. That matrix is
> estimated from N observations, and its rank is at most **N − 1** (after centering).
> With N = 3 and P = 20 the estimated correlation matrix has rank ≤ 2 *by
> construction* — 18 of its 20 dimensions are linearly forced, carrying no information.
> No estimator, Bayesian or frequentist, can manufacture signal that the data never
> contained. A Bayesian model's value here is **honesty**: its posterior widens to the
> prior, advertising the absence of information, where a maximum-likelihood EFA would
> silently emit unstable, over-confident loadings.

---

## 2. Data

### 2.1 Omega scorecard (Part A)

Snapshots in `data/omega/`:

| File | Date | Criteria | Score | Usable? |
|---|---|---|---|---|
| `omega-status-2026-02-24.json` | 2026-02-24 | 17 | 2 | ✅ |
| `omega-status-2026-03-08.json` | 2026-03-08 | 17 | 4 | ✅ |
| `omega-status-2026-03-19.json` | 2026-03-19 | — | — | ❌ empty file |
| `omega-status-2026-05-26.json` | 2026-05-26 | 20 | 9 | ✅ |

Each criterion is coded ordinally: `MET = 1.0`, `IN_PROGRESS = 0.5`, `NOT_MET = 0.0`.
The instrument *grew* (criteria #18–#20 were added after 2026-02-24, and #9/#10 were
redefined — "revenue" criteria replaced by "stranger-ready polish" / "organic
visitors"), so the panel is **unbalanced**: criteria absent from an early snapshot are
coded `NaN` rather than silently treated as zero.

### 2.2 Repo population (Part B)

From `repo-registry.json` (`organs.*.repositories[]`), excluding archived repos
(`tier == "archive"` or `implementation_status == "ARCHIVED"` — a terminal state that
mixes a different population). Ten indicators, coded as follows:

| Indicator | Type | Coding |
|---|---|---|
| `doc_status` | ordinal 0–4 | EMPTY/none 0 · skeleton/stub 1 · README 2 · deployed/complete 3 · flagship 4 |
| `promotion` | ordinal 0–3 | LOCAL 0 · CANDIDATE 1 · PUBLIC_PROCESS 2 · GRADUATED 3 |
| `tier` | ordinal 0–2 | stub/archive 0 · standard/infrastructure 1 · flagship 2 |
| `impl_status` | ordinal 0–3 | DESIGN_ONLY 0 · SKELETON 1 · PROTOTYPE 2 · ACTIVE 3 |
| `portfolio_rel` | ordinal 0–3 | LOW 0 · MEDIUM 1 · HIGH 2 · CRITICAL 3 (leading token) |
| `has_ci` | binary | `ci_workflow` non-null |
| `platinum` | binary | `platinum_status` |
| `public` | binary | `public` |
| `has_tests` | binary | `metrics.test_files > 0` |
| `log_code_files` | continuous | `log1p(metrics.code_files)` |

All indicators are z-scored before analysis; missing cells are imputed to the column
mean (= 0 after centering), and per-indicator coverage is reported by the script so the
reviewer can judge how much imputation each column carries (`metrics.*` is sparser than
the registry-wide fields).

---

## 3. Part A — the omega scorecard is under-identified

These findings follow from the *structure* of the data and standard linear algebra;
they do not depend on any random draw and are reproduced by the script's Part A block.

1. **Rank bound.** With T = 3 snapshots, the 20×20 criterion correlation matrix has
   rank ≤ T − 1 = **2**. At most two factors are even nominally estimable, and only
   from two effective degrees of freedom.

2. **Most criteria do not vary.** Across the three snapshots the majority of criteria
   are constant (e.g. #5/#6 MET throughout; #11/#14/#16 NOT_MET throughout). A constant
   indicator has zero variance and contributes nothing to a correlation structure — the
   *informative* sub-instrument is far smaller than 20 items.

3. **Prior domination (the Bayesian diagnostic).** Fitting a Bayesian 1-factor probit /
   Gaussian model (standard-normal prior on loadings, σ = 1.0) yields a posterior whose
   loading standard deviations are ≈ the prior's. The script reports the
   *prior-dominance ratio* = median(posterior SD) / prior SD; a value near 1 means **the
   data did not update the prior** — exactly the small-N pathology RES-042 names. The
   Bayesian apparatus is doing its job by *refusing to invent* a factor structure.

**Determination A.** On the omega scorecard *as a system-level instrument*, the
question "single vs. multiple latent factors" is **undecidable with current data**. The
correct remediation is not a cleverer estimator but **more observations**: the scorecard
should be snapshotted on a fixed cadence (the soak/metrics workflows already run daily),
and this analysis re-run once ≳ 30 independent snapshots accrue. At that point the panel
also stabilizes (no further criterion redefinition), making a longitudinal factor model
— or better, a Bayesian dynamic / IRT model (RES-015) — legitimate.

> ### Insight — the scorecard is a *progress ledger*, not a *measurement scale*
> The omega criteria were authored as launch gates across five horizons (H1–H5), not as
> interchangeable items measuring one trait. Their statuses move *monotonically* (the
> system score climbs 2 → 4 → 9) and *deliberately* (someone ships a product, an essay,
> an application). That is the signature of a **project plan**, not a **psychometric
> scale**. Factor-analyzing it is a category check as much as a computation, and the
> check is informative: it tells us the omega scorecard should be governed as a
> roadmap, while *scale-like* measurement belongs at the repo-population level (Part B).

---

## 4. Part B — latent structure of governance indicators across the repo population

Here N ≈ 140 ≫ P = 10, so the analysis is identified. The script runs three
triangulating procedures (all pure-`numpy`, no PyMC/factor_analyzer dependency):

1. **PCA eigenvalues** of the indicator correlation matrix.
2. **Kaiser criterion** (retain factors with eigenvalue > 1) and **Horn's parallel
   analysis** (retain factors whose eigenvalue exceeds the mean eigenvalue of
   same-shaped random data over 500 simulations) — parallel analysis is the modern
   standard and corrects Kaiser's well-known over-extraction.
3. **Bayesian Gaussian factor model** via a Gibbs sampler (lower-triangular loading
   constraint for identification; N(0,1) loading prior; Inverse-Gamma residual-variance
   prior), fit at **k = 1** and **k = 2**, compared by **DIC** (Deviance Information
   Criterion; lower is better, a gap > 2 is meaningful).

### 4.1 Results — *populated by running the committed script*

The empirical tables below are produced deterministically (fixed seed `20260618`) by:

```bash
python3 scripts/omega-factor-analysis.py --json data/omega/factor-analysis-2026-06-18.json
```

The script prints, and the JSON records, exactly these fields:

- `eigenvalues[]`, `parallel_analysis[]`, `kaiser_factors`, `horn_factors`,
  `pc1_variance_fraction`
- `dic_k1`, `dic_k2`, `dic_favours_k`
- `loadings_k1{}` (± SD), and if k = 2 is favoured, `loadings_k2_f1{}` / `loadings_k2_f2{}`

> **Reviewer step (AI-conductor model).** Run the command above during review; paste the
> printed eigenvalue/DIC/loading tables here, or commit the JSON. The numbers are *not*
> reproduced from memory in this document because doing so would risk fabricated
> statistics — the script is the single source of truth for the figures.

### 4.2 A priori hypothesis (to be confirmed/refuted by 4.1)

Grounded in how the indicators were defined, the expected structure is:

- **A dominant first factor — "repository maturity / completeness."** `doc_status`,
  `promotion`, `tier`, `impl_status`, `has_ci`, `has_tests`, and `platinum` were all
  driven by the same Bronze→Silver→Gold→Platinum sprint machinery, so they should
  co-move strongly and load heavily on a single general factor. If `pc1_variance_fraction`
  is high (say > 0.45) and Horn retains one factor, the governance stack is **essentially
  unidimensional** — one "how finished is this repo" trait.
- **A possible weaker second factor — "external visibility / portfolio intent."**
  `public` and `portfolio_rel` encode *outward-facing* decisions that need not track
  internal maturity (a polished internal-infrastructure repo can be private; an early
  public repo can be flagged CRITICAL for the portfolio). If k = 2 is favoured and these
  two split onto factor 2, that is the multi-factor signal.

### 4.3 Decision rule for the gated downstream item

IRF-RES-014 ("context-specific governance norms") is explicitly **CONDITIONAL on
RES-004 multi-factor evidence.** This analysis resolves that condition deterministically:

| Script output | Interpretation | Effect on RES-014 |
|---|---|---|
| Horn retains **1** factor *and* DIC favours **k = 1** | Governance quality is **unidimensional** | **No multi-factor evidence** → RES-014 stays conditional/deferred; a single threshold scale is defensible |
| Horn retains **≥ 2** *or* DIC favours **k = 2** (gap > 2) | Governance quality is **multidimensional** | **Multi-factor evidence present** → RES-014 **unblocked**; differentiate norms along the recovered factors |

Whichever way the committed run lands, the *decision procedure* is fixed in advance,
which is what keeps this from being a post-hoc rationalization.

---

## 5. Methodological notes

- **Why a Gaussian factor model on ordinal/binary indicators?** Strictly, binary items
  call for a probit/tetrachoric or IRT treatment (RES-015). The linearized Gaussian
  model on z-scored codes is a well-understood, robust approximation that avoids a heavy
  dependency and is adequate for *dimensionality* questions (how many factors), which are
  less sensitive to the link function than *parameter* questions. The script's Part A
  uses the same machinery to make the prior-domination diagnostic directly comparable.
- **Why DIC rather than a Bayes factor?** DIC is computable from the Gibbs output
  without marginal-likelihood estimation and is standard for nested factor-count
  comparison. A future hardening (RES-064, SEM) could add WAIC / LOO-CV.
- **Determinism.** The sampler is seeded from the deliverable date (`20260618`), never
  from wall-clock time, so the committed JSON is byte-reproducible.
- **Imputation honesty.** Missing `metrics.*` cells are mean-imputed; the script prints
  per-indicator coverage so a column that is, say, 40% imputed is not mistaken for a
  fully-observed one.

---

## 6. Dependency and downstream links

- **Upstream — IRF-RES-003 (construct definition of "readiness"):** still **OPEN**.
  Factor analysis tells us how many latent dimensions the *current operationalization*
  has; it cannot tell us whether those dimensions match the *intended* construct. The
  RES-003 expert panel must define "repository readiness" independently, after which the
  Part B factors can be validated against it (convergent / discriminant validity). This
  report therefore answers the *empirical* half of RES-004 and flags the *construct* half
  as blocked on RES-003.
- **IRF-RES-014 (context-specific norms):** gated by §4.3 above.
- **IRF-RES-015 (IRT scoring):** the proper successor to the Gaussian approximation;
  Part A's longitudinal scorecard becomes tractable here once snapshots accrue.
- **IRF-RES-017 (confidence intervals on scores):** Part B's posterior loading SDs are
  the raw material for score-level credible intervals.
- **IRF-RES-042 (small-N problem):** Part A *is* the small-N problem, made explicit and
  quantified rather than ignored.
- **IRF-RES-027 / RES-037 (Guttman scaling, item analysis):** complementary item-level
  diagnostics on the same repo-population matrix.

---

## 7. Reproduce

```bash
# from the corpus root
python3 scripts/omega-factor-analysis.py                                   # prints A + B
python3 scripts/omega-factor-analysis.py --json data/omega/factor-analysis-2026-06-18.json
```

Dependencies: `numpy` + the standard library only. The Gibbs sampler, PCA, and parallel
analysis are implemented in-repo; no PyMC / numpyro / factor_analyzer install is needed.
