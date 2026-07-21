# Volume XXIV Glossary

Definitions for terms introduced in **Volume XXIV — Dell VxRail
Hyperconverged Infrastructure**, alphabetized. See also the
[volume index](INDEX.md) for pointers back to the chapter section each
term is drawn from, and the [master glossary](../../GLOSSARY.md) for
cross-volume terminology.

**Binding constraint** — In HCI sizing, whichever of cores, memory, or
usable capacity is exhausted first and therefore sets the required node
count. A sizing exercise that does not name its binding constraint is
incomplete. Introduced in Chapter 01.

**Call-home** — Automated telemetry from a VxRail cluster to Dell,
raising support cases for hardware faults without human involvement. The
mechanism by which the single support boundary functions in practice.
Introduced in Chapter 08.

**Capacity chain** — The sequence of deductions from raw drive capacity
to genuinely usable capacity: formatting overhead, storage policy
multiplier, rebuild slack space, and admission control reservation. Each
step removes capacity and the third is the one most often omitted.
Introduced in Chapter 05.

**Capacity trigger threshold** — A utilization percentage, set well below
the point at which a cluster can no longer self-heal, whose crossing
initiates procurement rather than a warning. Introduced in Chapter 05.

**Continuously validated state** — The condition in which a VxRail
cluster's node firmware, BIOS, drivers, ESXi build, vSAN version, and
VxRail Manager version all match a combination Dell has explicitly tested
together. Independent patching of any component takes the cluster out of
this state and affects supportability. Introduced in Chapter 01.

**Coupled scaling** — The property of hyperconverged infrastructure that
compute and storage capacity grow together as nodes are added, whether or
not the workload needs both. The principal architectural cost of the HCI
model. Introduced in Chapter 01.

**Customer-managed vCenter** — A vCenter instance that exists
independently of VxRail and that a VxRail cluster joins at deployment,
leaving vCenter's own version policy and lifecycle with the customer.
Contrast *VxRail-managed vCenter*. Introduced in Chapter 01.

**Division of management** — The boundary between configuration VxRail
owns (firmware, hypervisor version, the networking objects it created)
and configuration the administrator owns (virtual machines, storage
policies, workload networking). The general rule: VxRail owns the
platform's own configuration; you own what runs on it. Introduced in
Chapter 04.

**Drift** — Divergence of a cluster from its continuously validated
state, arising from a version-mismatched node, an out-of-band patch, an
out-of-band firmware update, or an edit to a VxRail-owned configuration
object. Only the first has a legitimate remedy. Introduced in Chapter 06.

**Dynamic node** — A VxRail node carrying compute but no local vSAN
capacity, taking storage from an external array or another vSAN cluster.
Restores independent scaling of compute and storage at the cost of
reintroducing the external storage layer HCI removes. Introduced in
Chapter 02.

**Fault domain** — A grouping of vSAN hosts that share a failure risk —
typically a rack — which vSAN places object copies across rather than
merely across hosts. Configure to match physical reality, or not at all.
Introduced in Chapter 07.

**First run** — VxRail's initial deployment workflow: discovery,
validation, host configuration, vCenter deployment or join, cluster
construction, and VxRail Manager registration. Failures before the third
stage leave nothing built. Introduced in Chapter 03.

**Hyperconverged infrastructure (HCI)** — An architecture that collapses
compute and storage onto the same x86 nodes, replacing an external
storage array with software that pools the nodes' local drives into a
distributed datastore. Introduced in Chapter 01.

**Internal management VLAN** — The non-routable VLAN, 3939 by default,
carrying IPv6 multicast node-discovery advertisements between
unconfigured VxRail nodes and VxRail Manager. The most common VxRail
deployment blocker when the fabric does not carry it. Introduced in
Chapter 02.

**Jointly engineered system** — A platform whose hardware and software
are tested, certified, and supported together as one product by the
vendors of both, rather than assembled from independently supported
components. VxRail's defining commercial and operational property.
Introduced in Chapter 01.

**Lifecycle bundle** — The single packaged release that moves a VxRail
cluster from one continuously validated state to the next, carrying
firmware, drivers, hypervisor, storage stack, and management appliance
versions together. The unit of testing, and therefore the unit of
application. Introduced in Chapter 01, covered in Chapter 06.

**Localization** — The troubleshooting discipline of establishing which
layer a fault lives in — workload, vSphere, vSAN, network, VxRail, or
hardware — before investigating it, working from cheapest check to most
expensive. Introduced in Chapter 09.

**Pre-check** — VxRail's readiness assessment before an upgrade, covering
cluster health, capacity, certificates, connectivity, and version
consistency. Run days before the change window, so that findings can be
remediated outside it. Introduced in Chapter 06.

**Satellite node** — A single VxRail node at an edge site, managed by an
existing VxRail cluster's vCenter, with no local vSAN cluster of its own.
Introduced in Chapter 02.

**Slack space** — Free capacity on a vSAN cluster reserved for rebuilding
objects after a failure. Functional rather than spare: a cluster without
it cannot self-heal and has therefore given up the failure tolerance its
storage policy claims. Introduced in Chapter 05.

**Stretched cluster** — A vSAN cluster spanning two sites with
synchronous mirroring and a witness at a third location, surviving the
loss of an entire site with no data loss. Demands low inter-site latency,
substantial bandwidth, and double the capacity. Introduced in Chapter 07.

**Three-tier infrastructure** — The traditional model in which compute,
storage, and the fabric between them are separately purchased, scaled,
and supported layers. The architecture HCI consolidates. Introduced in
Chapter 01.

**Version reconciliation** — Bringing an incoming node to the cluster's
VxRail version, or the cluster to the node's, before the node can join.
Where the node ships newer, the expansion becomes a cluster upgrade — a
substantially larger change window. Introduced in Chapter 05.

**vSAN ReadyNode** — A hardware configuration validated by the vSAN
vendor for vSAN use but assembled and lifecycle-managed by the customer.
Sits between build-your-own and VxRail in delivery model. Introduced in
Chapter 01.

**VxRail API** — The versioned REST API served by VxRail Manager,
authenticated with vCenter credentials, governing cluster composition,
node lifecycle, system health, and upgrades. Distinct from the vSphere
API, which governs what runs on the platform. Endpoint versions differ
per resource. Introduced in Chapter 08.

**VxRail Manager** — The virtual appliance that serves as VxRail's
control plane, running on the cluster it manages and owning deployment,
node lifecycle, cluster expansion, and validated-state tracking. It
integrates with vCenter rather than replacing it. Introduced in
Chapter 01.

**VxRail-managed vCenter** — A vCenter instance deployed and
lifecycle-managed by VxRail Manager as part of the cluster itself. The
default topology for a standalone cluster. Contrast *customer-managed
vCenter*. Introduced in Chapter 01.

**Witness** — A lightweight appliance holding metadata components that
arbitrate which copy of data is authoritative after a partition in a
two-node or stretched cluster. Must not share a failure domain with
either data location; a witness that fails with what it arbitrates is not
a witness. Introduced in Chapter 07.
