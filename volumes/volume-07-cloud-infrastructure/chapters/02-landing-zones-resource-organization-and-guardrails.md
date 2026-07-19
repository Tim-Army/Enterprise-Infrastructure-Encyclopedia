# Chapter 02: Landing Zones, Resource Organization, and Guardrails

![Lab flow for this chapter: policy/required_tags.rego is evaluated with conftest against two sample Terraform plan representations; plan-compliant.json (a create action with all required tags) passes with zero failures, while plan-noncompliant.json (missing cost_center) fails, reporting the resource address and the missing tag with a nonzero exit code. As a negative test, plan-delete.json — a delete-only action with no tags at all — still passes, because the policy is intentionally scoped to evaluate only create actions, avoiding unnecessary friction against untagged legacy resources being removed.](../../../diagrams/volume-07-cloud-infrastructure/chapter-02-conftest-required-tags-flow.svg)

*Figure 2-1. Flow used throughout this chapter's Hands-On Lab: a policy-as-code guardrail evaluating a Terraform plan for required tags, correctly scoped to create actions only.*

## Learning Objectives

- Define a cloud landing zone and enumerate the components a production-ready
  landing zone must provide before the first workload is onboarded.
- Design a resource hierarchy (organization, folder/management-group,
  account/subscription/project, resource group) that maps to organizational
  and billing boundaries.
- Distinguish preventive, detective, and responsive guardrails, and choose
  the appropriate control type for a given risk.
- Implement policy as code using a generic policy engine and interpret a
  policy evaluation failure.
- Design a multi-account/subscription vending process that is repeatable and
  auditable.
- Explain how landing zone guardrails interact with the shared
  responsibility model introduced in [Chapter 01](01-cloud-operating-models-and-architecture-foundations.md).

## Theory and Architecture

### What a landing zone is

A landing zone is the pre-provisioned, governed environment a workload lands
into — it is not a single resource but a coordinated set of foundational
capabilities established before any application team requests an account or
project:

- A **resource hierarchy** that maps organizational, billing, and
  environment boundaries to the provider's native grouping constructs.
- **Identity foundations** (federation, baseline roles) — detailed in
  [Chapter 03](03-cloud-identity-access-and-cryptographic-services.md).
- **Network foundations** (hub connectivity, DNS, shared services) —
  detailed in [Chapter 04](04-cloud-networking-and-hybrid-connectivity.md).
- **Guardrails** — preventive and detective policy enforced across every
  account/project/subscription in the hierarchy.
- **Logging and monitoring foundations** that centralize audit and
  operational telemetry outside the reach of any single workload team.
- A **vending process** (self-service or ticket-driven) that provisions a
  new account/project pre-configured with all of the above.

Every major provider ships an opinionated reference implementation of this
pattern under a different name (landing zone accelerators, management group
hierarchies, resource manager hierarchies). The underlying architecture —
hierarchy, guardrails, shared services, vending — is consistent enough to
treat as a single provider-neutral model; provider-specific automation for
deploying it is out of scope for this volume.

### Resource hierarchy

A typical hierarchy has four logical levels, named differently per provider:

| Level | Purpose | Common provider terms |
| --- | --- | --- |
| Root/organization | Single trust and billing root; where organization-wide policy is anchored | Organization, tenant root |
| Grouping layer | Groups accounts/projects by environment, business unit, or compliance scope; policy inheritance point | Organizational unit, management group, folder |
| Billing/isolation boundary | The actual security and billing isolation boundary; most policy and IAM is scoped here | Account, subscription, project |
| Resource grouping | Logical grouping of resources within a boundary for lifecycle and access management | Resource group, resource folder, tag-based grouping |

Design the grouping layer around two axes simultaneously where possible:
**environment** (sandbox, dev, test, stage, prod) and **workload/business
unit**. A common pattern nests environment under business unit (or vice
versa) so that policy can be inherited coarsely (all prod accounts get the
strict policy set) while billing can still roll up by business unit for
chargeback. Avoid a single flat layer of accounts with no grouping — it
forces every policy to be assigned individually and does not scale past a
handful of accounts.

### Preventive, detective, and responsive guardrails

