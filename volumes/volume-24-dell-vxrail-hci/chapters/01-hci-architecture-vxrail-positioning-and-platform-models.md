# Chapter 01: HCI Architecture, VxRail Positioning, and Platform Models

## Learning Objectives

- Explain what hyperconverged infrastructure consolidates, and which
  operational problems that consolidation solves and creates.
- Distinguish VxRail from a build-your-own vSphere cluster on PowerEdge,
  and articulate what the jointly engineered model actually buys.
- Describe the continuously validated state and why it constrains
  ordinary vSphere administration.
- Identify the VxRail node series and platform options, and select an
  appropriate model for a stated workload profile.
- Locate the support boundary between Dell, Broadcom, and the customer.

## Theory and Architecture

### What hyperconverged infrastructure consolidates

Traditional three-tier infrastructure separates compute, storage, and the
network fabric between them into independently purchased, scaled, and
supported layers. A workload runs on a server, its data lives on a SAN
array, and a storage fabric connects the two. Each layer has its own
lifecycle, its own vendor relationship, and its own failure modes.

Hyperconverged infrastructure collapses compute and storage onto the same
x86 nodes, replacing the array with software that pools the nodes' local
drives into a distributed datastore. The network remains external, but
the storage fabric largely disappears into it.

The consolidation buys three things:

- **A single scaling unit.** Capacity and compute grow together by adding
  nodes, which makes growth predictable and procurement simpler.
- **A single management plane.** Storage provisioning becomes a policy
  applied to a virtual machine rather than a LUN negotiated with a
  storage team.
- **A shorter failure-domain chain.** There is no fabric between compute
  and storage to misconfigure, zone incorrectly, or lose a path across.

It also creates a real constraint, and honesty about it matters more than
the marketing: **compute and storage scale together whether or not you
want them to.** A workload that needs far more capacity than cores, or
far more cores than capacity, is a poor HCI fit — you buy the axis you
do not need in order to get the one you do. Storage-dense and
compute-dense node options soften this, but they do not remove it.

### Where VxRail sits

Once the decision to run vSphere and vSAN is made, three delivery models
are available:

| Model | What you assemble | What you own operationally |
| --- | --- | --- |
| Build-your-own on PowerEdge | Hardware, firmware, ESXi, vSAN, vCenter — sourced and versioned independently | Every compatibility decision, every upgrade sequence, and every interoperability failure |
| vSAN ReadyNode | A validated hardware configuration, assembled by you | Software lifecycle and firmware alignment remain yours |
| **VxRail** | Nothing — the platform arrives as an engineered system | Workload placement and capacity; the platform lifecycle is orchestrated for you |

VxRail's distinguishing claim is not performance and not hardware — a
VxRail node is a PowerEdge server. It is **lifecycle**. Dell and
Broadcom jointly test and certify a specific combination of node
firmware, BIOS, drivers, ESXi build, vSAN version, and VxRail Manager
version, and ship it as a single validated bundle.

### The continuously validated state

This is the central concept of the volume, and the one that most often
surprises administrators arriving from self-built vSphere.

A VxRail cluster is intended to sit, at all times, on a combination of
firmware and software that Dell has explicitly tested together. VxRail
Manager tracks that state, and the lifecycle upgrade path moves the
cluster from one validated state to the next as a unit.

The consequence is a genuine loss of autonomy, and it should be
understood before purchase rather than discovered afterwards:

- **You do not patch ESXi independently.** Applying a hypervisor patch
  outside the VxRail bundle takes the cluster out of its validated state
  and can affect supportability.
- **You do not update firmware independently.** Node firmware arrives
  through the VxRail bundle, not through the PowerEdge update paths that
  [Volume XXIII, Chapter 08](../../volume-23-dell-idrac-9-10-administration/chapters/08-firmware-idrac-bios-lifecycle-controller-and-platform-updates.md)
  covers.
- **You do not choose your own vCenter version freely** where vCenter is
  VxRail-managed.

In exchange, upgrades that are genuinely difficult to sequence correctly
on a self-built cluster — firmware, drivers, hypervisor, and storage
stack in the right order, with the cluster staying available throughout —
become a single orchestrated operation.

Whether that trade is worth making is an architectural decision, not a
technical one. A team with strong lifecycle discipline and a preference
for control may reasonably prefer ReadyNodes. A team whose upgrade
backlog is measured in years usually should not.

