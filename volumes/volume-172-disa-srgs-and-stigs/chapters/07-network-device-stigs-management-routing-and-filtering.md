# Chapter 07: Network Device STIGs — Management, Routing, and Filtering

## Learning Objectives

- Explain how network device STIGs are split between the management plane (NDM)
  and the traffic functions (router, firewall, ALG, IDPS, VPN).
- List the requirements that appear in nearly every NDM STIG, whatever the
  vendor.
- Describe typical router and firewall STIG requirements.
- Assess a network device manually against its STIGs, collecting evidence from
  `show` commands and configuration files.
- Fix common network device findings and verify the fixes.

## Theory and Architecture

Network devices are where STIG work is most manual. Few network STIGs have a
SCAP benchmark, devices do not run general-purpose agents, and the evidence
lives in running configurations and command output. The work is still very
structured, because every network STIG follows the SRG split from Chapter 03.

### The management plane and the traffic planes

```text
                ┌────────────────────────────────────┐
  Admin access  │  Management plane   → NDM STIG       │
  (SSH, HTTPS,  │  accounts, AAA, banners, logging,    │
   SNMP, NTP)   │  time, crypto, firmware, backups     │
                ├────────────────────────────────────┤
  User traffic  │  Traffic planes                      │
                │   routing          → Router STIG     │
                │   filtering        → Firewall STIG   │
                │   app inspection   → ALG STIG        │
                │   intrusion prev.  → IDPS STIG       │
                │   tunnels          → VPN STIG        │
                └────────────────────────────────────┘
```

Every network device gets the **NDM STIG** for its platform. Switches and
routers add Router (and, for switches, Layer 2 switch) STIGs. Firewalls add
Firewall or ALG STIGs, and IDPS and VPN STIGs when those features are used.
DISA and vendors publish this content for the major platforms, including Cisco
IOS XE and NX-OS, Juniper Junos, Palo Alto Networks, Fortinet FortiGate, F5
BIG-IP, and others. Check the library for the exact STIG names and releases for
your platform and software version. Chapter 10 covers the Fortinet portfolio in
detail, including the FortiGate STIGs and the SRGs for Fortinet products that
have no STIG.

### What nearly every NDM STIG requires

Because they all implement the same SRG, NDM STIGs from different vendors ask
for the same things in different syntax:

