# Case Study 06 — Edge / CDN Platform

## What this case teaches

Edge systems emphasize global distribution, caching, origin protection, routing, consistency of configuration, invalidation and cost-efficient delivery.

Core topics:
- cache keys;
- TTL and freshness;
- invalidation;
- origin shielding;
- regional/edge routing;
- stale-while-revalidate concepts;
- configuration propagation;
- global observability;
- DDoS/rate-limit considerations.

## Pass 1 — Use a managed CDN

Assume:
- one web application;
- users in one continent;
- static assets + public media;
- 100 Mbps average outbound traffic;
- small team.

The first architectural question should usually be:

> Can a managed CDN solve this better and more cheaply than building our own edge network?

Likely architecture:

```text
User
  |
  v
Managed CDN
  |
  +--> cache hit -> response
  |
  +--> cache miss -> Origin/API/Object Storage
```

## Cache key

The cache key defines when two requests are considered equivalent.

Potential dimensions:
- hostname;
- path;
- selected query parameters;
- content encoding;
- language/device where truly needed.

Adding too many dimensions destroys hit ratio. Omitting a required dimension can serve incorrect/private content.

## TTL / freshness

Caching is a correctness trade-off.

Questions:
- how stale can content be?
- can objects use immutable/versioned URLs?
- does origin provide validation metadata?
- what happens after content update/delete?

Versioned static assets make caching dramatically simpler:

```text
/app.abc123.js
```

can often be cached for a long time because a new deployment creates a new key.

## Invalidation

Invalidation is expensive/complex at global scale.

Prefer designs that reduce invalidation requirements:
- immutable/versioned assets;
- short TTL where business allows;
- explicit purge only where necessary.

Do not solve every freshness requirement with global purge.

## Private/authenticated content

Never assume CDN caching is safe merely because HTTPS is used.

Define:
- whether response is cacheable;
- cache-key identity dimensions;
- signed URLs/cookies where applicable;
- tenant/user isolation;
- sensitive headers/cookies;
- cache-control behavior.

A cache-key mistake can become a data leak.

## Observability baseline

- requests/sec;
- cache hit/miss ratio;
- origin request rate;
- edge and origin latency p50/p95/p99;
- 4xx/5xx;
- bytes served;
- egress cost;
- origin bandwidth/CPU;
- top objects/paths;
- geographic latency;
- stale/error-served responses.

Business view:
- page/video/download success;
- customer geography affected;
- latency impact on conversion/engagement where relevant.

## Pass 2 — Origin becomes bottleneck

Evidence:
- cache hit ratio 92%, but misses for popular uncached API/object paths overload origin during traffic spikes;
- many edge locations request the same newly popular object simultaneously.

Possible evolution:
- fix cacheability/key first;
- request collapsing/coalescing if supported;
- origin shield / regional cache tier;
- stale-on-error for business-safe content;
- rate limiting/load shedding at edge.

Do not simply scale origin indefinitely if repeated work is safely cacheable.

## Origin shielding

Conceptually:

```text
Edge POPs
   |
   v
Regional/Shield Cache
   |
   v
Origin
```

This can reduce duplicate misses hitting origin. It also adds another cache layer/freshness behavior that must be observed.

## Pass 3 — Design an edge platform

Now assume the business itself needs an edge platform:
- customers configure hostnames/rules;
- globally distributed points of presence;
- dynamic routing;
- cache purge;
- TLS certificate lifecycle;
- DDoS protection;
- high control-plane availability;
- data plane should continue if control plane is unavailable.

Natural separation:

```text
Control Plane
- customer configuration
- certificates
- policy/rules
- configuration distribution

Data Plane
- DNS/routing
- TLS termination
- request processing
- cache
- origin fetch
- security enforcement
```

The data plane should avoid synchronous dependency on a central control plane for every request.

## Configuration propagation

Global configuration is a distributed consistency problem.

Define:
- versioned configuration;
- propagation time target;
- atomicity per configuration bundle;
- rollback;
- behavior when a POP misses an update;
- audit trail;
- validation before rollout.

Strong global instantaneous consistency may be prohibitively expensive and unnecessary. Product semantics should define acceptable propagation delay.

## Routing

Conceptual techniques may include DNS-based routing, anycast/network routing and application-level regional selection.

Do not choose a mechanism without understanding:
- failure detection;
- convergence;
- locality;
- health checks;
- route flapping;
- provider/network constraints.

## Failure analysis

What if:
- origin is down?
- one POP fails?
- purge reaches only 80% of locations?
- bad configuration is globally distributed?
- TLS certificate renewal fails?
- shield layer is overloaded?
- control plane is unavailable?
- attacker creates extremely high-cardinality cache keys?

## Security

Consider:
- DDoS;
- rate limiting;
- WAF-like policy where justified;
- tenant isolation;
- TLS key protection;
- cache poisoning;
- request smuggling/desync classes;
- SSRF to origin/internal networks;
- configuration authorization/audit.

## ADR exercises

Write ADRs for:
1. managed CDN vs custom edge platform;
2. cache-key policy;
3. immutable assets vs purge-heavy design;
4. origin shielding trigger;
5. control-plane/data-plane separation;
6. acceptable configuration propagation consistency.

## What not to add without evidence

Do not automatically build:
- a global anycast network;
- custom cache software;
- multi-tier caching;
- your own DNS platform;
- global consensus for every configuration change.

Most product teams should buy the edge capability. Building an edge platform is justified only when edge itself is a strategic product/capability or managed offerings cannot satisfy concrete requirements.