# Chapter 9: vSphere Lifecycle, Automation, Observability, and Troubleshooting

## Learning Objectives

- Explain vSphere Lifecycle Manager (vLCM) images and contrast the
  image-based model with the legacy baseline-based patching model.
- Build and remediate a cluster-wide desired-state image, including
  firmware/driver add-ons and hardware compatibility checks.
- Explain how Auto Deploy's network-boot mechanism integrates with vLCM
  desired-state images for large, homogeneous fleets.
- Select the correct automation tool — PowerCLI, the vSphere Automation
  API/govmomi, Terraform, or Ansible — for a given operational task and
  team maturity.
- Configure vCenter Server alarms and explain the event/task/alarm data
  model that observability tooling builds on.
- Generate and interpret ESXi and vCenter Server log bundles for
  troubleshooting, and identify the key log files for common failure
  domains.
- Use `esxtop`/`resxtop` to perform first-pass host performance
  troubleshooting.

## Theory and Architecture

Chapters 2 and 3 covered how an individual ESXi host and vCenter Server
instance come into existence. This chapter covers how a fleet of them is
kept current, observed, and diagnosed once running — the day-2 operational
layer that spans the whole environment rather than a single host or
appliance.

### vSphere Lifecycle Manager: images versus baselines

**vSphere Lifecycle Manager (vLCM)** manages ESXi patching, upgrades, and
driver/firmware currency at the cluster level, and at the current vSphere
9.x baseline operates primarily through **cluster images** — a
desired-state model that has superseded the older **baseline-based**
patching approach (separate patch/extension/upgrade baselines attached to
individual hosts or clusters, remediated somewhat independently of each
other) for new cluster configurations.

- **Baseline-based management** (the legacy model, still encountered on
  environments upgraded forward from older releases and still supported
  for specific scenarios) treats patches, extensions, and upgrades as
  separate baseline types attached to a host or cluster, each remediated
  on its own schedule. It permits drift between hosts in the same cluster
  running slightly different accumulated patch sets unless carefully
  managed.
