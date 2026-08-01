# Volume CXIX Glossary

Definitions for terms introduced in **Volume CXIX — HPE Aruba CX 10000 Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Connection tracking (conntrack)** — tracking the state of each connection so that return and related traffic is permitted by state; what the CX 10000's DPU does in hardware and Track 2 reproduces with nftables.
- **CX 10000 distributed services switch** — the Aruba top-of-rack switch with an embedded DPU that runs stateful services (firewall, NAT, telemetry) for east-west traffic at line rate.
- **DPU (Data Processing Unit)** — the AMD Pensando processor embedded in the CX 10000 that offloads stateful services from the CPU and applies them at line rate.
- **established/related** — the connection states whose traffic is auto-permitted by a stateful firewall, so a reply needs no separate reverse rule.
- **Per-flow telemetry** — the DPU's inline visibility into every east-west connection (who, what, how long), available without a separate SPAN/tap.
- **PSM / Aruba Fabric Composer** — the Pensando Policy and Services Manager and Aruba management plane that author stateful policy and collect telemetry across the CX 10000 fleet.
- **Stateful firewall** — enforcement that tracks connection state, permitting replies by state and dropping unsolicited/invalid packets, stronger than a stateless L3/L4 ACL.
- **Stateless ACL** — a fixed 5-tuple permit that must open the reverse direction to allow replies, leaving an inbound hole a stateful firewall closes.
- **Track 1 / Track 2** — the two lab paths: the CX 10000/PSM at design level (Track 1) and a buildable stateful (conntrack) model in nftables (Track 2).
