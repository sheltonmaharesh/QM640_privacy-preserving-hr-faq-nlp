# Preliminary sample-size planning

These calculations reproduce the Week 1 synopsis planning assumptions. They are included because the synopsis rubric explicitly asks for a method, parameters, stepwise calculation, and a maximum across RQ1-RQ4.

They are **not final effect-size claims**. The assumptions should be revisited after the literature review, data audit, and mentor feedback.

## RQ1 - Recurring-topic coverage

Goal: estimate the proportion of eligible threads assignable to recurring topics.

Inputs:

- confidence = 95%
- p = 0.50 (conservative maximum-variance assumption)
- margin of error = +/- 0.03

Formula:

```
n = z^2 * p * (1-p) / e^2
```

Using the exact 97.5th percentile of the standard normal distribution gives raw n ≈ 1067.07, therefore **N1 = 1,068 eligible threads**.

## RQ2 - PII redaction and semantic preservation

Goal: compare the same observation before and after redaction.

Planning inputs:

- two-sided alpha = .05
- power = .80
- paired standardized effect dz = .30

The report may show the large-sample z approximation for transparency, but the repository checks the requirement with an **exact paired-t power calculation** using `statsmodels.stats.power.TTestPower`.

- z approximation: raw n ≈ 87.21, ceiling 88
- paired-t power solution: raw n ≈ 89.15, therefore **N2 = 90 paired observations**

Using 90 is more defensible than simply adding an arbitrary allowance to the z approximation.

## RQ3 - Cohesion, grounding, and review quality

Goal: plan for a small-to-moderate association.

Inputs:

- two-sided alpha = .05
- power = .80
- target correlation r = .25

Fisher-z approximation:

```
z_r = atanh(r)
n = ((z_(1-alpha/2) + z_power) / z_r)^2 + 3
```

This gives raw n ≈ 123.32, therefore **N3 = 124 cluster/FAQ observations**.

## RQ4 - Conflict-screening precision

Goal: estimate the precision of the conflict-screening signal after human review.

Inputs:

- confidence = 95%
- p = .50 because precision is unknown at Week 1
- margin of error = +/- .07

This gives raw n ≈ 195.99, therefore **N4 = 196 reviewed candidate FAQ pairs**.

## Rubric maximum

```
max(1068, 90, 124, 196) = 1068
```

The four RQs use different units of analysis. Therefore, 1,068 is treated as the **preliminary source-corpus target**, while the separate RQ2-RQ4 validation requirements remain in force.
