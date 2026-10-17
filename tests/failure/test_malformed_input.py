"""Malformed input must never crash."""

from typing import Any

import pytest


def test_parse_certificate_handles_empty_dict() -> None:
    from lib.certificate import parse_certificate
    with pytest.raises(ValueError):
        parse_certificate({})


def test_parse_certificate_handles_none() -> None:
    from lib.certificate import parse_certificate
    bad: Any = None
    with pytest.raises((ValueError, TypeError)):
        parse_certificate(bad)


def test_parse_certificate_handles_string() -> None:
    from lib.certificate import parse_certificate
    bad: Any = "not a dict"
    with pytest.raises((ValueError, TypeError)):
        parse_certificate(bad)


def test_oidc_handles_missing_claims() -> None:
    from lib.oidc import verify_oidc_claim
    assert verify_oidc_claim({}) is None


def test_oidc_handles_expired_token() -> None:
    from lib.oidc import verify_oidc_claim
    expired: dict[str, Any] = {
        "iss": "https://token.actions.githubusercontent.com",
        "aud": "nti-badge",
        "exp": 1,
        "repository": "test/repo",
    }
    assert verify_oidc_claim(expired) is None
