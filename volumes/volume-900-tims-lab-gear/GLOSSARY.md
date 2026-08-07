# Volume CM Glossary

Definitions for terms used in **Volume CM — Tim's Lab Gear**, alphabetized. See
also the [volume index](INDEX.md) for pointers to where each term is used, and
the [master glossary](../../GLOSSARY.md) for cross-volume terminology.

**BOSS (Boot Optimized Storage Solution)** — A Dell add-in card holding one or
two small M.2 SATA devices, typically mirrored, dedicated to the hypervisor
boot volume so it is separate from bulk data storage.

**Bond (Linux bond)** — A logical interface aggregating two or more physical
NICs. In `802.3ad` (LACP) mode it provides link redundancy and aggregate
throughput, and requires a matching port-channel on the switch.

**iDRAC (integrated Dell Remote Access Controller)** — Dell's out-of-band
management processor, providing remote console, power control, and virtual
media independent of the host operating system.

**LACP (Link Aggregation Control Protocol, IEEE 802.3ad)** — The protocol two
devices use to negotiate a bonded link. Both ends must run it; on Cisco NX-OS
the switch ports use `channel-group N mode active`.

**Native VLAN** — The VLAN a trunk carries untagged. Best practice is a
dedicated, otherwise-unused VLAN (here, 999) so tagged data never rides an
untagged path.

**NX-OS** — Cisco's operating system for Nexus switches. This lab's
`nexus-9k-1` runs `7.0(3)I2(2d)`.

**OOB (out-of-band) management** — A management network physically or logically
separate from the data network, so devices stay reachable when a data VLAN
fails. Here it is the `10.30.99.0/24` segment carrying the switch `mgmt0` and
the iDRACs.

**port-channel** — Cisco's term for a bonded/aggregated switch link (the
switch-side counterpart to a host bond).

**Proxmox VE** — The open-source virtualization platform running on
`proxmox-1`; combines KVM virtual machines and LXC containers with a web UI.

**Rack unit (RU / U)** — One 1.75-inch vertical slot in a 19-inch rack; hosts
here are identified by their rack unit (`ru08`–`ru12`).

**Trunk** — A switch port carrying multiple VLANs, tagged, with one native
(untagged) VLAN.

**Unraid** — The NAS operating system on `unraid-1`, providing bulk storage
with parity protection.

**VLAN (Virtual LAN)** — An isolated Layer-2 broadcast domain identified by a
tag. This lab's plan is recorded in Chapter 02.

**vmbr (virtual machine bridge)** — A Proxmox Linux bridge that connects VMs to
a physical NIC, bond, or VLAN. `vmbr0` is management; `vmbr1` is the VLAN-aware
trunk bridge.
