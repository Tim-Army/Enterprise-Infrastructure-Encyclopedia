# Chapter 02: NRS I — IP and Services Foundations

## Learning Objectives

- Explain the NRS I fundamentals (exam 4A0-100): TCP/IP, IPv4, Ethernet, forwarding.
- Navigate the SR OS classic CLI and MD-CLI.
- Configure ports, interfaces, and IP addressing on SR OS.
- Configure static routing and verify the route table.
- Complete a walkthrough for each NRS I foundation topic.

## Theory and Architecture

**NRS I** (exam **4A0-100**, "IP Networks and Services Fundamentals") establishes the vocabulary
and base skills: the **TCP/IP layered model**, **IPv4 addressing** and subnetting, **Ethernet**
switching, **packet forwarding** and the routing table, an introduction to **routing protocols**,
**MPLS tunneling**, and **VPN services** at a conceptual level. On the platform side, NRS I
introduces **SR OS** configuration: the object hierarchy (ports → interfaces → protocols →
services), the **classic CLI** (`configure`, `info`, `admin save`) and the **MD-CLI**
(model-driven, with candidate/commit semantics like `commit`). SR OS separates **router
interfaces** (Layer 3, bound to ports) from **service** constructs (introduced later). The
foundation is being able to bring up ports, assign IP interfaces, route statically, and read state.

## Design Considerations

Plan **IPv4 addressing** and interface roles before configuring. On SR OS, bind **interfaces to
ports** explicitly and use **system/loopback** interfaces for protocol stability. Prefer **MD-CLI**
with its candidate/commit model for safe changes, while knowing the classic CLI. Save configuration
deliberately.

## Implementation and Automation

The labs navigate the CLIs, configure a port and interface, add a static route, and verify state.

## Validation and Troubleshooting

Confirm the NRS I model:

```text
Fundamentals: TCP/IP model, IPv4 addressing, Ethernet, forwarding/route table, routing protocols, MPLS, VPNs.
SR OS: ports -> interfaces -> protocols -> services. Classic CLI (info/admin save) + MD-CLI (commit).
System interface (loopback) for protocol stability. Exam 4A0-100.
```

Common pitfalls: configuring an interface with **no port binding**; and forgetting to **save**
(classic) or **commit** (MD-CLI).

## Security and Best Practices

Use a stable **system interface** for protocols, plan addressing, and secure management access
(AAA, SSH). Prefer **MD-CLI** candidate/commit so changes are validated before activation. Save
configuration after verified changes.

## Hands-On Lab

NRS I walkthroughs. **Shared prerequisites** — an SR OS node (SR OS VSR in containerlab/EVE-NG),
in a lab. **Cost:** none with virtual SR OS.

### Lab 2.1 — Navigate the SR OS CLIs

**Objective:** Inspect configuration in classic CLI and MD-CLI.

```text
# Classic CLI:
A:router# configure
A:router>config# info
A:router# show router route-table

# MD-CLI:
[/]
A:router# show configuration
A:router# show router route-table
```

**Expected result:** the running configuration and route table in both **classic CLI** and
**MD-CLI** — SR OS navigation.

**Negative test:** expect Cisco/Juniper syntax on SR OS; the CLIs differ — learn SR OS `info`/`show
router`.

**Rollback:** none (read-only).

### Lab 2.2 — Configure a port and IP interface

**Objective:** Bring up a routed interface.

```text
A:router>config# port 1/1/1 no shutdown ethernet mode network
A:router>config# router interface "to-core" address 10.1.1.1/30 port 1/1/1
A:router# show router interface
```

**Expected result:** interface **to-core** with 10.1.1.1/30 bound to port 1/1/1 — a routed
interface up.

**Negative test:** create an interface with **no port**; SR OS interfaces bind to a **port** —
attach it.

**Rollback:** remove the interface and shut the port.

### Lab 2.3 — Configure the system interface

**Objective:** Create a stable loopback for protocols.

```text
A:router>config# router interface "system" address 10.0.0.1/32
A:router# show router interface "system"
```

**Expected result:** the **system** interface (10.0.0.1/32) — the stable router ID / protocol
source.

**Negative test:** source protocols from a physical interface that can flap; use the **system**
interface for stability.

**Rollback:** none (keep the system interface).

### Lab 2.4 — Static routing

**Objective:** Add and verify a static route.

```text
A:router>config# router static-route-entry 192.168.0.0/24 next-hop 10.1.1.2
A:router# show router route-table 192.168.0.0/24
```

**Expected result:** the static route to 192.168.0.0/24 in the **route table** — deterministic
forwarding.

**Negative test:** expect connectivity with no route/next-hop; the **route table** must have the
prefix — add the static route.

**Rollback:** remove the static-route-entry.

### Lab 2.5 — Verify forwarding state

**Objective:** Confirm the route and FIB.

```text
A:router# show router route-table
A:router# show router fib 1
```

**Expected result:** routes in the **RIB** and programmed into the **FIB** — end-to-end
forwarding readiness.

**Negative test:** assume a configured route is forwarding without checking the **FIB**; verify it
is programmed.

**Rollback:** none (read-only).

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

NRS I (4A0-100) establishes IP/Ethernet fundamentals and base SR OS skills: navigating the classic
and MD-CLI, configuring ports and interfaces, a stable system interface, static routing, and
verifying the RIB/FIB. Bind interfaces to ports, use the system interface for protocols, and
commit/save changes.

- [ ] I can navigate the classic CLI and MD-CLI.
- [ ] I can configure a port and IP interface.
- [ ] I can create the system interface.
- [ ] I can add and verify a static route.
- [ ] I completed Labs 2.1–2.5 including each negative test.
