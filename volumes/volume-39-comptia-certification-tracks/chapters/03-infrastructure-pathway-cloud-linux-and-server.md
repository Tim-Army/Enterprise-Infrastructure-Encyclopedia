# Chapter 03: Infrastructure Pathway — Cloud+, Linux+, and Server+

## Learning Objectives

- Enumerate the CompTIA Infrastructure certifications and their current exam codes.
- Describe the domain focus of Cloud+, Linux+, and Server+.
- Map each to the encyclopedia's cloud, Linux, and Windows Server volumes.
- Explain how the Infrastructure certs build on the Core pathway.
- Build a study path for a systems or cloud administrator.

## Theory and Architecture

The **Infrastructure** pathway certifies the roles that build and operate
systems — servers, operating systems, and cloud. As verified on comptia.org
(26 July 2026):

- **CompTIA Cloud+** — exam **CV0-004** (V4) across six weighted domains:
  **Cloud architecture (23%)**, **Deployment (19%)**, **Operations (17%)**,
  **Security (19%)**, **DevOps fundamentals (10%)**, and **Troubleshooting
  (12%)** — V4 adds the **DevOps-fundamentals** domain (CI/CD, IaC, automation).
  A 90-question exam (multiple-choice and performance-based) over 90 minutes with
  a **scaled passing score of 750 (100–900)**; 2–3 years as a systems
  administrator or cloud engineer recommended. Vendor-neutral cloud across
  **multi-cloud** environments, complementing the vendor cloud volumes (AWS
  XVII, Azure XXXIII, Google Cloud XXXIV) by teaching the concepts common to all
  of them.
- **CompTIA Linux+** — exam **XK0-006** (V8; XK0-005 retiring) across five
  weighted domains: **System management (23%)**, **Services and user management
  (20%)**, **Security (18%)**, **Automation, orchestration, and scripting
  (17%)**, and **Troubleshooting (22%)** — V8 adds Python scripting, Git,
  containers, and responsible-AI practices. A 90-question exam (multiple-choice
  and performance-based) over 90 minutes with a **scaled passing score of 720
  (100–900)**; ~12 months of Linux experience recommended. It precedes the
  distribution-specific depth of **Volume XIV (RHEL 10)** and **Volume XXI
  (Ubuntu Server)** and vendor exams such as RHCSA.
- **CompTIA Server+** — exam **SK0-005** (V5) across four weighted domains:
  **Server hardware installation and management (18%)**, **Server administration
  (30%)**, **Security and disaster recovery (24%)**, and **Troubleshooting
  (28%)**. A 90-question exam (multiple-choice and performance-based) over 90
  minutes with a **scaled passing score of 750 (100–900)**; A+ and ~2 years in a
  server environment recommended. Server administration on-premises and in
  hybrid environments; it precedes the Windows-specific depth of **Volume
  XXXVI**. (Server+ has historically carried **non-expiring** status — confirm on
  the page.)

## Design Considerations

Build the Infrastructure pathway on the Core foundation: **A+ and Network+**
give the hardware and networking grounding these exams assume, and **Security+**
supplies the security concepts each infrastructure domain applies. Choose the
credential by role — **Cloud+** for cloud/multi-cloud operations, **Linux+**
for Linux administrators, **Server+** for data-center and hybrid server
administrators.

These certifications are **vendor-neutral on purpose**: Cloud+ teaches the
cloud model that AWS, Azure, and Google Cloud each implement differently, so
it pairs naturally with a vendor cloud volume rather than replacing it.
Similarly, Linux+ precedes the RHEL and Ubuntu volumes, and Server+ precedes
the Windows Server volume. All three include **performance-based questions**,
so hands-on lab time — building servers, administering Linux, deploying cloud
resources — is essential.

## Implementation and Automation

Verify the Infrastructure codes from comptia.org:

```bash
for slug in cloud linux server; do
  code=$(curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/$slug/" \
    | grep -oE '\b(CV0-[0-9]{3}|XK0-[0-9]{3}|SK0-[0-9]{3})\b' | sort -u | tr '\n' ' ')
  echo "$slug -> $code"
done
# cloud -> CV0-004 ; linux -> XK0-005 XK0-006 ; server -> SK0-005
```

## Validation and Troubleshooting

