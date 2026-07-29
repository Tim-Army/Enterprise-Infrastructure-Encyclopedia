# Chapter 01: The CompTIA Certification Program

## Learning Objectives

- Explain what makes CompTIA certifications vendor-neutral and why that matters.
- Distinguish the classic "plus" certifications from the new Xpert "Pro" series and Essentials.
- Describe the exam experience: Pearson VUE, performance-based questions, and accreditation.
- Explain stackable certifications and how CompTIA credentials combine.
- Describe the Continuing Education renewal model and three-year validity.

## Theory and Architecture

**CompTIA** (the Computing Technology Industry Association) publishes the
industry's foundational **vendor-neutral** IT certifications. Vendor-neutral
means a credential validates a **skill domain** — supporting endpoints,
running a network, securing a system, administering Linux, analyzing data —
independent of any single manufacturer's products. That is exactly why
CompTIA sits *beneath* the vendor tracks in this encyclopedia: Security+
teaches the security concepts that Cisco, Palo Alto, Fortinet, and Zscaler
then implement in their own ways; Network+ teaches the networking that
precedes CCNA or JNCIA; Linux+ precedes RHCSA and the Ubuntu and RHEL volumes.

After CompTIA's **2024–2025 acquisition and relaunch**, the program runs on
**two parallel lines** plus a microcredential tier:

- **Classic "plus" certifications** — the traditional, knowledge-and-scenario
  exams delivered at a test center or online: **Tech+**, **A+**, **Network+**,
  **Security+** (Core); **Cloud+**, **Linux+**, **Server+** (Infrastructure);
  **CySA+**, **PenTest+**, **SecurityX** (Cybersecurity); **Data+**,
  **DataSys+** (Data); and **Project+** (professional; the business-cloud
  **Cloud Essentials+** certification retired in September 2025, now the Cloud
  Essentials course).
- **The Xpert Series ("Pro" credentials)** — newer, **hands-on,
  performance-based** certifications that go deeper and more practical:
  **Security Pro**, **CyberDefense Pro**, **Ethical Hacker Pro**, **Linux
  Pro**, **Hybrid Server Pro** (Core and Advanced), **CloudNetX**, and the AI
  and operational-technology security certs **SecAI+** and **SecOT+**.
- **Essentials microcredentials** — short, foundational credentials including a
  large **AI Essentials** line (AI Essentials, AI Prompting Essentials,
  Copilot 365 Essentials), plus Business, Project Management, and Soft Skills
  Essentials.

Exams are delivered through **Pearson VUE** — in a test center or
**online-proctored** — and blend multiple-choice with **performance-based
questions (PBQs)** that ask the candidate to complete a task in a simulated
environment. Many CompTIA certifications are **ISO/ANSI-accredited** and
recognized under the **U.S. DoD 8140/8570** directive, which drives their
adoption in government and regulated sectors.

CompTIA credentials are **stackable**: earning several combines into recognized
stackable certifications (for example, the Secure Infrastructure and Network
Vulnerability Assessment specialist and professional stacks), and passing an
exam contributes toward renewal of related certifications through Continuing
Education.

## Design Considerations

Plan a CompTIA path by **career stage and domain**. Complete newcomers start
at **Tech+** for digital-and-IT literacy, then **A+** for hands-on IT support.
Networking and security careers add **Network+** and **Security+** — Security+
in particular is the most widely required entry security credential. From
there, specialize: **Infrastructure** (Cloud+, Linux+, Server+),
**Cybersecurity** (CySA+, PenTest+, then SecurityX), or **Data** (Data+,
DataSys+). Choose the **Xpert "Pro"** credentials when a role needs
demonstrated, hands-on ability rather than knowledge validation — they are the
practical, lab-heavy tier.

Treat **currency** as a first-class concern. CompTIA renames and renumbers
often — verify the **current exam version** on comptia.org before studying,
and plan for the **three-year renewal** through Continuing Education so a
credential does not lapse. Recognize the **prerequisite guidance** (CompTIA
recommends experience and prior certs — for example Network+ before
Security+ — but rarely enforces them), and let the recommended order guide the
learning sequence even when it is not mandatory.

## Implementation and Automation

The authority for every fact is **comptia.org**, which (unlike some vendors'
sites) serves its certification pages as fetchable HTML. Confirm the current
exam code for a credential before investing study time:

```bash
# List every certification slug on the catalog page
curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/" \
  | grep -oE '/certifications/[a-z0-9-]+/?' | sort -u

# Read a certification page and extract its current exam code
curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/security/" \
  | grep -oE '\bSY0-[0-9]{3}\b' | sort -u   # -> SY0-701
```

## Validation and Troubleshooting

