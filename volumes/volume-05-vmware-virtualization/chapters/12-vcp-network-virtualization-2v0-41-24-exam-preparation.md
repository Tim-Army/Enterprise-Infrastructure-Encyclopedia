# Chapter 12: VCP Network Virtualization 2V0-41.24 Exam Preparation

![Lab flow for this chapter: from a clean NSX state, five timed steps are completed from memory without reference material — transport zone/uplink profile/TEP pool and transport node prep (target 20 minutes), Edge node and Edge cluster (15 minutes), Tier-0 BGP plus Tier-1 and overlay segment (20 minutes), a DFW default-deny plus scoped allow policy (15 minutes), and a blind negative test diagnosing one deliberately introduced fault using only Traceflow, BGP neighbor status, and transport node status (15 minutes). Total elapsed time under 90 minutes with all steps unaided is a strong exam-readiness signal.](../../../diagrams/volume-05-vmware-virtualization/chapter-12-nsx-timed-self-assessment-flow.svg)

*Figure 12-1. Flow used throughout this chapter's Hands-On Lab: a timed, unaided NSX build-and-troubleshoot exercise culminating in a blind fault diagnosis.*

## Learning Objectives

- Map the VCP-NV (2V0-41.24) exam's published blueprint sections to the
  NSX chapters in this volume and identify any gaps in hands-on
  experience before scheduling the exam.
- Explain the general blueprint domain structure Broadcom uses for
  current VCP exams and how it differs from a topic list.
- Build a self-assessment plan that exercises networking fundamentals,
  NSX architecture, design judgment, hands-on configuration, and
  troubleshooting separately, since the exam evaluates all five.
- Identify authoritative, non-proprietary study resources and distinguish
  them from unauthorized "exam dump" material that violates the
  certification agreement.
- Complete a comprehensive readiness lab exercising the full NSX
  installation-through-troubleshooting workflow from Chapters 10 and 11
  under time pressure, as a realistic self-assessment.

## Theory and Architecture

This chapter is study and review material for the **VMware Certified
Professional – Network Virtualization (VCP-NV), exam 2V0-41.24**. It does
not reproduce exam questions, does not reveal proprietary scoring
weightings, and is not a substitute for Broadcom's own exam guide — it
exists to organize this volume's NSX content (Chapters 8, 10, and 11
primarily, with Chapters 1 and 4 as networking prerequisites) against the
publicly published blueprint structure so a reader can self-assess
readiness before scheduling the exam. Always confirm current domain
names, exam length, and item count against Broadcom's published exam
guide before relying on this chapter — blueprints are revised
independently of this repository's release cycle, and this chapter's
value is organizational, not authoritative.

### Broadcom's current blueprint format

Current-generation VMware by Broadcom certification exams (including
2V0-41.24) are organized using a standardized, multi-section blueprint
format rather than a flat topic list. Understanding this format matters
because each section type calls for a different kind of preparation:

- **Foundational/standards section** — general networking and industry-
  standard knowledge (the OSI model, TCP/IP fundamentals, routing and
  switching concepts, common security standards) that exists independent
  of NSX specifically. This section rewards general networking
  competency, not NSX product familiarity — a candidate strong on NSX
  configuration but weak on underlying networking fundamentals (BGP
  path-selection basics, VLAN/trunking concepts) will find this section
  the harder one to cram for late, since it is not NSX-specific
  documentation that helps here.
- **Product fundamentals section** — NSX's own architecture: the
  management/control/data plane model, NSX Manager clustering, transport
  zones, Geneve overlay encapsulation, Edge node roles. This maps
  directly to [Chapter 10](10-installing-vmware-nsx.md)'s Theory and Architecture.
- **Plan and design section** — architectural judgment questions: given a
  set of requirements or constraints, what design decision is correct
  (transport zone scope, Edge sizing and placement, HA mode selection,
  DFW rule scoping strategy). This maps to the Design Considerations
  sections of Chapters 8, 10, and 11 — this is where understanding *why*
  a design choice is made, not just *how* to configure it, is tested.
- **Deploy, configure, and operate section** — hands-on configuration
  competency: host preparation, Tier-0/Tier-1 gateway configuration, DFW
  and Gateway Firewall rule construction, NAT, load balancing, VPN,
  micro-segmentation. This maps to the Implementation and Automation
  sections of Chapters 8, 10, and 11, and rewards actual lab repetition
  over passive reading.
