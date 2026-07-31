# Volume CXIII Glossary

Definitions for terms introduced in **Volume CXIII — Claroty xDome Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Baseline curation** — the human review step in which each learned flow is sanctioned or rejected before it becomes policy, keeping an attack observed during monitoring out of the enforced rules.
- **Collector** — a passive sensor placed on a SPAN/mirror that sees traffic without being inline; the source of discovery and baselining.
- **Communication baseline** — the learned matrix of which assets talk to which, on what protocol/port, over a monitoring window.
- **Deviation** — live traffic that departs from the baseline; raised as an anomaly whether or not an enforcer blocks it.
- **Enforcement via integration** — Claroty's model of pushing the derived policy to an external firewall, NAC, or switch, which does the blocking; xDome itself is passive.
- **Exposure management** — using the passively-built inventory (vendor/model/firmware) to map assets to known vulnerabilities and prioritize risk.
- **Observe-then-enforce** — the loop of discovering and baselining traffic, curating it, deriving a least-privilege policy, and enforcing it via an integrated device.
- **Purdue model** — the reference layering of OT (L0–L3+) that virtual zones and derived policies typically align to.
- **SPAN / mirror** — a switch feature that copies traffic to a monitoring port so a passive collector can see it.
- **Virtual zone** — a group of assets sharing a policy; the unit the derived segmentation policy is written between.
- **Track 1 / Track 2** — the two lab paths: the real xDome at design level (Track 1) and a buildable native observe-then-enforce model with `tcpdump` and nftables (Track 2).
