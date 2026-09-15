# CI/CD & Software Delivery — From Commit to Evidence

## Objective

CI/CD is not a YAML file and not a particular vendor. It is a feedback and delivery system that moves a change from source code to production safely, repeatedly and measurably.

```text
Idea
 -> Code
 -> Commit
 -> Build
 -> Test
 -> Security / quality checks
 -> Artifact
 -> Deploy
 -> Verify
 -> Observe
 -> Learn
```

The loop does not end at deployment. Production evidence is part of delivery.

# Continuous Integration

Continuous Integration means integrating small changes frequently into a shared codebase with automated feedback that detects integration problems quickly.

Important characteristics:
- small batches;
- frequent integration;
- reproducible builds;
- fast automated feedback;
- main/trunk remains releasable or quickly recoverable;
- failures are visible and repaired quickly.

A pipeline that runs once a week on long-lived branches is automation, but not strong continuous integration.

# Continuous Delivery vs Continuous Deployment

**Continuous Delivery:** every successful change is kept in a deployable state; production release may require an explicit business/human decision.

**Continuous Deployment:** every change satisfying automated policy is automatically released to production.

Neither is universally superior. Regulatory, risk, product and organizational constraints determine the appropriate release control.

# Pipeline as a feedback system

The purpose of pipeline stages is to answer useful questions as early and cheaply as possible.

```text
Fast / cheap feedback
  lint / static checks
  unit tests
        ↓
component / integration tests
        ↓
contract / security checks
        ↓
build immutable artifact
        ↓
deploy to appropriate environment
        ↓
post-deployment verification
        ↓
production telemetry
```

Do not create stages because a reference pipeline contains them. Each gate must protect a meaningful risk.

# Build once, promote the same artifact

Prefer:

```text
commit
 -> build artifact A
 -> test artifact A
 -> stage artifact A
 -> production artifact A
```

rather than rebuilding different binaries for every environment.

This improves provenance and reduces environment-specific build drift.

# Artifacts

Artifacts should be:
- immutable;
- uniquely versioned;
- traceable to source revision;
- reproducible where practical;
- stored in a controlled registry/repository;
- accompanied by useful provenance/metadata.

Useful identity chain:

```text
commit SHA
 -> pipeline run
 -> artifact digest/version
 -> deployment
 -> runtime version
 -> telemetry
```

This chain is essential for delivery observability.

# Pipeline observability

A pipeline is itself a production system for engineers. Observe it.

## Core pipeline metrics

Measure at minimum:
- pipeline success/failure rate;
- pipeline duration and percentiles;
- queue/wait time;
- stage duration;
- flaky test rate;
- retry/rerun frequency;
- artifact build time;
- deployment duration;
- rollback/roll-forward frequency;
- failure reason/category.

Then connect to delivery outcomes:
- lead time for changes;
- deployment frequency;
- change failure rate;
- recovery time;
- time from commit to production.

Do not optimize a pipeline solely to make a dashboard green. Connect metrics to developer and business outcomes.

# Deployment observability

Every deployment should create an observable change event containing enough identity to correlate production behavior.

Useful dimensions:

```text
deployment_id
service/application
environment
version / artifact digest
commit SHA
pipeline run
start/end time
strategy
result
rollback status
```

Dashboards and traces/logs should make it possible to ask:

> Did latency/errors/business conversion change after version X was deployed?

# Logs for delivery systems

Pipeline/deployment logs should be structured enough to diagnose failures without exposing secrets.

Never print:
- credentials;
- access tokens;
- private keys;
- sensitive environment values.

Log meaningful transitions and failure reasons rather than excessive shell noise.

# Tracing the delivery path

At larger platform scale, think of software delivery as a distributed workflow:

```text
Git provider
 -> CI orchestrator
 -> build workers
 -> artifact registry
 -> security scanners
 -> deployment controller
 -> cloud/orchestrator
 -> verification system
```

Correlation identifiers and workflow/run IDs make cross-system debugging easier. Full distributed tracing is useful only when complexity justifies it.

# DORA-style outcome metrics

Delivery metrics should help understand the engineering system rather than rank individuals.

