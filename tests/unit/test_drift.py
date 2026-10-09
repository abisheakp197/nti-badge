"""Unit tests for lib/drift.py"""
from lib.drift import compute_drift, is_significant_regression


def test_first_scan():
    d = compute_drift(None, {"score": 80})
    assert d["direction"] == "first_scan"


def test_improved():
    d = compute_drift({"score": 70}, {"score": 85})
    assert d["direction"] == "improved"
    assert d["delta"] == 15


def test_regressed():
    d = compute_drift({"score": 90}, {"score": 60})
    assert d["direction"] == "regressed"
    assert d["delta"] == -30


def test_stable():
    d = compute_drift({"score": 80}, {"score": 80})
    assert d["direction"] == "stable"


def test_significant_regression():
    d = compute_drift({"score": 90}, {"score": 60})
    assert is_significant_regression(d, threshold=10) is True


def test_insignificant_regression():
    d = compute_drift({"score": 90}, {"score": 85})
    assert is_significant_regression(d, threshold=10) is False
