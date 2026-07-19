# Chapter 10: Installing VMware NSX

![Lab topology for this chapter: a single-node NSX Manager (10.10.50.11, cluster VIP 10.10.50.10) creates a transport zone, uplink profile, and TEP IP pool (10.10.60.0/24, VLAN 300); an ESXi host with a Chapter 4 VDS is prepared as a transport node with management interface 10.10.50.101 and TEP interface TEP-1 at 10.10.60.11; an NSX Edge VM is deployed at management address 10.10.50.21, registers with NSX Manager, and gets its own TEP interface TEP-2 at 10.10.60.21; NSX Manager and both nodes' management interfaces share the 10.10.50.0/24 management network, while the two TEPs exchange Geneve-encapsulated overlay traffic on the separate 10.10.60.0/24 transport VLAN at MTU 9000.](../../../diagrams/volume-05-vmware-virtualization/chapter-10-nsx-installation-lab-topology.svg)

*Figure 10-1. Topology used throughout this chapter's Hands-On Lab: a
single-node NSX Manager, one ESXi host prepared as a transport node, and
one NSX Edge node, connected by a management network and an overlay
transport VLAN. IP addresses match the examples used in Implementation
and Automation and in the lab steps below.*

## Learning Objectives

- Explain NSX's management, control, and data plane architecture and how
  each maps to specific NSX components.
- Deploy an NSX Manager cluster and configure the cluster virtual IP
  (VIP).
- Explain transport zones, uplink profiles, and TEP IP pools, and their
  role in preparing hosts for overlay networking.
- Prepare ESXi hosts as transport nodes, including host-level prerequisites
  tied to the distributed switch covered in [Chapter 4](04-vsphere-virtual-networking.md).
- Deploy NSX Edge nodes and form an Edge cluster.
- Validate transport node and TEP connectivity after host preparation.
- Apply baseline security and access-control practices to a newly deployed
  NSX Manager cluster.

## Theory and Architecture

NSX is VMware's network virtualization and security platform, providing
overlay-based logical networking, distributed firewalling, and
gateway/edge services independent of the underlying physical network
topology. [Chapter 8](08-vsphere-and-nsx-security-architecture.md) introduced the NSX Distributed Firewall and Gateway
Firewall from a security-architecture perspective; this chapter and
[Chapter 11](11-configuring-vmware-nsx.md) cover the platform itself — how it is installed and then
configured for logical networking. This chapter addresses installation:
getting NSX Manager running, hosts and Edges prepared, and the overlay
transport fabric established. [Chapter 11](11-configuring-vmware-nsx.md) covers configuring segments,
gateways, routing, and services on top of that foundation.

### Management, control, and data plane

NSX separates concerns across three planes, consistent with modern
network virtualization architecture generally:

- **Management plane** — **NSX Manager**, the system of record for
  desired configuration and the API/UI surface administrators and
  automation interact with. NSX Manager runs as a cluster of appliance
  nodes (three nodes for production resiliency) rather than a single
  instance.
- **Control plane** — the **Central Control Plane (CCP)**, which runs as a
  role within the NSX Manager cluster nodes themselves (not a separate
  appliance) and computes and distributes the runtime state — logical
  topology, forwarding tables — that transport nodes need, so that data
  plane forwarding decisions do not depend on querying the management
  plane in real time.
- **Data plane** — the actual packet forwarding fabric: ESXi hosts
  prepared as **transport nodes**, and **NSX Edge nodes**, both of which
  run a **local control plane** component that receives state from the
  CCP and programs local forwarding tables, plus the switching component
  that performs the actual Geneve encapsulation/decapsulation and
  forwarding.

### NSX Manager cluster and the cluster VIP

Production NSX deployments run a **three-node NSX Manager cluster**,
providing both control-plane resiliency (CCP state computation continues
if a node is lost) and management-plane API/UI availability. A **cluster
virtual IP (VIP)** is configured across the three nodes so that
administrators, automation, and (crucially) transport nodes and Edges
addressing the management plane use a single stable address rather than
depending on any one node's individual IP — the VIP moves to a surviving
node automatically if the node currently holding it fails. A single-node
NSX Manager deployment is supported for lab/proof-of-concept use but
carries no management or control-plane resiliency and should not be
treated as a production pattern.

### Transport zones

A **transport zone** defines the scope of a logical network — which hosts
and Edge nodes can participate in the same set of logical switches
(**segments**, covered fully in [Chapter 11](11-configuring-vmware-nsx.md)). Two transport zone types
exist:

- **Overlay transport zone** — governs which transport nodes can
  participate in Geneve-encapsulated overlay segments. A host or Edge must
  be a member of the same overlay transport zone as the segments it needs
  to reach.
- **VLAN transport zone** — governs which transport nodes can host
  VLAN-backed segments (segments that map directly to a physical VLAN
  rather than an overlay, used for uplink-facing connectivity — an Edge
  node's northbound VLAN uplinks, for instance — or for workloads that
  need VLAN-backed rather than overlay connectivity for a specific
  reason).

A transport node is typically a member of exactly one overlay transport
zone (a host does not usually need to participate in multiple, functionally
separate overlay fabrics simultaneously) and one or more VLAN transport
zones as needed for its uplink connectivity requirements.

### Host preparation, uplink profiles, and TEPs

**Host preparation** installs NSX kernel modules onto ESXi hosts and
converts them into transport nodes — data-plane participants in the NSX
overlay fabric. At the vSphere 8.x/9.x and NSX 4.x baseline, NSX host
preparation integrates directly with the same **distributed switch (VDS)**
covered in [Chapter 4](04-vsphere-virtual-networking.md), rather than deploying the older, separately managed
**N-VDS (NSX virtual distributed switch)** that earlier NSX releases
required — a converged model where a single VDS carries both ordinary
vSphere port groups and NSX-managed overlay segments. This convergence
materially simplifies host networking design: there is one switching
object per host cluster to reason about, not a parallel N-VDS
infrastructure existing alongside the VDS used for everything else. Older
NSX deployments upgraded forward from pre-convergence releases may still
carry N-VDS instances pending migration, but new deployments at the
current baseline should prepare hosts directly against an existing VDS.

Host preparation requires several pieces of configuration to already
exist:

- An **uplink profile** — defines teaming policy for the host's NSX-used
  uplinks (active/standby uplink assignment, matching or complementing the
  VDS-level teaming design from [Chapter 4](04-vsphere-virtual-networking.md)), the transport VLAN used for
  Geneve-encapsulated traffic between TEPs, and the MTU to use for overlay
  traffic (Geneve encapsulation adds overhead, so the physical/VDS MTU
  must accommodate the overlay MTU plus that overhead — commonly driving
  the same MTU 9000 jumbo-frame requirement seen elsewhere in this volume
  for vSAN and vMotion).
- A **TEP (Tunnel Endpoint) IP pool** (or DHCP, if the transport VLAN has
  a DHCP server available) — the IP addresses that each host's TEP
  interface(s) use as the source/destination of Geneve-encapsulated
  overlay traffic between hosts. Every prepared transport node gets one or
  more TEP IPs from this pool (or DHCP), and TEP-to-TEP reachability
  across the transport VLAN is a hard prerequisite for any overlay traffic
  to forward at all.
- A **transport node profile** (when preparing a cluster of hosts at once
  rather than host-by-host) — bundles the transport zone, VDS/uplink
  mapping, uplink profile, and TEP IP assignment method into a single,
  reusable object applied to an entire cluster in one operation.

### NSX Edge nodes and Edge clusters

**NSX Edge nodes** provide the north-south connectivity between the NSX
overlay fabric and the physical network, along with centralized services
that cannot run purely distributed across every hypervisor host (routing
protocol peering, NAT, load balancing, VPN, and, where applicable,
DHCP server function). Edge nodes come in two form factors:

- **VM form factor** — an Edge deployed as a virtual appliance on an
  existing ESXi host, the common choice for most deployments due to
  simpler lifecycle management (it is just another VM from a vSphere
  operations standpoint) and easier scaling.
- **Bare metal form factor** — an Edge installed directly on physical
  hardware, chosen where the additional throughput/latency headroom of
  avoiding a hypervisor layer is specifically required (very high
  north-south throughput requirements, for instance).

Edge nodes are grouped into an **Edge cluster**, which — analogous to an
ESXi host cluster — provides a pool of Edge capacity that Tier-0 and
Tier-1 gateways ([Chapter 11](11-configuring-vmware-nsx.md)) are deployed onto, with the Edge cluster
governing placement and failover of the gateway's active/standby (or
active/active) instances across member Edge nodes.

