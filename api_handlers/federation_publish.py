"""POST /api/federation/publish — trigger an announce to all configured hubs."""
import json

from lib.federation_client import announce_to_all_hubs, can_announce
from lib.mode import get_mode


async def run():
    headers = {"Content-Type": "application/json"}
    if not can_announce():
        payload = {
            "error": "Node is not configured for federation.",
            "mode": get_mode(),
            "fix": "Set NTI_MODE=federated (or hub) and NTI_HUB_URLS=https://hub1.example,https://hub2.example",
        }
        return (403, headers, json.dumps(payload, indent=2).encode("utf-8"))
    results = await announce_to_all_hubs()
    return (200, headers, json.dumps({"published_to": len(results), "results": results}, indent=2).encode("utf-8"))
