"""POST /api/hub/register — register a node or hub with this hub.

Only active when NTI_MODE=hub.
"""
from http.server import BaseHTTPRequestHandler
import json
import asyncio
import os

from lib.mode import is_hub
from lib.hub_store import register_node, register_hub


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if not is_hub():
            self._respond(403, {"error": "This node is not running in hub mode. Set NTI_MODE=hub to enable registration."})
            return

        try:
            length = int(self.headers.get("content-length", 0))
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            self._respond(400, {"error": "invalid json"})
            return

        kind = body.get("kind", "node").lower()
        url = (body.get("url") or "").strip()
        if not url or not url.startswith("http"):
            self._respond(400, {"error": "url required (must start with http)"})
            return

        metadata = {
            "name": body.get("name", "unnamed"),
            "description": body.get("description", ""),
            "contact": body.get("contact", ""),
            "pubkey": body.get("pubkey", ""),
        }

        if kind == "hub":
            entry = asyncio.run(register_hub(url, metadata))
        else:
            entry = asyncio.run(register_node(url, metadata))

        self._respond(200, {"status": "registered", "kind": kind, "entry": entry})

    def _respond(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))
