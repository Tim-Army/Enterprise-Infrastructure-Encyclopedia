# Volume CM — Tim's Lab Gear

> The physical lab this encyclopedia is built and tested on: the reasoning
> behind the hardware choices, the as-built inventory of compute, network,
> and storage, and the diagrams that keep the picture true. A living
> reference for one specific lab, not a vendor-neutral guide.

## Overview

Volume CM is a **personal reference volume**. Where the instructional and
certification volumes teach technologies in the abstract, this one documents
the concrete rack the rest of the encyclopedia runs on — the Dell PowerEdge
hosts, the single Cisco Nexus doing all the VLAN and LACP work, the Unraid
NAS, and the management planes that keep it recoverable. It is the answer to
"what is this actually running on," kept in the same repository as the labs so
the two never drift apart.

It is deliberately lighter in structure than the instructional volumes: three
reference chapters rather than the full learning-objectives-through-lab
template, because its job is to *record* a lab, not to teach one.

- **[Chapter 01 — Equipment Considerations](chapters/01-equipment-considerations.md)**
  — the trade-offs that decide what earns a rack unit: compute, networking,
  storage, power and noise, rack and sourcing, and how each choice shows up in
  this lab.
- **[Chapter 02 — Current Equipment](chapters/02-current-equipment.md)**
  — the as-built inventory from the live configuration: hosts, the Nexus, the
  VLAN plan, addressing, storage, virtualization, and the management planes.
  Confirmed facts are recorded; hardware specifics still to measure are marked
  **TBD**. No credentials are included.
- **[Chapter 03 — Current Diagrams](chapters/03-current-diagrams.md)**
  — the lab drawn two ways (network topology and rack elevation) in the
  encyclopedia's house style, with the logical VLAN/addressing plan as the
  third view.

## Relationship to other volumes

This volume is the hardware backdrop for the hands-on builds elsewhere:

- **[Volume XXVI — Proxmox Virtualization Lab on Dell PowerEdge R640](../volume-026-proxmox-lab-poweredge-r640/README.md)**
  builds `proxmox-1` (ru12) — its network chapter covers the VLAN-aware bridge
  and the LACP bond referenced here.
- **[Volume XIX — Fortinet NSE Certification Program](../volume-019-fortinet-network-security/README.md)**
  covers the FortiGate-VM (`fortigate-7-6-2`) deployed onto this lab.

## Reading path

Read it top to bottom the first time — **considerations → inventory →
diagrams** — then treat Chapter 02 as the reference you update whenever the lab
changes, and regenerate Chapter 03's diagrams to match. A diagram that has
drifted from the running configuration is worse than none.

## Maintenance note

The inventory and diagrams describe a live lab and are expected to change. When
gear is added, moved, or reconfigured, update Chapter 02's tables first, then
regenerate the Chapter 03 figures so the drawn view and the recorded view stay
in agreement.
