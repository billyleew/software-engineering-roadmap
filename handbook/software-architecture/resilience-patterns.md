# Resilience Patterns — Apply Only to Real Failure Modes

Resilience is the ability to continue delivering acceptable behavior when components are slow, unavailable, overloaded or partially failing.

Patterns are not badges. Each one addresses a particular failure dynamic and can make a system worse when misapplied.

# 1. Timeout

Every remote operation needs a deliberate time budget.

Without a timeout, one slow dependency can hold threads/connections/resources until the caller itself becomes unhealthy.

Choose timeouts from end-to-end latency budgets and observed dependency behavior, not arbitrary defaults.

```text
Client budget: 1000 ms
 -> API processing: 100 ms
 -> dependency budget: 600 ms
 -> reserve for overhead/failure handling: 300 ms
```

# 2. Retry

Use when failure is likely transient and repeating the operation is safe.

Requirements:
- idempotency or naturally safe operation;
- bounded attempts/time;
- exponential backoff;
- jitter;
- awareness of caller deadline.

Never create nested uncontrolled retries across multiple layers. Three retries at each of four layers can create explosive request amplification.

# 3. Circuit Breaker

Use when a dependency's failure/latency causes repeated calls to waste resources and temporarily failing fast is useful.

Typical conceptual states:

```text
CLOSED -> failures exceed threshold -> OPEN
OPEN -> recovery interval -> HALF_OPEN
HALF_OPEN -> success -> CLOSED
          -> failure -> OPEN
```

Tune from real failure behavior. Avoid copying generic thresholds.

# 4. Bulkhead

Partition resources so one workload/dependency cannot exhaust everything.

Examples:
- separate thread/connection pools;
- per-tenant concurrency limits;
- isolated queues;
- separate worker pools.

Useful when resource contention creates blast-radius risk.

# 5. Rate limiting

Protect a capability from excessive consumption and enforce product/security policies.

Strategies include token bucket, leaky bucket, fixed/sliding windows and concurrency limits.

Choose the dimension deliberately: user, tenant, API key, IP, endpoint or expensive operation.

# 6. Load shedding

When capacity is exhausted, reject lower-priority/new work deliberately rather than allowing the entire system to collapse through uncontrolled queues and latency.

# 7. Backpressure

Communicate or enforce downstream capacity so producers do not create unbounded work.

For asynchronous systems monitor both queue depth and **age of oldest work**; a stable queue size can still hide stuck/slow processing.

# 8. Graceful degradation

Preserve critical capability while optional functionality is unavailable.

Example:

```text
Checkout critical
Recommendations optional

Recommendation service unavailable
 -> checkout continues without recommendations
```

This requires explicit product decisions about what is critical.

# 9. Fallback

Fallback is useful only if fallback behavior remains correct and safe. Returning stale account balances or approving a payment without authorization is not graceful degradation.

# 10. Idempotency

Critical whenever clients/workers may retry side-effecting operations.

Persist the logical operation identity and outcome with concurrency-safe semantics.

# 11. Dead-letter / quarantine

Messages that repeatedly fail due to permanent/data problems need an explicit inspection/recovery path rather than infinite retry.

A dead-letter queue without ownership, alerting and reprocessing procedure is merely a place where failures disappear.

# 12. Redundancy / failover

Replicas and multi-zone deployment improve resilience to particular infrastructure failures but add failover, consistency and cost concerns.

Test failover. A redundant architecture that has never exercised recovery contains unverified assumptions.

# Pattern composition

A dependency call might legitimately use:

```text
Deadline/timeout
 -> concurrency limit/bulkhead
 -> bounded retry for selected transient errors
 -> circuit breaker if repeated dependency failure warrants it
 -> fallback/degradation where business-safe
```

But every layer must be designed together. Blindly enabling all patterns can create worse latency and obscure failures.

# Retry storm example

```text
10,000 original requests
x 3 retries
= up to 30,000 dependency attempts
```

During an outage, retries can attack the system you are trying to recover.

Use backoff, jitter, retry budgets, load shedding and idempotency.

# Observability for resilience

Measure:
- timeout rate;
- retry attempts/success;
- circuit state/transitions;
- rejected requests;
- concurrency saturation;
- queue depth and age;
- dead-letter volume;
- degraded-mode usage;
- dependency latency/errors;
- customer/business impact.

A resilience pattern without telemetry is difficult to tune and may hide damage.

# Chaos and failure testing

After basic reliability exists, deliberately test realistic failures:
- dependency latency;
- dependency 5xx;
- connection reset;
- instance termination;
- DB failover;
- queue backlog;
- resource exhaustion.

Start safely in controlled environments and expand according to maturity/risk.

# Decision table

| Observed problem | Candidate | First questions |
|---|---|---|
| Slow remote call consumes resources | Timeout | What is the caller deadline? |
| Transient failure | Retry | Is repeating safe/idempotent? |
| Dependency repeatedly unhealthy | Circuit Breaker | Does failing fast protect us? |
| One dependency/workload exhausts shared pool | Bulkhead | Which resource needs isolation? |
| Incoming load exceeds allowed capacity | Rate limit / load shedding | Who/what should be prioritized? |
| Producer outruns consumer | Backpressure | Can producer slow or work be bounded? |
| Optional dependency unavailable | Graceful degradation | What capability is non-critical? |

# Exercise

Take a synchronous API calling three dependencies. First implement only deadlines/timeouts and observability. Inject latency/failures and measure behavior. Add **one resilience mechanism at a time only when the experiment demonstrates its value**. Compare latency, throughput, error rate and resource saturation before/after.