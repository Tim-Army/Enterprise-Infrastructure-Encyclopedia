# Volume CXV Glossary

Definitions for terms introduced in **Volume CXV — TXOne Networks Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Application lockdown** — StellarProtect's mode in which only allowlisted (by hash) applications may execute on the host; everything else is blocked.
- **Bump-in-the-wire** — a device cabled inline that inspects traffic transparently at Layer 2, without any device changing its IP or configuration.
- **Command filtering** — inline OT-protocol allow-listing that permits safe commands (read/status) and denies dangerous ones (write/stop/firmware) even from a trusted source.
- **EdgeIPS / EdgeFire** — TXOne's inline OT intrusion-prevention system and OT firewall, deployed transparently in front of a cell.
- **StellarProtect** — TXOne's OT endpoint protection that enforces application lockdown on hosts such as engineering workstations.
- **Transparent inline** — deployment in which the protective device sits in the traffic path but is invisible to the endpoints (no re-addressing), so it can be inserted into a live plant.
- **Trust list** — an inline allow-list of the sources permitted to reach a protected device; untrusted sources are dropped regardless of payload.
- **Virtual patching** — an IPS signature on the inline device that blocks a known exploit for an unpatchable device, putting the fix in the network rather than the device.
- **Track 1 / Track 2** — the two lab paths: the real TXOne EdgeIPS/EdgeFire/StellarProtect at design level (Track 1) and a buildable inline model — transparent redirect, signature inspector, and application-lockdown launcher (Track 2).
