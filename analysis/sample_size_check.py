"""Reproduce the Week 1 preliminary sample-size planning calculations.

The script intentionally keeps every assumption explicit so that a mentor can
change the assumptions and immediately see how the required sample changes.

These calculations are planning aids, not final effect-size claims.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, asdict
from typing import Dict, Any

from scipy.stats import norm
from statsmodels.stats.power import TTestPower


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
    """Sample size for estimating one proportion with a Wald-style CI."""
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


def paired_t_sample_size(
    *,
    effect_size_dz: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> tuple[float, int]:
    """Exact paired-t planning sample via the one-sample/paired t-test model.

    For a paired design, Cohen's dz is the mean within-pair difference divided
    by the SD of the within-pair differences.
    """
    if effect_size_dz <= 0:
        raise ValueError("effect_size_dz must be positive.")

    raw_n = TTestPower().solve_power(
        effect_size=effect_size_dz,
        alpha=alpha,
        power=power,
        alternative="two-sided",
    )
    return float(raw_n), math.ceil(float(raw_n))


def paired_z_approximation(
    *,
    effect_size_dz: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> tuple[float, int]:
    """Large-sample z approximation shown for transparency."""
    z_alpha = norm.ppf(1.0 - alpha / 2.0)
    z_beta = norm.ppf(power)
    raw_n = ((z_alpha + z_beta) / effect_size_dz) ** 2
    return raw_n, math.ceil(raw_n)


def correlation_sample_size_fisher_z(
    *,
    r: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> tuple[float, int]:
    """Approximate sample size for testing a non-zero correlation.

    Uses Fisher's z transform:
        z_r = atanh(r)
        n = ((z_(1-alpha/2) + z_power) / z_r)^2 + 3
    """
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

    rq2_z_raw, rq2_z_n = paired_z_approximation(
        effect_size_dz=0.30, alpha=0.05, power=0.80
    )
    rq2_raw, rq2_n = paired_t_sample_size(
        effect_size_dz=0.30, alpha=0.05, power=0.80
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
            assumptions={
                "confidence": 0.95,
                "p": 0.50,
                "margin_of_error": 0.03,
            },
        ),
        "RQ2": SampleSizeResult(
            rq="RQ2",
            unit="paired pre-/post-redaction observations",
            method="paired t-test power analysis",
            raw_n=rq2_raw,
            minimum_n=rq2_n,
            assumptions={
                "alpha": 0.05,
                "power": 0.80,
                "cohens_dz": 0.30,
                "z_approx_raw_n": rq2_z_raw,
                "z_approx_ceiling_n": rq2_z_n,
            },
        ),
        "RQ3": SampleSizeResult(
            rq="RQ3",
            unit="cluster/FAQ observations",
            method="Fisher-z correlation power approximation",
            raw_n=rq3_raw,
            minimum_n=rq3_n,
            assumptions={
                "alpha": 0.05,
                "power": 0.80,
                "target_r": 0.25,
            },
        ),
        "RQ4": SampleSizeResult(
            rq="RQ4",
            unit="human-reviewed candidate FAQ pairs",
            method="95% confidence interval for one proportion",
            raw_n=rq4_raw,
            minimum_n=rq4_n,
            assumptions={
                "confidence": 0.95,
                "p": 0.50,
                "margin_of_error": 0.07,
            },
        ),
    }


def main() -> None:
    results = calculate_all()

    print("QM 640 - Preliminary Sample Size Check")
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
        "Interpretation: use 1,068 as the preliminary source-corpus "
        "planning target; retain the separate RQ-specific validation "
        "requirements because the units of analysis differ."
    )


if __name__ == "__main__":
    main()
