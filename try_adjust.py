"""does peak-glucose individuality survive after removing age/bmi/labs?"""
import sys

import pandas as pd
from sklearn.linear_model import LinearRegression

sys.path.insert(0, "src")
import covariates as cov
import individuality as ind

df = pd.read_csv("features.csv")
cmat = cov.covariate_matrix()

d = df.merge(cmat, on="subject", how="left")
X = d[[c for c in cmat.columns if c != "subject"]].values
y = d["peak"].values
resid = y - LinearRegression().fit(X, y).predict(X)

print("peak icc raw  :", round(ind.icc(df, "peak"), 3))
print("peak icc resid:", round(ind.icc(d.assign(peak=resid), "peak"), 3))
