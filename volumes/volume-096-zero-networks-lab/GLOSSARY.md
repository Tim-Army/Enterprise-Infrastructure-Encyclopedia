# Volume XCVI Glossary

Definitions for terms introduced in **Volume XCVI — Zero Networks Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Agentless** — an enforcement model that installs no software on the protected host. Zero Networks enforces by remotely programming each host's own firewall (Windows Firewall over RPC, Linux over SSH), so the enforcement artifact is the native OS firewall.
- **Allow-list (learned)** — the least-privilege rule set derived automatically from observed traffic during the monitoring/learning phase.
- **Break-glass** — a pre-arranged recovery path when a policy locks you out: the out-of-band management adapter, a revert to monitoring, a rule flush, or a snapshot restore. With just-in-time access, break-glass is planned around the console or host, not a standing admin port.
- **Choke point** — a link or device all traffic to a segment must traverse, making it a valid enforcement point.
- **conntrack** — the Linux connection-tracking table; the source of observed flow data used to learn the allow-list.
- **Enforcement (Protected)** — the state in which the host's firewall default-denies and permits only the reviewed least-privilege rules.
- **Just-in-time (JIT) access** — administrative access that is closed by default and opened only for a specific source and a bounded time window after an authenticated request.
- **Just-in-time MFA** — Zero Networks' signature control: privileged ports (RDP, SSH, WinRM, SMB) are opened per-session only after multi-factor authentication, then closed automatically.
- **Learning phase (monitoring)** — the period (~30 days in production) during which the platform observes traffic without enforcing, to derive least-privilege rules.
- **Least privilege** — a policy that permits only the flows a host actually needs, defined by observed behavior rather than by guesswork.
- **nftables timeout set** — an `nftables` set whose elements auto-expire; used here to build a just-in-time grant that revokes itself, the native equivalent of a time-boxed MFA session.
- **PLC (Programmable Logic Controller)** — an industrial controller that exposes no manageable host firewall; protected from its managed neighbor rather than directly.
- **Privileged ports** — administrative protocols (RDP 3389, SSH 22, WinRM, SMB) that are the most abused lateral-movement paths and are gated behind just-in-time MFA.
- **Service account (privileged reach)** — the account Zero Networks uses to reach and program each host's firewall management interface; agentless still requires privileged reach.
- **Track 1 / Track 2** — this volume's dual paths: Track 1 uses a real Zero Networks deployment; Track 2 programs the same native firewalls the platform writes, with a `timeout`-based JIT grant.
- **VBS (Virtualization-Based Security)** — Windows security features, including Memory Integrity (HVCI), that run the Microsoft hypervisor beneath Windows and contend with VMware Workstation for VT-x.
- **WFP (Windows Filtering Platform)** — the Windows kernel filtering architecture; the firewall Zero Networks programs on Windows hosts, and the one you program by hand in Track 2.
