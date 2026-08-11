"""shared constants."""

# excursion window around a meal, in minutes
WINDOW_BEFORE = 30
WINDOW_AFTER = 240

# diabetes thresholds (ADA)
A1C_CUTOFF = 6.5
FASTING_GLU_CUTOFF = 126

# the per-meal features we extract, in a fixed order
FEATURES = [
    "baseline", "peak", "height", "auc", "time_to_peak",
    "up_slope", "down_slope", "time_to_return", "skew", "kurtosis",
]
