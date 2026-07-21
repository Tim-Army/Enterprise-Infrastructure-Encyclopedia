# Chapter 4: vSphere Virtual Networking

![Lab topology for this chapter: dvs-lab spans esxi-lab-01 and esxi-lab-02, each contributing two uplinks bundled into an Active LACP LAG (lag-lab); a VST-tagged port group (pg-lab-test, VLAN 150) hosts a test VM, NIOC shares favor vMotion traffic during contention, and vmkping at 8972 bytes confirms end-to-end MTU 9000. As a negative test, one physical uplink is disabled while the test VM has active traffic: the LAG shows that uplink as no longer bundled while the surviving uplink keeps carrying traffic with no sustained loss, and the failed uplink automatically rejoins the LAG once restored.](../../../diagrams/volume-05-vmware-virtualization/chapter-04-vds-lacp-uplink-failure-topology.svg)

*Figure 4-1. Topology used throughout this chapter's Hands-On Lab: a distributed switch with an LACP link aggregation group, tested against a live uplink failure.*

## Learning Objectives

- Compare the standard vSwitch (VSS) and distributed vSwitch (VDS)
  architectures and select correctly between them.
- Explain port groups, VLAN tagging modes (EST, VST, VGT), and NIC teaming
  and failover policy.
- Configure Link Aggregation Control Protocol (LACP) Link Aggregation
  Groups (LAGs) on a distributed switch.
- Explain Network I/O Control (NIOC) version 3 and configure bandwidth
  allocation shares/reservations/limits by traffic type.
- Explain private VLANs (PVLANs) and when they solve a segmentation
  problem VLANs alone cannot.
- Create and use custom VMkernel TCP/IP stacks to isolate traffic types at
  the routing/gateway level, not just the VLAN level.
- Diagnose common virtual-networking failures using `esxcli`, `net-stats`,
  and `pktcap-uw`.
- Apply port-level security settings (promiscuous mode, MAC address
  changes, forged transmits) correctly.

## Theory and Architecture

Every VM's network connectivity, every VMkernel service (management,
vMotion, storage, vSAN), and every NSX-prepared host's overlay traffic all
pass through vSphere's virtual networking layer before reaching a physical
NIC. This chapter covers that layer as it exists independent of NSX;
Chapters 10 and 11 cover how NSX extends (and, on current VDS-integrated
NSX deployments, directly uses) this same switching infrastructure for
overlay networking.

### Standard vSwitch versus distributed vSwitch

| Characteristic | Standard vSwitch (VSS) | Distributed vSwitch (VDS) |
| --- | --- | --- |
| Configuration scope | Per-host, configured independently on each host | Centralized at vCenter Server, pushed consistently to every member host |
| Port group consistency | Must be manually kept identical across hosts | Enforced centrally; a distributed port group is defined once |
| Advanced features | Basic NIC teaming, VLAN tagging, traffic shaping (egress only) | LACP LAGs, NIOC, Port Mirroring, NetFlow, ingress and egress traffic shaping, Network Health Check |
| vCenter dependency | None — a VSS is fully functional even with vCenter Server unavailable | Configuration changes require vCenter Server; a VDS's data plane (the per-host hidden proxy switch) continues forwarding traffic if vCenter is unavailable, but cannot be reconfigured until it returns |
| Licensing | Included at every vSphere edition | Requires an edition/license tier that includes VDS (bundled with vSAN and NSX entitlements at current licensing) |
| Typical use | Small environments, initial host bring-up before vCenter exists, edge/ROBO simplicity | Standard choice for any cluster of meaningful size, and a prerequisite for NSX host preparation |

A **standard vSwitch** is configured independently on each ESXi host —
functionally equivalent, entity-by-entity, to a small Layer 2 switch
living entirely inside that one host's VMkernel. It has no dependency on
vCenter Server (useful during initial host bring-up, before the host has
even joined a vCenter Server inventory) but must be manually kept
consistent across hosts in a cluster — a real operational burden and
common source of drift (a port group present on three hosts in a cluster
but missing on a fourth, breaking vMotion or causing intermittent VM
placement failures) at any scale beyond a handful of hosts.

