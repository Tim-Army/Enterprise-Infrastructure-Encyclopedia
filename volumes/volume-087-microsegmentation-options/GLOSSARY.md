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
- **Air-gapped deployment** — an installation with no connectivity to external networks; requires on-premises control planes and offline update paths.
- **CMVP (Cryptographic Module Validation Program)** — the NIST program that issues FIPS 140 certificates to specific cryptographic modules and versions. A certificate number is the only evidence of validation.
- **DPU (Data Processing Unit)** — a programmable processor on a NIC or switch that runs enforcement outside the host's trust domain, so policy survives host compromise.
- **FedRAMP "In Process"** — a Marketplace state indicating an authorization is being pursued. It is **not** authorization and permits no federal use.
- **HIP (Host Identity Protocol)** — the identity-based protocol underlying Tempered Airwall's encrypted overlay, which makes protected devices unaddressable rather than merely filtered.
- **IdentityGraph** — Elisity's aggregated view of each asset's identity and behavior, enriched from directory, EDR, and CMDB sources, used to drive policy.
- **MSS-Group** — Arista's Multi-Domain Segmentation Service group policy, enforced on EOS switches and managed through CloudVision.
- **SGACL (Security Group ACL)** — the Cisco TrustSec construct that enforces group-to-group permissions at the egress device.
- **SGT (Security Group Tag)** — the tag Cisco ISE assigns at authentication, carried inline or by SXP and enforced by SGACLs.
- **SPIFFE / SPIRE** — a standard workload-identity format (`spiffe://…`) and its reference issuing system, enabling cryptographic rather than address-based policy.
- **SXP** — the TrustSec protocol that carries IP-to-SGT bindings out of band where switches cannot tag inline; subject to per-node binding limits.
- **Visibility platform vs enforcement platform** — in OT, the distinction between products that map assets and flows (Nozomi, Claroty) and products that constrain traffic (Xage, TXOne, Zscaler/Airgap).
- **Designated country** — a country with a qualifying trade agreement with the United States; TAA permits federal purchase of articles made or substantially transformed there.
- **GSA MAS (Multiple Award Schedule)** — the principal federal purchasing vehicle. For most software security vendors the contract is held by a reseller, with the vendor listed only as manufacturer.
- **Substantial transformation** — the TAA test by which an article becomes a new and different article of commerce, with a distinct name, character, or use, in the country where the work was done.
- **TAA (Trade Agreements Act of 1979)** — the statute governing federal procurement of foreign goods. Compliance is determined **per SKU** and evidenced by a manufacturer's TAA letter or Certificate of Origin, not by a marketing claim.
