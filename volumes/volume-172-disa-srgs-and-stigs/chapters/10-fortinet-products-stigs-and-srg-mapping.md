# Chapter 10: Fortinet Products — STIGs and SRG Mapping

## Learning Objectives

- Identify which Fortinet products have published DISA STIGs and which do not.
- Describe what the FortiGate Firewall NDM STIG and the FortiGate Firewall STIG
  require, and configure the main requirements on FortiOS.
- Recognize the FortiGate functions that the two FortiGate STIGs do not cover,
  and the SRGs that apply to them.
- Map every major Fortinet product to the SRGs that apply when no STIG exists.
- Explain how FIPS-CC mode, the DoDIN Approved Products List, and Security
  Fabric management fit into a Fortinet STIG program.

## Theory and Architecture

Fortinet sells a large portfolio, much of it built around FortiOS and managed
together as the **Security Fabric**. DISA STIG coverage is far narrower than the
portfolio. At the time of writing, DISA has published STIGs for **FortiGate
only**:

| STIG | Current release (October 2026) | Rules | Covers |
| --- | --- | --- | --- |
| **Fortinet FortiGate Firewall NDM STIG** | V1R6, benchmark date 30 Sep 2026 | 60 (9 CAT I, 51 CAT II, 0 CAT III) | The FortiGate management plane: administrators, authentication, cryptography, sessions, auditing, logging, and software currency |
| **Fortinet FortiGate Firewall STIG** | V1R5, benchmark date 30 Sep 2026 | 29 (3 CAT I, 24 CAT II, 2 CAT III) | The FortiGate traffic-filtering function: policy filtering, DoS protection, traffic logging, and log protection |

These figures come from the October 2026 STIG Library Compilation, in which DISA
ships both STIGs in a single package, `U_FN_FortiGate_Firewall_Y26M10_STIG.zip`,
together with an overview, a revision history, and the original release memo.
NDM rules use STIG IDs beginning `FGFW-ND-`, and Firewall rules use IDs beginning
`FNFG-FW-`. STIGs update quarterly, so confirm the current release, rule count,
and rule text on the DoD Cyber Exchange before assessing. Recent releases also
say "DoW" (Department of War) where earlier releases said "DoD," for example in
the Standard Mandatory DoW Notice and Consent Banner; the requirement itself is
unchanged.

Every other Fortinet product (FortiManager, FortiAnalyzer, FortiSwitch, FortiAP,
FortiWeb, FortiMail, FortiClient, and the rest) has **no published STIG**. As
Chapter 03 explained, that does not exempt them. Each one is assessed directly
against the SRGs that match its functions.

### What the FortiGate NDM STIG requires

The NDM STIG implements the Network Device Management SRG for FortiOS. Its nine
CAT I rules are the ones that block an authorization:

| CAT I requirement | What it means on a FortiGate |
| --- | --- |
| Vendor-supported FortiOS release | Run a FortiOS version still inside Fortinet's support lifecycle |
| No unnecessary or non-secure functions, ports, protocols, or services | Management access limited to HTTPS and SSH, only on management interfaces; Telnet and HTTP off |
| LDAPS for LDAP connections | LDAP servers configured to use LDAPS rather than clear-text LDAP |
| FIPS 140-2 approved algorithms for authentication to a cryptographic module | FIPS-approved cryptography for administrator authentication |
| FIPS-validated HMAC for remote maintenance integrity | Approved MACs on SSH and HTTPS management sessions |
| FIPS-approved encryption for remote maintenance confidentiality | Approved ciphers on SSH and HTTPS management sessions |
| Idle sessions terminate after 10 minutes | Administrative idle timeout of 10 minutes or less |
| Only authorized administrators can view or change configuration and files | Administrator profiles that limit access, including to files and removable media |
| Log data sent to a central log server | Logs forwarded to FortiAnalyzer or a syslog server so alerts reach administrators and the ISSO |

The CAT II rules fill in the rest of the NDM pattern from Chapter 07: one local
account of last resort, lockout after three failed logons for 15 minutes, the
Standard Mandatory DoD Notice and Consent Banner shown until acknowledged, and a
long list of audit requirements (account creation, modification, and removal;
privileged functions; logons; administrator session start and end times).

### What the FortiGate Firewall STIG requires

The Firewall STIG implements the Firewall SRG for FortiOS. Its themes:

Its three CAT I rules require filters that use packet headers and attributes
(source and destination addresses and ports), protection of the traffic log from
unauthorized deletion, and filters that prevent or limit the effects of
commonly known denial-of-service attacks. The full set of themes:

