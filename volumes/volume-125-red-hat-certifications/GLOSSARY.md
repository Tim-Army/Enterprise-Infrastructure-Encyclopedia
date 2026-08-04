# Volume CXXV — Glossary

| Term | Definition |
|:---|:---|
| **CRC (OpenShift Local)** | CodeReady Containers — a single-node OpenShift that runs on a workstation, the free lab for the OpenShift-track exams. |
| **EX200** | The RHCSA exam — 100% performance-based, now based on RHEL 10; the shared Level-2 foundation and RHCE prerequisite. |
| **EX294** | The RHCE exam in the 2026 structure: Red Hat Certified Engineer — Advanced System Administrator in Ansible (the Ansible track's Engineer level). |
| **EX280** | The Red Hat Certified Specialist in OpenShift Administration exam (OCP 4.18); the OpenShift track's Level-2 credential, counts toward RHCA in OpenShift. |
| **EX316** | Red Hat Certified Specialist in OpenShift Virtualization — the current virtualization path after EX318's retirement. |
| **EX342** | The Enterprise Linux track's Engineer-level exam (advanced system administration). |
| **Level (1–5)** | Red Hat's 2026 progression: Technologist, Systems Administrator/Developer, Engineer, Specialist, Architect. |
| **Performance-based exam** | An exam scored on completing real tasks on live systems — every Red Hat certification exam; unverified work is unscored. |
| **RHCA** | Red Hat Certified Architect — since 2026 conferred **per track**: an Administrator exam + an Engineer exam + three Specialist electives within the same track. |
| **RHCE** | Red Hat Certified Engineer — repositioned in 2026 as the Ansible track's Engineer credential (EX294). |
| **RHCSA** | Red Hat Certified System Administrator (EX200) — the near-universal foundation, valid 3 years, prerequisite for RHCE. |
| **RHEL AI** | Red Hat's supported platform for fine-tuning and serving foundation models (InstructLab, Granite) — part of the provisional AI track. |
| **RHEL System Roles** | Pre-built, supported Ansible roles (timesync, firewall, selinux, storage, network, …) — an explicit EX294 objective: configure subsystems by setting role variables. |
| **SCC (Security Context Constraints)** | OpenShift's mechanism restricting what containers may do; the default `restricted-v2` forbids running as root — a defining EX280 topic absent from vanilla Kubernetes. |
| **semanage / restorecon** | The persistent SELinux context tools — `semanage fcontext` defines a rule, `restorecon` applies it; the correct fix for RHCSA's SELinux tasks. |
| **Specialist (RHCS)** | A Level-4 Red Hat Certified Specialist credential with no prerequisites; three same-track Specialists assemble an RHCA. |
| **Stratis** | Red Hat's modern local-storage manager (thin provisioning, snapshots) tested at the EX342/advanced level. |
| **Track** | One of Red Hat's five 2026 specialization paths: Enterprise Linux, Ansible, OpenShift, Cloud-Native Applications, AI. |
| **UBI (Universal Base Image)** | Red Hat's freely redistributable container base images, the sanctioned starting point for Cloud-Native builds. |
| **XFS** | The default RHEL filesystem — it can be grown online (`xfs_growfs`) but never shrunk, a recurring RHCSA storage fact. |