A **distributed vSwitch** decouples configuration from any single host:
the VDS object itself, and its port groups, are defined once at vCenter
Server and pushed consistently to every host added as a VDS member. Under
the hood, each member host still runs a local, hidden **host proxy
switch** that does the actual per-host packet forwarding — a VDS's control
plane lives at vCenter Server, but its data plane is fully distributed and
does not depend on vCenter Server being reachable for already-configured
traffic to keep flowing; only *changes* to that configuration require
vCenter Server availability.

### Port groups and VLAN tagging modes

A **port group** (standard vSwitch) or **distributed port group** (VDS) is
the policy object a VM's virtual NIC or a VMkernel adapter actually
connects to — carrying VLAN configuration, security policy, teaming and
failover policy, and (on a VDS) traffic shaping and NIOC association.
Three VLAN tagging modes exist:

- **External Switch Tagging (EST)** — the port group carries no VLAN tag
  at all (VLAN ID 0); the physical switch port is configured as an access
  port for a single VLAN, and tagging happens entirely outside the ESXi
  host. Simple, but every VLAN needs its own port group and its own
  dedicated physical access port configuration.
- **Virtual Switch Tagging (VST)** — the standard modern default: the
  port group is assigned a specific VLAN ID, the physical switch port
  is configured as an 802.1Q trunk carrying that VLAN (among others), and
  the vSwitch itself applies/strips the VLAN tag on the way in/out. Most
  vSphere networking in production uses VST.
- **Virtual Guest Tagging (VGT)** — the port group is set to VLAN ID 4095
  (a reserved value meaning "pass all tags through"), and the *guest
  OS inside the VM* applies its own 802.1Q tags. This is the correct
  (and only) mode for a VM that itself needs to see and route between
  multiple VLANs (a virtual router or firewall appliance, for instance)
  — but it also means the guest OS has direct control over VLAN tagging,
  which is a security-relevant capability that should not be granted to
  ordinary application VMs.

### NIC teaming and failover policy

A port group's **teaming and failover policy** determines how traffic is
distributed and failed over across the port group's configured uplinks:

- **Load balancing method** — options include **Route based on originating
  virtual port** (the traditional VSS/VDS default, deterministic per-VM-NIC
  uplink assignment, no physical switch configuration required),
  **Route based on IP hash** (requires a matching static EtherChannel on
  the physical switch, not LACP — a common point of confusion), **Route
  based on physical NIC load** (VDS-only, dynamically rebalances based on
  measured uplink utilization), and **Route based on LACP hash** used when
  the port group is actually connected to a LACP LAG.
- **Network failure detection** — link status only (fastest, but blind to
  upstream failures beyond the directly connected switch port) versus
  beacon probing (VSS-only, detects some additional failure classes at
  the cost of added complexity and known edge-case limitations — VMware
  guidance has long favored link status plus properly designed physical
  redundancy over beacon probing for most environments).
- **Failback** — whether a restored uplink automatically resumes active
  use (`Yes`, the default) or requires manual re-activation (`No`, useful
  where a flapping link would otherwise repeatedly move traffic back onto
  an unstable path).

### LACP Link Aggregation Groups

**LACP LAGs** are a VDS-only feature: multiple physical uplinks are bonded
into a single logical channel using the IEEE 802.3ad/802.1AX LACP
protocol, dynamically negotiated with a matching LAG configuration on the
physical switch (as opposed to the static EtherChannel that IP-hash-based
teaming without LACP requires). A VDS supports both **single a LAG**
spanning multiple uplinks used by the port groups that select it as their
active uplink set, and — where the switch topology supports it —
**multiple LAGs** across different uplink groups, though most designs use
one LAG per host uplink pair/set. LACP LAGs and simple static
NIC-teaming-based uplink assignment are mutually exclusive configurations
per port group: a port group uses either a LAG or the standard teaming
policy, not both simultaneously.

### Network I/O Control (NIOC) v3

