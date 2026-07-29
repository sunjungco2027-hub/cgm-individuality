"""fingerprinting: do meals from the same person cluster together once you take
out age/bmi/labs?"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics.pairwise import cosine_distances
from sklearn.preprocessing import StandardScaler

import covariates as cov
from individuality import FEATURES


def residual_matrix(path="features.csv"):
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
    within = D[same].mean()
    between = D[~same].mean()
    return within, between
