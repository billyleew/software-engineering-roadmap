# SLOs, Error Budgets & Alerting — Measure What Users Experience

## Start with the journey

Do not begin by selecting 99.99% because it sounds professional.

```text
critical user journey
 -> failure definition
 -> measurable indicator
 -> objective
 -> budget
 -> alerting policy
 -> engineering decisions
```

# Define valid events

An availability SLI commonly has a ratio form:

```text
successful valid events / total valid events
```

The difficult part is defining valid and successful correctly.

Questions:
- Are client mistakes counted against service availability?
- Are cancelled requests included?
- Is HTTP 200 enough, or must business processing succeed?
- How are timeouts classified?
- How are unknown outcomes handled?
- Are planned maintenance periods included?

Document semantics explicitly.

# Latency SLIs

A service can be technically successful but unusably slow.

Possible SLI:

```text
proportion of valid requests completed < 500 ms
```

A threshold-based SLI can connect naturally to error budgets: requests slower than the target consume budget.

Use p95/p99 for diagnostics/capacity, but think carefully before defining contractual/product behavior only from percentile graphs.

# Asynchronous SLIs

For queues/jobs, endpoint availability may be misleading.

Examples:
- 99.9% of accepted jobs complete within 10 minutes;
- 99.95% of messages reach terminal processing without manual intervention;
- oldest queue age remains within the customer freshness requirement.

Queue depth alone is often insufficient; 10,000 messages can be healthy at high throughput while 100 messages stuck for hours are unhealthy.

# Business SLIs

Where feasible connect technical reliability to outcomes:
- payment completion;
- order placement;
- login success;
- search result availability;
- data freshness;
- notification delivery.

Do not let business metrics replace technical diagnostics; use both.

# Choosing an SLO

Inputs include:
- user expectation;
- business impact;
- historical capability;
- dependency reliability;
- architecture cost;
- competitive/product requirements;
- recovery capability.

Higher reliability has nonlinear cost. Moving from 99.9 to 99.99 may require substantially different architecture and operations.

# Error-budget arithmetic

For an SLO target `T`, the conceptual allowed bad fraction is:

```text
1 - T
```

For a time-based approximation over 30 days:

```text
99%    -> about 7h 12m
99.9%  -> about 43m 12s
99.99% -> about 4m 19s
```

But request/event-based SLIs should be calculated from events rather than translating everything into downtime.

# Burn rate

If a 30-day error budget is consumed at 1x continuously, it is exhausted at the end of the window.

A 14x burn indicates consumption far faster than sustainable. Multi-window burn-rate alerting can distinguish urgent fast failures from slower persistent degradation.

Do not memorize one threshold set as universal. Tune based on SLO, traffic, response process and false-positive tolerance.

# Alert design

A page should generally be:
- user-impacting or imminently threatening SLO/business outcomes;
- actionable;
- urgent enough to wake/interupt a human;
- supported by a useful runbook/context.

Diagnostics such as CPU, disk or replica lag may support investigation without always paging directly.

# Symptom vs cause

Prefer paging on symptoms:

```text
checkout success falling
SLO burn high
queue jobs too old
```

Then use cause signals:

```text
DB CPU
connection saturation
pod OOM
provider latency
```

This reduces pages for infrastructure conditions that have no meaningful customer impact.

# Alert context

An alert should help answer:
- what user/service is affected?
- severity?
- current SLI/SLO burn?
- when started?
- recent deployments/config/infra changes?
- dashboard/runbook?
- likely dependency scope?

# Alert fatigue

Track:
- pages per on-call period;
- actionable vs non-actionable pages;
- repeated duplicate alerts;
- alerts auto-resolving without action;
- time to acknowledge/mitigate;
- top noisy rules.

Every useless page trains humans to distrust the system.

# Practical exercise — checkout

Suppose checkout receives 2,000,000 valid requests in 30 days and the SLO is 99.9% success.

Allowed bad requests:

```text
2,000,000 * 0.001 = 2,000
```

Now simulate:
- release causes 500 failed checkouts in 10 minutes;
- external provider causes 900 failures later;
- intermittent database issue causes another 800.

The service has exceeded its budget.

Discuss decisions:
- release policy changes?
- provider resilience?
- reliability work priority?
- whether failures belong in this SLI based on service responsibility?

# Exercise — false green

Dashboard says:

```text
HTTP availability = 99.99%
latency p95 = 180ms
CPU = 40%
```

But payment completion drops 30% because requests return `200 Accepted` while downstream processing is stuck.

Design a better SLI and alert.

# Exercise — alert review

Given alerts:
- CPU > 80% for 5m;
- any single HTTP 500;
- queue depth > 100;
- checkout success below target with rapid error-budget burn;
- disk 70%;

Classify each as page/ticket/dashboard/remove based on a supplied product context. Defend the choice.

# Principal review

For every SLO ask:
- Who cares about this behavior?
- What failure does it represent?
- Can the service actually control it?
- Is measurement trustworthy?
- What architecture is required to meet it?
- What does that architecture cost?
- What decision changes when budget burns?

An SLO with no consequence for engineering/product decisions is often just a dashboard target.