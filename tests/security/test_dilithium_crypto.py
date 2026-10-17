"""Category 5 Cryptographic Correctness Tests: Dilithium5 signature & offline verification."""

from typing import Any

from ube_foundation import PqcKeyPair  # type: ignore[import-untyped]

from nti_badge.crypto import (
    compute_cert_hash,
    sign_badge,
    verify_badge,
    verify_badge_offline,
    verify_cert_integrity,
    verify_dilithium_signature,
)


def test_valid_badge_signing_and_verification(sample_certificate: dict[str, Any]) -> None:
    kp = PqcKeyPair()
    badge = dict(sample_certificate)
    signed = sign_badge(badge, keypair=kp)

    assert verify_cert_integrity(signed) is True
    assert verify_dilithium_signature(signed) is True
    assert verify_badge(signed) is True
    assert verify_badge_offline(signed, pubkey=kp.public_key_hex()) is True


def test_tampered_score_rejected(sample_certificate: dict[str, Any]) -> None:
    kp = PqcKeyPair()
    badge = dict(sample_certificate)
    signed = sign_badge(badge, keypair=kp)

    tampered = dict(signed)
    tampered["score"] = 10
    tampered["cert_hash"] = compute_cert_hash(tampered)

    assert verify_dilithium_signature(tampered) is False
    assert verify_badge(tampered) is False


def test_tampered_subject_rejected(sample_certificate: dict[str, Any]) -> None:
    kp = PqcKeyPair()
    badge = dict(sample_certificate)
    signed = sign_badge(badge, keypair=kp)

    tampered = dict(signed)
    tampered["repo"] = "victim/repo"
    tampered["cert_hash"] = compute_cert_hash(tampered)

    assert verify_dilithium_signature(tampered) is False
    assert verify_badge(tampered) is False


def test_wrong_public_key_rejected(sample_certificate: dict[str, Any]) -> None:
    kp1 = PqcKeyPair()
    kp2 = PqcKeyPair()

    badge = dict(sample_certificate)
    signed = sign_badge(badge, keypair=kp1)

    assert verify_badge_offline(signed, pubkey=kp2.public_key_hex()) is False


def test_empty_signature_rejected(sample_certificate: dict[str, Any]) -> None:
    badge = dict(sample_certificate)
    badge["signature"] = ""
    badge["issuer_pubkey"] = "aabb"

    assert verify_dilithium_signature(badge) is False
    assert verify_badge(badge) is False


def test_truncated_signature_rejected(sample_certificate: dict[str, Any]) -> None:
    kp = PqcKeyPair()
    badge = dict(sample_certificate)
    signed = sign_badge(badge, keypair=kp)

    truncated = dict(signed)
    truncated["signature"] = signed["signature"][:10]

    assert verify_dilithium_signature(truncated) is False
    assert verify_badge(truncated) is False


def test_bit_flipped_signature_rejected(sample_certificate: dict[str, Any]) -> None:
    kp = PqcKeyPair()
    badge = dict(sample_certificate)
    signed = sign_badge(badge, keypair=kp)

    sig = signed["signature"]
    # Flip first character hex digit
    flipped_char = "0" if sig[0] != "0" else "1"
    flipped_sig = flipped_char + sig[1:]

    bit_flipped = dict(signed)
    bit_flipped["signature"] = flipped_sig

    assert verify_dilithium_signature(bit_flipped) is False
    assert verify_badge(bit_flipped) is False


def test_unknown_issuer_pubkey_rejected(sample_certificate: dict[str, Any]) -> None:
    badge = dict(sample_certificate)
    badge["issuer_pubkey"] = "11223344556677889900aabbccddeeff"
    badge["signature"] = "aabbcc"

    assert verify_dilithium_signature(badge) is False
    assert verify_badge(badge) is False
