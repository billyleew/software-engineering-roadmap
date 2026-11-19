# Kafka Case — PoC A: PostgreSQL Durable Event Inbox

**Runnable first slice:** a PostgreSQL-backed, at-least-once event inbox with unique delivery IDs, transactional processing, concurrent worker locking and deterministic projections. This is **not Kafka** and is not a production webhook service.

## Prerequisites

Python 3.11+, Docker Compose, a local port 55432 available.

```bash
cd pocs/kafka-event-inbox
docker compose up -d --wait
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[test]'
inbox init
inbox submit delivery-001 --kind push
inbox submit delivery-001 --kind push
inbox submit delivery-002 --kind issue
inbox work --count 2
inbox summary
python -m pytest -q
```

For PostgreSQL integration tests, **use a disposable database** (tests write rows):

```bash
INBOX_TEST_DSN='postgresql://inbox:local_dev_only@127.0.0.1:55432/inbox' python -m pytest -q
```

**Expected behavior:** the second `delivery-001` submission reports `added: false`. Processing both unique events produces one `push` and one `issue` projection. The injected-failure test proves a projection and its acknowledgement roll back together.

```bash
inbox submit delivery-crash --kind crash-demo
inbox work --inject-failure
inbox summary
inbox work
inbox summary
```

Use the crash demo on a clean inbox with only the intended pending event; otherwise `work` selects the oldest pending event.

## Architecture

```text
CLI (transport adapter)
  -> InboxStore (Postgres adapter)
       -> inbox_events (UNIQUE delivery_id)
       -> SELECT ... FOR UPDATE SKIP LOCKED
       -> kind_counts (transactional projection)
```

The domain module validates input and is independent of PostgreSQL. A future HTTP transport adapter can call the same application operations. This intentionally avoids interface proliferation until a second adapter or more domain complexity justifies ports.

## Guarantees and limitations

- Database transaction makes projection and processed acknowledgement atomic.
- Delivery IDs are unique; duplicate submissions are not reprocessed.
- Concurrent workers use row locking and `SKIP LOCKED`.
- A worker crash before commit rolls back its work, making the event eligible again.
- `fail` provides manual bounded retry/dead-letter state; automated poison-message handling and retries are **not yet integrated** into the worker.
- No HTTP endpoint, webhook signatures, real GitHub integration, Kafka broker, production-grade metrics or load benchmarks yet.
- All values in Compose are **local development credentials only**. Do not expose this service publicly.
- Integration tests are opt-in and should use a disposable database. The project does not yet have CI integration for PostgreSQL.
- No performance results are claimed.

## Next measurable increments

1. Add HTTP endpoint and HMAC signature verification.
2. Add bounded automatic retry with savepoints, backoff and dead-letter inspection.
3. Add reproducible load generator and p50/p95/p99 measurements.
4. Compare against a broker-backed adapter only after baseline measurements.

See [case study](../../handbook/system-design/cases/kafka-event-log/README.md) and [architecture-to-code framework](../../handbook/system-design/ARCHITECTURE-TO-CODE.md).
