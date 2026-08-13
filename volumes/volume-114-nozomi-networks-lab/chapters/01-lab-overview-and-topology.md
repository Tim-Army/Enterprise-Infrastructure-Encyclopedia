# Chapter 01: Lab Overview and Topology

![Lab topology: Nozomi Guardian passively dissects Modbus to the function code and baselines the process; a function-aware enforcer between the hmi operator and the plc (:502) permits Modbus reads, denies writes and non-Modbus, and flags a register value outside its learned range of 20-80 as a process anomaly even on a permitted read.](../../../diagrams/volume-114-nozomi-networks-lab/chapter-01-lab-topology.svg)

*Figure 1-1. Nozomi segments inside the protocol: the enforcer permits Modbus reads but denies writes and non-Modbus — a distinction no L4 firewall can make — while the learned process baseline flags a register value that falls outside its normal range even on an allowed read.*

## Learning Objectives

- State what this lab builds and how Nozomi segments OT at the **protocol and function** level, not just port.
- Understand passive deep-protocol analysis, the learned **network graph**, and **process-behavioral** baselining.
- Understand the two tracks — a design view of Nozomi Guardian/Vantage, and a buildable protocol-aware model.
- Read the lab topology and the protocol-policy plan.

## How to Use This Guide

### What this lab is

This is a build-it-yourself microsegmentation lab modeled on **Nozomi Networks**, whose strength is **deep protocol and process understanding**. Like Claroty, Nozomi is passive — a **Guardian** sensor watches a mirror and a **Vantage** SaaS aggregates — but its distinctive contribution is that it does not stop at "who talks to whom on which port." It dissects the **industrial protocol** (Modbus, DNP3, S7, and many more) down to the **function** and even the **process variable**, and it **baselines the behavior of the process itself** — so it can say not just "the HMI talks Modbus to the PLC" but "the HMI *reads* holding registers from the PLC, and it has never *written* them" and "register 40001 has always been between 20 and 80."

That enables a kind of segmentation the L3/L4 firewalls of the earlier tiers cannot express: **function-aware policy** ("HMI may send Modbus *read* to the PLC but not *write*") and **process-anomaly detection** ("a write arrived, or a value went out of its learned range"). Nozomi is a commercial platform, so this volume is **two-track**:

- **Track 1 — the real product (design level).** How Guardian learns the network graph and process baseline from a SPAN, and how policy and alerts are managed in Vantage, described accurately at the architecture level.
- **Track 2 — a buildable protocol-aware model.** One Linux host with a minimal Modbus-TCP server and a **function-aware proxy** that inspects the Modbus function code, permits reads, denies writes, and flags out-of-range values — a working reproduction of protocol- and process-aware OT segmentation.

### The moving parts

| Part | What it is | Nozomi construct |
|:---|:---|:---|
| **Guardian sensor** | Passive deep-protocol network sensor | Guardian on a SPAN |
| **Network graph** | Learned nodes, links, and protocols | Guardian network view |
| **Process baseline** | Learned normal function usage and variable ranges | Behavioral learning |
| **Protocol-aware policy** | Allow by protocol *and function*, not just port | Segmentation / assertion |
| **Vantage** | SaaS aggregation, alerting, management | Nozomi Vantage |

Two ideas carry the volume:

- **Segment by function, not just port.** "Modbus read allowed, Modbus write denied" is a control an L4 firewall cannot express — it needs protocol awareness.
- **Baseline the process, not just the flows.** A value out of its learned range is an incident even when the flow itself is permitted.

### Topology

```text
                     +--------------------------+
                     |  Nozomi Guardian/Vantage |  network graph + process
                     |  (passive deep-protocol) |  baseline + alerts
                     +------------+-------------+
              SPAN (passive)      | policy / assertions
                                  v
        +----------------- function-aware enforcer -----------------------+
        |  hmi 10.80.1.30  ==Modbus READ==>  plc 10.80.1.40 :502          |
        |                   X  Modbus WRITE (denied) ,  X non-Modbus       |
        |                   !  register out of learned range (anomaly)     |
        +-----------------------------------------------------------------+
   allowed:  hmi -> plc Modbus READ (fc 3/4)
   denied:   hmi -> plc Modbus WRITE (fc 6/16) ,  any non-Modbus to plc
   anomaly:  a read/write value outside the learned range
```

### The protocol-policy plan

| Flow | Protocol | Function | Decision |
|:---|:---|:---|:---|
| hmi → plc | Modbus/TCP 502 | Read (fc 3/4) | **Allow** |
| hmi → plc | Modbus/TCP 502 | Write (fc 6/16) | **Deny** |
| any → plc | non-Modbus | — | **Deny** |
| hmi → plc | Modbus read/write | value out of learned range | **Allow flow, raise anomaly** |

The lab permits only Modbus *reads* from the operator to the controller, denies writes and non-Modbus, and flags process values that fall outside the learned range.

## Conventions

| Convention | Meaning |
|:---|:---|
| **Track 1** | Design-level steps on real Nozomi Guardian/Vantage |
| **Track 2** | Buildable steps on the native protocol-aware model |
| `nozomi>` | Guardian/Vantage action (orientation only) |
| `bash` block | Bare commands; output follows on the next line |

Every exercise follows the same shape: **Objective**, **Walkthrough** (per track), **Expected result**, **Negative test**, **Rollback**.

## Summary and Completion Checklist

- [ ] Protocol- and function-aware segmentation (vs L4-only) understood.
- [ ] Process-behavioral baselining internalized.
- [ ] Track chosen (Track 2 is the buildable one).
- [ ] Topology and protocol-policy plan read.
