# Volume CIX Glossary

Definitions for terms introduced in **Volume CIX — Fortinet ISFW and VDOM Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Address object** — a named host/subnet in FortiOS (`config firewall address`) referenced by policies so rules read by name, not raw IP.
- **Automation stitch** — a FortiOS trigger-action rule (`config system automation-stitch`) that runs an action, such as quarantining a compromised host, when an event fires.
- **Custom service** — a named port/protocol (`config firewall service custom`), e.g. PGSQL=tcp/5432, MODBUS=tcp/502, used to scope a policy to a specific application.
- **Firewall policy** — an ordered FortiOS rule matching srcintf/dstintf, srcaddr/dstaddr, and service with an accept/deny action; first match wins, followed by an implicit deny.
- **Implicit deny** — the built-in final drop after the last policy; anything not explicitly permitted is denied, giving default-deny east-west once an ISFW is in the path.
- **Inter-VDOM link** — an internal link pair connecting two VDOMs so that specifically permitted traffic can cross between otherwise-isolated virtual firewalls.
- **ISFW (Internal Segmentation Firewall)** — the pattern of deploying a FortiGate inside the network to enforce east-west policy, not just at the perimeter.
- **Security Fabric** — Fortinet's architecture linking FortiGates and other Fortinet devices for shared objects, topology, telemetry, and coordinated enforcement across an estate.
- **VDOM (Virtual Domain)** — an independent virtual firewall within one FortiGate, with its own interfaces, routing, and policies; VDOMs have no path between them except an explicit inter-VDOM link.
- **Zone (system zone)** — a named group of interfaces (`config system zone`) so policies reference a role; an interface belongs to exactly one zone.
- **Track 1 / Track 2** — the two lab paths: real FortiGate-VM/FortiOS (Track 1) and a native Linux/nftables zone-and-table model (Track 2).
