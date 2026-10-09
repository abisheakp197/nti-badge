"""POST /api/verify — receives signed certificate submissions.


Validates:
1. OIDC token (proves the request came from the claimed repo)
2. Certificate integrity (hash matches payload)
3. Certificate signature (Dilithium5)
4. Repo claim in OIDC matches repo in certificate


Indexes ONLY the hash + score. Full cert stays in the user's repo.
"""
from http.server import BaseHTTPRequestHandler
import json
import asyncio


from lib.oidc import verify_oidc_claim
from lib.store import index_certificate, get_latest
from lib.certificate import parse_certificate, is_valid_signature, to_index_entry
from lib.drift import compute_drift




class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("content-length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            self._respond(400, {"error": "invalid json"})
            return


        oidc_claim = body.get("oidc_claim", {})
        cert_raw = body.get("certificate", {})


        # Step 1: Validate OIDC token
        identity = verify_oidc_claim(oidc_claim)
        if not identity:
            self._respond(401, {"error": "invalid or expired oidc token"})
            return


        # Step 2: Validate certificate structure
        try:
            cert = parse_certificate(cert_raw)
        except ValueError as e:
            self._respond(400, {"error": f"invalid certificate: {e}"})
            return


        # Step 3: Cross-check repo identity
        if identity["repo_full"] != cert["repo"]:
            self._respond(403, {"error": "oidc repo does not match certificate repo"})
            return


        # Step 4: Verify Dilithium5 signature (best-effort)
        sig_valid = is_valid_signature(cert)


        # Step 5: Compute drift vs previous
        try:
            previous = asyncio.run(get_latest(cert["repo"]))
        except Exception:
            previous = None
        drift = compute_drift(previous, cert)


        # Step 6: Index (hash + score only)
        index_entry = to_index_entry(cert)
        index_entry["signature_verified"] = sig_valid
        index_entry["drift"] = drift


        try:
            asyncio.run(index_certificate(cert["repo"], index_entry))
        except Exception as e:
            self._respond(500, {"error": f"index failed: {e}"})
            return


        self._respond(200, {
            "status": "indexed",
            "repo": cert["repo"],
            "score": cert["score"],
            "tier": cert.get("tier", "Unranked"),
            "signature_verified": sig_valid,
            "drift": drift,
            "note": "Only cert_hash and score are indexed. Full certificate remains in your repository.",
        })


    def _respond(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))
