# Incident Management & Postmortems — Restore, Learn, Improve

## Incident priorities

During an active incident:

```text
Protect people/data/correctness
 -> understand user impact
 -> contain blast radius
 -> mitigate/restore service
 -> communicate
 -> validate recovery
 -> investigate deeply afterward
```

Do not delay an available safe mitigation because the team wants the perfect root cause first.

# Severity

Define severity from impact rather than technical drama.

Possible dimensions:
- number/importance of users affected;
- revenue/business process impact;
- data integrity/security;
- geographic scope;
- duration;
- workaround availability;
- regulatory/customer commitments.

A dramatic CPU graph with no customer impact may be less severe than a quiet correctness bug affecting financial records.

# Roles

For significant incidents, explicit roles reduce coordination overload.

Typical responsibilities:
- Incident Commander — coordinates decisions/priorities;
- Technical Lead(s) — investigates/executes mitigation;
- Communications — stakeholder/customer updates;
- Scribe — timeline, decisions, evidence.

Small incidents may combine roles. The goal is clarity, not ceremony.

# Incident command principles

- establish one coordination channel;
- state current impact and hypothesis separately;
- assign actions with owners;
- timestamp important changes;
- avoid many people making uncoordinated production changes;
- record deployment/config/infrastructure events;
- periodically restate current state;
- rotate responders during long incidents.

# Evidence hierarchy during diagnosis

Start from impact:

```text
business/customer symptom
 -> SLI / request behavior
 -> recent changes
 -> application metrics/traces/logs
 -> dependencies
 -> runtime/resources
 -> infrastructure/network
```

Avoid jumping to the first red graph.

# Change correlation

Ask early:
- deployments?
- feature flags?
- config/secrets?
- infrastructure/IaC?
- database migrations?
- dependency/provider changes?
- traffic/input pattern changes?

Correlation is not proof, but recent changes are high-value evidence.

# Mitigation vs remediation

Mitigation restores acceptable service now:
- rollback;
- disable feature;
- shed load;
- fail over;
- increase constrained capacity;
- bypass optional dependency.

Remediation addresses the underlying systemic issue later.

Do not confuse emergency capacity increase with proof that architecture needs permanent overprovisioning.

# Communication

Useful updates contain:
- impact;
- start/current status;
- mitigation progress;
- next update expectation;
- confirmed facts vs hypotheses.

Avoid speculative root causes in customer/executive communication.

# Recovery validation

Do not close an incident because one graph turned green.

Verify:
- critical user journeys;
- backlog/reconciliation;
- error/latency recovery;
- data correctness;
- degraded modes disabled appropriately;
- downstream effects;
- business metrics.

# Postmortem structure

## Summary
What happened and why it mattered.

## Impact
Users, duration, business/data/security effects.

## Detection
How detected? Could it have been detected earlier?

## Timeline
Important events, decisions and mitigations with timestamps.

## Technical narrative
Explain propagation through the system.

## Contributing factors
Architecture, process, tooling, assumptions, workload, organizational factors.

## What went well
Controls/people/tooling that reduced impact.

## What made response harder
Missing telemetry, unclear ownership, unsafe rollback, noisy alerts, manual access, etc.

## Actions
Specific improvements with owners/priorities and expected risk reduction.

# Root cause caution

Complex incidents rarely have one useful root cause.

"Engineer deployed bad code" is shallow.

Ask:
- Why could the bad behavior pass tests?
- Why did rollout reach so much traffic?
- Why did telemetry not detect it?
- Why was rollback slow?
- Why did dependency failure propagate?
- Which assumptions were invalid?

Use techniques such as Five Whys carefully; do not force a single linear story onto a complex system.

# Action quality

Weak action:

```text
Engineers should be more careful.
```

Stronger actions:

```text
Add contract test for the broken invariant.
Add per-version checkout SLI to canary verification.
Make rollback independent of manual database access.
Add idempotency to reconciliation path.
```

Prefer changes to systems/defaults/tooling over reminders when possible.

# Learning from near misses

Do not study only outages. A failed deployment caught by canary or an operator catching dangerous IaC replacement before apply can reveal important systemic risk without customer harm.

# Incident metrics

Use carefully:
- detection time;
- acknowledgement time;
- mitigation/recovery time;
- incident frequency;
- recurrence;
- customer-impact duration;
- percentage linked to changes;
- action completion/effectiveness.

Do not optimize MTTR by declaring incidents resolved prematurely.

# Practical game day

Scenario:

A checkout release introduces a query that is fast in staging but expensive with production data.

Effects:

```text
new version deployed
 -> DB query time increases
 -> connection pool saturates
 -> checkout p99 rises
 -> requests timeout
 -> clients retry
 -> DB load rises further
 -> payment outcomes become ambiguous
```

Run the incident:
1. detect from user-centered SLI;
2. establish command;
3. correlate deployment;
4. inspect DB/application evidence;
5. halt rollout/rollback if safe;
6. manage ambiguous payment outcomes/reconciliation;
7. validate business recovery;
8. write postmortem.

Then ask which prevention is justified: query/index fix, realistic data/performance test, canary metric, retry policy change, connection isolation, or some combination.

Do not answer "add Redis" unless evidence shows caching is the right solution.