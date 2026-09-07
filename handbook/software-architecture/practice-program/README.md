# System Design Practice Program

## Objective

Turn architecture knowledge into repeatable decision-making skill.

The program is not about memorizing reference architectures. It is about practicing the same reasoning process until you can defend a design under pressure, uncertainty, scale changes and failure scenarios.

## Practice loop

```text
Clarify problem
 -> identify architecture drivers
 -> estimate scale
 -> model domain and invariants
 -> generate alternatives
 -> choose simplest adequate design
 -> analyze failure/security/operations
 -> define observability baseline
 -> defend trade-offs
 -> receive challenge questions
 -> revise architecture
 -> record ADRs
```

## Progression

### Level 1 — Fundamentals
Focus:
- requirements;
- quality attributes;
- rough capacity estimation;
- API/data model;
- simple architecture;
- basic trade-offs.

Target: 30-45 minutes per case.

### Level 2 — Distributed Systems
Add:
- idempotency;
- consistency;
- retries/timeouts;
- queues/events;
- replication;
- caching;
- failure ambiguity;
- backpressure.

Target: 45-60 minutes.

### Level 3 — Production Architecture
Add:
- SLI/SLO;
- observability;
- security/threat model;
- rollout/rollback;
- RTO/RPO;
- operational ownership;
- cost.

Target: 60-90 minutes.

### Level 4 — Principal Architect
Add:
- multiple credible alternatives;
- organization/team topology;
- migration strategy;
- architecture governance;
- technical debt;
- business/economic trade-offs;
- explicit rejection of trendy/unnecessary technology;
- evolution triggers based on evidence.

Target: design review rather than interview-only exercise.

## Weekly practice rhythm

A useful rhythm is:

```text
Day 1: new case — first-pass design
Day 2: capacity + data + consistency review
Day 3: failure/security/observability review
Day 4: challenge/defense session
Day 5: rewrite architecture + ADRs
```

One deeply reviewed case is more valuable than five superficial diagrams.

## Required deliverables per case

1. Problem statement and scope
2. Functional requirements
3. Ranked quality attributes
4. Constraints and assumptions
5. Scale estimates
6. Domain boundaries and invariants
7. API/event contracts
8. Data ownership and consistency model
9. At least two architecture alternatives
10. Chosen design and explicit trade-offs
11. Failure-mode analysis
12. Security analysis
13. Observability baseline
14. Deployment/recovery strategy
15. Cost/operational complexity analysis
16. ADRs
17. Evolution triggers
18. Post-review revision notes

## Rule of the program

You do not earn points for mentioning Redis, Kafka, Kubernetes, microservices, CQRS or any other technology.

You earn points for proving why a component is necessary, explaining its cost, and knowing when not to use it.