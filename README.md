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
- `src/individuality.py` - icc per feature (how person-specific each one is)

```
python build_features.py       # writes features.csv
python src/individuality.py    # icc per feature
```

So far baseline and peak glucose are the most person-specific (icc ~0.55-0.65),
timing/shape features much less so.

## status

next: adjust the icc for age/bmi/etc. to see what individuality survives, and
try telling people apart from their meal responses.
