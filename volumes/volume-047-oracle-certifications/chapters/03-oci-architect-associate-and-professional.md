# Chapter 03: OCI Architect (Associate and Professional)

## Learning Objectives

- Explain the OCI Architect Associate and Professional credentials.
- Summarize their exam topics.
- Apply OCI architecture: IAM, networking, compute, storage, and database design.
- Design for high availability, disaster recovery, and security (Professional).
- Complete a per-topic walkthrough for each Architect area.

## Theory and Architecture

The **OCI Architect** credentials certify designing and deploying solutions on
OCI:

- **Architect Associate (1Z0-1072)** — the core services in depth: **IAM**,
  **VCN networking**, **compute**, **storage**, **database**, and monitoring —
  deploying a working, secure architecture.
- **Architect Professional** — advanced design: **high availability and disaster
  recovery**, security architecture, hybrid/multicloud connectivity, migration,
  and cost/performance optimization.

Codes are year-versioned (e.g., **1Z0-1072-26**).

## Design Considerations

The Associate proves you can **build** a sound OCI environment; the Professional
proves you can **design** for resilience, security, and scale. Master VCN design
(subnets, gateways, routing, peering), IAM at scale (compartments, dynamic groups,
policies), storage/database selection, and — for the Professional — **HA/DR**
patterns (fault domains, availability domains, cross-region), **FastConnect/VPN**
connectivity, and migration approaches.

## Implementation and Automation

The labs below use OCI CLI patterns and design reasoning for each Architect area —
IAM, networking, compute/storage, database, and (Professional) HA/DR, security,
and connectivity.

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
education.oracle.com > OCI Architect Associate (1Z0-1072) / Professional:
  - Associate: IAM, VCN, compute, storage, database, monitoring
  - Professional: HA/DR, security, hybrid/multicloud, migration, optimization
```

Common pitfalls: single-AD deployments for HA (use multiple **ADs/fault
domains**); over-broad IAM; and public database subnets. On the Professional,
under-designing **DR** (define RTO/RPO and a cross-region strategy).

## Security and Best Practices

Design least-privilege **IAM**, private data tiers, and **defense-in-depth**
networking (NSGs, gateways); build for **HA** across fault/availability domains and
**DR** across regions to meet RTO/RPO; connect on-prem/multicloud with
**FastConnect/VPN**; and optimize cost with the right shapes and storage tiers.

## References and Knowledge Checks

- education.oracle.com: OCI Architect Associate and Professional exam topics; OCI Architecture Center; Well-Architected Framework.

**Knowledge checks**

1. What distinguishes the Architect Associate from the Professional?
2. How do fault domains, availability domains, and regions provide resilience?
3. What OCI options connect on-premises to OCI?

## Hands-On Lab

Per-topic walkthroughs — Architect Associate and Professional areas. OCI CLI is
illustrative.

**Shared prerequisites** — a shell; an OCI account for execution; `python3`.
**Cost:** none (Always Free where possible).

### Lab 3.1 — Associate: IAM at scale

**Objective:** Design compartments, dynamic groups, and policies.

```bash
python3 - <<'PY'
print("Compartments: per-environment (Dev/Test/Prod) isolation.")
print("Dynamic group: instances matching a rule (e.g., in compartment Prod) -> resource principals.")
print("Policy: 'Allow dynamic-group AppServers to read secrets in compartment Prod'")
PY
```

**Expected result:** an IAM design (compartments, dynamic groups, resource-principal
policy) — the IAM depth of the Associate.

**Negative test:** embed credentials in instances; use **dynamic groups +
resource principals** so instances authenticate without stored keys.

**Cleanup:** none.

### Lab 3.2 — Associate: VCN networking design

**Objective:** Design a multi-tier VCN.

```bash
python3 - <<'PY'
tiers = {"Public subnet":"load balancer (Internet Gateway)",
         "Private app subnet":"app servers (NAT GW for egress)",
         "Private DB subnet":"database (no internet; Service GW to OCI services)"}
