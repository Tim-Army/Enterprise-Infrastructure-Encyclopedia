# Chapter 01: vSphere 8 — What's New and the Upgrade from 7

## Learning Objectives

- Identify what vSphere 8 introduced over vSphere 7.
- Explain the vSphere Distributed Services Engine (DPU offload) and vSAN ESA.
- Plan a supported vSphere 7 → 8 upgrade.
- Understand the Broadcom licensing and lifecycle context.
- Verify current platform facts from the authoritative source.

## Theory and Architecture

**VMware vSphere 8** (GA October 2022) builds on the vSphere 7 platform
([Volume LXXI](../../volume-71-vmware-vsphere-7/README.md)) with several headline additions. The
flagship is the **vSphere Distributed Services Engine** (formerly Project Monterey): it offloads
**network and storage I/O and security** to a **DPU/SmartNIC**, freeing host CPU and improving
performance and isolation — vLCM manages the DPU's lifecycle too. Storage gains the **vSAN Express
Storage Architecture (ESA)** — a redesigned, NVMe-optimized architecture that runs alongside the
classic **Original Storage Architecture (OSA)**. Other advances: **vMotion unified data transport**
(faster migration of large/memory-heavy VMs), **device groups** and **vendor device groups** for
coordinated hardware (NICs/GPUs), new **VM hardware versions (v20, v21)**, **Tanzu** enhancements
(**workload availability zones**, supervisor services), and expanded **vLCM** (vSphere 8 is the
**last release to support the legacy baseline/VUM** lifecycle — images are the future). Update
releases (U1/U2/U3) added the latest CPUs, more DPU offload, and vSAN ESA improvements.

This is a **product deep-dive** of vSphere 8 — a companion to the vSphere 7 volume — emphasizing
**what changed**. Because vSphere 7 reached end of general support (2 April 2025), vSphere 8 is the
current target, and much of this volume's value is the **7 → 8 upgrade** and the new capabilities.
Under **Broadcom** (which acquired VMware), licensing is **subscription** — vSphere is delivered
through **VMware vSphere Foundation (VVF)** and **VMware Cloud Foundation (VCF)** bundles.

## Design Considerations

Adopt the **Distributed Services Engine (DPU)** where CPU offload and east-west isolation matter,
and **vSAN ESA** on NVMe hardware for performance. Upgrade **vCenter first, then hosts via vLCM**,
checking interoperability and backups. Move to **image-based vLCM** (baselines are on their way
out). Plan licensing around the **VVF/VCF** subscription bundles.

## Implementation and Automation

Confirm the ESXi 8 version:

```bash
esxcli system version get
# Product: VMware ESXi   Version: 8.0.x   Build: ...
```

## Validation and Troubleshooting

The verified vSphere 8 facts (Broadcom/VMware documentation, 28 July 2026):

```text
vSphere 8 GA Oct 2022. ESXi 8.0 + vCenter 8.0. NEW vs 7:
  - vSphere Distributed Services Engine: offload network/storage/security to DPU/SmartNIC.
  - vSAN 8 Express Storage Architecture (ESA), NVMe-optimized (alongside OSA).
  - vMotion unified data transport (large VMs); device groups; VM hardware v20/v21.
  - Tanzu workload availability zones + supervisor services; vLCM = last release to support baselines.
Upgrade: vCenter 7->8 first, then hosts via vLCM. Broadcom subscription (VVF/VCF).
```

Common pitfalls: upgrading **hosts before vCenter**; and assuming **baseline lifecycle** persists
(8 is the last release to support it — move to images).

## Security and Best Practices

Use the **DPU** for offloaded, isolated network/security services where available, adopt **vSAN
ESA** on suitable hardware, and standardize on **vLCM images**. Upgrade in the supported order with
backups. Track the **Broadcom subscription** licensing model. These build on the vSphere 7
practices.

## References and Knowledge Checks

- techdocs.broadcom.com (VMware vSphere 8 documentation and release notes): the platform and what's new.
- Related encyclopedia volumes: vSphere 7 (LXXI), VMware Virtualization (V), VxRail (XXIV).

**Knowledge checks**

1. What does the vSphere Distributed Services Engine offload, and to what?
2. What is vSAN ESA, and how does it relate to OSA?
3. In what order do you upgrade vCenter and hosts?

## Hands-On Lab

Orientation walkthroughs. **Shared prerequisites for Labs 1.1–1.3** — an ESXi 8 host (physical or
nested) and a shell with `python3`, in a lab. **Cost:** none with an evaluation license.

### Lab 1.1 — Confirm the ESXi 8 version

**Objective:** Verify the platform version.

```bash
esxcli system version get
esxcli hardware platform get
```

**Expected result:** **ESXi 8.0.x** with its build — confirming the version under test.

**Negative test:** assume a host is vSphere 8 from the UI theme; **`esxcli system version get`** is
authoritative — check it.

**Cleanup:** none (read-only).

### Lab 1.2 — Map the 7 → 8 differences

**Objective:** Record what vSphere 8 adds.

```python
python3 - <<'PY'
new_in_8={"Distributed Services Engine":"offload network/storage/security to DPU/SmartNIC",
          "vSAN ESA":"NVMe-optimized storage architecture (alongside OSA)",
          "vMotion unified data transport":"faster migration of large VMs",
          "Device groups":"coordinated NIC/GPU hardware","Tanzu":"workload availability zones + supervisor services",
          "vLCM":"last release to support baseline lifecycle (use images)"}
for k,v in new_in_8.items(): print(f"{k:32}: {v}")
PY
```

**Expected result:** the key **vSphere 8 additions** over 7 — the upgrade motivation.

**Negative test:** treat 8 as a minor patch of 7; the **DPU/ESA/lifecycle** changes are
significant — plan for them.

**Cleanup:** none.

### Lab 1.3 — Plan the upgrade order

**Objective:** Sequence a supported 7 → 8 upgrade.

```python
python3 - <<'PY'
steps=["Check interoperability + hardware compatibility (HCL)","Back up VCSA + VMs",
       "Upgrade vCenter 7 -> 8 FIRST","Upgrade hosts via vLCM (image or baseline)",
       "Upgrade VM hardware/Tools as needed","Validate"]
for i,s in enumerate(steps,1): print(f"{i}. {s}")
PY
```

**Expected result:** the supported upgrade sequence — **vCenter first**, then hosts, with backups
and validation.

**Negative test:** upgrade ESXi hosts before vCenter; **vCenter must be upgraded first** — follow
the order.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere 8 adds the Distributed Services Engine (DPU offload), vSAN ESA, vMotion unified data
transport, device groups, new VM hardware, Tanzu enhancements, and image-forward vLCM (the last
release to support baselines), under Broadcom subscription licensing. Upgrade vCenter first, then
hosts, and adopt the new capabilities where they fit.

- [ ] I can name the key vSphere 8 additions.
- [ ] I can explain the DPU offload and vSAN ESA.
- [ ] I can sequence a 7 → 8 upgrade.
- [ ] I can confirm the ESXi 8 version.
- [ ] I completed Labs 1.1–1.3 including each negative test.
