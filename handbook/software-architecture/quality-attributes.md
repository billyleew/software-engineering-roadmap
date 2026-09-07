# Quality Attributes — The Architecture Drivers

Functional requirements describe **what** a system does. Quality attributes describe **how well and under what conditions** it must do it.

Architecture is strongly shaped by the quality attributes that matter most.

## Availability

The proportion of time a capability is usable.

Questions:
- What availability does the business actually require?
- Per system, endpoint, journey or region?
- Is planned maintenance included?
- What dependencies limit achievable availability?

Higher availability generally increases redundancy, operational complexity and cost.

## Reliability

The probability the system performs correctly over a period of time. A service can be reachable yet unreliable if it returns incorrect results.

For payments, correctness and duplicate prevention can matter more than returning a fast response.

## Scalability

Ability to handle growth by adding resources or changing structure without unacceptable degradation.

Distinguish:
- request scalability;
- data scalability;
- organizational scalability;
- geographic scalability.

Do not design for imaginary hyperscale. Identify realistic growth and the cost of scaling later.

## Performance

Use measurable dimensions:
- latency percentiles (p50/p95/p99);
- throughput;
- concurrency;
- resource utilization;
- queue depth.

Average latency can hide severe tail latency.

## Consistency

Define what users are allowed to observe after writes and during failures.

Examples:
- strong/read-after-write requirement for account balance;
- eventual consistency acceptable for analytics dashboard;
- monotonic reads useful for user experience.

Consistency is a business-semantic decision before it becomes a database setting.

## Security

Includes confidentiality, integrity, availability, authentication, authorization, auditability, privacy and abuse resistance.

Ask what assets are valuable, who may access them, where trust boundaries exist and how compromise is contained.

## Maintainability / Modifiability

How safely and quickly can the system accommodate change?

Useful signals:
- lead time for common changes;
- number of components/teams touched;
- regression rate;
- test feedback time;
- coupling between modules/services.

## Observability

Ability to infer internal system state from emitted signals.

Logs alone are not observability. Design correlation, metrics, traces and business signals so unknown failures can be investigated.

## Recoverability

How quickly and completely can service/data be restored after failure?

Define:
- RTO — maximum acceptable recovery time;
- RPO — maximum acceptable data loss window.

Backups without restore testing are an assumption, not a recovery capability.

## Interoperability

Ability to exchange data and behavior correctly with other systems. Contracts, versioning, schemas and compatibility strategy become architectural concerns.

## Deployability

Ability to release changes safely and independently enough for business needs.

Microservices may improve independent deployability but introduce distributed-system and platform costs. A modular monolith with disciplined boundaries can often deploy rapidly with far less operational complexity.

## Testability

How easily behavior and failure modes can be verified. Architecture that hides dependencies or mixes infrastructure with policy makes testing expensive.

## Auditability

Ability to reconstruct who did what, when and why. Important for finance, security and regulated systems.

## Cost efficiency

Architecture consumes money through compute, storage, network, licenses and—often more significantly—engineering/operational effort.

## Sustainability

Consider resource efficiency where material: compute utilization, storage growth, network transfer and unnecessary model/AI inference.

# Quality attribute scenario template

```text
Attribute:
Source:
Stimulus:
Environment:
Artifact/capability affected:
Expected response:
Measurable response:
Business reason:
```

Example:

```text
Attribute: Availability
Source: Availability Zone failure
Stimulus: database primary becomes unavailable
Environment: normal production traffic
Artifact: checkout
Response: fail over automatically
Measure: checkout restored within 60 seconds, no committed order lost
Business reason: checkout downtime directly stops revenue
```

# Trade-off exercise

For a banking transfer system, rank these attributes and justify the order:

```text
correctness
availability
latency
consistency
security
auditability
cost
maintainability
```

Then repeat for a social-media "like" counter. If your architecture and priorities remain identical, the requirements have probably not influenced the design enough.