# Chapter 01: vSphere 7 Architecture and What's New

## Learning Objectives

- Explain the vSphere 7 platform: ESXi, vCenter Server, and the management model.
- Identify what vSphere 7 introduced (VCSA-only, vLCM, rewritten DRS, vSphere with Tanzu).
- Understand the vSphere 7 support lifecycle and its place today.
- Describe the tooling this volume uses (esxcli, PowerCLI, govc, the API).
- Verify current platform facts from the authoritative source.

## Theory and Architecture

**VMware vSphere 7** (GA April 2020) is the virtualization platform pairing the **ESXi** bare-metal
hypervisor with **vCenter Server** for centralized management. ESXi runs directly on server
hardware, abstracting CPU, memory, storage, and networking into virtual machines; vCenter Server
provides the single pane of glass, clustering, and the features that make virtualization an
enterprise platform — **vMotion**, **DRS**, **HA**, **vSAN**, and **SPBM**. vSphere 7 made several
notable changes: **vCenter Server is appliance-only (VCSA)** — the Windows-based vCenter was
removed; **vSphere Lifecycle Manager (vLCM)** introduced **image-based** host lifecycle management
(a desired-state image for a whole cluster) alongside the legacy baseline model; **DRS was
rewritten** to a per-VM, workload-centric scoring model; and **vSphere with Tanzu** brought
**Kubernetes** into vSphere, letting the same platform run VMs and containers.

This volume is a **product deep-dive** of vSphere 7 — distinct from
[Volume V (VMware Virtualization)](../../volume-05-vmware-virtualization/README.md) and its
certification appendix — teaching install, configuration, and operation with hands-on labs.
Because vSphere 7's **end of general support was 2 April 2025** (technical guidance to April 2027),
much of the installed base is planning or executing the **upgrade to vSphere 8**
([Volume LXXII](../../volume-72-vmware-vsphere-8/README.md)); this volume covers 7 as it stands and
flags the path forward. Note that under **Broadcom** (which acquired VMware), licensing moved to a
**subscription** model (VMware vSphere Foundation / VMware Cloud Foundation).

## Design Considerations

Treat **ESXi** as disposable and **vCenter** as the source of truth; manage clusters, not
individual hosts. Prefer **vLCM image-based** lifecycle for consistency. Design for the platform
features (vMotion/DRS/HA) from the start. Given vSphere 7's support status, plan the **upgrade to
8**. Automate with **PowerCLI/govc/API** rather than clicking.

## Implementation and Automation

Confirm the platform version from a host:

```bash
esxcli system version get
# Product: VMware ESXi   Version: 7.0.x   Build: ...
```

## Validation and Troubleshooting

The verified vSphere 7 facts (Broadcom/VMware documentation, 28 July 2026):

```text
vSphere 7 GA April 2020. ESXi 7.0 + vCenter Server 7.0 (VCSA appliance ONLY; Windows vCenter removed).
New: vLCM (image-based host lifecycle), rewritten per-VM DRS, vSphere with Tanzu (Kubernetes), vSAN 7.
Support: end of general support 2 Apr 2025; technical guidance to 2 Apr 2027 -> plan upgrade to vSphere 8.
Licensing: Broadcom subscription (VMware vSphere Foundation / Cloud Foundation).
```

Common pitfalls: expecting a **Windows vCenter** (7 is **VCSA-only**); and running vSphere 7 as a
long-term target past its **general-support** date.

## Security and Best Practices

Manage from **vCenter**, keep hosts on a consistent **vLCM image**, and secure the platform (SSO,
roles, TLS, lockdown mode — Chapter 8). Track the **support lifecycle** and plan upgrades. Automate
for repeatability and auditability. These practices carry into vSphere 8.

## References and Knowledge Checks

- techdocs.broadcom.com (VMware vSphere documentation): the ESXi/vCenter 7 documentation and release notes.
- Related encyclopedia volumes: VMware Virtualization (V), VxRail (XXIV), and vSphere 8 (LXXII).

**Knowledge checks**

1. What changed about vCenter Server in vSphere 7?
2. What did vSphere Lifecycle Manager introduce?
3. When did vSphere 7 reach end of general support?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — an ESXi 7 host (physical or
nested) and a shell with `curl`/`python3`, in a lab. **Cost:** none with an evaluation license.

### Lab 1.1 — Confirm the ESXi version

**Objective:** Verify the platform version and build.

```bash
esxcli system version get
esxcli hardware platform get
```

**Expected result:** **ESXi 7.0.x** with its build number and the hardware platform — confirming
the version under test.

**Negative test:** assume a host is vSphere 7 from the login banner alone; **`esxcli system version
get`** is authoritative — check it.

**Cleanup:** none (read-only).

### Lab 1.2 — Map the management model

**Objective:** Record the ESXi/vCenter relationship.

```python
python3 - <<'PY'
model={"ESXi 7":"bare-metal hypervisor (per host)","vCenter 7 (VCSA)":"central mgmt of many hosts (appliance only)",
       "cluster":"hosts grouped for vMotion/DRS/HA","vLCM":"desired-state image lifecycle"}
for k,v in model.items(): print(f"{k:18}: {v}")
PY
```

**Expected result:** the **ESXi → vCenter → cluster** model with vLCM — the platform architecture.

**Negative test:** manage each host standalone; **vCenter** provides clustering/features — manage
centrally.

**Cleanup:** none.

### Lab 1.3 — Check the support lifecycle

**Objective:** Reason about vSphere 7's lifecycle position.

```python
python3 - <<'PY'
from datetime import date
eogs=date(2025,4,2); today=date(2026,7,28)
print("vSphere 7 end of general support:", eogs)
print("past general support:", today>eogs, "-> plan/execute upgrade to vSphere 8")
PY
```

**Expected result:** vSphere 7 is **past general support** — the upgrade to vSphere 8 is the
forward path.

**Negative test:** deploy new vSphere 7 as a long-term platform; it is **past general support** —
target vSphere 8 for new builds.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere 7 pairs ESXi 7 with appliance-only vCenter Server 7, introduced image-based vLCM,
rewrote DRS, and brought Kubernetes via vSphere with Tanzu. It is past general support (2 April
2025), so it coexists with upgrade planning to vSphere 8, under Broadcom subscription licensing.
Manage centrally, keep a consistent image, and automate.

- [ ] I can explain the ESXi/vCenter/cluster model.
- [ ] I can name what vSphere 7 introduced.
- [ ] I can confirm the ESXi version with esxcli.
- [ ] I can state vSphere 7's support-lifecycle position.
- [ ] I completed Labs 1.1–1.3 including each negative test.
