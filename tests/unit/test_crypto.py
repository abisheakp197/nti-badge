"""Unit tests for lib/crypto.py"""
import pytest
from lib.crypto import compute_cert_hash, verify_cert_integrity


def test_compute_cert_hash_deterministic(sample_certificate):
    h1 = compute_cert_hash(sample_certificate)
    h2 = compute_cert_hash(sample_certificate)
    assert h1 == h2
    assert len(h1) == 64


def test_hash_ignores_signature_and_cert_hash(sample_certificate):
    cert_a = dict(sample_certificate); cert_a["signature"] = "aaaa"; cert_a["cert_hash"] = "bbbb"
    cert_b = dict(sample_certificate); cert_b["signature"] = "cccc"; cert_b["cert_hash"] = "dddd"
    assert compute_cert_hash(cert_a) == compute_cert_hash(cert_b)


def test_integrity_check_passes(sample_certificate):
    h = compute_cert_hash(sample_certificate)
    cert = dict(sample_certificate); cert["cert_hash"] = h
    assert verify_cert_integrity(cert) is True


def test_integrity_check_fails_on_tamper(sample_certificate):
    cert = dict(sample_certificate); cert["cert_hash"] = "deadbeef" * 8
    assert verify_cert_integrity(cert) is False


def test_integrity_check_fails_on_field_change(sample_certificate):
    h = compute_cert_hash(sample_certificate)
    cert = dict(sample_certificate); cert["cert_hash"] = h; cert["score"] = 50
    assert verify_cert_integrity(cert) is False
