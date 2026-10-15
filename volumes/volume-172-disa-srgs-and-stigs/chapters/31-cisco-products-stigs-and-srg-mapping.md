# Chapter 31: Cisco Products — STIGs and SRG Mapping

## Learning Objectives

- Identify the Cisco products that have DISA STIGs, and the separate STIGs in
  each package.
- Choose the right STIG package for a Cisco device from its operating system
  (IOS, IOS XE, IOS XR, NX-OS, ASA, ACI) and its role (router or switch).
- Describe the CAT I requirements of the Cisco NDM, Router, Layer 2 Switch,
  ASA, and ISE STIGs, and configure the main ones.
- Map Cisco products that have no STIG to the SRGs that apply to them.
- Recognize where DISA's fix text examples need checking against the Cisco
  command reference before use.

## Theory and Architecture

Cisco has the broadest STIG coverage of any network vendor. Where Fortinet has
STIGs for FortiGate only (Chapter 10), the October 2026 DISA library has **ten
Cisco STIG packages containing 25 separate STIGs and 1,096 rules** (149 CAT I,
768 CAT II, 179 CAT III). The next largest network vendor in that library,
Juniper, has three packages. Each package covers one product family, and inside it
DISA splits the requirements by plane, the way Chapter 07 describes:

- **NDM (Network Device Management)**: the management plane, from the NDM SRG.
- **RTR (Router)**: routing and traffic filtering, from the Router SRG.
- **L2S (Layer 2 Switch)**: switching and port security, from the Layer 2
  Switch SRG.
- Product-specific STIGs for the ASA (Firewall, IPS, VPN) and ISE (NAC).

### The Cisco STIG packages

| Package | STIG | Release | Benchmark date | Rules (CAT I / II / III) | Rule IDs |
| --- | --- | --- | --- | --- | --- |
| Cisco IOS Router | NDM | V3R9 | 30 Sep 2026 | 35 (8 / 27 / 0) | `CISC-ND-` |
| Cisco IOS Router | RTR | V3R5 | 30 Sep 2026 | 92 (9 / 56 / 27) | `CISC-RT-` |
| Cisco IOS Switch | NDM | V3R9 | 30 Sep 2026 | 35 (8 / 27 / 0) | `CISC-ND-` |
| Cisco IOS Switch | L2S | V3R3 | 30 Sep 2026 | 22 (1 / 17 / 4) | `CISC-L2-` |
| Cisco IOS Switch | RTR | V3R4 | 30 Sep 2026 | 53 (4 / 38 / 11) | `CISC-RT-` |
| Cisco IOS XE Router | NDM | V3R7 | 01 Apr 2026 | 42 (8 / 34 / 0) | `CISC-ND-` |
| Cisco IOS XE Router | RTR | V3R5 | 01 Oct 2025 | 97 (10 / 58 / 29) | `CISC-RT-` |
| Cisco IOS XE Switch | NDM | V3R6 | 01 Apr 2026 | 42 (8 / 34 / 0) | `CISC-ND-` |
| Cisco IOS XE Switch | L2S | V3R2 | 02 Jul 2025 | 22 (1 / 17 / 4) | `CISC-L2-` |
| Cisco IOS XE Switch | RTR | V3R4 | 01 Apr 2026 | 88 (8 / 52 / 28) | `CISC-RT-` |
| Cisco IOS XR Router | NDM | V3R6 | 01 Apr 2026 | 27 (7 / 20 / 0) | `CISC-ND-` |
| Cisco IOS XR Router | RTR | V3R3 | 01 Oct 2025 | 96 (10 / 57 / 29) | `CISC-RT-` |
| Cisco NX-OS Switch | NDM | V3R6 | 05 Jan 2026 | 42 (7 / 35 / 0) | `CISC-ND-` |
| Cisco NX-OS Switch | L2S | V3R4 | 01 Jul 2026 | 22 (1 / 17 / 4) | `CISC-L2-` |
| Cisco NX-OS Switch | RTR | V3R4 | 01 Apr 2026 | 78 (7 / 45 / 26) | `CISC-RT-` |
| Cisco ASA | NDM | V2R5 | 01 Jul 2026 | 47 (7 / 40 / 0) | `CASA-ND-` |
| Cisco ASA | Firewall | V2R1 | 24 Jul 2024 | 21 (2 / 19 / 0) | `CASA-FW-` |
| Cisco ASA | VPN | V2R2 | 24 Oct 2024 | 41 (10 / 28 / 3) | `CASA-VN-` |
| Cisco ASA | IPS | V2R1 | 24 Jul 2024 | 23 (0 / 23 / 0) | `CASA-IP-` |
| Cisco ISE | NDM | V2R4 | 01 Jul 2026 | 51 (9 / 39 / 3) | `CSCO-NM-` |
| Cisco ISE | NAC | V2R4 | 01 Jul 2026 | 30 (8 / 21 / 1) | `CSCO-NC-` |
| Cisco ACI | NDM | V1R2 | 05 Jan 2026 | 26 (7 / 19 / 0) | `CACI-ND-` |
| Cisco ACI | RTR | V1R2 | 05 Jan 2026 | 26 (0 / 18 / 8) | `CACI-RT-` |
| Cisco ACI | L2S | V1R2 | 05 Jan 2026 | 7 (1 / 4 / 2) | `CACI-L2-` |
| Cisco Secure Network Analytics (SNA) | SNA | V1R1 | 29 Jun 2026 | 31 (8 / 23 / 0) | `CSNA-ND-` |

