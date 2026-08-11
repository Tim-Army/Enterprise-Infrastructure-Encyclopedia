# Chapter 06: Firewall Policy, Authentication, VPN, and Zero-Trust Access

![Lab flow for this chapter: outbound and inbound firewall policies complete the prior chapter's NAT design, confirmed by a translated source address in the session list, and a site-to-site IPsec tunnel to a second firewall peer establishes with confirmed security associations. As a negative test, the tunnel's pre-shared key is changed to an incorrect value on one side only, and the tunnel is brought up again; IKE negotiation fails and debug output explicitly reports an authentication failure, confirming the mismatch is detectable rather than failing silently. Restoring the correct key re-establishes the tunnel, and SSL VPN separately confirms a connected, authenticated session.](../../../diagrams/volume-019-fortinet-network-security/chapter-06-ipsec-psk-mismatch-flow.svg)

*Figure 6-1. Flow used throughout this chapter's Hands-On Lab: firewall policy, authentication, and site-to-site/SSL VPN configuration, tested against a deliberate pre-shared key mismatch.*

## Learning Objectives

- Explain FortiGate's sequential firewall policy match model and build
  policies using address, service, schedule, and identity objects.
- Configure local and remote (LDAP/RADIUS) authentication and user groups.
- Build a route-based site-to-site IPsec VPN and a remote-access SSL VPN.
- Describe Zero Trust Network Access (ZTNA) architecture and how it differs
  from traditional remote-access VPN.
- Diagnose firewall policy, authentication, and VPN tunnel issues.

## Theory and Architecture

### The firewall policy engine

FortiGate evaluates firewall policies **sequentially, top to bottom**,
applying the **first policy that matches** all of a session's criteria —
source/destination interface, source/destination address, service (port/
protocol), schedule, and, where applicable, user/device identity. Once a
session matches a policy, FortiGate does not continue evaluating lower
policies for that session; this makes policy ordering a functional
concern, not just a readability one. An implicit **deny-all** policy exists
at the bottom of the policy list and matches any traffic no earlier policy
matched, so a FortiGate with no explicit policies blocks all traffic by
default, consistent with a default-deny security posture.

Firewall objects keep policies readable and reusable rather than repeating
raw IPs and ports inline:

| Object type | Purpose |
| --- | --- |
| Address / address group | Named IP, subnet, FQDN, or geography-based objects |
| Service / service group | Named protocol/port definitions |
| Schedule | Time-based windows a policy is active |
| Internet Service Database (ISDB) | Fortinet-maintained, continuously updated objects identifying traffic belonging to specific named cloud services/applications by their published IP ranges, reducing manual address-object maintenance for services that change IPs frequently |
| User / user group | Identity objects used for identity-based policy matching |

### Identity: local, remote, and single sign-on authentication

FortiGate supports several authentication sources, often combined in a
single user group:

- **Local users** are created and stored directly on the FortiGate,
  suitable for small deployments or break-glass accounts.
- **Remote authentication servers** — LDAP (commonly Active Directory) and
  RADIUS — let FortiGate delegate credential verification to an existing
  directory rather than duplicating account management.
- **Fortinet Single Sign-On (FSSO)** transparently maps already-authenticated
  Active Directory sessions (via a collector agent monitoring domain
  controller logon events, or an agentless polling method) to firewall
  policy decisions, so users are identified without an explicit captive
  portal login for policies that only need identity, not interactive
  authentication.
- **SAML** enables federated single sign-on against a modern identity
  provider for SSL VPN and administrative GUI login, aligning with the
  broader SSO patterns covered in [Volume X](../../volume-010-enterprise-cybersecurity/README.md).

### VPN architectures

FortiGate supports two structurally different remote-access approaches
alongside site-to-site connectivity:

- **Route-based IPsec** creates a virtual tunnel interface (an
  `ipsec` type interface) that participates in the routing table like any
  other interface — traffic is directed into the tunnel by a route, and
  firewall policy governs the tunnel interface the same way it governs any
  physical interface. This is the modern, preferred model over legacy
  **policy-based IPsec** (which binds encryption directly to a firewall
  policy rather than creating a routable interface) because it composes
  cleanly with dynamic routing, SD-WAN ([Chapter 08](08-sd-wan-operations-central-management-automation-and-troubleshooting.md)), and multiple
  concurrent tunnels.
- **SSL VPN** provides remote-access connectivity in **tunnel mode**
  (a full network-layer VPN client, comparable in function to IPsec
  remote access) or **web mode** (browser-based, clientless access to a
  defined set of internal web applications and bookmarks) — the two modes
  address different use cases: tunnel mode for users needing broad network
  access, web mode for constrained, application-specific access without
  installing client software.
- **Dial-up IPsec** supports remote-access VPN using an IPsec client
  (such as FortiClient) instead of SSL VPN, useful where an organization
  standardizes on IPsec/IKEv2 client tooling across platforms.

### Zero Trust Network Access (ZTNA)

Traditional remote-access VPN grants broad network reachability once a
tunnel is established, trusting the connection implicitly after initial
authentication. **ZTNA** instead evaluates identity and device posture
continuously and grants access to individual applications rather than
broad network segments:

- **ZTNA access proxy** sits in front of protected applications and
  brokers every connection attempt, rather than simply routing packets
  into a trusted network zone once a tunnel is up.
- **Device posture and tags** — FortiClient (endpoint agent) reports
  device posture (OS patch level, antivirus status, disk encryption,
  domain membership, and similar signals) to **FortiClient EMS**
  (Endpoint Management Server), which assigns **ZTNA tags** to compliant
  or non-compliant devices; firewall policy can then match on these tags
  to grant or deny access to a specific application per-connection,
  re-evaluated continuously rather than only at initial login.
