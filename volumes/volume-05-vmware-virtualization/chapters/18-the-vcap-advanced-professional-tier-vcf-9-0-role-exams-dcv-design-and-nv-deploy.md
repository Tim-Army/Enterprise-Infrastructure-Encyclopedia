# Chapter 18: The VCAP Advanced Professional Tier — VCF 9.0 Role Exams, DCV Design, and NV Deploy

![The VMware Certified Advanced Professional tier: a professional-tier (VCP) base row noting that a current VCP is the entry requirement, then the eight-exam VCF 9.0 role series on one 3V0 generation — Administrator (3V0-11.26), Architect (3V0-12.26), Support (3V0-13.26), Automation (3V0-21.25), Operations (3V0-22.25), Storage (3V0-23.25), VKS Kubernetes (3V0-24.25), Networking (3V0-25.25) — and two carried-over VCAP exams on older generations, VCAP-DCV Design (3V0-21.23) and VCAP-NV Deploy (3V0-41.22). Design-oriented VCAPs feed the Distinguished Expert defense in Chapter 19.](../../../diagrams/volume-05-vmware-virtualization/chapter-18-vcap-advanced-tier-map.svg)

*Figure 18-1. The advanced (3V0) tier: eight VCF 9.0 role exams on one generation, plus two carried-over VCAP exams. A current VCP is the gate; the design-oriented exams point onward to Chapter 19.*

## Learning Objectives

- Describe the VMware Certified Advanced Professional (VCAP) tier and how
  it differs from the VCP tier in [Chapters 12–17](17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md):
  advanced depth, a VCP prerequisite, and — for design exams — a bridge
  toward the Distinguished Expert defense.
- Identify the eight VCF 9.0 role-based VCAP exams and their codes, and
  explain why they share one `3V0` generation while the two carried-over
  VCAP exams do not.
- Map each advanced exam to the chapters in this volume that prepare it,
  and recognize where this volume's coverage is a foundation versus where
  Broadcom's advanced training is required to close the gap.
- Distinguish a *Design* VCAP (architecture judgment, no live build) from a
  *Deploy* VCAP (hands-on configuration against a clock) and prepare each
  in the way its format rewards.
- Sequence an advanced-tier plan realistically: which VCAP follows which
  VCP, and which design exams to prioritize if the Distinguished Expert
  credential is the goal.

## Theory and Architecture

The VCAP tier is the advanced level of the VMware certification hierarchy,
between the professional VCP tier and the Distinguished Expert. Where a VCP
attests competence in a role, a VCAP attests *advanced* competence — deeper
troubleshooting, larger-scale design, or hands-on deployment under time
pressure. A **current VCP is the prerequisite** for the VCAP tier; confirm
the exact qualifying VCP for each VCAP on Broadcom's page, since the
mapping is specific.

This chapter is study and review material, consistent with every
preparation chapter in this volume. It does not reproduce exam questions or
scoring weightings and is not a substitute for Broadcom's exam guides. The
codes below were verified against Broadcom's certification pages; verify
current blueprints, prerequisites, and delivery details directly before
scheduling, because the advanced tier is being actively rebuilt around VCF
9.0 and is the fastest-moving part of the program.

### The VCF 9.0 role series — eight exams, one generation

VMware Cloud Foundation 9.0 introduced a **role-based advanced series**:
eight VCAP exams on a common `3V0` generation, each attesting advanced
competence in one VCF role. They are the current heart of the tier:

| Role | Code | What it attests | This volume |
| --- | --- | --- | --- |
| Administrator | 3V0-11.26 | Advanced day-2 operation of a VCF fleet | [13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md), [14](14-vcp-vmware-cloud-foundation-administrator-2v0-17-25-exam-preparation.md) |
| Architect | 3V0-12.26 | Advanced VCF design — feeds the Distinguished Expert defense | [10](10-installing-vmware-nsx.md), [11](11-configuring-vmware-nsx.md) + design |
| Support | 3V0-13.26 | Advanced cross-component diagnosis | [13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md) |
| Automation | 3V0-21.25 | VCF Automation, infrastructure-as-code delivery | [9](09-vsphere-lifecycle-automation-observability-and-troubleshooting.md) |
| Operations | 3V0-22.25 | The VCF Operations suite (logs, metrics, flows) | [9](09-vsphere-lifecycle-automation-observability-and-troubleshooting.md), [13](13-vcp-vmware-cloud-foundation-support-2v0-15-25-exam-preparation.md) |
| Storage | 3V0-23.25 | vSAN and storage design/operation at scale | [6](06-vsphere-storage-and-vsan.md) |
| VKS (Kubernetes) | 3V0-24.25 | VCF Kubernetes Service / Supervisor | [8](08-vsphere-and-nsx-security-architecture.md) foundation |
| Networking | 3V0-25.25 | NSX within VCF 9.0 | [10](10-installing-vmware-nsx.md), [11](11-configuring-vmware-nsx.md) |

