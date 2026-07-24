# Chapter 01: Service Provider Architecture and the IOS XR Operating Model

## Learning Objectives

- Describe service provider network structure — access, aggregation,
  edge, and core — and the roles P, PE, and CE play
- Explain what distinguishes SP networks from enterprise: scale,
  multi-tenancy, and service-level obligations
- Operate IOS XR: its two-stage commit, configuration model, process
  restartability, and platform families
- Compare IOS XR, IOS XE, and NX-OS operating models where an SP
  engineer meets all three
- Stand up the lab environment used throughout this volume

## Theory and Architecture

### The shape of a provider network

A service provider network is organized by role, and the vocabulary is
load-bearing for the whole track:

- **P (provider) routers** — the core: label switching at high speed,
  no customer state, running the IGP and the label transport.
- **PE (provider edge) routers** — where customers attach and services
  live: VRFs, VPN address families, L2VPN attachment circuits, QoS
  policing. The PE is where the provider's products are configured.
- **CE (customer edge)** — the customer's device, often outside
  provider control; the PE-CE boundary is a contract expressed in
  routing.

Physically this maps to access (customer aggregation), aggregation/
pre-aggregation, the provider edge, and the core — with route
reflectors and often a separate control-plane hierarchy overlaid.
SPCOR's Architecture domain (15%) tests this structure and the plane
separation (management, control, data) that keeps it operable.

### What makes SP different

Three properties reshape every design decision:

- **Scale.** Full internet BGP tables (~1M IPv4 routes and growing),
  tens of thousands of VPN routes, thousands of devices. Techniques
  that are optional in the enterprise — route reflection, hierarchy,
  aggressive summarization — are mandatory here.
- **Multi-tenancy.** One physical network sells isolated services to
  thousands of customers simultaneously; VRFs and pseudowires are
  products, and one customer must never see another.
- **Service-level obligations.** SLAs on availability, latency, and
  restoration make sub-50-ms protection (Chapter 05) and measurable
  assurance (Chapter 09) contractual, not aspirational.

### IOS XR: the SP operating system

Cisco's flagship SP platforms run **IOS XR**, and its model differs
from IOS XE in ways that matter daily:

- **Two-stage configuration.** You edit a *candidate* configuration
  and then `commit` — atomically. Nothing takes effect until commit;
  `show configuration` (uncommitted) previews the delta, `commit
  confirmed` auto-rolls-back if you do not confirm, and `rollback`
  reverts to any prior commit. This is a safety model the enterprise
  IOS XE world approximates only with effort.
- **A structured configuration** with explicit hierarchy, `commit`
  labels, and per-commit history — the platform natively supports
  the change discipline other chapters have to build.
- **Process modularity.** XR is a microkernel-style system: processes
  restart independently (`process restart`), and a crashed protocol
  does not take the router down.
- **Platforms.** ASR 9000 (edge/aggregation), NCS 500/540/560
  (access/aggregation), NCS 5500/5700 and the 8000 series (core and
  high-scale), and **IOS XRv 9000**, the virtual node this volume
  labs on.

### Three operating models, one engineer

An SP engineer often touches IOS XR (core/edge), IOS XE (some edge and
CPE), and NX-OS (data-center interconnect — Volume XXVII). The
differences to keep straight: XR's commit model versus XE's immediate
apply; XR's address-family-structured config versus XE's flatter
style; and the show-command dialects. This chapter anchors on XR; the
volume flags XE differences where a design spans both.

## Design Considerations

