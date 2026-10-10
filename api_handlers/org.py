"""GET /api/org?name=<org> — aggregate all repos under an org or user."""
import json
from urllib.parse import urlparse, parse_qs

from lib.store import list_by_org
from lib.tiers import assign_tier


async def run(self_path: str = ""):
    headers = {"Content-Type": "application/json"}
    query_str = urlparse(self_path).query if "?" in self_path else self_path
    params = parse_qs(query_str)
    org = params.get("name", [""])[0]

    if not org:
        return (400, headers, json.dumps({"error": "name parameter required"}).encode("utf-8"))

    try:
        repos = await list_by_org(org)
    except Exception:
        repos = []

    if not repos:
        res = {"org": org, "repo_count": 0, "repos": [], "aggregate_score": 0}
        return (200, headers, json.dumps(res, indent=2).encode("utf-8"))

    scores = [r["score"] for r in repos if isinstance(r.get("score"), int)]
    aggregate = int(sum(scores) / len(scores)) if scores else 0
    worst = min(scores) if scores else 0
    best = max(scores) if scores else 0

    res = {
        "org": org,
        "repo_count": len(repos),
        "aggregate_score": aggregate,
        "worst_score": worst,
        "best_score": best,
        "tier": assign_tier(aggregate),
        "repos": sorted(repos, key=lambda r: r.get("score", 0), reverse=True),
    }
    return (200, headers, json.dumps(res, indent=2).encode("utf-8"))
