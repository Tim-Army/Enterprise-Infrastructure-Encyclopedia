# Volume LXXIII Glossary

Definitions for terms introduced in **Volume LXXIII — Check Point Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **CCSA (Certified Security Administrator)** — Check Point's foundational credential (exam 156-215.82 on R82) covering Gaia, policy, NAT, blades, and monitoring.
- **CCSE (Certified Security Expert)** — Check Point's advanced credential (exam 156-315.82) covering upgrades, ClusterXL, VPN, acceleration, and troubleshooting.
- **CCSM / CCSM Elite** — Certified Security Master (and Elite), earned by accumulating Infinity Specialist Accreditations after CCSE; CCSM is valid two years.
- **CCTE (Certified Troubleshooting Expert)** — Check Point's diagnostics credential (exam 156-588) covering fw monitor, kernel debug, and cpview.
- **clish** — Gaia's structured command-line shell (`set`/`show`/`save config`) for persistent configuration.
- **CloudGuard** — Check Point's cloud security family (network security, posture management/CSPM, and workload protection) for AWS/Azure/GCP.
- **ClusterXL** — Check Point's clustering for high availability and load sharing, using a virtual IP and synchronized connection state for transparent failover.
- **CoreXL** — a performance technology that spreads firewall inspection across multiple CPU cores via multiple firewall instances.
- **cpview** — Gaia's live statistics tool (CPU, memory, connections, throughput, blade stats).
- **fw monitor** — a packet capture tool showing traffic at four inspection points (i/I/o/O) to pinpoint where a packet is dropped or translated.
- **Gaia** — Check Point's hardened operating system for gateways and management, managed by clish, the Gaia Portal, and expert mode.
- **Harmony** — Check Point's user and access security family (endpoint, email/collaboration, browse, SASE).
- **Identity Awareness** — a Software Blade that maps traffic to users/groups (via AD, captive portal, or agents) so policy rules reference identities.
- **Infinity Specialist Accreditation (ISA)** — a focused Check Point accreditation on a product/topic (CloudGuard, Harmony, Maestro, VSX, automation) that builds toward CCSM.
- **Install Policy** — the action that compiles the rule base and pushes it to gateways so changes take effect.
- **Maestro** — Check Point's hyperscale orchestration that bundles many appliances into one elastic logical gateway (Security Group).
- **Management API / mgmt_cli** — the programmable interface (and CLI) for every SmartConsole operation: login → change → publish → install-policy.
- **NAT (Automatic / Manual)** — address translation configured automatically on objects (Hide/Static) or explicitly via manual NAT rules.
- **Quantum** — Check Point's network-security platform: Security Gateway (enforcement) plus Security Management Server (policy/logs).
- **R82** — the current Check Point software release under which the CCSA/CCSE/CCTE exams are versioned.
- **SecureXL** — a performance technology that accelerates established connections on a fast path, offloading the firewall.
- **Security Gateway** — the Check Point enforcement point that inspects and controls traffic per the installed policy.
- **Security Management Server** — the central server that stores policy, objects, and logs and pushes policy to gateways.
- **SIC (Secure Internal Communication)** — the certificate-based trust between the management server and gateways that secures their communication.
- **SmartConsole** — the Check Point administrator GUI client for building policy, managing objects, and reading logs.
- **Software Blade** — a modular security function on a gateway (IPS, Application Control, URL Filtering, Identity Awareness, Threat Prevention).
- **Threat Prevention** — the blades (IPS, Anti-Bot, Anti-Virus, Threat Emulation/Extraction) governed by profiles that move Detect → Prevent after tuning.
- **VSX (Virtual System Extension)** — a technology that runs many virtual gateways, each with its own policy, on one physical appliance.
