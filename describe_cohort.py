"""a quick summary of the cohort and the feature table."""
import os
import sys

sys.path.insert(0, "cgm")

import pandas as pd

from config import FEATURES


def main(path="features.csv"):
    if not os.path.exists(path):
        print("features.csv not built yet")
        return
    df = pd.read_csv(path)
    print("meals:", len(df))
    print("subjects:", df["subject"].nunique())

    try:
        import labels as lab
        d = lab.diabetes_labels()
        n_diab = sum(d.get(s, 0) for s in df["subject"].unique())
        print("diabetic subjects:", n_diab)
    except Exception:
        print("diabetic subjects: (bio.csv not available)")

    per = df.groupby("subject").size()
    print(f"meals per subject: min {per.min()}, median {int(per.median())}, max {per.max()}")

    print("feature completeness:")
    for c in FEATURES:
        present = 100 * (1 - df[c].isna().mean())
        print(f"  {c:16s} {present:5.1f}%")


if __name__ == "__main__":
    main()
