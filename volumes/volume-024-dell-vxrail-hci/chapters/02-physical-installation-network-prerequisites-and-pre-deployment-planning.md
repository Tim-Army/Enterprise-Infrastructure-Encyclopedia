# Chapter 02: Physical Installation, Network Prerequisites, and Pre-Deployment Planning

## Learning Objectives

- Enumerate the networks a VxRail cluster requires and explain what each
  carries.
- Explain why VxRail node discovery depends on IPv6 multicast and what
  breaks when the switch does not carry it.
- Configure top-of-rack switching to VxRail's requirements, including
  VLAN tagging, MTU, and spanning-tree behavior on node-facing ports.
- Prepare DNS, NTP, and IP address allocations correctly before
  deployment rather than during it.
- Complete a pre-deployment planning record that the deployment wizard
  can be driven from without further decisions.

## Theory and Architecture

### Why this chapter comes before deployment

VxRail's first-run deployment is a single, largely unattended workflow.
It succeeds quickly when its prerequisites are met and fails in ways that
are tedious to unwind when they are not. Almost every difficult VxRail
deployment traces back to something in this chapter — a VLAN that does
not carry IPv6 multicast, a DNS record that resolves forward but not
reverse, an MTU mismatch between the node and the switch.

The material here is unglamorous and it is where deployment engagements
are actually won or lost. It is also weighted heavily in the Deploy exam,
which reflects field reality rather than an examiner's preference.

### The networks a VxRail cluster requires

A VxRail cluster carries several logically distinct networks. They may
share physical uplinks, but they are separate VLANs with separate
purposes:

| Network | Carries | Notes |
| --- | --- | --- |
| External management | ESXi management, vCenter, VxRail Manager | Routable; reaches the rest of the estate |
| Internal management (discovery) | Node discovery between VxRail Manager and unconfigured nodes | Non-routable, IPv6 multicast, VLAN 3939 by default |
| vSAN | Distributed storage traffic between nodes | Non-routable within a standard cluster; highest bandwidth demand |
| vMotion | Live migration | Non-routable within a standard cluster |
| Guest / VM networks | Workload traffic | As many as the workloads require |

Two of these deserve individual attention because they behave differently
from the equivalent networks on a self-built vSphere cluster.

### Internal management and IPv6 multicast

This is the single most common VxRail deployment blocker, and it has no
equivalent in a build-your-own cluster.

An unconfigured VxRail node has no IP address you assigned and no
configuration you supplied. VxRail Manager finds such nodes by
advertisement: nodes announce themselves on the internal management VLAN
using multicast DNS over IPv6 link-local addressing, and VxRail Manager
listens for those announcements.

The consequence is concrete. **If the top-of-rack switches do not carry
IPv6 multicast on the internal management VLAN, VxRail Manager will not
see the nodes at all** — not partially, not slowly, not at all. The
deployment wizard will report that it found fewer nodes than expected, or
none, and the fault is in the fabric rather than in the nodes.

The default VLAN for this traffic is **3939**. It is non-routable by
design; discovery only ever needs to work within the rack, and giving it
a routed path serves no purpose while widening the management surface.

Where MLD snooping is enabled on the switches, an MLD querier must exist
for the VLAN, or snooping will prune the very traffic discovery depends
on. This is the specific failure mode that produces an intermittent,
maddening "some nodes appear and some do not" symptom.

### vSAN traffic and MTU

vSAN carries every write the cluster performs across the network, and it
is the network whose misconfiguration is felt as a performance problem
rather than as an outage — which makes it harder to diagnose later.

Jumbo frames (MTU 9000) are recommended for vSAN and vMotion, and the
requirement is **end to end**: the VMkernel adapter, the distributed
switch uplink, the physical switch port, and every switch in the path
between nodes must agree. A path where one hop is at 1500 does not fail
cleanly; it fragments or drops, and the symptom is degraded throughput
under load rather than a failed ping.

Two practical rules follow. Configure MTU consistently before deployment
rather than changing it afterwards, and test it with a
do-not-fragment ping at full payload size rather than assuming it — the
command is in *Validation and Troubleshooting* below.

### Switch configuration on node-facing ports

VxRail node-facing switch ports need three things beyond correct VLANs.

