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

FEATURES = [
    "baseline", "peak", "height", "auc", "time_to_peak",
    "up_slope", "down_slope", "time_to_return", "skew", "kurtosis",
]


def load(path="features.csv"):
    df = pd.read_csv(path)
    df["y"] = df["subject"].map(L.diabetes_labels())
    return df.dropna(subset=["y"])


def run(path="features.csv"):
    df = load(path)
    X = df[FEATURES].values
    y = df["y"].astype(int).values
    groups = df["subject"].values
    pipe = make_pipeline(
        SimpleImputer(strategy="median"),
        StandardScaler(),
        LogisticRegression(max_iter=1000),
    )
    proba = cross_val_predict(pipe, X, y, cv=GroupKFold(5), groups=groups,
                              method="predict_proba")[:, 1]
    print("grouped-cv auc:", round(roc_auc_score(y, proba), 3))


if __name__ == "__main__":
    run()
