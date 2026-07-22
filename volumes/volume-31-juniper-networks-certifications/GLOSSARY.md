# Volume XXXI Glossary

Definitions for terms introduced in **Volume XXXI — Juniper Networks
Certification Tracks**, alphabetized. See also the
[volume index](INDEX.md) and the [master glossary](../../GLOSSARY.md)
for cross-volume terminology.

**Candidate configuration** — The editable copy of a Junos device's
configuration that changes never touch the running system until
`commit`; the foundation of rollback, commit-confirmed, and
transactional automation. Introduced in Chapter 01.

**Commit confirmed** — A Junos commit that automatically rolls back
unless confirmed within a timer; the safety net for every remote or
automated change. Introduced in Chapter 01.

**ERB (edge-routed bridging)** — The EVPN-VXLAN model placing anycast
IRB gateways on every leaf, routing at the fabric edge. Contrast CRB,
which centralizes gateways. Introduced in Chapter 05.

**ESI-LAG** — EVPN Ethernet Segment Identifier LAG: active-active
multihoming where the fabric's control plane, not MC-LAG state,
coordinates the segment. Introduced in Chapter 05.

**Flow processing** — The SRX model that evaluates policy on a
session's first packet and fast-paths the rest via the session table.
Introduced in Chapter 04.

**IRB interface** — Integrated Routing and Bridging: the Junos routed
interface for a VLAN or VNI (`irb.N`), referenced by the VLAN it
serves. Introduced in Chapter 02.

**JNCIA / JNCIS / JNCIP / JNCIE** — Juniper's certification levels:
Associate, Specialist, Professional, Expert; written exams through
Professional, six-hour practicals at Expert. Introduced in Chapter 01.

**JSNAPy** — Juniper Snapshot Administrator for Python: snapshots
operational state and asserts invariants pre/post change. Introduced
in Chapter 06.

**Marvis** — The Mist AI engine: conversational queries, root-cause
identification, and recommended or automated actions over Mist
telemetry. Introduced in Chapter 07.

**PyEZ** — The `junos-eznc` Python library wrapping Junos NETCONF/XML
RPCs with device facts, tables, and transactional config management.
Introduced in Chapter 06.

**Routing instance** — A Junos routing table plus interfaces and
protocols (e.g., `instance-type vrf` for L3VPN customer separation).
Introduced in Chapter 03.

**SLE (service level expectation)** — Mist's user-experience metrics
(time-to-connect, throughput, coverage) decomposed into classifiers
that attribute every failed user-minute to a cause. Introduced in
Chapter 07.

**Security zone** — The SRX trust boundary interfaces join; policy is
written between zone pairs, and host-inbound services are gated per
zone. Introduced in Chapter 04.

**Virtual Chassis** — Multiple EX/QFX switches operating as one
logical device with a single control plane and configuration.
Introduced in Chapter 02.

**vJunos / vLabs** — Juniper's free virtual Junos images
(vJunos-switch, vJunos-router) and free hosted lab sandboxes; the lab
platforms this volume builds on. Introduced in Chapter 01.
