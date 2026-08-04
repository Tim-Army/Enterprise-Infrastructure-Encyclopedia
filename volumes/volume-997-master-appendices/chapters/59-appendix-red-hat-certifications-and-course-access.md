# Chapter 59: Appendix — Red Hat Certifications and Course Access

The **Red Hat** certification program, restructured for 2026 — the five tracks, five levels, and the
training/access model. Verified on **3 August 2026** from **redhat.com/en/services/certifications** and
the individual exam pages, the sources that anchor
[Volume CXXV — Red Hat Certification Tracks](../../volume-125-red-hat-certifications/README.md).
Third-party exam-dump sites were excluded as sources.

**How access works.** Red Hat exams are **100% performance-based** (real tasks on live systems) and are
scheduled through Red Hat — as **remote exams** or at testing centers. Training comes via a **Red Hat
Learning Subscription** (course + lab access) or individual courses; exams can be bought bundled or
standalone. Free lab environments make the hands-on practice no-cost: a **Red Hat Developer
subscription** (genuine RHEL, free for individual use), **AlmaLinux**/**Rocky Linux** (binary-compatible
rebuilds), and **CRC / OpenShift Local** (single-node OpenShift). Credentials appear in the **Red Hat
Certification Central** portal.

> **Currency.** The 2026 restructure introduced **five tracks × five levels**, a **track-specific
> RHCA** (Administrator + Engineer + three same-track Specialists — no more cross-track mixing), and
> three renewal paths (**retake / level up / advance**, where a higher exam auto-renews lower
> credentials). RHCSA (EX200) moved to **RHEL 10**; **EX318** (RHV virtualization) is retired in favor
> of **EX316** (OpenShift Virtualization); the **AI track** is new and its exam codes were **pending**
> at verification. Confirm exam codes and RHEL/OCP versions on redhat.com before booking.

## Free and low-cost resources and entry points

- **[Red Hat certifications](https://www.redhat.com/en/services/certifications)** — the authoritative
  program page and exam catalog
- **[RHCSA exam (EX200)](https://www.redhat.com/en/services/training/red-hat-certified-system-administrator-rhcsa-exam)**
  — the foundational exam objectives
- **[Red Hat Developer](https://developers.redhat.com/)** — free RHEL for individual use (the exam-grade lab)
- **AlmaLinux / Rocky Linux** — free RHEL-compatible rebuilds for RHCSA/RHCE practice
- **[OpenShift Local (CRC)](https://developers.redhat.com/products/openshift-local/overview)** — free
  single-node OpenShift for the OpenShift-track exams

## Fees, delivery, and renewal

- **Fees:** published per exam on redhat.com; the Red Hat Learning Subscription bundles courses, labs,
  and exam attempts. Lab practice on the free environments above is no-cost.
- **Delivery:** 100% performance-based; remote-proctored or at a testing center. Exams like EX280
  present **10–17 hands-on tasks** in a single lab session.
- **Prerequisites:** RHCSA (EX200) is required for RHCE; Specialist exams have **no prerequisites**;
  RHCA requires the track's Administrator + Engineer + three same-track Specialists.
- **Validity/renewal:** RHCSA is valid **3 years**; renew by **retake, level up, or advance** (a
  higher-level pass auto-renews lower credentials in the track).

## The program (five tracks × five levels)

Verified against redhat.com on 3 August 2026. Exam codes shown where confirmed; the AI track's codes
were pending.

### Levels

| Level | Name |
| --- | --- |
| 1 | Technologist |
| 2 | Systems Administrator / Developer |
| 3 | Engineer |
| 4 | Specialist (electives, no prerequisites) |
| 5 | Architect (track-specific RHCA) |

### Flagship exams by track

| Track | L2 (Admin/Dev) | L3 (Engineer) | Representative Specialists (L4) |
| --- | --- | --- | --- |
| Enterprise Linux | **RHCSA EX200** (RHEL 10) | **EX342** | EX415 Security, EX362 IdM, EX436 HA Clustering, EX442 Performance Tuning |
| Ansible | RHCSA EX200 | **RHCE EX294** | EX358 Services Mgmt & Automation, others in-track |
| OpenShift | **EX280** (OCP 4.18); L1 EX180 | **EX380** | EX480 MultiCluster Mgmt, **EX316 OpenShift Virtualization** |
| Cloud-Native Applications | **EX188** | **EX288** | build/pipeline, service mesh, serverless electives |
| AI *(new, provisional)* | codes pending | codes pending | RHEL AI / OpenShift AI focus — verify on redhat.com |

### RHCA (Level 5) — track-specific

RHCA = the track's **Administrator exam + Engineer exam + three Specialist electives within the same
track**. Examples: Enterprise Linux = EX200 + EX342 + {EX415, EX362, EX436}; OpenShift = EX280 + EX380 +
{EX480, EX316, EX288}.

## Notes

- **Everything is performance-based.** There is no multiple-choice Red Hat exam; study is repetition on
  a real lab, which the free environments make no-cost.
- **RHCE is now Ansible-track.** In the 2026 structure EX294 is explicitly the Ansible Engineer exam;
  EX342 is the Enterprise Linux Engineer exam.
- **Retirements move you forward.** EX318 → EX316. Verify a Specialist still exists before committing.
- **Red Hat anchors the IBM "PLUS" combos** ([Volume CXXIII](../../volume-123-ibm-certifications/README.md)),
  which bundle a Red Hat Certified Specialist (OpenShift) exam with an IBM Cloud Pak exam.
