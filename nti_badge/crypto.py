"""Certificate signature verification helpers.

Verifies Dilithium5 signatures on NTI-Cert/1 payloads. Supports offline
verification — no network required. This is what makes the certs portable.
"""

import hashlib
import hmac
import json
from typing import Any

_KEY_REGISTRY: dict[str, Any] = {}


def register_keypair(keypair: Any) -> str:
    """Register a keypair instance and return its public key hex."""
    pk_hex: str = keypair.public_key_hex()
    _KEY_REGISTRY[pk_hex] = keypair
    return pk_hex


def compute_cert_hash(payload: dict[str, Any]) -> str:
    """Deterministic hash of the cert payload without the signature/cert_hash fields."""
    clean = {k: v for k, v in payload.items() if k not in ("signature", "cert_hash")}
    message = json.dumps(clean, sort_keys=True).encode("utf-8")
    return hashlib.sha256(message).hexdigest()


def verify_cert_integrity(payload: dict[str, Any]) -> bool:
    """Verify cert hash matches payload using constant-time comparison."""
    expected_hash = compute_cert_hash(payload)
    actual_hash = payload.get("cert_hash")
    if not isinstance(actual_hash, str):
        return False
    return hmac.compare_digest(expected_hash, actual_hash)


def sign_badge(payload: dict[str, Any], keypair: Any | None = None) -> dict[str, Any]:
    """Sign a badge payload with Dilithium5 using ube_foundation.PqcKeyPair."""
    if keypair is None:
        from ube_foundation import PqcKeyPair  # type: ignore[import-untyped]
        keypair = PqcKeyPair()

    pk_hex = register_keypair(keypair)
    payload["issuer_pubkey"] = pk_hex

    clean = {k: v for k, v in payload.items() if k not in ("signature", "cert_hash")}
    message = json.dumps(clean, sort_keys=True).encode("utf-8")
    sig_hex: str = keypair.sign(message)

    payload["signature"] = sig_hex
    payload["cert_hash"] = compute_cert_hash(payload)
    return payload


def verify_dilithium_signature(payload: dict[str, Any]) -> bool:
    """Verify the Dilithium5 signature against the issuer public key.

    Does NOT fall back to hash check. Returns False if key or signature is invalid.
    """
    sig_hex = payload.get("signature")
    pk_hex = payload.get("issuer_pubkey")
    if not isinstance(sig_hex, str) or not isinstance(pk_hex, str) or not sig_hex or not pk_hex:
        return False

    key = _KEY_REGISTRY.get(pk_hex)
    if key is None:
        try:
            from ube_foundation import PqcKeyPair
            if hasattr(PqcKeyPair, "from_public_key_hex"):
                key = PqcKeyPair.from_public_key_hex(pk_hex)
        except Exception:  # noqa: BLE001
            key = None

    if key is None:
        return False

    try:
        clean = {k: v for k, v in payload.items() if k not in ("signature", "cert_hash")}
        message = json.dumps(clean, sort_keys=True).encode("utf-8")
        res: bool = key.verify(message, sig_hex)
        return res
    except Exception:  # noqa: BLE001
        return False


def verify_badge(payload: dict[str, Any]) -> bool:
    """Verify both integrity hash and Dilithium5 signature."""
    if not verify_cert_integrity(payload):
        return False
    return verify_dilithium_signature(payload)


def verify_badge_offline(payload: dict[str, Any], pubkey: str | None = None) -> bool:
    """Offline verification of badge JSON payload."""
    if pubkey is not None:
        issuer_pk = payload.get("issuer_pubkey")
        if not isinstance(issuer_pk, str) or not hmac.compare_digest(pubkey, issuer_pk):
            return False
    return verify_badge(payload)
