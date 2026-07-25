"""per-meal features from the excursion window."""
import windows as W


def features(w):
    return {
        "baseline": W.baseline(w),
        "peak": W.peak(w),
        "height": W.excursion_height(w),
        "auc": W.auc_above_baseline(w),
        "time_to_peak": W.time_to_peak(w),
    }
