"""Unit tests for lib/certificate.py"""
import pytest
from lib.certificate import parse_certificate, to_index_entry
from lib.crypto import compute_cert_hash


def _signed(sample_certificate):
    c = dict(sample_certificate); c["cert_hash"] = compute_cert_hash(c); return c


def test_parse_valid_certificate(sample_certificate):
    parsed = parse_certificate(_signed(sample_certificate))
    assert parsed["repo"] == "test/repo"
    assert parsed["score"] == 95


def test_parse_rejects_missing_fields(sample_certificate):
    bad = dict(sample_certificate); del bad["repo"]
    with pytest.raises(ValueError):
        parse_certificate(bad)


def test_parse_rejects_wrong_spec(sample_certificate):
    bad = _signed(sample_certificate); bad["spec"] = "NTI-Cert/2"
    with pytest.raises(ValueError):
        parse_certificate(bad)


def test_parse_rejects_invalid_score(sample_certificate):
    bad = _signed(sample_certificate); bad["score"] = 150
    with pytest.raises(ValueError):
        parse_certificate(bad)


def test_parse_rejects_tampered_hash(sample_certificate):
    bad = _signed(sample_certificate); bad["cert_hash"] = "0" * 64
    with pytest.raises(ValueError):
        parse_certificate(bad)


def test_to_index_entry_extracts_public_fields(sample_certificate):
    cert = _signed(sample_certificate)
    entry = to_index_entry(cert)
    assert entry["repo"] == "test/repo"
    assert entry["score"] == 95
    assert entry["cert_hash"] == cert["cert_hash"]
