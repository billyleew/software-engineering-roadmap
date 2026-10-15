"""Explicit opt-in source registry and resilient multi-feed ingestion."""
from __future__ import annotations
import json
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from .core import ingest_feed, normalize_url, fetch_public

def load_registry(path: str | Path) -> list[dict]:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or not isinstance(raw.get("sources"), list):
        raise ValueError("Registry must be an object with a sources array")
    sources, ids = [], set()
    for index, entry in enumerate(raw["sources"]):
        if not isinstance(entry, dict):
            raise ValueError(f"Source {index} must be an object")
        name, sid, mode = entry.get("name"), entry.get("id"), entry.get("mode")
        if not isinstance(sid, str) or not sid.strip() or sid in ids:
            raise ValueError(f"Missing/duplicate source id at {index}")
        ids.add(sid)
        if not isinstance(name, str) or not name.strip() or mode not in ("rss", "manual"):
            raise ValueError(f"Invalid name or mode for {sid}")
        if type(entry.get("enabled")) is not bool:
            raise ValueError(f"Source {sid} requires boolean enabled")
        url = entry.get("feed_url")
        if mode == "rss":
            if not isinstance(url, str) or not url:
                raise ValueError(f"RSS source {sid} requires feed_url")
            normalize_url(url)  # format only: no network on registry read
            if entry["enabled"] and entry.get("access_reviewed") is not True:
                raise ValueError(f"Enabled RSS source {sid} requires access_reviewed=true")
        elif entry["enabled"]:
            raise ValueError(f"Manual source {sid} cannot be enabled for automatic fetching")
        sources.append(entry)
    return sources

def fetch_all(db, sources: list[dict], *, fetcher=fetch_public, sleep=time.sleep) -> dict:
    results = []
    for source in sources:
        if source["mode"] != "rss" or not source["enabled"]:
            results.append({"id": source["id"], "status": "skipped"})
            continue
        try:
            stats = ingest_feed(db, source["feed_url"], source=source["name"], fetcher=fetcher)
            results.append({"id": source["id"], "status": "ok", **stats})
        except (ValueError, OSError, HTTPError, URLError, TimeoutError) as exc:
            # Keep failures isolated and never expose exception URLs containing tokens.
            results.append({"id": source["id"], "status": "error", "error_type": type(exc).__name__})
        sleep(0.5)  # modest pacing between enabled sources
    return {"sources": results, "added": sum(x.get("added", 0) for x in results),
            "duplicates": sum(x.get("duplicates", 0) for x in results),
            "rejected": sum(x.get("rejected", 0) for x in results),
            "errors": sum(x["status"] == "error" for x in results)}
