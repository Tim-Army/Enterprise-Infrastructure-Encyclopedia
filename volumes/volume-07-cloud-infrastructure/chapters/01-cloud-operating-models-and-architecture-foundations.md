# Chapter 01: Cloud Operating Models and Architecture Foundations

## Learning Objectives

- Differentiate IaaS, PaaS, SaaS, and FaaS service models and identify which
  operational responsibilities transfer to the provider under each.
- Explain the shared responsibility model and apply it to a concrete workload
  decision (who patches what, who encrypts what, who is accountable for
  availability).
- Compare public, private, hybrid, multicloud, and edge deployment models and
  articulate the primary driver for choosing each.
- Describe cloud provider physical and logical architecture: regions,
  availability zones, edge/points of presence, and the separation between
  control plane and data plane.
- Apply a Well-Architected-style pillar framework (operational excellence,
  security, reliability, performance efficiency, cost optimization,
  sustainability) to evaluate a design.
- Calculate composite availability for a multi-tier architecture from
  published component SLAs and interpret what the result does and does not
  guarantee.

## Theory and Architecture

### Service models

Cloud service models describe where the boundary sits between what a provider
operates and what the customer operates. The classic taxonomy from NIST SP
800-145 remains the reference point, extended in practice by two widely used
categories:

| Model | Provider operates | Customer operates | Representative example |
| --- | --- | --- | --- |
| IaaS (Infrastructure as a Service) | Physical hosts, hypervisor, network fabric, storage arrays | OS, runtime, middleware, application, data | Virtual machines, block volumes, virtual networks |
| PaaS (Platform as a Service) | Everything in IaaS plus OS patching, runtime, and often scaling | Application code, configuration, data | Managed application platforms, managed databases |
| SaaS (Software as a Service) | Everything, including the application itself | Configuration, data, user access | Hosted email, CRM, identity providers |
| FaaS (Function as a Service) | Everything except the function code and its trigger wiring | Function code, event bindings, cold-start tuning | Event-driven compute, serverless pipelines |

Moving down this table (IaaS toward SaaS) trades operational control for
reduced operational burden. An architecture team should treat the service
model as a per-workload decision, not a single organizational stance — a
single landing zone routinely hosts IaaS virtual machines, PaaS managed
databases, and SaaS identity providers side by side.

### Deployment models

- **Public cloud** — multi-tenant infrastructure operated by a third-party
  provider, consumed over the public internet or provider-managed private
  connectivity. Lowest capital commitment, highest elasticity.
- **Private cloud** — cloud-operating-model tooling (self-service catalog,
  metering, automation) applied to dedicated infrastructure, on-premises or
  hosted. Chosen for data residency, latency, or regulatory constraints that
  public regions cannot satisfy.
- **Hybrid cloud** — a single workload or application spans private and
  public infrastructure with defined integration points (identity,
  networking, data replication). Covered in depth in Chapter 07.
- **Multicloud** — an organization deliberately or incidentally operates
  workloads across more than one public provider, either for best-of-breed
  services, regulatory diversification, or negotiating leverage.
- **Edge** — compute and storage placed close to the data source or end
  user (retail sites, factory floors, cell towers) to reduce latency or keep
  data local, typically managed through the same control plane as the
  provider's regional infrastructure.

### Shared responsibility model

