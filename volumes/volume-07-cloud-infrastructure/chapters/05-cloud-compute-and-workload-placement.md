# Chapter 05: Cloud Compute and Workload Placement

![Lab flow for this chapter: from observed minimum and peak instance counts and a proposed reserved floor, a Terraform check block asserts the reserved floor never exceeds observed minimum demand; the default plan passes with no check failure, and the purchasing_mix output shows a validated reserved/on-demand/spot split. As a negative test, re-planning with a reserved floor double the observed minimum fails the check, reporting that the proposal commits to paying for capacity that is never used — an automated guardrail against over-committing reserved capacity before any real financial commitment is made.](../../../diagrams/volume-07-cloud-infrastructure/chapter-05-purchasing-mix-guardrail-flow.svg)

*Figure 5-1. Flow used throughout this chapter's Hands-On Lab: an on-demand/reserved/spot purchasing-mix calculation validated against observed demand, with a reserved-floor guardrail.*

## Learning Objectives

- Compare virtual machines, containers, and serverless/function compute as
  workload placement options, and choose correctly based on workload
  shape, not familiarity.
- Design an instance/machine-family and sizing strategy, including the
  role of right-sizing as a continuous practice rather than a one-time
  decision.
- Differentiate on-demand, reserved/committed-use, and spot/preemptible
  purchasing options, and design a workload placement strategy that uses
  each appropriately.
- Explain autoscaling models (reactive, scheduled, predictive) and design
  a scaling policy that avoids common thrashing failure modes.
- Design a golden-image and immutable-infrastructure pipeline for compute
  fleets.
- Implement and validate an autoscaling compute fleet as code, and
  diagnose common scaling and placement failures.

## Theory and Architecture

### The compute placement spectrum

Cloud compute is not a single decision but a spectrum, and a mature cloud
estate places different workloads at different points on it deliberately:

| Model | Unit of deployment | Provider manages | Customer manages | Typical fit |
| --- | --- | --- | --- | --- |
| Virtual machines (IaaS) | A full OS instance | Hypervisor, host hardware | OS, runtime, scaling logic, patching | Legacy or COTS software, workloads needing OS-level control or specific kernel/driver access |
| Container orchestration (covered in depth in [Volume VIII](../../volume-08-containers-platform-engineering/README.md)) | A container image on a scheduler | Node provisioning (if managed), scheduler control plane | Container images, resource requests, in-cluster networking | Microservices, workloads needing fast, dense scaling and packaging portability |
| Serverless / function compute | A function and its trigger | Everything except code and configuration | Function code, event bindings, cold-start tuning | Event-driven, bursty, or intermittent workloads where idle cost must be zero |
| Managed application platform (PaaS) | Application source or container, deployed to a managed runtime | Runtime, scaling, load balancing | Application code and configuration | Web applications and APIs where the team wants to skip infrastructure operations entirely |

This chapter focuses primarily on virtual machines and the placement,
sizing, and purchasing decisions around them, since container
orchestration receives dedicated treatment in [Volume VIII](../../volume-08-containers-platform-engineering/README.md). The decision
between these models for a given workload should be revisited
periodically — a workload built as a virtual machine fleet three years ago
because container orchestration was immature at the time may now be a
strong candidate for migration, and the reverse is also true when a
workload's actual usage pattern turns out to be steady-state rather than
bursty.

### Instance/machine families and sizing

Providers group virtual machine types into families optimized for
different resource ratios: general purpose (balanced CPU:memory),
compute-optimized (high CPU:memory ratio for CPU-bound workloads),
memory-optimized (high memory:CPU ratio for in-memory databases and
caches), storage-optimized (high local disk throughput/IOPS), and
accelerated-computing (GPU or other hardware accelerators attached).
Selecting the wrong family is a common, quietly expensive mistake: a
memory-bound workload placed on a general-purpose family either wastes
provisioned CPU it never uses or is forced to over-provision the whole
instance just to get enough memory, when a memory-optimized family at the
same or lower cost would fit the workload's actual resource ratio.

