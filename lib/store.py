"""Store layer. Uses lib/db.py so users can bring their own database.

Data custody principle:
- We index ONLY: repo, score, cert_hash, timestamp, tier, signature_verified
- The full certificate lives in the user's repository, never here.
"""

import json
from typing import Any

from lib.db import (
    backend_info,
    hget,
    hgetall,
    hset,
    lrange,
    ltrim,
    rpush,
    zadd,
    zrevrange,
)
from lib.mode import is_hub, is_standalone

INDEX_NS = "nti:index"
LEADERBOARD_NS = "nti:leaderboard"


async def index_certificate(repo_full: str, entry: dict[str, Any]) -> None:
    payload = json.dumps(entry)
    await hset(INDEX_NS, repo_full, payload)
    await zadd(LEADERBOARD_NS, {repo_full: entry.get("score", 0)})
    await rpush(f"nti:history:{repo_full}", payload)
    await ltrim(f"nti:history:{repo_full}", -500, -1)


async def get_latest(repo_full: str) -> dict[str, Any] | None:
    raw = await hget(INDEX_NS, repo_full)
    if not raw:
        return None
    res: dict[str, Any] = json.loads(raw)
    return res


async def get_history(repo_full: str, limit: int = 50) -> list[dict[str, Any]]:
    raw_entries = await lrange(f"nti:history:{repo_full}", -limit, -1)
    return [json.loads(e) for e in raw_entries]


async def list_all() -> list[dict[str, Any]]:
    entries = await hgetall(INDEX_NS)
    return [{"repo": k, **json.loads(v)} for k, v in entries.items()]


async def top_scores(limit: int = 50) -> list[dict[str, Any]]:
    results = await zrevrange(LEADERBOARD_NS, 0, limit - 1, withscores=True)
    out: list[dict[str, Any]] = []
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


async def list_by_org(org: str) -> list[dict[str, Any]]:
    all_entries = await list_all()
    return [e for e in all_entries if str(e.get("repo", "")).startswith(f"{org}/")]


async def store_status() -> dict[str, Any]:
    """Public status snapshot of the store."""
    info = backend_info()
    info["federation_enabled"] = not is_standalone()
    info["hub_enabled"] = is_hub()
    return info
