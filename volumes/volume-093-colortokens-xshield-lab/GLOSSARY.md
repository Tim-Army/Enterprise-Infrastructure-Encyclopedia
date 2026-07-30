# Volume XCIII Glossary

Definitions for terms introduced in **Volume XCIII — ColorTokens Xshield Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Agentless enforcement** — policy applied in the network path rather than on the protected device, for assets that cannot host an agent.
- **Break-glass** — a pre-arranged path or action that restores service when a policy locks you out: an out-of-band management route, a rule flush, a snapshot revert, or a fall back to Observe mode.
- **Choke point** — a link or device that all traffic to a segment must traverse, making it a valid place to enforce policy. If a device has a second path, policing one path polices nothing.
- **conntrack** — the Linux connection-tracking table; a source of live flow data that stands in for agent-reported flow telemetry.
- **ct-gw / ct-app01 / ct-db01 / ct-win01 / ct-ot01** — the lab's five virtual machines: three-legged router and Gatekeeper-equivalent, nginx application tier, PostgreSQL database tier, Windows SCADA/HMI workload, and the agentless "PLC".
- **Default-deny** — a policy whose base action is to drop, so only explicitly permitted flows pass. Enforced here on the router's `forward` chain, which polices transit rather than local traffic.
- **Design Exercise** — an exercise that cannot be reproduced without the commercial product or a licensed dependency, written as analysis with a model answer rather than simulated clicking.
- **EDR-mediated enforcement** — Xshield enforcing through an endpoint-detection agent already present (CrowdStrike, SentinelOne, Microsoft Defender for Endpoint) instead of adding a new agent.
- **Enforce mode** — the state in which policy actually blocks. In the native equivalent, the segmentation chain's trailing action becomes `drop`.
- **Gatekeeper** — the Xshield agentless appliance (data-center VM or shop-floor hardware) that becomes the default gateway for devices it protects, so all their traffic traverses it.
- **HMI (Human-Machine Interface)** — the operator workstation that supervises industrial equipment; here `ct-win01`, whose only legitimate east-west relationship is polling the PLC.
- **Host agent** — the Xshield agent that programs the native OS firewall — `iptables`/`nftables` on Linux, the Windows Filtering Platform on Windows — rather than supplying its own packet filter.
- **Lateral movement** — an attacker reaching hosts beyond the initially compromised one; the specific harm a flat network permits and microsegmentation exists to contain.
- **Modbus TCP** — a widely used industrial control protocol, TCP port 502; the one flow permitted to the lab's PLC.
- **Named set** — an `nftables` collection of addresses referenced by rules; the native stand-in for an Xshield tag or group, so policy survives membership changes.
- **Observe mode (simulate)** — the state in which policy reports what it *would* block without blocking, used to validate a policy before enforcing it.
- **PLC (Programmable Logic Controller)** — an industrial controller that typically cannot accept third-party software; the asset class the Gatekeeper exists to protect.
- **Product Key** — the per-tenant identifier embedded in an Xshield agent installer's file name and used during installation; obtained from the console's Agent Download page.
- **Progressive Segmentation** — ColorTokens' staged method: discover, visualize, ring-fence, then tighten — always moving through Observe before Enforce.
- **Ring-fence** — a coarse first boundary that permits traffic within a group of related assets and denies ingress from outside, applied before per-service rules.
- **Track 1 / Track 2** — this volume's dual paths: Track 1 uses a real Xshield tenant and console; Track 2 reproduces the same enforcement primitives natively with no tenant.
- **ULM (User Level Monitor)** — the reduced-performance mode VMware Workstation falls back to when the Microsoft hypervisor holds VT-x, reached through the Windows Hypervisor Platform API.
- **VBS (Virtualization-Based Security)** — Windows security features, including Memory Integrity (HVCI), that run the Microsoft hypervisor beneath Windows and so contend with Workstation for VT-x.
- **WFP (Windows Filtering Platform)** — the Windows kernel filtering architecture the Xshield agent programs on Windows hosts, reachable through `netsh advfirewall` and the `NetSecurity` PowerShell module.
- **Xshield AI Agent** — a ColorTokens capability introduced March 2026 that proposes policy from observed flows; treat its output as a draft to review, not to apply blind.
