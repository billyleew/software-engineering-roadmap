"""Offline V1 acceptance tests for CLI behavior and safe defaults."""
import json
from eli.cli import main, default_db, default_sources
from eli.core import connect, list_items

def test_default_paths_are_project_relative():
    assert default_db().endswith("/data/eli.sqlite3")
    assert default_sources().endswith("/config/sources.example.json")

def test_cli_end_to_end_without_network(tmp_path, capsys):
    db = tmp_path / "eli.sqlite3"
    url = "https://www.linkedin.com/posts/nk-systemdesign-one_if-you-want-to-become-god-level-at-system-share-7517932711509106688-Pz78/?utm_source=share"
    assert main(["--db", str(db), "add-url", url, "--title", "System design study inspiration", "--source", "LinkedIn (user-shared)"]) == 0
    assert json.loads(capsys.readouterr().out)["added"] is True
    assert main(["--db", str(db), "add-url", url, "--title", "System design study inspiration", "--source", "LinkedIn (user-shared)"]) == 0
    assert json.loads(capsys.readouterr().out)["added"] is False
    assert main(["--db", str(db), "digest", "--output", str(tmp_path / "digest.md")]) == 0
    digest = (tmp_path / "digest.md").read_text()
    assert "software-architecture" in digest
    assert "System design study inspiration" in digest
    with connect(db) as connection:
        assert len(list_items(connection)) == 1

def test_default_registry_skips_without_network(tmp_path, capsys):
    db = tmp_path / "eli.sqlite3"
    assert main(["--db", str(db), "fetch-all"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["errors"] == 0
    assert result["added"] == 0
    assert all(s["status"] == "skipped" for s in result["sources"])
