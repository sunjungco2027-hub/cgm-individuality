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

## Profiles cluster by person

Looking at all ten features together tells the same story. After residualizing
against the covariates, the mean cosine distance between two meals from the same
person is 0.912, smaller than the 0.997 between meals from different people. The
gap is a small effect by Cohen's conventions, d = 0.18, but the permutation test
rules out chance, with p = 0.003 across 300 shuffles of the subject labels. So
the individual signal is modest in size yet reliably present once demographics
and labs are removed.

## Re-identification

The re-identification task turns that signal into a concrete number. Given a
held-out meal, the nearest-neighbour model names the correct person first 13
percent of the time, against a chance rate of about 2 percent, and it places the
correct person in its top five guesses 42 percent of the time, against a chance
rate of 11 percent. Both are several times chance. The accuracy is far from
identification-grade, which is expected for a small set of features, but it shows
that a meal response carries enough of a signature to point back at the person
who produced it.

## Diabetes classification

The same features predict diabetes reasonably well. Under five-fold
subject-grouped cross-validation the logistic-regression classifier reaches an
area under the ROC curve of 0.87, so the features generalize to people the model
has not seen rather than memorizing individuals. The standardized coefficients
rank peak glucose first, then baseline glucose and the rise from baseline to
peak. The amplitude features do most of the work, with timing and shape features
contributing little on their own.

## The two results meet on the same features

Peak and baseline glucose are the two features that keep the most individuality
after covariate adjustment, and they are also the two that carry the most weight
in the diabetes classifier. The trait that makes a person recognizable is, at
least here, the same trait that flags their metabolic risk. That overlap is worth
a caution as much as a claim: because the diabetes label is defined by glucose
level, features that re-measure level are expected to predict it, so the honest
open question is how much the shape of the excursion adds beyond height. We leave
a direct test of that, holding out the amplitude features, for future work.




