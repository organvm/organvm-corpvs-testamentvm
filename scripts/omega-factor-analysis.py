#!/usr/bin/env python3
"""Bayesian factor analysis on the omega scorecard and the repo population.

IRF-RES-004 / GH#340 (commission INQ-2026-013, Wave 1).

The omega scorecard is a *system-level* instrument: it is regenerated as a single
20-criterion snapshot, and only three non-empty snapshots exist
(``data/omega/omega-status-*.json``). With N=3 observations on P=20 indicators a
classical EFA is non-identified -- the sample correlation matrix has rank <= N-1 = 2,
so any extracted factor is prior-dominated. This is exactly the "small-N problem"
that motivated budgeting a Bayesian alternative for RES-004.

This script therefore does two things:

  PART A -- Omega scorecard (system-level, longitudinal). Quantify the
  under-identification: rank of the criterion correlation matrix, and the degree
  to which a Bayesian 1-factor posterior is dominated by its prior (posterior SD
  of the loadings relative to the prior SD). The finding is methodological: the
  current scorecard data CANNOT distinguish single vs. multiple latent factors.

  PART B -- Repo population (cross-sectional, well-powered). Code the per-repo
  registry indicators (documentation status, promotion status, tier, CI presence,
  tests, code volume, visibility, ...) into an N(~145) x P matrix where a factor
  model is actually identified. Run (1) a frequentist PCA triangulation
  (eigenvalues, Kaiser, Horn parallel analysis) and (2) a Bayesian Gaussian factor
  model via Gibbs sampling for k=1 and k=2 factors, comparing them by DIC. This
  answers the substantive question -- single vs. multiple latent quality factors --
  on data that can actually support an answer.

Dependencies: numpy + the standard library only. The Gibbs sampler is implemented
directly so no PyMC/numpyro/factor_analyzer install is required.

Usage:
    python3 scripts/omega-factor-analysis.py            # prints summary
    python3 scripts/omega-factor-analysis.py --json OUT  # also writes results JSON
"""
from __future__ import annotations

import argparse
import glob
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 20260618  # deterministic: derived from the deliverable date, not Date.now()


# --------------------------------------------------------------------------- #
# Data loading                                                                #
# --------------------------------------------------------------------------- #
STATUS_CODE = {"MET": 1.0, "IN_PROGRESS": 0.5, "NOT_MET": 0.0}


def load_omega_snapshots():
    """Return (dates, criterion_names, matrix) for non-empty omega snapshots.

    matrix is (T snapshots) x (P criteria), coded MET=1 / IN_PROGRESS=0.5 /
    NOT_MET=0. Criteria are keyed by id; criteria absent from an early snapshot
    (the scorecard grew 17 -> 20) are recorded as NaN so they can be handled
    explicitly rather than silently imputed.
    """
    paths = sorted(glob.glob(os.path.join(ROOT, "data", "omega", "omega-status-*.json")))
    snaps = []
    for p in paths:
        try:
            with open(p) as fh:
                d = json.load(fh)
        except (ValueError, OSError):
            continue
        crit = d.get("criteria")
        if not crit:
            continue  # empty snapshot (e.g. 2026-03-19)
        snaps.append((os.path.basename(p), d))
    # union of criterion ids -> name
    ids = []
    names = {}
    for _, d in snaps:
        for c in d["criteria"]:
            cid = c["id"]
            if cid not in names:
                ids.append(cid)
                names[cid] = c["name"]
    ids.sort()
    dates = []
    rows = []
    for fname, d in snaps:
        dates.append(fname.replace("omega-status-", "").replace(".json", ""))
        by_id = {c["id"]: c for c in d["criteria"]}
        row = []
        for cid in ids:
            c = by_id.get(cid)
            if c is None:
                row.append(np.nan)
            else:
                row.append(STATUS_CODE.get(c.get("status"), np.nan))
        rows.append(row)
    return dates, [names[i] for i in ids], np.array(rows, dtype=float)


def _iter_repos(registry):
    organs = registry.get("organs", {})
    for org in organs.values():
        for r in org.get("repositories", []):
            yield r


