# Chapter 11: FortiSwitch Feature, Version, and SRG Map

## Learning Objectives

- Find which FortiSwitchOS releases list a given FortiSwitch feature.
- Map each FortiSwitch feature to the DISA SRG requirement it helps satisfy.
- Use the map to scope an SRG-based assessment of a FortiSwitch, which has no
  STIG of its own.
- Tell the difference between a feature that *implements* an SRG requirement
  and one that only needs to be disabled when unused.
- Account for FortiLink-managed switches, where evidence is collected on the
  FortiGate.

## Theory and Architecture

FortiSwitch has **no DISA STIG** (Chapter 10). A FortiSwitch in a DoD
environment is therefore assessed directly against the SRGs that match its
functions, as Chapter 03 describes. This chapter gives the two pieces of
information that assessment needs for every FortiSwitch feature: **which
FortiSwitchOS releases support it**, and **which SRG requirement it relates
to**.

### Where the version data comes from

Fortinet publishes a **Feature Matrix** for FortiSwitchOS releases, listing every
feature and which FortiSwitch model series support it. The version column in
this chapter was built from all 29 matrices Fortinet has published,
from FortiSwitchOS 7.0.0 through 8.0.0 (7.0.0, 7.0.1, 7.0.2, 7.0.3, 7.0.10, 7.0.11, 7.2.0, 7.2.1, 7.2.2, 7.2.3, 7.2.5, 7.2.7, 7.2.8, 7.2.9, 7.2.10, 7.4.0, 7.4.1, 7.4.2, 7.4.3, 7.4.4, 7.4.7, 7.6.0, 7.6.1, 7.6.2, 7.6.4, 7.6.5, 7.6.6, 7.6.7, 8.0.0). For each feature, the
table shows the first release in which the feature is listed:

| Version entry | Meaning |
| --- | --- |
| `7.0.0 or earlier` | Listed in the 7.0.0 matrix, the oldest one Fortinet publishes; the feature may be older |
| `7.4.3 and later` | First listed in 7.4.3 and in every later release train |
| `7.2.7+; 7.4.3+; 7.6.0+; 8.0.0+` | Added to several release trains at different patch levels (often backported); the first listing in each train is shown |

Three cautions apply. First, *listed* is not the same as *introduced*: a few
features existed before Fortinet added them to the matrix. Second, the matrix
lists features per **model series**, and many features are supported on only
some models; check the matrix for your exact model before relying on a feature.
Third, where Fortinet renamed a feature, the history follows it across names
(for example, *FortiSwitch Cloud* and *FortiLAN Cloud* became *FortiEdge Cloud*,
and *ACL (IPv4)* became *ACL (IPv4 ingress)*).

### Where the SRG data comes from

The SRG column uses requirement IDs from the October 2026 DISA library:

| SRG | Release | Applies to |
| --- | --- | --- |
| **Layer 2 Switch** | V3R4 | Switching functions: port and endpoint security, spanning tree, VLANs, flooding |
| **Network Device Management (NDM)** | V5R5 | The switch's management plane: administrators, logging, time, cryptography, firmware |
| **Router** | V5R2 | Layer 3 functions: routing protocols, uRPF, multicast, filtering |
| **AAA Services** | V2R3 | The authentication servers and protocols the switch relies on for 802.1X and RADIUS |

Each feature maps to one of three kinds of relationship:

- **Implements a requirement.** The feature is how the switch meets an SRG
  requirement. DHCP snooping implements the Layer 2 Switch SRG's DHCP snooping
  requirement, for example.
- **Must be configured to meet a requirement.** The feature is in scope of a
  requirement and has to be set up correctly. Routing protocols must
  authenticate their neighbors under the Router SRG, for example.
- **No direct requirement.** The feature is operational, such as PoE or port
  splitting. It has no SRG requirement of its own, but if it is not needed it
  falls under the Layer 2 Switch requirement to disable non-essential
  capabilities (`SRG-NET-000131-L2S-000014`).

The mapping is a starting point for an assessment, not a ruling. Confirm it with
your assessor, especially where a feature relates to an organization-defined
requirement.

## Design Considerations

- **Pick the release first, then the features.** If your design depends on a
  feature listed only from a certain release (for example RadSec from 7.6.4),
  that sets the minimum FortiSwitchOS version, and the firmware must also be a
  vendor-supported release (`SRG-APP-001035-NDM-000340`).
- **Use the security features the SRG expects.** The Layer 2 Switch SRG's
  endpoint and port requirements (802.1X or MAB, DHCP snooping, IP source guard,
  dynamic ARP inspection, root and BPDU guard, loop guard, storm control) all have
  FortiSwitch features listed since 7.0.0 or earlier. There is no technical reason
  to leave them unconfigured.
- **Disable what you do not use.** Every feature marked "No direct requirement"
  should be off unless it serves a documented purpose.
- **Plan for managed mode.** Most FortiSwitch deployments are managed by a
  FortiGate through FortiLink. Security Fabric features are available only in
  managed mode, and the switch configuration and evidence then live on the
  FortiGate.
- **Watch the Advanced Features license.** Several Layer 3 features (OSPF, BGP,
  IS-IS, VRF, PBR, EVPN) require the FortiSwitch Advanced Features license. The
  SRG requirements apply only if the feature is licensed and enabled.

## Implementation and Automation

### The FortiSwitch feature map

Abbreviations in the SRG column: **L2S** is the Layer 2 Switch SRG, **NDM** the
Network Device Management SRG, **RTR** the Router SRG, and **AAA** the AAA
Services SRG. The requirement titles are listed in the next table.

