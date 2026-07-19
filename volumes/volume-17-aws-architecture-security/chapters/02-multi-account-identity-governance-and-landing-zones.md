# Chapter 02: Multi-Account Identity, Governance, and Landing Zones

## Learning Objectives

- Design a multi-account structure using AWS Organizations organizational
  units (OUs) that separates workloads by environment and blast radius.
- Write and attach service control policies (SCPs) that enforce
  organization-wide guardrails independent of any single account's IAM
  configuration.
- Distinguish IAM users, groups, roles, identity-based policies,
  resource-based policies, and permission boundaries, and choose the
  correct mechanism for a given access-control requirement.
- Configure AWS IAM Identity Center permission sets to provide federated,
  short-lived access across multiple accounts.
- Explain what an AWS Control Tower landing zone automates and when it is
  appropriate versus a hand-built Organizations structure.

## Theory and Architecture

[Chapter 01](01-cloud-foundations-accounts-and-well-architected-design.md) established the AWS account as the atomic unit of isolation.
**AWS Organizations** groups multiple accounts under a single management
account, enabling consolidated billing, centralized policy enforcement, and
programmatic account creation. Accounts are arranged into **organizational
units (OUs)** — a hierarchical grouping construct, not a resource container
— so that policy can be attached once at an OU and inherited by every
account beneath it.

A typical enterprise OU structure separates accounts by function and
environment rather than by team or application, because environment is what
determines blast radius and guardrail strictness:

```text
Root
├── Security OU        (log-archive, audit/security-tooling accounts)
├── Infrastructure OU   (network hub, shared-services accounts)
├── Workloads OU
│   ├── Production OU   (prod-app-a, prod-app-b, ...)
│   ├── Staging OU
│   └── Sandbox OU       (per-developer or per-team sandbox accounts)
└── Suspended OU        (accounts pending decommission)
```

### Service control policies

**Service control policies (SCPs)** are JSON policies attached to the
Organizations root, an OU, or an individual account. Unlike IAM policies,
an SCP never *grants* permission by itself — it defines the maximum
permission boundary that IAM policies inside the account can grant. An
action is only allowed if it is permitted by both the effective SCP and an
IAM policy in the account; an SCP `Deny` cannot be overridden by any
in-account policy, including that account's own root user policy
equivalent. This makes SCPs the correct tool for guardrails that must hold
even against a misconfigured or compromised in-account administrator, such
as "deny disabling CloudTrail" or "deny leaving an approved Region list."

### IAM building blocks

| Construct | Attached to | Typical use |
| --- | --- | --- |
| Identity-based policy | IAM user, group, or role | Grants the principal permission to call actions |
| Resource-based policy | A resource (S3 bucket policy, KMS key policy, Lambda resource policy) | Grants a principal (including cross-account) permission on that specific resource |
| Permission boundary | An IAM user or role | Caps the maximum permissions that identity-based policies can grant to that principal, even if attached policies are broader |
| Service control policy | An Organizations root/OU/account | Caps the maximum permissions available anywhere in that account, regardless of IAM configuration |
| Session policy | An `AssumeRole` call | Further restricts a temporary session below the role's own permissions, scoped to that session only |

IAM **users** with long-lived access keys are the legacy access pattern and
should be reserved for the narrow cases that require a static credential
(certain third-party integrations, break-glass emergency access). IAM
**roles**, assumed via AWS Security Token Service (STS) to obtain temporary
credentials, are the default for both human and machine access. **IAM
Identity Center** (the successor to AWS SSO) federates a workforce identity
source — its own built-in directory, or an external IdP via SAML/SCIM such
as Microsoft Entra ID or Okta — and maps users and groups to **permission
sets**, which are templates that Identity Center provisions as IAM roles in
each assigned account.

### Landing zones

A **landing zone** is the automated baseline that provisions a multi-account
environment: the Organizations structure, a dedicated log-archive account,
a security-tooling/audit account, baseline SCPs, and account-vending
self-service. **AWS Control Tower** is AWS's managed landing zone service —
it deploys and manages this baseline, including a set of preventive SCPs
and detective AWS Config rules called **guardrails**, and provides an
**Account Factory** for repeatable, policy-compliant account creation.
Organizations that need customization beyond what Control Tower's guardrail
catalog supports often layer **AWS Control Tower Account Factory for
Terraform (AFT)** or a custom Terraform/CloudFormation pipeline on top of, or
instead of, Control Tower's native automation.

## Design Considerations

- **OU structure should reflect blast radius, not org chart.** Grouping
  accounts by team name defeats the purpose of SCP inheritance if two teams
  need different guardrails at the same maturity/environment level. Model
  OUs on environment and data sensitivity first; use tags and account names
  for team ownership.
