"""Tampered certificates must be rejected."""
import pytest
from lib.certificate import parse_certificate
from lib.crypto import compute_cert_hash


def _signed(sample_certificate):
    c = dict(sample_certificate); c["cert_hash"] = compute_cert_hash(c); return c


def test_reject_score_tampering(sample_certificate):
    cert = _signed(sample_certificate); cert["score"] = 100
    with pytest.raises(ValueError):
        parse_certificate(cert)


def test_reject_repo_tampering(sample_certificate):
    cert = _signed(sample_certificate); cert["repo"] = "attacker/target"
    with pytest.raises(ValueError):
        parse_certificate(cert)


def test_reject_cert_hash_tampering(sample_certificate):
    cert = _signed(sample_certificate); cert["cert_hash"] = "f" * 64
    with pytest.raises(ValueError):
        parse_certificate(cert)