- **Comparison to VPN.** ZTNA reduces lateral-movement blast radius (a
  compromised endpoint cannot reach the entire network the way a
  full-tunnel VPN client can) and supports continuous re-verification
  rather than a single point-in-time authentication event; VPN remains
  simpler to deploy for scenarios that genuinely require broad,
  general-purpose network access rather than access to a defined set of
  applications.

## Design Considerations

- **Policy ordering and hygiene.** Order policies from most specific to
  least specific, and periodically audit for unused, overly broad
  ("any/any/any"), or shadowed policies (a broad policy positioned above a
  more specific one that can therefore never match); FortiOS reports
  policy hit counts that make unused-policy identification straightforward
  over time.
- **Authentication method selection.** Local users do not scale past a
  small deployment and create credential-lifecycle duplication; prefer
  LDAP/RADIUS or SAML integration with the organization's existing
  identity provider so account lifecycle (onboarding, offboarding, and
  password rotation) is managed once, centrally, rather than duplicated on
  every FortiGate.
- **Split-tunnel vs. full-tunnel VPN.** Split-tunneling (only
  organization-destined traffic traverses the VPN; general internet
  traffic exits locally at the client) reduces VPN concentrator load and
  improves general browsing performance, at the cost of losing centralized
  inspection over the client's non-tunneled traffic; full-tunnel maximizes
  visibility and control at the cost of concentrator capacity and
  potential latency for general internet use. Choose deliberately per risk
  tolerance rather than defaulting either way without review.
- **ZTNA rollout strategy.** ZTNA with FortiClient EMS device posture
  requires managed endpoints running the FortiClient agent; a mixed estate
  with unmanaged or BYOD devices needs a defined fallback (a more
  constrained web-mode SSL VPN portal, for example) rather than assuming
  agent-based ZTNA covers every access scenario on day one.
- **VPN concentrator sizing.** Both IPsec and SSL VPN throughput and
  concurrent-session capacity are bounded by the FortiGate model's licensed
  and hardware-accelerated capacity; size the remote-access concentrator
  against expected concurrent remote users, not just total employee count.

## Implementation and Automation

### Service objects and firewall policy

```text
FGT-LAB-01 # config firewall service custom
FGT-LAB-01 (custom) # edit "HTTPS-8443"
FGT-LAB-01 (HTTPS-8443) # set tcp-portrange 8443
FGT-LAB-01 (HTTPS-8443) # next
FGT-LAB-01 (custom) # end
FGT-LAB-01 # config firewall policy
FGT-LAB-01 (policy) # edit 1
FGT-LAB-01 (1) # set name "LAN-to-WAN-Outbound"
FGT-LAB-01 (1) # set srcintf "port2"
FGT-LAB-01 (1) # set dstintf "port1"
FGT-LAB-01 (1) # set srcaddr "LAN-SUBNET"
FGT-LAB-01 (1) # set dstaddr "all"
FGT-LAB-01 (1) # set service "ALL"
FGT-LAB-01 (1) # set schedule "always"
FGT-LAB-01 (1) # set action accept
FGT-LAB-01 (1) # set nat enable
FGT-LAB-01 (1) # set ippool enable
FGT-LAB-01 (1) # set poolname "WAN1-POOL"
FGT-LAB-01 (1) # set logtraffic all
FGT-LAB-01 (1) # next
FGT-LAB-01 (policy) # edit 2
FGT-LAB-01 (2) # set name "WAN-to-DMZ-WebVIP"
FGT-LAB-01 (2) # set srcintf "port1"
FGT-LAB-01 (2) # set dstintf "port3"
FGT-LAB-01 (2) # set srcaddr "all"
FGT-LAB-01 (2) # set dstaddr "DMZ-WEB-VIP"
FGT-LAB-01 (2) # set service "HTTPS"
FGT-LAB-01 (2) # set schedule "always"
FGT-LAB-01 (2) # set action accept
FGT-LAB-01 (2) # set logtraffic all
FGT-LAB-01 (2) # next
FGT-LAB-01 (policy) # end
```

Policy 1 completes the source NAT design from [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md) by attaching
`WAN1-POOL` to actual outbound traffic; policy 2 completes the destination
NAT design by permitting inbound traffic to the `DMZ-WEB-VIP` object
created in [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md) — a VIP with no permitting policy is unreachable
regardless of its own configuration.

### Local user, remote LDAP server, and user group

```text
FGT-LAB-01 # config user local
FGT-LAB-01 (local) # edit "svc-breakglass"
FGT-LAB-01 (svc-breakglass) # set type password
FGT-LAB-01 (svc-breakglass) # set passwd <STRONG_PASSWORD>
FGT-LAB-01 (svc-breakglass) # next
FGT-LAB-01 (local) # end
FGT-LAB-01 # config user ldap
FGT-LAB-01 (ldap) # edit "CORP-AD"
FGT-LAB-01 (CORP-AD) # set server "10.10.10.20"
FGT-LAB-01 (CORP-AD) # set cnid "sAMAccountName"
FGT-LAB-01 (CORP-AD) # set dn "dc=nse-lab,dc=example"
FGT-LAB-01 (CORP-AD) # set type regular
FGT-LAB-01 (CORP-AD) # set username "svc-ldap-bind@nse-lab.example"
FGT-LAB-01 (CORP-AD) # set password <BIND_ACCOUNT_PASSWORD>
FGT-LAB-01 (CORP-AD) # next
FGT-LAB-01 (ldap) # end
FGT-LAB-01 # config user group
FGT-LAB-01 (group) # edit "VPN-Users"
FGT-LAB-01 (VPN-Users) # set member "CORP-AD" "svc-breakglass"
FGT-LAB-01 (VPN-Users) # next
FGT-LAB-01 (group) # end
```

