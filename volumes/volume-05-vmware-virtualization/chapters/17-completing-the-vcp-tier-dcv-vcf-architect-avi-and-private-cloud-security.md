# Chapter 17: Completing the VCP Tier — Data Center Virtualization, VCF Architect, Avi, and Private Cloud Security

![The VMware Certified Professional tier shown complete: the five 2V0-generation exams already covered in Chapters 12–16 (VCP-NV 2V0-41.24, VCP-VCF Administrator 2V0-17.25, VCP-VCF Support 2V0-15.25, VCP-VVF Administrator 2V0-16.25, VCP-VVF Support 2V0-18.25) in one group, and the four professional-level exams this chapter adds in a second group — VCP-DCV Data Center Virtualization (2V0-21.23, on the older vSphere 8 generation), VCP-VCF Architect (2V0-13.25), and two specialist-code VCPs, VCP-AVI Avi Load Balancer Administrator (6V0-22.25) and VCP-PCS Private Cloud Security Administrator (6V0-21.25). All nine sit at the same professional tier and none is a prerequisite for another.](../../../diagrams/volume-05-vmware-virtualization/chapter-17-vcp-tier-landscape.svg)

*Figure 17-1. The complete VCP tier: the five exams mapped in Chapters 12–16, plus the four this chapter adds. Same tier throughout — sequence by the role you hold, not by exam number.*

## Learning Objectives

- Place the four remaining professional-level VMware exams — VCP-DCV
  (2V0-21.23), VCP-VCF Architect (2V0-13.25), VCP-AVI (6V0-22.25), and
  VCP-PCS (6V0-21.25) — against the content already in this volume, and
  identify which existing chapters prepare each.
- Explain why VCP-DCV sits on the older vSphere 8 generation while the
  VVF/VCF exams target 9.0, and what that means for a candidate choosing
  between VCP-DCV and VCP-VVF Administrator.
- Distinguish the 2V0 mainstream-VCP code family from the 6V0 code family
  the Avi and Private Cloud Security exams carry, and read what that
  numbering signals about scope.
- Identify the VCP-VCF Architect exam as the design-role entry point that
  leads toward the VCAP Architect exam (Chapter 18) and, beyond it, the
  Distinguished Expert defense (Chapter 19).
- Build a self-assessment plan for each of the four exams that reuses this
  volume's existing labs rather than assuming a separate lab build.

## Theory and Architecture

Chapters 12 through 16 mapped five VMware Certified Professional exams to
this volume's content. They are not the whole professional tier. Broadcom's
current VCP lineup includes four more exams that this volume's material
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

### The four exams and what each is

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

### Reading the code families

The exam number's prefix is a genuine signal, not decoration:

- **`2V0-…`** is the mainstream professional (VCP) family — VCP-DCV,
  VCP-VCF Architect/Administrator/Support, VCP-VVF Administrator/Support,
  VCP-NV. These are the broad, role-defining exams.
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
  blueprint is the most likely of the four to shift as a 9.0-generation DCV
  successor appears. Before committing study time, confirm on Broadcom's
  page that 2V0-21.23 is still the current DCV exam rather than assuming it
  from this chapter.
- **Ethical preparation boundary.** As with every exam in this volume,
  prepare only from authorized sources: Broadcom's documentation and exam
  guide, official training, and hands-on practice. Material claiming to
  reproduce actual scored questions violates the certification agreement
  and is frequently wrong against the live blueprint — treat any such
  resource as disqualifying rather than helpful.

## Implementation and Automation

### Mapping each exam to existing chapters