| Category | Feature | First listed (FortiSwitchOS) | SRG requirement(s) |
| --- | --- | --- | --- |
| Security Fabric | Centralized configuration | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000340`; NDM `SRG-APP-000033-NDM-000212` |
| Security Fabric | Centralized firmware management | 7.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; NDM `SRG-APP-001035-NDM-000340` |
| Security Fabric | Automated detection and recommendations | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000100` |
| Security Fabric | Syslog collection | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325` |
| Security Fabric | Device detection | 7.0.0 or earlier | L2S `SRG-NET-000148-L2S-000015` |
| Security Fabric | Network device detection | 7.0.0 or earlier | L2S `SRG-NET-000148-L2S-000015` |
| Security Fabric | Block intra-VLAN traffic | 7.0.0 or earlier | L2S `SRG-NET-000715-L2S-000120` |
| Security Fabric | Host quarantine | 7.0.0 or earlier | L2S `SRG-NET-000057-L2S-000005`; L2S `SRG-NET-000715-L2S-000120` |
| Security Fabric | Automation stitches (zero-touch provisioning automation) | 7.4.3 and later | L2S `SRG-NET-000512-L2S-000100` |
| Security Fabric | Integrated FortiGate network access control (NAC) function | 7.0.0 or earlier | L2S `SRG-NET-000148-L2S-000015`; L2S `SRG-NET-000343-L2S-000016`; L2S `SRG-NET-000057-L2S-000005` |
| Security Fabric | NAC LAN segments | 7.0.1 and later | L2S `SRG-NET-000715-L2S-000120`; L2S `SRG-NET-000057-L2S-000005` |
| Security Fabric | FortiGuard IoT identification | 7.0.0 or earlier | L2S `SRG-NET-000148-L2S-000015` |
| Security Fabric | Matching FortiClient EMS tags in NAC policies | 7.0.0 or earlier | L2S `SRG-NET-000057-L2S-000005`; L2S `SRG-NET-000520-L2S-000105` |
| Security Fabric | Matching IoT/OT vulnerabilities in NAC policies | 7.4.0 and later | L2S `SRG-NET-000057-L2S-000005`; L2S `SRG-NET-000520-L2S-000105` |
| Security Fabric | Matching FortiVoice tags in NAC policies | 7.4.3 and later | L2S `SRG-NET-000057-L2S-000005`; L2S `SRG-NET-000520-L2S-000105` |
| Security Fabric | NAC: control of how long matched devices are kept | 7.4.3 and later | L2S `SRG-NET-000057-L2S-000005` |
| Security Fabric | NAC and 802.1X on same port | 7.6.4 and later | L2S `SRG-NET-000343-L2S-000016`; L2S `SRG-NET-000057-L2S-000005` |
| Security Fabric | Dynamic port policies (DPP) | 7.0.0 or earlier | L2S `SRG-NET-000057-L2S-000005`; L2S `SRG-NET-000520-L2S-000105` |
| Security Fabric | DPP: control of how long matched devices are kept | 7.4.3 and later | L2S `SRG-NET-000057-L2S-000005` |
| Security Fabric | FortiSwitch VLANs over VXLAN | 7.2.1 and later | L2S `SRG-NET-000715-L2S-000120` |
| Security Fabric | FortiLink management over VXLAN | 7.2.1 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000038-NDM-000213` |
| Security Fabric | FortiView Internal Hubs | 7.2.3 and later | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Security Fabric | NAC device telemetry | 7.2.3 and later | L2S `SRG-NET-000148-L2S-000015` |
| Security Fabric | Inter-VLAN routing offload | 7.4.1 and later | RTR `SRG-NET-000018-RTR-000001` |
| Security Fabric | FortiLink Secure Fabric authentication | 7.4.1 and later | NDM `SRG-APP-000516-NDM-000336`; L2S `SRG-NET-000325-L2S-000041` |
| Security Fabric | FortiLink Secure Fabric encryption | 7.4.1 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330` |
| Security Fabric | FortiLink using HTTPS | 7.4.2 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000142-NDM-000245` |
| Management and Configuration | CPLD software upgrade support for OS | 7.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352` |
| Management and Configuration | Firmware image rotation (dual-firmware image support) | 7.0.0 or earlier | NDM `SRG-APP-000457-NDM-000352`; L2S `SRG-NET-000235-L2S-000031` |
| Management and Configuration | HTTP REST APIs for configuration and monitoring | 7.0.0 or earlier | NDM `SRG-APP-000142-NDM-000245`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000033-NDM-000212` |
| Management and Configuration | Support for switch SNMP OID | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310` |
| Management and Configuration | IP conflict detection and notification | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000100` |
| Management and Configuration | FortiEdge Cloud configuration | 7.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000033-NDM-000212` |
| Management and Configuration | FortiSwitch Manager configuration | 7.2.1 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000033-NDM-000212` |
| Management and Configuration | Auto topology | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Security and Visibility | RADIUS for administrative authentication | 7.2.0 and later | NDM `SRG-APP-000516-NDM-000336`; AAA `SRG-APP-000516-AAA-000640`; AAA `SRG-APP-000172-AAA-000520` |
| Security and Visibility | TACACS+ for administrative authentication | 7.2.0 and later | NDM `SRG-APP-000516-NDM-000336`; AAA `SRG-APP-000516-AAA-000640` |
| Security and Visibility | 802.1X port mode | 7.0.0 or earlier | L2S `SRG-NET-000343-L2S-000016`; AAA `SRG-APP-000394-AAA-000430` |
| Security and Visibility | 802.1X MAC-based mode | 7.0.0 or earlier | L2S `SRG-NET-000148-L2S-000015`; L2S `SRG-NET-000343-L2S-000016`; AAA `SRG-APP-000158-AAA-000420` |
| Security and Visibility | 802.1X MAC-based mode: Wake-on-LAN | 7.2.2 and later | L2S `SRG-NET-000343-L2S-000016` |
| Security and Visibility | User-based (802.1X) VLAN assignment | 7.0.0 or earlier | L2S `SRG-NET-000057-L2S-000005`; L2S `SRG-NET-000343-L2S-000016` |
| Security and Visibility | 802.1X: priority for dynamic or egress VLAN assignment | 7.4.2 and later | L2S `SRG-NET-000057-L2S-000005` |
| Security and Visibility | 802.1X: MAB | 7.0.0 or earlier | L2S `SRG-NET-000148-L2S-000015` |
| Security and Visibility | 802.1X: MAB entry aging | 7.4.1 and later | L2S `SRG-NET-000148-L2S-000015` |
| Security and Visibility | 802.1X: limiting the number of MAB sessions | 7.4.7+; 7.6.2+; 8.0.0+ | L2S `SRG-NET-000148-L2S-000015`; L2S `SRG-NET-000193-L2S-000020` |
| Security and Visibility | Tagged VLAN support for authserver-timeout | 7.2.7+; 7.4.3+; 7.6.0+; 8.0.0+ | L2S `SRG-NET-000235-L2S-000031` |
| Security and Visibility | open-auth mode | 7.0.0 or earlier | L2S `SRG-NET-000343-L2S-000016` |
| Security and Visibility | MAC move | 7.0.1 and later | L2S `SRG-NET-000148-L2S-000015` |
| Security and Visibility | 802.1X/MAB priority | 7.2.1 and later | L2S `SRG-NET-000343-L2S-000016` |
| Security and Visibility | RADIUS accounting server support | 7.0.0 or earlier | AAA `SRG-APP-000023-AAA-000030`; NDM `SRG-APP-000516-NDM-000350` |
| Security and Visibility | RADIUS CoA and disconnect messages | 7.0.0 or earlier | L2S `SRG-NET-000057-L2S-000005`; AAA `SRG-APP-000516-AAA-000640` |
| Security and Visibility | 802.1X: RadSec (IPv4) | 7.6.4 and later | AAA `SRG-APP-000172-AAA-000520`; AAA `SRG-APP-000142-AAA-000020` |
| Security and Visibility | EAP pass-through | 7.0.0 or earlier | AAA `SRG-APP-000516-AAA-000440` |
| Security and Visibility | IP-MAC binding (IPv4) | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000026` |
| Security and Visibility | sFlow (IPv4) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000350` |
| Security and Visibility | Flow export (IPv4) | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000350` |
| Security and Visibility | ACL (IPv4 ingress) | 7.0.0 or earlier | RTR `SRG-NET-000018-RTR-000001`; L2S `SRG-NET-000512-L2S-000100` |
| Security and Visibility | ACL (IPv6 ingress) | 7.2.3 and later | RTR `SRG-NET-000018-RTR-000001`; L2S `SRG-NET-000512-L2S-000100` |
| Security and Visibility | Multistage ACL (IPv4) | 7.0.0 or earlier | RTR `SRG-NET-000018-RTR-000001` |
| Security and Visibility | Multiple ingress ACLs (IPv4) | 7.0.0 or earlier | RTR `SRG-NET-000018-RTR-000001` |
| Security and Visibility | ACL (IPv4 prelookup) | 7.4.3 and later | RTR `SRG-NET-000018-RTR-000001` |
| Security and Visibility | ACL (IPv4 egress) | 7.4.3 and later | RTR `SRG-NET-000018-RTR-000001` |
| Security and Visibility | ACL service (IPv4) | 7.4.3 and later | RTR `SRG-NET-000018-RTR-000001` |
| Security and Visibility | Schedule for ACLs (IPv4) | 7.0.0 or earlier | RTR `SRG-NET-000018-RTR-000001` |
| Security and Visibility | Dynamic ACLs (IPv4) | 7.2.2 and later | L2S `SRG-NET-000057-L2S-000005`; RTR `SRG-NET-000018-RTR-000001` |
| Security and Visibility | Dynamic ACLs: CoA (IPv4) | 7.4.7 and later | L2S `SRG-NET-000057-L2S-000005` |
| Security and Visibility | ACL: color marking (IPv4) | 7.2.0 and later | L2S `SRG-NET-000193-L2S-000020` |
| Security and Visibility | ACL: enhanced classifiers | 7.6.1 and later | RTR `SRG-NET-000018-RTR-000001` |
| Security and Visibility | ACL mirror | 7.6.0 and later | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Security and Visibility | DHCP snooping | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000025` |
| Security and Visibility | DHCPv6 snooping | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000025` |
| Security and Visibility | DHCP-snooping static entries (IPv4) | 7.2.2 and later | L2S `SRG-NET-000362-L2S-000025` |
| Security and Visibility | DHCP-snooping option 82 | 7.4.0 and later | L2S `SRG-NET-000362-L2S-000025` |
| Security and Visibility | DHCP-snooping monitor mode | 7.4.3 and later | L2S `SRG-NET-000362-L2S-000025` |
| Security and Visibility | Allowed DHCP server list | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000025` |
| Security and Visibility | Flap guard | 7.2.0 and later | L2S `SRG-NET-000193-L2S-000020` |
| Security and Visibility | IP source guard (IPv4) | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000026` |
| Security and Visibility | IP source-guard violation log (IPv4) | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000026`; NDM `SRG-APP-000516-NDM-000350` |
| Security and Visibility | Dynamic ARP inspection (IPv4) | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000027` |
| Security and Visibility | ARP timeout value | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000027` |
| Security and Visibility | DAI: monitor ARP packets | 7.4.3 and later | L2S `SRG-NET-000362-L2S-000027` |
| Security and Visibility | RMON group 1 | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310` |
| Security and Visibility | Reliable syslog | 7.0.0 or earlier | NDM `SRG-APP-000516-NDM-000350`; NDM `SRG-APP-000515-NDM-000325` |
| Security and Visibility | Packet capture | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Security and Visibility | MACsec: PSK mode | 7.0.0 or earlier | NDM `SRG-APP-000412-NDM-000331`; L2S `SRG-NET-000325-L2S-000041` |
| Security and Visibility | MACsec: Dynamic-CAK mode | 7.2.1 and later | NDM `SRG-APP-000412-NDM-000331`; L2S `SRG-NET-000325-L2S-000041` |
| Security and Visibility | MACsec: AWS Direct Connect support | 7.4.4 and later | NDM `SRG-APP-000412-NDM-000331` |
| Security and Visibility | LINCE support | 7.0.10+; 7.2.8+; 7.4.3+; 7.6.0+; 8.0.0+ | NDM `SRG-APP-000179-NDM-000265` |
| Security and Visibility | OS image signature verification | 7.4.0 and later | NDM `SRG-APP-000131-NDM-000243` |
| Security and Visibility | Configuration file verification | 8.0.0 and later | NDM `SRG-APP-000131-NDM-000243`; NDM `SRG-APP-000516-NDM-000340` |
| Security and Visibility | Network monitor | 7.4.1 and later | L2S `SRG-NET-000148-L2S-000015` |
| Security and Visibility | FIPS 140-3 (Level 1) and CC support | 7.6.4 and later | NDM `SRG-APP-000179-NDM-000265`; NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000411-NDM-000330` |
| Security and Visibility | FedRAMP support | 8.0.0 and later | NDM `SRG-APP-000179-NDM-000265` |
| Security and Visibility | OpenSSL security level for applications | 8.0.0 and later | NDM `SRG-APP-000412-NDM-000331`; NDM `SRG-APP-000142-NDM-000245` |
| Security and Visibility | DNS over TLS | 8.0.0 and later | NDM `SRG-APP-000412-NDM-000331` |
| Layer 2 | Link aggregation group size | 7.0.0 or earlier | L2S `SRG-NET-000760-L2S-000160` |
| Layer 2 | LAG min-max bundle | 7.0.0 or earlier | L2S `SRG-NET-000760-L2S-000160` |
| Layer 2 | LACP fallback mode | 7.4.0 and later | L2S `SRG-NET-000512-L2S-000005` |
| Layer 2 | IPv6 RA guard | 7.0.0 or earlier | RTR `SRG-NET-000512-RTR-000014` |
| Layer 2 | IGMP snooping | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000002` |
| Layer 2 | IGMP proxy | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000002` |
| Layer 2 | IGMP querier | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000002` |
| Layer 2 | MLD snooping | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000002` |
| Layer 2 | MLD proxy | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000002` |
| Layer 2 | MLD querier | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000002` |
| Layer 2 | LLDP transmit | 7.0.0 or earlier | L2S `SRG-NET-000131-L2S-000014` |
| Layer 2 | LLDP-MED | 7.0.0 or earlier | L2S `SRG-NET-000131-L2S-000014` |
| Layer 2 | LLDP-MED: ELIN support | 7.0.0 or earlier | L2S `SRG-NET-000131-L2S-000014` |
| Layer 2 | MAC learning limit | 7.0.0 or earlier | L2S `SRG-NET-000148-L2S-000015`; L2S `SRG-NET-000193-L2S-000020` |
| Layer 2 | Learning-limit violation log | 7.0.0 or earlier | L2S `SRG-NET-000148-L2S-000015`; NDM `SRG-APP-000516-NDM-000350` |
| Layer 2 | Learning-limit violation action | 7.0.2 and later | L2S `SRG-NET-000148-L2S-000015` |
| Layer 2 | set mac-violation-timer | 7.0.0 or earlier | L2S `SRG-NET-000148-L2S-000015` |
| Layer 2 | Sticky MAC | 7.0.0 or earlier | L2S `SRG-NET-000148-L2S-000015` |
| Layer 2 | Warning when the layer-2 table is getting full | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Layer 2 | MSTP instances | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000003` |
| Layer 2 | STP root guard | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000021` |
| Layer 2 | STP BPDU guard | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000022` |
| Layer 2 | Rapid PVST interoperation | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000003` |
| Layer 2 | VLANs supported by RPVST+ | 7.4.3 and later | L2S `SRG-NET-000512-L2S-000003` |
| Layer 2 | forced-untagged or force-tagged setting on switch interfaces | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000011`; L2S `SRG-NET-000512-L2S-000012` |
| Layer 2 | Private VLANs | 7.0.0 or earlier | L2S `SRG-NET-000715-L2S-000120` |
| Layer 2 | Multi-stage load balancing | 7.0.0 or earlier | L2S `SRG-NET-000760-L2S-000160` |
| Layer 2 | Priority-based Flow Control | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Layer 2 | Enhanced Transmission Selection (ETS) | 8.0.0 and later | L2S `SRG-NET-000193-L2S-000020` |
| Layer 2 | DCBX | 8.0.0 and later | L2S `SRG-NET-000131-L2S-000014` |
| Layer 2 | Ingress pause metering | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Layer 2 | Storm control | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000001`; L2S `SRG-NET-000193-L2S-000020` |
| Layer 2 | Per-port storm control | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000001` |
| Layer 2 | Global burst-size control | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000001` |
| Layer 2 | Storm-control monitoring | 7.4.3 and later | L2S `SRG-NET-000512-L2S-000001`; NDM `SRG-APP-000516-NDM-000350` |
| Layer 2 | MAC/IP/protocol-based VLAN assignment | 7.0.0 or earlier | L2S `SRG-NET-000057-L2S-000005` |
| Layer 2 | Virtual wire | 7.0.0 or earlier | L2S `SRG-NET-000715-L2S-000120` |
| Layer 2 | Loop guard | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000023` |
| Layer 2 | Percentage rate control | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Layer 2 | VLAN stacking (QinQ) | 7.0.0 or earlier | L2S `SRG-NET-000715-L2S-000120` |
| Layer 2 | VLAN mapping | 7.0.0 or earlier | L2S `SRG-NET-000715-L2S-000120` |
| Layer 2 | VLAN pruning | 7.6.1 and later | L2S `SRG-NET-000512-L2S-000009` |
| Layer 2 | SPAN | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Layer 2 | RSPAN and ERSPAN (IPv4) | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Layer 2 | FortiOS one-arm sniffer | 7.4.1 and later | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Layer 2 | Traffic policy (policer) | 7.2.3 and later | L2S `SRG-NET-000193-L2S-000020` |
| Layer 2 | Flow control | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Layer 2 | Layer-2 NAT (IPv4) | 8.0.0 and later | RTR `SRG-NET-000018-RTR-000001` |
| Layer 3 | VXLAN (hardware based) | 7.4.2 and later | L2S `SRG-NET-000715-L2S-000120` |
| Layer 3 | VXLAN: STP virtual root | 7.2.1 and later | L2S `SRG-NET-000512-L2S-000003` |
| Layer 3 | VXLAN: ECMP | 7.4.1 and later | L2S `SRG-NET-000760-L2S-000160` |
| Layer 3 | VXLAN: DHCP snooping | 7.4.3 and later | L2S `SRG-NET-000362-L2S-000025` |
| Layer 3 | VXLAN: DHCPv6 snooping | 7.4.3 and later | L2S `SRG-NET-000362-L2S-000025` |
| Layer 3 | VXLAN: QoS | 7.4.3 and later | L2S `SRG-NET-000193-L2S-000020` |
| Layer 3 | VXLAN: IGMP snooping (IPv4) | 7.6.0 and later | L2S `SRG-NET-000512-L2S-000002` |
| Layer 3 | SVI | 7.6.4 and later | RTR `SRG-NET-000018-RTR-000001`; NDM `SRG-APP-000038-NDM-000213` |
| Layer 3 | RVI | 7.0.0 or earlier | RTR `SRG-NET-000018-RTR-000001` |
| Layer 3 | Link monitor (IPv4/IPv6) | 7.0.0 or earlier | L2S `SRG-NET-000760-L2S-000160` |
| Layer 3 | Static routing (IPv4/IPv6) | 7.0.0 or earlier | RTR `SRG-NET-000018-RTR-000001` |
| Layer 3 | Software-based routing only (IPv4/IPv6) | 7.0.0 or earlier | RTR `SRG-NET-000018-RTR-000001` |
| Layer 3 | Hardware-based routing (IPv4/IPv6) | 7.0.0 or earlier | RTR `SRG-NET-000018-RTR-000001` |
| Layer 3 | ECMP with hardware-based routing | 7.2.2 and later | L2S `SRG-NET-000760-L2S-000160` |
| Layer 3 | Static BFD (IPv4/IPv6) | 7.0.0 or earlier | L2S `SRG-NET-000760-L2S-000160` |
| Layer 3 | uRPF | 7.0.0 or earlier | RTR `SRG-NET-000205-RTR-000014` |
| Layer 3 | DHCP relay (IPv4) | 7.0.0 or earlier | L2S `SRG-NET-000362-L2S-000025` |
| Layer 3 | DHCP server (IPv4) | 7.0.0 or earlier | L2S `SRG-NET-000131-L2S-000014` |
| Layer 3 (Advanced Features license) | Policy-based routing (IPv4) | 7.0.1 and later | RTR `SRG-NET-000018-RTR-000001` |
| Layer 3 (Advanced Features license) | VRF (IPv4/IPv6) | 7.0.0 or earlier | RTR `SRG-NET-000512-RTR-000005`; L2S `SRG-NET-000715-L2S-000120` |
| Layer 3 (Advanced Features license) | OSPF (IPv4/IPv6) | 7.0.0 or earlier | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | BFD for OSPF | 7.2.2 and later | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | OSPF database overflow protection (IPv4) | 7.0.0 or earlier | RTR `SRG-NET-000362-RTR-000110` |
| Layer 3 (Advanced Features license) | OSPF graceful restart (helper mode only) | 7.0.0 or earlier | L2S `SRG-NET-000760-L2S-000160` |
| Layer 3 (Advanced Features license) | OSPF: VRF support (IPv4) | 7.0.0 or earlier | RTR `SRG-NET-000512-RTR-000005` |
| Layer 3 (Advanced Features license) | OSPF reference bandwidth | 8.0.0 and later | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | OSPF network type | 8.0.0 and later | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | RIP (IPv4/IPv6) | 7.0.0 or earlier | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | BFD for RIP | 7.0.0 or earlier | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | VRRP (IPv4/IPv6) | 7.0.0 or earlier | L2S `SRG-NET-000760-L2S-000160`; RTR `SRG-NET-000230-RTR-000001` |
| Layer 3 (Advanced Features license) | BGP (IPv4/IPv6) | 7.0.0 or earlier | RTR `SRG-NET-000168-RTR-000078`; RTR `SRG-NET-000018-RTR-000002` |
| Layer 3 (Advanced Features license) | BFD for BGP | 7.0.0 or earlier | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | BGP: simplified fabric configuration | 7.6.0 and later | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | BGP: local AS | 8.0.0 and later | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | IS-IS (IPv4/IPv6) | 7.0.0 or earlier | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | BFD for IS-IS | 7.2.2 and later | RTR `SRG-NET-000168-RTR-000078` |
| Layer 3 (Advanced Features license) | PIM-SSM (IPv4) | 7.2.8 and later | RTR `SRG-NET-000019-RTR-000003`; RTR `SRG-NET-000019-RTR-000004` |
| Layer 3 (Advanced Features license) | VXLAN: BGP EVPN | 7.4.0 and later | RTR `SRG-NET-000168-RTR-000078`; L2S `SRG-NET-000715-L2S-000120` |
| Layer 3 (Advanced Features license) | VXLAN: BGP EVPN multihoming | 7.6.2 and later | L2S `SRG-NET-000760-L2S-000160` |
| Layer 3 (Advanced Features license) | VXLAN: Duplicate address detection | 7.4.1 and later | L2S `SRG-NET-000148-L2S-000015` |
| Layer 3 (Advanced Features license) | VXLAN: ARP/ND suppression | 7.4.0 and later | L2S `SRG-NET-000362-L2S-000027` |
| High Availability | MCLAG (multichassis link aggregation group) | 7.0.0 or earlier | L2S `SRG-NET-000760-L2S-000160` |
| High Availability | STP supported in MCLAGs | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000003` |
| High Availability | IGMP snooping support in MCLAG | 7.0.0 or earlier | L2S `SRG-NET-000512-L2S-000002` |
| High Availability | Layer-3 routing in MCLAG | 7.0.1 and later | L2S `SRG-NET-000760-L2S-000160` |
| High Availability | High-Availability Seamless Redundancy (HSR) | 7.4.0 and later | L2S `SRG-NET-000760-L2S-000160` |
| High Availability | Parallel Redundancy Protocol (PRP) | 7.4.0 and later | L2S `SRG-NET-000760-L2S-000160` |
| High Availability | MRP | 7.0.0 or earlier | L2S `SRG-NET-000760-L2S-000160` |
| High Availability | MRP: 2 rings supported | 7.4.4 and later | L2S `SRG-NET-000760-L2S-000160` |
| Quality of Service | 802.1p support, including priority queuing trunk and WRED | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Quality of Service | QoS queue counters | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Quality of Service | Tail-drop policy | 7.0.1 and later | L2S `SRG-NET-000193-L2S-000020` |
| Quality of Service | RED drop policy | 7.0.1 and later | L2S `SRG-NET-000193-L2S-000020` |
| Quality of Service | WRED drop policy | 7.0.1 and later | L2S `SRG-NET-000193-L2S-000020` |
| Quality of Service | Egress drop mode | 7.0.1 and later | L2S `SRG-NET-000193-L2S-000020` |
| Quality of Service | QoS marking (IPv4/IPv6) | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Quality of Service | Summary of configured queue mappings | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Quality of Service | Egress priority tagging | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Quality of Service | ECN (IPv4/IPv6) | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Quality of Service | Real-time egress queue rates | 7.0.0 or earlier | L2S `SRG-NET-000193-L2S-000020` |
| Miscellaneous | PoE pre-standard detection | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | PoE modes: first come, first served or priority based | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | Perpetual PoE | 7.2.1 and later | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | PoE disconnection type | 7.2.2 and later | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | PoE max power mode | 7.0.11+; 7.2.10+; 7.4.7+; 7.6.2+; 8.0.0+ | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | Split port | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | TDR (time-domain reflectometer)/cable diagnostics | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | Detect-by-module max speed detection and notification | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | Monitor system temperature (threshold and SNMP trap) | 7.0.0 or earlier | NDM `SRG-APP-000395-NDM-000310` |
| Miscellaneous | MAC notification SNMP trap | 7.2.0 and later | NDM `SRG-APP-000395-NDM-000310`; L2S `SRG-NET-000148-L2S-000015` |
| Miscellaneous | CLI to show the details of port statistics | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | Configuration of the QSFP low-power mode | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | Energy-efficient Ethernet | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | PHY Forward Error Correction (FEC) | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | PTP version-2 transparent clock | 7.0.0 or earlier | NDM `SRG-APP-000920-NDM-000320` |
| Miscellaneous | PTP layer-2 boundary clock | 7.4.3 and later | NDM `SRG-APP-000920-NDM-000320` |
| Miscellaneous | Layer-3 PTP | 8.0.0 and later | NDM `SRG-APP-000920-NDM-000320` |
| Miscellaneous | Use PTP to synchronize system clock | 7.6.2 and later | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000374-NDM-000299` |
| Miscellaneous | Automatically select system clock source | 8.0.0 and later | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000925-NDM-000330` |
| Miscellaneous | Alias commands | 7.0.0 or earlier | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | Automation stitches | 7.2.0 and later | L2S `SRG-NET-000512-L2S-000100` |
| Miscellaneous | Automation stitches: triggered by storm-control drop rate | 7.4.3 and later | L2S `SRG-NET-000512-L2S-000001` |
| Miscellaneous | Automation stitches: custom automation actions | 7.4.3 and later | L2S `SRG-NET-000512-L2S-000100` |
| Miscellaneous | Multiple path traceroute | 7.2.0 and later | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | Wake-on-LAN packets | 7.2.0 and later | L2S `SRG-NET-000131-L2S-000014` |
| Miscellaneous | Save event log in flash memory | 7.2.0 and later | NDM `SRG-APP-000357-NDM-000293` |
| Miscellaneous | max-frame-size | 7.4.3 and later | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | Support of 128 ports plus internal and mgmt | 7.6.0 and later | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | NTP server (IPv4/IPv6) | 7.6.2 and later | NDM `SRG-APP-000920-NDM-000320`; NDM `SRG-APP-000395-NDM-000347` |
| Miscellaneous | CLI reports if BIOS and firmware signatures are valid | 7.6.2 and later | NDM `SRG-APP-000131-NDM-000243` |
| Miscellaneous | Airflow shown in GUI | 7.4.7+; 7.6.2+; 8.0.0+ | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |
| Miscellaneous | Turn off front-panel LEDs | 8.0.0 and later | No direct requirement; if unused, disable (L2S `SRG-NET-000131-L2S-000014`) |

