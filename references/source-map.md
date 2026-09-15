# Tech Mastery Source Map

This file maps high-value external repositories to the learning system. These are discovery/reference sources, not material to copy blindly.

## System Design foundations

### donnemartin/system-design-primer
https://github.com/donnemartin/system-design-primer

Useful for:
- latency vs throughput;
- performance vs scalability;
- availability vs consistency;
- CAP and consistency patterns;
- replication/failover;
- DNS/CDN/load balancing/proxies;
- relational and NoSQL storage;
- caching strategies;
- queues/backpressure;
- communication fundamentals;
- system-design interview process and exercises.

Use as a breadth/checklist source. Re-evaluate simplified statements against DDIA and modern primary documentation where deeper precision matters.

### ByteByteGoHq/system-design-101
https://github.com/ByteByteGoHq/system-design-101

Useful for:
- visual mental models;
- API/protocol comparisons;
- database/storage patterns;
- real-world engineering case studies;
- architecture evolution examples;
- queues, Kafka, delivery semantics, locking and sharding.

Use visual explanations to discover concepts, then connect them to requirements, trade-offs and evidence rather than memorizing diagrams.

### karanpratapsingh/system-design
https://github.com/karanpratapsingh/system-design

Useful for a structured path across:
- IP/OSI/TCP/UDP;
- DNS/load balancing/caching/CDN;
- databases/indexes/transactions;
- CAP/PACELC;
- replication/sharding/consistent hashing;
- messaging/pub-sub;
- architecture styles;
- REST/GraphQL/gRPC/WebSockets/SSE;
- resilience, SLI/SLO and disaster recovery;
- case studies.

### systemdesign42/system-design-academy
https://github.com/systemdesign42/system-design-academy

Use as an additional structured system-design reference and cross-check source.

## Resource indexes

### ashishps1/awesome-system-design-resources
https://github.com/ashishps1/awesome-system-design-resources

Discovery index for system-design articles, case studies and learning material.

### madd86/awesome-system-design
https://github.com/madd86/awesome-system-design

Additional system-design discovery index.

### checkcheckzz/system-design-interview
https://github.com/checkcheckzz/system-design-interview

Useful primarily for additional design prompts and interview-style practice. Our handbook should go beyond interview optimization toward production architecture judgment.

## Scalability and architecture

### binhnguyennus/awesome-scalability
https://github.com/binhnguyennus/awesome-scalability

Useful for real engineering articles on scalability, availability, performance and production architecture.

### mehdihadeli/awesome-software-architecture
https://github.com/mehdihadeli/awesome-software-architecture

Useful for discovering architecture styles, DDD, microservices, modular monoliths, EDA, patterns and implementation references.

Rule: architecture style is selected from forces and trade-offs—not from popularity.

## Distributed systems and papers

### theanalyst/awesome-distributed-systems
https://github.com/theanalyst/awesome-distributed-systems

Discovery source for distributed-systems concepts, implementations and research.

### papers-we-love/papers-we-love
https://github.com/papers-we-love/papers-we-love

Research-paper directory useful for moving from practitioner summaries to foundational computer-science work.

Potential future reading paths:
- distributed systems;
- databases/storage;
- networking;
- operating systems;
- programming languages;
- security;
- machine learning/AI.

Do not optimize for number of papers read. Extract problem, assumptions, model, contribution, limitations, production relevance and how later systems changed the idea.

### jeffrey-xiao/papers
https://github.com/jeffrey-xiao/papers

Additional paper discovery/reference source.

## Learn by building

### codecrafters-io/build-your-own-x
https://github.com/codecrafters-io/build-your-own-x

High-value source for implementation labs. Candidate mastery projects:
- web server;
- database/key-value store;
- Redis-like cache;
- Kafka-like log/broker;
- container;
- Git;
- shell;
- network stack;
- search engine;
- language/interpreter;
- simplified AI model/RAG system.

The objective is not production parity. Build enough to understand invariants, data structures, protocols, persistence, concurrency, failure and operational behavior.

## Production architecture laboratory

### GoogleCloudPlatform/microservices-demo
https://github.com/GoogleCloudPlatform/microservices-demo

Use as a concrete distributed application to inspect:
- service boundaries;
- synchronous/asynchronous calls;
- deployment topology;
- containers/Kubernetes;
- observability;
- CI/CD;
- security;
- resilience;
- operational complexity.

Important exercise: design the same product first as a modular monolith and compare both designs. The lesson is not that microservices are correct; it is to understand what they buy and what they cost.

## Low-Level Design

### ashishps1/awesome-low-level-design
https://github.com/ashishps1/awesome-low-level-design

Useful for:
- object modeling;
- OOP/design principles;
- design patterns;
- machine-coding/LLD exercises;
- translating requirements into maintainable code structures.

Connect LLD upward to domain boundaries and architecture rather than treating it as a separate interview puzzle category.

## How to consume these sources

Use this workflow:

```text
Discover topic/source
 -> identify the problem
 -> read multiple perspectives when important
 -> find primary material when precision matters
 -> synthesize mental model
 -> identify alternatives/trade-offs
 -> implement or design an exercise
 -> introduce failure
 -> add observability
 -> defend the decision
 -> capture durable notes in this repository
```

## Source quality hierarchy

Depending on the question, prefer approximately:

```text
Primary specifications / official documentation / original papers
        ↓
High-quality books and engineering publications
        ↓
Company engineering case studies
        ↓
Curated educational repositories
        ↓
Awesome lists / aggregators for discovery
```

Aggregators are excellent maps. They are not automatically authoritative evidence.

## Maintenance rule

Do not import everything. A source enters the learning path only when it closes a knowledge gap, adds a useful exercise, provides a stronger mental model, or exposes a meaningful alternative/trade-off.