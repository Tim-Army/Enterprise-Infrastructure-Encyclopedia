# Chapter 03: Cloud Identity, Access, and Cryptographic Services

![Lab flow for this chapter: policy/no_wildcard_actions.rego denies any Allow statement combining a literal wildcard action with a literal wildcard resource; policy-scoped.json (actions scoped to specific prod database ARNs) passes with zero failures, while policy-overbroad.json (a single statement granting action:* on resource:*) fails, naming the offending statement. As a negative test, policy-prefix-wildcard.json — a legitimate action-prefix wildcard scoped to a specific resource — passes, confirming the guardrail targets only the literal double-wildcard pattern and does not false-positive on scoped prefix wildcards.](../../../diagrams/volume-07-cloud-infrastructure/chapter-03-iam-least-privilege-policy-flow.svg)

*Figure 3-1. Flow used throughout this chapter's Hands-On Lab: a local policy engine catching an overly broad IAM permission grant before it is ever attached to a real identity.*

## Learning Objectives

- Distinguish human, workload, and federated identity, and explain why
  long-lived static credentials are the highest-priority identity risk to
  eliminate in a cloud environment.
- Design a least-privilege access model using role-based and
  attribute-based access control, and explain when each is the better fit.
- Explain identity federation (SAML 2.0 and OIDC) and workload identity
  federation, and trace a federated sign-in from assertion to a
  short-lived, scoped credential.
- Differentiate provider-managed key management services from
  customer-managed and customer-supplied key models, and choose correctly
  among them for a given compliance requirement.
- Design a secrets management strategy that avoids embedding static
  credentials in code, configuration, or CI pipeline definitions.
- Write and evaluate a least-privilege access policy as code, and diagnose
  an access-denied error methodically rather than by broadening
  permissions.

## Theory and Architecture

### Identity is the new perimeter

In an on-premises data center, the network boundary (firewall, VLAN
segmentation, physical access control) did much of the work of keeping
unauthorized actors away from a resource. In a cloud environment, every
resource has a public or semi-public API endpoint, and the network boundary
around that endpoint is thin or absent by design — the control plane is
reachable from anywhere on the internet unless deliberately restricted.
Identity and the policy attached to it become the primary control: the
question is no longer only "can this packet reach the resource" but "does
the caller presenting this credential have permission to take this specific
action on this specific resource." Every chapter in this volume assumes
this identity-first posture; landing zone guardrails ([Chapter 02](02-landing-zones-resource-organization-and-guardrails.md)) and
network segmentation ([Chapter 04](04-cloud-networking-and-hybrid-connectivity.md)) are complementary, not substitutes.

### Three categories of identity

- **Human identity** — a person authenticating to a console, CLI, or API,
  almost always through a federated corporate identity provider (IdP)
  rather than a provider-native username and password. Human identity
  should require multi-factor authentication (MFA) universally and should
  hold standing permissions only for what routine work requires.
- **Workload identity** — an identity assumed by a running piece of
  software (a compute instance, a container, a CI pipeline job, a
  serverless function) to call other services. Workload identity should
  never be a long-lived static credential; the goal is always a
  short-lived, automatically rotated credential scoped to exactly what
  that workload needs.
- **Federated identity** — an identity asserted by an external identity
  provider (a corporate directory, a CI/CD platform, another cloud
  provider) and exchanged for a provider-native, time-boxed credential.
  Federation is the mechanism that makes both human and workload identity
  avoid long-lived provider-native secrets.

### Authentication vs. authorization

Authentication answers "who is this caller," and produces a verified
identity. Authorization answers "what is this verified identity allowed to
do," and is evaluated against a policy at the time of each request. Cloud
providers implement authorization as a policy evaluation engine that
inspects the identity, the requested action, the target resource, and
often request context (source network, time of day, MFA presence) before
allowing a control-plane or data-plane call to proceed. Treat these as two
independent controls to reason about separately during an incident: a
caller can be correctly authenticated and still correctly denied by
authorization policy, and that denial is the system working as designed,
not a fault.

### Access control models

- **Role-based access control (RBAC)** — permissions are bundled into
  named roles (`network-admin`, `read-only-auditor`, `database-operator`),
  and identities are granted membership in a role rather than having
  individual permissions assigned directly. RBAC is easy to reason about
  and audit ("who has the `network-admin` role") and is the right default
  for the majority of human and workload access.
