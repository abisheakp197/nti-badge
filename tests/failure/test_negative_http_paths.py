"""Category 11 Negative-Path Validation Tests: HTTP endpoint error handling."""

import json
from pathlib import Path

from api.index import handler as IndexHandler
from tests.test_api import MockRequest


def test_oversized_payload_returns_413(temp_store: Path) -> None:
    # Body larger than 1MB
    large_body = b"x" * (1_048_576 + 10)
    req = MockRequest(
        "POST",
        "/api/verify",
        headers={"content-length": str(len(large_body)), "content-type": "application/json"},
        body=large_body,
    )
    h, wfile = req.make_handler(IndexHandler)
    h.do_POST()
    assert h.response_code == 413  # type: ignore[attr-defined]
    res = json.loads(wfile.getvalue().decode("utf-8"))
    assert res.get("error") == "payload too large"


def test_wrong_content_type_returns_415(temp_store: Path) -> None:
    body = json.dumps({"test": 123}).encode("utf-8")
    req = MockRequest(
        "POST",
        "/api/verify",
        headers={"content-length": str(len(body)), "content-type": "text/plain"},
        body=body,
    )
    h, wfile = req.make_handler(IndexHandler)
    h.do_POST()
    assert h.response_code == 415  # type: ignore[attr-defined]
    res = json.loads(wfile.getvalue().decode("utf-8"))
    assert "unsupported media type" in res.get("error", "")


def test_malformed_json_returns_400(temp_store: Path) -> None:
    bad_json = b"{invalid-json"
    req = MockRequest(
        "POST",
        "/api/verify",
        headers={"content-length": str(len(bad_json)), "content-type": "application/json"},
        body=bad_json,
    )
    h, wfile = req.make_handler(IndexHandler)
    h.do_POST()
    assert h.response_code == 400  # type: ignore[attr-defined]
    res = json.loads(wfile.getvalue().decode("utf-8"))
    assert "invalid json" in res.get("error", "")


def test_unsupported_path_returns_404() -> None:
    req = MockRequest("GET", "/api/nonexistent")
    h, wfile = req.make_handler(IndexHandler)
    h.do_GET()
    assert h.response_code == 404  # type: ignore[attr-defined]
    res = json.loads(wfile.getvalue().decode("utf-8"))
    assert res.get("error") == "not found"