### Requirement reference

The SRG requirements used in the map, with their severity in the current SRG
releases:

| SRG | Requirement | Severity | Requirement title |
| --- | --- | --- | --- |
| L2S | `SRG-NET-000057-L2S-000005` | CAT II | The layer 2 switch must dynamically associate security attributes with organization-defined subjects in accordance with organization-defined security policies as information is created and combined. |
| L2S | `SRG-NET-000131-L2S-000014` | CAT II | The layer 2 switch must be configured to disable non-essential capabilities. |
| L2S | `SRG-NET-000148-L2S-000015` | CAT I | The layer 2 switch must uniquely identify all network-connected endpoint devices before establishing any connection. |
| L2S | `SRG-NET-000193-L2S-000020` | CAT II | The layer 2 switch must manage excess bandwidth to limit the effects of packet flooding types of denial of service (DoS) attacks. |
| L2S | `SRG-NET-000235-L2S-000031` | CAT II | The layer 2 switch must be configured to fail securely in the event of an operational failure. |
| L2S | `SRG-NET-000325-L2S-000041` | CAT II | The layer 2 switch must uniquely identify and authenticate source by organization, system, application, and/or individual for information transfer. |
| L2S | `SRG-NET-000343-L2S-000016` | CAT II | The layer 2 switch must authenticate all network-connected endpoint devices before establishing any connection. |
| L2S | `SRG-NET-000362-L2S-000021` | CAT III | The layer 2 switch must have Root Guard enabled on all switch ports connecting to access layer switches and hosts. |
| L2S | `SRG-NET-000362-L2S-000022` | CAT II | The layer 2 switch must have BPDU Guard enabled on all user-facing or untrusted access switch ports. |
| L2S | `SRG-NET-000362-L2S-000023` | CAT II | The layer 2 switch must have STP Loop Guard enabled on all non-designated STP switch ports. |
| L2S | `SRG-NET-000362-L2S-000025` | CAT II | The layer 2 switch must have DHCP snooping for all user VLANs to validate DHCP messages from untrusted sources. |
| L2S | `SRG-NET-000362-L2S-000026` | CAT II | The layer 2 switch must have IP Source Guard enabled on all user-facing or untrusted access switch ports. |
| L2S | `SRG-NET-000362-L2S-000027` | CAT II | The layer 2 switch must have Dynamic Address Resolution Protocol (ARP) Inspection (DAI) enabled on all user VLANs. |
| L2S | `SRG-NET-000512-L2S-000001` | CAT III | The layer 2 switch must have Storm Control configured on all host-facing switch ports. |
| L2S | `SRG-NET-000512-L2S-000002` | CAT III | The layer 2 switch must have IGMP or MLD Snooping configured on all VLANs |
| L2S | `SRG-NET-000512-L2S-000003` | CAT II | The layer 2 switch must implement Rapid STP where VLANs span multiple switches with redundant links. |
| L2S | `SRG-NET-000512-L2S-000005` | CAT II | The layer 2 switch must have all trunk links enabled statically. |
| L2S | `SRG-NET-000512-L2S-000009` | CAT II | The layer 2 switch must have the default VLAN pruned from all trunk ports that do not require it. |
| L2S | `SRG-NET-000512-L2S-000011` | CAT II | The layer 2 switch must have all user-facing or untrusted ports configured as access switch ports. |
| L2S | `SRG-NET-000512-L2S-000012` | CAT II | The layer 2 switch must have the native VLAN assigned to an ID other than the default VLAN for all 802.1q trunk links. |
| L2S | `SRG-NET-000512-L2S-000100` | CAT II | The layer 2 switch must be configured in accordance with the security configuration settings based on DoD security configuration or implementation guidance, including STIGs, NSA configuration guides, CTOs, and DTMs. |
| L2S | `SRG-NET-000520-L2S-000105` | CAT II | The layer 2 switch must dynamically associate security attributes with organization-defined objects in accordance with organization-defined security policies as information is created and combined. |
| L2S | `SRG-NET-000715-L2S-000120` | CAT II | The layer 2 switch must implement physically or logically separate subnetworks to isolate organization-defined critical system components and functions. |
| L2S | `SRG-NET-000760-L2S-000160` | CAT II | The layer 2 switch must establish organization-defined alternate communications paths for system operations organizational command and control. |
| NDM | `SRG-APP-000033-NDM-000212` | CAT I | The network device must be configured to assign appropriate user roles or access levels to authenticated users. |
| NDM | `SRG-APP-000038-NDM-000213` | CAT II | The network device must enforce approved authorizations for controlling the flow of management information within the network device based on information flow control policies. |
| NDM | `SRG-APP-000131-NDM-000243` | CAT II | The network device must prevent the installation of patches, service packs, or application components without verification the software component has been digitally signed using a certificate that is recognized and approved by the organization. |
| NDM | `SRG-APP-000142-NDM-000245` | CAT I | The network device must be configured to prohibit the use of all unnecessary and/or nonsecure functions, ports, protocols, and/or services |
| NDM | `SRG-APP-000179-NDM-000265` | CAT I | The network device must use FIPS 140-2 approved algorithms for authentication to a cryptographic module. |
| NDM | `SRG-APP-000357-NDM-000293` | CAT II | The network device must allocate audit record storage capacity in accordance with organization-defined audit record storage requirements. |
| NDM | `SRG-APP-000374-NDM-000299` | CAT II | The network device must record time stamps for audit records that can be mapped to Coordinated Universal Time (UTC) or Greenwich Mean Time (GMT). |
| NDM | `SRG-APP-000395-NDM-000310` | CAT II | The network device must be configured to authenticate SNMP messages using a FIPS-validated Keyed-Hash Message Authentication Code (HMAC). |
| NDM | `SRG-APP-000395-NDM-000347` | CAT II | The network device must authenticate Network Time Protocol sources using authentication that is cryptographically based. |
| NDM | `SRG-APP-000411-NDM-000330` | CAT I | The network devices must use FIPS-validated Keyed-Hash Message Authentication Code (HMAC) to protect the integrity of nonlocal maintenance and diagnostic communications. |
| NDM | `SRG-APP-000412-NDM-000331` | CAT I | The network device must be configured to implement cryptographic mechanisms using a FIPS 140-2 approved algorithm to protect the confidentiality of remote maintenance sessions  |
| NDM | `SRG-APP-000457-NDM-000352` | CAT II | The network device must install security-relevant firmware updates within 30 days unless the time period is directed by an authoritative source (e.g., IAVM, CTOs, DTMs, STIGs). |
| NDM | `SRG-APP-000515-NDM-000325` | CAT II | The network device must off-load audit records onto a different system or media than the system being audited. |
| NDM | `SRG-APP-000516-NDM-000336` | CAT I | The network device must be configured to use at least one authentication server for the purpose of authenticating users prior to granting administrative access. For boundary devices, two authentication servers are required. |
| NDM | `SRG-APP-000516-NDM-000340` | CAT II | The network device must be configured to conduct backups of system level information contained in the information system when changes occur. |
| NDM | `SRG-APP-000516-NDM-000350` | CAT I | The network device must be configured to send log data to at least one central log server for the purpose of forwarding alerts to the administrators and the information system security officer (ISSO). For boundary devices, two log servers are required. |
| NDM | `SRG-APP-000920-NDM-000320` | CAT II | The network device must be configured to synchronize system clocks within and between systems or system components. |
| NDM | `SRG-APP-000925-NDM-000330` | CAT II | The network device must be configured to compare the internal system clocks on an organization-defined frequency with organization-defined authoritative time source. |
| NDM | `SRG-APP-001035-NDM-000340` | CAT I | The network device hardware and software must be a version supported by the vendor. |
| RTR | `SRG-NET-000018-RTR-000001` | CAT II | The router must be configured to enforce approved authorizations for controlling the flow of information within the network based on organization-defined information flow control policies. |
| RTR | `SRG-NET-000018-RTR-000002` | CAT II | The BGP router must be configured to reject inbound route advertisements for any Bogon prefixes. |
| RTR | `SRG-NET-000019-RTR-000003` | CAT II | The multicast router must be configured to disable Protocol Independent Multicast (PIM) on all interfaces that are not required to support multicast routing. |
| RTR | `SRG-NET-000019-RTR-000004` | CAT II | The multicast router must be configured to bind a Protocol Independent Multicast (PIM) neighbor filter to interfaces that have PIM enabled. |
| RTR | `SRG-NET-000168-RTR-000078` | CAT II | The router must be configured to authenticate all routing protocol messages using NIST-validated FIPS 198-1 message authentication code algorithm. |
| RTR | `SRG-NET-000205-RTR-000014` | CAT I | The perimeter router must be configured to restrict it from accepting outbound IP packets that contain an illegitimate address in the source address field via egress filter or by enabling Unicast Reverse Path Forwarding (uRPF). |
| RTR | `SRG-NET-000230-RTR-000001` | CAT II | The router must be configured to implement message authentication for all control plane protocols. |
| RTR | `SRG-NET-000362-RTR-000110` | CAT II | The router must be configured to protect against or limit the effects of denial-of-service (DoS) attacks by employing control plane protection. |
| RTR | `SRG-NET-000512-RTR-000005` | CAT I | The PE router must be configured to have each Virtual Routing and Forwarding (VRF) instance bound to the appropriate physical or logical interfaces to maintain traffic separation between all MPLS L3VPNs. |
| RTR | `SRG-NET-000512-RTR-000014` | CAT II | The perimeter router must be configured to suppress Router Advertisements on all external IPv6-enabled interfaces. |
| AAA | `SRG-APP-000023-AAA-000030` | CAT II | AAA Services must be configured to provide automated account management functions. |
| AAA | `SRG-APP-000142-AAA-000020` | CAT I | AAA Services must be configured to use protocols that encrypt credentials when authenticating clients, as defined in the PPSM CAL and vulnerability assessments. |
| AAA | `SRG-APP-000158-AAA-000420` | CAT II | AAA Services used for 802.1x must be configured to uniquely identify network endpoints (supplicants) before the authenticator establishes any connection. |
| AAA | `SRG-APP-000172-AAA-000520` | CAT I | AAA Services must be configured to encrypt transmitted credentials using a FIPS-validated cryptographic module. |
| AAA | `SRG-APP-000394-AAA-000430` | CAT II | AAA Services used for 802.1x must be configured to authenticate network endpoint devices (supplicants) before the authenticator establishes any connection. |
| AAA | `SRG-APP-000516-AAA-000440` | CAT II | AAA Services used for 802.1x must be configured to use secure Extensible Authentication Protocol (EAP), such as EAP-TLS, EAP-TTLS, and PEAP. |
| AAA | `SRG-APP-000516-AAA-000640` | CAT II | AAA Services must be configured to use a unique shared secret for communication (i.e. RADIUS, TACACS+) with clients requesting authentication services. |

