"""Shared fixtures for the NTI test suite."""

import shutil
import pytest


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Every test starts with a clean environment."""
    for var in ["NTI_MODE", "NTI_NODE_URL", "NTI_NODE_NAME", "KV_URL", "REDIS_URL",
                "UPSTASH_REDIS_REST_URL", "UPSTASH_REDIS_REST_TOKEN",
                "NTI_HUB_URLS", "NTI_LOCAL_STORE"]:
        monkeypatch.delenv(var, raising=False)
    yield


@pytest.fixture
def temp_store(tmp_path, monkeypatch):
    """Temp directory for file-based DB tests."""
    store_dir = tmp_path / "nti-data"
    monkeypatch.setenv("NTI_LOCAL_STORE", str(store_dir))
    import importlib
    import lib.db
    import lib.store
    importlib.reload(lib.db)
    importlib.reload(lib.store)
    yield store_dir
    if store_dir.exists():
        shutil.rmtree(store_dir, ignore_errors=True)


@pytest.fixture
def standalone_mode(monkeypatch):
    monkeypatch.setenv("NTI_MODE", "standalone")
    yield "standalone"


@pytest.fixture
def federated_mode(monkeypatch):
    monkeypatch.setenv("NTI_MODE", "federated")
    monkeypatch.setenv("NTI_NODE_URL", "https://test-node.example.com")
    monkeypatch.setenv("NTI_HUB_URLS", "https://hub1.example.com,https://hub2.example.com")
    yield "federated"


@pytest.fixture
def hub_mode(monkeypatch):
    monkeypatch.setenv("NTI_MODE", "hub")
    monkeypatch.setenv("NTI_NODE_URL", "https://test-hub.example.com")
    monkeypatch.setenv("NTI_HUB_URLS", "https://hub-upstream.example.com")
    yield "hub"


@pytest.fixture
def sample_certificate():
    return {
        "spec": "NTI-Cert/1",
        "issuer": "https://github.com/test/repo",
        "issued_at": "2026-01-15T10:00:00Z",
        "id": "00000000-0000-0000-0000-000000000001",
        "repo": "test/repo",
        "commit_sha": "abc123def456",
        "score": 95,
        "profile": "NTI-1",
        "signature_alg": "Dilithium5",
        "issuer_pubkey": "aabbccddeeff",
        "signature": "112233445566",
        "cert_hash": "",
        "tier": "Platinum",
    }


@pytest.fixture
def valid_oidc_claim():
    return {
        "iss": "https://token.actions.githubusercontent.com",
        "aud": "nti-badge",
        "exp": 9999999999,
        "repository": "test/repo",
        "sub": "repo:test/repo:ref:refs/heads/main",
        "sha": "abc123def456",
    }
