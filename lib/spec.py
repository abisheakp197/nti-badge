"""NTI-Cert/1 specification constants re-exported from nti_badge."""
from nti_badge.spec import (
    CERT_SPEC,
    SUPPORTED_PROFILES,
    TIERS,
    SEVERITY_LEVELS,
    SUPPORTED_OIDC_ISSUERS,
    tier_for_score,
)

__all__ = [
    "CERT_SPEC",
    "SUPPORTED_PROFILES",
    "TIERS",
    "SEVERITY_LEVELS",
    "SUPPORTED_OIDC_ISSUERS",
    "tier_for_score",
]