Useful outcomes include:
- deployment frequency;
- lead time for changes;
- change failure rate;
- time to restore/recover.

Avoid weaponizing metrics. If engineers are individually judged by deployment counts, they will optimize the measurement rather than the system.

# Pipeline reliability

Ask the same questions as for customer-facing systems:
- What happens if a build worker dies?
- What happens if the artifact registry is unavailable?
- Can a pipeline safely retry?
- Can duplicate deployment commands occur?
- Is deployment idempotent?
- What happens when deployment succeeds but CI loses the response?
- How is partial rollout detected?
- How do we recover the delivery system itself?

# Pipeline performance

A 45-minute feedback loop changes developer behavior.

Before adding more compute, identify where time is spent:

```text
queue time
checkout
dependency installation
compile/build
tests
container build
security scans
artifact upload
deployment
verification
```

Then optimize the measured bottleneck through techniques such as caching, test parallelization, incremental builds or worker capacity.

Caching every stage by default can introduce stale/correctness problems. Treat build caches as another architecture trade-off.

# Branching and integration

Prefer short-lived changes and frequent integration where possible.

Long-lived branches increase:
- merge complexity;
- integration uncertainty;
- delayed feedback;
- batch size;
- release risk.

Branching strategy must fit product/release constraints. Trunk-based development is powerful but not a ritual.

# Environment strategy

Avoid treating environments as manually maintained pets.

Seek reproducibility across:
- infrastructure;
- configuration;
- application artifact;
- database/schema expectations;
- observability.

Perfect environment parity is often expensive or impossible. Make meaningful differences explicit and test the risks they create.

# Database changes in delivery

Application rollback is easy compared with incompatible data rollback.

Prefer compatible evolution:

```text
expand
 -> deploy compatible application
 -> migrate/backfill
 -> switch behavior
 -> verify
 -> contract
```

Database migrations are part of deployment design, not a separate afterthought.

# Security in CI/CD

Treat the pipeline as a high-value supply-chain system.

Protect:
- repository permissions;
- runner identity;
- secrets;
- artifacts;
- registries;
- deployment credentials;
- third-party actions/plugins;
- provenance.

Prefer short-lived workload identity over long-lived cloud credentials where supported.

Add security gates according to actual risk. A scanner that generates thousands of ignored findings creates theater, not security.

# Failure taxonomy

Classify delivery failures to improve the system:

```text
source / merge
build
unit test
integration test
flaky test
security/policy
artifact/registry
infrastructure
configuration
migration
deployment
health verification
runtime regression
external dependency
```

Without categories, "pipeline failed" is too weak for improvement.

# Start-simple maturity model

## Level 1 — Small product/team

```text
push / PR
 -> lint
 -> unit tests
 -> build
 -> deploy managed runtime
 -> smoke/health check
 -> basic logs + RED/business metrics
```

## Level 2 — Growing production system

Add when justified:
- integration/contract tests;
- artifact registry;
- IaC;
- automated migrations;
- environment promotion;
- security/dependency scanning;
- deployment annotations;
- automated rollback/roll-forward support;
- delivery dashboards.

## Level 3 — Multiple teams / higher risk

Potentially add:
- reusable pipeline components;
- golden paths;
- ephemeral test environments;
- progressive delivery;
- policy as code;
- signed/provenance-aware artifacts;
- platform-level telemetry;
- SLO-aware release verification.

Do not jump to Level 3 because another organization publishes its pipeline architecture.

# Practical lab

Take one small web API and implement an observable delivery path.

Iteration 1:
- build/test on every change;
- create one immutable artifact;
- deploy it;
- expose application version/commit safely;
- add structured application logs and basic RED/business metrics.

Iteration 2:
- record pipeline duration and stage timings;
- record deployment events;
- correlate runtime version with telemetry;
- deliberately break a test/build/deployment and diagnose it.

Iteration 3:
- introduce a slow pipeline stage;
- measure before optimizing;
- improve only the measured bottleneck;
- compare before/after.

Iteration 4:
- deploy a version that increases error rate;
- detect the regression from telemetry;
- rollback or roll forward;
- calculate detection and recovery time.

The lab succeeds when you can explain the complete path from commit to production outcome and diagnose where/why it failed.