# Containers — Understand the Runtime Before the Orchestrator

## Objective

Containers package an application and its runtime dependencies into a repeatable execution unit. They are useful because they improve portability, isolation and delivery consistency—not because every workload must run in a container.

Before Kubernetes, understand what a container actually is.

## Mental model

A container is not a tiny virtual machine. It is a process (or group of processes) isolated and constrained using operating-system capabilities.

Important Linux concepts:
- namespaces isolate views of processes, networking, mounts, users and other resources;
- cgroups account for and limit CPU/memory and other resources;
- capabilities reduce the privileges traditionally associated with root;
- filesystems/layers provide packaged runtime state;
- container runtimes create and manage the isolated process environment.

```text
Application process
 + filesystem/image
 + namespaces
 + cgroups
 + security constraints
 = containerized workload
```

A VM virtualizes a machine boundary; a container primarily isolates processes while sharing the host kernel.

# Images and layers

An image is an immutable package used to create containers. Layers allow reuse and efficient distribution, but layer design affects build speed, cache behavior, size and security.

Prefer:
- small appropriate base images;
- pinned/controlled dependencies;
- multi-stage builds where useful;
- deterministic builds where practical;
- no secrets in image layers;
- non-root runtime users;
- explicit versions rather than ambiguous mutable tags for production promotion.

Do not optimize image size blindly. Debuggability, compatibility and security also matter.

# Build context and caching

Container builds can become a CI bottleneck.

Measure:
- context transfer time;
- dependency installation;
- compilation;
- layer cache hit/miss;
- image export/push;
- registry download time.

Order layers so frequently changing source does not unnecessarily invalidate expensive stable dependency layers.

Build caching is an optimization with correctness implications. A fast stale build is worse than a slower correct build.

# Runtime lifecycle

A containerized application should behave predictably as a managed process:
- start deterministically;
- expose readiness only when able to serve;
- respond to termination signals;
- stop gracefully within a bounded time;
- externalize durable state;
- emit telemetry to external systems;
- avoid relying on local ephemeral filesystem state for business durability.

# PID 1 and graceful shutdown

The process receiving termination signals must correctly propagate/handle them.

For a server:

```text
SIGTERM
 -> stop accepting new work
 -> finish/cancel bounded in-flight work
 -> flush required state/telemetry
 -> close resources
 -> exit
```

If shutdown behavior is wrong, deployments can create failed requests even when the new version is healthy.

# Resource requests, limits and saturation

Even outside Kubernetes, understand resource constraints.

CPU exhaustion usually creates latency/throughput degradation. Memory limits can terminate processes abruptly.

Observe:
- CPU utilization/throttling;
- memory working set/limit;
- OOM kills;
- filesystem usage;
- network throughput/errors;
- process/thread/runtime metrics;
- application RED/business metrics.

Do not choose limits from guesses alone. Establish workload baselines and load-test important services.

# Networking

Container networking introduces virtual interfaces, address translation/bridges or overlay mechanisms depending on runtime/platform.

Know the path:

```text
client
 -> load balancer/proxy
 -> host/node network
 -> container network
 -> application port
```

When debugging, determine whether failure is DNS, routing, firewall/policy, proxy, connection, TLS or application-level.

# Storage

Container writable layers are normally ephemeral.

Use external durable systems/volumes when durability is required. Ask:
- who owns the data?
- what happens when the container is replaced?
- backup/restore?
- concurrency/access mode?
- performance?
- encryption?

Stateless application containers simplify scheduling, but the system itself is rarely stateless because databases, queues and object stores carry state.

# Security

Containerization is not a security boundary by itself.

Practices:
- run as non-root where practical;
- minimize Linux capabilities;
- read-only filesystem where feasible;
- avoid privileged containers;
- scan dependencies/images according to risk;
- patch/rebuild base images;
- use trusted registries;
- verify provenance/signatures where requirements justify it;
- never bake secrets into images;
- restrict network access and workload identity.

# Container observability

Correlate infrastructure/container signals with application signals.

```text
request/business failure
 -> application version
 -> container instance
 -> host/node
 -> resource saturation
 -> dependency behavior
 -> deployment event
```

A container restart count alone is not the business symptom. Determine why it restarted and what customer impact occurred.

# Failure exercises

Experiment locally or in a safe lab:
1. kill the process during active requests;
2. send SIGTERM and inspect graceful shutdown;
3. constrain memory until OOM;
4. constrain CPU and measure p50/p95/p99;
5. remove network access to a dependency;
6. make DNS fail;
7. fill ephemeral disk;
8. deploy an incompatible configuration;
9. restart the container and verify business state survives where required.

For every experiment record:
- expected behavior;
- observed behavior;
- telemetry;
- customer/business effect;
- recovery mechanism.

# When containers may not be necessary

A simple managed/serverless runtime may already solve packaging, scaling and operations sufficiently. Containers add value when their portability/runtime model solves a concrete delivery or operational requirement.

# Principal Engineer questions

- What problem does containerization solve here?
- What process/resource isolation do we rely on?
- What state survives replacement?
- What is our image/provenance strategy?
- How are vulnerabilities remediated?
- How do workloads receive identity/secrets?
- How does graceful termination work?
- What metrics prove resource sizing?
- Can engineers reproduce runtime behavior locally?
- Does orchestration complexity now justify Kubernetes, or is simpler compute enough?

# Practical lab

Containerize the observable API used in the CI/CD lab.

Then connect:

```text
commit SHA
 -> container image digest
 -> deployment
 -> container runtime
 -> application telemetry
```

Measure image build/pull/start time, CPU/memory behavior and shutdown. Break the container intentionally before considering orchestration.