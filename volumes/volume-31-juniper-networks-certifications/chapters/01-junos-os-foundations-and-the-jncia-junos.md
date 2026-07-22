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

Build a two-device topology (vJunos-switch pair or a vLabs sandbox):
hostname, management addressing, and NETCONF on both; an
interconnecting /30 with reachability proven by ping; a static default
route with a next-hop and a `show route` verification; break the link
address, prove the failure signature in `show interfaces terse` and the
log, then `rollback 1` and re-verify. Finish by exporting the
configuration as set commands and archiving it off-box.

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
