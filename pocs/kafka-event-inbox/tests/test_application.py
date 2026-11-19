from event_inbox.application import IngestEvent

class FakeRepository:
    def __init__(self):
        self.items = {}
    def submit(self, delivery_id, payload):
        if delivery_id in self.items:
            return False
        self.items[delivery_id] = payload
        return True

def test_ingest_use_case_and_dedup():
    repo = FakeRepository()
    use_case = IngestEvent(repo)
    assert use_case.execute("evt-1", {"kind": "push"})
    assert not use_case.execute("evt-1", {"kind": "push"})
    assert len(repo.items) == 1
