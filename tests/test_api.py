"""Integration tests for API endpoints."""

import io
import json
import time
from pathlib import Path
from typing import Any

from api.index import handler as IndexHandler
from lib.crypto import compute_cert_hash


class MockRequest:
    def __init__(
        self,
        method: str = "GET",
        path: str = "/",
        headers: dict[str, str] | None = None,
        body: bytes = b"",
    ) -> None:
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body

    def make_handler(self, handler_cls: type[IndexHandler]) -> tuple[IndexHandler, io.BytesIO]:
        rfile = io.BytesIO(self.body)
        wfile = io.BytesIO()

        h = handler_cls.__new__(handler_cls)
        h.rfile = rfile
        h.wfile = wfile
        h.path = self.path
        h.command = self.method
        h.headers = self.headers  # type: ignore[assignment]

        h.response_code = None  # type: ignore[attr-defined]
        h.response_headers = {}  # type: ignore[attr-defined]

        def send_response(code: int, message: str | None = None) -> None:
            h.response_code = code  # type: ignore[attr-defined]

        def send_header(keyword: str, value: str) -> None:
            h.response_headers[keyword] = value  # type: ignore[attr-defined]

        def end_headers() -> None:
            pass

        h.send_response = send_response  # type: ignore[method-assign]
        h.send_header = send_header  # type: ignore[method-assign]
        h.end_headers = end_headers  # type: ignore[method-assign]

        return h, wfile


def test_federation_endpoint() -> None:
    req = MockRequest("GET", "/api/federation")
    h, wfile = req.make_handler(IndexHandler)
    h.do_GET()
    res = json.loads(wfile.getvalue().decode("utf-8"))
    assert res["protocol"] == "NTI-Cert/1"
    assert "endpoints" in res


def test_badge_endpoint_default_and_unranked() -> None:
    req = MockRequest("GET", "/api/badge?repo=unknown/repo")
    h, wfile = req.make_handler(IndexHandler)
    h.do_GET()
    assert h.response_code == 200  # type: ignore[attr-defined]
    assert "image/svg+xml" in h.response_headers["Content-Type"]  # type: ignore[attr-defined]
    svg = wfile.getvalue().decode("utf-8")
    assert "<svg" in svg
    assert "NTI-1" in svg


def test_registry_leaderboard_transparency_endpoints() -> None:
    for endpoint in ["/api/registry", "/api/leaderboard", "/api/transparency"]:
        req = MockRequest("GET", endpoint)
        h, wfile = req.make_handler(IndexHandler)
        h.do_GET()
        assert h.response_code == 200  # type: ignore[attr-defined]
        res = json.loads(wfile.getvalue().decode("utf-8"))
        assert isinstance(res, dict)


def test_org_endpoint(temp_store: Path) -> None:
    req = MockRequest("GET", "/api/org?name=nonexistentorg")
    h, wfile = req.make_handler(IndexHandler)
    h.do_GET()
    assert h.response_code == 200  # type: ignore[attr-defined]
    res = json.loads(wfile.getvalue().decode("utf-8"))
    assert res["org"] == "nonexistentorg"
    assert res["repo_count"] == 0


def test_certificate_endpoint(temp_store: Path) -> None:
    req = MockRequest("GET", "/api/certificate?repo=test/repo")
    h, wfile = req.make_handler(IndexHandler)
    h.do_GET()
    assert h.response_code == 200  # type: ignore[attr-defined]
    res = json.loads(wfile.getvalue().decode("utf-8"))
    assert res["repo"] == "test/repo"


def test_verify_endpoint_valid_and_invalid(temp_store: Path) -> None:
    # 1. Invalid JSON
    req1 = MockRequest("POST", "/api/verify", body=b"invalid-json")
    h1, _wfile1 = req1.make_handler(IndexHandler)
    h1.do_POST()
    assert h1.response_code == 400  # type: ignore[attr-defined]

    # 2. Invalid OIDC
    body2 = json.dumps({"oidc_claim": {}, "certificate": {}}).encode("utf-8")
    req2 = MockRequest("POST", "/api/verify", headers={"content-length": str(len(body2))}, body=body2)
    h2, _wfile2 = req2.make_handler(IndexHandler)
    h2.do_POST()
    assert h2.response_code == 401  # type: ignore[attr-defined]

    # 3. Valid OIDC + Valid Cert
    raw_cert: dict[str, Any] = {
        "spec": "NTI-Cert/1",
        "issuer": "nti",
        "issued_at": "2025-01-01T00:00:00Z",
        "id": "cert_999",
        "repo": "testorg/testrepo",
        "commit_sha": "abc1234",
        "score": 95,
        "profile": "NTI-1",
        "signature_alg": "Dilithium5",
        "issuer_pubkey": "0x123",
        "signature": "0xsig",
    }
    raw_cert["cert_hash"] = compute_cert_hash(raw_cert)

    oidc_claim = {
        "iss": "https://token.actions.githubusercontent.com",
        "aud": "nti-badge",
        "exp": time.time() + 300,
        "repository": "testorg/testrepo",
    }

    body3 = json.dumps({"oidc_claim": oidc_claim, "certificate": raw_cert}).encode("utf-8")
    req3 = MockRequest("POST", "/api/verify", headers={"content-length": str(len(body3))}, body=body3)
    h3, wfile3 = req3.make_handler(IndexHandler)
    h3.do_POST()
    assert h3.response_code == 200  # type: ignore[attr-defined]
    res3 = json.loads(wfile3.getvalue().decode("utf-8"))
    assert res3["status"] == "indexed"
    assert res3["score"] == 95
