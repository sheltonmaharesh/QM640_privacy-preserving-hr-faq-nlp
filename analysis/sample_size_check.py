"""Reproduce the Week 1 preliminary sample-size planning calculations.

These calculations mirror the draft synopsis. They are planning aids, not
final effect-size claims. Each research question uses the method that matches
its planned metric.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict

from scipy.stats import norm


@dataclass(frozen=True)
class SampleSizeResult:
    rq: str
    unit: str
    method: str
    raw_n: float
    minimum_n: int
    assumptions: Dict[str, Any]


def proportion_ci_sample_size(
    *,
    p: float,
    margin_of_error: float,
    confidence: float = 0.95,
) -> tuple[float, int]:
    """Sample size for estimating one proportion with a normal-approximation CI."""
    if not 0 < p < 1:
        raise ValueError("p must be between 0 and 1.")
    if not 0 < margin_of_error < 1:
        raise ValueError("margin_of_error must be between 0 and 1.")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1.")

    alpha = 1.0 - confidence
    z = norm.ppf(1.0 - alpha / 2.0)
    raw_n = (z**2 * p * (1.0 - p)) / (margin_of_error**2)
    return raw_n, math.ceil(raw_n)


def correlation_sample_size_fisher_z(
    *,
    r: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> tuple[float, int]:
    """Approximate sample size for testing a non-zero correlation."""
    if not -1 < r < 1 or r == 0:
        raise ValueError("r must be between -1 and 1 and non-zero.")

    z_r = math.atanh(abs(r))
    z_alpha = norm.ppf(1.0 - alpha / 2.0)
    z_beta = norm.ppf(power)
    raw_n = ((z_alpha + z_beta) / z_r) ** 2 + 3.0
    return raw_n, math.ceil(raw_n)


def calculate_all() -> dict[str, SampleSizeResult]:
    rq1_raw, rq1_n = proportion_ci_sample_size(
        p=0.50, margin_of_error=0.03, confidence=0.95
    )

    # RQ2 evaluates PII precision and recall. Both are proportions, so the
    # planning target is based on CI precision for the relevant denominator.
    rq2_raw, rq2_n = proportion_ci_sample_size(
        p=0.50, margin_of_error=0.05, confidence=0.95
    )

    rq3_raw, rq3_n = correlation_sample_size_fisher_z(
        r=0.25, alpha=0.05, power=0.80
    )

    rq4_raw, rq4_n = proportion_ci_sample_size(
        p=0.50, margin_of_error=0.07, confidence=0.95
    )

    return {
        "RQ1": SampleSizeResult(
            rq="RQ1",
            unit="eligible HR email threads",
            method="95% confidence interval for one proportion",
            raw_n=rq1_raw,
            minimum_n=rq1_n,
            assumptions={"confidence": 0.95, "p": 0.50, "margin_of_error": 0.03},
        ),
        "RQ2": SampleSizeResult(
            rq="RQ2",
            unit="PII decisions in each relevant precision/recall denominator",
            method="95% confidence interval for precision/recall proportions",
            raw_n=rq2_raw,
            minimum_n=rq2_n,
            assumptions={"confidence": 0.95, "p": 0.50, "margin_of_error": 0.05},
        ),
        "RQ3": SampleSizeResult(
            rq="RQ3",
            unit="cluster/FAQ observations",
            method="Fisher-z correlation power approximation",
            raw_n=rq3_raw,
            minimum_n=rq3_n,
            assumptions={"alpha": 0.05, "power": 0.80, "target_r": 0.25},
        ),
        "RQ4": SampleSizeResult(
            rq="RQ4",
            unit="human-reviewed candidate FAQ pairs",
            method="95% confidence interval for one proportion",
            raw_n=rq4_raw,
            minimum_n=rq4_n,
            assumptions={"confidence": 0.95, "p": 0.50, "margin_of_error": 0.07},
        ),
    }


def main() -> None:
    results = calculate_all()

    print("QM640 - Preliminary Sample Size Check")
    print("=" * 46)

    for key in ("RQ1", "RQ2", "RQ3", "RQ4"):
        result = results[key]
        print(f"\n{key}")
        print(f"  Method:    {result.method}")
        print(f"  Unit:      {result.unit}")
        print(f"  Raw n:     {result.raw_n:.3f}")
        print(f"  Minimum n: {result.minimum_n}")
        print(f"  Inputs:    {result.assumptions}")

    minima = {key: result.minimum_n for key, result in results.items()}
    maximum = max(minima.values())

    print("\n" + "-" * 46)
    print(f"Rubric maximum of RQ minima: {maximum}")
    print(
        "Interpretation: 1,068 is the preliminary source-corpus target; "
        "RQ2-RQ4 retain their own validation quotas because units differ."
    )


if __name__ == "__main__":
    main()
