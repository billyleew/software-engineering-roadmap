# ADR Practice Program

## Purpose

Architecture Decision Records train one of the most important architect skills: making assumptions, alternatives and consequences explicit before they disappear into implementation history.

Use ADRs only for decisions with meaningful architectural consequences. Do not document every local coding choice.

## Compact ADR template

```markdown
# ADR-NNN: Decision title

## Status
Proposed / Accepted / Superseded / Deprecated

## Context
What problem, evidence and constraints require a decision?

## Decision Drivers
Which quality attributes/business constraints matter most?

## Options Considered
What credible alternatives exist?

## Decision
What was selected and why?

## Consequences
What becomes easier? What becomes harder?

## Risks and Mitigations
What can fail or become expensive?

## Validation
Which metrics/evidence will prove the decision was useful?

## Revisit Triggers
What future evidence would cause us to reconsider?
```

# Exercise 1 — PostgreSQL vs document database

Scenario:
- new B2B SaaS;
- 3 engineers;
- relational customer/order/billing domain;
- 20 peak RPS;
- product team predicts future flexibility requirements.

Write an ADR choosing a primary database.

Your alternatives must be credible. Do not describe the non-selected database as universally worse.

Explicitly address:
- transaction needs;
- schema flexibility;
- query patterns;
- team expertise;
- scaling expectations;
- migration/reversal cost.

# Exercise 2 — Cache adoption

Production evidence:
- product endpoint p99 = 950 ms;
- 80% DB time is one repeated read query;
- DB CPU 82% at peak;
- query/index optimization already reduced cost but target p99 remains unmet;
- 2-minute staleness is acceptable.

Write the ADR for either adding cache or choosing another alternative.

Include:
- target hit ratio;
- invalidation strategy;
- source of truth;
- cache outage behavior;
- telemetry;
- removal/revisit condition.

# Exercise 3 — Queue for image processing

Image upload currently performs thumbnail generation synchronously. Users experience 7-second response times.

Options might include:
- keep synchronous and optimize;
- asynchronous DB-backed job table + workers;
- managed queue + workers;
- event streaming platform.

Choose and defend based on scale and reliability requirements.

# Exercise 4 — Microservice extraction

A modular monolith has grown to 80 engineers. The Billing module:
- has a dedicated team;
- deploys at a different cadence;
- causes shared release coordination;
- has distinct security/compliance requirements;
- consumes 60% of compute during month-end processing.

Write an ADR deciding whether to extract Billing.

Address data ownership, transaction changes, API/events, migration, failure boundaries, observability and rollback.

# Exercise 5 — Kafka vs simpler messaging

Requirement:
- send email after user registration;
- 5k registrations/day;
- one consumer;
- no replay requirement beyond failed-job retry.

Write an ADR explaining why Kafka is or is not justified.

Then modify the scenario:
- 50 independent consumers;
- replay of 30 days of history;
- 100k events/sec;
- stream analytics required.

Write a new ADR and explain which decision drivers changed.

# Exercise 6 — Circuit breaker

A remote provider occasionally fails for 2-3 seconds. The application has proper 500 ms timeouts, idempotent bounded retry, and low call volume.

Decide whether a circuit breaker adds enough value.

Then change the failure profile to 20-minute degraded periods with high concurrency and resource saturation. Revisit the ADR.

# Exercise 7 — Build vs buy

The company needs search.

Compare:
- relational full-text search;
- managed search service;
- self-hosted Elasticsearch/OpenSearch-class platform;
- SaaS search vendor.

Include engineering effort, relevance features, availability, operational ownership, cost, vendor lock-in and expected product differentiation.

# ADR review questions

After writing any ADR, challenge it:

```text
Did evidence create the decision?
Is the simplest credible alternative represented fairly?
Did I state the cost of my chosen option?
Did I confuse a solution with a requirement?
Can another architect understand why we made this decision six months later?
Did I define how we will know if I was wrong?
```

A mature ADR records uncertainty. It should not pretend architecture decisions are permanent truths.