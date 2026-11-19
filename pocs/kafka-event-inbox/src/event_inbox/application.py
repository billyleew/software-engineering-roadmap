"""Application use cases, independent of HTTP and CLI."""
from __future__ import annotations
from typing import Protocol
from .domain import validate_event

class EventRepository(Protocol):
    def submit(self, delivery_id: str, payload: dict) -> bool: ...
    def summary(self) -> dict: ...

class IngestEvent:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, delivery_id: str, payload: dict) -> bool:
        validate_event(delivery_id, payload)
        return self.repository.submit(delivery_id, payload)
