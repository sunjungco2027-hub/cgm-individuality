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
