"""Hub-specific storage. Tracks registered nodes and hubs.

The hub holds a registry of other nodes. That's it. It never holds their
underlying data — only their announcement URL and metadata.
"""

import json
from datetime import UTC, datetime
from typing import Any

from lib.db import delete, hget, hgetall, hset

NODES_NS = "nti:hub:nodes"
HUBS_NS = "nti:hub:hubs"
HEALTH_NS = "nti:hub:health"


async def register_node(node_url: str, metadata: dict[str, Any]) -> dict[str, Any]:
    node_url = node_url.rstrip("/")
    entry = {
        "url": node_url,
        "name": metadata.get("name", "unnamed"),
        "description": metadata.get("description", ""),
        "contact": metadata.get("contact", ""),
        "pubkey": metadata.get("pubkey", ""),
        "registered_at": datetime.now(UTC).isoformat(),
    }
    await hset(NODES_NS, node_url, json.dumps(entry))
    return entry


async def unregister_node(node_url: str) -> None:
    await delete(f"{NODES_NS}:{node_url}")


async def get_node(node_url: str) -> dict[str, Any] | None:
    raw = await hget(NODES_NS, node_url.rstrip("/"))
    if not raw:
        return None
    res: dict[str, Any] = json.loads(raw)
    return res


async def list_nodes() -> list[dict[str, Any]]:
    entries = await hgetall(NODES_NS)
    return [json.loads(v) for v in entries.values()]


async def register_hub(hub_url: str, metadata: dict[str, Any]) -> dict[str, Any]:
    hub_url = hub_url.rstrip("/")
    entry = {
        "url": hub_url,
        "name": metadata.get("name", "unnamed-hub"),
        "description": metadata.get("description", ""),
        "registered_at": datetime.now(UTC).isoformat(),
    }
    await hset(HUBS_NS, hub_url, json.dumps(entry))
    return entry


async def list_hubs() -> list[dict[str, Any]]:
    entries = await hgetall(HUBS_NS)
    return [json.loads(v) for v in entries.values()]


async def record_health(node_url: str, status: dict[str, Any]) -> None:
    payload = {
        "node_url": node_url.rstrip("/"),
        "checked_at": datetime.now(UTC).isoformat(),
        "status": status,
    }
    await hset(HEALTH_NS, node_url.rstrip("/"), json.dumps(payload))


async def get_health(node_url: str) -> dict[str, Any] | None:
    raw = await hget(HEALTH_NS, node_url.rstrip("/"))
    if not raw:
        return None
    res: dict[str, Any] = json.loads(raw)
    return res
