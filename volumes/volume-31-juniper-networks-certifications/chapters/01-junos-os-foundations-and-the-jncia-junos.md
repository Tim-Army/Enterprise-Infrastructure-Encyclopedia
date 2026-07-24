# Chapter 01: Junos OS Foundations and the JNCIA-Junos

## Learning Objectives

- Explain the Junos OS architecture: the separation of control and
  forwarding planes, the routing engine, and the packet forwarding
  engine
- Navigate operational and configuration modes, the candidate
  configuration, and the commit model with confidence
- Configure interfaces, static routing, and basic routing policy on any
  Junos platform
- Map the Juniper certification program — eight tracks, four levels —
  and the role of the JNCIA-Junos (JN0-106) as the shared entry point
- Build a personal Junos lab with vLabs or vJunos images

## Theory and Architecture

### One operating system, one entry exam

Juniper's certification program is built on a fact of its product line:
**one network operating system** spans routers (MX, ACX), switches (EX,
QFX), and firewalls (SRX). Learn Junos once and the syntax, the commit
model, and the troubleshooting habits carry across every platform and
every track. The program mirrors this: the **JNCIA-Junos (JN0-106)** is
the prerequisite for both the Enterprise and Service Provider
specialist exams and the conceptual foundation for every other track.
The exam runs 90 minutes with 65 multiple-choice questions, written to
Junos OS 21.2, delivered by Pearson VUE (verified against Juniper's
certification pages, 22 July 2026 — JN0-106 replaced JN0-105 when the
older exam retired on 5 April 2026).

### Control plane and forwarding plane, honestly separated

Junos runs the **routing engine (RE)** — protocols, management, the
configuration database — as processes over a kernel, while the
**packet forwarding engine (PFE)** forwards traffic using a forwarding
table the RE pushes down. The separation is not marketing: `restart
routing` restarts the routing protocol daemon (rpd) without stopping
packet forwarding, and in-service software upgrades lean on the same
boundary. Daemons are isolated — rpd, dcd (interfaces), mgd
(management) — so one failing process does not take the box with it.

### The configuration model is the product

The single most exam-relevant idea in Junos is the **candidate
configuration**: edits never touch the running system until `commit`.
The model gives you `commit check` (validate without applying), `commit
confirmed` (auto-rollback unless confirmed — the remote-change safety
net), `rollback 0..49` (fifty stored configurations), and `show |
compare` (the diff before you leap). Configuration is a hierarchy —
`interfaces`, `protocols`, `policy-options`, `system` — edited with
`set`/`delete` statements or by navigating with `edit` and `up`.

## Design Considerations

- **Lab platform.** vJunos-switch and vJunos-router are free downloads
  that run in EVE-NG, GNS3, or CML alongside the rest of this
  encyclopedia's labs; Juniper vLabs provides free, time-boxed hosted
  topologies with nothing to install. Either covers every JNCIA-Junos
  objective.
- **Track choice comes later.** JNCIA-Junos is deliberately
  track-neutral. Defer the enterprise-versus-service-provider decision
  until Chapter 02 and 03; the foundation is identical.
- **Recertification.** Juniper certifications are valid for three
  years and re-certify by passing any exam at the same or higher level
  in any track — a design that rewards breadth.

## Implementation and Automation

```text
# First safe steps on any Junos box
cli                                   # from the shell to operational mode
show version                          # platform and Junos release
configure                             # enter configuration mode
set system host-name lab-ex1
set interfaces ge-0/0/0 unit 0 family inet address 10.30.10.21/24
show | compare                        # the diff against the running config
commit check                          # validate only
commit confirmed 5                    # apply; auto-rollback in 5 minutes
commit                                # confirm it
rollback 1                            # bring back the previous config
show configuration | display set      # the whole config as set commands
```

Automation starts on day one: every Junos box speaks NETCONF over SSH
(`set system services netconf ssh`), and `show ... | display xml`
reveals the structured data beneath every CLI command — the seed for
Chapter 06.

## Validation and Troubleshooting

- `show interfaces terse` — the one-screen state of every interface
- `show route protocol static` / `show route 10.30.10.0/24` — is the
  route there, and which protocol won?
