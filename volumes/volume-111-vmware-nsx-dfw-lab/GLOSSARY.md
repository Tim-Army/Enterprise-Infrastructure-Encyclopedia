# Volume CXI Glossary

Definitions for terms introduced in **Volume CXI — VMware NSX Distributed Firewall Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Applied To** — the DFW rule field that scopes where a rule is programmed (e.g. only the destination group's vNICs), controlling enforcement placement and scale.
- **Context profile** — an NSX profile adding Layer 7 matching (App-ID, FQDN) to a rule, so policy can require a specific application, not just a port.
- **Default rule** — the DFW catch-all layer-3 rule; set to Drop for zero-trust so anything not explicitly permitted is denied.
- **Distributed Firewall (DFW)** — NSX firewalling enforced in the hypervisor kernel at each VM's vNIC, filtering east-west traffic (including same-subnet, same-host) without a chokepoint.
- **Dynamic group** — an NSX group whose membership is computed from criteria (security tag, VM name, OS), so rules follow workloads automatically.
- **Identity Firewall** — NSX matching of AD/Entra user or group identity in a rule, adding *who* to the policy.
- **Security tag** — a label applied to a VM that group membership criteria consume; tagging a VM grants it its place in the policy.
- **Transport node** — an ESXi host prepared with the NSX kernel modules so the DFW enforces on its VMs; rules do nothing on an unprepared host.
- **vNIC enforcement** — the property that the rule is applied at the workload's own virtual interface, which is why DFW can filter a same-subnet peer.
- **vsipioctl getrules** — the host CLI that shows the DFW rules actually programmed at a given vNIC filter — the ground truth for what is enforced.
- **Track 1 / Track 2** — the two lab paths: real NSX Manager + ESXi (Track 1) and a native model where each namespace enforces its own nftables ruleset (Track 2).
