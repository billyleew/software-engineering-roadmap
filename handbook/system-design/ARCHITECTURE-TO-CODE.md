# Architecture-to-Code PoC Framework

**Purpose:** connect system-design research to maintainable code, explicit architecture decisions, automated tests, operational evidence and refactoring. This is a learning framework, **not** a mandate to use every pattern.

## Six independent decision axes

| Axis | Candidate approaches | Selection question |
|---|---|---|
| System topology | single process, modular monolith, services, event-driven, plugin-based | What deployment and communication boundaries are justified? |
| Application structure | simple layered/MVC, ports-and-adapters/Hexagonal, Clean, vertical slices | What dependency and change boundaries matter? |
| Domain modeling | transaction script, domain model, DDD aggregates, bounded contexts | How complex are invariants and business rules? |
| Code patterns | Strategy, Adapter, Factory, Repository, Observer, Decorator | What demonstrated variation or coupling do they solve? |
| Reliability/integration | idempotency, transactional outbox, retries, DLQ, circuit breaker, saga, CQRS | Which actual failure modes demand them? |
| Delivery/operations | source control, CI, test pyramid, containers, tracing, feature flags, IaC | How will we reproduce, ship, observe and operate the PoC? |

**Clarification:** MVC and Hexagonal can coexist (MVC at the HTTP/UI edge; ports and adapters around the domain). EDA can exist inside a monolith or between services. Git/source control is an engineering practice, not a system topology. A plugin architecture is an extensibility model and can be combined with other approaches.

## Default implementation policy

1. **Start minimal**: a single deployable with simple modules and straightforward dependencies, unless requirements demand otherwise.
2. **Identify change axes**: external providers, storage engines, domain rules, interfaces and scaling boundaries.
3. **Choose structure with evidence**: prefer simple layers for CRUD; use Hexagonal/ports-and-adapters where isolating infrastructure is valuable; use DDD for complex domain invariants; use plugins when independent extensions are a real requirement.
4. **Add patterns only when a testable problem exists**: e.g. Adapter for swapping a provider, Strategy for independently varying algorithms, Outbox for atomic persistence plus event publication.
5. **Test at boundaries**: domain unit tests, adapters with integration tests, API contracts, end-to-end workflows, failure injection and performance benchmarks.
6. **Refactor under pressure**: deliberately introduce a second implementation or workload; compare before/after complexity and behavior.
7. **Record an ADR** with alternatives, trade-offs, evidence, and a revisit trigger.

## Recommended PoC directory contract

```text
pocs/<case-slug>/
  README.md                 # goal, scope, assumptions, how to run
  docs/
    architecture.md         # system diagram and source-code boundaries
    adr-0001.md             # decisions and rejected alternatives
    threats.md              # trust boundaries and controls
    measurements.md         # workload, environment, results (no fabricated numbers)
  src/                      # language-specific app modules
  tests/                    # unit, integration, contract and failure tests
  scripts/                  # reproducible setup and load-test commands
```

The exact `src/` structure is language-dependent; do not enforce Java package conventions on Python/TypeScript or vice versa. A typical Hexagonal implementation separates **domain**, **application/use cases**, **ports**, and **adapters**. Dependency arrows point inward; the domain must not import HTTP/database frameworks.

## Example: GitHub webhook metrics ingestion

**Phase A — baseline:** one HTTP API, durable PostgreSQL inbox table with unique delivery ID, a worker, simple metrics projection. Unit-test deduplication and integration-test transaction boundaries. Measure ingest latency and throughput.

**Phase B — modular monolith:** split ingest, processing and reporting modules; define explicit interfaces. Use Hexagonal architecture only for boundaries that benefit from testing or substitution (e.g. GitHub webhook verification, storage and clock).

**Phase C — reliable async:** introduce transactional outbox and bounded retries when delivery to an external broker becomes necessary; test crash windows, duplicates and poison messages.

**Phase D — topology decision:** compare PostgreSQL workers, SQS and Kafka based on measured volume, ordering, replay, retention, operations and cost. Do **not** assume virtual threads, Kubernetes or Kafka are required.

**Phase E — evolutionary exercise:** when a specific module requires independent deployment, extract it and measure deployment/operational costs. Keep the monolith if extraction provides no clear benefit.

## Architecture review checklist

- Are dependency rules enforced by tests or static analysis?
- Are APIs, domain invariants and transactions explicit?
- Can the most important business behavior run without infrastructure?
- Are exceptions, retries, idempotency and timeouts tested?
- Does every nontrivial pattern have a stated reason?
- Are load-test data and measurements reproducible?
- Is the next scaling step tied to an observable threshold?
- Is the simplest credible alternative documented?

**Learning outcome:** be able to explain not only *how* the architecture works, but *why this implementation structure* fits the system's constraints and when it should change.