Right-sizing is a continuous practice, not a one-time launch decision.
Workload resource consumption drifts as application code, traffic
patterns, and dependencies change; a fleet sized correctly at launch is
commonly 20-40% oversized within a year without periodic review, driven by
a natural bias toward over-provisioning "to be safe" combined with nobody
being explicitly accountable for downsizing later.

### Purchasing options

- **On-demand** — pay per unit of time with no commitment, at the
  highest per-unit rate. The correct default for unpredictable or new
  workloads, and for the portion of any workload's capacity that varies
  above a predictable baseline.
- **Reserved / committed-use** — commit to a usage volume or specific
  instance configuration over a term (commonly one or three years) in
  exchange for a substantial discount (often 30-70% relative to
  on-demand). Correct for the well-understood, steady-state baseline
  portion of a workload's capacity — the capacity that is running
  regardless of demand fluctuation.
- **Spot / preemptible** — bid for or consume a provider's spare capacity
  at a steep discount (often 60-90% off on-demand), with the explicit
  condition that the provider can reclaim the capacity on short notice
  (seconds to a couple of minutes, depending on provider). Correct for
  fault-tolerant, interruptible, or stateless workloads: batch processing,
  CI/CD build agents, stateless web tiers behind a load balancer with
  healthy spare capacity, and horizontally scaled worker pools that can
  absorb the loss of any individual instance.

A mature fleet blends all three against the same demand curve: reserved
capacity sized to the workload's stable minimum (the floor that is always
running), on-demand or spot capacity absorbing the variable portion above
that floor, and spot specifically reserved for genuinely interruption-
tolerant components rather than applied indiscriminately across the whole
fleet. [Chapter 08](08-cloud-governance-security-and-finops.md) covers the FinOps discipline of tracking commitment
utilization and coverage against this blend over time.

### Autoscaling models

- **Reactive (metric-based) scaling** — adds or removes capacity in
  response to a real-time metric crossing a threshold (CPU utilization,
  queue depth, request latency). Simple to reason about but inherently
  lags the demand change it is reacting to by at least one evaluation
  period plus instance boot time.
- **Scheduled scaling** — adds or removes capacity on a known time-based
  pattern (business-hours traffic, a nightly batch window). Removes the
  reaction lag for predictable patterns entirely, at the cost of not
  adapting to demand that deviates from the schedule.
- **Predictive scaling** — uses historical demand patterns (often via a
  provider-native forecasting feature) to pre-provision capacity ahead of
  an anticipated demand increase, combining the responsiveness of
  scheduled scaling with adaptability to trend changes, at the cost of
  depending on a forecast that can be wrong for a genuinely novel event.

Combine reactive scaling as the default safety net with scheduled or
predictive scaling layered on top for well-understood demand patterns,
so the fleet is never solely dependent on reacting after a threshold is
already crossed for the traffic pattern that happens every single day.

### Immutable infrastructure and golden images

An immutable-infrastructure pattern treats a running compute instance as
disposable: instead of patching or reconfiguring a live instance in place,
a new golden image is built (through an automated image pipeline),
validated, and used to replace running instances via a rolling or
blue/green deployment, and the old instances are terminated rather than
modified. This eliminates configuration drift — the class of bug where a
production instance behaves differently from a freshly provisioned one
because of an undocumented manual change made months earlier — and makes
every deployed instance fleet-wide provably identical at any point in
time, which is a direct prerequisite for reliable autoscaling: a newly
launched instance from autoscaling must behave identically to its
siblings without any manual post-boot intervention.

## Design Considerations

### Choosing among VM, container, and serverless for a given workload

Ask, in order: does the workload need OS-level control, a specific kernel
module, or licensing tied to physical/virtual machine counts (favors VM);
is the workload naturally decomposed into independently scalable services
with a fast, uniform deployment/packaging need (favors container
orchestration, detailed in [Volume VIII](../../volume-08-containers-platform-engineering/README.md)); is the workload event-driven,
bursty, or has meaningfully idle periods where paying for standing
capacity is wasteful (favors serverless). A workload can and often does
mix models — a steady-state API tier on containers, a nightly batch job on
serverless, and a licensed COTS dependency on a VM, inside the same
architecture.

### Sizing methodology

