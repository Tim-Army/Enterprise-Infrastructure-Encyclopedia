# Chapter 1: Resilience Engineering and Critical-Service Design

![Lab flow for this chapter: find_spof.py analyzes a dependency graph and reports web-frontend and api-service as SPOFs, since both sit on the only path from ingress to the critical services; auth-service is correctly not reported, since it is a leaf with no outgoing path back toward the critical services — a shared-dependency risk rather than a topological chokepoint. As a negative test, removing the web-frontend-to-api-service edge leaves api-service with no inbound edge at all; every remaining node is then trivially reported as a 'SPOF', correctly signaling that the redesign severed the only route in — a worse problem than any single SPOF.](../../../diagrams/volume-12-resilience-lifecycle-management/chapter-01-spof-dependency-graph-flow.svg)

*Figure 1-1. Flow used throughout this chapter's Hands-On Lab: single-point-of-failure detection on a dependency graph, distinguishing topological chokepoints from shared-dependency risk.*

## Learning Objectives

- Define resilience engineering and distinguish it from adjacent disciplines such as high availability, disaster recovery, and security hardening.
- Classify services into criticality tiers and justify a tiering decision using business, technical, and regulatory inputs.
- Identify failure domains, blast radius, and single points of failure (SPOFs) in a multi-tier architecture.
- Apply core resilience patterns — redundancy, isolation, statelessness, and graceful degradation — to a service design.
- Calculate theoretical availability from component MTBF/MTTR figures and explain where the math breaks down in practice.
- Build a reusable service criticality register and dependency map that downstream chapters (BIA, HA design, DR, chaos testing) consume.

## Theory and Architecture

### Resilience Engineering as a Discipline

Resilience engineering is the deliberate practice of designing, building, and operating systems that continue to deliver acceptable service when components fail, inputs are hostile, or conditions exceed what was planned for. It is broader than high availability (HA), which is one implementation technique among several, and broader than disaster recovery (DR), which addresses a narrower class of large-scale, low-frequency events. Resilience engineering treats failure as a certainty rather than an exception: hardware fails, networks partition, humans make mistakes, dependencies degrade, and demand spikes unpredictably. The discipline's output is not a single control but a layered set of architectural decisions, operational practices, and organizational habits that keep the gap between "designed capacity" and "actual conditions" survivable.

Four properties distinguish a resilient system from a merely redundant one:

1. **Anticipation** — the organization has enumerated plausible failure modes before they occur, rather than discovering them during an incident.
2. **Absorption** — the system tolerates a defined amount of stress (component loss, latency, traffic surge) without operator intervention.
3. **Recovery** — when absorption capacity is exceeded, the system returns to a known-good state within a bounded time, and that bound is measured, not assumed.
4. **Adaptation** — lessons from near-misses and actual failures feed back into design, so the same failure mode does not recur unaddressed.

This chapter establishes the vocabulary and design primitives that the rest of Volume XII builds on: [Chapter 2](02-business-impact-analysis-and-continuity-planning.md) formalizes anticipation through business impact analysis; [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md) formalizes absorption through HA and fault-tolerance patterns; [Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md) formalizes recovery through backup and DR engineering; [Chapter 5](05-resilience-testing-exercises-and-chaos-engineering.md) formalizes adaptation through resilience testing and chaos engineering.

### Failure Domains and Blast Radius

A **failure domain** is the boundary within which a single fault can propagate without crossing into another domain. Failure domains exist at every layer of an architecture: a power circuit, a top-of-rack switch, a hypervisor host, an availability zone, a database shard, a Kubernetes node pool, a cloud region, or a third-party API provider. **Blast radius** is the practical consequence of a failure domain boundary — the set of users, transactions, or downstream services affected when that domain fails completely.

Resilient architectures are built by deliberately shrinking blast radius: partitioning a monolith into cells, sharding a database by customer or region, deploying compute across multiple availability zones, and isolating noisy-neighbor workloads with resource quotas. The trade-off is complexity and cost — more domains mean more failover logic, more data consistency questions, and more infrastructure to operate. [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md) covers the mechanics of multi-domain HA design in depth; this chapter is concerned with identifying and cataloging the domains that exist in a given architecture before deciding how to protect them.

### Criticality Tiering

Not every service warrants the same investment in resilience. A criticality tier framework maps each service to a target availability, an acceptable outage duration, and a corresponding architecture pattern. A common four-tier model:

