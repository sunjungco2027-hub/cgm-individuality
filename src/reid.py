"""re-identify subjects from held-out meals.

split each person's meals 80/20, train a nearest-neighbor on the 80, and see
how often it picks the right person for the held-out 20.
"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from fingerprint import residual_matrix


def split(subjects, frac=0.8):
    train, test = [], []
    for s in np.unique(subjects):
        idx = np.where(subjects == s)[0]
        cut = max(1, int(frac * len(idx)))
        train += list(idx[:cut])
        test += list(idx[cut:])
    return np.array(train), np.array(test)


def run(path="features.csv", k=10):
    Z, subjects = residual_matrix(path)
    tr, te = split(subjects)
    knn = KNeighborsClassifier(n_neighbors=k, metric="cosine").fit(Z[tr], subjects[tr])
    top1 = (knn.predict(Z[te]) == subjects[te]).mean()
    chance = 1 / len(np.unique(subjects))
    print(f"top-1 {top1:.3f}  (chance {chance:.3f})")


if __name__ == "__main__":
    run()
