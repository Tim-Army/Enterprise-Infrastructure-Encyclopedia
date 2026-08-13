# Chapter 01: The OPSWAT Academy and Critical Infrastructure Protection

![The OPSWAT Academy certification program: a free-first Critical Infrastructure Protection (CIP) academy across four tracks — CIP Essentials, CyberOps, OPSWAT Product Training, and End-User Guides. Associate-level certifications (ICIP, OCFA, OECA, OFSA, ONSA, OSSA — many free) build on the vendor-neutral CIP foundation into the MetaDefender product Professional certifications and the OT Security Expert designation, all badged on Credly with ISC2 CPE credit.](../../../diagrams/volume-129-opswat-certifications/chapter-01-certification-program.svg)

*Figure 1-1. The OPSWAT Academy: free foundational CIP and Associate certifications, then MetaDefender product Professional certs and an OT Security Expert track — organized to close the critical-infrastructure security skills gap.*

## Learning Objectives

- Describe the OPSWAT Academy program: the four tracks, the Associate certifications, the Professional product certs, and the OT Security Expert designation.
- Understand Critical Infrastructure Protection (CIP) and why OPSWAT's technologies target it.
- Know the logistics: the free-first model, Credly badges, ISC2 CPE credit, and validity.
- Set up a free study lab that models OPSWAT's core defensive techniques.

## What OPSWAT certifies

**OPSWAT** builds **Critical Infrastructure Protection (CIP)** technology — defenses for the file, device, network, and data-transfer paths into sensitive environments (utilities, manufacturing, government, healthcare, OT). Its signature techniques are **Deep CDR** (Content Disarm & Reconstruction), **Multiscanning** (many anti-malware engines in parallel), and secure data transfer across trust boundaries (including into air-gapped OT).

The **OPSWAT Academy** certifies practitioners on CIP concepts and the OPSWAT platform. Its distinguishing move is a **free-first model**: the foundational and Associate certifications are free (explicitly to address the CIP skills shortage), with advanced/product certifications paid.

## The program structure

Verified on opswatacademy.com, 4 August 2026. Four **tracks**:

| Track | What it covers |
|:---|:---|
| **CIP Essentials** | Vendor-neutral CIP foundations |
| **CyberOps** | Hands-on red/blue team, ethical hacking, OSINT, protocol analysis, PLC security |
| **OPSWAT Product Training** | MetaDefender platform technical training |
| **End-User Guides** | Product usage |

**Associate-level certifications** (Credly badges, many free):

| Cert | Focus |
|:---|:---|
| **ICIP** — Introduction to Critical Infrastructure Protection | CIP concepts; identifying critical networks (free intro) |
| **OCFA** — Cybersecurity Fundamentals Associate | Infosec vs cybersecurity vs ethical hacking; career paths |
| **OFSA** — File Security Associate | Protecting file systems; Deep CDR, multiscanning, static vs dynamic analysis |
| **OECA** — Endpoint Compliance Associate | Endpoint posture, NAC, BYOD risks |
| **ONSA** — Network Security Associate | NAC, layer-2 vs layer-3 deployments |
| **OSSA** — Secure Storage Associate | Secure file storage and transfer (MetaDefender Vault) |

**Professional-level** (product, paid — around US$1,000 each): **MetaDefender Core**, **MetaDefender MFT**, **MetaDefender ICAP**, and **MetaDefender Kiosk** Professional, plus a 3-day MetaDefender Platform Bootcamp. **Expert-level**: the **OPSWAT OT Security Expert** designation.

Badges issue on **Credly**; many courses carry **ISC2 CPE credit** (maintaining CISSP/SSCP/CCSP). Some Associate badges carry a validity window (they can expire) — **verify current validity on opswatacademy.com**.

## Hands-On Lab

The certifications are defensive-concept-and-product; this volume **models** OPSWAT's core techniques (CDR, multiscanning, posture, secure transfer) with **free Linux/Python primitives** — no OPSWAT software or license required. **Cost:** none.

### Lab 1.1 — Map the program

**Objective:** Fix the track and certification structure.

```bash
cat <<'EOF'
Tracks: CIP Essentials | CyberOps | OPSWAT Product Training | End-User Guides
Associate (Credly, many FREE): ICIP, OCFA, OFSA, OECA, ONSA, OSSA
Professional (paid ~$1,000): MetaDefender Core / MFT / ICAP / Kiosk
Expert: OPSWAT OT Security Expert
Badges: Credly | CPE: ISC2 | Validity: some certs expire -> verify on opswatacademy.com
EOF
```

**Expected result:** The free-first ladder — vendor-neutral CIP + Associate certs (free) building toward paid product Professionals and the OT Security Expert. This structure organizes the volume: [Chapter 02](02-cip-fundamentals.md) covers ICIP/OCFA, [03–04](03-file-security-cdr.md) OFSA, [05](05-endpoint-compliance.md) OECA, [06](06-network-security.md) ONSA, [07](07-secure-data-flow-ot.md) OSSA + OT boundary, [08](08-metadefender-professional-ot-expert.md) the product/Expert tier.

**Negative test:** Assuming the certifications never expire — some Associate badges carry a validity window; the exam program and Credly show expiry, so re-verify rather than assume permanence.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 1.2 — Stand up the study lab

**Objective:** Prepare the free primitives that model OPSWAT's techniques.

```bash
sudo apt-get update -qq && sudo apt-get install -y python3 file 2>/dev/null || echo "install python3 and file"
python3 -c "import hashlib, re, zipfile; print('hashlib/re/zipfile available for multiscan/CDR modeling')"
echo "lab ready: python models Deep CDR (strip active content), multiscanning (multi-source detection),"
echo "           endpoint posture, NAC decisions, and secure-transfer scanning"
```

**Expected result:** Python and its standard library present — this volume models Content Disarm & Reconstruction, multiscanning, posture checks, and boundary scanning on one host, so the CIP techniques are concrete without OPSWAT products.

**Negative test:** Expecting the labs to *be* MetaDefender — they model the **defensive concepts** the certifications teach; the real MetaDefender platform (30+ engines, production CDR) carries the authoritative implementation this volume points to.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Summary and Completion Checklist

- [ ] The four tracks, Associate certs, Professional product certs, and OT Security Expert understood.
- [ ] CIP and OPSWAT's core techniques (Deep CDR, multiscanning, secure transfer) internalized.
- [ ] The free-first model, Credly badges, CPE credit, and validity caveat known.
- [ ] The free study lab stood up.
