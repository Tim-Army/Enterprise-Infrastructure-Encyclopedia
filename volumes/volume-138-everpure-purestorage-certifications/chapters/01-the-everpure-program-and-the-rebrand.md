# Chapter 01: The Everpure Program and the Rebrand

![The Everpure IT Professional Certification program, formerly Pure Storage: twelve certifications across four levels. Associate level has Data Storage, priced at 200 US dollars. Professional level has FlashArray Storage, FlashBlade Storage, Portworx Enterprise, and Cyber Resilience, priced at 300 dollars. Specialist level has FlashArray Implementation, FlashBlade Implementation, FlashArray Support, FlashBlade Support, Cloud, and Migration, also 300 dollars. Expert level has Platform Architect at 400 dollars. All exams are multiple choice, delivered online and proctored with a webcam, closed book with no external materials permitted, and training is not required because each exam is designed to test on-the-job experience. Certifications are valid for three years and are renewed by retaking the updated exam; the Associate Data Storage certification renews automatically when a higher-level certification is earned, and Continuing Everpure Education credits apply to selected FlashArray exams. Badges issue through Credly.](../../../diagrams/volume-138-everpure-purestorage-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Everpure's twelve IT Professional Certifications across four levels, with pricing and the recertification paths.*

## Learning Objectives

- Explain the Pure Storage → Everpure rebrand and what did and did not change.
- Describe the twelve certifications and the four levels.
- Understand exam mechanics: format, pricing, validity, and both recertification paths.
- Set up a free study environment for the storage labs.

## First, the name

**Pure Storage is now Everpure, Inc.** If you learned this vendor under its old name — or search for it today — you need to know what moved:

| What changed | What did not |
|:---|:---|
| Company name: **Pure Storage → Everpure, Inc.** | Product names: **FlashArray**, **FlashBlade**, **FlashBlade//EXA**, **Portworx** |
| Corporate site: purestorage.com → **everpuredata.com** (301 redirect) | The **Evergreen** architecture and **Evergreen//One** subscription |
| Program branding: **Everpure certifications**, **Everpure Academy** | The **Pure Accelerate** conference, and **Pure.ai** |

One practical wrinkle: the certification platform is branded **Everpure Academy** but is **still hosted at `academy.purestorage.com`**. The old hostname remains the working URL, so a link that looks stale may be entirely current.

This volume uses **Everpure** for the company and the certifications, and keeps the former name in the title so it is findable either way. Where a product name contains "Pure," that is deliberate rather than an oversight.

## What Everpure does

Everpure builds enterprise **flash storage** and, increasingly, positions itself as a data platform:

| Product | What it is |
|:---|:---|
| **FlashArray** | Block storage — databases, virtualization, general enterprise workloads |
| **FlashBlade** | Unified file and object storage — unstructured data at scale |
| **FlashBlade//EXA** | The high-performance variant aimed at AI and HPC data pipelines |
| **Portworx** | Cloud-native storage for Kubernetes — persistent volumes for stateful containers |
| **Evergreen / Evergreen//One** | The non-disruptive upgrade architecture, and its as-a-service consumption model |

The **Evergreen** idea is the company's signature: controllers and media are upgraded without downtime and without the traditional forklift replacement cycle, and Evergreen//One turns that into a subscription. Chapter 02 examines what that means architecturally.

## The certification program

Everpure's **IT Professional Certifications** run through **Everpure Academy**, in four levels:

### Associate — $200

| Certification | Scope |
|:---|:---|
| **Data Storage** (DSA) | Foundational storage concepts and the Everpure portfolio |

### Professional — $300

| Certification | Scope |
|:---|:---|
| **FlashArray Storage** | Operating block storage |
| **FlashBlade Storage** | Operating file and object storage |
| **Portworx Enterprise** | Cloud-native and Kubernetes storage |
| **Cyber Resilience** | Immutability, ransomware recovery, data protection |

### Specialist — $300

| Certification | Scope |
|:---|:---|
| **FlashArray Implementation** | Deploying FlashArray |
| **FlashBlade Implementation** | Deploying FlashBlade |
| **FlashArray Support** | Troubleshooting and supporting FlashArray |
| **FlashBlade Support** | Troubleshooting and supporting FlashBlade |
| **Cloud** | Cloud storage services and hybrid deployments |
| **Migration** | Moving data onto the platform |

### Expert — $400

| Certification | Scope |
|:---|:---|
| **Platform Architect** | Designing complete Everpure solutions |

Note the useful structure: **Professional certifications are about operating** a product, while **Specialist certifications split into Implementation and Support** for the same products. Those are genuinely different jobs — deploying a system and diagnosing one that is misbehaving — and the program treats them that way.

A separate **Partner Sales Certification** track exists for partners, distinct from these IT Professional credentials.

## Exam mechanics

| Aspect | Detail |
|:---|:---|
| **Format** | Multiple choice |
| **Delivery** | **Online, proctored** — a webcam is required and you are monitored throughout |
| **Open book?** | **No.** "You won't be able to refer to any external materials during the exam." |
| **Training required?** | **No.** "Each exam is designed to test your **on-the-job experience**." |
| **Price** | Associate **$200** · Professional **$300** · Specialist **$300** · Expert **$400** |
| **Badge** | Credly, by email after passing |
| **Validity** | **Three years** |

That "designed to test your on-the-job experience" line is a genuine signal about how to prepare: the exams reward having operated the platform rather than having read about it, so study guides supplement experience rather than substituting for it.

## Recertification — two paths worth knowing

Certifications expire after **three years** and are renewed by **retaking the updated exam**. Two alternatives make that easier:

1. **The Associate (DSA) renews automatically** when you earn any Professional, Specialist, or Expert certification. Progress up the ladder and the foundation credential maintains itself.
2. **Continuing Everpure Education (CEE) credits** apply to **selected FlashArray exams** — check the individual exam page, since this does not apply universally.

## Free study environment

Everpure's arrays are hardware, so this volume's labs model the **storage disciplines** — non-disruptive upgrade sequencing, volume and host mapping, file-versus-object selection, data-reduction arithmetic, replication topologies and RPO, immutable snapshots and recovery drills, and Kubernetes persistent-volume binding — in free Python. Those concepts are what the exams test and what transfer across storage vendors.

## Hands-On Lab

### Lab 1.1 — Set up the study environment

**Objective:** Confirm the free toolchain.

```bash
python3 --version
mkdir -p ~/everpure-study && cd ~/everpure-study
python3 - <<'EOF'
print("Enterprise storage study environment ready.")
print("Labs model: non-disruptive upgrades, volume/host mapping, file vs object,")
print("data reduction ratios, replication RPO, immutable snapshots, Kubernetes PVs.")
print("No Everpure hardware required.")
EOF
```

**Expected result:** Python reports a version and the message prints. The storage reasoning — capacity, reduction ratios, RPO arithmetic, failover behavior — is vendor-independent and models cleanly.

**Negative test:** Assuming you need array access to study — you cannot practice the console, but the concepts the exams probe are reasoning you can build locally.

**Rollback:** `rm -rf ~/everpure-study` when finished.

### Lab 1.2 — Choose a level and plan recertification

**Objective:** Pick a certification and use the auto-renewal path deliberately.

```bash
python3 - <<'EOF'
CERTS = {
  "Associate":    {"price":200, "certs":["Data Storage (DSA)"]},
  "Professional": {"price":300, "certs":["FlashArray Storage","FlashBlade Storage",
                                          "Portworx Enterprise","Cyber Resilience"]},
  "Specialist":   {"price":300, "certs":["FlashArray Implementation","FlashBlade Implementation",
                                          "FlashArray Support","FlashBlade Support","Cloud","Migration"]},
  "Expert":       {"price":400, "certs":["Platform Architect"]},
}
for level, d in CERTS.items():
    print(f"{level:13} ${d['price']}  {len(d['certs'])} cert(s)")
    for c in d["certs"]:
        print(f"{'':15} - {c}")

print("\n--- recertification planning (3-year validity) ---")
def plan(holds_dsa, earns_higher):
    if holds_dsa and earns_higher:
        return "DSA renews AUTOMATICALLY — earning a higher cert maintains the foundation credential"
    if holds_dsa:
        return "DSA must be retaken before expiry (or earn a higher cert and it renews itself)"
    return "retake the updated exam before the expiry date"

for h, e in [(True, True), (True, False), (False, False)]:
    print(f"  holds DSA={str(h):5} earns higher cert={str(e):5} -> {plan(h, e)}")
print("\nCEE (Continuing Everpure Education) credits are an additional path for SELECT FlashArray")
print("exams — check the individual exam page rather than assuming it applies to yours.")
print("\nRecord your expiry date at pass time: three years is long enough to forget.")
EOF
```

**Expected result:** The twelve certifications print by level with pricing, and the recertification check shows the Associate maintaining itself for anyone progressing upward. That auto-renewal is worth planning around — someone who intends to earn a Professional certification anyway should sit the Associate first, because it then costs nothing to keep.

**Negative test:** Assuming CEE credits will renew any certification — they apply to *selected FlashArray exams* only, so a Portworx or Cyber Resilience holder planning on them will find themselves retaking the exam.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The Pure Storage → Everpure rebrand understood, including what kept its name.
- [ ] The twelve certifications and four levels mapped, with Implementation/Support recognized as distinct roles.
- [ ] Exam mechanics recorded: multiple choice, proctored, closed book, $200/$300/$400, three-year validity.
- [ ] Both recertification paths noted — DSA auto-renewal and CEE credits for select FlashArray exams.
- [ ] Free Python study environment ready.