## Design Considerations

- **NSX Manager cluster sizing and placement.** Deploy the standard
  three-node cluster (plus VIP) for any production environment; a
  single-node deployment should be explicitly scoped to lab/PoC use and
  not silently carried forward into production. Place the three manager
  nodes to survive the same failure domains the rest of the management
  domain is designed to survive (do not put all three on a single host
  with no anti-affinity rule).
- **Transport zone scope discipline.** Do not default every host and Edge
  into a single, all-encompassing overlay transport zone without
  considering whether that actually matches the intended logical network
  boundaries — transport zone membership is the outer boundary of which
  segments a given transport node can ever reach, and getting this wrong
  early requires host re-preparation to fix.
- **VDS convergence versus legacy N-VDS.** New deployments should prepare
  hosts directly against an existing VDS; environments still running
  N-VDS from an older NSX release should plan and schedule the migration
  to VDS-based host preparation rather than treating N-VDS as a
  permanent, parallel-forever architecture.
- **Uplink profile and MTU consistency with the base VDS design.** The
  uplink profile's teaming policy and transport VLAN MTU requirement must
  be reconciled with the VDS teaming and MTU design from [Chapter 4](04-vsphere-virtual-networking.md), not
  designed in isolation — a mismatch here is a common source of host
  preparation succeeding at the configuration level while TEP
  connectivity silently fails.
