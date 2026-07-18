# Chapter 1: VMware Virtualization Architecture and Design

## Learning Objectives

- Explain why x86 required hardware-assisted virtualization (VT-x/AMD-V)
  and how binary translation and paravirtualization solved the same
  problem before that hardware existed.
- Describe why ESXi is a Type-1 (bare-metal) hypervisor and how that
  differs architecturally from a Type-2 hypervisor such as VMware
  Workstation.
- Explain the internal structure of ESXi: the VMkernel, the per-vCPU
  Virtual Machine Monitor (VMM), the "world" scheduling abstraction, and
  the native device driver model.
- Identify the core components of the vSphere product architecture —
  ESXi, vCenter Server, the HTML5 vSphere Client, and the API surface
  (vSphere API, REST/Automation API, govmomi, PowerCLI).
- Navigate and design a vSphere inventory hierarchy (Datacenter, Cluster,
  Resource Pool, Folder, Host, VM) and explain the permission-propagation
  implications of each object type.
- Position VMware Cloud Foundation (VCF) and VMware vSphere Foundation
  (VVF) against standalone vSphere, at the level of workload domains,
  SDDC Manager, and Cloud Builder.
- Apply design criteria for cluster sizing, host hardware selection
  (CPU generation, NUMA topology, DPU/SmartNIC offload), scale-up versus
  scale-out host design, and multi-site/stretched-cluster availability
  design.

## Theory and Architecture

### x86 virtualization fundamentals

Classic virtualization theory (the Popek and Goldberg requirements) says
a hypervisor can safely virtualize an instruction set if every
instruction that reveals or changes privileged machine state can be
trapped and emulated. The original x86 instruction set, as implemented
through the early 2000s, violated this requirement: it contained roughly
seventeen "sensitive but unprivileged" instructions (for example,
`SGDT`, `SIDT`, `SLDT`, and `POPF` under certain conditions) that
behaved differently depending on the current privilege ring but did not
trap when executed at a lower ring. A guest operating system's kernel
code, which expects to run at ring 0, cannot be run directly at a
lower-privileged ring on unmodified x86 hardware without those
instructions silently producing incorrect results instead of faulting
into the hypervisor.

VMware's original solution, still conceptually relevant to understanding
why modern hypervisors are built the way they are, was **binary
translation (BT)**. The hypervisor scanned blocks of guest kernel code
at runtime and rewrote the sensitive instructions to safe equivalents
before execution, caching the translated blocks for reuse. User-mode
guest code, which does not contain privileged instructions, ran
natively at full speed; only kernel-mode code paid the translation
tax. This let VMware virtualize an unmodified x86 guest OS with no
hardware support and no guest OS modification — a capability that had
no precedent on x86 at the time.

**Paravirtualization** took a different approach: instead of trapping
or translating privileged instructions transparently, the guest OS (or
selected guest drivers) is modified to call the hypervisor explicitly
through a defined interface. Full paravirtualized kernels (in the style
of early Xen) never gained broad enterprise adoption on VMware
platforms, but the underlying idea persists today in **paravirtual
device drivers**: VMware Tools installs the PVSCSI (paravirtual SCSI)
storage adapter driver and the VMXNET3 paravirtual network adapter
driver, both of which communicate with the VMkernel through an
optimized ring-buffer protocol instead of emulating a physical
controller's full register-level behavior. These paravirtual devices
remain the recommended choice for storage and network adapters on
modern guest VMs because they reduce CPU overhead and increase
throughput compared with emulated devices (for example, the emulated
LSI Logic SAS controller or E1000 NIC).

Intel's VT-x (2005) and AMD's AMD-V (2006) resolved the underlying
trapping problem at the silicon level by introducing a new CPU
operating mode — VMX root and non-root operation on Intel, a similar
guest/host mode split on AMD. Guest code, including guest kernel code,
runs natively in non-root mode; any sensitive instruction now correctly
causes a VM-exit into root mode, where the hypervisor can inspect and
emulate it. This eliminated the need for kernel-code binary translation
for CPU virtualization. A second wave of hardware assistance addressed
memory virtualization: Intel's Extended Page Tables (EPT) and AMD's
Rapid Virtualization Indexing (RVI) let the CPU's memory management
unit walk a second, hardware-maintained level of address translation
(guest-physical to host-physical) instead of the hypervisor maintaining
software "shadow page tables" that had to be kept in sync with every
guest page table update — a historically expensive operation. Modern
ESXi uses hardware MMU virtualization (EPT/RVI) by default on any CPU
that supports it, which is universal in current server silicon; shadow
paging remains in the codebase primarily for compatibility with older
processors and specific corner cases (for example, some legacy
Fault Tolerance configurations), not as a normal production path on
current hardware.