| Tier | Description | Target Availability | Typical RTO | Typical Pattern |
| --- | --- | --- | --- | --- |
| Tier 0 | Life-safety, regulatory, or revenue-blocking; outage halts the business | 99.99%+ | Minutes | Active-active, multi-region, automated failover |
| Tier 1 | Core business function; outage is highly visible and costly | 99.9–99.99% | < 1 hour | Active-passive HA, automated failover |
| Tier 2 | Important but has manual workarounds | 99.5–99.9% | Hours | Clustered, manual or semi-automated failover |
| Tier 3 | Internal tooling, batch, non-customer-facing | 99–99.5% | Next business day | Backup/restore, no HA requirement |
| Tier 4 | Development, sandbox, decommission-candidate | Best effort | Not defined | None |

Tiering is a cross-functional decision, not an engineering-only one: it requires input from the business process owner (see [Chapter 2](02-business-impact-analysis-and-continuity-planning.md)'s business impact analysis methodology), the application owner, and often legal or compliance for regulated workloads. Tiering feeds directly into the redundancy budget — it is neither affordable nor necessary to run every service active-active across three regions.

### Core Resilience Patterns

Four patterns recur throughout this volume and are worth naming precisely before they are applied:

- **Redundancy** — duplicating a component so that the failure of one instance does not remove the capability. Redundancy is characterized by an N+M notation: N is the number of units required to carry full load, M is the number of spare units. N+1 tolerates one failure; 2N (equivalent to N+N) tolerates the loss of an entire half of capacity, commonly used for power and cooling.
- **Isolation** — bounding the blast radius of a failure through bulkheads: separate connection pools, separate thread pools, separate compute nodes, or separate network segments per tenant or function, so that saturation in one area cannot starve another.
- **Statelessness** — designing compute components to hold no durable state locally, so any instance can be replaced or added without a data-migration step. State is pushed to a purpose-built, independently resilient store (a database, object store, or cache tier).
- **Graceful degradation** — defining reduced-functionality modes that preserve the most critical capability of a service when full capacity is unavailable, rather than failing the entire request. [Chapter 3](03-high-availability-fault-tolerance-and-graceful-degradation.md) covers the implementation mechanics (circuit breakers, load shedding, feature flags) in detail.

### Reliability Math Refresher

Two figures anchor most availability conversations:

- **MTBF (Mean Time Between Failures)** — the average operating time between failures of a repairable component.
- **MTTR (Mean Time To Repair/Recover)** — the average time to restore a failed component to service.

Availability for a single component is:

```text
Availability = MTBF / (MTBF + MTTR)
```

For a series system (every component must be up for the system to be up), availabilities multiply:

```text
A_system = A_1 x A_2 x A_3 x ... x A_n
```

This is why chaining five "three-nines" (99.9%) components in series without redundancy yields roughly 99.5% availability, not 99.9% — each additional dependency in the critical path erodes the ceiling. For a parallel system with two identical components where either can carry the load:

```text
A_parallel = 1 - [(1 - A) x (1 - A)]
```

Two independent components at 99% availability in parallel yield 99.99% — a two-nines improvement from redundancy alone, provided the failures are truly independent (not sharing a power feed, a network path, or a software bug). This last caveat is the most common modeling error in practice: redundant pairs that share a hidden common-mode failure point deliver none of the calculated benefit. Identifying shared fate between "redundant" components is a primary output of the dependency-mapping exercise in this chapter's lab.

## Design Considerations

### Identifying Single Points of Failure

A SPOF is any component whose failure removes service capability with no automatic compensating path. SPOFs are not always obvious hardware — they are frequently:

- A single DNS zone or single authoritative name server for a critical hostname.
- A single certificate that, if it expires, takes down TLS termination for every dependent service.
- A shared authentication or authorization service with no fallback ([Chapter 4](04-backup-recovery-and-disaster-recovery-engineering.md)'s dependency on identity, and [Volume IV](../../volume-04-enterprise-systems-administration/README.md)'s directory services chapters, both intersect here).
- A single human who is the only person who knows how to execute a recovery procedure — an organizational SPOF as real as a hardware one.
- A single cloud region, single availability zone, or single third-party SaaS dependency embedded deep in a call graph.

SPOF identification should be systematic, not anecdotal. The lab in this chapter builds a dependency map specifically to surface these paths.

### Redundancy Trade-offs

Redundancy is not free, and more is not automatically better:

| Consideration | Impact |
| --- | --- |
| Cost | N+1 roughly doubles compute/licensing cost for the protected tier; 2N doubles again |
| Operational complexity | Failover logic, data synchronization, and split-brain avoidance all add operational surface area |
| Consistency | Synchronous replication for strong consistency costs latency; asynchronous replication risks data loss on failover |
| Testing burden | Redundancy that is never exercised is unverified and frequently broken when needed (see [Chapter 5](05-resilience-testing-exercises-and-chaos-engineering.md)) |

A resilient design matches redundancy investment to the criticality tier established earlier, and documents the residual risk explicitly rather than implying that redundancy equals zero risk.

### Coupling, Statelessness, and Isolation

Tight coupling between services — synchronous call chains, shared databases, shared credentials — multiplies blast radius: a failure or slowdown in one service directly degrades every caller. Design reviews should evaluate:

- Can this component be replaced with a fresh instance in under a minute with no data loss?
- Does a failure in a non-critical dependency (for example, a recommendation service) block a critical path (for example, checkout)? If so, is that call asynchronous, cached, or protected by a circuit breaker and a default response?
- Are noisy-neighbor workloads isolated with quotas, separate node pools, or separate namespaces?

### Aligning Architecture to Business Criticality

The most common resilience design failure is not a missing pattern — it is a mismatch between engineering effort and business criticality. Engineering teams over-invest in resilience for internal tooling they personally find interesting and under-invest in an unglamorous batch job that, it turns out, gates monthly revenue recognition. The criticality register produced in this chapter's lab is the artifact that prevents this mismatch: it forces an explicit, reviewed statement of tier before architecture decisions are made.

## Implementation and Automation

### Building a Service Criticality Register

A criticality register is a structured, version-controlled inventory, not a slide deck. A minimal schema:

```yaml
# criticality-register.yaml
- service_id: checkout-api
  owner: payments-team
  tier: 0
  target_availability: "99.99"
  rto_minutes: 5
  rpo_minutes: 0
  upstream_dependencies:
    - identity-service
    - payment-gateway-external
    - inventory-service
  downstream_consumers:
    - web-storefront
    - mobile-app-backend
  last_reviewed: "2026-06-01"

- service_id: nightly-reporting-batch
  owner: analytics-team
  tier: 3
  target_availability: "99.5"
  rto_minutes: 480
  rpo_minutes: 1440
  upstream_dependencies:
    - data-warehouse
  downstream_consumers:
    - finance-dashboards
  last_reviewed: "2026-05-14"
```

Storing this as structured data (YAML or JSON) rather than prose enables automation: CI checks that every production service has an entry, dashboards that group incidents by tier, and paging policies that route Tier 0/1 pages differently from Tier 3.

### Dependency Mapping as Code

Dependency maps decay quickly if maintained by hand. A pragmatic approach combines a declared dependency manifest (as above) with automated discovery from existing telemetry:

```bash
# Derive a first-pass dependency edge list from distributed trace data.
# Requires read access to a trace backend exposing a span-query API.
curl -s "https://traces.internal.example/api/v1/services/checkout-api/dependencies?window=7d" \
  | jq -r '.dependencies[] | "\(.parent) -> \(.child) (\(.call_count) calls, p99=\(.p99_ms)ms)"'
```

Reconcile the automated output against the declared manifest quarterly. Discrepancies are themselves valuable signal: an undeclared dependency is an unmanaged risk, and a declared dependency with zero observed traffic is a candidate for removal or reclassification.

### Encoding Redundancy in IaC

Redundancy decisions should be visible in infrastructure-as-code rather than left as tribal knowledge about "how many replicas we usually run." Example using Terraform 1.9.x syntax against a generic compute module:

```hcl
variable "service_tier" {
  description = "Criticality tier from the service register (0-4)"
  type        = number
}

locals {
  # Map criticality tier to a minimum replica count and spread policy.
  tier_replica_map = {
    0 = { min_replicas = 6, azs = 3 }
    1 = { min_replicas = 4, azs = 3 }
    2 = { min_replicas = 2, azs = 2 }
    3 = { min_replicas = 1, azs = 1 }
    4 = { min_replicas = 1, azs = 1 }
  }
  redundancy = local.tier_replica_map[var.service_tier]
}

resource "example_compute_group" "app" {
  name             = "checkout-api"
  min_size         = local.redundancy.min_replicas
  availability_zone_count = local.redundancy.azs
}
```

This ties the redundancy level directly to the register's declared tier, so a tier change is a one-line diff rather than a manual infrastructure change that can silently drift from policy.

### Automating SPOF Detection

Static analysis of the dependency graph can flag nodes with in-degree above a threshold and no declared redundant path:

```python
import networkx as nx

def find_spofs(graph: nx.DiGraph, critical_services: set[str]) -> list[str]:
    """Return nodes whose removal disconnects any critical service
    from its declared entry points."""
    spofs = []
    for node in graph.nodes:
        if node == "ingress":
            continue  # the entry point itself is not a candidate SPOF
        trial = graph.copy()
        trial.remove_node(node)
        for svc in critical_services:
            if svc in trial and not nx.has_path(trial, "ingress", svc):
                spofs.append(node)
                break
    return spofs
```

The entry-point guard matters: without it, the loop eventually tries to
remove `"ingress"` itself, and the subsequent `nx.has_path(trial, "ingress", svc)`
call raises `NodeNotFound` instead of returning a result, since the source
node no longer exists in the trial graph. Also note what this algorithm
does and does not detect: it finds *topological* SPOFs — nodes that sit on
the only path between the entry point and a critical service. It does not
find *shared-dependency* SPOFs — a node with no path-blocking role but that
many services call at runtime (a shared auth service, for example). A node
can be a real operational risk without ever appearing in this list; treat
it as one input to SPOF identification, not the whole analysis.

Run this analysis as a scheduled job against the dependency graph produced above, and alert when a new SPOF appears — most commonly introduced by a well-intentioned shared-services consolidation.

## Validation and Troubleshooting

### Verifying Redundancy Actually Works

Declared redundancy is a hypothesis until it is tested. Validation steps:

1. Confirm that redundant instances are physically or logically separated (different racks, different AZs, different power feeds) — query the cloud provider's or hypervisor's placement metadata rather than trusting naming conventions.
2. Confirm load balancer or DNS health checks actually remove a failed instance from rotation within the target RTO.
3. Confirm that removing one redundant unit does not silently violate a capacity assumption (N+1 that is actually running at N because of unaccounted growth).

### Common Anti-Patterns

- **Redundant but co-located**: two "redundant" VMs on the same hypervisor host, defeating the purpose of the redundancy.
- **Shared control plane**: independent data planes that all depend on one unreplicated configuration service or license server.
- **Silent capacity drift**: N+1 designed at launch that has become N+0 as traffic grew without a corresponding capacity review.
- **Redundancy without failover testing**: see [Chapter 5](05-resilience-testing-exercises-and-chaos-engineering.md) — untested failover is common cause of failed recovery during real incidents.

### Troubleshooting Availability Math Mismatches

When measured availability does not match the calculated theoretical availability, check for:

- Correlated failures (shared dependency violates the independence assumption behind the parallel-system formula).
- MTTR figures based on best-case manual recovery rather than observed incident data.
- Uncounted partial outages — degraded-but-technically-up states that customers experience as an outage but that internal availability tracking does not capture.

## Security and Best Practices

- Treat the criticality register and dependency map as sensitive operational data: they are a target map for an attacker planning to maximize impact. Restrict read access appropriately while keeping it available to the teams that need it.
- Do not let resilience redundancy undermine security segmentation — a redundant path that bypasses a firewall or an approval gate to save failover time is a control gap, not a resilience win. Coordinate with [Volume X](../../volume-10-enterprise-cybersecurity/README.md)'s cybersecurity architecture guidance when redundant paths cross trust boundaries.
- Avoid single points of failure in identity and secrets management specifically; an expired certificate or a locked-out break-glass account has caused more real outages industry-wide than raw hardware failure.
- Review the criticality register at a fixed cadence (quarterly is typical) and whenever a service's business role changes materially — a tier assignment that was correct at launch silently becomes wrong as a service's role in the business evolves.
- Keep tiering decisions and their rationale in version control with reviewable history; an auditor or incident reviewer will ask why a service was tiered the way it was.

## References and Knowledge Checks

### References

- ISO 22301:2019, *Security and resilience — Business continuity management systems*.
- NIST SP 800-34 Rev. 1, *Contingency Planning Guide for Federal Information Systems*.
- Site Reliability Engineering practices as documented in the publicly available Google SRE book series (sre.google/books).
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) for the Terraform baseline used in this chapter's examples.

