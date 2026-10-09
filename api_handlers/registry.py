"""GET /api/registry — JSON list of all indexed certs."""
import json

from lib.store import list_all


async def run():
    headers = {"Content-Type": "application/json"}
    try:
        entries = await list_all()
    except Exception:
        entries = []
    payload = json.dumps({
        "spec": "NTI-Cert/1",
        "count": len(entries),
        "note": "This is a federated index. Full certificates live in each repo. Anyone can mirror this endpoint.",
        "repos": entries,
    }, indent=2).encode("utf-8")
    return (200, headers, payload)