- **Troubleshooting section** — diagnostic reasoning using tools such as
  Traceflow, BGP neighbor status, and DFW rule hit counters to isolate a
  failure to a specific layer. This maps to the Validation and
  Troubleshooting sections of Chapters 8, 10, and 11.

### Skills the exam assumes coming in

The exam blueprint's stated candidate profile assumes hands-on NSX
administration experience already — it is not designed to be passable
from documentation reading alone, and the "deploy, configure, and
operate" and "troubleshoot" sections in particular are difficult to pass
through memorization without actual lab repetition. Treat the hands-on
labs in Chapters 8, 10, and 11 (and the comprehensive lab at the end of
this chapter) as mandatory preparation, not optional supplementary
material.

## Design Considerations

- **Diagnostic self-assessment before scheduling.** Do not schedule the
  exam based on comfort with reading this volume alone; use the
  five-domain structure above to self-rate readiness independently per
  domain (foundational networking, NSX fundamentals, design judgment,
  hands-on configuration, troubleshooting) and target additional lab time
  specifically at the weakest domain rather than re-reading domains
  already strong.
- **Lab environment fidelity.** A nested-lab NSX environment (as used
  throughout Chapters 10 and 11) is adequate for building configuration
  and troubleshooting muscle memory; it does not need to match production
  scale to be effective preparation, since the exam tests conceptual and
  procedural competency, not environment scale.
- **Time-boxed practice.** Because the deploy/configure/operate and
  troubleshooting sections are procedural, practice them under a
  self-imposed time constraint (attempt the comprehensive lab at the end
  of this chapter against a clock) rather than only untimed — exam time
  pressure is a real factor the blueprint's item count and time allotment
  reflect, and untimed practice alone does not train for it.
- **Currency against the live blueprint.** Broadcom revises exam guides
  independently of this repository; before scheduling, re-check the
  current published exam guide for the authoritative domain names, item
  count, and any recently added topic areas (the 2V0-41.24 generation has
  periodically added newer NSX capabilities such as Distributed IDS/IPS
  and API-driven automation as the product itself has grown) rather than
  relying solely on this chapter's summary.
- **Ethical preparation boundary.** Preparation must draw only from
  authorized sources: Broadcom's own documentation and exam guide,
  official training, hands-on lab practice, and legitimate study material
  that does not reproduce actual exam item content. Unauthorized "exam
  dump" material that claims to reproduce actual scored questions
  violates the certification agreement candidates accept at
  registration and undermines the credential's value — do not use it,
  and treat any study resource that claims to contain actual past exam
  questions as disqualifying rather than helpful.

## Implementation and Automation

### Building a domain-mapped study tracker

```text
# Example self-assessment tracker structure (adapt in a spreadsheet or
# plain-text file) — rate each row 1-5 based on comfort level, and treat
# anything below 3 as requiring additional lab time before scheduling.

Domain                        | Chapter(s) | Self-rating | Notes
-------------------------------|------------|--------------|------------------------------
Networking fundamentals        | 4          |              | OSI, VLAN/trunking, routing basics
NSX architecture fundamentals  | 8, 10      |              | Mgmt/control/data plane, Manager cluster
Design judgment                | 8, 10, 11  |              | Transport zone/Edge/HA-mode decisions
Host & Edge deployment         | 10         |              | Transport node prep, uplink profiles, TEPs
Gateway & routing config       | 11         |              | T0/T1, BGP, NAT, DHCP
DFW & micro-segmentation       | 8, 11      |              | Groups, Applied To, rule ordering
Troubleshooting                | 10, 11     |              | Traceflow, BGP status, DFW hit counters
```

### Re-running prior labs as timed drills

```text
# Suggested timed-drill sequence, reusing prior chapters' labs as
# practice repetitions rather than one-time exercises:

1. Chapter 10 lab (transport zone -> uplink profile -> TEP pool ->
   host preparation -> Edge deployment) — target: complete within 45
   minutes on a lab environment you have not pre-staged.
2. Chapter 11 lab (T0 with BGP -> T1 -> segment -> DHCP relay ->
   DFW default-deny -> Traceflow -> scoped allow) — target: complete
   within 45 minutes.
3. Chapter 8 lab (DFW dynamic security group by tag, Gateway Firewall
   rule) — target: complete within 20 minutes.
```

### Querying NSX Manager for a self-generated design-judgment drill