Size from observed or realistically projected utilization, not from a
round-number default ("everything gets a large instance"). Establish a
periodic right-sizing review (monthly or quarterly, tied into the FinOps
practice in [Chapter 08](08-cloud-governance-security-and-finops.md)) using actual CPU, memory, network, and disk I/O
utilization data, and treat a persistently underutilized instance family
as a finding requiring action, not a tolerable safety margin. Distinguish
genuine headroom (reserved for known future growth or burst tolerance,
documented) from unexplained slack (undocumented, should be reclaimed).

### Purchasing option allocation

Model the workload's demand curve explicitly (minimum, typical, and peak
concurrent capacity) before deciding a reserved/on-demand/spot split.
Committing too aggressively to reserved capacity against an
underestimated floor leaves the organization paying for unused
commitment during a demand dip; committing too conservatively leaves
on-demand savings unrealized. Revisit the commitment level whenever the
workload's demand shape changes materially, and track commitment
utilization as an ongoing metric rather than a decision made once at
launch and forgotten.

### Availability zone distribution vs. cost and latency

Distributing a fleet across multiple availability zones is the baseline
resilience pattern (established in [Chapter 01](01-cloud-operating-models-and-architecture-foundations.md)), but cross-zone network
traffic frequently carries a per-GB cost and marginally higher latency
than same-zone traffic. For latency- or cost-sensitive tiers with a
genuine same-zone-affinity requirement (a cache tier tightly coupled to
its application tier, for example), consider zone-aware routing that
prefers same-zone targets when healthy, falling back to cross-zone only
when necessary — while still maintaining enough capacity in every zone to
absorb a full zone failure without that fallback path becoming the normal
case.

### Scaling policy tuning to avoid thrashing

A reactive scaling policy with thresholds set too close together, or a
cooldown period set too short, causes thrashing: the fleet scales out,
the added capacity immediately drops the average metric below the
scale-in threshold, the fleet scales back in, and the cycle repeats,
producing instability and wasted instance boot/terminate churn instead of
a stable capacity level. Set scale-out and scale-in thresholds with
deliberate separation (a gap, not adjacent values), and set a cooldown
period long enough for newly launched instances to reach steady-state
utilization and be reflected in the aggregate metric before the policy
evaluates again.

## Implementation and Automation

### Defining a right-sized, tagged instance fleet as code

```hcl
# compute.tf — illustrative provider-neutral instance fleet definition.
variable "instance_family" {
  type        = string
  default     = "general-purpose-large"
  description = "Selected from observed CPU:memory utilization ratio, reviewed quarterly."
}

resource "cloud_instance_template" "app" {
  name            = "app-tier"
  instance_family  = var.instance_family
  image_id         = data.cloud_image.golden.id # built by the pipeline below

  tags = {
    environment = var.environment
    workload    = "app-tier"
    managed_by  = "autoscaling-group"
  }
}
```

### Blending purchasing options in one autoscaling group

```hcl
# autoscaling.tf — illustrative mixed on-demand/spot fleet.
resource "cloud_autoscaling_group" "app" {
  name           = "app-tier-${var.environment}"
  min_size        = 4  # reserved/committed-use floor, always running
  max_size        = 40
  desired_capacity   = 6

  instance_template = cloud_instance_template.app.id
  availability_zones = ["a", "b", "c"] # spread across zones for resilience

  purchasing_mix {
    on_demand_base_capacity  = 4  # matches the reserved commitment floor
    on_demand_percentage_above_base = 30 # 30% on-demand, 70% spot, above the floor
    spot_allocation_strategy = "capacity-optimized"
  }

  scaling_policy {
    metric              = "average_cpu_utilization"
    scale_out_threshold   = 65
    scale_in_threshold    = 35 # deliberate gap from scale-out threshold, avoids thrashing
    cooldown_seconds       = 300
  }
}
```

The `on_demand_base_capacity` set to match the reserved-capacity floor is
a deliberate pattern: it keeps the reserved commitment fully utilized at
all times (the base never scales below it under normal operation) while
letting variable demand above that floor draw on cheaper spot capacity by
default.

### Golden image pipeline (illustrative)