def _ord_doc(s):
    s = (s or "").upper()
    if not s or "EMPTY" in s or s == "NONE":
        return 0.0
    if "FLAGSHIP" in s:
        return 4.0
    if "DEPLOYED" in s or "COMPLETE" in s:
        return 3.0
    if "SKELETON" in s or "STUB" in s or "MINIMAL" in s:
        return 1.0
    return 2.0  # has a README of some kind


def _ord_promotion(s):
    return {"LOCAL": 0.0, "CANDIDATE": 1.0, "PUBLIC_PROCESS": 2.0, "GRADUATED": 3.0}.get((s or "").upper(), np.nan)


def _ord_tier(s):
    return {"stub": 0.0, "archive": 0.0, "standard": 1.0, "infrastructure": 1.0, "flagship": 2.0}.get((s or "").lower(), np.nan)


def _ord_impl(s):
    return {"DESIGN_ONLY": 0.0, "SKELETON": 1.0, "PROTOTYPE": 2.0, "ACTIVE": 3.0}.get((s or "").upper(), np.nan)


def _ord_portfolio(s):
    s = (s or "").upper()
    for tok, v in (("CRITICAL", 3.0), ("HIGH", 2.0), ("MEDIUM", 1.0), ("LOW", 0.0)):
        if s.startswith(tok) or (tok + " ") in s or (tok + "-") in s or (tok + ",") in s:
            return v
    return np.nan


INDICATORS = [
    "doc_status", "promotion", "tier", "impl_status",
    "portfolio_rel", "has_ci", "platinum", "public",
    "has_tests", "log_code_files",
]


def load_repo_matrix():
    """Return (indicator_names, repo_names, X) for the repo population.

    Archived repos (tier archive / implementation ARCHIVED) are excluded -- they
    are a terminal state that mixes a different population. Missing cells are NaN;
    standardization later imputes them to the column mean (=0 after centering).
    """
    with open(os.path.join(ROOT, "repo-registry.json")) as fh:
        reg = json.load(fh)
    repo_names, rows = [], []
    for r in _iter_repos(reg):
        tier = (r.get("tier") or "").lower()
        impl = (r.get("implementation_status") or "").upper()
        if tier == "archive" or impl == "ARCHIVED":
            continue
        m = r.get("metrics", {}) or {}
        code_files = m.get("code_files")
        test_files = m.get("test_files")
        row = [
            _ord_doc(r.get("documentation_status")),
            _ord_promotion(r.get("promotion_status")),
            _ord_tier(r.get("tier")),
            _ord_impl(r.get("implementation_status")),
            _ord_portfolio(r.get("portfolio_relevance")),
            1.0 if r.get("ci_workflow") else 0.0,
            1.0 if r.get("platinum_status") else 0.0,
            1.0 if r.get("public") else 0.0,
            (1.0 if (test_files or 0) > 0 else 0.0) if test_files is not None else np.nan,
            math.log1p(code_files) if isinstance(code_files, (int, float)) else np.nan,
        ]
        repo_names.append(f"{r.get('org','?')}/{r.get('name','?')}")
        rows.append(row)
    return INDICATORS, repo_names, np.array(rows, dtype=float)


# --------------------------------------------------------------------------- #
# Standardization + classical triangulation                                   #
# --------------------------------------------------------------------------- #
def standardize(X):
    """Z-score columns, imputing NaN to the column mean. Returns (Z, coverage)."""
    Z = X.copy()
    coverage = []
    for j in range(Z.shape[1]):
        col = Z[:, j]
        obs = col[~np.isnan(col)]
        coverage.append(len(obs) / len(col))
        mu = obs.mean() if len(obs) else 0.0
        sd = obs.std(ddof=1) if len(obs) > 1 else 1.0
        sd = sd if sd > 1e-9 else 1.0
        col = np.where(np.isnan(col), mu, col)
        Z[:, j] = (col - mu) / sd
    return Z, np.array(coverage)


def pca_eiguals(Z):
    """Eigenvalues of the correlation matrix (PCA), descending."""
    R = np.corrcoef(Z, rowvar=False)
    R = np.nan_to_num(R, nan=0.0)
    np.fill_diagonal(R, 1.0)
    vals = np.linalg.eigvalsh(R)
    return np.sort(vals)[::-1], R


