# Volume CXVII Glossary

Definitions for terms introduced in **Volume CXVII — Cisco ACI Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **APIC** — the Application Policy Infrastructure Controller, the single point of configuration for an ACI Nexus 9000 fabric.
- **Bridge domain (BD)** — the Layer 2 forwarding domain an EPG attaches to; multiple EPGs can share a BD, and ACI still enforces contracts between them.
- **Contract** — the policy object that permits traffic between two EPGs; it carries subjects and filters (protocol/port) and is provided by one EPG and consumed by another.
- **Endpoint Group (EPG)** — a group of endpoints sharing policy; the unit contracts are written between.
- **Intra-EPG isolation** — an EPG setting that denies traffic between members of the same EPG, closing the peer-to-peer lateral path.
- **Provide / consume** — the contract relationship: the provider EPG offers a service and the consumer EPG uses it.
- **Service graph** — an ACI construct that inserts a service device (firewall/IPS) into a contract's traffic path for deeper inspection.
- **uSeg EPG (micro-EPG)** — an EPG whose membership is determined by attribute (IP, MAC, VM property), enabling attribute-based micro-segmentation and quarantine independent of the base EPG.
- **Whitelist model** — ACI's default that traffic between EPGs is denied unless a contract permits it.
- **Track 1 / Track 2** — the two lab paths: the real APIC/ACI at design level (Track 1) and a buildable EPG/contract model in nftables (Track 2).