- **Plane separation as design**: dedicated management network,
  control-plane protection (Chapter 08's LPTS on XR), and a data plane
  that never carries management — the SP version of Volume XXVII's
  out-of-band doctrine.
- **Hierarchy is not optional**: IGP areas/levels, BGP route
  reflection, and a clear core/edge boundary are how the network
  scales past the point flat designs collapse.
- **Commit discipline from day one**: use `commit confirmed` for risky
  changes, label commits meaningfully, and treat rollback as a
  first-class recovery tool rather than a last resort.
- **Platform to role**: match XR platforms to core versus edge versus
  access by scale and feature needs, not by habit.

## Implementation and Automation

The volume's lab: a small provider core in CML with IOS XRv 9000 — two
P routers, two PE routers, CE stubs — over which every later chapter
layers IGP, BGP, MPLS, and services. The XR operating essentials:

```text
! Two-stage config: nothing is live until commit
configure
 interface Loopback0
  ipv4 address 10.0.0.1 255.255.255.255
 !
 hostname PE1
show configuration        ! preview the uncommitted delta
commit confirmed 2        ! auto-rollback in 2 min unless confirmed
commit                    ! confirm it (or 'rollback' to undo)
end

! History and recovery
show configuration commit list
rollback configuration to <commit-id>
show configuration commit changes last 1
```

```text
! Platform and plane sanity
show platform
show processes | include Restart
show running-config interface Loopback0
```

Automation enters immediately, as in Volumes XXVII–XXVIII: enable the
model-driven interfaces now (NETCONF/gNMI on XR) so Chapter 09 can
drive the lab programmatically.

```text
netconf-yang agent ssh
grpc
 port 57400
 no-tls        ! lab only; TLS in production (Chapter 08/09)
```

## Validation and Troubleshooting

Bring-up validation is XR-idiomatic: interfaces and loopbacks up
(`show ipv4 interface brief`), the commit actually applied (`show
configuration commit changes last 1` — the number-one XR surprise is
forgetting to commit), and processes healthy (`show processes
blocked`). The chapter's habit, kept for the volume: on XR, **check
whether it was committed** before theorizing about why a change did
nothing — the candidate/running distinction is the most common
false-alarm in the operating model, and `show configuration` (the
uncommitted buffer) is the first thing to read.

## Security and Best Practices

- Management-plane isolation, SSH-only, and AAA against TACACS+ from
  the first commit; XR task-based authorization scopes operators by
  named task groups.
- `commit confirmed` for anything touching reachability — a fat-finger
  that isolates a P router rolls itself back before the pager fires.
- Default credentials rotated at install per the encyclopedia's scope
  boundaries; console and auxiliary access controlled physically and
  logically.

## References and Knowledge Checks

- SPCOR 350-501 v1.1 Architecture domain (15%)
- Cisco IOS XR configuration and system management guides
- Cisco SP network design references (SRND / validated designs)

Knowledge checks:

1. Define P, PE, and CE, and state which device holds customer VPN
   state and which holds none.
2. A change appears to do nothing on IOS XR. What is the first thing
   to check, and which command shows the uncommitted buffer?
3. What does `commit confirmed` protect against, and when should it
   be your default?
4. Name the three planes and one XR mechanism that protects each.

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **the architecture
objectives of SPCOR 350-501 v1.1 (Domain 1) and the Virtualized Architecture
domain of SPCNI 300-540 v1.0** — mapped in the volume README's coverage tables.
Labs use the IOS XR CLI (`RP/0/RP0/CPU0:router#`) and NFV/orchestration tooling.
Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 1.1–1.8** — an IOS XR router (physical or
XRd/IOS XRv), an NFV infrastructure (NFVI) host with a VNF, and a management
station with SSH. **Cost:** none beyond lab resources.

### Lab 1.1 — Describe service provider architectures (SPCOR Objective 1.1)

**Objective:** Read a router's role in the SP layered architecture.

```text
show running-config | include hostname
show isis neighbors summary
show bgp all all summary | include Neighbor|memory
```

**Expected result:** the node's IGP/BGP posture revealing its role — SP networks
layer into **access**, **aggregation/edge (PE)**, and **core (P)**; a P router
runs the IGP and LDP/SR with no VPN/customer state, while a PE holds VRFs and BGP
customer routes. The neighbor counts locate the role.

**Negative test:** assume a router is a P node because it runs the core IGP; if
`show vrf all` lists customer VRFs it is a PE — the presence of customer state,
not the IGP, defines the role.

**Cleanup:** none (read-only).

### Lab 1.2 — Describe Cisco network software architecture (SPCOR Objective 1.2)

**Objective:** Read IOS XR's process/software model.

```text
show version | include "IOS XR|cisco"
show processes | include "Running|Restart"
show install active summary
```

**Expected result:** the IOS XR version, running processes, and active packages —
IOS XR is a microkernel, modular OS: each protocol is a restartable process, with
software delivered as packages (RPMs/SMUs) and configuration applied by
**two-stage commit**, unlike IOS's monolithic model.

**Negative test:** edit config and exit without `commit`; the change does not
take effect — IOS XR's candidate/commit model requires an explicit commit, a key
difference from IOS.

**Cleanup:** none (read-only).

### Lab 1.3 — Describe service provider virtualization (SPCOR Objective 1.3)

**Objective:** Read platform virtualization (LC/RP, or a virtual router).

```text
show platform
show virtual-machine 2>/dev/null || show version | include "XRv|XRd|virtual"
admin show environment 2>/dev/null | include "Location|Slot"
```

**Expected result:** the physical or virtual platform makeup — SP virtualization
spans hardware (line cards, route processors, fabric) and network functions run as
software (XRv/XRd, NFV VNFs), so a "router" may be a VM or container in an NFVI.

**Negative test:** treat a virtual XRd router as having hardware forwarding ASICs;
its data plane is software (or vendor NIC offload) with different scale limits —
the platform type sets the performance envelope.

**Cleanup:** none (read-only).

### Lab 1.4 — Describe IaaS constraints (SPCNI Objective 1.1)

**Objective:** Read the VLAN/segmentation scale of the virtualized fabric.

```text
show l2vpn bridge-domain summary
show evpn summary
show interface | utility egrep "encapsulation dot1q" | wc -l
```

**Expected result:** the L2 segment/bridge-domain count against the platform limit
— classic 802.1Q VLANs cap at 4094, an IaaS scale constraint; SP/DC fabrics use
VXLAN/EVPN or QinQ to segment beyond that for multi-tenant IaaS.

**Negative test:** plan an IaaS tenant model on plain VLANs beyond 4094 segments;
it cannot scale — the VLAN ceiling is the constraint that drives VXLAN/EVPN.

**Cleanup:** none (read-only).

### Lab 1.5 — Determine the cloud service model (SPCNI Objective 1.2)

**Objective:** Classify a workload against IaaS/PaaS/SaaS/FaaS.

```bash
kubectl get pods -A 2>/dev/null | head        # PaaS/containers
virsh list --all 2>/dev/null | head            # IaaS/VMs
```

**Expected result:** VMs (IaaS — customer manages the OS) vs pods (PaaS/containers
— platform manages the runtime) — the model determines who owns which layer:
**IaaS** (compute/network/storage), **PaaS** (runtime), **SaaS** (application),
**FaaS** (function/event); an SP hosting VNFs is consuming IaaS.

**Negative test:** manage OS patching on a SaaS offering; you cannot — the model
dictates the boundary of control, and misjudging it breaks the operational plan.

**Cleanup:** none (read-only).

### Lab 1.6 — Describe container orchestration and virtual machines (SPCNI Objective 1.3)

**Objective:** Contrast a VM and a container running network functions.

```bash
virsh dominfo vnf-router 2>/dev/null | head
kubectl describe pod cnf-router 2>/dev/null | head
```

**Expected result:** the VM's fixed vCPU/RAM vs the container's shared-kernel,
orchestrated lifecycle — VMs (hypervisor, full OS) give strong isolation;
containers (shared kernel, Kubernetes-orchestrated) give density and fast
scaling; SP CNFs increasingly run as containers under Kubernetes.

**Negative test:** expect kernel-level isolation from containers as from VMs;
containers share the host kernel — the isolation model differs and affects
security posture.

**Cleanup:** none (read-only).

### Lab 1.7 — Implement virtualization functions (SPCNI Objective 1.4)

**Objective:** Bring up a VNF and verify its virtual interfaces.

```bash
virsh start vnf-router && virsh domiflist vnf-router
ip link show | grep -E "vnet|tap"
```

**Expected result:** the VNF running with its vNICs mapped to host tap/SR-IOV
interfaces — implementing virtualization functions means instantiating a VNF and
wiring its virtual interfaces to the NFVI data path (OVS-DPDK, SR-IOV) for line-
rate forwarding.

**Negative test:** attach a VNF vNIC to a paravirtual (virtio) path expecting
line rate; without SR-IOV/DPDK the throughput is far lower — the data-path choice
sets performance.

**Cleanup:** `virsh shutdown vnf-router`.

### Lab 1.8 — Deploy NFV using automation and orchestration (SPCNI Objective 1.5)

**Objective:** Deploy a VNF/network service via an orchestrator.

```bash
# ETSI MANO / Cisco ESC / NSO deploys the VNF from a descriptor
osm ns-list 2>/dev/null | head || echo "orchestrator: NSO/ESC/OSM instantiates the VNFD/NSD"
kubectl get networkservices -A 2>/dev/null | head
```

**Expected result:** the network service instantiated from its descriptor — NFV
deployment is automated: an orchestrator (Cisco ESC/NSO, ETSI MANO/OSM) reads a
VNF/NS descriptor and instantiates, configures, and monitors the functions,
replacing manual VM builds.

**Negative test:** instantiate a VNFD whose image/flavor is unavailable on the
VIM; the orchestrator fails the deployment at the resource-allocation step —
descriptors must match VIM capacity.

**Cleanup:** terminate the test network service.

## Lab Verification

Verification means the topology is addressed and reachable at the
link layer, the commit/confirm/rollback sequence is evidenced in the
commit history, and the model-driven agents are enabled. Until then,
the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Service provider networking is enterprise networking under three
multipliers — scale, multi-tenancy, and SLAs — organized by the
P/PE/CE roles and operated, on Cisco, through IOS XR's committed,
modular, recoverable model. This chapter is SPCOR's Architecture
domain and the operating foundation every service in this volume is
committed onto.

- [ ] I can place P, PE, and CE and state what state each holds
- [ ] I use the two-stage commit model, including confirmed and
      rollback, fluently
- [ ] My CML core is built, committed, and exported
- [ ] I know why SP scale forbids flat designs