- **Preventive guardrails** block a noncompliant action before it takes
  effect — for example, a policy that rejects an API call attempting to
  create a publicly readable storage bucket. Preventive controls are the
  strongest guarantee but must be scoped carefully to avoid blocking
  legitimate work; they are best applied to a small set of
  high-consequence, low-legitimate-use actions.
- **Detective guardrails** evaluate resources after creation and report or
  remediate noncompliance — for example, a periodic scan that flags any
  encryption-at-rest setting that has drifted from policy. Detective
  controls are more flexible and easier to roll out broadly, at the cost of
  a window of noncompliance between creation and detection.
- **Responsive guardrails** trigger an automated action in reaction to an
  event — for example, automatically quarantining a credential detected in
  a public code repository. Responsive controls close the gap detective
  controls leave open but require reliable event delivery and a safe,
  well-tested remediation action (an overly aggressive auto-remediation is
  itself an incident risk).

Combine all three: prevent what can safely be prevented, detect everything
in scope for policy, and respond automatically only to the subset of
findings where an automated action is unambiguously safe.

### Policy as code

Guardrails should be expressed as code, versioned, tested, and deployed
through the same pipeline discipline as application infrastructure — not as
manually configured settings in a console. A policy-as-code engine
typically evaluates one of two inputs:

1. **A resource manifest before it is created** (a Terraform plan, an
   admission request) — enabling preventive enforcement.
2. **The actual state of deployed resources** (a periodic inventory export)
   — enabling detective enforcement.

The Open Policy Agent (OPA) project and its `conftest` companion tool are a
widely used, provider-neutral example of this pattern: policies are written
in the Rego language and evaluated against structured JSON or YAML input,
regardless of which cloud produced that input. This chapter's lab uses
`conftest` for that reason — the pattern transfers directly to whichever
provider-native or third-party policy engine an organization standardizes
on.

### Multi-account/subscription vending

A landing zone's value compounds through repeatability. A vending process
should be triggerable through a request (self-service form, pull request, or
ticket) and produce, without manual console work:

1. A new account/subscription/project created inside the correct hierarchy
   position.
2. Baseline identity federation and break-glass access configured.
3. Baseline network connectivity to shared services established.
4. The organization's guardrail policy set attached (inherited or
   explicitly applied).
5. Logging and monitoring pipelines wired to the central platform.
6. Cost allocation tags/labels and budget alerts configured.

Every step above should be defined in code so that account creation is
idempotent, auditable, and identical whether it is the first account vended
or the five hundredth.

## Design Considerations

### How many boundaries is too many

Each additional account/subscription/project boundary improves blast-radius
isolation and simplifies billing attribution, but adds cross-boundary
networking, identity federation, and shared-service replication cost. A
common failure mode is either a single flat account holding every workload
(no isolation, brittle blast radius) or an account-per-microservice sprawl
that multiplies the operational surface area of every guardrail and network
peering decision. Start from environment and compliance-scope boundaries
(these almost always justify a hard boundary), and only split further along
team or workload lines when the isolation benefit is concrete — a distinct
compliance obligation, a genuinely independent blast radius requirement, or
a genuinely independent budget owner.

### Policy inheritance vs. explicit assignment

Hierarchical policy inheritance (attach once at the grouping layer, apply to
every descendant account) reduces management overhead but makes the
effective policy on any single account harder to reason about without
tooling, since it is the union of everything inherited plus anything
applied locally. Maintain an "effective policy" reporting capability (native
to the provider or built on top of the policy engine) so that "what rules
actually apply to this account right now" is always answerable in one query,
not by walking the hierarchy by hand.

### Preventive control blast radius

A preventive control deployed at the wrong scope (for example, at the
organization root instead of a specific environment grouping) can halt
legitimate work across the entire estate simultaneously. Roll out new
preventive controls in detective (report-only) mode first, review the
findings against real traffic for a defined burn-in period, and only then
flip to enforcing mode — the same progressive-rollout discipline applied to
any other high-blast-radius change.

### Sandbox and break-glass design

Provide a genuinely isolated sandbox tier (its own account/subscription,
minimal guardrails, no path to production data or networks) so that
engineers can learn provider services without a change-management process
gating experimentation, and a break-glass access path for emergencies that
bypasses normal approval flow but is fully logged and automatically
time-boxed and reviewed after use.