**NIOC** governs bandwidth allocation across the different traffic types
that share physical uplinks on a VDS — management, vMotion, vSAN, NFS/
iSCSI storage, Fault Tolerance logging, vSphere Replication, and virtual
machine traffic each get an independent NIOC **network resource pool**,
configured with:

- **Shares** — a relative weight determining allocation *only when
  contention exists* (no traffic type is ever throttled below its share
  during periods of available bandwidth).
- **Reservation** — a guaranteed minimum bandwidth, admission-controlled
  against total physical uplink capacity (over-reserving beyond available
  capacity is rejected at configuration time, not silently
  under-delivered at runtime).
- **Limit** — a hard ceiling, rarely used in practice since it caps a
  traffic type even when bandwidth is otherwise idle.

NIOC v3's practical value is preventing one traffic type (a vMotion storm
during a maintenance window, for instance) from starving another (VM
production traffic) on shared uplinks, without requiring dedicated
physical NICs per traffic type in environments where that level of
physical separation is not cost-justified.

### Private VLANs (PVLANs)

A **PVLAN** subdivides a single "primary" VLAN into secondary VLANs with
three port types: **Promiscuous** (can communicate with everything in the
primary VLAN — typically a router/gateway port), **Isolated** (can
communicate only with promiscuous ports, never with other isolated ports
even within the same secondary VLAN), and **Community** (can communicate
with other ports in the same community secondary VLAN, plus promiscuous
ports, but not with isolated ports or other communities). PVLANs solve a
specific problem plain VLANs cannot solve alone: preventing lateral
communication between VMs that must all reach a shared gateway but must
never talk directly to each other (a multi-tenant DMZ segment, for
instance) without provisioning a separate VLAN — and the accompanying
physical switch configuration and IP subnet — for every such VM or small
group. PVLAN configuration requires matching support and configuration on
the physical switch, not just the VDS side, since secondary VLAN IDs must
be consistently understood end-to-end.

### Custom VMkernel TCP/IP stacks

Beyond the **default TCP/IP stack**, ESXi ships dedicated stacks for
**vMotion** and **provisioning** traffic, and supports creating **custom
TCP/IP stacks** for other traffic types. A dedicated stack carries its own
routing table, default gateway, and DNS configuration, independent of the
default stack — meaning vMotion traffic, for example, can be routed
through a completely different gateway than management traffic without
requiring source-based routing tricks on the default stack. This matters
most in designs where vMotion, storage, or backup traffic must traverse a
different Layer 3 path than management traffic, or where isolating a
traffic type's routing table is a deliberate security/segmentation
control rather than only a VLAN-level separation.

## Design Considerations

- **VSS versus VDS by cluster maturity, not just size.** A single lab host
  or a host bootstrapping before vCenter exists is a legitimate VSS use
  case; any cluster expected to grow, host vMotion-eligible workloads
  consistently, or eventually host NSX-prepared transport nodes should
  standardize on VDS from the start — retrofitting a running cluster from
  VSS to VDS is a supported but nontrivial migration best avoided by
  choosing correctly at initial build.
- **Load-balancing method against actual physical switch capability.**
  Route based on IP hash requires a static EtherChannel and will silently
  misbehave (intermittent connectivity, MAC flapping warnings) if paired
  with a physical switch side actually configured for LACP, or left
  unconfigured; LACP LAGs require the inverse. Confirm the physical
  network team's actual switch-side configuration before selecting a VDS
  load-balancing method — this is a cross-team dependency, not a
  vSphere-only decision.
- **NIOC reservations against real contention scenarios.** Reservations
  should reflect genuine minimum requirements under worst-case contention
  (a host performing simultaneous vMotion evacuation and normal VM traffic
  during a failure/maintenance event), not aspirational full-bandwidth
  guarantees for every traffic type simultaneously, which cannot all be
  satisfied at once by definition.
- **VGT scope discipline.** Grant VGT only to the specific VMs that
  genuinely require guest-controlled tagging (virtual routers/firewalls);
  applying VGT broadly as a convenience to avoid managing multiple VST
  port groups meaningfully expands what a compromised or misconfigured
  guest OS can do at the network layer.
