# Chapter 58: Appendix — Linux (LPI and Linux Foundation) Certifications and Course Access

The two **vendor-neutral Linux** certification programs — **LPI (Linux Professional Institute)** and the
**Linux Foundation** — organized for course access. Verified on **3 August 2026** from **lpi.org**
(certification and exam-objectives pages) and **training.linuxfoundation.org** (certification catalog),
the sources that anchor
[Volume CXXIV — Linux Foundation and LPI Certification Tracks](../../volume-124-linux-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works.** **LPI** exams are delivered through **Pearson VUE** (test center or OnVUE online);
every exam publishes free, detailed **objectives with per-objective weights** on lpi.org — the study
contract. **Linux Foundation** exams (LFCA, LFCS) are online-proctored through the Foundation's own
platform, bundled with a **killer.sh** exam simulator and a course option (LFS207 for LFCS). Both
programs test only **free, standard Linux**, so every lab is runnable at no cost on any Linux machine or
VM. Pricing is published at registration; confirm there.

> **Currency.** Two renewal cadences: **LPI professional/Open Technology = 5 years** (with
> **active-cert chaining** — LPIC-2 needs an active LPIC-1, LPIC-3 an active LPIC-2), **LPI Essentials =
> lifetime**, **LFCS = 2 years**. Objectives are **versioned** (101/102-500 v5.0; 201/202-450 v4.5) —
> study the current version. The Linux Foundation's **LFCT (Cloud Technician) is inactive** even though
> its LFS203 course still sells; verify a certification's status page, not course availability.

## Free and low-cost resources and entry points

- **[LPI certifications](https://www.lpi.org/our-certifications/)** — the authoritative program page
- **[LPI exam objectives](https://www.lpi.org/our-certifications/exam-101-objectives)** — free,
  weighted, per-exam (swap the exam number in the URL: 010/020/030/050, 101/102, 201/202, 300/303/305/306,
  701/702)
- **[Linux Foundation certification catalog](https://training.linuxfoundation.org/certification-catalog/)**
  — LFCA, LFCS, and the cloud-native family
- **[LFCS certification](https://training.linuxfoundation.org/certification/linux-foundation-certified-sysadmin-lfcs/)**
  — the performance-based exam details
- **Any Linux VM** — the only lab environment either program requires (both test standard free tooling)

## Fees, delivery, and renewal

- **Fees:** published at registration. LPI Essentials/LPIC exams via Pearson VUE; LFCS was **$445
  exam-only** at verification (bundles with THRIVE/LFS207 higher). Lab practice is free.
- **Delivery:** LPI — Pearson VUE (test center or OnVUE), multiple-choice/fill-in. Linux Foundation —
  online-proctored; **LFCS is performance-based** (2 hours in a live terminal), LFCA is 60 MCQ.
- **Prerequisites:** none for Essentials, LPIC-1, LFCA, LFCS, and the Open Technology exams; **LPIC-2
  requires active LPIC-1; LPIC-3 requires active LPIC-2**.
- **Validity/renewal:** LPI professional + Open Technology **5 years**, Essentials **lifetime**, LFCS
  **2 years**. Recertify per program policy.

## The certifications

Verified against lpi.org and training.linuxfoundation.org on 3 August 2026.

### LPI — Essentials (lifetime validity)

| Credential | Exam |
| --- | --- |
| Linux Essentials | 010 (40 Q / 60 min) |
| Security Essentials | 020 (40 Q / 60 min) |
| Web Development Essentials | 030 (40 Q / 60 min) |
| Open Source Essentials | 050 (40 Q / 60 min) |

### LPI — Professional ladder (5-year validity)

| Credential | Exams | Prerequisite |
| --- | --- | --- |
| LPIC-1 | 101-500 + 102-500 (objectives v5.0) | none |
| LPIC-2 | 201-450 + 202-450 (objectives v4.5) | active LPIC-1 |
| LPIC-3 Mixed Environments | 300 | active LPIC-2 |
| LPIC-3 Security | 303 | active LPIC-2 |
| LPIC-3 Virtualization and Containerization | 305 | active LPIC-2 |
| LPIC-3 High Availability and Storage Clusters | 306 | active LPIC-2 |

### LPI — Open Technology track (5-year validity, no prerequisites)

| Credential | Exam |
| --- | --- |
| DevOps Tools Engineer | 701 |
| BSD Specialist | 702 |

### Linux Foundation

| Credential | Format | Validity |
| --- | --- | --- |
| LFCA (Certified IT Associate) | 60 multiple-choice | per program |
| LFCS (Certified System Administrator) | **Performance-based**, 2 hrs; domains Operations Deployment 25%, Networking 25%, Storage 20%, Essential Commands 20%, Users and Groups 10% | 2 years |
| LFCT (Certified Cloud Technician) | **Inactive** (course LFS203 remains) | — |

## Notes

- **Two philosophies, one skill.** LPI tests knowledge against weighted public objectives; LFCS tests
  doing, in a live terminal. Candidates often stack LFCS onto LPIC-1 study as the practical capstone.
- **The Foundation's cloud-native family** (CKA/CKAD/CKS, KCNA, etc.) is a separate program — see
  [Volume XLI](../../volume-041-cncf-kubernetes-certifications/README.md).
- **Objective URLs are swappable** — the exam-objectives page pattern makes every blueprint one `curl`
  away, which is how this volume's per-topic labs were scoped.
