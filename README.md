# cgm-individuality

**Does a person's post-meal glucose curve carry a signature of who they are?**
This repository extracts shape features from continuous glucose monitor (CGM)
excursions and asks whether that signature survives adjustment for age and lab
values, whether it can re-identify a subject, and whether it predicts diabetes.

## Results

| Analysis | Metric | Value |
|---|---|---|
| Individuality (covariate-adjusted ICC) | peak / baseline glucose | 0.24 / 0.20 |
| Fingerprint (cosine distance) | within vs between subject | 0.91 vs 1.00, permutation p = 0.003 |
| Re-identification | top-1 / top-5 (chance) | 0.13 / 0.42 (0.02 / 0.11) |
| Diabetes classification | subject-grouped CV AUC | 0.87 |

Peak and baseline glucose turn out to be both the most person-specific features
and the strongest diabetes predictors.

## Repository layout

| Path | Contents |
|---|---|
| `src/` | feature extraction, ICC, fingerprinting, re-identification, classifier, plots |
| `build_features.py` / `run_all.py` | build the per-meal table / run the whole pipeline |
| `tests/` | end-to-end sanity check |
| `paper/` | manuscript (`paper.md`, IEEE `paper.tex`, `paper.docx`) and figures |

## Getting started

```bash
pip install -r requirements.txt
python run_all.py
```

Two checks live in `tests/`: `test_smoke.py` runs the pipeline end to end, and
`test_results.py` confirms the headline numbers land in sane ranges. Both skip
quietly if the dataset is not present.

`run_all.py` reports the individuality, fingerprint, re-identification, and
classification results in a single pass.

## Data

The analysis is built on the CGMacros dataset from PhysioNet, which is not
redistributed here. Put the per-subject `CGMacros-*.csv` files and `bio.csv`
under `data/` before running anything.

## Paper

The write-up lives in `paper/`: a markdown draft (`paper.md`), a two-column IEEE
version (`paper.tex`, compiles on Overleaf), and a Word export (`paper.docx`).

## Citing

Citation metadata is in `CITATION.cff`. Released under the MIT License (`LICENSE`).
