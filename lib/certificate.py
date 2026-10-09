"""NTI-Cert/1 certificate parsing and validation."""
from typing import Optional


from lib.spec import CERT_SPEC, SUPPORTED_PROFILES
from lib.crypto import verify_cert_integrity, verify_dilithium_signature




REQUIRED_FIELDS = [
    "spec", "issuer", "issued_at", "id", "repo", "commit_sha",
    "score", "profile", "signature_alg", "issuer_pubkey",
    "signature", "cert_hash",
]




def parse_certificate(payload: dict) -> dict:
    """Validate structure and return normalized cert or raise ValueError."""
    missing = [f for f in REQUIRED_FIELDS if f not in payload]
    if missing:
        raise ValueError(f"Missing required fields: {missing}")


    if payload["spec"] != CERT_SPEC:
        raise ValueError(f"Unsupported spec: {payload['spec']}")


    if payload["profile"] not in SUPPORTED_PROFILES:
        raise ValueError(f"Unsupported profile: {payload['profile']}")


    if not isinstance(payload["score"], int) or not (0 <= payload["score"] <= 100):
        raise ValueError("Score must be integer 0-100")


    if not verify_cert_integrity(payload):
        raise ValueError("Certificate hash mismatch — payload has been tampered with")


    return payload




def is_valid_signature(payload: dict) -> bool:
    return verify_dilithium_signature(payload)




def to_index_entry(payload: dict) -> dict:
    """Extract only the fields needed for the public registry index."""
    return {
        "repo": payload["repo"],
        "score": payload["score"],
        "cert_hash": payload["cert_hash"],
        "commit_sha": payload["commit_sha"],
        "timestamp": payload["issued_at"],
        "issuer_pubkey": payload["issuer_pubkey"],
        "signature": payload["signature"],
        "tier": payload.get("tier", "Unranked"),
        "profile": payload["profile"],
    }
