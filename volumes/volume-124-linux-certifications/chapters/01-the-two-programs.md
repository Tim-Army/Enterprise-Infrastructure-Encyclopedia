# Chapter 01: The Two Vendor-Neutral Linux Programs

![The two vendor-neutral Linux certification programs. LPI: the Essentials tier (Linux 010, Security 020, Web Development 030, Open Source 050 — lifetime validity) under the professional ladder LPIC-1 (101/102) to LPIC-2 (201/202) to four LPIC-3 specialties (300 Mixed Environments, 303 Security, 305 Virtualization and Containerization, 306 High Availability and Storage), plus the Open Technology track (701 DevOps Tools Engineer, 702 BSD Specialist) — all five-year validity. Linux Foundation: LFCA (60-question associate) and the performance-based LFCS (five weighted domains, two-year validity); LFCT is inactive.](../../../diagrams/volume-124-linux-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Two complementary programs: LPI's knowledge-tested ladder with published, weighted objectives, and the Linux Foundation's performance-based LFCS. Everything both programs test runs free on any Linux machine — this volume's labs are the exam practice.*

## Learning Objectives

- Describe both vendor-neutral Linux certification programs and how they complement each other.
- Know the LPI ladder: Essentials, LPIC-1/2/3, and the Open Technology track, with prerequisites and validity.
- Know the Linux Foundation pair: LFCA and the performance-based LFCS (and that LFCT is inactive).
- Choose the right entry point for your background.

## Program one: LPI (Linux Professional Institute)

LPI is the vendor-neutral Linux certification body. Every exam publishes **detailed public objectives with per-objective weights** — the closest thing in this encyclopedia to an open blueprint culture. Verified on lpi.org, 3 August 2026:

| Tier | Credential | Exams | Prerequisite | Validity |
|:---|:---|:---|:---|:---|
| Essentials | Linux Essentials | 010 (40 Q / 60 min) | none | lifetime |
| Essentials | Security Essentials | 020 (40 Q / 60 min) | none | lifetime |
| Essentials | Web Development Essentials | 030 (40 Q / 60 min) | none | lifetime |
| Essentials | Open Source Essentials | 050 (40 Q / 60 min) | none | lifetime |
| Professional | **LPIC-1** | 101-500 + 102-500 (v5.0) | none | 5 years |
| Professional | **LPIC-2** | 201-450 + 202-450 (v4.5) | active LPIC-1 | 5 years |
| Professional | **LPIC-3 Mixed Environments** | 300 | active LPIC-2 | 5 years |
| Professional | **LPIC-3 Security** | 303 | active LPIC-2 | 5 years |
| Professional | **LPIC-3 Virtualization and Containerization** | 305 | active LPIC-2 | 5 years |
| Professional | **LPIC-3 High Availability and Storage Clusters** | 306 | active LPIC-2 | 5 years |
| Open Technology | DevOps Tools Engineer | 701 | none | 5 years |
| Open Technology | BSD Specialist | 702 | none | 5 years |

The ladder is strict: LPIC-2 requires an **active** LPIC-1, LPIC-3 an active LPIC-2. LPIC-3 is the specialty tier — four separate certifications, each one exam.

## Program two: Linux Foundation

The Linux Foundation's Linux-side credentials (its Kubernetes/cloud-native family is [Volume XLI](../../volume-041-cncf-kubernetes-certifications/README.md)):

| Credential | Format | Details | Validity |
|:---|:---|:---|:---|
| **LFCA** (Certified IT Associate) | 60 multiple-choice | pre-professional IT/Linux/cloud breadth | — |
| **LFCS** (Certified System Administrator) | **Performance-based**, 2 hours, terminal | Five weighted domains: Operations Deployment 25%, Networking 25%, Storage 20%, Essential Commands 20%, Users and Groups 10% | 2 years |
| ~~LFCT (Certified Cloud Technician)~~ | — | **Inactive** — the certification has been discontinued (its LFS203 course remains) | — |

LFCS is the philosophical opposite of the LPI exams: no multiple choice — you fix real systems in a terminal for two hours (killer.sh-style simulator included with registration; $445 exam-only at verification time, one retake, distribution-independent).

## Choosing between (or stacking) them

- **New to IT:** Linux Essentials or LFCA first — both are gentle, no-prerequisite entries.
- **Working admin who wants proof of hands-on skill:** LFCS — performance-based résumés read differently.
- **Building a long-term Linux career ladder:** LPIC-1 → LPIC-2 → an LPIC-3 specialty; the published weighted objectives make study plans precise.
- **Stacking:** LFCS + LPIC-1 cover the same ground two ways (doing vs explaining); many candidates take LFCS after LPIC-1 study as the practical capstone.

Delivery: LPI exams through Pearson VUE (test center or OnVUE); Linux Foundation exams online-proctored through its own platform. Pricing is published at registration for both; confirm there.

## Hands-On Lab

### Lab 1.1 — Read a weighted objective

**Objective:** Use LPI's public objectives the way a study plan should.

```bash
curl -s https://www.lpi.org/our-certifications/exam-101-objectives | tr -s ' \n' ' ' | grep -o "Topic 10[1-4][^<]*" | head -4
```

**Expected result:** The four top-level topics of exam 101-500 (System Architecture; Linux Installation and Package Management; GNU and Unix Commands; Devices, Linux Filesystems, FHS) — each objective beneath them carries a weight of 1–5 that maps directly to question count. Weights tell you where the hours go.

**Negative test:** Study from a book's table of contents instead of the objectives — books drift from objective versions (101-500 is v5.0; 201-450 is v4.5); the objectives page is the contract.

**Cleanup:** None.

### Lab 1.2 — Confirm the LFCT retirement

**Objective:** Practice the currency check that caught a real retirement.

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://training.linuxfoundation.org/lfct-cert-inactive/
```

**Expected result:** `200` — the Linux Foundation's own "LFCT Cert Inactive" page exists; the certification is discontinued even though its course (LFS203) is still sold. A course on sale is not proof its certification lives.

**Negative test:** A third-party site still selling "LFCT prep" — stale mirrors again; the vendor's own inactive notice wins.

**Cleanup:** None.

## Summary and Completion Checklist

- [ ] Both programs mapped: LPI's ladder + Essentials, LF's LFCA/LFCS.
- [ ] Prerequisites and validity internalized (active-cert chaining; Essentials lifetime; LFCS 2 years).
- [ ] LFCT known inactive.
- [ ] Entry point chosen for your background.
