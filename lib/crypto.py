"""Certificate signature verification helpers re-exported from nti_badge."""

from nti_badge.crypto import (
    compute_cert_hash,
    register_keypair,
    sign_badge,
    verify_badge,
    verify_badge_offline,
    verify_cert_integrity,
    verify_dilithium_signature,
)

__all__ = [
    "compute_cert_hash",
    "register_keypair",
    "sign_badge",
    "verify_badge",
    "verify_badge_offline",
    "verify_cert_integrity",
    "verify_dilithium_signature",
]
