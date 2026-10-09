"""GET /api/federation — federation protocol manifest.


This endpoint makes NTI a protocol, not a product. Any organization can
read this manifest and stand up their own mirror. That is what makes NTI
neutral and un-killable.
"""
from http.server import BaseHTTPRequestHandler
import json




MANIFEST = {
    "protocol": "NTI-Cert/1",
    "federation_version": "1.0",
    "description": (
        "NTI is a federated certificate protocol. This registry is one node. "
        "Any party may run a mirror or their own private federation. "
        "Certificates are portable and verifiable offline."
    ),
    "endpoints": {
        "verify": "POST /api/verify",
        "badge": "GET /api/badge?repo=owner/repo",
        "certificate": "GET /api/certificate?repo=owner/repo",
        "registry": "GET /api/registry",
        "leaderboard": "GET /api/leaderboard",
        "transparency": "GET /api/transparency",
        "org": "GET /api/org?name=<org>",
        "federation_manifest": "GET /api/federation",
    },
    "mirror_howto": {
        "step_1": "Clone github.com/abisheakp197/nti-badge",
        "step_2": "Deploy to Vercel (or any Python serverless platform)",
        "step_3": "Attach a KV/Redis store",
        "step_4": "Announce your mirror. Clients can use it via the registry-url input.",
    },
    "cert_format": {
        "spec": "NTI-Cert/1",
        "signature_alg": "Dilithium5",
        "fields_required": [
            "spec", "issuer", "issued_at", "id", "repo", "commit_sha",
            "score", "profile", "signature_alg", "issuer_pubkey",
            "signature", "cert_hash",
        ],
    },
    "verification_offline": "nti-scanner verify ./nti-certificate.json",
    "license": "Apache-2.0",
    "neutrality": (
        "No central authority. No data custody. Certificates live in the user's "
        "repository. This registry indexes only {repo, score, cert_hash, timestamp}."
    ),
}




class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(MANIFEST, indent=2).encode("utf-8"))
