# Software Architecture & System Design

## Objective

Develop the ability to turn business problems and constraints into architecture decisions that can be explained, tested, operated, secured and evolved.

Architecture is not choosing technologies. Architecture is deciding which structural choices matter, why they matter, and which trade-offs the organization is willing to accept.

## Architecture decision flow

```text
Business objective / user problem
 -> Functional requirements
 -> Quality attributes
 -> Constraints and assumptions
 -> Domain model and boundaries
 -> Data and consistency requirements
 -> Architecture alternatives
 -> Trade-off analysis
 -> Decision / ADR
 -> Security and threat model
 -> Reliability and failure analysis
 -> Deployment / operations model
 -> Cost and team cognitive load
 -> Migration / rollout
 -> Measurement and evolution
```

## Learning path

1. Architecture thinking and decision process
2. Quality attributes and measurable scenarios
3. Architecture fitness functions and evolutionary architecture
4. Domain-Driven Design and boundaries
5. Data-intensive and distributed systems fundamentals
6. Architecture styles and selection
7. Integration and messaging patterns
8. Reliability and failure patterns
9. Security architecture
10. Data/API/event contracts
11. Migration and modernization
12. Architecture documentation and ADRs
13. System design case studies
14. Principal Architect reviews

## Architecture styles to master

- Layered Architecture
- Modular Monolith
- Service-Based Architecture
- Microservices
- Event-Driven Architecture
- Service-Oriented Architecture
- Microkernel / Plugin Architecture
- Space-Based Architecture
- Serverless
- CQRS
- Event Sourcing

The goal is not to prefer one style. The goal is to understand the forces that make each style appropriate or inappropriate.

## Definition of mastery

Given a problem, you should be able to:

- distinguish functional requirements from quality attributes;
- identify missing information and dangerous assumptions;
- model important domain boundaries;
- estimate scale sufficiently to influence design;
- propose at least two credible architecture alternatives;
- explain why one alternative is preferred;
- describe consistency and transaction semantics;
- identify failure modes and blast radius;
- define security trust boundaries;
- explain deployment and operational implications;
- estimate relative complexity and cost;
- define migration/rollback strategy;
- record significant decisions in ADRs;
- explain what evidence would cause the architecture to evolve.

## Principal Architect rule

Never defend an architecture because it is modern. Defend it because its trade-offs fit the current business, domain, scale, risk, team and operational constraints.