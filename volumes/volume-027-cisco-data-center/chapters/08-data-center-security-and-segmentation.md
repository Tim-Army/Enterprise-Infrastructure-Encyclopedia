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

This chapter carries a topic-level walkthrough lab for **every objective in
Domain 5 (Security) of the DCCOR 350-601 v1.2 exam guide** — network, compute,
and storage security — mapped in the volume README's coverage tables. Labs use
the NX-OS, UCS, and MDS CLIs. Each ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 8.1–8.3** — the fabric from earlier chapters
(Nexus leaves, a UCS domain, an MDS/FC fabric), management reachability, and
admin credentials. **Cost:** none beyond lab resources.

### Lab 8.1 — Apply network security (Objective 5.1)

**Objective:** Enforce a control-plane and data-plane guard on a Nexus leaf —
CoPP and a port ACL — and confirm the fabric-facing hardening.

```text
show policy-map interface control-plane | include "class-map|dropped"
show access-lists summary
config t
 ip access-list HOST-IN
  10 permit ip 10.20.1.0/24 any
  20 deny ip any any log
 interface ethernet 1/10
  ip port access-group HOST-IN in
end
show ip access-lists HOST-IN
```

**Expected result:** CoPP classes protecting the supervisor with drop counters
under attack, and the port ACL permitting only the host subnet — the two layers
that protect the control plane and segment the data plane on a leaf.

**Negative test:** source traffic from outside `10.20.1.0/24`; ACL entry 20
drops and logs it — the default-deny is what makes the ACL a control, not a
comment.

**Cleanup:** remove `HOST-IN` from the interface and delete the ACL.

### Lab 8.2 — Apply compute security (Objective 5.2)

**Objective:** Harden the UCS management plane — RBAC, secure protocols, and
KVM/IPMI restrictions.

```text
scope security
 show authentication
 show role
scope system
 scope services
  show telnet   ! should be disabled
  show ssh-server
```

**Expected result:** authentication bound to a AAA/LDAP realm, roles scoped to
least privilege, Telnet disabled, and SSH enabled — the UCS management-plane
hardening that protects service-profile and firmware operations.

**Negative test:** enable Telnet (`scope services ; enable telnet`); management
credentials now traverse in clear text — the negative shows why only SSH/HTTPS
belong on the management plane. Disable it again immediately.

**Cleanup:** confirm Telnet remains disabled; revert any test change.

### Lab 8.3 — Apply storage security (Objective 5.3)

**Objective:** Verify SAN access controls — single-initiator zoning, port
security, and (optionally) FC-SP authentication.

```text
show zoneset active vsan 100 | include "zone name|pwwn"
show port-security status vsan 100
show fcsp interface fc1/1 2>/dev/null || show fcsp database
```

**Expected result:** single-initiator zones (one host pWWN per zone), port
security binding devices to ports, and FC-SP/DHCHAP authenticating the ISL or
host — the layered SAN access model (zoning + port security + authentication).

**Negative test:** add a second initiator to an existing zone; hosts can now
see each other's targets — the multi-initiator zone is the classic storage
security anti-pattern this objective tests.

**Cleanup:** restore single-initiator zoning; remove any test port-security
entries.

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
