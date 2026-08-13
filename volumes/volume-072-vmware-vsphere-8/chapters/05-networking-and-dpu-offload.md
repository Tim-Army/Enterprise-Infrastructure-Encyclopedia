# Chapter 05: Networking and DPU Offload

## Learning Objectives

- Configure vSphere 8 distributed switch networking.
- Explain DPU-offloaded networking and NSX on the Distributed Services Engine.
- Separate and protect traffic types.
- Apply NIC teaming and Network I/O Control.
- Complete a walkthrough for each networking topic.

## Theory and Architecture

vSphere 8 networking keeps the vSphere 7 model — the **vSphere Distributed Switch (vDS)** managed in
vCenter, **port groups** and **VLAN-tagged VMkernel adapters**, **NIC teaming**, and **Network I/O
Control** — and adds the **Distributed Services Engine (DSE)** dimension. When a host has a **DPU**,
the vDS and (with **NSX**) the distributed firewall can **run on the DPU** instead of the host CPU:
packet switching and security enforcement happen on the SmartNIC, freeing host cores and isolating
the network data path from the workload domain. This is especially powerful for **NSX**
micro-segmentation at scale — the east-west firewall runs in hardware. Where no DPU exists,
networking behaves like vSphere 7. The design fundamentals are unchanged: use a **vDS**, **separate
traffic types** (management, vMotion, vSAN, VM) by VLAN/uplink, **team** NICs for redundancy, and
protect critical traffic with **NIOC** — DSE changes *where* the work runs, not the model.

## Design Considerations

Use the **vDS** everywhere; where DPUs are present, **offload** switching/NSX to them for CPU
savings and isolation. **Separate** traffic types and **team** uplinks. Apply **NIOC** to guarantee
bandwidth to vSAN/vMotion. Plan NSX micro-segmentation to exploit DPU acceleration where available.

## Implementation and Automation

The labs create a vDS and port group, add a VMkernel adapter, and reason about DPU offload.

## Validation and Troubleshooting

Confirm the networking model:

```text
vDS (vCenter-wide) + port groups + VMkernel adapters (mgmt/vMotion/vSAN) + VLANs + NIC teaming + NIOC.
DSE: with a DPU, vDS switching + NSX distributed firewall run ON the DPU -> host CPU freed, data path isolated.
No DPU -> behaves like vSphere 7. Separate traffic types; team uplinks.
```

Common pitfalls: expecting **DPU offload** on hosts without a DPU; and mixing all traffic on **one
VLAN/uplink**.

## Security and Best Practices

Prefer the **vDS**, offload **NSX security to the DPU** where available (hardware-enforced
micro-segmentation), **separate** and **team** traffic, and use **NIOC**. Apply port-group security
policies. DSE strengthens isolation between infrastructure and workloads.

## Hands-On Lab

Networking walkthroughs. **Shared prerequisites** — vCenter 8 with hosts and free uplinks, PowerCLI,
in a lab. **Cost:** none.

### Lab 5.1 — Create a distributed switch and port group

**Objective:** Build vCenter-wide networking.

```powershell
$vds = New-VDSwitch -Name "vds8-prod" -Location (Get-Datacenter DC1) -NumUplinkPorts 2
New-VDPortgroup -VDSwitch $vds -Name "app-vlan200" -VlanId 200
Get-VDPortgroup -VDSwitch $vds
```

**Expected result:** a **vDS** with a VLAN-200 port group — consistent networking across hosts.

**Negative test:** replicate a port group on each host's vSS; a **vDS** defines it once — use it.

**Rollback:** `Remove-VDSwitch vds8-prod -Confirm:$false`.

### Lab 5.2 — Add a vMotion VMkernel adapter

**Objective:** Dedicate a network to host traffic.

```powershell
$h = (Get-VMHost)[0]
New-VMHostNetworkAdapter -VMHost $h -PortGroup "vmotion" -VirtualSwitch (Get-VDSwitch vds8-prod) `
  -IP 10.0.60.11 -SubnetMask 255.255.255.0 -VMotionEnabled $true
Get-VMHostNetworkAdapter -VMHost $h -VMKernel | Select Name, IP, VMotionEnabled
```

**Host setup — deploying this image on your hypervisor.** The create/import and interface-mapping steps are the same for every appliance and are collected once in the Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md) — Proxmox, KVM, ESXi/vSphere, Workstation/Fusion, VirtualBox, Hyper-V, EVE-NG, GNS3, containerlab, Nutanix AHV, and Xen.

**Expected result:** a **VMkernel adapter** with **vMotion enabled** on its own network — separated
host traffic.

**Negative test:** share vMotion with management traffic; **dedicate** a VMkernel/VLAN to vMotion.

**Rollback:** remove the VMkernel adapter.

### Lab 5.3 — DPU-offloaded networking concept

**Objective:** Describe network offload with DSE.

```text
# With a DPU + DSE: the vDS forwarding and the NSX distributed firewall run on the DPU.
#   Host CPU no longer processes east-west switching/security -> more capacity for VMs; isolated data path.
"DPU networking: vDS + NSX DFW on the DPU -> host CPU freed + hardware-enforced micro-segmentation"
```

**Expected result:** the **DPU-offloaded networking** model — switching and security in hardware.

**Negative test:** expect DPU offload benefits with a software-only host; offload needs a **DPU** —
size hardware for it.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 5.4 — NIC teaming and NIOC

**Objective:** Redundant, protected networking.

```powershell
Get-VDPortgroup -VDSwitch (Get-VDSwitch vds8-prod) -Name "app-vlan200" |
  Get-VDUplinkTeamingPolicy | Set-VDUplinkTeamingPolicy -LoadBalancingPolicy LoadBalanceLoadBased `
  -ActiveUplinkPort "dvUplink1","dvUplink2"
# Enable Network I/O Control on the vDS to guarantee bandwidth to vSAN/vMotion.
```

**Expected result:** **NIC teaming** (two active uplinks) with **NIOC** available — redundant,
bandwidth-protected networking.

**Negative test:** run on a **single uplink** with no NIOC; a failure drops the network and vSAN can
starve — team and protect.

**Rollback:** revert the teaming policy.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere 8 networking keeps the vDS model (port groups, VMkernel adapters, teaming, NIOC) and adds
DPU offload via the Distributed Services Engine — running vDS switching and NSX security in hardware
to free host CPU and isolate the data path. Use a vDS, offload to DPUs where present, separate and
team traffic, and protect with NIOC.

- [ ] I can create a vDS and port group.
- [ ] I can add a vMotion VMkernel adapter.
- [ ] I can explain DPU-offloaded networking and NSX.
- [ ] I can configure NIC teaming and NIOC.
- [ ] I completed Labs 5.1–5.4 including each negative test.
