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


if __name__ == "__main__":
    files = subject_files()
    print("found", len(files), "subject files")
    if files:
        df = load_subject(files[0])
        print(os.path.basename(files[0]), "->", df.shape)
