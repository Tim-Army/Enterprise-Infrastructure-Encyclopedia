# Chapter 01: The Alibaba Cloud Certification Program

## Learning Objectives

- Explain Alibaba Cloud and its position in the market.
- Describe the ACA / ACP / ACE certification levels and domains.
- Understand the Alibaba Cloud Academy exam model.
- Map credentials to roles and plan a path.
- Verify current program facts from the authoritative source.

## Theory and Architecture

**Alibaba Cloud** is the leading cloud provider in the Asia-Pacific region and a global hyperscaler,
offering the familiar building blocks — compute, networking, storage, databases, big data, security,
containers, and AI — under its own service names. Its certification program, run by **Alibaba Cloud
Academy**, has three levels: **ACA (Alibaba Cloud Associate)** for foundational skills, **ACP
(Alibaba Cloud Professional)** for advanced practitioners, and **ACE (Alibaba Cloud Expert)** for
expert-level, specialized mastery. Each level spans **domains**: **Cloud Computing** (the core —
**ECS** compute, **VPC** networking, **OSS** storage, **RDS** databases, **SLB** load balancing),
**Cloud Security** (Security Center, **WAF**, **Anti-DDoS**), **Big Data** (**MaxCompute**,
**DataWorks**), **Cloud Native** (**ACK** Kubernetes, **Function Compute**), **Database**,
**Networking**, **DevOps**, and **Machine Learning/AI** (**PAI**). Exams are delivered **online,
proctored**, and typically valid **two years**. Alibaba Cloud joins the encyclopedia's cloud-provider
cluster alongside AWS (XVII), Azure (XXXIII), Google Cloud (XXXIV), and Oracle (XLVII). This volume
teaches each with hands-on labs, using the **aliyun** CLI syntax and modeling architecture/logic in
`python3`.

> **Scope.** Cloud administration is authorized work. The Cloud Security domain (Security Center, WAF,
> Anti-DDoS, RAM) is **defensive** — protecting your own tenancy, never an attack.

## Design Considerations

Start with **ACA Cloud Computing** — it grounds the platform. Advance to **ACP** for architecture
depth, and pursue **ACE** for expert specialization (ML/AI, security). Choose the **domain** matching
your role. Practice on a **free-tier/trial** account. Verify current exams and service names on
alibabacloud.com — cloud services evolve continuously.

## Implementation and Automation

Confirm your practice toolset (aliyun CLI concepts + python3 for modeling):

```bash
command -v python3 >/dev/null && echo "python3: ok" || echo "python3: install for labs"
command -v aliyun >/dev/null && echo "aliyun CLI: ok" || echo "aliyun CLI: install for real API calls (free-tier account)"
```

## Validation and Troubleshooting

The verified program facts (alibabacloud.com + Alibaba Cloud Academy, 29 July 2026):

```text
Levels: ACA (Associate), ACP (Professional), ACE (Expert). Domains: Cloud Computing (ECS/VPC/OSS/RDS/SLB), Cloud Security (Security Center/WAF/Anti-DDoS), Big Data (MaxCompute/DataWorks), Cloud Native (ACK/Function Compute), Database, Networking, DevOps, ML/AI (PAI).
Delivery: online proctored (Alibaba Cloud Academy). Validity ~2 years.
```

Common pitfalls: mapping AWS/Azure names 1:1 (Alibaba has its **own** service names — ECS/VPC/OSS/RDS);
and jumping to **ACP/ACE** without the **ACA** foundation.

## Security and Best Practices

Ground yourself in **ACA Cloud Computing**, advance by **domain and level**, and practice on a **free
tier**. Treat the Cloud Security domain as **defensive**. Verify current service names and exams on
alibabacloud.com.

## References and Knowledge Checks

- alibabacloud.com/training-and-certification and edu.alibabacloud.com: the levels, domains, and exams.
- Alibaba Cloud documentation: ECS, VPC, OSS, RDS, ACK, and PAI.

**Knowledge checks**

1. Name the three Alibaba Cloud certification levels.
2. What is ECS? OSS? RDS?
3. Which domain covers Security Center and WAF?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — a workstation with `python3`,
in a lab. **Cost:** none.

### Lab 1.1 — Map levels and domains

**Objective:** Learn the structure.

```python
python3 - <<'PY'
levels={"ACA":"Associate — foundational","ACP":"Professional — advanced","ACE":"Expert — specialized mastery"}
domains=["Cloud Computing","Cloud Security","Big Data","Cloud Native","Database","Networking","DevOps","ML/AI"]
for lvl,scope in levels.items(): print(f"{lvl}: {scope}")
print("Domains:", ", ".join(domains))
PY
```

**Expected result:** the **ACA/ACP/ACE** levels and **domains** — the map this volume follows.

**Negative test:** assume one certification covers everything; each targets a **level × domain** —
choose accordingly.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Map Alibaba service names

**Objective:** Learn the core services.

```python
python3 - <<'PY'
services={"ECS":"Elastic Compute Service (VMs)","VPC":"Virtual Private Cloud (networking)",
          "OSS":"Object Storage Service","RDS":"Relational Database Service","SLB/ALB":"load balancing",
          "ACK":"Container Service for Kubernetes","MaxCompute":"big data warehouse","PAI":"Platform for AI"}
for svc,desc in services.items(): print(f"{svc:12}: {desc}")
PY
```

**Expected result:** Alibaba Cloud's **own service names** — the vocabulary this volume uses.

**Negative test:** call object storage "S3" on the exam; Alibaba's is **OSS** — learn the native
names.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.3 — Plan a certification path

**Objective:** Sequence credentials for a role.

```python
python3 - <<'PY'
paths={"Cloud engineer":"ACA Cloud Computing -> ACP Cloud Computing","Security":"ACA -> ACP Cloud Security",
       "Big data":"ACA Big Data -> ACP Big Data","AI/ML":"...-> ACE Machine Learning","Cloud native":"ACA Cloud Native -> ACP Container Service"}
for role,path in paths.items(): print(f"{role:14}: {path}")
PY
```

**Expected result:** role-to-path sequences — the ladder this volume follows.

**Negative test:** attempt **ACE** first; it's expert-level — build from **ACA/ACP**.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Alibaba Cloud certifies its platform across ACA/ACP/ACE levels and domains (Cloud Computing, Security,
Big Data, Cloud Native, Database, Networking, DevOps, ML/AI) via Alibaba Cloud Academy — the leading
Asia-Pacific cloud, taught here as authorized administration with defensive security.

- [ ] I can name the ACA/ACP/ACE levels.
- [ ] I can map the core Alibaba service names.
- [ ] I can identify the security domain services.
- [ ] I can plan a certification path.
- [ ] I completed Labs 1.1–1.3 including each negative test.
