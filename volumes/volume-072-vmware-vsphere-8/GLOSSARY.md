# Volume LXXII Glossary

Definitions for terms introduced in **Volume LXXII — VMware vSphere 8**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Configuration profiles** — vSphere 8 U2+ desired-state, cluster-wide host configuration model (successor direction to host profiles).
- **Device group** — a binding of coordinated hardware (e.g., a NIC and GPU, or a vendor-defined set) that a VM consumes together, kept intact across placement and migration.
- **DPU (Data Processing Unit)** — a SmartNIC with its own CPU/memory/OS that runs offloaded services under the vSphere Distributed Services Engine.
- **DSE (vSphere Distributed Services Engine)** — vSphere 8's capability to run networking, storage, and NSX security on a DPU, offloading them from the host CPU.
- **ESA (Express Storage Architecture)** — vSAN 8's single-tier, all-NVMe, log-structured architecture giving RAID-5/6 with mirror-like performance.
- **Identity federation** — vCenter delegating authentication to an external identity provider (OIDC), so login and MFA happen at the IdP.
- **OSA (Original Storage Architecture)** — the classic two-tier (cache + capacity) vSAN architecture, still supported alongside ESA.
- **TPM 2.0 / secure boot** — hardware-rooted trust providing attestation of the ESXi boot chain.
- **VCF (VMware Cloud Foundation)** — Broadcom's private-cloud platform bundle that includes vSphere.
- **VVF (VMware vSphere Foundation)** — a Broadcom subscription bundle delivering vSphere and related components.
- **vGPU** — a virtual GPU profile (NVIDIA and others) giving a VM shared, accelerated GPU access.
- **vMotion unified data transport** — the vSphere 8 enhancement that speeds live migration of large, memory-heavy VMs.
- **vLCM (vSphere Lifecycle Manager)** — desired-state, image-based host (and DPU) lifecycle management; vSphere 8 is the last release to support the legacy baseline model.
- **vSphere Distributed Switch (vDS)** — the vCenter-managed distributed virtual switch, which can run on a DPU with DSE.
- **Workload availability zone** — a mapping of Tanzu Kubernetes workloads to vSphere failure domains for zone-fault tolerance.