### Collecting evidence

On a standalone FortiSwitch, collect `show full-configuration` and
`get system status` from the switch. On a FortiLink-managed switch, collect the
switch-related configuration from the FortiGate (the `switch-controller`
sections and the managed switch entries) as well as the switch's own status.
Attach both to the SRG-based checklist (Chapter 03).

## Validation and Troubleshooting

- **A feature in the map is missing on your switch.** Check the feature matrix for
  your model series; many features are supported on only some models. Then check
  your FortiSwitchOS release against the version column.
- **A feature is listed but its configuration is on the FortiGate.** The switch is
  FortiLink-managed. Collect the evidence from the FortiGate.
- **A Layer 3 feature will not enable.** It may require the Advanced Features
  license.
- **A requirement has no matching feature.** Some SRG requirements are met by
  procedure (for example, backups or account reviews) or by another system (such
  as the AAA server). Record how the requirement is met, not just which feature
  covers it.

## Security and Best Practices

- Keep FortiSwitchOS on a vendor-supported release and track the version column
  when planning upgrades.
- Enable the Layer 2 security features on every user-facing port, and record the
  ports where a feature cannot apply.
- Send FortiSwitch logs to a central log server and use FIPS-capable cryptography
  for management where the environment requires it.
- Review this map each time Fortinet publishes a new FortiSwitchOS major release or
  DISA updates an SRG.

