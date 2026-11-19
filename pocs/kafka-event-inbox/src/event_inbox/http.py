"""Local-only HTTP adapter. HMAC authenticates raw request bytes."""
from __future__ import annotations
import hashlib
import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .application import IngestEvent
from .storage import InboxStore

MAX_BODY = 64_000

def make_handler(store: InboxStore, secret: str):
    if not secret:
        raise ValueError("INBOX_WEBHOOK_SECRET must be configured")

    class Handler(BaseHTTPRequestHandler):
        def respond(self, status: int, payload: dict):
            body = json.dumps(payload).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path == "/healthz":
                self.respond(200, {"ok": True})
            elif self.path == "/stats":
                try:
                    self.respond(200, store.summary())
                except Exception:
                    self.respond(503, {"error": "database unavailable"})
            else:
                self.respond(404, {"error": "not found"})

        def do_POST(self):
            if self.path != "/events":
                self.respond(404, {"error": "not found"})
                return
            try:
                size = int(self.headers.get("Content-Length", "-1"))
            except ValueError:
                size = -1
            if size < 0 or size > MAX_BODY:
                self.respond(413, {"error": "invalid request size"})
                return
            raw = self.rfile.read(size)
            signature = self.headers.get("X-Inbox-Signature", "")
            expected = "sha256=" + hmac.new(secret.encode("utf-8"), raw, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected):
                self.respond(401, {"error": "invalid signature"})
                return
            try:
                event = json.loads(raw)
                if not isinstance(event, dict):
                    raise ValueError("JSON object required")
                if set(event) != {"delivery_id", "payload"}:
                    raise ValueError("expected delivery_id and payload")
                added = IngestEvent(store).execute(event["delivery_id"], event["payload"])
            except (ValueError, TypeError, UnicodeDecodeError):
                self.respond(400, {"error": "invalid event"})
                return
            except Exception:
                self.respond(503, {"error": "storage unavailable"})
                return
            self.respond(202 if added else 200, {"added": added})

    return Handler

def serve(store: InboxStore, *, host: str = "127.0.0.1", port: int = 8081,
          secret: str | None = None):
    secret = secret if secret is not None else os.getenv("INBOX_WEBHOOK_SECRET", "")
    server = ThreadingHTTPServer((host, port), make_handler(store, secret))
    try:
        print(f"Listening on http://{host}:{port}", flush=True)
        server.serve_forever()
    finally:
        server.server_close()
