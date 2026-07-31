# Volume CXIV — Nozomi Networks Build-It-Yourself Lab

> A build-it-yourself microsegmentation lab modeled on **Nozomi Networks**, whose distinctive strength is
> **deep protocol and process understanding**. Like a passive OT monitor it watches a mirror, but it
> dissects the industrial protocol down to the **function code** and the **process variable** — so it can
> segment at a granularity an L3/L4 firewall cannot express ("the operator may send Modbus *read* to the
> PLC but not *write*") and detect **process anomalies** ("a register value went outside its learned
> range") even on a permitted flow. The lab builds a minimal Modbus PLC and a **function-aware proxy**
> that permits reads, denies writes and non-Modbus, and flags out-of-range values — then shows the two
> events that L4 misses: a write **blocked** at the function level and a bad value **flagged** on an
> allowed read. Because Nozomi is commercial, this volume is **two-track**: Track 1 describes Guardian and
> Vantage at design level; **Track 2 is a fully buildable protocol-aware model** in Python + nftables.
> Nine chapters, ~22 walkthrough labs.

## Overview

Volume CXIV is a **hands-on lab volume** and the third of the OT-security tier. Where Claroty
([CXIII](../volume-113-claroty-xdome-lab/README.md)) segments from a flow baseline, Nozomi's contribution
is going **inside the protocol**: reading the Modbus function code and the register value, so policy can be
written per function and detection can fire on the process state itself. That is the difference between
"allow TCP/502" and "allow Modbus read, deny Modbus write, and alert if the value leaves 20–80".

The Track 2 model makes this concrete with a small Modbus-TCP server and a function-aware proxy, so the
read/write split and the value-range assertion are demonstrable on one host. The lab also draws the honest
line: Nozomi is passive and detects superbly, but **blocking a write needs an in-path OT-aware enforcer** —
which is exactly what the proxy stands in for, and what the next volume (TXOne) provides inline.

## Chapters

| Chapter | Title | Labs |
| --- | --- | --- |
| 01 | [Lab Overview and Topology](chapters/01-lab-overview-and-topology.md) | — |
| 02 | [Lab Preparation](chapters/02-lab-preparation.md) | 2.1–2.3 |
| 03 | [Network Graph and Protocol Identification](chapters/03-network-graph-and-protocol-id.md) | 3.1–3.2 |
| 04 | [Behavioral Baseline and the Dangerous Write](chapters/04-behavioral-baseline.md) | 4.1–4.3 |
| 05 | [Function-Aware Segmentation](chapters/05-function-aware-segmentation.md) | 5.1–5.2 |
| 06 | [Process Anomaly Detection](chapters/06-process-anomaly-detection.md) | 6.1–6.2 |
| 07 | [Enforcement and Verification](chapters/07-enforcement-and-verification.md) | 7.1–7.3 |
| 08 | [Vantage, Scale, and the Boundary](chapters/08-vantage-scale-and-boundary.md) | 8.1–8.3 |
| 09 | [Operations, Troubleshooting, and Teardown](chapters/09-operations-troubleshooting-teardown.md) | 9.1–9.3 |

## What you will be able to do

- Identify an OT protocol and its functions passively, not by port.
- Learn a process baseline (normal functions and value range).
- Enforce a function-aware policy: permit Modbus reads, deny writes and non-Modbus.
- Detect a process value outside its learned range on a permitted read.
- State the passive-plus-enforcer boundary and pair it with an inline OT IPS.

## Prerequisites

- **Track 1:** Nozomi Guardian + Vantage (commercial; covered at design level).
- **Track 2:** one Ubuntu 22.04 host with `python3`, `nftables`, and `iproute2` (fully buildable, no Nozomi software).

## See also

- [Volume CXIII — Claroty xDome](../volume-113-claroty-xdome-lab/README.md) — flow-baseline OT segmentation, a contrasting monitor model.
- [Volume CXII — Xage Security](../volume-112-xage-security-lab/README.md) — identity-brokered OT access.
- [Volume LXXXVII — Microsegmentation Options](../volume-087-microsegmentation-options/README.md) — the vendor-neutral decision guide this lab pairs with.
