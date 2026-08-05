# Chapter 08: NetBackup and the Veritas Portfolio

## Learning Objectives

- Explain the Cohesity–Veritas merger and what NetBackup adds.
- Describe NetBackup as enterprise backup and NetBackup Appliances as integrated systems.
- Understand multicloud data management across on-premises and cloud.
- Recognize the combined portfolio the certifications now span.

*Cert relevance: two Protection Professional certifications cover NetBackup and NetBackup Appliances (the Veritas heritage).*

## The Cohesity–Veritas merger

In **December 2024, Cohesity merged with Veritas** — specifically Veritas's data-protection business — combining Cohesity's modern, AI-powered platform with Veritas's long-established **enterprise backup**. The result is the **largest data-protection vendor** by customer base, and it brings **NetBackup** — one of the most widely deployed enterprise backup products, with a huge installed base — into the Cohesity portfolio. This is why the certification program includes **two NetBackup-focused Protection Professional certifications** ([Chapter 1](01-the-cohesity-program.md)): the combined company must certify professionals on **both** the modern Data Cloud *and* the NetBackup installed base. The lab models the combined portfolio.

## NetBackup and NetBackup Appliances

The Veritas heritage adds:

- **NetBackup** — enterprise **backup software**: a mature, scalable, heterogeneous backup platform protecting a vast range of workloads (enterprise applications, databases, VMs, cloud), long trusted in the largest data centers. It is certified via **Protection Professional — NetBackup**.
- **NetBackup Appliances** — **integrated appliances** (hardware plus NetBackup software) that deliver backup as a turnkey system rather than software you assemble on your own hardware — simpler to deploy and support. Certified via **Protection Professional — NetBackup and NetBackup Appliances**.

For a certification candidate, the point is that Cohesity now spans **two protection lineages** — the cloud-native Data Cloud and the enterprise NetBackup line — and the program certifies both. The lab models the two lineages.

## Multicloud data management

A theme across the combined portfolio is **multicloud data management** — protecting and managing data wherever it lives: **on-premises, and across AWS, Azure, and Google Cloud.** The **Protection Associate — Multicloud** certification ([Chapter 1](01-the-cohesity-program.md)) reflects this: modern enterprises run workloads across many clouds and on-prem, and data protection must span them all with consistent policy, immutability, and recovery. Multicloud is not a separate product so much as a **requirement** the whole platform meets — one control plane over data distributed across environments. The lab models multicloud protection.

## The combined portfolio the certs span

Putting it together, the Cohesity certification program now validates skills across a **combined portfolio**:

| Lineage | Products | Certification |
|:---|:---|:---|
| **Cohesity Data Cloud** | DataProtect, SmartFiles, FortKnox, DataHawk/Gaia | CCPA, CCIP, CCSS |
| **Veritas (merged 2024)** | NetBackup, NetBackup Appliances | CCPP (NetBackup) |
| **Cross-cutting** | Multicloud data management | CCPA — Multicloud |

The breadth reflects a company that unified the modern and the enterprise-established sides of data protection. For candidates, choosing which certifications to pursue means matching them to **which portfolio you operate** — Data Cloud, NetBackup, or both. The lab synthesizes.

## Hands-On Lab

Python models the combined portfolio and multicloud. **Cost:** none.

### Lab 8.1 — Mapping the combined portfolio to certifications

**Objective:** See which certifications map to which portfolio and environments.

```bash
python3 - <<'EOF'
PORTFOLIO = {
  "Cohesity Data Cloud (modern)": {
      "products": ["DataProtect", "SmartFiles", "FortKnox", "DataHawk/Gaia"],
      "certs": ["Protection Associate — DataProtect (COH100)",
                "Implementation Professional — SmartFiles (CCIP)",
                "Security Specialist (COH350)"],
  },
  "Veritas (merged Dec 2024)": {
      "products": ["NetBackup", "NetBackup Appliances"],
      "certs": ["Protection Professional — NetBackup (CCPP)",
                "Protection Professional — NetBackup and NetBackup Appliances (CCPP)"],
  },
  "Multicloud (cross-cutting)": {
      "products": ["on-prem + AWS + Azure + GCP data"],
      "certs": ["Protection Associate — Multicloud (CCPA)"],
  },
}
print("Cohesity + Veritas — the combined portfolio the certs span:\n")
for lineage, info in PORTFOLIO.items():
    print(f"   {lineage}")
    print(f"      products: {', '.join(info['products'])}")
    for c in info["certs"]:
        print(f"      cert: {c}")
    print()
print("The Dec 2024 VERITAS merger made Cohesity the largest data-protection vendor and")
print("added NETBACKUP (huge enterprise installed base) + NetBackup APPLIANCES (turnkey).")
print("So the program now spans TWO lineages — the cloud-native Data Cloud AND the")
print("enterprise NetBackup line — plus MULTICLOUD (protect data on-prem + across AWS/")
print("Azure/GCP with consistent policy). Match your certifications to the portfolio you")
print("actually OPERATE: Data Cloud, NetBackup, or both.")
EOF
```

**Expected result:** The combined portfolio mapped to certifications — Data Cloud (CCPA/CCIP/CCSS), Veritas NetBackup (CCPP), and cross-cutting Multicloud (CCPA) — reflecting the December 2024 merger. The lesson is that Cohesity now spans the cloud-native Data Cloud and the enterprise NetBackup lineage plus multicloud data management, and candidates should match certifications to the portfolio they operate.

**Negative test:** Assuming Cohesity is only the modern Data Cloud. Since the Veritas merger it also spans NetBackup and NetBackup Appliances (with their own Protection Professional certifications); the program covers both lineages.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The Cohesity–Veritas merger (December 2024) understood, and what NetBackup adds.
- [ ] NetBackup (enterprise backup software) and NetBackup Appliances (integrated systems) understood.
- [ ] Multicloud data management understood — one control plane across on-prem and AWS/Azure/GCP.
- [ ] The combined portfolio the certifications span recognized — Data Cloud, NetBackup, and multicloud.
