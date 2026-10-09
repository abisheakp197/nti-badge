"""GET /api/certificate?repo=owner/repo — returns the latest indexed cert metadata.


Note: this returns the INDEX entry (hash + score + metadata), not the full
certificate. The full certificate lives in the user's repository. To verify
a full certificate, use the offline verification tool in nti-scanner.
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import asyncio


from lib.store import get_latest, get_history




class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        repo = params.get("repo", [""])[0]
        if not repo or "/" not in repo:
            self._respond(400, {"error": "repo parameter required (owner/repo)"})
            return


        try:
            latest = asyncio.run(get_latest(repo))
            history = asyncio.run(get_history(repo, 50))
        except Exception:
            latest = None
            history = []


        self._respond(200, {
            "repo": repo,
            "latest": latest,
            "history_count": len(history),
            "history": history,
            "how_to_verify_offline": "pip install nti-scanner && nti-scanner verify ./nti-certificate.json",
        })


    def _respond(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
