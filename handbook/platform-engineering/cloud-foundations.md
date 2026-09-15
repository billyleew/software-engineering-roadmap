# Cloud Foundations — Learn Capabilities Before Product Names

## Objective

Cloud architecture is the composition of compute, network, identity, storage, data, messaging and operational capabilities under availability, security, performance and cost constraints.

Learn the durable concepts first; then map them to AWS, Azure, GCP or another provider.

# Shared responsibility

Managed services transfer some operational responsibility to the provider, not all responsibility.

For every service ask:
- what does the provider operate?
- what do we configure?
- what data/security/recovery responsibilities remain ours?
- what telemetry is exposed?
- what failure modes are outside our control?

# Regions and availability zones

A region is a geographic deployment area; availability zones are isolated infrastructure locations within a region (exact provider semantics vary).

Multi-AZ is often a reasonable availability mechanism for important production systems. Multi-region is much more expensive/complex and should follow business requirements such as disaster recovery, latency, residency or extreme availability.

Never equate "global product" automatically with active-active multi-region architecture.

# Identity first

Cloud security starts with identity and authorization.

Prefer:
- least privilege;
- workload/service identity;
- short-lived credentials;
- explicit trust relationships;
- separation of human and machine identity;
- centralized audit logs;
- controlled break-glass access.

Long-lived access keys embedded in CI or applications are a liability.

# Networking

Understand:
- address spaces/subnets;
- routing;
- public vs private exposure;
- NAT/egress;
- DNS;
- load balancing;
- firewalls/security groups/policies;
- TLS;
- private connectivity;
- network boundaries between environments/accounts/projects.

Debug from packet/request path rather than guessing.

```text
DNS
 -> edge/load balancer
 -> network policy/firewall
 -> routing
 -> runtime/service
 -> application
 -> dependency
```

# Compute models

## Virtual machines

High control and broad compatibility; more OS/runtime responsibility.

## Managed container compute

Container model without necessarily operating a full orchestrator control plane.

## Kubernetes

Powerful orchestration and platform API, with meaningful operational/cognitive complexity.

## Functions/serverless

Useful for event-driven/spiky/short-lived workloads and reduced infrastructure management; trade-offs include runtime constraints, latency characteristics, observability, concurrency semantics and provider coupling.

## Managed application platforms

Often an excellent simple default for small teams/products.

Decision should follow workload characteristics, not ideology.

# Storage

Understand distinct models:
- object storage;
- block storage;
- file storage;
- ephemeral/local storage.

Ask about durability, access patterns, latency, throughput, consistency semantics, lifecycle/retention, backup, encryption and cost.

# Databases

Managed relational databases are often strong defaults for transactional applications.

Cloud availability does not remove data architecture questions:
- transaction boundaries;
- indexes;
- query behavior;
- connection management;
- replication lag;
- backup/restore;
- RPO/RTO;
- schema migration;
- scaling limits.

Do not choose a cloud NoSQL service because it advertises massive scale when the application needs relational invariants at modest scale.

# Messaging

Cloud queues/pub-sub/event systems can reduce operational burden compared with self-hosting brokers.

Still understand:
- delivery semantics;
- visibility/acknowledgment;
- retries;
- DLQ;
- ordering scope;
- duplicate handling;
- retention;
- throughput quotas;
- consumer scaling;
- observability.

Managed does not mean semantics disappear.

# Autoscaling

Autoscaling responds to signals; it does not fix inefficient architecture.

Potential signals:
- CPU;
- memory;
- request concurrency;
- RPS;
- queue depth/oldest age;
- custom business workload.

Ask whether the resource can scale fast enough and whether dependencies (especially databases) can absorb increased concurrency.

Example anti-pattern:

```text
latency rises
 -> autoscale app 10x
 -> DB connections 10x
 -> database collapses
```

Observe the complete dependency chain.

# Cloud observability

Correlate four layers:

```text
Business
  payments/orders/signups
Application
  rate/errors/latency
Platform/runtime
  instances/tasks/pods/resources
Cloud dependencies
  DB/queue/storage/LB/network/provider APIs
```

Also record cloud/infrastructure changes as events.

# Quotas and throttling

Cloud control/data planes have quotas. Include them in capacity and failure analysis.

Observe:
- throttled requests;
- quota utilization;
- API errors;
- exhausted addresses/connections/resources;
- account-level limits.

# Resilience

Cloud primitives do not automatically make an application resilient.

Test:
- instance/process failure;
- zone impairment where feasible;
- database failover;
- dependency timeout;
- queue backlog;
- credential/identity failure;
- DNS/network issues;
- provider API throttling;
- restore from backup.

# Backup and disaster recovery

Backup is not recovery.

Define:
- RPO: acceptable data loss window;
- RTO: acceptable recovery time.

Then test restore/recovery. A backup never restored is an assumption.

# FinOps

Cloud makes spending programmable and easy to hide.

Track:
- compute;
- managed database;
- storage;
- network egress;
- load balancers/NAT;
- messaging;
- observability/log ingestion;
- backups/snapshots;
- idle environments;
- third-party services.

Prefer unit economics where possible:

```text
cost / order
cost / active customer
cost / API request
cost / GB processed
```

A cheaper service that requires significant operational staffing may have higher total cost.

# Account/project/environment boundaries

Use boundaries to manage blast radius, ownership, billing and permissions. The exact hierarchy is provider-specific.

Avoid putting every environment/team into one unrestricted security boundary merely because it is simpler initially.

# AWS mapping exercise

After understanding concepts, map them to AWS examples without treating these as universal answers:

```text
object storage       -> S3
VM compute           -> EC2
managed containers   -> ECS/Fargate
orchestration        -> EKS
functions            -> Lambda
relational DB        -> RDS/Aurora
queue                -> SQS
pub/sub               -> SNS/EventBridge (different semantics)
metrics/logs          -> CloudWatch
identity             -> IAM
DNS                   -> Route 53
CDN                   -> CloudFront
```

Then compare equivalent capabilities in another provider to prove you learned the abstraction rather than only the product vocabulary.

# Practical architecture exercise

Host the observable API from previous labs.

Pass 1:
- one region;
- simple managed runtime;
- managed relational DB;
- load balancing only if needed;
- backups;
- least-privilege workload identity;
- logs/metrics/business telemetry;
- IaC and CI/CD.

Pass 2: introduce measured load and a credible availability target. Decide whether to add horizontal compute scaling and multi-AZ data/runtime capability.

Pass 3: introduce one new requirement—large asynchronous jobs, geographic latency, stricter RTO/RPO or major traffic growth. Evolve only what that requirement forces.

For every new cloud component write:
- requirement;
- evidence/constraint;
- alternatives;
- cost;
- failure modes;
- telemetry;
- rollback/exit strategy.

# Principal Engineer questions

- Which responsibilities are we buying from the provider?
- What is still ours?
- What is the simplest compute model that fits?
- Which failure domains matter to the business?
- What is the data recovery plan and has it been tested?
- What quotas become architectural constraints?
- How does autoscaling affect downstream dependencies?
- What is our identity model?
- Can we correlate cloud changes with customer impact?
- What are our unit economics?
- What would justify multi-region?
- What would justify Kubernetes instead of simpler managed compute?