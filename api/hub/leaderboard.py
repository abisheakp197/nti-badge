"""GET /api/hub/leaderboard — unified leaderboard across all registered nodes."""
from http.server import BaseHTTPRequestHandler
import json
import asyncio

from lib.mode import is_hub
from lib.aggregator import aggregate_leaderboard


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if not is_hub():
            self._respond(403, {"error": "not a hub"})
            return
        result = asyncio.run(aggregate_leaderboard(50))
        self._respond(200, result)

    def _respond(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
