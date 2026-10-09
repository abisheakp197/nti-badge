"""Store layer. Uses lib/db.py so users can bring their own database.

Data custody principle:
- We index ONLY: repo, score, cert_hash, timestamp, tier, signature_verified
- The full certificate lives in the user's repository, never here.
"""

import json
from typing import Optional

from lib.db import (
    hset, hget, hgetall, zadd, zrevrange, rpush, lrange, ltrim, backend_info
)
from lib.mode import is_standalone, is_federated, is_hub


INDEX_NS = "nti:index"
LEADERBOARD_NS = "nti:leaderboard"


async def index_certificate(repo_full: str, entry: dict) -> None:
    payload = json.dumps(entry)
    await hset(INDEX_NS, repo_full, payload)
    await zadd(LEADERBOARD_NS, {repo_full: entry.get("score", 0)})
    await rpush(f"nti:history:{repo_full}", payload)
    await ltrim(f"nti:history:{repo_full}", -500, -1)


async def get_latest(repo_full: str) -> Optional[dict]:
    raw = await hget(INDEX_NS, repo_full)
    return json.loads(raw) if raw else None


async def get_history(repo_full: str, limit: int = 50) -> list:
    raw_entries = await lrange(f"nti:history:{repo_full}", -limit, -1)
    return [json.loads(e) for e in raw_entries]


async def list_all() -> list:
    entries = await hgetall(INDEX_NS)
    return [{"repo": k, **json.loads(v)} for k, v in entries.items()]


async def top_scores(limit: int = 50) -> list:
    results = await zrevrange(LEADERBOARD_NS, 0, limit - 1, withscores=True)
    out = []
    if not isinstance(results, list):
        return out
    for item in results:
        if isinstance(item, tuple):
            repo, score = item
        else:
            repo = item
            score = 0
        entry = await get_latest(repo)
        if entry:
            out.append({
                "repo": repo,
                "score": int(score),
                "timestamp": entry.get("timestamp", ""),
                "tier": entry.get("tier", "Unranked"),
            })
    return out


async def list_by_org(org: str) -> list:
    all_entries = await list_all()
    return [e for e in all_entries if e["repo"].startswith(f"{org}/")]


async def store_status() -> dict:
    """Public status snapshot of the store."""
    info = backend_info()
    info["federation_enabled"] = not is_standalone()
    info["hub_enabled"] = is_hub()
    return info