- `ping`, `traceroute`, and `monitor traffic interface ge-0/0/0`
  (tcpdump built in) for the data plane
- `show log messages | last 50` and `show system alarms` before
  touching anything
- `run` inside configuration mode executes operational commands without
  leaving your edit — the habit that separates fast candidates from
  slow ones

## Security and Best Practices

- Set a root authentication password before the first commit — Junos
  refuses to commit without one
- Prefer `commit confirmed` for any remote change, every time
- Use login classes to scope operator access; reserve the root shell
- Archive configurations off-box (`set system archival configuration`)
  and keep rollback depth in mind — fifty is generous, not infinite

## References and Knowledge Checks

- JNCIA-Junos (JN0-106) exam objectives on Juniper's certification
  pages — the authority on domains and weighting
- Juniper *Day One: Exploring the Junos CLI* (free library)
- Junos documentation: CLI User Guide, "Junos OS Overview"

Knowledge checks:

1. A colleague commits a change that severs your management session.
   What single earlier command would have saved the box, and what does
   it do?
2. Name the two Junos planes, the components that embody them, and one
   operational command that proves they are separate.
3. Where does a `set` statement live before `commit`, and how do you
   view exactly what will change?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every exam objective of
the JNCIA-Junos (JN0-106) exam** — the associate baseline for the Enterprise and
Service Provider tracks — mapped in the volume README's coverage tables. Labs use
the Junos CLI (operational and configuration modes). Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 1.1–1.7** — a Junos device (vMX/vSRX/vJunos or
hardware) running Junos OS 21.2+, console/SSH access, and a peer device for
routing. **Cost:** none beyond lab resources.

### Lab 1.1 — Networking Fundamentals (Objective: Networking Fundamentals)

**Objective:** Verify Layer 2/Layer 3 addressing and longest-match forwarding.

```text
show interfaces terse
show arp
show route 10.0.0.0/8
```

**Expected result:** interface IP/MAC bindings, the ARP (L2↔L3 resolution) table,
and the longest-match route for the destination — the fundamentals: L2 addressing
(MAC/ARP), L3 addressing (IP/subnet), and longest-prefix-match routing that Junos
applies to forward.

**Negative test:** look up a host in a subnet the device has no route to;
`show route` returns no match and traffic is dropped — longest-match needs a
covering route (or a default).

**Cleanup:** none (read-only).

### Lab 1.2 — Junos OS Fundamentals (Objective: Junos OS Fundamentals)

**Objective:** Read the control/forwarding-plane split (RE vs PFE).

```text
show chassis routing-engine | match "Model|Load"
show pfe statistics traffic | match "packets"
show system processes summary | match rpd
```

**Expected result:** the Routing Engine (control plane, runs `rpd`) and PFE
(forwarding plane) statistics — Junos separates the **Routing Engine** (protocols,
config, management) from the **Packet Forwarding Engine** (hardware forwarding);
transit traffic stays in the PFE, exception/host traffic punts to the RE.

**Negative test:** expect protocol computation on the PFE; it runs on the RE
(`rpd`) — conflating the planes misplaces where a CPU spike or a protocol fault
originates.

**Cleanup:** none (read-only).

### Lab 1.3 — User Interfaces (Objective: User Interfaces)

**Objective:** Exercise candidate vs active configuration and the CLI modes.

```text
configure
set system host-name LAB-R1
show | compare
commit check
rollback 0
exit
```

**Expected result:** `show | compare` shows the candidate change (`+ host-name
LAB-R1`), `commit check` validates it, and `rollback 0` discards it — Junos edits a
**candidate** config that only becomes **active** on `commit`, with `compare`,
`commit check`, and `rollback` as the safety net.

**Negative test:** make a change and `exit` configuration mode without committing;
`show configuration` (operational) shows the change absent — uncommitted candidate
edits do not take effect.

**Cleanup:** `rollback 0` (already done) leaves the candidate clean.

### Lab 1.4 — Configuration Basics (Objective: Configuration Basics)

**Objective:** Apply core initial configuration (user, interface, NTP, syslog).

