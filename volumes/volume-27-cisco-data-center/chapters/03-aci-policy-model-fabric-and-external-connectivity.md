# Chapter 03: ACI: Policy Model, Fabric Operations, and External Connectivity

## Learning Objectives

- Explain ACI's policy model — tenants, VRFs, bridge domains, EPGs,
  and contracts — and how it replaces device configuration with intent
- Describe fabric discovery, APIC clustering, and what the controller
  does and deliberately does not do
- Trace packet forwarding through an ACI fabric, including the roles of
  the TEP pool, COOP, and the spine proxy
- Connect the fabric outward with L2Outs and L3Outs, and integrate
  VMM domains
- Operate the fabric: faults, snapshots, upgrades, and the management
  practices DCACI weights at 20%

## Theory and Architecture

### The inversion: policy first, network rendered

ACI turns the operating model of Chapter 02 inside out. In an NX-OS
fabric you configure devices until the network expresses your intent.
In ACI you express intent as policy objects on the **APIC**, and the
fabric renders it: VLANs, VRFs, SVIs, and zoning rules appear on leaves
as consequences, not as things you typed. The exam's language is the
object tree, and fluency in it is non-negotiable:

- **Tenant** — the administrative container; `common` holds shared
  services, `infra` the fabric's own plumbing, `mgmt` management.
- **VRF (context)** — a routing space within a tenant.
- **Bridge domain (BD)** — a Layer 2 flood boundary with optional
  gateway SVIs; deliberately *not* a VLAN, though VLANs get consumed
  encapsulating traffic toward it.
- **EPG** — the endpoint group, ACI's atom of policy: a set of
  endpoints with identical policy needs, attached to one BD.
- **Contract** — the permission for EPG-to-EPG communication. Without
  a contract (or explicit exceptions like vzAny or preferred groups),
  inter-EPG traffic does not pass. The default is deny.

The security consequence deserves emphasis: **an ACI fabric is a
zero-trust segmentation engine by default**, which is why DCACI and the
Chapter 08 security story overlap.

### What the fabric itself does

The underlay is built for you: leaves and spines discover via LLDP,
receive addresses from the APIC's **TEP pool**, and form an IS-IS
routed infrastructure carrying VXLAN — the same encapsulation as
Chapter 02 with a different control plane. Endpoint learning is
centralized in **COOP** on the spines: every leaf reports local
endpoints, and unknown-destination traffic goes to the **spine proxy**
rather than flooding. The APIC cluster (three controllers in
production) holds policy and health but sits **out of the data plane**
— a fabric forwards happily with every APIC down, which is both a
resilience property and an exam question.

### Reaching the world: L3Out and friends

External routed connectivity is an **L3Out**: border leaves peer with
outside routers (OSPF, BGP, EIGRP, or static), external prefixes are
classified into an **external EPG**, and — the perennially forgotten
step — a contract between the external EPG and internal EPGs actually
permits the traffic. Transit routing between two L3Outs works but must
be designed, not assumed. Layer 2 extension uses static path bindings
or an L2Out; **ACI Anywhere** (the DCACI 10% domain) extends policy to
remote leaves, multiple pods sharing one APIC cluster (Multi-Pod), and
fully separate fabrics stitched by the Nexus Dashboard Orchestrator
(Multi-Site).

### VMM integration

A **VMM domain** connects the APIC to vCenter (or other managers): the
APIC creates a distributed port group per EPG, learns where VMs sit,
and pushes policy to the right leaf when a VM moves. Integration is
what converts ACI from a network that hosts virtualization into one
that tracks it.

## Design Considerations

- **Model tenants around administration, not org charts.** A tenant is
  a policy and RBAC boundary; dozens of near-empty tenants create
  contract sprawl across `common`.
- **One BD per EPG is the simple, debuggable default.** Multiple EPGs
  per BD is legitimate for microsegmentation but complicates flood
  behavior reasoning.
- **Decide the contract philosophy early**: strict per-service
  contracts (maximum control, maximum objects) versus coarse
  allow-groups with vzAny (operable, less granular). Retrofitting
  strictness later is the painful direction.
- **Border leaf pairs, not border everywhere**; keep L3Out policy
  concentrated and symmetrical.

