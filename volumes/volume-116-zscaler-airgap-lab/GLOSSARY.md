# Volume CXVI Glossary

Definitions for terms introduced in **Volume CXVI — Zscaler/Airgap Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Agentless isolation** — segmentation achieved without installing software on endpoints, by controlling the network layer (ARP/DHCP) rather than the hosts.
- **ARP/DHCP control** — the mechanism by which the Airgap enforcement point makes itself every device's only resolvable neighbor and hands out host-scoped routes, so no device can reach another directly.
- **Enforcement point** — the device all east-west traffic is forced through, where zero-trust policy and the kill switch are applied.
- **Kill switch** — a single control that instantly drops all east-west traffic across the protected VLAN for total containment during an incident.
- **Network of one** — the state in which each device is isolated so its only neighbor is the enforcement point, leaving no direct path between any two endpoints even on the same subnet.
- **Sanctioned flow** — an east-west connection explicitly permitted by policy (here `web -> db:5432`); everything else is denied by default.
- **Zero Trust Exchange (ZTE)** — Zscaler's cloud-delivered platform for identity-based, per-application north-south access (ZTNA), pairing with Airgap's east-west isolation.
- **Track 1 / Track 2** — the two lab paths: the real Zscaler/Airgap at design level (Track 1) and a buildable agentless-isolation model with `/32` host views and an nftables enforcer (Track 2).
