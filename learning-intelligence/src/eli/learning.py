"""Transparent, deterministic learning recommendations; no model/API keys required."""
from __future__ import annotations
import json
import re
from datetime import datetime, timezone
from pathlib import Path

TOPICS = {
    "software-architecture": ("architecture", "system design", "microservice", "monolith", "domain driven", "distributed"),
    "platform-devops": ("platform engineering", "devops", "ci/cd", "deployment", "kubernetes", "terraform", "container"),
    "reliability-sre": ("sre", "reliability", "incident", "observability", "latency", "performance", "availability"),
    "security": ("security", "oauth", "authorization", "authentication", "vulnerability", "supply chain", "threat"),
    "data-systems": ("postgres", "database", "sql", "replication", "indexing", "kafka", "streaming", "queue"),
    "ai-engineering": ("llm", "agent", "rag", "embedding", "prompt", "model evaluation", "machine learning"),
    "engineering-leadership": ("cto", "principal engineer", "leadership", "finops", "engineering economics", "team"),
}

def classify(title: str) -> list[dict]:
    """Rank topic matches by keyword count. Empty means human review, not irrelevant."""
    lowered = title.casefold()
    matches = []
    for topic, keywords in TOPICS.items():
        found = [word for word in keywords if re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", lowered)]
        if found:
            matches.append({"track": topic, "score": len(found), "matched": found})
    return sorted(matches, key=lambda x: (-x["score"], x["track"]))

def recommendations(db, limit: int = 20) -> list[dict]:
    from .core import list_items
    results = []
    for item in list_items(db, limit=500):
        matches = classify(item["title"])
        results.append({**item, "topics": matches, "review": "read" if matches else "triage"})
    results.sort(key=lambda item: (-sum(t["score"] for t in item["topics"]), -item["id"]))
    return results[:min(max(limit, 1), 500)]

def markdown_digest(items: list[dict]) -> str:
    lines = ["# Engineering Learning Intelligence — Review Queue", "",
             "Generated: " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
             "", "These are **candidate topics**, not verified claims or completed learning.", "",
             "Read the original source, verify its claims and choose at most 1–2 experiments.", ""]
    if not items:
        lines.append("No items yet. Use `eli add-url` or a permitted `eli fetch` feed.")
    for item in items:
        title = item["title"].replace("\n", " ").replace("\r", " ").replace("|", "\\|")
        url = item["url"]
        # URLs have already been validated as http(s) on import.
        labels = ", ".join(t["track"] for t in item["topics"]) or "manual triage"
        lines.extend([f"## {title}", f"Source: {item['source']} — {url}",
                      f"Roadmap topics: {labels}", f"Next action: {item['review']}; verify before a PoC.", ""])
    return "\n".join(lines)
