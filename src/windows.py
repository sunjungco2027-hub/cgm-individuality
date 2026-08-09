"""pull the glucose window around each meal."""
import pandas as pd

from config import WINDOW_AFTER, WINDOW_BEFORE


def excursion(df, meal_time, before=WINDOW_BEFORE, after=WINDOW_AFTER):
    """Glucose window around a meal, indexed by minutes relative to the meal.

    Spans `before` minutes before to `after` minutes after `meal_time`.
    """
    lo = meal_time - pd.Timedelta(minutes=before)
    hi = meal_time + pd.Timedelta(minutes=after)
    w = df[(df["Timestamp"] >= lo) & (df["Timestamp"] <= hi)].copy()
    w["min"] = (w["Timestamp"] - meal_time).dt.total_seconds() / 60.0
    return w[["min", "Libre GL"]].reset_index(drop=True)
