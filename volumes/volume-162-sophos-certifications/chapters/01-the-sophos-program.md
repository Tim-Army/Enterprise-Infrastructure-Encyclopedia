# Chapter 01: The Sophos Academy Certification Program

![The Sophos Academy certification program and the Sophos security platform beneath it. Sophos offers role-based technical certifications through Sophos Academy across four tiers: Technician, which validates support capabilities; Administrator, which validates day-to-day administration and ongoing operations; Engineer, which validates configuration and demonstration skills; and Architect, which validates deployment and design expertise, such as the Certified Architect for Central Endpoint, Intercept X, and Server. Certifications are earned per product, including Sophos Firewall and Central Endpoint with Intercept X, and are delivered as instructor-led training or self-study eLearning, with free foundational training and separate customer and partner tracks. The platform beneath is Sophos Central, the cloud console that manages every Sophos product, with Intercept X endpoint protection using Deep Learning, Exploit Prevention, and CryptoGuard anti-ransomware; the Sophos Firewall next-generation firewall; Synchronized Security linking firewall and endpoint through the Security Heartbeat for automatic response; and Sophos MDR, a managed detection and response service built on Sophos XDR. Sophos is a defensive cybersecurity vendor.](../../../diagrams/volume-162-sophos-certifications/chapter-01-program.svg)

*Figure 1-1. The four Sophos Academy tiers and the Sophos security platform they validate.*

## Learning Objectives

- Describe the Sophos Academy program — Technician, Administrator, Engineer, Architect tiers.
- Understand the per-product, role-based structure and training formats.
- Place the Sophos platform — Central, Intercept X, Firewall, Synchronized Security, MDR.
- Recognize Sophos's position as a defensive cybersecurity vendor.

> **Defensive framing.** This volume is about *defending* endpoints and networks — blocking malware and ransomware, inspecting traffic, isolating compromised devices, and detecting threats. Every mechanism (Deep Learning detection, CryptoGuard, Synchronized Security, MDR) is a protective control a security team uses to keep an organization safe. Nothing here is about attacking systems.

## What Sophos is

Sophos is a **cybersecurity vendor** spanning **endpoint protection**, **network security (firewall)**, and **managed detection and response (MDR)** — protecting organizations across their devices, networks, and cloud. Its products are unified under **Sophos Central** ([Chapter 2](02-sophos-central.md)), a single cloud console, and its signature idea is **Synchronized Security** ([Chapter 6](06-synchronized-security.md)) — products that **share threat intelligence and respond together**. Sophos is a defensive-security peer of the endpoint vendors ([SentinelOne CLI](../../volume-151-sentinelone-certifications/README.md), [CrowdStrike L](../../volume-050-crowdstrike-certifications/README.md)) and firewall vendors ([Fortinet XIX](../../volume-019-fortinet-network-security/README.md), [Check Point LXXIII](../../volume-073-check-point-certifications/README.md)) this shelf covers. The lab models the program.

## The program

**Sophos Academy** runs the certification program — **role-based technical certifications**, earned **per product**, across **four tiers**:

| Tier | Validates |
|:---|:---|
| **Technician** | **Support** — troubleshooting and supporting the product |
| **Administrator** | **Day-to-day administration** and ongoing operations |
| **Engineer** | **Configuration / demonstration** — administering common tasks |
| **Architect** | **Deployment and design** — architecting and deploying at scale |

The tiers rise from **supporting** a product (Technician) through **operating** it (Administrator/Engineer) to **designing and deploying** it (Architect). Certifications are **per product** — so you might be a *Certified Architect — Central Endpoint, Intercept X & Server*, or a *Certified Engineer — Sophos Firewall*. Training comes as **instructor-led** or **self-study eLearning**, with **free foundational training**, and separate **customer** and **partner** tracks. The lab models the tiers.

## The per-product, role-based structure

Because certifications combine a **role tier** with a **product**, the credential precisely describes what you can do with which product. A candidate chooses:

1. **Which product** — Firewall, Central Endpoint/Intercept X, MDR, and others.
2. **Which role tier** — Technician, Administrator, Engineer, or Architect, matching the depth their job needs.

This role-plus-product model means you certify on exactly what you operate, at the depth you operate it. The Architect tier (e.g., the Central Endpoint **AT15**) is the deepest, covering design decisions like update caches, message relays, AD sync, and segmented policy. The lab models the structure.

## The Sophos platform

Every certification sits on the Sophos platform, which the middle chapters cover: [Sophos Central (Ch 2)](02-sophos-central.md) the unified console, [Intercept X (Ch 3)](03-intercept-x.md) endpoint protection, [CryptoGuard and ransomware defense (Ch 4)](04-cryptoguard-and-ransomware-defense.md), [Sophos Firewall (Ch 5)](05-sophos-firewall.md), [Synchronized Security (Ch 6)](06-synchronized-security.md), [Sophos MDR (Ch 7)](07-sophos-mdr-and-xdr.md), and [operating Sophos (Ch 8)](08-operating-sophos.md). [Chapter 9](09-choosing-your-sophos-path.md) sequences a path. The lab situates them.

