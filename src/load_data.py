"""Helpers for reading the CGMacros csv files."""
import glob
import os

import pandas as pd

DATA_DIR = "data"


def subject_files(data_dir=DATA_DIR):
    """Return the list of per-subject CGMacros csv files."""
    files = glob.glob(os.path.join(data_dir, "**", "CGMacros-*.csv"), recursive=True)
    return sorted(f for f in files if "Dictionary" not in f)


def load_subject(path):
    """Read one subject file, parse the timestamp, sort by time."""
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
    df = df.dropna(subset=["Timestamp"]).sort_values("Timestamp")
    return df


def meal_events(df):
    """Rows that mark a meal (the meal-calorie column is > 0)."""
    cal = pd.to_numeric(df.get("Calories"), errors="coerce").fillna(0)
    return df[cal > 0]


if __name__ == "__main__":
    files = subject_files()
    print("found", len(files), "subject files")
    total_meals = 0
    for f in files:
        df = load_subject(f)
        total_meals += len(meal_events(df))
    print("total meal events:", total_meals)
