"""Forged OIDC tokens must be rejected."""
from lib.oidc import verify_oidc_claim


def test_reject_wrong_issuer():
    claim = {
        "iss": "https://attacker.example.com",
        "aud": "nti-badge",
        "exp": 9999999999,
        "repository": "test/repo",
    }
    assert verify_oidc_claim(claim) is None


def test_reject_wrong_audience():
    claim = {
        "iss": "https://token.actions.githubusercontent.com",
        "aud": "other-service",
        "exp": 9999999999,
        "repository": "test/repo",
    }
    assert verify_oidc_claim(claim) is None


def test_reject_missing_repo():
    claim = {
        "iss": "https://token.actions.githubusercontent.com",
        "aud": "nti-badge",
        "exp": 9999999999,
    }
    assert verify_oidc_claim(claim) is None
