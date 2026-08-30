# Engineering Principles

Principles are decision heuristics, not laws. Applying a principle mechanically can create the exact complexity it was intended to prevent.

## KISS — Keep It Simple

### Problem it addresses
Unnecessary complexity makes software harder to understand, test, operate and change.

### Practice
Prefer the smallest design that satisfies today's known requirements while leaving reasonable seams for likely change.

### Example
If one application with one team and moderate traffic can be cleanly divided into modules, begin with a modular monolith rather than creating five network services merely because the domains are distinct.

### Failure mode
"Simple" must not mean ignoring known requirements. Removing authentication from a payment system is simpler but incorrect.

## YAGNI — You Aren't Gonna Need It

Do not pay today's complexity cost for speculative future requirements.

Before implementing extensibility, ask:
- Which concrete requirement needs it?
- What evidence suggests this variation will occur?
- What would adding it later cost?
- Is the decision reversible?

### Exercise
Design a notification feature that currently supports email. First design it only for email. Then introduce a confirmed requirement for SMS and observe which abstractions become justified by real change pressure.

## DRY — Don't Repeat Yourself

DRY is primarily about duplicated **knowledge**, not visually similar lines of code.

Two pieces of code that happen to look identical but represent different business concepts may need to evolve independently. Combining them can create harmful coupling.

### Example
Two tax calculations that currently use `amount * 0.1` should not automatically share a function if they represent unrelated jurisdictions with independent rules.

## Separation of Concerns

Keep responsibilities that change for different reasons separate.

Examples:
- Domain rules should not depend directly on HTTP controllers.
- Business decisions should not be mixed with database serialization.
- Deployment configuration should not contain application business logic.

## High Cohesion

Things that participate in the same responsibility should live close together.

Low cohesion often appears as modules named `utils`, `common`, or `helpers` that accumulate unrelated behavior.

## Low Coupling

A component should know as little as practical about implementation details of other components.

Coupling is not inherently bad; a system with zero coupling does nothing. The objective is to control coupling at boundaries where independent change matters.

## SOLID

### Single Responsibility Principle
A module should have one primary reason to change. Think in terms of change responsibility rather than "one function per class".

### Open/Closed Principle
Prefer designs where expected variation can be introduced without repeatedly rewriting stable behavior. Do not create extension points before variation is demonstrated.

### Liskov Substitution Principle
A replacement implementation must preserve the behavioral expectations of the abstraction it implements.

### Interface Segregation Principle
Consumers should depend only on capabilities they actually need. Large interfaces create unnecessary coupling.

### Dependency Inversion Principle
High-value policy should not be controlled by low-level implementation details. Place abstractions at meaningful boundaries.

## Composition over inheritance

Prefer composing behavior when inheritance would couple unrelated lifecycle or variation concerns. Inheritance remains useful when there is a genuine substitutable relationship and stable hierarchy.

## Principle conflicts

Engineering decisions frequently involve principles pulling in different directions:

```text
DRY                     vs independent evolution
Abstraction             vs simplicity
Extensibility           vs YAGNI
Reuse                   vs coupling
Performance             vs readability
Consistency             vs team autonomy
```

The senior/principal skill is not memorizing the principles. It is explaining which trade-off matters in the current context.

## Practical review checklist

When reviewing a design, ask:
1. What requirement created this abstraction?
2. What change becomes easier because of it?
3. What complexity does it introduce?
4. Is business knowledge duplicated?
5. Are unrelated concepts coupled because their implementations currently look similar?
6. Is infrastructure leaking into domain logic?
7. Can the important business behavior be understood quickly?
8. Could a simpler design satisfy the same requirements?

## Exercise — evolve instead of predict

Build a small order-pricing module in three iterations:

**Iteration 1:** one product price and percentage discount.

**Iteration 2:** introduce coupons and customer-specific discounts. Refactor only after the new variation is understood.

**Iteration 3:** add an external tax provider. Introduce a boundary so the domain does not depend directly on the vendor SDK.

For every refactoring, write down which real change pressure justified it.