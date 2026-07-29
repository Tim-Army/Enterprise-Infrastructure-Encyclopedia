# Chapter 03: VxRail Manager Deployment and First-Run Configuration

## Learning Objectives

- Describe what happens during VxRail first run, in order, and what each
  stage depends on.
- Reach VxRail Manager's initialization interface and drive the
  deployment wizard from a prepared plan.
- Choose correctly between VxRail-managed and customer-managed vCenter at
  the point the wizard asks.
- Interpret deployment validation failures and map them back to the
  prerequisite that was not met.
- Verify a completed deployment and establish a post-deployment baseline.

## Theory and Architecture

### What first run actually does

VxRail's deployment is often described as "automated", which
undersells how much it does and leaves administrators unsure what to
check. The wizard performs, in sequence:

1. **Discovery.** VxRail Manager listens for node advertisements on the
   internal management VLAN and presents the nodes it finds. This is the
   step [Chapter 02](02-physical-installation-network-prerequisites-and-pre-deployment-planning.md)'s
   IPv6 multicast requirement exists for.
2. **Validation.** Every supplied parameter is checked before anything is
   changed: DNS resolves forward and reverse, NTP answers, the addresses
   are free, the VLANs carry traffic, the node versions match. This stage
   is the reason a correctly prepared deployment rarely fails
   destructively — it fails at validation, having built nothing.
3. **Host configuration.** ESXi management networking is applied to each
   node, hostnames set, and the nodes brought onto the management
   network.
4. **vCenter deployment or join.** Either a vCenter appliance is deployed
   and configured, or the cluster registers with an existing one.
5. **Cluster construction.** The distributed switch is created and
   configured, VMkernel adapters for vSAN and vMotion are placed, the
   vSAN datastore is built, and cluster services are enabled.
6. **VxRail Manager registration.** VxRail Manager migrates onto the
   cluster it just built and registers its plugin with vCenter.

Understanding the order matters for troubleshooting: a failure at stage 2
has changed nothing, while a failure at stage 5 has left a partially
built cluster that generally needs to be reset rather than repaired.

### Reaching the initialization interface

Before the cluster exists, VxRail Manager runs on the first node with a
factory-assigned temporary address. The deployment workstation reaches it
by being placed on the same management VLAN, or by the node being cabled
to a laptop directly.

Default temporary addressing and ports vary by VxRail generation, and
this is exactly the kind of detail that ages badly in documentation.
**Consult the VxRail deployment guide for the version you are
installing** rather than relying on a remembered address; the guide is
the authoritative source and it is version-specific for good reason.

What does not change is the shape of the problem: the workstation must
reach the temporary address, which usually means putting it on the
management VLAN untagged with a static address in the same range.

### The vCenter decision, at the moment it is asked

The wizard asks whether to deploy a new VxRail-managed vCenter or join an
existing customer-managed one. [Chapter 01](01-hci-architecture-vxrail-positioning-and-platform-models.md)
covered the trade; this is where it becomes irreversible in practice.

For a customer-managed vCenter, the wizard needs more than an address. It
needs an account with sufficient privilege to create the cluster objects,
the vCenter must already be at a version the VxRail release supports, and
a single sign-on domain and datacenter must be nominated. Each of these
is a place a deployment stalls if it was not established beforehand.

For a VxRail-managed vCenter, the wizard needs the addressing and names,
which the deployment plan already holds, and it handles the rest.

**A common and costly mistake** is selecting customer-managed vCenter
because an existing vCenter happens to be present, without checking its
version against the VxRail release's support matrix. The wizard will
refuse, correctly, and the remedy — upgrading vCenter — is not a task to
begin on deployment day.

### What the wizard configures that you do not touch afterwards

VxRail creates and owns a distributed switch, its port groups, and the
VMkernel adapters on it. Those objects are visible in vCenter and appear
editable, because vCenter does not know they are special.

They are not to be edited by hand. Changing VxRail-managed networking
objects through the vSphere Client is one of the more effective ways to
put a cluster into a state VxRail Manager cannot reconcile, and it is
tempting precisely because the vSphere Client presents no warning. This
is the same validated-state principle from Chapter 01 applied to
configuration rather than versions.

Newer VxRail releases support supplying a customer-managed distributed
switch instead, which shifts that boundary — but the boundary still
exists, it just moves.

## Design Considerations