These figures come from the XCCDF files in the October 2026 STIG Library
Compilation. Each package ships as one ZIP, such as
`U_Cisco_IOS-XE_Router_Y26M04_STIG.zip`, with an overview document and one
XCCDF file per STIG. STIGs update quarterly, so confirm the current release on
the DoD Cyber Exchange before assessing. None of the Cisco packages includes a
SCAP benchmark, so every Cisco assessment is manual (Chapter 07).

### Choosing the right package

The operating system decides the package, and the device's role decides which
STIGs in the package apply:

| Device | Package | STIGs to apply |
| --- | --- | --- |
| Router running IOS XE (for example ISR 4000, Catalyst 8000) | IOS XE Router | NDM and RTR |
| Catalyst 3650, 3850, or 9000 switch (IOS XE) | IOS XE Switch | NDM and L2S; RTR as well if the switch routes. Chapter 32 maps every Catalyst 9000 feature to these rules, and Chapter 33 aligns the rules with FortiSwitch |
| Catalyst 2960-family switch (classic IOS) | IOS Switch | NDM and L2S; RTR as well if the switch routes |
| Router running classic IOS | IOS Router | NDM and RTR |
| Router running IOS XR (for example ASR 9000, NCS) | IOS XR Router | NDM and RTR |
| Nexus switch running NX-OS | NX-OS Switch | NDM and L2S; RTR as well if the switch routes |
| ASA 5500 or 5500-X, including FirePOWER Services | ASA | NDM and Firewall; VPN if it terminates VPNs; IPS if the FirePOWER module is installed. Chapter 34 aligns these rules with FortiGate |
| Identity Services Engine | ISE | NDM and NAC |
| ACI fabric (APIC and its leaf and spine switches) | ACI | NDM, L2S, and RTR, assessed for the fabric as a whole |
| Secure Network Analytics (formerly Stealthwatch) | SNA | SNA (a single management-plane STIG) |

The overviews state the scope. The IOS XE Switch STIG names the Catalyst 3650,
3850, and 9000 Series; the IOS Switch STIG names the Catalyst 2960 family. The
Router STIGs apply their RTR rules by router role: a **perimeter router**
connects an enclave to NIPRNet or SIPRNet, and a **provider edge (PE) router**
gives customers MPLS, L2VPN, and L3VPN services on a backbone. Rules written for
one role are Not Applicable to the other. The ACI STIGs treat the fabric as a
single switch and put traditional perimeter routing out of scope. The ASA IPS
STIG is based on the ASA FirePOWER module, checked through ASDM.

The NDM STIGs for IOS, IOS XE, IOS XR, and NX-OS share one numbering scheme
(`CISC-ND-`). Across the six of them there are 51 rule IDs, and 21 appear in
all six. The same ID means the same requirement on every platform, with small
wording differences, so one set of procedures and evidence can serve a mixed
Cisco estate.

### What the NDM STIGs require

The IOS XE Router NDM STIG's eight CAT I rules are the pattern for every Cisco
NDM STIG:

