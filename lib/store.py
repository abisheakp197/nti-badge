"""Federated-friendly storage.


Design principle: NTI stores ONLY what is needed to index certificates —
never the full certificate, never the user's data. This keeps the registry
neutral and lets anyone run a mirror node.
"""
import os
import json
from typing import Optional


def _get_redis():
    kv_url = os.environ.get("KV_URL") or os.environ.get("REDIS_URL")
    if not kv_url:
        return None
    try:
        import redis.asyncio as aioredis
        return aioredis.from_url(kv_url, decode_responses=True)
    except Exception:
        return None


async def index_certificate(repo_full: str, entry: dict) -> None:
    """Store only the index entry (hash + score + timestamp)."""
    redis_client = _get_redis()
    if not redis_client:
        return
    try:
        payload = json.dumps(entry)
        await redis_client.hset("nti:index", repo_full, payload)
        await redis_client.zadd("nti:leaderboard", {repo_full: entry.get("score", 0)})
        # Append-only history (for drift detection + transparency pages)
        await redis_client.rpush(f"nti:history:{repo_full}", payload)
        # Cap history at 500 entries per repo to bound storage
        await redis_client.ltrim(f"nti:history:{repo_full}", -500, -1)
    finally:
        await redis_client.aclose()


async def get_latest(repo_full: str) -> Optional[dict]:
    redis_client = _get_redis()
    if not redis_client:
        return None
    try:
        raw = await redis_client.hget("nti:index", repo_full)
        return json.loads(raw) if raw else None
    finally:
        await redis_client.aclose()


async def get_history(repo_full: str, limit: int = 50) -> list:
    redis_client = _get_redis()
    if not redis_client:
        return []
    try:
        raw_entries = await redis_client.lrange(f"nti:history:{repo_full}", -limit, -1)
        return [json.loads(e) for e in raw_entries]
    finally:
        await redis_client.aclose()


async def list_all() -> list:
    redis_client = _get_redis()
    if not redis_client:
        return []
    try:
        entries = await redis_client.hgetall("nti:index")
        return [{"repo": k, **json.loads(v)} for k, v in entries.items()]
    finally:
        await redis_client.aclose()


async def top_scores(limit: int = 50) -> list:
    redis_client = _get_redis()
    if not redis_client:
        return []
    try:
        results = await redis_client.zrevrange("nti:leaderboard", 0, limit - 1, withscores=True)
        out = []
        for repo, score in results:
            raw = await redis_client.hget("nti:index", repo)
            entry = json.loads(raw) if raw else None
            if entry:
                out.append({"repo": repo, "score": int(score), "timestamp": entry.get("timestamp", "")})
        return out
    finally:
        await redis_client.aclose()


async def list_by_org(org: str) -> list:
    all_entries = await list_all()
    return [e for e in all_entries if e["repo"].startswith(f"{org}/")]
