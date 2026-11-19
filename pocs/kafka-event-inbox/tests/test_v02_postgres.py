"""Real DB integration: requires disposable INBOX_TEST_DSN."""
from concurrent.futures import ThreadPoolExecutor
import os
import uuid
import pytest
from event_inbox.storage import InboxStore

@pytest.fixture
def store():
    dsn = os.getenv("INBOX_TEST_DSN")
    if not dsn:
        pytest.skip("INBOX_TEST_DSN not set")
    s = InboxStore(dsn)
    s.initialize()
    return s

def test_concurrent_workers_process_once(store):
    key = "parallel-" + uuid.uuid4().hex
    kind = "parallel-kind-" + uuid.uuid4().hex
    store.submit(key, {"kind": kind})
    with ThreadPoolExecutor(max_workers=8) as pool:
        outcomes = list(pool.map(lambda _: store.work_one(delivery_id=key), range(8)))
    assert sum(item is not None for item in outcomes) == 1
    assert store.summary()["kinds"][kind] == 1

def test_invalid_kind_retries_then_dead(store):
    key = "poison-" + uuid.uuid4().hex
    assert store.submit(key, {"kind": ""})
    assert store.work_one(delivery_id=key, max_attempts=2)["status"] == "pending"
    # Fast-forward the retry window in this disposable test database.
    with store.connect() as conn:
        conn.execute("UPDATE inbox_events SET available_at=NOW() WHERE delivery_id=%s", (key,))
    assert store.work_one(delivery_id=key, max_attempts=2)["status"] == "dead"
    assert any(x["delivery_id"] == key for x in store.dead_letters())
    assert store.work_one(delivery_id=key) is None