```yaml
# .ci/golden-image-pipeline.yml — illustrative image-build pipeline.
stages:
  - build
  - validate
  - publish

build_image:
  stage: build
  script:
    - packer build -var "base_image=$BASE_IMAGE_ID" image.pkr.hcl

validate_image:
  stage: validate
  script:
    # Boot the candidate image, run compliance and smoke tests against it.
    - ./scripts/validate-golden-image.sh --image-id "$CANDIDATE_IMAGE_ID"

publish_image:
  stage: publish
  script:
    # Only tag as latest after validation passes; triggers a rolling
    # replacement of the autoscaling group's launch template.
    - cloud-cli image tag --id "$CANDIDATE_IMAGE_ID" --tag latest-validated
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
```

### Scheduled scaling layered on top of reactive scaling

```hcl
# scheduled-scaling.tf — illustrative business-hours pre-scale.
resource "cloud_scheduled_scaling_action" "business_hours_prescale" {
  autoscaling_group_id = cloud_autoscaling_group.app.id
  schedule            = "cron(0 12 * * MON-FRI)" # 12:00 UTC, before daily peak
  min_size             = 10 # raises the floor ahead of predictable demand
  desired_capacity        = 12
}
```

## Validation and Troubleshooting

- **Diagnose a scaling policy that never triggers** by checking, in
  order: the metric source is actually reporting data for the target
  group, the threshold values are on the correct side of the current
  baseline (a common transposition error swaps scale-out and scale-in
  thresholds), and the autoscaling group's `max_size` is not already
  reached.
- **Diagnose thrashing (rapid scale-out/scale-in cycling)** by checking
  the gap between scale-out and scale-in thresholds and the cooldown
  period first, before assuming the underlying demand is genuinely
  volatile — most thrashing is a policy-tuning problem, not a traffic
  problem.
- **Validate spot interruption handling explicitly**, not just in theory:
  trigger a controlled interruption (most providers offer a
  test/simulate-interruption API) and confirm the workload drains
  connections and the autoscaling group replaces the capacity within the
  expected time, rather than assuming statelessness without testing it.
- **Confirm zone distribution after every scaling event**, not only at
  initial launch — an autoscaling group can drift toward an uneven
  zone distribution over time as instances in different zones launch,
  terminate, and get replaced at different rates, quietly eroding the
  zone-redundancy assumption.
- **Treat a persistent low-utilization alert as an action item, not
  noise.** A right-sizing review that only happens when someone
  remembers to run it will not happen consistently; automate the report
  and route it to the owning team on a schedule.

## Security and Best Practices

- Build every instance from a golden image produced by a validated,
  version-controlled pipeline; never hand-configure a production instance
  and capture an image from it afterward, which reintroduces the
  configuration-drift risk immutable infrastructure is meant to eliminate.
- Patch by rebuilding and replacing the golden image and rolling the
  fleet, not by patching running instances in place, so the fleet stays
  provably identical and the patch is captured in the pipeline for the
  next build.
- Grant compute instances only the workload identity permissions
  established in [Chapter 03](03-cloud-identity-access-and-cryptographic-services.md) — never embed a long-lived credential in a
  golden image or instance user-data script.
- Apply the network segmentation controls from [Chapter 04](04-cloud-networking-and-hybrid-connectivity.md) to every
  instance regardless of purchasing option; a spot instance is not a
  lower-trust resource from a security perspective and should not receive
  weaker network controls.
- Set a maximum instance age or a mandatory periodic replacement policy
  even for otherwise healthy instances, so that the fleet never
  accumulates long-running instances that predate the current golden
  image and its patches.

## References and Knowledge Checks

### References

- Each major provider's compute instance family, autoscaling, and
  spot/preemptible-capacity documentation — consult the current vendor
  source for exact family names, discount levels, and interruption notice
  periods.
- HashiCorp Packer documentation, for the golden-image build pattern used
  in this chapter's illustrative pipeline.
- `SOFTWARE_VERSIONS.md` in this repository for the Terraform baseline.

### Knowledge checks

1. A workload has a well-understood, always-on baseline of six instances
   and an unpredictable burst up to thirty instances during promotional
   events. Describe an appropriate purchasing-option split.
