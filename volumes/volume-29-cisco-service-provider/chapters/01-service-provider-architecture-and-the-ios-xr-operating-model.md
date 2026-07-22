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

Build the volume's core in CML: two P routers, two PEs, CE stubs, all
IOS XRv 9000, loopbacks and point-to-point links addressed, MTU set
for later MPLS. Practice the operating model deliberately: make a
change with `commit confirmed`, let it roll back by not confirming,
and read the commit history; make a real change, label the commit,
then `rollback` it and back. Enable NETCONF/gRPC. Export the topology;
every later chapter reuses it. Capture `show configuration commit
list` showing your deliberate commit/rollback sequence.

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
