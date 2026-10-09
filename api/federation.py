"""GET /api/federation — federation manifest. Respects NTI_MODE.

In standalone mode: returns a manifest indicating this node does NOT federate.
In federated mode: returns a manifest with hub URLs and node metadata.
In hub mode: returns a manifest plus hub capabilities.
"""
from http.server import BaseHTTPRequestHandler
import json

from lib.mode import get_mode, get_node_info


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        mode = get_mode()
        node = get_node_info()

        manifest = {
            "protocol": "NTI-Cert/1",
            "federation_version": "1.0",
            "mode": mode,
            "node": {
                "name": node["node_name"],
                "url": node["node_url"],
                "description": node["node_description"],
                "contact": node["contact"],
            },
            "endpoints": {
                "verify": "POST /api/verify",
                "badge": "GET /api/badge?repo=owner/repo",
                "certificate": "GET /api/certificate?repo=owner/repo",
                "registry": "GET /api/registry",
                "leaderboard": "GET /api/leaderboard",
                "transparency": "GET /api/transparency",
                "org": "GET /api/org?name=<org>",
                "mode": "GET /api/mode",
                "federation_manifest": "GET /api/federation",
            },
            "cert_format": {
                "spec": "NTI-Cert/1",
                "signature_alg": "Dilithium5",
            },
            "verification_offline": "nti-scanner verify ./nti-certificate.json",
            "license": "Apache-2.0",
            "neutrality": (
                "No central authority. No data custody. Certificates live in the "
                "user's repository. This node indexes only {repo, score, cert_hash, timestamp}."
            ),
        }

        if mode == "standalone":
            manifest["federation"] = {
                "enabled": False,
                "reason": "Node is running in standalone mode (NTI_MODE=standalone). Set NTI_MODE=federated to publish to hubs.",
            }
        elif mode == "federated":
            manifest["federation"] = {
                "enabled": True,
                "hub_urls": node["hub_urls"],
                "note": "This node publishes its public index to the hubs listed above.",
            }
        elif mode == "hub":
            manifest["federation"] = {
                "enabled": True,
                "hub_urls": node["hub_urls"],
                "hub_enabled": True,
                "hub_endpoints": {
                    "register": "POST /api/hub/register",
                    "nodes": "GET /api/hub/nodes",
                    "aggregate_index": "GET /api/hub/index",
                    "aggregate_leaderboard": "GET /api/hub/leaderboard",
                },
                "note": "This node is a hub. It aggregates other nodes AND can federate with other hubs.",
            }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(manifest, indent=2).encode("utf-8"))
