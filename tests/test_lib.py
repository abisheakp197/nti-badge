"""Unit tests for library modules: crypto, oidc, store, certificate, tiers, drift, spec."""
import time
import pytest
from lib.spec import CERT_SPEC, SUPPORTED_PROFILES, TIERS, tier_for_score
from lib.crypto import compute_cert_hash, verify_cert_integrity, verify_dilithium_signature
from lib.tiers import assign_tier, tier_metadata
from lib.drift import compute_drift, is_significant_regression
from lib.certificate import parse_certificate, to_index_entry, is_valid_signature
from lib.oidc import verify_oidc_claim, detect_provider
import lib.store as store


def test_spec_and_tiers():
    assert tier_for_score(98) == "Platinum"
    assert tier_for_score(88) == "Gold"
    assert tier_for_score(75) == "Silver"
    assert tier_for_score(55) == "Bronze"
    assert tier_for_score(40) == "Unranked"

    assert assign_tier(90) == "Gold"
    meta = tier_metadata("Gold")
    assert meta["name"] == "Gold"
    assert meta["color"] == "#ffd700"
    assert meta["emoji"] == "🥇"


def test_crypto_hash_and_integrity():
    payload = {
        "spec": CERT_SPEC,
        "issuer": "nti",
        "issued_at": "2025-01-01T00:00:00Z",
        "id": "cert_123",
        "repo": "owner/repo",
        "commit_sha": "abc1234",
        "score": 90,
        "profile": "NTI-1",
        "signature_alg": "Dilithium5",
        "issuer_pubkey": "0x123",
        "signature": "0xsig",
    }
    cert_hash = compute_cert_hash(payload)
    assert isinstance(cert_hash, str)
    assert len(cert_hash) == 64  # sha256 hex string

    payload_with_hash = dict(payload, cert_hash=cert_hash)
    assert verify_cert_integrity(payload_with_hash) is True

    payload_tampered = dict(payload_with_hash, score=50)
    assert verify_cert_integrity(payload_tampered) is False

    # verify_dilithium_signature fallback returns False if ube_foundation import fails or isn't present
    assert isinstance(verify_dilithium_signature(payload_with_hash), bool)


def test_drift_detection():
    # First scan
    drift1 = compute_drift(None, {"score": 80})
    assert drift1["direction"] == "first_scan"
    assert drift1["delta"] == 0

    # Improved
    drift2 = compute_drift({"score": 80}, {"score": 90})
    assert drift2["direction"] == "improved"
    assert drift2["delta"] == 10

    # Regressed
    drift3 = compute_drift({"score": 90}, {"score": 75})
    assert drift3["direction"] == "regressed"
    assert drift3["delta"] == -15
    assert is_significant_regression(drift3, threshold=10) is True


def test_certificate_parsing():
    raw_payload = {
        "spec": CERT_SPEC,
        "issuer": "nti",
        "issued_at": "2025-01-01T00:00:00Z",
        "id": "cert_123",
        "repo": "owner/repo",
        "commit_sha": "abc1234",
        "score": 85,
        "profile": "NTI-1",
        "signature_alg": "Dilithium5",
        "issuer_pubkey": "0x123",
        "signature": "0xsig",
    }
    # Note: cert_hash is calculated on payload without 'signature' or 'cert_hash'
    # 'tier' is optional and not part of compute_cert_hash exclusions if it's in payload
    cert_hash = compute_cert_hash(raw_payload)
    cert = dict(raw_payload, cert_hash=cert_hash)

    parsed = parse_certificate(cert)
    assert parsed["repo"] == "owner/repo"

    index_entry = to_index_entry(parsed)
    assert index_entry["repo"] == "owner/repo"
    assert index_entry["score"] == 85
    assert index_entry["cert_hash"] == cert_hash

    # Missing field error
    invalid_cert = dict(cert)
    del invalid_cert["repo"]
    with pytest.raises(ValueError, match="Missing required fields"):
        parse_certificate(invalid_cert)


def test_oidc_verification():
    now = time.time() + 300
    github_claim = {
        "iss": "https://token.actions.githubusercontent.com",
        "aud": "nti-badge",
        "exp": now,
        "repository": "owner/repo",
        "sub": "repo:owner/repo:ref:refs/heads/main",
    }
    assert detect_provider(github_claim) == "github"
    res = verify_oidc_claim(github_claim)
    assert res is not None
    assert res["provider"] == "github"
    assert res["repo_full"] == "owner/repo"


@pytest.mark.asyncio
async def test_store_fallback_in_memory(temp_store):
    # Without REDIS_URL, store returns empty structures gracefully
    assert await store.get_latest("owner/repo") is None
    assert await store.get_history("owner/repo") == []
    assert await store.list_all() == []
    assert await store.top_scores() == []
    assert await store.list_by_org("owner") == []
