"""Normalization, safe acquisition, and SQLite persistence."""
from __future__ import annotations

import hashlib
import ipaddress
import json
import socket
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError

MAX_BYTES = 2_000_000
TRACKING = {"fbclid", "gclid", "mc_cid", "mc_eid"}
SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
 id INTEGER PRIMARY KEY,
 canonical_url TEXT NOT NULL UNIQUE,
 title TEXT NOT NULL,
 source TEXT NOT NULL,
 published_at TEXT,
 discovered_at TEXT NOT NULL,
 content_hash TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'unread'
);
CREATE INDEX IF NOT EXISTS idx_items_source ON items(source);
"""

def normalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    if parts.scheme.lower() not in ("http", "https") or not parts.hostname or parts.username or parts.password:
        raise ValueError("Expected an absolute http(s) URL without credentials")
    host = parts.hostname.lower().rstrip(".")
    port = parts.port
    netloc = host if port is None or (parts.scheme.lower(), port) in (("http", 80), ("https", 443)) else f"{host}:{port}"
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                             if k.lower() not in TRACKING and not k.lower().startswith("utm_")))
    return urlunsplit((parts.scheme.lower(), netloc, parts.path or "/", query, ""))

def validate_public_url(url: str, resolver=socket.getaddrinfo) -> str:
    canonical = normalize_url(url)
    host = urlsplit(canonical).hostname
    if not host or host == "localhost" or host.endswith(".localhost"):
        raise ValueError("Local addresses are not allowed")
    try:
        results = resolver(host, None, type=socket.SOCK_STREAM)
    except OSError as exc:
        raise ValueError(f"DNS resolution failed for {host}") from exc
    if not results:
        raise ValueError("No DNS results")
    for result in results:
        address = ipaddress.ip_address(result[4][0].split("%")[0])
        if not address.is_global:
            raise ValueError("Non-public network address blocked")
    return canonical

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Redirects disabled: review destination explicitly")

def fetch_public(url: str, *, max_bytes: int = MAX_BYTES) -> bytes:
    """Best-effort SSRF checks; use egress firewall/proxy in hostile environments.

    DNS rebinding is not completely eliminated by pre-resolution. Do not expose
    this fetcher as a public unauthenticated URL-fetching service.
    """
    canonical = validate_public_url(url)
    req = Request(canonical, headers={"User-Agent": "EngineeringLearningIntelligence/0.1 (+research)"})
    opener = build_opener(NoRedirect)
    with opener.open(req, timeout=12) as response:
        length = response.headers.get("Content-Length")
        if length and int(length) > max_bytes:
            raise ValueError("Response exceeds maximum size")
        data = response.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError("Response exceeds maximum size")
        return data

def connect(path: str | Path) -> sqlite3.Connection:
    db = sqlite3.connect(str(path))
    db.execute("PRAGMA busy_timeout=5000")
    db.executescript(SCHEMA)
    return db

def store(db: sqlite3.Connection, *, url: str, title: str, source: str,
          published_at: str | None = None) -> bool:
    canonical = normalize_url(url)
    if not title.strip() or not source.strip():
        raise ValueError("Title and source required")
    fingerprint = hashlib.sha256((canonical + "\n" + title.strip()).encode()).hexdigest()
    cursor = db.execute(
        "INSERT OR IGNORE INTO items(canonical_url,title,source,published_at,discovered_at,content_hash) VALUES(?,?,?,?,?,?)",
        (canonical, title.strip(), source.strip(), published_at,
         datetime.now(timezone.utc).isoformat(), fingerprint))
    db.commit()
    return cursor.rowcount == 1

def ingest_feed(db: sqlite3.Connection, url: str, *, source: str,
                fetcher=fetch_public) -> dict:
    import feedparser
    raw = fetcher(url)
    parsed = feedparser.parse(raw)
    if parsed.bozo and not parsed.entries:
        raise ValueError("Invalid RSS/Atom document")
    added, duplicates, rejected = 0, 0, 0
    for entry in parsed.entries:
        link = entry.get("link")
        title = entry.get("title")
        if not link or not title:
            rejected += 1
            continue
        try:
            # Entries are metadata only: no article-page fetching.
            if not urlsplit(link).hostname:
                rejected += 1
                continue
            inserted = store(db, url=link, title=title, source=source,
                             published_at=entry.get("published") or entry.get("updated"))
            added += int(inserted)
            duplicates += int(not inserted)
        except (ValueError, TypeError):
            rejected += 1
    return {"added": added, "duplicates": duplicates, "rejected": rejected}

def list_items(db: sqlite3.Connection, limit: int = 30) -> list[dict]:
    rows = db.execute(
        "SELECT id, title, canonical_url, source, published_at, status FROM items ORDER BY id DESC LIMIT ?",
        (min(max(limit, 1), 500),)).fetchall()
    return [dict(zip(("id", "title", "url", "source", "published_at", "status"), row)) for row in rows]