| CAT I requirement | Rule | What it means on IOS XE |
| --- | --- | --- |
| No unnecessary or nonsecure services | `CISC-ND-000470` | Disable the HTTP server, small servers, finger, PAD, BOOTP, and similar services |
| Only cryptographic representations of passwords | `CISC-ND-000620` | `service password-encryption`, and secrets stored as hashes |
| Management sessions end after five minutes of inactivity | `CISC-ND-000720` | `exec-timeout 5 0` on every line, and an HTTP idle timeout of 300 seconds |
| FIPS-validated HMAC for remote maintenance | `CISC-ND-001200` | SSH version 2 with `hmac-sha2-256` |
| FIPS-approved encryption for remote maintenance | `CISC-ND-001210` | SSH ciphers limited to AES in counter mode |
| At least two authentication servers | `CISC-ND-001370` | Two RADIUS or TACACS+ servers, with the local account as fallback only |
| Log data sent to at least two syslog servers | `CISC-ND-001450` | Two `logging host` entries |
| Supported IOS release | `CISC-ND-001470` | Run a release still inside Cisco's support lifecycle |

Two of these are stricter than the FortiGate NDM STIG in Chapter 10. The idle
timeout is **five minutes**, not ten, and Cisco NDM STIGs make **two**
authentication servers and **two** log servers CAT I requirements. The CAT II
rules fill in the rest of the NDM pattern: three failed logons followed by a
15-minute block, the DoD Notice and Consent Banner, auditing of administrator
activity and account changes, authenticated NTP, and SNMPv3.

The other NDM STIGs follow the same pattern with their own CAT I sets. The ASA
NDM STIG adds terminating management sessions after five minutes. The ISE NDM
STIG adds disabling Wireless Setup on production systems and verifying the
checksum of every software download. The SNA STIG requires DoD PKI as
multifactor authentication for interactive logins and an absolute session
timeout of eight hours.

### What the Router STIGs require

The RTR STIGs are the largest Cisco STIGs, at 53 to 97 rules. Their CAT I rules
fall into three groups:

- **Control plane protection**: protect the router against denial-of-service
  attacks (`CISC-RT-000120`).
- **Perimeter routers**: deny traffic by default, filter inbound traffic from
  an alternate gateway, do not peer with an alternate gateway's BGP service
  provider, and block packets with illegitimate source addresses (uRPF or
  egress filtering).
- **PE routers**: bind each VRF to the right interfaces and route targets,
  configure MPLS L2VPN identifiers correctly, and block traffic destined for
  the core infrastructure.

The CAT II and CAT III rules cover routing protocol authentication, BGP prefix
filtering, multicast (PIM) filtering, and logging of dropped packets.

### What the Layer 2 Switch STIGs require

The three L2S STIGs (IOS, IOS XE, NX-OS) have 22 rules each, with one CAT I
rule: **authenticate every endpoint before it connects** (`CISC-L2-000020`),
using 802.1X on host-facing ports and MAC Authentication Bypass for devices
that cannot do 802.1X. The CAT II rules are the familiar port security set:
root guard, BPDU guard, loop guard, DHCP snooping, IP Source Guard, dynamic ARP
inspection, storm control, VLAN pruning, and a non-default native VLAN.

### What the ASA and ISE STIGs require

The **ASA Firewall STIG** has two CAT I rules: filter outbound traffic to
authorized ports and services, and implement scanning threat detection. The
**ASA VPN STIG** has ten CAT I rules, most of them cryptographic: IKE for all
IPsec security associations, Diffie-Hellman group 16 or higher, SHA-2 for IKE
Phase 2, AES-256 for IKE Phase 1 and IPsec, TLS 1.2 or higher for remote
access, certificate-based authentication, revocation checking, and NSA-approved
or CSfC algorithms where classified traffic crosses an unclassified network.
The **ASA IPS STIG** has no CAT I rules. Its requirements cover IPS audit
records and their off-loading, blocking malicious code, prohibited mobile code,
denial-of-service traffic, and traffic from addresses with a bad reputation,
Advanced Malware Protection, automatic signature updates, and alerts to
administrators.

The **ISE NAC STIG** implements DoD Comply-to-Connect (C2C). Its CAT I rules
require TLS 1.2 between the endpoint agent and ISE, authorization policies
based on specific attributes, endpoint profiling, and posture assessment that
checks host firewall, anti-malware, and host IDS/IPS status on the clients the
NAC System Security Plan names. Chapter 25 uses this STIG as the expected
pattern for FortiNAC, because DISA has no NAC SRG.

