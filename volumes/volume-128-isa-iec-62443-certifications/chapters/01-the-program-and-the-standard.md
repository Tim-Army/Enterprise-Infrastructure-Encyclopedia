# Chapter 01: The ISA/IEC 62443 Program and the Standard

![The ISA/IEC 62443 Cybersecurity Certificate Program: Certificate 1 (Cybersecurity Fundamentals Specialist, course IC32) is the mandatory gate, then Certificates 2, 3, and 4 — Risk Assessment Specialist (IC33), Design Specialist (IC34), and Maintenance Specialist (IC37) — in any order, each a course plus exam mapped to a phase of the IACS security lifecycle (assess, design, operate/maintain). Earning all four automatically confers the ISA/IEC 62443 Cybersecurity Expert designation. All grounded in the IEC 62443 standard family.](../../../diagrams/volume-128-isa-iec-62443-certifications/chapter-01-certification-program.svg)

*Figure 1-1. The program: a mandatory Fundamentals gate, three lifecycle specialists (Assess/Design/Maintain) in any order, and an Expert designation earned automatically by holding all four — all built on the IEC 62443 standards for industrial control systems.*

## Learning Objectives

- Describe the ISA/IEC 62443 Cybersecurity Certificate Program: four certificates plus the Expert designation.
- Understand the IEC 62443 standard family and the roles it defines (asset owner, product supplier, service provider).
- Know why OT/ICS security differs from IT security, and how the lifecycle model organizes the program.
- Set up a free study lab that models industrial zones and conduits.

## What ISA/IEC 62443 certifies

**ISA/IEC 62443** is *the* consensus standard for the cybersecurity of **Industrial Automation and Control Systems (IACS)** — the OT world of PLCs, SCADA, DCS, RTUs, and the plant networks that run manufacturing, energy, water, and critical infrastructure. The **ISA/IEC 62443 Cybersecurity Certificate Program** certifies practitioners against that standard, across the whole IACS security lifecycle.

Unlike IT security certifications, 62443 is built for a world where **availability and safety outrank confidentiality** (you cannot reboot a running turbine to patch it), where devices live for decades, and where a security control that adds latency can be a safety hazard.

## The four certificates plus Expert

Verified on isa.org, 4 August 2026:

| Certificate | Course | Lifecycle phase | Prerequisite |
|:---|:---|:---|:---|
| **1 — Cybersecurity Fundamentals Specialist** | **IC32** | Foundation (the whole standard) | none |
| **2 — Cybersecurity Risk Assessment Specialist** | **IC33** | **Assess** (risk assessment of new/existing IACS) | Certificate 1 |
| **3 — Cybersecurity Design Specialist** | **IC34** | **Design** (secure design & implementation) | Certificate 1 |
| **4 — Cybersecurity Maintenance Specialist** | **IC37** | **Operate/Maintain** (operations & maintenance) | Certificate 1 |
| **ISA/IEC 62443 Cybersecurity Expert** | — | (all phases) | **all four certificates** |

The structure: **Certificate 1 (IC32) is the mandatory gate** — you must hold it before attempting 2, 3, or 4, which may be taken **in any order**. Earning all four **automatically** confers the **Expert** designation. Each certificate is a **course plus a proctored exam**; courses come in classroom, virtual (`V`), online self-paced (`E`), and modular (`M`) formats (IC32/IC32V/IC32E/IC32M, etc.). Notably, **the credentials do not expire** — there is no renewal requirement (though staying current with the evolving standard is still on you).

## The standard family and its roles

The IEC 62443 series is organized in four groups:

| Part group | Covers |
|:---|:---|
| **62443-1-x** | General: concepts, terminology, the reference model |
| **62443-2-x** | Policies & procedures: the asset owner's security program (2-1), patch management (2-3), service-provider requirements (2-4) |
| **62443-3-x** | System: risk assessment & system design (3-2), system security requirements and security levels (3-3) |
| **62443-4-x** | Component: secure product development lifecycle (4-1), technical security requirements for components (4-2) |

Three **roles** run through the standard, and the exams test which obligations fall on which:

- **Asset owner** — operates the IACS; owns the security program and the risk it accepts.
- **Product supplier** — builds the components/systems; owns secure development (4-1) and component requirements (4-2).
- **Integration/maintenance service provider** — designs, integrates, and maintains; owns the requirements in 2-4.

## Hands-On Lab

62443 is a standards/design certification, so this volume's labs **model** industrial security concepts (zones, conduits, security levels, risk scoring) with **free Linux primitives** — no OT hardware or ISA software required. **Cost:** none.

### Lab 1.1 — Map the program

**Objective:** Fix the certificate structure and prerequisite chain.

```bash
cat <<'EOF'
Certificate 1  IC32  Fundamentals Specialist   (mandatory gate)
   |-- Certificate 2  IC33  Risk Assessment  (Assess)   any order
   |-- Certificate 3  IC34  Design           (Design)   any order
   |-- Certificate 4  IC37  Maintenance      (Operate)  any order
ALL FOUR -> ISA/IEC 62443 Cybersecurity Expert (automatic; no exam of its own)
No renewal requirement. Verify current course/exam details on isa.org before registering.
EOF
```

**Expected result:** The gated ladder — IC32 first, then IC33/IC34/IC37 in any order, Expert on completing all four. This sequence structures the volume: [Chapters 02–03](02-fundamentals-concepts.md) cover IC32, [04–05](04-risk-assessment-high-level.md) IC33, [06–07](06-design-requirements.md) IC34, [08](08-maintenance-operations.md) IC37.

**Negative test:** Attempting IC33/IC34/IC37 without Certificate 1 — not allowed; the Fundamentals gate is a hard prerequisite, and the exam program enforces it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Stand up the study lab

**Objective:** Prepare the free primitives that model zones and conduits.

```bash
sudo apt-get update -qq && sudo apt-get install -y nftables iproute2 netcat-openbsd python3 2>/dev/null || \
  echo "install nftables, iproute2, netcat, python3 on your distro"
ip netns add ot-test 2>/dev/null && ip netns list | grep ot-test && sudo ip netns del ot-test
echo "lab ready: namespaces model zones, nftables models conduits, python models risk/SL scoring"
```

**Expected result:** Namespaces work and the tooling is present — this volume models 62443's zones/conduits, security levels, foundational requirements, and risk scoring on one host, so the standard's ideas are concrete without a plant.

**Negative test:** Expecting the labs to *be* an IACS — they model the **concepts** the certificates test; the actual standard and ISA courses carry the authoritative detail this volume points you to.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The four certificates + Expert, and the IC32 mandatory gate, understood.
- [ ] The IEC 62443 standard groups (1-x/2-x/3-x/4-x) and the three roles internalized.
- [ ] Why OT security inverts IT priorities (availability/safety first) grasped.
- [ ] The free study lab stood up.
