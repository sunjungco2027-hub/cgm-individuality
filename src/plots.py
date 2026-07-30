"""make the figures: the fingerprint distance histogram and feature weights."""
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_distances
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import classify
import fingerprint as fp
from config import FEATURES


def distance_hist():
    Z, s = fp.residual_matrix()
    D = cosine_distances(Z)
    iu = np.triu_indices(len(s), k=1)
    same = (s[:, None] == s[None, :])[iu]
    plt.figure()
    plt.hist(D[iu][same], bins=40, alpha=0.6, density=True, label="within subject")
    plt.hist(D[iu][~same], bins=40, alpha=0.6, density=True, label="between subjects")
    plt.xlabel("cosine distance")
    plt.ylabel("density")
    plt.legend()
    plt.savefig("figures/distance_hist.png", dpi=150, bbox_inches="tight")


def importance_bar():
    df = classify.load()
    X = df[FEATURES].values
    y = df["y"].astype(int).values
    pipe = make_pipeline(SimpleImputer(strategy="median"), StandardScaler(),
                         LogisticRegression(max_iter=1000)).fit(X, y)
    coefs = pipe[-1].coef_[0]
    order = np.argsort(np.abs(coefs))
    plt.figure()
    plt.barh([FEATURES[i] for i in order], coefs[order])
    plt.xlabel("standardized coefficient")
    plt.savefig("figures/importance.png", dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    distance_hist()
    importance_bar()
    print("saved figures")
