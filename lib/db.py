"""Database abstraction. User brings their own DB.

Backend priority:
1. KV_URL or REDIS_URL → Redis-compatible (Upstash, Valkey, Redis)
2. UPSTASH_REDIS_REST_URL + TOKEN → Upstash REST API
3. Neither → local file storage (works everywhere, zero config)
"""

import asyncio
import json
import os
from pathlib import Path
from typing import Any

BACKEND: str | None = None
_redis_client: Any = None
_file_lock = asyncio.Lock()
LOCAL_STORE_DIR = Path(os.environ.get("NTI_LOCAL_STORE", ".nti-data"))


def _detect_backend() -> str:
    if os.environ.get("KV_URL") or os.environ.get("REDIS_URL"):
        return "redis"
    if os.environ.get("UPSTASH_REDIS_REST_URL") and os.environ.get("UPSTASH_REDIS_REST_TOKEN"):
        return "upstash_rest"
    return "file"


def get_backend() -> str:
    global BACKEND
    if BACKEND is None:
        BACKEND = _detect_backend()
    return BACKEND


def _redis() -> Any:
    global _redis_client
    if _redis_client is None:
        try:
            import redis.asyncio as aioredis
            url = os.environ.get("KV_URL") or os.environ.get("REDIS_URL") or ""
            if url:
                _redis_client = aioredis.from_url(url, decode_responses=True)
        except Exception:  # noqa: BLE001
            _redis_client = None
    return _redis_client


async def _file_path(namespace: str) -> Path:
    store_dir = Path(os.environ.get("NTI_LOCAL_STORE", ".nti-data"))
    store_dir.mkdir(parents=True, exist_ok=True)
    clean_ns = namespace.replace(":", "_").replace("/", "_")
    return store_dir / f"{clean_ns}.json"


async def hset(namespace: str, key: str, value: str) -> None:
    if get_backend() == "redis":
        r = _redis()
        if r:
            await r.hset(namespace, key, value)
            return
    async with _file_lock:
        path = await _file_path(namespace)
        data: dict[str, Any] = {}
        if path.exists():
            try:
                data = json.loads(path.read_text())
            except Exception:  # noqa: BLE001
                data = {}
        data[key] = value
        path.write_text(json.dumps(data, indent=2))


async def hget(namespace: str, key: str) -> str | None:
    if get_backend() == "redis":
        r = _redis()
        if r:
            val: str | None = await r.hget(namespace, key)
            return val
    path = await _file_path(namespace)
    if not path.exists():
        return None
    try:
        val_str: str | None = json.loads(path.read_text()).get(key)
        return val_str
    except Exception:  # noqa: BLE001
        return None


async def hgetall(namespace: str) -> dict[str, str]:
    if get_backend() == "redis":
        r = _redis()
        if r:
            res_dict: dict[str, str] = await r.hgetall(namespace)
            return res_dict
    path = await _file_path(namespace)
    if not path.exists():
        return {}
    try:
        res_file: dict[str, str] = json.loads(path.read_text())
        return res_file
    except Exception:  # noqa: BLE001
        return {}


async def zadd(namespace: str, mapping: dict[str, int | float]) -> None:
    if get_backend() == "redis":
        r = _redis()
        if r:
            await r.zadd(namespace, mapping)
            return
    for key, score in mapping.items():
        await hset(namespace + ":zset", key, str(score))


async def zrevrange(
    namespace: str, start: int, end: int, withscores: bool = False
) -> list[str] | list[tuple[str, float]]:
    if get_backend() == "redis":
        r = _redis()
        if r:
            res_redis: list[str] | list[tuple[str, float]] = await r.zrevrange(namespace, start, end, withscores=withscores)
            return res_redis
    all_scores = await hgetall(namespace + ":zset")
    items = sorted(all_scores.items(), key=lambda x: float(x[1]), reverse=True)
    sliced = items[start : (end + 1 if end >= 0 else None)]
    if withscores:
        return [(k, float(v)) for k, v in sliced]
    return [k for k, _ in sliced]


async def rpush(namespace: str, value: str) -> None:
    if get_backend() == "redis":
        r = _redis()
        if r:
            await r.rpush(namespace, value)
            return
    async with _file_lock:
        path = await _file_path(namespace + ":list")
        data: list[str] = []
        if path.exists():
            try:
                data = json.loads(path.read_text())
            except Exception:  # noqa: BLE001
                data = []
        data.append(value)
        path.write_text(json.dumps(data))


async def lrange(namespace: str, start: int, end: int) -> list[str]:
    if get_backend() == "redis":
        r = _redis()
        if r:
            res_list: list[str] = await r.lrange(namespace, start, end)
            return res_list
    path = await _file_path(namespace + ":list")
    if not path.exists():
        return []
    try:
        data_file: list[str] = json.loads(path.read_text())
        return data_file[start : (end + 1 if end >= 0 else None)]
    except Exception:  # noqa: BLE001
        return []


async def ltrim(namespace: str, start: int, end: int) -> None:
    if get_backend() == "redis":
        r = _redis()
        if r:
            await r.ltrim(namespace, start, end)
            return
    path = await _file_path(namespace + ":list")
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text())
        data = data[start : (end + 1 if end >= 0 else None)]
        path.write_text(json.dumps(data))
    except Exception:  # noqa: BLE001, S110
        pass


async def delete(namespace: str) -> None:
    if get_backend() == "redis":
        r = _redis()
        if r:
            await r.delete(namespace)
            return
    path = await _file_path(namespace)
    if path.exists():
        path.unlink()


def backend_info() -> dict[str, Any]:
    return {
        "backend": get_backend(),
        "env_detected": {
            "KV_URL": bool(os.environ.get("KV_URL")),
            "REDIS_URL": bool(os.environ.get("REDIS_URL")),
            "UPSTASH_REDIS_REST_URL": bool(os.environ.get("UPSTASH_REDIS_REST_URL")),
        },
        "note": "Bring your own DB via KV_URL, REDIS_URL, or UPSTASH_REDIS_REST_URL. Otherwise file-based fallback is used.",
        "local_store_dir": str(LOCAL_STORE_DIR),
    }
