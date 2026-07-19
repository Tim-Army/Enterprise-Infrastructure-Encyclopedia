# Chapter 08: Cloud Governance, Security, and FinOps

![Lab flow for this chapter: two conftest policies — an encryption requirement and a required-cost-tags rule — evaluate simulated resource inventories; inventory-compliant.json (encrypted and fully tagged) passes both policies with zero failures, while inventory-noncompliant.json (unencrypted, missing tags) fails with two findings. As a negative test, inventory-out-of-scope.json (a log_group resource type neither policy governs) passes cleanly, confirming CSPM and tag-governance policies scoped to specific resource types do not produce false positives against resource types outside their intended scope.](../../../diagrams/volume-07-cloud-infrastructure/chapter-08-cspm-cost-tag-policy-flow.svg)

*Figure 8-1. Flow used throughout this chapter's Hands-On Lab: CSPM-style encryption and cost-tag governance policies evaluated against simulated resource inventories.*

## Learning Objectives

- Design a cloud security posture management practice that continuously
  evaluates configuration against a defined benchmark, rather than
  auditing only at point-in-time reviews.
- Map cloud compliance obligations to shared-responsibility boundaries and
  provider attestations, and explain what an attestation does and does not
  cover.
- Explain the FinOps operating model (Inform, Optimize, Operate) and apply
  it to a cost-accountability problem.
- Design a cost allocation and showback/chargeback mechanism using tagging
  and account/subscription structure.
- Evaluate commitment-discount strategy (reserved/committed-use coverage
  and utilization) as an ongoing optimization practice.
- Implement automated cost and security posture guardrails as code and
  validate their enforcement.

## Theory and Architecture

### Cloud security posture management

