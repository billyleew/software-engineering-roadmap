"""Sign and send a local event without third-party dependencies."""
import hashlib
import hmac
import json
import os
import sys
import urllib.request

secret = os.getenv("INBOX_WEBHOOK_SECRET", "")
if not secret:
    raise SystemExit("Set INBOX_WEBHOOK_SECRET")
key = sys.argv[1] if len(sys.argv) > 1 else "demo-001"
kind = sys.argv[2] if len(sys.argv) > 2 else "push"
body = json.dumps({"delivery_id": key, "payload": {"kind": kind}}).encode()
sig = "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
request = urllib.request.Request(
    "http://127.0.0.1:8081/events", data=body,
    headers={"Content-Type": "application/json", "X-Inbox-Signature": sig},
    method="POST")
with urllib.request.urlopen(request, timeout=5) as response:
    print(response.status, response.read().decode())
