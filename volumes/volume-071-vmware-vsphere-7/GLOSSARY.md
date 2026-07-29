# Volume LXXI Glossary

Definitions for terms introduced in **Volume LXXI — VMware vSphere 7**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Content Library** — a vCenter store for sharing templates, ISOs, and OVF/OVA across hosts and vCenters.
- **DRS (Distributed Resource Scheduler)** — the cluster service that balances load across hosts using vMotion; rewritten in vSphere 7 to a per-VM scoring model.
- **esxcli** — the ESXi command-line namespace for host configuration and diagnostics.
- **ESXi** — VMware's bare-metal (type-1) hypervisor.
- **EVC (Enhanced vMotion Compatibility)** — a cluster setting that masks CPU features to a common baseline so VMs vMotion across CPU generations.
- **govc** — the open-source Go command-line client for the vSphere API.
- **HA (High Availability)** — the cluster service that restarts VMs on surviving hosts after a host failure.
- **Host profile** — a captured reference host configuration applied and compliance-checked across a cluster.
- **Lockdown mode** — an ESXi security mode restricting direct host access to vCenter.
- **PowerCLI** — VMware's PowerShell module for automating vSphere.
- **SPBM (Storage Policy Based Management)** — attaching a storage policy to a VM so vSphere places and protects it to satisfy the policy.
- **SSO (Single Sign-On)** — vCenter's authentication service (vsphere.local plus AD/LDAP/federation).
- **Template** — a golden, non-runnable VM image for consistent deployment.
- **VCSA (vCenter Server Appliance)** — the Linux appliance form of vCenter Server; the only form in vSphere 7.
- **vCenter Server** — the centralized management platform for ESXi hosts and clusters.
- **vLCM (vSphere Lifecycle Manager)** — image-based, desired-state lifecycle management for cluster hosts.
- **VMFS** — VMware's clustered filesystem for block storage datastores.
- **VMkernel adapter** — a host network interface for management, vMotion, vSAN, or storage traffic.
- **vMotion** — live migration of a running VM between hosts with no downtime.
- **vSAN** — VMware's hyperconverged, software-defined storage pooling hosts' local disks.
- **vSphere with Tanzu** — running Kubernetes workloads (Supervisor, Tanzu Kubernetes clusters) on vSphere alongside VMs.