- **PVLAN physical switch dependency.** Do not design a PVLAN segmentation
  strategy without first confirming the physical switch vendor/platform
  supports PVLANs and that the network team is prepared to configure and
  maintain matching secondary VLAN mappings — a PVLAN design that only
  the VDS side understands does not function correctly end-to-end.
- **Custom TCP/IP stack complexity trade-off.** Dedicated stacks solve a
  real routing-isolation problem but add operational surface (each stack
  needs its own gateway/DNS configuration, tracked and documented
  separately); use them where a genuine Layer 3 isolation requirement
  exists, not reflexively for every traffic type.
- **Jumbo frame consistency across the entire path.** As with vSAN
  ([Chapter 6](06-vsphere-storage-and-vsan.md)), any traffic type relying on jumbo frames (vMotion, storage,
  vSAN) requires MTU 9000 configured consistently on the VMkernel adapter,
  the port group/VDS, and every physical switch port in the path — this is
  a virtual-networking design decision with a hard physical-network
  dependency, not something the VDS side can guarantee alone.

## Implementation and Automation

### Creating a distributed switch and adding hosts

```powershell
# PowerCLI: create a VDS and add cluster hosts as members with two uplinks each
$dc = Get-Datacenter -Name "corp-dc"
$vds = New-VDSwitch -Name "dvs-cluster-a" -Location $dc -NumUplinkPorts 2 -Mtu 9000

$cluster = Get-Cluster -Name "prod-cluster-a"
foreach ($vmhost in (Get-VMHost -Location $cluster)) {
  Add-VDSwitchVMHost -VDSwitch $vds -VMHost $vmhost
  $nics = Get-VMHostNetworkAdapter -VMHost $vmhost -Physical -Name "vmnic0", "vmnic1"
  Add-VDSwitchPhysicalNetworkAdapter -VMHostNetworkAdapter $nics -DistributedSwitch $vds -Confirm:$false
}
```

### Creating VST distributed port groups

```powershell
# PowerCLI: create tagged (VST) distributed port groups for VM and management traffic
New-VDPortgroup -VDSwitch $vds -Name "pg-vm-app-tier" -VlanId 120
New-VDPortgroup -VDSwitch $vds -Name "pg-management" -VlanId 10
```

### Configuring an LACP LAG

```powershell
# PowerCLI: create an LACP LAG on the VDS and assign it as the active uplink for a port group
$lag = New-VDSwitchLACPGroup -VDSwitch $vds -Name "lag-primary" -Mode Active -LoadBalancingMode "SourceAndDestIPPort"

$pg = Get-VDPortgroup -VDSwitch $vds -Name "pg-vm-app-tier"
$pg | Get-VDUplinkTeamingPolicy | Set-VDUplinkTeamingPolicy -EnableLoadBalancing $true -LoadBalancingPolicy "LoadBalanceLoadBased"
```

```bash
# esxcli: confirm LACP negotiation status per host
esxcli network vswitch dvs vmware lacp status get
```

### Configuring NIOC shares and reservations

```powershell
# PowerCLI: set NIOC shares/reservation for vMotion and VM traffic network resource pools
Get-VDSwitch -Name "dvs-cluster-a" | Get-NetworkResourcePool -Name "vMotion Traffic" |
  Set-NetworkResourcePool -SharesLevel High -ReservationMbit 2000

Get-VDSwitch -Name "dvs-cluster-a" | Get-NetworkResourcePool -Name "Virtual Machine Traffic" |
  Set-NetworkResourcePool -SharesLevel Normal
```

### Creating a PVLAN

```powershell
# PowerCLI: define primary and secondary PVLAN entries, then apply to a port group
$vds = Get-VDSwitch -Name "dvs-cluster-a"
New-VDSwitchPrivateVlan -VDSwitch $vds -PrimaryVlanId 200 -PrimaryVlanType Promiscuous
New-VDSwitchPrivateVlan -VDSwitch $vds -PrimaryVlanId 200 -SecondaryVlanId 201 -SecondaryVlanType Isolated

$pg = New-VDPortgroup -VDSwitch $vds -Name "pg-dmz-isolated" -PrivateVlanId 201
```

