"""GET /api/org?name=<org> — aggregate all repos under an org or user."""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import asyncio


from lib.store import list_by_org
from lib.tiers import assign_tier




class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        org = params.get("name", [""])[0]
        if not org:
            self._respond(400, {"error": "name parameter required"})
            return


        try:
            repos = asyncio.run(list_by_org(org))
        except Exception:
            repos = []


        if not repos:
            self._respond(200, {"org": org, "repo_count": 0, "repos": [], "aggregate_score": 0})
            return


        scores = [r["score"] for r in repos if isinstance(r.get("score"), int)]
        aggregate = int(sum(scores) / len(scores)) if scores else 0
        worst = min(scores) if scores else 0
        best = max(scores) if scores else 0


        self._respond(200, {
            "org": org,
            "repo_count": len(repos),
            "aggregate_score": aggregate,
            "worst_score": worst,
            "best_score": best,
            "tier": assign_tier(aggregate),
            "repos": sorted(repos, key=lambda r: r.get("score", 0), reverse=True),
        })


    def _respond(self, code, payload):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload, indent=2).encode("utf-8"))