Map the Infrastructure certifications:

| Certification | Exam | Focus | Precedes / practice in |
| --- | --- | --- | --- |
| Cloud+ | CV0-004 | Vendor-neutral multi-cloud | Volumes XVII, XXXIII, XXXIV |
| Linux+ | XK0-006 | Linux administration | Volumes XIV, XXI |
| Server+ | SK0-005 | Server hardware/software administration | Volume XXXVI |

Common pitfalls: studying **Linux+ XK0-005** instead of the current **XK0-006**;
treating **Cloud+** as a substitute for a vendor cloud certification (it is the
vendor-neutral complement, not a replacement); and skipping the **Core**
groundwork — the Infrastructure exams assume the hardware, networking, and
security fundamentals that A+, Network+, and Security+ provide.

## Security and Best Practices

Ground the Infrastructure pathway on **Security+** so its security domains
build on real understanding, and practice the **performance-based** tasks in a
lab (a Linux VM, a server build, a free-tier cloud account). Verify the
**current exam version** — Linux+ in particular recently moved to XK0-006.
Pair each credential with the matching vendor volume for depth: Cloud+ with
AWS/Azure/GCP, Linux+ with RHEL/Ubuntu, Server+ with Windows Server. Plan **CE
renewal** (Chapter 08), noting Server+'s historically non-expiring status.

## References and Knowledge Checks

- comptia.org: certification pages for Cloud+, Linux+, Server+.
- Cross-reference: [Volume XIV (RHEL)](../volume-14-red-hat-enterprise-linux-10/README.md), [Volume XXI (Ubuntu)](../volume-21-ubuntu-server-cloud-26-04-lts/README.md), [Volume XXXVI (Windows Server)](../volume-36-windows-server-2025-active-directory/README.md).

**Knowledge checks**

1. Why is Cloud+ a complement to, not a replacement for, a vendor cloud certification?
2. What is the current Linux+ exam code, and which version did it replace?
3. Which encyclopedia volume does Server+ precede?

## Hands-On Lab

Exam-preparation walkthroughs for the Infrastructure pathway.

**Shared prerequisites for Labs 3.1–3.2** — a browser and `curl`; a Linux VM
for Lab 3.2. **Cost:** none.

### Lab 3.1 — Confirm the Infrastructure codes (Topic: Verify the pathway)

**Objective:** Prove the current codes and the Linux+ version change.

```bash
curl -sSL -A "Mozilla/5.0" "https://www.comptia.org/en-us/certifications/linux/" \
  | grep -oE '\bXK0-[0-9]{3}\b' | sort -u
```

**Expected result:** **XK0-006** (and possibly XK0-005 noted as retiring) — the
current Linux+ exam.

**Negative test:** study XK0-005 material as if current; it is the retiring
version — confirm XK0-006.

**Cleanup:** none.

### Lab 3.2 — Practice a Linux+ performance skill (Topic: Hands-on preparation)

**Objective:** Perform a task a Linux+ PBQ simulates.

```bash
# Manage a service, a user, and permissions — core Linux+ objectives
sudo useradd -m -s /bin/bash appuser
sudo systemctl enable --now chronyd 2>/dev/null || sudo systemctl enable --now systemd-timesyncd
id appuser; systemctl is-enabled chronyd 2>/dev/null || systemctl is-enabled systemd-timesyncd
```

**Expected result:** the user exists and a time service is enabled and running
— exactly the kind of task Linux+ performance-based questions assess.

**Negative test:** attempt the same as a non-root user without `sudo`; it is
denied — Linux administration requires privilege, a Linux+ security concept.

**Cleanup:** `sudo userdel -r appuser`.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Infrastructure pathway runs Cloud+ (CV0-004), Linux+ (XK0-006), and Server+
(SK0-005) — vendor-neutral cloud, Linux, and server administration that builds
on the Core pathway and precedes the encyclopedia's vendor cloud, Linux, and
Windows Server volumes.

- [ ] I can list the Infrastructure certs and current exam codes.
- [ ] I can explain Cloud+ as a complement to vendor cloud certs.
- [ ] I can map each to its vendor volume.
- [ ] I can build a systems/cloud administrator study path.
- [ ] I completed Labs 3.1–3.2 including each negative test.
