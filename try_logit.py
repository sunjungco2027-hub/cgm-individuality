"""quick check: do the meal features separate diabetic vs not at all?"""
import sys
sys.path.insert(0, "src")

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

import labels as L

FEATS = ["baseline", "peak", "height", "auc", "time_to_peak",
         "up_slope", "down_slope", "time_to_return", "skew", "kurtosis"]

df = pd.read_csv("features.csv")
df["y"] = df["subject"].map(L.diabetes_labels())
df = df.dropna(subset=FEATS + ["y"])
X = df[FEATS].values
y = df["y"].astype(int).values

Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.3, random_state=0)
sc = StandardScaler().fit(Xtr)
m = LogisticRegression(max_iter=1000).fit(sc.transform(Xtr), ytr)
print("auc:", round(roc_auc_score(yte, m.predict_proba(sc.transform(Xte))[:, 1]), 3))