## Implementation and Automation

### Representing the hierarchy as code

Model the account hierarchy itself as data, not as a fixed set of Terraform
resources, so that adding an account is a data change reviewed through a
pull request rather than a module edit:

```hcl
# accounts.auto.tfvars.json — illustrative; provider resource types vary.
{
  "accounts": [
    { "name": "platform-shared-services", "group": "platform", "env": "prod" },
    { "name": "payments-prod",            "group": "payments", "env": "prod" },
    { "name": "payments-nonprod",         "group": "payments", "env": "nonprod" }
  ]
}
```

```hcl
# main.tf — illustrative provider-neutral vending loop.
variable "accounts" {
  type = list(object({
    name  = string
    group = string
    env   = string
  }))
}

resource "cloud_account" "vended" {
  for_each = { for a in var.accounts : a.name => a }

  name        = each.value.name
  parent_group = each.value.group
  tags = {
    environment = each.value.env
    managed_by  = "landing-zone-pipeline"
  }
}
```

### Expressing a guardrail as a Rego policy

The following policy, evaluated with `conftest`, denies any planned resource
missing a required tag set — a preventive control run against a Terraform
plan's JSON representation before `apply`:

```rego
# policy/required_tags.rego
package main

required_tags := {"environment", "owner", "cost_center"}

deny[msg] {
  resource := input.resource_changes[_]
  resource.change.actions[_] == "create"
  provided := {k | resource.change.after.tags[k]}
  missing := required_tags - provided
  count(missing) > 0
  msg := sprintf("%s is missing required tags: %v", [resource.address, missing])
}
```

This same pattern extends to detective use by pointing `conftest` at a JSON
export of already-deployed resource inventory instead of a plan file — the
policy logic does not need to change, only the input source.

## Validation and Troubleshooting

- **Validate hierarchy placement, not just existence.** An account created
  outside its intended grouping silently inherits the wrong policy set;
  reconcile the live hierarchy against the code-defined intent on a schedule,
  not only at creation time.
- **Test guardrails against both a compliant and a noncompliant sample
  before rollout.** A policy that never fires on real input has not been
  validated, regardless of how confident the author is in the Rego logic.
- **Diagnose an unexpected policy denial by requesting the effective policy
  set for the specific account**, not just the policy that was most recently
  changed — inherited policy from a parent grouping is a common source of
  "but I didn't set that rule" incidents.
- **Watch for guardrail drift after a hierarchy reorganization.** Moving an
  account to a new grouping changes its inherited policy immediately; treat
  hierarchy moves as a change with the same review rigor as a policy edit.
- **Track vending pipeline failures as production incidents.** A landing
  zone whose automated vending path is broken silently reverts the
  organization to manual, inconsistent account creation.

## Security and Best Practices

- Enforce the highest-consequence controls (public data exposure, disabling
  audit logging, removing the break-glass path) as preventive controls;
  everything else can start detective and tighten over time.
- Never grant standing access that bypasses guardrails for routine work;
  reserve unguarded access for the explicitly logged, time-boxed
  break-glass path.
- Keep the policy-as-code repository under the same change review and branch
  protection as application code — a guardrail is a security control, and
  its source should receive at least the same scrutiny as the resources it
  governs.
- Alert on guardrail policy changes themselves, in addition to alerting on
  policy violations — a weakened guardrail is often the actual incident, not
  a side effect of one.
- Periodically test that break-glass access still works end to end; an
  emergency path that has silently broken is discovered at the worst
  possible time.

## References and Knowledge Checks

### References

- Open Policy Agent documentation (openpolicyagent.org) and the `conftest`
  project documentation, for the policy-as-code pattern used in this
  chapter's lab.
- Each major provider's landing zone or resource-hierarchy reference
  architecture documentation — consult the current vendor source for
  provider-specific implementation detail.
- `SOFTWARE_VERSIONS.md` in this repository for the Terraform baseline.

### Knowledge checks

1. Why does a flat, single-layer account structure fail to scale past a
   small number of accounts, even if each individual account is well
   configured?
2. Give an example of a control that should be preventive and one that
   should be detective, and justify the difference.
3. A newly vended account shows an unexpected policy in effect. What two
   places would you check to find the source before assuming the policy
   engine is malfunctioning?
