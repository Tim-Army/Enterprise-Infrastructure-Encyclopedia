# Chapter 06: CCA-AppDS-Gateway — Secure Remote Access

## Learning Objectives

- Cover the Gateway exam's specific modules: NetScaler Gateway, authentication, end-user access, CVAD integration, AppExpert, content switching, and troubleshooting.
- Build the Gateway ICA-proxy pattern that fronts a Citrix Virtual Apps and Desktops site.
- Complete a walkthrough lab per module.

## The exam in brief

**Certification:** CCA-AppDS via the *NetScaler 14.x Essentials and NetScaler Gateway* exam. 60–70 questions, ~10% performance-based, English + Japanese, no prerequisites. **Recommended courses:** CNS-225 *NetScaler Essentials and Unified Gateway* or NS-232 *NetScaler Gateway*. Foundation modules (networking, HA, LB, SSL) are in [Chapter 05](05-appds-netscaler-platform-and-load-balancing.md); this chapter covers the Gateway-specific seven.

## Hands-On Lab

Walkthroughs use the NetScaler CLI against a lab VPX/CPX; the CVAD integration lab pairs with the Chapter 04 site. **Cost:** none with CPX Express.

### Lab 6.1 — Gateway virtual server (Gateway module)

**Objective:** Stand up the Gateway vserver, the object every other module hangs off.

```bash
enable ns feature SSLVPN
add vpn vserver gw_ext SSL 10.150.9.200 443
bind ssl vserver gw_ext -certkeyName lab_cert
show vpn vserver gw_ext
```

**Expected result:** `gw_ext` UP on 443 with the certificate bound — the secure front door. Gateway modes (ICA proxy, full VPN, clientless) are all delivered from this one object.

**Negative test:** Without the SSLVPN feature enabled the `add vpn vserver` fails — features gate commands.

**Rollback:** Keep for the following labs.

### Lab 6.2 — Authentication (authentication and authorization module)

**Objective:** Bind LDAP authentication to the gateway.

```bash
add authentication ldapAction lab_ldap -serverIP 10.150.0.10 -ldapBase "dc=lab,dc=local" -ldapBindDn "cn=svc,dc=lab,dc=local" -ldapBindDnPassword <pw> -ldapLoginName sAMAccountName
add authentication policy pol_ldap -rule true -action lab_ldap
bind authentication vserver gw_ext -policy pol_ldap -priority 100
```

**Expected result:** Gateway logons authenticate against the lab directory; `show authentication ldapAction lab_ldap` reports the reachable server. Authorization policies and session policies then decide what an authenticated user may do.

**Negative test:** Wrong `ldapLoginName` attribute: binds succeed, user logons fail — the classic misconfiguration the exam presents as "admin works, users don't."

**Rollback:** Keep for 6.3.

### Lab 6.3 — Session policy and end-user experience (end-user access module)

**Objective:** Shape what a logon delivers: ICA proxy toward StoreFront.

```bash
add vpn sessionAction act_ica -transparentInterception OFF -SSO ON -icaProxy ON -wihome "https://storefront.lab.local/Citrix/StoreWeb" -clientlessVpnMode OFF
add vpn sessionPolicy pol_ica true act_ica
bind vpn vserver gw_ext -policy pol_ica -priority 100
```

**Expected result:** Users landing on `gw_ext` are proxied to the StoreFront store with single sign-on — ICA-proxy mode, the deployment the exam cares most about. RDP proxy and clientless access are variations of the same session-policy machinery.

**Negative test:** `icaProxy ON` with no `wihome`: logon succeeds into nothing — a session policy must say where to land.

**Rollback:** Keep for 6.4.

### Lab 6.4 — CVAD integration (integration module)

**Objective:** Complete the Gateway ↔ StoreFront ↔ controllers triangle.

```bash
bind vpn vserver gw_ext -staServer "http://ddc1.lab.local"
show vpn vserver gw_ext | grep -A2 STA
# StoreFront: Manage Citrix Gateways > add gw_ext (public FQDN + STA list) > enable Remote Access on the store
```

**Expected result:** STA bound and `UP` on the gateway, StoreFront configured with the same STA list: launches produce STA tickets, the gateway validates them, and HDX flows through 443. This handshake is the integration module in one lab.

**Negative test:** Mismatch the STA lists (gateway lists ddc1, StoreFront lists ddc2): enumeration works, launches fail with a ticket error — the most-tested integration break.

**Rollback:** None — read-only; this lab changes no persistent state, so there is nothing to revert.

### Lab 6.5 — Rewrite and responder (AppExpert module)

**Objective:** Use AppExpert policies on gateway/LB traffic.

```bash
enable ns feature REWRITE RESPONDER
add rewrite action act_hsts insert_http_header Strict-Transport-Security "\"max-age=31536000\""
add rewrite policy pol_hsts true act_hsts
bind vpn vserver gw_ext -policy pol_hsts -priority 100 -type RESPONSE
add responder action act_block respondwith "\"HTTP/1.1 403 Forbidden\r\n\r\n\""
add responder policy pol_block "HTTP.REQ.URL.CONTAINS(\"/admin\")" act_block
```

**Expected result:** Responses gain the HSTS header; requests for `/admin` are answered 403 by NetScaler itself — rewrite mutates, responder replies. Policy expressions (`HTTP.REQ...`) are the AppExpert language the exam quotes.

**Negative test:** Bind the rewrite as `-type REQUEST`; the header never appears on responses — direction matters on every bind.

**Rollback:** Unbind and remove the lab policies.

### Lab 6.6 — Content switching in front of the gateway (content switching module)

**Objective:** One VIP, many destinations, by policy.

```bash
enable ns feature CS
add cs vserver cs_front SSL 10.150.9.210 443
bind ssl vserver cs_front -certkeyName lab_cert
add cs action act_to_lb -targetLBVserver lb_web
add cs policy pol_web -rule "HTTP.REQ.HOSTNAME.EQ(\"www.lab.local\")" -action act_to_lb
bind cs vserver cs_front -policyName pol_web -priority 100
bind cs vserver cs_front -vServer gw_ext -targetVserver gw_ext 2>/dev/null || true
```

**Expected result:** Hostname-based steering from one VIP: `www` to the LB vserver, gateway traffic to `gw_ext` (the unified-gateway pattern uses exactly this construction). Rule precedence is priority order, lowest first.

**Negative test:** Two policies matching the same request: the lower priority number wins — precedence, not specificity.

**Rollback:** Remove the CS lab objects.

### Lab 6.7 — Troubleshooting with nstrace (troubleshooting module)

**Objective:** Capture and read gateway traffic the exam way.

```bash
start nstrace -size 0 -filter "CONNECTION.DSTIP.EQ(10.150.9.200)"
# reproduce a logon, then:
stop nstrace
shell ls /var/nstrace/
```

**Expected result:** A capture directory of `.cap` files filtered to the gateway VIP, readable in Wireshark — `nstrace` plus `/var/log/ns.log` (syslog) are the two tools the troubleshooting module names; filters keep captures usable.

**Negative test:** Trace without a filter on a busy box — gigabytes of noise; the exam rewards knowing to filter at capture time.

**Rollback:** `shell rm -rf /var/nstrace/*` in the lab.

## Summary and Completion Checklist

- [ ] Gateway vserver, LDAP auth, and ICA-proxy session policy built.
- [ ] STA/StoreFront integration completed and its failure mode drilled.
- [ ] Rewrite/responder, content switching, and nstrace exercised.
