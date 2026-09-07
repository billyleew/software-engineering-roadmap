# Integration Architecture — APIs, Messages and Events

## Principle

Choose an integration style from interaction semantics rather than technology preference.

Ask first:

```text
Does the caller need an immediate answer?
Can work happen asynchronously?
Is the interaction a command, query or fact/event?
What happens if either side is unavailable?
What consistency is required?
Can delivery be duplicated or reordered?
```

# Synchronous request/response

## REST/HTTP

Strong default for public/business APIs and resource-oriented interactions due to broad interoperability and tooling.

Design concerns:
- resource/action semantics;
- status/error model;
- idempotency;
- pagination/filtering;
- authentication/authorization;
- rate limiting;
- version compatibility;
- timeout budgets.

## gRPC

Useful for strongly typed service-to-service RPC, streaming and performance-sensitive internal communication where ecosystem/client constraints fit.

It does not remove distributed-system failure. A local-looking function call remains a network operation.

# Asynchronous messaging

Useful when producer and consumer should be temporally decoupled or work can be buffered.

## Queue mental model

A message commonly represents work intended for processing, often by one worker from a competing consumer group.

Examples:
- generate invoice;
- resize image;
- send notification.

## Event mental model

An event represents a fact that already occurred.

Examples:
- `OrderConfirmed`;
- `PaymentAuthorized`;
- `CustomerAddressChanged`.

Consumers decide what the fact means to them. The producer should not need to know every reaction.

# Command vs event

```text
Command: SendWelcomeEmail
Intent: please perform an action

Event: CustomerRegistered
Fact: something already happened
```

Calling commands "events" can create hidden orchestration and misleading coupling.

# Event notification vs event-carried state

A small notification may contain an identifier requiring consumers to query the producer. Event-carried state can reduce synchronous coupling but duplicates data and creates schema/privacy considerations.

Choose deliberately.

# Orchestration vs choreography

## Orchestration
A coordinator explicitly manages workflow steps.

Strength: workflow is easier to discover/control.
Cost: coordinator can become central coupling if poorly designed.

## Choreography
Services react to events without one central workflow controller.

Strength: local autonomy/extensibility.
Cost: end-to-end business flow can become difficult to understand, debug and govern.

Do not assume choreography is inherently more decoupled or mature.

# Delivery and idempotency

Design consumers assuming redelivery is possible.

Use stable message/event identifiers and make side effects idempotent where required. Acknowledgement semantics, retry and dead-letter handling must be understood for the selected broker.

# Ordering

Define the scope where order is necessary. Partition/key messages so related operations preserve order where supported, rather than demanding global order.

# Retry and poison messages

Transient failures may be retried with bounded backoff. Permanent/data failures should not loop forever.

Define:
- retry count/time budget;
- backoff/jitter;
- dead-letter/quarantine strategy;
- operator/reprocessing workflow;
- idempotency during replay.

# Schema evolution

Events and APIs are contracts that may outlive a deployment.

Prefer additive compatible changes. Establish ownership, version policy, compatibility tests and deprecation strategy.

Schema registries can help at scale, but governance process matters more than merely installing one.

# API Gateway

Can centralize cross-cutting edge concerns such as routing, authentication integration, quotas and observability.

Avoid placing domain/business orchestration in a gateway until it becomes another hidden application.

# Integration anti-pattern: distributed monolith

A system can have many independently deployed services while remaining tightly coupled if:
- every request requires long synchronous call chains;
- services share internal database tables;
- deployments must be coordinated;
- contracts change in lockstep;
- one service outage breaks unrelated capabilities.

Service count does not create autonomy.

# Observability requirements

Every integration boundary should expose enough evidence to answer:
- request/message volume;
- success/failure;
- latency or processing time;
- retries;
- queue depth/lag/oldest age;
- dead-letter volume;
- dependency status;
- trace/correlation context;
- business outcome.

# Exercise — order workflow

Design:

```text
Order -> Inventory -> Payment -> Shipping -> Notification
```

Produce three designs:
1. synchronous HTTP chain;
2. orchestrated asynchronous workflow;
3. event-driven choreography.

For each, analyze latency, consistency, duplicate delivery, partial failure, debugging, observability, team ownership and operational complexity. Choose one for a five-person team and then reconsider the decision for five independent domain teams.