"""POST /api/hub/register — register a node or hub with this hub."""
import json

from lib.mode import is_hub
from lib.hub_store import register_node, register_hub


async def run(body_raw: str = ""):
    headers = {"Content-Type": "application/json"}
    if not is_hub():
        return (403, headers, json.dumps({"error": "This node is not running in hub mode. Set NTI_MODE=hub to enable registration."}).encode("utf-8"))

    try:
        body = json.loads(body_raw)
    except Exception:
        return (400, headers, json.dumps({"error": "invalid json"}).encode("utf-8"))

    kind = body.get("kind", "node").lower()
    url = (body.get("url") or "").strip()
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