Cloud security posture management (CSPM) is the continuous practice of
evaluating deployed cloud configuration against a defined security
benchmark and surfacing drift — distinct from a point-in-time audit,
which only reflects the environment's state at the moment it was
reviewed. A cloud environment's rate of change (new resources created
through self-service pipelines, configuration changed through automation)
makes point-in-time review alone insufficient: a resource compliant at
last quarter's audit can drift out of compliance the same afternoon
through a routine, individually reasonable change. CSPM tooling
continuously inventories deployed resources, evaluates them against a
benchmark (commonly a CIS Benchmark for the specific provider, or an
organization's own policy-as-code rule set from [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md)), and reports
or remediates findings on an ongoing basis rather than a periodic cycle.

### Compliance mapping and shared responsibility

A compliance framework (PCI DSS, HIPAA, SOC 2, ISO 27001, or a
sector-specific regulation) applies to the *system as operated*, not to
the cloud provider in isolation. A provider's compliance attestation
(commonly delivered as a SOC 2 Type II report or an ISO 27001
certification covering the provider's own infrastructure and services)
demonstrates that the provider's portion of the shared responsibility
boundary (established in [Chapter 01](01-cloud-operating-models-and-architecture-foundations.md)) meets the framework's control
objectives — it says nothing about whether the customer's configuration
of identity, network exposure, data handling, and application logic on
top of that infrastructure also meets them. Treat a provider attestation
as a necessary input to a compliance program, never as the compliance
program itself; map each control in the target framework explicitly to
either "satisfied by provider attestation" or "customer-owned, evidenced
by [specific control]," and keep that mapping current as services and
configuration change.

### The FinOps operating model

FinOps is the operating discipline that brings financial accountability
to the variable, consumption-based spending model cloud introduces
(established in [Chapter 01](01-cloud-operating-models-and-architecture-foundations.md)'s cloud economics discussion). The FinOps
Foundation's model organizes the discipline into three iterative phases:

1. **Inform** — establish visibility: allocate every cost to an owning
   team or workload (via the tagging and account structure covered
   below), benchmark spend against budget and against unit economics
   (cost per transaction, per customer, or per workload), and make that
   visibility available to the engineering teams actually generating the
   cost, not only to finance.
2. **Optimize** — act on that visibility: right-size resources (Chapter
   05), apply the correct storage tier and database instance class
   ([Chapter 06](06-cloud-storage-databases-and-data-services.md)), eliminate idle or orphaned resources, and increase
   commitment-discount coverage for well-understood steady-state demand.
3. **Operate** — operationalize the first two phases as a continuous,
   cross-functional practice: define who owns cost anomaly response, set
   budget alerting thresholds, incorporate cost review into the same
   design-review and change-management processes used for reliability and
   security, and revisit the cycle continuously rather than treating
   optimization as a one-time project.

FinOps is explicitly a cross-functional practice, not a finance-only
function or an engineering-only function — its central premise is that
engineers, who make the technical decisions that drive cost, need direct,
timely cost visibility to make good trade-offs, and finance needs
engineering-informed forecasting rather than a black-box monthly invoice.

### Cost allocation: tagging and account structure

Two complementary mechanisms make cost allocation possible:

- **Tagging/labeling** — every resource is tagged with attributes
  (environment, owning team, cost center, workload) at creation time,
  enforced through the same policy-as-code guardrails introduced in
  [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md). Tags enable granular showback (reporting cost by owner
  without a billing consequence) and chargeback (actually billing the
  cost back to the owning team's budget) at the resource level, within a
  shared account.
- **Account/subscription structure** — the resource hierarchy from
  [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md) provides a coarser, structurally enforced cost boundary:
  every resource in a given account or subscription is unambiguously
  attributable to whatever that account represents (a business unit, an
  environment), without depending on tag hygiene being perfect.

Neither mechanism alone is sufficient at scale: account-level allocation
is too coarse for shared or multi-tenant accounts, and tag-only allocation
degrades whenever tag enforcement lapses (an unretagged resource becomes
unallocated cost, colloquially "cost in the shadows"). Combine both:
account structure for the coarse, structurally guaranteed boundary, and
enforced tagging for granular attribution within it.

### Commitment-discount strategy as an ongoing practice

Reserved and committed-use discount instruments (introduced in [Chapter 05](05-cloud-compute-and-workload-placement.md)
for compute, and applicable to several other service categories) require
two ongoing metrics to manage well, not just a one-time purchase decision:

- **Coverage** — what percentage of actual eligible usage is covered by
  an active commitment, versus paying the higher on-demand rate. Low
  coverage on a stable, well-understood workload represents savings left
  unrealized.
- **Utilization** — what percentage of a purchased commitment's capacity
  is actually being consumed. Low utilization means the organization is
  paying for committed capacity it is not using, which is worse than
  paying on-demand for that same unused portion, since the commitment
  cost is fixed regardless of use.

Track both metrics continuously and adjust the commitment portfolio as
workload demand shape changes — a commitment strategy is a living
portfolio to manage, not a purchase to make once during initial cloud
adoption and revisit only at renewal.

### Preventive and detective guardrails applied to cost

The guardrail model from [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md) extends directly to cost governance:
preventive cost controls (a policy blocking creation of an
instance family known to be inappropriate for the workload, or requiring
a cost-center tag before resource creation succeeds) and detective cost
controls (a budget alert firing when spend exceeds a threshold, an
anomaly-detection system flagging an unusual spend pattern) work together
the same way preventive and detective security guardrails do — prevent
what can safely be prevented, detect the rest, and route detected findings
to an accountable owner.

## Design Considerations

### Scoping a CSPM benchmark

Adopt an established benchmark (a CIS Benchmark for the relevant provider,
or a framework-specific control set) as the starting point rather than
building a bespoke rule set from nothing, and layer organization-specific
rules (from the landing zone guardrails in [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md)) on top for
requirements the generic benchmark does not cover. Avoid enabling every
available benchmark rule indiscriminately at full enforcement from day
one — the progressive rollout discipline from [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md) (detective mode
first, burn-in, then enforcing) applies directly to CSPM rule rollout as
well.

### Building and maintaining the compliance control map

Treat the compliance control-to-evidence map as a living artifact owned
jointly by security/compliance and the platform engineering team, updated
whenever a new service is adopted or an existing control's implementation
changes — not a document produced once for an audit and then left stale
until the next one. A stale control map is a common source of audit
findings that have nothing to do with the actual state of the
environment, only with the documentation lagging behind it.

### Choosing showback vs. chargeback

Showback (visible cost attribution with no budget consequence) is
lower-friction to introduce and is the right starting point for an
organization new to cost accountability; chargeback (cost actually
debited against an owning team's budget) creates stronger behavioral
incentive toward optimization but requires cost allocation accuracy and
organizational buy-in mature enough to support disputes over shared or
misallocated cost. Introduce chargeback only after tag/account allocation
accuracy has been validated over a sustained period under showback,
otherwise chargeback disputes over allocation accuracy will undermine
trust in the entire cost-accountability program.

### Commitment risk tolerance

Longer commitment terms and broader-scope commitment instruments
generally offer deeper discounts in exchange for less flexibility.
Calibrate commitment term and scope to the organization's actual
confidence in a workload's multi-year demand trajectory — over-committing
against a workload facing an architecture change (a planned migration to
a different instance family, or to a managed service that removes the
underlying compute entirely) locks in cost for capacity that will not be
used as planned.

### Balancing security and cost guardrails against velocity

Both security and cost guardrails, applied too aggressively as preventive
controls, create friction that pushes teams toward workarounds
(shadow IT, undocumented exceptions) that undermine the guardrail's
purpose more than a well-calibrated detective control would have. Apply
the same preventive/detective/responsive triage from [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md) to cost
guardrails specifically: prevent the small set of clearly indefensible
patterns (an unbounded instance size with no approval, a public storage
bucket), and handle the long tail of optimization opportunities
detectively, routed to owning teams as actionable, specific findings.

## Implementation and Automation

### CSPM finding evaluated as policy-as-code

```rego
# policy/encryption_required.rego — illustrative CSPM-style detective rule,
# evaluated against a periodic resource inventory export (not a plan).
package main

deny[msg] {
  resource := input.resources[_]
  resource.type == "storage_bucket"
  resource.encryption_enabled == false
  msg := sprintf("%s has encryption disabled, violating baseline security posture", [resource.id])
}

deny[msg] {
  resource := input.resources[_]
  resource.type == "managed_database"
  resource.storage_encrypted == false
  msg := sprintf("%s has unencrypted storage, violating baseline security posture", [resource.id])
}
```

### Enforced tagging as a preventive cost/governance guardrail

```hcl
# policy/required_cost_tags.tf — illustrative provider-neutral policy
# resource requiring cost-allocation tags at creation time.
resource "cloud_policy" "require_cost_tags" {
  name  = "require-cost-allocation-tags"
  scope  = var.organization_root_id
  effect = "deny"

  condition {
    missing_any_of_tags = ["cost_center", "owner", "environment"]
  }

  # Rolled out in audit/detective mode first per Chapter 02's guardrail
  # rollout discipline; flip enforcement_mode to "deny" only after burn-in.
  enforcement_mode = "audit"
}
```

### Budget alert as a detective cost guardrail

```hcl
# budgets.tf — illustrative budget with staged alert thresholds.
resource "cloud_budget" "payments_prod" {
  name          = "payments-prod-monthly"
  scope         = var.payments_prod_account_id
  amount_monthly    = 50000

  alert_threshold {
    percentage = 80
    notify     = ["payments-team-lead@example.com"]
  }
  alert_threshold {
    percentage = 100
    notify     = ["payments-team-lead@example.com", "finops@example.com"]
  }
  alert_threshold {
    percentage    = 120
    notify        = ["finops@example.com", "engineering-director@example.com"]
    trigger_incident = true
  }
}
```

### Commitment coverage and utilization reporting (illustrative)

```bash
#!/usr/bin/env bash
# commitment-health-check.sh — illustrative coverage/utilization report.
set -euo pipefail

COVERAGE=$(cloud-cli billing get-commitment-coverage --scope "payments-prod")
UTILIZATION=$(cloud-cli billing get-commitment-utilization --scope "payments-prod")

echo "Commitment coverage: ${COVERAGE}%"
echo "Commitment utilization: ${UTILIZATION}%"

if (( $(echo "$UTILIZATION < 85" | bc -l) )); then
  echo "WARNING: utilization below 85% target — review commitment sizing." >&2
fi
if (( $(echo "$COVERAGE < 70" | bc -l) )); then
  echo "NOTICE: coverage below 70% target — evaluate additional commitment purchase for stable baseline." >&2
fi
```

## Validation and Troubleshooting

- **Diagnose a CSPM finding by checking whether it is a true positive
  against current intent first**, not by immediately remediating — a
  benchmark rule occasionally flags a deliberate, documented exception
  (a specific public bucket serving static assets, for example); confirm
  against the resource's documented purpose before treating every finding
  as an incident.
- **Diagnose an unexpectedly large "unallocated" cost bucket** by
  auditing for resources missing required tags first — this is usually a
  tagging enforcement gap (a preventive policy rolled out in audit mode
  and never flipped to enforcing, or a resource type the policy does not
  yet cover), not a billing system error.
- **Investigate low commitment utilization by workload, not in
  aggregate** — an aggregate utilization number can look acceptable while
  masking a specific overcommitted workload offset by an undercommitted
  one; review coverage and utilization per workload or account.
- **Validate that a compliance control's evidence still reflects current
  configuration** on the same cadence as CSPM findings are reviewed, not
  only immediately before an audit — a control map update process that
  only runs pre-audit produces stale evidence for the majority of the
  year.
- **Test budget alert thresholds by intentionally exceeding a test
  budget's low threshold in a non-production account**, confirming the
  notification actually reaches the intended recipient, rather than
  trusting the configuration without having observed a real alert fire.

## Security and Best Practices

- Run CSPM continuously against a recognized benchmark, layered with
  organization-specific policy from [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md), and route findings to the
  owning team with enough context to act, not just a resource ID.
- Maintain the compliance control-to-evidence map as a living document
  updated on every material service or configuration change, with
  explicit ownership assigned.
- Treat cost governance guardrails with the same preventive/detective
  triage discipline as security guardrails — prevent only clearly
  indefensible patterns, and route the long tail detectively to avoid
  driving teams toward workarounds.
- Require enforced, policy-validated tagging as a precondition for
  resource creation wherever the platform can enforce it, since accurate
  cost and ownership attribution is itself a security control (it is
  what makes "who owns this resource and why does it still exist"
  answerable during an incident).
- Review commitment-discount coverage and utilization on a recurring
  schedule as part of the standing FinOps Operate phase, not only at
  contract renewal.
- Alert on guardrail and budget policy changes themselves, consistent
  with the guidance in [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md) — a weakened cost or security guardrail
  is frequently the actual finding, not a side effect of one.

## References and Knowledge Checks

### References

- CIS Benchmarks (Center for Internet Security), for provider-specific
  security configuration baselines.
- FinOps Foundation, *FinOps Framework* (Inform, Optimize, Operate
  phases).
- AICPA SOC 2 Trust Services Criteria, for the shape of a typical provider
  attestation.
- Each major provider's compliance attestation and CSPM/security-posture
  service documentation — consult the current vendor source.
- `SOFTWARE_VERSIONS.md` in this repository for the Terraform baseline.

### Knowledge checks

1. A provider holds a current SOC 2 Type II attestation. What does this
   confirm, and what does it explicitly not confirm about a specific
   customer workload's compliance posture?
2. Explain why point-in-time compliance audits are insufficient on their
   own in a cloud environment, and what CSPM adds.
3. A commitment instrument shows 95% utilization but only 40% coverage.
   What does this combination indicate, and what action does it suggest?
4. Why should chargeback typically be introduced only after a sustained
   period of accurate showback, rather than immediately?
5. Give an example of a cost guardrail that should be preventive and one
   that should be detective, and justify the difference using the same
   reasoning applied to security guardrails in [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md).

## Hands-On Lab

### Lab 8.1 — CSPM policy evaluation and cost-tag enforcement with conftest

This lab evaluates a simulated resource inventory against a CSPM-style
encryption policy and a required-tags cost-governance policy using
`conftest`, entirely on the local filesystem. No cloud account or
credentials are required.

**Prerequisites**

- `conftest` installed (validated against the `conftest` 0.5x series).
- A POSIX shell and `jq`.

**Steps**

1. Create the lab directory and policy subdirectory:

   ```bash
   mkdir -p ~/labs/vol07-ch08/policy && cd ~/labs/vol07-ch08
   ```

2. Save the encryption policy from this chapter's Implementation and
   Automation section to `policy/encryption_required.rego`.

3. Create `policy/required_cost_tags.rego`:

   ```rego
   package main

   required_tags := {"cost_center", "owner", "environment"}

   deny[msg] {
     resource := input.resources[_]
     provided := {k | resource.tags[k]}
     missing := required_tags - provided
     count(missing) > 0
     msg := sprintf("%s is missing required cost-allocation tags: %v", [resource.id, missing])
   }
   ```

4. Create a **compliant** inventory snapshot at `inventory-compliant.json`:

   ```json
   {
     "resources": [
       {
         "id": "storage_bucket.reports",
         "type": "storage_bucket",
         "encryption_enabled": true,
         "tags": { "cost_center": "cc-4471", "owner": "data-platform", "environment": "prod" }
       },
       {
         "id": "managed_database.orders",
         "type": "managed_database",
         "storage_encrypted": true,
         "tags": { "cost_center": "cc-4471", "owner": "payments-team", "environment": "prod" }
       }
     ]
   }
   ```

5. Create a **noncompliant** inventory snapshot at
   `inventory-noncompliant.json`:

   ```json
   {
     "resources": [
       {
         "id": "storage_bucket.legacy-exports",
         "type": "storage_bucket",
         "encryption_enabled": false,
         "tags": { "owner": "data-platform" }
       }
     ]
   }
   ```

6. Evaluate the compliant inventory:

   ```bash
   conftest test inventory-compliant.json --policy policy
   ```

   **Expected result:** `PASS` with zero failures across both policies.

7. Evaluate the noncompliant inventory:

   ```bash
   conftest test inventory-noncompliant.json --policy policy
   ```

   **Expected result:** `FAIL` with two findings: an encryption-disabled
   violation for `storage_bucket.legacy-exports`, and a missing-tags
   violation listing `cost_center` and `environment` as missing.
   Confirm the nonzero exit code with `echo $?` (prints `1`).

**Negative test**

8. Confirm the encryption policy correctly ignores resource types it does
   not govern by adding an unrelated, fully untagged resource type to a
   new file, `inventory-out-of-scope.json`:

   ```json
   {
     "resources": [
       { "id": "log_group.app", "type": "log_group", "retention_days": 30 }
     ]
   }
   ```

   Run `conftest test inventory-out-of-scope.json --policy policy`.

   **Expected result:** `PASS` — neither policy rule matches a
   `log_group` resource type, demonstrating that CSPM and tag-governance
   policies scoped to specific resource types do not produce false
   positives against resource types outside their intended scope.

**Cleanup**

9. Remove the lab directory:

   ```bash
   cd ~ && rm -rf ~/labs/vol07-ch08
   ```

   **Expected result:** The directory no longer exists. No cloud
   resources, budgets, or commitments were created at any point in this
   lab.

## Summary and Completion Checklist

Cloud governance, security, and FinOps share the same underlying pattern
established in [Chapter 02](02-landing-zones-resource-organization-and-guardrails.md): continuous, policy-as-code evaluation against
a defined benchmark, preferring prevention where it is safe and detection
everywhere else, with findings routed to an accountable owner. This
chapter applied that pattern to continuous security posture management,
compliance control mapping against the shared responsibility model, and
the FinOps Inform/Optimize/Operate cycle, including cost allocation
through tagging and account structure and ongoing commitment-discount
coverage and utilization management. [Chapter 09](09-cloud-automation-observability-resilience-and-lifecycle-operations.md) completes the volume with
the automation, observability, resilience, and lifecycle operations
practices that keep all of this running day to day.

- [ ] Can explain why continuous CSPM is necessary in addition to
      point-in-time compliance audits.
- [ ] Can map a compliance control to either provider attestation or
      customer-owned evidence, and explain the difference.
- [ ] Can describe the FinOps Inform/Optimize/Operate cycle and apply it
      to a cost-accountability scenario.
- [ ] Can distinguish coverage from utilization for a commitment-discount
      instrument and diagnose a mismatch between them.
- [ ] Completed Lab 8.1, including the negative test and cleanup.
