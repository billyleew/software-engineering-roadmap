import socket
import sqlite3
import pytest
from eli.core import connect, normalize_url, store, list_items, ingest_feed, validate_public_url

def test_url_normalization():
    assert normalize_url("HTTPS://Example.COM/a?utm_source=x&b=2&a=1#fragment") == "https://example.com/a?a=1&b=2"

@pytest.mark.parametrize("url", ["file:///etc/passwd", "http://user:pass@example.com", "/relative", "http://"])
def test_invalid_urls(url):
    with pytest.raises(ValueError):
        normalize_url(url)

def test_dedup_and_persistence(tmp_path):
    path = tmp_path / "items.db"
    with connect(path) as db:
        assert store(db, url="https://example.com/post?utm_source=x", title="Post", source="manual")
        assert not store(db, url="https://example.com/post", title="Post", source="manual")
    with connect(path) as db:
        rows = list_items(db)
        assert len(rows) == 1
        assert rows[0]["url"] == "https://example.com/post"

def test_feed_integration_idempotent(tmp_path):
    xml = b"""<?xml version="1.0"?><rss version="2.0"><channel><title>Engineering</title>
    <item><title>Trade-offs</title><link>https://example.com/article</link></item>
    <item><title>Duplicate</title><link>https://example.com/article?utm_source=feed</link></item>
    </channel></rss>"""
    with connect(tmp_path / "feed.db") as db:
        first = ingest_feed(db, "https://example.com/feed", source="Example", fetcher=lambda _: xml)
        second = ingest_feed(db, "https://example.com/feed", source="Example", fetcher=lambda _: xml)
        assert first == {"added": 1, "duplicates": 1, "rejected": 0}
        assert second["added"] == 0
        assert len(list_items(db)) == 1

def test_ssrf_blocks_private_and_mixed_addresses():
    def fake_resolver(host, port, type):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", ("8.8.8.8", 0)),
                (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 0))]
    with pytest.raises(ValueError, match="Non-public"):
        validate_public_url("https://example.com/feed", resolver=fake_resolver)

def test_ssrf_blocks_localhost():
    with pytest.raises(ValueError):
        validate_public_url("http://localhost/admin", resolver=lambda *a, **kw: [])

def test_invalid_feed(tmp_path):
    with connect(tmp_path / "feed.db") as db:
        with pytest.raises(ValueError, match="Invalid"):
            ingest_feed(db, "https://example.com/feed", source="Example", fetcher=lambda _: b"<broken")
