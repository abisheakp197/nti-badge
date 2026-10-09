"""GET /api/hub/index — aggregated index from all registered nodes."""
import json

from lib.mode import is_hub
from lib.aggregator import aggregate_index


async def run():
    headers = {"Content-Type": "application/json"}
    if not is_hub():
        return (403, headers, json.dumps({"error": "not a hub"}).encode("utf-8"))
    result = await aggregate_index()
    return (200, headers, json.dumps(result, indent=2).encode("utf-8"))