- **Deploy from a workstation that will remain reachable.** Deployment
  takes a substantial amount of time and the session should not depend on
  a laptop that will move, sleep, or change networks partway through.
- **Do not deploy the cluster and its first workloads in the same
  window.** A cluster that has just been built should be verified,
  baselined, and backed up before anything of value runs on it.
- **Set the management account passwords deliberately.** Deployment
  establishes credentials for ESXi root, vCenter administrator, VxRail
  Manager, and the service accounts. These are tier-0 credentials
  belonging in a vault from the moment they are set, not afterwards.
- **Decide the cluster name carefully.** It propagates into object names,
  certificates, and support records, and renaming afterwards ranges from
  awkward to unsupported.
- **Expect validation to fail at least once on a first deployment.**
  Treat that as the system working. The failure names a prerequisite; fix
  the prerequisite and re-run. Working around validation is not
  available, which is a feature.

## Implementation and Automation

### 1. Pre-flight checks from the deployment workstation

Before opening the wizard, confirm from the workstation itself that the
environment matches the plan. Failures found here cost minutes; the same
failures found at validation cost a deployment window:

```bash
# Every planned name must resolve both ways.
for h in esxi-01 esxi-02 esxi-03 vxm-01 vcsa-01; do
  ip=$(dig +short "${h}.lab.example.com")
  ptr=$(dig +short -x "$ip" 2>/dev/null)
  printf '%-10s %-14s %s\n' "$h" "${ip:-MISSING}" "${ptr:-MISSING}"
done

# Planned addresses must be free — a reply here is a problem, not success.
for ip in 10.10.10.11 10.10.10.12 10.10.10.13 10.10.10.30 10.10.10.31; do
  if ping -c1 -W1 "$ip" >/dev/null 2>&1; then
    echo "IN USE: $ip"
  else
    echo "free:   $ip"
  fi
done

# NTP must answer.
ntpdate -q ntp.lab.example.com
```

Note the inversion in the second check: for addressing, a successful ping
is the failure condition. Duplicate-address collisions are a recurring
deployment problem and this check takes seconds.

### 2. Driving the wizard from the plan

With `vxrail-deployment-plan.yml` from Chapter 02 complete, the wizard
becomes transcription rather than decision-making. Work through it in the
order the plan is written, and resist filling in anything the plan does
not contain — a value invented at the keyboard is a value nobody
reviewed.

Where the wizard offers to validate before proceeding, always take it.

### 3. Confirming the cluster after deployment

Deployment reporting success and the cluster being correct are related
but not identical claims. Verify independently:

```bash
# Host-level: build, cluster membership, and vSAN health.
esxcli system version get
esxcli vsan cluster get
esxcli vsan health cluster list
```

```powershell
# Cluster-level, from PowerCLI: confirm every node joined and services
# came up as intended.
Connect-VIServer -Server vcsa-01.lab.example.com

Get-Cluster | Select-Object Name, HAEnabled, DrsEnabled, DrsAutomationLevel
Get-VMHost | Select-Object Name, ConnectionState, PowerState, Version, Build
Get-VsanClusterConfiguration | Select-Object Cluster, VsanEnabled, StretchedClusterEnabled
```

Every host should report the same `Version` and `Build`. A node running a
different build than its peers has not been brought fully into the
validated state, and that discrepancy should be resolved before the
cluster carries workloads.

### 4. Capturing the post-deployment baseline

The state of a cluster on the day it was built is the reference every
later change is compared against. Capture it while it is true:

```powershell
# A dated baseline of cluster composition and configuration.
$stamp = Get-Date -Format 'yyyy-MM-dd'

Get-VMHost |
  Select-Object Name, Version, Build, Model,
    @{N='CPUCores'; E={$_.NumCpu}},
    @{N='MemoryGB'; E={[math]::Round($_.MemoryTotalGB, 0)}} |
  Export-Csv -Path "./vxrail-baseline-hosts-$stamp.csv" -NoTypeInformation

Get-VDSwitch | Get-VDPortgroup |
  Select-Object VDSwitch, Name, VlanConfiguration |
  Export-Csv -Path "./vxrail-baseline-port-groups-$stamp.csv" -NoTypeInformation
```

## Validation and Troubleshooting

### Reading validation failures

Validation failures are specific, and the useful skill is mapping them
back to the prerequisite rather than reacting to the message:

