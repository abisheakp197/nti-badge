"""GET /api/transparency — append-only log of indexed cert hashes."""

import json

from lib.store import list_all


async def run() -> tuple[int, dict[str, str], bytes]:
    headers = {"Content-Type": "application/json"}
    try:
        entries = await list_all()
    except Exception:  # noqa: BLE001
        entries = []
    log = sorted(
        [
            {
                "repo": e.get("repo", ""),
                "cert_hash": e.get("cert_hash", ""),
                "timestamp": e.get("timestamp", ""),
                "signature_verified": e.get("signature_verified", False),
            }
            for e in entries
        ],
        key=lambda x: x["timestamp"],
    )
    payload = json.dumps({"count": len(log), "log": log}, indent=2).encode("utf-8")
    return (200, headers, payload)
