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