## Implementation and Automation

ACI work is done against the APIC — UI for learning, API for
everything repeated. The canonical objects, as the REST payloads the
DCNAUTO exam also expects (abbreviated):

```json
POST /api/mo/uni.json
{ "fvTenant": { "attributes": { "name": "TENANT-A" }, "children": [
  { "fvCtx": { "attributes": { "name": "VRF-A" } } },
  { "fvBD": { "attributes": { "name": "BD-WEB" }, "children": [
      { "fvRsCtx": { "attributes": { "tnFvCtxName": "VRF-A" } } },
      { "fvSubnet": { "attributes": { "ip": "10.30.1.1/24" } } } ] } },
  { "fvAp": { "attributes": { "name": "APP1" }, "children": [
      { "fvAEPg": { "attributes": { "name": "WEB" }, "children": [
          { "fvRsBd": { "attributes": { "tnFvBDName": "BD-WEB" } } } ] } } ] } }
] } }
```

Contracts follow the same pattern (`vzBrCP`, `vzSubj`, `vzFilter`),
consumed and provided by EPGs. In the lab you will click these once,
then script them with the API and never click them again — which is
the honest description of ACI operations at scale.

Fabric operations essentials:

```text
# Configuration snapshots before every change window (UI or API):
POST /api/mo/uni/fabric/configexp-defaultOneTime.json
# Faults are the fabric telling you what it could not render:
GET /api/class/faultInst.json?query-target-filter=eq(faultInst.severity,"critical")
```

## Validation and Troubleshooting

ACI troubleshooting starts from **faults, not symptoms**: the APIC
raises a fault against the exact object it failed to render, with a
code you can look up. The workflow: check faults on the involved
objects, verify the endpoint is learned (`show endpoint` on the leaf,
or the EP tracker), verify contract programming (zoning-rule table on
the leaf: `show zoning-rule scope <vrf-scope>`), then use the built-in
**Visibility & Troubleshooting** tool to trace the pair. The classic
failures: traffic dropped because a contract is missing or attached in
the wrong direction (provider/consumer inverted); an endpoint never
learned because the domain-to-EPG association or VLAN pool omits the
encapsulation; an L3Out that peers correctly but passes nothing
because the external EPG has no contract or its subnet scope flags are
wrong.

## Security and Best Practices

- The default-deny contract model is the segmentation design — resist
  the "permit-any contract everywhere" anti-pattern that converts ACI
  into an expensive VLAN fabric.
- RBAC by tenant with security domains; the APIC is the keys to
  everything, so its AAA (TACACS+/RADIUS), certificate hygiene, and
  audit log retention are Chapter 08 material applied here.
- Snapshots before changes, config-export to off-fabric storage on a
  schedule, and an upgrade cadence that follows Cisco's recommended
  releases — fabric-wide upgrades are routine in ACI, and fear of them
  is how estates end up years behind.

## References and Knowledge Checks

- Cisco ACI fundamentals and policy model documentation (APIC
  configuration guides)
- DCACI 300-620 v1.2 exam topics — note the 20% weights on fabric
  infrastructure, external connectivity, and management
- Cisco DevNet ACI sandboxes and the always-on APIC

Knowledge checks:

1. Two EPGs share a bridge domain. Can their endpoints communicate
   without a contract? Explain precisely what the default permits.
2. All three APICs are unreachable. What happens to forwarding, and
   what can you no longer do?
3. An L3Out's OSPF adjacency is full but external users cannot reach
   the WEB EPG. Name the two most likely missing objects.
4. What problem does the spine proxy solve that flood-and-learn VXLAN
   could not?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every objective in
the DCACI 300-620 v1.2 exam guide** — all six domains, from fabric
infrastructure through ACI Anywhere — mapped in the volume README's coverage
tables. Labs use the APIC CLI (`moquery`), the APIC REST API (`icurl` on the
controller, `curl` remotely), and the object model. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.21** — an ACI fabric with at least one
APIC reachable at `$APIC`, two leaves and one spine discovered, an API token
in `$TOK` (from `aaaLogin`), and a VMM domain (vCenter) for the integration
labs. `icurl` runs on the APIC; remote calls use `curl -k`. **Cost:** none
beyond lab resources.

