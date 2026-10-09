"""Fetch indexes from registered nodes and merge them.

Design principle: The hub never trusts nodes. Every index entry includes
the node's signature. Verification is the responsibility of the caller.
"""

import asyncio
from typing import List

import httpx

from lib.hub_store import list_nodes


TIMEOUT = 10.0


async def fetch_node_index(node_url: str) -> dict:
    url = node_url.rstrip("/") + "/api/registry"
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(url)
            if r.status_code == 200:
                data = r.json()
                return {
                    "node_url": node_url,
                    "ok": True,
                    "count": data.get("count", 0),
                    "repos": data.get("repos", []),
                }
    except Exception as e:
        return {"node_url": node_url, "ok": False, "error": str(e), "repos": []}
    return {"node_url": node_url, "ok": False, "error": "unreachable", "repos": []}


async def fetch_node_manifest(node_url: str) -> dict:
    url = node_url.rstrip("/") + "/api/federation"
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            r = await client.get(url)
            if r.status_code == 200:
                return r.json()
    except Exception:
        pass
    return {}


async def aggregate_index(limit_nodes: int = 100) -> dict:
    nodes = await list_nodes()
    nodes = nodes[:limit_nodes]
    if not nodes:
        return {"count": 0, "repos": [], "sources": []}

    tasks = [fetch_node_index(n["url"]) for n in nodes]
    results = await asyncio.gather(*tasks)

    merged = {}
    sources = []
    for r in results:
        if r.get("ok"):
            sources.append({"url": r["node_url"], "count": r["count"]})
            for entry in r.get("repos", []):
                repo = entry.get("repo")
                if not repo:
                    continue
                score = entry.get("score", 0)
                prev = merged.get(repo)
                if prev is None or score > prev.get("score", 0):
                    entry["_source_node"] = r["node_url"]
                    merged[repo] = entry

    repos = sorted(merged.values(), key=lambda x: x.get("score", 0), reverse=True)
    return {"count": len(repos), "repos": repos, "sources": sources}


async def aggregate_leaderboard(limit: int = 50) -> dict:
    agg = await aggregate_index(limit_nodes=100)
    repos = agg.get("repos", [])
    repos = repos[:limit]
    return {
        "count": len(repos),
        "leaderboard": [
            {
                "repo": r.get("repo"),
                "score": r.get("score", 0),
                "tier": r.get("tier", "Unranked"),
                "timestamp": r.get("timestamp", ""),
                "source_node": r.get("_source_node", ""),
            }
            for r in repos
        ],
    }