```bash
# curl against the NSX Manager Policy API: pull current transport zone,
# gateway, and DFW policy inventory from a lab environment, then practice
# explaining *why* each object is configured the way it is — a
# self-generated design-judgment exercise rather than passive reading
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' \
  https://nsx-vip.corp.example/policy/api/v1/infra/tier-0s | jq '.results[].display_name'
curl -k -u admin:'<NSX_ADMIN_PASSWORD>' \
  https://nsx-vip.corp.example/policy/api/v1/infra/domains/default/security-policies | jq '.results[].display_name'
```

## Validation and Troubleshooting

- **Domain-by-domain readiness signal.** Comfort explaining a design
  decision out loud (why active/standby was chosen over active/active for
  a specific gateway, for instance) without referring back to the chapter
  text is a stronger readiness signal than recognizing the right answer
  when reading it — practice explaining, not just recalling.
- **Lab-without-notes test.** Attempt the comprehensive lab at the end of
  this chapter without referring back to Chapters 10/11's implementation
  examples; note every point where reference material was needed, and
  treat each as a specific, named gap to close before scheduling rather
  than a general "review more" conclusion.
- **Troubleshooting scenario self-generation.** Deliberately break a lab
  configuration (an incorrect BGP AS number, a DFW rule with the wrong
  Applied To scope, a TEP pool exhausted) and practice diagnosing it from
  symptoms alone using Traceflow, BGP neighbor status, and DFW hit
  counters — this is the most direct way to rehearse the exam's
  troubleshooting section, since that section is fundamentally about
  diagnostic reasoning under uncertainty, not fact recall.
- **Recognize documentation-only knowledge gaps.** If a concept is only
  understood well enough to recognize in the official documentation but
  not well enough to configure unaided in a lab, treat it as not yet
  exam-ready — the deploy/configure/operate section specifically tests
  unaided procedural competency.

## Security and Best Practices

- Register for the exam only through Broadcom's authorized testing
  partner; verify current identification and testing-environment
  requirements (whether in-person at a test center or online-proctored)
  directly from the official registration portal before exam day, since
  these requirements change and vary by delivery method.
- Do not use, purchase, or reference unauthorized exam question dumps —
  beyond the ethical and contractual violation, they are frequently
  inaccurate or outdated relative to the current live blueprint, making
  them actively counterproductive preparation even setting aside the
  policy violation.
- Practice in an isolated lab environment, not in any production NSX
  deployment — the deliberate-failure troubleshooting drills above are by
  design disruptive and must never be rehearsed against systems carrying
  real workloads.
- Protect lab credentials used during exam preparation the same way
  production credentials are protected ([Chapter 8](08-vsphere-and-nsx-security-architecture.md)'s RBAC and credential
  hygiene guidance applies equally to a lab environment, and building
  that habit during preparation reinforces it for real deployments
  afterward).

## References and Knowledge Checks

**References**

- [Broadcom Education Services](https://www.broadcom.com/support/education/vmware) — official 2V0-41.24 exam guide (current
  blueprint domains, item count, exam duration, and registration
  requirements — verify directly before scheduling).
- [VMware NSX 4.x Documentation (the full documentation set referenced
  throughout Chapters 8, 10, and 11).](https://techdocs.broadcom.com/us/en/vmware-cis/nsx/vmware-nsx/4-2.html)
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this repository's certification-to-volume mapping.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline referenced throughout this volume.
- See [Chapter 8](08-vsphere-and-nsx-security-architecture.md) for DFW/Gateway Firewall security architecture.
- See [Chapter 10](10-installing-vmware-nsx.md) for NSX installation and transport fabric.
- See [Chapter 11](11-configuring-vmware-nsx.md) for NSX logical networking configuration.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Broadcom exam item)*

1. Explain, without referring back to [Chapter 10](10-installing-vmware-nsx.md), the difference between
   an overlay transport zone and a VLAN transport zone, and give a
   scenario requiring each.
2. Explain, without referring back to [Chapter 11](11-configuring-vmware-nsx.md), why a Tier-0 gateway
   requires Edge capacity while Tier-1 East-West routing does not
   necessarily.
3. Walk through, from memory, the steps Traceflow output would show for
   a packet blocked by a DFW default-deny rule versus a packet dropped by
   a BGP routing failure — what specifically distinguishes the two in the
   tool's output?
4. Given a requirement for strict NAT session-state consistency on a
   Tier-1 gateway, justify the correct HA mode choice without looking it
   up.
