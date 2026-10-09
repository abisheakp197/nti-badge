from http.server import BaseHTTPRequestHandler
import json
import asyncio

# Import all handlers as functions (not BaseHTTPRequestHandler classes)
from lib.routes import route_request


class handler(BaseHTTPRequestHandler):
    """Single serverless function that routes all /api/* requests."""

    def do_GET(self):
        self._handle("GET")

    def do_POST(self):
        self._handle("POST")

    def _handle(self, method):
        path = self.path
        length = int(self.headers.get("content-length", 0)) if method == "POST" else 0
        body_raw = self.rfile.read(length).decode("utf-8") if length else ""

        try:
            status, headers, payload = asyncio.run(
                route_request(method=method, path=path, body_raw=body_raw)
            )
        except Exception as e:
            status = 500
            headers = {"Content-Type": "application/json"}
            payload = json.dumps({"error": "internal", "detail": str(e)}).encode("utf-8")

        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if isinstance(payload, str):
            payload = payload.encode("utf-8")
        self.wfile.write(payload)
