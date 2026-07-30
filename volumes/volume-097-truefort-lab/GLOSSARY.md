# Volume XCVII Glossary

Definitions for terms introduced in **Volume XCVII — TrueFort Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Application baseline** — the recorded normal behavior of an application — which process, run by which account, connects to which peer on which port — from which least-privilege policy is authored.
- **Application-centric** — organizing policy around the application a set of workloads serves, and around its behavior, rather than around individual hosts or addresses.
- **auditd** — the Linux audit daemon; a native source of process and syscall telemetry that stands in for agent-reported behavior.
- **Behavioral baselining** — learning an application's normal behavior so deviations (a new process, a service account used from a new place) can be flagged.
- **Break-glass** — a pre-arranged recovery path when a policy locks you out: the out-of-band adapter, a revert to monitoring, a rule flush, or a snapshot restore.
- **EDR-leveraged** — sourcing telemetry from an endpoint detection and response agent (CrowdStrike, SentinelOne, Microsoft Defender for Endpoint) already deployed, so no new agent is required.
- **Identity-aware policy** — policy that permits a flow based on the process and account behind it, not only the source address and port.
- **nftables skuid owner match** — an `nftables` rule that matches the UID owning the local socket, used here to permit only the sanctioned service identity to egress to the database — the native analogue of binding a permission to a process identity.
- **PLC (Programmable Logic Controller)** — an industrial controller that runs no agent and emits no telemetry; protected from its managed neighbor rather than baselined directly.
- **Process attribution** — identifying the process (and user) behind a network connection, via `ss -tnp` on Linux; the signal that distinguishes the app from a webshell on the same host.
- **Service account** — a non-human identity an application uses to reach a resource (here `svc_app` for the database). Its theft and reuse is a common lateral-movement technique.
- **Service-account binding** — TrueFort's signature control: tying a service account's permitted use to the specific host and process identity that legitimately use it, so a stolen credential is denied elsewhere.
- **Service-account misuse** — a valid service credential presented from an illegitimate host or process; caught by identity-aware policy even though the password is correct.
- **tf-gw / tf-app01 / tf-db01 / tf-win01 / tf-ot01** — the lab's five virtual machines: router and OT enforcement point, nginx application tier, PostgreSQL database tier, Windows SCADA/HMI workload, and the agentless "PLC".
- **Track 1 / Track 2** — this volume's dual paths: Track 1 uses a real TrueFort Platform deployment; Track 2 reproduces enforcement natively and rebuilds the behavioral/identity signals from OS tooling.
- **VBS (Virtualization-Based Security)** — Windows security features, including Memory Integrity (HVCI), that run the Microsoft hypervisor beneath Windows and contend with VMware Workstation for VT-x.
- **WFP (Windows Filtering Platform)** — the Windows kernel filtering architecture; the firewall enforcement lands on in Track 2 on Windows.
