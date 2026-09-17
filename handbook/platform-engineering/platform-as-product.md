# Platform as a Product — Internal Developer Platforms That Reduce Cognitive Load

## Objective

An Internal Developer Platform (IDP) is a set of capabilities, interfaces and paved roads that enables product teams to deliver and operate software with less repeated infrastructure work and lower cognitive load.

The platform is not Kubernetes, Backstage, Terraform or a portal. Those may be implementation components.

```text
Developer problem
 -> developer journey
 -> reusable capability
 -> safe abstraction
 -> self-service interface
 -> paved road
 -> adoption
 -> measured outcome
 -> feedback
 -> evolution
```

# Platform customers

Treat engineers and engineering teams as customers without forgetting that the ultimate purpose is better product/business delivery.

Discover pain through:
- interviews;
- workflow observation;
- support requests;
- incident/postmortem evidence;
- onboarding friction;
- CI/CD telemetry;
- security/reliability gaps;
- duplicated infrastructure work.

Do not build a platform roadmap solely from the platform team's preferred technologies.

# Developer journeys

Map complete jobs such as:
- create a new service;
- deploy a change;
- create a database/queue;
- obtain workload identity;
- add secrets/configuration;
- expose an API;
- add telemetry;
- define SLO/alerts;
- troubleshoot production;
- perform rollback;
- decommission a service.

Measure steps, waiting, handoffs, errors and required specialist knowledge.

# Paved roads / golden paths

A paved road is an easy, supported path for common workloads.

A good paved road:
- encodes secure/reliable defaults;
- is discoverable;
- provides self-service;
- has useful documentation/examples;
- is observable;
- has ownership/support;
- permits justified escape hatches.

It should make the right thing easier, not merely make alternatives forbidden.

# Abstraction design

Hide complexity that most consumers should not need, while preserving important choices.

Example platform contract:

```yaml
service:
  runtime: java
  exposure: internal
  database: postgres
  observability: standard
  slo_tier: critical
```

The platform may translate that intent into pipelines, IaC, runtime configuration, identity, telemetry and policy.

Do not expose every raw cloud/Kubernetes option through a giant YAML schema. That is infrastructure complexity with another syntax.

# Self-service

Self-service means a team can perform common operations safely without waiting for another team to manually execute tickets.

Possible interfaces:
- CLI;
- API;
- Git workflow;
- templates;
- developer portal;
- IDE integration.

A portal is not required for platform engineering. Build one when discovery, catalog, workflows and visibility justify it.

# Service catalog

At organizational scale a catalog can answer:
- who owns this service?
- repository?
- runtime/environment?
- dependencies?
- documentation?
- SLO?
- dashboards/runbooks?
- security classification?
- lifecycle status?

Catalog metadata must be trustworthy and preferably derived/validated automatically where possible.

# Platform APIs

Think in capabilities rather than infrastructure resources.

```text
Product team asks for:
"durable relational storage for service X"

rather than necessarily:
"create these 47 provider-specific resources"
```

The abstraction should remain escapable when workloads genuinely require provider-specific capabilities.

# Platform SLOs

The platform itself is a production system for engineers.

Possible SLIs:
- deployment orchestration availability;
- environment provisioning success;
- CI queue time;
- paved-road deployment duration;
- artifact registry availability;
- developer portal/API availability.

Separate platform-caused failures from application failures.

# Adoption

Adoption is stronger evidence than mandate.

Track:
- percentage of eligible teams using paved roads;
- repeated escape-hatch reasons;
- time to first production deploy;
- support volume;
- workflow success;
- upgrade/version adoption;
- satisfaction/qualitative feedback.

If teams consistently bypass the platform, investigate the product rather than blaming the users.

# Platform team boundaries

Platform teams should own reusable capabilities, not absorb every product team's operational responsibility.

A healthy model:

```text
Platform owns paved-road capabilities + platform reliability
Product team owns its service/product behavior + business reliability
Shared standards define the interface
```

# Build vs buy

Evaluate managed/commercial/open-source/internal solutions through:
- requirements;
- integration effort;
- operational burden;
- security/compliance;
- customization;
- lock-in/exit cost;
- staffing;
- total cost;
- strategic differentiation.

Building a platform component internally is not automatically more sophisticated.

# Anti-patterns

## Platform by mandate
"All teams must use this" before proving usefulness.

## Ticket-driven platform
A central team manually performs every operation behind a portal.

## Kubernetes exposure
Every developer must understand cluster internals for normal application delivery.

## Abstraction cliff
Simple path works until one option changes, then consumers must understand the entire underlying stack.

## Platform as project
Large one-time launch without continuous product discovery/feedback.

## Too many golden paths
Every team gets a unique template, eliminating standardization value.

# Practical lab

Turn the observable application path into a small paved road.

Consumer input should describe intent. Platform automation should provide:
- repository/pipeline template;
- artifact build;
- IaC/runtime;
- workload identity/secrets integration;
- deployment;
- logs/metrics/deployment annotations;
- health checks;
- rollback path;
- ownership metadata.

Then onboard a second intentionally different service and record where the abstraction fails.

# Principal Engineer questions

- Who is the platform customer?
- Which developer journey are we improving?
- What is the current baseline?
- Which complexity should be hidden and which must remain visible?
- What is the escape hatch?
- How is platform adoption measured?
- What is the platform SLO?
- Which responsibilities remain with product teams?
- What is cheaper/better to buy?
- What capability should we deliberately not build?
- How will we deprecate platform APIs safely?