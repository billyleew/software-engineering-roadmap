# Design Patterns — Problem First

Patterns are names for recurring design solutions. They are not objectives.

The wrong question is:
> Where can I use Strategy?

The better question is:
> This behavior varies independently and conditionals are spreading. Which design makes that variation explicit?

## Creational

### Factory
Use when creation logic is meaningful, variable, or should be separated from consumers.

Avoid factories that merely rename a constructor without reducing coupling or expressing intent.

### Builder
Useful for complex construction with many optional parameters or staged validation.

### Singleton
Global uniqueness is occasionally required, but global mutable state creates hidden coupling and testing problems. Prefer explicit lifecycle/dependency management where possible.

## Structural

### Adapter
Translate an external interface into an internal interface the application controls.

**Excellent boundary pattern:** wrap payment, email, storage or other vendor SDKs so vendor models do not spread through the domain.

### Facade
Expose a simpler interface over a complex subsystem.

### Decorator
Add behavior around an object without modifying its core responsibility. Useful for logging, metrics, caching or authorization when applied at the appropriate boundary.

### Proxy
Control access to another object, commonly for remote access, lazy loading or policy enforcement.

## Behavioral

### Strategy
Use when multiple algorithms/behaviors implement the same capability and vary independently.

Example: pricing strategy by customer/contract type.

### Observer
Use for one-to-many notification inside a process. For distributed systems, do not assume an in-memory Observer pattern provides durable event delivery semantics.

### Command
Represent an action/request as data or an object. Useful when actions need queuing, auditing, retrying or composition.

### State
Useful when behavior changes materially according to explicit lifecycle state and state transitions matter.

### Chain of Responsibility
Useful when a request passes through a configurable sequence of handlers, such as validation or policy checks.

## Enterprise/application patterns

### Repository
Provides a collection-like boundary around persistence when domain/application code benefits from not knowing storage details.

### Unit of Work
Coordinates persistence changes that must commit as one logical transaction.

### Dependency Injection
Makes dependencies explicit and allows implementations to be composed externally.

### Service Layer
Defines an application boundary/use cases. Avoid turning it into a collection of business logic that belongs in the domain.

## Distributed-system patterns

These solve different problems from GoF object patterns:
- Circuit Breaker — stop repeatedly calling an unhealthy dependency
- Retry with exponential backoff and jitter — recover from transient failures without creating retry storms
- Bulkhead — isolate resource exhaustion/failure
- Saga — coordinate a distributed business transaction through steps/compensations
- Transactional Outbox — reliably connect local state change with message publication
- Idempotency — make repeated execution safe

## Pattern selection template

Before adopting a pattern, write:

```text
Problem:
Change pressure:
Current failure/pain:
Candidate pattern:
Simpler alternative:
New complexity introduced:
How we will know the pattern helped:
```

## Exercise

Start with a checkout implementation containing direct conditionals for card, PIX and invoice payments.

Do not refactor immediately.

Add requirements one at a time:
1. Different authorization logic per method.
2. External providers.
3. Retry behavior for one provider.
4. Auditing.
5. A new payment method.

At each step decide whether Strategy, Adapter, Decorator, Factory or no pattern is justified. Record rejected patterns and why.