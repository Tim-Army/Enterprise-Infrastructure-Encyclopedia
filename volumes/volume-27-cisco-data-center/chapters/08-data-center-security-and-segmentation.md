# Chapter 08: Data Center Security and Segmentation

## Learning Objectives

- Apply AAA, RBAC, and management-plane hardening consistently across
  NX-OS, ACI, MDS, and UCS/Intersight
- Choose and implement segmentation at the right layer: VRFs and
  VLANs, EVPN tenancy, ACI contracts, and microsegmentation
- Protect the control plane with CoPP and the first-hop toolkit
- Secure the storage and compute planes — zoning as access control,
  KVM/CIMC discipline, firmware trust
- Audit the estate: logging, time, and configuration integrity as
  security controls

## Theory and Architecture

### The data center's security shape

Perimeter controls assume traffic crosses the perimeter; the data
center's dominant flows never do. East-west traffic between workloads
is where lateral movement lives, so data center security is
**segmentation-first**: decide which communication is legitimate and
make everything else impossible-by-default. The platforms of this
volume each offer that at different granularity, and DCCOR's Security
domain (15%) tests choosing among them as much as configuring them:

| Layer | Mechanism | Granularity |
| --- | --- | --- |
| Routing | VRF / EVPN tenant (L3VNI) | Tenant — no route, no path |
| Bridging | VLAN / VNI boundaries | Segment |
| Policy | ACI contracts between EPGs | Application tier |
| Endpoint | uSeg EPGs, attribute-based | Workload |
| Storage | VSANs and zoning | Initiator-target pair |

The pattern that scales: coarse isolation at routing (tenants that
must never touch get separate VRFs), application policy at the
contract layer, and microsegmentation reserved for the workloads
whose threat model earns its operational cost.

### Management plane: the actual keys

Every chapter has repeated it; here is the consolidated doctrine. The
management plane — NX-OS mgmt0, APIC, UCS Manager/FIs, CIMC/KVM, MDS,
NDFC, Intersight — is the highest-value target in the building,
because it configures everything else. Controls: out-of-band network,
reachable only from administration bastions; **AAA against
TACACS+/RADIUS with named accounts** and local break-glass in a
sealed-envelope process; role separation per platform (network,
compute, storage, security roles — UCS locales, ACI security domains,
NX-OS roles); session logging centralized; and certificates real, not
self-signed warnings everyone clicks through for a decade.

### Control-plane protection

Switch CPUs are finite and reachable: **CoPP** polices what punts to
the supervisor (NX-OS ships a default policy — tune, do not disable;
ACI manages its own). First-hop security at the leaf edge — DHCP
snooping, Dynamic ARP Inspection, storm control, BPDU Guard — is
Chapter 02's edge discipline reframed as security: the fabric trusts
its control plane, so protect the places untrusted hosts can inject.
Underlay and overlay protocol authentication (IGP, BGP EVPN, and vPC
peer-keepalive in its own VRF) closes the join-the-fabric attack.

### Compute and storage planes

UCS: the service-profile model means *identity is assignable* — so
RBAC over who may associate profiles is access control over what a
server *is*. KVM/CIMC sessions are console access; log and gate them
accordingly. Firmware from Cisco-signed bundles through staged host
firmware packages — supply-chain discipline at the compute layer.
Storage: zoning is the SAN's ACL (Chapter 05), default-zone deny,
port and fabric binding where the environment warrants, and the MDS
management plane on the same OOB/AAA regime as everything else.

## Design Considerations

- **Segment by blast radius, not by org chart**: the question per
  boundary is "what is contained when this side is compromised."
- **Contracts versus firewalls**: ACI contracts enforce reachability;
  they do not inspect. Traffic needing L7 inspection gets service
  graphs / PBR steering through firewalls — design where those
  chokepoints are *before* someone needs one at 2 a.m.
- **Consistency beats cleverness**: the same AAA source, logging
  targets, NTP, and banner on every platform; snowflake hardening is
  unauditable.
- **Microsegmentation is a program, not a feature flag**: it needs
  application dependency knowledge, an owner, and a rollback story.

## Implementation and Automation

NX-OS hardening baseline (the pattern; render it with Chapter 06
tooling so it is *provably* everywhere):