- **SCPs are guardrails, not fine-grained authorization.** Because SCPs
  apply organization-wide and are usually managed by a small platform/
  security team, keep them coarse (deny leaving approved Regions, deny
  disabling logging, deny leaving the Organization) rather than trying to
  encode per-application authorization logic, which belongs in IAM policy
  inside the account.
- **Control Tower vs. hand-built Organizations.** Control Tower
  accelerates a compliant baseline and is the right default for a new
  enterprise landing zone. A hand-built Organizations/Terraform approach
  gives full control and is more appropriate for organizations with
  unusual compliance requirements Control Tower's guardrail catalog cannot
  express, or that already have a mature IaC platform team.
- **Permission set scope.** Broad permission sets (for example, granting
  `AdministratorAccess` in every account to every engineer) defeat the
  purpose of account segregation. Scope permission sets per OU/account
  group and prefer time-bound elevation workflows for break-glass access
  over standing broad access.
- **Log-archive and audit account isolation.** The account that stores
  CloudTrail logs and Config history should be a dedicated account that
  workload teams have no standing write access to; this prevents an
  attacker (or a well-intentioned but destructive script) with workload
  account access from tampering with the audit trail.
- **Root user in member accounts.** Member accounts still each have a root
  user. Control Tower and most landing zone patterns leave member-account
  root credentials unknown/unused by design, relying on Identity Center
  federation for all access; plan a documented, auditable root-password-
  reset break-glass procedure rather than assuming root access is never
  needed.

## Implementation and Automation

### 1. Organizations structure and OUs (Terraform)

```hcl
resource "aws_organizations_organization" "org" {
  aws_service_access_principals = [
    "cloudtrail.amazonaws.com",
    "config.amazonaws.com",
    "sso.amazonaws.com",
  ]
  feature_set = "ALL"
}

resource "aws_organizations_organizational_unit" "security" {
  name      = "Security"
  parent_id = aws_organizations_organization.org.roots[0].id
}

resource "aws_organizations_organizational_unit" "workloads" {
  name      = "Workloads"
  parent_id = aws_organizations_organization.org.roots[0].id
}

resource "aws_organizations_organizational_unit" "production" {
  name      = "Production"
  parent_id = aws_organizations_organizational_unit.workloads.id
}
```

### 2. Service control policy: deny disabling logging and Region restriction

```hcl
data "aws_iam_policy_document" "scp_guardrails" {
  statement {
    sid       = "DenyCloudTrailTamper"
    effect    = "Deny"
    actions   = [
      "cloudtrail:StopLogging",
      "cloudtrail:DeleteTrail",
      "cloudtrail:UpdateTrail",
    ]
    resources = ["*"]
  }

  statement {
    sid       = "DenyOutsideApprovedRegions"
    effect    = "Deny"
    not_actions = [
      "iam:*", "organizations:*", "route53:*", "cloudfront:*",
      "waf:*", "support:*", "sts:*", "budgets:*",
    ]
    resources = ["*"]
    condition {
      test     = "StringNotEquals"
      variable = "aws:RequestedRegion"
      values   = ["us-east-1", "us-west-2"]
    }
  }
}

resource "aws_organizations_policy" "guardrails" {
  name    = "baseline-guardrails"
  type    = "SERVICE_CONTROL_POLICY"
  content = data.aws_iam_policy_document.scp_guardrails.json
}

resource "aws_organizations_policy_attachment" "guardrails_prod" {
  policy_id = aws_organizations_policy.guardrails.id
  target_id = aws_organizations_organizational_unit.production.id
}
```

### 3. Account vending via the CLI

```bash
aws organizations create-account \
  --email "aws-prod-payments@example.com" \
  --account-name "prod-payments" \
  --role-name OrganizationAccountAccessRole \
  --iam-user-access-to-billing ALLOW

# Poll creation status
aws organizations describe-create-account-status \
  --create-account-request-id <REQUEST_ID>

# Move the new account into the Production OU
aws organizations move-account \
  --account-id <NEW_ACCOUNT_ID> \
  --source-parent-id <ROOT_ID> \
  --destination-parent-id <PRODUCTION_OU_ID>
```

### 4. IAM Identity Center permission sets

```bash
aws sso-admin create-permission-set \
  --instance-arn "$IDC_INSTANCE_ARN" \
  --name "NetworkAdmin" \
  --session-duration "PT4H" \
  --description "Network engineering access, 4-hour sessions"

aws sso-admin attach-managed-policy-to-permission-set \
  --instance-arn "$IDC_INSTANCE_ARN" \
  --permission-set-arn "$PERMISSION_SET_ARN" \
  --managed-policy-arn "arn:aws:iam::aws:policy/AmazonVPCFullAccess"

aws sso-admin create-account-assignment \
  --instance-arn "$IDC_INSTANCE_ARN" \
  --target-id "<PRODUCTION_ACCOUNT_ID>" \
  --target-type AWS_ACCOUNT \
  --permission-set-arn "$PERMISSION_SET_ARN" \
  --principal-type GROUP \
  --principal-id "$NETWORK_ENGINEERS_GROUP_ID"
```

