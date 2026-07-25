"""per-meal features from the excursion window."""
import numpy as np


def baseline(w):
    return w[w["min"] <= 0]["Libre GL"].mean()


def peak(w):
    return w["Libre GL"].max()


def height(w):
    return peak(w) - baseline(w)


def auc(w):
    # area of the rise above baseline (ignore dips below it)
    b = baseline(w)
    above = np.clip(w["Libre GL"] - b, 0, None)
    return np.trapezoid(above, w["min"])


def time_to_peak(w):
    i = w["Libre GL"].idxmax()
    return w.loc[i, "min"]


def features(w):
    return {
        "baseline": baseline(w),
        "peak": peak(w),
        "height": height(w),
        "auc": auc(w),
        "time_to_peak": time_to_peak(w),
    }
