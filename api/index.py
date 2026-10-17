import asyncio
import json
from http.server import BaseHTTPRequestHandler
from typing import Any

from lib.routes import route_request

MAX_PAYLOAD_SIZE = 1_048_576  # 1MB


class handler(BaseHTTPRequestHandler):
    """Single serverless function that routes all /api/* requests."""

    def do_GET(self) -> None:
        self._handle("GET")

    def do_POST(self) -> None:
        self._handle("POST")

    def _handle(self, method: str) -> None:
        path = self.path
        content_type = self.headers.get("content-type", "").lower()

        try:
            length = int(self.headers.get("content-length", 0)) if method == "POST" else 0
        except ValueError:
            length = 0

        # Check payload size limit (1MB max)
        if length > MAX_PAYLOAD_SIZE:
            self._send_json_response(413, {"error": "payload too large"})
            return

        # Check Content-Type for POST requests
        if method == "POST" and content_type and "application/json" not in content_type:
            self._send_json_response(415, {"error": "unsupported media type, expected application/json"})
            return

        body_raw = self.rfile.read(length).decode("utf-8", errors="replace") if length else ""

        try:
            status, headers, payload = asyncio.run(
                route_request(method=method, path=path, body_raw=body_raw, content_type=content_type)
            )
        except Exception:  # noqa: BLE001
            status = 500
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"error": "internal_server_error", "message": "An unexpected error occurred"}).encode("utf-8")

        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        self.wfile.write(payload)

    def _send_json_response(self, status: int, data: dict[str, Any]) -> None:
        payload = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(payload)
