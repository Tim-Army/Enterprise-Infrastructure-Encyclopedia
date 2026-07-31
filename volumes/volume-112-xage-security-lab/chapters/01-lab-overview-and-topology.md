# Chapter 01: Lab Overview and Topology

![Lab topology: Xage brokers every connection by identity. The Xage Fabric holds identities and access policy; each asset sits behind a broker and has no direct path. The web app's service identity svc-web is brokered to db:5432 and the operator op-hmi is brokered to a legacy Modbus plc:502; an attacker with no identity is denied at the broker.](../../../diagrams/volume-112-xage-security-lab/chapter-01-lab-topology.svg)

*Figure 1-1. Xage wraps each asset in an identity-checking broker: access is granted to a proven identity, not a network address, so a legacy PLC with no authentication of its own is reachable only by a granted, authenticated identity and an attacker is denied at the broker.*

## Learning Objectives

- State what this lab builds and how Xage segments OT by **identity-brokered access**, not by network location.
- Understand the **Xage Fabric** — a decentralized mesh of enforcement nodes with a tamper-resistant identity/policy store.
- Understand the two tracks — a design-level view of the real Xage Fabric, and a buildable native identity-broker model.
- Read the lab topology and the identity plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab modeled on **Xage Security**, whose approach to protecting operational technology (OT) is different from every firewall and fabric in the previous tier: instead of filtering packets by address, Xage places an **enforcement point in front of each protected asset** and **brokers every connection through an identity check** — so a legacy PLC that speaks unauthenticated Modbus is suddenly reachable only by a named, authenticated identity with an explicit policy grant. Policy and identity live in the **Xage Fabric**, a decentralized mesh of nodes backed by a tamper-resistant distributed store, so there is no single controller to compromise.

This matters because most OT is **brownfield**: devices that cannot be patched, cannot authenticate, and cannot defend themselves. Xage's model is to wrap them, not change them. Xage is a commercial platform without an open evaluation, so this volume is **two-track** with an honest split:

- **Track 1 — the real product (design level).** How the **Xage Fabric Manager**, enforcement nodes, identities, and access policies are configured in the real product, described accurately at the UI/architecture level.
- **Track 2 — a buildable native model.** One Linux host where an **identity-brokering proxy** in front of the PLC requires a valid identity token before forwarding to the device, with nftables ensuring the PLC is reachable *only* through the broker — a working reproduction of identity-brokered OT access.

### The moving parts

| Part | What it is | Xage construct |
|:---|:---|:---|
| **Enforcement point** | A node in front of a protected asset that brokers access | Xage Node / enforcement point |
| **Identity** | A named user, service, or device with credentials/MFA | Fabric identity |
| **Access policy** | Who (identity) may reach what (asset/service), brokered | Xage access policy |
| **Fabric** | The decentralized, tamper-resistant identity/policy mesh | Xage Fabric |
| **Broker session** | A per-connection, identity-checked, logged proxy session | Brokered access |

Two ideas carry the volume:

- **Access is by identity, brokered per connection.** Nothing reaches the asset directly; every session is authenticated, authorized, and recorded — even to a device that has no security of its own.
- **The fabric is decentralized.** Policy and identity are distributed and tamper-resistant, so there is no central controller whose compromise unlocks the estate.

### Topology

```text
                     +---------------------------+
                     |  Xage Fabric              |  identities + access policy
                     |  (decentralized nodes)    |  tamper-resistant store
                     +-------------+-------------+
                                   | policy
             +---------------------+---------------------+
      IT  [broker] web -> db:5432          OT  [broker] hmi -> plc:502
        +-----+        +----+                  +-----+        +-----+
        | web | =====> | db |                  | hmi | =====> | plc |
        +-----+ (ident)+----+                  +-----+ (ident)+-----+
                                                             ^  no direct path;
      X  attacker -> plc:502 (no identity, denied at broker) +  broker-only
```

Every arrow passes an enforcement point that checks identity before forwarding. The PLC has **no direct network path** — it is reachable only through its broker, which denies anyone without a valid identity.

### The identity and access plan

| Asset | Address | Reachable only by (identity) | Service |
|:---|:---|:---|:---|
| db | 10.60.1.20 | `svc-web` (the web app) | 5432 |
| plc | 10.60.9.40 (isolated OT cell) | `op-hmi` (an authenticated operator) | 502 |

The attacker — any source without a valid identity — is denied at the broker, even for the legacy PLC that has no authentication of its own.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Design-level steps on the real Xage Fabric (UI/architecture) |
| **Track 2** | Buildable steps on the native identity-broker model |
| `xage>` | Xage Fabric Manager action (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Cleanup**.

## Summary and Completion Checklist

- [ ] Identity-brokered access (vs address filtering) understood.
- [ ] The decentralized Xage Fabric and brownfield-OT protection internalized.
- [ ] Track chosen (Track 2 is the buildable one).
- [ ] Topology and identity plan read.