**Portfast or edge-port behavior.** Node ports connect to hypervisors,
not to switches. Leaving standard spanning-tree convergence on those
ports delays link-up by tens of seconds, which is long enough to fail
deployment steps and long enough to cause avoidable disruption during
node reboots in normal operation. Configure them as edge ports with BPDU
guard.

**Correct tagging.** The conventional layout is ESXi management untagged
(native VLAN) with vSAN, vMotion, and internal management tagged. VxRail
also supports a tagged management VLAN, but the choice must be made
before deployment and matched on both the switch and the wizard.

**Link aggregation, carefully.** Standard VxRail deployments do not
require LACP and are commonly deployed without it. Where LACP is used it
must be configured in a way the distributed switch's uplink teaming
agrees with, and misaligned LACP is a reliable way to produce a cluster
that half-works.

### DNS and NTP

VxRail requires **forward and reverse DNS records to exist before
deployment** for every ESXi host, for VxRail Manager, and for vCenter
where vCenter is VxRail-managed. Not one of these is optional and the
reverse records are the ones most often forgotten.

The reason reverse matters is that certificate generation and several
internal component registrations resolve by PTR. A deployment where
forward resolution works and reverse does not will proceed some distance
and then fail in a place that gives no hint about DNS.

NTP is equally non-negotiable. A cluster whose nodes disagree about time
produces certificate validation failures and inconsistent logging, and
the failures do not name time as the cause. Supply a reachable NTP source
and confirm it resolves and responds before deployment begins, not
during.

### Node minimums and cluster types

The number of nodes available constrains which cluster types are
possible:

| Cluster type | Node count | Notes |
| --- | --- | --- |
| Standard cluster | Three or more | The normal deployment; availability policy sets the practical floor higher than three for many workloads |
| Two-node cluster | Two, plus an external witness | For small sites; the witness must be hosted somewhere that is not either node |
| Satellite node | One | A single node managed by an existing VxRail cluster's vCenter, for edge sites; no local vSAN cluster |
| Dynamic node cluster | Compute nodes with no local vSAN capacity | Storage supplied externally rather than by local drives |

**Dynamic nodes deserve a specific note** because they contradict the HCI
premise. A dynamic-node cluster is VxRail's answer to the coupled-scaling
constraint from [Chapter 01](01-hci-architecture-vxrail-positioning-and-platform-models.md):
the nodes carry compute but not storage capacity, and storage arrives
from an external array or from another vSAN cluster. It buys back
independent scaling at the cost of reintroducing the external storage
layer HCI set out to remove. That is a legitimate trade for
compute-heavy estates that already own array capacity, and a poor one for
a greenfield site that chose HCI to be rid of the array.

## Design Considerations

- **Decide tagged versus untagged management before the switch is
  configured.** Changing it after deployment means reconfiguring the
  management VMkernel on every host, which is disruptive and easy to do
  incorrectly.
- **Allocate contiguous IP ranges per network, with headroom.** The
  deployment wizard consumes ranges rather than individual addresses for
  ESXi, vSAN, and vMotion. Allocating exactly the number of nodes you
  have today makes the next expansion harder than it needs to be.
- **Place the two-node witness where it does not share fate with either
  node.** A witness hosted on one of the two nodes it arbitrates is not a
  witness. A witness at a site whose link failure also partitions the
  cluster is only marginally better.
- **Confirm the switch actually supports what the design assumes.** IPv6
  multicast, MLD querier behavior, jumbo frames at the required scale,
  and port count for both node uplinks and any out-of-band management
  ports are worth verifying against the specific switch model rather than
  the vendor category.
- **Plan iDRAC connectivity alongside cluster networking.** Each node
  has an iDRAC that will be needed during troubleshooting, exactly as
  [Volume XXIII, Chapter 03](../../volume-023-dell-idrac-9-10-administration/chapters/03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md)
  describes. Discovering during an outage that iDRAC was never cabled is
  a preventable and common failure.
- **Consider whether a fabric automation integration applies.** Dell's
  SmartFabric Services can configure a supported PowerSwitch fabric for
  VxRail automatically. Where the switching is Dell and supported, it
  removes an entire class of manual misconfiguration; where it is not, it
  is irrelevant, and the manual configuration in this chapter stands.

## Implementation and Automation

### 1. Preparing DNS records

Every host and appliance needs matching forward and reverse records.
Create them, then verify both directions — creation and correctness are
different things:

