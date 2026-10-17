"""Central route dispatcher. Each route is a function returning (status, headers, body)."""

import json
from urllib.parse import urlparse

from api_handlers.badge import run as badge_run
from api_handlers.certificate import run as cert_run
from api_handlers.federation import run as federation_run
from api_handlers.federation_publish import run as publish_run
from api_handlers.hub_index import run as hub_index_run
from api_handlers.hub_leaderboard import run as hub_leaderboard_run
from api_handlers.hub_nodes import run as hub_nodes_run
from api_handlers.hub_register import run as hub_register_run
from api_handlers.leaderboard import run as leaderboard_run
from api_handlers.mode import run as mode_run
from api_handlers.org import run as org_run
from api_handlers.registry import run as registry_run
from api_handlers.transparency import run as transparency_run
from api_handlers.verify import run as verify_run


async def route_request(
    method: str, path: str, body_raw: str = "", content_type: str = ""
) -> tuple[int, dict[str, str], bytes]:
    """Route a request to the correct handler function."""
    req_path = urlparse(path).path

    # Check payload size limit (1MB max)
    if method == "POST" and len(body_raw.encode("utf-8")) > 1_048_576:
        return (
            413,
            {"Content-Type": "application/json"},
            json.dumps({"error": "payload too large"}).encode("utf-8"),
        )

    # Check content type header for POST endpoints if specified
    if method == "POST" and content_type and "application/json" not in content_type.lower():
        return (
            415,
            {"Content-Type": "application/json"},
            json.dumps({"error": "unsupported media type, expected application/json"}).encode("utf-8"),
        )

    # -------- GET routes --------
    if method == "GET":
        if req_path == "/api/badge":
            return await badge_run(self_path=path)
        if req_path == "/api/registry":
            return await registry_run()
        if req_path == "/api/leaderboard":
            return await leaderboard_run()
        if req_path == "/api/certificate":
            return await cert_run(self_path=path)
        if req_path == "/api/transparency":
            return await transparency_run()
        if req_path == "/api/org":
            return await org_run(self_path=path)
        if req_path == "/api/federation":
            return await federation_run()
        if req_path == "/api/mode":
            return await mode_run()
        if req_path == "/api/hub/nodes":
            return await hub_nodes_run()
        if req_path == "/api/hub/index":
            return await hub_index_run()
        if req_path == "/api/hub/leaderboard":
            return await hub_leaderboard_run()

    # -------- POST routes --------
    if method == "POST":
        if req_path == "/api/verify":
            return await verify_run(body_raw=body_raw)
        if req_path == "/api/federation/publish":
            return await publish_run()
        if req_path == "/api/hub/register":
            return await hub_register_run(body_raw=body_raw)

    # -------- Fallback --------
    return (
        404,
        {"Content-Type": "application/json"},
        json.dumps({"error": "not found", "path": path}).encode("utf-8"),
    )