### Type-1 vs. Type-2 hypervisor architecture

A **Type-2 hypervisor** runs as an application on top of a general-purpose
host operating system. VMware Workstation and VMware Fusion are Type-2:
the host OS (Windows, Linux, or macOS) owns the hardware, schedules the
CPU, and manages devices; the hypervisor is a privileged process (with a
kernel-mode driver component) that intercepts and virtualizes hardware
access for its guest VMs. This model is well suited to desktop and
engineering use because it coexists with normal host applications, but
it inherits the host OS's scheduling latency, patching cadence, and
attack surface.

**ESXi is a Type-1 (bare-metal) hypervisor**: it installs directly onto
server hardware and *is* the operating system layer. There is no
underlying general-purpose OS to schedule against, patch independently,
or compromise as a separate attack surface. This distinction matters for
three practical reasons an architect should be able to articulate:

- **Performance determinism.** The VMkernel's scheduler makes CPU and
  memory placement decisions directly against physical NUMA topology and
  physical CPU state, without competing against unrelated host-OS
  workloads or a second scheduler layer.
- **Attack surface.** ESXi's installed footprint is deliberately small
  (a purpose-built image, historically well under a gigabyte for the
  base hypervisor) compared to a general-purpose OS hosting a Type-2
  hypervisor, which reduces the number of components that can be
  exploited to reach the virtualization layer.
- **Operational model.** Patching, certificate management, and lifecycle
  operations target the hypervisor directly (through vSphere Lifecycle
  Manager, covered in Chapter 9) rather than through a host OS's own
  patch management stack layered underneath a separate hypervisor
  product.

Historically, VMware's earlier product, "ESX Classic," included a
Linux-derived **Service Console** — a limited general-purpose OS
partition used for agents and local administration, running alongside
the VMkernel. ESXi (first standalone with vSphere 4, and the only
architecture since vSphere 5.0 following ESX's end of life) removed the
Service Console entirely. Local administration moved to the Direct
Console User Interface (DCUI) and remote administration moved to the
vSphere API, `esxcli`, and PowerCLI — closing off what had been a
meaningful attack surface and management-plane inconsistency.

### ESXi internal architecture

ESXi's kernel, the **VMkernel**, is a purpose-built, POSIX-adjacent
microkernel — not a general-purpose OS kernel repurposed for
virtualization. It owns four core responsibilities: CPU scheduling,
memory management, native device I/O, and the virtual switching layer.

The VMkernel schedules work using an abstraction called a **world**: a
schedulable execution context roughly analogous to a process or thread
in a conventional OS, but purpose-built for the hypervisor's needs.
Every running vCPU of every powered-on VM is backed by its own world.
For a multi-vCPU VM, ESXi schedules each vCPU's world independently
under a relaxed co-scheduling model — the vCPUs do not need to start and
stop in lockstep, but the scheduler tracks skew between them so that a
guest OS relying on tightly correlated timing across vCPUs does not
observe pathological drift. Alongside guest vCPU worlds, VMkernel
management agents (for example, the components backing `hostd`, the
management-agent process that vCenter Server talks to) also run as
worlds, giving the scheduler a single, consistent abstraction for all
work on the host.

Each running vCPU is paired with an instance of the **Virtual Machine
Monitor (VMM)** — the component that actually virtualizes that CPU
context: it configures the VMX non-root execution environment, handles
VM-exits caused by privileged instructions or hardware traps, virtualizes
the guest's view of CPU state (registers, MSRs where applicable), and
cooperates with the VMkernel's memory subsystem for address translation.
Conceptually, the VMM is per-vCPU, not per-VM: an 8-vCPU VM is backed by
eight VMM/world pairs, coordinated by the VMkernel scheduler, not by one
monolithic VMM instance managing every vCPU.

Device I/O follows ESXi's **native device driver model**. Rather than
routing I/O through a general-purpose OS's driver stack, hardware
vendors (or VMware itself) provide drivers written specifically against
the VMkernel's driver API and packaged as **VIBs** (vSphere Installation
Bundles) — signed packages that also carry certified/supported metadata
consumed by vSphere Lifecycle Manager (vLCM, covered in Chapter 9).
Drivers run in the VMkernel's address space with direct hardware access,
which is what makes ESXi's I/O path efficient, but it also means driver
quality and VMware/vendor certification status materially affect host
stability — an uncertified or mismatched driver-to-firmware combination
is a common root cause of host-level instability in production.

