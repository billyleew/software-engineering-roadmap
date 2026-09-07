# System Design Review Scorecard

Use this scorecard after each case study. Score each dimension from 0 to 3.

```text
0 = missing / misunderstood
1 = present but weak or superficial
2 = solid and defensible
3 = strong, explicit and trade-off aware
```

## 1. Problem framing

Did the design clearly identify:
- the user/business problem;
- critical journeys;
- scope and exclusions;
- assumptions and unknowns?

## 2. Architecture drivers

Were quality attributes ranked and made measurable rather than described vaguely?

Examples: correctness, availability, p99 latency, consistency, security, recoverability, cost.

## 3. Capacity reasoning

Were estimates sufficient to influence architecture without false precision?

Look for:
- average vs peak load;
- read/write ratio;
- data growth;
- retention;
- concurrency;
- bandwidth/storage implications.

## 4. Domain model and boundaries

Did the design identify:
- business invariants;
- bounded contexts/capabilities;
- transaction boundaries;
- ownership;
- differences between logical and deployment boundaries?

## 5. Data architecture

Was storage selected from access patterns and consistency needs rather than trend?

Did the design explain:
- source of truth;
- indexes;
- transactions;
- replication/partitioning only if justified;
- schema evolution;
- retention/recovery?

## 6. Integration semantics

Are APIs, commands, events and messages clearly distinguished?

Did the design address:
- timeouts;
- idempotency;
- retries;
- ordering;
- duplicate delivery;
- version compatibility?

## 7. Architecture alternatives

Were at least two credible alternatives considered?

A strong answer explains why a simpler option was rejected instead of creating a weak straw-man alternative.

## 8. Trade-off quality

Does the selected architecture explicitly state what becomes easier and harder?

Look for trade-offs in:
- reliability;
- consistency;
- deployment;
- cost;
- operations;
- team cognitive load;
- vendor lock-in;
- migration.

## 9. Failure analysis

Did the design reason about:
- slow dependency;
- unavailable dependency;
- lost response after successful operation;
- duplicate request;
- out-of-order message;
- partial workflow completion;
- overload/backpressure;
- data corruption?

## 10. Resilience pattern discipline

Were timeouts, retries, circuit breakers, bulkheads, queues, caching and similar patterns introduced only when a concrete failure dynamic justified them?

Deduct for pattern stacking without evidence.

## 11. Security

Did the design identify:
- assets;
- trust boundaries;
- authentication;
- authorization;
- least privilege;
- sensitive data;
- secrets;
- abuse/fraud;
- auditability;
- dependency/supply-chain risk?

## 12. Observability

Can the architecture answer:
- is the user journey healthy?
- where is latency introduced?
- which dependency failed?
- which deployment changed behavior?
- what is the actual bottleneck?

Look for RED/business metrics, structured logs, correlation, traces where justified, saturation and SLOs.

## 13. Delivery and recovery

Did the solution cover:
- CI/CD implications;
- schema migration;
- rollout;
- rollback;
- backups;
- restore testing;
- RTO/RPO;
- ownership/on-call?

## 14. Cost and organizational fit

Was the architecture reasonable for the actual team and business?

A technically capable system can still be a poor design if it requires a platform team the company does not have.

## 15. Evolution

Did the design define evidence that would cause it to change?

Examples:
- database saturation after query/index optimization;
- deployment contention;
- queue age;
- regional latency;
- team ownership changes;
- cost per transaction.

# Interpretation

Maximum score: **45**.

```text
0-18   Foundation needs work
19-27  Good implementation-level reasoning
28-35  Strong senior architecture reasoning
36-41  Staff/Principal-level design discussion
42-45  Exceptional — validate that complexity is genuinely justified
```

The score is a coaching device, not an objective measure of seniority. A simple architecture with excellent reasoning can score higher than a complex architecture.