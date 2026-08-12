"""make the figures: the fingerprint distance histogram and feature weights."""
import os

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
import load_data as ld
import windows as W
from config import FEATURES


def window_example():
    """a labelled example excursion: the mean meal response of one subject."""
    df = ld.load_subject(ld.subject_files()[0])
    grid = np.arange(-30, 241)
    stack = []
    for t in ld.meal_events(df)["Timestamp"]:
        w = W.excursion(df, t)
        s = w.set_index(w["min"].round().astype(int))["Libre GL"]
        s = s[~s.index.duplicated()].reindex(grid)
        if s.notna().mean() > 0.9:
            stack.append(s.to_numpy(dtype=float))
    mean = np.nanmean(np.array(stack), axis=0)
    base = np.nanmean(mean[grid <= 0])
    pk_i = int(np.nanargmax(mean))

    plt.figure(figsize=(5, 3))
    plt.plot(grid, mean, color="#1f77b4")
    plt.axhline(base, ls="--", color="gray", lw=1)
    plt.axvline(0, color="gray", lw=0.8)
    plt.scatter([grid[pk_i]], [mean[pk_i]], color="crimson", zorder=5)
    plt.annotate("peak", (grid[pk_i], mean[pk_i]),
                 textcoords="offset points", xytext=(6, 3))
    plt.annotate("baseline", (grid[0], base),
                 textcoords="offset points", xytext=(2, 4))
    plt.xlabel("minutes relative to meal")
    plt.ylabel("glucose (mg/dL)")
    plt.savefig("figures/window_example.png", dpi=150, bbox_inches="tight")


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
    os.makedirs("figures", exist_ok=True)
    window_example()
    distance_hist()
    importance_bar()
    print("saved figures")