### vSphere product architecture

"vSphere" is VMware's product name for the combination of the ESXi
hypervisor and the management layer built around it:

- **ESXi hosts** — the Type-1 hypervisor described above, running on
  physical server hardware.
- **vCenter Server** — the centralized management plane. Since vSphere
  6.5, vCenter Server ships exclusively as the vCenter Server Appliance
  (VCSA), a preconfigured Linux (VMware Photon OS) virtual appliance;
  the legacy Windows-installable vCenter Server was discontinued.
  Chapter 3 covers VCSA deployment, identity, and recovery in depth.
- **vSphere Client** — the HTML5-based, Clarity Design System web client
  served by vCenter Server. It replaced both the legacy Windows C#
  client and the earlier Flash-based vSphere Web Client, both long since
  retired.
- **vSphere APIs and SDKs** — the vSphere Web Services API (a SOAP-based
  managed-object API that models every inventory object, its properties,
  and the operations that can be performed on it) and the newer
  vSphere Automation API (a REST API covering a growing subset of the
  same functionality, plus vCenter-specific constructs such as tagging
  and content libraries). **govmomi** is VMware's own open-source Go
  library and CLI (`govc`) for the vSphere Web Services API, widely used
  as the foundation for third-party automation tooling and Kubernetes
  cloud-provider integrations. **PowerCLI** is VMware's PowerShell
  module, which wraps both the SOAP and REST APIs behind PowerShell
  cmdlets (`Connect-VIServer`, `Get-VM`, `New-VM`, and so on) and is the
  most common day-to-day automation surface for vSphere administrators.

Every one of these components talks to the same underlying managed
object model — the vSphere Client, PowerCLI, govmomi, and third-party
integrations are different doors into the same API surface, not
separate control planes. That property is what makes vSphere
automatable end to end: anything achievable in the UI has a
corresponding, scriptable API call.

### vSphere inventory hierarchy

vCenter Server organizes everything it manages into a strict
containment hierarchy. Understanding this hierarchy is a prerequisite
for correct permission and resource-allocation design:

| Object | Purpose | Permission/resource note |
| --- | --- | --- |
| vCenter Server (root) | Top of the inventory tree | Permissions here apply globally unless overridden below |
| Datacenter | Top-level grouping of hosts, clusters, VMs, networks, and datastores | A hard boundary: you cannot vMotion or resource-pool across datacenters, only between them via cross-datacenter/cross-vCenter migration |
| Folder | Organizational container (VM/Template, Host/Cluster, Network, Datastore folder types) | Primary structural tool for delegating permissions by team, environment, or business unit |
| Cluster | A set of ESXi hosts pooled for HA/DRS | Unit of admission control, DRS load balancing, and EVC baseline |
| Resource Pool | Share/reservation/limit-based CPU and memory allocation carve-out within a cluster or standalone host | A **resource-allocation** construct, not a security boundary — a common design mistake is treating resource pools as tenant isolation |
| Host | An individual ESXi host | Can hold permissions directly, though folder-based delegation is more common at scale |
| VM | An individual virtual machine | Leaf object; inherits permissions from its parent folder by default |

