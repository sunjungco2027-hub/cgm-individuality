"""pull the glucose window around each meal."""
import pandas as pd


def excursion(df, meal_time, before=30, after=240):
    # window from `before` min before the meal to `after` min after
    lo = meal_time - pd.Timedelta(minutes=before)
    hi = meal_time + pd.Timedelta(minutes=after)
    w = df[(df["Timestamp"] >= lo) & (df["Timestamp"] <= hi)].copy()
    w["min"] = (w["Timestamp"] - meal_time).dt.total_seconds() / 60.0
    return w[["min", "Libre GL"]].reset_index(drop=True)