### Cisco products without a STIG

Many Cisco products have no STIG in the October 2026 library. Assess each one
against the SRGs that match its functions (Chapter 03). The table is a starting
point, not a ruling; confirm it with your assessor.

| Product | What it does | SRGs and STIGs to start from |
| --- | --- | --- |
| **Secure Firewall Threat Defense (FTD)** and **Secure Firewall Management Center** | Next-generation firewall software and its manager | Firewall, IDPS, and VPN SRGs for FTD, and the NDM SRG for both. The ASA STIGs apply to ASA software, not to FTD |
| **Catalyst 9800 wireless controllers** and **Cisco access points** | Enterprise wireless | DISA's Network WLAN STIGs and the NDM SRG; check whether wireless is permitted at all |
| **Catalyst SD-WAN** (Manager, Controller, Validator, and IOS XE routers in controller mode) | Software-defined WAN | NDM SRG for the controllers. The IOS XE Router STIGs still state the requirements for the routers, but in controller mode the settings come from SD-WAN Manager templates, so trace each rule to its template setting |
| **Catalyst Center** (formerly DNA Center) and **Nexus Dashboard** | Central network management and automation | NDM SRG; like FortiManager, it controls many devices, so treat its access control and auditing as high impact |
| **Secure Email Gateway** and **Secure Web Appliance** | Email security and web proxy | ALG SRG and NDM SRG |
| **Secure Client** (formerly AnyConnect) | Endpoint VPN and security agent | The host operating system STIG, with the VPN SRG for its remote-access role |
| **Unified Communications Manager** and collaboration servers | Voice and video call control | EVVM SRGs (session management, endpoint, and policy) and the NDM SRG |
| **UCS servers** and **Intersight** | Compute and server management | NDM SRG for the management interfaces, and the STIG for each hosted operating system or hypervisor |
| **Meraki**, **Umbrella**, **Duo**, **Webex**, and **Secure Access** | Cloud-managed or cloud-delivered services | The Cloud Computing SRG; confirm each offering's FedRAMP or DoD authorization and impact level before use (Chapter 08) |

## Design Considerations

- **Pick the package by operating system, not model family.** A Catalyst 9000
  switch takes the IOS XE Switch package, while a Catalyst 2960 takes the IOS
  Switch package. Check `show version` before choosing.
- **Apply RTR rules to any device that routes.** A Layer 3 switch running
  routing protocols takes the Switch package's RTR STIG as well as NDM and L2S.
- **Plan for two of everything.** Two authentication servers and two log
  servers are CAT I requirements in the Cisco NDM STIGs. Build them into the
  management design before deployment.
- **Assign router roles before assessing.** Decide which routers are perimeter
  routers and which are PE routers, and record it, so the role-specific rules
  can be marked Applicable or Not Applicable consistently.
- **Use one NDM baseline across platforms.** Because the `CISC-ND-` rules are
  shared, one AAA, logging, NTP, SSH, and banner baseline can cover IOS, IOS XE,
  IOS XR, and NX-OS devices, with per-platform syntax.
- **Run FIPS-capable releases.** Several CAT I rules depend on FIPS-validated
  cryptography. Confirm that the software release and platform have the FIPS
  validation the environment requires, and check the DoDIN Approved Products
  List for the exact model and release.

## Implementation and Automation

The commands below follow DISA's fix text for the IOS XE Router and Switch
STIGs. Check them against the Cisco command reference for your platform and
release before use (see *Validation and Troubleshooting*).
[Volume III](../../volume-003-cisco-enterprise-networking/README.md) and
[Volume XXV](../../volume-025-cisco-security/README.md) cover Cisco
configuration in depth.

### Services, passwords, sessions, and lockout

```text
no ip http server
no service pad
no service tcp-small-servers
no service udp-small-servers
service password-encryption
!
line con 0
 exec-timeout 5 0
line vty 0 31
 exec-timeout 5 0
 transport input ssh
!
login block-for 900 attempts 3 within 120
login on-failure log
login on-success log
```

Configure every VTY line, not only the first few. From IOS XE 17.1.1, a
Catalyst 9300 has 32 VTY lines by default (16 before that), so the examples use
`line vty 0 31`; check the range on your device with `show line`. The fix text
examples configure only lines 0 to 4, which would leave the rest without the
timeout, SSH-only access, and AAA login.

