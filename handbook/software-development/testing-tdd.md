# Testing & TDD

## Objective

Testing exists to create confidence that valuable behavior works and remains safe to change. Coverage is evidence about execution, not proof of correctness.

## Test levels

### Unit tests
Fast tests for focused behavior with minimal external dependencies.

### Component/service tests
Exercise a meaningful application slice while controlling external systems.

### Integration tests
Verify real boundaries such as databases, brokers, filesystems and vendor adapters.

### Contract tests
Verify assumptions between independently evolving consumers/providers.

### End-to-end tests
Validate a small set of critical journeys through the deployed system. Keep them focused because they are slower and more failure-prone.

### Non-functional tests
Performance, load, resilience, recovery and security tests validate quality attributes that functional tests cannot prove.

## What to test

Prioritize:
1. Business invariants
2. High-risk behavior
3. Boundaries and integrations
4. Failure/retry behavior
5. Security-sensitive behavior
6. Previously observed defects
7. Critical customer journeys

## Avoid testing implementation details

A test that breaks every time internal structure changes discourages refactoring.

Prefer:

```text
Given customer is premium
When order total is 100
Then eligible discount is applied
```

rather than asserting which private methods were invoked.

## TDD

```text
RED -> GREEN -> REFACTOR
```

**Red:** express a small missing behavior.

**Green:** implement the simplest correct solution.

**Refactor:** improve design with the safety of passing tests.

TDD is especially useful for domain logic and design discovery. It is not mandatory for every configuration file, prototype or trivial integration.

## Test doubles

Use stubs/fakes/mocks where they improve control over a boundary. Excessive mocking often signals that implementation structure rather than behavior is being tested.

## Example — transfer money

Important invariants:
- amount must be positive
- source must have sufficient funds
- debit and credit must not become partially committed
- duplicate requests must not transfer twice
- authorization must be enforced

Tests should include success, insufficient balance, duplicate request, storage failure, concurrent requests and authorization failure.

## Production confidence

Testing continues after deployment through:
- health checks
- synthetic tests
- metrics
- tracing
- canary analysis
- SLO monitoring
- rollback capability

A test suite is one part of a feedback system, not the entire quality strategy.

## Exercise

Implement a money-transfer use case using TDD. Start with pure domain rules. Add persistence. Then introduce a simulated timeout after the debit step and redesign the workflow so partial failure cannot silently corrupt the transfer.