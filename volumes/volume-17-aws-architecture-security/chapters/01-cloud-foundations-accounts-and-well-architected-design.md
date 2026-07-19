# Chapter 01: Cloud Foundations, Accounts, and Well-Architected Design

![Lab flow for this chapter: caller identity and Region defaults are confirmed, root is verified to have no access keys, and a monthly cost guardrail budget is created and confirmed with a near-zero actual spend; a sample workload registers in the Well-Architected Tool. As a negative test, a second budget is submitted with an invalid time unit; the Budgets API returns a validation error rather than creating a partially configured guardrail, confirming malformed input is rejected outright.](../../../diagrams/volume-17-aws-architecture-security/chapter-01-account-baseline-budget-guardrail-flow.svg)

*Figure 1-1. Flow used throughout this chapter's Hands-On Lab: an AWS account baseline hardened with a cost guardrail and a registered Well-Architected workload, tested against malformed budget input.*

## Learning Objectives

- Explain the AWS shared responsibility model and identify which controls
  belong to AWS versus the customer for a given service category.
- Describe AWS global infrastructure (Regions, Availability Zones, edge
  locations, Local Zones, Wavelength Zones) and select a Region using
  latency, data-residency, service-availability, and cost criteria.
- Summarize the six pillars of the AWS Well-Architected Framework and apply
  them to evaluate a workload design.
- Harden a new AWS account's root user and configure baseline cost and
  billing controls before any workload is deployed.
- Register a workload in the AWS Well-Architected Tool and produce a
  prioritized list of improvement items from a pillar review.

## Theory and Architecture

Amazon Web Services delivers infrastructure and platform services from a
globally distributed footprint that is organized into three nested units:
**Regions**, **Availability Zones (AZs)**, and **edge locations**. A Region
is a fully independent geographic area (for example `us-east-1` in Northern
Virginia or `eu-central-1` in Frankfurt) containing multiple AZs. Each AZ is
one or more discrete data centers with independent power, cooling, and
networking, connected to other AZs in the same Region by low-latency, high-
throughput private fiber. Designing across at least two AZs is the baseline
unit of high availability on AWS; designing across Regions is the baseline
unit of disaster recovery and data-residency control, covered in depth in
[Chapter 06](06-reliability-migration-multi-region-and-disaster-recovery.md).

Beyond the standard Region/AZ model, AWS offers infrastructure that trades
some independence for proximity to users or specific regulatory boundaries:

| Infrastructure type | Purpose | Independence from parent Region |
| --- | --- | --- |
| Availability Zone | HA within a Region | Independent facilities, shared Region control plane |
| Local Zone | Single-digit-millisecond latency to a metro area | Extension of a parent Region; subset of services |
| Wavelength Zone | Ultra-low-latency compute embedded in telco 5G networks | Extension of a parent Region for edge compute |
| Edge location / Regional edge cache | CloudFront, Route 53, Global Accelerator points of presence | Global network, not a deployable compute target |
| AWS Outposts | AWS-managed rack or server on customer premises | Physically on-premises, managed as an extension of a home Region |

### Shared responsibility model

AWS operates a **shared responsibility model** that divides security and
operational obligations between AWS and the customer. AWS is responsible for
"security **of** the cloud": the physical facilities, hardware, the
virtualization layer, and the managed-service control planes. The customer
is responsible for "security **in** the cloud": identity and access
configuration, data classification and encryption choices, network
controls, guest operating system patching (where applicable), and
application-layer security. The exact line moves with the service's
abstraction level:

- **Infrastructure services** (EC2, EBS, self-managed VPC networking) put
  the guest OS, patching, and network ACL/security-group configuration on
  the customer.
- **Container/managed services** (RDS, ECS on Fargate, EKS control plane)
  shift OS and orchestration-layer patching to AWS while the customer still
  owns schema/workload configuration, IAM policy, and data.
