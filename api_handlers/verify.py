"""POST /api/verify — receives signed certificate submissions.

Validates:
1. OIDC token (proves the request came from the claimed repo)
2. Certificate integrity (hash matches payload)
3. Certificate signature (Dilithium5)
4. Repo claim in OIDC matches repo in certificate

Indexes ONLY the hash + score. Full cert stays in the user's repo.
"""

import json

from lib.certificate import is_valid_signature, parse_certificate, to_index_entry
from lib.drift import compute_drift
from lib.oidc import verify_oidc_claim
from lib.store import get_latest, index_certificate


async def run(body_raw: str = "") -> tuple[int, dict[str, str], bytes]:
    headers = {"Content-Type": "application/json"}

    try:
        body = json.loads(body_raw)
    except Exception:  # noqa: BLE001
        return (400, headers, json.dumps({"error": "invalid json"}).encode("utf-8"))

    if not isinstance(body, dict):
        return (400, headers, json.dumps({"error": "request body must be a JSON object"}).encode("utf-8"))

    oidc_claim = body.get("oidc_claim", {})
    cert_raw = body.get("certificate", {})

    # Step 1: Validate OIDC token
    identity = verify_oidc_claim(oidc_claim)
    if not identity:
        return (401, headers, json.dumps({"error": "invalid or expired oidc token"}).encode("utf-8"))

    # Step 2: Validate certificate structure
    try:
        cert = parse_certificate(cert_raw)
    except (ValueError, TypeError) as e:
        return (400, headers, json.dumps({"error": f"invalid certificate: {e}"}).encode("utf-8"))

    # Step 3: Cross-check repo identity
    if identity["repo_full"] != cert["repo"]:
        return (403, headers, json.dumps({"error": "oidc repo does not match certificate repo"}).encode("utf-8"))

    # Step 4: Verify Dilithium5 signature
    sig_valid = is_valid_signature(cert)

    # Step 5: Compute drift vs previous
    try:
        previous = await get_latest(cert["repo"])
    except Exception:  # noqa: BLE001
        previous = None
    drift = compute_drift(previous, cert)

    # Step 6: Index (hash + score only)
    index_entry = to_index_entry(cert)
    index_entry["signature_verified"] = sig_valid
    index_entry["drift"] = drift

    try:
        await index_certificate(cert["repo"], index_entry)
    except Exception:  # noqa: BLE001
        return (500, headers, json.dumps({"error": "index failed"}).encode("utf-8"))

    res_payload = {
        "status": "indexed",
        "repo": cert["repo"],
        "score": cert["score"],
        "tier": cert.get("tier", "Unranked"),
        "signature_verified": sig_valid,
        "drift": drift,
        "note": "Only cert_hash and score are indexed. Full certificate remains in your repository.",
    }
    return (200, headers, json.dumps(res_payload).encode("utf-8"))
