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
- `src/features.py` - baseline, peak, height, auc, time to peak
- `build_features.py` - run everything into one row-per-meal table

```
python build_features.py   # writes features.csv
```

## status

next: a few more shape/slope features, then check how consistent each one is
within a person vs between people.
