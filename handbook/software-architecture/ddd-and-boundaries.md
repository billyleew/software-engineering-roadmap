# Domain-Driven Design & Architecture Boundaries

DDD is most valuable when business complexity is the difficult part of the system. It is not a requirement for every CRUD application.

## Strategic design first

Before entities and repositories, understand the business landscape.

### Ubiquitous Language

Develop shared language between engineers and domain experts. Code, conversations and documentation should reflect important domain concepts consistently.

If "customer", "account" or "order" means different things to different parts of the business, that is evidence of context boundaries rather than merely a naming problem.

### Subdomains

Classify capabilities:
- **Core:** creates meaningful competitive differentiation;
- **Supporting:** necessary but not differentiating;
- **Generic:** common capability that may often be bought/outsourced.

This influences build-vs-buy and where the strongest engineering investment belongs.

### Bounded Context

A boundary inside which a domain model and language are internally consistent.

A bounded context is a **model boundary**, not automatically:
- a repository;
- a team;
- a database;
- a microservice.

Those physical/organizational boundaries may align later when useful.

### Context Mapping

Understand relationships between contexts and which direction dependencies flow. Integration contracts deserve explicit ownership.

## Tactical design

### Entity
Has identity that remains meaningful through state changes.

### Value Object
Defined by its value rather than identity; often immutable. Examples: Money(amount, currency), Address, DateRange.

### Aggregate
A consistency boundary protecting business invariants. External modifications go through the aggregate root.

Do not create huge aggregates simply to mirror object graphs. Large aggregates increase contention and transaction scope.

### Domain Service
Domain behavior that does not naturally belong to one entity/value object. Avoid using "service" as a dumping ground for all logic.

### Domain Event
A meaningful business fact that has occurred, such as `PaymentAuthorized` or `OrderConfirmed`.

Name events in past tense. Distinguish facts from commands (`AuthorizePayment`).

## Invariants

Architecture should protect rules that must always be true.

Example transfer invariants:
- transfer amount > 0;
- source and destination are valid;
- currency rules are satisfied;
- committed money cannot disappear between debit and credit.

Identifying invariants helps determine transaction and aggregate boundaries.

## Boundary discovery questions

- Which terms have different meanings in different workflows?
- Which rules must change together?
- Which data must be strongly consistent together?
- Which capabilities have independent lifecycle/ownership?
- Which integrations are volatile?
- Which parts are core differentiation?
- Where does organizational ownership already exist?

## DDD and microservices

DDD can help discover sensible service boundaries, but:

```text
bounded context != microservice
```

Start with logical boundaries. Introduce network/process boundaries when deployment, scaling, reliability, security or ownership requirements justify them.

## Anti-Corruption Layer

When integrating with a legacy/external model that does not fit your domain, translate at the boundary instead of allowing external concepts to contaminate the internal model.

## Example — commerce

Potential contexts:

```text
Catalog
Pricing
Ordering
Payments
Inventory
Shipping
Customer Support
```

"Product" may mean sellable catalog information in Catalog but a stock-keeping unit in Inventory. Trying to force one universal Product model can increase coupling.

## Exercise — banking

Model a digital bank without drawing infrastructure first.

Identify contexts such as Customer Identity, Accounts, Transfers, Cards, Payments, Notifications and Compliance. For each:
1. define purpose;
2. define key language;
3. identify invariants;
4. identify owned data;
5. identify events/commands exchanged;
6. identify consistency requirements;
7. decide whether the boundary is logical only or deserves an independent deployment;
8. justify the decision.

The architecture diagram comes **after** this reasoning.