# Chapter 09: Catalyst Center, SD-Access, Assurance, and Operations

## Learning Objectives

- Explain Cisco Catalyst Center's role as the single management,
  automation, and assurance plane for the Catalyst estate built across
  this volume.
- Describe SD-Access fabric architecture — control plane, border, edge,
  and fabric WLC roles — and how LISP and VXLAN implement it.
- Explain how SD-Access Virtual Networks (VNs) and Scalable Group Tags
  (SGTs) extend the VRF-lite and TrustSec concepts from Chapters 3 and 7
  into a fabric-managed overlay.
- Describe the Catalyst Center automation workflow (Discovery, Inventory,
  LAN Automation, Provision) used to build an underlay and fabric.
- Use Catalyst Center Assurance to validate fabric and client health, and
  interpret common fabric failure signatures at the CLI.
- Apply operational and security best practices for a Catalyst
  Center–managed estate.

## Theory and Architecture

### Catalyst Center's role

**Cisco Catalyst Center** (the current name for the platform previously
shipped as Cisco DNA Center) is the centralized management,
automation, and assurance controller for the Catalyst 9000 estate this
volume has built chapter by chapter. Where Chapters 1–8 configured
switches, routers, and controllers directly through the CLI or
device-level programmability, Catalyst Center operates one layer above
that: it discovers and inventories the estate, automates day-0/day-1
provisioning (including the SD-Access fabric overlay), and continuously
correlates telemetry from every managed device into Assurance health
scores — without requiring an operator to touch individual device CLI for
routine changes.

Catalyst Center is delivered as a physical or virtual appliance and
requires the **Network Advantage** or higher licensing tier introduced in
Chapter 1 on every device it fully manages for SD-Access and Assurance
features. It communicates with managed devices using the same
programmability surfaces covered in Chapter 8 (NETCONF, RESTCONF, SNMP,
and CLI via SSH) rather than a proprietary agent, which is why every
device configured through this volume's earlier chapters is
Catalyst-Center-manageable without a forklift change.

### SD-Access fabric architecture

**Software-Defined Access (SD-Access)** is Cisco's fabric-based evolution
of the traditional campus described in Chapter 1. Instead of VLANs and a
routed/switched hierarchy carrying both topology and policy together
(the traditional model used in Chapters 2–3), SD-Access separates the
physical **underlay** (plain Layer 3 routed connectivity between fabric
nodes) from a **VXLAN-encapsulated overlay** that carries both traffic
and policy, decoupling where an endpoint is physically connected from
what network and policy it belongs to.

Four fabric roles, implemented on the same Catalyst 9000 platforms
already covered in this volume, cooperate to build a fabric site:

| Role | Function |
| --- | --- |
| Control Plane Node | Runs LISP to maintain a host-tracking database mapping every endpoint (by IP/MAC) to the fabric edge node it is currently attached to |
| Border Node | The fabric's exit point to networks outside the fabric (traditional campus, WAN, data center, internet); translates between fabric VXLAN/SGT and the outside world's normal routing and VLANs |
| Edge Node | Where endpoints physically connect; performs VXLAN encapsulation/decapsulation and applies SGT-based policy at the point closest to the endpoint |
| Fabric WLC | A Catalyst 9800 controller (Chapter 5) integrated into the fabric; APs become fabric edge nodes for wireless clients, carrying wireless traffic in the same VXLAN overlay as wired traffic |

A **fabric site** is one instance of these roles operating together
(commonly one campus or one large branch); a **fabric domain** groups
multiple fabric sites connected by a **transit** — either an **IP-based
transit** (traditional routed connectivity between sites, policy
re-applied at each site's border) or an **SD-Access transit** (extends
the fabric's VXLAN/SGT overlay itself between sites for uninterrupted
end-to-end policy).

### LISP and VXLAN in the fabric

SD-Access implements its overlay with two complementary protocols working
at different layers:

- **LISP (Locator/ID Separation Protocol)** is the fabric's control
  plane. It separates an endpoint's identity (its IP address) from its
  location (the Routing Locator, or RLOC, of the fabric edge node it is
  attached to). When an edge node needs to forward traffic to an
  endpoint it doesn't have a local host route for, it queries the Control
  Plane Node's LISP map server/resolver for that endpoint's current RLOC
  — the fabric's answer to "where is this host right now," which is what
  allows an endpoint to keep the same IP address as it moves between
  fabric edge nodes (a wired move, or a wireless roam) without a routing
  protocol reconvergence event.
