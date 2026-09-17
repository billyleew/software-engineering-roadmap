# Security Engineering — Build Security Into the Engineering System

## Objective

Security Engineering manages risk to confidentiality, integrity, availability, authenticity and accountability across software, data, infrastructure and organizational workflows.

Security is not a scanner at the end of CI/CD.

```text
Business/data asset
 -> threat model
 -> trust boundaries
 -> controls
 -> secure implementation/defaults
 -> verification
 -> telemetry/detection
 -> response/recovery
 -> learn/evolve
```

# Risk mental model

Ask:
- What are we protecting?
- From whom/what?
- What could go wrong?
- What is the likelihood/exposure?
- What is the impact?
- Which control reduces risk?
- What does the control cost or break?
- What residual risk remains?

Do not implement every possible control equally. Prioritize meaningful risk.

# Core properties

## Confidentiality
Only authorized parties can access information.

## Integrity
Data/system behavior cannot be modified improperly and unauthorized changes can be detected/prevented.

## Availability
Authorized users can access required capabilities when needed.

## Authentication
Who/what is this principal?

## Authorization
What is this principal allowed to do?

## Accountability/auditability
Can important actions be attributed and investigated?

# Threat modeling

For a feature/system:
1. identify assets;
2. map components/data flows;
3. mark trust boundaries;
4. identify threats/abuse cases;
5. prioritize by risk;
6. choose mitigations;
7. define verification/detection;
8. revisit when architecture changes.

STRIDE can be used as a prompt/checklist, not a substitute for thinking:
- Spoofing;
- Tampering;
- Repudiation;
- Information disclosure;
- Denial of service;
- Elevation of privilege.

# Identity and access

Principles:
- least privilege;
- deny by default where appropriate;
- short-lived credentials;
- workload identity instead of shared static keys;
- separation of duties for high-risk actions;
- strong authentication for privileged access;
- periodic access lifecycle/revocation;
- auditable emergency/break-glass procedures.

# Application security

Study:
- input validation;
- output encoding;
- injection classes;
- authentication/session management;
- authorization and object-level access;
- CSRF where relevant;
- SSRF;
- unsafe deserialization;
- file/upload handling;
- rate limiting/abuse controls;
- secrets;
- cryptographic API use;
- dependency risk;
- business-logic abuse.

Use OWASP material as a risk-learning source, not merely a compliance checklist.

# API security

For every API ask:
- authenticated actor/workload?
- authorization at resource/action level?
- input/schema constraints?
- replay/idempotency concerns?
- rate/abuse limits?
- sensitive data in URL/logs/errors?
- version/deprecation strategy?
- audit requirements?

An API Gateway does not automatically secure application authorization.

# Data security

Classify data and define:
- collection minimization;
- purpose/use;
- access;
- encryption in transit/at rest;
- key management;
- retention/deletion;
- backup protection;
- masking/tokenization where useful;
- auditability;
- residency/regulatory constraints.

Encryption cannot compensate for unrestricted application authorization.

# Secrets management

Never store secrets in source code, container images or ordinary logs.

Prefer:
- dedicated secret stores;
- workload identity/dynamic credentials;
- rotation;
- access auditing;
- scoped secrets;
- short lifetime where feasible.

Assume accidental exposure can happen; design revocation/rotation.

# Software supply chain

Protect:

```text
source
 -> dependency
 -> build runner
 -> CI workflow
 -> artifact
 -> registry
 -> deployment
 -> runtime
```

Study:
- dependency pinning/updates;
- malicious/compromised packages;
- CI permissions;
- third-party actions/plugins;
- artifact provenance;
- SBOM;
- signing/verification where justified;
- trusted registries;
- build isolation;
- branch/review controls.

# Container security

- minimal/trusted base image;
- non-root;
- minimal capabilities;
- avoid privileged workloads;
- read-only filesystem where practical;
- image scanning/remediation;
- runtime restrictions;
- workload identity;
- network controls;
- secrets outside image.

# Kubernetes security

Study:
- RBAC;
- service accounts/workload identity;
- admission/policy;
- pod security controls;
- network policies;
- secrets integration;
- audit logs;
- cluster-admin protection;
- control-plane/node lifecycle;
- tenant isolation boundaries;
- operator/controller privileges.

# Cloud security

Understand:
- account/project boundaries;
- IAM/trust policies;
- public exposure;
- security groups/firewalls;
- private networking;
- encryption/key services;
- audit/control-plane logs;
- organization policies;
- backup security;
- provider shared-responsibility model.

# CI/CD security

Pipelines are privileged production infrastructure.

Threats include:
- secret theft;
- malicious dependency/build script;
- compromised runner;
- untrusted PR executing privileged code;
- artifact substitution;
- overprivileged deployment identity.

Use environment protections and short-lived identity appropriate to risk.

# Observability and detection

Security needs telemetry, but avoid logging sensitive data.

Potential signals:
- authentication anomalies;
- authorization denials;
- privileged actions;
- secret/key changes;
- unusual network/access patterns;
- WAF/abuse signals;
- artifact/deployment changes;
- policy violations;
- data access anomalies.

Detection must connect to response ownership/runbooks.

# Vulnerability management

A scanner finding is not automatically equal to exploitable risk.

Prioritize using context:
- exploitability/reachability;
- exposure;
- privilege required;
- asset/data criticality;
- known exploitation;
- compensating controls;
- remediation risk.

Still patch known high-risk vulnerabilities quickly; contextual prioritization should reduce noise, not excuse neglect.

# Security in architecture reviews

Ask:
- assets/data classification?
- actors/trust boundaries?
- authentication/authorization?
- external inputs?
- privileged operations?
- secrets/keys?
- data retention?
- dependency/supply-chain risk?
- abuse/DoS?
- audit/detection?
- incident/recovery?

# Security and reliability

Security and reliability overlap:
- DDoS affects availability;
- credential compromise can destroy data;
- ransomware/corruption requires recovery;
- aggressive controls can create outages;
- emergency access needs safe governance.

Test security controls under failure conditions.

# Security and DevEx

Secure defaults should be easier than insecure custom configuration.

Platform paved roads can provide:
- workload identity;
- secret integration;
- TLS;
- dependency scanning;
- artifact provenance;
- policy checks;
- standard logging/audit;
- network defaults.

Security that requires manual specialist tickets for every normal action will often be bypassed.

# Security learning path

1. threat/risk modeling
2. identity, authentication and authorization
3. application/API security
4. data/cryptography fundamentals
5. secrets/key management
6. supply-chain security
7. container/Kubernetes/cloud security
8. security observability/detection
9. vulnerability management
10. incident response/recovery
11. secure platform engineering
12. governance/compliance as engineering constraints

# Practical capstone

Threat-model the platform/application built in Stage 2.

Map:

```text
Internet/user
 -> edge/API
 -> application
 -> database
 -> queue/dependencies
 -> cloud identity
 -> CI/CD
 -> artifact registry
 -> deployment platform
 -> observability
```

Then:
- identify trust boundaries/assets;
- prioritize threats;
- implement selected controls;
- add security telemetry;
- simulate credential/dependency/access failure safely;
- document response;
- write security ADRs for major trade-offs.

# Principal Engineer questions

- What are the highest-value assets?
- What is the realistic threat model?
- Where are trust boundaries?
- Which identities are overprivileged?
- Can a compromised CI job reach production?
- Can one tenant/user access another's resources?
- Which sensitive data enters logs/traces?
- How are secrets revoked?
- How do we know a control is working?
- What is our detection/response path?
- Which security requirement materially changes architecture?
- What residual risk is consciously accepted and by whom?