"""NTI Badge core package."""

name = "nti-badge"
__version__ = "0.1.0"

from nti_badge.badge import render_badge_svg
from nti_badge.certificate import parse_certificate, is_valid_signature, to_index_entry
from nti_badge.crypto import compute_cert_hash, verify_cert_integrity, verify_dilithium_signature
from nti_badge.spec import CERT_SPEC, SUPPORTED_PROFILES, TIERS, tier_for_score
from nti_badge.tiers import assign_tier, tier_metadata
from nti_badge.drift import compute_drift, is_significant_regression
from nti_badge.oidc import verify_oidc_claim, detect_provider

__all__ = [
    "name",
    "__version__",
    "render_badge_svg",
    "parse_certificate",
    "is_valid_signature",
    "to_index_entry",
    "compute_cert_hash",
    "verify_cert_integrity",
    "verify_dilithium_signature",
    "CERT_SPEC",
    "SUPPORTED_PROFILES",
    "TIERS",
    "tier_for_score",
    "assign_tier",
    "tier_metadata",
    "compute_drift",
    "is_significant_regression",
    "verify_oidc_claim",
    "detect_provider",
]