### Creating a custom VMkernel TCP/IP stack

```bash
# esxcli: create a custom TCP/IP stack for backup traffic with its own routing table
esxcli network ip netstack add -N backup-stack

esxcli network ip interface add -i vmk3 -p pg-backup -N backup-stack
esxcli network ip interface ipv4 set -i vmk3 -N backup-stack \
  -I 10.10.40.11 -N 255.255.255.0 -t static

esxcli network ip route ipv4 add -N backup-stack -n default -g 10.10.40.1
```

### Applying port-level security settings

```powershell
# PowerCLI: enforce reject on promiscuous mode, MAC changes, and forged transmits
Get-VDPortgroup -Name "pg-vm-app-tier" | Get-VDSecurityPolicy |
  Set-VDSecurityPolicy -AllowPromiscuous $false -ForgedTransmits $false -MacChanges $false
```

## Validation and Troubleshooting

- **Uplink and teaming state.** `esxcli network vswitch dvs vmware
  lacp status get` (LACP) and `esxcli network nic list` confirm physical
  link/negotiated speed; a port group showing intermittent connectivity
  with IP-hash load balancing selected almost always traces to a physical
  switch side not actually configured with a matching static EtherChannel
  — verify the physical configuration before assuming a vSphere-side
  fault.
- **VLAN tagging mismatches.** A VM unable to reach expected peers despite
  correct IP configuration should prompt checking the port group's VLAN
  ID against the physical switch trunk's allowed-VLAN list first — a VLAN
  present on the port group but pruned from the trunk on the physical
  switch produces exactly this symptom and is not diagnosable from the
  ESXi side alone.
- **MTU path validation.** As with vSAN traffic, `vmkping -I <vmkernel
  adapter> -d -s 8972 <destination>` is the standard end-to-end jumbo-frame
  validation test; a failure with a smaller payload size succeeding
  isolates an MTU mismatch to a specific segment of the path.
- **Packet capture with pktcap-uw.** `pktcap-uw` captures traffic at
  specific points in the ESXi virtual networking stack (a VM's vNIC, a
  VMkernel port, an uplink, or a specific vSwitch/VDS port), which is
  substantially more precise for isolating whether a packet is being
  dropped at ingress, at a firewall rule, or never leaving the originating
  vNIC than a physical-switch-side capture alone can determine.

  ```bash
  # pktcap-uw: capture traffic on a specific VM's vNIC (identify the switch port with --uplink or vsish first)
  pktcap-uw --vmk vmk0 --dir 2 -o /tmp/capture-vmk0.pcap
  ```

- **Throughput/statistics review.** `esxtop` in network mode (`n`) and
  `net-stats -A -t vW` report per-vNIC/per-uplink throughput, dropped
  packet counts, and (on a VDS) NIOC-reserved-versus-consumed bandwidth,
  useful for confirming whether a perceived performance issue is an
  actual bandwidth/drop condition versus a guest-OS-level symptom.
- **VDS configuration push failures.** A configuration change that
  succeeds at vCenter Server but does not take effect on a specific host
  typically indicates that host lost connectivity to vCenter Server during
  the push; `vSphere Client > select VDS > Configure > Topology` and the
  per-host network configuration status will show the specific host as
  out of sync, and a proxy-switch resync (host reconnect, or `Update
  Network Resource Pool` retry) resolves it once connectivity is restored.

## Security and Best Practices

- Set port-group security policy to reject promiscuous mode, MAC address
  changes, and forged transmits by default at every port group, enabling
  exceptions only for the specific VMs that have a legitimate requirement
  (a nested-hypervisor lab VM, a network monitoring appliance needing
  promiscuous capture) and documenting why.
- Restrict VGT to the specific VMs that require guest-controlled VLAN
  tagging; treat a broad VGT grant as an elevated-trust configuration
  requiring the same review rigor as a firewall rule change.
