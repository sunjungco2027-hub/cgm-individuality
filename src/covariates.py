"""per-subject covariates to adjust the icc against."""
import pandas as pd

import load_data as ld

NUMERIC = [
    "Age", "BMI", "Body weight", "Height", "A1c PDL (Lab)",
    "Fasting GLU - PDL (Lab)", "Insulin", "Triglycerides", "Cholesterol",
    "HDL", "Non HDL", "LDL (Cal)", "VLDL (Cal)", "Cho/HDL Ratio",
]


def covariate_matrix(data_dir=ld.DATA_DIR):
    b = ld.load_bio(data_dir)
    m = b[["subject"]].copy()
    for c in NUMERIC:
        if c in b.columns:
            m[c] = pd.to_numeric(b[c], errors="coerce")
    return m
