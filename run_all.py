"""run the whole pipeline and print a one-page summary."""
import os
import sys

sys.path.insert(0, "src")

import build_features as bf
import classify
import fingerprint as fp
import individuality as ind
import reid


def main():
    if not os.path.exists("features.csv"):
        bf.build().to_csv("features.csv", index=False)

    print("== individuality (icc, raw vs covariate-adjusted) ==")
    ind.run()

    print("\n== fingerprint ==")
    Z, s = fp.residual_matrix()
    w, b = fp.within_between(Z, s)
    gap, p = fp.separation_test(Z, s)
    print(f"within {w:.3f} / between {b:.3f} | perm p {p:.3f} | cohen d {fp.cohens_d(Z, s):.3f}")

    print("\n== re-identification ==")
    reid.run()

    print("\n== diabetes classification ==")
    classify.run()

    print("\n== ablation: auc as feature groups are removed ==")
    classify.ablation()


if __name__ == "__main__":
    main()
