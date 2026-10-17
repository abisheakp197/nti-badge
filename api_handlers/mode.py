"""GET /api/mode — returns operational mode and status."""

import json

from lib.mode import get_mode, get_node_info
from lib.store import store_status


async def run() -> tuple[int, dict[str, str], bytes]:
    headers = {"Content-Type": "application/json"}
    mode = get_mode()
    node = get_node_info()
    store_info = await store_status()

    payload = {
        "mode": mode,
        "node_info": node,
        "store": store_info,
        "capabilities": {
            "verify": True,
            "badge_rendering": True,
            "certificate_lookup": True,
            "org_aggregation": True,
            "federation": get_mode() != "standalone",
            "hub_mode": get_mode() == "hub",
        },
    }
    return (200, headers, json.dumps(payload, indent=2).encode("utf-8"))
