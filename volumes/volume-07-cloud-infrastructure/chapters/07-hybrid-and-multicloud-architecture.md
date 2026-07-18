# Chapter 07: Hybrid and Multicloud Architecture

## Learning Objectives

- Distinguish the drivers for hybrid cloud from the drivers for
  multicloud, and evaluate whether a proposed multicloud initiative is
  addressing a real requirement or adding cost without a corresponding
  benefit.
- Design a hybrid architecture pattern (cloud bursting, tiered
  data-gravity placement, or disaster recovery) matched to a specific
  business driver.
- Evaluate abstraction layer options (Kubernetes as a portability layer,
  multicloud management tooling, Terraform provider abstraction) and their
  real limits.
- Design identity, data, and network consistency across more than one
  provider or between a provider and an on-premises environment.
- Evaluate the trade-offs of an edge computing deployment layered onto a
  hybrid or multicloud architecture.
- Implement a provider-abstracted Terraform module structure and validate
  its behavior against two simulated backends.

## Theory and Architecture

### Hybrid cloud drivers

Hybrid cloud connects on-premises infrastructure and one public cloud
provider for a specific, workload-driven reason — it is a deliberate
architecture pattern, not a transitional state on the way to "full
cloud." The recurring drivers are:

- **Data residency or gravity** — regulatory, contractual, or sheer data
  volume reasons keep a data set on-premises while compute that needs
  low-latency access to it either stays on-premises too or is placed as
  close to it as connectivity allows.
- **Latency-sensitive or deterministic workloads** — industrial control
  systems, point-of-sale processing, or anything requiring latency or
  jitter guarantees a shared public cloud region cannot contractually
  provide.
- **Incremental migration** — an organization migrating an existing
  estate to cloud over time necessarily operates a hybrid environment
  during the migration window, which for a large estate can span years.
- **Elastic burst capacity ("cloud bursting")** — steady-state capacity
  runs on-premises (already paid for as sunk capital cost), and demand
  spikes burst into public cloud capacity provisioned only when needed.
- **Regulatory or sovereign requirements** — a specific workload must
  remain under direct organizational control or within a specific legal
  jurisdiction not adequately covered by the provider's regional
  footprint or compliance attestations.

### Multicloud drivers

Multicloud — deliberately operating production workloads across more than
one public cloud provider — has a narrower, and more frequently
misapplied, set of legitimate drivers:

- **Best-of-breed service selection** — a specific managed service on a
  second provider is materially better suited to a specific workload (a
  particular data-analytics or machine-learning service, for example)
  than the equivalent on the primary provider.
- **Regulatory diversification or contractual requirement** — some
  regulated industries or public-sector contracts require avoiding
  single-vendor concentration risk as an explicit compliance control, not
  an optional best practice.
- **Mergers and acquisitions** — an acquired company already operates on
  a different provider, and consolidating onto one provider is a
  multi-year project rather than an immediate requirement.
- **Negotiating leverage** — a credible ability to shift material
  workload volume improves commercial negotiating position with either
  provider, though this driver alone rarely justifies the ongoing
  operational cost of active multicloud on its own.