The fix text for `CISC-ND-000470` lists more services to disable, including
BOOTP, DNS server, identd, finger, rcp and rsh, and call-home. Disable any that
are enabled and not needed.

### SSH cryptography

```text
ip ssh version 2
ip ssh server algorithm mac hmac-sha2-256
ip ssh server algorithm encryption aes256-ctr aes192-ctr aes128-ctr
```

### Two authentication servers

```text
aaa new-model
radius server RADIUS_1
 address ipv4 <RADIUS_1_IP>
 key <SHARED_SECRET>
radius server RADIUS_2
 address ipv4 <RADIUS_2_IP>
 key <SHARED_SECRET>
aaa group server radius RADIUS_SERVERS
 server name RADIUS_1
 server name RADIUS_2
aaa authentication login LOGIN_AUTHENTICATION group RADIUS_SERVERS local
aaa authentication login CONSOLE group RADIUS_SERVERS local
!
line con 0
 login authentication CONSOLE
line vty 0 31
 login authentication LOGIN_AUTHENTICATION
```

Keep one local account as the account of last resort, for use only when both
servers are unreachable.

### Banner and logging

```text
banner login ^C
<APPROVED_DOD_NOTICE_AND_CONSENT_BANNER_TEXT>
^C
!
logging host <SYSLOG_1_IP>
logging host <SYSLOG_2_IP>
logging userinfo
archive
 log config
  logging enable
  notify syslog contenttype plaintext
  hidekeys
```

The `archive log config` block records every configuration command an
administrator enters, which several audit rules require.

### 802.1X on access ports (Layer 2 Switch STIG)

```text
aaa authentication dot1x default group RADIUS_SERVERS
dot1x system-auth-control
!
interface range <ACCESS_PORTS>
 switchport mode access
 authentication host-mode single-host
 dot1x pae authenticator
 authentication port-control auto
```

Add MAC Authentication Bypass for devices that cannot do 802.1X. Use
`multi-domain` host mode where a phone and a computer share a port.

### ASA session timeouts and IKE group

```text
ssh timeout 5
console timeout 5
http server idle-timeout 5
!
crypto ikev2 policy 1
 group 20
```

The fix text for `CASA-VN-000210` uses `group 24`, but ASA 9.15(1) removed DH
groups 1, 2, 5, and 24, so the example uses group 20 (384-bit elliptic curve),
which meets the requirement for group 16 or higher. Chapter 34 lists the other
ASA fix text corrections.

### Collecting evidence

Collect `show running-config`, `show version`, `show ip ssh`,
`show line vty 0 31`, `show ntp associations`, `show logging`, and
`show snmp user` from each IOS or IOS XE device (Chapter 07). On an ASA, also
collect `show running-config all` for the settings that do not appear in the
default output. Attach the output to each rule in the checklist.

## Validation and Troubleshooting

- **A fix text command does not parse.** DISA's fix text is an example, and
  some examples need correcting. The IOS XE Router NDM fix for `CISC-ND-001370`
  uses `radius host` (the commands are `radius-server host`, or a
  `radius server` block as in the L2S fix) and writes
  `aaa authentication CONSOLE` without the `login` keyword. Check every fix
  text example against the Cisco command reference before deploying it.
- **The wrong package was used.** If many rules do not match the device's
  commands, the device may run a different operating system than assumed.
  Check `show version` and use the matching package.
- **Role-specific rules marked inconsistently.** Perimeter and PE rules must be
  Not Applicable on routers that do not have those roles. Record the role in
  the checklist so the next assessor reaches the same result.
- **Administrators are locked out after AAA changes.** Keep a session open
  while testing, and confirm the local fallback works before closing it.
- **Evaluate-STIG covers some platforms.** DoD users can automate parts of the
  assessment for supported Cisco platforms with Evaluate-STIG (Chapter 04).
  Review its results; it does not replace the assessor's judgment.

## Security and Best Practices

- Push the NDM baseline from configuration management (Ansible network modules,
  Catalyst Center, or NSO templates) so new devices start compliant and stay
  that way.
- Use a dedicated management network or VRF, and allow management protocols
  only from it.
