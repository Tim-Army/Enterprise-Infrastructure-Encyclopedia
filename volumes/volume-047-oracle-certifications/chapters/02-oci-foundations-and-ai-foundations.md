# Chapter 02: OCI Foundations and AI Foundations

## Learning Objectives

- Explain the OCI Foundations and AI Foundations associate credentials.
- Summarize their exam topics.
- Apply core OCI concepts: regions, compartments, IAM, compute, storage, networking.
- Understand OCI AI services and AI/ML foundations.
- Complete a per-topic walkthrough for each Foundations area.

## Theory and Architecture

Two associate credentials establish the OCI baseline:

- **OCI Foundations Associate (1Z0-1085)** — foundational cloud and OCI knowledge:
  cloud concepts, the **OCI core services** (compute, storage, networking,
  database), **identity (IAM)** and security, and pricing/support/SLA.
- **OCI AI Foundations Associate (1Z0-1122)** — AI/ML/deep-learning fundamentals
  and the **OCI AI services** (Vision, Language, Speech, Document Understanding,
  and **OCI Generative AI**).

Both are entry-level and require no prerequisites.

## Design Considerations

Foundations is the **entry point** for every OCI path. Learn the OCI structure —
**regions and availability domains**, **compartments** for organization/isolation,
and **IAM** (users, groups, dynamic groups, policies) — plus the core service
categories. AI Foundations adds the AI vocabulary and OCI's managed AI services,
setting up the Data Science and Generative AI professional credentials.

## Implementation and Automation

The labs below use the **OCI CLI** (`oci`, illustrative patterns) and AI-service
concepts to make each Foundations area concrete — IAM, compute, storage,
networking, and the OCI AI services.

## Validation and Troubleshooting

Confirm the blueprints before studying:

```text
education.oracle.com > OCI Foundations (1Z0-1085) / AI Foundations (1Z0-1122):
  - Foundations: cloud concepts, core services, IAM/security, pricing/support
  - AI Foundations: AI/ML/DL basics, OCI AI services (incl. Generative AI)
  - associate level, no prerequisites (year-versioned codes)
```

Common pitfalls: confusing a **region** with an **availability domain**; putting
all resources in the root **compartment** (use compartments for isolation); and
writing overly broad **IAM policies**.

## Security and Best Practices

Organize resources with **compartments** and enforce **least-privilege IAM
policies**; use **regions/availability domains** for resilience; and prefer OCI's
**managed AI services** over building from scratch where they fit. Use the **Always
Free** tier to practice at no cost.

## References and Knowledge Checks

- education.oracle.com: OCI Foundations and AI Foundations exam topics; OCI documentation; Oracle Learning Explorer.

**Knowledge checks**

1. What is the difference between a region and an availability domain?
2. What do compartments provide in OCI?
3. Name three OCI AI services.

## Hands-On Lab

Per-topic walkthroughs — OCI Foundations and AI Foundations areas. OCI CLI patterns
are illustrative; no account required to study them.

**Shared prerequisites** — a shell; an OCI Always Free account for execution;
`python3`. **Cost:** none (Always Free).

### Lab 2.1 — Cloud concepts and OCI structure

**Objective:** Describe regions, availability domains, and compartments.

```bash
python3 - <<'PY'
print("Region: a geographic area; contains one or more Availability Domains (fault-isolated DCs).")
print("Fault Domains: isolation within an AD.")
print("Compartment: logical container for resources + IAM boundary (not tied to a region).")
PY
```

**Expected result:** the OCI structural hierarchy — the cloud-concepts foundation
of 1Z0-1085.

**Negative test:** treat a compartment as region-scoped; compartments span regions
in a tenancy — they are a logical/IAM boundary.

**Cleanup:** none.

### Lab 2.2 — Identity and Access Management (IAM)

**Objective:** Read the OCI IAM policy model.

