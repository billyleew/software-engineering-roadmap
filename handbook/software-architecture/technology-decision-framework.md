# Technology Decision Framework — Problem Before Product

## Purpose

Technologies, architecture styles and patterns are tools. A tool being excellent at solving one class of problem does not mean your system has that problem.

The architect's job is not to maximize the number of technologies in a diagram. It is to minimize accidental complexity while satisfying business and technical requirements.

## The decision sequence

```text
Problem
 -> Evidence
 -> Requirement / quality attribute
 -> Constraints
 -> Simplest viable option
 -> Alternatives
 -> Trade-offs
 -> Decision
 -> Instrumentation
 -> Verify
 -> Evolve only when evidence changes
```

## Technology adoption questions

Before adding an architectural component ask:

1. What concrete problem are we solving?
2. What evidence shows the problem exists or is a hard known requirement?
3. What happens if we do nothing?
4. Can the current technology solve it with configuration, indexing, tuning or a simpler design?
5. What is the simplest alternative?
6. What capability does the new technology add?
7. What new failure modes does it create?
8. What operational expertise does it require?
9. What security surface does it add?
10. What does it cost to operate, observe, upgrade and recover?
11. How do we migrate away from it?
12. Which metric will prove that adoption helped?

# Monolith vs microservices

## Bad reasoning

```text
Monoliths do not scale.
Microservices are modern.
Therefore: microservices.
```

## Better reasoning

A well-designed monolith can scale very far. A poorly designed microservice ecosystem can become a distributed monolith with worse reliability and delivery characteristics.

Start with logical modularity. Introduce network boundaries when there is demonstrated value such as independent scaling, deployment, ownership, security or failure isolation.

## Evidence that may justify extraction

- one module has materially different scaling pressure;
- deployment contention is measurably slowing teams;
- a capability needs different availability/security isolation;
- a stable domain boundary maps to independent ownership;
- a workload requires a materially different runtime/resource profile.

# Relational vs NoSQL

## Bad reasoning

```text
NoSQL scales better.
SQL is old.
Therefore: replace MySQL/PostgreSQL.
```

## Better reasoning

Relational databases provide powerful transactions, constraints, indexes and flexible querying. NoSQL models make different trade-offs for specific access, scale, distribution or schema needs.

Questions before changing:
- Which query/data model does relational storage fail to support adequately?
- Is the problem actually an index/query/schema issue?
- What transaction/constraint capabilities will be lost or moved into application logic?
- Is horizontal partitioning truly required?
- What consistency behavior does the business permit?

# Redis / caching

## Bad reasoning

```text
Redis is fast.
Every service should have Redis.
```

## Better reasoning

A cache introduces duplicated state and invalidation/freshness problems. Use it when measured repeated reads, expensive computation, session/state patterns, rate limiting or another concrete use case justifies it.

Before caching:
- measure source latency/load;
- optimize source/query first where sensible;
- define TTL/freshness;
- define source of truth;
- define behavior when cache is unavailable;
- understand stampede/hot-key risk;
- measure hit ratio and actual latency/load improvement.

# Kafka / event streaming

## Bad reasoning

```text
We are event-driven, so use Kafka.
```

## Better reasoning

Kafka-class logs are valuable when durable ordered streams, replay, high throughput, multiple independent consumers or stream processing are genuine requirements.

A simpler queue/broker, managed messaging service, database outbox plus worker, or even synchronous interaction may fit better.

Questions:
- Do we require replay?
- How long must events be retained?
- How many independent consumers?
- What ordering scope?
- What throughput?
- Is event history itself valuable?
- Can the team operate the platform or should it be managed?

# RabbitMQ / queues

Queues are excellent for asynchronous work distribution and routing patterns, but do not introduce a broker when a synchronous operation is simpler and business semantics require an immediate result.

Understand acknowledgement, redelivery, dead-letter handling, durability, ordering and backpressure rather than treating the broker as magic reliability.

# Circuit breaker

## Bad reasoning

```text
Distributed systems need circuit breakers.
Put one around every call.
```

## Better reasoning

A circuit breaker is useful when repeated calls to a failing/slow dependency would consume resources or amplify failure and when temporary rejection/fallback is meaningful.

It can be unnecessary or harmful when:
- failures are not transient;
- there is no useful fallback/degradation;
- thresholds are poorly tuned;
- another layer already provides equivalent protection;
- the dependency is local/not a failure boundary.

Always start with sensible timeouts. Add retries only for safe transient failures. Add a circuit breaker when the failure dynamics justify it.

# Kubernetes

Kubernetes solves orchestration problems: scheduling, service discovery, desired-state reconciliation, scaling, rollout and workload management. It also creates a substantial platform and cognitive surface.

Do not ask "Should we use Kubernetes?" Ask whether the workload/team has orchestration requirements that justify it versus simpler managed compute/serverless/container platforms.

# Pattern stacking anti-pattern

Avoid designs such as:

```text
Microservices
+ Kafka
+ Redis
+ Service Mesh
+ CQRS
+ Event Sourcing
+ Circuit Breakers everywhere
+ Kubernetes
```

unless each element has its own demonstrated architectural force.

Every added component creates:

```text
capability
+ dependency
+ failure mode
+ security surface
+ observability requirement
+ upgrade lifecycle
+ expertise requirement
+ financial cost
```

# Architecture complexity budget

Treat complexity as a limited budget. Spend it where it buys measurable business/quality value.

Prefer essential domain complexity over accidental infrastructure complexity.

# Technology ADR extension

For technology adoption, include:

```text
Observed problem/evidence:
Requirement/quality attribute:
Current solution and limitation:
Options:
Why the simplest option is insufficient:
Chosen technology/pattern:
New complexity introduced:
Failure modes:
Operational ownership:
Security implications:
Cost:
Success metrics:
Exit/reversal strategy:
Review trigger/date:
```

# Exercise — remove technologies

Given this proposed architecture:

```text
React
 -> API Gateway
 -> 12 microservices
 -> Redis per service
 -> Kafka
 -> Elasticsearch
 -> PostgreSQL
 -> MongoDB
 -> Kubernetes
 -> Service Mesh
```

The product has 3 engineers, 5,000 customers and 15 peak RPS.

Do not justify the diagram. Remove every component that lacks a demonstrated requirement. Build the simplest credible architecture, instrument it, and write the evidence that would justify adding each removed technology later.