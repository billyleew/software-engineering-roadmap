"""PostgreSQL adapter: atomic deduplication, leases, retry and projections."""
from __future__ import annotations
import json
import psycopg
from psycopg.rows import dict_row
from .domain import validate_event

DDL = """
CREATE TABLE IF NOT EXISTS inbox_events (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  delivery_id VARCHAR(128) NOT NULL UNIQUE,
  payload JSONB NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending','processing','processed','dead')),
  attempts INTEGER NOT NULL DEFAULT 0,
  available_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  leased_until TIMESTAMPTZ,
  last_error TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  processed_at TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS inbox_ready_idx ON inbox_events(available_at, id)
  WHERE status IN ('pending','processing');
CREATE TABLE IF NOT EXISTS kind_counts (
  kind TEXT PRIMARY KEY,
  total BIGINT NOT NULL DEFAULT 0
);
"""

class InboxStore:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def connect(self):
        return psycopg.connect(self.dsn, row_factory=dict_row)

    def initialize(self):
        with self.connect() as conn:
            conn.execute(DDL)

    def submit(self, delivery_id: str, payload: dict) -> bool:
        key, encoded = validate_event(delivery_id, payload)
        with self.connect() as conn:
            row = conn.execute(
                """INSERT INTO inbox_events(delivery_id,payload)
                   VALUES (%s,%s::jsonb) ON CONFLICT (delivery_id) DO NOTHING
                   RETURNING id""", (key, encoded)).fetchone()
            return row is not None

    def process_one(self, *, max_attempts: int = 3, lease_seconds: int = 30,
                    inject_failure: bool = False) -> dict | None:
        """One transaction claims, projects and acknowledges an event.

        A crash before commit rolls back both projection and acknowledgement.
        SKIP LOCKED prevents concurrent workers from claiming the same row.
        """
        if max_attempts < 1 or lease_seconds < 1:
            raise ValueError("positive max_attempts and lease_seconds required")
        with self.connect() as conn:
            row = conn.execute(
                """SELECT id, delivery_id, payload, attempts FROM inbox_events
                   WHERE (status='pending' AND available_at<=NOW())
                      OR (status='processing' AND leased_until<=NOW())
                   ORDER BY id FOR UPDATE SKIP LOCKED LIMIT 1"""
            ).fetchone()
            if row is None:
                return None
            # The processing state and projection are in the same transaction.
            conn.execute(
                """UPDATE inbox_events SET status='processing', attempts=attempts+1,
                   leased_until=NOW()+(%s * INTERVAL '1 second') WHERE id=%s""",
                (lease_seconds, row["id"]))
            try:
                kind = row["payload"]["kind"]
                if not isinstance(kind, str) or not kind:
                    raise ValueError("kind must be nonempty")
                conn.execute(
                    """INSERT INTO kind_counts(kind,total) VALUES (%s,1)
                       ON CONFLICT(kind) DO UPDATE SET total=kind_counts.total+1""",
                    (kind,))
                if inject_failure:
                    raise RuntimeError("injected failure before commit")
                conn.execute(
                    """UPDATE inbox_events SET status='processed', processed_at=NOW(),
                       leased_until=NULL, last_error=NULL WHERE id=%s""", (row["id"],))
                return {"delivery_id": row["delivery_id"], "status": "processed"}
            except (ValueError, RuntimeError) as exc:
                # Use a savepoint so a future adapter/database error does not
                # leave a half-applied projection in this transaction.
                # The injected error occurs after projection: transaction rollback
                # must prevent double-counting. Re-raise and do not ack.
                raise

    def fail_one(self, delivery_id: str, *, max_attempts: int = 3) -> str:
        """Mark an invalid event for bounded retry/dead-letter inspection."""
        with self.connect() as conn:
            row = conn.execute(
                """SELECT attempts FROM inbox_events
                   WHERE delivery_id=%s AND status!='processed' FOR UPDATE""",
                (delivery_id,)).fetchone()
            if row is None:
                raise ValueError("event missing or already processed")
            attempts = row["attempts"] + 1
            status = "dead" if attempts >= max_attempts else "pending"
            conn.execute(
                """UPDATE inbox_events SET status=%s, attempts=%s,
                   available_at=NOW()+(%s * INTERVAL '1 second'),
                   leased_until=NULL, last_error='manual failure' WHERE delivery_id=%s""",
                (status, attempts, min(2 ** attempts, 60), delivery_id))
            return status

    def summary(self) -> dict:
        with self.connect() as conn:
            statuses = conn.execute(
                "SELECT status,COUNT(*) AS n FROM inbox_events GROUP BY status").fetchall()
            kinds = conn.execute(
                "SELECT kind,total FROM kind_counts ORDER BY kind").fetchall()
            return {"statuses": {r["status"]: r["n"] for r in statuses},
                    "kinds": {r["kind"]: r["total"] for r in kinds}}
