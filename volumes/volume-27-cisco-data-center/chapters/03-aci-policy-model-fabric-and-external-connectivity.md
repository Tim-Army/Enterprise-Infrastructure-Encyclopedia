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
DCAUTO exam also expects (abbreviated):

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

On the DevNet always-on APIC sandbox (or ACI Simulator): build
TENANT-A with VRF, two BDs with gateways, WEB and APP EPGs, and a
contract permitting only TCP/8080 WEB→APP. Verify with the EP tracker
and the leaf zoning-rule table that the contract rendered. Add an
L3Out simulation (static route external EPG) and attach a contract to
expose WEB externally. Then reproduce the two classic faults: delete
the contract and capture the drop plus the zoning-rule change; remove
the EPG's domain association and capture the fault the APIC raises.
Export the tenant configuration as JSON — it becomes Chapter 06's
automation input.

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
