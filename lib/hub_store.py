"""Hub-specific storage. Tracks registered nodes and hubs.

The hub holds a registry of other nodes. That's it. It never holds their
underlying data — only their announcement URL and metadata.
"""

import json
from typing import Optional, List
from datetime import datetime, timezone

from lib.db import hset, hget, hgetall, delete


NODES_NS = "nti:hub:nodes"
HUBS_NS = "nti:hub:hubs"
HEALTH_NS = "nti:hub:health"


async def register_node(node_url: str, metadata: dict) -> dict:
    node_url = node_url.rstrip("/")
    entry = {
        "url": node_url,
        "name": metadata.get("name", "unnamed"),
        "description": metadata.get("description", ""),
        "contact": metadata.get("contact", ""),
        "pubkey": metadata.get("pubkey", ""),
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    await hset(NODES_NS, node_url, json.dumps(entry))
    return entry


async def unregister_node(node_url: str) -> None:
    await delete(f"{NODES_NS}:{node_url}")


async def get_node(node_url: str) -> Optional[dict]:
    raw = await hget(NODES_NS, node_url.rstrip("/"))
    return json.loads(raw) if raw else None


async def list_nodes() -> List[dict]:
    entries = await hgetall(NODES_NS)
    return [json.loads(v) for v in entries.values()]


async def register_hub(hub_url: str, metadata: dict) -> dict:
    hub_url = hub_url.rstrip("/")
    entry = {
        "url": hub_url,
        "name": metadata.get("name", "unnamed-hub"),
        "description": metadata.get("description", ""),
        "registered_at": datetime.now(timezone.utc).isoformat(),
    }
    await hset(HUBS_NS, hub_url, json.dumps(entry))
    return entry


async def list_hubs() -> List[dict]:
    entries = await hgetall(HUBS_NS)
    return [json.loads(v) for v in entries.values()]


async def record_health(node_url: str, status: dict) -> None:
    payload = {
        "node_url": node_url.rstrip("/"),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
    }
    await hset(HEALTH_NS, node_url.rstrip("/"), json.dumps(payload))


async def get_health(node_url: str) -> Optional[dict]:
    raw = await hget(HEALTH_NS, node_url.rstrip("/"))
    return json.loads(raw) if raw else None
