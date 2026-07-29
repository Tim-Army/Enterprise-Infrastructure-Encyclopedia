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

**Cleanup:**

```text
config firewall policy
    delete 1
end
```

### Lab 6.2 — Firewall objects: addresses, services, schedules (Topic: Firewall objects)

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

### Lab 6.4 — Site-to-site IPsec VPN (Topic: IPsec VPN)

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

### Lab 6.5 — SSL VPN for remote access (Topic: SSL/dial-up VPN)

**Objective:** Enable SSL VPN web/tunnel mode for remote users.

```text
config vpn ssl settings
    set servercert Fortinet_Factory
    set tunnel-ip-pools SSLVPN_TUNNEL_ADDR1
    set port 10443
    set source-interface port1
end
config firewall policy
    edit 30
        set name sslvpn-access
        set srcintf ssl.root
        set dstintf port2
        set srcaddr all
        set dstaddr all
        set action accept
        set schedule always
        set service ALL
        set groups staff
    next
end
diagnose vpn ssl list
```

**Expected result:** remote users reach `https://<wan-ip>:10443`, authenticate, and get
an IP from the tunnel pool; `diagnose vpn ssl list` shows the active session — SSL VPN
gives clientless/tunnel remote access without a site-to-site peer.

**Negative test:** enable SSL VPN settings but write no firewall policy from `ssl.root`;
users authenticate but reach nothing — the policy is what authorizes traffic off the
tunnel.

**Cleanup:** delete policy 30 and disable SSL VPN settings.

### Lab 6.6 — ZTNA access proxy (Topic: Zero Trust Network Access)

**Objective:** Publish an internal app through a ZTNA access proxy.

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