### VxRail Manager and the management topology

VxRail Manager is the platform's control plane: a virtual appliance that
runs on the cluster it manages and owns deployment, node lifecycle,
cluster expansion, and the validated-state tracking described above. It
integrates into vCenter rather than replacing it, so day-to-day
virtualization administration remains a vSphere activity.

Two deployment topologies exist for vCenter itself, and the choice is
made at deployment time:

- **VxRail-managed vCenter**, deployed and lifecycle-managed by VxRail
  Manager as part of the cluster. Simplest, and the default for a
  standalone cluster.
- **Customer-managed vCenter**, an existing vCenter the cluster joins.
  Necessary where multiple clusters share a vCenter or where vCenter
  version policy is set outside the VxRail lifecycle, and it moves
  vCenter's own upgrade responsibility back to you.

Beneath VxRail Manager, each node retains its iDRAC, which behaves as
[Volume XXIII](../../volume-23-dell-idrac-9-10-administration/README.md)
describes. VxRail Manager orchestrates against those controllers much as
OpenManage Enterprise does across a PowerEdge fleet.

### Platform and node models

VxRail node series are differentiated by chassis form factor and
workload profile rather than by feature tier. The families in current use
cover, broadly:

| Profile | Typical use |
| --- | --- |
| General purpose | Mixed virtualization workloads; the default starting point |
| Compute dense | High core count per rack unit for consolidation-driven deployments |
| Storage dense | Capacity-led workloads where per-node storage outweighs core count |
| Performance and accelerated | GPU-equipped nodes for VDI, AI, and inference workloads |
| Ruggedized and edge | Short-depth or environmentally hardened nodes for edge sites |

Because node families and model numbers change with each hardware
generation, this volume deliberately does not enumerate current model
numbers — they would be stale before the volume's baseline is next
revised. Consult the current VxRail specification sheets and confirm the
node series against the workload profile you are designing for.

**All-flash versus hybrid, and the vSAN generation beneath.** Node
storage configuration determines which vSAN architecture is available.
The distinction between vSAN's original architecture and its express
storage architecture is covered in
[Volume V, Chapter 06](../../volume-05-vmware-virtualization/chapters/06-vsphere-storage-and-vsan.md);
what matters here is that the choice is made at node purchase and is not
trivially reversible.

### The support boundary

VxRail's most practical benefit is arguably the support model, and it is
worth understanding precisely.

Dell is the single point of contact for the entire stack — hardware,
VxRail Manager, and the bundled vSphere and vSAN software. A caller does
not have to establish whether a fault is a Dell problem or a Broadcom
problem before opening a case, and does not have to broker between two
vendors when the answer is contested.

That boundary holds only while the cluster is in a supported state.
Taking the cluster outside its validated state — the independent patching
described above — is what moves a problem back across the boundary onto
the customer.

## Design Considerations

- **Decide the vCenter topology before deployment, not after.**
  Converting between VxRail-managed and customer-managed vCenter is
  disruptive. A single cluster with no existing vSphere estate is well
  served by VxRail-managed vCenter; an organization with an established
  vCenter and version policy usually is not.
- **Size for the axis you will exhaust first, then check the other.**
  HCI's coupled scaling means the binding constraint is whichever of
  cores, memory, or capacity runs out first. Sizing on capacity alone
  routinely produces clusters with idle cores, and sizing on cores alone
  produces clusters that fill unexpectedly.
- **Account for failures-to-tolerate overhead in usable capacity.** Raw
  drive capacity is not usable capacity. The storage policy chosen in
  [Volume V, Chapter 06](../../volume-05-vmware-virtualization/chapters/06-vsphere-storage-and-vsan.md)
  determines the multiplier, and the difference between mirroring and
  erasure coding is substantial at scale.
- **Minimum node counts constrain small deployments more than expected.**
  Availability policy, not workload, sets the floor on cluster size.
  Designing a small site around a two-node or three-node cluster requires
  knowing what each configuration can and cannot tolerate, which
  [Chapter 07](07-availability-stretched-clusters-and-data-protection.md)
  covers.
- **The validated state is an operational commitment, not a feature.**
  If the organization's security policy mandates patching hypervisors on
  a fixed cadence independent of vendor bundles, that policy and VxRail's
  lifecycle model are in direct tension. Resolve it at design time.