Every cloud provider publishes some form of a shared responsibility model;
the details vary by name, but the shape is consistent. The provider is
always responsible for the security **of** the cloud (physical facilities,
host infrastructure, hypervisor isolation, and — for managed services — the
service's own control plane). The customer is always responsible for
security **in** the cloud, and the exact line moves with the service model:

```text
IaaS:  Customer -> OS, patching, network config, identity, data, app code
PaaS:  Customer -> App config, identity, data, access policy
SaaS:  Customer -> Configuration, data classification, user/access governance
```

Misreading this boundary is one of the most common sources of production
incidents and audit findings in cloud environments: teams assume a managed
database's storage encryption also implies encrypted backups, or that a
provider's DDoS protection removes the need for application-layer rate
limiting. Document the boundary explicitly per service in an architecture
decision record; do not rely on institutional memory.

### Provider architecture: regions, zones, and edge

Cloud providers organize physical infrastructure hierarchically:

- **Region** — a geographic area containing multiple isolated data centers,
  chosen for data residency, latency to users, and disaster-recovery
  separation from other regions.
- **Availability zone (AZ)** — one or more discrete data centers within a
  region, engineered with independent power, cooling, and networking so a
  single-zone failure does not take down the region. Distributing a workload
  across at least two (commonly three) zones is the baseline resilience
  pattern for any tier that cannot tolerate a zone outage.
- **Edge location / point of presence (PoP)** — a smaller facility, often in
  a metro area, used for content delivery, DNS resolution, or edge compute,
  connected back to a parent region over the provider's private backbone.

Logically, every provider separates a **control plane** (the APIs and
services used to create, modify, and delete resources — for example, the
component that processes a "create virtual machine" request) from a **data
plane** (the component that actually carries application traffic or serves
application data once the resource exists). This separation matters
operationally: a control-plane degradation may block new deployments and
scaling actions while already-running workloads on the data plane continue
to serve traffic unaffected, and vice versa. Design health checks and
runbooks to distinguish the two failure modes.

### A Well-Architected-style pillar framework

Most major providers publish a named "well-architected" framework; the
pillar names differ slightly, but the underlying dimensions are consistent
enough to treat as provider-neutral evaluation criteria:

1. **Operational excellence** — the ability to run and monitor systems to
   deliver business value and continuously improve supporting processes.
2. **Security** — protecting information, systems, and assets through risk
   assessment and mitigation strategies.
3. **Reliability** — the ability to recover from failure, scale to meet
   demand, and prevent disruption.
4. **Performance efficiency** — using resources efficiently to meet
   requirements and maintaining that efficiency as demand and technology
   evolve.
5. **Cost optimization** — avoiding unnecessary costs and understanding
   spend drivers (expanded in Chapter 08 as FinOps).
6. **Sustainability** — minimizing the environmental impact of running cloud
   workloads, including region and instance-family selection.

Use these pillars as a structured review checklist during design reviews
regardless of which provider (or providers) host the workload; each
provider's own framework documentation can supply provider-specific checks
underneath each pillar.

### Cloud economics fundamentals

Cloud consumption pricing inverts the traditional capital-expenditure (capex)
model: instead of purchasing hardware sized for peak demand years in
advance, teams pay operating expenditure (opex) for what they consume,
scaling up and down with demand. This shift has architectural consequences:

- **Elasticity becomes a design requirement**, not an optimization — an
  architecture that cannot scale down wastes the primary economic benefit of
  the model.
- **Idle capacity is a direct, continuous cost**, unlike depreciating
  owned hardware, which motivates aggressive automation of start/stop and
  scale-to-zero patterns.
- **Committed-use and reservation instruments** (covered in Chapter 08) let
  an organization trade flexibility for discount once a workload's baseline
  demand is well understood.

## Design Considerations

### Choosing a service model per workload

Favor the highest-level service model that meets the workload's control,
compliance, and portability requirements. A team defaulting to IaaS for
every workload "because that's what we know" pays an ongoing operational
tax (patching, scaling logic, high-availability wiring) that a managed
PaaS or SaaS equivalent would absorb. Conversely, workloads with unusual
kernel, driver, or licensing requirements, or that require deep control
over the network stack, still belong on IaaS.

### Provider selection criteria

Evaluate providers (or provider combinations) against:

- **Capability breadth and maturity** for the specific services the
  workload needs, not just marketing feature lists.
- **Regional footprint** relative to user and data-residency requirements.
- **Compliance attestations** relevant to the industry (audit reports,
  certifications) and how quickly the provider extends new attestations to
  new regions.
- **Existing organizational skills and tooling** — a second provider adds
  real operational cost even when the target workload is simple.
- **Pricing model fit** — consumption-based, reserved, or spot/preemptible
  capacity, matched to the workload's demand shape.

### Portability and exit strategy

Every adoption of a provider-managed service is a deliberate trade of
portability for reduced operational burden. Make the trade consciously:

- Prefer open standards and widely supported runtimes at the application
  layer (containers, standard SQL dialects, object storage APIs) when
  portability is a stated requirement.
- Where a proprietary managed service is adopted for its operational value
  (which is often the right call), document the estimated cost and time to
  migrate away from it, so the decision is revisited with facts rather than
  re-litigated from scratch during an outage or contract renegotiation.
- Do not conflate "multicloud" with "portable" — running on two providers
  without an abstraction layer usually means maintaining two full
  implementations, not one portable one. See Chapter 07 for the trade-offs
  in more detail.

### SLA interpretation and composite availability

A provider's published SLA for a single service is not the availability a
customer's application actually delivers. Composite availability compounds
across every dependency in the request path. For independent components in
series, multiply the availabilities:

```text
Availability(system) = Availability(A) x Availability(B) x Availability(C)
```

For example, a three-tier design depending on a compute service (99.99%),
a managed database (99.95%), and a DNS/routing layer (99.99%) in series
yields:

```text
0.9999 x 0.9995 x 0.9999 = 0.9993 (~99.93%)
```

That is roughly 6.1 hours of potential annual downtime, worse than any
single component's published number — a common and costly misreading during
design review. Redundant components in parallel (for example, two
independent AZ deployments behind a load balancer) combine differently:

```text
Availability(parallel) = 1 - [(1 - A1) x (1 - A2)]
```

Two independent 99.9%-available zonal deployments in parallel yield
`1 - (0.001 x 0.001) = 0.999999` (~99.9999%) for that tier alone, assuming
true independence of failure modes — which is only valid if the zones do
not share a hidden single point of failure such as a single regional DNS
endpoint or a single control-plane dependency.

### Build vs. buy for platform capabilities

Before building a capability (a custom secrets rotation service, a custom
job scheduler) on IaaS, evaluate whether a managed equivalent already meets
the requirement. The build option is frequently chosen for perceived control
but rarely accounts for the ongoing patching, on-call, and disaster-recovery
burden the team is implicitly signing up to carry indefinitely.

## Implementation and Automation

### IaC-first operating model

Treat infrastructure as code from the first resource created, not as a
retrofit. Every subsequent chapter in this volume assumes an
infrastructure-as-code (IaC) baseline using a declarative tool such as
Terraform (illustrative examples in this volume use Terraform-style HCL at
the 1.9.x baseline recorded in `SOFTWARE_VERSIONS.md`; exact provider syntax
varies by cloud and by tool — OpenTofu, Pulumi, and provider-native
frameworks follow the same principles).

A minimal, provider-neutral root module structure:

```text
foundation/
├── main.tf          # Provider and top-level resource wiring
├── variables.tf      # Input variables (environment, region, tags)
├── outputs.tf        # Values consumed by downstream modules/pipelines
├── versions.tf        # Required provider and Terraform version constraints
└── terraform.tfvars.example
```

```hcl
# versions.tf — illustrative; pin exact provider source/version per vendor.
terraform {
  required_version = ">= 1.9.0"
  required_providers {
    cloud = {
      source  = "<PROVIDER_NAMESPACE>/<PROVIDER_NAME>"
      version = ">= 5.0"
    }
  }
}
```

```hcl
# variables.tf — a tagging/labeling contract enforced across every module.
variable "environment" {
  description = "Deployment environment identifier."
  type        = string
  validation {
    condition     = contains(["dev", "test", "stage", "prod"], var.environment)
    error_message = "environment must be one of: dev, test, stage, prod."
  }
}

variable "owner_tag" {
  description = "Team or cost-center accountable for the resource."
  type        = string
}
```

Native `validation` blocks like the one above are the first line of policy
enforcement — cheap, fast, and run before any API call is made. Chapter 02
and Chapter 08 build on this with organization-wide policy-as-code guardrails
that catch what per-module validation cannot.

### CLI, console, and API — automation-first principle

Every provider exposes the same underlying control-plane API through three
surfaces: an interactive console, a CLI, and the API/SDK directly. Adopt an
automation-first default: the console is for exploration, incident response,
and read-only review; anything that creates or changes a resource in a
persistent environment goes through code, reviewed and applied by a
pipeline. This is not a stylistic preference — it is what makes drift
detection, audit trails, and disaster recovery via redeploy possible.

## Validation and Troubleshooting

- **Validate the responsibility boundary, not just the resource.** For every
  managed service adopted, write down (in the architecture decision record)
  which specific security and reliability controls the provider guarantees
  and which the team must implement. Review this list at each major version
  or SLA change from the provider.
- **Common misconception: "cloud is inherently more secure."** The
  provider's physical and hypervisor security posture is generally strong,
  but misconfiguration of the customer-owned portion of the responsibility
  boundary (identity, network exposure, storage access policy) is the
  dominant cause of cloud security incidents industry-wide. Treat the cloud
  as neutral ground that inherits the rigor — or the gaps — of the team
  operating it.
- **Common misconception: region and zone are interchangeable.** A
  single-region, single-zone deployment has no protection against a
  zone-level failure regardless of how the provider markets regional
  durability for storage; compute and networking resilience must be
  designed explicitly across zones.
- **Diagnosing a control-plane vs. data-plane incident.** If existing
  connections continue to serve traffic but new deployments, scaling
  actions, or resource lookups fail, suspect a control-plane issue —
  check the provider's status page and avoid triggering additional
  control-plane calls (such as repeated retries of a failing create
  operation) that can extend the incident. If existing traffic is failing
  end to end, the issue is data-plane or the workload itself.
- **Re-run the composite availability calculation** whenever a dependency is
  added to a critical path — a single new synchronous call to an external
  service silently lowers the system's ceiling regardless of how resilient
  the rest of the design is.

## Security and Best Practices

- Document the shared responsibility boundary per service in onboarding
  material and architecture decision records; do not leave it implicit.
- Apply the security pillar of the Well-Architected framework as a
  standing design-review gate, not a one-time checklist at launch.
- Default to the least-privileged, most-managed service model that meets
  requirements — every layer of infrastructure a team operates directly is
  a layer it must also patch, monitor, and defend.
- Treat provider status pages and change logs as an operational input;
  subscribe programmatically where the provider supports it, rather than
  relying on manual checks.
- Avoid single points of shared fate: verify that "redundant" components
  do not secretly share a control-plane dependency, a DNS zone, or a
  certificate authority that would defeat the redundancy under a real
  failure.

## References and Knowledge Checks

### References

- NIST SP 800-145, *The NIST Definition of Cloud Computing*.
- NIST SP 800-146, *Cloud Computing Synopsis and Recommendations*.
- Each major provider's published Well-Architected (or equivalent) framework
  documentation — consult the current vendor source, since pillar names and
  guidance are revised independently of this chapter.
- `SOFTWARE_VERSIONS.md` in this repository for the Terraform baseline used
  in illustrative examples throughout this volume.

### Knowledge checks

1. A workload requires kernel-level tuning and a licensed driver unavailable
   on any managed runtime. Which service model is appropriate, and why?
2. A managed relational database service encrypts data at rest by default.
   Whose responsibility is it to ensure application-layer field encryption
   for a regulated data element, and why?
3. Two independent zonal deployments each publish 99.95% availability and
   sit behind a shared DNS record with no independent failover mechanism.
   What is the actual availability ceiling of the combined system, and why
   is the naive parallel-availability formula not valid here?
4. Name two indicators that distinguish a control-plane incident from a
   data-plane incident during a live provider event.
5. Why does adding a synchronous call to a third-party API in a request path
   always lower a system's theoretical maximum availability, even if the
   third party's own SLA is excellent?

## Hands-On Lab

### Lab 1.1 — Provider-neutral IaC scaffold with tagging governance

This lab builds a minimal, fully local Terraform root module that enforces a
tagging/labeling contract before any real cloud resource is ever created. It
requires no cloud account and no credentials, and it is safe to run
repeatedly on a laptop or CI runner.

**Prerequisites**

- Terraform 1.9.x or later (`terraform -version` to confirm) or a compatible
  OpenTofu release.
- A POSIX shell.
- No cloud account, credentials, or network access required — this lab uses
  only Terraform's built-in `local` and `random` providers, which run
  entirely on the local machine.

**Steps**

1. Create a working directory and the module files.

   ```bash
   mkdir -p ~/labs/vol07-ch01 && cd ~/labs/vol07-ch01
   ```

2. Create `versions.tf`:

   ```hcl
   terraform {
     required_version = ">= 1.9.0"
     required_providers {
       local  = { source = "hashicorp/local",  version = ">= 2.5" }
       random = { source = "hashicorp/random", version = ">= 3.6" }
     }
   }
   ```

3. Create `variables.tf` with a validated tagging contract:

   ```hcl
   variable "environment" {
     type = string
     validation {
       condition     = contains(["dev", "test", "stage", "prod"], var.environment)
       error_message = "environment must be one of: dev, test, stage, prod."
     }
   }

   variable "owner_tag" {
     type = string
     validation {
       condition     = length(var.owner_tag) > 0
       error_message = "owner_tag must not be empty."
     }
   }
   ```

4. Create `main.tf`, which simulates resource creation locally (a
   `local_file` stands in for a real cloud resource) and stamps the
   validated tags into it:

   ```hcl
   resource "random_id" "resource_suffix" {
     byte_length = 4
   }

   resource "local_file" "simulated_resource" {
     filename = "${path.module}/output/resource-${random_id.resource_suffix.hex}.json"
     content = jsonencode({
       environment = var.environment
       owner       = var.owner_tag
       created_by  = "terraform"
     })
   }
   ```

5. Create `outputs.tf`:

   ```hcl
   output "resource_file" {
     value = local_file.simulated_resource.filename
   }
   ```

6. Initialize and apply with valid input:

   ```bash
   terraform init
   terraform apply -auto-approve \
     -var="environment=dev" \
     -var="owner_tag=platform-team"
   ```

   **Expected result:** Terraform reports `Apply complete! Resources: 2
   added`, and `output/resource-<hex>.json` exists containing the
   `environment` and `owner` values supplied.

7. Verify the output file:

   ```bash
   cat output/resource-*.json
   ```

   **Expected result:** JSON containing `"environment": "dev"` and
   `"owner": "platform-team"`.

**Negative test**

8. Attempt to apply with an invalid environment value:

   ```bash
   terraform apply -auto-approve \
     -var="environment=production" \
     -var="owner_tag=platform-team"
   ```

   **Expected result:** Terraform refuses to proceed and reports the custom
   validation error `environment must be one of: dev, test, stage, prod.`
   This demonstrates policy enforcement at the module boundary, before any
   resource (simulated or real) is touched.

**Cleanup**

9. Destroy the local state and remove the working directory:

   ```bash
   terraform destroy -auto-approve \
     -var="environment=dev" \
     -var="owner_tag=platform-team"
   cd ~ && rm -rf ~/labs/vol07-ch01
   ```

   **Expected result:** Terraform reports `Destroy complete! Resources: 2
   destroyed`, and the working directory no longer exists.

## Summary and Completion Checklist

This chapter established the vocabulary and mental models the rest of the
volume builds on: service models and where the operational boundary sits in
each, deployment models and their primary selection drivers, the shared
responsibility model as a documented (not assumed) artifact, provider
physical/logical architecture (regions, zones, edge, control plane vs. data
plane), a provider-neutral Well-Architected-style pillar framework, and the
composite-availability math that keeps SLA claims honest during design
review.

- [ ] Can explain the operational boundary for IaaS, PaaS, SaaS, and FaaS.
- [ ] Can state the shared responsibility model for a specific managed
      service used in your environment, in writing.
- [ ] Can compute composite availability for a multi-tier design and explain
      why it differs from any single component's published SLA.
- [ ] Can distinguish a control-plane incident from a data-plane incident.
- [ ] Completed Lab 1.1, including the negative test and cleanup.