### Knowledge Checks

1. Explain the difference between a failure domain and blast radius, and give an example where shrinking one does not shrink the other.
2. A service has two "redundant" application servers, both plugged into the same power distribution unit. What is the actual availability benefit of this configuration, and why?
3. Walk through the four criticality tiers and identify which architecture pattern each typically requires.
4. Why can automated dependency discovery from trace data diverge from a manually maintained dependency manifest, and which source should be treated as authoritative?
5. Describe two organizational (non-technical) single points of failure and how to mitigate each.

## Hands-On Lab

### Lab: Building a Criticality Register and SPOF Map

**Objective:** Produce a version-controlled criticality register and a dependency graph for a sample three-tier application, then use the graph to identify at least one single point of failure.

**Prerequisites:**

- A workstation with `git`, `python3` (3.11+), `pip`, and `jq` installed.
- Python packages: `networkx`, `pyyaml` (`pip install networkx pyyaml`).
- A text editor.

**Procedure:**

1. Create a working directory and initialize the register file.

   ```bash
   mkdir -p ~/labs/resilience-ch1 && cd ~/labs/resilience-ch1
   ```

2. Create `criticality-register.yaml` describing a sample three-tier application (web front end, API service, database) plus one shared authentication service, using the schema shown earlier in this chapter. Assign tiers 0–3 to each component based on your own judgment of business impact.

