"""NTI-Cert/1 specification constants re-exported from nti_badge."""
from nti_badge.spec import (
    CERT_SPEC,
    SEVERITY_LEVELS,
    SUPPORTED_OIDC_ISSUERS,
    SUPPORTED_PROFILES,
    TIERS,
    tier_for_score,
)

__all__ = [
    "CERT_SPEC",
    "SEVERITY_LEVELS",
    "SUPPORTED_OIDC_ISSUERS",
    "SUPPORTED_PROFILES",
    "TIERS",
    "tier_for_score",
]
