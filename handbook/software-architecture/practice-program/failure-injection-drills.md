# Failure Injection Drills

## Purpose

Architecture becomes real when assumptions are stressed.

For each drill, do not start by naming a resilience pattern. First describe what the system should do, what the user should observe, and which invariant must remain true.

# Drill 1 — Lost payment response

Scenario:

```text
API -> provider: authorize payment
provider: charge succeeds
provider -> API: response lost
API: timeout
client: retries
```

Answer:
- what state does the API return after timeout?
- how is the logical payment identified?
- how are concurrent duplicates handled?
- what is persisted before/after provider call?
- how is provider reconciliation performed?
- when may the user safely retry?
- which metrics expose ambiguous outcomes?

# Drill 2 — Slow dependency

A customer-profile dependency normally responds in 80 ms but now takes 8 seconds.

Observe the impact on:
- request latency;
- connection/thread/event-loop resources;
- upstream timeouts;
- retries;
- queueing;
- user experience.

Design the initial response using timeout budgets before considering a circuit breaker.

# Drill 3 — Retry storm

A dependency returns 503 for 30 seconds. Five upstream services each retry three times immediately.

Estimate request amplification and explain how:
- bounded retry budgets;
- exponential backoff;
- jitter;
- load shedding;
- circuit breaking where appropriate
could change the failure dynamics.

# Drill 4 — Database primary failure

The primary database becomes unavailable.

Answer:
- what availability does the business require?
- is failover automatic or manual?
- what may be lost under the chosen replication mode?
- what happens to in-flight transactions?
- how are retries made safe?
- how will you know failover actually works?

Then write the RTO/RPO expected by the design.

# Drill 5 — Stale replica

A user updates their shipping address then immediately reads from a replica that is 4 seconds behind.

Decide whether this is acceptable.

If not, consider read-after-write routing, primary reads for selected operations, session consistency or another design. Do not demand strong consistency everywhere if only one journey requires it.

# Drill 6 — Queue consumer outage

Producers continue publishing for 45 minutes while consumers are unavailable.

Analyze:
- queue growth;
- oldest-message age;
- storage limits;
- business delay tolerance;
- recovery throughput;
- retry/dead-letter behavior;
- whether work remains valuable after delay.

# Drill 7 — Poison message

One invalid message crashes/retries indefinitely.

Design:
- retry classification;
- quarantine/dead-letter handling;
- alerting;
- operator ownership;
- replay after correction;
- idempotency during reprocessing.

# Drill 8 — Cache outage

Redis becomes unavailable during peak traffic.

Answer:
- is the cache an optimization or hidden source of truth?
- does traffic fall back safely to the database?
- can the database survive the miss storm?
- how are hot keys/stampedes controlled?
- should the product degrade or reject requests?

A cache outage should not reveal that the architecture secretly requires the cache for correctness unless that was a deliberate decision.

# Drill 9 — Partial saga

Order created, inventory reserved, payment authorized, shipping creation fails.

Define:
- current business state;
- compensation options;
- irreversible actions;
- retry behavior;
- user-visible status;
- reconciliation/manual intervention.

Do not describe compensation as an automatic equivalent of ACID rollback.

# Drill 10 — Region failure

A multi-region service loses one region.

Answer:
- active-active or active-passive?
- where is authoritative data?
- can traffic move safely?
- what consistency changes during partition/failover?
- what is the DNS/routing behavior?
- what dependencies remain regional?
- how often is this scenario tested?

# Drill 11 — Bad deployment

A release causes checkout errors to rise from 0.1% to 8%.

Design the detection and response:
- deployment annotation;
- error/SLO alert;
- canary metrics;
- automatic/manual rollback;
- database compatibility;
- trace/log correlation;
- post-incident learning.

# Drill 12 — Telemetry failure

The application is healthy but the telemetry collector/exporter is overloaded.

Decide:
- can telemetry backpressure application traffic?
- should telemetry be dropped/buffered?
- what data receives priority?
- how is the observability pipeline itself monitored?

Observability must not become a new single point of failure for the product.

# Review template

For every failure exercise record:

```text
Invariant at risk:
User-visible behavior:
Failure propagation:
Detection signal:
Containment mechanism:
Recovery:
Data reconciliation:
Pattern considered:
Why pattern is/is not justified:
New complexity introduced:
Test proving recovery:
```

The aim is to reason from failure semantics to patterns, never from pattern catalog to architecture.