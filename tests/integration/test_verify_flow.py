"""End-to-end: verify a certificate through the system."""

import asyncio
from pathlib import Path
from typing import Any

from lib.certificate import parse_certificate, to_index_entry
from lib.crypto import compute_cert_hash
from lib.oidc import verify_oidc_claim
from lib.store import get_latest, index_certificate


def _signed(sample_certificate: dict[str, Any]) -> dict[str, Any]:
    c = dict(sample_certificate)
    c["cert_hash"] = compute_cert_hash(c)
    return c


def test_full_verify_flow(temp_store: Path, sample_certificate: dict[str, Any], valid_oidc_claim: dict[str, Any]) -> None:
    cert = _signed(sample_certificate)

    identity = verify_oidc_claim(valid_oidc_claim)
    assert identity is not None
    assert identity["repo_full"] == "test/repo"

    parsed = parse_certificate(cert)
    assert parsed["repo"] == "test/repo"
    assert identity["repo_full"] == parsed["repo"]

    entry = to_index_entry(parsed)
    asyncio.run(index_certificate(parsed["repo"], entry))

    retrieved = asyncio.run(get_latest("test/repo"))
    assert retrieved is not None
    assert retrieved["score"] == 95


def test_verify_rejects_oidc_repo_mismatch(temp_store: Path, sample_certificate: dict[str, Any], valid_oidc_claim: dict[str, Any]) -> None:
    cert = _signed(sample_certificate)
    cert["repo"] = "attacker/repo"
    cert["cert_hash"] = compute_cert_hash(cert)
    identity = verify_oidc_claim(valid_oidc_claim)
    assert identity is not None
    parsed = parse_certificate(cert)
    assert identity["repo_full"] != parsed["repo"]