```bash
# Forward resolution for each planned ESXi host, VxRail Manager, vCenter.
for h in esxi-01 esxi-02 esxi-03 vxm-01 vcsa-01; do
  printf '%-10s -> %s\n' "$h" "$(dig +short "${h}.lab.example.com")"
done

# Reverse resolution for the same addresses — the half that gets skipped.
for ip in 10.10.10.11 10.10.10.12 10.10.10.13 10.10.10.20 10.10.10.21; do
  printf '%-14s -> %s\n' "$ip" "$(dig +short -x "$ip")"
done
```

Every line of both loops must return a value, and the reverse lookups
must return the same names the forward lookups were performed on. A
blank or mismatched result is a deployment failure that has not happened
yet.

### 2. Verifying NTP before deployment

```bash
# Confirm the planned NTP source is reachable and answering.
ntpdate -q ntp.lab.example.com || chronyc -h ntp.lab.example.com tracking
```

### 3. Switch configuration pattern

The exact syntax depends on the switch platform; the intent does not.
Expressed for a Dell PowerSwitch running OS10, a node-facing port
carrying untagged management and tagged vSAN, vMotion, and discovery
looks like:

```text
interface ethernet 1/1/1
 description VxRail-node-01-nic0
 no shutdown
 switchport mode trunk
 switchport access vlan 100          ! external management, untagged
 switchport trunk allowed vlan 3939,110,120,200-210
 mtu 9216
 spanning-tree port type edge
 spanning-tree bpduguard enable
```

Note `mtu 9216` rather than 9000: switch MTU settings generally describe
the full frame including headers, while the VMkernel MTU describes the
payload. Setting the switch to exactly 9000 is a common and subtle error
that leaves jumbo frames failing by a few bytes.

The internal management VLAN additionally needs IPv6 multicast to pass.
Where MLD snooping is enabled, ensure a querier exists for VLAN 3939.

### 4. Capturing the plan as a machine-readable record

The deployment wizard asks for the same information every time. Record it
once, in a form that can be reviewed and diffed, rather than assembling
it live:

```yaml
# vxrail-deployment-plan.yml — reviewed and signed off before day one.
cluster:
  name: vxrail-lab-01
  domain: lab.example.com
networks:
  management:
    vlan: 100
    tagged: false
    subnet: 10.10.10.0/24
    gateway: 10.10.10.1
  discovery:
    vlan: 3939
    ipv6_multicast: required
  vsan:
    vlan: 110
    subnet: 10.10.110.0/24
    mtu: 9000
  vmotion:
    vlan: 120
    subnet: 10.10.120.0/24
    mtu: 9000
addressing:
  esxi_hosts: 10.10.10.11-10.10.10.20   # range, with headroom
  vxrail_manager: 10.10.10.30
  vcenter: 10.10.10.31
services:
  dns: [10.10.10.5, 10.10.10.6]
  ntp: [ntp.lab.example.com]
  syslog: [10.10.10.7]
vcenter_topology: vxrail-managed        # decided in Chapter 01
```

## Validation and Troubleshooting

### Testing jumbo frames properly

A standard ping proves reachability and nothing about MTU. The test that
matters sets the do-not-fragment bit and a payload that fills the frame:

```bash
# From an ESXi host, against another host's vSAN VMkernel address.
# -d sets do-not-fragment; -s 8972 is 9000 minus 28 bytes of IP/ICMP header.
vmkping -I vmk1 -d -s 8972 10.10.110.12
```

If this fails while a plain `vmkping` succeeds, the path is not carrying
jumbo frames somewhere, and the cluster will run — badly — until someone
finds it.

### Confirming discovery traffic

Where the wizard reports missing nodes, establish whether the problem is
the node or the fabric before touching either:

```bash
# On a node that has been imaged, confirm IPv6 link-local is present
# on the discovery interface.
esxcli network ip interface ipv6 address list
```

An absent IPv6 link-local address points at the node; a present one with
no nodes visible to VxRail Manager points at the switch.

### Common failures and their real causes

