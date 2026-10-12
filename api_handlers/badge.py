"""GET /api/badge?repo=owner/repo — serves verified SVG badge.

Renders a tiered badge based on the latest indexed cert for the repo.
If no cert is indexed, returns a grey "not verified" badge.
"""
from urllib.parse import urlparse, parse_qs

from lib.store import get_latest
from lib.tiers import tier_metadata
from nti_badge.badge import render_badge_svg


def _badge_svg(label: str, value: str, color: str, tier_emoji: str = "") -> str:
    return render_badge_svg(label, value, color, tier_emoji)


async def run(self_path: str = ""):
    query_str = urlparse(self_path).query if "?" in self_path else self_path
    params = parse_qs(query_str)
    repo = params.get("repo", [""])[0]

    headers = {
        "Content-Type": "image/svg+xml; charset=utf-8",
        "Cache-Control": "public, max-age=300",
    }

    if not repo or "/" not in repo:
        return (200, headers, _badge_svg("NTI-1", "not verified", "#555").encode("utf-8"))

    try:
        entry = await get_latest(repo)
    except Exception:
        entry = None

    if not entry:
        return (200, headers, _badge_svg("NTI-1", "not verified", "#555").encode("utf-8"))

    score = entry.get("score", 0)
    tier = entry.get("tier", "Unranked")
    meta = tier_metadata(tier)

    return (200, headers, _badge_svg("NTI-1", f"{score}/100 {tier}", meta["color"], meta["emoji"]).encode("utf-8"))