3. Create `dependencies.yaml` listing directed edges, for example:

   ```yaml
   edges:
     - [ingress, web-frontend]
     - [web-frontend, api-service]
     - [api-service, auth-service]
     - [api-service, database]
     - [web-frontend, auth-service]
   ```

4. Write `find_spof.py` implementing the SPOF-detection function shown earlier in this chapter, loading `dependencies.yaml` and treating `api-service` and `database` as the critical services to protect.

5. Run the analysis:

   ```bash
   python3 find_spof.py
   ```

**Expected Result:** The script reports `['web-frontend', 'api-service']` as SPOFs. Both sit on the *only* path from `ingress` to the critical services: removing `web-frontend` disconnects `ingress` from everything downstream, and removing `api-service` disconnects `ingress` from `database` (its only inbound edge). `auth-service` is **not** reported, even though both `web-frontend` and `api-service` call it — the graph's edges point from caller to callee, so `auth-service` is a leaf with no outgoing path back toward the critical services, and removing a leaf can never disconnect anything upstream of it. This is a useful distinction to internalize: a widely-depended-upon service like a shared auth provider is a real operational risk, but it is a *shared-dependency* risk, not the *topological chokepoint* risk this particular algorithm detects — treat them as two different questions.

6. Update `criticality-register.yaml` to raise `web-frontend` and `api-service` to reflect that each is a hard chokepoint for every request, and add a note in `last_reviewed` justifying the change.