| Theme | Typical requirements |
| --- | --- |
| **Filtering** | Filter traffic using packet headers and attributes; filter traffic according to DoD Ports, Protocols, and Services Management (PPSM) Category Assurance List rules; filter remote access VPN traffic |
| **Denial of service** | Employ DoS protection filters; block outbound DoS attacks; manage bandwidth to limit packet flooding |
| **Traffic logging** | Log event type, date and time, network location, and the outcome of each firewall rule |
| **Log protection** | Protect traffic logs from unauthorized modification and deletion; protect logs in transit to the central server; queue logs locally when the audit server is unreachable |
| **Attack surface** | Disable network services the device does not need |

### What the two FortiGate STIGs do not cover

A FortiGate often does much more than filter traffic. The two STIGs cover the
management plane and the firewall function only. Other enabled functions fall
back to their SRGs:

| FortiGate function | Applicable SRG |
| --- | --- |
| IPS sensors | Intrusion Detection and Prevention Systems (IDPS) SRG |
| SSL VPN and IPsec VPN | Virtual Private Network (VPN) SRG |
| Web filtering, application control, SSL/SSH inspection, explicit proxy | Application Layer Gateway (ALG) SRG |
| Routing (static, BGP, OSPF) | Router SRG |

If a function is not enabled, record its SRG as Not Applicable with that
justification. If it is enabled, assess it against the SRG, as in Chapter 03.

### Every other Fortinet product

The table maps the major Fortinet products to the SRGs and STIGs to start from.
It is a starting point for scoping, not a ruling: confirm applicability with
your assessor, because the right SRGs depend on how each product is deployed and
which features are enabled. Almost every product with an administrative
interface also takes the NDM SRG for its management plane, and products
delivered as a VM or software also bring the STIG for the host operating system
or hypervisor they run on.

| Product | What it does | SRGs and STIGs to start from |
| --- | --- | --- |
| **FortiGate** (hardware and VM) | Next-generation firewall | FortiGate NDM and Firewall STIGs; IDPS, VPN, ALG, and Router SRGs for enabled functions |
| **FortiManager** | Central management of FortiGates and other devices | NDM SRG; it controls the configuration of every managed device, so treat its access control and auditing as high impact. Chapter 13 maps every FortiManager feature to its release, SRG requirement, and configuration command |
| **FortiAnalyzer** | Log collection, analytics, and reporting | Central Log Server SRG and NDM SRG; it is the central log server the FortiGate STIGs depend on, so its log protection, retention, and access control matter. Chapter 12 maps every FortiAnalyzer feature to its release, SRG requirement, and configuration command |
| **FortiSwitch** | Ethernet switching, often managed by FortiGate through FortiLink | Layer 2 Switch SRG and NDM SRG; when FortiGate manages the switch through FortiLink, collect the evidence on the FortiGate. Chapter 11 maps every FortiSwitch feature to its supported releases and SRG requirement |
| **FortiAP** | Wireless access points, usually managed by FortiGate | DISA's generic Network WLAN STIGs (controller management, controller platform, and access point) plus the NDM SRG; check whether wireless is permitted in the environment at all. Chapter 14 maps every FortiAP feature to its release, WLAN STIG or SRG requirement, and configuration command |
| **FortiExtender** | Cellular WAN connectivity | NDM SRG; cellular WAN use is subject to local DoD connection approval. Chapter 15 maps every FortiExtender feature to its release, SRG requirement, and configuration command |
| **FortiWeb** | Web application firewall | ALG SRG and NDM SRG. Chapter 16 maps every FortiWeb feature to its release, SRG requirement, and configuration command |
| **FortiMail** | Email security gateway | ALG SRG and NDM SRG. Chapter 17 maps every FortiMail feature to its release, SRG requirement, and configuration command |
| **FortiProxy** | Secure web gateway | ALG SRG and NDM SRG. Chapter 18 maps every FortiProxy feature to its release, SRG requirement, and configuration command |
| **FortiADC** | Application delivery controller and load balancer | ALG SRG and NDM SRG, plus the VPN SRG if it terminates VPN or TLS for remote users. Chapter 19 maps every FortiADC feature to its release, SRG requirement, and configuration command |
| **FortiDDoS** | DDoS mitigation | NDM SRG; its filtering role relates to the Firewall SRG's DoS requirements. Chapter 20 maps every FortiDDoS feature to its release, SRG requirement, and configuration command |
| **FortiSandbox** | Malware detonation and analysis | NDM SRG; protect its threat data and integrations |
| **FortiVoice** | Business phone system and unified communications | Enterprise Voice, Video, and Messaging (EVVM) SRGs (session management, endpoint, and policy) and the NDM SRG |
| **FortiAuthenticator** | Authentication, RADIUS and LDAP services, SSO, certificates | AAA Services SRG and NDM SRG; because other devices depend on it for administrator authentication, its availability and logging carry extra weight |
| **FortiToken** | Hardware and software MFA tokens | No separate SRG; assessed as part of the authentication design of the systems that use it |
| **FortiPAM** | Privileged access management | NDM SRG and the Application Security and Development requirements that apply to the application |
| **FortiNAC** | Network access control | NDM SRG plus the requirements for the network access function; DISA publishes STIGs for other NAC products that show the expected pattern |
| **FortiSIEM** | Security information and event management | Central Log Server SRG, the NDM SRG for the appliance interface, and the operating system STIG or GPOS SRG for the underlying host |
| **FortiClient** and **FortiClient EMS** | Endpoint VPN and protection agent; its management server | The host operating system STIG for endpoints, with the VPN SRG for the client's remote-access role; the Windows Server STIG for the EMS server, with the Unified Endpoint Management (UEM) Server and Agent SRGs as the closest match for central endpoint management |
| **FortiEDR** | Endpoint detection and response | The host operating system STIG for agents; NDM and application requirements for the management console |
| **FortiSASE** | Cloud-delivered security service | The Cloud Computing SRG; confirm the offering's authorization status and impact level before use (Chapter 08) |
| **FortiGate VM in public cloud** | FortiGate on AWS, Azure, or another cloud | The FortiGate STIGs, plus the Cloud Computing SRG obligations of the hosting environment |

