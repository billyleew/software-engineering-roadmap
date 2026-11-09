# Evidence-Based System Design and PoC Evaluation

This rubric evaluates engineering judgment rather than diagram complexity. Use it for design reviews, self-assessment, and future ELI-assisted feedback. Scores are **learning feedback**, not a claim of objective architecture quality.

## Scoring (0–3 for each dimension)

0 = missing; 1 = asserted without evidence; 2 = reasoned and partially validated; 3 = independently reproducible evidence and explicit trade-offs.

| Dimension | What strong evidence looks like |
|---|---|
| Problem framing | Explicit functional/nonfunctional requirements, assumptions, workload and SLOs |
| Capacity and economics | Reproducible calculations, peak estimates, storage and cost sensitivity |
| System architecture | Simple baseline, component responsibilities, alternatives and failure boundaries |
| Code architecture | Enforced dependency direction, cohesive modules, justified patterns and domain invariants |
| Data and consistency | Schema, indexes, transaction boundaries, ordering, deduplication and retention |
| Security | Threat model, authorization tests, secrets handling, abuse and privacy controls |
| Reliability | Timeout, retry, overload, crash/recovery and partial failure tests |
| Quality engineering | Automated unit/integration/contract tests and reproducible environment |
| Performance evidence | Workload, environment, p50/p95/p99, throughput and resource use |
| Decisions and evolution | ADR, rejected options, measured trigger for complexity and retrospective |

**Maximum:** 30 points. Report dimension scores and evidence links; never present a single number without its rationale. Unmeasured areas must score 0 or 1.

## Review gates

- **Gate 0 — Research:** sources and uncertainty recorded; no assumption is presented as a verified production fact.
- **Gate 1 — Design:** minimal architecture, competing alternatives, threats and measurable acceptance criteria documented.
- **Gate 2 — Working PoC:** automated tests pass and README reproduces the result locally.
- **Gate 3 — Evidence:** representative load and failure tests, actual measured results and known limitations.
- **Gate 4 — Evolution:** refactor or topology change justified by evidence; ADR and learning notes completed.

**Never mark a gate passed without links to its evidence.** Future AI reviewers may propose scores, but a human must approve them.

## Feedback format

For every review, report: **what works**, **what is unverified**, **most consequential failure mode**, **simplest credible alternative**, **next measurable experiment**, and **confidence**. Favor one high-value experiment over an unbounded list of technologies.