| Symptom | Usual cause |
| --- | --- |
| Wizard finds no nodes, or fewer than expected | IPv6 multicast not passing on VLAN 3939, or MLD snooping without a querier |
| Deployment progresses then fails during component registration | Missing reverse DNS records |
| Certificate or authentication errors mid-deployment | NTP unreachable or nodes disagreeing on time |
| Cluster builds, then storage performance is poor under load | MTU mismatch somewhere in the vSAN path |
| Nodes take 30+ seconds to come up after reboot | Spanning-tree not configured as edge port |

Note what the table shows: in every row, the symptom appears somewhere
other than where the fault is. That is why this chapter's checks are
worth performing in advance rather than being derived from a failure.

## Security and Best Practices

- **Keep the internal management VLAN non-routable.** It has no
  legitimate off-rack purpose, and routing it exposes an unauthenticated
  discovery mechanism to the wider network.
- **Separate management from workload networks physically where
  practical, and by VLAN always.** The reasoning matches
  [Volume XXIII, Chapter 03](../../volume-023-dell-idrac-9-10-administration/chapters/03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md);
  the stakes are higher because VxRail Manager's reach exceeds any single
  iDRAC's.
- **Enable BPDU guard on node-facing ports.** Beyond the convergence
  benefit, it prevents a mis-cabled node port from participating in
  spanning tree in ways it should not.
- **Record the deployment plan as a controlled document.** It contains
  the addressing and topology of the platform, and it is the artifact a
  support case, an audit, or a rebuild will need.
- **Do not put credentials in the deployment plan file.** The plan should
  be reviewable and diffable, which is incompatible with holding secrets.
  Reference where credentials live rather than embedding them.

## References and Knowledge Checks

**References**