## Design Considerations

- **Expect to write your own SRG assessments.** Outside FortiGate, every
  Fortinet product in scope needs an SRG-based checklist (Chapter 03). Budget
  assessor time for it, and reuse the result across identical devices.
- **Run FortiOS in FIPS-CC mode where DoD requires it.** FortiOS has a FIPS-CC
  operating mode that restricts the device to FIPS-approved cryptography and
  Common Criteria-evaluated behavior. Several CAT I NDM rules depend on approved
  cryptography. Enabling FIPS-CC mode changes device behavior and can require a
  reset of the configuration, so plan it at deployment rather than retrofitting.
- **Check the DoDIN Approved Products List.** DoD networks generally require
  products listed on the DoD Information Network (DoDIN) Approved Products List.
  APL testing evaluates products against the applicable STIGs and SRGs, and many
  Fortinet products and specific firmware versions are listed. Confirm the exact
  model and firmware against the current APL entry.
- **Use the Security Fabric to keep settings consistent.** FortiManager can push
  the same STIG-aligned settings to every FortiGate and keep them from drifting.
  Remember that FortiManager then becomes one of the most sensitive systems in
  the environment.
- **Keep FortiAnalyzer in scope.** The FortiGate STIGs require central logging,
  so the FortiAnalyzer receiving those logs must itself be hardened, protected,
  and sized for retention.
- **Watch firmware lifecycles.** Running a FortiOS release outside vendor support
  is a CAT I finding. Track Fortinet's end-of-support dates for every product.

## Implementation and Automation

The FortiOS commands below show how the main FortiGate NDM requirements are
typically met. Values must match the current STIG's fix text, and command
options vary between FortiOS releases, so check them against the STIG and the
FortiOS CLI reference for your version. [Volume XIX](../../volume-019-fortinet-network-security/README.md)
covers FortiGate deployment and hardening in depth.

### Administrative sessions, lockout, and banner

```text
config system global
    set admintimeout 10
    set admin-lockout-threshold 3
    set admin-lockout-duration 900
    set pre-login-banner enable
end
```

