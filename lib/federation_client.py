"""Outbound federation client.

A federated node uses this to publish its public index to hubs.
Runs on a cron or is triggered by /api/federation/publish.

The node NEVER gives data to hubs. It only announces its URL. Hubs pull
the node's public index on-demand. This preserves node sovereignty.
"""

import asyncio
import httpx

from lib.mode import get_hub_urls, get_node_info, is_federated, is_hub


TIMEOUT = 10.0


async def announce_to_hub(hub_url: str) -> dict:
    """Announce this node to a hub. Hub stores node URL; pulls index on demand."""
    node = get_node_info()
    payload = {
        "kind": "hub" if is_hub() else "node",
        "url": node["node_url"],
        "name": node["node_name"],
        "description": node["node_description"],
        "contact": node["contact"],
        "pubkey": "",
    }
    url = hub_url.rstrip("/") + "/api/hub/register"
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.post(url, json=payload)
            if r.status_code == 200:
                return {"hub": hub_url, "ok": True, "response": r.json()}
            return {"hub": hub_url, "ok": False, "status": r.status_code}
    except Exception as e:
        return {"hub": hub_url, "ok": False, "error": str(e)}


async def announce_to_all_hubs() -> list:
    hubs = get_hub_urls()
    if not hubs:
        return []
    tasks = [announce_to_hub(h) for h in hubs]
    return await asyncio.gather(*tasks)


def can_announce() -> bool:
    return (is_federated() or is_hub()) and bool(get_hub_urls())
