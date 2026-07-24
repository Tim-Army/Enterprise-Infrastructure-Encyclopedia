# Chapter 09: Design, Troubleshooting, and Certification Readiness

## Learning Objectives

- Apply a requirements-driven design method to data center projects,
  producing decisions that trace to constraints — DCID's discipline
- Run a structured troubleshooting methodology across network,
  compute, and storage, with evidence at every elimination — DCIT's
  discipline
- Operate the estate on purpose: upgrades, capacity, configuration
  management, and the management-and-operations practices DCIT
  weights at 20%
- Assemble a personal readiness plan for DCCOR and your chosen
  concentration, aligned to the verified blueprint weights

## Theory and Architecture

### Design as constraint satisfaction

DCID's four domains — network design 35%, compute 25%, storage 20%,
automation 20% — share one method. Gather **requirements**
(applications, growth, availability targets, compliance); surface
**constraints** (budget, facilities power/cooling — decisive since
Chapter 07 — existing estate, team skills); then make **traceable
decisions**. A design decision without a requirement behind it is
taste; the exam's scenario questions and real design reviews both
probe for the trace.

The recurring data center decisions, with their tension named:

- **ACI versus NX-OS/NDFC fabric**: policy model and integrations
  versus operational transparency and team familiarity. The deciding
  requirement is usually operational: who runs it, and what do they
  need to see?
- **Oversubscription ratios**: cost versus the applications' real
  concurrency — 3:1 general purpose, tighter for storage-heavy, 1:1
  for AI backends (Chapter 07's arithmetic).
- **Scale-up versus scale-out compute**: fewer bigger nodes (license
  economics, blast radius) versus more smaller ones (failure
  granularity, scheduling freedom).
- **Where inspection lives**: contracts/enforcement in-fabric versus
  service-graph steering through firewalls — decided by compliance
  requirements, not preference (Chapter 08).
- **Multi-site model**: EVPN Multi-Site or ACI Multi-Site for
  active-active tenancy, versus DR-oriented designs; RPO/RTO
  requirements decide, and they must be written down first.

### Troubleshooting as hypothesis elimination

DCIT's method, generalized from the ladders every chapter built:
**define the failure precisely** (who, to what, since when, what
changed); **draw the path** — for a data center flow that means
host → vNIC/profile → leaf → fabric → policy layer → storage or
peer; **split the path** at the easiest observable point and prove
each half; **consult the system's own diagnosis first** (ACI faults,
UCS FSM, FLOGI/FCNS, EVPN route presence — this volume's platforms
narrate their failures); and **change one thing**, verifying after.
The discipline that separates professionals: evidence at each step —
the counters, route entries, or fault codes that eliminated a layer —
because evidence survives handoffs and postmortems, and hunches do
not.

### Operations as a designed system

DCIT's Management and Operations domain (20%) is the chapter's third
leg. Upgrades: staged, rehearsed on virtual twins (CML, ACI
Simulator), rolled by automation with health asserts between waves —
ISSU where supported, maintenance-mode drains where not. Capacity:
watched as trends (telemetry into time series), acted on before the
fabric teaches the lesson. Configuration: rendered from source of
truth, drift-detected, snapshotted before every window (APIC
config-export, NX-OS checkpoints, UCS backups — all automatable, so
all automated). Incident practice: runbooks per failure class
(Chapters 02–08 each produced entries), postmortems that feed the
runbooks, and the on-call rotation actually drilled on the
break-glass path.

## Design Considerations

This section, unusually, is the chapter: the design method above
applied as a checklist for any new data center project —
requirements written and signed, constraints surfaced early
(facilities first for AI), decisions traced, failure domains drawn
on the diagram, operational model chosen with the team that will run
it, and day-2 tooling (telemetry, automation, backups) in the design
rather than appended after go-live.

## Implementation and Automation

The rehearsal pattern that makes upgrades boring, expressed as
pipeline stages (Chapter 06 tooling):

```yaml
# upgrade-wave.yml (conceptual stages)
- stage: preflight
  checks: [snapshot_taken, evpn_peers_established, vpc_consistent,
           faults_below_threshold, backup_verified]
- stage: drain
  action: maintenance-mode isolate {{ node }}     # GIR on NX-OS
- stage: upgrade
  action: install nxos {{ target_image }}
- stage: verify
  checks: [version_matches, evpn_peers_established, endpoints_relearned,
           copp_violations_flat]
- stage: restore
  action: maintenance-mode insert {{ node }}
- stage: soak
  wait: 30m
  checks: [no_new_faults, telemetry_deltas_nominal]
```

