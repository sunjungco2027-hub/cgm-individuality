"""quick sanity check that the pipeline still runs end to end.

run with:  python tests/test_smoke.py
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import load_data as ld
import windows as W
import features as F


def test_window_and_features():
    df = ld.load_subject(ld.subject_files()[0])
    meals = ld.meal_events(df)
    assert len(meals) > 0

    w = W.excursion(df, meals.iloc[0]["Timestamp"])
    assert w["min"].min() >= -30 and w["min"].max() <= 240

    f = F.features(w)
    for k, v in f.items():
        assert v is not None and not np.isnan(float(v)), k
    print("window + features ok")


def test_meal_count():
    total = sum(len(ld.meal_events(ld.load_subject(p))) for p in ld.subject_files())
    assert total > 1000, total
    print("meal count ok:", total)


if __name__ == "__main__":
    test_window_and_features()
    test_meal_count()
    print("all good")