```text
! AAA with fallback
feature tacacs+
tacacs-server host 10.10.10.10 key 7 "…"
aaa group server tacacs+ TACS
  server 10.10.10.10
  use-vrf management
aaa authentication login default group TACS local
aaa accounting default group TACS

! Management access
ip access-list MGMT-ONLY
  permit tcp 10.10.0.0/24 any eq 22
  deny ip any any log
line vty
  access-class MGMT-ONLY in
ssh key rsa 2048
no feature telnet

! Edge protection on host ports
interface e1/10
  spanning-tree bpduguard enable
  storm-control broadcast level 1.00

! Control plane: verify, then tune
show copp status
show policy-map interface control-plane | include class|violate
```

ACI security posture checks via API (Chapter 03's tongue):

```text
GET /api/class/aaaUser.json                       ! local accounts audit
GET /api/class/vzBrCP.json?rsp-subtree=full       ! contract inventory
GET /api/class/fvRsDomAtt.json                    ! EPG-domain exposure
# uSeg EPG: attribute-based membership (VM name, IP, MAC) — policy
# follows the workload, not the port.
```

## Validation and Troubleshooting

Security validation is proving the negative: from a workload segment,
demonstrate that cross-tenant routes are absent (`show ip route vrf`),
that non-contracted flows drop (attempt + zoning-rule hit counters on
the leaf), that management interfaces are unreachable from workload
space (scan from a workload VM — expect silence), and that AAA
fallback works by testing break-glass *in a window, deliberately*.
Troubleshooting security is usually troubleshooting over-blocking:
the method is the same ladder as ever, plus reading enforcement
artifacts — contract hit counters, CoPP violate counters (legitimate
protocol punts being policed shows as flapping adjacencies under
load), and DAI/snooping drops (a "broken" server that is actually a
static-IP host missing from the binding table).

## Security and Best Practices

This chapter *is* the practices; the meta-practices that keep it
true: hardening rendered by automation and verified by drift
detection (a control that decays silently is not a control);
quarterly access recertification for the management plane; logging
with synchronized time (forensics dies without NTP discipline); and
change artifacts for every security-relevant modification — the
Chapter 06 habit, applied where auditors care most.

## References and Knowledge Checks

- Cisco NX-OS security configuration guide; ACI security white papers
- DCCOR 350-601 v1.2 Security domain (15%); DCACI ACI Management
  domain (20%)
- CIS-style hardening references for platform baselines

Knowledge checks:

1. Rank VRF isolation, contracts, and uSeg EPGs by granularity and by
   operational cost, and give a workload class appropriate to each.
2. Why must the vPC peer-keepalive live outside the paths it
   arbitrates, and what attack does keepalive isolation also blunt?
3. CoPP violate counters climb during a routing convergence event.
   What is happening, and what is the correct response (and the
   wrong one)?
4. Prove-the-negative: name three artifacts that demonstrate
   segmentation is working without waiting for an incident.

## Hands-On Lab

Harden the volume's running estate: render the NX-OS baseline via the
Chapter 06 role onto all fabric nodes (idempotent, assert-checked);
configure TACACS+ (or the lab's AAA stand-in) with a tested
break-glass; enable BPDU Guard/storm control on host ports and
demonstrate a violation event; in the ACI sandbox, create a uSeg EPG
that captures a workload by attribute and prove policy followed it;
and produce the prove-the-negative artifact set — cross-VRF route
absence, contract drop counters, and a management-plane scan from
workload space showing nothing listening.

## Lab Verification

Verification means the baseline rendered fleet-wide by automation,
the violation and uSeg captures behaved as designed, and the
negative-proof artifacts exist and say what they must. Until then,
the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Data center security is segmentation chosen at the right layer,
management planes treated as the crown jewels they are, control
planes policed, and every hardening decision rendered by automation
so it is uniformly, provably true. The platforms differ; the doctrine
does not — and the exam's security questions across DCCOR and DCACI
reward exactly that consolidation.

- [ ] I can choose the segmentation layer per workload class and
      defend the choice
- [ ] My management-plane doctrine is one page and true on every
      platform
- [ ] My hardening is rendered, not typed, and drift-checked
- [ ] I can prove the negative with named artifacts
