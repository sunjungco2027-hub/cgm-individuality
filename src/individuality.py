"""how individual is each feature? (icc per feature)

icc close to 1 means the feature is very consistent within a person and differs
between people; close to 0 means it's basically noise from meal to meal.
"""
import numpy as np
import pandas as pd

FEATURES = [
    "baseline", "peak", "height", "auc", "time_to_peak",
    "up_slope", "down_slope", "time_to_return", "skew", "kurtosis",
]


def icc(df, col, group="subject"):
    # icc(1,1) from a one-way anova, handles the uneven group sizes
    groups = [g[col].dropna().values for _, g in df.groupby(group)]
    groups = [g for g in groups if len(g) > 0]
    k = len(groups)
    n = sum(len(g) for g in groups)
    grand = np.concatenate(groups).mean()
    ms_between = sum(len(g) * (g.mean() - grand) ** 2 for g in groups) / (k - 1)
    ms_within = sum(((g - g.mean()) ** 2).sum() for g in groups) / (n - k)
    n0 = (n - sum(len(g) ** 2 for g in groups) / n) / (k - 1)
    return (ms_between - ms_within) / (ms_between + (n0 - 1) * ms_within)


def run(path="features.csv"):
    df = pd.read_csv(path)
    for c in FEATURES:
        print(f"{c:16s} {icc(df, c):.3f}")


if __name__ == "__main__":
    run()
