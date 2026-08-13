# Chapter 17: Completing the VCP Tier — Data Center Virtualization, VCF Architect, Avi, Private Cloud Security, and Cloud Operations

![The VMware Certified Professional tier shown complete: the five 2V0-generation exams already covered in Chapters 12–16 (VCP-NV 2V0-41.24, VCP-VCF Administrator 2V0-17.25, VCP-VCF Support 2V0-15.25, VCP-VVF Administrator 2V0-16.25, VCP-VVF Support 2V0-18.25) in one group, and the professional-level exams this chapter adds in a second group — VCP-DCV Data Center Virtualization (2V0-21.23, on the older vSphere 8 generation), VCP-VCF Architect (2V0-13.25), the two specialist-code VCPs VCP-AVI Avi Load Balancer Administrator (6V0-22.25) and VCP-PCS Private Cloud Security Administrator (6V0-21.25), and VCP-CO Cloud Operations (2V0-32.24). All ten sit at the same professional tier and none is a prerequisite for another.](../../../diagrams/volume-005-vmware-virtualization/chapter-17-vcp-tier-landscape.svg)

*Figure 17-1. The complete VCP tier: the five exams mapped in Chapters 12–16, plus the four shown here and VCP-CO Cloud Operations (2V0-32.24), added in this revision. Same tier throughout — sequence by the role you hold, not by exam number.*

## Learning Objectives

- Place the five remaining professional-level VMware exams — VCP-DCV
  (2V0-21.23), VCP-VCF Architect (2V0-13.25), VCP-AVI (6V0-22.25), VCP-PCS
  (6V0-21.25), and VCP-CO (2V0-32.24) — against the content already in this
  volume, and identify which existing chapters prepare each.
- Explain why VCP-DCV sits on the older vSphere 8 generation while the
  VVF/VCF exams target 9.0, and what that means for a candidate choosing
  between VCP-DCV and VCP-VVF Administrator.
- Distinguish the 2V0 mainstream-VCP code family from the 6V0 code family
  the Avi and Private Cloud Security exams carry, and read what that
  numbering signals about scope.
- Identify the VCP-VCF Architect exam as the design-role entry point that
  leads toward the VCAP Architect exam (Chapter 18) and, beyond it, the
  Distinguished Expert defense (Chapter 19).
- Build a self-assessment plan for each of the five exams that reuses this
  volume's existing labs rather than assuming a separate lab build.

## Theory and Architecture

Chapters 12 through 16 mapped five VMware Certified Professional exams to
this volume's content. They are not the whole professional tier. Broadcom's
current VCP lineup includes five more exams that this volume's material
already substantially prepares a reader for, and this chapter organizes
them the same way the earlier preparation chapters do: as blueprint-mapped
self-assessment material, not as reproductions of proprietary exam content.

As with every preparation chapter in this volume, this is study and review
material. It does not reproduce exam questions, does not reveal scoring
weightings, and is not a substitute for Broadcom's own exam guide. Confirm
current domain names, exam length, item count, and price against the
official exam guide before scheduling — the codes below were verified
against Broadcom's certification pages, but blueprints and delivery details
are revised independently of this repository's release cycle.

### The five exams and what each is

- **VCP-DCV — Data Center Virtualization (2V0-21.23).** The long-running
  flagship VCP, and the one most people mean by "the VCP." Its code
  (`.23`) places it on the **vSphere 8 generation**, one generation behind
  the 9.0-targeted VVF and VCF exams in Chapters 13–16. It tests core
  vSphere administration end to end — installation, configuration, VM and
  resource management, storage and vSAN, availability and mobility — which
  is exactly the ground [Chapters 1–9](01-vmware-virtualization-architecture-and-design.md)
  cover. For a reader whose environment is vSphere 8, this is the closest
  match; for a reader on 9.0, [VCP-VVF Administrator](15-vcp-vmware-vsphere-foundation-administrator-2v0-16-25-exam-preparation.md)
  is the current-generation equivalent.

- **VCP-VCF Architect (2V0-13.25).** The **design-role** VCP for VMware
  Cloud Foundation 9.0. Where VCP-VCF Administrator (Chapter 14) tests
  building and operating a VCF estate, the Architect exam tests *designing*
  one: turning requirements, constraints, and assumptions into a defensible
  conceptual, logical, and physical design. It is the professional-tier
  entry point to the design discipline that continues through
  [VCAP Architect (Chapter 18)](18-the-vcap-advanced-professional-tier-vcf-9-0-role-exams-dcv-design-and-nv-deploy.md)
  and culminates in the [Distinguished Expert defense (Chapter 19)](19-vcdx-the-distinguished-expert-design-defense-discipline.md).

- **VCP-AVI — Avi Load Balancer Administrator (6V0-22.25).** Covers the
  **VMware Avi Load Balancer** (formerly Avi Networks / NSX Advanced Load
  Balancer): a software-defined, scale-out application delivery controller
  providing load balancing, WAF, and GSLB with centralized policy. Its
  `6V0` code marks it as a **specialist** exam rather than a mainstream
  `2V0` VCP — narrower product scope, and independent of the vSphere/VCF
  sequence. It complements the North-South and application-delivery
  material adjacent to [Chapter 11](11-configuring-vmware-nsx.md)'s load
  balancing discussion.

- **VCP-PCS — Private Cloud Security Administrator (6V0-21.25).** Covers
  securing a VMware private cloud — the vDefend Distributed Firewall and
  Advanced Threat Prevention, micro-segmentation, and the platform
  hardening that [Chapter 8](08-vsphere-and-nsx-security-architecture.md)
  builds. Like VCP-AVI it carries a `6V0` specialist code and stands
  outside the administrator/support pairing.

- **VCP-CO — Cloud Operations (2V0-32.24).** Covers operating a VMware
  private cloud with the **Aria** management stack: **Aria Operations**
  (vRealize Operations) for metric analytics, capacity, and cost; **Aria
  Operations for Logs** (vRealize Log Insight) for log analytics; and
  **Aria Suite Lifecycle** (vRealize Suite Lifecycle Manager) for deploy,
  patch, and content management. Despite the operations focus it carries a
  mainstream `2V0` code, and its subject matter sits alongside
  [Chapter 9](09-vsphere-lifecycle-automation-observability-and-troubleshooting.md)'s
  observability and lifecycle material — though the Aria products themselves
  need their own lab, as this volume is vSphere/NSX-centric.

### Reading the code families

The exam number's prefix is a genuine signal, not decoration:

- **`2V0-…`** is the mainstream professional (VCP) family — VCP-DCV,
  VCP-VCF Architect/Administrator/Support, VCP-VVF Administrator/Support,
  VCP-NV, and VCP-CO (Cloud Operations). These are the broad, role-defining
  exams.
- **`6V0-…`** is the specialist family — narrower single-product scope
  (Avi, Private Cloud Security here). A `6V0` still confers a VCP-branded
  credential, but its blueprint is scoped to one product area rather than a
  whole platform role.
- **`3V0-…`** is the advanced (VCAP) family, and **`5V0-…`** the
  specialist-skills family — both covered in later chapters (18 and 20).

Knowing the family tells you roughly how wide to prepare before you open
the exam guide: a `2V0` expects platform breadth, a `6V0` expects depth in
one product.

## Design Considerations

- **DCV or VVF Administrator — pick by product generation, not prestige.**
  These two overlap heavily in content; the deciding factor is which
  vSphere generation you run and certify against. On vSphere 8, VCP-DCV
  (2V0-21.23) is the direct match. On vSphere Foundation 9.0, VCP-VVF
  Administrator (2V0-16.25) is current. Holding both adds little for most
  readers — they test the same core skill against different generations.
- **Architect before you can defend.** If the goal is the Distinguished
  Expert credential, VCP-VCF Architect is where the design vocabulary
  starts — requirements/constraints/assumptions/risks, and the
  conceptual→logical→physical progression. Treat it as the first rung of
  the design path, not a sideways option, and carry its habits into
  Chapters 18 and 19.
- **Specialist exams reward a running product, not reading.** VCP-AVI and
  VCP-PCS are `6V0` product exams; both are far easier to pass with the
  product actually deployed in a lab than from documentation. For Avi, that
  means a controller and service-engine pair with at least one virtual
  service configured; for PCS, a vDefend Distributed Firewall enforcing a
  real micro-segmentation policy as in [Chapter 8](08-vsphere-and-nsx-security-architecture.md).
- **Currency cuts hardest on the older generation.** VCP-DCV's vSphere 8
  blueprint is the most likely of the five to shift as a 9.0-generation DCV
  successor appears. Before committing study time, confirm on Broadcom's
  page that 2V0-21.23 is still the current DCV exam rather than assuming it
  from this chapter.
- **VCP-CO stands apart — it tests the Aria stack, not vSphere.** Unlike the
  other four, Cloud Operations targets Aria Operations, Aria Operations for
  Logs, and Aria Suite Lifecycle, which this volume does not deploy. Treat
  Chapters 1–9 as the platform context the exam assumes, and close the
  product-specific gap with a real Aria lab and the recommended vRealize
  Operations / Log Insight / Suite Lifecycle courses — reading alone will
  not carry it.
- **Ethical preparation boundary.** As with every exam in this volume,
  prepare only from authorized sources: Broadcom's documentation and exam
  guide, official training, and hands-on practice. Material claiming to
  reproduce actual scored questions violates the certification agreement
  and is frequently wrong against the live blueprint — treat any such
  resource as disqualifying rather than helpful.

## Implementation and Automation

### Mapping each exam to existing chapters

```text
# Reuse this volume's chapters as the study spine for all five exams.
# Rate each row 1–5; treat anything below 3 as needing lab time first.

Exam (code)                         | Primary chapters      | Self-rating
------------------------------------|-----------------------|------------
VCP-DCV (2V0-21.23)                 | 1,2,3,4,5,6,7,8,9     |
VCP-VCF Architect (2V0-13.25)       | 1,8,10,11 + design    |
VCP-AVI (6V0-22.25)                 | 4,11 (app delivery)   |
VCP-PCS (6V0-21.25)                 | 8,10,11 (vDefend)     |
VCP-CO (2V0-32.24)                  | 9 + Aria stack lab    |
```

### An Avi controller inventory drill (self-generated design questions)

```bash
# Against a lab Avi Controller, pull the virtual-service and pool
# inventory over the REST API, then practice explaining *why* each
# object is configured as it is — a design-judgment drill, not a
# config walkthrough. Replace host/credentials with your lab values.
curl -k -s -u 'admin:<AVI_ADMIN_PASSWORD>' \
  https://avi-controller.corp.example/api/virtualservice | \
  jq '.results[] | {name, enabled, services}'
curl -k -s -u 'admin:<AVI_ADMIN_PASSWORD>' \
  https://avi-controller.corp.example/api/pool | \
  jq '.results[] | {name, lb_algorithm, health_monitor_refs}'
```

### A Private Cloud Security posture check (reuse Chapter 8's lab)

```bash
# Confirm a micro-segmentation policy is actually enforcing before
# treating PCS preparation as done. Pull the DFW policy and rule
# inventory from NSX Manager (as in Chapter 8) and verify a
# default-deny plus scoped-allow structure exists.
curl -k -s -u 'admin:<NSX_ADMIN_PASSWORD>' \
  https://nsx-vip.corp.example/policy/api/v1/infra/domains/default/security-policies | \
  jq '.results[] | {display_name, category}'
```

## Validation and Troubleshooting

- **Generation check before DCV.** The single most common misstep on
  VCP-DCV is preparing against the wrong vSphere generation. Verify the
  live exam guide targets the version you have lab access to; a 9.0-only
  lab is a weaker fit for a vSphere 8 blueprint than it looks.
- **Design articulation for the Architect exam.** The readiness signal for
  VCP-VCF Architect is being able to state, out loud and unaided, why a
  given requirement forces a specific design decision and what constraint
  or assumption bounds it — not recognizing a correct diagram. Practice
  narrating a design, not reviewing one.
- **Specialist exams need the product running.** If VCP-AVI or VCP-PCS
  concepts are understood only well enough to recognize in documentation
  but not to configure unaided, treat them as not yet exam-ready. Both
  blueprints assume hands-on administration of the specific product.
- **Cross-check the 6V0 scope boundary.** A frequent trap on specialist
  exams is over-preparing platform breadth (the `2V0` mindset) and
  under-preparing the one product's depth. Confirm your study is scoped to
  Avi or vDefend specifically, not vSphere generally.

## Security and Best Practices

- Register only through Broadcom's authorized testing partner, and confirm
  current identification and proctoring requirements from the official
  registration portal before exam day; these vary by delivery method and
  change over time.
- Do not purchase or reference unauthorized exam dumps — beyond the
  contractual violation, they are commonly inaccurate against the live
  blueprint, which for VCP-DCV's older generation is a particular risk.
- Run the Avi and vDefend preparation labs in an isolated environment, not
  against production application-delivery or security enforcement — a
  mis-scoped DFW rule or a misconfigured virtual service can black-hole
  real traffic.
- Protect lab credentials (Avi Controller, NSX Manager) with the same
  discipline as production, per [Chapter 8](08-vsphere-and-nsx-security-architecture.md)'s
  RBAC and credential-hygiene guidance; building the habit in preparation
  reinforces it for the real deployment the credential attests to.

