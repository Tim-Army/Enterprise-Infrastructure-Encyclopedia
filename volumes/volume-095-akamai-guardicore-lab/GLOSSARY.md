# Volume XCV Glossary

Definitions for terms introduced in **Volume XCV — Akamai Guardicore Segmentation Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Agent (Guardicore)** — the software on each managed workload that reports flows with process and user context and programs the native OS firewall — `iptables`/`nftables` on Linux, the Windows Filtering Platform on Windows.
- **Aggregator / Collector** — Centra components that gather and correlate flow telemetry from agents (and optional network collectors) into the Reveal map.
- **Alert-only** — a policy posture in which a rule reports what it *would* block without blocking, used to validate policy before enforcing it.
- **Allow / block / alert rule** — the ordered rule types in a Guardicore policy: permit a flow, deny it, or raise an alert. Order matters — a block placed ahead of broad allows enforces first.
- **Break-glass** — a pre-arranged path or action that restores service when a policy locks you out: an out-of-band management route, a rule flush, a revert to alert-only, or a snapshot restore.
- **Centra** — Guardicore's control plane: a Management server plus Aggregators and Collectors. It holds labels and policy and never sits in the data path.
- **Choke point** — a link or device that all traffic to a segment must traverse, making it a valid place to enforce and observe policy.
- **conntrack** — the Linux connection-tracking table; a source of live flow data that stands in for agent-reported telemetry.
- **Deception (dynamic)** — a Guardicore capability that redirects a suspicious connection to a decoy so the attacker's next move is observed rather than served; especially high-value on a single-flow OT segment.
- **Enforcement** — the state in which a Guardicore policy actually blocks. In the native equivalent, the segmentation chain's base policy becomes `drop`.
- **gc-gw / gc-app01 / gc-db01 / gc-win01 / gc-ot01** — the lab's five virtual machines: three-legged router and OT enforcement point, nginx application tier, PostgreSQL database tier, Windows SCADA/HMI workload, and the agentless "PLC".
- **Label** — a free-form key/value pair (for example `Role: Web`, `Environment: Dev`) that Guardicore policy references so rules survive re-addressing and cloning.
- **Lateral movement** — an attacker reaching hosts beyond the initially compromised one; the harm a flat network permits and microsegmentation contains.
- **Modbus TCP** — an industrial control protocol, TCP port 502; the one flow permitted to the lab's PLC.
- **Named set** — an `nftables` collection of addresses referenced by rules; the native stand-in for a Guardicore labeled group.
- **Process/user context** — the identity of the process and user behind a flow, reported by the Guardicore agent and shown in Reveal; it lets a rule name the software, not just the host.
- **Process-scoped policy** — a rule that permits only a named process (not "any process on the host") to make a flow, narrowing trust to the software that earned it.
- **Reveal** — Guardicore's flow map, drawn from agent telemetry with process and user context, used to discover dependencies before writing policy.
- **Ring-fence** — a coarse first boundary that permits traffic within a group of related assets and denies ingress from outside, applied before per-service rules.
- **Track 1 / Track 2** — this volume's dual paths: Track 1 uses a real Guardicore Centra environment and agent; Track 2 reproduces the same enforcement primitives natively with no Centra.
- **VBS (Virtualization-Based Security)** — Windows security features, including Memory Integrity (HVCI), that run the Microsoft hypervisor beneath Windows and contend with VMware Workstation for VT-x.
- **WFP (Windows Filtering Platform)** — the Windows kernel filtering architecture the Guardicore agent programs on Windows hosts.
