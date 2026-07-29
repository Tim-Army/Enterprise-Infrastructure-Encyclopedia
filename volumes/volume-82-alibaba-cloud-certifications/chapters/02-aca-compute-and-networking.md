# Chapter 02: ACA — Compute and Networking

## Learning Objectives

- Launch and manage ECS instances.
- Design a VPC with vSwitches and routing.
- Secure traffic with security groups.
- Distribute load with SLB/ALB.
- Complete a walkthrough for each compute/networking topic.

## Theory and Architecture

The **ACA Cloud Computing** foundation starts with compute and networking. **ECS (Elastic Compute
Service)** provides virtual machines — you choose an **instance type** (vCPU/memory), **image**, and
**disk**, launch it into a network, and manage its lifecycle. Networking is built on the **VPC
(Virtual Private Cloud)** — an isolated private network defined by a **CIDR block**, subdivided into
**vSwitches** (subnets, each in one Availability Zone), with **route tables** directing traffic and
**Internet/NAT Gateways** for outbound/inbound internet. **Security groups** are stateful virtual
firewalls attached to ECS instances, allowing inbound/outbound traffic by protocol/port/source
(default-deny). **Server Load Balancer (SLB)** — with the newer **Application Load Balancer (ALB)**
for HTTP(S) — distributes traffic across backend ECS instances for scale and availability. Together
these are the core of any Alibaba Cloud deployment: compute in a segmented, secured, load-balanced
network. This chapter teaches each with a hands-on walkthrough (VPC/CIDR planning, security-group
rules, and load-balancing logic; aliyun CLI syntax with `python3` modeling).

## Design Considerations

Plan **VPC CIDR** and **vSwitch** subnets across **Availability Zones** for HA. Attach least-privilege
**security groups** (default-deny, allow only needed). Choose **ECS instance types** to workload. Use
**SLB/ALB** to distribute load across AZs. Separate public and private subnets (NAT for private
egress). Tag resources.

## Implementation and Automation

The labs plan a VPC, write security-group rules, and design load balancing.

## Validation and Troubleshooting

Confirm the compute/networking model:

```text
ECS = VMs (instance type + image + disk). VPC = isolated network (CIDR) -> vSwitches (subnets, one per AZ) + route tables + Internet/NAT gateways. Security groups = stateful firewalls on ECS (default-deny).
SLB/ALB = distribute traffic across backend ECS (scale + HA).
```

Common pitfalls: overlapping **VPC CIDRs** (blocks peering); and a single-AZ deployment (no HA — spread
vSwitches across **AZs**).

## Security and Best Practices

Plan non-overlapping **CIDRs**, spread **vSwitches across AZs**, attach least-privilege **security
groups**, and load-balance across AZs with **SLB/ALB**. Separate public/private subnets. All work is
authorized administration.

## Hands-On Lab

Compute/networking walkthroughs. **Shared prerequisites** — `python3`; aliyun CLI + free-tier optional.
**Cost:** none (modeled).

### Lab 2.1 — Plan a VPC and vSwitches

**Objective:** Segment the network across AZs.

```python
python3 - <<'PY'
import ipaddress
vpc=ipaddress.ip_network("10.0.0.0/16")
subnets=list(vpc.subnets(new_prefix=24))[:4]
zones=["az-a","az-b","az-a","az-b"]
for sn,az in zip(subnets,zones): print(f"vSwitch {sn} -> {az}")
print("VPC: /16 network split into /24 vSwitches spread across AZs for HA")
PY
```

**Expected result:** vSwitches carved from the VPC CIDR and **spread across AZs** — HA network design.

**Negative test:** put all vSwitches in **one AZ**; an AZ outage takes everything — spread across AZs.

**Cleanup:** none.

### Lab 2.2 — Write security-group rules

**Objective:** Least-privilege instance firewall.

```python
python3 - <<'PY'
rules=[("inbound","tcp",443,"0.0.0.0/0","allow web"),("inbound","tcp",22,"10.0.0.0/16","allow SSH from VPC only"),
       ("inbound","all","all","0.0.0.0/0","DENY (default)")]
for direction,proto,port,src,desc in rules: print(f"{direction} {proto}/{port} from {src}: {desc}")
print("Security group: default-deny; allow 443 from anywhere, SSH only from inside the VPC")
PY
```

**Expected result:** a least-privilege **security group** (web open, SSH internal-only, default-deny)
— ECS hardening.

**Negative test:** open SSH (22) to `0.0.0.0/0`; the world can brute-force it — restrict SSH to the
**VPC/bastion**.

**Cleanup:** none.

### Lab 2.3 — Design load balancing

**Objective:** Scale and survive failures.

```python
python3 - <<'PY'
alb={"listener":"HTTPS:443","backends":["ecs-az-a-1","ecs-az-b-1"],"health_check":"/healthz",
     "algorithm":"round robin","cross_zone":True}
for k,v in alb.items(): print(f"{k:12}: {v}")
print("ALB: distribute across AZs + health checks -> unhealthy backends removed automatically")
PY
```

**Expected result:** an **ALB** distributing across AZs with health checks — scalable, available
frontend.

**Negative test:** point users at a single ECS instance; it's a SPOF — front it with **SLB/ALB** across
AZs.

**Cleanup:** none.

### Lab 2.4 — Choose an ECS instance type

**Objective:** Right-size compute.

```python
python3 - <<'PY'
workloads={"web frontend":"general purpose (g-series), moderate vCPU/mem",
           "in-memory cache":"memory optimized (r-series)","batch compute":"compute optimized (c-series)",
           "ML training":"GPU instance (gn-series)"}
for wl,itype in workloads.items(): print(f"{wl:16}: {itype}")
print("ECS: match instance family to the workload (general/compute/memory/GPU)")
PY
```

**Expected result:** each workload matched to an **ECS instance family** — right-sized compute.

**Negative test:** run ML training on a general-purpose instance with no GPU; it's slow/costly — use a
**GPU instance**.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ACA compute and networking covers ECS instances in a VPC segmented by vSwitches across AZs, secured by
default-deny security groups and load-balanced with SLB/ALB — the core of any Alibaba Cloud deployment.

- [ ] I can plan a VPC and vSwitches across AZs.
- [ ] I can write least-privilege security-group rules.
- [ ] I can design load balancing.
- [ ] I can choose an ECS instance type.
- [ ] I completed Labs 2.1–2.4 including each negative test.
