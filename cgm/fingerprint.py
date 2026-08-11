"""fingerprinting: do meals from the same person cluster together once you take
out age/bmi/labs?"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics.pairwise import cosine_distances
from sklearn.preprocessing import StandardScaler

import covariates as cov
from config import FEATURES


def residual_matrix(path: str = "features.csv") -> tuple[np.ndarray, np.ndarray]:
    """residualize every feature against the covariates, then z-score."""
    df = pd.read_csv(path)
    cmat = cov.covariate_matrix()
    d = df.merge(cmat, on="subject", how="left")
    cov_cols = [c for c in cmat.columns if c != "subject"]
    d = d.dropna(subset=cov_cols + FEATURES).reset_index(drop=True)
    X = d[cov_cols].astype(float).values
    res = {}
    for f in FEATURES:
        y = d[f].astype(float).values
        res[f] = y - LinearRegression().fit(X, y).predict(X)
    Z = StandardScaler().fit_transform(pd.DataFrame(res).values)
    return Z, d["subject"].values


def within_between(Z, subjects):
    """mean cosine distance for same-person meal pairs vs different-person."""
    D = cosine_distances(Z)
    same = subjects[:, None] == subjects[None, :]
    eye = np.eye(len(subjects), dtype=bool)
    within = D[same & ~eye].mean()   # same person, drop the self-comparison
    between = D[~same].mean()        # different person (self-pairs stay out)
    return within, between


def separation_test(Z, subjects, n_perm=300, seed=0):
    """is the within-vs-between gap bigger than you'd get by shuffling labels?"""
    D = cosine_distances(Z)
    eye = np.eye(len(subjects), dtype=bool)

    def gap(sub):
        same = sub[:, None] == sub[None, :]
        return D[~same].mean() - D[same & ~eye].mean()

    obs = gap(subjects)
    rng = np.random.default_rng(seed)
    count = sum(gap(rng.permutation(subjects)) >= obs for _ in range(n_perm))
    return obs, (count + 1) / (n_perm + 1)


def cohens_d(Z, subjects):
    D = cosine_distances(Z)
    iu = np.triu_indices(len(subjects), k=1)
    same = (subjects[:, None] == subjects[None, :])[iu]
    w, b = D[iu][same], D[iu][~same]
    pooled = np.sqrt((w.var(ddof=1) + b.var(ddof=1)) / 2)
    return (b.mean() - w.mean()) / pooled