## References and Knowledge Checks

**References**

- [Broadcom Education Services — VMware certification](https://www.broadcom.com/support/education/vmware) —
  the authoritative exam guides for 2V0-21.23, 2V0-13.25, 6V0-22.25,
  6V0-21.25, and 2V0-32.24 (current blueprint domains, item count, duration,
  price, and registration requirements — verify directly before scheduling).
- [VMware Avi Load Balancer documentation](https://techdocs.broadcom.com/us/en/vmware-security-load-balancing/avi-load-balancer.html) —
  product reference for VCP-AVI preparation.
- [VMware Cloud Operations 8.x Professional exam guide (2V0-32.24)](https://docs.broadcom.com/docs/vmw-vcp-co-8-x-exam-guide) —
  the authoritative VCP-CO blueprint (seven standardized sections, 55
  objectives) that this chapter's Labs 17.73–17.127 map to.
- [VMware Aria Operations, Operations for Logs, and Suite Lifecycle documentation](https://techdocs.broadcom.com/us/en/vmware-cis/aria.html) —
  product reference for VCP-CO preparation.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this repository's certification-to-volume mapping.
- [Appendix — VMware and Broadcom Certifications and Course Access](../../volume-997-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md) —
  the course catalog mapping official training to each exam.
- See [Chapter 8](08-vsphere-and-nsx-security-architecture.md) for the
  security foundation behind VCP-PCS.
- See [Chapters 1–9](01-vmware-virtualization-architecture-and-design.md)
  for the vSphere core behind VCP-DCV.

**Knowledge checks** *(original conceptual review questions — not
reproductions of any Broadcom exam item)*

1. Explain why a reader running vSphere Foundation 9.0 might choose
   VCP-VVF Administrator over VCP-DCV, and when the reverse is correct.
2. From memory, distinguish what the `2V0` and `6V0` code families signal
   about an exam's breadth, and name one exam in each.
3. State the design progression VCP-VCF Architect begins and the two later
   milestones it leads to in this volume.
4. Given a lab with an Avi Controller and one virtual service, describe a
   design-judgment drill you could run without changing any configuration.
5. Why is preparing VCP-PCS from documentation alone weaker than for a
   `2V0` exam, and what minimum lab state closes that gap?

## Hands-On Lab

This chapter carries topic-level walkthrough labs for the five professional
exams it completes — **VCP-DCV (2V0-21.23)**, **VCP-VCF Architect
(2V0-13.25, a design exam)**, **VCP-AVI (6V0-22.25)**, **VCP-PCS
(6V0-21.25)**, and **VCP-CO (2V0-32.24)** — one lab per testable objective,
mapped in the volume README's coverage tables. The Architect design objectives get command-driven
design walkthroughs plus the Design Exercise below. Every lab ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites** — a vSphere 8.x/9.x lab (vCenter + ESXi + vSAN),
PowerCLI connected as administrator, SSH to hosts for `esxcli`; the AVI labs
add an NSX Advanced Load Balancer (Avi) Controller reachable at `$AVI` with
an `Authorization` header in `$AH`; the PCS labs add NSX with the vDefend
(distributed firewall/IDS-IPS) feature set; the VCP-CO labs use a separate
**Aria** stack (Aria Operations, Aria Operations for Logs, Aria Suite
Lifecycle) with its own prerequisites listed at Lab 17.73. **Cost:** none
beyond lab hardware; each lab cleans up after itself.

**VCP-DCV (2V0-21.23) — Labs 17.1–17.32**

### Lab 17.1 — Prerequisites and components for a vSphere 8.x implementation (Objective 1.1)

**Objective:** Confirm the version and build of the core components.

```powershell
Get-VMHost | Select Name, Version, Build
$global:DefaultVIServer | Select Name, Version, Build
```

**Expected result:** ESXi and vCenter at compatible 8.x versions/builds —
the interoperability prerequisite for the implementation.

**Negative test:** an ESXi build newer than vCenter is unsupported; vCenter
refuses to manage it until upgraded — the version-skew rule.

**Rollback:** none (read-only).

### Lab 17.2 — vCenter architecture and topology (Objective 1.2)

**Objective:** Read the vCenter Server Appliance's service topology.

```powershell
(Get-View ServiceInstance).Content.About |
  Select FullName, ApiVersion, InstanceUuid
```

**Expected result:** the appliance's product/API version and instance UUID —
the single-appliance vpxd/PSC-embedded topology of vSphere 8.

**Negative test:** expecting an external Platform Services Controller;
vSphere 8 has none (embedded only) — a topology change from 6.x.

**Rollback:** none (read-only).

### Lab 17.3 — vSphere Lifecycle Manager concepts (Objective 1.6)

**Objective:** Read whether a cluster is managed by a vLCM image or
baselines.

```powershell
Get-Cluster | Select Name,
  @{N='ImageManaged';E={[bool]($_ | Get-LcmImage -ErrorAction SilentlyContinue)}}
```

**Expected result:** each cluster's lifecycle model — a single desired-state
image is the vSphere 8 direction, replacing per-component baselines.

**Negative test:** mixing baseline and image management on one cluster is
not allowed; a cluster is one model or the other.

**Rollback:** none (read-only).

### Lab 17.4 — Use cases for VMware Tools (Objective 1.12)

**Objective:** Read guest Tools status to confirm the guest-integration
features it enables.

```powershell
Get-VM | Get-VMGuest | Select VmName, ToolsVersion, State |
  Sort-Object State
```

**Expected result:** per-VM Tools version/state; `toolsOk` enables quiesced
snapshots, guest customization, and graceful shutdown — the use cases the
objective tests.

**Negative test:** a VM with Tools `notRunning` cannot be gracefully shut
down or quiesced — the features that depend on Tools stop working.

**Rollback:** none (read-only).

### Lab 17.5 — vSphere in the Software-Defined Data Center (Objective 2.1)

**Objective:** Read the compute layer of the SDDC — vSphere as the
virtualization foundation NSX and vSAN build on.

```powershell
Get-Cluster | Select Name, @{N='Hosts';E={($_|Get-VMHost).Count}},
  @{N='vSAN';E={$_.VsanEnabled}}, DrsEnabled, HAEnabled
```

**Expected result:** clusters showing compute + vSAN state — vSphere is the
SDDC's compute pillar, with vSAN (storage) and NSX (network) layered on.

**Negative test:** treating vSphere as the whole SDDC ignores the network/
security virtualization NSX provides — vSphere is one pillar, not all three.

**Rollback:** none (read-only).

### Lab 17.6 — Use cases for vCenter Converter (Objective 2.3)

**Objective:** Identify a physical/foreign-VM workload that Converter would
migrate (P2V/V2V).

```powershell
# inventory candidate targets Converter would import into
Get-VMHost | Select Name, @{N='FreeGB';E={[math]::Round($_.MemoryTotalGB - $_.MemoryUsageGB)}}
Get-Datastore | Select Name, @{N='FreeGB';E={[math]::Round($_.FreeSpaceGB)}}
```

**Expected result:** hosts/datastores with capacity to receive a converted
workload — Converter's target. Converter itself is a standalone tool run
against the source.

**Negative test:** Converter cannot hot-clone a running physical host with
an unsupported OS; the use case has OS/version boundaries.

**Rollback:** none (read-only).

### Lab 17.7 — Configure Virtual Standard Switch advanced options (Objective 4.3)

**Objective:** Set security and teaming policy on a standard switch.

```powershell
$vs = Get-VMHost | Select -First 1 | Get-VirtualSwitch -Standard | Select -First 1
$vs | Get-SecurityPolicy | Set-SecurityPolicy -AllowPromiscuous $false `
  -ForgedTransmits $false -MacChanges $false
$vs | Get-NicTeamingPolicy | Select LoadBalancingPolicy, @{N='Active';E={$_.ActiveNic}}
```

**Expected result:** promiscuous mode / forged transmits / MAC changes all
rejected, and the teaming policy shown — the hardened VSS baseline.

**Negative test:** leaving `AllowPromiscuous` true lets any VM sniff the
port group — the exposure the secure baseline closes.

**Rollback:** restore prior security policy if changed.

### Lab 17.8 — Deploy and configure the vCenter Server Appliance (Objective 4.5)

**Objective:** Validate a VCSA deployment spec before an unattended install.

```bash
# on the VCSA installer media
./vcsa-deploy install --verify-only --accept-eula ./vcsa-embedded.json
```

**Expected result:** the template validation passes — the JSON spec (network,
SSO, appliance size) is correct for an unattended deploy.

**Negative test:** a spec whose target ESXi is unreachable or whose SSO
password fails complexity is rejected at `--verify-only`, before any
deployment.

**Rollback:** none (verify only; nothing deployed).

### Lab 17.9 — Deploy and configure vCenter High Availability (Objective 4.7)

**Objective:** Read vCenter HA cluster state (active/passive/witness).

```powershell
$vch = Get-View (Get-View ServiceInstance).Content.FailoverClusterManager -ErrorAction SilentlyContinue
$vch.GetVchaClusterHealth().RuntimeInfo | Select ClusterState, ClusterMode
```

**Expected result:** `ClusterState: healthy`, `ClusterMode: enabled` with
three nodes — vCenter survives an appliance failure.

**Negative test:** VCHA with active and passive on the same host defeats the
purpose; anti-affinity must separate them — a single host failure would take
both.

**Rollback:** none (read-only).

### Lab 17.10 — Configure vCenter file-based backup (Objective 4.11)

**Objective:** Schedule a file-based backup via the appliance management
API.

```bash
curl -sk -u administrator@vsphere.local -X POST \
  "https://vcsa.lab:5480/api/appliance/recovery/backup/schedules/daily" \
  -H 'Content-Type: application/json' \
  -d '{"location":"sftp://backup.lab/vc","recurrence_info":{"hour":2,"minute":0},"retention_info":{"max_count":7}}'
curl -sk -u administrator@vsphere.local "https://vcsa.lab:5480/api/appliance/recovery/backup/schedules" | jq -r 'keys[]'
```

**Expected result:** a `daily` schedule to the SFTP target, retaining 7 —
the supported vCenter backup method (no VM-level snapshot needed).

**Negative test:** backing up vCenter by snapshotting its VM instead risks
an inconsistent quiesce; file-based backup is the supported path.

**Rollback:** delete the `daily` schedule.

### Lab 17.11 — Configure vSphere Trust Authority (Objective 4.12)

**Objective:** Read the Trust Authority attestation state for a host.

```powershell
Get-VMHost | Select Name,
  @{N='Attested';E={($_ | Get-View).Runtime.CryptoState}}
```

**Expected result:** hosts reporting an attested crypto state — Trust
Authority verifies host integrity before releasing encryption keys.

**Negative test:** a host that fails attestation is denied encryption keys;
its encrypted VMs will not power on — the guarantee Trust Authority enforces.

**Rollback:** none (read-only).

### Lab 17.12 — Configure vSphere Lifecycle Manager (Objective 4.14)

**Objective:** Check cluster image compliance before remediation.

```powershell
Get-Cluster | ForEach-Object {
  $_ | Test-LcmClusterCompliance -ErrorAction SilentlyContinue |
    Select @{N='Cluster';E={$_.Cluster}}, Status
}
```

**Expected result:** each cluster's compliance (`Compliant` / `NonCompliant`)
against its desired-state image — the drift vLCM remediates.

**Negative test:** remediating a `NonCompliant` cluster without checking
hardware-compatibility (vSAN HCL) first can fail mid-rollout — check
compliance and HCL before remediation.

**Rollback:** none (read-only).

### Lab 17.13 — Configure different network stacks (Objective 4.15)

**Objective:** Add a dedicated TCP/IP stack (e.g. for vMotion).

```powershell
$h = Get-VMHost | Select -First 1
$h | Get-VMHostNetworkStack | Select Id, @{N='Gateway';E={$_.DefaultGateway}}
# a VMkernel on the vMotion stack isolates its routing table
$h | Get-VMHostNetworkAdapter -VMKernel | Select Name, @{N='Stack';E={$_.ExtensionData.Spec.NetStackInstanceKey}}
```

**Expected result:** the default, vMotion, and provisioning stacks, each with
its own gateway — traffic-type isolation at the routing level.

**Negative test:** running vMotion on the default stack forces it to share
the management gateway; a dedicated stack gives vMotion its own route.

**Rollback:** none (read-only).

### Lab 17.14 — Configure host profiles (Objective 4.16)

**Objective:** Extract a host profile from a reference host.

```powershell
$ref = Get-VMHost | Select -First 1
New-VMHostProfile -Name dcv-profile -ReferenceHost $ref
Get-VMHostProfile -Name dcv-profile | Select Name, @{N='RefHost';E={$_.ReferenceHost}}
```

**Host setup — deploying this image on your hypervisor.** The create/import and interface-mapping steps are the same for every appliance and are collected once in the Master Appendices: [Deploying Lab Appliance Images on Each Hypervisor](../../volume-997-master-appendices/chapters/73-appendix-deploying-lab-appliance-images-on-each-hypervisor.md) — Proxmox, KVM, ESXi/vSphere, Workstation/Fusion, VirtualBox, Hyper-V, EVE-NG, GNS3, containerlab, Nutanix AHV, and Xen.

**Expected result:** a host profile capturing the reference host's config —
the template for consistent host configuration.

**Negative test:** applying the profile to a host with different physical
NICs raises compliance failures on the NIC mappings — profiles encode
host-specific bindings that must be customized.

**Rollback:** `Remove-VMHostProfile -Profile (Get-VMHostProfile dcv-profile) -Confirm:$false`.

### Lab 17.15 — Monitor VCSA and vSphere resources (Objective 5.2)

**Objective:** Read appliance and cluster resource pressure.

```powershell
Get-Cluster | Get-Stat -Stat cpu.usage.average,mem.usage.average -Realtime -MaxSamples 1 |
  Select Entity, MetricId, Value
```

**Expected result:** current CPU/memory pressure per cluster — the health
signal to act on before contention hits guests.

**Negative test:** monitoring guest metrics only misses VCSA appliance
exhaustion, which degrades the whole management plane.

**Rollback:** none (read-only).

### Lab 17.16 — Identify and use resource monitoring tools (Objective 5.3)

**Objective:** Use `esxtop` batch mode to capture host-level counters.

```bash
esxtop -b -n 1 | head -1 | tr ',' '\n' | grep -iE '%RDY|%USED|%SWPWT' | head
```

**Expected result:** the counter columns available (CPU ready, used, swap
wait) — the authoritative host tool alongside vCenter performance charts.

**Negative test:** vCenter charts sample at coarser intervals than `esxtop`;
a sub-20-second contention spike is visible in `esxtop` but averaged away in
charts — pick the tool for the timescale.

**Rollback:** none (read-only).

### Lab 17.17 — Configure Network I/O Control (Objective 5.4)

**Objective:** Reserve bandwidth for a traffic type on a distributed switch.

```powershell
$vds = Get-VDSwitch | Select -First 1
$vds | Get-VDResourcePool 2>$null
# NIOC shares/reservation per system traffic (vMotion, mgmt, vSAN)
(Get-View $vds.Id).Config.VmVnicNetworkResourcePool | Select Name, @{N='Reservation';E={$_.AllocationInfo.Reservation}}
```

**Expected result:** NIOC enabled with per-traffic shares/reservations — the
control that keeps vMotion from starving vSAN on a shared uplink.

**Negative test:** without NIOC, a vMotion burst saturates the uplink and
delays vSAN I/O — the contention NIOC bounds.

**Rollback:** none (read-only).

### Lab 17.18 — Configure Storage I/O Control (Objective 5.5)

**Objective:** Enable SIOC on a datastore and set a congestion threshold.

```powershell
$ds = Get-Datastore | Where-Object {$_.Type -eq 'VMFS'} | Select -First 1
$ds | Set-Datastore -StorageIOControlEnabled $true
$ds | Select Name, StorageIOControlEnabled
```

**Expected result:** `StorageIOControlEnabled: True` — VMs get fair datastore
I/O by shares when latency crosses the threshold.

**Negative test:** without SIOC, a single VM's I/O storm inflates latency for
every VM on the datastore — the "noisy neighbor" SIOC arbitrates.

**Rollback:** `$ds | Set-Datastore -StorageIOControlEnabled $false`.

### Lab 17.19 — Offload a VM port group to a DPU (Objective 5.6)

**Objective:** Confirm a host's data-processing-unit (DPU) offload
capability.

```bash
esxcli network nic dpu list 2>/dev/null
esxcli system settings kernel list -o dpuOffload 2>/dev/null
```

**Expected result:** a listed DPU device (if present) — network processing
offloaded from host CPU to the SmartNIC, freeing cores for workloads.

**Negative test:** enabling DPU-backed networking on a host with no DPU has
no effect; the hardware must be present and in the switch's offload config.

**Rollback:** none (read-only).

### Lab 17.20 — Performance impact of VM snapshots (Objective 5.7)

**Objective:** Observe delta-disk growth that degrades performance.

```powershell
$vm = Get-VM | Select -First 1
$vm | New-Snapshot -Name perf-test
$vm | Get-Snapshot | Select Name, @{N='SizeMB';E={[math]::Round($_.SizeMB)}}, Created
```

**Expected result:** a snapshot whose delta grows with every write — long-
lived snapshots inflate I/O and consume datastore space.

**Negative test:** treating snapshots as backups leaves them for weeks; the
delta chain slows the VM and risks datastore-full — snapshots are short-term.

**Rollback:** `$vm | Get-Snapshot | Remove-Snapshot -Confirm:$false`.

### Lab 17.21 — Use Update Planner (Objective 5.8)

**Objective:** Read Update Planner interoperability for a target vCenter
version.

```powershell
# via vSphere Automation API — pre-update checks / interop
Get-View (Get-View ServiceInstance).Content.About | Select Version, Build
```

**Expected result:** the current version as the Planner's baseline; Update
Planner then reports interop and pre-checks for the chosen target release.

**Negative test:** upgrading vCenter without checking Update Planner interop
can strand an incompatible external product (e.g. an old SRM) — the check
prevents it.

**Rollback:** none (read-only).

### Lab 17.22 — Use performance charts (Objective 5.10)

**Objective:** Pull an overview performance metric series for a VM.

```powershell
Get-Stat -Entity (Get-VM | Select -First 1) -Stat cpu.ready.summation `
  -Realtime -MaxSamples 10 | Select Timestamp, Value
```

**Expected result:** a CPU-ready time series — the chart data that reveals
contention over time, not just an instant.

**Negative test:** reading a single sample hides a periodic spike a chart's
series exposes — trends need multiple samples.

**Rollback:** none (read-only).

### Lab 17.23 — Proactive management with Skyline (Objective 5.11)

**Objective:** Read Skyline Health findings (proactive advisories).

```powershell
Get-VMHost | Select -First 1 | Get-View |
  ForEach-Object { $_.ConfigManager.HealthStatusManager } 2>$null
# Skyline Health surfaces proactive findings in vCenter's Skyline Health UI/API
```

**Expected result:** health findings with recommended actions — proactive
signals before a problem becomes an outage.

**Negative test:** waiting for an alarm is reactive; Skyline flags a known
issue (e.g. a risky driver) before it triggers — proactive vs reactive.

**Rollback:** none (read-only).

### Lab 17.24 — Update vCenter via the management interface (Objective 5.12)

**Objective:** Check for available patches through the VAMI update API.

```bash
curl -sk -u administrator@vsphere.local \
  "https://vcsa.lab:5480/api/appliance/update/pending?source_type=LAST_CHECK" | jq -r '.[].version'
```

**Expected result:** any pending patch versions — the appliance's supported
patch path (VAMI on 5480), not an in-guest package manager.

**Negative test:** patching the VCSA's underlying Photon OS with `tdnf`
directly is unsupported and can break the appliance — use VAMI.

**Rollback:** none (read-only).

### Lab 17.25 — Enable vCLS retreat mode (Objective 6.1)

**Objective:** Use retreat mode to remove vCLS agent VMs for maintenance.

```powershell
$cl = Get-Cluster | Select -First 1
$dom = $cl.ExtensionData.MoRef.Value   # domain-c<N>
New-AdvancedSetting -Entity $global:DefaultVIServer `
  -Name "config.vcls.clusters.$dom.enabled" -Value $false -Confirm:$false
```

**Expected result:** the advanced setting `...enabled = false` — vCLS agent
VMs are removed, the documented retreat-mode procedure for datastore
maintenance.

**Negative test:** deleting vCLS VMs by hand without retreat mode; vCenter
recreates them immediately — retreat mode is the only supported removal.

**Rollback:** set the value back to `$true` to restore vCLS.

### Lab 17.26 — Generate a log bundle (Objective 6.3)

**Objective:** Export a host support bundle for diagnostics.

```bash
vm-support -w /vmfs/volumes/datastore1/support 2>/dev/null &
ls -1 /vmfs/volumes/datastore1/support/*.tgz 2>/dev/null | tail -1
```

**Expected result:** a `.tgz` support bundle — the log set VMware support and
deep troubleshooting require.

**Negative test:** collecting only `/var/log` misses configuration and state
that `vm-support` bundles — the full bundle is what's actionable.

**Rollback:** delete the support bundle after use.

### Lab 17.27 — Create and manage VM snapshots (Objective 7.1)

**Objective:** Take, list, and revert a snapshot.

```powershell
$vm = Get-VM | Select -First 1
$vm | New-Snapshot -Name pre-change -Description 'before test'
$vm | Get-Snapshot | Select Name, Created
$vm | Get-Snapshot -Name pre-change | Set-VM -Snapshot {$_} -Confirm:$false
```

**Expected result:** a snapshot created, listed, and reverted to — a
point-in-time rollback for a risky change.

**Negative test:** a snapshot taken with memory on a heavily loaded VM can
stun it during quiesce; know when to exclude memory.

**Rollback:** `$vm | Get-Snapshot | Remove-Snapshot -Confirm:$false`.

### Lab 17.28 — Create DRS affinity and anti-affinity rules (Objective 7.5)

**Objective:** Keep two VMs apart with an anti-affinity rule.

```powershell
$cl = Get-Cluster | Select -First 1
New-DrsRule -Cluster $cl -Name keep-apart -KeepTogether $false `
  -VM (Get-VM | Select -First 2)
Get-DrsRule -Cluster $cl | Select Name, KeepTogether, Enabled
```

**Expected result:** an anti-affinity rule spreading the two VMs across
hosts — HA for a clustered app pair.

**Negative test:** an anti-affinity rule for 3 VMs on a 2-host cluster cannot
be satisfied; DRS reports a rule violation — rule needs enough hosts.

**Rollback:** `Get-DrsRule -Cluster $cl -Name keep-apart | Remove-DrsRule -Confirm:$false`.

### Lab 17.29 — Configure role-based access control (Objective 7.7)

**Objective:** Create a custom role and assign it scoped to a folder.

```powershell
New-VIRole -Name dcv-operator -Privilege (Get-VIPrivilege -Id VirtualMachine.Interact.PowerOn,VirtualMachine.Interact.PowerOff)
New-VIPermission -Entity (Get-Folder -Name vm) -Principal 'lab\ops' `
  -Role (Get-VIRole -Name dcv-operator) -Propagate:$true
Get-VIPermission | Where-Object {$_.Role -eq 'dcv-operator'} | Select Principal, Role
```

**Expected result:** a custom power-on/off role bound to the VM folder — least
privilege by role and scope.

**Negative test:** a `dcv-operator` principal tries to reconfigure a VM's
hardware; denied — the role grants power control only.

**Rollback:** remove the permission and role.

### Lab 17.30 — Manage host profiles (Objective 7.8)

**Objective:** Check a host's compliance against its attached profile.

```powershell
Get-VMHost | Where-Object {$_ | Get-VMHostProfile} |
  ForEach-Object { Test-VMHostProfileCompliance -VMHost $_ } |
  Select VMHost, IncomplianceElementList
```

**Expected result:** compliance results per host; any `IncomplianceElement`
names the drifted setting to remediate.

**Negative test:** applying a profile without first placing the host in
maintenance mode fails for settings that require it — order matters.

**Rollback:** none (read-only compliance check).

### Lab 17.31 — Use predefined alarms (Objective 7.10)

**Objective:** List a built-in alarm and its trigger.

```powershell
Get-AlarmDefinition | Where-Object {$_.Name -match 'host connection'} |
  Select Name, Enabled, @{N='Trigger';E={($_ | Get-AlarmDefinition).ExtensionData.Info.Expression.Expression.EventTypeId}}
```

**Expected result:** the predefined "host connection and power" alarm and its
event trigger — coverage that ships with vCenter.

**Negative test:** assuming predefined alarms notify by default; most only
change state — an action (email/SNMP) must be added to be alerted.

**Rollback:** none (read-only).

### Lab 17.32 — Create custom alarms (Objective 7.11)

**Objective:** Create a custom alarm on a metric threshold.

```powershell
$m = New-AlarmDefinition -Name high-vm-cpu -Entity (Get-Datacenter | Select -First 1) `
  -MetricCondition -Metric 'cpu.usage.average' -Operator IsAbove -Threshold 90 `
  -ErrorAction SilentlyContinue
Get-AlarmDefinition -Name high-vm-cpu | Select Name, Enabled
```

**Expected result:** a custom alarm firing above 90% CPU — monitoring tuned
to a workload's own threshold.

**Negative test:** a threshold set at 100% never fires before saturation is
already hurting; thresholds must leave reaction headroom.

**Rollback:** `Get-AlarmDefinition -Name high-vm-cpu | Remove-AlarmDefinition -Confirm:$false`.

**VCP-VCF Architect (2V0-13.25, design) — Labs 17.33–17.40**

### Lab 17.33 — Differentiate business and technical requirements (Objective 1.1)

**Objective:** Separate a stated need into its business "why" and technical
"what," reading the current state each is measured against.

```powershell
Get-VM | Measure-Object | Select @{N='VMs';E={$_.Count}}
Get-Cluster | Select Name, @{N='Hosts';E={($_|Get-VMHost).Count}}
```

**Decision to record:** for one requirement, write the business objective
("reduce risk of outage") and the technical requirement it implies ("N+1 HA,
RTO 0"). **Negative test:** a technical requirement with no business driver
is unjustifiable scope; a business objective with no technical requirement
is not buildable — each needs its pair.

**Rollback:** none (read-only).

### Lab 17.34 — Differentiate conceptual, logical, and physical design (Objective 1.2)

**Objective:** Read a running design at each layer to keep them distinct.

```powershell
Get-Cluster | Select Name, HAEnabled, DrsEnabled           # logical
Get-VMHost | Select Name, Model, NumCpu                    # physical
```

**Decision to record:** the conceptual capability → the logical construct →
the physical instantiation for one requirement. **Negative test:** naming a
product in the conceptual model prematurely binds a physical choice the
requirements may not support.

**Rollback:** none (read-only).

### Lab 17.35 — Differentiate requirements, assumptions, constraints, risks (Objective 1.3)

**Objective:** Classify each design input (RCAR) with the current-state
evidence.

```powershell
Get-VMHost | Measure-Object MemoryTotalGB -Sum | Select @{N='TotalRAM_GB';E={[math]::Round($_.Sum)}}
```

**Decision to record:** tag each input requirement / constraint (e.g. the
host cap) / assumption / risk, each with a measurable test. **Negative
test:** an unstated assumption ("the network is 25 GbE") becomes an
undocumented risk if wrong — surface it.

**Rollback:** none (read-only).

### Lab 17.36 — Develop a risk mitigation strategy (Objective 1.5)

**Objective:** Identify a single point of failure and the mitigation.

```powershell
Get-Cluster | Select Name, @{N='Hosts';E={($_|Get-VMHost).Count}},
  @{N='AdmissionControl';E={$_.HAAdmissionControlEnabled}}
```

**Decision to record:** for the top risk (e.g. a 2-host cluster with no
failover capacity), the mitigation (add a host / enable admission control)
and its cost. **Negative test:** logging a risk with no mitigation and no
owner is not risk management — each risk needs a response.

**Rollback:** none (read-only).

### Lab 17.37 — Document design decisions (Objective 1.6)

**Objective:** Capture a decision with its justification and alternative.

```powershell
Get-Cluster | Select Name, @{N='vSAN';E={$_.VsanEnabled}}
```

**Decision to record:** one decision as {decision, justification, rejected
alternative, impact} — e.g. "vSAN over external array: no SAN skills on
staff (justification); rejected FC array (alternative); adds host-local
disk cost (impact)." **Negative test:** a decision with no recorded
alternative cannot be defended in a design review — the rejected option is
the argument.

**Rollback:** none (read-only).

### Lab 17.38 — Develop a design validation strategy (Objective 1.7)

**Objective:** Define the test that proves the design meets a requirement.

```powershell
Get-Cluster | Select Name, HAEnabled, HAFailoverLevel
```

**Decision to record:** the validation test for the HA requirement (power
off a host; confirm VMs restart within RTO). **Negative test:** a design
signed off without a validation test can fail its first real failover — the
test is the proof.

**Rollback:** none (read-only).

### Lab 17.39 — Gather and analyze business objectives (Objective 3.1)

**Objective:** Translate objectives into measurable acceptance criteria.

```powershell
Get-Datastore | Select Name, @{N='FreeGB';E={[math]::Round($_.FreeSpaceGB)}}, @{N='CapGB';E={[math]::Round($_.CapacityGB)}}
```

**Decision to record:** each objective with a number (capacity growth %,
RPO, RTO) the design will be measured by. **Negative test:** "improve
performance" without a metric cannot be designed to or validated.

**Rollback:** none (read-only).

### Lab 17.40 — Create a conceptual model (Objective 3.2)

**Objective:** Express the solution as capabilities and relationships, no
products.

```powershell
Get-Cluster | Select Name, @{N='Capabilities';E={'availability, performance, manageability'}}
```

**Decision to record:** the conceptual entities and how they relate, traced
to the objectives from 3.1. **Negative test:** a conceptual model that
already names vSAN/NSX has skipped to physical — keep it product-neutral.

**Rollback:** none (read-only).

**VCP-AVI (6V0-22.25) — Labs 17.41–17.61 (NSX Advanced Load Balancer / Avi)**

### Lab 17.41 — Distributed data plane (Objective 1.2)

**Objective:** Read the Service Engines that form Avi's distributed data
plane.

```bash
curl -sk -H "$AH" "$AVI/api/serviceengine" | jq -r '.results[] | "\(.name)\t\(.oper_status.state)"'
```

**Expected result:** multiple Service Engines `OPER_UP` — the data plane is
distributed across SEs, not a single appliance.

**Negative test:** a single SE is a single point of failure; a distributed
data plane needs an SE group with more than one member.

**Rollback:** none (read-only).

### Lab 17.42 — Service Engine tasks (Objective 1.3)

**Objective:** Read what an SE handles (virtual services placed on it).

```bash
curl -sk -H "$AH" "$AVI/api/serviceengine" | jq -r '.results[0].virtualservice_refs | length'
```

**Expected result:** the count of virtual services an SE hosts — the SE
terminates client connections, load-balances to pools, and runs policies.

**Negative test:** placing every virtual service on one SE overloads it;
placement across the SE group is what scales.

**Rollback:** none (read-only).

### Lab 17.43 — L4 load-balancing characteristics (Objective 1.4)

**Objective:** Read an L4 (TCP/UDP) virtual service.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | select(.application_profile_ref|test("System-L4")) | .name'
```

**Expected result:** virtual services using an L4 application profile — fast
transport-layer load balancing with no HTTP awareness.

**Negative test:** expecting content-based routing on an L4 VS fails; L4 has
no visibility into HTTP headers/URLs — that needs L7.

**Rollback:** none (read-only).

### Lab 17.44 — L7 load-balancing characteristics (Objective 1.5)

**Objective:** Read an L7 (HTTP) virtual service and its rules.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | select(.application_profile_ref|test("System-HTTP")) | "\(.name)\t\(.http_policies|length) policies"'
```

**Expected result:** HTTP virtual services with policy counts — L7 inspects
headers/URLs for content switching, redirects, and WAF.

**Negative test:** an L7 VS without SSL termination cannot inspect encrypted
payloads; HTTPS content rules require TLS termination at the VS.

**Rollback:** none (read-only).

### Lab 17.45 — High-availability modes (Objective 1.7)

**Objective:** Read the SE group HA mode (Active/Active, N+M, Active/Standby).

```bash
curl -sk -H "$AH" "$AVI/api/serviceenginegroup" | jq -r '.results[] | "\(.name)\t\(.ha_mode)"'
```

**Expected result:** each SE group's `ha_mode` (`HA_MODE_SHARED` = N+M,
`HA_MODE_SHARED_PAIR` = A/S, `HA_MODE_LEGACY_ACTIVE_STANDBY`) — the failover
model.

**Negative test:** Active/Active needs enough SE capacity to absorb a peer's
load on failure; undersizing defeats the HA mode.

**Rollback:** none (read-only).

### Lab 17.46 — Service Engine Groups (Objective 1.8)

**Objective:** Read SE group sizing parameters.

```bash
curl -sk -H "$AH" "$AVI/api/serviceenginegroup" | jq -r '.results[] | "\(.name)\tmax_se=\(.max_se)\tvs_per_se=\(.max_vs_per_se)"'
```

**Expected result:** per-group `max_se` and `max_vs_per_se` — the group is
the unit of SE scaling and tenancy isolation.

**Negative test:** two tenants sharing one SE group share fate and capacity;
isolation requires separate groups.

**Rollback:** none (read-only).

### Lab 17.47 — Elastic scale-out use case (Objective 1.9)

**Objective:** Read a virtual service's scaled-out SE set.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | "\(.name)\t\(.num_se_assigned // 1) SEs"'
```

**Expected result:** virtual services spread across multiple SEs — Avi scales
a VS out under load without a config change.

**Negative test:** a VS pinned to one SE cannot scale out; elastic scale-out
requires the SE group to permit it.

**Rollback:** none (read-only).

### Lab 17.48 — Virtual service, pool, and VIP interaction (Objective 1.10)

**Objective:** Trace a VS to its pool and VIP.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[0] | "\(.name)\tVIP:\(.vip[0].ip_address.addr)\tpool:\(.pool_ref)"'
```

**Expected result:** the VS bound to a VIP (front-end IP) and a pool
(back-end servers) — the three-object model of an Avi service.

**Negative test:** a VS with no pool has nowhere to send traffic; the VIP
answers but every request fails — all three objects are required.

**Rollback:** none (read-only).

### Lab 17.49 — Features inside an application profile (Objective 1.11)

**Objective:** Read an application profile's L7 feature set.

```bash
curl -sk -H "$AH" "$AVI/api/applicationprofile" | jq -r '.results[] | "\(.name)\t\(.type)"'
```

**Expected result:** profiles (System-HTTP, System-L4, System-Secure-HTTP)
whose type sets features — caching, compression, X-Forwarded-For, WAF.

**Negative test:** applying an L4 profile to a service needing HTTP caching
disables the L7 features caching depends on.

**Rollback:** none (read-only).

### Lab 17.50 — Functions of the policy engine (Objective 1.12)

**Objective:** Read the HTTP policies attached to a virtual service.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | select(.http_policies|length>0) | "\(.name)\t\(.http_policies|length) policies"'
```

**Expected result:** virtual services with HTTP request/response/security
policies — the policy engine rewrites, redirects, and blocks in-flight.

**Negative test:** rules evaluated in the wrong index order shadow later
rules; policy order is the control, as with any rule engine.

**Rollback:** none (read-only).

### Lab 17.51 — Certificate management (Objective 1.13)

**Objective:** Read the SSL certificates Avi manages for TLS termination.

```bash
curl -sk -H "$AH" "$AVI/api/sslkeyandcertificate" | jq -r '.results[] | "\(.name)\t\(.type)"'
```

**Expected result:** system and virtual-service certificates — Avi
terminates TLS at the VS using these, and can auto-renew.

**Negative test:** a VS referencing an expired certificate serves TLS errors
to every client; certificate lifecycle is a load-balancer responsibility.

**Rollback:** none (read-only).

### Lab 17.52 — Turn a WAF on and off (Objective 1.14)

**Objective:** Read WAF policy attachment on virtual services.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | "\(.name)\tWAF:\(.waf_policy_ref // "none")"'
```

**Expected result:** which virtual services have a WAF policy bound —
attaching/detaching `waf_policy_ref` turns WAF on/off per VS.

**Negative test:** enabling WAF in blocking mode without a learning period
blocks legitimate traffic; start in detection mode.

**Rollback:** none (read-only).

### Lab 17.53 — Capacity impact of WAF (Objective 1.15)

**Objective:** Read SE resource sizing that WAF inspection consumes.

```bash
curl -sk -H "$AH" "$AVI/api/serviceenginegroup" | jq -r '.results[] | "\(.name)\t vcpu=\(.vcpus_per_se)\tmem_mb=\(.memory_per_se)"'
```

**Expected result:** the per-SE CPU/memory — WAF's deep inspection raises SE
CPU per request, so WAF-enabled services need more SE headroom.

**Negative test:** enabling WAF on an SE group sized for L4 throughput
overloads it; capacity must be re-sized for inspection.

**Rollback:** none (read-only).

### Lab 17.54 — Service Engine capacity limits (Objective 5.1)

**Objective:** Read the SE group's capacity ceilings.

```bash
curl -sk -H "$AH" "$AVI/api/serviceenginegroup" | jq -r '.results[] | "max_se=\(.max_se)\tmax_vs_per_se=\(.max_vs_per_se)\tse_dp_mem=\(.memory_per_se)"'
```

**Expected result:** the maximum SEs, virtual services per SE, and per-SE
memory — the hard limits a capacity plan must respect.

**Negative test:** provisioning virtual services beyond `max_vs_per_se`
forces scale-out or placement failures — the ceiling is real.

**Rollback:** none (read-only).

### Lab 17.55 — Impact of elastic scale-out (Objective 5.2)

**Objective:** Read a scaled-out VS's per-SE distribution.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice/<vs-uuid>/runtime" | jq -r '.vip_summary[0].service_engine | length'
```

**Expected result:** the count of SEs serving the VS after scale-out —
throughput rises with SE count, at the cost of more SE resource.

**Negative test:** scale-out with no spare SE capacity in the group cannot
add an SE; the VS stays capacity-bound.

**Rollback:** none (read-only).

### Lab 17.56 — Performance limits of analytics and logs (Objective 5.3)

**Objective:** Read the analytics profile controlling log/metric volume.

```bash
curl -sk -H "$AH" "$AVI/api/analyticsprofile" | jq -r '.results[] | "\(.name)\tsignificant_log_throttle=\(.significant_log_throttle)"'
```

**Expected result:** throttle settings that bound analytics load — full
non-significant logging at high request rates costs SE CPU and storage.

**Negative test:** enabling full logging for every request on a high-traffic
VS degrades SE performance; throttling protects the data plane.

**Rollback:** none (read-only).

### Lab 17.57 — Significant vs non-significant logging (Objective 6.1)

**Objective:** Read which log type a virtual service records.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | "\(.name)\tnon_sig=\(.analytics_policy.full_client_logs.enabled)"'
```

**Expected result:** whether non-significant (all) client logs are on;
significant logs (errors, anomalies) are always kept, non-significant are
opt-in.

**Negative test:** relying on non-significant logs for a rare error wastes
storage; significant logs already capture the anomaly.

**Rollback:** none (read-only).

### Lab 17.58 — Enable real-time analytics (Objective 6.3)

**Objective:** Read the real-time metrics window on a VS.

```bash
curl -sk -H "$AH" "$AVI/api/analyticsprofile" | jq -r '.results[0].metrics_realtime_update | "enabled=\(.enabled)\tduration=\(.duration)"'
```

**Expected result:** real-time updates enabled with a duration — sub-minute
metric granularity for live troubleshooting.

**Negative test:** with real-time analytics off, the UI shows only rolled-up
metrics; a live spike is invisible until aggregation.

**Rollback:** none (read-only).

### Lab 17.59 — Diagnose a real-time analytics problem (Objective 6.4)

**Objective:** Read VS health/analytics to localize a fault.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice/<vs-uuid>/runtime" | jq -r '.health_score.health_score'
curl -sk -H "$AH" "$AVI/api/analytics/metrics/virtualservice/<vs-uuid>?metric_id=l4_server.avg_rtt" | jq -r '.series[0].data[-1].value'
```

**Expected result:** a health score plus a specific metric (server RTT); a
low score with high back-end RTT points at the pool, not the client.

**Negative test:** blaming the client for slowness while server RTT is high
misdirects the fix — the metric names the layer.

**Rollback:** none (read-only).

### Lab 17.60 — Interpret a health score (Objective 6.5)

**Objective:** Read the components that make up a VS health score.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice/<vs-uuid>/runtime" | jq -r '.health_score | "score=\(.health_score)\treason=\(.reason)"'
```

**Expected result:** the score and its dominant reason (performance,
resources, anomalies, security) — the score aggregates these into one
number.

**Negative test:** a high score with an active security penalty still hides
an attack in progress; read the reason, not just the number.

**Rollback:** none (read-only).

### Lab 17.61 — Log changes when WAF is enabled (Objective 6.6)

**Objective:** Read WAF-enriched log fields on a VS.

```bash
curl -sk -H "$AH" "$AVI/api/analytics/logs/virtualservice/<vs-uuid>?type=1&waf_log.rule_matches=*" | jq -r '.results[0].waf_log.status'
```

**Expected result:** WAF log entries carrying matched rules and a status
(FLAGGED/REJECTED) — logs gain WAF context once WAF is on.

**Negative test:** looking for WAF fields with WAF disabled finds none; the
enrichment appears only when WAF inspects.

**Rollback:** none (read-only).

**VCP-PCS (6V0-21.25) — Labs 17.62–17.72 (NSX vDefend / Private Cloud Security)**

### Lab 17.62 — Private cloud data-center security (Topic 01)

**Objective:** Read the security features enabled on the NSX fabric.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/settings/firewall/security" | jq -r '.'
```

**Expected result:** global firewall/security settings — the private-cloud
security baseline NSX enforces east-west and at the edge.

**Negative test:** perimeter-only security leaves east-west traffic
unguarded; private-cloud security is defined by internal segmentation too.

**Rollback:** none (read-only).

### Lab 17.63 — vDefend firewall architecture (Topic 02)

**Objective:** Confirm the distributed firewall runs in the hypervisor data
path.

```bash
curl -sk -H "$H" "$NSX/api/v1/firewall/status" | jq -r '.'
```

**Expected result:** DFW enabled with per-host enforcement — rules apply at
each vNIC in the hypervisor, not at a chokepoint appliance.

**Negative test:** a chokepoint-firewall mindset (hairpin all east-west to an
appliance) does not scale; the distributed model enforces inline.

**Rollback:** none (read-only).

### Lab 17.64 — vDefend firewall management (Topic 03)

**Objective:** Read the distributed-firewall policy layout.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/domains/default/security-policies" \
  | jq -r '.results[] | "\(.display_name)\tcat=\(.category)"'
```

**Expected result:** security policies ordered by category (Ethernet,
Emergency, Infrastructure, Environment, Application) — the managed rule
hierarchy.

**Negative test:** an Application-category allow placed above an
Infrastructure-category deny is not reordered across categories — category
order is fixed and part of the model.

**Rollback:** none (read-only).

### Lab 17.65 — Plan application segmentation (Topic 06)

**Objective:** Read the groups that define a micro-segment.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/domains/default/groups" \
  | jq -r '.results[] | "\(.display_name)\t\(.expression[0].resource_type // "static")"'
```

**Expected result:** groups defined by tags/criteria (dynamic) or members
(static) — the membership that scopes segmentation rules.

**Negative test:** static IP-based groups drift as workloads move; tag-based
dynamic groups keep segmentation correct through vMotion.

**Rollback:** none (read-only).

### Lab 17.66 — Gateway Firewall (Topic 09)

**Objective:** Read north-south gateway firewall rules on a Tier-0/Tier-1.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/domains/default/gateway-policies" \
  | jq -r '.results[] | "\(.display_name)\t\(.category)"'
```

**Expected result:** gateway policies enforcing perimeter (north-south)
control — distinct from the distributed east-west firewall.

**Negative test:** relying on the gateway firewall for east-west traffic
misses intra-segment flows it never sees; DFW handles those.

**Rollback:** none (read-only).

### Lab 17.67 — Security automation (Topic 10)

**Objective:** Drive a security policy through the declarative API (as code).

```bash
curl -sk -X PATCH -H "$H" -H 'Content-Type: application/json' \
  "$NSX/policy/api/v1/infra" \
  -d '{"resource_type":"Infra","children":[{"resource_type":"ChildResourceReference","id":"default","target_type":"Domain","children":[{"resource_type":"ChildSecurityPolicy","SecurityPolicy":{"resource_type":"SecurityPolicy","id":"auto-web","category":"Application","rules":[{"resource_type":"Rule","id":"a1","action":"ALLOW","source_groups":["ANY"],"destination_groups":["ANY"],"services":["ANY"]}]}}]}]}'
```

**Expected result:** a hierarchical (single-call) policy apply — security as
code, versionable and repeatable via CI.

**Negative test:** click-driven rule creation is not reproducible across
environments; the declarative API is what makes security automatable.

**Rollback:** delete the `auto-web` policy.

### Lab 17.68 — Security operations (Topic 11)

**Objective:** Read open security alarms across the fabric.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/alarms?status=OPEN&feature_name=distributed_firewall" \
  | jq -r '.results[] | "\(.event_type)\t\(.severity)"'
```

**Expected result:** open DFW-related alarms — the operational signal for
capacity, rule-realization, or IDS/IPS events.

**Negative test:** clearing an alarm without addressing its cause (e.g. DFW
rule limit) lets it re-fire; operations reads the cause, not just the alarm.

**Rollback:** none (read-only).

### Lab 17.69 — Role-based access control (Topic 12)

**Objective:** Read NSX security-role bindings.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/aaa/role-bindings" \
  | jq -r '.results[] | "\(.name)\t\(.roles_for_paths[0].roles[0].role)"'
```

**Expected result:** principals bound to security roles (e.g.
`security_engineer`, `auditor`) — least-privilege for security operations.

**Negative test:** a `security_engineer` editing enforcement-point/system
settings is denied; the role scopes to security objects only.

**Rollback:** none (read-only).

### Lab 17.70 — Troubleshooting (Topic 13)

**Objective:** Read a DFW rule's realized state and hit count to diagnose a
block.

```bash
curl -sk -H "$H" "$NSX/api/v1/firewall/sections/<id>/rules/<rule-id>/stats" \
  | jq -r '"hits=\(.hit_count)\tbytes=\(.byte_count)"'
```

**Expected result:** hit and byte counts; a rule that should match but shows
zero hits is shadowed by an earlier rule — the ordering fault.

**Negative test:** assuming a "deny" rule is the culprit when its hit count
is zero misdirects the fix; the shadowing rule above it is the cause.

**Rollback:** none (read-only).

### Lab 17.71 — Advanced Threat Prevention (Topic 14)

**Objective:** Read the Distributed IDS/IPS profile and its mode.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/settings/firewall/security/intrusion-services" \
  | jq -r '.ids_enabled'
curl -sk -H "$H" "$NSX/policy/api/v1/infra/domains/default/intrusion-service-policies" \
  | jq -r '.results[] | "\(.display_name)"'
```

**Expected result:** IDS/IPS enabled with intrusion-service policies —
signature-based threat detection inline in the data path.

**Negative test:** IDS in detect-only mode logs but does not block; expecting
prevention requires the policy action set to reject/drop.

**Rollback:** none (read-only).

### Lab 17.72 — Malware Prevention and Detection (Topic 16)

**Objective:** Read the malware-prevention feature state and detected files.

```bash
curl -sk -H "$H" "$NSX/policy/api/v1/infra/settings/firewall/security/malware-prevention" \
  | jq -r '.'
```

**Expected result:** malware-prevention configuration (file extraction,
verdict source) — NSX extracts and scores files traversing the fabric.

**Negative test:** malware prevention without a reachable cloud/analyst
verdict source can only do local heuristics; the verdict pipeline must be
connected.

**Rollback:** none (read-only).

**VCP-CO (2V0-32.24) — Labs 17.73–17.127 (Aria Operations / Aria Operations for Logs / Aria Suite Lifecycle)**

These labs cover **every objective** in the VMware Cloud Operations 8.x
Professional blueprint (seven standardized sections; Section 5 has no
testable objectives, so it has no labs). Each drives a product REST API
against a lab deployment so the check is reproducible; the design and
sizing objectives are evidence-gathering drills that read the real signal a
judgment rests on. The exam's products are **Aria Operations** (vRealize
Operations v8.6), **Aria Operations for Logs** (vRealize Log Insight v8.8),
and **Aria Suite Lifecycle** (vRealize Suite Lifecycle Manager v8.8).

**Shared prerequisites for Labs 17.73–17.127**

- A lab Aria stack: an Aria Operations node at `$VROPS`, an Aria Operations
  for Logs node at `$LI`, and an Aria Suite Lifecycle appliance at
  `$VRSLCM`. Acquire API credentials and export them as headers: `VH` for
  Aria Operations (`Authorization: vRealizeOpsToken <token>` from
  `POST /suite-api/api/auth/token/acquire`), `LH` for Log Insight
  (`Authorization: Bearer <sessionId>` from `POST /api/v2/sessions`), and
  `LCH` for Suite Lifecycle (`Authorization: Bearer <token>`).
- `curl` and `jq`. All read drills are non-destructive; the few that change
  state name their rollback.
- **Cost:** none beyond the lab appliances.

### Lab 17.73 — SaaS versus on-premises cloud management (Objective 1.1)

**Objective:** Confirm you are on an on-premises deployment by reading the appliance build the SaaS offering does not expose.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/versions/current" | jq -r '"\(.releaseName)\tbuild \(.buildNumber)"'
```

**Expected result:** a release name and build number — an on-premises node you install and patch yourself; the SaaS offering (Aria Operations Cloud) has no such appliance endpoint and is vendor-operated.

**Negative test:** expecting to `ssh` into or patch a SaaS tenant fails — lifecycle there is Broadcom's, not yours.

**Rollback:** none (read-only).

### Lab 17.74 — Aria Suite Lifecycle capabilities (Objective 1.2)

**Objective:** Read the Suite Lifecycle version — the product that installs, patches, and manages content for the rest of the suite.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcmversion" | jq -r '"\(.productName)\t\(.productVersion)"'
```

**Expected result:** the vRSLCM product name and version — a single control plane for deploy, upgrade, certificate, and content operations across the Aria products.

**Negative test:** deploying each Aria product by hand loses the binary mapping, content pipelines, and one-click patching Lifecycle provides.

**Rollback:** none (read-only).

### Lab 17.75 — Aria Operations capabilities (Objective 1.3)

**Objective:** Read the installed solutions (adapters) that give Aria Operations its monitoring reach.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/solutions" | jq -r '.solution[] | "\(.name)\t\(.adapterKindKeys|length) adapter(s)"'
```

**Expected result:** solutions such as `VMware vSphere` with one or more adapter kinds — Aria Operations is a metric/analytics engine whose reach is defined by the solutions installed.

**Negative test:** no vSphere solution installed means no vCenter metrics; capability follows the solution set, not the appliance alone.

**Rollback:** none (read-only).

### Lab 17.76 — Aria Operations for Logs capabilities (Objective 1.4)

**Objective:** Read the Log Insight version and confirm it is a syslog/ingest-and-query engine.

```bash
curl -sk -H "$LH" "$LI/api/v2/version" | jq -r '.version'
```

**Expected result:** a Log Insight version string — a log aggregation, indexing, and interactive-analytics product distinct from the metric analytics of Aria Operations.

**Negative test:** querying metrics (CPU%, capacity) in Log Insight returns nothing useful; logs and metrics are different stores with different tools.

**Rollback:** none (read-only).

### Lab 17.77 — Cloud Management components and integrations (Objective 2.1)

**Objective:** Read the adapter kinds bound into Aria Operations — the integration points of the solution.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/adapterkinds" | jq -r '.["adapter-kind"][] | .key' | head
```

**Expected result:** adapter kinds (`VMWARE`, `LogInsightAdapter`, storage/network packs) — the components a Cloud Management solution stitches together around the vSphere source of truth.

**Negative test:** treating Aria Operations as standalone ignores the vROps↔Log Insight↔Lifecycle integrations the exam expects you to name.

**Rollback:** none (read-only).

### Lab 17.78 — True Visibility Suite management packs (Objective 2.2)

**Objective:** Read the third-party management packs (True Visibility Suite) that extend monitoring beyond VMware.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/solutions" | jq -r '.solution[] | select(.name|test("VMware")|not) | .name'
```

**Expected result:** non-VMware solutions (storage arrays, databases, applications) — the True Visibility Suite role is monitoring heterogeneous, non-VMware infrastructure through Aria Operations.

**Negative test:** expecting native NetApp/SQL metrics without the matching TVS management pack installed returns nothing.

**Rollback:** none (read-only).

### Lab 17.79 — Skyline, Federated Analytics, and AI use cases (Objective 2.3)

**Objective:** Read whether the node is registered to Broadcom's cloud services that power Skyline / Federated Analytics / AI recommendations.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/deployment/config/globalsettings" | jq -r '.keyValues[] | select(.key|test("cloud|ceip|telemetry";"i")) | "\(.key)=\(.values[0])"'
```

**Expected result:** CEIP/cloud-connection settings — Skyline (proactive support findings), Federated Analytics, and vRealize AI Cloud all depend on cloud connectivity and telemetry being enabled.

**Negative test:** with CEIP/cloud off, AI-driven recommendations and Skyline findings never populate; the use case requires the connection.

**Rollback:** none (read-only).

### Lab 17.80 — Suite Lifecycle use case (Objective 2.4)

**Objective:** Read the environments Suite Lifecycle manages — its use case as the suite's deploy/patch control plane.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/lcops/api/v2/environments" | jq -r '.[] | "\(.environmentName)\t\(.products|length) product(s)"'
```

**Expected result:** one or more environments each holding managed products — the use case is centralized lifecycle (install, upgrade, cert rotation) rather than per-product manual ops.

**Negative test:** installing a product outside Lifecycle leaves it unmanaged — later patches and cert rotations must be done by hand.

**Rollback:** none (read-only).

### Lab 17.81 — Remote Collectors, Cloud Proxies, Collector Groups (Objective 2.5)

**Objective:** Read the collectors and collector groups that gather data for Aria Operations.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/collectors" | jq -r '.collector[] | "\(.name)\t\(.state)"'
curl -sk -H "$VH" "$VROPS/suite-api/api/collectorgroups" | jq -r '.collectorGroups[]?.name'
```

**Expected result:** collectors (`RUNNING`) and any collector groups — remote collectors/cloud proxies gather data at a remote site and forward it; collector groups give them HA and load sharing.

**Negative test:** pointing every remote site's adapters at the analytics cluster directly floods the WAN; the collector's job is to localize collection.

**Rollback:** none (read-only).

### Lab 17.82 — Log Insight and Log Insight Cloud (Objective 2.6)

**Objective:** Read Log Insight's forwarding configuration — the bridge to Log Insight Cloud or another cluster.

```bash
curl -sk -H "$LH" "$LI/api/v2/forwarding" | jq -r '.forwarders[]? | "\(.name)\t\(.protocol)\t\(.host)"'
```

**Expected result:** any configured forwarders (to Log Insight Cloud or a peer) — on-prem Log Insight ingests locally and can forward to Log Insight Cloud for SaaS retention/analytics.

**Negative test:** expecting Log Insight Cloud to see on-prem events with no forwarder configured — nothing arrives.

**Rollback:** none (read-only).

### Lab 17.83 — Aria Operations architecture modes (Objective 3.1)

**Objective:** Read the Aria Operations node roles to identify the deployment mode (standalone, clustered, HA, or Continuous Availability).

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/deployment/node" | jq -r '.nodes[] | "\(.name)\t\(.role)\t\(.state)"'
```

**Expected result:** a single node (standalone) or a master + data/replica nodes (clustered/HA); a CA deployment shows a fault-domain split. The mode determines resilience and scale ceiling.

**Negative test:** enabling HA on a two-node cluster without a witness/replica leaves no quorum — the design must place roles deliberately.

**Rollback:** none (read-only).

### Lab 17.84 — Log Insight architecture modes (Objective 3.2)

**Objective:** Read the Log Insight cluster nodes to distinguish standalone from clustered.

```bash
curl -sk -H "$LH" "$LI/api/v2/cluster/nodes" | jq -r '.nodes[] | "\(.id)\t\(.role)\t\(.status)"'
```

**Expected result:** one node (standalone) or a master plus workers behind an Integrated Load Balancer — a cluster scales ingest and adds resilience a standalone cannot.

**Negative test:** pointing syslog sources at a worker's own address instead of the ILB VIP breaks failover; clustered design requires the VIP.

**Rollback:** none (read-only).

### Lab 17.85 — Size a Log Insight deployment (Objective 3.3)

**Objective:** Read the current ingestion rate to size a Log Insight deployment for a scenario.

```bash
curl -sk -H "$LH" "$LI/api/v2/events/count?timestamp>$(( ($(date +%s) - 86400) * 1000 ))" | jq -r '.count'
```

**Expected result:** the last 24 hours' event count — divide by day for events/second; Log Insight sizing (nodes, disk) follows ingest rate and required retention, not host count.

**Negative test:** sizing on raw VM count ignores chatty sources; a few high-rate syslog senders can dominate ingest and change the node count.

**Rollback:** none (read-only).

### Lab 17.86 — Size an Aria Operations deployment (Objective 3.4)

**Objective:** Read the monitored-object count to size an Aria Operations deployment.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/resources?pageSize=1" | jq -r '.pageInfo.totalCount'
```

**Expected result:** the total resource (object) count — Aria Operations sizing (node count and profile: small/medium/large) is driven by object and metric counts, which map to the published sizing guidelines.

**Negative test:** sizing to today's count with no headroom means a re-scale as soon as the estate grows; sizing plans for growth and collection interval.

**Rollback:** none (read-only).

### Lab 17.87 — Design collector-group placement (Objective 3.5)

**Objective:** Read collector-group membership to reason about remote-site data collection placement.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/collectorgroups" | jq -r '.collectorGroups[] | "\(.name)\tmembers=\(.collectorId|length)"'
```

**Expected result:** groups with more than one collector — the design places a collector group per site/fault domain so remote collection survives a single collector loss and stays local to the source.

**Negative test:** one collector per site with no group gives no failover; if it drops, that site goes dark until it returns.

**Rollback:** none (read-only).

### Lab 17.88 — Installation prerequisites: DNS and NTP (Objective 4.1)

**Objective:** Verify forward/reverse DNS and time sync — the prerequisites an Aria install fails without.

```bash
host "$VROPS" && host "$(dig +short "$VROPS" | tail -1)"
curl -sk -H "$VH" "$VROPS/suite-api/api/deployment/config/ntp" | jq -r '.timeServers[]?'
```

**Expected result:** matching forward and reverse records and at least one NTP server — Aria nodes require resolvable FQDNs, reverse PTRs, synced time, and dedicated service accounts before deployment.

**Negative test:** a missing PTR or drifting clock breaks certificate trust and cluster membership; the installer will not complete.

**Rollback:** none (read-only).

### Lab 17.89 — Deploy Aria Suite Lifecycle (Objective 4.2)

**Objective:** Confirm Suite Lifecycle is deployed and reachable — the first appliance in a Lifecycle-driven build.

```bash
curl -sk -o /dev/null -w '%{http_code}\n' -H "$LCH" "$VRSLCM/lcm/lcops/api/v2/environments"
```

**Expected result:** `200` — vRSLCM is deployed (from its OVA, sized per the guide, with DNS/NTP set) and its API answers; it is the platform every subsequent product install runs through.

**Negative test:** a `401`/`000` means the token or appliance is wrong — no Lifecycle-driven install can proceed until vRSLCM itself is up.

**Rollback:** none (read-only).

### Lab 17.90 — Manual Aria Operations install shape (Objective 4.3)

**Objective:** Read node roles to recognize a manual (OVA) standalone-or-cluster install.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/deployment/node" | jq -r '.nodes[] | "\(.role)"' | sort | uniq -c
```

**Expected result:** one `MASTER` (standalone) or a `MASTER` plus `DATA`/`REPLICA` roles (cluster) — a manual install deploys each OVA, runs initial setup on the master, then joins data nodes.

**Negative test:** joining a data node before the master finishes initial setup fails; order matters in a manual cluster build.

**Rollback:** none (read-only).

### Lab 17.91 — Install Aria Operations via Suite Lifecycle (Objective 4.4)

**Objective:** Read the environment holding Aria Operations to confirm a Lifecycle-driven install.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/lcops/api/v2/environments" | jq -r '.[] | .products[] | select(.id=="vrops") | "\(.id)\t\(.version)\t\(.nodes|length) node(s)"'
```

**Expected result:** the `vrops` product with a version and node count — Lifecycle deploys the cluster from a mapped binary and records it as a managed product (standalone or multi-node).

**Negative test:** a Lifecycle install with no binary mapped for the target version fails at the deploy step; the binary must be in the mapping first.

**Rollback:** none (read-only).

### Lab 17.92 — Manual Log Insight install shape (Objective 4.5)

**Objective:** Read Log Insight cluster roles to recognize a manual standalone/cluster install.

```bash
curl -sk -H "$LH" "$LI/api/v2/cluster/nodes" | jq -r '.nodes[] | .role' | sort | uniq -c
```

**Expected result:** a `MASTER` alone (standalone) or a `MASTER` plus `WORKER` nodes (cluster) — a manual install deploys each OVA and joins workers to the master, then fronts them with the Integrated Load Balancer.

**Negative test:** adding a worker without configuring the ILB VIP means sources still hit one node; the manual cluster is not complete until the VIP is set.

**Rollback:** none (read-only).

### Lab 17.93 — Install Log Insight via Suite Lifecycle (Objective 4.6)

**Objective:** Read the environment holding Log Insight to confirm a Lifecycle-driven install.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/lcops/api/v2/environments" | jq -r '.[] | .products[] | select(.id=="vrli") | "\(.id)\t\(.version)\t\(.nodes|length) node(s)"'
```

**Expected result:** the `vrli` product with version and node count — Lifecycle deploys the Log Insight cluster from its mapped binary and manages it thereafter.

**Negative test:** expecting Lifecycle to manage a Log Insight it did not deploy — an out-of-band install must be imported before Lifecycle can patch it.

**Rollback:** none (read-only).

### Lab 17.94 — Configure RBAC across the suite (Objective 4.7)

**Objective:** Read the role definitions in Aria Operations and Log Insight to confirm least-privilege RBAC.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/auth/roles" | jq -r '.userRoles[] | .name'
curl -sk -H "$LH" "$LI/api/v2/roles" | jq -r '.roles[]?.name'
```

**Expected result:** roles such as `Administrator`, `ReadOnly`, plus custom scoped roles — RBAC in Aria Operations, Log Insight, and Suite Lifecycle is configured per product and ideally backed by the same identity source.

**Negative test:** granting everyone `Administrator` defeats separation of duties; the exam expects scoped roles mapped to job function.

**Rollback:** none (read-only).

### Lab 17.95 — Configure Suite Lifecycle settings (Objective 4.8)

**Objective:** Read core Suite Lifecycle settings (DNS, NTP, binary mapping) that must be configured before product operations.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/lcops/api/v2/settings/dns" | jq -r '.dnsServers[]?'
curl -sk -H "$LCH" "$VRSLCM/lcm/lcops/api/v2/settings/ntp" | jq -r '.ntpServers[]?'
```

**Expected result:** configured DNS and NTP servers — Suite Lifecycle settings (storage extension, binary/product mapping, DNS, NTP, passwords, license store, identity, and environments) underpin every deploy and patch.

**Negative test:** an empty binary mapping blocks installs and upgrades; settings are the platform every product action depends on.

**Rollback:** none (read-only).

### Lab 17.96 — Configure data sources (Objective 4.9)

**Objective:** Read the adapter instances (data sources) feeding Aria Operations.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/adapters" | jq -r '.adapterInstancesInfoDto[] | "\(.resourceKey.name)\t\(.adapterKindKey)"'
```

**Expected result:** adapter instances such as a vCenter adapter — configuring data sources (vCenter for Aria Operations, vSphere integration for Log Insight) is what makes the products observe the environment.

**Negative test:** a collecting adapter in a `DATA_RECEIVING=false` state produces empty dashboards; the data source must be connected and collecting.

**Rollback:** none (read-only).

### Lab 17.97 — Install management and content packs (Objective 4.10)

**Objective:** Read installed content packs in Log Insight and management packs in Aria Operations.

```bash
curl -sk -H "$LH" "$LI/api/v2/content/contentpack/list" | jq -r '.contentPackMetadataList[]? | .name'
curl -sk -H "$VH" "$VROPS/suite-api/api/solutions" | jq -r '.solution[].name'
```

**Expected result:** content packs (vSphere, NSX, etc.) in Log Insight and solutions/management packs in Aria Operations — packs add dashboards, alerts, and parsing for a specific product.

**Negative test:** parsing NSX logs without the NSX content pack yields unstructured events; the pack supplies the fields and queries.

**Rollback:** none (read-only).

### Lab 17.98 — Content management in Suite Lifecycle (Objective 4.11)

**Objective:** Read the content Suite Lifecycle manages — dashboards, templates, and policies under version control.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/lcops/api/v2/content" | jq -r '.[]? | "\(.contentName)\t\(.contentType)"' | head
```

**Expected result:** managed content items with types — Content Management in Suite Lifecycle captures, versions, and promotes content (dashboards, alerts, blueprints) across environments like source control.

**Negative test:** editing a dashboard directly in production, outside Content Management, loses the version history and the promote-to-prod pipeline.

**Rollback:** none (read-only).

### Lab 17.99 — Integrate Aria Operations and Log Insight (Objective 4.12)

**Objective:** Confirm the Log Insight ↔ Aria Operations integration that enables launch-in-context and metric-from-log alerts.

```bash
curl -sk -H "$LH" "$LI/api/v2/vrops" | jq -r '"\(.host)\tenabled=\(.enabled)"'
```

**Expected result:** the Aria Operations host with `enabled=true` — the integration sends Log Insight alerts to Aria Operations and enables launch-in-context between logs and objects.

**Negative test:** without the integration, an operator jumps between two consoles by hand instead of pivoting from an object's metric spike to its logs.

**Rollback:** none (read-only).

### Lab 17.100 — Generate support/log bundles (Objective 6.1)

**Objective:** Read where each product exposes support-bundle generation for troubleshooting.

```bash
curl -sk -o /dev/null -w 'vrops-support-bundle-endpoint: %{http_code}\n' -H "$VH" "$VROPS/suite-api/api/deployment/logs"
```

**Expected result:** a `200`/`202` from the Aria Operations log/support endpoint — each product (Aria Operations, Log Insight, Suite Lifecycle) generates a support bundle from its admin UI or API for Broadcom support.

**Negative test:** collecting only the master node's bundle in a cluster omits the failing data node's logs; a cluster bundle must span nodes.

**Rollback:** delete any generated bundle after download.

### Lab 17.101 — Manage the Aria Operations cluster (Objective 6.2)

**Objective:** Read cluster node online/offline state via the CaSA admin API.

```bash
curl -sk -H "$VH" "$VROPS/casa/deployment/cluster/info" | jq -r '.nodes[] | "\(.node_name)\t\(.node_state)"'
```

**Expected result:** each node with a state (`RUNNING`/`OFFLINE`) — cluster management (take a node offline for maintenance, bring it online, rebalance) is done through the Cluster Administration (CaSA) interface.

**Negative test:** powering off a data node instead of taking it offline gracefully risks sharded-data resync storms on return.

**Rollback:** bring any node taken offline back online.

### Lab 17.102 — Manage admin and root passwords (Objective 6.3)

**Objective:** Read the admin-account state and confirm the password-management path for admin/root.

```bash
curl -sk -H "$VH" "$VROPS/casa/os/slice/user" | jq -r '.users[]? | "\(.username)\t\(.locked)"'
```

**Expected result:** the `admin`/`root` accounts and their lock state — the product `admin` password is changed in CaSA, and appliance `root` via the console/SSH `passwd`; both must be rotated and unlocked to operate.

**Negative test:** a locked `root` with an expired `admin` password can strand you out of a node that otherwise runs; manage both proactively.

**Rollback:** none (read-only — do not change live credentials in this drill).

### Lab 17.103 — Change the Suite Lifecycle auth provider (Objective 6.4)

**Objective:** Read the configured identity provider in Suite Lifecycle before changing it.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/authzn/api/idp" | jq -r '.[]? | "\(.name)\t\(.type)"'
```

**Expected result:** the current IdP (local, or an external vIDM/Workspace ONE Access) — changing the auth provider re-points Suite Lifecycle login at a new identity source.

**Negative test:** switching the IdP without pre-creating admin mappings in the new source locks every administrator out; map roles first.

**Rollback:** none (read-only).

### Lab 17.104 — Troubleshoot Log Insight cluster health (Objective 6.5)

**Objective:** Read per-node status and load to diagnose common Log Insight cluster issues.

```bash
curl -sk -H "$LH" "$LI/api/v2/cluster/nodes" | jq -r '.nodes[] | "\(.role)\t\(.status)\tload=\(.currentLoad // "n/a")"'
```

**Expected result:** each node `CONNECTED` with balanced load — a `DISCONNECTED` worker or a skewed load points at the ILB, a network partition, or an over-subscribed node.

**Negative test:** blaming ingest slowness on the master when a worker is `DISCONNECTED` misreads the cause; read node status before tuning.

**Rollback:** none (read-only).

### Lab 17.105 — Troubleshoot Aria Operations cluster health (Objective 6.6)

**Objective:** Read node status and adapter data-receiving state to diagnose Aria Operations cluster problems.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/deployment/node/status" | jq -r '"cluster=\(.overallState)"'
curl -sk -H "$VH" "$VROPS/suite-api/api/adapters" | jq -r '.adapterInstancesInfoDto[] | "\(.resourceKey.name)\t\(.dataReceiving)"'
```

**Expected result:** an overall cluster state plus each adapter's data-receiving flag — a degraded cluster or an adapter not receiving is the usual root of "missing metrics."

**Negative test:** restarting the whole cluster for one stuck adapter is heavy-handed; the adapter state localizes the fault first.

**Rollback:** none (read-only).

### Lab 17.106 — Troubleshoot Suite Lifecycle health (Objective 6.7)

**Objective:** Read recent Suite Lifecycle requests to find failed operations and their errors.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/request/api/v2/requests?status=FAILED" | jq -r '.[]? | "\(.requestName)\t\(.state)"' | head
```

**Expected result:** any failed requests (deploy, upgrade, cert) with state — Suite Lifecycle troubleshooting starts from the request log, where each step records its error.

**Negative test:** re-running a failed upgrade without reading the request error repeats the same failure; the log names the precondition that was unmet.

**Rollback:** none (read-only).

### Lab 17.107 — Suite Lifecycle administrative day-2 tasks (Objective 7.1)

**Objective:** Read the appliance-level (system) settings Suite Lifecycle exposes for day-2 administration.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/lcops/api/v2/settings/product-support-pack" | jq -r '.[]? | "\(.name)\t\(.version)"' | head
```

**Expected result:** support/product packs available to apply — administrative day-2 tasks (support-pack updates, system patching, certificate replacement) are driven from Suite Lifecycle's settings, not each product.

**Negative test:** patching products while skipping the Suite Lifecycle support pack can leave the manager behind its managed products' supported matrix.

**Rollback:** none (read-only).

### Lab 17.108 — Suite Lifecycle operational environment tasks (Objective 7.2)

**Objective:** Read the day-2 environment actions Suite Lifecycle offers for a managed product.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/lcops/api/v2/environments" | jq -r '.[] | "\(.environmentName): \(.products[].id)"'
```

**Expected result:** environments and their products, each of which exposes day-2 actions (add node, upgrade, trigger inventory sync, replace certificate) — operational environment tasks act on the deployed products as a unit.

**Negative test:** scaling a product by deploying a node outside Lifecycle puts its inventory out of sync; day-2 scale should go through the environment.

**Rollback:** none (read-only).

### Lab 17.109 — Suite Lifecycle content day-2 tasks (Objective 7.3)

**Objective:** Read the content pipelines Suite Lifecycle uses for capture/test/release day-2 content tasks.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/lcops/api/v2/content/pipelines" | jq -r '.[]? | "\(.pipelineName)\t\(.status)"' | head
```

**Expected result:** content pipelines with status — operational content tasks (capture from source, test, release to target) move dashboards/policies through environments under version control.

**Negative test:** hand-copying content between environments skips the pipeline's test gate and version record.

**Rollback:** none (read-only).

### Lab 17.110 — Manage authentication and user access control (Objective 7.4)

**Objective:** Read the Suite Lifecycle users and their role bindings.

```bash
curl -sk -H "$LCH" "$VRSLCM/lcm/authzn/api/users" | jq -r '.[]? | "\(.username)\t\(.role)"'
```

**Expected result:** users mapped to roles (`ADMIN`, `CONTENT_RELEASE_MANAGER`, `VIEWER`) — access control is managed centrally and should map to the same identity source as the products.

**Negative test:** local-only accounts drift from the corporate directory; joining an external IdP keeps access lifecycle in one place.

**Rollback:** none (read-only).

### Lab 17.111 — Manage Aria Operations licensing and groups (Objective 7.5)

**Objective:** Read the installed licenses and license groups in Aria Operations.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/deployment/licenses" | jq -r '.solutionLicenses[] | "\(.licenseKey[0:7])…\t\(.edition // "n/a")"'
```

**Expected result:** one or more license keys with editions — licensing groups assign specific objects to a license so mixed-edition estates are metered correctly.

**Negative test:** letting objects auto-consume the wrong-edition license under-provisions features; license groups bind objects to the intended entitlement.

**Rollback:** none (read-only).

### Lab 17.112 — Configure Aria Operations event/log forwarding (Objective 7.6)

**Objective:** Read the Aria Operations outbound (log/event) forwarding settings.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/deployment/config/loginsight" | jq -r '"host=\(.host)\tenabled=\(.enabled)"'
```

**Expected result:** the Log Insight/syslog target and enabled flag — Aria Operations forwards its own audit and alert events so they land in the log store alongside everything else.

**Negative test:** relying on the UI alone for Aria Operations' own events loses them on appliance replacement; forwarding preserves them externally.

**Rollback:** none (read-only).

### Lab 17.113 — Patch Aria Operations without Suite Lifecycle (Objective 7.7)

**Objective:** Read the CaSA upgrade/PAK status used to patch Aria Operations directly (no Suite Lifecycle).

```bash
curl -sk -H "$VH" "$VROPS/casa/upgrade/cluster/status" | jq -r '"phase=\(.upgrade_phase // "IDLE")\tready=\(.is_ready_for_upgrade // "n/a")"'
```

**Expected result:** an upgrade phase and readiness flag — without Suite Lifecycle you stage a PAK and drive the upgrade from CaSA, which reports each phase.

**Negative test:** applying a PAK without taking a snapshot/backup first leaves no clean rollback if the upgrade fails mid-cluster.

**Rollback:** none (read-only — do not start a live upgrade in this drill).

### Lab 17.114 — Custom dashboards, views, reports, super metrics (Objective 7.8)

**Objective:** Read the custom content — dashboards, views, reports, and super metrics — in Aria Operations.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/dashboards" | jq -r '.uiDashboards | length as $d | "dashboards=\($d)"'
curl -sk -H "$VH" "$VROPS/suite-api/api/supermetrics" | jq -r '.superMetrics | length as $s | "supermetrics=\($s)"'
```

**Expected result:** counts of dashboards and super metrics — custom dashboards/views/reports present data for an audience, and super metrics derive new values (e.g. cluster headroom) from base metrics.

**Negative test:** a super metric referencing a metric that stops collecting silently returns no data; custom content must be validated after adapter changes.

**Rollback:** none (read-only).

### Lab 17.115 — Manage alerts, symptoms, and notifications (Objective 7.9)

**Objective:** Read alert definitions and their symptoms in Aria Operations.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/alertdefinitions?pageSize=1" | jq -r '.pageInfo.totalCount as $t | "alertDefinitions=\($t)"'
curl -sk -H "$VH" "$VROPS/suite-api/api/symptomdefinitions?pageSize=1" | jq -r '.pageInfo.totalCount as $t | "symptomDefinitions=\($t)"'
```

**Expected result:** counts of alert and symptom definitions — an alert fires when its symptoms trigger, and notification rules route it (email, SNMP, Log Insight, webhook).

**Negative test:** an alert with no notification rule fires silently in the UI; someone must be told for it to matter.

**Rollback:** none (read-only).

### Lab 17.116 — Optimize performance of a managed environment (Objective 7.10)

**Objective:** Read Aria Operations' Workload Optimization signal for a compute cluster.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/resources?resourceKind=ClusterComputeResource&pageSize=1" \
  | jq -r '.resourceList[0].identifier as $id | "clusterId=\($id)"'
```

**Expected result:** a cluster resource id whose Workload Optimization score/recommendation Aria Operations computes — performance optimization rebalances workloads across hosts/clusters to relieve contention.

**Negative test:** acting on optimization without a defined operational-intent policy (balance vs consolidate) can fight DRS; set intent first.

**Rollback:** none (read-only).

### Lab 17.117 — Optimize capacity of a managed environment (Objective 7.11)

**Objective:** Read remaining-capacity/time-remaining analytics for a cluster.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/resources?resourceKind=ClusterComputeResource&pageSize=1" \
  | jq -r '.resourceList[0].identifier' \
  | xargs -I{} curl -sk -H "$VH" "$VROPS/suite-api/api/resources/{}/stats?statKey=capacity|timeRemaining&maxSamples=1" \
  | jq -r '.values[]?.["stat-list"].stat[]? | "\(.statKey.key)=\(.data[0])"'
```

**Expected result:** a time-remaining value in days — capacity optimization reclaims idle/oversized/powered-off VMs and forecasts when a cluster runs out, driving right-sizing and reclamation.

**Negative test:** reclaiming on utilization alone without time-remaining forecasting can starve a cluster that is about to spike; capacity uses the forecast, not the instant.

**Rollback:** none (read-only).

### Lab 17.118 — Plan a workload or cloud migration (Objective 7.12)

**Objective:** Read the resource inventory that a What-If/migration plan is built from.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/resources?resourceKind=VirtualMachine&pageSize=1" | jq -r '.pageInfo.totalCount as $t | "vmCount=\($t)"'
```

**Expected result:** the VM count feeding a migration plan — Aria Operations' What-If scenarios model adding/removing workloads or moving them to another cluster or public cloud and report the capacity impact.

**Negative test:** planning a migration on host counts without the per-VM demand profile under-sizes the target; the plan needs measured demand.

**Rollback:** none (read-only).

### Lab 17.119 — Assess the cost of a managed environment (Objective 7.13)

**Objective:** Read a cost metric Aria Operations computes for the environment.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/resources?resourceKind=ClusterComputeResource&pageSize=1" \
  | jq -r '.resourceList[0].identifier' \
  | xargs -I{} curl -sk -H "$VH" "$VROPS/suite-api/api/resources/{}/stats?statKey=cost|totalCost&maxSamples=1" \
  | jq -r '.values[]?.["stat-list"].stat[]? | "\(.statKey.key)=\(.data[0])"'
```

**Expected result:** a total-cost value for the cluster — cost analytics attribute infrastructure spend to clusters, VMs, and business groups so showback/chargeback and reclamation savings can be reported.

**Negative test:** cost figures with no cost drivers configured fall back to defaults that misstate spend; the cost model must be set for your prices.

**Rollback:** none (read-only).

### Lab 17.120 — Monitor operating systems and applications (Objective 7.14)

**Objective:** Read whether Application/OS monitoring (Telegraf agents) is reporting into Aria Operations.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/resources?adapterKind=ApplicationDiscoveryAdapter&pageSize=1" \
  | jq -r '.pageInfo.totalCount as $t | "appObjects=\($t)"'
```

**Expected result:** application/OS objects discovered — Aria Operations monitors in-guest OS and application services via agents (Telegraf), extending visibility below the VM into the workload.

**Negative test:** expecting service-level (MySQL, IIS) metrics without the agent deployed returns only VM-level counters.

**Rollback:** none (read-only).

### Lab 17.121 — Manage jobs with Automation Central (Objective 7.15)

**Objective:** Read scheduled Automation Central jobs (reclamation, right-sizing) in Aria Operations.

```bash
curl -sk -H "$VH" "$VROPS/suite-api/api/schedules" | jq -r '.schedules[]? | "\(.name)\t\(.actionType // .type)"' | head
```

**Expected result:** scheduled jobs with their action type — Automation Central centralizes recurring operational jobs (power-off idle VMs, reclaim snapshots, right-size) with schedules and approvals.

**Negative test:** an unattended reclamation job with no approval step can delete a VM someone still needs; Automation Central adds the approval gate.

**Rollback:** none (read-only).

### Lab 17.122 — Manage authentication and access in Log Insight (Objective 7.16)

**Objective:** Read Log Insight's authentication providers and roles.

```bash
curl -sk -H "$LH" "$LI/api/v2/auth-providers" | jq -r '.providers[]? | "\(.type)\t\(.enabled)"'
curl -sk -H "$LH" "$LI/api/v2/roles" | jq -r '.roles[]?.name'
```

**Expected result:** the enabled providers (Local, Active Directory/vIDM) and role list — Log Insight access is managed with roles and dataset-scoped permissions, backed by the chosen identity source.

**Negative test:** granting broad roles without dataset restrictions lets a team read another tenant's logs; scope datasets to the role.

**Rollback:** none (read-only).

### Lab 17.123 — Patch Log Insight without Suite Lifecycle (Objective 7.17)

**Objective:** Read the Log Insight version and cluster readiness used when patching directly (no Suite Lifecycle).

```bash
curl -sk -H "$LH" "$LI/api/v2/version" | jq -r '.version'
curl -sk -H "$LH" "$LI/api/v2/cluster/nodes" | jq -r '[.nodes[]|select(.status=="CONNECTED")]|length as $n | "connectedNodes=\($n)"'
```

**Expected result:** current version and count of connected nodes — a direct upgrade uploads a PAK in the admin UI and applies it rolling across the cluster, which must be fully connected first.

**Negative test:** starting a rolling upgrade with a disconnected worker can strand that node on the old build; the cluster should be healthy before patching.

**Rollback:** none (read-only — do not start a live upgrade in this drill).

### Lab 17.124 — Configure and manage Log Insight agents (Objective 7.18)

**Objective:** Read the Log Insight agents and their configuration groups.

```bash
curl -sk -H "$LH" "$LI/api/v2/agents" | jq -r '.agents[]? | "\(.hostname)\t\(.status)"' | head
```

**Expected result:** agents with a status (`Active`) — Log Insight agents collect logs and events from OSes/apps and are configured centrally through agent groups (which files, what parsing, where to send).

**Negative test:** an agent with no group falls back to defaults and may not collect the intended files; agent groups drive what each agent does.

**Rollback:** none (read-only).

### Lab 17.125 — Log forwarding, masking, and filtering (Objective 7.19)

**Objective:** Read the forwarding destinations and any masking/filtering rules in Log Insight.

```bash
curl -sk -H "$LH" "$LI/api/v2/forwarding" | jq -r '.forwarders[]? | "\(.name)\tfilter=\(.filter // "none")"'
```

**Expected result:** forwarders each with an optional filter — forwarding relays events to another cluster or Log Insight Cloud, filtering limits which events go, and masking redacts sensitive fields before they leave.

**Negative test:** forwarding raw events without masking can leak secrets/PII downstream; masking must be applied before the forward.

**Rollback:** none (read-only).

### Lab 17.126 — Retention and archiving settings (Objective 7.20)

**Objective:** Read Log Insight's retention and archiving configuration.

```bash
curl -sk -H "$LH" "$LI/api/v2/retention" | jq -r '"retentionDays=\(.retentionDays // .dataArchiveRetentionDays // "n/a")"'
curl -sk -H "$LH" "$LI/api/v2/archive" | jq -r '"archiveEnabled=\(.enabled)\tpath=\(.path // "n/a")"'
```

**Expected result:** a retention window and archive path — retention bounds searchable storage; archiving writes older buckets to NFS so they can be restored for compliance without occupying live index.

**Negative test:** a long retention with no archive fills the index disk and stops ingest; retention and archiving are sized together.

**Rollback:** none (read-only).

### Lab 17.127 — System notifications for Log Insight (Objective 7.21)

**Objective:** Read Log Insight's system-notification configuration (health and capacity alerts about the appliance itself).

```bash
curl -sk -H "$LH" "$LI/api/v2/notification/system" | jq -r '"email=\(.emailEnabled)\tsnmp=\(.snmpEnabled)"'
```

**Expected result:** the enabled system-notification channels — system notifications warn on Log Insight's own health (disk, node down, ingest backpressure), distinct from user-defined content alerts on ingested data.

**Negative test:** relying only on content alarms misses the appliance running out of disk; system notifications watch the platform itself.

**Rollback:** none (read-only).

### Lab 17.128 — Five-exam readiness drill (integrative)

**Objective:** Confirm, without booking any exam, which of the five
professional-level exams in this chapter you are closest to ready for, by
running one scoped drill per exam against this volume's existing labs.

**Prerequisites**

- The lab environments from earlier chapters: a vSphere cluster (Chapters
  1–9), NSX with a vDefend DFW policy (Chapters 8, 10–11), and — if
  available — a lab Avi Controller with one virtual service and an Aria
  stack (Aria Operations, Aria Operations for Logs, Aria Suite Lifecycle).
- The domain-mapped tracker from the Implementation section above.
- No reference material open during each timed drill.

**Steps**

1. **VCP-DCV drill (target 20 minutes).** From memory, provision a VM from
   a template, apply a storage policy, and vMotion it between hosts.

   **Expected result:** all three complete unaided; note any step that
   needed [Chapters 5–7](05-virtual-machine-lifecycle-and-resource-management.md).

2. **VCP-VCF Architect drill (target 15 minutes).** Take one written
   requirement (for example, "recover a workload domain within four hours
   of a site failure") and write the conceptual, logical, and physical
   design decisions it forces, naming one constraint and one assumption.

   **Expected result:** a coherent three-level design chain on paper,
   defensible aloud.

3. **VCP-AVI drill (target 15 minutes).** If an Avi lab exists, inspect one
   virtual service and its pool, then explain its load-balancing algorithm
   and health monitor choice without opening documentation. If no Avi lab
   exists, record this as a lab gap to close before scheduling.

   **Expected result:** an unaided explanation, or an identified gap.

4. **VCP-PCS drill (target 15 minutes).** Verify a default-deny plus
   scoped-allow micro-segmentation policy is enforcing (reuse
   [Chapter 8](08-vsphere-and-nsx-security-architecture.md)'s lab), then
   explain how you would prove a specific flow is blocked by policy rather
   than by routing.

   **Expected result:** the policy enforces, and you can name the tool
   (Traceflow, DFW hit counters) that distinguishes the two causes.

5. **VCP-CO drill (target 15 minutes).** If an Aria lab exists, read an Aria
   Operations cluster's node roles and one cluster's capacity time-remaining,
   and pull the Aria Operations for Logs cluster node list, then explain the
   deployment mode and one sizing driver without opening documentation. If no
   Aria lab exists, record this as a lab gap to close before scheduling.

   **Expected result:** an unaided explanation, or an identified gap.

6. **Score and target.** Rank the five drills by how far over time or how
   reference-dependent each was. The weakest is the exam furthest from
   ready; direct additional lab time there rather than re-reading a domain
   already strong.

7. **Rollback:** revert the VM, remove any test design notes, and return the
   DFW policy and Avi objects to their baseline state so the labs are ready
   for future runs.

## Design Exercise

VCP-VCF Architect (2V0-13.25) is a **design** exam: the command-driven
walkthroughs above (Labs 17.33–17.40) exercise the evidence each decision
rests on; this exercise is the reasoning half — no lab required, only a
requirements set and a defensible argument.

**Scenario.** A business wants to consolidate three aging vSphere clusters
onto a new VCF 9.0 platform. Stated objectives: no more than one host of
capacity lost to failover, a hardware refresh budget of ten hosts, existing
workloads migrated with under four hours of total downtime, and a
demonstrable audit trail for every design decision.

**Produce, defending each choice against a rejected alternative:**

1. **Requirements register** — classify every objective as a requirement,
   constraint, assumption, or risk, each with a measurable acceptance test
   (Objective 1.3).
2. **Conceptual → logical → physical chain** — one traceable line from a
   business objective down to a host-level specification, keeping the layers
   distinct (Objectives 1.2, 3.2).
3. **Risk-mitigation strategy** — the top three risks (e.g. the ten-host cap
   versus the one-host-failover requirement) with a mitigation and owner for
   each (Objective 1.5).
4. **Decision log** — at least five decisions recorded as {decision,
   justification, rejected alternative, impact} (Objective 1.6).
5. **Validation strategy** — the concrete test that will prove each major
   requirement is met after build (Objective 1.7).

**Success looks like:** every physical choice traces up to a stated business
objective, every risk has a mitigation, and every decision names the option
it rejected — the standard a design review and this exam apply. Archive the
artifact; it is the seed of a VCDX submission
([Chapter 19](19-vcdx-the-distinguished-expert-design-defense-discipline.md)).

## Lab Verification

Complete this sign-off once the five drills have been run end to end. Until
then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The VMware Certified Professional tier is wider than the five exams
Chapters 12–16 map. VCP-DCV (2V0-21.23) is the vSphere 8-generation
flagship that this volume's Chapters 1–9 already cover; VCP-VCF Architect
(2V0-13.25) opens the design path that runs through VCAP Architect and the
Distinguished Expert defense; and VCP-AVI (6V0-22.25) and VCP-PCS
(6V0-21.25) are `6V0` specialist exams scoped to the Avi Load Balancer and
vDefend private-cloud security respectively, while VCP-CO (2V0-32.24) is
the mainstream Cloud Operations exam over the Aria management stack (Aria
Operations, Aria Operations for Logs, Aria Suite Lifecycle). Read the code
family to gauge breadth, pick DCV versus VVF by product generation rather
than prestige, and prepare the specialist and operations exams against a
running product, not documentation.

- [ ] Can place all five exams against specific chapters in this volume.
- [ ] Can choose between VCP-DCV and VCP-VVF Administrator by product
      generation.
- [ ] Can read what a `2V0` versus `6V0` code signals about exam breadth.
- [ ] Has identified VCP-VCF Architect as the start of the design path to
      Chapters 18 and 19.
- [ ] Has run one scoped drill per exam and identified the weakest.
- [ ] Has verified each code against Broadcom's live certification page
      before scheduling.
- [ ] Completed the hands-on readiness lab, including cleanup.
