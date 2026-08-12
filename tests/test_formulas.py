"""check the statistics on synthetic data, where the answers are known.

these do not touch the dataset, so they always run. they pin down the icc
formula, the permutation p-value, and the cohen's d sign, which is what the
paper leans on.

run with:  python tests/test_formulas.py
"""
import os
import sys

import numpy as np
from scipy.stats import f_oneway

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cgm"))

import fingerprint as fp
from individuality import _icc_from_groups


def _synthetic_groups(seed=3):
    rng = np.random.default_rng(seed)
    return [rng.normal(loc=m, scale=1.0, size=n)
            for m, n in [(0, 7), (2, 5), (-1, 9), (3, 4), (1, 6)]]


def test_icc_matches_the_f_route():
    # icc(1,1) = (F - 1) / (F + n0 - 1) with F the one-way anova statistic,
    # so an independent path through scipy should land on the same number.
    groups = _synthetic_groups()
    k = len(groups)
    n = sum(len(g) for g in groups)
    n0 = (n - sum(len(g) ** 2 for g in groups) / n) / (k - 1)
    f = f_oneway(*groups).statistic
    expected = (f - 1) / (f + n0 - 1)
    got = _icc_from_groups(groups)
    assert np.isclose(got, expected, atol=1e-9), (got, expected)
    print("icc matches the f route")


def test_icc_is_one_when_perfectly_consistent():
    # no within-person variance -> all variance is between people -> icc = 1.
    groups = [np.array([5.0, 5.0, 5.0]), np.array([9.0, 9.0, 9.0, 9.0])]
    assert _icc_from_groups(groups) == 1.0
    print("icc is one when perfectly consistent")


def test_icc_is_near_zero_without_between_structure():
    # every group drawn from the same distribution -> little between variance.
    rng = np.random.default_rng(0)
    groups = [rng.normal(0, 1, 30) for _ in range(20)]
    assert _icc_from_groups(groups) < 0.1
    print("icc is near zero without between structure")


def test_permutation_p_respects_its_lower_bound():
    # p = (count + 1) / (n_perm + 1) can never fall below 1 / (n_perm + 1).
    rng = np.random.default_rng(1)
    Z = rng.normal(size=(40, 5))
    subjects = np.repeat(np.arange(8), 5)
    n_perm = 200
    _, p = fp.separation_test(Z, subjects, n_perm=n_perm, seed=0)
    assert 1 / (n_perm + 1) <= p <= 1.0, p
    print("permutation p respects its lower bound")


def test_cohens_d_is_positive_when_meals_cluster_by_person():
    # build meals that sit near a per-person centre; same-person pairs should
    # be closer, so the between-minus-within effect size is positive.
    rng = np.random.default_rng(2)
    subjects = np.repeat(np.arange(10), 6)
    centres = rng.normal(0, 3, size=(10, 5))
    Z = centres[subjects] + rng.normal(0, 0.2, size=(60, 5))
    assert fp.cohens_d(Z, subjects) > 0
    print("cohen's d is positive when meals cluster by person")


if __name__ == "__main__":
    test_icc_matches_the_f_route()
    test_icc_is_one_when_perfectly_consistent()
    test_icc_is_near_zero_without_between_structure()
    test_permutation_p_respects_its_lower_bound()
    test_cohens_d_is_positive_when_meals_cluster_by_person()
    print("all good")
