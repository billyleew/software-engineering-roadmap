"""Integration tests require INBOX_TEST_DSN and a disposable database."""
import os
import uuid
import pytest
from event_inbox.storage import InboxStore

@pytest.fixture
def store():
    dsn = os.getenv("INBOX_TEST_DSN")
    if not dsn:
        pytest.skip("Set INBOX_TEST_DSN to run real PostgreSQL integration tests")
    s = InboxStore(dsn)
    s.initialize()
    return s

def test_dedup_projection_and_crash_rollback(store):
    key = "test-" + uuid.uuid4().hex
    kind = "kind-" + uuid.uuid4().hex
    assert store.submit(key, {"kind": kind})
    assert not store.submit(key, {"kind": kind})
    with pytest.raises(RuntimeError, match="injected"):
        store.process_one(inject_failure=True)
    assert kind not in store.summary()["kinds"]
    assert store.process_one() == {"delivery_id": key, "status": "processed"}
    assert store.summary()["kinds"][kind] == 1
