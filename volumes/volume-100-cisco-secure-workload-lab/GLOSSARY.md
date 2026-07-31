# Volume C Glossary

Definitions for terms introduced in **Volume C — Cisco Secure Workload Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Agent (Secure Workload)** — the software on each managed workload that reports comprehensive flow and process telemetry and enforces policy by programming the native host firewall (`iptables`/`ipset` on Linux, WFP on Windows).
- **Application Dependency Mapping (ADM)** — the analysis that clusters workloads into tiers from their flow patterns, discovers the application's dependencies, and generates a least-privilege policy.
- **Auto-generated policy** — the least-privilege policy ADM produces from discovered dependencies, reviewed by a human before enforcement.
- **Break-glass** — a pre-arranged recovery path when a policy locks you out: the out-of-band adapter, a revert to analysis (non-enforced), a chain flush, or a snapshot restore.
- **Cluster** — Secure Workload's control plane (an on-premises appliance or SaaS tenant) that ingests telemetry, runs ADM, holds scopes and policy, and performs policy analysis.
- **conntrack** — the Linux connection-tracking table; the native source of the flow telemetry ADM consumes.
- **cw-gw / cw-app01 / cw-db01 / cw-win01 / cw-ot01** — the lab's five virtual machines: router and OT enforcement point, nginx application tier, PostgreSQL database tier, Windows SCADA/HMI workload, and the agentless "PLC".
- **ipset** — a Linux facility for efficient address groups referenced by `iptables`; the native stand-in for the agent's grouped enforcement, so membership changes without rewriting rules.
- **Policy analysis (what-if)** — replaying real (live and historical) flows against a candidate policy to see exactly what it would allow and deny, before enforcing it.
- **PLC (Programmable Logic Controller)** — an industrial controller that runs no agent; protected from its managed neighbor rather than directly.
- **Scope** — a hierarchical grouping of workloads used to organize the estate and delegate policy authoring per team or tier.
- **Telemetry** — the comprehensive flow and process data agents report, from which ADM discovers the application and policy analysis evaluates candidate rules.
- **Track 1 / Track 2** — this volume's dual paths: Track 1 uses a real Secure Workload cluster and agents; Track 2 reproduces telemetry, ADM, analysis, and enforcement natively.
- **VBS (Virtualization-Based Security)** — Windows security features, including Memory Integrity (HVCI), that run the Microsoft hypervisor beneath Windows and contend with VMware Workstation for VT-x.
- **WFP (Windows Filtering Platform)** — the Windows kernel filtering architecture the Secure Workload agent programs on Windows hosts.
