# Case Study 04 — Messaging Platform

## What this case teaches

Messaging systems combine persistent connections, delivery semantics, ordering, presence, offline users and multi-device synchronization.

Core topics:
- WebSocket/persistent connection management;
- message durability;
- delivery acknowledgements;
- ordering scope;
- offline delivery;
- presence as ephemeral state;
- fan-out to devices;
- idempotency and deduplication;
- observability for delivery latency and backlog.

## Pass 1 — Small product

Assume:
- 100k registered users;
- 10k concurrent users;
- one-to-one chat only;
- one region;
- average 2 messages/user/minute while active;
- small team.

### Functional requirements
- connect/disconnect;
- send message;
- receive message;
- fetch conversation history;
- message delivery acknowledgement;
- basic online/offline presence.

### Initial architecture

```text
Client
  |
  v
Connection/API Layer
  |
  +--> PostgreSQL (users, conversations, messages)
  |
  +--> in-process / simple shared connection registry if required
  |
  +--> push notification provider for offline users
```

A relational store may be entirely adequate initially. Do not assume a chat system automatically requires a specialized distributed database.

## Message identity

Every logical message should have a stable client or server message ID.

Why:
- retries happen;
- client may not know whether server accepted a message;
- duplicate send attempts must not create duplicate conversation effects.

## Delivery states

Example:

```text
CREATED
 -> ACCEPTED
 -> DELIVERED_TO_DEVICE
 -> READ
```

These states have different meanings. Avoid claiming "delivered" when the message only reached the server.

## Ordering

Global ordering is unnecessary.

Usually the useful scope is per conversation.

Possible strategy:
- monotonic conversation sequence number generated on accepted messages;
- clients order by sequence, not unreliable wall-clock timestamps.

Do not rely on clocks across devices/servers for strict ordering.

## Presence

Presence is ephemeral and can tolerate weaker consistency than messages.

Examples:
- online;
- last seen;
- typing indicator.

If a presence update is lost, eventual correction is usually acceptable. Do not give presence the same durability guarantees as message content.

## Offline delivery

If recipient is disconnected:
- persist message first;
- notify via mobile push where useful;
- deliver pending messages on reconnect;
- track device/session acknowledgement where needed.

Push notifications are hints, not the source of truth for message delivery.

## Observability baseline

Technical:
- active connections;
- connection establishment errors;
- send/receive rate;
- accepted-to-delivered latency p50/p95/p99;
- DB latency;
- pending/offline message count;
- push notification failures.

Business/product:
- messages accepted;
- conversations with delivery delay;
- messages older than threshold not delivered;
- reconnect frequency;
- active conversations.

## Pass 2 — Connection scale

Evidence:
- 1M concurrent connections;
- individual app instances cannot maintain all sockets;
- users reconnect frequently;
- messages for one user may arrive through different connection nodes.

Potential evolution:

```text
Clients
  |
  v
Connection Gateways
  |
  +--> Connection Directory / routing state
  |
  +--> Messaging Service
          |
          +--> Message Store
          +--> Delivery Queue / broker if justified
```

The connection directory is ephemeral routing state, distinct from durable message history.

A broker becomes useful if it solves real routing/buffering/decoupling needs, not because messaging products are assumed to need Kafka.

## Pass 3 — Multi-device / groups / global

New requirements:
- multiple devices per user;
- groups up to thousands of members;
- global users;
- regional routing;
- media attachments;
- stronger privacy/security requirements.

Now architecture may need:
- per-user/device delivery state;
- group fan-out strategy;
- media object storage;
- regional connection gateways;
- durable asynchronous delivery;
- partitioning by conversation/user;
- stronger end-to-end encryption/key-management design where product requires it.

## Group fan-out trade-off

### Fan-out on send
Create delivery work for each recipient/device when message is accepted.

Strength: fast recipient reads/delivery.
Cost: write amplification for large groups.

### Fan-out on read
Store once and let recipients read from shared conversation history.

Strength: low write amplification.
Cost: more read coordination, difficult per-device delivery semantics.

Hybrid approaches may be justified by group-size distribution.

## Failure analysis

What if:
- sender retries after network timeout?
- recipient reconnects to another gateway?
- delivery acknowledgement is lost?
- two messages race in one conversation?
- push succeeds but message persistence failed?
- one delivery worker is delayed?
- connection directory is stale?

## ADR exercises

Write ADRs for:
1. relational message store initially;
2. per-conversation sequence ordering;
3. presence as weaker-consistency ephemeral data;
4. when a delivery broker becomes justified;
5. connection-gateway separation;
6. group fan-out strategy.

## What not to add without evidence

Do not automatically add:
- Cassandra/Dynamo-style storage;
- Kafka;
- Redis for every user state;
- global active-active writes;
- service mesh;
- microservice per chat capability.

Let concurrency, history volume, delivery semantics and global requirements drive evolution.