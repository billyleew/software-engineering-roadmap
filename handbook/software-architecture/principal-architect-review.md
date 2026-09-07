# Principal Architect Review

Use this as a design-review framework. It is intentionally uncomfortable: architecture review should expose assumptions before production exposes them more expensively.

## Problem

- What business/customer outcome are we solving?
- Which requirements are truly architectural?
- Which statements are assumptions rather than facts?
- What is explicitly out of scope?

## Scale

- Expected and peak traffic?
- Data growth and retention?
- Read/write ratio?
- Geographic distribution?
- Which dimension could grow unexpectedly?

## Domain

- What are the business invariants?
- Where are bounded contexts?
- Who owns each capability/data set?
- Are service boundaries based on domain/operational needs or nouns in a diagram?

## Architecture

- What alternatives were considered?
- Why was this option selected?
- What simpler architecture was rejected, and why?
- Which decisions are difficult to reverse?
- Where are the highest coupling points?

## Data

- System of record for each important datum?
- Transaction boundaries?
- Consistency requirements?
- Replication/partitioning strategy if needed?
- Schema evolution?
- Retention/deletion/privacy?
- Backup and restore?

## APIs and events

- Contract ownership?
- Version/compatibility strategy?
- Idempotency?
- Timeouts?
- Retry policy?
- Pagination/rate limiting?
- Event schema evolution?
- Duplicate/out-of-order handling?

## Failure

- What if each dependency is slow?
- What if it is unavailable?
- What if response is lost after success?
- What if only half a workflow succeeds?
- Blast radius?
- Backpressure/load shedding?
- Recovery behavior?

## Security

- Assets and trust boundaries?
- Authentication vs authorization?
- Least privilege?
- Secrets?
- Encryption?
- Auditability?
- Abuse/fraud scenarios?
- Dependency/supply-chain risk?
- Tenant isolation?

## Reliability / SRE

- Critical SLIs?
- SLOs?
- Alert conditions?
- Capacity limits?
- Degradation strategy?
- RTO/RPO?
- Runbooks?
- How is the system debugged at 03:00?

## Delivery

- CI/CD path?
- Migration strategy?
- Backward compatibility?
- Canary/blue-green/feature flags?
- Rollback?
- Database migration rollback/forward-fix strategy?

## Cost and organization

- Infrastructure cost at expected and 10x usage?
- Licensing?
- Operational burden?
- Team skills?
- On-call implications?
- Cognitive load?
- Build vs buy?
- Vendor lock-in/exit cost?

## Evolution

- Which changes are expected?
- Which architecture assumptions should be monitored?
- What fitness functions can detect erosion?
- What evidence triggers service extraction, repartitioning, different storage, or other structural evolution?

# Architecture review output

A strong review should produce:

```text
1. Problem statement
2. Requirements and quality attributes
3. Assumptions / open questions
4. Domain boundaries
5. Architecture alternatives
6. Recommended architecture
7. Trade-offs
8. Data / consistency model
9. APIs / events
10. Failure model
11. Security model
12. Reliability / SLOs
13. Deployment / migration
14. Cost / organizational impact
15. ADRs
16. Risks
17. Evidence that will trigger evolution
```

# Capstone — design a payment platform

Design a payment platform supporting card and PIX with:
- merchant API;
- idempotent payment creation;
- asynchronous provider callbacks;
- refunds;
- reconciliation;
- immutable audit needs;
- sensitive customer/payment data;
- provider outage handling;
- peak traffic 10x normal;
- an initially small engineering team.

Deliver:
1. requirements and assumptions;
2. quality-attribute scenarios;
3. domain/context map;
4. scale estimates;
5. at least three architecture alternatives;
6. architecture decision and ADRs;
7. API and event contracts;
8. data ownership/consistency strategy;
9. sequence diagrams for success, timeout and duplicate requests;
10. threat model;
11. failure-mode analysis;
12. observability and SLO design;
13. CI/CD and rollout approach;
14. RTO/RPO and recovery approach;
15. cost/complexity analysis;
16. evolution plan for 10x and 100x growth.

Do not receive credit merely for producing a diagram. Every important box and arrow must have a reason.