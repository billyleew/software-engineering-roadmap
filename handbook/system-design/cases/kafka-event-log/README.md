# Case Study 01 — Kafka-Inspired Durable Event Log

**Status:** proposed (no implementation or benchmark yet)
**Source to read:** [System Design One — How Kafka Works](https://newsletter.systemdesign.one/p/how-kafka-works)
**Source status:** user-supplied educational reference; claims about production implementations require verification against [Apache Kafka documentation](https://kafka.apache.org/documentation/) and version-specific behavior.

## Learning question

When does a durable append-only log provide enough value to justify its operational complexity compared with a relational inbox/outbox or a managed queue?

**We are not rebuilding Kafka.** We will implement bounded components to understand its underlying guarantees and compare alternatives.

## First-principles research questions

1. What is the difference between queue semantics and a partitioned append-only log?
2. What does ordering guarantee within a partition, and what does it *not* guarantee globally?
3. What happens when a consumer crashes after processing but before committing progress?
4. How do retention, replay, partitions and consumer groups affect storage and throughput?
5. Which guarantees depend on producer configuration, broker replication and consumer behavior?
6. Why does end-to-end exactly-once behavior require application-level reasoning?

## PoC A — PostgreSQL durable inbox (baseline)

**Single deployable:** HTTP webhook receiver + Postgres + background worker.

- Accept a synthetic webhook with a unique delivery ID and payload.
- Persist it in a table with a unique delivery constraint; return success only after commit.
- Claim pending work transactionally, with lease/recovery semantics; implement idempotent projection.
- Record processed and failed state; bound retries and make poison messages inspectable.
- Expose basic counters and latency histograms.
- Test duplicate delivery, concurrent consumers, crash after commit, crash during processing and replay.

**Code architecture:** start with simple modules: transport adapter, application use case, domain policy, persistence adapter, worker. Introduce Hexagonal ports where they make tests and provider substitution easier; avoid needless abstractions.

## PoC B — Log semantics

Extend the exercise with a minimal *educational* append-only event log or use a local Kafka broker **only after** PoC A passes. Investigate partition-key ordering, consumer offsets, replay and retention. Do not claim equivalence to Kafka's durability or replication guarantees.

## PoC C — Architecture comparison

Compare Postgres inbox/outbox, a managed queue such as SQS (conceptual or optional cloud test), and Kafka for:

| Decision | Postgres inbox | Managed queue | Kafka |
|---|---|---|---|
| Ordering | Application-controlled | Service-specific | Per partition |
| Replay | Retain rows explicitly | Service-dependent | Retention-based |
| Operations | Reuse database | Cloud service and IAM | Broker/cluster operations |
| Delivery | Application-managed | At-least-once common | Configuration-dependent |
| Best fit | Modest load, transactional coupling | Decoupled task processing | Multiple consumers, retained streams, partitioned scale |

This table is a **starting hypothesis**, not a benchmark result.

## Evidence required before calling this complete

- Executable local setup and automated tests.
- Workload generator with fixed seed and documented environment.
- Throughput and p95/p99 ingestion-to-processing latency.
- Duplicate-processing count, recovery time and data-loss check after injected crashes.
- Storage growth and rough cost/operational comparison.
- ADR explaining why the baseline should or should not evolve.

## Explicit non-goals

Production-grade Kafka broker, distributed consensus implementation, real GitHub webhook credentials, Kubernetes deployment, public internet exposure and claims of million-event throughput without measurements.

## Knowledge gaps to discover

What changes when processing must be ordered by entity? When multiple projections need independent replay? When downstream processing is slower than ingestion? When retention requirements grow? Which bottleneck appears first: CPU, disk, database locks or external I/O?

Use [the shared case template](../../CASE-TEMPLATE.md), [Architecture-to-Code framework](../../ARCHITECTURE-TO-CODE.md), and [evaluation rubric](../../CASE-EVALUATION-RUBRIC.md).
