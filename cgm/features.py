"""per-meal features from the excursion window."""
import numpy as np
from scipy.stats import kurtosis, skew


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


def time_to_return(w):
    b = baseline(w)
    pk = time_to_peak(w)
    after = w[w["min"] > pk]
    back = after[after["Libre GL"] <= b + 5]
    if len(back) == 0:
        # never got back to baseline inside the window
        return w["min"].iloc[-1]
    return back["min"].iloc[0]


def up_slope(w):
    ttp = time_to_peak(w)
    return height(w) / ttp if ttp > 0 else np.nan


def down_slope(w):
    pk = time_to_peak(w)
    after = w[w["min"] >= pk]
    if len(after) < 2:
        return np.nan
    dg = after["Libre GL"].iloc[-1] - peak(w)
    dt = after["min"].iloc[-1] - pk
    return dg / dt if dt > 0 else np.nan


def curve_skew(w):
    return skew(w["Libre GL"])


def curve_kurtosis(w):
    return kurtosis(w["Libre GL"])


def features(w):
    return {
        "baseline": baseline(w),
        "peak": peak(w),
        "height": height(w),
        "auc": auc(w),
        "time_to_peak": time_to_peak(w),
        "up_slope": up_slope(w),
        "down_slope": down_slope(w),
        "time_to_return": time_to_return(w),
        "skew": curve_skew(w),
        "kurtosis": curve_kurtosis(w),
    }
