import json
import pytest
from eli.core import connect, list_items
from eli.sources import load_registry, fetch_all

FEED = b"""<?xml version="1.0"?><rss version="2.0"><channel><title>Engineering</title>
<item><title>Database indexing</title><link>https://example.org/indexing</link></item>
</channel></rss>"""

def registry(tmp_path, entries):
    path = tmp_path / "sources.json"
    path.write_text(json.dumps({"sources": entries}))
    return path

def source(sid, url, *, enabled=True, reviewed=True):
    return {"id": sid, "name": sid, "mode": "rss", "feed_url": url,
            "enabled": enabled, "access_reviewed": reviewed}

def test_registry_validation(tmp_path):
    with pytest.raises(ValueError, match="access_reviewed"):
        load_registry(registry(tmp_path, [source("a", "https://example.org/feed", reviewed=False)]))
    with pytest.raises(ValueError, match="duplicate"):
        load_registry(registry(tmp_path, [source("a", "https://example.org/feed"),
                                         source("a", "https://example.org/feed2")]))
    with pytest.raises(ValueError, match="cannot be enabled"):
        load_registry(registry(tmp_path, [{"id": "linkedin", "name": "LinkedIn",
                                          "mode": "manual", "enabled": True}]))

def test_multi_source_partial_failure_and_rerun(tmp_path):
    sources = load_registry(registry(tmp_path, [
        source("one", "https://example.org/one"),
        source("two", "https://example.org/two"),
        source("off", "https://example.org/off", enabled=False)]))
    def fetch(url):
        if url.endswith("/two"):
            raise OSError("simulated timeout")
        return FEED
    with connect(tmp_path / "items.db") as db:
        first = fetch_all(db, sources, fetcher=fetch, sleep=lambda _: None)
        assert first["added"] == 1
        assert first["errors"] == 1
        assert first["sources"][2]["status"] == "skipped"
        assert len(list_items(db)) == 1
        second = fetch_all(db, sources, fetcher=fetch, sleep=lambda _: None)
        assert second["added"] == 0
        assert second["duplicates"] == 1

def test_two_sources_deduplicate_globally(tmp_path):
    sources = load_registry(registry(tmp_path, [
        source("one", "https://example.org/one"), source("two", "https://example.org/two")]))
    with connect(tmp_path / "items.db") as db:
        result = fetch_all(db, sources, fetcher=lambda _: FEED, sleep=lambda _: None)
        assert result["added"] == 1
        assert result["duplicates"] == 1