2. Why does immutable infrastructure make autoscaling more reliable than
   a mutable, patched-in-place fleet?
3. An autoscaling group is thrashing (scaling out and back in every few
   minutes). What two policy parameters would you check first, and why?
4. Why should a golden image pipeline validate the candidate image before
   tagging it for use, rather than validating after it is already rolled
   out to production instances?
5. Explain why a spot instance should receive the same network
   segmentation controls as an on-demand instance.

## Hands-On Lab

### Lab 5.1 — Right-sizing and purchasing-mix calculator with validation

This lab builds a local Terraform configuration that calculates a
recommended on-demand/reserved/spot split from a supplied demand profile
and validates the result against a policy rule (the reserved floor must
never exceed the observed minimum demand, which would mean paying for
committed capacity that is never used). No cloud account or credentials
are required.

**Prerequisites**

- Terraform 1.9.x or later, or a compatible OpenTofu release.
- A POSIX shell.

**Steps**

1. Create the working directory:

   ```bash
   mkdir -p ~/labs/vol07-ch05 && cd ~/labs/vol07-ch05
   ```

2. Create `variables.tf`:

   ```hcl
   variable "observed_minimum_instances" {
     type    = number
     default = 6
   }

   variable "observed_peak_instances" {
     type    = number
     default = 30
   }

   variable "proposed_reserved_floor" {
     type    = number
     default = 6
   }
   ```

3. Create `main.tf` with the calculation and a validating `check` block:

   ```hcl
   locals {
     variable_capacity  = var.observed_peak_instances - var.proposed_reserved_floor
     spot_capacity     = floor(local.variable_capacity * 0.7)
     on_demand_capacity  = local.variable_capacity - local.spot_capacity
   }

   check "reserved_floor_not_oversized" {
     assert {
       condition     = var.proposed_reserved_floor <= var.observed_minimum_instances
       error_message = "proposed_reserved_floor exceeds observed_minimum_instances; this commits to paying for capacity that is never used."
     }
   }

   output "purchasing_mix" {
     value = {
       reserved   = var.proposed_reserved_floor
       on_demand  = local.on_demand_capacity
       spot      = local.spot_capacity
       total_peak  = var.observed_peak_instances
     }
   }
   ```

4. Initialize and plan with the default (valid) values:

   ```bash
   terraform init
   terraform plan
   ```

   **Expected result:** Plan succeeds with no check failure, and the
   `purchasing_mix` output shows `reserved = 6`, `on_demand = 8`,
   `spot = 16`, `total_peak = 30`.

**Negative test**

5. Re-run with a reserved floor that exceeds observed minimum demand:

   ```bash
   terraform plan -var="proposed_reserved_floor=12"
   ```

   **Expected result:** Terraform reports the check failure
   `proposed_reserved_floor exceeds observed_minimum_instances; this
   commits to paying for capacity that is never used.`, demonstrating
   automated guardrails against over-committing reserved capacity before
   any real financial commitment is made.

**Cleanup**

6. Remove the lab directory:

   ```bash
   cd ~ && rm -rf ~/labs/vol07-ch05
   ```

   **Expected result:** The directory no longer exists. No cloud compute
   resources or purchasing commitments were created at any point in this
   lab.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Cloud compute placement is a continuous set of decisions, not a single
launch-time choice: which service model fits the workload, which instance
family matches its resource ratio, how purchasing options blend against
its demand curve, how autoscaling policy responds to (and avoids
thrashing against) real demand, and how immutable golden images keep the
resulting fleet free of configuration drift. [Chapter 06](06-cloud-storage-databases-and-data-services.md) turns to the
storage and database services this compute fleet depends on, and Chapter
08 returns to purchasing-mix optimization as an ongoing FinOps practice.

- [ ] Can choose among VM, container, and serverless placement for a
      stated workload shape and justify the choice.
- [ ] Can design a blended on-demand/reserved/spot purchasing strategy
      against an explicit demand curve.
- [ ] Can tune a reactive scaling policy to avoid thrashing.
- [ ] Can explain how immutable infrastructure and golden images eliminate
      configuration drift.
- [ ] Completed Lab 5.1, including the negative test and cleanup.