5. What single networking fundamental (independent of NSX) most
   commonly trips up candidates who are otherwise strong on NSX-specific
   configuration, according to this chapter's discussion of the
   foundational blueprint section?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every testable
objective in the VCP-NV (2V0-41.24) exam guide** — Section 4
Deploy/Configure/Operate (4.1–4.13) and Section 5 Troubleshoot (5.1–5.3).
Each is mapped in the volume README's coverage table and ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 12.1–12.16**

- An NSX 4.x deployment reachable at `$NSX` (NSX Manager), a vCenter with a
  prepared cluster, and an API token or basic auth in `$H` (an
  `Authorization` header). Labs use the **NSX Policy API**
  (`/policy/api/v1/...`) via `curl`/`Invoke-RestMethod`, the declarative
  surface the exam and Chapters 10–11 use.
- **Cost:** none beyond lab hardware; every lab deletes what it creates.

### Lab 12.1 — Prepare an NSX infrastructure for deployment (Objective 4.1)

**Objective:** Confirm transport nodes and a transport zone — the fabric
segments ride on.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/sites/default/enforcement-points/default/transport-zones" \
  | jq -r '.results[] | "\(.display_name)\t\(.tz_type)"'
curl -sk -H "$H" "$NSX/api/v1/transport-nodes" | jq '.result_count'
```

**Expected result:** at least one OVERLAY and one VLAN transport zone, and a
nonzero transport-node count — the prepared fabric.

**Negative test:** create a segment referencing an unprepared host; it has
no realized state on that host, proving preparation is a prerequisite.

**Cleanup:** none (read-only).

### Lab 12.2 — Configure segments (Objective 4.2)

**Objective:** Create an overlay segment declaratively.

```bash
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/segments/web-seg" \
  -d '{"display_name":"web-seg","transport_zone_path":"/infra/sites/default/enforcement-points/default/transport-zones/overlay-tz","subnets":[{"gateway_address":"10.10.10.1/24"}]}'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/segments/web-seg" | jq -r '.display_name, .subnets[0].gateway_address'
```

**Expected result:** `web-seg` with gateway `10.10.10.1/24` — an L2 overlay
segment ready for workloads.

**Negative test:** PATCH a segment onto a VLAN transport zone with an
overlay-only gateway config; realization fails, showing segment type must
match the transport zone.

**Cleanup:** `curl -sk -X DELETE -H "$H" "$NSX/policy/api/v1/infra/segments/web-seg"`.

### Lab 12.3 — Deploy and configure NSX Edge nodes (Objective 4.3)

**Objective:** Verify Edge nodes and their Edge cluster membership.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/sites/default/enforcement-points/default/edge-clusters" \
  | jq -r '.results[] | .display_name'
curl -sk -H "$H" "$NSX/api/v1/transport-nodes?node_types=EdgeNode" \
  | jq -r '.results[] | "\(.display_name)\t\(.node_deployment_info.deployment_config.form_factor)"'
```

**Expected result:** an Edge cluster and its member Edge nodes with form
factor (MEDIUM/LARGE) — the nodes that host Tier-0/Tier-1 services.

**Negative test:** place a Tier-0 SR on an empty Edge cluster; the gateway
has no realized services — Edge nodes must exist first.

**Cleanup:** none (read-only).

### Lab 12.4 — Configure the Tier-1 gateway (Objective 4.4)

**Objective:** Create a Tier-1 gateway and attach the segment.

```bash
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/tier-1s/t1-web" \
  -d '{"display_name":"t1-web","route_advertisement_types":["TIER1_CONNECTED"]}'
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/segments/web-seg" \
  -d '{"connectivity_path":"/infra/tier-1s/t1-web"}'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/tier-1s/t1-web" | jq -r '.route_advertisement_types[]'
```

**Expected result:** a Tier-1 advertising `TIER1_CONNECTED` with the segment
attached — north-south routing for the segment's subnet begins here.

**Negative test:** attach the segment to a Tier-1 with no linked Tier-0; the
route never reaches the physical fabric, proving the Tier-1→Tier-0 link is
required.

**Cleanup:** delete the Tier-1 after detaching the segment.

### Lab 12.5 — Create and configure a Tier-0 gateway with OSPF (Objective 4.5)

**Objective:** Enable OSPF on a Tier-0 and read the adjacency.

