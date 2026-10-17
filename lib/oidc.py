"""Multi-provider OIDC verification re-exported from nti_badge."""
from nti_badge.oidc import (
    JWKS_CACHE,
    JWKS_TTL,
    PROVIDERS,
    detect_provider,
    fetch_jwks,
    verify_oidc_claim,
)

__all__ = [
    "JWKS_CACHE",
    "JWKS_TTL",
    "PROVIDERS",
    "detect_provider",
    "fetch_jwks",
    "verify_oidc_claim",
]
