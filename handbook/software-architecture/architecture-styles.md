# Architecture Styles — Selection by Trade-off

Architecture styles provide structural constraints and recurring trade-offs. They can be combined, but combining styles also combines complexity.

# Layered Architecture

Typical structure:

```text
Presentation
 -> Application/Business
 -> Persistence
 -> Database
```

**Good fit:** straightforward business applications, teams needing familiar structure, relatively simple deployment.

**Strengths:** simple mental model, broad ecosystem support, low operational cost.

**Risks:** layers can become technical silos; business rules may leak everywhere; changes can cut across every layer.

# Modular Monolith

One deployable application with explicit internal module/domain boundaries.

**Good fit:** many new products, small/medium teams, domains needing clear boundaries without distributed operations.

**Strengths:** local transactions, simple deployment/debugging, low network complexity, easier refactoring.

**Risks:** boundaries can decay without enforcement; whole application usually deploys/scales together; poor modularity creates a "big ball of mud".

**Important:** a monolith is a deployment topology, not automatically bad architecture.

# Service-Based Architecture

A small number of coarse-grained services, often sharing some infrastructure/data patterns.

**Good fit:** when independent deployment/ownership is useful for major domains but full microservice granularity is unnecessary.

**Strengths:** compromise between monolith simplicity and service autonomy.

**Risks:** shared database coupling, ambiguous ownership, distributed failure without full isolation benefits.

# Microservices

Many independently deployable services aligned to business capabilities and ownership boundaries.

**Good fit when there is evidence for:** independent scaling, independent deployment, distinct reliability requirements, strong team ownership boundaries, heterogeneous lifecycle needs.

**Strengths:** deployment/scaling isolation, bounded ownership, fault isolation when designed correctly.

**Costs:** network failure, distributed transactions, observability, platform requirements, contract/version management, testing complexity, data ownership, incident complexity and cognitive load.

Do not use service count as a maturity metric.

# Event-Driven Architecture (EDA)

Components communicate through events representing facts that occurred.

**Good fit:** asynchronous workflows, decoupled reactions, integration, variable workloads, event history/replay where required.

**Strengths:** temporal decoupling, extensibility of consumers, buffering.

**Risks:** eventual consistency, duplicates, ordering, schema evolution, difficult debugging, hidden workflows and operational broker complexity.

An event is not simply an asynchronous RPC command with a different name.

# Service-Oriented Architecture (SOA)

Enterprise services integrate capabilities across heterogeneous systems, historically often using centralized integration/governance patterns.

**Good fit:** enterprise integration where reusable business services and heterogeneous legacy systems dominate.

**Strengths:** interoperability and reuse across large organizations.

**Risks:** centralized governance/integration layers can become bottlenecks; shared canonical models can increase coupling.

# Microkernel / Plugin Architecture

A stable core provides essential capabilities while plugins add variable features.

**Good fit:** IDEs, developer tools, workflow engines, product platforms with customer-specific extensions.

**Strengths:** extensibility and separation between stable core and optional capabilities.

**Risks:** plugin compatibility, lifecycle/version management, extension security and API stability.

# Space-Based Architecture

Distributes state/processing across nodes to reduce central database bottlenecks, often using in-memory data grids and partitioned processing.

**Good fit:** extreme throughput and elasticity where centralized persistence becomes the limiting factor.

**Strengths:** high scalability and reduced contention.

**Risks:** complex consistency, data synchronization, recovery, operational expertise and cost. Usually unjustified for ordinary workloads.

# Serverless

Functions/managed services where infrastructure lifecycle and scaling are substantially delegated to the provider.

**Good fit:** event processing, variable workloads, APIs with appropriate execution characteristics, small teams benefiting from managed operations.

**Strengths:** low infrastructure management, elastic scaling, pay-per-use characteristics.

**Risks:** cold starts, runtime limits, observability, provider coupling, cost surprises at sustained scale, distributed workflow complexity.

# CQRS

Separates models/paths for commands and queries.

**Good fit:** read and write models have materially different needs or complex domains benefit from independent representations.

**Risk:** duplicated models and synchronization complexity. CRUD systems rarely need it.

CQRS does not require Event Sourcing.

# Event Sourcing

Stores domain state as a sequence of events rather than only current state.

**Good fit:** audit/history is central and the domain benefits from reconstructing temporal state.

**Costs:** event evolution, replay, projections, debugging, storage, privacy/deletion requirements and substantial conceptual complexity.

Do not choose it merely because the system already publishes events.

# Selection matrix

Evaluate styles using forces rather than popularity:

| Force | Modular Monolith | Service-Based | Microservices | EDA |
|---|---|---|---|---|
| Initial operational simplicity | High | Medium | Low | Medium-Low |
| Local transaction simplicity | High | Medium | Low | Low |
| Independent deployment | Low-Medium | High | High | Consumer-dependent |
| Independent scaling | Medium | High | High | High |
| Distributed failure exposure | Low | Medium | High | High |
| Small-team fit | High | Medium-High | Often Low | Context-dependent |
| Eventual consistency burden | Low | Medium | Medium-High | High |

This table is a heuristic, not a scoring algorithm.

# Architecture selection exercise

For each scenario, choose two plausible styles, compare them and reject one explicitly:

1. New SaaS product, four engineers, unknown product-market fit.
2. Global payment processor with independently owned domains.
3. IDE supporting third-party extensions.
4. Flash-sale platform with extreme short-lived traffic spikes.
5. Enterprise integrating decades of heterogeneous systems.

For every choice explain **why not the alternatives**. Architecture maturity is visible in rejected options as much as selected ones.