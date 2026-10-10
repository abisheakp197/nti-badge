"""GET /api/leaderboard — top 50 repos by score."""
import json

from lib.store import top_scores


async def run():
    headers = {"Content-Type": "application/json"}
    try:
        entries = await top_scores(50)
    except Exception:
        entries = []
    payload = json.dumps({"leaderboard": entries}, indent=2).encode("utf-8")
    return (200, headers, payload)
