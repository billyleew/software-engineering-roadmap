# Refactoring, Legacy Code & Debugging

These three skills belong together: understand existing behavior, create safety, improve structure, and diagnose unexpected behavior using evidence.

# Refactoring

Refactoring changes internal structure while preserving externally observable behavior.

## Safe loop

```text
Behavior understood
 -> tests green
 -> one small structural change
 -> tests green
 -> commit
 -> repeat
```

Useful techniques include Extract Function/Method, Rename, Move Function, Encapsulate Data, Replace Conditional with Polymorphism when variation warrants it, Introduce Parameter Object, Split Phase, and removing duplicated knowledge.

## Rule

Do not combine a large behavior change and a large structural rewrite when they can be separated. Smaller steps make failures attributable.

## Example

Before adding a new payment provider:
1. Characterize current payment behavior.
2. Isolate the current provider behind a meaningful payment boundary.
3. Keep tests green.
4. Add the new provider.
5. Add contract/integration tests for provider-specific behavior.

# Working with Legacy Code

Legacy code is code that is risky to change because feedback and boundaries are insufficient, regardless of its age.

## Change algorithm

```text
Identify desired change
 -> locate behavior
 -> identify dependencies
 -> create a test seam
 -> add characterization tests
 -> make minimal structural change
 -> implement new behavior
 -> verify
```

## Characterization tests

Their first purpose is to record what the system **currently does**, including behavior that may look strange. Once behavior is captured, decide deliberately whether it is correct or should change.

## Seams

A seam is a place where behavior can be changed or substituted without editing the core logic under test. Examples include interfaces, injected functions, adapters, wrapper modules and process boundaries.

## Rewrite warning

A full rewrite removes accumulated implementation problems but can also discard years of undocumented business knowledge. Prefer incremental replacement unless evidence shows that evolution is more expensive or unsafe than migration.

# Systematic Debugging

Debugging is an evidence-generation process.

```text
Observe
 -> Reproduce
 -> Hypothesize
 -> Design experiment
 -> Narrow search space
 -> Confirm cause
 -> Fix
 -> Verify
 -> Prevent recurrence
```

## Symptom vs root cause

Example:

```text
Symptom: API returns 500
Observation: DB connection pool exhausted
Contributing factor: requests wait too long
Root cause: a code path fails to close connections after timeout
```

Increasing pool size may hide the symptom without correcting the defect.

## Debugging questions

- What changed?
- Can I reproduce it?
- What evidence distinguishes competing hypotheses?
- What is the smallest experiment I can run?
- At which boundary does expected behavior become incorrect?
- Is this deterministic, timing-related, data-dependent or environment-dependent?
- Am I fixing the cause or suppressing the symptom?

## Distributed debugging

For distributed systems, correlate:
- request/trace ID
- timestamps
- service/version
- deployment/change event
- logs
- metrics
- traces
- dependency behavior
- retries/timeouts

Do not infer causation solely from two events occurring near each other.

# Practical lab — fragile payment service

Create a deliberately poor payment module containing:
- business rules in the HTTP controller
- direct vendor SDK calls
- duplicated validation
- no tests
- generic exception handling
- a retry that can duplicate a charge

Then evolve it:
1. Add characterization tests.
2. Separate domain rules from transport.
3. Create a payment-provider seam.
4. Introduce explicit errors.
5. Make the payment operation idempotent.
6. Add integration tests.
7. Add structured logs and correlation IDs.
8. Inject a timeout failure and debug it using evidence.
9. Document why each structural change was made.

The goal is not a perfect final architecture. The goal is practicing safe evolution.