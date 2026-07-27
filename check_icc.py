"""quick check: how much of the variance in peak glucose is between people?"""
import pandas as pd

df = pd.read_csv("features.csv")

means = df.groupby("subject")["peak"].mean()
print("between-subject var / total var (peak):", round(means.var() / df["peak"].var(), 3))