- **Serverless/abstracted services** (Lambda, S3, DynamoDB) shift nearly all
  infrastructure operations to AWS; the customer's remaining responsibility
  concentrates almost entirely on identity, resource policy, and data
  handling.

This model is the reason Volume XVII treats identity and network
configuration as first-class chapters (Chapters 02 and 03) rather than an
afterthought: on AWS, customer-side misconfiguration — not a breach of AWS's
physical or hypervisor layer — is the dominant real-world root cause of
cloud security incidents.

### The AWS Well-Architected Framework

The Well-Architected Framework organizes architectural judgment into six
pillars. Every design decision in this volume is evaluated against them:

1. **Operational Excellence** — run and monitor systems to deliver business
   value and continually improve supporting processes. Emphasizes
   infrastructure as code, small reversible changes, and runbooks.
2. **Security** — protect information, systems, and assets through risk
   assessments and mitigation strategies. Emphasizes identity, detective
   controls, data protection, and incident response.
3. **Reliability** — ensure a workload performs its intended function
   correctly and consistently, including recovery from failure.
4. **Performance Efficiency** — use computing resources efficiently to meet
   requirements and maintain efficiency as demand and technology evolve.
5. **Cost Optimization** — avoid unnecessary costs and understand where
   money is spent, including the ability to scale cost with value delivered.
6. **Sustainability** — minimize the environmental impact of running cloud
   workloads, including energy efficiency and resource utilization.

Each pillar carries a design-principle checklist and a set of trade-offs
that frequently conflict with other pillars (for example, multi-Region
active-active reliability increases cost and reduces sustainability
efficiency per transaction). The **AWS Well-Architected Tool**, available
free in the AWS Management Console and via the `wellarchitected` CLI
namespace, walks an architect through a structured pillar-by-pillar review
of a defined workload and records improvement items with risk ratings.

### The account as the unit of isolation

An **AWS account** is the fundamental security, billing, and resource
isolation boundary. Resources in one account cannot see or affect resources
in another account unless a trust relationship (a role, resource policy, or
Resource Access Manager share) explicitly grants it. Every account has
exactly one **root user**, created with the account and possessing
unrestricted access that cannot be limited by any policy. [Chapter 02](02-multi-account-identity-governance-and-landing-zones.md)
extends this single-account model into multi-account governance with AWS
Organizations, but every account — including a future member account in an
Organization — still starts from the same root-user and billing foundation
covered here.

## Design Considerations

- **Region selection is a compound decision, not a defaults choice.**
  Evaluate latency to the primary user base, data-residency and
  sovereignty requirements (some workloads must legally stay within a
  jurisdiction), the specific services and instance types available in
  that Region (newer Regions launch with a smaller service catalog), and
  per-Region pricing differences, which can vary by double-digit
  percentages for the same service.
- **AZ count is a reliability/cost trade-off.** Two AZs is the practical
  minimum for HA; three AZs improves resilience against a correlated
  failure and simplifies quorum-based systems (for example, a 3-AZ RDS
  Multi-AZ cluster or a distributed consensus store) at proportionally
  higher fixed cost.
- **Single account vs. landing zone from day one.** A single AWS account is
  appropriate only for a proof of concept or a very small, low-blast-radius
  workload. Any account expected to run production workloads, host multiple
  teams, or eventually require compliance segregation should be planned
  against the multi-account model in [Chapter 02](02-multi-account-identity-governance-and-landing-zones.md) before the first workload
  is deployed — retrofitting account boundaries under an existing workload
  is materially more disruptive than starting with them.
- **Free Tier boundaries are workload-shaping, not just cost-shaping.**
  Many AWS Free Tier offers are time-boxed (12 months from account
  creation) or usage-capped per month; a lab or proof of concept that
  exceeds NAT gateway hours, EBS gp3 storage, or data-transfer allowances
  will incur charges even in a new account. Treat Free Tier limits as a
  design input, not a guarantee.
