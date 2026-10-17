"""NTI Badge core package."""

name = "nti-badge"
__version__ = "0.1.0"

from nti_badge.badge import render_badge_svg
from nti_badge.certificate import is_valid_signature, parse_certificate, to_index_entry
from nti_badge.crypto import (
    compute_cert_hash,
    register_keypair,
    sign_badge,
    verify_badge,
    verify_badge_offline,
    verify_cert_integrity,
    verify_dilithium_signature,
)
from nti_badge.drift import compute_drift, is_significant_regression
from nti_badge.oidc import detect_provider, verify_oidc_claim
from nti_badge.spec import CERT_SPEC, SUPPORTED_PROFILES, TIERS, tier_for_score
from nti_badge.tiers import assign_tier, tier_metadata

__all__ = [
    "CERT_SPEC",
    "SUPPORTED_PROFILES",
    "TIERS",
    "__version__",
    "assign_tier",
    "compute_cert_hash",
    "compute_drift",
    "detect_provider",
    "is_significant_regression",
    "is_valid_signature",
    "name",
    "parse_certificate",
    "register_keypair",
    "render_badge_svg",
    "sign_badge",
    "tier_for_score",
    "tier_metadata",
    "to_index_entry",
    "verify_badge",
    "verify_badge_offline",
    "verify_cert_integrity",
    "verify_dilithium_signature",
    "verify_oidc_claim",
]
