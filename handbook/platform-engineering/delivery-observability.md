# Software Delivery Observability — Observe the Engineering System

## Principle

Observability should cover not only the application runtime but the complete path by which software becomes production.

```text
Developer
 -> source control
 -> CI
 -> artifact
 -> security/policy
 -> deployment
 -> runtime
 -> customer/business outcome
```

If delivery is slow or unreliable, treat it as a system to investigate with evidence.

# Three observability domains

## 1. Delivery flow

Understand how changes move.

Signals:
- commit-to-build wait;
- build duration;
- test duration;
- pipeline queue time;
- artifact publication;
- approval wait time;
- deployment duration;
- commit-to-production lead time.

## 2. Delivery reliability

Understand how often and why delivery fails.

Signals:
- pipeline failure rate;
- flaky tests;
- deployment failures;
- rollback/roll-forward rate;
- migration failures;
- environment/configuration failures;
- infrastructure/provisioning failures;
- recovery time.

## 3. Change impact

Understand what deployed software did to the product.

Signals:
- error-rate delta;
- latency delta;
- saturation delta;
- SLO/error-budget impact;
- business KPI delta;
- incident/change correlation.

# Correlation model

Aim to connect:

```text
work item / change
 -> commit SHA
 -> pull request
 -> CI run
 -> artifact digest
 -> deployment ID
 -> runtime version
 -> trace/log/metric
 -> customer/business result
```

Not every organization needs a giant database connecting all of these on day one. Start by preserving stable identifiers and metadata so correlation can grow naturally.

# Metrics

Useful delivery metrics include:

```text
pipeline_duration_seconds{pipeline,stage}
pipeline_runs_total{pipeline,result}
deployment_total{service,environment,result}
deployment_duration_seconds{service,environment}
rollback_total{service,reason}
flaky_test_total{suite,test?}
```

Be careful with cardinality. Commit SHA, deployment ID and test names can be poor metric labels at scale; use logs/traces/events for highly unique values and metrics for aggregation.

# Logs

Delivery logs answer detailed questions:
- which command/tool failed?
- which dependency could not be downloaded?
- which migration failed?
- why did verification reject the release?

Prefer structured metadata and explicit failure categories.

Redact secrets aggressively because delivery systems often have privileged credentials.

# Traces

For sophisticated internal platforms, tracing can expose latency across CI orchestration, workers, registries, deployment controllers and cloud APIs.

Do not add tracing merely because OpenTelemetry exists. First ask whether pipeline metrics/logs cannot identify the delay or failure boundary.

# Events

Deployment events are particularly valuable. Record changes as first-class events and overlay them on runtime/business dashboards.

Example:

```text
14:02 deploy checkout v2.14.0 begins
14:05 10% canary
14:07 p99 +35%
14:08 payment completion -4%
14:09 promotion halted
14:11 rollback complete
14:14 metrics recover
```

This is far more useful than separately knowing that "a deploy happened" and "latency increased."

# Delivery SLOs

Not every pipeline needs formal SLOs. At platform scale, internal reliability objectives can be useful.

Examples:
- 99.9% of CI orchestration requests accepted successfully;
- 95% of standard builds begin within 2 minutes;
- 95% of paved-road deployments complete within 10 minutes excluding intentional approvals;
- platform-caused deployment failure below agreed threshold.

Separate platform-caused failures from application/test failures when evaluating platform reliability.

# Developer experience and telemetry

Quantitative signals alone are insufficient.

Combine:

```text
Telemetry
+ developer feedback
+ workflow observation
+ incident/postmortem evidence
```

A fast pipeline can still be painful if errors are incomprehensible or local reproduction is impossible.

# Anti-pattern: dashboard-driven theater

Do not create dozens of dashboards that nobody uses.

Every dashboard should support a decision or investigation.

Examples:
- Is delivery getting slower?
- Which stage causes most waiting?
- Why do deployments fail?
- Which services have the highest change failure rate?
- Did a release cause this incident?
- Is the paved road improving developer outcomes?

# Anti-pattern: measuring individuals

Delivery telemetry is for improving the socio-technical system, not creating simplistic developer rankings.

Metrics can be gamed and often represent team/system constraints more than individual performance.

# Observability maturity

## Start
- pipeline result/duration;
- deployment result/duration;
- runtime version metadata;
- deployment annotations;
- application RED/business metrics.

## Grow
- stage/queue timings;
- failure taxonomy;
- DORA-style outcomes;
- change/incident correlation;
- developer feedback;
- cost per build/deployment.

## Platform scale
- standardized telemetry across teams;
- internal platform SLOs;
- cross-system correlation;
- automated release analysis;
- telemetry cost/cardinality governance;
- platform product analytics.

# Practical investigation

Scenario:

Developers report: "CI is slow. We need larger runners."

Do not resize runners immediately.

Collect:

```text
Total p95 pipeline: 24 min
Queue: 45 sec
Dependency restore: 2 min
Compile: 3 min
Unit tests: 4 min
Integration tests: 13 min
Image build/push: 1 min
```

Now investigate the 13-minute integration stage: parallelism, duplicated setup, external dependencies, test architecture and flakiness.

The same evidence-first reasoning used for production architecture applies to the engineering platform.