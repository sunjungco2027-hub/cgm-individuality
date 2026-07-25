"""pull the glucose window around each meal."""
import numpy as np
import pandas as pd


def excursion(df, meal_time, before=30, after=240):
    # window from `before` min before the meal to `after` min after
    lo = meal_time - pd.Timedelta(minutes=before)
    hi = meal_time + pd.Timedelta(minutes=after)
    w = df[(df["Timestamp"] >= lo) & (df["Timestamp"] <= hi)].copy()
    w["min"] = (w["Timestamp"] - meal_time).dt.total_seconds() / 60.0
    return w[["min", "Libre GL"]].reset_index(drop=True)


def baseline(w):
    # average glucose in the 30 min before the meal
    pre = w[w["min"] <= 0]["Libre GL"]
    return pre.mean()


def peak(w):
    return w["Libre GL"].max()


def excursion_height(w):
    return peak(w) - baseline(w)


def auc_above_baseline(w):
    b = baseline(w)
    return np.trapezoid(w["Libre GL"] - b, w["min"])
