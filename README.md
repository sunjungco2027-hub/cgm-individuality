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

```
python build_features.py       # writes features.csv
python src/individuality.py    # icc + covariate-adjusted icc per feature
```

Baseline and peak glucose stay the most person-specific even after adjusting for
age, sex, bmi, ethnicity and the lab panel (adjusted icc ~0.20-0.24), so it's not
just demographics.

## status

next: tell people apart from their meal responses (nearest-neighbour on the
residualized features) to put a number on the individuality.
