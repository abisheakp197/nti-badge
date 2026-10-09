"""GET /api/hub/nodes — list all registered nodes and hubs."""
import json

from lib.mode import is_hub
from lib.hub_store import list_nodes, list_hubs


async def run():
    headers = {"Content-Type": "application/json"}
    if not is_hub():
        return (403, headers, json.dumps({"error": "not a hub"}).encode("utf-8"))
    nodes = await list_nodes()
    hubs = await list_hubs()
    payload = json.dumps({"node_count": len(nodes), "hub_count": len(hubs), "nodes": nodes, "hubs": hubs}, indent=2).encode("utf-8")
    return (200, headers, payload)
