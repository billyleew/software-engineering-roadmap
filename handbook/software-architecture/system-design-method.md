# System Design Method — From Problem to Evidence

Use this method for architecture interviews, production design, case studies and AI architecture reviews.

# Phase 1 — Clarify the problem

Do not draw boxes yet.

Capture:
- users/actors;
- business outcome;
- critical user journeys;
- functional requirements;
- explicitly excluded scope;
- assumptions/open questions.

# Phase 2 — Identify architecture drivers

Rank important quality attributes rather than saying all are equally critical.

Examples:
- correctness;
- availability;
- latency;
- throughput;
- consistency;
- security;
- auditability;
- recoverability;
- modifiability;
- cost.

Create measurable scenarios for the most important attributes.

# Phase 3 — Estimate scale

Back-of-the-envelope estimates:

```text
DAU / MAU
peak concurrent users
average + peak RPS
read/write ratio
payload/object size
data generated/day
retention
bandwidth
geographic distribution
```

Do enough mathematics to distinguish 20 RPS from 20,000 RPS and 2 GB from 2 PB. Do not create false precision.

# Phase 4 — Model the domain

Identify:
- capabilities/subdomains;
- ubiquitous language;
- invariants;
- bounded contexts;
- transaction boundaries;
- ownership.

Keep logical domain boundaries independent from deployment topology initially.

# Phase 5 — Define contracts

Design critical APIs/events and semantics:
- command/query/event;
- request/response;
- idempotency;
- error behavior;
- pagination;
- versioning;
- schema evolution.

# Phase 6 — Data design

For each important datum define:
- owner/source of truth;
- model;
- access patterns;
- transaction needs;
- consistency;
- retention;
- indexes;
- replication/partitioning only if required.

# Phase 7 — Generate architecture alternatives

Produce at least two credible options.

Example:

```text
A. Modular monolith + PostgreSQL
B. Modular monolith + queue for async work
C. Service-based architecture
```

Do not make the alternatives artificially bad just to justify your preferred solution.

# Phase 8 — Select the simplest adequate design

Compare against requirements, quality attributes, team, cost and reversibility.

Architecture should contain the minimum necessary complexity—not the minimum number of components at any cost.

# Phase 9 — Failure analysis

Walk critical paths and inject failures:
- timeout;
- lost response;
- duplicate request;
- partial commit;
- stale read;
- node failure;
- dependency outage;
- overload;
- corrupt/invalid data.

Design semantics before adding resilience patterns.

# Phase 10 — Security

Identify:
- assets;
- actors;
- trust boundaries;
- authentication;
- authorization;
- secrets;
- encryption;
- abuse/fraud;
- audit;
- supply-chain risks.

# Phase 11 — Observability before scaling

Define the minimum telemetry needed to validate architecture assumptions:

```text
RED metrics
business success/failure
DB/dependency health
structured logs
correlation IDs
critical resource saturation
```

Add distributed tracing and advanced telemetry when architecture/diagnostic complexity warrants it.

# Phase 12 — Deployment and operation

Define:
- build/artifact;
- deployment topology;
- configuration/secrets;
- database migration;
- rollout;
- rollback;
- autoscaling if justified;
- backup/restore;
- RTO/RPO;
- ownership/on-call.

# Phase 13 — Cost

Estimate relative cost of:
- compute;
- database;
- storage;
- network;
- messaging;
- observability;
- licenses;
- AI/model inference where relevant;
- engineering/operations.

# Phase 14 — ADR

Record significant decisions and rejected alternatives.

# Phase 15 — Validate and evolve

Define baselines and success signals.

```text
Assumption -> metric/evidence -> threshold -> potential decision
```

Example:

```text
Assumption: PostgreSQL handles expected reads comfortably
Evidence: DB CPU, query p99, connection saturation
Trigger: sustained saturation under expected peak after query/index optimization
Potential options: cache, replica, data-access redesign, partitioning depending on evidence
```

# Architecture review summary template

```text
Problem:
Critical requirements:
Quality attributes:
Constraints:
Scale estimates:
Domain boundaries:
Data/consistency:
Options:
Decision:
Trade-offs:
Failure modes:
Security:
Observability baseline:
Deployment/recovery:
Cost:
ADRs:
Assumptions to validate:
Evolution triggers:
```

# Core habit

Whenever someone proposes a technology, pattern or architecture style, ask:

> Which requirement, measured problem or credible constraint makes this necessary?

Whenever someone proposes scaling, ask:

> What does our telemetry say is currently limiting us?

Whenever someone proposes optimization, ask:

> What baseline will we compare against afterward?