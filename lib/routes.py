"""Central route dispatcher. Each route is a function returning (status, headers, body)."""

import json
from typing import Tuple, Dict
from urllib.parse import urlparse


async def route_request(method: str, path: str, body_raw: str) -> Tuple[int, Dict, bytes]:
    """Route a request to the correct handler function."""

    req_path = urlparse(path).path

    # -------- GET routes --------
    if method == "GET":
        if req_path == "/api/badge":
            from api_handlers.badge import run as badge_run
            return await badge_run(self_path=path)
        if req_path == "/api/registry":
            from api_handlers.registry import run
            return await run()
        if req_path == "/api/leaderboard":
            from api_handlers.leaderboard import run
            return await run()
        if req_path == "/api/certificate":
            from api_handlers.certificate import run
            return await run(self_path=path)
        if req_path == "/api/transparency":
            from api_handlers.transparency import run
            return await run()
        if req_path == "/api/org":
            from api_handlers.org import run
            return await run(self_path=path)
        if req_path == "/api/federation":
            from api_handlers.federation import run
            return await run()
        if req_path == "/api/mode":
            from api_handlers.mode import run
            return await run()
        if req_path == "/api/hub/nodes":
            from api_handlers.hub_nodes import run
            return await run()
        if req_path == "/api/hub/index":
            from api_handlers.hub_index import run
            return await run()
        if req_path == "/api/hub/leaderboard":
            from api_handlers.hub_leaderboard import run
            return await run()

    # -------- POST routes --------
    if method == "POST":
        if req_path == "/api/verify":
            from api_handlers.verify import run
            return await run(body_raw=body_raw)
        if req_path == "/api/federation/publish":
            from api_handlers.federation_publish import run
            return await run()
        if req_path == "/api/hub/register":
            from api_handlers.hub_register import run
            return await run(body_raw=body_raw)

    # -------- Fallback --------
    return (404, {"Content-Type": "application/json"}, json.dumps({"error": "not found", "path": path}).encode("utf-8"))
