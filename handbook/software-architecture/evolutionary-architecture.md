# Evolutionary Architecture — Scale When Evidence Requires It

## Principle

Architecture should support change without attempting to predict every future requirement.

```text
Build the simplest architecture that satisfies current known requirements
 -> instrument it
 -> observe real behavior
 -> identify change pressure
 -> evolve the constrained part
 -> verify improvement
```

This is not "ignore scale until production breaks". It means identify credible risks up front, preserve sensible options, and avoid paying unnecessary distributed-system cost before evidence or known requirements justify it.

# Reversible vs irreversible decisions

Spend more analysis on decisions that are expensive to reverse:
- data model/ownership;
- public contracts;
- vendor lock-in;
- partition keys;
- regulatory/data residency;
- irreversible business workflows.

Keep reversible choices lightweight.

# Architecture fitness functions

A fitness function is an automated or measurable check that protects an architectural characteristic as the system evolves.

Examples:
- module dependency rule prevents domain A importing internals of domain B;
- p95 latency remains under an agreed threshold;
- API compatibility test passes;
- no critical dependency vulnerability is accepted;
- service recovery meets RTO in resilience exercise;
- deployment frequency/lead time does not regress beyond target.

Not every architecture decision can or should be automated, but important constraints should be observable where practical.

# Scaling dimensions

"Scale" is not one thing:
- traffic;
- data volume;
- tenants/customers;
- geographic reach;
- number of engineers/teams;
- feature complexity;
- compliance obligations;
- integrations;
- availability expectations.

Different dimensions lead to different architectural changes.

# Scaling ladder

A possible evolution—not a mandatory recipe:

```text
Single application + relational DB
 -> vertical tuning / query optimization / indexes
 -> cache for measured hot reads
 -> background queue for appropriate asynchronous work
 -> replicas for read/availability needs
 -> modular boundaries strengthened
 -> extract selected service for demonstrated independent need
 -> partition data where capacity requires it
 -> multi-region only when business/reliability requirements justify it
```

At every arrow ask whether the previous architecture is actually the bottleneck.

# Modular monolith to services

Extract a module only with a reason such as:
- independent scaling profile;
- materially different availability/security requirement;
- independent release cadence causing measurable contention;
- strong ownership/team boundary;
- technology/runtime requirement;
- blast-radius isolation.

"Microservices are more scalable" is not sufficient evidence.

Before extraction, establish clean logical boundaries and contracts inside the monolith. A poorly separated module becomes a poorly separated network service.

# Strangler migration

For legacy modernization, route selected capabilities gradually from old to new implementation rather than replacing everything at once.

Useful ingredients:
- explicit routing boundary;
- compatibility layer;
- observability comparing old/new behavior;
- incremental traffic migration;
- rollback path;
- data migration/reconciliation strategy.

# Architecture technical debt

Technical debt is not simply "old technology". Record:
- decision/shortcut;
- reason it was accepted;
- consequence/interest paid;
- trigger for repayment;
- expected remediation cost.

Some debt is economically rational if consciously accepted.

# Measure architecture outcomes

Architecture should improve outcomes such as:
- reliability/SLO attainment;
- lead time;
- deployment frequency;
- change failure rate;
- recovery time;
- latency/throughput;
- cloud cost per business transaction;
- incident rate/blast radius;
- developer cognitive load;
- customer/business conversion.

Do not optimize a technical metric without connecting it to a desired outcome.

# Example — premature scaling

A team predicts massive traffic and starts with Kubernetes, 18 microservices, Kafka, Redis, three database technologies and a service mesh.

Actual first-year workload: 20 requests/second and four engineers.

The bottleneck becomes organizational and operational complexity, not compute.

Alternative:

```text
modular application
+ PostgreSQL
+ managed queue where asynchronous work is real
+ basic cache only if measured
+ CI/CD
+ structured logs + RED/business metrics
+ clear domain boundaries
```

If traffic grows, telemetry shows where the next investment belongs.

# Architecture evolution record

For each significant scaling change record:

```text
Observed evidence:
Baseline:
Problem/bottleneck:
Hypothesis:
Options considered:
Chosen change:
Expected improvement:
New complexity/cost:
Rollback:
After-change measurement:
Decision: keep / adjust / revert
```

# Exercise

Build or model an e-commerce platform in stages:

**Stage 1:** 100 users/day, two engineers.

**Stage 2:** 100k users/day; database reads become the measured bottleneck.

**Stage 3:** checkout and catalog now have different scaling/release profiles.

**Stage 4:** multiple teams and one region has strict data-residency requirements.

At each stage, modify only architecture elements justified by new requirements/evidence. Keep an ADR history showing why the architecture evolved.