### Lab 3.1 — Describe ACI architecture (Objective 1.1)

**Objective:** Read the fabric's node inventory (spines, leaves, APICs).

```text
moquery -c fabricNode | egrep 'name|role|model' | head
```

**Expected result:** each node with `role` of `spine`, `leaf`, or
`controller` — the Clos fabric where policy lives on the APIC cluster and is
rendered into leaf/spine hardware.

**Negative test:** `moquery -c fabricNode -f 'fabric.Node.role=="border"'`
returns nothing — roles are a closed set; there is no "border" node role in
ACI (border leaves are ordinary leaves with an L3Out).

**Cleanup:** none (read-only).

### Lab 3.2 — Describe the ACI Object Model (Objective 1.2)

**Objective:** Walk the Management Information Tree (MIT) from a tenant down.

```text
moquery -c fvTenant -f 'fv.Tenant.name=="PROD"'
moquery -c fvAEPg | grep dn | head
```

**Expected result:** the tenant object and the distinguished names (`dn`) of
its EPGs, e.g. `uni/tn-PROD/ap-APP/epg-WEB` — every ACI object has a unique
`dn` locating it in the tree.

**Negative test:** query a class name with a typo (an extra letter); the APIC
returns an error, not an empty set — the class must exist in the model.

**Cleanup:** none (read-only).

### Lab 3.3 — Utilize faults, events, audit log, and health score (Objective 1.3)

**Objective:** Read active faults and the fabric health score.

```text
moquery -c faultInst -f 'fault.Inst.severity=="critical"' | grep -E 'descr|dn' | head
moquery -c fabricHealthTotal
```

**Expected result:** any critical faults with their `dn` and description, and
the overall health score (0–100) — ACI's built-in operational telemetry, no
external NMS required.

**Negative test:** disable an interface bound to an EPG; within seconds a
fault appears and the affected object's health score drops — faults are
event-driven, not polled.

**Cleanup:** re-enable the interface; confirm the fault clears and health
recovers.

### Lab 3.4 — Describe ACI fabric discovery (Objective 1.4)

**Objective:** Confirm nodes were discovered and registered via LLDP/DHCP.

```text
moquery -c dhcpClient | egrep 'name|nodeRole|state' | head
moquery -c fabricNode -f 'fabric.Node.fabricSt=="active"' | grep -c dn
```

**Expected result:** discovered nodes in `state: assigned` with a fabric
membership, and the count of `active` nodes — the APIC discovers the fabric
through LLDP neighbors and infra-VLAN DHCP.

**Negative test:** a node cabled but not registered shows `state: unsupported`
or missing from `fabricNode` until you accept it — discovery proposes,
the admin registers.

**Cleanup:** none (read-only).

### Lab 3.5 — Implement ACI policies (Objective 1.5)

**Objective:** Create a tenant with an application profile via REST.

```text
icurl -k -X POST 'https://localhost/api/mo/uni.json' -d '
{"fvTenant":{"attributes":{"name":"LAB"},"children":[
 {"fvAp":{"attributes":{"name":"APP"}}}]}}'
moquery -c fvAp -f 'fv.Ap.name=="APP"'
```

**Expected result:** the POST returns `imdata: []` (success) and the app
profile is queryable under `uni/tn-LAB/ap-APP` — policy created declaratively.

**Negative test:** POST the same tenant with an illegal name (spaces); the
APIC rejects it with a naming-policy error — the model enforces object naming.

**Cleanup:** `icurl -k -X POST 'https://localhost/api/mo/uni/tn-LAB.json' -d
'{"fvTenant":{"attributes":{"name":"LAB","status":"deleted"}}}'`.

### Lab 3.6 — Implement ACI logical constructs (Objective 1.6)

**Objective:** Build the EPG → BD → VRF chain a workload needs.

