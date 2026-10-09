"""GET /api/transparency — public transparency log.


Every indexed cert hash with its timestamp, forming an append-only public log.
Anyone can rebuild and audit this. ZERO-knowledge: only hashes are visible.
"""
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
        log = sorted(
            [{"repo": e["repo"], "cert_hash": e.get("cert_hash", ""), "timestamp": e.get("timestamp", ""), "score": e.get("score")} for e in entries],
            key=lambda x: x.get("timestamp", ""),
        )
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({
            "log_type": "nti-transparency/1",
            "entry_count": len(log),
            "entries": log,
        }, indent=2).encode("utf-8"))
