# Volume LXXXVII Glossary

Definitions for terms introduced in **Volume LXXXVII — Microsegmentation Options**.
See the [master glossary](../../GLOSSARY.md) for cross-volume terms.

- **Agentless microsegmentation** — enforcement without installing an agent on the workload (via the hypervisor, network fabric, an inline appliance, or by remotely programming the host's built-in firewall).
- **Application security group (ASG)** — an Azure construct that groups VMs for use as a source/destination in NSG rules, tag-like rather than IP-based.
- **Calico** — a Kubernetes CNI providing NetworkPolicy plus cluster-wide GlobalNetworkPolicy and WireGuard encryption.
- **Cilium** — an eBPF-based Kubernetes CNI providing identity-aware L3–L7 policy and the Hubble observability layer.
- **Contract (Cisco ACI)** — an allowlist policy that permits traffic between Endpoint Groups; without one, inter-EPG traffic is denied.
- **Distributed Firewall (DFW)** — VMware NSX's per-vNIC stateful firewall enforced in the hypervisor kernel.
- **East-west traffic** — traffic between workloads inside a network (as opposed to north-south perimeter traffic).
- **eBPF** — a Linux kernel technology Cilium uses to enforce and observe network policy efficiently.
- **Endpoint Group (EPG)** — a Cisco ACI grouping of workloads to which contract-based policy is applied.
- **Gatekeeper** — ColorTokens' agentless appliance that acts as the default gateway to segment OT/IoT/legacy devices that cannot run an agent.
- **Lateral movement** — an attacker's east-west progression from an initial foothold toward valuable systems.
- **Microsegmentation** — enforcing least-privilege network policy between individual workloads to contain lateral movement.
- **Multi-factor segmentation** — Zero Networks' network-layer MFA that keeps privileged ports closed until a second factor opens them just-in-time.
- **NetworkPolicy** — the built-in Kubernetes object that allows pod-to-pod traffic by label selector, enforced by the CNI.
- **PCE / VEN (Illumio)** — the Policy Compute Engine (controller) and Virtual Enforcement Node (workload agent) of Illumio.
- **Ring-fencing** — isolating a group of assets (a flat or high-risk zone) behind a segmentation boundary.
- **Security group** — an AWS stateful, instance-level allowlist of permitted traffic.
- **Xshield** — ColorTokens' microsegmentation platform spanning host-agent, EDR, cloud, Kubernetes, and Gatekeeper enforcement.