- **TEP IP pool sizing and DHCP versus static pool choice.** Size the TEP
  IP pool for the maximum expected transport node count with reasonable
  growth headroom (pool exhaustion blocks further host preparation);
  DHCP-assigned TEPs reduce IP pool management overhead in large,
  frequently-changing fleets at the cost of adding a DHCP service
  availability dependency to the overlay fabric's basic function.
- **Edge node form factor and sizing.** VM form factor Edges are the
  default choice; bare metal is a deliberate, throughput-driven exception,
  not a default. Size Edge VM compute resources (and Edge cluster member
  count) against actual expected north-south throughput and the specific
  gateway services (NAT, load balancing) planned for [Chapter 11](11-configuring-vmware-nsx.md)'s
  configuration — undersized Edges are a common, hard-to-diagnose source
  of throughput ceilings that appear unrelated to Edge sizing at first
  glance.
- **Edge cluster failure-domain placement.** Spread Edge cluster members
  across different ESXi hosts (and, ideally, different racks/power
  domains) using anti-affinity, mirroring the same failure-domain
  discipline applied to vSphere HA/DRS clusters generally.

## Implementation and Automation

### Deploying an NSX Manager node via OVA

```bash
# ovftool: deploy an NSX Manager appliance OVA to an existing ESXi host
ovftool --acceptAllEulas --skipManifestCheck \
  --name=nsx-mgr-01 \
  --datastore=ds-vmfs6-tier1 \
  --network="pg-management" \
  --prop:nsx_ip_0=10.10.50.11 \
  --prop:nsx_netmask_0=255.255.255.0 \
  --prop:nsx_gateway_0=10.10.50.1 \
  --prop:nsx_dns1_0=10.10.10.10 \
  --prop:nsx_ntp_0=10.10.10.10 \
  --prop:nsx_hostname=nsx-mgr-01.corp.example \
  --prop:nsx_passwd_0='<NSX_ADMIN_PASSWORD>' \
  --prop:nsx_cli_passwd_0='<NSX_CLI_PASSWORD>' \
  --prop:nsx_isSSHEnabled=True \
  nsx-manager.ova vi://root:<ESXI_ROOT_PASSWORD>@esxi01.corp.example
```

