"""diabetes label per subject, from the ADA thresholds in bio.csv."""
import pandas as pd

import load_data as ld


def diabetes_labels(data_dir=ld.DATA_DIR):
    b = ld.load_bio(data_dir)
    a1c = pd.to_numeric(b["A1c PDL (Lab)"], errors="coerce")
    fg = pd.to_numeric(b["Fasting GLU - PDL (Lab)"], errors="coerce")
    label = ((a1c >= 6.5) | (fg >= 126)).astype(int)
    return dict(zip(b["subject"], label))


if __name__ == "__main__":
    labs = diabetes_labels()
    print("subjects:", len(labs), "| diabetic:", sum(labs.values()))
