# Volume CXXVI — Glossary

| Term | Definition |
|:---|:---|
| **ACE** | Aviatrix Certified Engineer — the certification program: Associate (free), Professional, Design Expert, plus focused courses (Security, Hybrid Cloud, Cloud Backbone, Automation, Operations). |
| **ACE Associate** | The free, self-paced foundational credential on multicloud networking across AWS/Azure/GCP/OCI; the mandatory prerequisite for ACE Professional. |
| **ACE Professional** | The instructor-led, hands-on credential (3 days) on multicloud transit/HA, egress, firewall insertion, and connectivity; requires the Associate plus ~1 year of cloud experience. |
| **ACE Design Expert** | The capstone credential on designing scalable, resilient multicloud networks. |
| **Active-active HA** | Aviatrix's high-availability model where both gateways in a pair forward traffic (ECMP), not active-standby — scaling throughput and failing over fast. |
| **Controller** | Aviatrix's central control plane: deploys and orchestrates gateways, programs routing/policy across all clouds, and handles overlapping-CIDR NAT. |
| **CoPilot** | Aviatrix's observability/operations plane: topology maps, FlowIQ flow visibility, analytics, alerting, and compliance views across clouds. |
| **Distributed Cloud Firewall (DCF)** | Aviatrix's distributed, tag/group-based segmentation enforced in the gateways across the fabric, without hairpinning to a central appliance. |
| **Egress control** | Filtering outbound (internet-bound) traffic at the gateway, ideally by FQDN, to prevent unrestricted egress and exfiltration. |
| **FireNet** | Firewall Network Service — Aviatrix's transparent insertion of third-party NGFWs (Palo Alto, Fortinet, Check Point) into the traffic path for deep inspection. |
| **FQDN filtering** | Egress allowlisting by fully-qualified domain name rather than IP, so rules survive the IP rotation of cloud/SaaS services. |
| **FlowIQ** | CoPilot's flow-analytics feature: per-flow records aggregated into topology, throughput/latency analytics, and security alerts. |
| **Gateway** | The Aviatrix data-plane instance deployed into a VPC/VNet, taking transit, spoke, egress, firewall, or VPN roles. |
| **Network domain** | A transit-level segmentation grouping of spokes; only allowed domain pairs may communicate, isolating (e.g.) prod from dev. |
| **Overlay** | The Aviatrix software network layered over cloud-native constructs, giving consistent transit, encryption, egress, segmentation, and visibility across clouds. |
| **Site2Cloud** | Aviatrix's IPsec connectivity from on-premises/branch sites to cloud gateways, with route exchange and overlapping-CIDR NAT. |
| **Spoke** | A workload VPC/VNet attached to the transit backbone via a spoke gateway. |
| **Transit** | The multicloud backbone formed by peered Aviatrix transit gateways, carrying any-to-any spoke traffic through a hub (O(1) to add a spoke). |
| **User VPN** | Aviatrix's OpenVPN-based remote-user access with SAML/MFA and per-user policy, typically split-tunneled to cloud CIDRs. |