- Segment management, vMotion, storage, vSAN, and general VM traffic onto
  distinct VLANs (and, where NIOC reservations alone are not considered
  sufficient isolation, distinct physical uplinks) — do not rely on VLAN
  separation alone without NIOC protecting shared uplinks from
  traffic-type starvation during contention.
- Use PVLANs where lateral communication between same-segment VMs must be
  prevented without provisioning a full separate VLAN/subnet per
  isolation boundary, and confirm the physical switch side is correctly
  configured to match before relying on it as a control.
- Prefer VDS over VSS for any environment where centrally auditable,
  consistent network policy across hosts is a security requirement — VSS's
  per-host independent configuration is inherently harder to audit for
  drift at scale.
- Apply the principle of least routing exposure to custom TCP/IP stacks:
  a dedicated stack for backup or storage traffic should not have a
  default gateway route to networks it does not need to reach.

## References and Knowledge Checks

**References**

- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *vSphere Networking* (standard and
  distributed switches, port groups, VLAN tagging modes, NIC teaming).
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *Network I/O Control*.
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *Private VLANs* and *Custom TCP/IP
  Stacks*.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline referenced throughout this volume.
- See [Chapter 6](06-vsphere-storage-and-vsan.md) for the vSAN-specific VMkernel networking requirements
  that build on the concepts in this chapter.
- See Chapters 10 and 11 for how NSX host preparation extends this same
  VDS infrastructure for overlay networking.

**Knowledge checks**

1. What continues to function on a VDS-connected host if vCenter Server
   becomes unreachable, and what stops functioning?
2. Why must Route based on IP hash never be paired with a physical switch
   side configured for LACP (as opposed to a static EtherChannel)?
3. Explain the specific lateral-communication problem PVLANs solve that
   VLANs alone cannot, using the Isolated port type.
4. Why does VGT represent an elevated-trust configuration compared to
   VST, from a guest-OS-capability standpoint?
5. Give a concrete scenario where a custom VMkernel TCP/IP stack is
   necessary rather than merely convenient.

## Hands-On Lab

**Objective:** Build a distributed switch, add hosts, create VST port
groups, configure an LACP LAG, apply NIOC shares, and validate teaming
behavior including a deliberate uplink failure.

**Prerequisites**

- A vSphere 9.x lab with at least 2 ESXi hosts (nested is acceptable) in
  one cluster, each with at least two unused physical (or nested virtual)
  uplinks not already claimed by another vSwitch.
- A lab physical/virtual switch upstream capable of LACP configuration for
  the LAG portion of the exercise (a nested lab using a virtual switch
  supporting LACP passthrough, or a physical lab switch port group,
  either is acceptable).
- PowerCLI connected to the lab vCenter with networking-modify privileges.

**Steps**

1. Create the VDS and add both hosts with one uplink each initially:

   ```powershell
   Connect-VIServer -Server vcenter-lab.local
   $dc = Get-Datacenter -Name "lab-dc"
   $vds = New-VDSwitch -Name "dvs-lab" -Location $dc -NumUplinkPorts 2 -Mtu 9000
   foreach ($vmhost in (Get-VMHost -Location (Get-Cluster -Name "lab-cluster"))) {
     Add-VDSwitchVMHost -VDSwitch $vds -VMHost $vmhost
     Add-VDSwitchPhysicalNetworkAdapter -VMHostNetworkAdapter (Get-VMHostNetworkAdapter -VMHost $vmhost -Name "vmnic1") -DistributedSwitch $vds -Confirm:$false
   }
   ```

   **Expected result:** both hosts appear as VDS members under `vSphere
   Client > Networking > dvs-lab > Hosts`.

2. Create a VST-tagged port group and deploy a small test VM onto it:

   ```powershell
   New-VDPortgroup -VDSwitch $vds -Name "pg-lab-test" -VlanId 150
   ```

   **Expected result:** the test VM's vNIC connects successfully and
   obtains/uses an IP address on the lab VLAN 150 subnet.

