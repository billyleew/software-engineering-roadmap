import hashlib
import hmac
import http.client
import json
import threading
from http.server import ThreadingHTTPServer
from event_inbox.http import make_handler

class FakeStore:
    def __init__(self):
        self.events = {}
    def submit(self, key, payload):
        if key in self.events:
            return False
        self.events[key] = payload
        return True
    def summary(self):
        return {"events": len(self.events)}

def test_http_hmac_and_dedup():
    store = FakeStore()
    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(store, "test-secret"))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        raw = json.dumps({"delivery_id": "http-1", "payload": {"kind": "push"}}).encode()
        signature = "sha256=" + hmac.new(b"test-secret", raw, hashlib.sha256).hexdigest()
        def send(sig):
            conn = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
            try:
                conn.request("POST", "/events", body=raw,
                             headers={"X-Inbox-Signature": sig, "Content-Type": "application/json"})
                response = conn.getresponse()
                return response.status, json.loads(response.read())
            finally:
                conn.close()
        assert send("bad")[0] == 401
        assert send(signature) == (202, {"added": True})
        assert send(signature) == (200, {"added": False})
        assert len(store.events) == 1
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=3)
