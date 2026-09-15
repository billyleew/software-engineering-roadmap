# Infrastructure as Code — Make Infrastructure Reproducible and Reviewable

## Objective

Infrastructure as Code (IaC) expresses infrastructure configuration in versioned definitions so changes can be reviewed, automated, reproduced and audited.

IaC is not valuable because infrastructure becomes text. Its value comes from controlled change.

```text
Desired infrastructure
 -> review
 -> plan/diff
 -> policy/security checks
 -> apply
 -> verify
 -> observe
 -> detect drift
```

# Declarative vs imperative

Declarative systems describe desired state and rely on an engine/controller to determine changes. Imperative systems describe actions.

Neither model eliminates operational reasoning. Understand ordering, dependencies, failure and reconciliation semantics of the chosen tool.

# State

Many IaC tools need state describing known managed resources.

State is operationally important:
- protect it;
- control concurrent changes/locking;
- back it up where appropriate;
- avoid sensitive outputs;
- understand recovery/import/move workflows;
- know what happens when reality diverges from state.

# Plan before apply

A plan/diff should answer:
- what will be created?
- changed?
- destroyed/replaced?
- what is unexpectedly different?
- what is high risk?

Human review is useful only if the plan is understandable. A 10,000-line unread plan is not meaningful governance.

# Modules and abstraction

Reuse repeated infrastructure patterns, but avoid premature abstraction.

A good module:
- encodes a stable organizational capability;
- provides safe defaults;
- exposes meaningful choices;
- hides irrelevant provider complexity;
- is versioned/tested/documented.

A bad module exposes dozens of raw provider options and merely moves complexity to another file.

# Drift

Drift occurs when real infrastructure no longer matches the declared/known state.

Causes:
- manual console changes;
- emergency fixes;
- external controllers;
- failed partial operations;
- provider behavior;
- unmanaged resources.

Observe drift rather than assuming Git is reality.

# IaC pipeline

A useful flow:

```text
change
 -> format/static validation
 -> security/policy checks
 -> plan
 -> review/approval proportional to risk
 -> apply
 -> verification
 -> infrastructure/deployment event
 -> runtime observation
```

Do not require the same approval ceremony for every environment/resource. Controls should be risk-based.

# Infrastructure observability

Observe both the **IaC delivery system** and the resulting infrastructure.

IaC delivery signals:
- plan duration;
- apply duration;
- failure rate/category;
- queue/lock wait;
- drift detections;
- manual interventions;
- rollback/recovery actions;
- resource changes/destructions.

Runtime signals depend on resource type:
- compute saturation;
- network errors/latency;
- database connections/latency/storage;
- queue depth/age;
- load balancer errors;
- storage capacity/latency;
- cloud-provider quota/throttling.

Correlate infrastructure changes with runtime behavior.

# Failure modes

Ask:
- apply succeeds partially then fails—what state remains?
- process loses connection after provider accepted operation—how is result reconciled?
- two pipelines change same state concurrently?
- resource replacement destroys data?
- provider API throttles?
- credentials expire mid-run?
- state backend unavailable?
- module upgrade changes behavior unexpectedly?

IaC is a distributed system interacting with remote control planes. Partial failure is normal.

# Secrets

Do not treat an IaC state file as a safe secret store merely because the repository does not contain the value.

Prefer dedicated secret management and workload identity. Mark sensitive outputs, restrict state access and understand whether providers persist secret values into state.

# Policy as Code

Useful when an organization repeatedly needs enforceable constraints such as:
- encryption required;
- public access prohibited;
- approved regions;
- mandatory ownership/cost metadata;
- restricted instance families;
- backup requirements.

Policy should prevent meaningful risk without turning the platform into an obstacle course. Measure denied changes and developer friction.

# Testing

Layers can include:
- syntax/static validation;
- module unit-like tests where supported;
- policy/security checks;
- plan assertions;
- ephemeral integration tests;
- post-apply verification;
- resilience/recovery exercises.

# Environment strategy

Avoid copy/paste infrastructure per environment where shared modules can express stable commonality. But do not force environments to be identical when production requirements legitimately differ.

Make differences explicit.

# GitOps distinction

IaC and GitOps are related but not identical.

IaC describes/provisions infrastructure. GitOps commonly uses Git as the desired-state source for continuously reconciled operational resources.

Do not adopt GitOps merely to avoid running an apply command. Ask whether continuous reconciliation, auditability, environment promotion and operating model justify it.

# Cost and FinOps

Infrastructure code is also a cost-producing program.

A change may be technically valid while economically harmful.

Review:
- estimated recurring cost;
- data transfer;
- storage growth;
- idle capacity;
- redundancy;
- observability cost;
- managed service premium;
- licensing.

Where possible annotate changes with cost estimates or at least make material cost changes reviewable.

# Practical lab

Provision the runtime for the CI/CD API using IaC.

Iteration 1:
- network/runtime/database as appropriate;
- remote/protected state if the tool needs it;
- plan in CI;
- apply through controlled workflow;
- tag/label resources with ownership/environment.

Iteration 2:
- manually introduce safe drift;
- detect it;
- decide whether code or infrastructure is authoritative;
- reconcile.

Iteration 3:
- make a change requiring resource replacement;
- identify blast radius before apply;
- verify after apply;
- correlate infrastructure change with telemetry.

Iteration 4:
- introduce a policy preventing one meaningful insecure configuration;
- measure whether the developer error message makes remediation obvious.

# Principal Engineer questions

- What infrastructure should IaC own?
- Where is state and how is it recovered?
- Who may apply changes?
- How do we prevent concurrent conflicting operations?
- How do we detect drift?
- Which changes require stronger review?
- What is our module/version strategy?
- How do we test modules?
- What secrets enter state?
- How are infrastructure changes correlated with incidents?
- What does each change cost?
- What escape hatch exists during incidents, and how is emergency drift reconciled afterward?