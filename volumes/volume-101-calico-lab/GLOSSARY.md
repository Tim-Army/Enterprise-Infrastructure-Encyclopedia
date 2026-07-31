# Volume CI Glossary

Definitions for terms introduced in **Volume CI — Calico Build-It-Yourself Lab**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **calicoctl** — Calico's CLI, used for resources `kubectl` does not manage as first-class objects: `GlobalNetworkPolicy`, `Tier`, `HostEndpoint`, and `NetworkSet`.
- **Calico** — an open-source Kubernetes CNI and network-policy engine that enforces Kubernetes NetworkPolicy and its own richer policy, in an iptables or eBPF dataplane.
- **Default-deny** — a NetworkPolicy that selects pods (`podSelector: {}`) and names a policy type with no rules, denying all traffic of that type until explicit allows are added; the floor segmentation builds on.
- **Failsafe ports** — the ports Calico always permits to and from a node (SSH, DNS, the Kubernetes API, BGP, etcd) so that a HostEndpoint policy cannot lock you out of the node.
- **GlobalNetworkPolicy** — a Calico policy that is cluster-wide (not namespaced) and can express an explicit `Deny` and rule order, unlike Kubernetes NetworkPolicy.
- **HostEndpoint** — a Calico object that applies policy to a node's own interfaces, extending segmentation from pods to the host itself.
- **kind** — "Kubernetes in Docker"; a tool that runs a full Kubernetes cluster as containers on one host, used here to build the lab cluster.
- **Label selector** — the mechanism by which Kubernetes and Calico policy selects pods (for example `app == 'web'`); the durable alternative to pod IPs, which are ephemeral.
- **Namespace** — a Kubernetes organizational boundary that, by default, does **not** isolate network traffic; isolation requires a NetworkPolicy.
- **NetworkPolicy (Kubernetes)** — the standard, namespaced, allow-only policy object Calico enforces; the portable starting point for segmentation.
- **NetworkSet / GlobalNetworkSet** — a named group of external IPs/CIDRs that Calico policy can select on, used to govern flows to endpoints outside the cluster.
- **PLC (Programmable Logic Controller)** — the unpatchable OT device; in Kubernetes, its analog is an endpoint outside the cluster, governed by a NetworkSet.
- **Single-track** — this volume has no "Track 2" because Calico is open source; every command runs the real enforcement engine.
- **Tier** — an ordered group of Calico policies; higher-order tiers (for example a `security` tier) evaluate before the default tier, letting a platform team set guardrails app teams cannot override.
