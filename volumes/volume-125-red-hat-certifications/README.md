# Volume CXXV — Red Hat Certification Tracks

> The certification map for **Red Hat**, restructured for 2026 and verified on redhat.com, 3 August 2026:
> **five tracks** (Enterprise Linux, Ansible, OpenShift, Cloud-Native Applications, and a new,
> provisional **AI** track) across **five progressive levels** (Technologist, Systems
> Administrator/Developer, Engineer, Specialist electives, Architect) — every exam **100%
> performance-based** on live systems, no multiple choice. **RHCSA (EX200)**, now on **RHEL 10**, is the
> shared Level-2 foundation and RHCE prerequisite; **RHCE (EX294)** is the Ansible-track Engineer exam
> and **EX342** the Enterprise Linux Engineer exam; **OpenShift** runs EX180 → **EX280** (OCP 4.18) →
> EX380; **Cloud-Native** runs EX188 → EX288. The big 2026 change is a **track-specific RHCA**: an
> Administrator exam + an Engineer exam + **three Specialist electives within the same track** (ending
> the old "any five specialists" accumulation); **EX318** virtualization retired in favor of **EX316**
> (OpenShift Virtualization); and renewal now offers **retake, level up, or advance**. Because the exams
> are hands-on, every chapter is a **walkthrough lab** runnable free on a **Red Hat Developer
> subscription**, **AlmaLinux/Rocky**, and **CRC**.

## Overview

Volume CXXV is a **certification-tracks volume** and the vendor-specific counterpart to the
vendor-neutral [Volume CXXIV](../volume-124-linux-certifications/README.md). Because every Red Hat exam
is performance-based, the volume is structured like the exams: task-shaped walkthroughs with a
verification step, drilling RHCSA end to end (Chapters 02–03) and then each track's Engineer and
Specialist path. It complements the hands-on RHEL depth of
[Volume XIV](../volume-014-red-hat-enterprise-linux-10/README.md) by mapping the whole credential ladder
around it.

Its standing disciplines are version parity (lab must match the exam's RHEL/OCP version), the
track-specific RHCA rule, and honest treatment of the still-forming AI track (whose exam codes are
flagged pending official verification).

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [The Red Hat Certification Program](chapters/01-the-red-hat-program.md) | 1.1–1.2 |
| 02 | [RHCSA — Users, Storage, and Boot (EX200)](chapters/02-rhcsa-users-storage-boot.md) | 2.1–2.5 |
| 03 | [RHCSA — Services, Networking, SELinux, and Containers (EX200)](chapters/03-rhcsa-services-networking-selinux-containers.md) | 3.1–3.6 |
| 04 | [The Enterprise Linux Track — Advanced Administration (EX342)](chapters/04-enterprise-linux-track-ex342.md) | 4.1–4.5 |
| 05 | [The Ansible Track — RHCE (EX294)](chapters/05-ansible-track-ex294.md) | 5.1–5.5 |
| 06 | [The OpenShift Track — Administration (EX280)](chapters/06-openshift-track-ex280.md) | 6.1–6.5 |
| 07 | [The Cloud-Native and AI Tracks](chapters/07-cloud-native-and-ai-tracks.md) | 7.1–7.4 |
| 08 | [Specialist Electives (Level 4)](chapters/08-specialist-electives.md) | 8.1–8.5 |
| 09 | [Choosing a Track, Currency, and Career](chapters/09-choosing-currency-and-career.md) | 9.1–9.2 |

## What you will be able to do

- Map Red Hat's 2026 five-track, five-level, performance-based program.
- Drill RHCSA (EX200) end to end the way the hands-on exam presents tasks.
- Work each track's Engineer exam (EX342 / EX294 / EX280 / EX288) and its Specialist electives.
- Assemble a valid track-specific RHCA and plan renewals by leveling up.
- Keep a plan current through RHEL-version rebasing, retirements, and the provisional AI track.

## Prerequisites

- Linux fundamentals and a RHEL-family lab (RHEL developer subscription / AlmaLinux / Rocky); CRC or `kind`/`minikube` for the OpenShift chapters.
- Related depth: [Volume XIV](../volume-014-red-hat-enterprise-linux-10/README.md) (RHEL/RHCSA), [Volume LIX](../volume-059-ansible/README.md) (Ansible), [Volume XLI](../volume-041-cncf-kubernetes-certifications/README.md) (Kubernetes/OpenShift foundations).

## See also

- [Volume CXXIV — Linux Foundation and LPI Certification Tracks](../volume-124-linux-certifications/README.md) — the vendor-neutral Linux programs, for contrast.
- [Volume CXXIII — IBM Certification Tracks](../volume-123-ibm-certifications/README.md) — whose six "PLUS" combinations bundle a Red Hat OpenShift Specialist exam.
- [Master Appendices — Red Hat appendix](../volume-997-master-appendices/chapters/59-appendix-red-hat-certifications-and-course-access.md) — exams, tracks, and course access.