```bash
echo 'Allow group Developers to manage instances in compartment Dev'
python3 - <<'PY'
print("OCI policy syntax: Allow <group> to <verb> <resource-type> in <compartment> [where ...]")
print("Verbs: inspect < read < use < manage (increasing privilege).")
PY
```

**Expected result:** the OCI policy statement structure and verb hierarchy — the
IAM model 1Z0-1085 tests.

**Negative test:** grant `manage all-resources` in the tenancy for convenience;
scope policies to a **compartment** and least verb.

**Cleanup:** none.

### Lab 2.3 — Compute and storage

**Objective:** Identify core compute and storage services.

```bash
oci compute instance list --compartment-id <ocid> 2>/dev/null | head \
  || python3 - <<'PY'
print("Compute: VM/bare-metal instances, shapes (flexible OCPU/memory), autoscaling.")
print("Storage: Block Volume (persistent disk), Object Storage (buckets), File Storage (NFS).")
PY
```

**Expected result:** the compute shapes and storage types — the core-services area
of 1Z0-1085.

**Negative test:** use Object Storage as a boot volume; **Block Volume** backs
instances — match the storage type to the use.

**Cleanup:** none.

### Lab 2.4 — Networking (VCN)

**Objective:** Describe the Virtual Cloud Network building blocks.

```bash
python3 - <<'PY'
vcn = {"VCN":"private network (CIDR)","Subnet":"public/private segment",
       "Gateways":"Internet GW, NAT GW, Service GW, Dynamic Routing GW (DRG)",
       "Security":"Security Lists / Network Security Groups (NSGs)"}
for k,v in vcn.items(): print(f"{k:9}: {v}")
PY
```

**Expected result:** the VCN components (subnets, gateways, NSGs) — the networking
foundation of 1Z0-1085.

**Negative test:** put a database in a **public** subnet with an Internet gateway;
keep data tiers in **private** subnets — segment by exposure.

**Cleanup:** none.

### Lab 2.5 — AI Foundations: AI/ML/DL basics

**Objective:** Distinguish AI, ML, and deep learning.

```bash
python3 - <<'PY'
print("AI: systems that mimic intelligence. ML: learn patterns from data.")
print("DL: ML with deep neural networks. GenAI: models that generate content (LLMs, diffusion).")
print("Supervised/unsupervised/reinforcement learning are ML paradigms.")
PY
```

**Expected result:** the AI/ML/DL/GenAI relationships — the fundamentals of
1Z0-1122.

**Negative test:** use "AI" and "deep learning" interchangeably; DL is a **subset**
of ML, which is a subset of AI — be precise.

**Cleanup:** none.

### Lab 2.6 — AI Foundations: OCI AI services

**Objective:** Match a task to an OCI AI service.

```bash
python3 - <<'PY'
services = {"Extract text/objects from images":"OCI Vision",
            "Sentiment / entities / translation":"OCI Language",
            "Transcribe audio":"OCI Speech",
            "Parse forms/invoices":"OCI Document Understanding",
            "LLM generation / chat / RAG":"OCI Generative AI"}
for task,svc in services.items(): print(f"{task:34} -> {svc}")
PY
```

**Expected result:** tasks mapped to OCI managed AI services — the AI-services area
of 1Z0-1122.

**Negative test:** build a custom OCR model when **OCI Vision/Document
Understanding** already does it; use the managed service where it fits.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

OCI Foundations (1Z0-1085) and AI Foundations (1Z0-1122) establish the OCI
baseline: cloud concepts, the OCI structure (regions, ADs, compartments, IAM), the
core services (compute, storage, VCN), and the AI/ML fundamentals plus OCI's
managed AI services. They are the entry point for every OCI path.

- [ ] I can describe regions, availability domains, and compartments.
- [ ] I can read an OCI IAM policy and the verb hierarchy.
- [ ] I can identify core compute, storage, and VCN services.
- [ ] I can distinguish AI/ML/DL and match tasks to OCI AI services.
- [ ] I completed Labs 2.1–2.6 including each negative test.