- **VXLAN** is the fabric's data plane encapsulation. Edge and border
  nodes wrap the endpoint's original frame in a VXLAN header carrying a
  VNI (mapping to the endpoint's Virtual Network) and an SGT (Chapter 7),
  then route that VXLAN packet across the plain-routed underlay to the
  destination edge/border node, which decapsulates it and delivers the
  original frame with its Virtual Network and SGT context intact.

This is the fabric-managed evolution of two concepts already introduced
in this volume: a **Virtual Network (VN)** is functionally the fabric's
managed equivalent of the VRF-lite macro-segmentation from Chapter 3
(each VN maps to its own VRF in the underlay/border), and the SGT carried
in the VXLAN header is the same TrustSec SGT from Chapter 7 — SD-Access
does not replace those concepts, it automates and carries them
consistently across an entire fabric site instead of requiring
per-device manual configuration.

### Catalyst Center automation workflow

Catalyst Center builds and operates a fabric (or a traditional,
non-fabric managed estate) through a sequential workflow:

1. **Discovery** — Catalyst Center probes a defined IP range or seed
   device using SNMP/SSH credentials to find devices and add them to
   inventory.
2. **Inventory** — discovered devices are polled for state (software
   version, uptime, interface list, neighbors) and become managed;
   inventory is the prerequisite for every later automation and
   Assurance step.
3. **LAN Automation** — provisions the underlay automatically: Catalyst
   Center allocates IP addressing and pushes routed point-to-point links
   and an IGP (IS-IS, by default) between fabric-candidate devices
   starting from a seed border/control-plane device, removing the
   need to hand-configure the underlay device by device.
4. **Provision** — assigns discovered devices to a site (a Catalyst
   Center site hierarchy modeling the organization's physical areas,
   buildings, and floors) and, for fabric devices, assigns their fabric
   role (control plane, border, edge) and Virtual Network/SGT policy
   membership.

Wireless is provisioned the same way: a Catalyst 9800 (Chapter 5) is
added to inventory, assigned to a site, and — for a fabric-integrated
design — enabled as the site's fabric WLC, at which point its APs become
fabric edge nodes automatically.

### Assurance

**Catalyst Center Assurance** continuously ingests telemetry (streaming
where supported, per Chapter 8's model-driven telemetry, and polled
where not) from every managed device and client, then correlates it into
per-device, per-client, and per-site health scores rather than requiring
an operator to interpret raw counters. Key Assurance capabilities:

- **Health scores** — a 1–10 (or good/fair/poor) score per device, per
  client, and per site derived from multiple underlying KPIs (CPU,
  memory, interface errors, AP/WLC join state, authentication success
  rate), giving operators a single number to triage before drilling into
  raw metrics.
- **Path Trace** — simulates or observes the actual forwarding path
  between two endpoints (or an endpoint and a destination), reporting
  each hop's forwarding decision, QoS treatment (Chapter 6), and any ACL
  or SGACL (Chapter 7) enforcement encountered along the way — a
  significant improvement over manually correlating `traceroute` output
  with per-hop configuration.
- **AI Network Analytics** — baselines normal behavior per site over time
  (client counts, throughput, authentication latency) and flags
  statistically significant deviations, surfacing emerging problems
  before they cross a static, manually set threshold.

## Design Considerations

- **Fabric vs. traditional campus** — adopt SD-Access where the
  organization's segmentation, mobility, or automation requirements
  justify the added architectural and licensing complexity (frequent
  endpoint moves across the campus that must retain consistent policy,
  or a segmentation requirement too fine-grained for VLAN-based design
  alone); a smaller, stable campus may be well served by the traditional
  hierarchical design from Chapters 1–3 without a fabric overlay at all.
- **Site hierarchy first** — build the Catalyst Center site hierarchy
  (areas/buildings/floors) to match the organization's actual physical
  and administrative structure before provisioning any device; the site
  hierarchy is the anchor for location-specific settings (AP RF profiles,
  DHCP/DNS, software image assignment) throughout the platform, and
  restructuring it later is disruptive.
- **Underlay IGP choice** — LAN Automation defaults to IS-IS for the
  underlay; accept the default unless a specific operational reason
  (existing OSPF expertise, integration constraint) justifies deviating,
  since a supported default reduces the number of decisions requiring
  independent validation.
- **Transit selection** — use IP-based transit between fabric sites when
  policy can acceptably be re-applied at each site's border; use
  SD-Access transit only where uninterrupted end-to-end VN/SGT policy
  across sites is a hard requirement, since SD-Access transit adds
  topology and failure-domain complexity an IP-based transit avoids.
- **Migration approach** — migrate an existing traditional campus to
  SD-Access incrementally, site by site or even switch-block by
  switch-block, rather than as a single cutover; Catalyst Center supports
  a phased approach where fabric and non-fabric sites coexist and
  exchange traffic through a border node during the transition.
- **Assurance data retention and scale** — size the Catalyst Center
  appliance (or its cluster) against the actual managed device and
  client count and the desired Assurance data retention window; both
  directly drive appliance sizing and are far more disruptive to change
  after deployment than before.
- **High availability** — deploy Catalyst Center as a three-node cluster
  for production use; a single-node deployment is appropriate only for a
  lab or a proof-of-concept, never for a production automation and
  Assurance control plane the network now depends on operationally.

## Implementation and Automation

Catalyst Center's primary interface is its web GUI and REST API rather
than per-device CLI, so the "implementation" for this chapter is the
sequential workflow itself, illustrated with the CLI-visible results it
produces on managed devices, plus the REST API calls that drive it
programmatically.

### Discovery and inventory (REST API)

```bash
# Authenticate and obtain a token
curl -k -X POST https://catalyst-center.example.internal/dna/system/api/v1/auth/token \
  -u netadmin:<PASSWORD>

# Start a discovery job against a seed device range
curl -k -X POST https://catalyst-center.example.internal/dna/intent/api/v1/discovery \
  -H "X-Auth-Token: <TOKEN>" -H "Content-Type: application/json" \
  -d '{
        "name": "Campus-Discovery-01",
        "discoveryType": "CDP",
        "ipAddressList": "10.10.99.2",
        "cdpLevel": 3,
        "protocolOrder": "ssh",
        "globalCredentialIdList": ["<CLI_CRED_ID>", "<SNMP_CRED_ID>"]
      }'
```

### LAN Automation (underlay provisioning)

```bash
curl -k -X POST https://catalyst-center.example.internal/dna/intent/api/v1/lan-automation \
  -H "X-Auth-Token: <TOKEN>" -H "Content-Type: application/json" \
  -d '{
        "discoveredDeviceSiteNameHierarchy": "Global/Campus/Building-A",
        "primaryDeviceManagementIPAddress": "10.10.99.2",
        "peerDeviceManagedIPAddress": "10.10.99.3",
        "ipPools": [
          { "ipPoolName": "UNDERLAY-POOL", "ipPoolRole": "MAIN_POOL" }
        ]
      }'
```

Once LAN Automation completes, the resulting underlay is visible from the
device CLI exactly like any manually built IS-IS underlay:

```text
EDGE-01# show isis neighbors
EDGE-01# show ip route isis
```

### Fabric site and role provisioning (REST API)

```bash
curl -k -X POST https://catalyst-center.example.internal/dna/intent/api/v1/business/sda/fabric-site \
  -H "X-Auth-Token: <TOKEN>" -H "Content-Type: application/json" \
  -d '{ "siteNameHierarchy": "Global/Campus/Building-A" }'

curl -k -X POST https://catalyst-center.example.internal/dna/intent/api/v1/business/sda/device \
  -H "X-Auth-Token: <TOKEN>" -H "Content-Type: application/json" \
  -d '{
        "deviceManagementIpAddress": "10.10.99.4",
        "siteNameHierarchy": "Global/Campus/Building-A",
        "deviceRole": "EDGE"
      }'
```

### Resulting fabric state on the device

Once Catalyst Center provisions a device into a fabric role, the LISP and
VXLAN configuration it pushes is inspectable with standard IOS XE CLI,
even though it was never typed by hand:

```text
EDGE-01# show lisp session
EDGE-01# show lisp instance-id 4099 ipv4 server summary
EDGE-01# show interface vxlan 0
EDGE-01# show fabric edge sso summary
```

### Virtual Network and SGT policy (GUI-driven, CLI-visible result)

Virtual Networks and their SGT-based access-control policy are authored
in Catalyst Center's Policy application (mapping endpoints/groups to
VNs and SGTs, and defining SGT-to-SGT access contracts — the fabric's
managed equivalent of the SGACL matrix from Chapter 7). The resulting
per-device configuration is visible the same way:

