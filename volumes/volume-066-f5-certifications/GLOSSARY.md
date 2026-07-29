# Volume LXVI Glossary

Definitions for terms introduced in **Volume LXVI — F5 Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Advanced WAF (ASM)** — BIG-IP Application Security Manager, F5's web application firewall (attack signatures + positive security + bot defense).
- **APM** — BIG-IP Access Policy Manager, F5's access and identity gateway (authentication, SSO, ZTNA, VPN).
- **AS3 (Application Services 3)** — the declarative JSON extension that defines BIG-IP applications idempotently via iControl REST.
- **BIG-IP** — F5's application delivery and security platform, running the TMOS operating system.
- **DO (Declarative Onboarding)** — the Automation Toolchain component that declares base system config (VLANs, self-IPs, HA).
- **F5-CA** — F5 Certified Administrator, BIG-IP; the foundation credential, rebuilt in 2025 into five exams (F5CAB1–F5CAB5).
- **F5-CTS** — F5 Certified Technology Specialist; the specialization level (LTM, DNS, Advanced WAF/ASM, APM).
- **F5-CSE** — F5 Certified Solution Expert (Security, exam 401); the top level, integrating the modules.
- **Full proxy** — BIG-IP's architecture of terminating the client connection and originating a separate server connection, enabling inspection and manipulation.
- **GSLB (Global Server Load Balancing)** — load balancing across sites at the DNS layer, provided by BIG-IP DNS/GTM.
- **iControl REST** — BIG-IP's REST API (`/mgmt/tm/...`) returning structured JSON.
- **iRules** — event-driven Tcl scripts that inspect and act on traffic on the BIG-IP.
- **LTM** — BIG-IP Local Traffic Manager, F5's core load balancer / application delivery controller.
- **Monitor** — a health check (ICMP/TCP/HTTP/HTTPS) that marks pool members up or down.
- **OneConnect** — an LTM profile that reuses server-side connections to reduce backend load.
- **Persistence** — keeping a client's session on the same pool member (cookie, source-address, SSL, universal).
- **Pool / pool member** — a group of backend servers (pool) and the individual servers (members) behind a virtual server.
- **qkview / iHealth** — a diagnostic snapshot (qkview) uploaded to F5 iHealth for automated analysis.
- **self-IP** — the BIG-IP's own IP address on a VLAN.
- **SNAT** — Source/Secure NAT; replaces the client source IP with a BIG-IP address for return-path symmetry.
- **TMOS** — Traffic Management Operating System, the OS of BIG-IP, with its TMM data-plane microkernel.
- **tmsh** — the BIG-IP Traffic Management Shell (CLI).
- **UCS** — User Configuration Set; a BIG-IP configuration backup archive.
- **Virtual server** — a BIG-IP listener (IP:port) that receives client traffic and applies policy.
- **Wide IP** — a BIG-IP DNS name mapped to GSLB pools for global load balancing.