```text
configure
set system login user neteng class read-only authentication plain-text-password
set interfaces ge-0/0/0 unit 0 family inet address 10.0.0.1/30
set system ntp server 10.0.0.200
set system syslog host 10.0.0.201 any info
show | compare
commit and-quit
```

**Expected result:** the candidate diff showing the user, interface address, NTP,
and syslog, then a successful commit — configuration basics: users/login classes,
interface addressing, and system services (NTP, syslog), optionally reused via
**configuration groups**.

**Negative test:** commit an interface address overlapping another interface's
subnet; Junos rejects the commit with a conflict — commit-time validation catches
overlaps.

**Cleanup:** `configure; delete system login user neteng; commit`.

### Lab 1.5 — Operational Monitoring and Maintenance (Objective: Operational Monitoring and Maintenance)

**Objective:** Monitor interfaces and reachability; read software version.

```text
show interfaces ge-0/0/0 extensive | match "error|drops|rate"
monitor interface traffic
ping 10.0.0.2 count 3
traceroute 10.0.0.2
show version
```

**Expected result:** interface counters/errors, live traffic, reachability, and the
Junos version — the operational toolset for monitoring (show/monitor, interface
stats) and maintenance (ping/traceroute, version for upgrades, root-password
recovery).

**Negative test:** `ping` a host across a downed interface; it fails with no
response while `show interfaces` shows the link `down` — the interface state
explains the reachability failure.

**Cleanup:** none (read-only; press `q` to exit monitor).

### Lab 1.6 — Routing Fundamentals (Objective: Routing Fundamentals)

**Objective:** Read the routing vs forwarding table and add a static route.

```text
show route protocol static
configure
set routing-options static route 192.0.2.0/24 next-hop 10.0.0.2
commit and-quit
show route 192.0.2.0/24
show route forwarding-table destination 192.0.2.1
```

**Expected result:** the static route in the RIB (`show route`) and its resolved
entry in the FIB (`show route forwarding-table`) — Junos builds the **routing
table** (RIB, all candidate routes with preferences) and installs the best into the
**forwarding table** (FIB) the PFE uses.

**Negative test:** add a static route whose next-hop is unreachable; it stays
`hidden` in the RIB and never enters the FIB — the next-hop must resolve.

**Cleanup:** `configure; delete routing-options static route 192.0.2.0/24; commit`.

### Lab 1.7 — Routing Policy and Firewall Filters (Objective: Routing Policy and Firewall Filters)

**Objective:** Apply a routing policy and a firewall filter, and verify effect.

```text
configure
set policy-options policy-statement REJECT-RFC1918 term t1 from route-filter 10.0.0.0/8 orlonger
set policy-options policy-statement REJECT-RFC1918 term t1 then reject
set firewall family inet filter PROTECT term t1 from source-address 0.0.0.0/0
set firewall family inet filter PROTECT term t1 then count blocked discard
show | compare
commit and-quit
show firewall filter PROTECT
```

**Expected result:** the policy and filter in the candidate diff, then the filter's
counters — routing **policy** controls which routes are imported/exported (match
terms → accept/reject), while **firewall filters** control which packets are
permitted (match → count/accept/discard), each evaluated top-down with a default at
the end.

**Negative test:** a policy with a term that never matches falls through to the
default policy (e.g., accept for BGP) — the default action applies when no term
matches, so an incomplete policy can leak routes.

**Cleanup:** `configure; delete policy-options policy-statement REJECT-RFC1918;
delete firewall family inet filter PROTECT; commit`.

## Lab Verification

Verification means both devices commit cleanly with root
authentication set, the /30 passes traffic both directions, the static
route appears with the expected next-hop, and the rollback restored the
working state with a matching `show | compare` proof.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] Junos architecture explained: RE, PFE, and daemon isolation
- [ ] Candidate configuration and commit lifecycle demonstrated
- [ ] Interfaces, static routing, and rollback proven in the lab
- [ ] JNCIA-Junos (JN0-106) objectives reviewed against this chapter
- [ ] Lab platform (vLabs or vJunos) chosen and working