```text
icurl -k -X POST 'https://localhost/api/mo/uni/tn-LAB.json' -d '
{"fvTenant":{"attributes":{"name":"LAB"},"children":[
 {"fvCtx":{"attributes":{"name":"VRF1"}}},
 {"fvBD":{"attributes":{"name":"BD1"},"children":[
   {"fvRsCtx":{"attributes":{"tnFvCtxName":"VRF1"}}}]}},
 {"fvAp":{"attributes":{"name":"APP"},"children":[
   {"fvAEPg":{"attributes":{"name":"WEB"},"children":[
     {"fvRsBd":{"attributes":{"tnFvBDName":"BD1"}}}]}}]}}]}}'
moquery -c fvRsBd -f 'fv.RsBd.tnFvBDName=="BD1"'
```

**Expected result:** the EPG `WEB` bound to `BD1`, which is bound to `VRF1` —
the endpoint/bridge-domain/context hierarchy that replaces VLAN/SVI/VRF.

**Negative test:** create an EPG whose `fvRsBd` names a nonexistent BD; a
fault (`resolvable`) appears until the BD exists — ACI relationships are
validated.

**Cleanup:** delete tenant `LAB` as in Lab 3.5.

### Lab 3.7 — Describe endpoint learning (Objective 2.1)

**Objective:** Read a learned endpoint's MAC/IP and its location.

```text
moquery -c fvCEp | egrep 'mac|ip|dn' | head
moquery -c fvRsCEpToPathEp | grep tDn | head
```

**Expected result:** endpoints (`fvCEp`) with MAC, IP, and the path
(leaf/port) where they were learned — the COOP database the spines maintain.

**Negative test:** move a host to another leaf and re-query; the path updates
and the stale entry ages out — endpoint moves are learned, not flooded.

**Cleanup:** none (read-only).

### Lab 3.8 — Implement bridge domain settings (Objective 2.2)

**Objective:** Tune a BD's unicast routing and flooding behavior.

```text
icurl -k -X POST 'https://localhost/api/mo/uni/tn-LAB/BD-BD1.json' -d '
{"fvBD":{"attributes":{"name":"BD1","unicastRoute":"yes",
 "arpFlood":"no","unkMacUcastAct":"proxy"}}}'
moquery -c fvBD -f 'fv.BD.name=="BD1"' | egrep 'arpFlood|unkMacUcastAct|unicastRoute'
```

**Expected result:** `unicastRoute: yes`, `arpFlood: no`, and
`unkMacUcastAct: proxy` — the spine-proxy hardware forwarding that avoids
flooding unknown unicast.

**Negative test:** set `unkMacUcastAct: flood` with a silent host; traffic
floods the BD instead of using the proxy — the setting directly changes
forwarding.

**Cleanup:** restore defaults or delete tenant `LAB`.

### Lab 3.9 — Implement Layer 2 connectivity (Objective 3.1)

**Objective:** Bind an EPG to a leaf port (static path) for L2.

```text
icurl -k -X POST 'https://localhost/api/mo/uni/tn-LAB/ap-APP/epg-WEB.json' -d '
{"fvRsPathAtt":{"attributes":{"tDn":"topology/pod-1/paths-101/pathep-[eth1/5]",
 "encap":"vlan-100","mode":"regular"}}}'
moquery -c fvRsPathAtt -f 'fv.RsPathAtt.encap=="vlan-100"'
```

**Expected result:** the static binding mapping VLAN 100 on leaf 101 eth1/5
into EPG `WEB` — the point where a physical port joins the policy fabric.

**Negative test:** bind the same encap to a second EPG on the same port
without a valid VLAN pool; the APIC raises an encap-overlap fault.

**Cleanup:** delete the `fvRsPathAtt`, or delete tenant `LAB`.

### Lab 3.10 — Implement Layer 3 Out (Objective 3.2)

**Objective:** Read an L3Out and its external EPG (routed edge).

```text
moquery -c l3extOut | grep dn | head
moquery -c l3extInstP | egrep 'name|dn' | head
moquery -c l3extSubnet | grep ip | head
```

**Expected result:** the L3Out, its external EPG (`l3extInstP`), and the
external subnets classified into it — how ACI advertises and classifies
outside routes (transit routing and VRF route leaking excluded per the
blueprint).

**Negative test:** an external subnet with no scope flag matches nothing;
traffic is not classified into the external EPG until `import-security` (or
the appropriate scope) is set.

**Cleanup:** none (read-only).

### Lab 3.11 — Implement virtual networking integration (Objective 4.1)

