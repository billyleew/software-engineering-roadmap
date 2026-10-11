"""CLI for local, human-reviewed engineering research."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from .core import connect, ingest_feed, list_items, store

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
    args = parser.parse_args(argv)
    try:
        path = Path(args.db)
        path.parent.mkdir(parents=True, exist_ok=True)
        with connect(path) as db:
            if args.command == "add-url":
                result = {"added": store(db, url=args.url, title=args.title, source=args.source)}
            elif args.command == "fetch":
                result = ingest_feed(db, args.url, source=args.source)
            else:
                result = list_items(db, args.limit)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"eli: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
