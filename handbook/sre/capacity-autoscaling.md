# Capacity Engineering & Autoscaling — Scale the Bottleneck, Not the Diagram

## Objective

Capacity engineering determines whether the system has enough resources and headroom to satisfy workload and reliability objectives.

```text
workload
 -> demand model
 -> resource consumption
 -> bottleneck
 -> headroom
 -> scaling/recovery behavior
 -> cost
```

# Establish workload shape

Measure/estimate:
- requests/events per second;
- peak/average ratio;
- concurrency;
- payload size;
- read/write mix;
- job arrival rate;
- processing time;
- storage growth;
- tenant skew;
- geographic/time patterns.

Averages hide peaks.

# Little's Law intuition

For a stable system:

```text
concurrency ≈ throughput × time-in-system
```

If a dependency slows from 0.2s to 5s at the same request rate, required in-flight concurrency can increase 25x. Latency can therefore become a capacity problem even without traffic growth.

# Saturation

Saturation means demand is approaching/exceeding a constrained resource's useful capacity.

Potential resources:
- CPU;
- memory;
- threads/event loops;
- connection pools;
- DB connections/locks/IO;
- network bandwidth;
- disk IOPS;
- queue consumers;
- provider quotas.

Observe saturation together with user latency/errors.

# Queues

Track both:
- depth;
- oldest-message/job age.

Also measure arrival vs processing rate.

If:

```text
produce = 1000 jobs/s
consume = 800 jobs/s
```

backlog grows 200/s. Autoscaling consumers helps only if downstream systems can handle the additional concurrency.

# Headroom

Running permanently at the edge of saturation reduces resilience to bursts, failures and slower dependencies.

Headroom should reflect:
- scale-up time;
- traffic variability;
- failure scenarios;
- SLO requirements;
- cost.

Do not choose a universal 50% or 30% rule without context.

# Vertical vs horizontal scaling

Vertical: more resources per instance. Often simplest until limits/cost/failure constraints appear.

Horizontal: more instances/partitions/workers. Requires workload to distribute effectively and dependencies to scale accordingly.

"Horizontal is more scalable" does not mean it is always the first choice.

# Autoscaling signals

CPU can work for CPU-correlated workloads.

Other signals may be better:
- request concurrency;
- requests/sec per instance;
- queue age/depth;
- active connections;
- custom work units.

Choose a signal that predicts the constrained capacity.

# Autoscaling dynamics

Consider:
- measurement delay;
- provisioning/startup time;
- cooldown/stabilization;
- burst size;
- scale-down safety;
- minimum capacity;
- downstream limits.

Autoscaling is a feedback controller. Poor tuning can oscillate.

# Database bottlenecks

Before scaling architecture, inspect:
- slow queries/query plans;
- indexes;
- connection management;
- lock contention;
- transaction duration;
- N+1 patterns;
- unnecessary reads/writes;
- data model.

Example:

```text
app CPU 35%
DB CPU 85%
connection pool saturated
one query = 70% DB time
```

Adding application replicas may worsen the bottleneck.

# Cache as capacity tool

Cache can reduce repeated expensive work, but first quantify:
- workload eligible for caching;
- expected hit ratio;
- acceptable staleness;
- invalidation model;
- source-of-truth behavior;
- failure/stampede risk.

# Load testing

Use tests to answer hypotheses:
- sustainable throughput?
- saturation point?
- latency curve?
- autoscaling response?
- dependency limit?
- recovery after overload?

Test realistic data/access distributions. A database query against 100 rows in staging says little about 500 million production rows.

# Capacity observability

A useful dashboard connects:

```text
traffic/work arrival
 -> concurrency
 -> latency/errors
 -> app saturation
 -> dependency saturation
 -> scaling action
 -> cost
```

Annotate deployments/config/infrastructure changes.

# Cost-aware capacity

Overprovisioning buys headroom but costs money. Underprovisioning risks SLOs.

Track:
- cost per request/job/order;
- idle capacity;
- peak capacity;
- autoscaling efficiency;
- reserved/committed capacity economics where relevant.

# Capacity review exercise

Scenario:
- 1,000 RPS current peak;
- app instances 30% CPU;
- DB CPU 78%;
- DB connection pool 90%;
- p99 rising;
- product predicts 2x traffic in six months.

Candidate proposals:
1. double Kubernetes replicas;
2. add Redis;
3. shard database;
4. inspect queries/indexes/connections;
5. upgrade DB vertically;
6. introduce read replicas.

Rank what to investigate/do first and state what evidence would justify each later option.

# Principal Engineer questions

- What is the actual bottleneck?
- What telemetry proves it?
- What is peak vs average workload?
- What headroom does the SLO require?
- How fast can capacity be added?
- Does scaling one tier overload another?
- Is the bottleneck an inefficient query/code path rather than infrastructure?
- What is the cost of extra headroom?
- What happens during dependency slowdown?
- What threshold would justify partitioning/sharding?