Confirm a credential's pathway, exam, and status on the certification page:

```text
comptia.org > Certifications > open the credential page:
  - the current exam code and version
  - the exam objectives (blueprint) download
  - number of questions, time, and passing score
  - whether it is a classic exam, an Xpert "Pro" credential, or an Essentials microcredential
```

Common pitfalls: studying a **retired exam version** because a course or dump
is stale (Network+ N10-008 → N10-009, Security+ SY0-601 → SY0-701, Linux+
XK0-005 → XK0-006, and the CASP+ → **SecurityX (CAS-005)** and ITF+ → **Tech+
(FC0-U71)** renames); assuming a **hard prerequisite** where CompTIA only
recommends one; confusing a classic **"plus"** exam with the newer **"Pro"**
credential of a similar name (both a Linux+ and a Linux Pro exist, for
example); and letting a certification **lapse** by missing the three-year CE
window.

## Security and Best Practices

Verify certification facts on **comptia.org**, never a third-party dump site —
dumps are inaccurate, violate the candidate agreement, and can void a
credential. Use official **CertMaster** learning and practice, and get
hands-on for the **performance-based questions** and the **Xpert "Pro"** labs.
Plan **renewal** through Continuing Education from the day a credential is
earned. For teams in regulated environments, map required roles to the
**DoD 8140/8570-recognized** CompTIA credentials and track renewals centrally.

## References and Knowledge Checks

- comptia.org: *Certifications* catalog; *Continuing Education*; *Stackable certifications*; individual exam pages.

**Knowledge checks**

1. What does "vendor-neutral" mean, and why does it place CompTIA beneath the vendor tracks?
2. What is the difference between a classic "plus" exam and an Xpert "Pro" credential?
3. How long are most CompTIA certifications valid, and how are they renewed?

## Hands-On Lab

Exam-preparation walkthroughs for navigating and verifying the program.

**Shared prerequisites for Labs 1.1–1.3** — a web browser and `curl`.
**Cost:** none.

### Lab 1.1 — Enumerate the CompTIA catalog (Topic: Read the program)

**Objective:** List the current certifications from the authoritative source.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/" \
  | grep -oE '/certifications/[a-z0-9-]+/?' | sort -u | head -40
```

**Expected result:** a list of certification slugs including the classic certs
(`/a/`, `/network/`, `/security/`, `/linux/`, `/cloud/`), the Xpert "Pro"
credentials (`/cloudnetx/`, `/hybrid-server-pro-core/`, `/ethical-hacker-pro/`),
and Essentials (`/ai-essentials/`) — the whole restructured program in one view.

**Negative test:** rely on a years-old blog list; it omits the Xpert "Pro"
series and the AI Essentials line, and may cite retired exam versions — use
the live catalog.

**Cleanup:** none.

### Lab 1.2 — Confirm a current exam code (Topic: Verify currency)

**Objective:** Prove the current Security+ exam version.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/security/" \
  | grep -oE '\bSY0-[0-9]{3}\b' | sort -u
```

**Expected result:** **SY0-701** (the current Security+; SY0-601 retired) — the
exam page is the authority for the version to study.

**Negative test:** search for "SY0-601" study material; it targets the retired
version — always confirm the current code first.

**Cleanup:** none.

### Lab 1.3 — Distinguish classic from Xpert (Topic: Understand the structure)

**Objective:** See that a "plus" cert and a "Pro" cert can coexist.

```bash
for slug in linux linux-pro server hybrid-server-pro-core; do
  title=$(curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/$slug/" \
    | grep -oE '<title>[^<]*</title>' | head -1)
  echo "$slug -> $title"
done
```

**Expected result:** `Linux+` and `Linux Pro`, and `Server+` and `Hybrid
Server Pro I: Core`, are distinct credentials — the classic knowledge exam and
the newer hands-on "Pro" credential sit side by side.

**Negative test:** assume "Linux+" and "Linux Pro" are the same exam; they are
different credentials in different lines — check both.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

CompTIA is the vendor-neutral foundation beneath the encyclopedia's vendor
tracks. After its relaunch it runs two parallel lines — the classic "plus"
certifications and the hands-on Xpert "Pro" series — plus an Essentials
microcredential tier. Exams run on Pearson VUE with performance-based
questions, many are ISO/ANSI and DoD-recognized, credentials are stackable,
and most are valid three years and renewed through Continuing Education.

- [ ] I can explain vendor-neutrality and CompTIA's place in the stack.
- [ ] I can distinguish classic "plus", Xpert "Pro", and Essentials.
- [ ] I can verify a current exam code on comptia.org.
- [ ] I can explain stackable certifications and CE renewal.
- [ ] I completed Labs 1.1–1.3 including each negative test.
