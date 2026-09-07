# Case Study 05 — Ride Dispatch Platform

## What this case teaches

Ride dispatch combines rapidly changing geospatial state, low-latency matching, regional partitioning, transactional trip state and real-time client updates.

Core topics:
- geospatial indexing;
- ephemeral vs durable state;
- matching algorithms;
- regional partitioning;
- state machines;
- concurrency;
- consistency trade-offs;
- real-time updates;
- observability around match quality and latency.

## Pass 1 — One city

Assume:
- 20k riders;
- 5k drivers;
- 1k concurrent trips;
- one city;
- one region;
- 5 engineers.

### Functional requirements
- driver goes online/offline;
- driver periodically sends location;
- rider requests trip;
- find nearby available drivers;
- offer trip;
- driver accepts/rejects;
- trip transitions through pickup/in-progress/completed/cancelled;
- rider and driver receive updates.

### Domain boundaries

Possible logical contexts:
- Rider/Driver Identity;
- Availability;
- Dispatch;
- Trip;
- Pricing;
- Payments;
- Notifications.

Do not make each context a microservice initially.

## Separate ephemeral and durable state

Driver location changes frequently and may not need durable transactional history for every update.

Trip state, payment state and audit-sensitive events are different.

Example:

```text
Ephemeral:
- current driver location
- current availability
- heartbeat/connection state

Durable:
- trip request
- assigned driver
- accepted trip
- trip lifecycle
- fare/payment
- audit events
```

Mixing both into the same storage semantics can be inefficient or confusing.

## Initial architecture

```text
Rider/Driver Apps
      |
      v
Application/API
      |
      +--> PostgreSQL (trip + durable business state)
      |
      +--> geospatial-capable store/index for current driver location
      |
      +--> realtime connection/push channel
```

A single deployable application may still be appropriate.

## Matching flow

```text
Rider requests trip
 -> validate request
 -> query nearby available drivers
 -> rank candidate drivers
 -> offer to one/small batch
 -> first valid acceptance wins
 -> persist assignment atomically
 -> notify rider/driver
```

## Concurrency problem

Two riders may try to acquire the same driver.

Do not solve this with "the UI won't send two requests".

Protect assignment with durable concurrency semantics such as:
- database conditional update/version;
- transactional state transition;
- compare-and-set.

## Geospatial search

At modest scale, geospatial support in an existing database may be enough.

At higher update/query rates, specialized in-memory/geospatial indexing may become justified.

Questions:
- update frequency per driver;
- acceptable location staleness;
- search radius;
- density distribution;
- hotspot regions;
- cost of index updates.

## Observability baseline

Technical:
- location updates/sec;
- location-update lag/failures;
- candidate-search p95/p99;
- assignment transaction conflicts;
- realtime connection failures;
- API error/latency.

Business/product:
- request-to-match latency;
- match success rate;
- offer acceptance rate;
- cancellation rate;
- pickup ETA accuracy;
- percentage of requests with no candidate;
- driver utilization.

A platform can be technically healthy while matching badly. Product metrics are essential.

## Pass 2 — City scale pressure

Evidence:
- 100k online drivers;
- 1M location updates/minute;
- central location table becomes write-heavy;
- dense downtown zones become hotspots.

Potential evolution:
- move live location to a purpose-built partitioned/geospatial index;
- partition by geographic cell/region;
- reduce update frequency adaptively when vehicle movement is low;
- keep durable trip state in transactional storage;
- isolate dispatch compute if CPU/latency pressure is real.

Notice: the measured problem is **location update/search pressure**, not "the monolith" in general.

## Pass 3 — Multi-region / multiple cities

New requirements:
- many cities/countries;
- data residency constraints;
- independent regional operations;
- regional outages must not stop all dispatch;
- pricing rules vary by market.

Regional partitioning becomes a natural architectural boundary because most trips occur within one geography.

Possible model:

```text
Global control plane
      |
      +--> Region A dispatch/data plane
      +--> Region B dispatch/data plane
      +--> Region C dispatch/data plane
```

Keep cross-region dependencies away from the real-time dispatch critical path unless required.

## Failure analysis

What if:
- driver location is 20 seconds stale?
- two riders receive offers to same driver?
- driver accepts but response is lost?
- realtime connection drops after assignment?
- regional location index is unavailable?
- pricing service becomes slow?
- notification fails but assignment succeeds?

Distinguish state from communication. If notification fails, the persisted trip assignment may still be correct and recoverable on reconnect.

## Resilience

Use patterns only for demonstrated failure modes:
- timeout candidate search;
- bounded retry for safe location updates;
- idempotent trip-request creation;
- graceful degradation if non-critical ETA enrichment fails;
- avoid retrying assignment blindly without concurrency control.

## ADR exercises

Write ADRs for:
1. separating live location from durable trip state;
2. initial geospatial storage choice;
3. driver assignment concurrency mechanism;
4. when dispatch becomes independently deployable;
5. geographic partitioning strategy;
6. regional independence and failure isolation.

## What not to add without evidence

Do not automatically add:
- Kafka for every location update;
- microservice per domain noun;
- global distributed database;
- Redis solely because location is "real time";
- CQRS/event sourcing for all trip state.

Use the access pattern, latency target, update rate and regional requirements to justify complexity.