### Route-based site-to-site IPsec VPN

```text
FGT-LAB-01 # config vpn ipsec phase1-interface
FGT-LAB-01 (phase1-interface) # edit "to-Branch02"
FGT-LAB-01 (to-Branch02) # set interface "port1"
FGT-LAB-01 (to-Branch02) # set ike-version 2
FGT-LAB-01 (to-Branch02) # set peertype any
FGT-LAB-01 (to-Branch02) # set net-device disable
FGT-LAB-01 (to-Branch02) # set proposal aes256-sha256
FGT-LAB-01 (to-Branch02) # set dhgrp 14
FGT-LAB-01 (to-Branch02) # set remote-gw 198.51.100.50
FGT-LAB-01 (to-Branch02) # set psksecret <STRONG_PRESHARED_KEY>
FGT-LAB-01 (to-Branch02) # next
FGT-LAB-01 (phase1-interface) # end
FGT-LAB-01 # config vpn ipsec phase2-interface
FGT-LAB-01 (phase2-interface) # edit "to-Branch02-p2"
FGT-LAB-01 (to-Branch02-p2) # set phase1name "to-Branch02"
FGT-LAB-01 (to-Branch02-p2) # set proposal aes256-sha256
FGT-LAB-01 (to-Branch02-p2) # set dhgrp 14
FGT-LAB-01 (to-Branch02-p2) # set src-subnet 10.10.10.0 255.255.255.0
FGT-LAB-01 (to-Branch02-p2) # set dst-subnet 10.20.10.0 255.255.255.0
FGT-LAB-01 (to-Branch02-p2) # next
FGT-LAB-01 (phase2-interface) # end
FGT-LAB-01 # config router static
FGT-LAB-01 (static) # edit 2
FGT-LAB-01 (2) # set dst 10.20.10.0 255.255.255.0
FGT-LAB-01 (2) # set device "to-Branch02"
FGT-LAB-01 (2) # next
FGT-LAB-01 (static) # end
FGT-LAB-01 # config firewall policy
FGT-LAB-01 (policy) # edit 3
FGT-LAB-01 (3) # set name "LAN-to-Branch02-VPN"
FGT-LAB-01 (3) # set srcintf "port2"
FGT-LAB-01 (3) # set dstintf "to-Branch02"
FGT-LAB-01 (3) # set srcaddr "LAN-SUBNET"
FGT-LAB-01 (3) # set dstaddr "all"
FGT-LAB-01 (3) # set service "ALL"
FGT-LAB-01 (3) # set schedule "always"
FGT-LAB-01 (3) # set action accept
FGT-LAB-01 (3) # set logtraffic all
FGT-LAB-01 (3) # next
FGT-LAB-01 (policy) # edit 4
FGT-LAB-01 (4) # set name "Branch02-to-LAN-VPN"
FGT-LAB-01 (4) # set srcintf "to-Branch02"
FGT-LAB-01 (4) # set dstintf "port2"
FGT-LAB-01 (4) # set srcaddr "all"
FGT-LAB-01 (4) # set dstaddr "LAN-SUBNET"
FGT-LAB-01 (4) # set service "ALL"
FGT-LAB-01 (4) # set schedule "always"
FGT-LAB-01 (4) # set action accept
FGT-LAB-01 (4) # set logtraffic all
FGT-LAB-01 (4) # next
FGT-LAB-01 (policy) # end
```

A route-based tunnel requires policies in **both directions** because the
tunnel interface is treated like any other interface — one policy alone
only permits traffic entering the tunnel, not returning from it.

### SSL VPN remote access with local authentication and MFA

```text
FGT-LAB-01 # config vpn ssl settings
FGT-LAB-01 (settings) # set servercert "Fortinet_Factory"
FGT-LAB-01 (settings) # set tunnel-ip-pools "SSLVPN_TUNNEL_ADDR1"
FGT-LAB-01 (settings) # set source-interface "port1"
FGT-LAB-01 (settings) # set source-address "all"
FGT-LAB-01 (settings) # set port 10443
FGT-LAB-01 (settings) # config authentication-rule
FGT-LAB-01 (authentication-rule) # edit 1
FGT-LAB-01 (1) # set groups "VPN-Users"
FGT-LAB-01 (1) # set portal "full-access"
FGT-LAB-01 (1) # next
FGT-LAB-01 (authentication-rule) # end
FGT-LAB-01 (settings) # end
FGT-LAB-01 # config vpn ssl web portal
FGT-LAB-01 (portal) # edit "full-access"
FGT-LAB-01 (full-access) # set tunnel-mode enable
FGT-LAB-01 (full-access) # set split-tunneling enable
FGT-LAB-01 (full-access) # set split-tunneling-routing-address "LAN-SUBNET"
FGT-LAB-01 (full-access) # next
FGT-LAB-01 (portal) # end
FGT-LAB-01 # config firewall policy
FGT-LAB-01 (policy) # edit 5
FGT-LAB-01 (5) # set name "SSLVPN-to-LAN"
FGT-LAB-01 (5) # set srcintf "ssl.root"
FGT-LAB-01 (5) # set dstintf "port2"
FGT-LAB-01 (5) # set srcaddr "SSLVPN_TUNNEL_ADDR1"
FGT-LAB-01 (5) # set dstaddr "LAN-SUBNET"
FGT-LAB-01 (5) # set service "ALL"
FGT-LAB-01 (5) # set schedule "always"
FGT-LAB-01 (5) # set action accept
FGT-LAB-01 (5) # set logtraffic all
FGT-LAB-01 (5) # next
FGT-LAB-01 (policy) # end
```

