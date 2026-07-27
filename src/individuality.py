"""how individual is each feature? (icc per feature)

icc close to 1 means the feature is very consistent within a person and differs
between people; close to 0 means it's basically noise from meal to meal.
"""
import pandas as pd

FEATURES = [
    "baseline", "peak", "height", "auc", "time_to_peak",
    "up_slope", "down_slope", "time_to_return", "skew", "kurtosis",
]


def icc(df, col, group="subject"):
    means = df.groupby(group)[col].mean()
    return means.var() / df[col].var()


def run(path="features.csv"):
    df = pd.read_csv(path)
    for c in FEATURES:
        print(f"{c:16s} {icc(df, c):.3f}")


if __name__ == "__main__":
    run()