Multicloud adopted primarily for perceived resilience ("if one provider
has an outage, we're not fully down") deserves particular scrutiny: true
cross-provider failover for a stateful workload requires the workload to
already be built provider-abstracted end to end (data replication,
identity, networking, and deployment automation, all working identically
on both providers), which is a substantial, continuous engineering
investment that is easy to underestimate and that most organizations
never actually complete or keep continuously validated. An organization
that has not tested an actual cross-provider failover should not assume
one would work.

### Portability vs. redundancy: a critical distinction

"We run on two providers" does not by itself mean "we are protected if
one provider fails." Two distinct, frequently conflated goals:

- **Portability** — the ability to move a workload from one provider to
  another over a planned migration window, typically to avoid lock-in or
  to react to a pricing or capability change. Achieved through open
  standards (containers, standard SQL, object storage APIs) and
  infrastructure-as-code discipline, even if the workload runs on only
  one provider at any given moment.
- **Active multi-provider redundancy** — the workload runs
  simultaneously (active-active) or is kept continuously warm
  (active-passive with fast failover) on two providers at the same time,
  so that a single provider's outage does not interrupt service. Requires
  everything portability requires, plus continuous data replication
  across providers, cross-provider identity federation, cross-provider
  network connectivity, and — critically — a regularly tested failover
  procedure.

Running two full, independently maintained implementations on two
providers without either goal clearly targeted is the worst outcome: it
carries the full operational cost of multicloud (duplicated pipelines,
duplicated on-call knowledge, duplicated security review) while
delivering neither the flexibility benefit of true portability nor the
availability benefit of tested active redundancy.

### Abstraction layer options and their real limits

- **Containers and Kubernetes** — a container image runs identically
  regardless of the underlying provider, and Kubernetes provides a
  provider-neutral scheduling and networking API surface (detailed in
  Volume VIII). This genuinely abstracts the *compute runtime* layer, but
  does not abstract the managed services (databases, object storage,
  managed queues, identity) a real application depends on around that
  runtime — those remain provider-specific unless deliberately
  abstracted separately.
- **Infrastructure-as-code provider abstraction** — a Terraform module
  structure (or equivalent) can expose a provider-neutral interface
  (variables in, outputs out) while swapping the underlying provider
  implementation per environment. This genuinely reduces the blast
  radius of learning a second provider's syntax, but does not eliminate
  the need to understand each provider's actual service behavior,
  quotas, and failure modes — the abstraction covers syntax, not
  semantics.
- **Multicloud management platforms** — third-party tooling that
  presents a unified console, policy engine, or cost view across
  providers. Genuinely useful for governance and visibility (extending
  the guardrail patterns from Chapter 02 across providers), but does not
  by itself make workloads portable or redundant — it is an operations
  layer, not an application architecture.

Treat every abstraction layer as covering a specific, bounded layer of the
stack, and be explicit about which layers remain provider-specific
underneath it — the most common multicloud architecture failure is
assuming an abstraction (most often "we use Kubernetes everywhere") covers
more of the stack than it actually does.

### Consistency across providers or hybrid boundaries

A workload spanning providers or spanning on-premises and cloud needs
three specific forms of consistency to function coherently:

- **Identity consistency** — a single federated identity source of truth
  (Chapter 03) that every provider or environment trusts, rather than
  separate identity stores per provider that drift out of sync and
  produce inconsistent access reviews.
- **Network consistency** — routable, non-overlapping address space
  (Chapter 04) and consistent DNS resolution across every environment,
  so a workload's dependency lookups behave identically regardless of
  where the workload currently runs.
- **Data consistency** — a defined replication or synchronization
  mechanism (Chapter 06) with an explicit RPO across the hybrid or
  multicloud boundary, since data is usually the hardest and most
  expensive layer to keep consistent across providers, and inconsistent
  data undermines every other consistency effort.

### Edge computing as an extension of hybrid architecture

Edge computing places compute and storage physically close to the data
source or end user (retail locations, factory floors, telecommunications
infrastructure) to reduce latency or satisfy local data-processing
requirements, typically managed through the same control plane, identity,
and deployment pipeline as the provider's regional infrastructure rather
than as an independently operated environment. Edge deployments introduce
their own constraints not present in a regional deployment: intermittent
or lower-bandwidth connectivity back to the region, physically less secure
locations, and often no local operations staff — which pushes edge
architecture toward autonomous local operation (the edge site continues
functioning during a connectivity loss to the region) with eventual
reconciliation once connectivity returns, rather than assuming continuous
connectivity to the region.

## Design Considerations

### Testing whether a multicloud driver is real

Before approving a multicloud initiative, require the proposing team to
answer: which specific driver from the list above applies, concretely,
to this workload; what is the ongoing operational cost (duplicated
pipelines, duplicated security review, duplicated on-call expertise) of
maintaining this workload across two providers; and if the driver is
resilience, has a cross-provider failover actually been tested, or is it
assumed. A multicloud proposal that cannot answer these concretely is
very often solving a hypothetical problem at a very real, ongoing cost.

### Choosing a hybrid pattern deliberately

Match the hybrid pattern to the actual driver rather than defaulting to
the same pattern for every workload: cloud bursting fits a workload with
a genuine steady-state/peak demand gap and sunk on-premises capacity;
tiered data-gravity placement fits a workload constrained by where its
data must live; disaster recovery to cloud fits a workload where
on-premises remains primary but a fully cloud-hosted standby is more
cost-effective than a second physical site. Applying a cloud-bursting
pattern to a data-residency-driven requirement (or vice versa) solves the
wrong problem.

### Depth of abstraction investment

Decide, per workload, how deep the abstraction investment needs to go.
A workload with a genuine, near-term portability requirement justifies
provider-neutral IaC modules and containerized compute; a workload with no
stated portability requirement should be allowed to use a provider's
native managed services directly rather than paying the abstraction tax
"just in case." Revisit this decision if the workload's stated
requirement changes — do not retrofit deep abstraction after the fact
without a concrete driver, and do not build a portable abstraction from
day one for a workload with no plausible migration scenario.

### Consistency investment vs. workload criticality

Full identity, network, and data consistency across a hybrid or
multicloud boundary is expensive to build and to keep continuously
correct. Scale the investment to the workload's actual criticality: a
tier-1 workload with a genuine cross-provider active-active requirement
justifies the full consistency investment and its ongoing validation;
a lower-tier workload with an occasional batch data export to a second
provider does not need continuous identity federation or a
fully-routed network between the two.

### Edge site autonomy boundary

Define explicitly what an edge site must be able to do entirely on its
own when disconnected from the region (accept transactions, authenticate
local users, serve cached content) versus what genuinely requires the
region to be reachable, and design the reconciliation process for when
connectivity returns (conflict resolution for data written independently
at both the edge and the region during the disconnection window is
frequently the hardest part of this design, not the disconnected
operation itself).

## Implementation and Automation

### Provider-abstracted Terraform module structure

```text
modules/
├── object-storage/
│   ├── main.tf         # dispatches to the provider-specific submodule
│   ├── variables.tf      # provider-neutral interface
│   ├── outputs.tf       # provider-neutral outputs
│   ├── provider-a/       # implementation for provider A
│   └── provider-b/       # implementation for provider B
```

```hcl
# modules/object-storage/variables.tf — provider-neutral interface.
variable "provider_target" {
  type = string
  validation {
    condition     = contains(["provider-a", "provider-b"], var.provider_target)
    error_message = "provider_target must be one of: provider-a, provider-b."
  }
}

variable "bucket_name" {
  type = string
}

variable "lifecycle_days_to_archive" {
  type    = number
  default = 90
}
```

```hcl
# modules/object-storage/main.tf — dispatches by provider_target;
# the caller's interface never changes when the target provider does.
module "provider_a_bucket" {
  count  = var.provider_target == "provider-a" ? 1 : 0
  source = "./provider-a"

  bucket_name         = var.bucket_name
  lifecycle_days_to_archive = var.lifecycle_days_to_archive
}

module "provider_b_bucket" {
  count  = var.provider_target == "provider-b" ? 1 : 0
  source = "./provider-b"

  bucket_name         = var.bucket_name
  lifecycle_days_to_archive = var.lifecycle_days_to_archive
}

output "bucket_endpoint" {
  value = var.provider_target == "provider-a" ? try(module.provider_a_bucket[0].endpoint, null) : try(module.provider_b_bucket[0].endpoint, null)
}
```

This structure keeps the *calling* code (every environment root module
that consumes `modules/object-storage`) fully provider-neutral; only the
two small provider-specific submodules contain real provider syntax. A
new environment target is a variable change, not a rewrite — this is the
concrete, bounded value an IaC abstraction layer delivers, consistent
with the "abstracts syntax, not semantics" limit described earlier in this
chapter.

### Cross-provider identity federation trust

```hcl
# federation-crossprovider.tf — illustrative: both providers trust the
# same external identity provider, avoiding separate per-provider
# identity stores that drift out of sync.
resource "cloud_iam_federation_trust" "shared_idp_provider_a" {
  provider = provider.provider_a
  issuer   = var.corporate_idp_issuer_url
  audience = "provider-a-sts"
}

resource "cloud_iam_federation_trust" "shared_idp_provider_b" {
  provider = provider.provider_b
  issuer   = var.corporate_idp_issuer_url
  audience = "provider-b-sts"
}
```

### Data replication across providers with an explicit RPO check

```bash
#!/usr/bin/env bash
# cross-provider-replication-check.sh — illustrative RPO validation.
set -euo pipefail

REQUIRED_RPO_MINUTES=15

LAST_SYNC_EPOCH=$(cloud-cli-b storage stat --bucket "dr-replica" --field last_sync_epoch)
NOW_EPOCH=$(date +%s)
LAG_MINUTES=$(( (NOW_EPOCH - LAST_SYNC_EPOCH) / 60 ))

if [ "$LAG_MINUTES" -gt "$REQUIRED_RPO_MINUTES" ]; then
  echo "REPLICATION LAG BREACH: ${LAG_MINUTES}m exceeds RPO of ${REQUIRED_RPO_MINUTES}m" >&2
  exit 1
fi

echo "Replication lag ${LAG_MINUTES}m within ${REQUIRED_RPO_MINUTES}m RPO."
```

## Validation and Troubleshooting

- **Test cross-provider or hybrid failover on a schedule, not only in
  design documents.** An untested failover procedure should be treated as
  an unvalidated assumption, not a working control — this is the single
  most common gap between a multicloud architecture diagram and its
  actual resilience posture.
- **Diagnose an abstraction-layer failure by checking which layer
  actually failed.** A Kubernetes-based application failing after a
  provider migration is more often caused by a provider-specific managed
  service dependency underneath the abstraction (a queue, a database, an
  identity binding) than by the container runtime itself; validate each
  layer named in the "abstraction layer options" section independently.
- **Monitor replication lag continuously against the stated RPO**, using
  a check similar to the script above wired into standing observability
  (Chapter 09), rather than discovering a replication lag breach only
  during an actual failover attempt.
- **Validate identity consistency by auditing for orphaned,
  provider-local identities** — an identity created directly in a
  provider's own store, outside the shared federation source, is a common
  drift point that undermines the entire premise of a single identity
  source of truth.
- **Diagnose edge site reconciliation conflicts explicitly**, and design
  and test the conflict-resolution rule (last-write-wins, a merge
  strategy, or manual review) before an edge site's first real
  disconnection event, not after.

## Security and Best Practices

- Apply the identity model from Chapter 03 as a single federated source of
  truth across every provider and environment; do not allow
  provider-local identity stores to accumulate as an exception.
- Extend the guardrail and policy-as-code discipline from Chapter 02
  across every provider a workload touches — a guardrail enforced on only
  one of two providers a workload runs on is a governance gap, not a
  partial mitigation.
- Encrypt data in transit across every hybrid connectivity path and every
  cross-provider replication link, in addition to the connectivity-layer
  protections established in Chapter 04.
- Scope credentials and network access for edge sites tightly, and assume
  an edge site is physically less secure than a provider region — design
  for the edge site being compromised or physically accessed by an
  unauthorized party as a real threat scenario, not a theoretical one.
- Require a documented, dated record of the last successful cross-provider
  or hybrid failover test for any workload whose resilience justification
  depends on that failover working.

## References and Knowledge Checks

### References

- NIST SP 800-146, *Cloud Computing Synopsis and Recommendations*, for
  hybrid and multi-provider consumption model definitions.
- Each major provider's hybrid connectivity and cross-region/cross-cloud
  replication documentation — consult the current vendor source for exact
  service names and limits.
- `SOFTWARE_VERSIONS.md` in this repository for the Terraform baseline.

### Knowledge checks

1. A team proposes multicloud "for resilience" but has never tested a
   cross-provider failover. What is the actual current resilience
   posture of this architecture, and why?
2. Explain the difference between portability and active multi-provider
   redundancy, and why achieving one does not imply the other.
3. Why does adopting Kubernetes across two providers abstract the compute
   runtime layer but not necessarily the rest of an application's
   dependencies?
4. A workload requires data residency in a specific jurisdiction with no
   burst-capacity or DR driver. Which hybrid pattern fits, and why would
   a cloud-bursting pattern be the wrong choice here?
5. Why is conflict resolution during edge-site reconciliation frequently
   harder than designing the disconnected-operation mode itself?

## Hands-On Lab

### Lab 7.1 — Provider-abstracted module dispatch with simulated backends

This lab builds the provider-abstracted Terraform module structure from
this chapter using only the local `local_file` provider to simulate two
different "providers," proving the calling interface stays identical
while the underlying implementation changes. No cloud account or
credentials are required.

**Prerequisites**

- Terraform 1.9.x or later, or a compatible OpenTofu release.
- A POSIX shell.

**Steps**

1. Create the working directory and module structure:

   ```bash
   mkdir -p ~/labs/vol07-ch07/modules/object-storage/provider-a
   mkdir -p ~/labs/vol07-ch07/modules/object-storage/provider-b
   cd ~/labs/vol07-ch07
   ```

2. Create `modules/object-storage/provider-a/main.tf` (simulates
   provider A's bucket resource with a `local_file`):

   ```hcl
   terraform {
     required_providers {
       local = { source = "hashicorp/local", version = ">= 2.5" }
     }
   }

   variable "bucket_name" { type = string }
   variable "lifecycle_days_to_archive" { type = number }

   resource "local_file" "bucket" {
     filename = "${path.module}/../../../output/provider-a-${var.bucket_name}.json"
     content  = jsonencode({ provider = "provider-a", bucket = var.bucket_name, archive_days = var.lifecycle_days_to_archive })
   }

   output "endpoint" {
     value = "provider-a://${var.bucket_name}"
   }
   ```

3. Create `modules/object-storage/provider-b/main.tf` (simulates a
   differently shaped provider B resource):

   ```hcl
   terraform {
     required_providers {
       local = { source = "hashicorp/local", version = ">= 2.5" }
     }
   }

   variable "bucket_name" { type = string }
   variable "lifecycle_days_to_archive" { type = number }

   resource "local_file" "container" {
     filename = "${path.module}/../../../output/provider-b-${var.bucket_name}.json"
     content  = jsonencode({ provider = "provider-b", container_name = var.bucket_name, tiering_days = var.lifecycle_days_to_archive })
   }

   output "endpoint" {
     value = "provider-b://${var.bucket_name}"
   }
   ```

4. Create `modules/object-storage/main.tf`, `variables.tf`, and
   `outputs.tf` using the exact dispatch pattern shown in this chapter's
   Implementation and Automation section (the `provider_target`
   variable, the two conditional `module` blocks, and the conditional
   `bucket_endpoint` output).

5. Create the root `main.tf` at `~/labs/vol07-ch07/main.tf`:

   ```hcl
   module "app_bucket" {
     source           = "./modules/object-storage"
     provider_target       = var.provider_target
     bucket_name         = "app-data"
     lifecycle_days_to_archive = 60
   }

   variable "provider_target" {
     type    = string
     default = "provider-a"
   }

   output "endpoint" {
     value = module.app_bucket.bucket_endpoint
   }
   ```

6. Initialize and apply with the default target:

   ```bash
   terraform init
   terraform apply -auto-approve
   ```

   **Expected result:** Apply succeeds, `endpoint` output shows
   `"provider-a://app-data"`, and
   `output/provider-a-app-data.json` exists.

7. Switch the target provider without changing the calling interface:

   ```bash
   terraform apply -auto-approve -var="provider_target=provider-b"
   ```

   **Expected result:** Apply succeeds, `endpoint` output now shows
   `"provider-b://app-data"`, and `output/provider-b-app-data.json` now
   exists — demonstrating that the root module's interface (`bucket_name`,
   `lifecycle_days_to_archive`) never changed while the underlying
   implementation swapped.

**Negative test**

8. Attempt to apply with an unsupported provider target:

   ```bash
   terraform apply -auto-approve -var="provider_target=provider-c"
   ```

   **Expected result:** Terraform refuses to proceed and reports the
   custom validation error `provider_target must be one of: provider-a,
   provider-b.`, demonstrating that the abstraction layer's interface
   rejects an unimplemented target explicitly rather than silently doing
   nothing.

**Cleanup**

9. Destroy and remove the working directory:

   ```bash
   terraform destroy -auto-approve -var="provider_target=provider-b"
   cd ~ && rm -rf ~/labs/vol07-ch07
   ```

   **Expected result:** Terraform reports the resources destroyed, and
   the working directory no longer exists.

## Summary and Completion Checklist

Hybrid cloud and multicloud are distinct architecture patterns, each
justified by specific, concrete drivers — not defaults, and not the same
thing as each other. This chapter distinguished portability from active
multi-provider redundancy, evaluated the real, bounded scope of
abstraction layers like Kubernetes and provider-abstracted IaC modules,
and covered the identity, network, and data consistency work required to
make a hybrid or multicloud boundary function coherently, including the
autonomy and reconciliation design edge computing adds on top. Chapter 08
covers governing this multi-provider estate with consistent policy and
cost management, and Chapter 09 covers the automation and observability
practices that keep it operationally sound.

- [ ] Can articulate a concrete, workload-specific driver for a proposed
      multicloud or hybrid initiative, or identify that none exists.
- [ ] Can distinguish portability from active multi-provider redundancy
      and explain why achieving one does not guarantee the other.
- [ ] Can name the specific layer an abstraction (Kubernetes, IaC module)
      covers and the layers that remain provider-specific underneath it.
- [ ] Can design identity, network, and data consistency across a hybrid
      or multicloud boundary appropriate to a workload's criticality.
- [ ] Completed Lab 7.1, including the negative test and cleanup.