def parallel_analysis(Z, n_iter=500, rng=None):
    """Horn's parallel analysis: mean eigenvalues of random data of the same shape.

    A factor is retained if its observed eigenvalue exceeds the random mean.
    """
    rng = rng or np.random.default_rng(SEED)
    n, p = Z.shape
    acc = np.zeros(p)
    for _ in range(n_iter):
        Rr = np.corrcoef(rng.standard_normal((n, p)), rowvar=False)
        Rr = np.nan_to_num(Rr, nan=0.0)
        np.fill_diagonal(Rr, 1.0)
        acc += np.sort(np.linalg.eigvalsh(Rr))[::-1]
    return acc / n_iter


# --------------------------------------------------------------------------- #
# Bayesian Gaussian factor model via Gibbs sampling                           #
# --------------------------------------------------------------------------- #
def gibbs_factor(Z, k, n_iter=4000, burn=1000, prior_sd=1.0, rng=None):
    """Gibbs sampler for X_i = Lambda f_i + eps_i, f_i ~ N(0,I_k), eps_ij ~ N(0,psi_j).

    Identification: lower-triangular Lambda (Lambda[j,l]=0 for l>j) with the
    leading k x k block constrained, the standard Bayesian-EFA constraint.
    Priors: Lambda_jl ~ N(0, prior_sd^2); psi_j ~ InvGamma(a0, b0).
    Returns a dict of posterior summaries including a DIC for model comparison.
    """
    rng = rng or np.random.default_rng(SEED)
    n, p = Z.shape
    a0, b0 = 1.0, 1.0
    # lower-triangular mask: free where j >= l
    mask = np.array([[1.0 if j >= l else 0.0 for l in range(k)] for j in range(p)])
    Lam = np.zeros((p, k))
    Lam[mask.astype(bool)] = 0.1
    psi = np.ones(p)
    F = rng.standard_normal((n, k))

    lam_draws, psi_draws, dev_draws = [], [], []
    prior_prec = 1.0 / (prior_sd ** 2)

    def deviance(Lam, psi):
        # -2 * sum log N(x_i | 0, Sigma), Sigma = Lam Lam' + diag(psi)
        Sigma = Lam @ Lam.T + np.diag(psi)
        sign, logdet = np.linalg.slogdet(Sigma)
        Sinv = np.linalg.inv(Sigma)
        quad = np.einsum("ij,jk,ik->", Z, Sinv, Z)
        return n * (p * math.log(2 * math.pi) + logdet) + quad

    for it in range(n_iter):
        # --- sample factor scores F | Lam, psi, Z ---
        Psi_inv = 1.0 / psi
        V = np.linalg.inv(np.eye(k) + (Lam.T * Psi_inv) @ Lam)
        M = Z @ (Psi_inv[:, None] * Lam) @ V
        L = np.linalg.cholesky(V)
        F = M + rng.standard_normal((n, k)) @ L.T
        # --- sample loadings Lam_j | F, psi_j, Z_j (respect triangular mask) ---
        for j in range(p):
            free = np.where(mask[j] > 0)[0]
            if len(free) == 0:
                continue
            Fj = F[:, free]
            prec = (Fj.T @ Fj) / psi[j] + prior_prec * np.eye(len(free))
            cov = np.linalg.inv(prec)
            mean = cov @ (Fj.T @ Z[:, j]) / psi[j]
            Lam[j, free] = mean + rng.standard_normal(len(free)) @ np.linalg.cholesky(cov).T
        # --- sample residual variances psi_j ---
        resid = Z - F @ Lam.T
        a_n = a0 + n / 2.0
        b_n = b0 + 0.5 * np.sum(resid ** 2, axis=0)
        psi = b_n / rng.gamma(a_n, size=p)  # InvGamma via 1/Gamma(rate=b_n)... see note
        # NB: rng.gamma uses shape=a_n, scale=1; InvGamma(a,b) sample = b / Gamma(a,1)
        psi = np.maximum(psi, 1e-6)
        if it >= burn:
            lam_draws.append(Lam.copy())
            psi_draws.append(psi.copy())
            dev_draws.append(deviance(Lam, psi))

    lam_draws = np.array(lam_draws)
    psi_draws = np.array(psi_draws)
    dev_draws = np.array(dev_draws)
    lam_mean = lam_draws.mean(axis=0)
    lam_sd = lam_draws.std(axis=0)
    # DIC = 2*mean(deviance) - deviance(posterior mean)
    dbar = dev_draws.mean()
    dhat = deviance(lam_mean, psi_draws.mean(axis=0))
    pD = dbar - dhat
    dic = dbar + pD
    # proportion of variance explained per factor (from posterior-mean loadings)
    comm = (lam_mean ** 2).sum(axis=0)  # column sums of squared loadings
    total_var = comm.sum() + psi_draws.mean(axis=0).sum()
    return {
        "k": k,
        "lam_mean": lam_mean,
        "lam_sd": lam_sd,
        "psi_mean": psi_draws.mean(axis=0),
        "dic": float(dic),
        "pD": float(pD),
        "dbar": float(dbar),
        "var_per_factor": comm,
        "prop_var_per_factor": comm / total_var,
        "n_draws": len(lam_draws),
    }