| Requirement | What it means in practice |
| --- | --- |
| **Centralized authentication** | Administrators authenticate through TACACS+ or RADIUS backed by the enterprise directory, ideally with MFA |
| **Account of last resort** | Exactly one local account, used only when the AAA servers are unreachable |
| **Logon banner** | The DoD Notice and Consent Banner (or your organization's equivalent) before login |
| **Session timeout** | Idle administrative sessions end after 10 minutes or less |
| **Lockout** | Accounts lock after a small number of failed logons |
| **Secure management protocols** | SSHv2 and HTTPS with FIPS-approved algorithms; Telnet, HTTP, and SNMPv1/v2c disabled |
| **Restricted management access** | Management only from defined administrative networks |
| **Authenticated time** | NTP from at least two sources, with authentication |
| **Central logging** | Logs sent to a central syslog or SIEM, with audit records for administrator actions |
| **SNMPv3** | Authentication and encryption (authPriv) if SNMP is used at all |
| **Supported, current firmware** | Vendor-supported software at a current release |
| **Configuration backup** | Regular backups of the configuration to a secure location |

### Typical router and firewall requirements

| Area | Examples |
| --- | --- |
| **Router** | Authenticated routing protocols; unicast reverse path forwarding where applicable; IP source routing, directed broadcasts, ICMP redirects, and proxy ARP disabled; control plane protection; BGP prefix limits and filtering |
| **Firewall and ALG** | Deny by default with explicit allow rules; logging of denied and permitted traffic as required; no "any any" rules; inspection enabled for the protocols that cross the boundary; the firewall fails closed |
| **IDPS** | Current signatures, updated automatically; blocking mode for defined threats; alerting to the SOC |
| **VPN** | FIPS-approved IKE and IPsec parameters; certificate-based authentication; session limits and timeouts |

## Design Considerations

- **Build STIG settings into your device templates.** Banners, AAA, timeouts,
  NTP, logging, and SNMPv3 belong in the standard configuration every new device
  receives, not a post-deployment task.
- **Design for out-of-band management.** Several NDM requirements are far easier
  to meet with a dedicated management network.
- **Plan the AAA dependency.** Centralized authentication means the AAA servers
  become critical. Keep at least two, reachable from every device, and test the
  account-of-last-resort procedure.
- **Watch firmware currency.** Unsupported firmware is a high-severity finding on
  most platforms. Track vendor end-of-support dates in your lifecycle plan.
- **Disable features you do not use.** Every enabled feature can bring another
  STIG (VPN, IDPS) and more attack surface.

## Implementation and Automation

### Collect the evidence

Manual network assessment is mostly reading configuration. Collect the running
configuration and key `show` output once per assessment, then work through the
checklist against those files:

```text
Cisco IOS XE                          FortiOS
────────────                          ───────
show running-config                   show full-configuration
show version                          get system status
show ip ssh                           show system admin
show line vty 0 15                    show system global
show ntp associations                 show system ntp
show logging                          show log syslogd setting
show snmp user                        show system snmp user
```

Save the output with the date and device name. It becomes the evidence attached
to each rule in the checklist.

### Example fixes

The syntax differs by platform, but the intent is the same. A few common NDM
settings on Cisco IOS XE:

```text
line vty 0 15
 exec-timeout 10 0
 transport input ssh
!
ip ssh version 2
banner login ^C
<APPROVED_LOGON_BANNER_TEXT>
^C
logging host <SYSLOG_SERVER_IP>
ntp authenticate
```

And on FortiOS:

```text
config system global
    set admintimeout 10
    set pre-login-banner enable
    set admin-lockout-threshold 3
end
config system password-policy
    set status enable
    set minimum-length 15
end
config log syslogd setting
    set status enable
    set server <SYSLOG_SERVER_IP>
end
```

Treat these as examples of the pattern. The STIG for your platform and software
version gives the exact required values and commands; follow its fix text. For
FortiGate specifics, see
[Volume XIX](../../volume-019-fortinet-network-security/README.md), whose
deployment and hardening chapter covers these settings in depth.

### Automating network checks

Some tools parse saved device configurations against STIG rules, including
Evaluate-STIG for supported Cisco platforms (DoD users) and commercial
configuration-audit products. Configuration management (Ansible network
modules, vendor managers such as FortiManager or Panorama) is the best way to
keep STIG settings consistent once you have them right.

## Validation and Troubleshooting

- **Locked out after enabling AAA.** Test the AAA configuration on one session
  while keeping another session open, and confirm the account of last resort
  works before closing it.
- **NTP authentication shows unsynchronized.** Key IDs and keys must match on
  both ends, and the key must be marked trusted where the platform requires it.
- **SSH clients cannot connect after crypto changes.** Older clients may not
  support the approved ciphers and key exchange algorithms. Upgrade the client.
- **Logs do not reach the SIEM.** Check the source interface or VRF the device
  uses for syslog, and the firewall rules on the path.
- **A rule refers to a feature the platform does not have.** Record the product
  limitation as a finding with mitigation, not as Not Applicable, unless the
  rule's own text says it applies only when the feature exists.

## Security and Best Practices

- Use a dedicated management network and restrict management access to it.
- Store the account-of-last-resort password in a vault, rotate it, and alert on
  its use.
- Back up configurations automatically and keep them encrypted, because they
  contain secrets and topology.
- Keep firmware on a vendor-supported, current release and track the STIG for
  that release.
- Review firewall rules on a schedule. A rule set that met the STIG at
  deployment drifts as exceptions accumulate.

## References and Knowledge Checks

**References:**

- DISA Network Device Management SRG and the Router, Firewall, ALG, IDPS, and
  VPN SRGs (DoD Cyber Exchange).
- Vendor STIGs for your platforms, from the DoD Cyber Exchange library.
- [Volume XIX — Fortinet Network Security](../../volume-019-fortinet-network-security/README.md)
  and [Volume XVI — Palo Alto Networks Security](../../volume-016-palo-alto-networks-security/README.md)
  for platform hardening detail.

**Knowledge checks:**

1. Which STIG applies to every network device, and what does it cover?
2. List six requirements that appear in nearly every NDM STIG.
3. What is the account of last resort, and how should it be protected?
4. Give three typical router STIG requirements.
5. Why are network device STIGs assessed mostly by hand?

## Summary and Completion Checklist

Network device STIGs split the management plane (NDM) from the traffic
functions (router, firewall, ALG, IDPS, and VPN). Every device gets an NDM STIG,
and NDM STIGs share the same requirements across vendors: central AAA, an
account of last resort, banners, timeouts, lockout, secure protocols, restricted
access, authenticated NTP, central logging, SNMPv3, current firmware, and
backups. Assessment is mostly manual, using saved configuration and command
output as evidence, and the best long-term fix is building STIG settings into
device templates and configuration management.

- [ ] Can explain the NDM and traffic-plane STIG split.
- [ ] Can list the common NDM requirements.
- [ ] Can describe typical router and firewall requirements.
- [ ] Can assess a device by hand with evidence.
