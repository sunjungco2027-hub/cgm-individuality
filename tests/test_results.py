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


if __name__ == "__main__":
    test_individuality()
    test_fingerprint()
    test_classifier_beats_chance()
    print("all good")