```text
BORDER-01# show vrf | include VN
BORDER-01# show cts role-based permissions
```

## Validation and Troubleshooting

```text
EDGE-01# show fabric edge sso summary
EDGE-01# show lisp session
CTRL-01# show lisp instance-id 4099 ipv4 server summary
CTRL-01# show lisp instance-id 4099 ipv4 map-cache
BORDER-01# show lisp instance-id 4099 ipv4 database
DIST-01# show wireless fabric summary
```

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Discovery job completes with zero devices found | Seed IP unreachable, or SNMP/SSH credentials in the discovery job don't match the device's actual configured credentials | Confirm reachability and credential set independently via a manual SSH test before re-running discovery |
| LAN Automation never completes for a candidate device | Candidate device not directly connected (via a supported discovery protocol) to an already-provisioned seed device, or an IP pool exhausted | Confirm CDP/LLDP adjacency to the seed device, check IP pool utilization in Catalyst Center |
| Endpoint in the fabric can't reach a host outside the fabric | Border node's `show lisp session` shows no session to the Control Plane Node, or the VN's VRF isn't correctly leaked/exported at the border | `show lisp session`, `show vrf`, confirm the border's external routing (Chapter 3 concepts) is correctly redistributing fabric VN routes |
| Endpoint loses connectivity briefly on a wired move between edge nodes | Expected during LISP map-cache reconvergence; investigate only if the outage duration exceeds the design's tolerance | `show lisp instance-id <id> ipv4 server summary` on the Control Plane Node, confirm registration updates promptly from the new edge |
| Fabric WLC's APs not appearing as fabric edge nodes | Catalyst 9800 not yet provisioned as the site's fabric WLC in Catalyst Center, or AP still on a non-fabric-enabled site tag (Chapter 5) | `show wireless fabric summary` on the WLC, confirm the AP's site tag maps to the fabric-enabled site |
| Assurance health score for a device is poor but the device CLI shows no obvious fault | A KPI outside the CLI's normal `show` output (interface error trend, historical baseline deviation from AI Network Analytics) is driving the score | Drill into the specific KPI contributing to the health score in Assurance rather than relying on CLI alone |