NX-OS Graceful Insertion and Removal (GIR) is the drain primitive:

```text
system mode maintenance      ! isolate: protocols withdraw gracefully
show system mode
system mode normal           ! reinsert after verification
```

Snapshot and checkpoint primitives worth muscle memory:

```text
checkpoint pre-change        ! NX-OS local checkpoint
rollback running-config checkpoint pre-change
show diff rollback-patch checkpoint pre-change running-config
```

## Validation and Troubleshooting

A worked elimination, the volume's flows in one scenario — "app tier
cannot reach its database, started 09:12": define (one EPG pair, all
endpoints, after a change window); path (VM → vNIC → leaf →
contract → leaf → VM); system's own diagnosis first — APIC faults
show a contract render failure on one leaf (fault code against the
zoning rule); evidence — `show zoning-rule` on that leaf missing the
entry present on its peers; cause — last night's automation ran
against a leaf mid-upgrade and skipped its assert (the Chapter 06
post-condition existed and was ignored — process failure, not tool
failure); fix — re-run render on that leaf, verify rule presence and
hit counters, then fix the pipeline so asserts gate the change
record. The postmortem writes itself because every step left
evidence — which is the point of the method.

## Security and Best Practices

- Rehearsed rollback is a security control: the fastest way out of a
  bad change is the difference between an incident and an outage.
