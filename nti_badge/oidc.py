"""Multi-provider OIDC verification.

Supports GitHub Actions, GitLab CI, Google Cloud, Azure DevOps, and custom
OIDC issuers. The badge is ecosystem-agnostic by design — it is a federated
protocol, not a GitHub-only product.
"""

import time
from typing import Any

import httpx

JWKS_CACHE: dict[str, dict[str, Any]] = {}
JWKS_TTL = 3600

PROVIDERS = {
    "github": {
        "config_url": "https://token.actions.githubusercontent.com/.well-known/openid-configuration",
        "audience": "nti-badge",
        "repo_claim": "repository",
    },
    "gitlab": {
        "config_url": "https://gitlab.com/.well-known/openid-configuration",
        "audience": "nti-badge",
        "repo_claim": "project_path",
    },
    "google": {
        "config_url": "https://accounts.google.com/.well-known/openid-configuration",
        "audience": "nti-badge",
        "repo_claim": "sub",
    },
    "azure": {
        "config_url": "https://login.microsoftonline.com/common/v2.0/.well-known/openid-configuration",
        "audience": "nti-badge",
        "repo_claim": "sub",
    },
}


async def fetch_jwks(provider: str) -> dict[str, Any]:
    entry = JWKS_CACHE.get(provider, {})
    if entry.get("keys") and time.time() - float(entry.get("fetched_at", 0)) < JWKS_TTL:
        res_keys: dict[str, Any] = entry["keys"]
        return res_keys
    cfg = PROVIDERS.get(provider)
    if not cfg:
        return {}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(cfg["config_url"])
        r.raise_for_status()
        jwks_uri = str(r.json().get("jwks_uri"))
        r2 = await client.get(jwks_uri)
        r2.raise_for_status()
        keys_data: dict[str, Any] = r2.json()
        JWKS_CACHE[provider] = {"keys": keys_data, "fetched_at": time.time()}
        return keys_data


def detect_provider(payload: dict[str, Any]) -> str | None:
    if not isinstance(payload, dict):
        return None
    iss = str(payload.get("iss", ""))
    for name, cfg in PROVIDERS.items():
        if cfg["config_url"].split("/.well-known")[0] in iss:
            return name
    return None


def verify_oidc_claim(token_payload: dict[str, Any], expected_repo: str | None = None) -> dict[str, Any] | None:
    """Validate OIDC claims. Returns normalized identity or None."""
    if not isinstance(token_payload, dict):
        return None

    provider = detect_provider(token_payload)
    if not provider:
        return None

    cfg = PROVIDERS[provider]

    exp = token_payload.get("exp", 0)
    if not isinstance(exp, (int, float)) or exp < time.time():
        return None

    aud = token_payload.get("aud")
    audiences = aud if isinstance(aud, list) else [aud] if aud else []
    if cfg["audience"] not in audiences:
        return None

    repo = token_payload.get(cfg["repo_claim"])
    if not repo:
        return None

    # Normalize: strip URL prefixes for gitlab/google/azure
    if provider == "gitlab" and isinstance(repo, str):
        repo = repo.rstrip("/")
    if expected_repo and repo != expected_repo:
        return None

    return {
        "provider": provider,
        "repo_full": repo,
        "subject": token_payload.get("sub", ""),
        "issuer": token_payload.get("iss", ""),
        "raw_claims": {
            "sha": token_payload.get("sha") or token_payload.get("commit_sha", ""),
            "ref": token_payload.get("ref", ""),
            "actor": token_payload.get("actor") or token_payload.get("user_login", ""),
        },
    }