### Forming the NSX Manager cluster and configuring the VIP

```bash
# NSX CLI (on the first deployed manager node): join additional manager nodes to the cluster
join management-cluster 10.10.50.11 thumbprint <NODE1_API_THUMBPRINT> \
  username admin password '<NSX_ADMIN_PASSWORD>'
```

```bash
# curl against the NSX Manager Policy API: configure the cluster virtual IP
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-mgr-01.corp.example/api/v1/cluster/api-virtual-ip \
  -H "Content-Type: application/json" \
  -d '{"ip_address": "10.10.50.10"}'
```

### Creating transport zones

```bash
# curl against the NSX Manager Policy API: create an overlay transport zone
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/sites/default/enforcement-points/default/transport-zones/tz-overlay-01 \
  -H "Content-Type: application/json" \
  -d '{
        "display_name": "tz-overlay-01",
        "tz_type": "OVERLAY_STANDARD"
      }'
```

### Creating an uplink profile and TEP IP pool

```bash
# curl against the NSX Manager Policy API: create an uplink profile with an active/standby
# teaming policy and a transport VLAN, then an IP pool for TEP addressing
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/host-switch-profiles/uplink-profile-01 \
  -H "Content-Type: application/json" \
  -d '{
        "resource_type": "PolicyUplinkHostSwitchProfile",
        "display_name": "uplink-profile-01",
        "transport_vlan": 300,
        "mtu": 9000,
        "teaming": {
          "active_list": [{"uplink_name": "uplink-1", "uplink_type": "PNIC"}],
          "standby_list": [{"uplink_name": "uplink-2", "uplink_type": "PNIC"}],
          "policy": "FAILOVER_ORDER"
        }
      }'

curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/ip-pools/tep-pool-01 \
  -H "Content-Type: application/json" \
  -d '{"display_name": "tep-pool-01"}'

curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/ip-pools/tep-pool-01/ip-subnets/subnet-01 \
  -H "Content-Type: application/json" \
  -d '{
        "resource_type": "IpAddressPoolStaticSubnet",
        "cidr": "10.10.60.0/24",
        "allocation_ranges": [{"start": "10.10.60.10", "end": "10.10.60.100"}],
        "gateway_ip": "10.10.60.1"
      }'
```

### Preparing an ESXi cluster as transport nodes via a transport node profile

```bash
# curl against the NSX Manager Policy API: create a transport node profile
# referencing the existing VDS, uplink profile, and TEP pool
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/host-transport-node-profiles/tnp-cluster-a \
  -H "Content-Type: application/json" \
  -d '{
        "display_name": "tnp-cluster-a",
        "host_switch_spec": {
          "resource_type": "StandardHostSwitchCollection",
          "host_switches": [{
            "host_switch_id": "dvs-cluster-a",
            "host_switch_mode": "STANDARD",
            "host_switch_type": "VDS",
            "uplink_profile_id": "uplink-profile-01",
            "ip_assignment_spec": {
              "resource_type": "StaticIpPoolSpec",
              "ip_pool_id": "tep-pool-01"
            },
            "uplinks": [
              {"uplink_name": "uplink-1", "vds_uplink_name": "Uplink 1"},
              {"uplink_name": "uplink-2", "vds_uplink_name": "Uplink 2"}
            ]
          }]
        },
        "transport_zone_endpoints": [{"transport_zone_id": "tz-overlay-01"}]
      }'
```

