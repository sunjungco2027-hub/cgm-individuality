# Introduction

Continuous glucose monitors are now cheap enough that people without diabetes
wear them, and each sensor produces a dense record of how the body handles food.
The most informative part of that record is the meal response: glucose rises
after eating, reaches a peak, and returns toward baseline. The height, timing, and
steepness of that curve differ from person to person, and this paper asks a
simple question about those differences. Is the shape of a meal response
individual to the person, in a way that ordinary explanations like age and body
weight cannot account for, and if so, does that same individual signal say
anything about their metabolic health?

Earlier work has shown that people mount different responses to the same food and
that continuous glucose patterns fall into distinct groups. What it has largely
left untested is whether the individual part survives once demographics and
laboratory values are removed, and it has not tried to measure that individuality
the way biometrics does, by asking whether an unseen meal can be traced back to
the right person. Framing the problem as re-identification is what lets us report
individuality as an accuracy rather than an impression.

This paper makes two contributions. First, using covariate-adjusted repeatability,
multivariate distance, and a re-identification test on held-out meals, we show
that postprandial excursion profiles carry an individual signal that demographics
and labs do not explain. Second, we show that the same features that make a
person identifiable also predict diabetes under subject-grouped cross-validation,
so individuality and clinical signal turn out to live in the same features rather
than in separate ones.
