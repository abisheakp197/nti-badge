"""GET /api/leaderboard — top 50 repos by score."""
from http.server import BaseHTTPRequestHandler
import json
import asyncio


from lib.store import top_scores




class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            entries = asyncio.run(top_scores(50))
        except Exception:
            entries = []
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"leaderboard": entries}, indent=2).encode("utf-8"))