- **Attribute-based access control (ABAC)** — authorization decisions are
  evaluated against attributes of the identity, the resource, and the
  request context at evaluation time (for example, "allow if the caller's
  `team` tag matches the resource's `owner` tag"). ABAC scales better than
  RBAC when the number of distinct role/resource combinations would
  otherwise grow combinatorially — a single tag-matching policy can replace
  hundreds of per-team, per-resource roles — at the cost of being harder to
  audit by inspection alone, since the effective permission set depends on
  attribute values evaluated at request time.

Most mature environments combine both: RBAC for coarse-grained job-function
roles, ABAC layered on top for fine-grained, resource-scoped restriction
(most commonly, restricting a role's permissions to only the resources
carrying a matching project or environment tag).

### The least-privilege principle in practice

Least privilege means an identity holds exactly the permissions its current
task requires, for exactly as long as the task requires them, and no more.
In practice this is a discipline applied continuously, not a one-time grant
decision:

- Start from zero permissions and add explicitly, rather than starting
  from a broad built-in role and attempting to narrow it later — the
  latter pattern reliably leaves unused permissions in place because
  removing access is politically and operationally harder than granting
  it.
- Prefer time-boxed, just-in-time elevation for sensitive or rarely used
  permissions over standing grants.
- Periodically review actual permission usage (most providers offer some
  form of access-analyzer or last-accessed reporting) and remove
  permissions that have gone unused for a defined period.

### Federation: SAML 2.0 and OIDC

Both SAML 2.0 and OpenID Connect (OIDC, built on OAuth 2.0) let an external
identity provider assert identity to a cloud provider without the cloud
provider ever storing or verifying a password. The mechanics differ but the
shape of the flow is the same:

1. A human (browser-based flow) or a workload (machine-to-machine flow)
   authenticates to the identity provider (corporate IdP for humans; a
   CI/CD platform's own OIDC issuer for workloads).
2. The identity provider issues a signed assertion (a SAML assertion or an
   OIDC JSON Web Token) containing the verified identity and, often,
   attributes such as group membership.
3. The cloud provider validates the assertion's signature against a
   pre-configured trust relationship with that identity provider, maps the
   asserted identity/attributes to a provider-native role, and issues a
   short-lived, scoped credential (commonly valid for 15 minutes to a few
   hours).
4. The caller uses that short-lived credential for the duration of the
   session or job; no long-lived provider-native secret was ever created
   or exchanged.

### Workload identity federation

The same pattern extends to workloads that need to call a cloud provider's
API from outside that provider — most commonly a CI/CD pipeline job
deploying infrastructure. Workload identity federation lets a CI/CD
platform's own OIDC issuer assert "this specific pipeline, on this specific
branch, in this specific repository, is currently running" directly to the
cloud provider's federation trust configuration, which exchanges that
assertion for a short-lived credential scoped to a specific deployment
role. This eliminates the single most common secret-sprawl problem in
cloud automation: a long-lived cloud access key stored as a CI/CD platform
secret, which is powerful, rarely rotated, and reusable by anyone who can
read that secret store or trigger that pipeline in an unintended context.

### Cryptographic services: key management models

Cloud providers offer a spectrum of key management responsibility:

| Model | Who generates the key | Who holds the key material | Typical use |
| --- | --- | --- | --- |
| Provider-managed keys | Provider | Provider, never exposed | Default encryption at rest with no special compliance requirement |
| Customer-managed keys (CMK) | Customer, via the provider's key management service | Provider's KMS, customer controls policy/rotation/deletion | Regulatory requirements for key ownership, audit, and revocation control |
| Customer-supplied/imported keys | Customer, outside the provider | Provider's KMS, but the customer retains the authoritative copy | Compliance regimes requiring the key never originate inside the provider |
| Hold-your-own-key / external key store | Customer, in customer-controlled hardware | Never resident in the provider at rest; released per-operation | Highest-assurance regulatory requirements; adds latency and availability dependency on the external key store |

Moving down this table increases customer control and audit granularity
(who used which key, when, and for what) at the cost of increasing the
customer's own operational burden — key rotation, availability of the
external key store, and disaster-recovery planning for the key material
itself. Choose the least operationally burdensome model that satisfies the
actual compliance requirement; "customer-managed keys everywhere" is a
common over-application of a control that a specific regulator or
contract clause requires only for a narrow data classification.

### Secrets management vs. key management

Key management services handle cryptographic keys used for
encryption/decryption and signing operations, typically without ever
exposing the raw key material to the caller. Secrets management services
store and serve arbitrary sensitive values — database passwords, API
tokens, TLS private keys used by an application — that the application
does, at some point, need in plaintext to function. Treat these as
distinct services with distinct threat models: a key management service's
job is to never reveal the key; a secrets management service's job is to
reveal the secret only to an authorized, authenticated caller and to make
that access auditable and rotatable.

## Design Considerations

### Choosing RBAC, ABAC, or both

Default to RBAC for any environment with a small, stable number of job
functions and resource groupings. Introduce ABAC deliberately when the
number of role/resource combinations is growing faster than the team can
maintain distinct roles for — the signal is usually a role-naming pattern
that has started encoding project or team names directly into role names
(`payments-team-prod-network-admin`), which is a sign that a tag-matching
ABAC policy would collapse dozens of roles into one reusable pattern.

### Standing access vs. just-in-time elevation

Standing (always-on) privileged access is convenient but is also always
available to be misused, whether by a compromised credential or an
insider. Just-in-time elevation — a time-boxed, logged, and (for
higher-risk actions) approved grant of elevated permission — reduces the
window of exposure at the cost of added friction and a dependency on the
elevation system's own availability. Reserve standing access for
permissions genuinely needed continuously (a monitoring system's
read-only access) and require just-in-time elevation for anything
destructive or rarely used.

### Federation trust scope

A federation trust relationship (SAML or OIDC) should be scoped as
narrowly as the identity provider allows. For workload identity federation
specifically, scope the trust to a specific repository, branch, and
environment — a trust configured to accept an assertion from "any
pipeline in this CI/CD organization" rather than "this specific repository
on this specific branch" means any pipeline anywhere in that organization
can assume the deployment role, which defeats the isolation the pattern is
meant to provide.

### Key management model selection

Map the key management model decision to an actual compliance obligation
or documented risk acceptance, not to a default assumption that more
customer control is always better. Customer-managed keys introduce a real
operational responsibility: a customer-managed key that is accidentally
deleted or has its policy misconfigured can render encrypted data
permanently unreadable, which is a considerably worse outcome than the
provider-managed default in most threat models. Document key rotation
policy, deletion protection, and who holds emergency access before
adopting customer-managed keys broadly.

### Secrets lifecycle and rotation

Design secrets management around automatic rotation from the start rather
than retrofitting it. A secret that requires a manual, coordinated rotation
across every consumer is a secret that will not be rotated on schedule in
practice. Prefer secrets that a dependent workload fetches dynamically at
runtime (or short-lived dynamic credentials generated per-session by the
secrets engine itself, for services that support it) over secrets baked
into a deployment artifact, which forces a redeploy for every rotation.

## Implementation and Automation

### Defining a least-privilege role as code

```hcl
# roles/database-operator.tf — illustrative, provider-neutral shape.
variable "environment" {
  type = string
}

resource "cloud_iam_role" "database_operator" {
  name        = "database-operator-${var.environment}"
  description = "Operate managed database instances in ${var.environment}; no network or IAM changes."

  permissions = [
    "database:Describe*",
    "database:Reboot",
    "database:CreateSnapshot",
    "database:ListSnapshots",
  ]

  # Attribute-based condition: only resources tagged for this environment.
  condition {
    test     = "StringEquals"
    variable = "resource.tags.environment"
    values   = [var.environment]
  }
}
```

```hcl
# federation.tf — illustrative workload identity federation trust,
# scoped to a single repository, branch, and environment.
resource "cloud_iam_federation_trust" "ci_deploy" {
  name           = "ci-deploy-${var.environment}"
  issuer         = "https://token.actions.example-ci.com"
  audience       = "cloud-provider-sts"

  subject_condition {
    # Scoped narrowly: this repo, this branch, this environment only.
    claim  = "sub"
    equals = "repo:example-org/infra-repo:ref:refs/heads/main"
  }

  assumable_role = cloud_iam_role.database_operator.name
}
```

Native validation and narrow subject conditions like these are the policy
layer's first defense; combine them with the organization-wide
policy-as-code guardrails from [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md) for a defense-in-depth posture
rather than relying on any single layer.

### Requesting a federated credential (illustrative flow)

```bash
# Illustrative OIDC-to-cloud-credential exchange, run inside a CI job.
# The CI platform injects a short-lived OIDC token; this exchanges it
# for a scoped, short-lived cloud credential. Exact command varies by
# provider and CI platform.
CLOUD_CREDENTIALS=$(cloud-cli sts assume-role-with-web-identity \
  --role-arn "arn:example:iam::123456789012:role/database-operator-prod" \
  --web-identity-token "$CI_OIDC_TOKEN" \
  --role-session-name "ci-deploy-$(date +%s)" \
  --duration-seconds 900)
```

Note the 900-second (15-minute) duration: scope the credential lifetime to
slightly longer than the job's expected runtime, not to the provider's
maximum allowed duration. A shorter lifetime narrows the window an
exfiltrated credential remains useful.

### Provisioning a customer-managed key

```hcl
# kms.tf — illustrative customer-managed key with rotation and
# deletion protection.
resource "cloud_kms_key" "app_data" {
  description             = "Customer-managed key for application data at rest."
  rotation_enabled         = true
  rotation_period_days      = 90
  deletion_window_days      = 30 # mandatory waiting period before destroy takes effect

  key_administrators = ["group:security-key-admins"]
  key_users          = ["role:database-operator-prod"]
}
```

The `deletion_window_days` waiting period is a deliberate safeguard: it
converts an accidental or malicious key deletion into a recoverable event
during the window, at the cost of the key (and anything encrypted with it)
remaining technically destroyable-in-progress and billable during that
period.

### Storing and consuming a secret dynamically

```hcl
# secrets.tf — illustrative secret definition; value is written outside
# of Terraform state through a separate, audited process.
resource "cloud_secrets_manager_secret" "db_password" {
  name                    = "app/prod/db-password"
  rotation_enabled         = true
  rotation_interval_days     = 30
  rotation_lambda_arn      = cloud_function.rotate_db_password.arn
}
```

```bash
# Application startup — fetch the current secret value at runtime
# rather than baking it into the deployment artifact.
DB_PASSWORD=$(cloud-cli secrets get-value --name "app/prod/db-password" --query "value")
```

## Validation and Troubleshooting

- **Diagnose access-denied errors methodically.** Check, in order: (1) is
  the identity authenticated as expected (correct account/tenant, not an
  unintended session), (2) what is the effective policy for this identity
  on this specific resource (request an effective-permissions or
  policy-simulator report rather than reading individual role definitions
  by eye), (3) is there an explicit deny anywhere in the evaluated policy
  set — an explicit deny anywhere in scope overrides any allow, which is a
  common source of "but I granted that permission" confusion.
- **Do not resolve an access-denied error by broadening the grant.**
  Widening a role to fix a single denied action routinely leaves excess
  permission in place long after the original task is done. Grant the
  specific missing permission, scoped to the specific resource, and record
  why.
- **Validate federation trust scope after every change.** Confirm the
  subject condition still matches only the intended repository, branch,
  and environment; a broadened trust condition is a silent, high-impact
  security regression that produces no error until it is exploited.
- **Test key deletion protection before relying on it.** Confirm the
  deletion window and any required approval step actually behave as
  configured in a non-production key, rather than assuming the
  configuration is correct.
- **Alert on secrets access patterns, not only on secrets rotation
  failure.** An unexpected spike in reads of a specific secret, or a read
  from an unexpected identity or network location, is often the first
  observable sign of a compromised credential.

## Security and Best Practices

- Eliminate long-lived, static cloud access keys wherever federation is
  available; treat any remaining static key as a tracked exception with an
  owner, a justification, and a mandatory rotation schedule.
- Require multi-factor authentication for every human identity without
  exception, including break-glass accounts — a break-glass account with a
  password-only fallback defeats the purpose of MFA everywhere else.
- Scope workload identity federation trust to the narrowest subject
  condition the identity provider supports (repository, branch, and
  environment, not organization-wide).
- Apply least privilege as a continuous discipline: start from zero,
  review actual usage on a schedule, and remove unused permissions rather
  than accumulating them.
- Separate key management administration from key usage — the identity
  that can change a key's policy or schedule its deletion should not
  routinely be the same identity that uses the key for everyday
  encryption/decryption operations.
- Never place a secret value in source code, a Terraform variable
  committed to version control, or a CI/CD pipeline definition file in
  plaintext; reference it from a secrets manager at runtime instead.

## References and Knowledge Checks

### References

- NIST SP 800-63, *Digital Identity Guidelines*.
- OASIS SAML 2.0 Technical Overview.
- OpenID Connect Core 1.0 specification (openid.net).
- Each major provider's identity, key management, and secrets management
  service documentation — consult the current vendor source for exact API
  and CLI syntax.
- `SOFTWARE_VERSIONS.md` in this repository for the Terraform baseline used
  in illustrative examples throughout this volume.

### Knowledge checks

1. Why is a long-lived static cloud access key considered a higher risk
   than a federated, short-lived credential even if both are granted
   identical permissions?
2. Give a concrete example of a role/resource scenario better served by
   ABAC than by adding more RBAC roles.
3. A CI/CD pipeline's workload identity federation trust is scoped to
   `repo:example-org/*` instead of a specific repository. What is the
   practical security consequence?
4. A team requests customer-managed keys for a dataset with no specific
   regulatory requirement citing key ownership. What operational risk
   should be weighed against the perceived security benefit?
5. Walk through the correct order of checks for diagnosing an unexpected
   access-denied error, and explain why widening the role first is the
   wrong first step.

## Hands-On Lab

### Lab 3.1 — Evaluating least-privilege policy with a local policy engine

This lab evaluates a candidate IAM policy document against a set of sample
requested actions using `conftest`, entirely on the local filesystem. It
demonstrates catching an overly broad permission grant before it is ever
attached to a real identity. No cloud account or credentials are required.

**Prerequisites**

- `conftest` installed (validated against the `conftest` 0.5x series).
- A POSIX shell and `jq`.

**Steps**

1. Create the lab directory and a policy subdirectory:

   ```bash
   mkdir -p ~/labs/vol07-ch03/policy && cd ~/labs/vol07-ch03
   ```

2. Create `policy/no_wildcard_actions.rego`, a policy that denies any
   statement granting a wildcard action alongside a wildcard resource — a
   common accidental over-grant pattern:

   ```rego
   package main

   deny[msg] {
     statement := input.statements[_]
     statement.effect == "Allow"
     statement.action[_] == "*"
     statement.resource[_] == "*"
     msg := sprintf("statement %q grants wildcard action on wildcard resource", [statement.sid])
   }
   ```

3. Create a **compliant** candidate policy at `policy-scoped.json`:

   ```json
   {
     "statements": [
       {
         "sid": "AllowDatabaseReboot",
         "effect": "Allow",
         "action": ["database:Reboot", "database:Describe*"],
         "resource": ["arn:example:database:us-east-1:*:db/prod-*"]
       }
     ]
   }
   ```

4. Create a **noncompliant** candidate policy at `policy-overbroad.json`:

   ```json
   {
     "statements": [
       {
         "sid": "EmergencyAccess",
         "effect": "Allow",
         "action": ["*"],
         "resource": ["*"]
       }
     ]
   }
   ```

5. Evaluate the scoped policy:

   ```bash
   conftest test policy-scoped.json --policy policy
   ```

   **Expected result:** `PASS` with zero failures.

6. Evaluate the overbroad policy:

   ```bash
   conftest test policy-overbroad.json --policy policy
   ```

   **Expected result:** `FAIL`, reporting `statement "EmergencyAccess"
   grants wildcard action on wildcard resource`, with a nonzero exit code
   (confirm with `echo $?`, which should print `1`).

**Negative test**

7. Confirm the policy does not falsely flag a wildcard used narrowly (a
   wildcard *action prefix* on a specific resource, which is a common and
   legitimate pattern). Create `policy-prefix-wildcard.json`:

   ```json
   {
     "statements": [
       {
         "sid": "AllowDescribeActions",
         "effect": "Allow",
         "action": ["database:Describe*"],
         "resource": ["arn:example:database:us-east-1:*:db/prod-*"]
       }
     ]
   }
   ```

   Run `conftest test policy-prefix-wildcard.json --policy policy`.

   **Expected result:** `PASS` — the policy specifically targets a literal
   `"*"` action combined with a literal `"*"` resource, not a scoped
   prefix wildcard, confirming the guardrail does not create false-positive
   friction against legitimate least-privilege patterns.

**Cleanup**

8. Remove the lab directory:

   ```bash
   cd ~ && rm -rf ~/labs/vol07-ch03
   ```

   **Expected result:** The directory no longer exists. No cloud identity,
   role, or credential was created at any point in this lab.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Identity is the primary control boundary in cloud infrastructure. This
chapter covered the three categories of identity (human, workload,
federated), the difference between authentication and authorization,
RBAC and ABAC as complementary access control models, how SAML 2.0 and
OIDC federation eliminate long-lived static credentials for both human
sign-in and CI/CD workload access, the spectrum of key management
responsibility from provider-managed to hold-your-own-key, and secrets
management as a distinct discipline from key management. [Chapter 04](04-cloud-networking-and-hybrid-connectivity.md) builds
the network foundation that sits alongside this identity foundation, and
[Chapter 08](08-cloud-governance-security-and-finops.md) returns to access governance at the organizational policy
level.

- [ ] Can explain why federation eliminates the need for long-lived static
      cloud credentials.
- [ ] Can choose correctly between RBAC and ABAC for a given scaling
      scenario.
- [ ] Can select an appropriate key management model against a stated
      compliance requirement, and explain the operational trade-off.
- [ ] Can diagnose an access-denied error using the effective-policy
      method rather than by broadening a grant.
- [ ] Completed Lab 3.1, including the negative test and cleanup.
