# Engineering Books — Study Map

## Purpose

Books are treated as knowledge sources feeding the handbook, not as independent silos. The goal is to extract durable mental models, challenge them against modern practice, and apply them in exercises and real systems.

This repository contains **original study notes and practical synthesis**, not replacement reproductions of copyrighted books. When chapter-specific personal notes or excerpts are available, they can be expanded into deeper chapter-aligned exercises.

## Reading sequence

### 1. The Pragmatic Programmer — Andrew Hunt & David Thomas
Primary contribution: engineering mindset, feedback, responsibility, automation, adaptability and professional practice.

Apply to:
- Software development
- Debugging
- Automation
- Technical decision making

Practice: maintain an engineering journal recording one assumption, one experiment, one lesson and one automation opportunity from each meaningful task.

### 2. Refactoring — Martin Fowler
Primary contribution: disciplined improvement of existing design while preserving behavior.

Apply to:
- Refactoring
- Code smells
- Safe evolutionary design
- Testing as change safety

Practice: take one working module, establish tests, perform one refactoring at a time, and commit each behavior-preserving step independently.

### 3. Working Effectively with Legacy Code — Michael Feathers
Primary contribution: changing difficult systems safely through characterization, seams and dependency control.

Apply to:
- Legacy modernization
- Testability
- Incremental architecture evolution

Practice: select an untested module, capture current behavior, introduce one seam and implement a new requirement without rewriting the subsystem.

### 4. Why Programs Fail — Andreas Zeller
Primary contribution: scientific debugging and systematic isolation of causes.

Apply to:
- Debugging
- Incident investigation
- Experiment design
- Root-cause analysis

Practice: deliberately inject a defect, write competing hypotheses before editing code, and use experiments to eliminate hypotheses.

### 5. Domain-Driven Design — Eric Evans
Primary contribution: managing domain complexity through language, models and boundaries.

Apply to:
- Domain modeling
- Bounded contexts
- Aggregates and invariants
- Architecture boundaries

Practice: model a non-trivial business domain with domain experts/users in plain language before choosing persistence or service boundaries.

### 6. Designing Data-Intensive Applications — Martin Kleppmann
Primary contribution: reasoning about data systems, distributed systems and trade-offs.

Apply to:
- Storage
- Replication
- Partitioning
- Transactions
- Consistency
- Streams
- Distributed failure

Practice: design the same system under three different consistency/availability requirements and document why the architecture changes.

### 7. The Mythical Man-Month — Frederick P. Brooks Jr.
Primary contribution: limits of coordination, communication and simplistic scheduling assumptions in software projects.

Apply to:
- Technical leadership
- Team design
- Delivery planning
- CTO thinking

Practice: analyze a delayed project and separate implementation effort from communication, coordination, dependency and integration costs.

### 8. Clean Code — Robert C. Martin
Primary contribution: influential heuristics for readable and maintainable code.

Read critically. Treat recommendations as hypotheses to evaluate against language, team, domain and empirical outcomes rather than universal rules.

Apply to:
- Naming
- Functions
- Error handling
- readability
- code review

Practice: compare two implementations with a team. Measure comprehension and change effort rather than counting compliance with style rules.

## Additional architecture/platform sources

The eight books do not fully cover modern architecture, platform engineering, SRE, security or AI engineering. Supplement the roadmap with topics from:
- Fundamentals of Software Architecture
- Software Architecture: The Hard Parts
- Release It!
- Building Microservices
- Site Reliability Engineering
- Building Secure & Reliable Systems
- Accelerate
- Patterns of Enterprise Application Architecture

## Study method for every chapter/topic

When reading, create notes using:

```text
Chapter/topic:
Problem being discussed:
Key mental model:
Important concepts:
Assumptions/context:
What still applies today:
What should be challenged/updated:
Example from my work or a realistic system:
Exercise:
How I would use this in code/architecture/platform work:
How this changes a Principal Engineer decision:
Questions remaining:
```

Do not optimize for finishing books. Optimize for transferring ideas into engineering judgment.