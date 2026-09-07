# Architecture Defense Drills

## Purpose

A strong architect must explain not only what was selected, but why alternatives were rejected and which evidence would cause the decision to change.

Use these prompts after finishing any case study.

# Challenge set — technology pressure

## "Why not microservices?"

Answer with:
- current deployment/ownership problem;
- scaling profile;
- transaction needs;
- team size;
- operational maturity;
- measurable reason extraction would help.

A good answer may be "not yet".

## "Why not Redis?"

Explain:
- measured latency/load problem;
- whether query/index optimization was considered;
- freshness requirements;
- source of truth;
- cache-failure behavior;
- target hit ratio;
- evidence proving value.

## "Why not Kafka?"

Explain whether you need:
- replay;
- durable history;
- high stream throughput;
- multiple independent consumers;
- ordering scope;
- stream processing.

If the requirement is only asynchronous work, explain why a simpler queue may be sufficient.

## "Why not NoSQL?"

Describe:
- access patterns;
- transaction/invariant requirements;
- data model;
- partitioning needs;
- consistency needs;
- scale evidence.

## "Why not Kubernetes?"

Explain whether the workload actually needs orchestration features that simpler managed compute cannot provide economically.

## "Why no circuit breaker?"

Show timeout/retry behavior first. Explain whether repeated dependency failure creates resource exhaustion and whether fail-fast behavior provides value.

# Challenge set — scale

## "What happens at 10x traffic?"

Do not redesign everything.

Identify likely limits from current telemetry/architecture:
- CPU/memory;
- DB connections/query time;
- storage;
- queue throughput;
- dependency quotas;
- network;
- hot partitions/keys.

State what you would measure before changing architecture.

## "What happens at 100x?"

Now consider whether structure itself changes: partitioning, regionalization, workload separation, specialized storage, stronger platform automation.

Still distinguish known requirements from speculative architecture.

## "One customer becomes 40% of traffic. What changes?"

Discuss hot-key/tenant isolation, quotas, partition strategy, noisy-neighbor control and business prioritization.

# Challenge set — reliability

## "The dependency succeeded but your timeout fired. What now?"

Explain ambiguity, idempotency, pending/unknown state and reconciliation.

## "The queue delivers the message twice."

Explain consumer idempotency/deduplication and side-effect safety.

## "Messages arrive out of order."

Define whether ordering matters and at what scope. Avoid global ordering unless required.

## "The database fails during a transaction."

Explain atomicity, retry safety, client-visible semantics and unknown commit outcomes where applicable.

## "The cache is down."

Explain whether correctness depends on it and whether fallback traffic overloads the source.

# Challenge set — observability

## "How do you know this is the bottleneck?"

A strong answer references baseline evidence rather than intuition.

## "What would be on your first dashboard?"

Prefer critical user journey, RED signals, DB/dependency health, saturation and business success metrics over dozens of infrastructure charts.

## "Why do you need tracing?"

Justify it from cross-boundary diagnostic complexity. A small monolith may not need distributed tracing initially.

## "Your p50 is fine but users complain."

Investigate p95/p99, segmented traffic, dependency tails and specific journeys.

# Challenge set — organization and cost

## "Your architecture needs six platform specialists but the team has four engineers."

Re-evaluate the design. Team capability is an architecture constraint.

## "Managed service costs 3x self-hosted infrastructure. Why buy it?"

Compare total cost of ownership: engineering time, on-call, upgrades, security, recovery and opportunity cost.

## "How would you migrate away from this vendor?"

Describe lock-in surface, contract boundaries, data export/migration and whether the exit cost is acceptable relative to current value.

# Challenge set — design change

After defending the architecture, inject one new requirement:
- regulatory data residency;
- 99.99% availability;
- offline support;
- ten engineering teams;
- global users;
- audit retention for seven years;
- tenfold traffic;
- strict p99 latency;
- provider becomes unreliable;
- infrastructure budget cut by 50%.

Then answer:

```text
What stays unchanged?
What assumption is invalidated?
What component/boundary must evolve?
What new trade-off appears?
Do we need a migration or a rewrite?
What evidence will validate the change?
```

# Principal-level defense rule

Do not respond to pressure by adding technology immediately.

Use this sequence:

```text
Challenge
 -> requirement behind challenge
 -> evidence
 -> current design capability
 -> gap
 -> options
 -> trade-off
 -> smallest justified evolution
```

The ability to say "the current design is still sufficient, and here is the evidence" is as important as knowing how to design the larger system.