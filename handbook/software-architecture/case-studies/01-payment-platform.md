# Case Study 01 — Payment Platform

## What this case teaches

Correctness under ambiguity is the main problem. A timeout does not tell you whether money moved.

Core topics:
- idempotency;
- transaction boundaries;
- provider integration;
- asynchronous callbacks;
- reconciliation;
- auditability;
- partial failure;
- retries and timeouts;
- observability tied to business outcomes.

## Pass 1 — Small product

Assume:
- 5 engineers;
- 20k customers;
- peak 30 RPS;
- card + PIX;
- one region;
- one external card provider;
- strong audit needs;
- six-month launch target.

### Functional requirements
- create payment;
- query payment;
- receive provider webhook;
- refund;
- reconcile provider state;
- expose merchant-facing status.

### Quality attributes
Ranked:
1. correctness;
2. auditability;
3. security;
4. availability;
5. recoverability;
6. latency;
7. cost.

### Initial architecture

A reasonable first option:

```text
Merchant
   |
   v
Payment API
   |
   +--> PostgreSQL
   |
   +--> Provider Adapter --> Card Provider
   |
   +--> Outbox --> Worker --> async tasks
```

One modular application can be enough initially.

Why not microservices yet?
- tiny team;
- low scale;
- local transactions are valuable;
- deployment independence has little demonstrated value.

### Data model

```text
Payment
- payment_id
- merchant_id
- idempotency_key
- amount
- currency
- method
- state
- provider_reference
- version
- created_at
- updated_at

PaymentAttempt
- attempt_id
- payment_id
- provider
- request_fingerprint
- outcome
- provider_reference
- created_at

OutboxEvent
- event_id
- type
- aggregate_id
- payload
- published_at
```

Protect uniqueness of `(merchant_id, idempotency_key)` at the database level.

### Payment state model

Example:

```text
CREATED
 -> PROCESSING
 -> AUTHORIZED
 -> FAILED
 -> UNKNOWN
 -> REFUNDED
```

`UNKNOWN` is important. Sometimes the correct answer is "we do not yet know" rather than inventing success/failure.

## Critical scenario — response lost after charge

```text
Merchant -> Payment API: create payment
Payment API -> Provider: authorize
Provider -> Payment API: SUCCESS   X response lost
Payment API -> Merchant: timeout
Merchant -> Payment API: retry same idempotency key
```

Correct behavior:
- do not create a second logical payment;
- return stored/in-progress state where possible;
- reconcile with provider when outcome is uncertain.

## Webhooks

Provider callbacks are untrusted network input.

Design for:
- signature/authentication verification;
- duplicate callbacks;
- out-of-order callbacks;
- unknown references;
- replay;
- delayed delivery;
- processing idempotency.

Persist enough evidence before acknowledging where appropriate.

## Reconciliation

Reconciliation is not a fallback hack. For payment systems it is an architectural capability.

Compare:

```text
internal payment state
vs
provider settlement/transaction state
```

Detect mismatches and provide controlled repair/escalation workflows.

## Observability baseline

Technical:
- payment-create rate;
- p50/p95/p99 latency;
- 4xx/5xx;
- provider latency/errors/timeouts;
- DB pool/query latency;
- webhook processing lag;
- outbox backlog;
- reconciliation failures.

Business:
- payments attempted;
- authorization success rate;
- unknown-state count/age;
- duplicate prevention count;
- refund success rate;
- reconciliation mismatch rate;
- value of payments affected.

## SLI/SLO examples

Do not define one SLO for the whole application if business semantics differ.

Possible indicators:
- accepted payment requests processed without duplicate financial effect;
- status-query availability;
- webhook processing freshness;
- reconciliation completion time.

## Security review

Ask:
- Can raw card data be avoided/tokenized?
- Which services/users can initiate refunds?
- Are authorization decisions auditable?
- Are webhook signatures validated?
- Are secrets rotated?
- Are logs free of sensitive payment data?
- Can one merchant access another merchant's payment?

## Pass 2 — Growth pressure

New evidence:
- 500 RPS peak;
- provider callbacks spike asynchronously;
- reconciliation jobs interfere with online payment latency.

Do not decompose everything.

Possible evolution:
- isolate reconciliation/background worker resource pools;
- separate callback processing queue;
- introduce read model/replica if status-query load proves substantial;
- extract provider integration only if scaling/ownership/release pressure justifies it.

## Pass 3 — Multi-provider / multi-region

New requirements:
- multiple providers;
- regional payment methods;
- merchant routing policies;
- regional data/regulatory constraints;
- 99.99% availability for status and payment intake.

Now stronger service boundaries may become useful:

```text
Payment Orchestration
Provider Adapters
Ledger / Financial Records
Reconciliation
Merchant Configuration / Routing
```

But each boundary needs explicit consistency and ownership semantics.

## ADR exercises

Write ADRs for:
1. Why relational storage is the first system of record.
2. Why payment creation requires idempotency keys.
3. Why outbox is used for state-change/event publication.
4. When reconciliation becomes a separately scaled workload.
5. When provider integration deserves its own deployment.

## Failure drill

Inject:
- provider timeout after successful charge;
- duplicate webhook;
- DB unavailable after provider success;
- outbox publisher stopped for 20 minutes;
- stale provider credentials;
- reconciliation mismatch.

For each answer:
- what does the merchant see?
- can money duplicate/disappear?
- what telemetry fires?
- how does recovery happen?
- is human intervention required?

## What not to add without evidence

Do not automatically add:
- Kafka;
- Redis;
- event sourcing;
- 15 microservices;
- multi-region writes;
- service mesh.

Each may eventually be useful. None is a prerequisite for a correct payment platform.