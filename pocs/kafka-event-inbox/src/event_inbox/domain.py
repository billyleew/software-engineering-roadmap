"""Domain policy: validation and deterministic projections."""
from __future__ import annotations
import json

MAX_PAYLOAD_BYTES = 64_000

def validate_event(delivery_id: str, payload: dict) -> tuple[str, str]:
    if not isinstance(delivery_id, str) or not (1 <= len(delivery_id) <= 128):
        raise ValueError("delivery_id must be 1..128 characters")
    if not all(c.isascii() and (c.isalnum() or c in "-_.") for c in delivery_id):
        raise ValueError("delivery_id contains invalid characters")
    if not isinstance(payload, dict) or not isinstance(payload.get("kind"), str):
        raise ValueError("payload must contain a string kind")
    encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True, allow_nan=False)
    if len(encoded.encode("utf-8")) > MAX_PAYLOAD_BYTES:
        raise ValueError("payload too large")
    return delivery_id, encoded
