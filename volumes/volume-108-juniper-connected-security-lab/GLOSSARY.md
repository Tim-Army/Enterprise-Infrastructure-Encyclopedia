# Volume CVIII Glossary

Definitions for terms introduced in **Volume CVIII — Juniper Connected Security Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Address book** — the Junos collection of named addresses and address sets that security policies reference by name instead of by raw IP.
- **Application (Junos)** — the service a policy matches (port/protocol), e.g. `junos-postgresql`; scoping the application is what makes a zone policy microsegmentation rather than a coarse allow.
- **Connected Security** — Juniper's model in which central management and threat intelligence drive enforcement, including reactive containment of infected hosts via dynamic address groups.
- **Dynamic address group** — an address group whose membership is fed dynamically (by a feed, Policy Enforcer, or an operator); a standing policy that denies the group contains any member without a rule edit.
- **host-inbound-traffic** — the zone setting that permits traffic *to the SRX itself* (e.g. ping, ssh); zones deny even this by default, illustrating the default-deny posture.
- **Policy Enforcer** — the Junos component that connects Security Director to threat feeds (ATP Cloud, SecIntel) and pushes dynamic containment updates to the SRX estate.
- **Security Director** — Juniper's central manager for authoring and templating SRX security policy across many devices.
- **Security policy** — an ordered rule within a from-zone/to-zone context matching source/destination address and application, with a permit or deny action; first match wins, default is deny.
- **Security zone** — a named grouping of interfaces/segments; the SRX denies inter-zone traffic unless a policy permits it, and will not forward through an interface not in a zone.
- **Track 1 / Track 2** — the two lab paths: real vSRX/Junos (Track 1) and a native Linux/nftables zone model (Track 2).
- **vSRX** — the virtual SRX firewall (vSRX 3.0), used as the Track 1 enforcement point on a 60-day evaluation.
