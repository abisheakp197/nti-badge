"""GET /api/certificate?repo=owner/repo — returns the latest indexed cert metadata."""
import json
from urllib.parse import urlparse, parse_qs

from lib.store import get_latest, get_history


async def run(self_path: str = ""):
    headers = {"Content-Type": "application/json"}
    query_str = urlparse(self_path).query if "?" in self_path else self_path
    params = parse_qs(query_str)
    repo = params.get("repo", [""])[0]

    if not repo or "/" not in repo:
        return (400, headers, json.dumps({"error": "repo parameter required (owner/repo)"}).encode("utf-8"))

    try:
        latest = await get_latest(repo)
        history = await get_history(repo, 50)
    except Exception:
        latest = None
        history = []

    payload = json.dumps({
        "repo": repo,
        "latest": latest,
        "history_count": len(history),
        "history": history,
        "how_to_verify_offline": "pip install nti-scanner && nti-scanner verify ./nti-certificate.json",
    }, indent=2).encode("utf-8")

    return (200, headers, payload)
