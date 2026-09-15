# Deployment Strategies — Control Risk with Feedback

## Principle

A deployment strategy is a risk-control mechanism. Choose it from failure impact, rollback difficulty, traffic shape, state/data changes and required confidence—not because canary or blue/green sounds mature.

```text
Change risk
 + blast radius
 + detection capability
 + rollback/recovery characteristics
 + infrastructure cost
 -> deployment strategy
```

# Rolling deployment

Replace instances incrementally.

Good default when:
- application versions are temporarily compatible;
- partial mixed-version operation is safe;
- infrastructure supports health-aware replacement;
- fast rollback/roll-forward is possible.

Risks:
- old/new versions coexist;
- API/schema compatibility matters;
- a subtle regression may reach all traffic before detection.

Observe rollout health by version, not only globally.

# Recreate deployment

Stop old version and start new version.

Simple and sometimes perfectly acceptable for internal/non-critical systems where downtime is allowed.

Do not pay for zero-downtime complexity if the business explicitly accepts a maintenance window.

# Blue/Green

Maintain old and new production-capable environments and switch traffic.

Strengths:
- rapid traffic switch;
- strong environment-level rollback capability;
- useful for high-risk changes.

Costs/risks:
- duplicated capacity;
- state/database compatibility remains difficult;
- environment drift if poorly managed;
- traffic switch does not undo external side effects.

# Canary

Expose a new version to a limited subset of traffic before increasing exposure.

Can reduce blast radius **only if you can detect meaningful regressions before promotion**.

A canary without useful telemetry is merely a slower rollout.

Observe per-version:
- request rate;
- errors;
- latency distributions;
- resource saturation;
- business success metrics;
- dependency behavior;
- critical logs/traces.

Compare canary against a suitable baseline/control and account for low traffic/sample size.

# Progressive delivery

Automate traffic progression based on explicit verification criteria.

Example:

```text
5%
 -> verify
25%
 -> verify
50%
 -> verify
100%
```

Possible gates:
- error-rate delta;
- latency regression;
- SLO burn;
- business KPI regression;
- critical synthetic checks.

Automation is dangerous if the metrics are weak or thresholds meaningless.

# Feature flags

Separate deployment from feature exposure.

Useful for:
- gradual enablement;
- experimentation;
- operational kill switches;
- decoupling code deployment from product release.

Costs:
- branching behavior in production;
- test matrix growth;
- stale flags;
- configuration risk.

Flags need ownership, observability and removal lifecycle.

# Shadow / mirrored traffic

Send production-like traffic to a new implementation without using its result for the customer.

Useful for validating performance/behavior, but be careful with side effects, privacy and cost. Shadow writes must not accidentally execute real business operations.

# Deployment verification

A successful orchestrator status does not mean a successful release.

Verification layers can include:

```text
process started
 -> readiness/health
 -> synthetic transaction
 -> technical telemetry
 -> business telemetry
 -> sustained SLO behavior
```

# Health checks

Differentiate:
- liveness: should this process be restarted?
- readiness: should this instance receive traffic?
- startup: does initialization require a longer allowance?

Do not make liveness depend on every external dependency; a database outage can otherwise cause restart storms.

# Rollback vs roll forward

Rollback is not always safest.

If a deployment includes an irreversible or incompatible database/data transformation, old code may no longer work correctly. Sometimes a small forward fix is safer.

Plan recovery before release.

# Database compatibility

During mixed-version or rollback-capable deployments, use compatible schema evolution.

Example:

```text
1 add nullable/new field
2 deploy code supporting old + new
3 backfill
4 switch reads/writes
5 verify
6 later remove old field
```

# Deployment observability

Every deployment should be visible as an event on relevant dashboards.

Ask:
- What changed?
- Which version is serving this request?
- When did the rollout start?
- What percentage is on the new version?
- Did error/latency/business behavior change?
- Was rollback triggered?

# Choosing the strategy

| Situation | Possible starting strategy |
|---|---|
| Small internal app, downtime acceptable | Recreate |
| Standard stateless service, compatible versions | Rolling |
| High-risk release, fast environment switch valuable | Blue/Green |
| High traffic and strong per-version telemetry | Canary |
| Mature automated verification | Progressive delivery |
| Product exposure should be independent of deploy | Feature flag |

This table is a starting heuristic, not a rule.

# Practical exercise

Deploy the same API using three strategies:
1. rolling;
2. blue/green;
3. canary.

Inject a regression that affects only one endpoint and increases p99 latency without causing health-check failure.

For each strategy measure:
- users exposed;
- time to detect;
- time to recover;
- infrastructure cost/complexity;
- telemetry required.

Then write an ADR choosing the simplest strategy appropriate for the product's actual risk.