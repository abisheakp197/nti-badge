"""GET /api/registry — JSON list of all indexed certs."""
from http.server import BaseHTTPRequestHandler
import json
import asyncio


from lib.store import list_all




class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            entries = asyncio.run(list_all())
        except Exception:
            entries = []
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({
            "spec": "NTI-Cert/1",
            "count": len(entries),
            "note": "This is a federated index. Full certificates live in each repo. Anyone can mirror this endpoint.",
            "repos": entries,
        }, indent=2).encode("utf-8"))