- **Edge deployments inherit the whole model, including its upgrades.** A
  ruggedized node at a remote site is still subject to bundle-based
  lifecycle management, and the bandwidth and maintenance-window
  implications of that are easy to underestimate.

## Implementation and Automation

This chapter is architectural and has no deployment procedure of its own;
[Chapter 02](02-physical-installation-network-prerequisites-and-pre-deployment-planning.md)
begins the build. What can usefully be done at this stage is
establishing where a candidate environment stands.

### 1. Confirming what an existing cluster is running

On a deployed cluster, the VxRail version and its validated-state
alignment are visible through VxRail Manager in the vSphere Client. From
the command line, the underlying ESXi build is confirmed the same way as
any vSphere host:

```bash
# ESXi build on a node — the hypervisor half of the validated state.
esxcli system version get

# vSAN health summary, which the cluster's storage policy compliance
# ultimately rests on.
esxcli vsan health cluster list
```

These report the *current* state. Whether that state is a *validated*
state is a question only VxRail Manager can answer, which is precisely
the point of the model.

### 2. Recording a sizing baseline before a design conversation

Before selecting node models, capture what the existing estate actually
consumes. Where the workloads already run on vSphere, PowerCLI gives a
defensible baseline rather than an estimate:

```powershell
# Per-VM consumed compute and storage, as a sizing input.
Connect-VIServer -Server vcenter.example.com

Get-VM | Select-Object Name,
    NumCpu,
    MemoryGB,
    @{N='ProvisionedGB'; E={[math]::Round($_.ProvisionedSpaceGB, 1)}},
    @{N='UsedGB';        E={[math]::Round($_.UsedSpaceGB, 1)}} |
  Sort-Object UsedGB -Descending |
  Export-Csv -Path ./vxrail-sizing-baseline.csv -NoTypeInformation
```

The gap between provisioned and used space in that output is usually the
single largest correction to a first-pass capacity estimate.

## Validation and Troubleshooting

At this stage, validation means confirming that the architectural
decisions are internally consistent rather than testing a deployment.

- **Check that the sizing model names its binding constraint.** A sizing
  document that does not say which of cores, memory, or capacity is
  expected to run out first has not been completed.
- **Check that usable capacity, not raw capacity, is the figure quoted.**
  If the storage policy and its overhead are not stated alongside the
  capacity number, the number is not meaningful.
- **Check that the vCenter topology decision is recorded with its
  reason.** This decision is expensive to revisit and its rationale is
  routinely forgotten.
- **Check that the patching policy conflict has been resolved
  explicitly.** Either the organization accepts bundle-based lifecycle,
  or VxRail is the wrong platform. Leaving this unstated defers a
  conflict into production.

**A common early misconception.** Administrators new to VxRail frequently
assume that because a node is a PowerEdge server, the PowerEdge update
tooling applies to it. It does not, and using it is a reliable way to
leave the validated state. The hardware is familiar; the lifecycle is
not.

## Security and Best Practices

- **Treat VxRail Manager as a tier-0 management system.** It holds
  credentials for the cluster's hosts and, in the VxRail-managed
  topology, for vCenter. Access to it is equivalent to access to the
  platform.
- **Keep the management network separate from workload networks.** The
  reasoning is the same as for iDRAC in
  [Volume XXIII, Chapter 03](../../volume-23-dell-idrac-9-10-administration/chapters/03-management-network-ipv4-ipv6-dns-ntp-and-connectivity.md),
  and the consequences of getting it wrong are larger because the
  management plane reaches further.
- **Do not defer certificate planning.** VxRail deployment generates
  certificates for its components; replacing them with
  internal-CA-issued certificates afterwards is more disruptive than
  planning for it beforehand.
- **Record the support entitlement alongside the design.** The single
  point of contact is only useful if the entitlement is current and the
  cluster is in a supported state; both are worth an explicit
  operational check rather than an assumption.

## References and Knowledge Checks

**References**