4. Why should a new preventive control be deployed in detective/report-only
   mode before it is switched to enforcing?
5. What specific risk does an untested break-glass path create, and how
   would you catch that risk before an actual emergency?

## Hands-On Lab

### Lab 2.1 — Policy-as-code guardrail evaluation with conftest

This lab evaluates a sample Terraform plan against a required-tags guardrail
policy using `conftest`, entirely on the local filesystem. No cloud account
or credentials are required.

**Prerequisites**

- `conftest` installed (a single static binary — see the project's
  installation instructions for your OS; this lab was validated against the
  `conftest` 0.5x series).
- `jq` installed for inspecting JSON output.
- A POSIX shell.

**Steps**

1. Create the lab directory and a policy subdirectory:

   ```bash
   mkdir -p ~/labs/vol07-ch02/policy && cd ~/labs/vol07-ch02
   ```

2. Save the guardrail policy from this chapter to `policy/required_tags.rego`
   (use the exact contents from the Implementation and Automation section
   above).

3. Create a **compliant** sample plan representation at
   `plan-compliant.json`:

   ```json
   {
     "resource_changes": [
       {
         "address": "cloud_storage_bucket.reports",
         "change": {
           "actions": ["create"],
           "after": {
             "tags": {
               "environment": "prod",
               "owner": "data-platform",
               "cost_center": "cc-4471"
             }
           }
         }
       }
     ]
   }
   ```

4. Create a **noncompliant** sample plan representation at
   `plan-noncompliant.json` (missing `cost_center`):

   ```json
   {
     "resource_changes": [
       {
         "address": "cloud_storage_bucket.reports",
         "change": {
           "actions": ["create"],
           "after": {
             "tags": {
               "environment": "prod",
               "owner": "data-platform"
             }
           }
         }
       }
     ]
   }
   ```

5. Evaluate the compliant plan:

   ```bash
   conftest test plan-compliant.json --policy policy
   ```

   **Expected result:** `PASS` with zero failures reported.

6. Evaluate the noncompliant plan:

   ```bash
   conftest test plan-noncompliant.json --policy policy
   ```

   **Expected result:** `FAIL`, with a message equivalent to
   `cloud_storage_bucket.reports is missing required tags: {"cost_center"}`
   and a nonzero exit code — confirm with `echo $?` immediately after,
   which should print `1`.

**Negative test**

7. Confirm the policy correctly ignores non-create actions by adding a
   `"delete"`-only resource change with no tags at all to a new file,
   `plan-delete.json`, and re-running `conftest test plan-delete.json
   --policy policy`.

   **Expected result:** `PASS` — the policy only evaluates `create` actions,
   demonstrating that a guardrail scoped too broadly (for example, blocking
   deletions on untagged legacy resources) would create unnecessary friction;
   this policy is intentionally scoped to prevent only new noncompliant
   creation.

**Cleanup**

8. Remove the lab directory:

   ```bash
   cd ~ && rm -rf ~/labs/vol07-ch02
   ```

   **Expected result:** The directory and all sample files and policies no
   longer exist. No cloud resources were created at any point in this lab.

## Summary and Completion Checklist

A landing zone is the coordinated set of hierarchy, identity, network,
guardrail, logging, and vending capabilities a workload inherits before it
is created — not a single account or a single policy. This chapter covered
how to design a resource hierarchy that maps to real organizational and
billing boundaries, the difference between preventive, detective, and
responsive guardrails, how to express guardrails as version-controlled
policy as code, and how to design a repeatable account-vending process.
[Chapter 03](03-cloud-identity-access-and-cryptographic-services.md) builds the identity foundation this landing zone assumes, and
[Chapter 08](08-cloud-governance-security-and-finops.md) returns to policy as code at the governance and FinOps level.

- [ ] Can describe the four-level resource hierarchy pattern and map it to
      at least one real provider's terminology.
- [ ] Can classify a given control as preventive, detective, or responsive
      and justify the classification.
- [ ] Can write and evaluate a basic policy-as-code rule against both a
      compliant and noncompliant input.
- [ ] Can describe the minimum set of steps a repeatable account-vending
      pipeline must automate.
- [ ] Completed Lab 2.1, including the negative test and cleanup.