- **Well-Architected reviews are cheapest early.** Running a Well-Architected
  review before significant investment is far less costly than remediating
  an entrenched design; schedule a lightweight review at the end of the
  design phase and a fuller review before go-live and again after major
  architecture changes.

## Implementation and Automation

### 1. Root user hardening

Perform these steps immediately after account creation, before any other
configuration:

```bash
# There is no CLI action for root MFA enrollment — it must be done once in
# the console under "My Security Credentials." Verify the account has no
# root access keys, since root should never hold long-lived programmatic
# credentials:
aws iam list-access-keys --output table
# Expect no output when authenticated as an IAM Identity Center user;
# if run as root and any keys are listed, delete them:
aws iam delete-access-key --access-key-id <ACCESS_KEY_ID> --user-name root
```

After enabling a hardware or virtual MFA device on root in the console,
confirm the account alias and contact information are current, since AWS
uses account-level contacts for security and billing notifications:

```bash
aws iam create-account-alias --account-alias my-org-prod-2026
aws account put-alternate-contact \
  --alternate-contact-type SECURITY \
  --email-address secops@example.com \
  --phone-number "+1-555-0100" \
  --title "Security Operations" \
  --name "SecOps Team"
```

### 2. AWS CLI v2 installation and profile configuration

```bash
# macOS
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
aws --version

# Configure a named profile using IAM Identity Center (recommended over
# long-lived IAM user access keys, detailed further in Chapter 02)
aws configure sso --profile sandbox
aws sts get-caller-identity --profile sandbox
```

### 3. Baseline cost and billing controls

```bash
# Create a monthly cost budget with an alert at 80% of a $50 threshold
aws budgets create-budget \
  --account-id 111122223333 \
  --budget '{
    "BudgetName": "monthly-account-guardrail",
    "BudgetLimit": {"Amount": "50", "Unit": "USD"},
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }' \
  --notifications-with-subscribers '[{
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80
    },
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "secops@example.com"}]
  }]'

# Enable cost allocation tags used later for chargeback (Chapter 07)
aws ce update-cost-allocation-tags-status \
  --cost-allocation-tags-status TagKey=environment,Status=Active TagKey=owner,Status=Active
```

### 4. Registering a workload in the Well-Architected Tool

```bash
aws wellarchitected create-workload \
  --workload-name "payments-api-prod" \
  --description "Customer-facing payments API" \
  --environment PRODUCTION \
  --aws-regions "us-east-1" "us-west-2" \
  --lenses "wellarchitected" \
  --review-owner "platform-team@example.com"

# List open improvement items after completing a pillar questionnaire
aws wellarchitected list-answers \
  --workload-id <WORKLOAD_ID> \
  --lens-alias wellarchitected \
  --pillar-id security
```

Terraform can express the same workload registration declaratively for
teams that manage Well-Architected reviews as code:

```hcl
resource "aws_wellarchitected_workload" "payments_api" {
  workload_name  = "payments-api-prod"
  description    = "Customer-facing payments API"
  environment    = "PRODUCTION"
  review_owner   = "platform-team@example.com"
  lenses         = ["wellarchitected"]
  aws_regions    = ["us-east-1", "us-west-2"]
}
```

## Validation and Troubleshooting

- **Confirm root has no active access keys.** `aws iam list-access-keys
  --user-name root` (run with root credentials, or check the console Security
  Credentials page) must show zero keys. Any result other than zero is a
  standing security finding.
- **Confirm CLI identity resolves to the intended principal.** `aws sts
  get-caller-identity --profile sandbox` must return the expected account ID
  and an assumed-role or IAM Identity Center ARN, never a root ARN.
- **Confirm budget notifications are wired correctly.** Use `aws budgets
  describe-notifications-for-budget` and verify the subscriber list matches
  the intended distribution list; a budget with no working subscriber
  silently fails to alert.
- **Common failure: Region mismatch.** A resource created successfully but
  "not found" on a later lookup is very often a `--region` flag or
  `AWS_DEFAULT_REGION` mismatch between the two commands, not a permissions
  or replication issue. Always pass `--region` explicitly in
  troubleshooting sessions rather than relying on profile defaults.
