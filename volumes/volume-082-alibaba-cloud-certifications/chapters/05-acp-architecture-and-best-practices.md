# Chapter 05: ACP — Architecture and Best Practices

## Learning Objectives

- Design highly available, multi-AZ architectures.
- Scale automatically with Auto Scaling.
- Optimize cost across pricing models.
- Apply well-architected best practices.
- Complete a walkthrough for each architecture topic.

## Theory and Architecture

The **ACP Cloud Computing** level moves from operating services to **architecting** solutions.
**High availability** means eliminating single points of failure: deploy across multiple
**Availability Zones**, put ECS behind **SLB/ALB**, use **RDS multi-AZ** and **OSS** (inherently
redundant), and design for graceful degradation. **Auto Scaling** adjusts ECS capacity to demand —
scaling out on load (CPU/requests) and in when idle — for both **availability** and **cost**. **Cost
optimization** balances pricing models: **pay-as-you-go** for variable/short-lived workloads,
**subscription (reserved)** for steady baseline, and **preemptible/spot** instances for
fault-tolerant batch — right-sizing and turning off idle resources. Overarching this is a
**well-architected** mindset: reliability, security, performance efficiency, cost optimization, and
operational excellence — the same pillars across clouds. An ACP designs systems that are resilient,
elastic, cost-effective, and secure. This chapter teaches each with a hands-on walkthrough (HA design,
auto-scaling logic, and cost modeling).

## Design Considerations

Design **multi-AZ** with load balancing and managed-service redundancy (no SPOFs). Use **Auto
Scaling** with sensible thresholds and cooldowns. Optimize **cost** by matching pricing models to
workload patterns and right-sizing. Apply the **well-architected pillars**. Automate with
Infrastructure-as-Code (ROS / Terraform). Monitor with CloudMonitor.

## Implementation and Automation

The labs design HA, configure auto scaling, and optimize cost.

## Validation and Troubleshooting

Confirm the architecture model:

```text
HA: multi-AZ + SLB/ALB + RDS multi-AZ + OSS redundancy (no SPOFs). Auto Scaling: scale out/in on metrics (CPU/requests) for availability + cost. Cost: pay-as-you-go (variable) vs subscription/reserved (steady) vs preemptible/spot (batch) + right-sizing.
Well-architected pillars: reliability, security, performance, cost, operations.
```

Common pitfalls: a **single-AZ** "HA" design (still a SPOF at AZ level); and paying **on-demand** for a
steady 24/7 baseline (use **subscription/reserved**).

## Security and Best Practices

Design **multi-AZ** with no SPOFs, scale with **Auto Scaling**, optimize **cost** by pricing model and
right-sizing, and apply the **well-architected pillars**. Automate and monitor. All work is authorized
architecture.

## Hands-On Lab

Architecture walkthroughs. **Shared prerequisites** — `python3`. **Cost:** none (modeled).

### Lab 5.1 — Design a multi-AZ HA architecture

**Objective:** Eliminate single points of failure.

```python
python3 - <<'PY'
arch={"frontend":"ALB across az-a + az-b","compute":"ECS auto-scaling group spanning 2 AZs",
      "database":"RDS primary az-a + standby az-b (auto failover)","storage":"OSS (multi-AZ redundant)"}
for tier,design in arch.items(): print(f"{tier:9}: {design}")
print("ACP HA: every tier spans AZs -> no single point of failure")
PY
```

**Expected result:** an architecture with **every tier spanning AZs** — highly available design.

**Negative test:** call a single-AZ deployment "highly available"; an AZ outage kills it — span **AZs**.

**Cleanup:** none.

### Lab 5.2 — Configure Auto Scaling

**Objective:** Match capacity to demand.

```python
python3 - <<'PY'
scaling={"min":2,"max":10,"scale_out":"avg CPU > 70% for 5 min -> +2","scale_in":"avg CPU < 30% for 10 min -> -1",
         "cooldown":"300s"}
for k,v in scaling.items(): print(f"{k:11}: {v}")
print("Auto Scaling: grow on load, shrink when idle -> availability + cost efficiency")
PY
```

**Expected result:** an **Auto Scaling** policy (min/max, out/in thresholds, cooldown) — elastic
capacity.

**Negative test:** fix the fleet at peak size 24/7; you overpay off-peak — use **Auto Scaling**.

**Cleanup:** none.

### Lab 5.3 — Optimize cost by pricing model

**Objective:** Match pricing to workload.

```python
python3 - <<'PY'
workloads={"steady 24/7 baseline":"subscription (reserved) — cheapest for always-on",
           "variable daytime traffic":"pay-as-you-go for the peaks","fault-tolerant batch":"preemptible/spot (cheapest, interruptible)",
           "dev/test overnight":"stop when idle (pay only when running)"}
for wl,model in workloads.items(): print(f"{wl:26}: {model}")
PY
```

**Expected result:** each workload matched to a **pricing model** — cost optimization.

**Negative test:** run everything **pay-as-you-go** including a steady baseline; **subscription** is
cheaper for always-on — mix models.

**Cleanup:** none.

### Lab 5.4 — Apply the well-architected pillars

**Objective:** Evaluate a design holistically.

```python
python3 - <<'PY'
review={"Reliability":"multi-AZ + backups + auto scaling","Security":"RAM least privilege + WAF + Security Center",
        "Performance":"right-sized instances + CDN + caching","Cost":"reserved baseline + spot batch + right-sizing",
        "Operations":"IaC (ROS) + CloudMonitor + runbooks"}
for pillar,practice in review.items(): print(f"{pillar:12}: {practice}")
PY
```

**Expected result:** a design evaluated across the **five pillars** — well-architected review.

**Negative test:** optimize only for **cost** and ignore reliability/security; a cheap fragile system
fails — balance all **pillars**.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The ACP architects resilient, elastic, cost-effective Alibaba Cloud solutions — multi-AZ HA, Auto
Scaling, pricing-model cost optimization, and the well-architected pillars — moving from operating
services to designing systems.

- [ ] I can design a multi-AZ HA architecture.
- [ ] I can configure Auto Scaling.
- [ ] I can optimize cost by pricing model.
- [ ] I can apply the well-architected pillars.
- [ ] I completed Labs 5.1–5.4 including each negative test.
