# Volume LXII Glossary

Definitions for terms introduced in **Volume LXII — Arista Certification Tracks**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **ACE (Arista Certified Engineer)** — Arista's certification program, revised 1 June 2025 into a tiered Learning Track model (Associate → Specialist → Professional).
- **Anycast gateway** — a distributed default gateway where every leaf shares the same gateway IP/MAC for a subnet, so hosts route at their local VTEP; configured via EVPN IRB.
- **Arista Academy** — Arista's training portal (training.arista.com) hosting the ACE learning tracks, courses, and exams.
- **AVD (Arista Validated Designs)** — an Ansible collection that generates and deploys complete, validated leaf-spine/EVPN fabrics from a concise data model.
- **cEOS / vEOS** — containerized (cEOS) and virtual-machine (vEOS) EOS images used for free lab practice, e.g., in containerlab.
- **Change Control** — CloudVision's governed deployment workflow: stage → snapshot → review/approve → execute, with automatic rollback on failure.
- **CloudVision (CVP)** — Arista's single management plane for provisioning, streaming telemetry, change control, and services across data center, campus, and WAN.
- **Configlet** — a static EOS configuration snippet assigned to devices in CloudVision (the legacy provisioning model, largely superseded by Studios).
- **eAPI** — EOS's JSON-RPC API (over HTTP/HTTPS at `/command-api`) for running CLI commands programmatically and receiving structured JSON.
- **EOS (Extensible Operating System)** — Arista's Linux-based network OS with a single binary image, streaming state, and full programmability.
- **EVPN (Ethernet VPN)** — the BGP control plane (address family `l2vpn evpn`) that distributes MAC/IP reachability for VXLAN overlays.
- **IRB (Integrated Routing and Bridging)** — routing between VXLAN segments at the VTEP, enabling the anycast gateway for inter-subnet traffic.
- **L3VPN** — MPLS Layer-3 VPN using MP-BGP (VPNv4) and per-customer VRFs over an MPLS core.
- **LDP (Label Distribution Protocol)** — distributes MPLS labels between core routers to build label-switched paths.
- **MLAG (Multi-Chassis Link Aggregation)** — two EOS switches presenting a single logical LAG to a downstream device for active-active redundancy without spanning-tree blocking.
- **MSS (Macro-Segmentation Service)** — CloudVision's service for inserting firewalls/segmentation policy across the fabric.
- **pyeapi** — Arista's Python client library for eAPI.
- **Studios** — CloudVision's modern, workflow-driven, abstracted provisioning model that generates device configs from a data-driven model (preferred over per-device configlets).
- **VLAN / trunk** — a Layer-2 broadcast domain (VLAN) and a port carrying multiple tagged VLANs (802.1Q trunk).
- **VTEP (VXLAN Tunnel Endpoint)** — the switch interface (a VXLAN-enabled SVI/loopback) that encapsulates/decapsulates VXLAN traffic.
- **VXLAN (VNI)** — MAC-in-UDP overlay encapsulation; each Layer-2 segment maps to a VXLAN Network Identifier (VNI).