for sub,role in tiers.items(): print(f"{sub:19} -> {role}")
PY
```

**Expected result:** a three-tier VCN with correct gateways — the networking design
of the Associate.

**Negative test:** give the DB subnet an Internet Gateway; keep it **private** with
a Service Gateway — never expose the database.

**Cleanup:** none.

### Lab 3.3 — Associate: compute and storage selection

**Objective:** Choose compute shapes and storage.

```bash
python3 - <<'PY'
print("Compute: Flexible shapes (choose OCPU/memory); autoscaling for variable load.")
print("Storage: Block (boot/data), Object (unstructured/backup, tiers), File (shared NFS).")
PY
```

**Expected result:** compute-shape and storage-type selection — the resource-design
area of the Associate.

**Negative test:** fixed shapes for spiky workloads; use **flexible shapes +
autoscaling** to match demand and cost.

**Cleanup:** none.

### Lab 3.4 — Associate: database services

**Objective:** Select an OCI database service.

```bash
python3 - <<'PY'
dbs = {"Autonomous Database":"self-managing (ATP/ADW); least ops",
       "Base Database / Exadata":"managed Oracle DB with more control",
       "MySQL HeatWave":"MySQL + in-memory analytics"}
for k,v in dbs.items(): print(f"{k:22}: {v}")
PY
```

**Expected result:** the OCI database options and when to use each — the database
area of the Associate.

**Negative test:** self-manage a DB on a VM when **Autonomous Database** fits;
prefer managed services to cut operational load.

**Cleanup:** none.

### Lab 3.5 — Professional: high availability and DR

**Objective:** Design HA/DR to an RTO/RPO.

```bash
python3 - <<'PY'
print("HA: spread across Fault Domains + Availability Domains in a region.")
print("DR: cross-region replication (Object Storage, Autonomous DB Autonomous Data Guard).")
print("Set RTO/RPO -> choose active-active, active-passive, or backup/restore accordingly.")
PY
```

**Expected result:** an HA/DR design mapped to RTO/RPO — the resilience design of
the Professional.

**Negative test:** deploy in one AD and call it HA; use **multiple ADs/fault
domains** and **cross-region** for DR.

**Cleanup:** none.

### Lab 3.6 — Professional: hybrid and multicloud connectivity

**Objective:** Connect OCI to on-prem/other clouds.

```bash
python3 - <<'PY'
conn = {"Site-to-Site VPN":"encrypted over internet (quick, lower bandwidth)",
        "FastConnect":"private, dedicated, high-bandwidth link",
        "Multicloud":"OCI-Azure Interconnect; database@Azure/AWS/GCP"}
for k,v in conn.items(): print(f"{k:18}: {v}")
PY
```

**Expected result:** the connectivity options (VPN, FastConnect, multicloud
interconnect) — the hybrid/multicloud design of the Professional.

**Negative test:** run production hybrid traffic over VPN expecting FastConnect
performance; choose **FastConnect** for bandwidth/latency SLAs.

**Cleanup:** none.

### Lab 3.7 — Professional: security architecture

**Objective:** Layer OCI security controls.

```bash
python3 - <<'PY'
controls = ["IAM least privilege + MFA","NSGs/security lists (segmentation)",
            "Vault (keys/secrets) + encryption","Cloud Guard (posture/threat detection)",
            "WAF + DDoS protection at the edge"]
for c in controls: print("-", c)
PY
```

**Expected result:** a defense-in-depth OCI security architecture — the security
design of the Professional.

**Negative test:** rely on network controls alone; layer **IAM, encryption, Cloud
Guard, and WAF** — defense in depth.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The OCI Architect credentials cover building (Associate — IAM, VCN, compute,
storage, database) and designing (Professional — HA/DR, security, hybrid/
multicloud, migration) solutions on OCI. Together they certify sound, resilient,
secure OCI architecture.

- [ ] I can design IAM (compartments, dynamic groups, policies) and a multi-tier VCN.
- [ ] I can select compute, storage, and database services.
- [ ] I can design HA/DR to an RTO/RPO and hybrid/multicloud connectivity.
- [ ] I can layer an OCI security architecture.
- [ ] I completed Labs 3.1–3.7 including each negative test.