```powershell
# PowerCLI + NSX PowerCLI module: apply the transport node profile to a cluster
Connect-NsxtServer -Server nsx-vip.corp.example -User admin -Password '<NSX_ADMIN_PASSWORD>'
$cluster = Get-Cluster -Name "prod-cluster-a"
New-NsxtPolicyTransportNodeCollection -Cluster $cluster -TransportNodeProfile "tnp-cluster-a"
```

### Deploying an Edge node and forming an Edge cluster

```bash
# ovftool: deploy an NSX Edge VM appliance
ovftool --acceptAllEulas --skipManifestCheck \
  --name=nsx-edge-01 \
  --datastore=ds-vmfs6-tier1 \
  --network="pg-management=pg-management" \
  --network="pg-uplink=pg-edge-uplink" \
  --prop:nsx_ip_0=10.10.50.21 \
  --prop:nsx_netmask_0=255.255.255.0 \
  --prop:nsx_gateway_0=10.10.50.1 \
  --prop:nsx_hostname=nsx-edge-01.corp.example \
  --prop:nsx_passwd_0='<NSX_ADMIN_PASSWORD>' \
  --deploymentOption=medium \
  nsx-edge-node.ova vi://root:<ESXI_ROOT_PASSWORD>@esxi01.corp.example
```

```bash
# curl against the NSX Manager Policy API: register the Edge node and create an Edge cluster
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' -X PUT \
  https://nsx-vip.corp.example/policy/api/v1/infra/sites/default/enforcement-points/default/edge-clusters/edge-cluster-01 \
  -H "Content-Type: application/json" \
  -d '{
        "display_name": "edge-cluster-01",
        "members": [{"transport_node_id": "<EDGE_NODE_ID>"}]
      }'
```

## Validation and Troubleshooting

- **Manager cluster health.** `GET
  /api/v1/cluster/status` (Policy or Manager API) reports each node's
  cluster role status; a node showing `DOWN` or `DEGRADED` after a join
  operation most commonly traces to NTP drift between nodes (cross-
  reference the NTP prerequisite from Chapters 2 and 3 — NSX Manager
  clustering has the same time-synchronization dependency) or a
  management-network reachability issue between nodes.

  ```bash
  curl -k -u admin:'<NSX_ADMIN_PASSWORD>' https://nsx-vip.corp.example/api/v1/cluster/status
  ```

- **Transport node preparation failures.** A host stuck in `Installing` or
  showing a preparation failure most often traces to a VDS/uplink
  mismatch (the uplink profile references uplink names that do not exist
  on the target VDS) or a TEP IP pool exhaustion; the transport node's
  detailed status in the vSphere Client's NSX Manager plugin view (or the
  Policy API's transport node status endpoint) names the specific failure
  stage.
- **TEP connectivity verification.** From the ESXi host's shell, the
  `nsxcli` (NSX-specific host CLI, distinct from `esxcli`) reports TEP
  configuration and reachability directly:

  ```bash
  # nsxcli on a prepared ESXi transport node
  get logical-switch
  get vteps
  ping ++netstack=vxlan <PEER_TEP_IP>
  ```

  A TEP ping failure with the underlying VDS uplink otherwise healthy
  points to a transport VLAN MTU mismatch (Geneve overhead not
  accommodated end-to-end) or a transport VLAN not actually trunked to the
  physical switch port the uplink profile assumes.
- **Edge node deployment and cluster membership issues.** An Edge that
  deploys successfully as a VM but fails to register with NSX Manager
  typically indicates a management-plane reachability issue (the Edge's
  management interface cannot reach the NSX Manager VIP) rather than an
  Edge-internal fault; confirm basic IP connectivity from the Edge's
  management interface before escalating further.
- **Certificate/thumbprint mismatches during cluster join.** A manager
  cluster join failing on a thumbprint mismatch indicates the node's API
  certificate changed (or was never what the join command expected) since
  the thumbprint was retrieved — re-retrieve the current thumbprint
  immediately before retrying rather than reusing a stale value.

## Security and Best Practices

