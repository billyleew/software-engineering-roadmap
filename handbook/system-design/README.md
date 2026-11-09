# System Design Case Lab — V1

The case lab turns engineering learning into evidence-based architecture practice. Inspired by a user-shared [LinkedIn system design post](https://www.linkedin.com/posts/nk-systemdesign-one_if-you-want-to-become-god-level-at-system-share-7517932711509106688-Pz78/). The post content has **not** been independently retrieved or verified; the cases below are our own proposed curriculum, not a reproduction of that post.

## Study contract

For every case, use **Read → Understand → Challenge → Design → Implement → Test → Measure → Decide**.

1. **Requirements**: users, workloads, SLOs, functional/nonfunctional requirements, privacy, constraints, and explicit assumptions.
2. **Back-of-envelope estimates**: QPS, peak traffic, bytes/day, storage growth, bandwidth, cost range; show formulas.
3. **Architecture options**: start with a minimal design; compare at least two alternatives, including a monolith or managed service where relevant.
4. **Data and APIs**: schemas, consistency, idempotency, pagination, versioning, indexes, retention.
5. **Failure modes**: dependency outages, retries, duplicates, timeouts, partial failures, recovery, disaster scenarios.
6. **Security**: authentication, authorization, abuse, secrets, PII, audit, threat model.
7. **Delivery**: local PoC, reproducible setup, CI tests, observability, load and fault tests.
8. **Decision record**: evidence, measured limits, rejected alternatives, operational complexity, next experiment.

**Rule:** no Kafka, Kubernetes, CQRS, event sourcing, Redis, sharding or microservices merely because the case is called "system design." Each choice must address a measured constraint.

## Case progression

| Level | Case | Core decisions | First measurable lab |
|---|---|---|---|
| 1 | URL shortener | ID generation, unique keys, cache, redirects | API + Postgres; measure p95 redirects and collision handling |
| 1 | Rate limiter | token bucket vs sliding window; distributed accuracy | middleware + concurrency tests |
| 1 | Notification service | delivery guarantees, provider failures, idempotency | retry worker + DLQ simulation |
| 2 | File upload service | direct upload, malware scanning, access control | signed upload + size/format validation |
| 2 | Search/autocomplete | indexes, ranking, freshness | compare SQL full-text and dedicated search |
| 2 | Activity feed | fan-out on write/read, pagination, hot users | load-test alternative feed models |
| 2 | E-commerce inventory | reservation, concurrency, overselling | transactional reservation + chaos test |
| 3 | Payment processing | idempotency, reconciliation, ledger, compliance boundaries | double-submit + partial failure simulation (no real funds) |
| 3 | Event ingestion/metrics | backpressure, at-least-once, schema evolution | webhook ingestion with durable inbox and replay |
| 3 | Multi-tenant SaaS | isolation, quotas, migration, authorization | tenant isolation security tests |
| 4 | Global chat | ordering, offline delivery, presence, partitioning | multi-client delivery and recovery tests |
| 4 | Video platform | upload pipeline, transcoding, CDN, cost | mock media workflow + throughput/cost model |

Start with **URL shortener**, **rate limiter**, then **event ingestion/metrics**. The third case can connect to the GitHub webhook metrics architecture already under discussion.

## Case template

Copy [CASE-TEMPLATE.md](CASE-TEMPLATE.md) for each new case. Store completed work in `handbook/system-design/cases/<slug>/` with `README.md`, `adr.md`, `measurements.md`, and a link to a runnable PoC. Never claim benchmark results without actual measurements.

## How ELI contributes

ELI V1 stores candidate source metadata, deduplicates it and creates a review queue. Human reviewers map an article to a case, validate claims and decide whether a lab is justified. Future AI-assisted case generation must cite original sources, distinguish sourced claims from assumptions, and require human approval before modifying a case or running infrastructure.