- **Common failure: stale SSO session.** `aws sso login --profile sandbox`
  tokens expire (commonly in 8–12 hours depending on the Identity Center
  session policy); an `ExpiredToken` or `UnauthorizedException` error on an
  otherwise-correct command usually means the session needs to be
  re-authenticated, not that the underlying permission set changed.
- **Well-Architected Tool review not saving answers.** Confirm the calling
  principal has the `wellarchitected:UpdateAnswer` action; the tool silently
  ignores UI changes submitted by a principal without write permission and
  the review will appear to revert on refresh.

## Security and Best Practices

- Enable MFA on the root user immediately, store the MFA device/recovery
  codes in an organization-controlled secrets vault (not an individual's
  personal device only), and never create root access keys.
- Use the root user only for the small set of tasks that require it (for
  example, closing an account or certain Organizations management-account
  actions); perform all daily operations through IAM Identity Center
  federated identities or IAM roles, detailed in [Chapter 02](02-multi-account-identity-governance-and-landing-zones.md).
- Enable AWS CloudTrail in every account from the first hour of its
  existence — a trail created after an incident cannot retroactively
  produce the missing history. [Chapter 08](08-security-architecture-detection-and-incident-response.md) covers CloudTrail Lake and
  organization-wide trails in depth.
- Set a billing alert at a low, easily exceeded threshold in every new
  account (as shown above) to catch runaway resource creation, whether
  from a lab mistake or a compromised credential, within hours instead of
  at month-end.
- Treat the AWS account ID as sensitive-but-not-secret: it is required for
  cross-account trust policies and should not be published unnecessarily,
  but a leaked account ID alone does not grant access.
- Run a full Well-Architected Security-pillar review before any workload
  handling regulated or customer data goes to production, and re-run it
  after any material architecture change.

## References and Knowledge Checks

**References**

- [AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html) — the six-pillar whitepaper and the
  Well-Architected Tool documentation.
