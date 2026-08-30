# Software Development

## Objective

Develop the ability to create software that is correct, understandable, testable, maintainable, and safe to evolve.

This track deliberately separates **principles**, **practices**, **patterns**, and **book-derived learning**. A book is a source of ideas; it is not the architecture of this handbook.

## Learning path

1. Engineering principles and code quality
2. Cohesion, coupling and boundaries
3. SOLID, KISS, YAGNI and DRY
4. Refactoring
5. Legacy code
6. Systematic debugging
7. Testing and TDD
8. Design patterns
9. Application architecture: Layered, MVC, Clean and Hexagonal
10. API and integration design
11. Code review and engineering standards
12. Capstone refactoring exercise

## Definition of mastery

For any codebase, be able to answer:

- What behavior must be preserved?
- Where are the important business rules?
- Which dependencies are stable or volatile?
- Where is coupling preventing change?
- What should be tested before changing it?
- Is a pattern solving a demonstrated problem or merely adding ceremony?
- What is the smallest safe improvement?
- How would this design behave under failure?
- Can another engineer understand the intent without reverse-engineering accidental complexity?

## Practice loop

```text
Understand behavior
 -> identify pain/change pressure
 -> characterize with tests
 -> make the smallest design improvement
 -> implement change
 -> verify behavior
 -> review complexity
 -> document important decisions
```

## Core principle

Good design is not the maximum number of abstractions. Good design makes important behavior clear and expected change inexpensive.