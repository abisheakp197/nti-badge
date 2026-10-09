"""Certificate signature verification helpers.


Verifies Dilithium5 signatures on NTI-Cert/1 payloads. Supports offline
verification — no network required. This is what makes the certs portable.
"""
import json
import hashlib
from typing import Optional




def compute_cert_hash(payload: dict) -> str:
    """Deterministic hash of the cert payload without the signature field."""
    clean = {k: v for k, v in payload.items() if k not in ("signature", "cert_hash")}
    message = json.dumps(clean, sort_keys=True).encode("utf-8")
    return hashlib.sha256(message).hexdigest()




def verify_dilithium_signature(payload: dict) -> bool:
    """Verify the signature against the embedded public key.


    Uses ube-foundation if available. Falls back to hash-only check.
    """
    sig_hex = payload.get("signature")
    pk_hex = payload.get("issuer_pubkey")
    if not sig_hex or not pk_hex:
        return False
    try:
        from ube_foundation import PqcKeyPair
        clean = {k: v for k, v in payload.items() if k not in ("signature", "cert_hash")}
        message = json.dumps(clean, sort_keys=True).encode("utf-8")
        key = PqcKeyPair.from_public_key_hex(pk_hex) if hasattr(PqcKeyPair, "from_public_key_hex") else None
        if key is None:
            # Fallback: recompute hash integrity
            return compute_cert_hash(payload) == payload.get("cert_hash")
        return key.verify(message, sig_hex)
    except Exception:
        return False




def verify_cert_integrity(payload: dict) -> bool:
    """Verify cert hash matches payload (integrity check)."""
    return compute_cert_hash(payload) == payload.get("cert_hash")