- Upgrade currency is vulnerability management for infrastructure —
  the estate that fears its upgrade process accumulates CVEs with
  its technical debt (Chapter 03's ACI note, generalized).
- Evidence discipline doubles as audit readiness; the same artifacts
  serve postmortems and compliance.

## References and Knowledge Checks

- DCID 300-610 v1.2, DCIT 300-615 v1.2 exam topics (the method
  chapters' blueprints)
- Cisco NX-OS GIR and ISSU documentation; ACI upgrade guides
- This volume's chapters 02–08 runbook entries

Knowledge checks:

1. A design review asks for 1:1 oversubscription on a
   general-purpose fabric "to be safe." Argue from requirements —
   both the case against and the single workload class that changes
   the answer.
2. Name the drain-verify-restore primitives on NX-OS and in ACI
   terms, and where health asserts belong in the wave.
3. In the worked scenario, identify the two distinct failures — the
   technical one and the process one — and the artifact that caught
   each.
4. Build the weight-ordered study sequence for *your* concentration
   from the verified tables in this volume's README, and defend the
   ordering.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every objective in the
DCIT 300-615 v1.2 exam guide** — troubleshooting across network, compute,
storage, automation, and management — plus a **Design Exercise** covering the
DCID 300-610 v1.2 design concentration, both mapped in the volume README's
coverage tables. Troubleshooting labs are diagnostic walkthroughs: each drives
the real `show`/debug commands, states the healthy baseline and the fault
signature that distinguishes it, and names the misdiagnosis to avoid. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 9.1–9.19** — the fabric built across Chapters
01–08 (Nexus spine-leaf with vPC and VXLAN EVPN, an ACI fabric, a UCS domain,
an MDS/FC fabric, Nexus Dashboard/Intersight), with the ability to induce and
repair faults. **Cost:** none beyond lab resources.

### Lab 9.1 — Troubleshoot routing protocols (DCIT Objective 1.1)

**Objective:** Isolate an OSPF underlay adjacency stuck below FULL.

```text
show ip ospf neighbors
show ip ospf interface ethernet 1/1 | include "Timer|Area|Network|MTU"
show logging last 20 | include OSPF
```

**Expected result:** healthy peers are `FULL`; a stuck `EXSTART/EXCHANGE`
almost always means an **MTU mismatch**, and `2WAY` on a multi-access link is a
DR/BDR election, not a fault. The interface output localizes it.

**Negative test:** assume a `2WAY` neighbor is broken and "fix" it; on a
broadcast segment that is normal — the misdiagnosis wastes a window. Confirm
adjacency need before acting.

**Cleanup:** correct the MTU (or timers/area) and confirm `FULL`.

### Lab 9.2 — Troubleshoot switching protocols: RSTP+, LACP, vPC (DCIT Objective 1.2)

**Objective:** Diagnose a suspended vPC VLAN.

```text
show vpc brief
show vpc consistency-parameters vlans
show port-channel summary
```

**Expected result:** `peer adjacency formed ok` and no Type-1/Type-2
inconsistencies when healthy; a **Type-2 consistency failure** suspends the
VLAN on the secondary — the consistency-parameters output names the mismatched
attribute.

**Negative test:** treat the suspended VLAN as a physical-link fault; the ports
are up — the cause is configuration consistency, not cabling.

**Cleanup:** align the mismatched parameter on both peers; confirm the VLAN
returns to forwarding.

### Lab 9.3 — Troubleshoot overlay protocols: VXLAN EVPN (DCIT Objective 1.3)

**Objective:** Find why hosts on two leaves cannot reach each other over the
overlay.

```text
show nve peers
show bgp l2vpn evpn summary
show l2route evpn mac all
show interface nve1 | include "MTU|state"
```

**Expected result:** NVE peers present and Type-2 MACs learned when healthy;
missing NVE peers with BGP up points to **`send-community extended`** absent;
intermittent unicast loss with ARP working points to an **underlay MTU hole**.

**Negative test:** blame the overlay for a problem that is underlay ECMP + MTU;
`ping` with large packets across each underlay path localizes the bad link —
overlay symptoms often have underlay causes.

**Cleanup:** restore extended communities / MTU; confirm end-to-end reachability.

### Lab 9.4 — Troubleshoot ACI (DCIT Objective 1.4)

**Objective:** Diagnose an EPG with no connectivity using faults and health.

```text
moquery -c faultInst -f 'fault.Inst.severity=="critical"' | egrep 'descr|dn' | head
moquery -c fvRsPathAtt | grep tDn | head
moquery -c fvRsBd
```

**Expected result:** a fault naming the unresolved relationship — a missing
`fvRsBd` (EPG not bound to a BD) or a missing static path is the usual cause;
health score drops on the affected object.

**Negative test:** assume a data-plane problem when the fault clearly shows an
unresolved policy relationship — in ACI, read the fault before the wire.

**Cleanup:** resolve the relationship (bind BD/path); confirm the fault clears.

### Lab 9.5 — Troubleshoot UCS rack servers (DCIT Objective 2.1)

**Objective:** Diagnose a rack server failing service-profile association.

```text
scope server 1
show fault
show assoc
connect nxos ; show sel 1
```

**Expected result:** the association fault reason (firmware host-pack
mismatch, insufficient resources, or a pinning/adapter issue) and the System
Event Log — the fault plus SEL localize a rack-server association failure.

**Negative test:** re-acknowledge the server repeatedly hoping association
completes; without fixing the named fault it will not — read the fault reason.

**Cleanup:** correct the named cause; re-associate and confirm.

### Lab 9.6 — Troubleshoot UCS blade chassis (DCIT Objective 2.2)

**Objective:** Diagnose a chassis/IOM discovery failure.

```text
scope chassis 1
show fault
connect nxos a ; show fex detail
scope org ; scope chassis-disc-policy ; show detail
```

**Expected result:** a discovery fault and the FEX state; a chassis discovered
with fewer links than the **chassis discovery policy** requires stays
under-provisioned — the policy vs actual-link mismatch is the classic cause.

**Negative test:** lower the discovery policy to "1-link" to force discovery;
it hides an actual cabling fault — fix the cabling, do not mask it.

**Cleanup:** restore correct cabling/policy; re-acknowledge the chassis.

### Lab 9.7 — Troubleshoot packet flow from server to fabric (DCIT Objective 2.3)

**Objective:** Trace a blade's traffic from vNIC through the FI to the uplink.

```text
connect nxos a
show interface vethernet 1000
show mac address-table | include 0025.b5
show pinning server-interfaces
```

**Expected result:** the vNIC's vEthernet, its MAC learned, and its **pinning**
to an uplink; a server that cannot reach the network often has a pinning border
or a disjoint-L2 uplink-group problem — the pinning output localizes it.

**Negative test:** assume the array/host is at fault when the vNIC's uplink
pinning points to a downed border interface — trace the pin before blaming the
endpoint.

**Cleanup:** correct the uplink/pinning; confirm the vNIC forwards.

### Lab 9.8 — Troubleshoot hardware interoperability (DCIT Objective 2.4)

**Objective:** Diagnose an adapter/transceiver interoperability fault.

```text
show interface ethernet 1/49 transceiver details
show hardware internal error | include "interop|mismatch" 2>/dev/null
scope server 1 ; scope adapter 1 ; show detail
```

**Expected result:** transceiver type/vendor and adapter model against the
compatibility matrix; an unsupported optic or a VIC/expander mismatch raises an
interop fault — the details output names the incompatible part.

**Negative test:** force a link up with an unsupported optic; it may link but
error under load — the compatibility matrix, not link state, is the arbiter.

**Cleanup:** replace with a supported part; confirm clean counters.

### Lab 9.9 — Troubleshoot firmware upgrades, packages, and interoperability — compute (DCIT Objective 2.5)

**Objective:** Diagnose a stalled UCS firmware upgrade.

```text
scope firmware
show fsm status
scope org ; scope fw-host-pack default ; show fault
```

**Expected result:** the firmware **FSM** stage where it stalled and any
host-pack fault — an upgrade halted at `user-ack` awaits acknowledgement; one
halted on an incompatible bundle names the version conflict.

**Negative test:** assume the upgrade hung when it is correctly waiting at a
`user-ack` maintenance gate — check the FSM before intervening.

**Cleanup:** acknowledge or correct the bundle; let the FSM complete.

### Lab 9.10 — Troubleshoot Fibre Channel physical infrastructure (DCIT Objective 3.1)

**Objective:** Diagnose an FC port that will not come up.

```text
show interface fc1/1
show interface fc1/1 transceiver
show port internal info interface fc1/1 | include "reason|admin|oper"
```

**Expected result:** the port state and the **down reason** (e.g.,
`link-failure`, `isolation`, or `SFP-not-present`); a physical FC problem shows
in the transceiver/down-reason, distinct from a services problem.

**Negative test:** chase zoning when the port down-reason is `SFP validation
failed` — the physical layer must be clean before services matter.

**Cleanup:** replace/reseat the optic or fix the VSAN; confirm the port is `up`.

### Lab 9.11 — Troubleshoot Fibre Channel services (DCIT Objective 3.2)

**Objective:** Diagnose a host that logs in (FLOGI) but cannot see its target.

```text
show flogi database interface fc1/1
show fcns database vsan 100
show zoneset active vsan 100
```

**Expected result:** FLOGI present and the device in the name server, but the
target missing from the **active zoneset** — an FC-services problem is
"logged-in but not zoned," distinct from a physical fault.

**Negative test:** reseat cables for a problem that is purely zoning; FLOGI was
already fine — read the name server and active zoneset first.

**Cleanup:** add the correct zone/activate; confirm the initiator sees the
target.

### Lab 9.12 — Troubleshoot automation and scripting tools (DCIT Objective 4.1)

**Objective:** Diagnose a failing NX-API/Ansible automation run.

```bash
ansible-playbook -i inv site.yml -vvv 2>&1 | grep -E 'FAILED|401|403|Connection'
curl -sk -u admin:$PW https://$NXOS/ins -d '[{"jsonrpc":"2.0","method":"cli","params":{"cmd":"show clock","version":1},"id":1}]' -o /dev/null -w '%{http_code}\n'
```

**Expected result:** the failing task and HTTP status — `401/403` is
credentials/RBAC, a connection error is `feature nxapi` off or a firewall, and
a `200` with an error body is a bad command — the status code localizes the
layer.

**Negative test:** rewrite the playbook logic when the real cause is a `403`
(the automation account lacks a role) — check auth before logic.

**Cleanup:** fix credentials/feature/reachability; re-run to `changed=0`.

### Lab 9.13 — Troubleshoot programmability and orchestration (DCIT Objective 4.2)

**Objective:** Diagnose a Terraform/NDFC orchestration drift or apply failure.

```bash
terraform plan -no-color | grep -E 'will be|Error:'
curl -sk -H "Authorization: $NDFC_TOK" "https://$DCNM/.../control/fabrics" -o /dev/null -w '%{http_code}\n'
```

**Expected result:** the plan's intended changes or a provider error, plus the
NDFC API status — orchestration failures are usually state drift (someone
changed the fabric out-of-band) or an expired API token, both visible here.

**Negative test:** `terraform apply` to "force" past drift without reading the
plan — you may overwrite a deliberate out-of-band change; read the plan first.

**Cleanup:** reconcile state (import or revert); re-plan to a clean diff.

### Lab 9.14 — Troubleshoot firmware upgrades, packages, and interoperability — fabric (DCIT Objective 5.1)

**Objective:** Diagnose a stalled NX-OS/fabric ISSU.

```text
show install all status
show incompatibility-all nxos bootflash:target.bin
show module | include "ok|fail|pwr"
```

**Expected result:** the install stage and any **incompatibility** entries; an
ISSU aborts on a feature incompatible with hitless upgrade (or a single
supervisor) — the incompatibility list names it.

**Negative test:** retry ISSU unchanged after it aborted for incompatibility;
it will abort again — resolve the named feature or accept a disruptive upgrade.

**Cleanup:** resolve incompatibilities or schedule a disruptive window; complete
the install.

### Lab 9.15 — Troubleshoot centralized management integration: Nexus Dashboard and Intersight (DCIT Objective 5.2)

**Objective:** Diagnose a fabric/domain that will not onboard or stay connected.

```bash
curl -sk -b cookie.txt "https://$ND/api/v1/infra/fabrics" | jq -r '.items[] | "\(.spec.name) \(.status.health)"'
curl -s -H "X-Starship-Api-Key: $IK" "https://intersight.com/api/v1/asset/DeviceRegistrations?\$select=DeviceHostname,ConnectionStatus" | jq -r '.Results[] | "\(.DeviceHostname) \(.ConnectionStatus)"'
```

**Expected result:** onboarded fabrics with health and Intersight device
`ConnectionStatus`; a `Connected`→`NotConnected` flap points to a **device
connector / proxy / certificate** problem, not a fabric fault.

**Negative test:** troubleshoot the fabric data plane when the connector's
outbound HTTPS to Intersight is blocked — the management integration is the
break, and the data plane is fine.

**Cleanup:** restore connector reachability/certs; confirm `Connected`.

### Lab 9.16 — Troubleshoot network security (DCIT Objective 5.3)

**Objective:** Diagnose traffic blocked by CoPP or an ACL.

```text
show access-lists HOST-IN | include "match"
show policy-map interface control-plane | include "dropped"
show logging last 30 | include "ACLLOG|DENY"
```

**Expected result:** ACL hit counters and CoPP drops; traffic "disappearing"
that traces to a **default-deny ACL match** or a **CoPP-policed class** is a
policy drop, not a forwarding fault — the counters and logs pinpoint which.

**Negative test:** chase routing for traffic an ACL is dropping by design;
the ACLLOG entry names the denied flow — read the logs before the routing table.

**Cleanup:** adjust the ACL/CoPP if the drop was unintended; re-verify.

### Lab 9.17 — Troubleshoot ACI security domains and role mapping (DCIT Objective 5.4)

**Objective:** Diagnose a user who cannot see or change expected objects.

```text
moquery -c aaaUser -f 'aaa.User.name=="neteng"'
moquery -c aaaUserDomain | egrep 'name|dn' | head
moquery -c aaaDomainRef 2>/dev/null | head
```

**Expected result:** the user's security-domain memberships and roles; objects
tagged with a domain the user does not belong to are invisible to them — a
**security-domain/role-mapping mismatch**, not a permissions bug.

**Negative test:** grant `admin` to "fix" it when correct scoping is the goal —
over-granting hides the real mapping error and breaks least privilege.

**Cleanup:** correct the domain membership/role; confirm scoped access.

### Lab 9.18 — Troubleshoot data center compute security (DCIT Objective 5.5)

**Objective:** Diagnose a UCS management-plane security misconfiguration.

```text
scope security ; show authentication
scope system ; scope services ; show telnet ; show ssh-server
show fault | include "security|auth"
```

**Expected result:** the AAA realm binding and disabled Telnet; failed logins
tracing to a **broken LDAP/AAA provider order** (falling back incorrectly) or
an inadvertently enabled insecure protocol — the auth config and faults localize
it.

**Negative test:** switch to local auth to "unblock" logins, masking a
reachable-AAA problem — fix the provider, do not bypass central auth.

**Cleanup:** restore the AAA provider/order; keep insecure protocols disabled.

### Lab 9.19 — Troubleshoot storage security (DCIT Objective 5.6)

**Objective:** Diagnose an ISL or host isolated by a SAN security control.

```text
show port-security database vsan 100
show fabric-binding violations vsan 100 2>/dev/null
show fcsp interface fc1/1 2>/dev/null || show fcsp database
```

**Expected result:** a **port-security or fabric-binding violation** (an
unlisted pWWN/switch WWN) or an **FC-SP/DHCHAP** authentication failure — a SAN
"link down" that is actually a security control rejecting an unauthorized
device.

**Negative test:** replace optics/cables for a link that is administratively
isolated by fabric binding — the violation log, not the physical layer, is the
cause.

**Cleanup:** authorize the device (or remove it); clear the violation and
confirm the port joins.

## Design Exercise

**DCID (300-610 Designing Cisco Data Center Infrastructure)** is a design
concentration: it tests designing a data center from requirements — network,
compute, storage, and automation — rather than configuration recall. This
exercise covers DCID's four design domains; no lab is required.

**Scenario.** Design the data center infrastructure for an enterprise
standing up an **AI/ML training cluster** alongside traditional virtualized
and database workloads: two data centers (active/active), a GPU pod requiring
lossless RDMA, existing FC storage plus a new all-NVMe array, a mandate to
manage everything through Nexus Dashboard and Intersight, and 99.99%
availability with no single point of failure. Requirements: non-blocking
east-west for AI collectives; segmentation between AI, production, and DMZ;
DCI for workload mobility and storage replication; and automated, repeatable
provisioning.

**Produce, defending each choice against a rejected alternative:**

1. **Requirements and constraints** — classify each requirement with a
   measurable acceptance test (e.g., RoCEv2 job-completion latency, RPO/RTO for
   replication), and map risks to design decisions.
2. **Network design (DCID D1)** — the fabric: spine-leaf sizing and
   oversubscription, VXLAN EVPN vs ACI for segmentation, QoS for lossless
   Ethernet (PFC/ECN) on the AI pod, DCI via VXLAN EVPN Multi-Site vs ACI
   Multi-Site, and redundancy (vPC, anycast gateway, RR placement).
3. **Compute design (DCID D2)** — UCS-X vs rack, VIC/adapter and virtualization
   choices, UCS-X performance sizing for AI/ML, and Ethernet vs FC connectivity
   per workload.
4. **Storage design (DCID D3)** — FC vs iSCSI vs NVMe/TCP per workload,
   multipathing and addressing, QoS/lossless requirements, and traditional vs
   high-performance storage tiers.
5. **Automation design (DCID D4)** — orchestration with Nexus Dashboard
   Fabric Controller and Intersight Cloud Orchestrator, Terraform/Ansible for
   Day-0/Day-1, and automatic network deployment.
6. **Resilience and decision log** — HA for every layer (fabric, compute,
   storage, management), the active/active DCI failure model, and at least six
   decisions recorded as {decision, justification, rejected alternative,
   impact}.

**Success looks like:** every design choice traces to a requirement, each
resilience and segmentation claim names the failure or exposure it addresses,
lossless/RDMA requirements are met by an explicit QoS design, and each decision
names the rejected option and its trade-off — the design standard DCID applies,
and the basis of a CCIE Data Center lab design.

## Lab Verification

Verification means the upgrade wave completed with all asserts green
and evidence archived, the injected fault was diagnosed by method
with its chain intact, and the postmortem and study plan exist.
Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Design traces decisions to requirements; troubleshooting eliminates
hypotheses with evidence; operations rehearses change until it is
boring. Those three disciplines are DCID and DCIT by name, but they
are also simply how the estate this volume built stays up. With the
core and five concentrations verified, mapped, and practiced, the
track is yours to schedule.

- [ ] My design checklist starts from requirements and facilities
- [ ] My elimination method leaves an evidence chain by habit
- [ ] My upgrade wave ran green end to end
- [ ] My exam plan is weight-ordered against the verified blueprints