- Treat ISE and Catalyst Center as high-impact systems: ISE decides who reaches
  the network, and Catalyst Center can change every device.
- Track Cisco software lifecycles. A release outside support is a CAT I finding
  on every Cisco NDM STIG.
- Review each Cisco STIG every quarter; the packages in this chapter range from
  July 2024 to September 2026 releases, and they change independently.

## References and Knowledge Checks

**References:**

- DISA Cisco STIG packages from the October 2026 STIG Library Compilation:
  `U_Cisco_IOS_Router_Y26M10_STIG.zip`, `U_Cisco_IOS_Switch_Y26M10_STIG.zip`,
  `U_Cisco_IOS-XE_Router_Y26M04_STIG.zip`, `U_Cisco_IOS-XE_Switch_Y26M04_STIG.zip`,
  `U_Cisco_IOS-XR_Router_Y26M04_STIG.zip`, `U_Cisco_NX-OS_Switch_Y26M07_STIG.zip`,
  `U_Cisco_ASA_Y26M07_STIG.zip`, `U_Cisco_ISE_Y26M07_STIG.zip`,
  `U_Cisco_ACI_Y26M01_STIG.zip`, and `U_Cisco_SNA_V1R1_STIG.zip`, with their
  overview documents.
- DISA NDM, Router, Layer 2 Switch, Firewall, IDPS, VPN, ALG, and EVVM SRGs;
  the Network WLAN STIGs; the Cloud Computing SRG.
- Cisco command references and configuration guides for each platform and
  release.
- [Chapter 03](03-the-srg-catalog-how-stigs-are-built-and-what-to-do-without-one.md)
  (SRG-based assessment),
  [Chapter 07](07-network-device-stigs-management-routing-and-filtering.md)
  (network device STIGs),
  [Chapter 10](10-fortinet-products-stigs-and-srg-mapping.md) (the Fortinet
  equivalent of this chapter), and
  [Chapter 25](25-fortinac-feature-version-and-srg-map.md) (the ISE NAC STIG
  used as a pattern).
- [Volume III — Cisco Enterprise Networking](../../volume-003-cisco-enterprise-networking/README.md),
  [Volume XXV — Cisco Security](../../volume-025-cisco-security/README.md),
  [Volume XXVII — Cisco Data Center](../../volume-027-cisco-data-center/README.md),
  and [Volume CVII — Cisco ISE and TrustSec Build-It-Yourself Lab](../../volume-107-cisco-ise-trustsec-lab/README.md).

**Knowledge checks:**

1. How many Cisco STIG packages are in the October 2026 library, and which
   STIGs does the ASA package contain?
2. Which package and STIGs apply to a Catalyst 9300 switch that runs OSPF?
3. Name four of the eight CAT I rules in the IOS XE Router NDM STIG.
4. How do the Cisco NDM STIGs differ from the FortiGate NDM STIG on idle
   timeout, authentication servers, and log servers?
5. What is the difference between a perimeter router and a PE router in the
   Router STIGs, and why does it matter for an assessment?
6. Which SRGs apply to Cisco Secure Firewall Threat Defense, and why do the ASA
   STIGs not apply to it?
7. Why should every fix text example be checked against the Cisco command
   reference?

## Summary and Completion Checklist

Cisco has ten STIG packages in the October 2026 library: IOS Router and Switch,
IOS XE Router and Switch, IOS XR Router, NX-OS Switch, ASA, ISE, ACI, and
Secure Network Analytics, with 25 STIGs and 1,096 rules between them. Each
package splits the requirements into NDM, RTR, and L2S STIGs, or
product-specific STIGs for the ASA and ISE. The operating system picks the
package and the device's role picks the STIGs. The Cisco NDM STIGs share rule
IDs across platforms, and they require a five-minute idle timeout and two
authentication and two log servers as CAT I rules. Cisco products without a
STIG, such as Secure Firewall Threat Defense, Catalyst Center, and the cloud
services, are assessed against their SRGs. DISA's fix text examples must be
checked against the Cisco command reference before use.

- [ ] Can list the Cisco STIG packages and the STIGs in each.
- [ ] Can choose the package and STIGs for any Cisco device.
- [ ] Can configure the main IOS XE NDM and Layer 2 Switch requirements.
- [ ] Can scope the SRGs for a Cisco product without a STIG.
- [ ] Can spot and correct fix text examples that will not parse.
