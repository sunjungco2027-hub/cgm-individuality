"""build a feature table with one row per meal."""
import os
import re
import sys

import pandas as pd

sys.path.insert(0, "cgm")
import load_data as ld
import windows as W
import features as F


def subject_id(path):
    m = re.search(r"CGMacros-(\d+)", os.path.basename(path))
    return int(m.group(1)) if m else None


def build():
    rows = []
    for path in ld.subject_files():
        df = ld.load_subject(path)
        for t in ld.meal_events(df)["Timestamp"]:
            w = W.excursion(df, t)
            if len(w) < 60:
                continue
            row = F.features(w)
            row["subject"] = subject_id(path)
            rows.append(row)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    table = build()
    print(table.shape)
    table.to_csv("features.csv", index=False)