- Restrict NSX Manager API/UI access to a defined management network
  reachable only by authorized administrators and automation service
  accounts, consistent with the broader management-plane hardening
  approach in [Chapter 8](08-vsphere-and-nsx-security-architecture.md).
- Change default administrative credentials immediately after deployment,
  and integrate NSX Manager with the same centralized identity approach
  (Active Directory, or VMware Identity/OIDC federation where supported)
  used for vCenter Server in [Chapter 3](03-vcenter-server-deployment-identity-and-recovery.md), rather than maintaining a separate
  local-only credential set indefinitely.
- Deploy the three-node NSX Manager cluster with anti-affinity across
  hosts and failure domains; treat a single-node deployment as
  explicitly non-production.
- Limit which physical/VLAN segments can reach the NSX Manager and Edge
  management interfaces at the network layer, independent of NSX
  Manager's own authentication controls — the management plane should not
  be reachable from general workload segments.
- Validate NTP synchronization across all NSX Manager nodes, transport
  nodes, and Edge nodes before and after cluster formation; NSX Manager
  clustering, like vCenter Server ([Chapter 3](03-vcenter-server-deployment-identity-and-recovery.md)) and vSAN ([Chapter 6](06-vsphere-storage-and-vsan.md)), fails
  in confusing ways under sufficient clock drift.
- Confirm host preparation and Edge deployment used images/OVAs retrieved
  from an authenticated, verified Broadcom source with checksum
  validation — an installation-time software supply-chain control that is
  easy to skip under deployment time pressure but should not be.

## References and Knowledge Checks

**References**

- [VMware NSX 4.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/nsx/vmware-nsx/4-2.html) — *NSX Manager Installation and Cluster
  Configuration*.
- [VMware NSX 4.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/nsx/vmware-nsx/4-2.html) — *Transport Zones, Uplink Profiles, and
  Host Preparation*.
- [VMware NSX 4.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/nsx/vmware-nsx/4-2.html) — *NSX Edge Installation and Edge
  Clusters*.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline referenced throughout this volume.
- See [Chapter 4](04-vsphere-virtual-networking.md) for the VDS foundation NSX host preparation builds on.
- See [Chapter 8](08-vsphere-and-nsx-security-architecture.md) for NSX Distributed Firewall and Gateway Firewall
  security architecture.
- See [Chapter 11](11-configuring-vmware-nsx.md) for segment, gateway, and routing configuration built on
  top of the transport fabric installed in this chapter.

**Knowledge checks**

1. Which NSX component runs the Central Control Plane role, and why does
   that placement matter for data-plane resiliency if a single node is
   lost?
2. What changed about host preparation's relationship to N-VDS at the
   current NSX 4.x/vSphere 9.x baseline compared to earlier NSX releases?
3. Why must an uplink profile's transport VLAN MTU setting be reconciled
   with the underlying VDS's MTU configuration rather than set
   independently?
4. What is the functional difference between an overlay transport zone
   and a VLAN transport zone?
5. Give one scenario where a bare metal Edge node form factor is the
   justified choice over the VM form factor.

## Hands-On Lab

**Objective:** Deploy a single-node NSX Manager (lab-scoped), create an
overlay transport zone, uplink profile, and TEP pool, prepare one nested
ESXi host as a transport node, deploy an Edge VM, and validate TEP
connectivity — including a deliberate uplink-profile misconfiguration
negative test.

**Prerequisites**

- A vSphere 9.x lab with at least one ESXi host (nested is acceptable)
  already prepared with a VDS (from the [Chapter 4](04-vsphere-virtual-networking.md) lab or equivalent),
  reachable NTP and DNS, and sufficient free capacity for an NSX Manager
  appliance and an Edge VM.
- The NSX Manager and NSX Edge OVA files staged locally, and `ovftool`
  installed on the deploying workstation.
- A lab overlay-capable VLAN (transport VLAN) trunked to the relevant
  physical/nested switch ports, with jumbo frames (MTU 9000) supported
  end-to-end.