### 5. A permission boundary for delegated role creation

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "DenyIAMPrivilegeEscalation",
      "Effect": "Deny",
      "Action": ["iam:CreateUser", "iam:CreatePolicy", "iam:AttachUserPolicy"],
      "Resource": "*"
    },
    {
      "Sid": "AllowServiceUsage",
      "Effect": "Allow",
      "Action": ["ec2:*", "s3:*", "logs:*"],
      "Resource": "*"
    }
  ]
}
```

Attach this document as a permission boundary on any role a delegated team
is allowed to create, so that even a role with an over-broad identity
policy cannot escalate beyond the boundary.

## Validation and Troubleshooting

- **Verify SCP effective permissions before rollout.** Use `aws
  organizations describe-effective-policy` (for Control Tower-managed
  guardrails) or the IAM Policy Simulator to confirm a new SCP does not
  accidentally block a required action; an overly broad `Deny` SCP can lock
  an entire OU out of a service until corrected by an Organizations
  management-account principal.
- **Confirm permission set provisioning propagated.** After
  `create-account-assignment`, run `aws sso-admin
  list-account-assignments` and confirm `PROVISIONING_STATUS` reaches
  `SUCCEEDED`; a `FAILED` status usually indicates the target account is
  suspended or was removed from the Organization.
- **Common failure: SCP vs. IAM policy confusion.** An `AccessDenied` error
  with no corresponding `Deny` statement in the caller's IAM policy is the
  classic signature of an SCP blocking the action; check the effective OU
  chain, not just the account's own IAM policies.
- **Common failure: stale permission set after policy edit.** Editing a
  permission set's attached policies does not retroactively update
  already-provisioned account roles. Run `aws sso-admin
  provision-permission-set --target-type ALL_PROVISIONED_ACCOUNTS` after
  every permission set change.
- **Verify account move did not orphan billing.** After `move-account`,
  confirm the account still reports through consolidated billing with `aws
  organizations describe-account` and that the destination OU's SCPs are
  now visible via `describe-effective-policy` from within the member
  account.

## Security and Best Practices

- Enforce MFA for every human Identity Center user and keep permission set
  session durations short (1–4 hours) for privileged permission sets;
  reserve longer sessions for low-privilege, read-only sets.
- Isolate the log-archive and security-tooling accounts from workload
  accounts; workload account administrators should have no ability to
  modify or delete centralized CloudTrail/Config data.
- Apply an SCP that denies leaving the Organization
  (`organizations:LeaveOrganization`) and denies disabling the
  organization's CloudTrail or Config recorder from every member account.
- Use permission boundaries on any role that a non-security team is allowed
  to create programmatically, preventing privilege escalation through
  self-authored IAM policies.
- Avoid `AdministratorAccess` as a standing permission set for engineering
  roles; prefer scoped managed or customer-managed policies plus a
  time-bound, logged elevation workflow for the rare cases that need
  broader access.
- Rotate and audit any IAM user access keys that must exist (legacy
  integrations) on a fixed schedule using `aws iam
  generate-credential-report`, and track the report for keys older than 90
  days.

## References and Knowledge Checks

**References**

- AWS Organizations documentation — organizational units, SCPs, and
  consolidated billing.
- AWS Control Tower documentation — landing zones, guardrails, and Account
  Factory.
- AWS IAM Identity Center documentation — permission sets and account
  assignments.
- AWS IAM documentation — policy evaluation logic, permission boundaries,
  and the IAM Policy Simulator.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this chapter maps to the identity, governance, and multi-account domains
  of the AWS Certified Solutions Architect and AWS Certified Security
  blueprints.

**Knowledge checks**

1. Why can a service control policy `Deny` statement not be overridden by
   an in-account IAM policy, even one attached to that account's
   administrator role?
2. What is the practical difference between a permission boundary and a
   service control policy?
3. Why should a log-archive account be isolated from the workload accounts
   whose logs it stores?
4. What does provisioning status `FAILED` on an Identity Center account
   assignment most commonly indicate?

## Hands-On Lab

**Objective:** Create an organizational unit, attach a Region-restriction
SCP, and verify the guardrail blocks out-of-Region resource creation.

**Cost implications:** AWS Organizations, OUs, and SCPs carry no direct
charge. This lab does not require creating a new member account; it applies
an SCP to an existing sandbox account's OU and uses only free-tier-eligible
API calls (`describe-vpcs`) to test the guardrail. Do not run this lab
against an OU containing production accounts.

**Prerequisites**

- An AWS Organizations management account, or delegated administrator
  access, with an existing OU you can safely attach a test SCP to (create a
  dedicated `Sandbox-Test` OU if none exists).
- AWS CLI v2 configured with a profile that has Organizations
  administrator permissions.

**Steps**

1. Create a test OU and confirm the "all features" Organizations mode is
   active (SCPs require it):

   ```bash
   aws organizations describe-organization --query "Organization.FeatureSet"
   ```

   **Expected result:** `"ALL"`.

2. Create the test OU:

   ```bash
   ROOT_ID=$(aws organizations list-roots --query "Roots[0].Id" --output text)
   aws organizations create-organizational-unit \
     --parent-id "$ROOT_ID" \
     --name "Sandbox-Test"
   ```

3. Write a Region-restriction SCP to a file:

   ```bash
   cat > scp-region-restrict.json <<'EOF'
   {
     "Version": "2012-10-17",
     "Statement": [{
       "Sid": "DenyOutsideUSEast1",
       "Effect": "Deny",
       "NotAction": ["iam:*", "organizations:*", "sts:*", "support:*"],
       "Resource": "*",
       "Condition": {
         "StringNotEquals": {"aws:RequestedRegion": "us-east-1"}
       }
     }]
   }
   EOF
   ```

4. Create and attach the policy:

   ```bash
   SANDBOX_OU_ID=$(aws organizations list-organizational-units-for-parent \
     --parent-id "$ROOT_ID" \
     --query "OrganizationalUnits[?Name=='Sandbox-Test'].Id" --output text)

   POLICY_ID=$(aws organizations create-policy \
     --name "region-restrict-sandbox" \
     --type SERVICE_CONTROL_POLICY \
     --content file://scp-region-restrict.json \
     --query "Policy.PolicySummary.Id" --output text)

   aws organizations attach-policy \
     --policy-id "$POLICY_ID" \
     --target-id "$SANDBOX_OU_ID"
   ```

   **Expected result:** No error; `aws organizations
   list-policies-for-target --target-id "$SANDBOX_OU_ID" --filter
   SERVICE_CONTROL_POLICY` lists `region-restrict-sandbox`.

5. Move a test account into the OU (use an existing sandbox account, not a
   production account):

   ```bash
   aws organizations move-account \
     --account-id <SANDBOX_ACCOUNT_ID> \
     --source-parent-id "$ROOT_ID" \
     --destination-parent-id "$SANDBOX_OU_ID"
   ```

6. From within the sandbox account (assume its role), verify the allowed
   Region works:

   ```bash
   aws ec2 describe-vpcs --region us-east-1
   ```

   **Expected result:** Normal JSON output listing VPCs.

7. **Negative test:** Attempt the same call against a non-approved Region:

   ```bash
   aws ec2 describe-vpcs --region eu-west-1
   ```

   **Expected result:** An `AccessDenied` (`UnauthorizedOperation` or
   explicit SCP-denial) error, confirming the guardrail blocks the
   out-of-Region call regardless of the account's own IAM policy.

8. **Cleanup:**

   ```bash
   aws organizations move-account \
     --account-id <SANDBOX_ACCOUNT_ID> \
     --source-parent-id "$SANDBOX_OU_ID" \
     --destination-parent-id "$ROOT_ID"

   aws organizations detach-policy \
     --policy-id "$POLICY_ID" \
     --target-id "$SANDBOX_OU_ID"

   aws organizations delete-policy --policy-id "$POLICY_ID"

   aws organizations delete-organizational-unit --organizational-unit-id "$SANDBOX_OU_ID"

   rm -f scp-region-restrict.json
   ```

   Confirm removal with `aws organizations
   list-organizational-units-for-parent --parent-id "$ROOT_ID"`; the
   `Sandbox-Test` OU must no longer appear.

## Summary and Completion Checklist

AWS Organizations and organizational units give a platform team a single
place to enforce guardrails through service control policies, which cap
maximum permissions regardless of any account's own IAM configuration. IAM
users, roles, resource-based policies, and permission boundaries each solve
a distinct authorization problem, and IAM Identity Center federates human
access across accounts through short-lived permission sets rather than
long-lived per-account credentials. AWS Control Tower automates the
landing-zone baseline — OU structure, log-archive/audit accounts, and
guardrails — and is the recommended starting point for a new enterprise
multi-account environment.

- [ ] Can design an OU structure organized by environment and blast radius.
- [ ] Can write and attach a service control policy and explain why it
      cannot be overridden by in-account IAM.
- [ ] Can distinguish identity-based, resource-based, and boundary policies
      and choose correctly among them.
- [ ] Can configure an IAM Identity Center permission set and account
      assignment.
- [ ] Completed the hands-on lab, including the negative test and cleanup.
