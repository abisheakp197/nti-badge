"""GET /api/badge?repo=owner/repo — serves verified SVG badge.


Renders a tiered badge based on the latest indexed cert for the repo.
If no cert is indexed, returns a grey "not verified" badge.
"""
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import asyncio


from lib.store import get_latest
from lib.tiers import tier_metadata




def _badge_svg(label: str, value: str, color: str, tier_emoji: str = "") -> str:
    label_w = 120
    value_w = 140
    total = label_w + value_w
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="22" role="img" aria-label="{label}: {value}">
  <title>{label}: {value}</title>
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <clipPath id="r"><rect width="{total}" height="22" rx="4" fill="#fff"/></clipPath>
  <g clip-path="url(#r)">
    <rect width="{label_w}" height="22" fill="#0a0a0a"/>
    <rect x="{label_w}" width="{value_w}" height="22" fill="{color}"/>
    <rect width="{total}" height="22" fill="url(#s)"/>
  </g>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_w // 2}" y="15">NTI-1 {tier_emoji}</text>
    <text x="{label_w + value_w // 2}" y="15">{value}</text>
  </g>
</svg>'''




class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        repo = params.get("repo", [""])[0]


        if not repo or "/" not in repo:
            self._send(_badge_svg("NTI-1", "not verified", "#555"))
            return


        try:
            entry = asyncio.run(get_latest(repo))
        except Exception:
            entry = None


        if not entry:
            self._send(_badge_svg("NTI-1", "not verified", "#555"))
            return


        score = entry.get("score", 0)
        tier = entry.get("tier", "Unranked")
        meta = tier_metadata(tier)


        self._send(_badge_svg("NTI-1", f"{score}/100 {tier}", meta["color"], meta["emoji"]))


    def _send(self, svg):
        self.send_response(200)
        self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
        self.send_header("Cache-Control", "public, max-age=300")
        self.end_headers()
        self.wfile.write(svg.encode("utf-8"))
