# Results

## Cohort

The pipeline extracts 1,657 meal excursions from 45 subjects. Applying the ADA
thresholds at the subject level labels 18 of the 45 as diabetic, so about 40
percent of the cohort, and every meal inherits its subject's label. The
classification task below is therefore moderately imbalanced but not severely so.

## Individuality of single features

The amplitude features are the most person-specific. Peak glucose has the highest
raw ICC at 0.65 and baseline glucose is next at 0.56, meaning that most of the
variance in these features is between people rather than within a person across
meals. Timing and distribution-shape features sit much lower, mostly under 0.15.
Adjusting for the covariates shrinks every ICC, as expected, but does not erase
the leaders: peak and baseline glucose keep adjusted ICCs of 0.24 and 0.20. In
other words, part of what makes two people's meal responses differ in height is
not explained by their age, body size, or blood chemistry.