3. Add the second uplink from each host, then create and assign an LACP
   LAG:

   ```powershell
   foreach ($vmhost in (Get-VMHost -Location (Get-Cluster -Name "lab-cluster"))) {
     Add-VDSwitchPhysicalNetworkAdapter -VMHostNetworkAdapter (Get-VMHostNetworkAdapter -VMHost $vmhost -Name "vmnic2") -DistributedSwitch $vds -Confirm:$false
   }
   $lag = New-VDSwitchLACPGroup -VDSwitch $vds -Name "lag-lab" -Mode Active
   ```

   **Expected result:** `esxcli network vswitch dvs vmware lacp status
   get` on each host reports the LAG as `bundled` once the upstream switch
   side is configured to match.

4. Apply NIOC shares favoring vMotion traffic during contention:

   ```powershell
   Get-VDSwitch -Name "dvs-lab" | Get-NetworkResourcePool -Name "vMotion Traffic" |
     Set-NetworkResourcePool -SharesLevel High
   ```

   **Expected result:** the network resource pool shows the updated
   shares value under `vSphere Client > dvs-lab > Configure > Resource
   Allocation`.

5. Validate MTU consistency for the jumbo-frame-enabled VDS:

   ```bash
   vmkping -I vmk0 -d -s 8972 <PEER_HOST_VMKERNEL_IP>
   ```

   **Expected result:** the ping succeeds at the full jumbo-frame payload
   size, confirming MTU 9000 end-to-end.

6. **Negative test:** simulate an uplink failure by disabling one physical
   uplink's link (or administratively shutting the corresponding physical
   switch port) while the test VM has active traffic flowing:

   **Expected result:** the test VM's connectivity briefly pauses (or
   shows no interruption at all if the LAG is correctly negotiated and
   the remaining member link absorbs traffic) and resumes/continues on
   the surviving uplink; `esxcli network vswitch dvs vmware lacp status
   get` shows the failed uplink as no longer bundled while the healthy
   uplink remains active. Confirm no sustained packet loss beyond the
   brief convergence window.

7. Restore the failed uplink and confirm it rejoins the LAG:

   **Expected result:** the uplink returns to `bundled` status without
   manual intervention (LACP renegotiates automatically).

8. **Cleanup:** remove the test VM, remove the LAG assignment and port
   group, and remove the hosts from the VDS if the VDS was created solely
   for this lab.

   ```powershell
   Get-VM -Name "lab-test-vm" | Remove-VM -DeletePermanently -Confirm:$false
   Get-VDPortgroup -Name "pg-lab-test" | Remove-VDPortgroup -Confirm:$false
   Get-VDSwitch -Name "dvs-lab" | Remove-VDSwitch -Confirm:$false
   ```

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

vSphere virtual networking centers on the choice between standard and
distributed vSwitches, with VDS the standard choice for any cluster beyond
minimal scale due to its centralized configuration, LACP LAG support, and
Network I/O Control. Port groups carry VLAN tagging (EST, VST, or the
elevated-trust VGT mode), teaming/failover policy, and security settings
that must be correctly matched against actual physical switch
configuration — a cross-team dependency, not a purely virtual one. NIOC
protects shared uplinks from traffic-type starvation under contention,
PVLANs solve lateral-communication isolation problems VLANs alone cannot,
and custom TCP/IP stacks provide Layer 3 routing isolation for traffic
types that need it. This same VDS infrastructure is what NSX host
preparation builds directly on top of in Chapters 10 and 11.

- [ ] Can select correctly between VSS and VDS for a given environment.
- [ ] Can configure VST port groups and explain when VGT is genuinely
      required.
- [ ] Can configure an LACP LAG and match it to correct physical switch
      configuration.
- [ ] Can configure NIOC shares/reservations to protect critical traffic
      types under contention.
- [ ] Can explain PVLAN port types and the specific isolation problem
      they solve.
- [ ] Can create and justify use of a custom VMkernel TCP/IP stack.
- [ ] Completed the hands-on lab, including the LACP uplink-failure
      negative test and full cleanup.
