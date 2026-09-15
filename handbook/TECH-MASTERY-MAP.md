# Tech Mastery Knowledge System

## Mission

Turn this repository into a coherent engineering knowledge system rather than a collection of technologies, links, interview answers or fashionable architecture patterns.

The goal is to develop judgment from implementation through Principal Engineer and AI-first CTO decisions.

```text
Computer Science Foundations
        ↓
Software Development
        ↓
Low-Level Design
        ↓
Domain & Data Modeling
        ↓
Software Architecture
        ↓
Distributed Systems & System Design
        ↓
Platform Engineering / DevOps / SRE
        ↓
Security & FinOps
        ↓
AI Engineering & AI Architecture
        ↓
Principal Engineer / CTO
```

These areas eventually become parallel rather than strictly sequential.

## Universal learning loop

Every important topic should eventually support this loop:

```text
Understand
 -> Model
 -> Compare alternatives
 -> Build
 -> Test
 -> Break
 -> Observe
 -> Measure
 -> Scale only when justified
 -> Defend the decision
 -> Record the decision
 -> Revisit with evidence
```

## Universal concept template

For concepts, patterns and technologies ask:

1. What problem does it solve?
2. What is the mental model?
3. What requirement or architecture force makes it relevant?
4. When should it be used?
5. When should it NOT be used?
6. What are simpler alternatives?
7. What trade-offs does it introduce?
8. What failure modes does it create or address?
9. What are the consistency/concurrency implications?
10. What are the security implications?
11. How is it tested?
12. How is it observed?
13. How is it operated and recovered?
14. What does it cost technically and organizationally?
15. What evidence would justify adopting or removing it?
16. What practical exercise proves understanding?

## Repository evolution

The repository may progressively include:

```text
handbook/
  software-development/
  software-architecture/
  platform-engineering/
  sre/
  security/
  ai-engineering/
  principal-engineer-cto/

fundamentals/
  networking/
  operating-systems/
  databases/
  concurrency/
  storage/
  protocols/
  distributed-systems/

system-design/
  concepts/
  case-studies/
  practice-program/
  failure-analysis/
  architecture-defense/

low-level-design/
  modeling/
  oop/
  patterns/
  exercises/

labs/
  build-your-own/
  failure-injection/
  observability/
  distributed-systems/

papers/
  reading-paths/
  notes/

references/
  source-map.md
  engineering-blogs.md
```

This is a target information architecture, not a command to create empty folders. Create sections when substantive learning material exists.

## Four depths of mastery

### Depth 1 — Explain

Can explain the concept and vocabulary without memorized buzzwords.

### Depth 2 — Decide

Can compare alternatives and identify when the concept should not be used.

### Depth 3 — Implement and operate

Can build a simplified implementation, test it, observe it, debug it and understand its failure modes.

### Depth 4 — Evolve and lead

Can decide whether the organization should adopt it, estimate cost/risk, define standards, guide teams and revisit the decision from production evidence.

## Evidence-first architecture rule

```text
Trend != requirement
Capability != need
Possible scale != current bottleneck
More components != more mature architecture
```

Prefer:

```text
Problem
 -> requirement
 -> evidence / credible constraint
 -> alternatives
 -> simplest adequate design
 -> instrumentation
 -> measurement
 -> evolution
```

## Source strategy

External repositories, books, papers, engineering blogs and documentation are inputs—not the handbook itself.

For each useful external source:
- identify durable concepts;
- verify claims when necessary;
- synthesize in our own words;
- preserve attribution/reference links;
- challenge advice against current context;
- connect it to exercises and decisions;
- avoid copying copyrighted material wholesale.

## Definition of success

The repository succeeds when it helps answer questions such as:

- Why this architecture rather than a simpler one?
- Why SQL rather than NoSQL—or vice versa?
- Why a queue rather than synchronous communication?
- Why Redis here, and why not elsewhere?
- What evidence justifies Kafka?
- What happens if the operation succeeds but the response is lost?
- What data proves the system needs to scale?
- How will we observe the change?
- How will we recover when it fails?
- What does the decision cost the organization?
- What would make us reverse the decision?

The objective is not to know every technology. The objective is to build the reasoning system needed to learn and choose technologies correctly.