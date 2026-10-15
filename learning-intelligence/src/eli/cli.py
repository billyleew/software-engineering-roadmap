"""CLI for local, human-reviewed engineering research."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from .core import connect, ingest_feed, list_items, store
from .learning import recommendations, markdown_digest
from .sources import load_registry, fetch_all

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="eli", description="Engineering Learning Intelligence v1")
    parser.add_argument("--db", default=os.getenv("ELI_DB", "learning-intelligence/data/eli.sqlite3"))
    commands = parser.add_subparsers(dest="command", required=True)
    manual = commands.add_parser("add-url", help="Save a manually reviewed public URL (no fetching)")
    manual.add_argument("url")
    manual.add_argument("--title", required=True)
    manual.add_argument("--source", required=True)
    feed = commands.add_parser("fetch", help="Import metadata from a permitted RSS/Atom feed")
    feed.add_argument("url")
    feed.add_argument("--source", required=True)
    listing = commands.add_parser("list", help="List imported items")
    listing.add_argument("--limit", type=int, default=30)
    digest = commands.add_parser("digest", help="Generate a Markdown study review queue")
    digest.add_argument("--limit", type=int, default=20)
    digest.add_argument("--output", help="Write Markdown to this file instead of stdout")
    multi = commands.add_parser("fetch-all", help="Import from reviewed and enabled registry feeds")
    multi.add_argument("--sources", default="config/sources.example.json", help="Source registry JSON")
    source_list = commands.add_parser("sources", help="Show registry sources and their status")
    source_list.add_argument("--sources", default="config/sources.example.json", help="Source registry JSON")
    args = parser.parse_args(argv)
    try:
        if args.command == "sources":
            result = [{"id": s["id"], "name": s["name"], "mode": s["mode"], "enabled": s["enabled"], "access_reviewed": s.get("access_reviewed", False)} for s in load_registry(args.sources)]
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 0
        path = Path(args.db)
        path.parent.mkdir(parents=True, exist_ok=True)
        with connect(path) as db:
            if args.command == "add-url":
                result = {"added": store(db, url=args.url, title=args.title, source=args.source)}
            elif args.command == "fetch":
                result = ingest_feed(db, args.url, source=args.source)
            elif args.command == "fetch-all":
                result = fetch_all(db, load_registry(args.sources))
            elif args.command == "digest":
                result = markdown_digest(recommendations(db, args.limit))
            else:
                result = list_items(db, args.limit)
        if args.command == "digest":
            if args.output:
                output = Path(args.output)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(result, encoding="utf-8")
                print(f"Wrote {output}")
            else:
                print(result)
        else:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"eli: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
