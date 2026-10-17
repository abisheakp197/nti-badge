"""GET /api/leaderboard — top 50 repos by score."""

import json

from lib.store import top_scores


async def run() -> tuple[int, dict[str, str], bytes]:
    headers = {"Content-Type": "application/json"}
    try:
        entries = await top_scores(50)
    except Exception:  # noqa: BLE001
        entries = []
    payload = json.dumps({"leaderboard": entries}, indent=2).encode("utf-8")
    return (200, headers, payload)