**Negative Test:** Remove the `[web-frontend, api-service]` edge from `dependencies.yaml` (simulating a redesign where the web front end talks only to auth, not the API) and rerun the script. `api-service` now has no inbound edge at all, so it is unreachable from `ingress` regardless of which other node is removed — the script reports every remaining node (`['web-frontend', 'api-service', 'auth-service', 'database']`) as a "SPOF" for it. That result is correct, if blunt: when a critical service loses its only path in, every node trivially satisfies "removing this node leaves the service unreachable," because it was already unreachable before any node was removed. The finding here is not "four new SPOFs appeared" — it is that the redesign severed the only route to `api-service` entirely, which is a worse problem than any single SPOF. If the SPOF list does not change at all after this edit, the detection logic or the edge list is broken, not the architecture.

**Validation Evidence:** Capture the script output before and after step 6 in a `RESULTS.md` file alongside the YAML files, showing the SPOF list shrinking or the tier assignment change.

**Cleanup:**

```bash
cd ~ && rm -rf ~/labs/resilience-ch1
```

No shared or production systems were modified; this lab is entirely local to the working directory.

## Summary and Completion Checklist

Resilience engineering starts with an honest inventory: which services matter, how much, and what they depend on. Criticality tiering translates business impact into an engineering budget for redundancy; failure-domain and dependency analysis surface the SPOFs that undermine that redundancy; and the reliability math grounds availability targets in verifiable numbers rather than aspiration. Every later chapter in this volume — BIA, HA design, backup/DR, chaos testing, patching, modernization, sustainability, and decommissioning — treats the criticality register and dependency map built here as a foundational input.

**Completion checklist:**

- [ ] Can articulate the four properties of a resilient system (anticipation, absorption, recovery, adaptation).
- [ ] Can classify a service into a criticality tier and justify the assignment.
- [ ] Can compute series and parallel availability from MTBF/MTTR inputs and explain the independence assumption.
- [ ] Produced a version-controlled criticality register for a sample application.
- [ ] Produced a dependency graph and identified at least one SPOF programmatically.
- [ ] Understands why redundancy, isolation, statelessness, and graceful degradation are distinct patterns, not synonyms.
