# Methods

## Data and feature extraction

We use the public CGMacros dataset, which pairs minute-level CGM traces with meal
logs and a per-subject panel of demographics and fasting labs. A meal is any
logged event with positive caloric intake. Around each meal we take the window
from 30 minutes before to 240 minutes after and resample it onto a one-minute
grid relative to the meal, so every excursion is described on the same time axis.
After dropping windows with too little coverage, this yields 1,657 meal
excursions from 45 subjects.

From each window we compute ten features that summarize the curve rather than a
single average. Four are amplitude features (pre-meal baseline, peak, the rise
from baseline to peak, and the area above baseline), two are timing features
(time to peak and time back to baseline), two are kinetic (the average up-slope
and down-slope), and two describe the distribution of glucose in the window
(skewness and kurtosis). The result is one row per meal, which the later analyses
treat as a repeated measurement of the person who ate it.

## Covariate-adjusted individuality

For each feature we first ask how much of its variance is between people rather
than within a person across meals. We use the intraclass correlation coefficient
in its one-way form, computed from the between- and within-subject mean squares
with a correction for the uneven number of meals per subject. A raw ICC near one
means the feature is highly repeatable within a person and separates people well.

A raw ICC can be inflated by nothing more than demographics: older or heavier
people simply run higher. To remove that, we regress each feature on a set of
covariates and recompute the ICC on the residuals. The covariates are the
fourteen numeric fields in the subject panel (age, body-mass index, weight,
height, HbA1c, fasting glucose, insulin, and the full lipid profile) together
with one-hot encodings of sex and self-identified ethnicity. What survives this
adjustment is individuality that age, body size, and blood chemistry do not
explain.

## Multivariate fingerprinting

The ICC looks at one feature at a time. To ask whether the whole excursion
profile clusters by person, we residualize all ten features against the same
covariates, standardize them, and measure the cosine distance between every pair
of meals. If meals carry an individual signature, two meals from the same person
should sit closer together than two meals from different people. We compare the
mean within-subject distance to the mean between-subject distance and summarize
the gap with Cohen's d. Because the pairs are not independent, we test the gap
with a permutation test: we shuffle the subject labels 300 times and count how
often a reshuffled gap is at least as large as the observed one.

## Re-identification

Distances tell us that people separate, but not by how much in practical terms.
To put a number on it we set up a re-identification task. Each subject's meals
are split, 80 percent into a gallery and 20 percent held out. A nearest-neighbour
model with ten neighbours and a cosine metric is fit on the residualized gallery
features, and we ask it to name the subject behind each held-out meal. We report
top-1 accuracy, whether the correct person is the first guess, and top-5
accuracy, whether the correct person is among the first five, each against the
chance rates of 1/45 and 5/45.

## Diabetes classification

Finally we test whether the same features predict diabetes. Subjects are labelled
diabetic if their HbA1c is at least 6.5 percent or their fasting glucose is at
least 126 mg/dL, following the ADA thresholds, and the label is carried down to
every meal from that subject. A logistic-regression classifier is trained on the
meal-level features after median imputation and standardization. Because meals
from one person are correlated, a random split would let the model recognize the
person instead of the condition, so we evaluate with five-fold cross-validation
grouped by subject, meaning every subject's meals fall entirely in either the
training or the test fold. We read feature importance from the standardized
logistic-regression coefficients.
