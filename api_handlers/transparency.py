"""GET /api/transparency — public transparency log."""
import json

from lib.store import list_all


async def run():
    headers = {"Content-Type": "application/json"}
    try:
        entries = await list_all()
    except Exception:
        entries = []
    log = sorted(
        [{"repo": e["repo"], "cert_hash": e.get("cert_hash", ""), "timestamp": e.get("timestamp", ""), "score": e.get("score")} for e in entries],
        key=lambda x: x.get("timestamp", ""),
    )
    payload = json.dumps({
        "log_type": "nti-transparency/1",
        "entry_count": len(log),
        "entries": log,
    }, indent=2).encode("utf-8")
    return (200, headers, payload)
