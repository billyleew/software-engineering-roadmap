# Architecture Decision Process

## 1. Start with the problem

Before technologies, establish:

```text
Who has the problem?
What outcome matters?
What behavior is required?
What happens if we do nothing?
What constraints are real?
Which assumptions remain unverified?
```

A requirement such as "use Kafka" is normally a proposed solution. Ask what requirement created it: asynchronous processing, replay, decoupling, throughput, integration, auditability, or something else.

## 2. Functional requirements

Describe capabilities and critical journeys. Prioritize them rather than treating every feature as equally architectural.

Example for payments:
- authorize payment;
- capture payment;
- refund;
- query status;
- prevent duplicate charge;
- reconcile with provider.

## 3. Quality attributes

Turn vague words into scenarios. "Highly available" is not sufficient.

Example:

```text
Source: payment provider outage
Stimulus: provider is unavailable for 10 minutes
Environment: peak traffic
Expected response: requests fail safely or queue where business permits
Measure: no duplicate charges; recovery begins automatically; alert within 2 min
```

## 4. Constraints

Examples:
- four engineers;
- launch in three months;
- AWS already contracted;
- regulatory data residency;
- existing PostgreSQL expertise;
- fixed budget;
- integration with a legacy mainframe.

Constraints often eliminate technically attractive options.

## 5. Domain and boundaries

Identify business capabilities, language, invariants, ownership and transaction boundaries before drawing service boxes.

Do not equate a bounded context automatically with a microservice. A modular monolith can preserve domain boundaries without network boundaries.

## 6. Quantify enough to make decisions

Estimate:
- active users;
- requests/second average and peak;
- read/write ratio;
- data growth;
- object sizes;
- latency targets;
- availability target;
- retention;
- geographic distribution.

Back-of-the-envelope estimates need not predict reality perfectly. They reveal which constraints matter.

## 7. Generate alternatives

Always compare meaningful alternatives.

Example:

```text
A. Modular monolith + PostgreSQL + queue
B. Service-based architecture + PostgreSQL per domain group
C. Microservices + event streaming
```

## 8. Analyze trade-offs

Evaluate each option against:
- business fit;
- quality attributes;
- delivery speed;
- consistency needs;
- failure isolation;
- deployment independence;
- team ownership;
- observability;
- security;
- infrastructure cost;
- operational complexity;
- cognitive load;
- migration complexity;
- reversibility.

Architecture is usually a trade-off between desirable properties, not a search for a universally best design.

## 9. Failure analysis

For every important interaction ask:

```text
What if it is slow?
What if it is unavailable?
What if the response is lost?
What if the operation succeeds but we believe it failed?
What if the request/message arrives twice?
What if messages arrive out of order?
What if only half of the workflow commits?
What if a dependency returns incorrect data?
```

## 10. Security analysis

Identify assets, actors, trust boundaries, authentication, authorization, sensitive data, secrets, abuse cases and dependency/supply-chain risks.

Threat modeling belongs before implementation, not only in a final security review.

## 11. Operational analysis

Ask how the system will be:
- deployed;
- configured;
- observed;
- scaled;
- recovered;
- rolled back;
- debugged at 03:00;
- operated by the actual team.

## 12. Economics

Include engineering time, infrastructure, licensing, operational burden, support, incident cost, opportunity cost and exit/migration cost.

A technically elegant architecture that the company cannot economically operate is a bad architecture.

## 13. Decide and document

Use an ADR for significant decisions.

```markdown
# ADR-NNN: Decision title

## Status
Proposed / Accepted / Superseded / Deprecated

## Context
What problem and forces require a decision?

## Decision
What did we choose?

## Alternatives considered
What credible alternatives were evaluated?

## Consequences
What becomes easier and harder?

## Risks and mitigations
What can go wrong and how will risk be controlled?

## Evidence / fitness functions
How will we know the decision remains appropriate?
```

## 14. Architecture is a hypothesis

A decision is made with current evidence. Define signals that would justify revisiting it.

Example: start with a modular monolith. Reconsider extraction when a module has independent scaling pressure, a distinct availability requirement, ownership boundaries, or deployment contention that creates measurable delivery problems.

## Practice scenario

Design an online payment platform for 20,000 customers, a five-person engineering team and a six-month launch target.

Create three alternatives. Do not choose technologies first. Define requirements, quality attributes and constraints, then compare modular monolith, service-based and microservice approaches. Record the selected option as an ADR and list evidence that would cause you to revisit it.