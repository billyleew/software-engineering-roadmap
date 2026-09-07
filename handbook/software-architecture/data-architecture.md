# Data Architecture — DDIA Applied

## Principle

Choose data systems from access patterns, invariants, consistency, scale, failure behavior and operational constraints—not from database popularity.

```text
Domain invariants
 -> access patterns
 -> transaction boundaries
 -> consistency requirements
 -> expected scale
 -> failure/recovery requirements
 -> storage alternatives
 -> trade-offs
```

# Start with a relational database when it fits

PostgreSQL/MySQL-class relational databases are an excellent default for many transactional systems because they provide mature transactions, constraints, indexes, query capabilities and operational knowledge.

Do not introduce multiple database technologies merely to appear architecturally sophisticated.

# SQL vs NoSQL is not a binary maturity ladder

"NoSQL" contains different models solving different problems:
- key-value;
- document;
- wide-column;
- graph;
- search/index engines;
- time-series.

Ask what access pattern or scaling/availability constraint the model improves and what capabilities become harder.

# Data modeling

Model for both domain correctness and expected access.

Relational normalization reduces problematic duplication and update anomalies. Denormalization can improve read performance but introduces synchronization responsibility.

Do not denormalize until there is a reason you can explain and validate.

# Indexes

Indexes trade write/storage cost for read efficiency.

Before adding an index:
- identify the query/access pattern;
- inspect query plans;
- understand selectivity/cardinality;
- measure before and after;
- account for write amplification/storage.

# Transactions and invariants

Use database constraints and local transactions aggressively for invariants contained within one transactional boundary.

Examples:
- unique idempotency key;
- foreign-key relationship where appropriate;
- balance/version constraints;
- atomic order state transition.

Application checks without database protection can fail under concurrency.

# Replication

Replication can improve read capacity, availability and locality but creates questions about lag and failover.

If a write is followed immediately by a replica read, is stale data acceptable? The answer comes from product semantics.

# Partitioning

Partition when data/throughput requires it, not by default.

A good partition key distributes load while supporting dominant access patterns. Repartitioning is expensive, so understand hotspot risk and growth dimensions.

# Caching

A cache trades freshness/complexity for latency/load reduction.

Before caching, ask:
1. Is there a measured latency/load problem?
2. Can the underlying query be fixed first?
3. What is the source of truth?
4. How stale may data be?
5. How is invalidation handled?
6. What happens on cache failure?
7. Can cache stampede occur?

Common patterns:
- cache-aside;
- read-through;
- write-through;
- write-behind (higher consistency/durability complexity).

Cache invalidation is business semantics as much as infrastructure.

# OLTP vs OLAP

Operational transactional workloads and analytical workloads have different access patterns.

Avoid allowing expensive analytical queries to unpredictably damage critical transactional performance. As needs grow, separate operational and analytical paths appropriately.

# Streams and derived data

Treat indexes, caches, search views, analytics projections and materialized views as derived representations where possible. Clearly identify the authoritative source and how derived data is rebuilt/reconciled.

# Schema evolution

Data outlives application deployments.

Prefer backward/forward-compatible evolution where rolling deployments or multiple consumers coexist.

Typical safe migration:

```text
expand schema
 -> deploy compatible writers/readers
 -> migrate/backfill data
 -> switch behavior
 -> verify
 -> contract/remove old schema
```

# Data ownership in services

Independent services should not casually modify another service's tables. Shared databases can be pragmatic, especially in service-based architectures, but ownership must remain explicit.

Logical ownership is more important than slogans such as "database per service".

# Data retention, privacy and deletion

Architecture must account for:
- retention period;
- legal/regulatory requirements;
- deletion requests;
- backups;
- replicas;
- logs/events;
- encryption;
- audit requirements.

Event sourcing and immutable histories require especially careful privacy/deletion design.

# Backup is not recovery

Define RPO/RTO and regularly test restore procedures. Replication protects against some infrastructure failures but does not protect against every logical corruption or accidental deletion.

# Practical exercise — evolve a database

Start with one PostgreSQL database for an order platform.

Measure real/simulated workloads and evolve only when evidence justifies it:
1. baseline queries and p95/p99 latency;
2. add an index for a demonstrated slow access path;
3. introduce cache only for a measured repeated-read bottleneck;
4. add a read replica and define acceptable staleness;
5. simulate data growth and evaluate partitioning;
6. separate analytics when analytical load harms OLTP;
7. document each change as an architecture decision including what simpler option was rejected.

The objective is to experience **evolution from evidence**, not to end with the maximum number of data technologies.