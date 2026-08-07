# Chapter 01: Equipment Considerations

This volume documents the physical lab this encyclopedia is built and tested
on. Before the inventory (Chapter 02) and the diagrams (Chapter 03), this
chapter records the *reasoning* — the trade-offs that decide what hardware
earns a rack unit. A home or personal lab is not a production data center on a
budget; it is a deliberately different set of compromises, and writing them
down keeps future purchases honest.

## Why physical gear at all

Cloud is cheaper to start and impossible to beat for elastic capacity, but a
physical lab buys three things a cloud account does not: **hands on the real
control planes** (iDRAC, NX-OS, a hypervisor's bare-metal networking), **fixed
cost** for a workload that runs 24×7, and **failure you can cause on purpose**
— pull a NIC, corrupt a boot device, mis-tag a VLAN — without a bill or a
blast radius. Everything in this encyclopedia that says "run it and watch it
break" assumes gear you own.

The counter-cost is real: power, noise, heat, space, and the time to keep it
running. The considerations below are ordered the way they actually bite.

## Compute

- **Buy decommissioned enterprise, not new prosumer.** A three-generations-old
  dual-socket server has more cores, more ECC RAM capacity, and real
  out-of-band management (iDRAC / iLO) for a fraction of a new workstation.
  The tax is power draw and noise.
- **RAM over cores, for a virtualization lab.** VM density is capped by memory
  long before CPU. Prioritize total DIMM capacity (and populate channels for
  bandwidth) over top clock speed.
- **Out-of-band management is non-negotiable.** iDRAC / iLO gives console,
  power, and virtual media when the OS or the data network is down — the only
  way to recover a host you just mis-networked from across the house.
- **Nested virtualization** (Intel VT-x/EPT, AMD-V/RVI exposed to guests) is
  required to run GNS3, EVE-NG, or a nested hypervisor inside a VM. Confirm the
  platform and hypervisor pass it through.
- **Boot devices separate from data.** A small mirrored boot device (Dell BOSS,
  or a pair of SATA SSDs) keeps the hypervisor off the bulk storage, so a data
  array can be rebuilt without reinstalling the host.

## Networking

- **One managed L3 switch is the backbone.** VLANs, tagged trunks, LACP
  port-channels, and inter-VLAN routing are the whole point; an unmanaged
  switch teaches none of it. Used enterprise switches (Cisco Nexus / Catalyst,
  Arista) are cheap on the second-hand market.
- **10 Gb where the hosts live, 1 Gb is fine for management.** SFP+ with DAC
  cables inside a rack is cheaper and cooler than 10GBASE-T.
- **Reserve a separate out-of-band (OOB) management network.** Keep iDRAC/iLO,
  the switch's own `mgmt0`, and the hypervisor management IPs reachable even
  when a data VLAN is broken. Mixing management into a data VLAN is how you
  lock yourself out — a lesson this lab learned the hard way (see Chapter 02's
  VLAN plan, and the OOB-versus-data-VLAN note there).
- **Pick a native/parking VLAN that carries no data.** Trunk mismatches are
  silent; a dedicated unused native VLAN (and consistent native across every
  trunk) prevents leakage and the tagged-versus-untagged bugs that eat an
  afternoon.
- **LACP needs both ends.** A host bond in `802.3ad` mode only aggregates if
  the switch ports are a matching `channel-group … mode active`; otherwise it
  silently falls back to one link.

## Storage

- **Separate bulk NAS from host-local fast storage.** A NAS (Unraid, TrueNAS,
  Synology) holds ISOs, backups, and media; host-local NVMe/SSD holds running
  VM disks where latency matters.
- **Shared storage unlocks clustering.** vSAN, Ceph, or an NFS/iSCSI target is
  what lets VMs migrate between hosts — worth planning the network for
  (dedicated vMotion / vSAN VLANs) even before the second host arrives.
- **RAID level follows the data, not habit.** Mirrors for boot and latency-
  sensitive VM storage; parity (RAID-5/6, or Unraid's parity) for bulk where
  capacity and rebuild-tolerance beat IOPS.

## Power, cooling, and noise

- **Know the circuit.** Several enterprise servers plus a switch can approach a
  15 A circuit's safe continuous load. Measure real draw, don't trust
  nameplate.
- **Redundant PSUs, and a UPS.** Dual PSUs on separate outlets survive a
  tripped strip; a UPS rides out brownouts and lets hosts shut down cleanly.
- **Noise is a home constraint, not a data-center one.** 1U servers scream;
  location (basement, garage, closet with airflow) matters more than any spec.

## Rack and physical

- **A rack pays for itself in cable sanity.** Rack units, depth, a PDU, and
  consistent labeling (every port on the switch here carries a
  `rack-unit;role` description) turn "which cable is that" into a lookup.
- **Label at the switch and the host.** Interface descriptions that name the
  rack unit and NIC (`ru12;vmnic1`) are the single highest-value habit in this
  lab.

## Budget and sourcing

- **Used enterprise is the sweet spot** — decommissioned three-to-five-year-old
  gear from the refurb market or retired fleets. Accept the trade: little or no
  warranty, higher power draw, and firmware you may have to update yourself.
- **Buy for the plan, not the moment.** Enough DIMM slots, NIC ports, and
  switch ports to reach the *next* host, so the lab grows without a forklift.

## How these choices show up in this lab

Every principle above has a concrete consequence in the next chapter: enterprise
Dell compute with iDRAC, a single Nexus doing all the VLAN and LACP work, an
Unraid NAS for bulk, a dedicated management plane kept off the data VLANs, and a
labeled rack. Chapter 02 is the inventory; Chapter 03 draws it.
