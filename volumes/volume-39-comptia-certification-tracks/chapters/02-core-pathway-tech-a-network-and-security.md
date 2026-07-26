# Chapter 02: Core Pathway — Tech+, A+, Network+, and Security+

## Learning Objectives

- Enumerate the CompTIA Core certifications and their current exam codes.
- Explain the intended sequence from Tech+ through Security+.
- Describe each Core exam's domain focus and format.
- Map the Core certifications to the encyclopedia's networking and security volumes.
- Build a foundational study path for a new IT professional.

## Theory and Architecture

The **Core** pathway is CompTIA's foundation and the most widely held part of
the program. As verified on comptia.org (26 July 2026), it runs in four steps:

- **CompTIA Tech+** — exam **FC0-U71** (V6; renamed from **ITF+**, IT
  Fundamentals). Foundational technology and digital literacy across six
  weighted domains: **Tech concepts and terminology (13%)**, **Infrastructure
  (24%)**, **Applications and software (18%)**, **Software development concepts
  (13%)**, **Data and database fundamentals (13%)**, and **Security (19%)**. A
  70-question, multiple-choice exam over 60 minutes with a passing score of
  **650 (900-point scale)** and no prior experience required. The entry point
  for people new to IT. (The base **FC0-U71** does not expire; an **FC0-U71-CE**
  variant carries a 5-year CE validity.)
- **CompTIA A+** — the **Core Series** (V15): two exams that must both be passed
  and both taken from the **same version** (no mixing) — **220-1201 (Core 1)**
  and **220-1202 (Core 2)**. Each is up to 90 questions (multiple-choice,
  drag-and-drop, and performance-based) over 90 minutes, with ~12 months of
  IT-support experience recommended. **Core 1** weights **Mobile devices (13%)**,
  **Networking (23%)**, **Hardware (25%)**, **Virtualization and cloud computing
  (11%)**, and **Hardware and network troubleshooting (28%)** (passing 675/900);
  **Core 2** weights **Operating systems (28%)**, **Security (28%)**, **Software
  troubleshooting (23%)**, and **Operational procedures (21%)** (passing
  700/900). A+ is the classic first professional certification for help-desk and
  desktop-support roles.
- **CompTIA Network+** — exam **N10-009** (V9) across five weighted domains:
  **Networking concepts (23%)**, **Network implementation (20%)**, **Network
  operations (19%)**, **Network security (14%)**, and **Network troubleshooting
  (24%)**. A 90-question exam (multiple-choice and performance-based) over 90
  minutes with a **scaled passing score of 720 (100–900)**; A+ and 9–12 months
  of networking experience recommended. Vendor-neutral networking before a
  vendor track such as Cisco CCNA (Volume III) or Juniper JNCIA (Volume XXXI).
- **CompTIA Security+** — exam **SY0-701** (V7). Core cybersecurity across five
  weighted domains: **General security concepts (12%)**, **Threats,
  vulnerabilities, and mitigations (22%)**, **Security architecture (18%)**,
  **Security operations (28%)**, and **Security program management and oversight
  (20%)**. A 90-question exam (multiple-choice and performance-based) over 90
  minutes with a **scaled passing score of 750 (100–900)**; Network+ and ~2
  years of security/sysadmin experience recommended. **The most widely required
  entry-level security certification**, and a DoD 8140/8570 baseline.

## Design Considerations

Sequence the Core pathway by experience. A complete beginner starts at
**Tech+**; someone already comfortable with computers can begin at **A+**.
**Network+** and **Security+** follow, and CompTIA recommends (but does not
require) **A+ before Network+ before Security+** — the order builds the mental
model each later exam assumes. **Security+ is the anchor** of most IT-security
careers and often the first CompTIA cert an employer mandates, so many
learners target it directly with prior networking knowledge.

Because A+ requires **two exams**, budget for both. All four Core exams include
**performance-based questions**, so hands-on practice — building a PC,
configuring a small network, hardening a system — matters as much as reading.
The Core certifications map straight into the encyclopedia's foundations
(Volumes I, II, IV) and precede every vendor networking and security track.

## Implementation and Automation

Verify the Core codes from comptia.org:

