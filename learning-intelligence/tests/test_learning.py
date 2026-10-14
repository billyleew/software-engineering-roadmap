from eli.core import connect, store
from eli.learning import classify, recommendations, markdown_digest

def test_classify_explainable():
    result = classify("Kubernetes deployment reliability and observability")
    assert {item["track"] for item in result} >= {"platform-devops", "reliability-sre"}
    assert classify("Unrelated headline") == []

def test_recommendations_and_digest(tmp_path):
    with connect(tmp_path / "test.db") as db:
        store(db, url="https://example.org/ai", title="LLM agent evaluation", source="Example")
        store(db, url="https://example.org/other", title="An unrelated headline", source="Example")
        items = recommendations(db)
        assert items[0]["topics"][0]["track"] == "ai-engineering"
        assert items[-1]["review"] == "triage"
        md = markdown_digest(items)
        assert "LLM agent evaluation" in md
        assert "https://example.org/ai" in md
        assert "not verified claims" in md

def test_empty_digest():
    assert "No items yet" in markdown_digest([])
