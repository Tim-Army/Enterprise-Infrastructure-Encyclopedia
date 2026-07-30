# Volume XCIX Glossary

Definitions for terms introduced in **Volume XCIX — Tempered Airwall Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Airwall Agent** — the on-host component that gives a device a cryptographic identity and an encrypted overlay tunnel; reproduced in Track 2 by WireGuard on the host.
- **Airwall Conductor** — Airwall's orchestration console, where overlay networks and trust are defined and identities are issued, licensed, and revoked; reproduced in Track 2 by the hub configuration and forward policy on `aw-gw`.
- **Airwall Gateway** — an appliance placed in front of a device that can run no agent; it holds the identity and tunnel on the device's behalf and carries it onto the overlay. In Track 2, `aw-gw` plays this role for the PLC.
- **aw-gw / aw-app01 / aw-db01 / aw-win01 / aw-ot01** — the lab's five virtual machines: router, overlay hub, and gateway; nginx application tier; PostgreSQL database; Windows SCADA/HMI workload; and the agentless "PLC".
- **Break-glass** — a pre-arranged recovery path when the overlay or cloaking locks you out: the out-of-band underlay management adapter, dropping the overlay, or a snapshot restore.
- **Cloaking** — making a protected device dark on the underlay: it does not respond to anything off the overlay, so it is invisible and unaddressable. In Track 2, a host firewall that drops all non-WireGuard underlay traffic.
- **Cryptographic identity** — a device's identity expressed as a key (a WireGuard public key), used to authorize connections instead of an IP address.
- **HIP (Host Identity Protocol)** — the protocol Airwall is built on, which identifies hosts by cryptographic identity rather than IP and underpins the encrypted overlay.
- **Overlay hub** — the central node all overlay traffic routes through (here `aw-gw`), where trust policy is enforced.
- **Overlay network / trust policy** — the definition of which identities may communicate; microsegmentation in Airwall is expressed as overlay membership, not firewall rules.
- **PLC (Programmable Logic Controller)** — an industrial controller that can hold no identity of its own; carried onto the overlay by an Airwall Gateway.
- **Track 1 / Track 2** — this volume's dual paths: Track 1 uses a real Airwall deployment (Conductor, Agents, Gateways); Track 2 builds a genuine encrypted overlay with WireGuard.
- **Underlay** — the ordinary IP network (the VMware segments) beneath the overlay; after cloaking, protected devices are dark on it.
- **VBS (Virtualization-Based Security)** — Windows security features, including Memory Integrity (HVCI), that run the Microsoft hypervisor beneath Windows and contend with VMware Workstation for VT-x.
- **WireGuard** — the open-source encrypted-tunnel technology used in Track 2 as a faithful stand-in for the Airwall HIP overlay: public-key identities, always-on encryption, default-deny, and silent cloaking.