**Steps**

1. Deploy a single NSX Manager node using the `ovftool` example in
   Implementation and Automation, adjusted to lab addressing.

   **Expected result:** the NSX Manager UI becomes reachable at
   `https://<manager-ip>/` and the cluster status API reports the single
   node as `UP`.

2. Create an overlay transport zone, an uplink profile referencing the
   lab's VDS uplink names, and a TEP IP pool sized for at least 4
   addresses.

   **Expected result:** all three objects are visible under `System >
   Fabric` in the NSX Manager UI.

3. **Negative test:** create a second uplink profile that intentionally
   references an uplink name that does not exist on the lab VDS (for
   example, `uplink-3` when the VDS has only two uplinks configured), and
   attempt to prepare the lab host using a transport node profile built
   from this incorrect uplink profile.

   **Expected result:** host preparation fails, with the transport node
   status reporting an uplink mapping error rather than succeeding
   silently — confirm the specific failure reason references the
   nonexistent uplink name.

4. Correct the transport node profile to reference the correct uplink
   profile from step 2, and re-run host preparation:

   **Expected result:** the host transitions through `Installing` to a
   `Success`/green transport node status.

5. From the prepared host's shell, verify TEP configuration:

   ```bash
   nsxcli
   get vteps
   ```

   **Expected result:** the host reports at least one TEP interface with
   an IP address drawn from the configured TEP pool.

6. Deploy an NSX Edge VM using the `ovftool` example, adjusted to lab
   addressing, and register it with NSX Manager.

   **Expected result:** the Edge node appears under `System > Fabric >
   Nodes > Edge Transport Nodes` with a healthy status, and can be added
   to a new Edge cluster.

7. Validate MTU end-to-end for the transport VLAN:

   ```bash
   vmkping ++netstack=vxlan -d -s 8972 <PEER_TEP_IP>
   ```

   **Expected result:** the ping succeeds at full jumbo-frame payload
   size, confirming the transport VLAN correctly carries Geneve-
   encapsulated traffic with room for encapsulation overhead.

8. **Cleanup:** remove the transport node profile and revert host
   preparation (uninstall NSX from the host), delete the Edge VM and Edge
   cluster, remove the transport zone/uplink profile/TEP pool objects,
   and power off/delete the NSX Manager appliance if it was deployed
   solely for this lab.

## Summary and Completion Checklist

NSX separates management (NSX Manager, deployed as a resilient three-node
cluster with a VIP), control (the Central Control Plane running within
manager nodes), and data plane (transport nodes and Edge nodes) concerns.
Host preparation at the current baseline converges directly onto the
existing VDS rather than a separate N-VDS, and depends on a correctly
matched transport zone, uplink profile, and TEP IP pool before any overlay
traffic can forward — TEP-to-TEP reachability across the transport VLAN,
including correct MTU accommodation for Geneve encapsulation overhead, is
the foundational connectivity requirement everything else in [Chapter 11](11-configuring-vmware-nsx.md)
builds on. Edge nodes, deployed as VM or bare metal form factor and
grouped into Edge clusters, provide the north-south and centralized
services layer. Getting this installation foundation right — manager
cluster resiliency, correct transport fabric configuration, validated TEP
connectivity — is what makes the logical networking and security
configuration in the next chapter possible.

- [ ] Can explain NSX's management/control/data plane separation and where
      each component runs.
- [ ] Can deploy an NSX Manager cluster with a VIP.
- [ ] Can create a transport zone, uplink profile, and TEP IP pool
      correctly matched to an existing VDS.
- [ ] Can prepare ESXi hosts as transport nodes and validate TEP
      connectivity.
- [ ] Can deploy Edge nodes and form an Edge cluster.
- [ ] Can diagnose a host preparation failure caused by an uplink profile
      mismatch.
- [ ] Completed the hands-on lab, including the uplink-profile negative
      test and full cleanup.