# --------------------------------------------------------------------------- #
# Reporting                                                                    #
# --------------------------------------------------------------------------- #
def section(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="write machine-readable results to this path")
    ap.add_argument("--iter", type=int, default=4000)
    ap.add_argument("--burn", type=int, default=1000)
    args = ap.parse_args()
    rng = np.random.default_rng(SEED)
    out = {"seed": SEED, "irf": "IRF-RES-004", "gh": 340}

    # ----- PART A: omega scorecard --------------------------------------- #
    section("PART A -- Omega scorecard (system-level, longitudinal)")
    dates, crit_names, M = load_omega_snapshots()
    T, P = M.shape
    print(f"non-empty snapshots T = {T}: {dates}")
    print(f"criteria P = {P}")
    # variance per criterion across snapshots; constant criteria carry no info
    var = np.nanvar(M, axis=0)
    n_varying = int((var > 1e-9).sum())
    print(f"criteria that ever change across snapshots: {n_varying}/{P}")
    # correlation rank: bounded by T-1
    Za, cov_a = standardize(M)
    Ra = np.corrcoef(Za, rowvar=False)
    Ra = np.nan_to_num(Ra, nan=0.0)
    rank = int(np.linalg.matrix_rank(Ra, tol=1e-8))
    print(f"rank(correlation matrix) = {rank}  (upper bound for #identifiable factors; T-1 = {T-1})")
    # Bayesian 1-factor: measure prior dominance
    bay_a = gibbs_factor(Za, k=1, n_iter=args.iter, burn=args.burn, prior_sd=1.0, rng=rng)
    median_post_sd = float(np.median(bay_a["lam_sd"]))
    print(f"Bayesian 1-factor: median posterior SD of loadings = {median_post_sd:.3f} "
          f"(prior SD = 1.000)")
    dominance = median_post_sd / 1.0
    print(f"prior-dominance ratio (posterior SD / prior SD) = {dominance:.2f}  "
          f"-> {'PRIOR-DOMINATED (data uninformative)' if dominance > 0.7 else 'data informative'}")
    print("CONCLUSION A: with T=3 snapshots the omega scorecard cannot statistically")
    print("distinguish single vs. multiple latent factors; any extracted structure")
    print("is the prior, not the data. (Re-run when >= ~30 snapshots accrue.)")
    out["part_a"] = {
        "snapshots": dates, "n_criteria": P, "n_varying": n_varying,
        "corr_rank": rank, "median_post_loading_sd": median_post_sd,
        "prior_dominance_ratio": dominance,
        "verdict": "under-identified; single-vs-multiple undecidable on current data",
    }

    # ----- PART B: repo population --------------------------------------- #
    section("PART B -- Repo population (cross-sectional, well-powered)")
    ind_names, repo_names, X = load_repo_matrix()
    Zb, coverage = standardize(X)
    N, Pb = Zb.shape
    print(f"repos N = {N}  indicators P = {Pb}")
    print("indicator coverage (fraction non-missing):")
    for nm, cov in zip(ind_names, coverage):
        print(f"  {nm:16s} {cov*100:5.1f}%")
    # frequentist triangulation
    eig, R = pca_eiguals(Zb)
    pa = parallel_analysis(Zb, n_iter=500, rng=rng)
    kaiser = int((eig > 1.0).sum())
    horn = int((eig > pa).sum())
    print("\nPCA eigenvalues (correlation matrix), with Horn parallel-analysis threshold:")
    for i, (e, p_) in enumerate(zip(eig, pa), 1):
        flag = " *" if e > p_ else ""
        print(f"  factor {i:2d}: eigenvalue = {e:5.2f}   PA-random = {p_:5.2f}{flag}")
    print(f"Kaiser criterion (eigenvalue > 1): {kaiser} factor(s)")
    print(f"Horn parallel analysis (eigenvalue > random): {horn} factor(s)")
    var_pc1 = float(eig[0] / eig.sum())
    print(f"first principal component explains {var_pc1*100:.1f}% of total variance")
    # Bayesian model comparison k=1 vs k=2
    bay1 = gibbs_factor(Zb, k=1, n_iter=args.iter, burn=args.burn, rng=rng)
    bay2 = gibbs_factor(Zb, k=2, n_iter=args.iter, burn=args.burn, rng=rng)
    print(f"\nBayesian factor model DIC:  k=1 -> {bay1['dic']:.1f}   k=2 -> {bay2['dic']:.1f}")
    better = 2 if bay2["dic"] < bay1["dic"] - 2 else 1
    print(f"DIC favours k = {better}  (lower is better; >2 difference is meaningful)")
    print("\nk=1 standardized loadings (posterior mean +/- SD):")
    order = np.argsort(-np.abs(bay1["lam_mean"][:, 0]))
    for j in order:
        print(f"  {ind_names[j]:16s} {bay1['lam_mean'][j,0]:+.2f} +/- {bay1['lam_sd'][j,0]:.2f}")
    if better == 2:
        print("\nk=2 standardized loadings (posterior mean), factor1 | factor2:")
        for j in range(Pb):
            print(f"  {ind_names[j]:16s} {bay2['lam_mean'][j,0]:+.2f} | {bay2['lam_mean'][j,1]:+.2f}")
    out["part_b"] = {
        "n_repos": N, "indicators": ind_names,
        "coverage": {nm: round(float(c), 3) for nm, c in zip(ind_names, coverage)},
        "eigenvalues": [round(float(e), 3) for e in eig],
        "parallel_analysis": [round(float(p_), 3) for p_ in pa],
        "kaiser_factors": kaiser, "horn_factors": horn,
        "pc1_variance_fraction": round(var_pc1, 3),
        "dic_k1": round(bay1["dic"], 1), "dic_k2": round(bay2["dic"], 1),
        "dic_favours_k": better,
        "loadings_k1": {ind_names[j]: round(float(bay1["lam_mean"][j, 0]), 3) for j in range(Pb)},
        "loadings_sd_k1": {ind_names[j]: round(float(bay1["lam_sd"][j, 0]), 3) for j in range(Pb)},
        "loadings_k2_f1": {ind_names[j]: round(float(bay2["lam_mean"][j, 0]), 3) for j in range(Pb)},
        "loadings_k2_f2": {ind_names[j]: round(float(bay2["lam_mean"][j, 1]), 3) for j in range(Pb)},
    }

    section("SUMMARY")
    print(f"PART A (omega scorecard): under-identified (rank {rank}, prior-dominated). "
          "Single-vs-multiple undecidable on current data.")
    print(f"PART B (repo population): {horn}-factor solution by Horn PA / DIC favours "
          f"k={better}; PC1 explains {var_pc1*100:.0f}% of variance.")

    if args.json:
        with open(args.json, "w") as fh:
            json.dump(out, fh, indent=2)
        print(f"\nwrote results -> {args.json}")


if __name__ == "__main__":
    sys.exit(main())
