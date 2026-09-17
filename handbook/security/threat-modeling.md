# Threat Modeling — Security Architecture Before Controls

## Objective

Threat modeling is structured reasoning about how a system can be abused or compromised and which risks deserve engineering attention.

```text
System purpose
 -> assets
 -> actors
 -> data flows
 -> trust boundaries
 -> threats / abuse cases
 -> risk
 -> mitigations
 -> verification + detection
```

# Step 1 — Understand the system

Document:
- business purpose;
- critical journeys;
- users/administrators/services;
- sensitive assets/data;
- components/dependencies;
- external systems;
- deployment/runtime;
- regulatory/business constraints.

# Step 2 — Draw data flows

Use a simple data-flow diagram rather than a decorative architecture picture.

For each flow capture:
- source/destination;
- protocol/interface;
- authentication;
- data classification;
- encryption/trust assumptions.

# Step 3 — Mark trust boundaries

Examples:
- Internet -> edge;
- user -> authenticated application;
- application -> privileged internal service;
- workload -> cloud control plane;
- CI runner -> production deployment role;
- tenant A -> shared multi-tenant data layer;
- employee -> privileged admin system.

Crossing a network is not the only trust boundary. Identity/privilege changes matter.

# Step 4 — Identify threats

Use abuse questions:
- Can an actor pretend to be someone else?
- Can data/config/artifacts be modified?
- Can an important action be denied/hidden?
- Can sensitive data leak?
- Can resources be exhausted?
- Can privilege increase?
- Can business rules be abused without exploiting code?

STRIDE can help prompt these categories.

# Step 5 — Model business abuse

Technical checklists often miss domain attacks.

For payments/rewards examples:
- replay same operation;
- manipulate amount/account;
- race concurrent redemptions;
- exploit retry to double-spend;
- enumerate another customer's object ID;
- abuse refund/transfer rules;
- create resource exhaustion cheaply.

Domain invariants are security controls too.

# Step 6 — Prioritize

Avoid pretending risk scores are mathematically precise.

Use evidence/context:
- exposure/reachability;
- attacker capability;
- exploit complexity;
- privilege required;
- affected asset;
- blast radius;
- financial/data/safety/regulatory impact;
- detectability/recoverability.

Separate known fact from assumption.

# Step 7 — Select controls

Possible responses:
- eliminate risky capability;
- reduce exposure;
- prevent;
- detect;
- limit blast radius;
- recover;
- transfer/accept risk explicitly.

Prefer controls close to the source of risk and secure defaults.

# Step 8 — Verify

For each important mitigation define evidence:
- unit/integration security test;
- authorization test;
- policy test;
- dependency scan;
- penetration/security review where justified;
- configuration validation;
- runtime detection;
- incident exercise.

# Threat model as living artifact

Revisit when:
- new external integration;
- new sensitive data;
- auth model changes;
- multi-tenancy introduced;
- architecture/service boundary changes;
- new privileged automation/AI agent;
- cloud/runtime migration;
- major incident reveals new assumptions.

# CI/CD example

Assets:
- source code;
- build secrets;
- artifacts;
- production deploy permission.

Trust boundaries:

```text
external contributor/PR
 -> repository workflow
 -> CI runner
 -> artifact registry
 -> deployment identity
 -> production
```

Threats:
- malicious PR executes privileged workflow;
- third-party action compromised;
- artifact replaced after testing;
- long-lived cloud credential stolen;
- build logs leak token.

Potential controls:
- isolate untrusted builds;
- least-privilege workflow permissions;
- short-lived federated identity;
- immutable/digest-addressed artifacts;
- protected production environments;
- provenance/signature verification where warranted;
- secret redaction/detection.

# Multi-tenant API example

Critical invariant:

```text
Authenticated user from Tenant A
MUST NOT read/update Tenant B resources.
```

Test authorization at the resource/domain boundary. Do not rely only on hidden UI links or guessed identifiers being difficult.

# AI preview

Future AI/agent architectures add trust boundaries:
- user content -> model context;
- retrieved documents -> model;
- model -> tool invocation;
- agent -> filesystem/code/cloud/financial systems;
- external tool result -> subsequent decisions.

Prompt injection, excessive tool permission and untrusted retrieved content will later be handled as security architecture problems, not merely prompt-writing problems.

# Threat-model review template

```text
System:
Business purpose:
Critical journeys:
Assets/data:
Actors:
Dependencies:
Trust boundaries:
Threats/abuse cases:
Risk assumptions:
Existing controls:
Proposed controls:
Verification:
Detection/response:
Residual risks:
Owners:
Review trigger/date:
```

# Principal Engineer questions

- Which attack creates the largest credible business impact?
- What assumption makes it possible?
- Is prevention, detection, containment or recovery the best investment?
- Does the proposed control create reliability/DevEx risk?
- Is authorization enforced where the resource/domain decision is made?
- Can compromise move laterally?
- Can the organization revoke/recover quickly?
- What evidence proves the mitigation?