- **Image-based management** (the current standard for new clusters)
  defines a single **desired-state image** for the entire cluster: a base
  ESXi image (a specific version), optional **vendor add-ons** (OEM
  packages, such as a server vendor's management agent bundle), optional
  **firmware and drivers add-ons** (integrated through a **Hardware
  Support Manager**, a vendor-supplied plugin that lets vLCM manage
  firmware alongside software as part of the same image), and optional
  **components** (individual VIBs layered on top, such as an NSX or
  third-party agent). Every host in the cluster is expected to converge on
  *exactly* this image — vLCM reports and remediates drift at the whole-
  image level rather than patch-by-patch, which eliminates the
  "which hosts got which patches in what order" ambiguity baseline
  management could produce.

```powershell
# PowerCLI: retrieve the current desired-state image for a cluster
$cluster = Get-Cluster -Name "prod-cluster-a"
Get-VMHostImage -Cluster $cluster
```

vLCM performs a **hardware compatibility check** against the VMware
Compatibility Guide data set before allowing an image to be set as a
cluster's desired state, and a **remediation pre-check** before actually
applying it — surfacing issues (a host that would fail to enter
maintenance mode due to DRS/HA constraints, insufficient capacity to
evacuate, an incompatible driver) before committing to the change rather
than discovering them mid-remediation.

### Auto Deploy and vLCM image integration

[Chapter 2](02-esxi-installation-configuration-and-host-operations.md) introduced **Auto Deploy** as a network-boot mechanism. At the
vSphere 9.x baseline, Auto Deploy's boot images are sourced directly from
vLCM cluster images rather than a separately managed Image Builder
profile — a host's Auto Deploy rule assigns it to a cluster, and that
cluster's vLCM desired-state image *is* the image the host boots. This
means image lifecycle for a stateless Auto Deploy fleet and image
lifecycle for a fleet of disk-installed hosts in the same cluster use the
same remediation workflow — there is no longer a separate "Auto Deploy
image management" process distinct from ordinary vLCM cluster image
management.

### Automation tooling landscape

| Tool | Model | Typical fit |
| --- | --- | --- |
| PowerCLI | Imperative PowerShell module wrapping the vSphere API | Ad hoc administration, scripted runbooks, environments with existing PowerShell skill |
| vSphere Automation API / govmomi | Direct REST (Automation API) or Go SDK (govmomi) access to the vCenter Server object model | Custom tooling, integrations, non-PowerShell automation platforms |
| Terraform (vSphere provider) | Declarative, state-tracked infrastructure-as-code | GitOps-style provisioning workflows, teams already using Terraform for other infrastructure domains |
| Ansible (`vmware.vmware` / `community.vmware` collections) | Declarative-leaning, agentless configuration management | Teams standardized on Ansible for cross-platform configuration management, day-2 configuration tasks |

None of these tools is universally correct; the right choice tracks the
team's existing automation investment more than any inherent technical
superiority. A common, defensible pattern is Terraform (or a
Terraform-adjacent pipeline) for initial provisioning of durable objects
(clusters, resource pools, VMs as code) paired with PowerCLI or Ansible
for imperative day-2 operational tasks (patch remediation triggers,
one-off reporting, break-fix scripting) that do not fit a declarative
state model cleanly.

```hcl
# Terraform (vSphere provider): declare a VM resource against an existing template
resource "vsphere_virtual_machine" "app01" {
  name             = "app01"
  resource_pool_id = data.vsphere_resource_pool.pool.id
  datastore_id     = data.vsphere_datastore.ds.id
  num_cpus         = 2
  memory           = 4096
  guest_id         = data.vsphere_virtual_machine.template.guest_id

  network_interface {
    network_id = data.vsphere_network.app_network.id
  }

  clone {
    template_uuid = data.vsphere_virtual_machine.template.id
  }
}
```

```yaml
# Ansible (community.vmware collection): report cluster vLCM compliance status
- name: Report cluster image compliance
  community.vmware.vmware_cluster_info:
    hostname: "{{ vcenter_hostname }}"
    username: "{{ vcenter_username }}"
    password: "{{ vcenter_password }}"
    cluster_name: "prod-cluster-a"
  register: cluster_facts
```

### vCenter Server event, task, and alarm model

vCenter Server records two related but distinct streams for everything
that happens in the inventory: **tasks** (operations initiated by a user
or the system, with a start/end state and success/failure result — a
vMotion, a power-on, a remediation) and **events** (a broader stream of
notable occurrences, including many that are not tied to a discrete task,
such as a host disconnecting or a license expiring soon). **Alarms**
are user- or system-defined rules evaluated against events and/or
performance metric thresholds, producing a defined **action** (an email
notification, an SNMP trap, running a script, or simply changing an
object's displayed alarm state) when triggered. This event/task/alarm
data model is also what most third-party observability and SIEM
integrations for vSphere consume, typically via the same vSphere
Automation API or the older SOAP-based `EventManager`/`AlarmManager`
managed objects rather than a separate telemetry pipeline.

### Skyline Health Diagnostics and Skyline Advisor

Beyond vSAN's cluster-scoped Skyline Health ([Chapter 6](06-vsphere-storage-and-vsan.md)), the broader
**Skyline** capability (delivered as **Skyline Health Diagnostics**,
runnable connected or in a disconnected/air-gapped mode, and the
cloud-connected **Skyline Advisor** service for environments permitted to
send telemetry to Broadcom) proactively evaluates a vSphere environment
against a continuously updated library of known issue signatures —
misconfigurations, known problematic version/driver combinations, and
common support-case root causes — surfacing findings before they become
outages rather than only after a support case is opened.

### Log architecture

| Component | Key log location | Typical content |
| --- | --- | --- |
| ESXi VMkernel | `/var/log/vmkernel.log` | Kernel-level events: device, storage path, network, PSOD context |
| ESXi host management | `/var/log/hostd.log` | Host-local management agent (VM lifecycle operations, host-local API calls) |
| ESXi vCenter agent | `/var/log/vpxa.log` | Communication between the host and vCenter Server |
| vCenter Server core service | `vpxd.log` (within the appliance) | Core vCenter Server task/event processing, DRS/HA orchestration decisions |
| vCenter Server appliance management | VAMI logs (within the appliance) | Appliance-level services, backup jobs, patching |

Both ESXi hosts and the VCSA support generating a complete **support
bundle** (historically referred to by the underlying `vm-support` /
`vc-support` tooling) — a single archive collecting the relevant logs,
configuration state, and, for ESXi, an optional core dump, formatted for
submission to support or for offline analysis. Generating a support
bundle proactively as part of incident response (before state that
explains the failure rotates out of local retention) is standard practice,
not something to defer until a support case is already open.

```bash
# esxcli: generate a support bundle on an ESXi host
vm-support
```

```bash
# From the VCSA appliance shell (or VAMI): generate a vCenter Server support bundle
generate-support-bundle.sh
```

## Design Considerations

- **Baseline-to-image migration timing.** Environments still on
  baseline-based patching should plan a deliberate migration to
  image-based cluster management rather than indefinitely maintaining the
  older model — image-based management is where current and future vLCM
  capability investment is concentrated, and mixed baseline/image
  management across a fleet adds operational complexity without a
  corresponding benefit.
- **Hardware Support Manager dependency for firmware management.**
  Integrated firmware/driver management through vLCM requires the server
  vendor's Hardware Support Manager plugin to be deployed and kept current
  — evaluate vendor support for this integration as part of hardware
  procurement decisions, not as an afterthought once hosts are already
  racked.
  the desired-state image.
- **Remediation window and evacuation capacity.** A cluster image
  remediation evacuates each host in turn (via DRS-driven vMotion, or
  HA-orchestrated where DRS is unavailable); size cluster N+1/N+2 capacity
  with remediation-time evacuation in mind, not only steady-state failure
  tolerance, since a remediation in progress temporarily reduces available
  capacity the same way a host failure would.
- **Automation tool consolidation versus tool sprawl.** Standardizing on
  too few tools for genuinely different job shapes (declarative
  provisioning versus imperative break-fix scripting) forces awkward
  workarounds; standardizing on too many multiplies the operational
  knowledge burden and credential/service-account surface. Choose
  deliberately per job shape and document the choice.
- **Alarm signal-to-noise ratio.** Default out-of-the-box alarms are a
  reasonable starting point, not a finished alerting strategy — tune
  thresholds and scope alarms to what is actually actionable; an
  environment that pages on every transient, self-resolving condition
  trains responders to ignore alerts, which is worse than having fewer,
  better-tuned ones.
- **Log retention and centralization design.** Local ESXi/vCenter log
  retention is bounded by local storage and rotation policy; design
  centralized log forwarding (syslog from ESXi, as covered in [Chapter 2](02-esxi-installation-configuration-and-host-operations.md),
  plus vCenter Server's own log forwarding/integration options) as a
  day-one requirement for any environment with a real incident-response or
  compliance retention need.
- **Skyline Advisor connectivity posture.** Cloud-connected Skyline
  Advisor provides continuously updated findings without local content
  maintenance, at the cost of requiring outbound telemetry connectivity;
  air-gapped or connectivity-restricted environments should plan for the
  disconnected Skyline Health Diagnostics mode and a deliberate process
  for periodically updating its local content instead.

## Implementation and Automation

### Setting and remediating a cluster image

```powershell
# PowerCLI: set a cluster's desired-state image (base image plus a vendor add-on)
$cluster = Get-Cluster -Name "prod-cluster-a"
Set-VMHostImage -Cluster $cluster -BaseImageVersion "9.0.0-<BUILD>" `
  -VendorAddOn "dell-esxi-addon-9.0-<VERSION>"

# Run a remediation pre-check before committing
Test-VMHostImageCompliance -Cluster $cluster

# Remediate the cluster to the desired-state image
Update-VMHostImage -Cluster $cluster -Confirm:$false
```

### Checking image compliance across a cluster

```powershell
# PowerCLI: report per-host compliance against the cluster's desired-state image
Get-VMHostImageCompliance -Cluster (Get-Cluster -Name "prod-cluster-a") |
  Select-Object VMHost, ComplianceStatus
```

### Creating a custom vCenter Server alarm

```powershell
# PowerCLI: create an alarm that triggers an email notification on repeated host disconnects
$alarmMgr = Get-View -Id (Get-View ServiceInstance).Content.AlarmManager
$spec = New-Object VMware.Vim.AlarmSpec
$spec.Name = "Host Disconnected - Repeated"
$spec.Enabled = $true
$spec.Description = "Alerts when a host disconnects from vCenter Server more than once in 30 minutes."
# Trigger/action definitions omitted for brevity; configure via vSphere Client
# Alarm Definitions for the full event-based trigger and action specification.
```

```powershell
# PowerCLI (simpler path): use New-AlarmDefinition for a metric-based alarm
Get-View ServiceInstance | Out-Null
New-AlarmDefinition -Name "Datastore Usage Critical" -Entity (Get-Datacenter -Name "corp-dc") `
  -Enabled:$true -ActionRepeatMinutes 60
```

### Generating support bundles on demand

```bash
# esxcli (from the ESXi shell): generate a host support bundle to a datastore path
vm-support -w /vmfs/volumes/ds-vmfs6-tier1/support-bundles/
```

```bash
# From the VCSA shell: generate a vCenter Server support bundle
generate-support-bundle.sh
```

### First-pass performance troubleshooting with esxtop

```bash
# esxtop: interactive host performance view (press 'c' for CPU, 'm' for memory,
# 'n' for network, 'd' for disk adapter, 'u' for disk device)
esxtop

# resxtop: same tool, run remotely against a target host without local shell access
resxtop --server esxi01.corp.example --username root

# Batch mode: capture a fixed-duration performance snapshot for later analysis
esxtop -b -d 5 -n 12 > /tmp/esxtop-capture.csv
```

## Validation and Troubleshooting

- **vLCM remediation failure diagnosis.** A failed remediation reports the
  specific host and failure stage (pre-check, maintenance-mode entry,
  image apply, post-remediation validation) in the vLCM task detail;
  the most common root causes are DRS/HA constraints preventing clean
  evacuation (an affinity rule with no valid alternate host, insufficient
  cluster slack capacity) and a firmware/driver compatibility rejection
  from the Hardware Support Manager — both are visible in the pre-check
  output if run before committing, which is why skipping the pre-check to
  save time is a false economy.
- **Compliance drift after remediation.** A host reporting non-compliant
  immediately after a reported-successful remediation usually indicates a
  component (a third-party VIB, such as a backup or security agent)
  installed outside vLCM's desired-state image after the fact — bring
  that component into the image definition itself rather than reinstalling
  it manually after every remediation cycle.
- **Alarm not firing as expected.** Confirm the alarm's scope (the
  inventory object it is attached to — alarms do not automatically
  inherit down from a parent object unless explicitly configured to) and
  that the triggering condition's actual threshold/event name matches
  what is occurring; a surprisingly common cause is an alarm correctly
  defined but disabled, or scoped to an object below where the condition
  is actually occurring.
- **Missing or rotated log data during incident response.** If a support
  bundle generated after the fact is missing the relevant window, check
  local log rotation settings (`esxcli system syslog config get` reports
  local rotation size/count) against how long ago the incident occurred
  — this is precisely the gap centralized syslog forwarding ([Chapter 2](02-esxi-installation-configuration-and-host-operations.md))
  is designed to close, and its absence should be treated as a finding
  during incident retrospectives.
- **esxtop/resxtop interpretation basics.** Sustained `%RDY` (CPU ready
  time) above a low single-digit percentage on a VM's world indicates CPU
  contention at the scheduler level, not necessarily a guest-OS-level CPU
  problem; sustained device latency (`DAVG`/`KAVG` in the disk views)
  above a few milliseconds for the storage tier in use indicates a
  storage-path or array-side bottleneck rather than a compute-layer issue
  — esxtop's value is precisely this ability to distinguish which layer a
  performance symptom actually originates in before escalating further.

## Security and Best Practices

- Use dedicated, least-privilege service accounts for automation tooling
  (Terraform, Ansible, custom API integrations) rather than personal or
  shared administrative credentials, and prefer API token or
  certificate-based authentication over long-lived stored passwords where
  the tool supports it.
- Restrict who can modify a cluster's vLCM desired-state image to a
  defined change-control process — an unreviewed image change is
  effectively an unreviewed fleet-wide software change with the same
  blast radius as any other unmanaged production change.
- Verify VIB and image component acceptance levels ([Chapter 2](02-esxi-installation-configuration-and-host-operations.md)) as part of
  any custom image or component addition to a vLCM desired-state image,
  not only at individual host install time.
- Encrypt and access-control support bundles and log exports before
  transmission — they routinely contain configuration detail (network
  topology, hostnames, sometimes credentials embedded in scripts or
  configuration that should not have been placed there in the first
  place) that is sensitive independent of the specific incident being
  investigated.
- Scope automation credentials to the specific inventory objects and
  privileges the automation actually requires, following the same
  least-privilege RBAC discipline covered for human accounts in Chapters
  3 and 8.
- Evaluate Skyline Advisor's telemetry/connectivity posture against
  organizational data-handling policy explicitly, rather than defaulting
  it on or off without a documented decision.

## References and Knowledge Checks

**References**

- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *vSphere Lifecycle Manager* (cluster
  images, Hardware Support Manager, remediation).
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *Auto Deploy*.
- [VMware vSphere 9.x Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/9-0.html) — *vCenter Server Events, Alarms, and
  Automation* (Automation API, PowerCLI).
- [Broadcom Skyline Documentation](https://techdocs.broadcom.com/us/en/vmware-cis/skyline/health-diagnostics/4-0-7/installation-instructions.html) — *Skyline Health Diagnostics* and
  *Skyline Advisor*.
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — dated vSphere
  9.x / NSX 4.x baseline, plus Terraform and Ansible tooling baselines,
  referenced throughout this volume.
- See [Chapter 2](02-esxi-installation-configuration-and-host-operations.md) for ESXi installation methods and Host Profiles, which
  vLCM images complement at the fleet level.
- See [Chapter 7](07-vsphere-availability-mobility-and-cluster-services.md) for DRS/HA behavior that governs remediation-time host
  evacuation.

**Knowledge checks**

1. What does image-based vLCM management eliminate that baseline-based
   management could not, regarding drift between hosts in the same
   cluster?
2. How does Auto Deploy's image source change under current vLCM
   integration compared to a separately managed Image Builder profile?
3. Give a criterion for choosing Terraform versus Ansible versus PowerCLI
   for a specific automation task, rather than treating them as
   interchangeable.
4. Why is a vLCM remediation pre-check not merely a convenience step?
5. In esxtop's CPU view, what does sustained high `%RDY` indicate, and how
   does that differ in root cause from a guest-OS-reported high CPU
   utilization?

## Hands-On Lab

**Objective:** Set a vLCM desired-state image on a lab cluster, run a
compliance check, create a custom alarm, generate a support bundle, and
perform a basic esxtop-based performance observation — including a
deliberate non-compliant-component negative test.

**Prerequisites**

- A vSphere 9.x lab cluster with at least 2 hosts under vLCM image
  management (or convertible to it), and enough free capacity for DRS to
  evacuate one host at a time.
- PowerCLI connected to the lab vCenter with cluster and vLCM privileges.
- SSH or console access to at least one ESXi host for `esxtop` and
  `vm-support`.

**Steps**

1. Confirm (or convert) the cluster to image-based management and inspect
   the current desired-state image:

   ```powershell
   Connect-VIServer -Server vcenter-lab.local
   $cluster = Get-Cluster -Name "lab-cluster"
   Get-VMHostImage -Cluster $cluster
   ```

   **Expected result:** the command returns the current base image
   version and any configured add-ons/components.

2. Run a compliance check against the current image:

   ```powershell
   Get-VMHostImageCompliance -Cluster $cluster | Select-Object VMHost, ComplianceStatus
   ```

   **Expected result:** all hosts report `Compliant` if the cluster was
   already converged.

3. **Negative test:** manually install an unmanaged VIB on one host,
   outside the desired-state image, to simulate configuration drift:

   ```bash
   esxcli software vib install -v /vmfs/volumes/ds-vmfs6-tier1/test-vibs/lab-test.vib \
     --no-sig-check
   ```

   Then re-run the compliance check:

   ```powershell
   Get-VMHostImageCompliance -Cluster $cluster | Select-Object VMHost, ComplianceStatus
   ```

   **Expected result:** the modified host now reports non-compliant,
   demonstrating vLCM's whole-image drift detection.

4. Remediate the cluster to bring the drifted host back into compliance:

   ```powershell
   Test-VMHostImageCompliance -Cluster $cluster
   Update-VMHostImage -Cluster $cluster -Confirm:$false
   ```

   **Expected result:** the previously drifted host reports `Compliant`
   again after remediation completes, and the manually installed test VIB
   is removed as part of convergence to the desired-state image.

5. Create a custom alarm scoped to the lab cluster (for example, a
   datastore usage warning threshold) using the vSphere Client's Alarm
   Definitions editor or `New-AlarmDefinition`.

   **Expected result:** the alarm appears under `vSphere Client > select
   cluster > Configure > Alarm Definitions` and shows as enabled.

6. Generate a support bundle from one lab host:

   ```bash
   vm-support -w /vmfs/volumes/ds-vmfs6-tier1/support-bundles/
   ```

   **Expected result:** a `.tgz` support bundle archive appears at the
   specified datastore path.

7. Observe CPU ready time under a synthetic load (start several CPU-bound
   test VMs beyond the host's logical CPU count to intentionally induce
   contention):

   ```bash
   esxtop
   # press 'c' for the CPU view, observe %RDY per VM world
   ```

   **Expected result:** `%RDY` rises measurably for the contended VMs
   while the test load runs, and returns to baseline after stopping the
   extra load — confirming the tool correctly reflects scheduler
   contention.

8. **Cleanup:** remove the test alarm definition, delete the generated
   support bundle from the datastore, and power off/remove any synthetic
   load-generation test VMs.

   ```powershell
   Get-AlarmDefinition -Name "Datastore Usage Critical" | Remove-AlarmDefinition -Confirm:$false
   ```

## Summary and Completion Checklist

vSphere Lifecycle Manager's image-based cluster management is the current
standard for keeping a fleet current, replacing the older baseline model's
patch-by-patch drift risk with a single desired-state image encompassing
base ESXi version, vendor add-ons, firmware/driver management through a
Hardware Support Manager, and individual components — with Auto Deploy now
sourcing its boot images directly from the same cluster image rather than
a separately managed profile. Automation tool selection (PowerCLI,
vSphere Automation API/govmomi, Terraform, Ansible) should track team
skill and job shape rather than a single mandated tool. The event/task/
alarm data model underlies both native vCenter Server alerting and most
third-party observability integrations, and effective troubleshooting
depends on knowing where the relevant log data lives, generating support
bundles proactively, and using `esxtop`/`resxtop` to correctly attribute a
performance symptom to the layer it actually originates in.

- [ ] Can explain the difference between baseline-based and image-based
      vLCM management and why the latter is the current standard.
- [ ] Can set, check compliance against, and remediate a cluster
      desired-state image.
- [ ] Can select an appropriate automation tool for a given task and
      justify the choice.
- [ ] Can create a custom vCenter Server alarm and explain the
      event/task/alarm data model.
- [ ] Can generate ESXi and vCenter Server support bundles and identify
      key log files for a given failure domain.
- [ ] Can use esxtop/resxtop to distinguish scheduler-level contention
      from other performance symptom sources.
- [ ] Completed the hands-on lab, including the drift negative test and
      full cleanup.
