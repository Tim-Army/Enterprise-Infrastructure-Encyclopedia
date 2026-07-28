# Chapter 05: vSphere Networking

## Learning Objectives

- Explain vSphere standard switches and distributed switches.
- Configure port groups, VLANs, and VMkernel adapters.
- Apply NIC teaming and failover policies.
- Understand distributed switch benefits at scale.
- Complete a walkthrough for each networking topic.

## Theory and Architecture

vSphere connects VMs and hosts through virtual switches. A **vSphere Standard Switch (vSS)** exists
**per host** — simple but managed host by host. A **vSphere Distributed Switch (vDS)** is configured
once in **vCenter** and spans all hosts in the cluster, giving consistent networking, advanced
features (NetFlow, port mirroring, LACP, Network I/O Control), and central management — the standard
for production. Traffic attaches via **port groups** (for VMs) and **VMkernel adapters** (for host
traffic: management, vMotion, vSAN, storage), each optionally tagged with a **VLAN**. **NIC teaming**
binds multiple physical uplinks for redundancy and load distribution, with **failover policies**
(active/standby, load-balancing method). Separating traffic types (management/vMotion/vSAN) onto
different VLANs/uplinks is a core design practice. Networking is what makes VMs reachable and the
cluster's features (vMotion, vSAN) work.

## Design Considerations

Use a **vDS** in production for consistency and features; reserve the **vSS** for tiny/edge cases.
Separate **traffic types** (management, vMotion, vSAN, VM) by VLAN and, ideally, uplinks. **Team**
NICs for redundancy with an appropriate load-balancing policy. Enable **Network I/O Control** to
protect critical traffic. Plan VLANs before deploying.

## Implementation and Automation

The labs inspect a standard switch, create a distributed switch and port group, and configure a
VMkernel adapter — with PowerCLI/esxcli.

## Validation and Troubleshooting

Confirm the networking model:

```text
vSS (per host) vs vDS (vCenter-wide, consistent, advanced features) -> use vDS in production.
Port groups (VMs) + VMkernel adapters (mgmt/vMotion/vSAN/storage) + VLAN tags.
NIC teaming (redundancy + load balancing) + failover policy. Separate traffic types.
```

Common pitfalls: managing many hosts with **per-host vSS** (drift); and mixing all traffic on **one
VLAN/uplink** (no isolation/redundancy).

## Security and Best Practices

Prefer the **vDS**, **separate** traffic types, **team** uplinks, and enable **Network I/O Control**.
Isolate management. Apply security policies (reject promiscuous/MAC changes/forged transmits) on
port groups. Consistent, redundant networking underpins the whole platform.

## Hands-On Lab

Networking walkthroughs. **Shared prerequisites** — vCenter 7 with hosts and free uplinks, PowerCLI,
in a lab. **Cost:** none.

### Lab 5.1 — Inspect standard switch networking

**Objective:** Review a host's vSS.

```bash
esxcli network vswitch standard list
esxcli network vswitch standard portgroup list
```

**Expected result:** the host's **standard switch** and port groups — the per-host networking view.

**Negative test:** manage a large cluster with per-host **vSS** and expect consistency; drift is
inevitable — move to a **vDS**.

**Cleanup:** none (read-only).

### Lab 5.2 — Create a distributed switch and port group

**Objective:** Build vCenter-wide networking.

```powershell
$vds = New-VDSwitch -Name "vds-prod" -Location (Get-Datacenter DC1) -NumUplinkPorts 2
New-VDPortgroup -VDSwitch $vds -Name "app-vlan100" -VlanId 100
Get-VDPortgroup -VDSwitch $vds
```

**Expected result:** a **vDS** with a VLAN-100 port group, managed centrally — consistent networking
across hosts.

**Negative test:** create the same port group on each host's vSS; a **vDS** defines it once for all —
use it.

**Cleanup:** `Remove-VDSwitch vds-prod -Confirm:$false`.

### Lab 5.3 — Add a VMkernel adapter for vMotion

**Objective:** Dedicate a network to host traffic.

```powershell
$h = (Get-VMHost)[0]
New-VMHostNetworkAdapter -VMHost $h -PortGroup "vmotion" -VirtualSwitch (Get-VDSwitch vds-prod) `
  -IP 10.0.50.11 -SubnetMask 255.255.255.0 -VMotionEnabled $true
Get-VMHostNetworkAdapter -VMHost $h -VMKernel | Select Name, IP, VMotionEnabled
```

**Expected result:** a **VMkernel adapter** with **vMotion enabled** on its own network — separated
host traffic.

**Negative test:** run vMotion on the management VMkernel with no separation; **dedicate** a
VMkernel/VLAN to vMotion for performance and isolation.

**Cleanup:** remove the VMkernel adapter.

### Lab 5.4 — NIC teaming and failover

**Objective:** Configure uplink redundancy.

```powershell
Get-VDPortgroup -VDSwitch (Get-VDSwitch vds-prod) -Name "app-vlan100" |
  Get-VDUplinkTeamingPolicy | Set-VDUplinkTeamingPolicy -LoadBalancingPolicy LoadBalanceLoadBased `
  -ActiveUplinkPort "dvUplink1","dvUplink2"
```

**Expected result:** **NIC teaming** with two active uplinks and a load-based policy — redundant,
balanced networking.

**Negative test:** run a port group on a **single uplink**; a NIC/switch failure drops the network —
**team** the uplinks.

**Cleanup:** revert the teaming policy.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere networking spans per-host standard switches and vCenter-wide distributed switches (preferred
in production), with port groups and VLAN-tagged VMkernel adapters, NIC teaming for redundancy, and
traffic separation by type. Use a vDS, separate traffic, team uplinks, and enable Network I/O
Control.

- [ ] I can inspect standard-switch networking.
- [ ] I can create a vDS and port group.
- [ ] I can add a vMotion VMkernel adapter.
- [ ] I can configure NIC teaming/failover.
- [ ] I completed Labs 5.1–5.4 including each negative test.