**Objective:** Confirm the VMM domain pushed a port group to vCenter.

```text
moquery -c vmmDomP | grep name
moquery -c compVm | egrep 'name|state' | head
```

**Expected result:** the VMM domain and the discovered VMs — ACI created a
distributed port group in vCenter for each EPG associated with the domain.

**Negative test:** associate an EPG to the VMM domain but leave the VM's vNIC
on the old port group; the endpoint never appears in `fvCEp` — attachment
requires the vNIC on the ACI-created port group.

**Cleanup:** remove the test EPG-to-VMM association.

### Lab 3.12 — Describe resolution and deployment immediacy in VMM (Objective 4.2)

**Objective:** Read the immediacy settings that control policy push timing.

```text
moquery -c fvRsDomAtt | egrep 'resImedcy|instrImedcy|tDn' | head
```

**Expected result:** `resImedcy` (pre-provision / immediate / on-demand) and
`instrImedcy` — resolution immediacy decides when policy is downloaded to the
leaf; deployment immediacy decides when it is programmed into hardware.

**Negative test:** with `on-demand` resolution and no attached endpoint, the
VLAN is not programmed on the leaf; `show vlan extended` on the leaf omits it
until a VM attaches — immediacy is why.

**Cleanup:** none (read-only).

### Lab 3.13 — Implement a service graph (Objective 4.3)

**Objective:** Read a deployed service graph (firewall insertion).

```text
moquery -c vnsAbsGraph | grep name
moquery -c vnsGraphInst | egrep 'name|configSt' | head
```

**Expected result:** the abstract graph and its rendered instance in
`configSt: applied` — a firewall or load balancer inserted between EPGs by
policy, not by cabling.

**Negative test:** apply a contract with a graph whose device cluster is
down; the graph instance shows `configSt: failed` with a fault — insertion
depends on a healthy service device.

**Cleanup:** none (read-only).

### Lab 3.14 — Implement out-of-band and in-band management (Objective 5.1)

**Objective:** Read the OOB and in-band management EPGs and node addresses.

```text
moquery -c mgmtRsOoBStNode | grep addr | head
moquery -c mgmtInB
```

**Expected result:** each node's OOB address (via `mgmt` tenant's OOB EPG) and
the in-band EPG if configured — the two management planes ACI separates.

**Negative test:** remove an OOB contract; management reachability to that
node over OOB stops while the fabric data plane is unaffected — the planes are
independent.

**Cleanup:** restore the OOB contract.

### Lab 3.15 — Utilize traditional and AI-assisted monitoring tools (Objective 5.2)

**Objective:** Export fabric telemetry to Nexus Dashboard Insights.

```text
moquery -c telemetryFtriggerConfig 2>/dev/null | head
curl -sk -b cookie.txt "https://$ND/sedgeapi/v1/cisco-nir/api/api/telemetry/v2/anomalies/summary" | jq '.totalItemsCount'
```

**Expected result:** the anomaly count from Nexus Dashboard Insights — the
AI-assisted layer that flags fabric anomalies traditional faults miss.

**Negative test:** query before onboarding the fabric to Insights; the API
returns no data — AI assistance requires the fabric be onboarded and
streaming.

**Cleanup:** none (read-only).

### Lab 3.16 — Implement configuration backup (Objective 5.3)

**Objective:** Take a config snapshot and confirm it can be exported.

```text
icurl -k -X POST 'https://localhost/api/mo/uni/fabric.json' -d '
{"configExportP":{"attributes":{"name":"snap-lab","adminSt":"triggered",
 "format":"json","snapshot":"yes"}}}'
moquery -c configSnapshot | grep fileName | tail -3
```

**Expected result:** a new snapshot with a timestamped filename — the
point-in-time backup you can roll back to or export off-box.

**Negative test:** trigger an export to a remote path with wrong credentials;
`moquery -c configJob` shows the job `failed` — verify the remote location
before relying on off-box backups.

**Cleanup:** delete the snapshot via its `configSnapshot` object.

### Lab 3.17 — Implement AAA and RBAC (Objective 5.4)

**Objective:** Create a security domain and a restricted local user.