### ZTNA access proxy (illustrative)

```text
FGT-LAB-01 # config firewall access-proxy
FGT-LAB-01 (access-proxy) # edit "ztna-corp-apps"
FGT-LAB-01 (ztna-corp-apps) # set vip "DMZ-WEB-VIP"
FGT-LAB-01 (ztna-corp-apps) # next
FGT-LAB-01 (access-proxy) # end
```

Full ZTNA deployment additionally requires FortiClient EMS to issue device
posture tags and a corresponding `ztna-ems-tag` match condition on the
permitting firewall policy; provisioning FortiClient EMS itself is outside
this lab's scope and is addressed at a design level only in this chapter.

## Validation and Troubleshooting

- **Policy match troubleshooting.** `diagnose debug flow filter` combined
  with `diagnose debug flow show console enable` and `diagnose debug
  enable` traces a live session through policy lookup, NAT, and routing
  decisions in real time — the single most useful tool for "why is this
  traffic being blocked/allowed unexpectedly" investigations.
- **Policy hit counters.** `diagnose firewall iprope show` (or the GUI
  policy list's hit-count column) identifies unused policies, supporting
  the policy-hygiene design guidance above.
- **IPsec tunnel state.** `diagnose vpn tunnel list` shows phase1/phase2
  status; `diagnose vpn ike log-filter` combined with
  `diagnose debug application ike -1` traces IKE negotiation in detail,
  the correct tool for phase1/phase2 proposal mismatches, wrong
  pre-shared keys, or peer-ID mismatches that prevent tunnel
  establishment.
- **SSL VPN session state.** `get vpn ssl monitor` lists active SSL VPN
  sessions and their source IP, useful both for validating successful
  connections and for incident investigation.
- **Common phase1/phase2 mismatch.** The single most frequent site-to-site
  IPsec failure is a proposal (encryption/hash/DH group) or subnet
  mismatch between the two peers — both sides must agree exactly on
  phase1 and phase2 parameters, and `diagnose debug application ike -1`
  output explicitly names which proposal failed to match.
- **NAT-T (NAT traversal) issues.** If either IPsec peer sits behind a
  NAT device, confirm UDP 4500 is not blocked upstream; a tunnel that
  negotiates phase1 successfully but fails to pass phase2 traffic through
  an intermediate NAT device is a common variant of this failure.

## Security and Best Practices

- End every policy set with an explicit review of the implicit deny —
  confirm no unintended broad "any/any/any" policy exists above it, and
  enable logging on the deny policy itself (or a final explicit deny
  policy with logging) so blocked traffic is visible for investigation.
- Require MFA on VPN authentication (SSL VPN and dial-up IPsec) for the
  same reasons established in [Chapter 01](01-nse-1-cybersecurity-awareness-and-digital-safety.md) — a leaked password alone should
  not be sufficient to establish a tunnel into the internal network.
- Avoid weak or deprecated IKE/IPsec proposals — do not configure DES,
  3DES, or MD5-based proposals on new tunnels; use AES-256 with SHA-256 or
  stronger and Diffie-Hellman group 14 or higher, as shown in this
  chapter's examples.
- Prefer ZTNA over full-tunnel VPN for application-specific remote access
  where FortiClient EMS and managed endpoints are available — it reduces
  lateral-movement blast radius and enforces continuous posture
  verification rather than a single login-time check.
- Set explicit SSL VPN and IPsec idle timeouts appropriate to the
  organization's risk tolerance, and review active session lists
  (`get vpn ssl monitor`, `diagnose vpn tunnel list`) periodically for
  sessions that should not still be active.

## References and Knowledge Checks

**References**

- [Fortinet, *FortiOS Administration Guide*](https://docs.fortinet.com/product/fortigate/8.0.0) — firewall policy,
  authentication, IPsec VPN, SSL VPN, and ZTNA.
- [Fortinet, *FortiOS CLI Reference*](https://docs.fortinet.com/document/fortigate/8.0.0/cli-reference/84566/fortios-cli-reference) — `config firewall policy`,
  `config user group`, `config vpn ipsec phase1-interface`,
  `config vpn ssl settings`, `config firewall access-proxy`.
- [Fortinet NSE Training Institute, *NSE 4: FortiGate Security* course
  (firewall policy, authentication, SSL VPN, and Zero Trust Access
  domains).](https://training.fortinet.com/local/staticpage/view.php?page=nse_4)
- [SOFTWARE_VERSIONS.md](../../../SOFTWARE_VERSIONS.md) — FortiOS 7.6.x
  baseline used throughout this volume.

**Knowledge checks**

1. Why does FortiGate's sequential, first-match policy model make policy
   ordering a functional concern rather than only a readability concern?
2. Why does a route-based IPsec tunnel require firewall policies in both
   directions, unlike a simpler default-route scenario?
3. Name two differences between SSL VPN tunnel mode and web mode, and one
   scenario better suited to each.
4. How does ZTNA's continuous device-posture evaluation differ from a
   traditional VPN's point-in-time authentication model?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **each task under the NSE 4
objectives *Firewall Policies and Authentication* (20–25%) and *VPNs* (10–15%)** —
mapped in the volume README's coverage tables. Every command is a real FortiOS 7.6 CLI
action; each lab ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 6.1–6.6** — a FortiGate on FortiOS 7.6 with a WAN and
LAN interface, a client host, and (for the VPN labs) a peer FortiGate or a remote
client. **Cost:** none beyond lab resources.

### Lab 6.1 — Firewall policy and policy order (Topic: Firewall policies)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Write an allow policy and observe top-down matching.

```text
config firewall policy
    edit 1
        set name allow-web
        set srcintf port2
        set dstintf port1
        set srcaddr all
        set dstaddr all
        set action accept
        set schedule always
        set service HTTP HTTPS DNS
        set nat enable
        set logtraffic all
    next
end
diagnose firewall iprope lookup 10.10.10.20 5000 8.8.8.8 443 6 port2
```

**Expected result:** the lookup resolves to policy `1` and permits the flow; FortiOS
evaluates policies **top-down and stops at the first match** — the implicit deny at the
bottom drops everything unmatched.

**Negative test:** place a broad `deny all` above `allow-web`; the web policy is never
reached and traffic is blocked — policy order, not just content, decides the outcome.

**Gotcha — `iprope lookup` does not evaluate ICMP (FortiOS 7.6):** the tool resolves TCP
and UDP flows (protocol `6`/`17`), but **rejects ICMP (protocol `1`)**, failing with
`Command fail. Return code -16` no matter how the type and code are encoded in the port
fields. A ping-only policy therefore cannot be confirmed this way — verify it with a live
ping (a data-plane test) instead. The restriction has a useful flip side: run the lookup
with a service your policy does *not* cover — say `TCP/80` against a ping-only rule — and it
resolves to `policy id: 0`, the implicit deny, which is a fast way to prove least-privilege
segmentation is holding before any host is even on the wire.

```text
config firewall policy
    delete 1
end
```

### Lab 6.2 — Firewall objects: addresses, services, schedules (Topic: Firewall objects)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Build reusable objects and reference them in a policy.

```text
config firewall address
    edit web-servers
        set subnet 10.10.10.48 255.255.255.240
    next
end
config firewall service custom
    edit APP-8443
        set tcp-portrange 8443
    next
end
config firewall schedule recurring
    edit business-hours
        set day monday tuesday wednesday thursday friday
        set start 08:00
        set end 18:00
    next
end
```

**Expected result:** an address group, a custom service, and a time schedule usable by
any policy — objects centralize definitions so a change propagates everywhere they are
referenced.

**Negative test:** hard-code IPs and ports directly into dozens of policies; a subnet
change means editing each one — objects exist precisely to avoid that.

**Cleanup:** delete the three objects after use.

### Lab 6.3 — Firewall authentication (Topic: Authentication)

**Eval FortiGate — capable.** Runs on the free/licensed evaluation FortiGate-VM as-is.

**Objective:** Require user authentication on a policy via a local user group.

```text
config user local
    edit alice
        set type password
        set passwd <strong-password>
    next
end
config user group
    edit staff
        set member alice
    next
end
config firewall policy
    edit 5
        set name auth-web
        set srcintf port2
        set dstintf port1
        set srcaddr all
        set dstaddr all
        set action accept
        set schedule always
        set service HTTP HTTPS
        set groups staff
        set nat enable
    next
end
diagnose firewall auth list
```

**Expected result:** users hitting the policy are challenged; after login `diagnose
firewall auth list` shows the authenticated session bound to `alice` — identity-based
policy ties access to who the user is, not just their IP.

**Negative test:** expect the policy to match before the user authenticates; unauth
traffic falls through to the next policy or the implicit deny — the `groups` binding
gates the match on successful auth.

**Cleanup:** delete policy 5, the group, and the user.

#### Building the GUI client that completes the captive-portal challenge

Firewall authentication is finished by the *user*, in a browser. The first
time an unauthenticated session matches the `auth-web` policy, the FortiGate
intercepts the HTTP request and returns a **captive-portal** login page — a
headless host cannot complete that exchange, so the lab needs one graphical
client on the protected VLAN (`port2`/VLAN 200 in
[Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md)).
Any desktop with a browser works; the walkthrough below builds a minimal
Ubuntu 24.04 workstation on the KVM/Proxmox lab host used elsewhere in this
volume.

**1. Create the VM from an Ubuntu cloud image, placed on the VLAN behind the
FortiGate.** cloud-init sets the login user and a static address whose
gateway is the FortiGate's VLAN-200 interface:

```bash
# on the hypervisor
wget -O noble.img \
  https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
qm create 210 --name ubuntu-ws --memory 4096 --cores 2 \
    --net0 virtio,bridge=vmbr2,tag=200 --serial0 socket --vga std
qm importdisk 210 noble.img local-lvm
qm set 210 --scsi0 local-lvm:vm-210-disk-0 --boot order=scsi0
qm set 210 --ide2 local-lvm:cloudinit \
    --ciuser labuser --cipassword '<lab-password>' \
    --ipconfig0 ip=10.200.0.20/24,gw=10.200.0.1 --nameserver 8.8.8.8
qm disk resize 210 scsi0 20G
qm start 210
```

**2. Install a desktop and a browser with autologin.** Drive the serial
console (`qm terminal 210`), log in as `labuser`, then:

```bash
sudo apt-get update
sudo apt-get install -y xfce4 xfce4-goodies lightdm
sudo systemctl set-default graphical.target
sudo install -d /etc/lightdm/lightdm.conf.d
sudo tee /etc/lightdm/lightdm.conf.d/50-autologin.conf >/dev/null <<'EOF'
[Seat:*]
autologin-user=labuser
autologin-user-timeout=0
EOF
sudo groupadd -f autologin && sudo gpasswd -a labuser autologin
```

> **Gotcha — the default `firefox` is a snap that will not launch here.** On
> Ubuntu 24.04, `apt install firefox` pulls a *transitional* package that
> installs the Firefox **snap**. In a minimal VM the snap fails at launch
> with `cannot change mount namespace ... would affect the host in
> /var/lib/snapd` and exits immediately — the browser window never appears.
> Removing the snap can itself hang if a Firefox process is still running or
> snapd is wedged, so kill any `firefox` first, then mask snapd.

Install the real **.deb** from the Mozilla Team PPA and pin it so APT
prefers it over the snap-transitional package:

```bash
sudo systemctl mask --now snapd.service snapd.socket   # stop snap interfering
sudo apt-get purge -y firefox                          # drop the snap wrapper
sudo add-apt-repository -y ppa:mozillateam/ppa
printf 'Package: *\nPin: release o=LP-PPA-mozillateam\nPin-Priority: 1001\n' \
  | sudo tee /etc/apt/preferences.d/mozilla-firefox
sudo apt-get update && sudo apt-get install -y firefox
readlink -f "$(which firefox)"   # -> /usr/lib/firefox/firefox.sh, NOT /snap/bin
```

> **Gotcha — an `apt` upgrade can drop you back to the login greeter.** With
> `needrestart` in automatic mode, a `dist-upgrade` restarts `lightdm`,
> which ends the autologin session and returns to the greeter;
> `autologin-user-timeout=0` only re-fires on a fresh boot, so **reboot**
> the VM after a large upgrade to bring the desktop back automatically. For
> headless checks, capture the VGA framebuffer from the hypervisor
> (`qm monitor 210` then `screendump /tmp/ws.ppm`) instead of relying on the
> serial console, which shows only text.

**3. Complete the challenge.** With the XFCE desktop up (Proxmox noVNC, or a
`screendump`), open Firefox and browse to any HTTP site that matches the
`auth-web` policy. The FortiGate returns the captive-portal login; sign in
as `alice`, and the requested page loads. Back on the FortiGate,
`diagnose firewall auth list` now shows the session bound to `alice` —
the same result as the CLI walkthrough above, driven end to end through a
real browser.

#### How the captive-portal challenge works end to end

The `auth-web` policy does more than "prompt for a password" — it drives a
specific redirect-and-POST exchange worth understanding, because it explains
the design choices in the client build above.

**Interception.** An unauthenticated HTTP request that matches the policy is
intercepted by the FortiGate, which answers with a small HTML page that
redirects the browser to its captive portal on the ingress interface:

```text
<script>window.location="http://10.200.0.1:1000/fgtauth?<magic>";</script>
```

`10.200.0.1` is the port2 (VLAN 200) address the client already uses as its
gateway, `1000` is the active-authentication port, and `<magic>` is a
one-time token binding this login attempt to this request.

**The portal form.** The browser loads `…/fgtauth?<magic>` and receives the
Fortinet **"Authentication Required"** page: a form that POSTs back to the
same host with four fields — the hidden `4Tredir` (the original URL to return
to), the hidden `magic`, and the `username` and `password` the user types.

**Authentication and binding.** On a correct password the FortiGate replies
`303 See Other` with `Location:` set to the original destination, and binds
an authenticated session to the client's **source IP**:

```text
FGT # diagnose firewall auth list
10.200.0.20, alice
    type: fw, ... expire: 268, allow-idle: 300
    group_name: staff
----- 1 listed, 0 filtered ------
```

Because the binding is per source IP, every subsequent session from
`10.200.0.20` — any application, not just the browser — is treated as
authenticated until the session times out or idles past `allow-idle`.

> **Gotcha — DNS is blocked before login.** The same policy that forces
> authentication also blocks the client's DNS, so a browser cannot even
> resolve `example.com` to begin the exchange. Two clean options: browse to
> an HTTP **IP address** (for example `http://1.1.1.1`) so the FortiGate
> intercepts TCP 80 directly with no name lookup — which is why the client
> walkthrough tests against an IP — or add a narrow policy **above** the
> `auth-web` policy that permits `DNS` with no `groups`, so name resolution
> works pre-login and users can browse to hostnames. After a successful login
> every protocol, DNS included, flows through the authenticated policy.

Two settings tune the behavior:

```text
config user setting
    set auth-timeout 30        # minutes an authenticated session lasts
    set auth-type http https   # protocols that trigger active authentication
end
```

For guest-network-style enforcement the portal can instead be enabled on the
interface itself (`config system interface` → `set security-mode
captive-portal`); the policy-plus-group method shown here is the standard way
to make identity a match condition on a specific firewall rule.

**Clean up** by reversing the three bindings — remove the group from the
policy first, since a group cannot be deleted while a policy still references
it:

```text
config firewall policy
    edit 5
        unset groups
    next
end
config user group
    delete staff
end
config user local
    delete alice
end
diagnose firewall auth clear
```

#### Watching logins succeed and fail in the event log

`diagnose firewall auth list` shows only **active, successful** sessions — a
rejected login never creates one, so failed attempts never appear there.
Every attempt, pass or fail, is instead written to the **event log, subtype
`user`**.

**From the CLI**, filter the event log and display it:

```text
FGT # execute log filter reset
FGT # execute log filter category 1            # 1 = event log
FGT # execute log filter field subtype user    # authentication events
FGT # execute log display
```

To see only failures, add the failed-authentication log ID before
displaying (run `execute log filter reset` afterward so later displays are
not stuck on the filter):

```text
FGT # execute log filter field logid 0102043009   # "Authentication failed"
FGT # execute log display
```

A rejected password reads like this — note it carries the `srcip`,
`policyid`, and `user`, so you can see exactly who failed against which
policy:

```text
logid="0102043009" subtype="user" logdesc="Authentication failed"
srcip=10.200.0.20 policyid=2 interface="port2" user="alice" group="N/A"
action="authentication" status="failure" reason="invalid username/password"
msg="User alice failed in authentication"
```

The user-event log IDs worth recognizing:

| logid | Event |
|-------|-------|
| `0102043008` | Authentication **success** |
| `0102043009` | Authentication **failed** |
| `0102043039` / `0102043040` | Auth **logon** / **logout** |
| `0102043037` | Auth session **flush** (for example, `diagnose firewall auth clear`) |

**From the GUI**, the same records are under **Log & Report → System
Events**; on FortiOS 7.6 choose **User Events** from the event-type
selector (there is no separate "User Events" item in the left menu). Two
settings commonly hide them: the **time range** — widen it past the default
hour to cover the attempt — and the **log source**. This appliance logs to
**disk** (`get log disk setting` shows `status: enable`) with memory logging
disabled, so select **Disk**, not Memory; on a device with only memory
logging you would choose the opposite.

**Three outcomes, three behaviors.** Driving the portal from the client
shows the FortiGate handles the two failure cases differently:

| Attempt | FortiGate response | Logged | `auth list` |
|---------|--------------------|--------|-------------|
| valid user + correct password | `303` redirect to the requested site | success `0102043008` | user listed |
| valid user + **wrong password** | re-serves the "Authentication Failed" form | failure `0102043009` | empty |
| **unknown username** + any password | empty HTTP response (browser shows a blank/error page) | no failure event | empty |

Both failure rows deny access, but only a *known* user with a bad password
produces a `0102043009` record; an unknown username is dropped without a
failed-authentication log — worth knowing when you are hunting for failed
logins and an attempt seems to be missing.

### Lab 6.4 — Site-to-site IPsec VPN (Topic: IPsec VPN)

**Eval FortiGate — capable (limited crypto).** A site-to-site IPsec tunnel builds and comes up on the eval, but an evaluation-licensed VM is **low-encryption (DES-only)** and cannot negotiate strong (AES) proposals — restrict the phase-1/2 ciphers accordingly; production uses AES-GCM.

**Objective:** Build a route-based IPsec tunnel to a peer.

```text
config vpn ipsec phase1-interface
    edit to-branch
        set interface port1
        set remote-gw 198.51.100.10
        set proposal aes256-sha256
        set psksecret <shared-key>
    next
end
config vpn ipsec phase2-interface
    edit to-branch-p2
        set phase1name to-branch
    next
end
config router static
    edit 100
        set dst 172.16.20.0 255.255.255.0
        set device to-branch
    next
end
diagnose vpn tunnel list name to-branch
```

**Expected result:** phase-1 and phase-2 negotiate, `diagnose vpn tunnel list` shows
the tunnel `up` with SAs installed, and traffic to `172.16.20.0/24` routes over the
virtual interface — a route-based IPsec tunnel connects two sites.

**Negative test:** mismatch the pre-shared key or proposal between peers; phase-1 fails
and the tunnel stays down — both ends must agree on authentication and encryption.

**Cleanup:** delete the static route, phase-2, and phase-1.

#### Standing up the tunnel between two FortiGates — the gotchas that bite

Building this tunnel between two live FortiGate-VMs surfaces four things the
bare configuration above does not warn you about.

**The evaluation license is low-encryption only — DES, not AES.** On an
eval-licensed FortiGate-VM, `set proposal aes256-sha256` is rejected, and
the only proposals offered are `des-*`:

```text
FGT (to-fgt1) # set proposal aes256-sha256
command parse error before 'aes256-sha256'
Command fail. Return code -61
FGT (to-fgt1) # set proposal ?
des-md5  des-sha1  des-sha256  des-sha384  des-sha512
```

Use `des-sha256` on both Phase 1 and Phase 2. Two eval boxes share the same
limit, so DES matches automatically — which is exactly why a second
FortiGate is a cleaner lab peer than a general-purpose IPsec stack that
(rightly) deprecates single-DES.

**A route-based tunnel will not come up without a firewall policy that
references the tunnel interface.** With everything else correct, IKE refuses
to establish, and `diagnose debug application ike -1` shows the reason:

```text
ike ...:to-fgt1: ignoring request to establish IPsec SA, no policy configured
```

Add at least one policy with the tunnel interface as source or destination
on each peer (for example `srcintf port3, dstintf to-fgt2`) and the SA
establishes. This is the most common reason a freshly configured route-based
tunnel stays down.

**Bring it up with `auto-negotiate` — the static route is only active once
the tunnel is.** A route pointing at a tunnel interface is installed only
after the tunnel comes up, so a ping meant to *trigger* the tunnel can leak
out the default route and never signal IKE. Setting `set auto-negotiate
enable` under `config vpn ipsec phase2-interface` makes the FortiGate build
the tunnel proactively, independent of traffic:

```text
FGT # diagnose vpn ike gateway clear name to-fgt1     # force a fresh attempt
FGT # diagnose vpn ike gateway list
  name: to-fgt1
  IKE SA: created 1/1  established 1/1
  IPsec SA: created 1/1  established 1/1
  proposal: des-sha256
FGT # get vpn ipsec tunnel summary
'to-fgt1' ...  selectors(total,up): 1/1  rx(pkt,err): 25/0  tx(pkt,err): 5/0
```

`selectors(total,up): 1/1` plus a climbing `tx`/`rx` packet count confirms
traffic is being encrypted over the tunnel. A ping across the protected
subnets is the end-to-end proof — the target's ingress interface needs
`allowaccess ping` (or a real host behind it) to answer.

**The negative test has a specific signature.** Change the pre-shared key on
one peer only: the responder — not the initiator — reports the reason, while
the initiator simply retransmits Phase 1:

```text
# responder, from diagnose debug application ike -1:
ike 0:to-fgt2: responder: main mode get 3rd message...
ike 0:to-fgt2: parse error
ike 0:to-fgt2: probable pre-shared secret mismatch

# initiator:
ike 0:to-fgt1:7: sent IKE msg (P1_RETRANSMIT): ...
```

`get vpn ipsec tunnel summary` then shows `selectors(total,up): 1/0` — the
selector exists but is down. Restore the matching key and a `diagnose vpn
ike gateway clear` brings it back to `1/1`. The pre-shared key authenticates
each peer's identity, so no amount of matching proposals, selectors, or
routes compensates for a mismatched key.

### Lab 6.5 — SSL VPN for remote access (Topic: SSL/dial-up VPN)

**Eval FortiGate — capable (limited crypto).** SSL VPN runs on the eval with the low-encryption cipher set; the strong (AES) suites a production portal uses need a licensed FortiGate.

> **FortiOS 7.6 change — SSL VPN *tunnel mode* has been removed.** Verified
> on FortiGate-VM 7.6.7: a portal no longer accepts `set tunnel-mode enable`
> (the keyword is gone), the tunnel plumbing such as `tunnel-ip-pools` and
> `split-tunneling` is absent, and web mode has been rebranded **"Agentless
> VPN."** Fortinet is deliberately retiring SSL VPN in favor of IPsec and
> ZTNA, so a tunnel-mode walkthrough no longer applies to current firmware —
> this lab has been replaced by the note below.

**What remains, and what to use instead:**

- **Clientless (Agentless) web VPN** still exists for browser-based access
  to internal web, RDP, SSH, and SMB resources. A remote user browses to
  `https://<wan-ip>:10443`, authenticates against a user group bound to the
  built-in `web-access` portal by an SSL-VPN authentication rule, and works
  through the portal; `diagnose vpn ssl list` shows the active web session.
  On an evaluation license the portal count is capped at one, so you modify
  the existing `web-access` portal rather than adding your own (`edit
  "<new>"` fails with "reached the maximum number of entries").
- **Full-tunnel remote access** — the job tunnel mode used to do — moves to
  **IPsec dial-up** (the Phase 1 / Phase 2 mechanics of Lab 6.4 with a
  dial-up peer instead of a static site-to-site peer) or to **ZTNA** in
  Lab 6.6, which is Fortinet's strategic replacement for client VPN.

**Takeaway:** on FortiOS 7.6 and later, "SSL VPN" means clientless Agentless
web access only. If you need a routed tunnel for roaming users, reach for
IPsec dial-up or ZTNA — do not build lab or production designs around SSL VPN
tunnel mode.

### Lab 6.6 — ZTNA access proxy (Topic: Zero Trust Network Access)

**Eval FortiGate — licensed-only.** The ZTNA access proxy needs **strong encryption** for the FortiGate↔EMS TLS (the eval is DES-only) and **FortiClient EMS** for client certificates and device tags — see the lab-environment note below. On the eval, read and design.

**Objective:** Publish an internal app through a ZTNA access proxy.

> **Lab environment note — this leg needs strong encryption.** The FortiGate-to-EMS
> Security Fabric connector that feeds this access proxy its device-posture tags and
> client-certificate trust is an HTTPS/TLS session that requires **strong (AES) encryption**.
> The free **evaluation FortiGate-VM license is low-encryption (DES-only)** — confirmed on
> both FortiOS 7.6 and 8.0 evaluation builds, where `strong-crypto` is not an available
> command and IPsec/TLS proposals offer only DES. A current EMS (Apache on OpenSSL 3.x)
> refuses every cipher weaker than AES, so an eval FortiGate never completes the TLS
> handshake to EMS (it drops the connection before sending a ClientHello) and the connector
> never comes up — leaving the proxy with no posture data. Running this lab end to end
> therefore requires a **properly licensed FortiGate** (a paid BYOL license or a FortiFlex
> entitlement); the EMS server and FortiClient endpoint enrollment themselves run on any
> license and are unaffected.

```text
config firewall vip
    edit ztna-web
        set type access-proxy
        set extip 203.0.113.90
        set extintf port1
        set server-type https
        set extport 443
    next
end
config firewall access-proxy
    edit ztna-web
        set vip ztna-web
        config api-gateway
            edit 1
                config realservers
                    edit 1
                        set ip 10.10.10.50
                        set port 443
                    next
                end
            next
        end
    next
end
diagnose firewall access-proxy list 2>/dev/null | head
```

**Expected result:** the app is reached through the access proxy, which checks device
posture (FortiClient EMS tags) and identity on every request — ZTNA replaces implicit
VPN trust with per-session, posture-aware authorization.

**Negative test:** treat ZTNA like a VPN and grant standing network access; that
reintroduces the flat-trust model ZTNA exists to eliminate — access is per-session and
re-evaluated.

**Cleanup:** delete the access-proxy and the VIP.

## Lab Verification

Complete this sign-off once the lab has been run end to end, including the
negative test. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

This chapter completed the NAT design from [Chapter 05](05-interfaces-routing-nat-virtual-domains-and-high-availability.md) with permitting
firewall policies, added local and remote authentication with a user
group, and built both a route-based site-to-site IPsec VPN and a
remote-access SSL VPN, validated with a deliberate pre-shared key mismatch
negative test. It also introduced ZTNA architecture as the modern
alternative to broad-access VPN for application-specific remote access.
[Chapter 07](07-fortiguard-security-profiles-ssl-inspection-and-threat-prevention.md) attaches FortiGuard security profiles and SSL inspection to the
policies built here, turning permit/deny decisions into fully inspected,
threat-aware traffic handling.

- [ ] Can explain FortiGate's sequential firewall policy match model and
      the implicit deny.
- [ ] Can configure local and LDAP/RADIUS authentication with a user
      group.
- [ ] Can build and validate a route-based site-to-site IPsec VPN,
      including both required policy directions.
- [ ] Can configure SSL VPN remote access and describe ZTNA's
      architectural difference from traditional VPN.
- [ ] Completed the hands-on lab, including the negative test.