## Security and Best Practices

- Restrict Catalyst Center GUI and API access with role-based access
  control scoped to job function (read-only monitoring vs. full
  provisioning), the same least-privilege principle applied to device CLI
  access in Chapter 7; a Catalyst Center administrator account
  effectively has provisioning authority over the entire managed estate.
- Store discovery and device credentials in Catalyst Center's credential
  store, never as ad hoc entries duplicated outside it, and rotate them
  on the same schedule as the TACACS+/RADIUS credentials from Chapter 7.
- Back up the Catalyst Center appliance/cluster on a defined schedule and
  test restoration; because Catalyst Center becomes the automation and
  policy source of truth for the estate, losing it without a tested
  backup is a materially larger operational risk than losing a single
  device's configuration.
- Keep Catalyst Center's software version within Cisco's published
  compatibility matrix against the managed IOS XE and Catalyst 9800
  software trains; an unsupported combination can silently break
  provisioning or Assurance data collection rather than failing loudly.
- Treat the SD-Access fabric's Control Plane Node and Border Node
  availability as critical-path infrastructure; loss of the Control
  Plane Node stops new endpoint registration fabric-wide (existing
  sessions continue forwarding via cached state), so these roles should
  be deployed redundantly per the design guide's HA guidance.
- Audit VN and SGACL policy changes made through Catalyst Center with
  the same change-control rigor applied to manually authored TrustSec
  policy in Chapter 7, since a policy change here applies fabric-wide
  the moment it is deployed.
- Use Assurance proactively (reviewing health-score trends and AI Network
  Analytics deviations on a defined cadence) rather than only after a
  user-reported incident; the value of continuous telemetry correlation
  is largely lost if it is only consulted reactively.

## References and Knowledge Checks

**Authoritative references**

- Cisco, *Catalyst Center User Guide* and *SD-Access Solution Design
  Guide*, current release.
- Cisco, *Software-Defined Access Deployment Guide*.
- RFC 9300/9301 (LISP), RFC 7348 (VXLAN).
- Cisco Catalyst Center REST API reference (Cisco DevNet).

**Knowledge checks**

1. What is the functional relationship between an SD-Access Virtual
   Network and the VRF-lite macro-segmentation introduced in Chapter 3?
2. Describe the roles of LISP and VXLAN in the SD-Access fabric and which
   plane (control vs. data) each implements.
3. What does the LAN Automation step of the Catalyst Center workflow
   provision, and what underlay protocol does it use by default?
4. What is the difference between IP-based transit and SD-Access transit
   between two fabric sites?
5. Why does losing the Control Plane Node affect new endpoint
   registration fabric-wide but not necessarily break already-established
   sessions?

## Hands-On Lab

**Objective:** Use a Catalyst Center instance to provision two fabric
sites, validate underlay and fabric formation through both the Catalyst
Center GUI/API and device CLI, and use Assurance Path Trace to confirm
policy enforcement between two test endpoints.

**Prerequisites**

- Access to a Catalyst Center appliance/cluster, either an organization-
  owned instance or a reserved Cisco DevNet Catalyst Center sandbox (the
  DevNet "Always-On" or reservable SD-Access sandbox provides a
  pre-built or buildable fabric topology suitable for this lab without
  requiring dedicated fabric-capable hardware).
