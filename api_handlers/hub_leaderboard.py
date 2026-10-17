"""GET /api/hub/leaderboard — unified leaderboard across all registered nodes."""

import json

from lib.aggregator import aggregate_leaderboard
from lib.mode import is_hub


async def run() -> tuple[int, dict[str, str], bytes]:
    headers = {"Content-Type": "application/json"}
    if not is_hub():
        return (403, headers, json.dumps({"error": "not a hub"}).encode("utf-8"))
    result = await aggregate_leaderboard(50)
    return (200, headers, json.dumps(result, indent=2).encode("utf-8"))
