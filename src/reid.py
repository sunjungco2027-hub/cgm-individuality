"""re-identify subjects from held-out meals.

split each person's meals 80/20, train a nearest-neighbor on the 80, and see
how often it picks the right person for the held-out 20.
"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

from fingerprint import residual_matrix


def split(subjects: np.ndarray, frac: float = 0.8, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    train, test = [], []
    for s in np.unique(subjects):
        idx = np.where(subjects == s)[0]
        rng.shuffle(idx)  # don't just take the earliest meals
        cut = max(1, int(frac * len(idx)))
        train += list(idx[:cut])
        test += list(idx[cut:])
    return np.array(train), np.array(test)


def score(Z, subjects, seed=0, k=10):
    """top-1 and top-5 accuracy for one gallery/probe split."""
    tr, te = split(subjects, seed=seed)
    knn = KNeighborsClassifier(n_neighbors=k, metric="cosine").fit(Z[tr], subjects[tr])
    top1 = (knn.predict(Z[te]) == subjects[te]).mean()
    order = np.argsort(-knn.predict_proba(Z[te]), axis=1)[:, :5]
    top5_labels = knn.classes_[order]
    top5 = np.mean([subjects[te][i] in top5_labels[i] for i in range(len(te))])
    return top1, top5


def run(path="features.csv", k=10):
    Z, subjects = residual_matrix(path)
    top1, top5 = score(Z, subjects, seed=0, k=k)
    n = len(np.unique(subjects))
    print(f"top-1 {top1:.3f}  (chance {1 / n:.3f})")
    print(f"top-5 {top5:.3f}  (chance {5 / n:.3f})")


if __name__ == "__main__":
    run()
