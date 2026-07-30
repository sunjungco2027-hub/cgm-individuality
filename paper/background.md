# Background and Related Work

Continuous glucose monitoring (CGM) records interstitial glucose every few
minutes and has changed how day-to-day metabolism is observed (Danne et al.,
2017). In routine use, though, most of that signal is compressed into a handful
of static summaries. Time in range and the glucose management indicator report
how often glucose sits inside a target band or estimate an A1c-like average
(Battelino et al., 2019; Bergenstal et al., 2018), and variability indices add a
measure of spread (Monnier et al., 2008). These numbers are useful for
management, but they mostly describe where glucose sits rather than how it moves.
A meal response has a shape: a rise, a peak, and a return toward baseline, and
that shape is largely lost once a day is reduced to an average. Clinical
guidelines have argued for years that the postprandial period itself carries
information about metabolic health (Ceriello and Colagiuri, 2008), which suggests
the excursion is worth modeling on its own terms.

That the same meal can produce very different responses in different people is by
now well documented. Zeevi et al. (2015) found that postprandial responses to
identical foods vary widely across individuals and can be predicted from personal
and microbiome features, which motivated personalized rather than uniform dietary
advice. Hall et al. (2018) took the idea further, clustering CGM traces into
distinct "glucotypes" that separated people by how variable their glucose was,
including people without a diabetes diagnosis. Both results establish that
individual differences are real. What they leave open is whether those
differences are stable and specific enough to act as a signature of the person
once the obvious explanations, such as age, body mass, and blood chemistry, are
accounted for.

Measuring how much of a trait belongs to the person is an old problem. The
intraclass correlation coefficient (ICC) splits the variance of repeated
measurements into a between-subject part and a within-subject part, so a high ICC
means a feature is consistent within a person yet differs across people. A
related but stricter view comes from biometrics, where the question is not only
whether people differ on average but whether an unseen sample can be matched back
to the right individual. Posing CGM meal responses this way, as a
re-identification task, turns a loose notion of individuality into a measurable
quantity: how often the correct person appears among the top guesses for a
held-out meal. To our knowledge this framing has not been applied to
postprandial glucose curves, even though recognizing a person from a
physiological signal is a familiar goal elsewhere.

CGM-derived features have also been used to separate diabetic from non-diabetic
individuals, which is consistent with the underlying physiology: impaired insulin
secretion and insulin resistance push peaks higher and slow the return to
baseline after eating (DeFronzo, 2004). One caution runs through this line of
work. When the diabetes label is itself defined by fasting glucose or A1c,
features that essentially re-measure glucose level will track that label almost
by construction. The more informative question is whether the shape and timing of
the excursion, and not only its height, add anything beyond the diagnostic
thresholds. We keep this distinction in mind when we later separate amplitude
features from shape and kinetic ones.

Taken together, earlier work shows that glycemic responses are individual and
that CGM features carry information about metabolic status, but it stops short in
two places. It rarely tests whether the individual signal survives adjustment for
demographics and laboratory covariates, so it stays unclear how much of the
apparent individuality is just a stand-in for known differences. And it does not
put a number on that individuality through re-identification. This paper takes up
both gaps, and then asks a question that ties them together: are the features
that make a person identifiable the same ones that make them classifiable as
diabetic?