Edit the banner text in the `pre_admin-disclaimer-text` replacement message so
it shows the Standard Mandatory DoD Notice and Consent Banner (or your
organization's approved banner):

```text
config system replacemsg admin pre_admin-disclaimer-text
    set buffer "<APPROVED_DOD_NOTICE_AND_CONSENT_BANNER_TEXT>"
end
```

### Management access limited to secure protocols

```text
config system interface
    edit "<MGMT_INTERFACE>"
        set allowaccess https ssh
    next
end
```

Remove administrative access (`allowaccess`) from every interface that is not a
management interface, and restrict each administrator account to trusted
management hosts with `trusthost` entries under `config system admin`.

### Central authentication over LDAPS

```text
config user ldap
    edit "<LDAP_SERVER_NAME>"
        set server "<LDAP_SERVER_FQDN>"
        set secure ldaps
        set ca-cert "<CA_CERTIFICATE_NAME>"
        set port 636
    next
end
```

Administrators authenticate remotely through LDAPS, RADIUS, or TACACS+, and only
one local administrator remains as the account of last resort.

### Central logging, protected in transit

```text
config log fortianalyzer setting
    set status enable
    set server "<FORTIANALYZER_IP>"
    set enc-algorithm high
end
config log setting
    set fwpolicy-implicit-log enable
end
```

Set `logtraffic all` on firewall policies that the STIG requires to be logged,
and keep local disk or memory logging enabled so logs queue when the central
server is unreachable.

### Check software currency

```text
get system status
```

Compare the reported FortiOS version with Fortinet's supported-release lifecycle
and the version listed for the device on the DoDIN APL.

## Validation and Troubleshooting

- **No SCAP benchmark exists for FortiGate.** Assessment is manual: collect
  `show full-configuration`, `get system status`, and the relevant `show` output,
  and attach it as evidence in STIG Viewer (Chapter 07).
- **A command option in the fix text does not exist on your FortiOS release.**
  The STIG may have been written against a different release. Find the
  equivalent setting for your version and record how it meets the requirement.
- **Administrators are locked out after enabling remote authentication.** Keep
  one session open while testing, and confirm the account of last resort works
  before closing it.
- **Logs stop reaching FortiAnalyzer after encryption changes.** Both ends must
  agree on the encryption level; check the FortiAnalyzer side and the source
  interface the FortiGate uses for logging.
- **FIPS-CC mode was enabled and some features stopped working.** FIPS-CC mode
  disables non-approved algorithms and some features by design. Review which
  features you rely on before enabling it in production.

## Security and Best Practices

- Treat FortiManager and FortiAnalyzer as tier-zero systems: the first controls
  every device's configuration, the second holds the evidence for every
  investigation.
- Use a dedicated management network for every Fortinet product, and remove
  administrative access from data interfaces.
- Keep firmware on supported releases listed on the DoDIN APL, and track the
  matching STIG release for FortiGate.
- Build STIG settings into FortiManager templates or configuration scripts, so
  new devices start compliant.
- Document the SRG assessment for every Fortinet product without a STIG, and
  review it each quarter alongside the FortiGate STIG updates.

## References and Knowledge Checks

**References:**

- DISA Fortinet FortiGate Firewall NDM STIG and Fortinet FortiGate Firewall
  STIG, distributed together as `U_FN_FortiGate_Firewall_Y26M10_STIG.zip` in the
  October 2026 STIG Library Compilation (DoD Cyber Exchange).
- DISA Network Device Management, Firewall, IDPS, VPN, ALG, Router, Layer 2
  Switch, AAA Services, Central Log Server, UEM, and EVVM SRGs; the Network
  WLAN STIGs; the Cloud Computing SRG.
- DoD Information Network (DoDIN) Approved Products List.
- Fortinet FortiOS documentation, including the CLI reference and FIPS-CC mode
  guidance, and Fortinet's product lifecycle information.
- [Volume XIX — Fortinet Network Security](../../volume-019-fortinet-network-security/README.md).

**Knowledge checks:**

1. Which Fortinet products have published DISA STIGs?
2. Name four of the nine CAT I rules in the FortiGate NDM STIG.
3. Which SRGs apply to a FortiGate that also runs IPS and SSL VPN?
4. How do you assess FortiManager or FortiAnalyzer when they have no STIG?
5. Why do FortiManager and FortiAnalyzer deserve extra protection in a STIG
   program?
6. What does FIPS-CC mode change, and why plan it at deployment?

## Summary and Completion Checklist

Among Fortinet products, only FortiGate has DISA STIGs: the FortiGate Firewall
NDM STIG for the management plane and the FortiGate Firewall STIG for traffic
filtering. FortiGate functions outside those STIGs (IPS, VPN, application-layer
inspection, routing) fall back to their SRGs, and every other Fortinet product
is assessed against the SRGs that match its functions, almost always starting
with the NDM SRG. FIPS-CC mode, DoDIN APL listing, supported firmware, and a
hardened FortiManager and FortiAnalyzer round out a Fortinet STIG program.

- [ ] Can name the two Fortinet STIGs and what each covers.
- [ ] Can configure the main FortiGate NDM requirements on FortiOS.
- [ ] Can map FortiGate functions outside the STIGs to their SRGs.
- [ ] Can scope the SRGs for any other Fortinet product.
- [ ] Can explain the roles of FIPS-CC mode and the DoDIN APL.