## Hands-On Lab

Python models the program. **Cost:** none.

### Lab 1.1 — Map the role tiers and per-product structure

**Objective:** Represent the four tiers and the role-plus-product model.

```bash
python3 - <<'EOF'
TIERS = {
  "Technician":    "SUPPORT — troubleshoot + support the product",
  "Administrator": "day-to-day ADMINISTRATION + ongoing operations",
  "Engineer":      "CONFIGURATION / demonstration — administer common tasks",
  "Architect":     "DEPLOYMENT + DESIGN — architect + deploy at scale (deepest)",
}
PRODUCTS = ["Sophos Firewall", "Central Endpoint, Intercept X & Server", "Sophos MDR", "Email", "Wireless", "ZTNA"]
print("Sophos Academy — role-based tiers (per product):\n")
for i, (tier, what) in enumerate(TIERS.items(), 1):
    print(f"   {i}. {tier:14} {what}")
print(f"\n   ...earned PER PRODUCT (e.g. 'Certified Architect — Central Endpoint, Intercept X & Server'):")
for p in PRODUCTS:
    print(f"      - {p}")
print("\nThe model = ROLE TIER x PRODUCT: certify on exactly what you operate, at the depth your")
print("job needs. TECHNICIAN (support) -> ADMINISTRATOR/ENGINEER (operate) -> ARCHITECT (design +")
print("deploy). Training: instructor-led OR self-study eLEARNING; FREE foundational training;")
print("CUSTOMER + PARTNER tracks. Sophos = defensive cybersecurity (endpoint + firewall + MDR),")
print("unified by Sophos Central + Synchronized Security. Peers: SentinelOne (CLI)/CrowdStrike (L)")
print("(endpoint), Fortinet (XIX)/Check Point (LXXIII) (firewall), Rapid7 (CXXXVII) (MDR/SOC).")
EOF
```

**Expected result:** The four role tiers (Technician/Administrator/Engineer/Architect) and the per-product model (e.g., Certified Architect — Central Endpoint, Intercept X & Server), with eLearning/instructor-led delivery and free foundational training. The program lesson is that Sophos combines a role tier with a product, so you certify on exactly what you operate at the depth your job needs, over a defensive platform spanning endpoint, firewall, and MDR unified by Sophos Central.

**Negative test:** Expecting a single "Sophos Certified Professional" exam. Certifications are role-tier-plus-product (Technician through Architect, per product); you certify for your role on the specific products you operate.

**Cleanup:** None.

### Lab 1.2 — Match tier to role need

**Objective:** Reason about picking the right tier for a job.

```bash
python3 - <<'EOF'
JOBS = [
  ("help-desk supporting Sophos endpoints",        "Technician",    "support/troubleshoot"),
  ("admin running day-to-day endpoint policy",     "Administrator", "operate day-to-day"),
  ("engineer configuring a new firewall rollout",  "Engineer",      "configure/administer tasks"),
  ("architect designing a multi-site deployment",  "Architect",     "design + deploy at scale"),
]
print("Match the Sophos tier to the job:\n")
for job, tier, why in JOBS:
    print(f"   {job:44} -> {tier:14} ({why})")
print("\nPick the TIER that matches your role's DEPTH: don't over-certify (an Architect cert for")
print("a help-desk role) or under-certify (Technician for someone designing deployments). The")
print("role-plus-product model means the credential PRECISELY describes what you can do with which")
print("product — support it, operate it, or design + deploy it. Match tier to need, on the products")
print("you actually run.")
EOF
```

**Expected result:** Jobs matched to tiers — help-desk → Technician, day-to-day admin → Administrator, configuring a rollout → Engineer, designing a multi-site deployment → Architect. The lesson is to pick the tier matching your role's depth (support, operate, or design/deploy) on the products you run, since the role-plus-product credential precisely describes your capability.

**Negative test:** Pursuing the Architect tier for a help-desk support role. The tiers map to depth; a support role is served by Technician, while Architect suits those designing and deploying — match the tier to the job.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] The program understood — Sophos Academy, four role tiers (Technician/Administrator/Engineer/Architect), per product.
- [ ] The per-product, role-based structure and training formats (eLearning/instructor-led, free foundational) understood.
- [ ] The Sophos platform placed — Central, Intercept X, Firewall, Synchronized Security, MDR.
- [ ] Sophos recognized as a defensive cybersecurity vendor, a peer of the endpoint, firewall, and MDR vendors.
