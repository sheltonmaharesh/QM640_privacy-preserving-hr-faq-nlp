import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "analysis" / "sample_size_check.py"
SPEC = importlib.util.spec_from_file_location("sample_size_check", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def test_rq1_minimum():
    raw, n = MODULE.proportion_ci_sample_size(
        p=0.50, margin_of_error=0.03, confidence=0.95
    )
    assert 1067 < raw < 1068
    assert n == 1068


def test_rq2_minimum_exact_paired_t():
    raw, n = MODULE.paired_t_sample_size(
        effect_size_dz=0.30, alpha=0.05, power=0.80
    )
    assert 89 < raw < 90
    assert n == 90


def test_rq3_minimum():
    raw, n = MODULE.correlation_sample_size_fisher_z(
        r=0.25, alpha=0.05, power=0.80
    )
    assert 123 < raw < 124
    assert n == 124


def test_rq4_minimum():
    raw, n = MODULE.proportion_ci_sample_size(
        p=0.50, margin_of_error=0.07, confidence=0.95
    )
    assert 195 < raw < 196
    assert n == 196


def test_rubric_maximum():
    results = MODULE.calculate_all()
    assert max(r.minimum_n for r in results.values()) == 1068
