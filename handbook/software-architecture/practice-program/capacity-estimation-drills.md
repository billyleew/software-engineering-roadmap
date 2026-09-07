# Capacity Estimation Drills

## Purpose

Capacity estimation is not about perfect forecasting. It is about distinguishing orders of magnitude so architecture decisions are proportionate to the problem.

## Core formulas

```text
Requests/day = daily active users × actions per user
Average RPS = requests/day ÷ 86,400
Peak RPS = average RPS × peak factor
Storage/day = writes/day × average record/object size
Bandwidth = requests/sec × average payload size
```

Use round numbers. State assumptions explicitly.

# Drill 1 — Small SaaS

Assumptions:
- 10,000 DAU;
- 20 API requests per active user/day;
- peak factor 5x;
- average response 8 KB.

Calculate:
1. requests/day;
2. average RPS;
3. peak RPS;
4. approximate outbound bandwidth at peak.

Then answer: does this scale alone justify microservices, Kafka or sharding?

# Drill 2 — Social feed

Assumptions:
- 5M DAU;
- each user opens feed 10 times/day;
- 20 posts returned per request;
- average feed item payload 2 KB;
- peak factor 4x.

Estimate feed-read RPS and payload bandwidth.

Then compare two alternatives:
- compute feed on read;
- precompute/materialize portions of feed.

Do not choose based on RPS alone. Identify follower distribution and ranking requirements that would influence the decision.

# Drill 3 — Video upload

Assumptions:
- 100,000 uploads/day;
- average upload 500 MB;
- each source generates 5 transcoded variants averaging a combined 700 MB;
- retain everything.

Estimate:
- ingest storage/day;
- transcoded storage/day;
- storage/month before replication/overhead.

Then identify which costs dominate: API CPU, storage, network egress, or transcoding compute.

# Drill 4 — Messaging

Assumptions:
- 20M daily users;
- 50 messages/user/day;
- average message envelope 1 KB;
- peak factor 6x.

Estimate message throughput at average and peak.

Then discuss why persistent connections, online-user concurrency and delivery fan-out may matter more than raw message size.

# Drill 5 — Payments

Assumptions:
- 30M payments/month;
- 40% occur during the busiest 6 hours/day;
- provider p95 latency 450 ms;
- each API instance safely handles 300 concurrent in-flight payment calls.

Estimate busiest-period average throughput and reason about concurrency using Little's-Law-style thinking:

```text
in-flight ≈ throughput × latency
```

Then add a provider slowdown from 450 ms to 5 seconds and estimate how in-flight resource demand changes without changing request rate.

Lesson: latency can become a capacity problem.

# Drill 6 — Logs and telemetry

Assumptions:
- 2,000 RPS;
- 4 structured log events/request;
- 1 KB/log event;
- 30-day retention.

Estimate raw log volume/day and/month.

Then change to 20 logs/request and calculate again.

Discuss why observability cost/cardinality/sampling are architecture concerns.

# Drill 7 — Cache economics

Baseline:
- product-detail endpoint: 4,000 RPS;
- 85% of requests target repeated hot products;
- DB query p95 80 ms;
- application p95 110 ms;
- DB CPU 75% at peak.

Propose a cache experiment.

Define before implementation:
- target hit ratio;
- acceptable staleness;
- expected DB load reduction;
- cache-failure behavior;
- measurements proving success.

Then challenge yourself: could an index/query change solve the problem more simply?

# Drill 8 — Queue backlog

A worker pool processes 800 jobs/sec while producers generate 1,000 jobs/sec for a 30-minute peak.

Calculate backlog growth.

Then answer:
- how long does recovery take if production falls to 500 jobs/sec afterward?
- what does queue depth tell you?
- why is oldest-message age also important?
- should you add workers, shed work, slow producers, or accept delay?

# Practice rule

After every calculation, write one sentence:

> "This estimate changes my architecture because..."

If the estimate does not influence a decision, it may not have been necessary.