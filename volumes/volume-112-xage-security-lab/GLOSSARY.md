# Volume CXII Glossary

Definitions for terms introduced in **Volume CXII — Xage Security Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Access policy** — a grant binding an identity to a specific asset and service; the broker forwards only when the presented identity matches a grant.
- **Broker session** — a per-connection, identity-authenticated, logged proxy from a caller to an asset; nothing reaches the asset except through it.
- **Brownfield OT** — existing operational-technology devices that cannot be patched, cannot authenticate, and cannot defend themselves; the target Xage wraps rather than changes.
- **Decentralized fabric** — the Xage architecture in which identity and policy are replicated across nodes in a tamper-resistant store, so there is no single controller whose breach unlocks the estate and nodes keep enforcing if the manager is offline.
- **Enforcement point (node)** — a Xage node placed in the path to an asset (or as the only route into an OT cell) that brokers access by identity.
- **Identity** — the unit of Xage policy: a named user, service, or device with credentials (and MFA for humans), proven per connection.
- **Isolation** — removing every direct network path to an asset so it is reachable only through its broker; brokering and isolation together are one control.
- **Xage Fabric** — the decentralized mesh of nodes and the tamper-resistant identity/policy store that backs it.
- **Track 1 / Track 2** — the two lab paths: the real Xage Fabric at design level (Track 1) and a buildable native identity-broker model with `socat` and nftables (Track 2).