- [AWS shared responsibility model](https://aws.amazon.com/compliance/shared-responsibility-model/) — AWS Cloud Security documentation.
- [AWS Global Infrastructure documentation](https://aws.amazon.com/about-aws/global-infrastructure/) — Regions, Availability Zones,
  Local Zones, and Wavelength.
- [AWS Billing and Cost Management documentation](https://docs.aws.amazon.com/account-billing/) — AWS Budgets and cost
  allocation tags.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — the dated AWS
  service-surface baseline referenced throughout this volume.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  maps this volume to the AWS Certified Solutions Architect and AWS
  Certified Security blueprint domains; consult the official AWS exam
  guide for the authoritative, current domain weighting.

**Knowledge checks**

1. Which party is responsible for guest operating system patching on Amazon
   EC2, and how does that responsibility change on AWS Fargate?
2. Name two factors, besides latency, that should influence AWS Region
   selection for a new workload.
3. Which Well-Architected pillar most directly addresses the trade-off
   between multi-Region active-active reliability and per-transaction
   infrastructure cost?
4. Why should a new AWS account's root user never hold an access key?

## Hands-On Lab

**Objective:** Harden a new or sandbox AWS account's baseline posture and
register a workload in the AWS Well-Architected Tool.

**Cost implications:** This lab uses no billable resources beyond
negligible API calls; AWS Budgets and the Well-Architected Tool are free.
No cleanup billing risk exists, but complete the cleanup steps to avoid
leaving unused artifacts in the account.

**Prerequisites**

- An AWS account you control (a personal sandbox or dedicated training
  account, not a shared production account) with console and AWS CLI v2
  access as an administrator.
- An email address you can receive budget alerts at.

**Steps**

1. Confirm the caller identity and Region defaults:

   ```bash
   aws sts get-caller-identity
   aws configure get region
   ```

   **Expected result:** A JSON block with your account ID and principal
   ARN, and a configured default Region.

2. Verify root has no access keys (requires root sign-in for a fully
   authoritative check, or review via the console Security Credentials
   page if signed in as an IAM Identity Center administrator):

   ```bash
   aws iam list-access-keys --user-name root --output table
   ```

   **Expected result:** An empty key list.

3. Create a monthly cost guardrail budget:

   ```bash
   aws budgets create-budget \
     --account-id "$(aws sts get-caller-identity --query Account --output text)" \
     --budget '{
       "BudgetName": "lab-guardrail",
       "BudgetLimit": {"Amount": "10", "Unit": "USD"},
       "TimeUnit": "MONTHLY",
       "BudgetType": "COST"
     }' \
     --notifications-with-subscribers '[{
       "Notification": {
         "NotificationType": "ACTUAL",
         "ComparisonOperator": "GREATER_THAN",
         "Threshold": 80
       },
       "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "YOUR_EMAIL@example.com"}]
     }]'
   ```

4. Confirm the budget was created:

   ```bash
   aws budgets describe-budgets \
     --account-id "$(aws sts get-caller-identity --query Account --output text)" \
     --query "Budgets[?BudgetName=='lab-guardrail']"
   ```

   **Expected result:** A JSON object describing the `lab-guardrail` budget
   with an `ActualSpend` amount near zero.

5. Register a sample workload in the Well-Architected Tool:

   ```bash
   aws wellarchitected create-workload \
     --workload-name "lab-workload" \
     --description "Well-Architected Tool lab" \
     --environment PREPRODUCTION \
     --aws-regions "$(aws configure get region)" \
     --lenses "wellarchitected" \
     --review-owner "YOUR_EMAIL@example.com"
   ```

   **Expected result:** JSON output containing a `WorkloadId`.

6. **Negative test:** Attempt to create a second budget with an invalid
   time unit to confirm input validation is enforced (this should fail,
   not silently create a broken budget):

   ```bash
   aws budgets create-budget \
     --account-id "$(aws sts get-caller-identity --query Account --output text)" \
     --budget '{
       "BudgetName": "lab-invalid",
       "BudgetLimit": {"Amount": "10", "Unit": "USD"},
       "TimeUnit": "FORTNIGHTLY",
       "BudgetType": "COST"
     }'
   ```

   **Expected result:** A `ValidationException` error. This confirms the
   Budgets API rejects malformed input rather than creating a
   partially-configured guardrail.

7. **Cleanup:**

   ```bash
   aws budgets delete-budget \
     --account-id "$(aws sts get-caller-identity --query Account --output text)" \
     --budget-name "lab-guardrail"

   aws wellarchitected delete-workload --workload-id <WORKLOAD_ID>
   ```

   Confirm removal:

   ```bash
   aws budgets describe-budgets \
     --account-id "$(aws sts get-caller-identity --query Account --output text)"
   aws wellarchitected list-workloads --query "WorkloadSummaries[?WorkloadName=='lab-workload']"
   ```

   Both queries should return no trace of the lab artifacts.

## Summary and Completion Checklist

AWS infrastructure is organized as Regions built from independent
Availability Zones, extended at the edge by Local Zones, Wavelength, and a
global CDN/DNS network. The shared responsibility model determines which
security controls AWS owns and which the customer must configure, and that
division shifts with each service's abstraction level. The Well-Architected
Framework's six pillars — Operational Excellence, Security, Reliability,
Performance Efficiency, Cost Optimization, and Sustainability — provide the
structured vocabulary this entire volume uses to evaluate design choices.
Every account begins with root-user hardening, CLI/identity configuration,
and cost guardrails before a single workload resource is created.

- [ ] Can explain the shared responsibility model boundary for at least
      three AWS service abstraction levels.
- [ ] Can name and describe all six Well-Architected Framework pillars.
- [ ] Can state at least three factors relevant to AWS Region selection.
- [ ] Has hardened root-user access and configured a cost guardrail budget.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
