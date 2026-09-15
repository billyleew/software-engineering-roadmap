# Disaster Recovery & Chaos Engineering — Recovery Must Be Proven

## Principle

Reliability is not proven by architecture diagrams. Recovery mechanisms must be exercised.

```text
credible failure
 -> business impact
 -> recovery objective
 -> mechanism
 -> runbook/automation
 -> experiment
 -> evidence
 -> improvement
```

# RTO and RPO

**RTO (Recovery Time Objective):** target time to restore acceptable service after disruption.

**RPO (Recovery Point Objective):** maximum acceptable data-loss window expressed in time.

These should come from business requirements, not infrastructure defaults.

A near-zero RPO/RTO can require substantially more complex and expensive architecture.

# Backup vs replication

Replication improves availability and may reduce data loss, but can replicate corruption/deletion.

Backups preserve recoverable historical state, but restore can be slow or fail if never tested.

Use each for the problem it solves.

# Backup design

Consider:
- frequency;
- retention;
- encryption;
- access control;
- immutability/isolation where threat model requires;
- geographic/failure-domain placement;
- consistency/application coordination;
- restoration tooling;
- cost.

# Restore testing

A backup should have evidence that it can restore.

Measure:
- restore duration;
- data completeness/correctness;
- application startup/reconciliation;
- DNS/traffic switching if relevant;
- manual steps;
- missing credentials/configuration;
- operator knowledge.

# Failure domains

Model failures such as:
- process/container;
- node/VM;
- availability zone;
- region;
- database;
- queue/broker;
- object storage access;
- DNS/network;
- identity provider;
- CI/CD/control plane;
- human/operator error;
- data corruption;
- compromised credentials.

Not every system needs protection from every failure at the same level.

# Multi-AZ vs multi-region

Multi-AZ can address infrastructure-zone failures while remaining within one regional system.

Multi-region can support regional disaster recovery, residency and global latency but adds:
- data consistency complexity;
- traffic management;
- replication/failover semantics;
- operational testing;
- cost;
- security/compliance scope.

Do not build active-active multi-region because the architecture diagram looks resilient.

# DR strategies

Conceptual strategies range from:

```text
backup + restore
 -> minimal standby capability
 -> warm standby
 -> active/active
```

Increasing recovery speed generally increases cost and complexity. Match strategy to RTO/RPO and business impact.

# Runbooks

A useful runbook contains:
- trigger/decision criteria;
- prerequisites/access;
- exact high-level recovery sequence;
- safety checks;
- validation;
- rollback/fallback;
- communication/ownership.

Runbooks rot. Exercises reveal stale assumptions.

# Game days

A game day is a planned exercise of operational response/recovery.

Examples:
- restore database from backup;
- fail an application instance/node;
- simulate provider timeout;
- disable a zone in a safe environment;
- rotate/revoke credentials;
- rebuild environment from IaC;
- recover a queue consumer backlog.

# Chaos Engineering

Chaos Engineering is hypothesis-driven experimentation about system behavior under failure.

Good structure:

```text
steady state
 -> hypothesis
 -> failure injection
 -> observe
 -> bound blast radius
 -> stop condition
 -> recovery
 -> learn
```

Example:

> If one checkout instance disappears, customer success rate remains within SLO because healthy instances absorb traffic and readiness removes the failed instance.

Then test it.

# Start small

Maturity progression:
1. local/unit dependency failures;
2. test/staging failure injection;
3. controlled production experiments with tiny blast radius where justified;
4. automated recurring resilience validation for critical assumptions.

Do not begin by randomly terminating production resources.

# Observability prerequisite

Before injecting failure, ensure you can see:
- user/business outcome;
- SLI/SLO;
- application behavior;
- resource/dependency behavior;
- change/experiment event;
- recovery.

If you cannot observe the expected steady state, you cannot reliably evaluate the experiment.

# Failure experiment catalog

## Dependency latency
Increase provider latency. Observe timeouts, concurrency, retries, circuit behavior and customer outcome.

## Dependency unavailable
Observe fail-fast/degradation and retry amplification.

## Lost response after success
Simulate payment/provider success with lost response. Verify idempotency, unknown state and reconciliation.

## Database failover
Observe connection recovery, transaction failures, retry safety and recovery time.

## Queue consumer outage
Observe queue depth/oldest age, autoscaling/recovery and downstream load when consumers return.

## Bad deployment
Introduce controlled latency/error regression and validate canary/alerts/rollback.

## Telemetry degradation
Test what operators can still diagnose if one observability backend is unavailable.

# DR observability

Track:
- backup success/failure;
- backup age;
- restore-test success;
- measured restore duration;
- replication lag;
- failover events;
- recovery milestones;
- reconciliation backlog;
- achieved RTO/RPO during exercises.

"Backup job green" is not equivalent to recoverability.

# Practical capstone

For the study application:
1. define business impact of total DB loss;
2. choose RTO/RPO;
3. implement backup;
4. destroy/recreate a safe test database;
5. restore data;
6. measure recovery;
7. verify application/business correctness;
8. document gaps;
9. inject one dependency failure;
10. write an ADR explaining whether stronger DR architecture is justified.

# Principal Engineer questions

- Which disasters are credible enough to design for?
- What does the business require for RTO/RPO?
- Has recovery been tested end-to-end?
- Does replication protect against this failure or copy it?
- Who can trigger failover?
- What data needs reconciliation afterward?
- Which manual steps dominate RTO?
- What does stronger DR cost?
- Is multi-region actually necessary?
- Which architecture assumption should our next failure experiment challenge?