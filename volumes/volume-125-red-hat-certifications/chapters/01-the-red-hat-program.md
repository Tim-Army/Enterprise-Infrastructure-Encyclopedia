# Chapter 01: The Red Hat Certification Program

![The Red Hat certification program restructured for 2026: five tracks (Enterprise Linux, Ansible, OpenShift, Cloud-Native Applications, AI) across five progressive levels (Technologist, Systems Administrator/Developer, Engineer, Specialist electives, Architect). RHCSA EX200 on RHEL 10 is the shared Level 2 foundation; RHCA is now conferred track-specifically from an Administrator exam plus an Engineer exam plus three same-track Specialist electives. Every exam is 100% performance-based on live systems.](../../../diagrams/volume-125-red-hat-certifications/chapter-01-certification-program.svg)

*Figure 1-1. Red Hat's 2026 program: five tracks × five levels, all performance-based. RHCSA (EX200, RHEL 10) is the shared foundation; RHCA is now track-specific, ending the old "any five specialists" accumulation.*

## Learning Objectives

- Describe Red Hat's restructured 2026 certification program: five tracks, five levels, all performance-based.
- Know the flagship exams: RHCSA (EX200), the Engineer level (EX294/EX342), OpenShift (EX280), and how RHCA is now conferred.
- Understand what changed in 2026: the track structure, RHEL 10 basis, track-specific RHCA, and retirements.
- Set up a free RHEL-family lab for the performance-based exams.

## The program restructured

Red Hat's certifications are **100% performance-based** — every exam is real tasks on live systems, no multiple choice. In 2026 Red Hat reorganized the catalog into **five tracks**, each with **five progressive levels**. Verified on redhat.com, 3 August 2026:

| Level | Name | What it is |
|:---|:---|:---|
| 1 | Technologist | Foundational entry (e.g. OpenShift EX180) |
| 2 | Systems Administrator / Developer | Core working credential (RHCSA EX200; OpenShift EX280) |
| 3 | Engineer | Advanced administration/automation (EX294, EX342) |
| 4 | Specialist | Focused elective exams (no prerequisites) |
| 5 | Architect | Track-specific RHCA |

The five tracks: **Enterprise Linux**, **Ansible**, **OpenShift**, **Cloud-Native Applications**, and a new **AI** track (its exam codes were still pending at verification — confirm on redhat.com before planning).

## The flagship credentials

| Credential | Exam | Level / track |
|:---|:---|:---|
| **RHCSA** (Certified System Administrator) | **EX200** (RHEL 10) | L2, shared by Enterprise Linux + Ansible |
| **RHCE** — Advanced System Administrator in Ansible | **EX294** | L3, Ansible track |
| Advanced System Administrator (Enterprise Linux) | **EX342** | L3, Enterprise Linux track |
| **RHCS in OpenShift Administration** | **EX280** (OCP 4.18) | L2, OpenShift track |
| Advanced OpenShift Administrator | **EX380** | L3, OpenShift track |
| Cloud-Native Developer | **EX188** / **EX288** | Cloud-Native track |

**RHCSA (EX200)** is the hinge: a 100% hands-on exam (2.5–3 hours, valid 3 years, based on **RHEL 10**), the prerequisite for RHCE and the entry to both the Enterprise Linux and Ansible tracks. Its name, code, and objective areas are unchanged despite the RHEL 10 rebase.

## What changed in 2026

- **Track-specific RHCA.** Previously you accumulated *any five* Specialist exams. Now **RHCA is conferred per track**: an Administrator/Developer exam + an Engineer exam + **three Specialist electives within the same track** — no more cross-domain mixing.
- **RHCE repositioned.** EX294 is explicitly the *Ansible* Engineer exam; EX342 is the *Enterprise Linux* Engineer exam.
- **RHEL 10 basis.** RHCSA (and the Linux-track exams) moved to RHEL 10; the RHEL 9 EX200 may linger for a window — check the exam page before booking.
- **Retirements.** **EX318** (Virtualization Specialist) is retired; virtualization candidates are directed to **EX316** (OpenShift Virtualization Specialist).
- **Renewal paths.** Three options replaced the single retake: **retake, level up, or advance** — passing a higher-level exam automatically renews lower credentials in the same track.

## Relationship to the rest of the encyclopedia

This volume is the **certification map**; the hands-on RHEL depth lives in [Volume XIV — Red Hat Enterprise Linux 10](../../volume-014-red-hat-enterprise-linux-10/README.md) (which targets RHCSA), OpenShift/Kubernetes foundations in [Volume XLI](../../volume-041-cncf-kubernetes-certifications/README.md), and Ansible in [Volume LIX](../../volume-059-ansible/README.md). Red Hat also anchors the **six IBM "PLUS" combinations** ([Volume CXXIII](../../volume-123-ibm-certifications/README.md)), which bundle a Red Hat Certified Specialist (OpenShift) exam.

## Hands-On Lab

RHCSA-family exams run on RHEL; a free equivalent lab uses **AlmaLinux**, **Rocky Linux**, or a **RHEL developer subscription** (free for individual use) — CentOS Stream tracks ahead of RHEL. **Cost:** none.

### Lab 1.1 — Confirm the exam's RHEL basis

**Objective:** Practice the currency check the RHEL 10 rebase makes necessary.

```bash
cat /etc/os-release | grep -E "^(NAME|VERSION)=" 
# On a RHEL-family lab host, confirm the major version matches the exam (RHEL 10 for current EX200)
rpm -q redhat-release 2>/dev/null || rpm -q almalinux-release rocky-release 2>/dev/null || echo "use a RHEL-family distro"
```

**Expected result:** The distribution and major version — your lab must match the exam's RHEL major version (10 for the current EX200). A RHEL 9 lab studies a version the exam is leaving; the exam page is authoritative on which is live.

**Negative test:** Studying EX200 on RHEL 8 — several tools (network, package, SELinux defaults) differ enough to cost points; version parity is not optional on a performance exam.

**Cleanup:** None.

### Lab 1.2 — Prove your lab is exam-representative

**Objective:** Confirm the performance-exam primitives exist on your lab.

```bash
systemctl --version | head -1        # systemd (services/targets)
getenforce                            # SELinux (enforcing expected)
firewall-cmd --state 2>/dev/null || echo "install firewalld"
command -v dnf && command -v podman   # package + container tooling
```

**Expected result:** systemd present, SELinux **Enforcing**, firewalld running, and `dnf`/`podman` available — the exact subsystems RHCSA tests. If SELinux is disabled or firewalld is missing, your lab misrepresents the exam.

**Negative test:** `setenforce 0` (permissive) and treat SELinux tasks as passing — the real exam runs Enforcing; practicing in permissive teaches the wrong habits.

**Cleanup:** Restore `setenforce 1` if you changed it.

## Summary and Completion Checklist

- [ ] Five-track, five-level, all-performance-based structure understood.
- [ ] Flagship exams (EX200/EX294/EX342/EX280) and their track placement known.
- [ ] 2026 changes internalized: track-specific RHCA, RHEL 10 basis, EX318 retirement, renewal paths.
- [ ] A RHEL-family lab stood up with SELinux enforcing.