- [Dell VxRail product documentation](https://www.dell.com/support/home/en-us/product-support/product/vxrail-appliance-series/docs)
  — the VxRail network planning guide is the authoritative source for
  current port, VLAN, and bandwidth requirements.
- [Volume V, Chapter 04](../../volume-005-vmware-virtualization/chapters/04-vsphere-virtual-networking.md)
  — vSphere distributed switching, VMkernel adapters, and teaming, which
  this chapter's fabric requirements terminate on.
- [Volume XXIII, Chapter 03](../../volume-023-dell-idrac-9-10-administration/chapters/03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md)
  — iDRAC management networking for the nodes beneath the cluster.
- [Volume II, Chapter 03](../../volume-002-network-engineering-foundations/chapters/03-ethernet-switching-vlans-and-layer-2-resilience.md)
  — VLAN design and spanning-tree behavior underlying the switch
  configuration here.

**Knowledge checks**

1. VxRail Manager reports finding two of four nodes. Name the two most
   likely fabric causes and how you would distinguish between them.
2. Why is `mtu 9216` on the switch the correct counterpart to `9000` on
   the VMkernel adapter?
3. A deployment fails partway through component registration with no
   network error. What should be checked first, and why does the error
   not name it?
4. Explain why the internal management VLAN is non-routable by design,
   and what would be gained by routing it. (The answer to the second
   half is "nothing" — be able to say why.)
5. Under what circumstances is a dynamic-node cluster the right choice,
   and what does it give up?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each task under the "Hardware Installation
and Initialization" and "Network Environment Requirements" domains** — network prerequisites,
cabling, the deployment configuration, and pre-deploy validation. Getting these right is what makes
the Chapter 03 deployment succeed. Each ends **`**Lab verified by:** *pending*`** until a human
runs it.

**Shared prerequisites for Labs 2.1–2.4** — access to the top-of-rack (ToR) switches and the
planned IP/VLAN scheme, a workstation for validation, and the Dell VxRail network planning guide.
**Cost:** none.

### Lab 2.1 — Network VLANs and requirements (Topic: Network requirements)

**Objective:** Define the required VxRail networks.

```text
# Plan the VLANs VxRail requires on the ToR switches:
#   - Management (ESXi mgmt + vCenter + VxRail Manager)
#   - vSAN         (storage traffic; jumbo frames recommended)
#   - vMotion      (live migration)
#   - VxRail Discovery / internal management (Loudmouth/IPv6 multicast on the mgmt VLAN)
#   - VM/Workload networks
# Confirm the switch trunks the VLANs to every node port and MTU 9000 where required.
```

**Expected result:** the required VLANs (management, vSAN, vMotion, discovery, VM) planned and
trunked to all node ports — VxRail has strict network prerequisites; the internal node discovery
uses IPv6 multicast on the management VLAN at initialization, and vSAN benefits from jumbo frames,
so the switch must be configured *before* deployment.

**Negative test:** deploy without trunking the vSAN/vMotion VLANs to every node port; initialization
fails or the cluster forms without storage/migration networks — the network must be fully prepared
first, which is why the exam weights network requirements.

**Rollback:** none (planning/switch config).

### Lab 2.2 — Physical cabling and ToR switch prep (Topic: Hardware installation)

**Objective:** Verify node uplinks and switch readiness.

```text
# Confirm per node:
#   - node NIC ports cabled to the ToR switch(es) per the design (redundant uplinks)
#   - switch ports set to trunk the VxRail VLANs, correct MTU, spanning-tree edge/portfast
#   - out-of-band iDRAC ports cabled to the management network (Volume XXIII)
```

**Expected result:** each node's data uplinks and iDRAC are cabled and the switch ports are
correctly configured (trunk, MTU, edge) — VxRail initialization drives the nodes over these
uplinks, so cabling and switch-port configuration errors are the most common cause of a failed
first deployment.

**Negative test:** leave a node port on an access VLAN or without portfast; discovery times out or
STP delays bring-up — the physical/switch layer must match the VxRail requirements exactly.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.3 — The deployment configuration (Topic: Pre-deployment planning)

**Objective:** Prepare the VxRail configuration inputs.

```text
# Assemble the deployment inputs (VxRail configuration JSON / the Manager's guided form):
#   - hostnames + IPs for ESXi hosts, vCenter, VxRail Manager (contiguous or per-host)
#   - DNS + NTP servers (must resolve/serve before deployment)
#   - VLAN IDs and subnets/gateways for each network
#   - passwords and vCenter mode (VxRail-managed embedded vCenter, or customer external vCenter)
```

**Expected result:** a complete configuration (JSON or validated form) with hostnames, IPs, DNS,
NTP, VLANs, and the vCenter choice — VxRail deployment is data-driven; a validated configuration
file is what the Manager consumes to build the cluster unattended, and DNS/NTP must already work.

**Negative test:** start deployment with DNS records not yet created or NTP unreachable; validation
fails — DNS forward/reverse records and a reachable NTP source are hard prerequisites, not
post-deploy tasks.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 2.4 — Pre-deployment validation (Topic: Network initialization)

**Objective:** Prove the environment is ready before deploying.

```bash
# From a jump host on the management VLAN, validate the prerequisites:
nslookup vxm.lab.example.com          # DNS forward record exists
nslookup 192.168.10.50                # reverse (PTR) record exists
ping -c1 <ntp-server> && chronyc sources 2>/dev/null | head
ping -M do -s 8972 -c1 <vsan-peer>    # jumbo-frame (MTU 9000) end-to-end test
```

**Expected result:** DNS forward/reverse resolve, NTP is reachable, and a 9000-MTU ping succeeds
end-to-end — pre-deployment validation catches the network/DNS/NTP/MTU issues that would otherwise
fail the deployment hours in; passing these checks first is what makes Chapter 03 succeed on the
first attempt.

**Negative test:** skip the jumbo-frame test and deploy; if an intermediate switch does not pass
MTU 9000, vSAN performance/health suffers after deployment — the `ping -M do -s 8972` proves the
path end-to-end before you commit.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

VxRail deployment is unforgiving of unmet prerequisites and generous when
they are met. The requirements that differ most from a self-built cluster
are IPv6 multicast on a non-routable internal management VLAN for node
discovery, end-to-end jumbo frames for vSAN, and forward *and reverse*
DNS for every host and appliance. Each of these produces a failure whose
symptom appears far from its cause, which is precisely why they are
verified in advance rather than diagnosed later. The output of this
chapter is a reviewed deployment plan complete enough that the wizard in
Chapter 03 requires no further decisions.

- [ ] Can name every network a VxRail cluster requires and what it
      carries.
- [ ] Can explain the IPv6 multicast discovery requirement and the two
      fabric conditions that break it.
- [ ] Can configure node-facing switch ports correctly, including the
      9216/9000 MTU relationship.
- [ ] Has created and verified forward and reverse DNS for every planned
      name.
- [ ] Can test jumbo frames in a way that actually proves them.
- [ ] Has produced a complete deployment plan containing no credentials.
