# Volume CXVIII Glossary

Definitions for terms introduced in **Volume CXVIII — Arista MSS-Group Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **CloudVision** — Arista's management and telemetry platform where security groups and MSS/MSS-Group policy are defined and pushed to the EOS fabric.
- **EOS** — Arista's switch operating system; MSS-Group policy is enforced in the switch ASIC at line rate.
- **Firewall redirect** — the MSS macro-segmentation action of steering a selected inter-group flow through an inserted firewall for inspection, then returning it, with no endpoint change.
- **Group policy** — an MSS-Group rule permitting traffic between a source and destination security group with an L4 match; the default between groups is deny.
- **MSS (Macro-Segmentation Service)** — Arista's segmentation that inserts a firewall into the path of selected flows by redirect (service insertion).
- **MSS-Group** — Arista's micro-segmentation: group-to-group policy enforced directly in the fabric.
- **Security group** — a group of endpoints sharing policy, populated by subnet/VLAN/interface/identity; the unit MSS policy is written between.
- **Service insertion** — steering traffic through a service device (firewall/IPS) via the fabric rather than by re-cabling endpoints.
- **Track 1 / Track 2** — the two lab paths: EOS/CloudVision at design level (Track 1) and a buildable group-policy + firewall-redirect model in nftables (Track 2).
