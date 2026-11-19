import pytest
from event_inbox.domain import validate_event

def test_valid_event():
    key, payload = validate_event("delivery-1", {"kind": "push"})
    assert key == "delivery-1"
    assert payload == '{"kind":"push"}'

@pytest.mark.parametrize("key", ["", "with spaces", "../bad", "x" * 129])
def test_reject_invalid_ids(key):
    with pytest.raises(ValueError):
        validate_event(key, {"kind": "push"})

def test_reject_invalid_payload():
    with pytest.raises(ValueError):
        validate_event("id", {"other": 1})