```bash
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/tier-0s/t0/ospf" -d '{"enabled":true}'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/tier-0s/t0/locale-services/default/ospf/neighbors/status" \
  | jq -r '.results[] | "\(.neighbor_address)\t\(.state)"'
```

**Expected result:** an OSPF neighbor in `FULL` state — the Tier-0 is
exchanging routes with the physical router.

**Negative test:** mismatch the OSPF area between Tier-0 and the physical
peer; the adjacency stalls in `EXSTART`/`INIT`, the classic area-mismatch
symptom.

**Cleanup:** disable OSPF on the Tier-0.

### Lab 12.6 — Configure the Tier-0 gateway with BGP (Objective 4.6)

**Objective:** Establish a BGP neighbor and confirm the session.

```bash
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/tier-0s/t0/locale-services/default/bgp/neighbors/peer1" \
  -d '{"neighbor_address":"192.168.100.1","remote_as_num":"65001"}'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/tier-0s/t0/locale-services/default/bgp/neighbors/peer1/status" \
  | jq -r '.results[].connection_state'
```

**Expected result:** connection state `ESTABLISHED` — the Tier-0 peers with
AS 65001 and can exchange prefixes.

**Negative test:** set the wrong `remote_as_num`; the session flaps in
`CONNECT`/`ACTIVE` — the AS mismatch BGP refuses to establish over.

**Cleanup:** delete the BGP neighbor.

### Lab 12.7 — Configure VRF Lite (Objective 4.7)

**Objective:** Create a VRF on the Tier-0 for tenant route isolation.

```bash
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/tier-0s/t0-vrf-a" \
  -d '{"display_name":"t0-vrf-a","vrf_config":{"tier0_path":"/infra/tier-0s/t0"}}'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/tier-0s/t0-vrf-a" | jq -r '.vrf_config.tier0_path'
```

**Expected result:** a VRF Tier-0 parented to `t0` — tenant traffic uses a
separate routing table over shared Edge infrastructure.

**Negative test:** advertise overlapping tenant prefixes without VRF
separation; routes collide — the isolation VRF Lite provides.

**Cleanup:** delete the VRF Tier-0.

### Lab 12.8 — Configure Network Address Translation (Objective 4.8)

**Objective:** Add a SNAT rule so a private subnet egresses on one IP.

```bash
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/tier-1s/t1-web/nat/USER/nat-rules/snat-web" \
  -d '{"action":"SNAT","source_network":"10.10.10.0/24","translated_network":"203.0.113.10"}'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/tier-1s/t1-web/nat/USER/nat-rules/snat-web" | jq -r '.action, .translated_network'
```

**Expected result:** a SNAT rule translating `10.10.10.0/24` to
`203.0.113.10` — private hosts share one routable source address.

**Negative test:** create the SNAT on a Tier-1 whose `10.10.10.0/24` is also
advertised to the Tier-0; asymmetric routing breaks return traffic — why
NAT and route advertisement must be coordinated.

**Cleanup:** delete the NAT rule.

### Lab 12.9 — Deploy Virtual Private Networks (Objective 4.9)

**Objective:** Read IPSec VPN session status on the Tier-0.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/tier-0s/t0/locale-services/default/ipsec-vpn-services" \
  | jq -r '.results[].display_name'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/tier-0s/t0/locale-services/default/ipsec-vpn-services/svc/sessions" \
  | jq -r '.results[] | "\(.display_name)\t\(.enabled)"'
```

**Expected result:** the VPN service and its sessions — encrypted
connectivity to a remote site over the Tier-0.

**Negative test:** a session with mismatched pre-shared keys stays down; the
tunnel status never reaches `UP`, the PSK-mismatch symptom.

**Cleanup:** disable/delete the lab VPN session.

### Lab 12.10 — Manage users and roles (Objective 4.10)

**Objective:** Assign an NSX RBAC role binding and read it back.

```bash
curl -sk -X POST -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/aaa/role-bindings" \
  -d '{"name":"net-eng","type":"remote_group","identity_source_type":"LDAP","roles_for_paths":[{"path":"/","roles":[{"role":"network_engineer"}]}]}'
