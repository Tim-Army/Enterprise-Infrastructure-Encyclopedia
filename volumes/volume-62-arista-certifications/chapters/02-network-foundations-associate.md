# Chapter 02: Network Foundations — Associate

## Learning Objectives

- Explain what the Network Foundations (Associate) certifies.
- Navigate EOS and manage configuration.
- Configure switching (VLANs, trunks) and interfaces.
- Configure IP routing and protocols.
- Complete a walkthrough for each foundations topic.

## Theory and Architecture

The **Network Foundations Track** leads to the **ACE Associate (Level 1)** — the
foundational credential validating core Arista/EOS knowledge: **EOS fundamentals** (the
CLI, config model, single-image OS, SysDB), **switching** (VLANs, trunking, MLAG basics),
**interfaces**, and **IP routing** (static and dynamic — OSPF/BGP fundamentals). EOS uses
a familiar industry-standard CLI, so the skills transfer, while its Linux underpinnings and
programmability differentiate it. This is the entry point required before the Specialist
tracks.

## Design Considerations

Learn the **EOS config model** (running vs startup, `show running-config`, sessions),
segment with **VLANs/trunks**, and route with **OSPF/BGP**. Understand that EOS is one
image across platforms and exposes state via SysDB — the basis for its telemetry and
automation.

## Implementation and Automation

The labs use the EOS CLI for config, switching, interfaces, and routing.

## Validation and Troubleshooting

Confirm the topics:

```text
Associate (Network Foundations): EOS fundamentals (CLI/config/SysDB); switching (VLANs/trunks/MLAG);
interfaces; IP routing (static, OSPF, BGP fundamentals).
```

Common pitfalls: forgetting to **save** (`copy running-config startup-config`); and access
ports where trunks are needed.

## Security and Best Practices

Use **config sessions** for safe changes, save to **startup-config**, segment with
**VLANs**, and secure management (AAA, SSH). Verify with `show` commands before and after.

## Hands-On Lab

Foundations walkthroughs. **Shared prerequisites** — a cEOS/vEOS switch (containerlab) with
CLI access. **Cost:** none.

### Lab 2.1 — Navigate EOS and view config

**Objective:** Inspect the running configuration.

```text
switch> enable
switch# show running-config | section interface
switch# show version | include Software image
```

**Expected result:** the interface config and EOS image version — EOS fundamentals.

**Negative test:** edit `startup-config` directly expecting it to be live; changes apply to
**running-config** — configure there, then save.

**Cleanup:** none (read-only).

### Lab 2.2 — Create a VLAN and access port

**Objective:** Configure switching.

```text
switch# configure
switch(config)# vlan 100
switch(config-vlan-100)# name users
switch(config)# interface Ethernet1
switch(config-if-Et1)# switchport access vlan 100
switch(config)# end
switch# show vlan 100
```

**Expected result:** VLAN 100 with Ethernet1 as an access port — layer-2 segmentation.

**Negative test:** put a multi-VLAN uplink on an access port; use a **trunk**
(`switchport mode trunk`) for multiple VLANs.

**Cleanup:** `configure; no vlan 100`.

### Lab 2.3 — Configure a trunk

**Objective:** Carry multiple VLANs on an uplink.

```text
switch(config)# interface Ethernet2
switch(config-if-Et2)# switchport mode trunk
switch(config-if-Et2)# switchport trunk allowed vlan 100,200
switch# show interfaces Ethernet2 switchport
```

**Expected result:** Ethernet2 as a **trunk** allowing VLANs 100 and 200 — inter-switch
transport.

**Negative test:** allow **all** VLANs on every trunk; **prune** to needed VLANs to limit
broadcast/scope.

**Cleanup:** `default interface Ethernet2`.

### Lab 2.4 — IP routing with OSPF

**Objective:** Enable dynamic routing.

```text
switch(config)# interface Ethernet3
switch(config-if-Et3)# no switchport
switch(config-if-Et3)# ip address 10.0.3.1/30
switch(config)# router ospf 1
switch(config-router-ospf)# network 10.0.3.0/30 area 0
switch# show ip ospf neighbor
```

**Expected result:** an OSPF process with the interface in area 0 (neighbors when peered) —
dynamic routing.

**Negative test:** static-route a large dynamic topology; **OSPF/BGP** adapts to changes —
use dynamic routing at scale.

**Cleanup:** `no router ospf 1`.

### Lab 2.5 — Save the configuration

**Objective:** Persist changes.

```text
switch# copy running-config startup-config
switch# show startup-config | include vlan 100
```

**Expected result:** the config saved to **startup-config** — persistent across reload.

**Negative test:** reload without saving; changes are **lost** — copy to startup-config.

**Cleanup:** none.

## Lab Verification

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The Network Foundations (Associate) certifies core EOS skills: the config model and CLI,
switching (VLANs/trunks), interfaces, and IP routing (OSPF/BGP fundamentals). This chapter
configured switching, a trunk, OSPF, and saved the config.

- [ ] I can navigate EOS and view config.
- [ ] I can configure VLANs and access/trunk ports.
- [ ] I can enable dynamic routing (OSPF).
- [ ] I can save configuration to startup-config.
- [ ] I completed Labs 2.1–2.5 including each negative test.