```text
# Reuse this volume's chapters as the study spine for all four exams.
# Rate each row 1–5; treat anything below 3 as needing lab time first.

Exam (code)                         | Primary chapters      | Self-rating
------------------------------------|-----------------------|------------
VCP-DCV (2V0-21.23)                 | 1,2,3,4,5,6,7,8,9     |
VCP-VCF Architect (2V0-13.25)       | 1,8,10,11 + design    |
VCP-AVI (6V0-22.25)                 | 4,11 (app delivery)   |
VCP-PCS (6V0-21.25)                 | 8,10,11 (vDefend)     |
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
  the authoritative exam guides for 2V0-21.23, 2V0-13.25, 6V0-22.25, and
  6V0-21.25 (current blueprint domains, item count, duration, price, and
  registration requirements — verify directly before scheduling).
- [VMware Avi Load Balancer documentation](https://techdocs.broadcom.com/us/en/vmware-security-load-balancing/avi-load-balancer.html) —
  product reference for VCP-AVI preparation.
- [CERTIFICATION_BLUEPRINTS.md](../../../CERTIFICATION_BLUEPRINTS.md) —
  this repository's certification-to-volume mapping.
- [Appendix — VMware and Broadcom Certifications and Course Access](../../volume-97-master-appendices/chapters/07-appendix-vmware-broadcom-certifications-and-course-access.md) —
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

This chapter carries topic-level walkthrough labs for the four professional
exams it completes — **VCP-DCV (2V0-21.23)**, **VCP-VCF Architect
(2V0-13.25, a design exam)**, **VCP-AVI (6V0-22.25)**, and **VCP-PCS
(6V0-21.25)** — one lab per testable objective, mapped in the volume
README's coverage tables. The Architect design objectives get command-driven
design walkthroughs plus the Design Exercise below. Every lab ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites** — a vSphere 8.x/9.x lab (vCenter + ESXi + vSAN),
PowerCLI connected as administrator, SSH to hosts for `esxcli`; the AVI labs
add an NSX Advanced Load Balancer (Avi) Controller reachable at `$AVI` with
an `Authorization` header in `$AH`; the PCS labs add NSX with the vDefend
(distributed firewall/IDS-IPS) feature set. **Cost:** none beyond lab
hardware; each lab cleans up after itself.

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** restore prior security policy if changed.

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

**Cleanup:** none (verify only; nothing deployed).

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

**Cleanup:** none (read-only).

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

**Cleanup:** delete the `daily` schedule.

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

### Lab 17.14 — Configure host profiles (Objective 4.16)

**Objective:** Extract a host profile from a reference host.

```powershell
$ref = Get-VMHost | Select -First 1
New-VMHostProfile -Name dcv-profile -ReferenceHost $ref
Get-VMHostProfile -Name dcv-profile | Select Name, @{N='RefHost';E={$_.ReferenceHost}}
```

**Expected result:** a host profile capturing the reference host's config —
the template for consistent host configuration.

**Negative test:** applying the profile to a host with different physical
NICs raises compliance failures on the NIC mappings — profiles encode
host-specific bindings that must be customized.

**Cleanup:** `Remove-VMHostProfile -Profile (Get-VMHostProfile dcv-profile) -Confirm:$false`.

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** `$ds | Set-Datastore -StorageIOControlEnabled $false`.

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

**Cleanup:** none (read-only).

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

**Cleanup:** `$vm | Get-Snapshot | Remove-Snapshot -Confirm:$false`.

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** set the value back to `$true` to restore vCLS.

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

**Cleanup:** delete the support bundle after use.

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

**Cleanup:** `$vm | Get-Snapshot | Remove-Snapshot -Confirm:$false`.

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

**Cleanup:** `Get-DrsRule -Cluster $cl -Name keep-apart | Remove-DrsRule -Confirm:$false`.

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

**Cleanup:** remove the permission and role.

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

**Cleanup:** none (read-only compliance check).

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

**Cleanup:** none (read-only).

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

**Cleanup:** `Get-AlarmDefinition -Name high-vm-cpu | Remove-AlarmDefinition -Confirm:$false`.

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

### Lab 17.38 — Develop a design validation strategy (Objective 1.7)

**Objective:** Define the test that proves the design meets a requirement.

```powershell
Get-Cluster | Select Name, HAEnabled, HAFailoverLevel
```

**Decision to record:** the validation test for the HA requirement (power
off a host; confirm VMs restart within RTO). **Negative test:** a design
signed off without a validation test can fail its first real failover — the
test is the proof.

**Cleanup:** none (read-only).

### Lab 17.39 — Gather and analyze business objectives (Objective 3.1)

**Objective:** Translate objectives into measurable acceptance criteria.

```powershell
Get-Datastore | Select Name, @{N='FreeGB';E={[math]::Round($_.FreeSpaceGB)}}, @{N='CapGB';E={[math]::Round($_.CapacityGB)}}
```

**Decision to record:** each objective with a number (capacity growth %,
RPO, RTO) the design will be measured by. **Negative test:** "improve
performance" without a metric cannot be designed to or validated.

**Cleanup:** none (read-only).

### Lab 17.40 — Create a conceptual model (Objective 3.2)

**Objective:** Express the solution as capabilities and relationships, no
products.

```powershell
Get-Cluster | Select Name, @{N='Capabilities';E={'availability, performance, manageability'}}
```

**Decision to record:** the conceptual entities and how they relate, traced
to the objectives from 3.1. **Negative test:** a conceptual model that
already names vSAN/NSX has skipped to physical — keep it product-neutral.

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

### Lab 17.42 — Service Engine tasks (Objective 1.3)

**Objective:** Read what an SE handles (virtual services placed on it).

```bash
curl -sk -H "$AH" "$AVI/api/serviceengine" | jq -r '.results[0].virtualservice_refs | length'
```

**Expected result:** the count of virtual services an SE hosts — the SE
terminates client connections, load-balances to pools, and runs policies.

**Negative test:** placing every virtual service on one SE overloads it;
placement across the SE group is what scales.

**Cleanup:** none (read-only).

### Lab 17.43 — L4 load-balancing characteristics (Objective 1.4)

**Objective:** Read an L4 (TCP/UDP) virtual service.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | select(.application_profile_ref|test("System-L4")) | .name'
```