| Validation failure | Prerequisite not met |
| --- | --- |
| Fewer nodes discovered than expected | IPv6 multicast on the internal management VLAN, or MLD snooping without a querier |
| Hostname cannot be resolved | Missing forward DNS record |
| Certificate or component registration errors | Missing reverse DNS, or NTP unreachable |
| IP address already in use | Address allocated from a range that is not actually free |
| vCenter version not supported | Customer-managed vCenter below the VxRail release's minimum |
| Node version mismatch | A node imaged at a different VxRail version than its peers |

Every one of these is a Chapter 02 item except the last two, which is a
reasonable summary of where deployment effort belongs.

### When deployment fails after building something

A failure past the validation stage generally leaves partial
configuration. The correct response is usually to reset the nodes to
factory state and re-run rather than to repair by hand, because hand
repair produces a cluster whose configuration VxRail Manager did not
create and may not reconcile.

Node reset is a documented VxRail procedure and its exact form is
version-specific — this is a case for the current deployment guide and,
where the deployment is in support scope, for opening a case rather than
improvising. Deployment-time cases are routine and Dell expects them.

### Verifying the VxRail Manager plugin registered

If the VxRail plugin does not appear in the vSphere Client after
deployment, the cluster is built but its management integration is not.
Confirm the plugin's registration state in vCenter before concluding the
deployment is complete; an unregistered plugin means lifecycle management
— the entire point of the platform — is not available.

## Security and Best Practices

- **Change and vault every default credential at deployment.** ESXi root,
  vCenter administrator, and VxRail Manager credentials are set during
  first run; the moment to place them in a credential vault is
  immediately, not at the next audit.
- **Replace default certificates on a planned schedule.** Deployment
  generates self-signed certificates. Replacing them with
  internal-CA-issued certificates is meaningfully easier soon after
  deployment than after integrations have been built against them.
- **Restrict access to VxRail Manager to a management network.** It holds
  credentials for every host in the cluster; treat network access to it
  as equivalent to administrative access to the platform.
- **Enable syslog forwarding before workloads arrive.** The logs from
  deployment and early operation are the ones you most want later and are
  the easiest to lose.
- **Record the deployment outcome against the plan.** Note anything that
  differed from the plan and why. The gap between planned and built
  configuration is where later troubleshooting starts.

## References and Knowledge Checks

**References**

