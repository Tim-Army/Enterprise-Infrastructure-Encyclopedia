# Chapter 07: High Availability and Disaster Recovery

## Learning Objectives

- Explain why the binary hub is on the critical path and must not go down.
- Understand high-availability clustering for Artifactory.
- Place disaster recovery through replication.
- Describe repository federation across sites.

*Cert relevance: this is the **Associate JFrog DevOps HA/DR** certification — keeping the binary hub always available.*

## The binary hub is critical infrastructure

Once Artifactory is the [single source of truth for binaries (Chapter 2)](02-artifactory-the-universal-binary-repository.md), it sits on the **critical path of every build and every deployment.** Every CI job pulls dependencies from it; every deployment pulls artifacts from it. If Artifactory is **down**, then *no builds run and no deployments happen* — the entire software delivery pipeline halts, organization-wide. This makes it **critical infrastructure**, and its availability requirements are correspondingly high — the subject of the **HA/DR** certification.

The uncomfortable truth is that centralizing binaries (which brings all the benefits of the previous chapters) also **concentrates risk**: the one hub everything depends on is a single point of failure *unless* it is made highly available. The lab quantifies the blast radius of an outage.

## High availability: clustering

**High availability (HA)** eliminates the single point of failure by running Artifactory as a **cluster** of multiple nodes behind a load balancer, sharing storage and a database. If one node fails, the others keep serving — no downtime. HA is about surviving the *expected* failures (a node crashes, a server needs patching) without interrupting service: with a cluster, you can lose a node, or take one down for maintenance, and builds and deployments continue.

The certification covers designing this correctly — enough nodes for the load and for redundancy, shared storage that is itself redundant, a database that is highly available, and a load balancer distributing traffic. The lab models availability.

## Disaster recovery: replication

**High availability** handles a node failure *within* a site; **disaster recovery (DR)** handles losing an *entire site* (a data-center outage, a region failure). DR is achieved through **replication** — continuously copying artifacts (and configuration) to a **second site**, so that if the primary is lost, the secondary can take over with minimal data loss.

The distinction the certification tests: **HA ≠ DR.** HA protects against component failures within a site; DR protects against losing the whole site. A mature deployment needs *both* — an HA cluster at each site, and replication between sites. The lab distinguishes them.

## Repository federation

**Federation** addresses **multi-site organizations**: teams in different geographies each need fast, local access to the same binaries. A **federated repository** is automatically **bidirectionally synchronized** across multiple Artifactory instances in different locations — a developer in each region reads and writes to their *local* instance (fast), and the artifacts synchronize across all sites automatically. This gives every site local performance while keeping the binary set consistent globally — and, as a side effect, contributes to DR (the artifacts already exist in multiple places). The lab is covered within the availability exercise.

## Hands-On Lab

Python models availability and DR. **Cost:** none.

### Lab 7.1 — Why the binary hub must be highly available

**Objective:** Quantify the organization-wide blast radius of a hub outage, and how HA prevents it.

```bash
python3 - <<'EOF'
DEVELOPERS = 800
DEPLOYS_PER_DAY = 300
BUILDS_PER_DAY = 5000

print("Artifactory is on the CRITICAL PATH: every build + deploy pulls from it.\n")
print("SINGLE NODE (no HA) — the node goes down for 2 hours:")
frac = 2/24
builds_blocked = int(BUILDS_PER_DAY * frac)
deploys_blocked = int(DEPLOYS_PER_DAY * frac)
print(f"   ~{builds_blocked} builds and ~{deploys_blocked} deployments BLOCKED")
print(f"   all {DEVELOPERS} developers stalled — can't pull deps, can't ship")
print("   -> a 2-hour hub outage halts the ENTIRE delivery pipeline, org-wide.")
print("      Centralizing binaries concentrated the risk into one node.\n")

print("HA CLUSTER (3 nodes behind a load balancer):")
print("   node 2 crashes -> nodes 1 and 3 keep serving -> ZERO downtime")
print("   patch node 1 (take it out of rotation) -> others serve -> ZERO downtime")
print("   builds + deploys: uninterrupted\n")

print("Availability math (rough): if one node is up 99% of the time,")
p_node_down = 0.01
p_all_3_down = p_node_down ** 3
print(f"   1 node:  {100*(1-p_node_down):.1f}% available (down ~{0.01*365*24:.0f}h/yr)")
print(f"   3-node HA cluster: {100*(1-p_all_3_down):.6f}% (all 3 down at once is ~{p_all_3_down:.0e})")
print("\nThe lesson: making Artifactory the single source of truth puts it on the")
print("critical path of EVERY build and deploy — so an outage halts the whole pipeline")
print("for the whole org. HA (a multi-node CLUSTER) removes the single point of failure:")
print("lose a node, or patch one, and service continues. That's why the HA/DR cert")
print("exists — the binary hub is critical infrastructure and must never fully go down.")
print("\n(HA handles NODE failure within a site. Losing the whole SITE needs DR —")
print("replication to a second site. HA != DR; a mature setup has both.)")
EOF
```

**Expected result:** A single-node outage blocking thousands of builds and hundreds of deployments org-wide, versus an HA cluster surviving node failures and maintenance with zero downtime and far higher availability. The HA lesson is that centralizing binaries puts the hub on the critical path of every build and deploy, so it must be a highly-available cluster — with DR (site replication) as the separate defense against losing a whole site.

**Negative test:** Running the binary hub as a single node because it "usually works." An outage halts every build and deployment organization-wide; an HA cluster removes the single point of failure so node failures and maintenance cause no downtime.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The binary hub understood as critical infrastructure on the path of every build and deployment.
- [ ] High availability understood as a cluster removing the single point of failure within a site.
- [ ] Disaster recovery understood as replication to a second site — distinct from HA (HA ≠ DR).
- [ ] Repository federation understood as bidirectional cross-site synchronization for local performance and consistency.
