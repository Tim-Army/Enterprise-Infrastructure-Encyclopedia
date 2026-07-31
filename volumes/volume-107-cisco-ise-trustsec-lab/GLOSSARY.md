# Volume CVII Glossary

Definitions for terms introduced in **Volume CVII — Cisco ISE and TrustSec Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **CMD (Cisco Meta Data)** — the Layer 2 field into which a TrustSec-capable device inserts the SGT for **inline** propagation; requires supporting ASICs, which is why this lab uses SXP instead.
- **CTS (Cisco TrustSec)** — Cisco's group-based segmentation architecture: classify endpoints into Security Groups, propagate the tag, and enforce SGACLs in the network.
- **Egress policy matrix** — the grid of SGACLs indexed by *(source SGT row, destination SGT column)*; the cell holds the ACL applied when the row-group sends to the column-group, and the default cell sets the fail-open/closed posture.
- **Enforcement (role-based)** — the switch feature (`cts role-based enforcement`) that actually applies matrix SGACLs; separate from downloading policy, so policy can exist without being enforced.
- **Environment data** — the SGT name/number table and related metadata a NAD downloads from ISE; must reach `state COMPLETE` before enforcement works.
- **IP-SGT mapping** — a static binding of an IP address to an SGT, authored in ISE; the simplest reproducible way to assign a tag, used throughout this lab.
- **ISE (Identity Services Engine)** — Cisco's policy engine: it defines Security Groups and SGACLs, holds the egress matrix, and distributes bindings via SXP.
- **Monitor mode** — a rollout mode (`cts role-based monitor`) in which the enforcer reports would-be drops without dropping, so a matrix can be validated before it can cause an outage.
- **NAD (Network Access Device)** — the switch/router that enforces TrustSec; registered with ISE over RADIUS with CTS credentials.
- **SGACL (Security Group ACL)** — an access list keyed on source and destination SGT rather than IP; ends in `deny ip` for microsegmentation so only named ports pass.
- **SGT (Security Group Tag)** — a 16-bit tag naming an endpoint's group (WEB=10, DB=20, HMI=30, PLC=40 here); the identity TrustSec policy is written against.
- **SXP (SGT Exchange Protocol)** — the protocol that distributes IP-SGT *bindings* to devices that cannot read inline tags; directional (speaker/listener).
- **Track 1 / Track 2** — the two lab paths: real ISE + IOS-XE (Track 1) and a native Linux/nftables model of bindings and the tag matrix (Track 2).
- **Unknown (SGT 0)** — the group for endpoints with no binding; the default matrix row for Unknown must be a deliberate permit/deny decision.
