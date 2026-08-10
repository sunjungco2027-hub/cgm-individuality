"""per-subject covariates to adjust the icc against."""
import pandas as pd

import load_data as ld

NUMERIC = [
    "Age", "BMI", "Body weight", "Height", "A1c PDL (Lab)",
    "Fasting GLU - PDL (Lab)", "Insulin", "Triglycerides", "Cholesterol",
    "HDL", "Non HDL", "LDL (Cal)", "VLDL (Cal)", "Cho/HDL Ratio",
]
CATEGORICAL = ["Gender", "Self-identify"]


def covariate_matrix(data_dir: str = ld.DATA_DIR) -> pd.DataFrame:
    b = ld.load_bio(data_dir)
    m = b[["subject"]].copy()
    for c in NUMERIC:
        if c in b.columns:
            m[c] = pd.to_numeric(b[c], errors="coerce")
    cats = [c for c in CATEGORICAL if c in b.columns]
    if cats:
        dummies = pd.get_dummies(b[cats].astype(str), drop_first=True).astype(float)
        m = pd.concat([m, dummies], axis=1)
    return m