Two structural points matter. First, the eight share a generation, so a
candidate pursuing more than one benefits from the common VCF 9.0 platform
knowledge — the marginal cost of a second role exam is lower than the
first. Second, this volume is a **foundation** for these, not full advanced
coverage: the Automation, Operations, and VKS exams in particular reach
into VCF products (VCF Automation, the Operations suite, the VCF Kubernetes
Service) that Chapters 1–11 introduce but do not exhaust. Expect to
supplement with Broadcom's advanced training and hands-on time on the
specific product.

### The two carried-over VCAP exams — both retiring 31 July 2026

Alongside the VCF 9.0 series, two older-generation VCAP exams remain in
the catalog, but **both are retiring on 31 July 2026** — Broadcom's own
certification pages state no new exam registrations will be available
after that date (verified 23 July 2026). Treat them as closing, not as
options to plan a multi-month study path around:

- **VCAP-DCV Design (3V0-21.23) — retiring [31 July 2026](https://www.broadcom.com/support/education/vmware/certification/vcap-dcv-design).** Advanced
  vSphere 8 design. It historically was the most direct on-ramp to the
  Distinguished Expert defense (Chapter 19) because it exercises the same
  conceptual→logical→physical design discipline and the same
  requirement/constraint/assumption/risk analysis a defense demands. With
  its retirement, **the current design on-ramp is the VCF Architect role
  (3V0-12.26)** in the 9.0 series above — pursue that unless you can sit
  3V0-21.23 before the retirement date.
- **VCAP-NV Deploy (3V0-41.22) — retiring [31 July 2026](https://www.broadcom.com/support/education/vmware/certification/vcap-nv-deploy).** Advanced NSX-T
  hands-on **deployment** — a live-build exam rather than a multiple-choice
  one. It pairs with [VCP-NV (Chapter 12)](12-vcp-network-virtualization-2v0-41-24-exam-preparation.md)
  and rewards the timed build-and-troubleshoot practice that chapter's lab
  trains, but with the retirement its deploy-format practice now points
  toward the VCF Networking role (3V0-25.25) for anyone starting fresh.

### Design versus Deploy — two different exams to prepare for

The tier contains two fundamentally different exam formats, and conflating
them wastes preparation:

- A **Design** exam (VCAP-DCV Design, the Architect role) tests
  *architecture judgment*. There is no live system to configure; you reason
  from requirements to a defensible design. Prepare by articulating design
  decisions and their justifications, not by drilling configuration.
- A **Deploy** exam (VCAP-NV Deploy) tests *hands-on configuration against
  a clock*. Prepare by building, breaking, and rebuilding in a lab until
  the procedures are muscle memory, as in Chapter 12's timed lab.

Read each exam guide for its format before planning; the same "VCAP" label
covers both.

## Design Considerations

- **VCAP follows the matching VCP — but confirm the exact prerequisite.**
  The natural path is VCP-VCF Administrator → VCAP Administrator, VCP-NV →
  VCAP-NV Deploy, and so on. Broadcom specifies the qualifying VCP per
  VCAP, and it is not always the identically named one; check the page
  before assuming.
- **Prioritize by goal, not by completeness.** Very few readers should
  pursue all ten advanced exams. If the goal is operational seniority, one
  or two role exams matching your job (Administrator, Operations) suffice.
  If the goal is Distinguished Expert, a **Design** exam is the one that
  matters, because it rehearses the defense — and with VCAP-DCV Design
  retiring 31 July 2026, that now means the **VCF Architect role
  (3V0-12.26)** for anyone not already booked on 3V0-21.23.
- **This volume is a floor for the advanced tier.** Treat Chapters 1–11 as
  establishing the platform knowledge each advanced exam assumes coming in,
  then close the remaining gap with Broadcom's advanced courses and
  product-specific lab time. Do not expect this volume alone to carry an
  advanced exam the way it can carry a VCP.
- **The advanced tier moves fastest — verify currency hardest.** The VCF
  9.0 role series is new (`.25`/`.26` codes) and still settling; exam
  availability, prerequisites, and even which roles exist may change. The
  currency-check discipline in [Chapter 20](20-vmware-telco-cloud-and-keeping-the-certification-program-current.md)
  applies most sharply here.
- **Deploy exams demand a real lab; design exams demand a whiteboard.**
  Allocate lab hardware to the Deploy exams (VCAP-NV Deploy) where it is
  indispensable, and allocate uninterrupted articulation practice to the
  Design exams where a running lab helps far less than the ability to
  reason a design aloud.

## Implementation and Automation

### An advanced-tier study spine

```text
# Sequence advanced exams after the matching VCP. Rate readiness per
# exam 1–5; below 3 means supplement with Broadcom advanced training
# before booking. "Format" drives how you prepare, not just what.

Advanced exam (code)             | Format  | After VCP        | Rating
---------------------------------|---------|------------------|-------
VCAP-DCV Design (3V0-21.23)*     | Design  | VCP-DCV          |
VCAP-NV Deploy (3V0-41.22)*      | Deploy  | VCP-NV           |
  * both retiring 31 July 2026 — no new registrations after that date
VCF Administrator (3V0-11.26)    | Written | VCP-VCF Admin    |
VCF Architect (3V0-12.26)        | Design  | VCP-VCF Architect|
VCF Support (3V0-13.26)          | Written | VCP-VCF Support  |
VCF Automation (3V0-21.25)       | Written | VCP-VCF (role)   |
VCF Operations (3V0-22.25)       | Written | VCP-VCF (role)   |
VCF Storage (3V0-23.25)          | Written | VCP-VCF (role)   |
VCF VKS (3V0-24.25)              | Written | VCP-VCF (role)   |
VCF Networking (3V0-25.25)       | Written | VCP-NV / VCP-VCF |
```

### A Deploy-exam timed-build harness (reuse Chapter 12's approach)

```bash
# VCAP-NV Deploy rewards timed, unaided NSX builds. Wrap Chapter 12's
# lab in a timer and log elapsed time per phase so you can see which
# procedure is still too slow. Adapt paths to your lab.
start=$(date +%s)
echo "Phase 1 — transport zone, uplink profile, TEP pool, host prep"
# ... perform the build unaided ...
echo "Phase 1 elapsed: $(( ($(date +%s) - start) / 60 )) min"
```

### A Design-exam articulation template

```text
# For a Design exam (VCAP-DCV Design or Architect), practice turning a
# requirement into a justified design. Fill this from memory for a given
# scenario, then defend each cell aloud — that is the exam's real skill.

Requirement:
Constraint(s):
Assumption(s):
Risk(s) + mitigation:
Conceptual decision:
Logical decision:
Physical decision:
Justification (why this, not the alternative):
```

## Validation and Troubleshooting

- **Confirm the format before you prepare.** The clearest early
  self-check: can you state whether your target exam is Design, Deploy, or
  written? Preparing a Deploy exam with flashcards, or a Design exam with
  configuration drills, is the most common wasted effort at this tier.
- **Deploy readiness is a stopwatch, not a checklist.** For VCAP-NV Deploy,
  the readiness signal is completing Chapter 12's build phases unaided and
  within their time boxes repeatedly — not once. Log times across several
  attempts and watch the slowest phase, not the average.
- **Design readiness is an unaided justification.** For a Design exam, the
  signal is defending each design decision aloud against "why not the
  alternative?" without notes. If a decision can be stated but not defended,
  it is not yet ready.
- **Prerequisite gaps surface at registration, not before.** Because each
  VCAP requires a specific current VCP, verify your qualifying VCP is
  current and correct for the exact VCAP before investing study time; a
  lapsed or mismatched VCP blocks the booking.
- **Watch for role-series churn.** If a VCF 9.0 role exam code you prepared
  against no longer resolves on Broadcom's page, treat it as possibly
  renumbered or superseded and re-verify against the live certification
  landing page before rescheduling.

## Security and Best Practices

- Register only through Broadcom's authorized testing partner; Deploy exams
  in particular have specific lab-delivery and identification requirements —
  confirm them from the official portal well before exam day.
- Prepare Deploy exams in an isolated lab, never against production NSX —
  the timed, deliberately disruptive drills are unsafe against systems
  carrying real workloads.
- Do not use unauthorized dumps; at the advanced tier they are both a
  contractual violation and especially unreliable, since the VCF 9.0 series
  is new enough that circulating material is likely stale or fabricated.
- Handle any design document you author for practice as you would a real
  customer design — it will contain realistic architecture detail, and the
  habit of protecting it matters for the Distinguished Expert defense in
  [Chapter 19](19-vcdx-the-distinguished-expert-design-defense-discipline.md),
  where the design is the deliverable.

## References and Knowledge Checks

**References**

- [Broadcom Education Services — VMware certification](https://www.broadcom.com/support/education/vmware) —
  the authoritative exam guides for the VCF 9.0 role series (3V0-11.26
  through 3V0-25.25), VCAP-DCV Design (3V0-21.23), and VCAP-NV Deploy
  (3V0-41.22); confirm current codes, prerequisites, format, and price.
- [VMware Cloud Foundation documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vcf.html) —
  product reference for the VCF 9.0 role exams.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this repository's certification-to-volume mapping.
- [Appendix — VMware and Broadcom Certifications and Course Access](../../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md) —
  official training mapped to each advanced exam.
- See [Chapter 17](17-completing-the-vcp-tier-dcv-vcf-architect-avi-and-private-cloud-security.md)
  for the professional tier below this one, and
  [Chapter 19](19-vcdx-the-distinguished-expert-design-defense-discipline.md)
  for the design defense above it.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Broadcom exam item)*

1. Explain how a VCAP differs from a VCP in what it attests, and name the
   general prerequisite the VCAP tier imposes.
2. Why do the eight VCF 9.0 role exams share a `3V0` generation, and what
   practical advantage does that give a candidate taking more than one?
3. Distinguish a Design VCAP from a Deploy VCAP by format, and state how
   preparation should differ between them.
4. Which single advanced exam most directly rehearses the Distinguished
   Expert defense, and why?
5. Where is this volume a foundation rather than full coverage for the
   advanced tier, and how would you close that gap responsibly?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every objective in
the two format-defined VCAP exam guides** — VCAP-NV Deploy (3V0-41.22, ten
hands-on objectives) and VCAP-DCV Design (3V0-21.23, fourteen design
objectives). Following the house rule for design exams, the Design
objectives get **command-driven design walkthroughs** here — each reads the
real evidence a design decision rests on and records the decision and the
rejected alternative — *and* a reasoning-only **Design Exercise** section
below. The eight VCF 9.0 role exams (3V0-11.26 … 3V0-25.25) have no
published objective guide at press time; Lab 18.25 covers them against
Broadcom's standardized Deploy/Configure/Operate section. All labs are
mapped in the volume README's coverage table and end
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 18.1–18.24**

- For the Deploy labs: an NSX 4.x lab reachable at `$NSX` with an
  `Authorization` header in `$H` (as in Chapter 12). For the Design
  walkthroughs: read access to a reference VCF/vSphere environment and a
  requirements document to reason from.
- **Cost:** none beyond lab hardware; Deploy labs delete what they create,
  Design walkthroughs are read-only.

**VCAP-NV Deploy (3V0-41.22) — Labs 18.1–18.10**

### Lab 18.1 — Prepare NSX infrastructure (Objective 4.1)

**Objective:** Prepare a cluster as transport nodes with a transport-node
profile.

```bash
curl -sk -H "$H" "$NSX/api/v1/transport-node-collections" \
  | jq -r '.results[] | "\(.display_name)\t\(.state)"'
curl -sk -H "$H" "$NSX/api/v1/transport-nodes?node_types=HostNode" \
  | jq -r '.results[] | "\(.display_name)\t\(.node_deployment_info.os_type)"'
```

**Expected result:** a transport-node collection in `SUCCESS` and host
transport nodes listed — the prepared fabric an advanced deploy starts from.

**Negative test:** apply a transport-node profile referencing a missing
uplink profile; preparation fails on that host — profile dependencies are
validated.

**Cleanup:** none (read-only inspection of an existing prep).

### Lab 18.2 — Create and manage virtual networks (Objective 4.2)

**Objective:** Build a multi-segment overlay topology and confirm
realization.

```bash
for s in app db; do
  curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
    "$NSX/policy/api/v1/infra/segments/$s-seg" \
    -d "{\"display_name\":\"$s-seg\",\"connectivity_path\":\"/infra/tier-1s/t1-app\",\"subnets\":[{\"gateway_address\":\"10.20.${s/app/1}.1/24\"}]}"
done
curl -sk -H "$H" "$NSX/policy/api/v1/infra/realized-state/status?intent_path=/infra/tier-1s/t1-app" | jq -r '.publish_status'
```

**Expected result:** both segments realized (`publish_status: REALIZED`) on
the Tier-1 — a working multi-tier virtual network.

**Negative test:** overlapping subnets on two segments of the same Tier-1
are rejected at realization — the overlap constraint.

**Cleanup:** delete the two segments.

### Lab 18.3 — Deploy and manage network services (Objective 4.3)

**Objective:** Deploy a Tier-1 load balancer virtual server.

```bash
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/lb-services/lb-app" -d '{"connectivity_path":"/infra/tier-1s/t1-app","size":"SMALL"}'
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/lb-virtual-servers/vs-web" \
  -d '{"ip_address":"10.20.1.100","ports":["443"],"application_profile_path":"/infra/lb-app-profiles/default-https-lb-app-profile","lb_service_path":"/infra/lb-services/lb-app"}'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/lb-virtual-servers/vs-web" | jq -r '.ip_address'
```

**Expected result:** an LB service and a virtual server on `10.20.1.100:443`
— an L4/L7 network service delivered by NSX.

**Negative test:** attach a virtual server to an LB service on an
undersized/empty Edge cluster; it never reaches `UP` — Edge capacity gates
LB deployment.

**Cleanup:** delete the virtual server and LB service.

### Lab 18.4 — Secure a virtual data center (Objective 4.4)

**Objective:** Build a distributed-firewall micro-segmentation policy with a
default deny.

```bash
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/domains/default/security-policies/app-dfw" \
  -d '{"category":"Application","rules":[{"id":"web-to-app","display_name":"web-to-app","source_groups":["/infra/domains/default/groups/web"],"destination_groups":["/infra/domains/default/groups/app"],"services":["/infra/services/HTTPS"],"action":"ALLOW"},{"id":"deny","display_name":"deny","action":"DROP"}]}'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/domains/default/security-policies/app-dfw/rules" | jq -r '.results[] | "\(.display_name)\t\(.action)"'
```

**Expected result:** an allow for web→app on HTTPS followed by an explicit
deny — a zero-trust micro-segment.

**Negative test:** place the deny *above* the allow; legitimate web→app
traffic is dropped — DFW evaluates top-down, so order is the control.

**Cleanup:** delete the security policy.

### Lab 18.5 — Deploy central authentication (Objective 4.6)

**Objective:** Integrate an external identity source (Workspace ONE
Access/VIDM) for NSX auth.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/aaa/vidm" | jq -r '.vidm_enable, .host_name'
```

**Expected result:** `vidm_enable: true` with the configured host — NSX
delegates authentication to central SSO.

**Negative test:** a VIDM host with an untrusted certificate fails
integration; NSX rejects the OAuth handshake — the thumbprint must be
trusted.

**Cleanup:** none (read-only; do not disable a shared VIDM in a lab).

### Lab 18.6 — Configure Enhanced Data Path (Objective 5.1)

**Objective:** Confirm a segment/host is using the Enhanced Data Path
(N-VDSe) mode for NFV performance.

```bash
curl -sk -H "$H" "$NSX/api/v1/transport-nodes/<tn-id>" \
  | jq -r '.host_switch_spec.host_switches[] | "\(.host_switch_name)\t\(.host_switch_mode)"'
```

**Expected result:** a host switch reporting `ENS`/`ENS_INTERRUPT` mode —
the enhanced data path for high-throughput, latency-sensitive workloads.

**Negative test:** run a DPDK-dependent workload on a `STANDARD` host switch;
throughput falls short — the workload requires the enhanced data path mode.

**Cleanup:** none (read-only).

### Lab 18.7 — Configure Quality of Service (Objective 5.2)

**Objective:** Apply a QoS (traffic-shaping) profile to a segment.

```bash
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra/qos-profiles/qos-gold" \
  -d '{"shaper_configurations":[{"resource_type":"IngressRateShaper","enabled":true,"peak_bandwidth":200,"average_bandwidth":100,"burst_size":102400}]}'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/qos-profiles/qos-gold" | jq -r '.shaper_configurations[0].average_bandwidth'
```

**Expected result:** a QoS profile capping average ingress at 100 Mbps —
per-segment bandwidth control.

**Negative test:** a noisy segment with no QoS profile starves its
neighbors on a shared uplink; the profile is what bounds it.

**Cleanup:** delete the QoS profile.

### Lab 18.8 — Perform advanced troubleshooting (Objective 6.1)

**Objective:** Capture live packet flow with a port-connection / packet
capture between two ports.

```bash
curl -sk -X POST -H "$H" -H 'Content-Type: application/json' \
  "$NSX/api/v1/tools/tracepacket" \
  -d '{"source":{"lport_id":"<src>"},"destination":{"lport_id":"<dst>"},"payload":{"resource_type":"FieldsPayload","frame_size":128}}' | jq -r '.id'
```

**Expected result:** a trace whose observations pinpoint the exact
component (segment, DFW, gateway) that forwarded or dropped the packet —
advanced fault isolation.

**Negative test:** guessing from interface counters alone cannot say *which*
DFW rule dropped a flow; the trace names it.

**Cleanup:** none (diagnostic).

### Lab 18.9 — Perform operational management (Objective 7.1)

**Objective:** Take and verify an NSX Manager configuration backup.

```bash
curl -sk -X POST -H "$H" "$NSX/api/v1/cluster/backups?action=backup_to_remote"
curl -sk -H "$H" "$NSX/api/v1/cluster/backups/status" | jq -r '.cluster_backup_statuses[0] | "\(.success)\t\(.end_time)"'
```

**Expected result:** a backup with `success: true` and a fresh timestamp —
the operational safety net for the control plane.

**Negative test:** a backup to an unreachable SFTP target returns
`success: false`; operational management means verifying, not assuming, the
backup.

**Cleanup:** none.

### Lab 18.10 — Use API and CLI to manage a deployment (Objective 7.2)

**Objective:** Read realized state via the API to script an audit.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/realized-state/realized-entities?intent_path=/infra/segments/app-seg" \
  | jq -r '.results[] | "\(.entity_type)\t\(.state)"'
```

**Expected result:** each realized entity for the segment and its state —
the API surface that makes NSX auditable and automatable at scale.

**Negative test:** an intent whose realized entities show `ERROR` while the
intent object looks fine confirms realization, not intent, is where a
silent failure hides.

**Cleanup:** none (read-only).

**VCAP-DCV Design (3V0-21.23) — Labs 18.11–18.24 (command-driven design walkthroughs)**

### Lab 18.11 — Differentiate conceptual, logical, and physical design (Objective 1.2)

**Objective:** Read one running design at all three layers to tell them
apart in practice.

```powershell
Get-Cluster | Select Name, HAEnabled, DrsEnabled          # logical: what capability
Get-VMHost | Select Name, Model, ProcessorType, NumCpu    # physical: what hardware
```

**Decision to record:** the conceptual requirement ("tolerate one host
failure") → logical choice (HA + N+1) → physical instantiation (host count
and model). Note where a physical constraint forces a logical change.

**Negative test:** conflating logical and physical — sizing "4 hosts" before
the requirement is known — produces a design that cannot be justified from
objectives.

**Cleanup:** none (read-only).

### Lab 18.12 — Describe VMware Cloud Foundation architecture (Objective 2.1)

**Objective:** Read the actual VCF topology a design will extend.

```bash
curl -sk -H "Authorization: Bearer $token" "https://sddc-manager.lab/v1/domains" \
  | jq -r '.elements[] | "\(.name)\t\(.type)\t\(.clusters | length) clusters"'
```

**Decision to record:** whether the design adds a VI workload domain or
extends the management domain, and why — the VCF architectural boundary the
design must respect.

**Negative test:** designing workloads onto the management domain violates
VCF separation of concerns — the architecture constrains the design.

**Cleanup:** none (read-only).

### Lab 18.13 — Describe VMware Validated Solutions architecture (Objective 2.2)

**Objective:** Compare the environment against a Validated Solution's
prescribed component set.

```bash
curl -sk -H "Authorization: Bearer $token" "https://sddc-manager.lab/v1/vrslcm" \
  | jq -r '.status'   # lifecycle-managed solution components
```

**Decision to record:** which Validated Solution the design follows and any
justified deviation — VVS gives a proven baseline; deviations must be
argued, not accidental.

**Negative test:** a bespoke architecture that ignores the relevant
Validated Solution carries risk the VVS already retired.

**Cleanup:** none (read-only).

### Lab 18.14 — Gather and analyze requirements (Objective 3.1)

**Objective:** Turn stated objectives into classified requirements,
constraints, assumptions, and risks (RCAR).

```powershell
# inventory the current state the requirements will be measured against
Get-VMHost | Measure-Object -Property NumCpu,MemoryTotalGB -Sum |
  Select Property, Sum
Get-VM | Measure-Object | Select @{N='VMs';E={$_.Count}}
```

**Decision to record:** each business objective tagged R/C/A/R with a
measurable acceptance test. **Negative test:** an unmeasurable requirement
("must be fast") cannot be designed to or validated — rewrite it as a number
(p95 latency) before proceeding.

**Cleanup:** none (read-only).

### Lab 18.15 — Create a conceptual model (Objective 3.2)

**Objective:** Express the solution as capabilities, independent of product.

```powershell
Get-Cluster | Select Name, @{N='Capability';E={'compute-availability'}}
```

**Decision to record:** the conceptual entities (availability, security,
management) and their relationships — no product names yet. **Negative
test:** naming "vSAN" in the conceptual model prematurely binds a physical
choice a requirement might not support.

**Cleanup:** none (read-only).

### Lab 18.16 — Create a logical design (Objective 3.3)

**Objective:** Map capabilities to logical constructs (clusters, resource
pools, networks) with justification.

```powershell
Get-Cluster | Select Name, HAEnabled, DrsEnabled,
  @{N='FailuresToTolerate';E={($_ | Get-VsanClusterConfiguration).GuestTrimUnmap}} 2>$null
```

**Decision to record:** the logical cluster/network layout and the
requirement each element satisfies. **Negative test:** a logical element
with no traceable requirement is scope creep — remove or justify it.

**Cleanup:** none (read-only).

### Lab 18.17 — Create a physical design (Objective 3.4)

**Objective:** Specify concrete hardware/config that realizes the logical
design.

```powershell
Get-VMHost | Select Name, Model, NumCpu,
  @{N='RAM_GB';E={[math]::Round($_.MemoryTotalGB)}}, @{N='NICs';E={($_|Get-VMHostNetworkAdapter -Physical).Count}}
```

**Decision to record:** exact host count/model, NIC layout, and datastore
sizing, each traced to a logical requirement. **Negative test:** a physical
spec that cannot meet the logical N+1 (e.g. 2 hosts for a 3-host quorum) is
an invalid design.

**Cleanup:** none (read-only).

### Lab 18.18 — Design for manageability: capacity planning (Objective 3.5)

**Objective:** Read current utilization to size headroom.

```powershell
Get-Cluster | Get-Stat -Stat cpu.usage.average,mem.usage.average -Realtime -MaxSamples 1 |
  Group-Object MetricId | Select Name, @{N='AvgPct';E={[math]::Round(($_.Group.Value|Measure-Object -Average).Average,1)}}
```

**Decision to record:** the target utilization ceiling (e.g. 70%) and the
capacity buffer it implies. **Negative test:** designing to 100% utilization
leaves no room for failover or growth — a capacity design must reserve
headroom.

**Cleanup:** none (read-only).

### Lab 18.19 — Design for manageability: scalability (Objective 3.6)

**Objective:** Confirm the design's scale-out unit and its limits.

```powershell
Get-Cluster | Select Name, @{N='Hosts';E={($_|Get-VMHost).Count}}, @{N='MaxHosts';E={64}}
```

**Decision to record:** the scale-out increment (add-host vs add-cluster)
and the config maximum it approaches. **Negative test:** a design that
scales only by resizing hosts (scale-up) hits a hard ceiling a scale-out
unit avoids.

**Cleanup:** none (read-only).

### Lab 18.20 — Design for manageability: lifecycle (Objective 3.7)

**Objective:** Read the lifecycle-management baseline the design must
sustain.

```powershell
Get-Cluster | Select Name, @{N='Image';E={($_ | Get-LcmClusterImage).Version}} 2>$null
```

**Decision to record:** how the design is patched/upgraded (vLCM image vs
baseline) and the maintenance-window impact. **Negative test:** a design with
no rollback path for firmware/driver updates risks an unrecoverable upgrade.

**Cleanup:** none (read-only).

### Lab 18.21 — Design for availability (Objective 3.8)

**Objective:** Verify the availability mechanisms satisfy the RTO.

```powershell
Get-Cluster | Select Name, HAEnabled,
  @{N='AdmissionControl';E={$_.HAAdmissionControlEnabled}}, @{N='FailoverLevel';E={$_.HAFailoverLevel}}
```

**Decision to record:** the failures-to-tolerate and admission-control
policy that meet the stated RTO. **Negative test:** HA enabled but admission
control disabled means a failover may find no capacity — availability on
paper only.

**Cleanup:** none (read-only).

### Lab 18.22 — Design for performance (Objective 3.9)

**Objective:** Baseline latency against the performance requirement.

```powershell
Get-Stat -Entity (Get-Cluster) -Stat 'disk.maxTotalLatency.latest' -Realtime -MaxSamples 5 |
  Measure-Object Value -Maximum | Select @{N='MaxLatency_ms';E={$_.Maximum}}
```

**Decision to record:** the observed vs required latency and the design lever
(all-flash, storage policy, DRS) chosen to close any gap. **Negative test:**
designing for average latency ignores a p99 that violates the SLA.

**Cleanup:** none (read-only).

### Lab 18.23 — Design for security (Objective 3.10)

**Objective:** Read the current security posture the design must maintain or
raise.

```powershell
Get-VMHost | Select Name,
  @{N='LockdownMode';E={($_ | Get-View).Config.LockdownMode}},
  @{N='ExecInstalledOnly';E={($_ | Get-AdvancedSetting -Name VMkernel.Boot.execInstalledOnly).Value}}
```

**Decision to record:** the lockdown mode and secure-boot/execInstalledOnly
choices, traced to the security requirement. **Negative test:** a design that
leaves lockdown `disabled` on hosts handling regulated data fails its own
security objective.

**Cleanup:** none (read-only).

### Lab 18.24 — Design for recoverability (Objective 3.11)

**Objective:** Confirm the backup/replication design meets the RPO.

```powershell
Get-Cluster | Get-VM | Get-Snapshot | Select VM, Created, SizeGB |
  Sort-Object Created -Descending | Select -First 5
```

**Decision to record:** the backup frequency/replication interval that
satisfies the RPO, and the restore-test cadence. **Negative test:** relying
on snapshots as "backup" — they share the datastore's fate — fails
recoverability; the design needs off-array copies.

**Cleanup:** remove any lab snapshots created.

### Lab 18.25 — VCF 9.0 role-exam readiness (3V0-11.26 … 3V0-25.25)

**Objective:** Because the eight VCF 9.0 role exams publish no detailed
objective guide yet, exercise each role against Broadcom's standardized
**Deploy/Configure/Operate** section using the matching product surface —
Administrator/Operations (SDDC Manager + VCF Operations APIs, Chapter 14),
Architect (design chain, Labs 18.11–18.24), Networking (NSX, Chapter 12),
Storage (vSAN, Chapter 6), Support (Chapters 13/16), Automation (VCF
Operations Orchestrator, Lab 16.9), and VKS (vSphere Kubernetes Service).

```bash
# example — VKS/Supervisor readiness: confirm the Supervisor cluster is running
curl -sk -H "Authorization: Bearer $token" "https://vcenter.lab/api/vcenter/namespace-management/clusters" \
  | jq -r '.[] | "\(.cluster)\t\(.config_status)\t\(.kubernetes_status)"'
```

**Expected result:** for VKS, a Supervisor cluster `RUNNING`/`READY`; for
each other role, the Deploy/Configure/Operate lab already cited returns its
healthy baseline — a per-role readiness signal.

**Negative test:** treating a role exam as covered by the VCP of the same
product understates the advanced tier's depth; re-check against the live
guide once Broadcom publishes it ([[encyclopedia-cert-currency-check-cadence]]).

**Cleanup:** none (read-only).

### Lab 18.26 — Two-format readiness artifact (integrative)

**Objective:** Produce, without booking any exam, one concrete readiness
artifact for each of the two advanced-exam formats — a timed Deploy log and
a defended Design chain — so you can judge which format you are closer to
ready for.

**Prerequisites**

- The NSX lab from [Chapters 10–11](10-installing-vmware-nsx.md), reset to
  a clean state, and a timer (for the Deploy artifact).
- The Design articulation template from the Implementation section and one
  realistic scenario (for the Design artifact).
- No reference material open during the timed and articulation portions.

**Steps**

1. **Deploy artifact (timed, target 45 minutes).** Run
   [Chapter 12](12-vcp-network-virtualization-2v0-41-24-exam-preparation.md)'s
   NSX build (transport zone through Tier-0 BGP and a DFW policy) unaided,
   logging elapsed time per phase.

   **Expected result:** a per-phase time log, with the slowest phase
   identified as the VCAP-NV Deploy weak point to drill next.

2. **Design artifact (target 30 minutes).** Take one requirement (for
   example, "the design must survive the loss of any single availability
   zone with no data loss") and complete the Design articulation template
   from memory — conceptual, logical, physical, plus constraints,
   assumptions, and risks.

   **Expected result:** a filled template whose every decision you can
   defend aloud against "why not the alternative?"

3. **Defend the design (target 15 minutes).** Have a partner (or, working
   alone, a recorded self-review) challenge each design decision. Mark any
   decision you cannot justify unaided.

   **Expected result:** a list of design decisions needing more depth —
   the VCAP Design / Architect weak points.

4. **Compare formats.** Judge which artifact was stronger. A clean Deploy
   log with a slow but improving time points toward a Deploy exam; a design
   you can defend end to end points toward a Design exam and, beyond it,
   Chapter 19.

5. **Cleanup:** tear down the NSX build to its clean baseline and archive
   (do not discard) the design artifact — it is the seed of a Distinguished
   Expert design document.

## Design Exercise

VCAP-DCV Design (3V0-21.23) is a **design** exam: it rewards reasoning from
requirements to a defensible architecture, not configuration recall. The
command-driven walkthroughs above (Labs 18.11–18.24) exercise the evidence
each decision rests on; this exercise is the reasoning half — no lab
environment required, only a requirements set and justification.

**Scenario.** A regulated customer needs a VCF 9.0 private cloud for 400
VMs with these stated objectives: tolerate one host failure with no service
loss (RTO 0 for HA-restartable workloads), keep management and workload
domains separated, encrypt data at rest, sustain p99 storage latency under
5 ms, and recover any workload to within 15 minutes of failure (RPO 15m).
Budget caps the design at eight hosts total.

**Produce, defending each choice against a rejected alternative:**

1. **Requirements table** — classify each objective above as a requirement,
   constraint, assumption, or risk (RCAR), and give each a measurable
   acceptance test.
2. **Conceptual model** — the capabilities (availability, security,
   manageability, recoverability) with no product names.
3. **Logical design** — domain topology, cluster count and roles,
   failures-to-tolerate, network and storage-policy design; trace each
   element to a requirement.
4. **Physical design** — host count/model split across management and
   workload domains within the eight-host cap, NIC and datastore layout,
   encryption mechanism (vSAN data-at-rest vs VM encryption).
5. **Justification and risk** — for at least three decisions, state the
   alternative you rejected and why. Identify the requirement the eight-host
   constraint puts most at risk, and the design compromise you make.

**Success looks like:** every physical choice is traceable up through the
logical and conceptual layers to a stated objective, and no requirement is
left unaddressed or silently violated by the budget constraint — the
qualifying-standard a Design exam applies. This artifact is also the seed
of the VCDX design document ([Chapter 19](19-vcdx-the-distinguished-expert-design-defense-discipline.md)).

## Lab Verification

Complete this sign-off once both artifacts have been produced and the
design defended. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The VCAP tier is the advanced level between VCP and Distinguished Expert,
gated by a current VCP. Its current heart is the eight-exam VCF 9.0 role
series on one `3V0` generation — Administrator (3V0-11.26), Architect
(3V0-12.26), Support (3V0-13.26), Automation (3V0-21.25), Operations
(3V0-22.25), Storage (3V0-23.25), VKS (3V0-24.25), and Networking
(3V0-25.25) — alongside two carried-over exams, VCAP-DCV Design (3V0-21.23)
and VCAP-NV Deploy (3V0-41.22), **both retiring 31 July 2026**. Prepare by
format, not by label: Design
exams reward defensible architecture judgment, Deploy exams reward timed
unaided builds. This volume is the foundation the tier assumes; close the
remainder with Broadcom's advanced training. If Distinguished Expert is the
goal, a Design exam is the one that rehearses it.

- [ ] Can describe how the VCAP tier differs from the VCP tier and the
      prerequisite it imposes.
- [ ] Can list the eight VCF 9.0 role exams and why they share a
      generation.
- [ ] Can distinguish a Design exam from a Deploy exam and prepare each
      accordingly.
- [ ] Knows which advanced exam most rehearses the Distinguished Expert
      defense.
- [ ] Has produced both a timed Deploy log and a defended Design chain.
- [ ] Has verified the current codes, prerequisites, and formats against
      Broadcom before scheduling.
- [ ] Completed the hands-on lab, including archiving the design artifact.