curl -sk -H "$H" "$NSX/policy/api/v1/aaa/role-bindings" | jq -r '.results[] | "\(.name)\t\(.roles_for_paths[0].roles[0].role)"'
```

**Expected result:** the group bound to `network_engineer` — scoped NSX
administration.

**Negative test:** a `network_engineer` principal attempts to edit
enforcement points/system settings; denied — the role lacks that scope.

**Cleanup:** delete the role binding.

### Lab 12.11 — Perform operations tasks (Objective 4.11)

**Objective:** Configure remote syslog and confirm a backup is current.

```bash
curl -sk -X PUT -H "$H" -H 'Content-Type: application/json' \
  "$NSX/api/v1/node/services/syslog/exporters/lab" \
  -d '{"exporter_name":"lab","level":"INFO","server":"10.0.0.50","port":514,"protocol":"UDP"}'
curl -sk -H "$H" "$NSX/api/v1/cluster/backups/status" | jq -r '.cluster_backup_statuses[0].success'
```

**Expected result:** a syslog exporter to `10.0.0.50:514` and a most-recent
backup `success: true` — the operational hygiene the exam expects.

**Negative test:** a backup target with bad SFTP credentials reports
`success: false`; an unverified backup is not a backup.

**Cleanup:** delete the syslog exporter.

### Lab 12.12 — Monitor a VMware NSX implementation (Objective 4.12)

**Objective:** Read open NSX alarms to run the fabric by exception.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/alarms?status=OPEN" \
  | jq -r '.results[] | "\(.feature_name)\t\(.severity)"' | sort | uniq -c
```

**Expected result:** open alarms grouped by feature and severity — the
monitoring signal for control-plane, edge, and DFW health.

**Negative test:** rely on segment reachability alone while a `CRITICAL`
edge-tunnel alarm is open; the overlay is degraded though pings still pass —
why alarms, not spot checks, drive monitoring.

**Cleanup:** none (read-only).

### Lab 12.13 — Use NSX Intelligence (Objective 4.13)

**Objective:** Pull a micro-segmentation recommendation from NSX
Intelligence.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/recommendations" \
  | jq -r '.results[] | "\(.display_name)\t\(.status)"'
```

**Expected result:** recommendation entities with status — Intelligence
observes real flows and proposes DFW rules from them.

**Negative test:** author DFW rules by guesswork instead; either over-blocking
or leaving gaps that Intelligence's flow-based recommendation would have
caught.

**Cleanup:** none (read-only).

### Lab 12.14 — Use log files to troubleshoot (Objective 5.1)

**Objective:** Search NSX Manager logs for a realization failure.

```bash
# on NSX Manager over SSH
grep -iE 'error|realization' /var/log/policy/policy.log | tail -15
```

**Expected result:** log lines naming the entity that failed to realize —
the authoritative record of why an intended config did not take effect.

**Negative test:** a config that shows "in progress" indefinitely with no
error log is usually a downstream (transport-node) issue, not a policy
error — absence of policy errors redirects the search.

**Cleanup:** none (read-only).

### Lab 12.15 — Identify tools available for troubleshooting (Objective 5.2)

**Objective:** Run Traceflow to trace a packet through the overlay.

```bash
curl -sk -X POST -H "$H" -H 'Content-Type: application/json' \
  "$NSX/api/v1/traceflow" \
  -d '{"lport_id":"<src-logical-port>","packet":{"frame_size":128,"ip_header":{"src_ip":"10.10.10.5","dst_ip":"10.10.20.5"}}}' \
  | jq -r '.id'
# then GET /api/v1/traceflow/<id>/observations
```

**Expected result:** a Traceflow ID whose observations show each hop
(segment, DFW, Tier-1, Tier-0) with `DELIVERED` or a `DROPPED` verdict at the
exact component — the definitive path diagnostic.

**Negative test:** guess the fault from pings alone; Traceflow instead names
the DFW rule or routing hop that dropped the packet.

**Cleanup:** none (diagnostic; observations expire).

### Lab 12.16 — Troubleshoot common NSX issues (Objective 5.3)

**Objective:** Diagnose a broken DFW rule by reading its realized state and
hit count.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/domains/default/security-policies/app-policy/rules" \
  | jq -r '.results[] | "\(.display_name)\t\(.action)\t\(.sequence_number)"'
curl -sk -H "$H" "$NSX/api/v1/firewall/sections/<id>/rules/<rule-id>/stats" | jq -r '.hit_count'
```

**Expected result:** the rule order/action and a hit count; a rule with zero
hits that should be matching means an earlier rule shadows it — the ordering
bug DFW troubleshooting hunts.

**Negative test:** add an explicit allow *below* a broad deny; its zero hit
count proves it is unreachable — rule order, not rule content, is the fault.

**Cleanup:** none (read-only).