Permissions assigned at any level **propagate downward** by default
(propagation can be disabled per-assignment). Because of this, folders
— not resource pools — are the correct tool for building permission
boundaries between teams or environments (for example, a
`Production/App-Tier` VM folder with one set of delegated administrators
and a `Development` VM folder with another). Resource pools should be
sized and nested based on a documented share/reservation/limit strategy
tied to workload priority, not used as a substitute organizational
structure; VMware's own guidance warns against deep resource pool
nesting because child pools' shares are relative only to sibling pools
at the same level, which produces non-obvious allocation results as
nesting grows (informally known as the "resource pool priority-pie
paradox").

### VMware Cloud Foundation and vSphere Foundation

Standalone vSphere — an independently licensed and deployed set of
ESXi hosts managed by a vCenter Server instance — remains a fully
supported deployment model and is what most of this volume's hands-on
material assumes. Broadcom's current product architecture, however,
increasingly ships vSphere as a component of a larger, pre-integrated
bundle rather than as a standalone purchase for many customers:

- **VMware Cloud Foundation (VCF)** is the full software-defined data
  center (SDDC) stack: vSphere and vSAN for compute and storage,
  NSX for network virtualization, and **SDDC Manager** as the
  lifecycle-management and orchestration layer sitting above all of it.
  VCF organizes capacity into **workload domains** — one mandatory
  **management domain** that hosts the SDDC Manager, vCenter Server
  instances, and NSX Manager cluster for the environment, plus one or
  more **VI (virtual infrastructure) workload domains** that host
  tenant/application workloads, each with its own vCenter Server and
  (optionally) its own NSX instance for isolation. **Cloud Builder** is
  the appliance used for the initial, automated bring-up of the
  management domain from a validated bill-of-materials — it is a
  bring-up tool, not an ongoing management plane; day-2 lifecycle
  operations (patching, upgrades, additional workload domains) are
  handled by SDDC Manager after initial deployment.
- **VMware vSphere Foundation (VVF)** is positioned as a lighter bundle
  built on the same vSphere and vSAN foundation, aimed at customers who
  want an HCI-based private cloud without the full NSX-based network
  virtualization and SDDC Manager-driven multi-domain lifecycle
  automation that VCF provides.

Both VCF and VVF are built on the same vSphere 9.x / NSX 4.x baseline
covered throughout this volume — the architectural concepts in this
chapter (VMkernel, inventory hierarchy, cluster design) apply
identically whether vSphere is deployed standalone or as a component
inside VCF/VVF. Exact packaging, included components, and licensing
mechanics change over time; verify current entitlements against
Broadcom's published bill-of-materials for the release you are
deploying rather than assuming this chapter's description of bundling
is a licensing reference.

## Design Considerations

- **Cluster sizing and admission control.** A cluster's usable capacity
  is not its raw sum of CPU/memory — HA admission control reserves
  capacity to guarantee VMs can restart after a host failure. Percentage-
  based admission control (reserve N% of cluster CPU and memory) scales
  more gracefully as a cluster grows than slot-based or dedicated-
  failover-host policies, but every policy trades usable capacity for
  failure headroom, and that trade-off should be sized against the
  cluster's actual host count and failures-to-tolerate target, not left
  at a default.
- **Host count vs. failure headroom.** Small clusters (3–4 hosts) lose a
  large fraction of capacity to a single-host-failure reservation;
  larger clusters (8–16+ hosts) amortize that reservation across more
  hosts and tolerate a host failure with proportionally less capacity
  impact. This is a direct argument for scale-out over very small
  scale-up clusters wherever licensing and rack/power constraints allow
  it.
- **CPU generation consistency and EVC.** Mixing CPU generations within
  a cluster requires Enhanced vMotion Compatibility (EVC), which masks
  newer CPU feature flags to the lowest common denominator so that
  vMotion between mismatched hosts stays safe. Design new clusters with
  a single CPU generation where possible; where mixed generations are
  unavoidable (phased hardware refresh), set the EVC baseline
  deliberately and document which guest-visible CPU features are being
  masked as a result.
- **NUMA topology alignment.** Modern multi-socket (and even
  single-socket, multi-die) server CPUs expose non-uniform memory access
  domains. Size VMs so their vCPU and vRAM allocation fit within a
  single NUMA node where the workload allows it; a VM sized larger than
  one NUMA node's local memory and core count will span nodes and incur
  remote-memory-access latency. Host hardware selection (cores per
  socket, memory channels per socket, DIMMs populated per channel)
  should be chosen with the target VM sizing profile in mind, not
  purely on aggregate core/RAM count.
- **DPU/SmartNIC offload.** Current-generation hosts can offload network
  and security data-plane processing (and, in NSX-integrated designs,
  the distributed firewall) onto a DPU/SmartNIC via the vSphere
  Distributed Services Engine model (introduced conceptually in this
  chapter, detailed in Chapter 4). This frees host CPU cycles otherwise
  spent on software packet processing, at the cost of added hardware
  complexity, DPU-specific firmware/driver lifecycle management, and
  dependency on a narrower hardware compatibility list than standard
  NICs.
- **Scale-up vs. scale-out host design.** Fewer, larger hosts reduce
  per-host licensing and management overhead and simplify NUMA-friendly
  large-VM placement, but increase blast radius (a single host failure
  removes a larger fraction of cluster capacity) and increase HA
  admission-control reservation as a percentage of the cluster. More,
  smaller hosts reduce blast radius and improve DRS placement
  granularity, but increase per-host fixed costs (management NICs,
  chassis overhead, per-socket licensing where applicable) and the
  operational surface (more hosts to patch, monitor, and replace).
  Most enterprise designs land on a middle ground informed by the
  largest single VM the cluster must host comfortably and the
  organization's tolerance for single-host blast radius.
- **Multi-site and stretched-cluster design.** A stretched cluster (most
  commonly built on a vSAN stretched cluster, covered in Chapter 6)
  spans two active sites plus a witness host or appliance at a third
  location, and requires the inter-site network to meet strict latency
  and bandwidth requirements to keep synchronous replication and
  cluster heartbeat traffic viable. Site affinity is enforced through
  DRS host groups and VM/host affinity rules so that, under normal
  operation, a VM's compute and its preferred storage replica stay on
  the same site, minimizing cross-site traffic while still allowing an
  automatic failover if a site is lost. Multi-site design should
  explicitly state its target RPO/RTO and confirm the inter-site link's
  measured latency and bandwidth against the storage platform's
  documented requirements before committing to a stretched design over
  two independent clusters with asynchronous replication.

## Implementation and Automation

Architecture and design decisions become durable only when they are
expressed as automatable, auditable configuration rather than one-off
UI clicks. This section demonstrates the automation surfaces introduced
above — PowerCLI, the REST/Automation API, and govmomi — applied to
inventory structure, the first thing an architecture is expressed
through.

### Connecting with PowerCLI

```powershell
# Install PowerCLI from the PowerShell Gallery (one-time, per admin workstation).
Install-Module -Name VMware.PowerCLI -Scope CurrentUser

# Lab/self-signed certificate environments: decide the trust posture explicitly
# rather than silently ignoring certificate errors in production.
Set-PowerCLIConfiguration -InvalidCertificateAction Ignore -Confirm:$false

Connect-VIServer -Server vcenter01.lab.local -User 'administrator@vsphere.local'
```

### Building the inventory hierarchy

```powershell
# Create a Datacenter object directly under the vCenter Server root folder.
New-Datacenter -Location (Get-Folder -NoRecursion) -Name '<DATACENTER_NAME>'

# Create VM folders that will become the permission-delegation boundary
# described in Design Considerations.
$dc = Get-Datacenter -Name '<DATACENTER_NAME>'
New-Folder -Location (Get-Folder -Name 'vm' -Location $dc) -Name 'Production'
New-Folder -Location (Get-Folder -Name 'vm' -Location $dc) -Name 'Development'

# Create a cluster with HA and DRS enabled, and a percentage-based admission
# control policy sized for an assumed single-host failure to tolerate.
New-Cluster -Location $dc -Name '<CLUSTER_NAME>' `
  -HAEnabled -HAAdmissionControlEnabled `
  -DrsEnabled -DrsAutomationLevel FullyAutomated

Set-Cluster -Cluster '<CLUSTER_NAME>' `
  -HAFailoverLevel 1 -Confirm:$false
```

### Tagging for policy-based governance

Tags and tag categories provide a cross-cutting classification layer
that is independent of the folder hierarchy — useful for attributes
that do not map cleanly to a single containment tree, such as
application owner, data classification, or backup policy.

```powershell
New-TagCategory -Name 'DataClassification' -Cardinality Single `
  -EntityType VirtualMachine

New-Tag -Name 'Restricted' -Category 'DataClassification'
New-Tag -Name 'Internal' -Category 'DataClassification'

Get-VM -Name '<VM_NAME>' | New-TagAssignment -Tag 'Restricted'
```

### Querying the same object model with govmomi

`govc`, govmomi's reference CLI, talks to the identical managed-object
API that PowerCLI wraps — useful for automation written in Go, for
lightweight container-based tooling, or simply to confirm that an
object created through PowerCLI is visible through a completely
independent client.

```bash
export GOVC_URL='https://vcenter01.lab.local'
export GOVC_USERNAME='administrator@vsphere.local'
export GOVC_PASSWORD='<PASSWORD>'
export GOVC_INSECURE=1   # lab/self-signed certificate environments only

# List the datacenter's inventory tree, confirming the folder/cluster
# structure created above is visible through a second API client.
govc find / -type f
govc ls "/<DATACENTER_NAME>/vm"
```

### Querying inventory through the REST/Automation API

```bash
# Authenticate and obtain a session token from the vSphere Automation API.
SESSION=$(curl -sk -X POST \
  -u 'administrator@vsphere.local:<PASSWORD>' \
  https://vcenter01.lab.local/api/session)

# List clusters visible to this session.
curl -sk -H "vmware-api-session-id: ${SESSION//\"/}" \
  https://vcenter01.lab.local/api/vcenter/cluster
```

## Validation and Troubleshooting

- Confirm the inventory hierarchy matches the intended design:
  `Get-Datacenter`, `Get-Folder -Type VM`, and `Get-Cluster | Select
  Name, HAEnabled, DrsEnabled` should reflect exactly the objects and
  settings created above, with no orphaned or duplicate folders left
  over from earlier iterations.
- Confirm HA admission control is actually enforcing the intended
  headroom: `vSphere Client > Hosts and Clusters > select cluster >
  Configure > vSphere Availability` shows the current "Percentage of
  cluster resources reserved" and any admission-control warning if the
  cluster is already over the configured threshold.
- Confirm NUMA topology before finalizing VM sizing standards:
  `vSphere Client > Hosts and Clusters > select host > Configure >
  Hardware > Processors` (or `esxcli hardware cpu global get` /
  `vsish`-level detail for deeper inspection) shows the number of NUMA
  nodes and cores per node so that a "max VM size" standard can be set
  to fit within one node.
- Confirm tag assignments landed where intended: `Get-VM -Name
  '<VM_NAME>' | Get-TagAssignment` should list the expected tags; an
  empty result usually means the tag category's entity type did not
  match the object type it was applied to.

| Symptom | Likely cause | Diagnostic step |
| --- | --- | --- |
| `New-Cluster` succeeds but HA shows a configuration error afterward | Hosts not yet added to the cluster, or a network/management-agent issue on a host | `vSphere Client > cluster > Monitor > vSphere HA` for the specific host-level error |
| vMotion fails between two hosts in an otherwise healthy cluster | CPU feature mismatch without EVC enabled | `Get-Cluster '<CLUSTER_NAME>' \| Get-EvcMode`; enable/raise the EVC baseline if hosts differ in CPU generation |
| Resource pool allocation behaves unexpectedly under contention | Deep resource-pool nesting causing non-obvious relative-share behavior | Flatten the resource pool tree or document expected shares at each nesting level explicitly |
| A delegated administrator can see VMs outside their assigned folder | Permission propagation left enabled, or the permission was assigned above the intended folder | `Get-VIPermission -Entity '<FOLDER_NAME>'` and check `Propagate` and `Entity` for every assignment above that folder |
| govc/REST calls fail with a certificate error but PowerCLI works | Certificate trust handled differently per client (PowerCLI's `Ignore` setting does not apply to other tools) | Set `GOVC_INSECURE=1` or `-k`/`-sk` for lab use, or install the vCenter's CA certificate for anything beyond a lab |

## Security and Best Practices

- Treat folders, not resource pools, as the permission-delegation
  boundary. Resource pools should be documented and sized purely against
  a share/reservation/limit strategy.
- Assign permissions as close to the objects that need them as
  practical, and prefer group-based role assignment (through an
  identity source, covered in Chapter 3) over individual named-user
  permissions, so access reviews scale with the organization rather
  than with the object count.
- Disable permission propagation deliberately wherever a delegated
  administrator's authority should stop at a specific folder boundary —
  the default is propagate-on, and leaving it on unexamined is a common
  source of over-broad access.
- Keep the vCenter Server root and Datacenter objects reserved for a
  small, audited set of full administrators; delegate at the folder and
  cluster level for everyone else.
- Use dedicated, minimally privileged service accounts (not personal
  administrator credentials) for PowerCLI, govmomi, and REST API
  automation, and rotate their credentials on the same cadence as other
  privileged service accounts.
- Design the management network, host hardware, and inventory structure
  together — a well-designed permission model does not compensate for a
  management network that is reachable from general-purpose VM traffic
  (Chapter 4 and Chapter 8 cover network and security architecture in
  depth).

## References and Knowledge Checks

**References**

- VMware vSphere 9.x Documentation — vSphere Concepts and Planning
  Guide, vSphere Virtual Machine Administration Guide, and vSphere
  Resource Management Guide.
- VMware govmomi project documentation and `govc` CLI reference
  (open-source, github.com/vmware/govmomi).
- VMware PowerCLI User's Guide and cmdlet reference.
- Broadcom VMware Cloud Foundation and VMware vSphere Foundation product
  documentation for current workload-domain and bill-of-materials
  details.

**Knowledge Checks**

1. Why did x86 require either binary translation or hardware-assisted
   virtualization before an unmodified guest kernel could run safely at
   a lower privilege ring?
2. What is the relationship between a VMkernel "world" and a VM's vCPU
   count?
3. Why is a resource pool an inappropriate substitute for a permission
   boundary, even though it appears alongside folders in the inventory
   tree?
4. In a VCF deployment, what is the architectural difference between
   the management domain and a VI workload domain?
5. Why does mixing CPU generations within a cluster require an explicit
   EVC baseline decision rather than being handled transparently?

## Hands-On Lab

**Objective:** Build a permission-delegation-ready inventory hierarchy
(datacenter, cluster, folders, tag category) against a lab vCenter
Server using PowerCLI, verify the structure through a second, independent
API client (govc), and prove the resulting permission boundary with a
negative test.

### Prerequisites

- A lab vCenter Server Appliance already deployed and reachable (nested
  or physical), with at least one ESXi host registered — full deployment
  steps are covered in Chapter 2 (ESXi) and Chapter 3 (vCenter). This
  lab assumes that groundwork already exists.
- A workstation with PowerShell 7.x and the `VMware.PowerCLI` module
  installed, and `govc` installed for the cross-verification step
  (`brew install govmomi` or the equivalent binary release for your OS).
- An `administrator@vsphere.local` (or equivalent) credential with
  privileges to create inventory objects and permissions.
- A second, lower-privileged local SSO user account already created (for
  the negative test) — this can be created ahead of time via
  `vSphere Client > Administration > Single Sign On > Users and Groups`.

### Procedure

1. Connect with PowerCLI and confirm the target vCenter Server:

   ```powershell
   Connect-VIServer -Server vcenter01.lab.local -User 'administrator@vsphere.local'
   Get-Datacenter
   ```

   **Expected result:** the session connects without error and lists any
   pre-existing datacenters.

2. Create the datacenter, folders, and cluster:

   ```powershell
   New-Datacenter -Location (Get-Folder -NoRecursion) -Name 'LAB-DC'
   $dc = Get-Datacenter -Name 'LAB-DC'
   New-Folder -Location (Get-Folder -Name 'vm' -Location $dc) -Name 'Restricted-Apps'

   New-Cluster -Location $dc -Name 'LAB-CLUSTER' `
     -HAEnabled -HAAdmissionControlEnabled `
     -DrsEnabled -DrsAutomationLevel FullyAutomated
   ```

   **Expected result:** `Get-Cluster LAB-CLUSTER | Select Name,
   HAEnabled, DrsEnabled` shows both features enabled.

3. Create a tag category and tag for data classification, and confirm
   it is visible through a second API client (govc):

   ```powershell
   New-TagCategory -Name 'DataClassification' -Cardinality Single -EntityType VirtualMachine
   New-Tag -Name 'Restricted' -Category 'DataClassification'
   ```

   ```bash
   export GOVC_URL='https://vcenter01.lab.local'
   export GOVC_USERNAME='administrator@vsphere.local'
   export GOVC_PASSWORD='<PASSWORD>'
   export GOVC_INSECURE=1

   govc tags.category.ls
   govc tags.ls
   ```

   **Expected result:** `DataClassification` and `Restricted` both
   appear in the govc output, confirming both clients see the same
   underlying object model.

4. Create a custom role scoped to read-only VM interaction and assign it
   to the lower-privileged user at the `Restricted-Apps` folder only:

   ```powershell
   $privileges = Get-VIPrivilege -Name 'VirtualMachine.Interact.PowerOn',
                                        'VirtualMachine.Interact.PowerOff'
   New-VIRole -Name 'LabRestrictedOperator' -Privilege $privileges

   New-VIPermission -Entity (Get-Folder -Name 'Restricted-Apps') `
     -Principal 'lab-restricted-user' -Role 'LabRestrictedOperator' `
     -Propagate:$true
   ```

   **Expected result:** `Get-VIPermission -Entity (Get-Folder -Name
   'Restricted-Apps')` shows the new assignment with `Propagate: True`.

5. Move an existing test VM (create one if none exists) into the
   `Restricted-Apps` folder and confirm it inherits the permission:

   ```powershell
   Get-VM -Name '<TEST_VM_NAME>' | Move-VM -Destination (Get-Folder -Name 'Restricted-Apps')
   ```

   **Expected result:** the VM now appears under `Restricted-Apps` in the
   vSphere Client inventory tree.

### Negative Test

Log in to the vSphere Client as `lab-restricted-user` (the account
scoped to `LabRestrictedOperator` at the `Restricted-Apps` folder only).
Attempt two actions: first, power on the test VM inside
`Restricted-Apps` — this should succeed, confirming the assigned
privileges work. Second, attempt to view or modify any object outside
that folder (for example, the `LAB-CLUSTER` object's settings, or a VM
in a different folder). The vSphere Client should either hide those
objects entirely or return a permission-denied error, proving the
folder-scoped permission boundary — not a resource pool, and not a
naming convention — is what is actually enforcing isolation.

### Cleanup

```powershell
Remove-VIPermission -Entity (Get-Folder -Name 'Restricted-Apps') `
  -Principal 'lab-restricted-user' -Role 'LabRestrictedOperator' -Confirm:$false
Remove-VIRole -Role 'LabRestrictedOperator' -Confirm:$false

Get-VM -Name '<TEST_VM_NAME>' | Move-VM -Destination (Get-Folder -Name 'vm' -Location (Get-Datacenter -Name 'LAB-DC'))

Remove-TagAssignment -TagAssignment (Get-TagAssignment -Category 'DataClassification') -Confirm:$false
Remove-Tag -Tag 'Restricted' -Confirm:$false
Remove-TagCategory -Category 'DataClassification' -Confirm:$false

Remove-Cluster -Cluster 'LAB-CLUSTER' -Confirm:$false
Remove-Folder -Folder 'Restricted-Apps' -Confirm:$false
Remove-Datacenter -Datacenter 'LAB-DC' -Confirm:$false

Disconnect-VIServer -Server vcenter01.lab.local -Confirm:$false
```

## Summary and Completion Checklist

x86 virtualization went from software-only binary translation, through
paravirtual device drivers, to today's hardware-assisted VT-x/AMD-V and
EPT/RVI foundation — and that history explains specific ESXi design
choices still visible today, from the native VMkernel driver model to
paravirtual PVSCSI/VMXNET3 adapters. ESXi's Type-1, bare-metal
architecture (VMkernel, per-vCPU VMM, world-based scheduling) is the
foundation the rest of vSphere is built on, and the vSphere product
architecture — ESXi, vCenter Server, the HTML5 Client, and a unified API
surface reachable through PowerCLI, govmomi, or REST — makes every
design decision in this chapter automatable and auditable. Inventory
hierarchy design (datacenter, folder, cluster, resource pool) is not
cosmetic: it directly determines how permissions propagate and how
resources are shared. VCF and VVF package this same vSphere/NSX
foundation into a lifecycle-managed SDDC stack for customers who need
it, without changing the underlying architectural concepts.

- [ ] Can explain why hardware-assisted virtualization replaced binary
      translation for CPU virtualization, and what EPT/RVI replaced for
      memory virtualization.
- [ ] Can articulate the practical differences between Type-1 and
      Type-2 hypervisor architecture beyond "one has a host OS."
- [ ] Can describe the VMkernel/VMM/world relationship for a
      multi-vCPU VM.
- [ ] Can design an inventory hierarchy that uses folders (not resource
      pools) as the permission-delegation boundary.
- [ ] Can position VCF and VVF against standalone vSphere without
      overstating a specific point release or SKU.
- [ ] Completed the hands-on lab, including the negative permission
      test proving folder-scoped delegation is actually enforced.
