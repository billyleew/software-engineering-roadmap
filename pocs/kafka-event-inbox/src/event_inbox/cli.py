"""Small CLI that exercises the real PostgreSQL persistence boundary."""
from __future__ import annotations
import argparse
import json
import os
import sys
from .storage import InboxStore

def main(argv=None):
    parser = argparse.ArgumentParser(prog="inbox")
    parser.add_argument("--dsn", default=os.getenv("INBOX_DSN",
        "postgresql://inbox:local_dev_only@127.0.0.1:55432/inbox"))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    submit = sub.add_parser("submit")
    submit.add_argument("delivery_id")
    submit.add_argument("--kind", required=True)
    work = sub.add_parser("work")
    work.add_argument("--count", type=int, default=1)
    work.add_argument("--inject-failure", action="store_true")
    work.add_argument("--delivery-id", help="Process only this delivery ID (testing)")
    fail = sub.add_parser("fail")
    fail.add_argument("delivery_id")
    sub.add_parser("summary")
    args = parser.parse_args(argv)
    store = InboxStore(args.dsn)
    try:
        if args.command == "init":
            store.initialize()
            result = {"initialized": True}
        elif args.command == "submit":
            result = {"added": store.submit(args.delivery_id, {"kind": args.kind})}
        elif args.command == "work":
            if not 1 <= args.count <= 10000:
                raise ValueError("count must be 1..10000")
            result = [store.process_one(inject_failure=args.inject_failure, delivery_id=args.delivery_id)
                      for _ in range(args.count)]
        elif args.command == "fail":
            result = {"status": store.fail_one(args.delivery_id)}
        else:
            result = store.summary()
        print(json.dumps(result, indent=2))
        return 0
    except Exception as exc:
        print(f"inbox: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