**Expected result:** virtual services using an L4 application profile — fast
transport-layer load balancing with no HTTP awareness.

**Negative test:** expecting content-based routing on an L4 VS fails; L4 has
no visibility into HTTP headers/URLs — that needs L7.

**Cleanup:** none (read-only).

### Lab 17.44 — L7 load-balancing characteristics (Objective 1.5)

**Objective:** Read an L7 (HTTP) virtual service and its rules.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | select(.application_profile_ref|test("System-HTTP")) | "\(.name)\t\(.http_policies|length) policies"'
```

**Expected result:** HTTP virtual services with policy counts — L7 inspects
headers/URLs for content switching, redirects, and WAF.

**Negative test:** an L7 VS without SSL termination cannot inspect encrypted
payloads; HTTPS content rules require TLS termination at the VS.

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

### Lab 17.46 — Service Engine Groups (Objective 1.8)

**Objective:** Read SE group sizing parameters.

```bash
curl -sk -H "$AH" "$AVI/api/serviceenginegroup" | jq -r '.results[] | "\(.name)\tmax_se=\(.max_se)\tvs_per_se=\(.max_vs_per_se)"'
```

**Expected result:** per-group `max_se` and `max_vs_per_se` — the group is
the unit of SE scaling and tenancy isolation.

**Negative test:** two tenants sharing one SE group share fate and capacity;
isolation requires separate groups.

**Cleanup:** none (read-only).

### Lab 17.47 — Elastic scale-out use case (Objective 1.9)

**Objective:** Read a virtual service's scaled-out SE set.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | "\(.name)\t\(.num_se_assigned // 1) SEs"'
```

**Expected result:** virtual services spread across multiple SEs — Avi scales
a VS out under load without a config change.

**Negative test:** a VS pinned to one SE cannot scale out; elastic scale-out
requires the SE group to permit it.

**Cleanup:** none (read-only).

### Lab 17.48 — Virtual service, pool, and VIP interaction (Objective 1.10)

