# Kubernetes — Orchestration as a Trade-off, Not a Destination

## Objective

Kubernetes provides a declarative control plane for scheduling and operating containerized workloads across compute resources.

Learn it deeply enough to use and operate it—but also deeply enough to know when **not** to use it.

# The problem Kubernetes addresses

At sufficient scale/complexity an organization may repeatedly need:
- workload scheduling;
- desired-state reconciliation;
- service discovery;
- rolling updates;
- health-based replacement;
- horizontal scaling;
- configuration/secrets integration;
- workload resource isolation;
- extensible operational APIs;
- consistent runtime primitives across many workloads/teams.

Kubernetes packages these into a common platform model.

If a managed runtime already solves the actual requirements for a small team, Kubernetes may simply move infrastructure work back into the organization.

# Reconciliation mental model

Kubernetes is fundamentally controller-driven.

```text
Desired state
     ↓
API server / stored state
     ↓
controllers observe
     ↓
actual state differs?
     ↓
act toward desired state
     ↓
observe again
```

This reconciliation model is more important than memorizing commands.

# Core objects

Understand conceptually:
- Pod — schedulable workload unit;
- Deployment — desired replica/update management for stateless-style workloads;
- Service — stable service discovery/network endpoint abstraction;
- ConfigMap/Secret — configuration inputs (with security caveats);
- StatefulSet — identity/order/storage-oriented workload management;
- Job/CronJob — finite/scheduled work;
- Ingress/Gateway ecosystem — inbound traffic routing depending on platform;
- Namespace — logical scoping, not a complete security boundary by itself.

# Scheduler and resources

The scheduler places workloads based on declared requirements and cluster state.

Requests communicate expected resource needs for scheduling; limits constrain usage depending on resource/runtime behavior.

Bad sizing can cause:
- poor bin packing;
- CPU throttling;
- OOM kills;
- wasted capacity;
- unstable autoscaling;
- noisy-neighbor behavior.

Use workload evidence/load tests, not arbitrary templates.

# Probes

- readiness: should this workload receive traffic?
- liveness: should it be restarted?
- startup: should slower initialization be allowed before other probes apply?

Bad probes create outages. If liveness fails whenever the database is unavailable, Kubernetes may restart every application instance during a dependency outage.

# Networking

Understand the request path rather than treating cluster networking as magic:

```text
external client
 -> cloud/edge LB
 -> ingress/gateway
 -> service
 -> pod/workload
 -> downstream service/database
```

Study DNS, service discovery, network policies, load balancing, connection behavior and TLS boundaries.

# Storage and state

Kubernetes can orchestrate stateful workloads, but orchestration does not remove distributed data-system complexity.

For databases ask whether a managed database provides better reliability/operational economics than running it yourself in Kubernetes.

# Deployments and rollout

Kubernetes supports rolling updates, but safe delivery still requires:
- compatible versions;
- readiness correctness;
- database/schema strategy;
- telemetry;
- verification;
- recovery.

A Deployment object does not create a complete release strategy.

# Autoscaling

Possible layers:
- workload/pod scaling;
- node/compute scaling;
- event/queue-driven scaling through additional systems;
- vertical recommendations/adjustment depending on approach.

Avoid CPU-only thinking. Queue age/concurrency/business workload may be better signals.

Always model downstream capacity.

# Kubernetes observability

Observe at multiple levels:

```text
Business outcomes
        ↓
Application RED / domain metrics
        ↓
Pod/container
        ↓
Workload/controller
        ↓
Node
        ↓
Cluster/control plane
        ↓
Cloud dependencies
```

Useful signals:
- desired vs available replicas;
- restart/OOM counts;
- pending/unschedulable workloads;
- CPU/memory usage and throttling;
- node pressure/capacity;
- rollout failures;
- autoscaler behavior;
- API/control-plane latency/errors where relevant;
- DNS/network errors;
- storage failures;
- application and business metrics.

Do not stop at `kubectl get pods`.

# Debugging path

When a request fails:

```text
business symptom
 -> application telemetry
 -> deployed version/change
 -> workload readiness/restarts
 -> service/network/DNS
 -> node/resources
 -> dependency/cloud service
```

Start from customer impact and narrow the failure boundary.

# Security

Study:
- RBAC/least privilege;
- workload identity;
- admission/policy;
- secrets integration;
- network policy;
- image provenance/scanning;
- pod/container security controls;
- control-plane access;
- audit logs;
- tenant isolation limitations;
- supply chain.

A cluster administrator credential is a powerful production credential.

# Cluster/platform upgrades

Kubernetes creates a lifecycle obligation:
- version upgrades;
- API deprecations;
- node/runtime upgrades;
- CNI/network components;
- ingress/gateway components;
- autoscaling components;
- observability stack;
- operators/controllers;
- security patches.

Count this in total cost of ownership.

# Operators and CRDs

Kubernetes can be extended through custom resources/controllers.

This is powerful because platform capabilities can use the same declarative/reconciliation model. It is dangerous because every operator adds code, privileges, failure modes, upgrades and expertise requirements.

Do not turn Kubernetes into a distributed application framework for every business concept.

# Service mesh caution

A service mesh can centralize capabilities such as traffic policy, mTLS and telemetry, but also adds another distributed control/data plane.

Do not adopt one automatically because the system uses microservices or Kubernetes. Identify the concrete cross-service requirements first.

# When Kubernetes may be justified

Signals can include:
- many containerized workloads/teams;
- repeated orchestration requirements;
- need for consistent platform primitives;
- complex scheduling/resource needs;
- strong internal platform investment;
- portability/control requirements that outweigh managed-platform simplicity;
- ecosystem capabilities providing real value.

# When simpler compute may win

For a small team with a handful of standard APIs/workers, a managed container/application platform can reduce:
- control-plane responsibility;
- upgrades;
- networking complexity;
- security surface;
- observability/platform maintenance;
- on-call cognitive load.

# Decision ADR exercise

Compare:

```text
Option A: managed application/container runtime
Option B: managed Kubernetes
```

Evaluate:
- workload count/types;
- team/platform expertise;
- deployment needs;
- autoscaling;
- networking;
- isolation/security;
- observability;
- reliability;
- portability;
- operational burden;
- total cost;
- future option value.

Do not give Kubernetes points simply because it can do more things.

# Practical lab

Only after the container/cloud labs:

1. deploy the same API to Kubernetes;
2. configure requests/limits from measured behavior;
3. implement readiness/liveness/startup correctly;
4. expose service traffic;
5. connect runtime version to logs/metrics/traces;
6. perform rolling deployment;
7. inject bad readiness;
8. trigger CPU/memory pressure;
9. kill pods/nodes where safe;
10. observe reconciliation and customer impact;
11. configure horizontal scaling from a meaningful signal;
12. compare operational work against the simpler managed runtime.

The final question is not "Can I deploy to Kubernetes?"

It is:

> Did Kubernetes solve enough real orchestration/platform problems to justify the complexity we just experienced?