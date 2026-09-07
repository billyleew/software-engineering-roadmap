# Observability Architecture — Start Simple, Scale with Evidence

## Principle

Observability is part of architecture, not an operations feature added after implementation.

At the same time, do not begin by building an enormous telemetry platform for traffic and failure modes you do not yet have.

```text
Instrument the critical path
 -> establish baseline
 -> observe real behavior
 -> identify bottleneck/risk
 -> form hypothesis
 -> improve architecture
 -> measure again
```

Scale systems from evidence, not imagination.

## Monitoring vs observability

**Monitoring** answers known questions: is CPU high, is error rate above threshold, is the queue growing?

**Observability** helps investigate questions that were not predicted when the system was built by providing enough correlated evidence to understand internal state from system outputs.

Both are necessary.

# The core signals

## Metrics

Aggregated numeric measurements over time. Excellent for trends, alerting, SLOs and capacity decisions.

Useful categories:
- request rate;
- error rate;
- latency distributions;
- saturation;
- queue depth/age;
- resource utilization;
- dependency health;
- business outcomes.

Prefer percentiles such as p95/p99 when tail latency matters. Averages can hide poor user experience.

### RED method
For request-driven services:

```text
Rate
Errors
Duration
```

### USE method
For resources:

```text
Utilization
Saturation
Errors
```

## Logs

Logs capture discrete events and context.

Prefer structured logs over free-form strings.

Useful fields include:

```text
timestamp
level
service
version
environment
trace_id
request_id
operation
outcome
error_code
duration
```

Never log secrets, credentials, full tokens or unnecessary sensitive/regulated data.

Logs should explain meaningful state transitions and failures, not narrate every line of code.

## Distributed traces

A trace follows work across boundaries. Spans describe individual operations and dependencies.

Tracing becomes particularly valuable when a request crosses services, queues, databases or external providers.

Use trace/span IDs to correlate traces with logs and, where supported, exemplars/metrics.

Do not introduce a complex tracing estate solely because tracing exists. A small monolith may initially gain more from good metrics and structured logs.

## Events and audit trails

Operational logs and business/audit events are different concerns.

Important business transitions such as `PaymentAuthorized`, `RefundRequested` or privileged configuration changes may require durable auditability independent of ordinary application log retention.

## Profiles

Continuous or targeted profiling helps explain CPU, memory, allocation, lock/contention and runtime behavior when metrics show resource/performance problems.

Profiling is another diagnostic signal, not a substitute for metrics/traces/logs.

# Business observability

Technical health without business health can be misleading.

Examples:

```text
HTTP 2xx rate = 99.99%
payments approved = unexpectedly near zero
```

The platform looks healthy while the product is failing.

Connect system signals to outcomes such as:
- payments attempted/approved/declined;
- orders completed;
- signup conversion;
- jobs completed;
- reconciliation mismatch;
- revenue-impacting failures.

# Correlation

A useful observability model connects:

```text
Business transaction
  -> request / trace
  -> service
  -> deployment version
  -> infrastructure
  -> dependency
  -> logs / metrics / spans
```

During an incident you should be able to ask: "Which customer journey degraded after which deployment, in which dependency, and why?"

# Cardinality

Labels/dimensions make telemetry powerful but high-cardinality dimensions can create severe cost/performance problems.

Do not put unconstrained values such as user IDs, request IDs or raw URLs into metric labels. Those values may belong in traces/logs instead.

# Sampling

High-volume tracing/logging may require sampling. Sampling is a trade-off between cost and diagnostic fidelity.

Prefer policies that preserve important failures/high-latency traces where possible. Understand what evidence becomes invisible when sampling.

# Alerts

Alert on conditions requiring human action, preferably symptoms tied to user/business impact rather than every low-level anomaly.

Bad alert:

```text
CPU > 70% for 1 minute
```

Potentially better:

```text
checkout SLO burn rate indicates material risk of exhausting error budget
```

CPU can then be diagnostic evidence.

Avoid alert fatigue: a page that nobody should act on should not be a page.

# SLI, SLO and error budgets

An SLI measures a user-relevant behavior. An SLO defines the target level. The error budget expresses tolerated unreliability.

Example:

```text
SLI: proportion of valid payment-create requests completed successfully within 800 ms
SLO: 99.9% over 30 days
```

SLOs should influence engineering priorities and reliability investment rather than exist only on dashboards.

# Start-simple maturity model

## Level 0 — Development

- useful structured application logs;
- explicit error handling;
- health/readiness signals;
- correlation/request ID where useful.

## Level 1 — First production version

- RED metrics for critical endpoints;
- core resource/dependency metrics;
- business-success metrics;
- simple dashboards;
- a small number of actionable alerts;
- deployment/version annotation.

## Level 2 — Growing system

Add based on observed need:
- distributed tracing;
- queue/stream metrics;
- database/query telemetry;
- SLI/SLO/error budgets;
- centralized telemetry;
- synthetic checks;
- improved correlation.

## Level 3 — Distributed/high-scale platform

Where justified:
- OpenTelemetry-based standardized instrumentation;
- tail-aware sampling;
- service dependency maps;
- automated SLO/burn-rate alerting;
- continuous profiling;
- telemetry pipelines/collectors;
- tenant/cost controls;
- anomaly/change correlation;
- platform-provided observability defaults.

Do not jump levels because another company operates at Level 3.

# Evidence-driven scaling

Before changing architecture because "traffic may grow", establish baseline measurements:

```text
RPS / throughput
p50 / p95 / p99 latency
error rate
CPU / memory
DB connections
query latency
cache hit ratio
queue depth + oldest-message age
external dependency latency/errors
storage growth
cost per transaction/request
business throughput
```

Then identify the actual constraint.

Example:

```text
Observation: checkout p99 increased from 300 ms to 2.4 s
Evidence: application CPU remains 35%
Evidence: DB pool is saturated
Evidence: one query now consumes 70% DB time

Bad reaction: add Kubernetes nodes
Better investigation: query plan/index/data-access pattern/connection lifetime
```

# Observability-driven architecture loop

```text
Hypothesis
 -> instrumentation
 -> baseline
 -> load / real production behavior
 -> evidence
 -> bottleneck/failure mode
 -> architecture decision
 -> ADR
 -> deploy safely
 -> compare before/after
```

Architecture decisions should increasingly be supported by telemetry as the system matures.

# Observability as a design requirement

During architecture review ask:
- How will we know this capability is healthy?
- How will we know customers are succeeding?
- How will we detect partial failure?
- Can we correlate an operation across boundaries?
- How will we distinguish application, dependency and infrastructure problems?
- Which signals support capacity decisions?
- Which telemetry contains sensitive data?
- What is telemetry retention and cost?
- How do we observe the observability pipeline itself?

# Practical exercise

Start with a small checkout API and PostgreSQL.

Iteration 1: add structured logs, RED metrics, DB pool/query metrics, payment-success metric and one dashboard.

Iteration 2: generate load. Do not optimize before collecting the baseline.

Iteration 3: inject slow database queries and provider latency. Diagnose using existing evidence and record gaps.

Iteration 4: add only the missing telemetry needed to distinguish failures. If the system becomes distributed, add tracing and propagate context across HTTP/messages.

Iteration 5: make one architecture/performance change based on measured evidence and compare before/after.

The exercise succeeds when the decision is supported by data, not when the dashboard contains the largest number of charts.