"""GET /api/mode — returns the deployment mode and capabilities."""
import json

from lib.mode import get_node_info, get_mode
from lib.db import backend_info


async def run():
    headers = {"Content-Type": "application/json"}
    info = get_node_info()
    info["database"] = backend_info()
    info["capabilities"] = {
        "badge": True,
        "verify": True,
        "registry": True,
        "leaderboard": True,
        "transparency": True,
        "certificate_lookup": True,
        "org_aggregation": True,
        "federation": not get_mode() == "standalone",
        "hub_mode": get_mode() == "hub",
    }
    info["links"] = {
        "badge": "/api/badge?repo=owner/repo",
        "registry": "/api/registry",
        "leaderboard": "/api/leaderboard",
        "transparency": "/api/transparency",
        "certificate": "/api/certificate?repo=owner/repo",
        "org": "/api/org?name=<org>",
        "federation": "/api/federation",
    }
    return (200, headers, json.dumps(info, indent=2).encode("utf-8"))