**Objective:** Trace a VS to its pool and VIP.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[0] | "\(.name)\tVIP:\(.vip[0].ip_address.addr)\tpool:\(.pool_ref)"'
```

**Expected result:** the VS bound to a VIP (front-end IP) and a pool
(back-end servers) — the three-object model of an Avi service.

**Negative test:** a VS with no pool has nowhere to send traffic; the VIP
answers but every request fails — all three objects are required.

**Cleanup:** none (read-only).

### Lab 17.49 — Features inside an application profile (Objective 1.11)

**Objective:** Read an application profile's L7 feature set.

```bash
curl -sk -H "$AH" "$AVI/api/applicationprofile" | jq -r '.results[] | "\(.name)\t\(.type)"'
```

**Expected result:** profiles (System-HTTP, System-L4, System-Secure-HTTP)
whose type sets features — caching, compression, X-Forwarded-For, WAF.

**Negative test:** applying an L4 profile to a service needing HTTP caching
disables the L7 features caching depends on.

**Cleanup:** none (read-only).

### Lab 17.50 — Functions of the policy engine (Objective 1.12)

**Objective:** Read the HTTP policies attached to a virtual service.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | select(.http_policies|length>0) | "\(.name)\t\(.http_policies|length) policies"'
```

**Expected result:** virtual services with HTTP request/response/security
policies — the policy engine rewrites, redirects, and blocks in-flight.

**Negative test:** rules evaluated in the wrong index order shadow later
rules; policy order is the control, as with any rule engine.

**Cleanup:** none (read-only).

### Lab 17.51 — Certificate management (Objective 1.13)

**Objective:** Read the SSL certificates Avi manages for TLS termination.

```bash
curl -sk -H "$AH" "$AVI/api/sslkeyandcertificate" | jq -r '.results[] | "\(.name)\t\(.type)"'
```

**Expected result:** system and virtual-service certificates — Avi
terminates TLS at the VS using these, and can auto-renew.

**Negative test:** a VS referencing an expired certificate serves TLS errors
to every client; certificate lifecycle is a load-balancer responsibility.

**Cleanup:** none (read-only).

### Lab 17.52 — Turn a WAF on and off (Objective 1.14)

