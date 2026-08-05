# Discussion

Two findings sit next to each other here. The shape of a meal response holds an
individual component that survives adjustment for demographics and fasting labs,
and the features that carry that component are the same ones that predict
diabetes. The most likely reading is that amplitude features such as peak and
baseline glucose reflect slower-moving traits of a person's metabolism, things
like insulin secretion and clearance, that a one-time demographic and lab panel
does not fully capture. Latent factors of that kind, and possibly gastric
emptying or gut microbiome, would show up as stable between-person differences in
how high glucose climbs and how it settles, which is what the ICC and the
fingerprint analyses pick up. For the growing number of people who already wear a
sensor, this points toward a passive form of metabolic characterization that
needs no extra visit.

## Limitations

The study is small. Forty-five subjects and a single dataset limit how far the
numbers generalize, and the cohort leans toward one population, so the same
analysis on a broader group could look different. The most important caveat is
the label itself. Diabetes here is defined by fasting glucose and HbA1c, and the
two strongest predictors re-measure glucose level, so part of the classification
result is expected almost by definition. We flag the shape and kinetic features as
the more interesting question and leave a clean test, holding out the amplitude
features, for later. The re-identification accuracy is well above chance but
modest, and it moves a little with the random split, so it should be read as
evidence of a signature rather than as a working identifier. Finally, the ten
features are a compact summary, and meal composition, time of day, and overlap
between nearby meals are not modeled, all of which could sharpen or blur the
individual signal.
