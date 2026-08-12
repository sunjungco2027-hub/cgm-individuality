"""check the headline results land in sane ranges.

needs the feature table (features.csv) and bio.csv in data/; skips otherwise.
run with:  python tests/test_results.py
"""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "cgm"))

import pandas as pd

FEATURES_CSV = os.path.join(HERE, "..", "features.csv")


def _ready():
    if not os.path.exists(FEATURES_CSV):
        print("features.csv not built, skipping")
        return False
    return True


def test_individuality():
    if not _ready():
        return
    import covariates as cov
    import individuality as ind
    df = pd.read_csv(FEATURES_CSV)
    cmat = cov.covariate_matrix()
    assert 0.4 < ind.icc(df, "peak") <= 1.0
    assert 0.4 < ind.icc(df, "baseline") <= 1.0
    assert ind.adjusted_icc(df, "peak", cmat) > 0.15
    assert ind.adjusted_icc(df, "baseline", cmat) > 0.10
    for c in ind.FEATURES:
        a = ind.adjusted_icc(df, c, cmat)
        assert a == a and a <= 1.0, (c, a)  # not nan, not above 1
    print("icc ranges ok")


def test_fingerprint():
    if not _ready():
        return
    import fingerprint as fp
    Z, s = fp.residual_matrix(FEATURES_CSV)
    within, between = fp.within_between(Z, s)
    assert within < between, (within, between)
    _, p = fp.separation_test(Z, s)
    assert p < 0.05, p
    print("fingerprint ok")


def test_classifier_beats_chance():
    if not _ready():
        return
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import roc_auc_score
    from sklearn.model_selection import GroupKFold, cross_val_predict
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    import classify
    df = classify.load(FEATURES_CSV)
    X = df[classify.FEATURES].values
    y = df["y"].astype(int).values
    pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                         LogisticRegression(max_iter=1000))
    proba = cross_val_predict(pipe, X, y, cv=GroupKFold(5),
                              groups=df["subject"].values,
                              method="predict_proba")[:, 1]
    assert roc_auc_score(y, proba) > 0.7
    print("classifier ok")


def test_reported_numbers_reproduce():
    """the headline numbers quoted in the paper should fall out of the pipeline."""
    if not _ready():
        return
    import numpy as np
    import covariates as cov
    import individuality as ind
    import fingerprint as fp
    import reid
    import classify

    df = pd.read_csv(FEATURES_CSV)
    cmat = cov.covariate_matrix()
    assert abs(ind.icc(df, "peak") - 0.646) < 0.01
    assert abs(ind.icc(df, "baseline") - 0.556) < 0.01
    assert abs(ind.adjusted_icc(df, "peak", cmat) - 0.244) < 0.01
    assert abs(ind.adjusted_icc(df, "baseline", cmat) - 0.197) < 0.01

    Z, s = fp.residual_matrix(FEATURES_CSV)
    within, between = fp.within_between(Z, s)
    assert abs(within - 0.912) < 0.005 and abs(between - 0.998) < 0.005
    assert abs(fp.cohens_d(Z, s) - 0.183) < 0.01
    _, p = fp.separation_test(Z, s)
    assert p <= 0.01

    top1, top5 = np.array([reid.score(Z, s, seed=i, k=10)
                           for i in range(20)]).mean(axis=0)
    assert abs(top1 - 0.147) < 0.02 and abs(top5 - 0.388) < 0.02

    cdf = classify.load(FEATURES_CSV)
    assert abs(classify.grouped_auc(cdf, classify.FEATURES) - 0.870) < 0.01
    no_amp = [c for c in classify.FEATURES if c not in classify.AMPLITUDE]
    assert abs(classify.grouped_auc(cdf, no_amp) - 0.664) < 0.02
    print("reported numbers reproduce")


if __name__ == "__main__":
    test_individuality()
    test_fingerprint()
    test_classifier_beats_chance()
    test_reported_numbers_reproduce()
    print("all good")