- [Dell VxRail product documentation](https://www.dell.com/support/home/en-us/product-support/product/vxrail-appliance-series/docs)
  — the authoritative source for current node models, release notes, and
  support matrices.
- [Dell Technologies Proven Professional certification](https://learning.dell.com/content/dell/en-us/home/certification-overview.html)
  — current VxRail exam codes and descriptions.
- [Volume V, Chapter 06](../../volume-05-vmware-virtualization/chapters/06-vsphere-storage-and-vsan.md)
  — vSAN architecture, storage policies, and the capacity overhead this
  chapter's sizing guidance depends on.
- [Volume XXIII, Chapter 01](../../volume-23-dell-idrac-9-10-administration/chapters/01-architecture-generations-licensing-and-first-access.md)
  — iDRAC architecture, which is present beneath every VxRail node.

**Knowledge checks**

1. A workload needs a large amount of capacity and very little compute.
   Explain why this is a poor HCI fit, and what node choice partially
   mitigates it.
2. What specifically does the continuously validated state prevent an
   administrator from doing, and what does it provide in exchange?
3. Under what circumstances would customer-managed vCenter be the correct
   topology, and what responsibility does that choice move back to you?
4. Why is applying a PowerEdge firmware update to a VxRail node a
   problem, given that the node *is* a PowerEdge server?
5. What single fact must accompany a usable-capacity figure for it to be
   meaningful?

## Hands-On Lab

**Objective:** Produce a defensible VxRail sizing baseline and platform
decision record for a stated workload, without requiring VxRail hardware.

**Prerequisites:** An existing vSphere environment to measure — nested is
sufficient, and [Volume V](../../volume-05-vmware-virtualization/README.md)'s
lab environment serves — plus PowerCLI as installed in
[Volume V, Chapter 09](../../volume-05-vmware-virtualization/chapters/09-vsphere-lifecycle-automation-observability-and-troubleshooting.md).

**This lab does not deploy VxRail.** No free or virtual VxRail edition
exists, as the volume README states. What it does is exercise the
architectural reasoning the Deploy exam tests and that a real engagement
begins with.

**Procedure**

1. Connect to your vCenter and export the sizing baseline using the
   PowerCLI snippet in *Implementation and Automation* above.
2. From the exported CSV, compute totals for vCPU, memory, provisioned
   storage, and used storage.
3. Establish the binding constraint: divide each total by a plausible
   per-node figure for a general-purpose node and record which axis
   requires the most nodes.
4. Apply a storage policy overhead multiplier to the used-storage figure
   — model both a mirroring policy and an erasure-coding policy — and
   recompute the storage-driven node count for each.
5. Write a one-page decision record stating: the binding constraint, the
   node count under each storage policy, the recommended vCenter
   topology with its reason, and whether the organization's patching
   policy is compatible with bundle-based lifecycle management.

**Negative test**

6. Recompute step 4 using *provisioned* rather than *used* storage. Note
   the difference in node count. This is the error that most commonly
   inflates a first-pass HCI quote, and seeing the size of it once is
   worth more than being told about it.

**Expected results**

- A sizing baseline traceable to measured data rather than estimates.
- A node count that differs meaningfully between the two storage
  policies, demonstrating that policy is a sizing input and not a
  post-deployment detail.
- A decision record in which the patching-policy question is answered
  rather than deferred.

**Cleanup**

7. The lab produces documents rather than infrastructure; retain the
   decision record as input to
   [Chapter 02](02-physical-installation-network-prerequisites-and-pre-deployment-planning.md).
   Disconnect the PowerCLI session with `Disconnect-VIServer`.

## Summary and Completion Checklist

Hyperconverged infrastructure trades independent scaling of compute and
storage for a single scaling unit, a single management plane, and a
shorter failure chain. VxRail applies that model as a jointly engineered
system whose distinguishing property is not its hardware — the nodes are
PowerEdge servers — but its lifecycle: a continuously validated state in
which firmware, hypervisor, storage stack, and management appliance move
together as one tested bundle. That model trades administrative autonomy
for orchestrated upgrades and a single support boundary, and whether the
trade is correct is an architectural judgment to make before purchase.

- [ ] Can explain what HCI consolidates and the coupled-scaling
      constraint it introduces.
- [ ] Can distinguish VxRail from ReadyNodes and build-your-own, and
      state what the jointly engineered model actually provides.
- [ ] Can describe the continuously validated state and name three
      things it prevents.
- [ ] Can select a node profile for a stated workload and justify it.
- [ ] Can locate the support boundary and identify what moves a problem
      back across it.
- [ ] Has produced a sizing baseline from measured data and a decision
      record naming the binding constraint.
