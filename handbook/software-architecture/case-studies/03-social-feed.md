# Case Study 03 — Social Feed

## What this case teaches

Feeds force trade-offs between write amplification, read latency, ranking complexity, cacheability and hot-user behavior.

Core topics:
- fan-out on write vs fan-out on read;
- eventual consistency;
- ranking;
- hot keys/hot users;
- caching;
- timeline materialization;
- observability tied to freshness and user experience.

## Pass 1 — Small product

Assume:
- 50k users;
- 5k daily active users;
- 20 posts/second peak;
- 200 feed reads/second peak;
- chronological feed first;
- one region;
- small team.

### Functional requirements
- follow/unfollow;
- create post;
- read home feed;
- read profile feed;
- delete post.

### Initial architecture

A simple design can work:

```text
Client
  |
  v
Application
  |
  +--> PostgreSQL
  |      |- users
  |      |- follows
  |      |- posts
  |
  +--> optional cache only if measured need appears
```

For a small system, querying recent posts from followed users with proper indexes may be enough. Do not introduce precomputed timelines before there is evidence that reads are too expensive.

## Data model

```text
User(id, ...)
Follow(follower_id, followed_id, created_at)
Post(id, author_id, created_at, content_ref, deleted_at)
```

Indexes should reflect real feed/profile access patterns.

## Pass 2 — Read pressure appears

Evidence:
- feed query p99 becomes high;
- DB spends most time repeatedly joining follows + posts;
- feed reads outnumber writes by a large factor.

Now compare two approaches.

### Fan-out on read
At request time, fetch recent posts from followed users and merge/rank.

Strengths:
- simple write path;
- no timeline duplication;
- updates/deletes naturally reflected.

Costs:
- expensive reads for users following many accounts;
- latency increases with graph size.

### Fan-out on write
When an author posts, append post reference to follower timelines.

Strengths:
- fast feed reads;
- read path becomes simple.

Costs:
- large write amplification;
- celebrity/hot-user problem;
- consistency/deletion/update complexity;
- timeline storage growth.

## Hybrid approach

A common conceptual answer is hybrid fan-out:
- ordinary users: fan-out on write;
- very high-follower accounts: merge at read time.

But do not adopt hybrid complexity until follower-distribution data shows it is needed.

## Ranking

Do not jump directly to ML ranking.

Progression:

```text
chronological
 -> simple heuristic ranking
 -> feature-based scoring
 -> ML ranking only when product evidence and data maturity justify it
```

Ranking changes architecture because it introduces feature freshness, experimentation, model serving and explainability/quality monitoring.

## Caching

Potential cache targets:
- user/feed page results;
- post metadata;
- follow graph fragments;
- ranking features.

Before caching:
- identify actual bottleneck;
- define staleness;
- define invalidation/deletion behavior;
- monitor hit ratio and hot-key concentration.

Do not put Redis everywhere just because feeds are read-heavy.

## Consistency

A home feed usually tolerates some eventual consistency.

Examples that may be acceptable:
- a newly followed account takes seconds to appear;
- a new post appears with slight delay.

Examples that may need stronger behavior:
- blocked/private-user content must not leak;
- deleted/restricted content should be suppressed promptly.

Security/privacy rules can require stronger filtering than ordinary freshness rules.

## Observability baseline

Technical:
- feed read p50/p95/p99;
- DB query latency;
- rows scanned;
- cache hit ratio if cache exists;
- timeline generation lag;
- fan-out job queue age;
- hot partition/key distribution.

Business/product:
- feed loads succeeded;
- feed freshness delay;
- empty-feed rate;
- posts viewed/session;
- ranking experiment metrics where relevant.

## Pass 3 — Large scale

New requirements:
- tens of millions of users;
- highly skewed follower distribution;
- global users;
- ranked feed;
- high post volume;
- independent feed, social graph and ranking teams.

Possible evolution:
- dedicated social-graph storage/read model;
- timeline materialization service;
- queue/stream for fan-out where throughput/replay semantics justify it;
- distributed caches for hot timelines;
- partitioning by user/timeline;
- ranking service/feature store if ML is justified;
- regional read paths.

Each addition should map to a specific force.

## Failure analysis

What if:
- fan-out job is delivered twice?
- one follower partition is delayed?
- celebrity posts to 50M followers?
- cache contains a deleted post?
- ranking service is unavailable?
- social graph returns stale privacy state?

Graceful degradation might fall back to chronological ranking. It must never bypass privacy/blocking constraints.

## ADR exercises

Write ADRs for:
1. chronological SQL feed as the initial design;
2. when timeline precomputation becomes justified;
3. fan-out-on-write vs fan-out-on-read;
4. celebrity/hot-user strategy;
5. cache introduction based on measured query/read pressure;
6. ranking fallback behavior.

## What not to add without evidence

Do not automatically add:
- Kafka;
- graph database;
- Redis cluster;
- ML ranking;
- sharding;
- dozens of feed microservices.

A feed is an excellent place to learn that architectural sophistication should follow measured product and scale pressure.