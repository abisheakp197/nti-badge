"""POST /api/federation/publish — trigger an announce to all configured hubs.

Useful for cron jobs or manual publish.
"""
from http.server import BaseHTTPRequestHandler
import json
import asyncio

from lib.federation_client import announce_to_all_hubs, can_announce
from lib.mode import get_mode


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if not can_announce():
            self._respond(403, {
                "error": "Node is not configured for federation.",
                "mode": get_mode(),
                "fix": "Set NTI_MODE=federated (or hub) and NTI_HUB_URLS=https://hub1.example,https://hub2.example",
            })
            return
        results = asyncio.run(announce_to_all_hubs())
        self._respond(200, {"published_to": len(results), "results": results})

    def do_GET(self):
        self._respond(405, {"error": "use POST"})

    def _respond(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
