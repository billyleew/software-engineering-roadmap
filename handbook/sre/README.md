# Site Reliability Engineering — Reliability as an Engineering Decision

## Objective

SRE applies software-engineering methods to operations and reliability. The goal is not maximum reliability at any cost. The goal is the level of reliability the users and business need, delivered sustainably.

```text
User journey
 -> reliability expectation
 -> SLI
 -> SLO
 -> error budget
 -> telemetry + alerting
 -> engineering/release decisions
 -> incidents + learning
 -> reliability improvement
```

# Reliability is a product property

A system can be technically "up" while the customer journey is broken.

Examples:
- API returns HTTP 200 but payment authorization never completes;
- website loads but login fails;
- queue consumers run but jobs are delayed six hours;
- checkout works but p99 latency causes abandonment.

Start from user/business outcomes, then choose technical signals.

# SLI, SLO and SLA

## SLI — Service Level Indicator

A measurement of service behavior.

Examples:
- proportion of valid requests completed successfully;
- proportion completed below a latency threshold;
- proportion of jobs completed within ten minutes;
- proportion of payment operations reaching a known terminal state.

## SLO — Service Level Objective

A target for an SLI over a window.

Example:

```text
99.9% of valid checkout requests complete successfully
within the defined measurement window.
```

An SLO is an engineering/product objective, not automatically a contractual promise.

## SLA — Service Level Agreement

A business/legal agreement that may include consequences when a service commitment is missed. Do not casually use SLA and SLO as synonyms.

# Good SLIs

Prefer signals close to user experience.

For request-driven services:
- availability/success;
- latency;
- correctness where measurable.

For asynchronous systems:
- successful processing;
- queue/job age;
- completion time;
- data freshness.

For data systems:
- successful queries/writes;
- latency;
- freshness;
- durability/recovery indicators.

# Error budgets

An SLO defines an allowed amount of unreliability.

If the objective is 99.9%, the remaining 0.1% is the conceptual error budget for the measured window/SLI.

The value is organizational: reliability and feature velocity can be discussed using shared evidence.

Error budgets should inform decisions, not become mechanical punishment.

# Burn rate

Burn rate describes how quickly error budget is being consumed relative to the allowed rate.

A fast burn indicates urgent risk; a slow burn may justify a different response.

This is often more useful than alerting on every isolated failure.

# Alerting principle

Page humans for actionable conditions threatening meaningful user/business outcomes.

Use dashboards/tickets/logs for lower-urgency diagnostics.

A CPU alert is often diagnostic. An SLO burn or critical journey failure is closer to a paging symptom.

# Toil

Toil is repetitive operational work that is manual, automatable, tactical and tends to scale with service growth.

Examples:
- repeated manual deployments;
- routine certificate renewal;
- repetitive account provisioning;
- manually restarting known-stuck jobs;
- repeated incident mitigation with known steps.

Measure and automate high-value toil. Do not automate a broken process merely to preserve it faster.

# Reliability architecture

SRE connects to architecture through:
- timeouts;
- idempotency;
- retries/backoff/jitter;
- circuit breaking when justified;
- bulkheads;
- load shedding;
- backpressure;
- graceful degradation;
- redundancy/failover;
- backup/restore;
- capacity/headroom;
- disaster recovery.

Patterns follow observed/credible failure modes.

# Incident management

A mature reliability system needs:
- detection;
- severity classification;
- clear incident command/roles;
- mitigation priority;
- communication;
- evidence/timeline;
- recovery validation;
- post-incident learning;
- high-quality follow-up actions.

During an incident, restore service before pursuing perfect root-cause analysis unless safety/correctness demands otherwise.

# Postmortems

A useful postmortem asks how the system and organization allowed the incident, not who to blame.

Study:
- initiating change/event;
- contributing conditions;
- detection gaps;
- propagation/blast radius;
- mitigation/recovery;
- what went well;
- what made response harder;
- systemic improvements.

Avoid the shallow conclusion "engineer made mistake." Human error is usually the beginning of analysis, not the end.

# Capacity engineering

Capacity is reliability work.

Observe:
- request/event rate;
- concurrency;
- latency distributions;
- CPU/memory;
- DB connections/query time;
- queue depth and oldest age;
- storage growth;
- dependency quotas;
- autoscaling behavior;
- headroom.

Scale the constrained resource, not whichever graph is easiest to see.

# Disaster recovery

Define business-driven:
- RTO — how quickly service must be restored;
- RPO — how much data loss is acceptable.

Then design backup/replication/failover accordingly and test it.

# Reliability testing

Use progressively stronger methods:

```text
unit/integration failure tests
 -> load tests
 -> dependency failure simulation
 -> recovery/restore tests
 -> game days
 -> controlled chaos experiments
```

Chaos Engineering is not random production destruction. It is hypothesis-driven experimentation about system resilience with controlled blast radius.

# Observability connection

SRE consumes observability to make decisions.

```text
Metrics -> trends, SLI/SLO, saturation
Logs -> detailed evidence
Traces -> request/dependency path
Events -> deployments/config/infrastructure changes
Profiles -> resource bottlenecks
Business metrics -> actual customer outcome
```

Telemetry that never informs a decision is a cost candidate.

# Reliability and delivery

Connect CI/CD to SRE:

```text
commit
 -> deployment
 -> change event
 -> canary/progressive exposure
 -> SLI/business telemetry
 -> continue / halt / rollback / roll-forward
```

This closes the software-delivery feedback loop.

# Learning path

1. SLI/SLO/SLA and error budgets
2. alerting and burn rates
3. incident management
4. postmortems and learning
5. toil and automation
6. capacity/headroom/autoscaling
7. reliability patterns
8. backup, restore and disaster recovery
9. game days and chaos/failure engineering
10. reliability economics and organizational trade-offs

# Principal Engineer questions

- Which user journey are we protecting?
- Is the SLI actually representative of that journey?
- Why is this SLO the right target?
- What does additional reliability cost?
- What happens when error budget is exhausted?
- Which failures page a human and why?
- What is the blast radius of this dependency?
- Can the system degrade safely?
- Is recovery tested or assumed?
- What toil is consuming engineering capacity?
- What did the last incidents teach us about architecture?
- Which reliability investment has the highest business value?

# Capstone

Use the application/platform built in the Platform Engineering labs and add:
- user-centered SLIs;
- SLOs;
- error-budget analysis;
- actionable alerts;
- incident simulation;
- runbook;
- postmortem;
- capacity/load test;
- backup/restore validation;
- failure experiment;
- reliability ADR.

The goal is to prove not only that the system runs, but that its reliability can be measured, defended, recovered and evolved.