## References and Knowledge Checks

**References:**

- Fortinet, *Feature Matrix for FortiSwitchOS*, releases 7.0.0 to 8.0.0
  (docs.fortinet.com, FortiSwitch documentation, "FortiSwitchOS Feature
  Matrix").
- DISA Layer 2 Switch SRG V3R4, Network Device Management SRG V5R5, Router SRG
  V5R2, and AAA Services SRG V2R3, from the October 2026 STIG Library
  Compilation.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment) and
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (Fortinet
  products).

**Knowledge checks:**

1. Why does a FortiSwitch assessment use SRGs rather than a STIG?
2. What does a version entry of `7.0.0 or earlier` mean, and why "or earlier"?
3. Which four SRGs does the map use, and what does each cover?
4. Which FortiSwitch features implement the Layer 2 Switch SRG's DHCP snooping,
   IP source guard, and dynamic ARP inspection requirements?
5. What applies to a feature marked "No direct requirement"?
6. Where do you collect evidence for a FortiLink-managed switch?

## Summary and Completion Checklist

FortiSwitch has no STIG, so it is assessed against the Layer 2 Switch, NDM,
Router, and AAA Services SRGs. This chapter maps all 235 features in the
FortiSwitchOS 8.0.0 feature matrix to the releases that list them, built from
every feature matrix Fortinet has published since 7.0.0, and to the SRG
requirement each feature implements or must be configured to meet. Operational
features with no direct requirement fall under the requirement to disable
non-essential capabilities when unused.

- [ ] Can find the releases that support a FortiSwitch feature.
- [ ] Can map a FortiSwitch feature to its SRG requirement.
- [ ] Can scope an SRG-based FortiSwitch assessment from the map.
- [ ] Can handle FortiLink-managed switches and licensed Layer 3 features.
