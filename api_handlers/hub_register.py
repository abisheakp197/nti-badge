"""POST /api/hub/register — register a node or hub with this hub."""

import json

from lib.hub_store import register_hub, register_node
from lib.mode import is_hub


async def run(body_raw: str = "") -> tuple[int, dict[str, str], bytes]:
    headers = {"Content-Type": "application/json"}
    if not is_hub():
        return (403, headers, json.dumps({"error": "This node is not running in hub mode. Set NTI_MODE=hub to enable registration."}).encode("utf-8"))

    try:
        body = json.loads(body_raw)
    except (json.JSONDecodeError, TypeError, ValueError):
        return (400, headers, json.dumps({"error": "invalid json"}).encode("utf-8"))

    if not isinstance(body, dict):
        return (400, headers, json.dumps({"error": "invalid json format"}).encode("utf-8"))

    kind = str(body.get("kind", "node")).lower()
    url = str(body.get("url", "")).strip()
    if not url or not url.startswith("http"):
        return (400, headers, json.dumps({"error": "url required (must start with http)"}).encode("utf-8"))

    metadata = {
        "name": body.get("name", "unnamed"),
        "description": body.get("description", ""),
        "contact": body.get("contact", ""),
        "pubkey": body.get("pubkey", ""),
    }

    if kind == "hub":
        entry = await register_hub(url, metadata)
    else:
        entry = await register_node(url, metadata)

    return (200, headers, json.dumps({"status": "registered", "kind": kind, "entry": entry}).encode("utf-8"))