- At least three Catalyst 9000-series devices (physical, CML, or the
  sandbox's provided topology) cabled to act as control plane/border and
  two edge nodes, with CDP/LLDP enabled between them (default) so
  Discovery and LAN Automation can walk the topology.
- API/GUI credentials for the Catalyst Center instance with provisioning
  rights, and CLI/SSH credentials pre-staged on the seed device matching
  a global credential set defined in Catalyst Center.

**Procedure**

1. In Catalyst Center, define a site hierarchy (for example, `Global/
   Campus/Building-A`) matching the lab topology, then run Discovery
   against the seed border/control-plane device's management IP.

   ```text
   Catalyst Center > Provision > Inventory > Add Device Discovery
   ```

   **Expected result:** the discovery job completes and the seed device
   appears in Inventory with a `Managed` status.

2. Run LAN Automation from the seed device to provision the underlay to
   the two candidate edge switches, using the REST API call or the
   equivalent GUI workflow shown in Implementation.

   **Expected result:** both edge switches appear in Inventory as
   `Managed`, and CLI on any provisioned device confirms IS-IS adjacency:

   ```text
   EDGE-01# show isis neighbors
   ```

3. Create the fabric site over `Global/Campus/Building-A`, then assign
   fabric roles: the seed device as Control Plane + Border, and the two
   candidate devices as Edge.

4. Confirm fabric formation from the device CLI:

   ```text
   EDGE-01# show fabric edge sso summary
   EDGE-01# show lisp session
   ```

   **Expected result:** `show lisp session` on the edge node shows an
   established session to the Control Plane Node's RLOC.

5. Define a Virtual Network and assign a test wired endpoint's connected
   port on `EDGE-01` to it through Catalyst Center's Policy application,
   then confirm registration on the Control Plane Node:

   ```text
   CTRL-01# show lisp instance-id <VN_INSTANCE_ID> ipv4 server summary
   ```

   **Expected result:** the test endpoint's IP/MAC appears registered
   against `EDGE-01`'s RLOC.

6. Use Assurance's Path Trace between the test endpoint and a second
   endpoint (either in the same VN on `EDGE-02`, or an external host
   reachable through the Border Node) and review the reported path,
   including any SGACL enforcement encountered.

   **Expected result:** Path Trace reports each fabric hop, confirms
   VXLAN encapsulation/decapsulation at the edge/border nodes, and shows
   the policy (permit/deny) applied for that SGT pair.

7. **Negative test:** in Catalyst Center's Policy application, apply an
   explicit deny SGACL between the test endpoint's SGT and the second
   endpoint's SGT, then re-run Path Trace (or a live ping) between them.

   ```text
   BORDER-01# show cts role-based permissions
   ```

   **Expected result:** Path Trace (or the ping) now shows the traffic
   denied at the enforcing node, and `show cts role-based permissions`
   reflects the updated deny entry — confirming centrally authored fabric
   policy took effect without any manual per-device ACL change.

**Cleanup**

- Remove the deny SGACL added in the negative test if the fabric is
  shared with other labs.
- If the fabric site was built solely for this lab, remove the fabric
  role assignments and delete the fabric site from Catalyst Center before
  releasing the devices, then confirm each device's `show lisp session`
  and `show interface vxlan 0` no longer show fabric state.
- Release any reserved DevNet sandbox session per its posted reservation
  window.

## Summary and Completion Checklist

Catalyst Center closes the loop on this volume: it automates the
underlay, overlay, and policy that Chapters 1 through 8 built one device
and one protocol at a time, using LISP for fabric control-plane host
tracking and VXLAN to carry the same VRF/VN and SGT concepts from
Chapters 3 and 7 consistently across an entire fabric site. Assurance
then turns the telemetry surfaces from Chapter 8 into continuously
correlated health scores and path-level policy visibility, moving
day-2 operations from reactive CLI troubleshooting toward proactive,
estate-wide observability.

- [ ] Can explain Catalyst Center's role relative to direct device
      configuration covered in Chapters 1–8.
- [ ] Can describe the SD-Access fabric roles and the LISP/VXLAN
      control-plane/data-plane split.
- [ ] Can explain how SD-Access Virtual Networks and SGTs extend the
      VRF-lite and TrustSec concepts from Chapters 3 and 7.
- [ ] Can walk through the Discovery/Inventory/LAN Automation/Provision
      workflow and validate fabric state at the CLI.
- [ ] Completed the hands-on lab, including the SGACL deny negative test
      and cleanup.
