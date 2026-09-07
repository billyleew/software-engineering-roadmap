# System Design Case Studies

## Purpose

These case studies are not attempts to reproduce the internal architecture of real companies. They are engineering exercises inspired by familiar product categories.

The objective is to practice the same decision process repeatedly under different forces:

```text
Problem
 -> Requirements
 -> Quality attributes
 -> Scale estimates
 -> Domain boundaries
 -> Data model
 -> Architecture alternatives
 -> Trade-offs
 -> Failure model
 -> Security
 -> Observability
 -> Operations
 -> Cost
 -> ADRs
 -> Evolution triggers
```

## Ground rule

Do not start with the famous-company answer.

Do not say:
- "YouTube uses X, therefore we need X";
- "Uber uses microservices, therefore dispatch requires microservices";
- "Twitter needs Kafka, therefore feeds need Kafka".

Each case begins at a modest scale. Add complexity only when new requirements or measured evidence justify it.

## Case sequence

1. **Payment platform** — correctness, idempotency, external providers, reconciliation, auditability.
2. **Video platform** — large objects, asynchronous processing, object storage, CDN, transcoding.
3. **Social feed** — fan-out, caching, ranking, hot users, eventual consistency.
4. **Messaging platform** — persistent connections, presence, ordering, offline delivery, multi-device synchronization.
5. **Ride dispatch** — geospatial data, real-time matching, rapidly changing state, regional partitioning.
6. **Edge/CDN platform** — caching, DNS/routing, global distribution, invalidation, origin protection.

## How to study each case

For every case, complete three passes:

### Pass 1 — Simple
Design for a small team and realistic early-stage traffic. Prefer managed components and a simple operational model.

### Pass 2 — Growth pressure
A new measurable bottleneck or business requirement is introduced. Evolve only the affected architecture.

### Pass 3 — Large scale / organizational scale
Add geographic, reliability, throughput, team-ownership or regulatory constraints and revisit prior decisions.

## Required deliverables

For each case produce:
- problem statement;
- assumptions and open questions;
- functional requirements;
- ranked quality attributes;
- rough capacity estimates;
- domain/context map;
- APIs/events;
- data ownership and consistency rules;
- at least two architecture alternatives;
- selected architecture and rejected alternatives;
- critical sequence diagrams;
- failure-mode analysis;
- threat/security considerations;
- observability baseline;
- SLI/SLO ideas;
- cost/operational implications;
- ADRs;
- evidence that would trigger the next architecture evolution.

## Principal Engineer habit

At every step ask:

> Which requirement or evidence justifies this component?

If the answer is only "best practice" or "this is what large companies use", the decision is incomplete.