**Objective:** Read WAF policy attachment on virtual services.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice" | jq -r '.results[] | "\(.name)\tWAF:\(.waf_policy_ref // "none")"'
```

**Expected result:** which virtual services have a WAF policy bound —
attaching/detaching `waf_policy_ref` turns WAF on/off per VS.

**Negative test:** enabling WAF in blocking mode without a learning period
blocks legitimate traffic; start in detection mode.

**Cleanup:** none (read-only).

### Lab 17.53 — Capacity impact of WAF (Objective 1.15)

**Objective:** Read SE resource sizing that WAF inspection consumes.

```bash
curl -sk -H "$AH" "$AVI/api/serviceenginegroup" | jq -r '.results[] | "\(.name)\t vcpu=\(.vcpus_per_se)\tmem_mb=\(.memory_per_se)"'
```

**Expected result:** the per-SE CPU/memory — WAF's deep inspection raises SE
CPU per request, so WAF-enabled services need more SE headroom.

**Negative test:** enabling WAF on an SE group sized for L4 throughput
overloads it; capacity must be re-sized for inspection.

**Cleanup:** none (read-only).

### Lab 17.54 — Service Engine capacity limits (Objective 5.1)

**Objective:** Read the SE group's capacity ceilings.

```bash
curl -sk -H "$AH" "$AVI/api/serviceenginegroup" | jq -r '.results[] | "max_se=\(.max_se)\tmax_vs_per_se=\(.max_vs_per_se)\tse_dp_mem=\(.memory_per_se)"'
```

**Expected result:** the maximum SEs, virtual services per SE, and per-SE
memory — the hard limits a capacity plan must respect.

**Negative test:** provisioning virtual services beyond `max_vs_per_se`
forces scale-out or placement failures — the ceiling is real.

**Cleanup:** none (read-only).

### Lab 17.55 — Impact of elastic scale-out (Objective 5.2)

**Objective:** Read a scaled-out VS's per-SE distribution.

```bash
curl -sk -H "$AH" "$AVI/api/virtualservice/<vs-uuid>/runtime" | jq -r '.vip_summary[0].service_engine | length'
```

**Expected result:** the count of SEs serving the VS after scale-out —
throughput rises with SE count, at the cost of more SE resource.

**Negative test:** scale-out with no spare SE capacity in the group cannot
add an SE; the VS stays capacity-bound.

**Cleanup:** none (read-only).

### Lab 17.56 — Performance limits of analytics and logs (Objective 5.3)

**Objective:** Read the analytics profile controlling log/metric volume.

```bash
curl -sk -H "$AH" "$AVI/api/analyticsprofile" | jq -r '.results[] | "\(.name)\tsignificant_log_throttle=\(.significant_log_throttle)"'
```

**Expected result:** throttle settings that bound analytics load — full
non-significant logging at high request rates costs SE CPU and storage.

**Negative test:** enabling full logging for every request on a high-traffic
VS degrades SE performance; throttling protects the data plane.

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

### Lab 17.58 — Enable real-time analytics (Objective 6.3)

**Objective:** Read the real-time metrics window on a VS.

```bash
curl -sk -H "$AH" "$AVI/api/analyticsprofile" | jq -r '.results[0].metrics_realtime_update | "enabled=\(.enabled)\tduration=\(.duration)"'
```

**Expected result:** real-time updates enabled with a duration — sub-minute
metric granularity for live troubleshooting.

**Negative test:** with real-time analytics off, the UI shows only rolled-up
metrics; a live spike is invisible until aggregation.

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

### Lab 17.61 — Log changes when WAF is enabled (Objective 6.6)

**Objective:** Read WAF-enriched log fields on a VS.

```bash
curl -sk -H "$AH" "$AVI/api/analytics/logs/virtualservice/<vs-uuid>?type=1&waf_log.rule_matches=*" | jq -r '.results[0].waf_log.status'
```

**Expected result:** WAF log entries carrying matched rules and a status
(FLAGGED/REJECTED) — logs gain WAF context once WAF is on.

**Negative test:** looking for WAF fields with WAF disabled finds none; the
enrichment appears only when WAF inspects.

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** delete the `auto-web` policy.

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

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

**Cleanup:** none (read-only).

### Lab 17.73 — Four-exam readiness drill (integrative)

**Objective:** Confirm, without booking any exam, which of the four
professional-level exams in this chapter you are closest to ready for, by
running one scoped drill per exam against this volume's existing labs.

**Prerequisites**

- The lab environments from earlier chapters: a vSphere cluster (Chapters
  1–9), NSX with a vDefend DFW policy (Chapters 8, 10–11), and — if
  available — a lab Avi Controller with one virtual service.
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

5. **Score and target.** Rank the four drills by how far over time or how
   reference-dependent each was. The weakest is the exam furthest from
   ready; direct additional lab time there rather than re-reading a domain
   already strong.

6. **Cleanup:** revert the VM, remove any test design notes, and return the
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

Complete this sign-off once the four drills have been run end to end. Until
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
vDefend private-cloud security respectively. Read the code family to gauge
breadth, pick DCV versus VVF by product generation rather than prestige,
and prepare the specialist exams against a running product, not
documentation.

- [ ] Can place all four exams against specific chapters in this volume.
- [ ] Can choose between VCP-DCV and VCP-VVF Administrator by product
      generation.
- [ ] Can read what a `2V0` versus `6V0` code signals about exam breadth.
- [ ] Has identified VCP-VCF Architect as the start of the design path to
      Chapters 18 and 19.
- [ ] Has run one scoped drill per exam and identified the weakest.
- [ ] Has verified each code against Broadcom's live certification page
      before scheduling.
- [ ] Completed the hands-on readiness lab, including cleanup.