### Lab 12.17 — Comprehensive NSX build-and-troubleshoot (integrative)

**Objective:** Complete a timed, comprehensive NSX build-and-troubleshoot
exercise spanning installation through logical networking and security,
as a realistic self-assessment for exam readiness.

**Prerequisites**

- A nested or physical lab environment with vCenter Server, at least two
  ESXi hosts prepared with a VDS ([Chapter 4](04-vsphere-virtual-networking.md)), and NSX Manager deployed
  ([Chapter 10](10-installing-vmware-nsx.md)), reset to a clean/unconfigured NSX state (no existing
  transport zones, gateways, or DFW policy beyond defaults).
- A timer or stopwatch.
- No reference material open at the start of the timed portion (steps
  1–6); reference material is permitted only during the review portion
  (step 7).

**Steps**

1. **(Timed, target 20 minutes)** From memory, create an overlay
   transport zone, an uplink profile, and a TEP IP pool, and prepare both
   lab hosts as transport nodes.

   **Expected result:** both hosts report a healthy transport node
   status without needing to reopen [Chapter 10](10-installing-vmware-nsx.md).

2. **(Timed, target 15 minutes)** Deploy an Edge node and form an Edge
   cluster.

   **Expected result:** the Edge node registers successfully and appears
   in the new Edge cluster.

3. **(Timed, target 20 minutes)** Create a Tier-0 gateway with a BGP
   neighbor to a lab upstream router, and a Tier-1 gateway attached
   beneath it with an overlay segment.

   **Expected result:** the BGP neighbor reaches `Established`, and a
   test VM placed on the segment obtains connectivity through the
   gateway hierarchy.

4. **(Timed, target 15 minutes)** Build a DFW policy section with a
   default-deny rule and a scoped allow rule for a specific application
   flow, using dynamic groups.

   **Expected result:** the intended flow succeeds and out-of-scope
   flows are correctly blocked.

5. **Negative test (timed, target 15 minutes):** have a lab partner (or,
   working alone, deliberately introduce without looking at the change
   log) one fault among: an incorrect BGP AS number, a DFW rule with an
   incorrect Applied To scope, or a TEP pool exhausted of addresses.
   Diagnose and correct the fault using Traceflow, BGP neighbor status,
   and/or transport node status as appropriate — without reference
   material.

   **Expected result:** the fault is correctly identified and resolved
   within the time box, using only the diagnostic tools covered in
   Chapters 10 and 11.

6. Stop the timer. Total elapsed time under 90 minutes with all
   expected results achieved unaided is a strong exam-readiness signal;
   significantly over time or requiring reference material indicates
   which specific domain (from the Design Considerations tracker) needs
   additional practice.

7. **Review (untimed):** for any step that required reference material or
   ran over its time box, revisit the corresponding section of [Chapter 10](10-installing-vmware-nsx.md)
   or 11 and repeat that specific step in isolation until it can be
   completed unaided within its target time.

8. **Cleanup:** remove all objects created during the exercise (DFW
   policy, segments, Tier-1 and Tier-0 gateways, Edge cluster and Edge
   node, transport node preparation, transport zone/uplink profile/TEP
   pool) to return the lab to its clean starting state for future
   practice runs.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The VCP-NV (2V0-41.24) exam blueprint follows Broadcom's current
standardized five-section structure — foundational networking knowledge,
NSX product fundamentals, design judgment, hands-on deploy/configure/
operate competency, and troubleshooting — each of which maps to specific
sections of Chapters 8, 10, and 11 in this volume. Effective preparation
treats these as five separately assessable skills, weights lab repetition
heavily for the procedural sections, and draws exclusively from
authorized sources. This chapter's comprehensive, timed lab is designed
as a realistic self-assessment; performance against it, not comfort with
reading this volume, is the better signal for exam readiness.

- [ ] Can map each blueprint section to specific chapters in this volume.
- [ ] Has self-rated readiness across all five domains and targeted
      additional practice at the weakest one.
- [ ] Can complete NSX installation (transport zone through Edge cluster)
      from memory within a reasonable time box.
- [ ] Can complete logical networking and DFW configuration from memory
      within a reasonable time box.
- [ ] Can diagnose at least one deliberately introduced fault using
      Traceflow and BGP/transport node status without reference material.
- [ ] Has verified the current live exam guide against this chapter's
      summary before scheduling.
- [ ] Completed the comprehensive hands-on lab, including the negative
      test and cleanup.
