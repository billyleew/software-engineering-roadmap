# Distributed Systems Foundations

A distributed system exchanges local simplicity for capabilities such as independent scaling, geographic distribution, fault isolation or organizational autonomy.

The network makes failure ambiguous. A request timeout does not tell you whether the operation failed or succeeded and the response was lost.

## Fundamental assumptions

Design as though:

```text
networks can fail
latency changes
nodes crash
clocks disagree
messages can be lost
delivery can be duplicated
messages can arrive out of order
partitions happen
dependencies become slow before becoming unavailable
partial success is normal
```

# Replication

Maintain copies of data for availability, read scale, geographic locality or recovery.

Trade-offs include replication lag, conflict handling, failover and consistency.

Common mental models:
- leader/follower;
- multi-leader;
- leaderless/quorum-based.

Ask what happens to writes during failover and what stale reads mean to the business.

# Partitioning / Sharding

Split data across nodes to increase capacity/throughput.

The partition key is an architecture decision. Poor keys create hotspots, expensive cross-partition operations and difficult rebalancing.

Ask:
- Which queries need multiple partitions?
- How will partitions be rebalanced?
- Can one customer/tenant become a hotspot?
- How is uniqueness enforced?

# Consistency

Consistency models define which values operations may observe.

Important ideas include:
- linearizable/strong behavior;
- read-after-write;
- monotonic reads;
- causal relationships;
- eventual consistency.

Do not choose consistency from database terminology alone. Begin with business invariants.

# CAP

During a network partition, a distributed system cannot simultaneously guarantee both perfect availability for every request and strong consistency across the partition.

CAP is about behavior **during partition**, not a permanent choice of only two letters.

# PACELC

PACELC adds an important everyday trade-off:

```text
If Partition -> Availability vs Consistency
Else          -> Latency vs Consistency
```

Distributed trade-offs exist even when nothing is visibly broken.

# Transactions

Local ACID transactions are extremely valuable. Avoid abandoning them merely because distributed patterns are fashionable.

Across independent services, consider whether the business workflow truly requires one atomic transaction or can model intermediate states and compensation.

# Saga

A saga coordinates a business workflow as local transactions plus subsequent actions/compensations.

Example:

```text
Create Order
 -> Reserve Inventory
 -> Authorize Payment
 -> Confirm Order
```

If payment fails, release inventory. Compensation is business behavior, not a magical database rollback: some actions may be irreversible.

# Transactional Outbox

Problem:

```text
DB commit succeeds
message publish fails
```

Writing domain state and an outbox record in the same local transaction lets a separate publisher reliably deliver the message later.

Consumers must still handle duplicates.

# Idempotency

An operation is idempotent when repeating the same logical request does not produce additional unintended effects.

For payments, use a stable idempotency key tied to the logical operation and persist the result/state. Do not rely only on "we retry once".

# Delivery semantics

"Exactly once" should trigger questions about scope and guarantees. End-to-end business exactly-once effects generally require application-level idempotency/deduplication even when infrastructure provides stronger processing guarantees.

# Ordering

Global ordering is expensive and often unnecessary. Determine the smallest scope where order matters: per account, order, aggregate, partition key, etc.

# Timeouts

Every remote call should have a deliberate timeout derived from the caller's latency budget. Infinite/default timeouts turn slow dependencies into resource exhaustion.

# Retries

Retry only failures likely to be transient and only when repeating the operation is safe.

Use bounded retries, exponential backoff and jitter. Uncoordinated retries can amplify an outage into a retry storm.

# Circuit Breaker

Stop sending requests temporarily when a dependency is demonstrably unhealthy, allowing recovery and protecting caller resources.

# Bulkhead

Separate resource pools so failure or saturation in one dependency/workload does not consume all capacity.

# Backpressure

When producers exceed consumer capacity, the system needs an explicit strategy: slow producers, buffer within limits, shed load, prioritize, or reject work.

An unbounded queue is delayed failure, not resilience.

# Concurrency

Concurrent changes require explicit semantics. Tools include:
- database constraints;
- optimistic concurrency/versioning;
- pessimistic locking where appropriate;
- compare-and-set;
- partitioned ownership/serialization.

Distributed locks should be used only with clear understanding of failure, lease and fencing semantics.

# Practice — payment timeout ambiguity

A client sends `POST /payments`. The provider charges the card, but the network drops the response. Your API sees a timeout.

Answer before writing code:
1. Can the API safely retry?
2. How is the logical payment identified?
3. Where is idempotency state stored?
4. What if two API instances process the same key concurrently?
5. What does the customer see while outcome is unknown?
6. How is reconciliation performed if the provider remains unavailable?
7. Which metrics/alerts expose the problem?

This scenario contains more architecture learning than drawing ten microservice boxes.