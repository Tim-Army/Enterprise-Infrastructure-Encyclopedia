# Chapter 01: Lab Overview and Topology

![Lab topology: TXOne EdgeIPS inline (transparent bump-in-the-wire) in front of an unpatchable PLC, applying a virtual patch, trust list, and command filter without changing the PLC's IP. The operator's sanctioned Modbus read passes; the attacker's exploit and untrusted traffic are dropped inline, shielding the PLC without patching it. StellarProtect locks the engineering host to an application allowlist, blocking a malware binary.](../../../diagrams/volume-115-txone-networks-lab/chapter-01-lab-topology.svg)

*Figure 1-1. TXOne blocks inline where the passive monitors only detect: a transparent EdgeIPS virtual-patches an unpatchable PLC — dropping the exploit at the wire without touching the device — while StellarProtect application-lockdown blocks unapproved software on the engineering host.*

## Learning Objectives

- State what this lab builds and how TXOne protects OT **inline and transparently** — the enforcement the passive monitors delegate.
- Understand **virtual patching**, **protocol trust lists**, and **StellarProtect endpoint lockdown**.
- Understand the two tracks — a design view of EdgeIPS/EdgeFire and StellarProtect, and a buildable inline model.
- Read the lab topology and the protection plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab modeled on **TXOne Networks**, the OT-security vendor whose products *block* rather than merely observe. Where Claroty and Nozomi are passive and delegate enforcement, TXOne's **EdgeIPS** and **EdgeFire** sit **inline** as a **transparent bump-in-the-wire** — dropped in front of an OT cell **without changing any IP or topology** — and enforce OT-aware policy, including **virtual patching**: IPS signatures that shield an unpatchable device from a known exploit without touching the device. On the endpoint, **StellarProtect** locks an OT host down to an **application allowlist**, so only approved software runs. Together they cover the network *and* the host.

The theme of this volume is **enforcement for the unpatchable**: OT devices that cannot be fixed are protected by a transparent inline shield and by locking down the machines around them. TXOne is a commercial platform, so this volume is **two-track**:

- **Track 1 — the real product (design level).** How EdgeIPS/EdgeFire are inserted transparently, how virtual-patch signatures and trust lists are managed, and how StellarProtect enforces application lockdown, described accurately.
- **Track 2 — a buildable inline model.** One Linux host where a **transparent inline filter** shields a vulnerable "PLC" from an exploit signature and enforces a trust list, and an **application-allowlist** wrapper models endpoint lockdown — a working reproduction of inline OT protection.

### The moving parts

| Part | What it is | TXOne construct |
|:---|:---|:---|
| **Transparent inline device** | Bump-in-the-wire IPS/firewall, no IP change | EdgeIPS / EdgeFire |
| **Virtual patch** | An IPS signature that blocks an exploit for an unpatchable device | EdgeIPS virtual patching |
| **Protocol trust list** | Allow only sanctioned sources/commands inline | EdgeIPS/EdgeFire policy |
| **Application lockdown** | Only approved binaries run on the host | StellarProtect |

Two ideas carry the volume:

- **Protect what you cannot patch.** A transparent inline shield blocks the exploit even though the device stays vulnerable.
- **Network and endpoint together.** Inline IPS guards the wire; application lockdown guards the host — OT needs both.

### Topology

```text
   operator                 transparent inline               unpatchable OT
   +-----+   ==Modbus==>   +---------------------+   ==>   +-------------------+
   | hmi |                 |  TXOne EdgeIPS      |         | plc :502          |
   +-----+                 |  (bump-in-the-wire) |         | vulnerable, cannot|
                           |  virtual patch +    |         | be patched        |
   +-----+   X exploit --> |  trust list         | --X-->  +-------------------+
   | atk |  (blocked inline)+---------------------+
   +-----+
                           +------------------------------+
                           |  ews (engineering host)      |  StellarProtect:
                           |  only approved binaries run   |  application lockdown
                           +------------------------------+
   allowed:  hmi -> plc sanctioned Modbus
   blocked:  known exploit signature (virtual patch) , untrusted source , unapproved binary on ews
```

### The protection plan

| Target | Threat | TXOne control |
|:---|:---|:---|
| plc (unpatchable) | known exploit signature | **Virtual patch** (inline IPS drops it) |
| plc | untrusted source / bad command | **Trust list** (inline allow-list) |
| ews (OT host) | unauthorized/malware binary | **Application lockdown** (StellarProtect) |

The lab shields the vulnerable PLC from an exploit **without patching it**, restricts who may reach it, and locks the engineering host to approved software.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Design-level steps on real EdgeIPS/EdgeFire/StellarProtect |
| **Track 2** | Buildable steps on the native inline model |
| `txone>` | EdgeIPS/StellarProtect action (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Rollback**.

## Summary and Completion Checklist

- [ ] Transparent inline protection and virtual patching understood.
- [ ] Network (IPS/trust list) plus endpoint (lockdown) coverage internalized.
- [ ] Track chosen (Track 2 is the buildable one).
- [ ] Topology and protection plan read.
