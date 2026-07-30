# Volume XCIV Glossary

Definitions for terms introduced in **Volume XCIV — Illumio Segmentation Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Break-glass** — a pre-arranged path or action that restores service when a policy locks you out: an out-of-band management route, a rule flush, a revert to Visibility Only, or a snapshot restore.
- **Choke point** — a link or device that all traffic to a segment must traverse, making it a valid place to enforce policy. If a device has a second path, policing one path polices nothing.
- **conntrack** — the Linux connection-tracking table; a source of live flow data that stands in for VEN-reported flow telemetry.
- **Draft / active policy** — Illumio keeps authored policy in a draft state until it is **provisioned**, at which point the PCE compiles and activates it. The split is a change-control gate between deciding and imposing policy.
- **Enforcement boundary** — the object that defines a **Selective Enforcement** scope: a specific service is enforced while all other traffic stays in visibility.
- **Enforcement state** — one of Idle, Visibility Only, Selective Enforcement, or Full Enforcement, set per workload to control how much of policy the VEN actually applies.
- **Full Enforcement** — the default-deny state in which only flows explicitly allowed by policy pass. In the native equivalent, the segmentation chain's base policy becomes `drop`.
- **il-gw / il-app01 / il-db01 / il-win01 / il-ot01** — the lab's five virtual machines: three-legged router and OT enforcement point, nginx application tier, PostgreSQL database tier, Windows SCADA/HMI workload, and the agentless "PLC".
- **Illumination** — Illumio's traffic map, which correlates VEN-reported flows into a visual graph used to discover dependencies before writing policy.
- **Label** — one of Illumio's four policy dimensions — **Role**, **Application**, **Environment**, **Location** — against which policy is written so that rules survive re-addressing and cloning.
- **Lateral movement** — an attacker reaching hosts beyond the initially compromised one; the specific harm a flat network permits and microsegmentation exists to contain.
- **Modbus TCP** — a widely used industrial control protocol, TCP port 502; the one flow permitted to the lab's PLC.
- **Named set** — an `nftables` collection of addresses referenced by rules; the native stand-in for an Illumio label, so policy survives membership changes.
- **NEN (Network Enforcement Node)** — an Illumio component that enforces policy by pushing ACLs to switches and load balancers, used for path-based control of assets that cannot host a VEN; emulated natively in this lab by the router's forward-chain rules.
- **PCE (Policy Compute Engine)** — Illumio's control plane and console; it holds labels and policy, correlates flows into Illumination, and compiles policy into per-workload rules. It never sits in the data path.
- **Pairing profile / pairing key** — the PCE object and one-time activation code used to install and register (pair) a VEN onto a workload.
- **PLC (Programmable Logic Controller)** — an industrial controller that typically cannot accept third-party software; the asset class the unmanaged-workload model exists to protect.
- **Provision** — the action of activating draft policy so the PCE compiles and distributes it to VENs.
- **Track 1 / Track 2** — this volume's dual paths: Track 1 uses a real Illumio PCE and VEN; Track 2 reproduces the same enforcement primitives natively with no PCE.
- **Unmanaged workload** — a device represented in the PCE without a VEN (an IP or IP list), whose protection is enforced by the managed workloads that communicate with it.
- **VBS (Virtualization-Based Security)** — Windows security features, including Memory Integrity (HVCI), that run the Microsoft hypervisor beneath Windows and so contend with VMware Workstation for VT-x.
- **VEN (Virtual Enforcement Node)** — the Illumio agent that programs the native OS firewall — `iptables`/`nftables` on Linux, the Windows Filtering Platform on Windows — and reports flows to the PCE, rather than supplying its own packet filter.
- **Visibility Only** — the enforcement state in which the VEN reports every flow but blocks nothing, used to validate policy before enforcing it.
- **WFP (Windows Filtering Platform)** — the Windows kernel filtering architecture the VEN programs on Windows hosts, reachable through `netsh advfirewall` and the `NetSecurity` PowerShell module.
