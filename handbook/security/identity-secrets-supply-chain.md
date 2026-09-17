# Identity, Secrets & Software Supply Chain

## Identity before network location

Modern distributed/cloud systems should not assume "inside the network = trusted."

Every important action should have an identifiable principal and explicit authorization.

```text
principal
 -> authentication
 -> identity claims
 -> authorization policy
 -> resource/action
 -> audit
```

# Human identity

Protect privileged human access with:
- centralized identity where appropriate;
- MFA/strong authentication;
- role-based/attribute-based authorization as needed;
- least privilege;
- temporary elevation for sensitive operations;
- lifecycle provisioning/revocation;
- auditable break-glass access.

Avoid shared administrator accounts.

# Workload identity

Applications need identity too.

Prefer platform/cloud-issued short-lived workload credentials over static secrets embedded in configuration.

Examples of conceptual mechanisms:
- workload service account/role;
- OIDC/federated identity from CI;
- managed identity metadata/token service;
- certificate-based workload identity where justified.

# Authorization

Authentication answers who; authorization answers whether that identity may perform this action on this resource.

Enforce authorization server-side and close to the protected resource/domain boundary.

Study:
- RBAC;
- ABAC/policy-based approaches;
- resource ownership;
- tenant isolation;
- delegated authorization/scopes;
- privileged admin actions.

Beware role explosion and overly broad wildcard permissions.

# OAuth 2.x and OpenID Connect mental model

Learn protocols from primary specifications/current security guidance when implementing them.

Conceptually:
- OAuth provides delegated authorization mechanisms;
- OpenID Connect adds an identity/authentication layer using OAuth foundations;
- access tokens authorize API access according to their semantics;
- ID tokens represent authentication claims for the client and should not casually be substituted for API authorization tokens.

Do not design custom authentication protocols because token formats appear simple.

# Secrets lifecycle

A secret needs:

```text
creation
 -> storage
 -> distribution/access
 -> use
 -> rotation
 -> revocation
 -> audit
 -> destruction
```

Questions:
- Who can read it?
- Which workload needs it?
- Can identity remove the need for it?
- How quickly can it rotate?
- What happens if exposed?
- Does it leak into logs/state/build artifacts?

# Secret zero problem

If an application needs a credential to retrieve other credentials, determine how the initial identity is established. Cloud/workload identity mechanisms often reduce static bootstrap secrets.

# Encryption and keys

Use established cryptographic libraries/services and protocols.

Understand distinctions:
- encryption vs hashing;
- symmetric vs asymmetric cryptography;
- transport encryption vs data-at-rest encryption;
- key encryption keys/data keys;
- signing vs encryption;
- password hashing/KDFs.

Do not invent cryptographic algorithms or protocols.

# Supply chain model

```text
Developer
 -> source repository
 -> dependencies
 -> CI workflow
 -> build runner
 -> artifact
 -> registry
 -> deployment controller
 -> runtime
```

Each step can alter what reaches production.

# Repository security

Depending on risk:
- protected branches/rulesets;
- required review;
- signed commits are optional context-dependent controls, not universal proof of safety;
- restricted workflow modification;
- CODEOWNERS/review for sensitive paths;
- secret scanning;
- dependency update process.

# Dependency risk

Threats:
- known vulnerabilities;
- malicious packages;
- dependency confusion/typosquatting;
- compromised maintainer/release;
- abandoned dependency;
- transitive risk.

Controls:
- lockfiles/version control;
- trusted registries;
- vulnerability/reputation review proportional to risk;
- automated updates with tests;
- dependency minimization;
- artifact verification when ecosystem supports it.

# CI runner security

Treat runner execution as code execution.

Questions:
- Can untrusted PR code access secrets?
- Are runners ephemeral?
- Can one build contaminate another?
- What network access exists?
- What cloud identity does the runner receive?
- Can build code modify deployment infrastructure?

Separate build and production privileges where possible.

# Artifact integrity and provenance

Goal:

```text
source revision
 -> controlled build
 -> immutable artifact digest
 -> verified promotion
 -> production runtime
```

Possible mechanisms depending on maturity/risk:
- immutable registry;
- digest-based deployment;
- SBOM;
- build provenance/attestations;
- signing and verification;
- policy preventing untrusted artifacts.

The objective is confidence about what was built and what is running, not collecting security acronyms.

# SBOM

A Software Bill of Materials inventories software components/dependencies. It improves visibility and incident/vulnerability response, but does not by itself prove software is safe.

# CI/CD identity lab

Replace a long-lived cloud deployment key with short-lived federated identity where your chosen lab platform supports it.

Compare:

```text
static key
 -> stored secret
 -> long lifetime
 -> manual rotation
 -> broad exposure risk
```

with:

```text
CI identity assertion
 -> trust policy
 -> short-lived scoped credential
 -> deploy
 -> expiry
```

Document new trust assumptions introduced by federation.

# Supply-chain incident exercise

Scenario: a dependency used in builds is reported compromised.

Determine:
- which services/artifacts contain it?
- which versions are deployed?
- whether malicious behavior is reachable?
- when introduced?
- what credentials/network/data it could access?
- how to rebuild/redeploy safely?
- whether artifacts can be trusted?
- what telemetry detects exploitation?

This connects SBOM/provenance to actual incident response.

# Principal Engineer questions

- Can static credentials be replaced by workload identity?
- Which identity can deploy production?
- Can untrusted code obtain that identity?
- How is tenant/resource authorization enforced?
- How quickly can compromised access be revoked?
- Can we identify every deployed artifact affected by a dependency incident?
- Do we know what source/build produced production?
- Which controls materially reduce supply-chain risk vs produce scanner noise?