```bash
for slug in tech a network security; do
  code=$(curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/$slug/" \
    | grep -oE '\b(FC0-U[0-9]{2}|220-1[0-9]{3}|N10-[0-9]{3}|SY0-[0-9]{3})\b' | sort -u | tr '\n' ' ')
  echo "$slug -> ${code:-'(see page; A+ shows Core 1/Core 2)'}"
done
# tech -> FC0-U71 ; network -> N10-009 ; security -> SY0-701 ; A+ -> 220-1201 / 220-1202
```

## Validation and Troubleshooting

Map the Core certifications:

| Certification | Exam(s) | Focus | Precedes / practice in |
| --- | --- | --- | --- |
| Tech+ | FC0-U71 | Digital and IT literacy | Volume I |
| A+ | 220-1201 + 220-1202 | IT support, hardware, OS, troubleshooting | Volume IV |
| Network+ | N10-009 | Vendor-neutral networking | Volume II; Cisco III, Juniper XXXI |
| Security+ | SY0-701 | Core cybersecurity | Volume X; the security tracks |

Common pitfalls: studying the **retired** Network+ N10-008 or Security+ SY0-601
instead of N10-009 / SY0-701; forgetting that **A+ needs both** Core 1 and Core
2; confusing **Tech+** with the old ITF+ name (same lineage, new name and code
FC0-U71); and underestimating the **performance-based questions**, which reward
hands-on practice over memorization.

## Security and Best Practices

Anchor an IT-security career on **Security+**, and build the groundwork with
**A+** and **Network+** so its concepts land on real understanding. Practice
the **performance-based** skills hands-on. Verify the **current exam version**
before studying, and plan **CE renewal** (Chapter 08). For DoD and regulated
environments, note that **A+, Network+, and Security+** are recognized baseline
certifications under **DoD 8140/8570**.

## References and Knowledge Checks

- comptia.org: certification pages for Tech+, A+, Network+, Security+.
- Cross-reference: [Volume II — Network Engineering Foundations](../volume-02-network-engineering-foundations/README.md); [Volume X — Enterprise Cybersecurity](../volume-10-enterprise-cybersecurity/README.md).

**Knowledge checks**

1. How many exams does A+ require, and what are their current codes?
2. What is the recommended order through the Core pathway, and is it enforced?
3. Which Core certification is the most widely required entry-level security credential?

## Hands-On Lab

Exam-preparation walkthroughs for the Core pathway.

**Shared prerequisites for Labs 2.1–2.2** — a browser; `curl` for Lab 2.1.
**Cost:** none.

### Lab 2.1 — Confirm the Core exam codes (Topic: Verify the pathway)

**Objective:** Prove the current Core codes.

```bash
for slug in tech network security; do
  curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/$slug/" \
    | grep -oE '\b(FC0-U[0-9]{2}|N10-[0-9]{3}|SY0-[0-9]{3})\b' | sort -u | tr '\n' ' '; echo " <- $slug"
done
```

**Expected result:** FC0-U71, N10-009, and SY0-701 — the current Tech+,
Network+, and Security+ exams.

**Negative test:** search the A+ page for a single exam code; A+ is a **Core
Series of two** (220-1201 and 220-1202), not one exam.

**Cleanup:** none.

### Lab 2.2 — Plan a foundational path (Topic: Study plan)

**Objective:** Sequence the Core pathway for a career-changer.

```text
Tech+ (FC0-U71)            digital/IT literacy
  -> A+ (220-1201 + 220-1202)   IT support, hands-on
  -> Network+ (N10-009)         vendor-neutral networking
  -> Security+ (SY0-701)        core cybersecurity (the anchor)
Practice: Volume I (foundations), IV (systems admin), II (networking), X (security).
```

**Expected result:** a Tech+ → A+ → Network+ → Security+ sequence tied to the
encyclopedia's foundation volumes — the recommended learning order.

**Negative test:** jump straight to Security+ with no networking background; its
architecture and operations domains are far harder without Network+ groundwork.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Core pathway runs Tech+ (FC0-U71), A+ (220-1201 + 220-1202), Network+
(N10-009), and Security+ (SY0-701), in that recommended order. It is the
vendor-neutral foundation beneath every networking and security track, anchored
by Security+, with performance-based questions that reward hands-on practice.

- [ ] I can list the Core certifications and current exam codes.
- [ ] I know A+ requires two exams.
- [ ] I can map the Core certs to the foundation and vendor volumes.
- [ ] I can build a foundational study path anchored on Security+.
- [ ] I completed Labs 2.1–2.2 including each negative test.