```text
icurl -k -X POST 'https://localhost/api/mo/uni/userext.json' -d '
{"aaaUser":{"attributes":{"name":"neteng","pwd":"C1sco12345!"},"children":[
 {"aaaUserDomain":{"attributes":{"name":"LAB-DOM"},"children":[
   {"aaaUserRole":{"attributes":{"name":"tenant-admin","privType":"writePriv"}}}]}}]}}'
moquery -c aaaUser -f 'aaa.User.name=="neteng"'
```

**Expected result:** the user scoped to `LAB-DOM` with `tenant-admin` write
privileges — RBAC confines the user to objects tagged with that security
domain.

**Negative test:** log in as `neteng` and query a tenant outside `LAB-DOM`;
the APIC returns no objects — the domain boundary is enforced.

**Cleanup:** delete the `aaaUser`.

### Lab 3.18 — Configure an upgrade (Objective 5.5)

**Objective:** Read the firmware/maintenance policy that stages an upgrade.

```text
moquery -c firmwareFwP
moquery -c maintMaintP | egrep 'name|adminSt'
moquery -c maintUpgJob | egrep 'desiredVersion|upgradeStatus' | head
```

**Expected result:** the target firmware version and maintenance group state —
ACI upgrades by group with a scheduler, keeping the fabric forwarding through
a rolling upgrade.

**Negative test:** put every leaf in one maintenance group; a simultaneous
upgrade risks a forwarding outage — the negative shows why groups exist.

**Cleanup:** none (read-only).

### Lab 3.19 — Describe Multi-Pod (Objective 6.1)

**Objective:** Read the pods and the inter-pod network (IPN) peering.

```text
moquery -c fabricPod | grep dn
moquery -c fvPodConnP 2>/dev/null | head
```

**Expected result:** more than one `fabricPod` and the pod-connection profile
— Multi-Pod is one APIC cluster across pods joined by an IPN, a single
availability zone.

**Negative test:** a single-pod fabric returns exactly one `fabricPod`; the
Multi-Pod constructs are absent — the topology dictates the objects.

**Cleanup:** none (read-only).

### Lab 3.20 — Describe Multi-Site (Objective 6.2)

**Objective:** Read the site registration in Nexus Dashboard Orchestrator.

```text
curl -sk -b cookie.txt "https://$ND/mso/api/v1/sites" | jq -r '.sites[] | "\(.name) \(.status)"'
```

**Expected result:** each ACI site registered to the Orchestrator — Multi-Site
is separate APIC clusters (separate availability zones) with policy stitched
by NDO, unlike Multi-Pod's single cluster.

**Negative test:** query before adding a site; the `sites` array is empty —
NDO orchestrates only registered sites.

**Cleanup:** none (read-only).

### Lab 3.21 — Describe Remote Leaf (Objective 6.3)

**Objective:** Read a remote-leaf's association to its pod over the WAN.

```text
moquery -c fabricNode -f 'fabric.Node.role=="remote-leaf-wan" or fabric.Node.nodeType=="remote-leaf-wan"' 2>/dev/null
moquery -c tunnelIf | grep -i dci | head
```

**Expected result:** the remote leaf attached to a main pod's spines across a
routed WAN — extending the fabric to a satellite location without a local
spine.

**Negative test:** a remote leaf whose IPN/underlay to the spines is down
falls out of the fabric; `fabricNode` shows it inactive — remote leaves depend
on the WAN underlay.

**Cleanup:** none (read-only).

## Lab Verification

Verification means the contract-scoped flow passed, both induced
faults were observed with their fault codes, and the tenant JSON
export re-imports cleanly. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

ACI renders intent: tenants, BDs, EPGs, and contracts describe what
should communicate, and the fabric — TEP underlay, COOP learning,
spine proxy — makes it so, deny-by-default. External reachability is
policy (L3Out plus contract), virtualization is tracked through VMM
domains, and operations revolve around faults, snapshots, and
disciplined upgrades. It is the deepest single-exam mapping in this
volume: all six DCACI domains land here.

- [ ] I can walk the object tree from tenant to contract from memory
- [ ] I can trace an inter-EPG packet, including the proxy path
- [ ] My lab enforced, broke, and re-enforced a contract with evidence
- [ ] I can name what survives (and what stops) when APICs are down
