"""Malformed input must never crash."""
import pytest


def test_parse_certificate_handles_empty_dict():
    from lib.certificate import parse_certificate
    with pytest.raises(ValueError):
        parse_certificate({})


def test_parse_certificate_handles_none():
    from lib.certificate import parse_certificate
    with pytest.raises((ValueError, TypeError)):
        parse_certificate(None)


def test_parse_certificate_handles_string():
    from lib.certificate import parse_certificate
    with pytest.raises((ValueError, TypeError)):
        parse_certificate("not a dict")


def test_oidc_handles_missing_claims():
    from lib.oidc import verify_oidc_claim
    assert verify_oidc_claim({}) is None


def test_oidc_handles_expired_token():
    from lib.oidc import verify_oidc_claim
    expired = {
        "iss": "https://token.actions.githubusercontent.com",
        "aud": "nti-badge",
        "exp": 1,
        "repository": "test/repo",
    }
    assert verify_oidc_claim(expired) is None
