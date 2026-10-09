"""GET /api/mode — returns the deployment mode and capabilities."""
from http.server import BaseHTTPRequestHandler
import json
import asyncio

from lib.mode import get_node_info, get_mode
from lib.db import backend_info


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        info = get_node_info()
        info["database"] = backend_info()
        info["capabilities"] = {
            "badge": True,
            "verify": True,
            "registry": True,
            "leaderboard": True,
            "transparency": True,
            "certificate_lookup": True,
            "org_aggregation": True,
            "federation": not get_mode() == "standalone",
            "hub_mode": get_mode() == "hub",
        }
        info["links"] = {
            "badge": "/api/badge?repo=owner/repo",
            "registry": "/api/registry",
            "leaderboard": "/api/leaderboard",
            "transparency": "/api/transparency",
            "certificate": "/api/certificate?repo=owner/repo",
            "org": "/api/org?name=<org>",
            "federation": "/api/federation",
        }
        self._respond(200, info)

    def _respond(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
