# cgm-individuality

Is the *shape* of someone's glucose response after a meal individual to them?

I'm using the public CGMacros dataset (continuous glucose monitor readings +
meal logs) to look at postprandial glucose curves and check how much of the
curve shape is person-specific vs. just noise from meal to meal.

## data

CGMacros from PhysioNet. The data isn't in this repo — download it and drop the
`CGMacros-XXX.csv` files (and `bio.csv`) into a `data/` folder.

## what's here

- `src/load_data.py` - read the CGMacros files, find meal events
- `src/windows.py` - pull the -30 to +240 min window around a meal
- `src/features.py` - baseline, peak, height, auc, timing, slopes, shape
- `build_features.py` - run everything into one row-per-meal table
- `src/covariates.py` - per-subject demographics + labs to adjust against
- `src/individuality.py` - icc per feature, raw and covariate-adjusted
- `src/fingerprint.py` - cosine distance within vs between people, permutation test
- `src/reid.py` - nearest-neighbour: guess whose meal a held-out one is
- `src/labels.py` - diabetic / not from the lab thresholds
- `src/classify.py` - predict diabetes (subject-grouped cv) + feature weights

```
python build_features.py       # writes features.csv
python src/individuality.py    # icc + covariate-adjusted icc per feature
python src/reid.py             # re-identification accuracy
python src/classify.py         # diabetes prediction + feature weights
python tests/test_smoke.py     # quick sanity check
```

Baseline and peak glucose stay the most person-specific even after adjusting for
age, sex, bmi, ethnicity and the lab panel (adjusted icc ~0.20-0.24). After
removing the covariates, meals from the same person are still closer to each
other than to other people's (within cosine ~0.91 vs between ~1.00, permutation
p ~0.003), and a nearest-neighbour picks the right person for a held-out meal
well above chance (top-5 ~0.4 vs 0.11 chance).

The same features also predict diabetes reasonably well with subject-grouped
cross-validation (auc ~0.87), and peak / baseline glucose are both the most
person-specific and the most predictive.

## status

cleaning up and writing this up.
