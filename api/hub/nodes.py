"""GET /api/hub/nodes — list all registered nodes and hubs."""
from http.server import BaseHTTPRequestHandler
import json
import asyncio

from lib.mode import is_hub
from lib.hub_store import list_nodes, list_hubs


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not is_hub():
            self._respond(403, {"error": "not a hub"})
            return
        nodes = asyncio.run(list_nodes())
        hubs = asyncio.run(list_hubs())
        self._respond(200, {"node_count": len(nodes), "hub_count": len(hubs), "nodes": nodes, "hubs": hubs})

    def _respond(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
