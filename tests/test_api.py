"""Integration tests for API endpoints."""
import json
import io
import time
import pytest
from lib.crypto import compute_cert_hash
from api.badge import handler as BadgeHandler
from api.verify import handler as VerifyHandler
from api.registry import handler as RegistryHandler
from api.leaderboard import handler as LeaderboardHandler
from api.certificate import handler as CertificateHandler
from api.transparency import handler as TransparencyHandler
from api.org import handler as OrgHandler
from api.federation import handler as FederationHandler


class MockRequest:
    def __init__(self, method="GET", path="/", headers=None, body=b""):
        self.method = method
        self.path = path
        self.headers = headers or {}
        self.body = body

    def make_handler(self, handler_cls):
        rfile = io.BytesIO(self.body)
        wfile = io.BytesIO()

        # instantiate without calling __init__ BaseHTTPRequestHandler
        h = handler_cls.__new__(handler_cls)
        h.rfile = rfile
        h.wfile = wfile
        h.path = self.path
        h.command = self.method
        h.headers = self.headers

        # mock response methods
        h.response_code = None
        h.response_headers = {}

        def send_response(code, message=None):
            h.response_code = code

        def send_header(keyword, value):
            h.response_headers[keyword] = value

        def end_headers():
            pass

        h.send_response = send_response
        h.send_header = send_header
        h.end_headers = end_headers

        return h, wfile


def test_federation_endpoint():
    req = MockRequest("GET", "/api/federation")
    h, wfile = req.make_handler(FederationHandler)
    h.do_GET()
    res = json.loads(wfile.getvalue().decode("utf-8"))
    assert res["protocol"] == "NTI-Cert/1"
    assert "endpoints" in res


def test_badge_endpoint_default_and_unranked():
    req = MockRequest("GET", "/api/badge?repo=unknown/repo")
    h, wfile = req.make_handler(BadgeHandler)
    h.do_GET()
    assert h.response_code == 200
    assert "image/svg+xml" in h.response_headers["Content-Type"]
    svg = wfile.getvalue().decode("utf-8")
    assert "<svg" in svg
    assert "NTI-1" in svg


def test_registry_leaderboard_transparency_endpoints():
    for handler_cls in [RegistryHandler, LeaderboardHandler, TransparencyHandler]:
        req = MockRequest("GET", "/")
        h, wfile = req.make_handler(handler_cls)
        h.do_GET()
        assert h.response_code == 200
        res = json.loads(wfile.getvalue().decode("utf-8"))
        assert isinstance(res, dict)


def test_org_endpoint(temp_store):
    req = MockRequest("GET", "/api/org?name=nonexistentorg")
    h, wfile = req.make_handler(OrgHandler)
    h.do_GET()
    assert h.response_code == 200
    res = json.loads(wfile.getvalue().decode("utf-8"))
    assert res["org"] == "nonexistentorg"
    assert res["repo_count"] == 0


def test_certificate_endpoint(temp_store):
    req = MockRequest("GET", "/api/certificate?repo=test/repo")
    h, wfile = req.make_handler(CertificateHandler)
    h.do_GET()
    assert h.response_code == 200
    res = json.loads(wfile.getvalue().decode("utf-8"))
    assert res["repo"] == "test/repo"


def test_verify_endpoint_valid_and_invalid(temp_store):
    # 1. Invalid JSON
    req1 = MockRequest("POST", "/api/verify", body=b"invalid-json")
    h1, wfile1 = req1.make_handler(VerifyHandler)
    h1.do_POST()
    assert h1.response_code == 400

    # 2. Invalid OIDC
    body2 = json.dumps({"oidc_claim": {}, "certificate": {}}).encode("utf-8")
    req2 = MockRequest("POST", "/api/verify", headers={"content-length": str(len(body2))}, body=body2)
    h2, wfile2 = req2.make_handler(VerifyHandler)
    h2.do_POST()
    assert h2.response_code == 401

    # 3. Valid OIDC + Valid Cert
    raw_cert = {
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
    h3, wfile3 = req3.make_handler(VerifyHandler)
    h3.do_POST()
    assert h3.response_code == 200
    res3 = json.loads(wfile3.getvalue().decode("utf-8"))
    assert res3["status"] == "indexed"
    assert res3["score"] == 95
