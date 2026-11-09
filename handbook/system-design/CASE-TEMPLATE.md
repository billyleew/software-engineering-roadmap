# Case: <name>

**Status:** proposed | designing | implementing | measured | reviewed
**Learning objective:**
**Source references:** (original links; label unverified material)

## Problem statement
Who needs this system, and why?

## Functional requirements
- 

## Nonfunctional requirements and SLOs
- Availability:
- Latency (p50/p95/p99):
- Durability and consistency:
- Privacy/security:

## Assumptions and capacity estimates
| Variable | Assumption | Calculation | Confidence |
|---|---|---|---|
| Daily active users | | | |
| Requests/user/day | | | |
| Peak factor | | | |
| Average record bytes | | | |
| Retention | | | |

## API contracts and data model
Describe routes, schemas, validation, authorization and idempotency.

## Minimal architecture
Explain components, request/data flow, deployment and operations. Add a diagram.

## Alternative architectures and trade-offs
| Option | Benefit | Cost/complexity | Trigger for adoption |
|---|---|---|---|
| | | | |

## Failure modes and mitigations
Cover outages, overload, retries, duplicates, timeouts, data corruption and recovery.

## Security and threat model
Assets, trust boundaries, abuse scenarios, controls, residual risk.

## Code architecture and design patterns
Specify the application structure (MVC/layered, Clean, Hexagonal, vertical slices, etc.), domain boundaries, dependency direction, selected design patterns, and reasons for each. Explain which patterns were rejected and why. See [Architecture-to-Code PoC Framework](ARCHITECTURE-TO-CODE.md).

## PoC plan
Repository/path, setup commands, tests, expected evidence.

## Measurement plan
Workload, environment, dataset, metrics, acceptance thresholds, actual results.

## ADR / final decision
Chosen option, rejected alternatives, evidence, revisit criteria.

## Review questions
What would break at 10x scale? What assumptions remain untested?
