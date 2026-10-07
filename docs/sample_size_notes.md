# Preliminary sample-size planning

These calculations reproduce the Week 1 synopsis planning assumptions. They are included because the synopsis rubric explicitly asks for a method, parameters, stepwise calculation, and a maximum across RQ1-RQ4.

They are **not final effect-size claims**. The assumptions should be revisited after the literature review, data audit, and mentor feedback.

## RQ1 - Recurring-topic coverage

Goal: estimate the proportion of eligible threads assignable to recurring topics.

Inputs:
- confidence = 95%
- p = 0.50
- margin of error = +/- 0.03

Formula:

```
n = z^2 * p * (1-p) / e^2
```

This gives raw n ≈ 1067.1, therefore **N1 = 1,068 eligible threads**.

## RQ2 - PII detection precision and recall

RQ2 evaluates the hybrid German/English spaCy NER + regex detector using **precision and recall** against human-reviewed reference labels. Because these metrics are proportions, the sample-size method is aligned to CI precision rather than to a paired mean-difference test.

Inputs:
- confidence = 95%
- p = 0.50 because the true precision/recall is unknown at Week 1
- margin of error = +/- 0.05

The same proportion formula gives raw n ≈ 384.16, therefore **N2 = 385 relevant PII decisions per denominator**.

For precision, the denominator is predicted-positive PII detections. For recall, the denominator is reference-positive PII entities. Annotation therefore continues until the applicable denominator contains at least 385 observations. F1 is derived from precision and recall.

## RQ3 - Cohesion, grounding, and review quality

Inputs:
- two-sided alpha = .05
- power = .80
- target correlation r = .25

Fisher-z approximation:

```
z_r = atanh(r)
n = ((z_(1-alpha/2) + z_power) / z_r)^2 + 3
```

This gives raw n ≈ 123.3, therefore **N3 = 124 cluster/FAQ observations**.

## RQ4 - Conflict-screening precision

Inputs:
- confidence = 95%
- p = .50
- margin of error = +/- .07

This gives raw n ≈ 196.0, therefore **N4 = 196 reviewed candidate FAQ pairs**.

## Rubric maximum

```
max(1068, 385, 124, 196) = 1068
```

The four RQs use different units of analysis. Therefore, 1,068 is treated as the **preliminary source-corpus target**, while the separate RQ2-RQ4 validation requirements remain in force.
