"""predict diabetes from the meal features.

meals from one person must not be split across train and test, otherwise the
model just recognises the person, so we group the cross-validation by subject.
"""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GroupKFold, cross_val_predict
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import labels as L
from config import FEATURES


def load(path: str = "features.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df["y"] = df["subject"].map(L.diabetes_labels())
    return df.dropna(subset=["y"])


def _pipe():
    return make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        LogisticRegression(max_iter=1000),
    )


def grouped_auc(df: pd.DataFrame, cols) -> float:
    """subject-grouped 5-fold CV AUC for a chosen set of features."""
    X = df[cols].values
    y = df["y"].astype(int).values
    proba = cross_val_predict(_pipe(), X, y, cv=GroupKFold(5),
                              groups=df["subject"].values,
                              method="predict_proba")[:, 1]
    return roc_auc_score(y, proba)


def run(path: str = "features.csv") -> None:
    df = load(path)
    X = df[FEATURES].values
    y = df["y"].astype(int).values
    print("grouped-cv auc:", round(grouped_auc(df, FEATURES), 3))

    # which features carry the most weight (standardized coefficients)
    pipe = _pipe()
    pipe.fit(X, y)
    coefs = pipe[-1].coef_[0]
    order = np.argsort(-np.abs(coefs))
    print("\ntop features:")
    for i in order:
        print(f"  {FEATURES[i]:16s} {coefs[i]:+.2f}")


AMPLITUDE = ["baseline", "peak", "height", "auc"]


def ablation(path: str = "features.csv") -> None:
    """does prediction hold up once the glucose-level features are taken out?"""
    df = load(path)
    subsets = [
        ("all features", FEATURES),
        ("without peak and baseline", [c for c in FEATURES if c not in ("peak", "baseline")]),
        ("without any amplitude", [c for c in FEATURES if c not in AMPLITUDE]),
        ("peak and baseline only", ["peak", "baseline"]),
    ]
    for name, cols in subsets:
        print(f"{name:26s} auc {grouped_auc(df, cols):.3f}")


if __name__ == "__main__":
    run()