- [Dell VxRail product documentation](https://www.dell.com/support/home/en-us/product-support/product/vxrail-appliance-series/docs)
  — the version-specific deployment guide, which is authoritative for
  initialization addressing, wizard fields, and node reset procedures.
- [Volume V, Chapter 03](../../volume-005-vmware-virtualization/chapters/03-vcenter-server-deployment-identity-and-recovery.md)
  — vCenter deployment, single sign-on, and identity, which the
  customer-managed topology assumes.
- [Volume V, Chapter 04](../../volume-005-vmware-virtualization/chapters/04-vsphere-virtual-networking.md)
  — distributed switching, which VxRail creates and owns.
- [Chapter 02](02-physical-installation-network-prerequisites-and-pre-deployment-planning.md)
  — the prerequisites every validation failure in this chapter maps back
  to.

**Knowledge checks**

1. List the six stages of first run in order, and state which stages can
   fail without leaving partial configuration.
2. What three things does a customer-managed vCenter require that a
   VxRail-managed one does not?
3. Why is editing VxRail-created distributed switch objects through the
   vSphere Client a problem, given that the client permits it?
4. In the pre-flight address check, why is a successful ping the failure
   condition?
5. A deployment fails at stage 5. Why is resetting the nodes usually
   preferable to repairing the partial configuration by hand?

## Hands-On Lab

This chapter is the **highest-value chapter for the Deploy exam**: "Deploying the VxRail Cluster"
is its heaviest domain at **24%**, and "Post-Deployment procedures" adds 18%. It carries a lab for
each deployment step — initialization, the deployment wizard, build validation, and first
post-deployment tasks. Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 3.1–3.4** — VxRail nodes racked and cabled with the network
prepared and validated (Chapter 02), the deployment configuration ready, and a workstation on the
management VLAN. **Cost:** none beyond lab hardware.

### Lab 3.1 — Initialize and reach VxRail Manager (Topic: Deployment)

**Objective:** Bring up the primary node and reach the deployment UI.

```text
# Power on the nodes. VxRail's internal discovery (IPv6 multicast on the mgmt VLAN) elects a
#   primary node and starts VxRail Manager on it. From the jump host:
#   - browse to the VxRail Manager initial IP (default per the platform guide)
#   - confirm the Manager sees all expected nodes in the "discovered nodes" list
```

**Expected result:** VxRail Manager is reachable and lists every discovered node — first-run
discovery over the management VLAN is what assembles the nodes into a deployable set; all expected
nodes appearing confirms the network prep (Chapter 02) is correct and the build can proceed.

**Negative test:** find fewer nodes than expected in discovery; a node is on the wrong VLAN or its
uplink/MTU is wrong — the discovery count is the immediate check that the physical/network layer is
right before you deploy.

**Cleanup:** none (proceed to Lab 3.2).

### Lab 3.2 — Run the deployment wizard (Topic: Cluster build)

**Objective:** Configure and start the cluster build.

```text
# In VxRail Manager: run the guided deployment (or upload the validated configuration JSON):
#   - choose vCenter: VxRail-managed embedded vCenter, or a customer-supplied external vCenter
#   - enter hostnames/IPs, DNS, NTP, VLAN IDs, and passwords from the plan (Chapter 02)
#   - validate the configuration, then start the build
```

**Expected result:** the wizard validates the inputs and begins building the cluster (deploying
vCenter if embedded, configuring ESXi hosts, forming the vSAN datastore) — the deployment is a
guided, validated, largely unattended process that turns discovered nodes into a running vSphere+
vSAN cluster.

**Negative test:** proceed past a validation warning (e.g. a DNS record missing); the build fails
partway and must be cleaned up — let validation pass cleanly before starting, because a mid-build
failure is costly to unwind.

**Cleanup:** none (proceed to validation).

### Lab 3.3 — Validate the built cluster (Topic: Deployment validation)

**Objective:** Confirm the cluster deployed correctly.

```bash
curl -sk -u 'administrator@vsphere.local:<pass>' https://<vxm>/rest/vxm/v1/system | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print('version:',d.get('version'),'health:',d.get('health'),'installed:',d.get('installed'))"
# vSphere Client: confirm the cluster, all hosts connected, and a healthy vSAN datastore.
```

**Expected result:** the VxRail system reports installed/healthy, all hosts are connected in
vCenter, and the vSAN datastore is present and healthy — validating the deployed state (via the API
and the vSphere Client) confirms the build succeeded before any workload is placed.

**Negative test:** place production VMs immediately without checking vSAN health; a disk-group or
network warning left from deployment degrades storage under load — validate health first.

**Cleanup:** none.

### Lab 3.4 — First post-deployment tasks (Topic: Post-deployment)

**Objective:** Complete the essential post-deploy configuration.

```text
# In VxRail Manager / vSphere Client, complete first tasks:
#   - register the cluster for support (SupportAssist / Secure Connect Gateway, Chapter 09)
#   - configure a vSAN storage policy appropriate to the cluster size (FTT, Chapter 07)
#   - set up alerting/CloudIQ, and confirm the LCM baseline (Continuously Validated State)
#   - create workload networks/port groups for VMs
```

**Expected result:** the cluster is registered for support, has an appropriate default storage
policy, is monitored, and is ready for workloads — post-deployment procedures (18% of the exam) turn
a freshly built cluster into a production-ready, supported, monitored platform.

**Negative test:** hand a freshly deployed cluster to production with no support registration, no
reviewed storage policy, and no monitoring; the first hardware fault has no proactive case and the
default policy may not match your resilience needs — post-deploy tasks are what make it operable.

**Cleanup:** none.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

VxRail first run is a six-stage sequence that validates everything before
it changes anything, which is why a well-prepared deployment either
succeeds or fails harmlessly at validation. The decisions that matter are
made before the wizard opens — the vCenter topology, the addressing, the
names — and the wizard itself should be transcription from a reviewed
plan. Afterwards, the cluster's own reporting of success is not
verification: confirm build consistency across nodes, confirm the VxRail
plugin registered, and capture a dated baseline while the cluster is
still in the state it was designed to be in.

- [ ] Can describe the six first-run stages and which fail non-
      destructively.
- [ ] Can state what customer-managed vCenter additionally requires.
- [ ] Can map each validation failure back to its prerequisite.
- [ ] Knows not to edit VxRail-owned networking objects by hand, and why.
- [ ] Has run a complete pre-flight check including address availability.
- [ ] Has captured a dated post-deployment baseline and verified it
      detects drift.
