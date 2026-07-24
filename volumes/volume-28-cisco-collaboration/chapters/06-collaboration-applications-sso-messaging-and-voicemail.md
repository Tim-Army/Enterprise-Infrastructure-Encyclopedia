# Chapter 06: Collaboration Applications: SSO, Messaging, and Voicemail

## Learning Objectives

- Implement SAML single sign-on across the collaboration
  applications, and explain the assertion flow you will troubleshoot
- Deploy IM and Presence with its CUCM integration, and understand
  presence federation boundaries
- Configure Unity Connection: integration, call handlers, users, and
  the dial-plan seams voicemail lives in
- Manage the application clients — Jabber and Webex App — and their
  service discovery across cloud and on-premises profiles
- Validate each integration and troubleshoot the SSO, presence, and
  voicemail failure classics

## Theory and Architecture

### SAML SSO: one login, many applications

CLICA opened with SSO (15%) because everything else authenticates
through it. The flow to internalize: the client requests a protected
resource (CUCM user page, Unity web, Jabber/Webex App login); the
service (SP) redirects to the **identity provider** (IdP — AD FS,
Azure AD/Entra, Okta, Duo) with a SAML request; the user
authenticates *at the IdP* (passwords never touch the collaboration
apps — the point); the IdP returns a signed **assertion**; the SP
validates signature and conditions and grants a session. The moving
parts that break: metadata exchange (SP and IdP each import the
other's), certificate expiry on either side (the recurring outage),
clock skew (assertions carry validity windows — NTP again), and
NameID/attribute mapping to the LDAP-synchronized identity from
Chapter 03. Cluster-wide SSO mode in CUCM covers the UC apps;
"run-on-all-nodes" and per-node metadata details are the operational
texture the exam probes.

**OAuth 2.0** with refresh tokens rides alongside for the soft
clients — token lifetimes, not passwords, on every reconnect.

### IM and Presence: the messaging fabric on-premises

IM&P attaches to CUCM (same cluster security, users from the same
LDAP truth), serves Jabber/Webex App presence and chat, and
federates: **intra-domain** with itself, **inter-domain** via
XMPP/SIP federation to partners, and — the modern seam — **presence
and messaging coexistence with Webex** during cloud migration.
Services worth naming: Cisco XCP router (the XMPP core), Presence
Engine, and the SIP proxy that connects presence to telephony state
(off-hook shows busy). High availability is subcluster pairs with
user redundancy groups — balanced assignment, automatic failover.

### Unity Connection: voicemail as a routed application

Unity Connection answers what CUCM forwards (Chapter 03's trunk and
Chapter 04's CFNA chains) and renders mailboxes: **users** (synced
from LDAP), **call handlers** (auditor attendants, menus, greetings),
**directory handlers** (dial-by-name), **routing rules** (direct
versus forwarded arrival), and **notification devices** (MWI, email,
SMTP single inbox to Exchange/O365). Integration is a SIP trunk with
its own port group and MWI dial mechanics. Design texture: search
spaces exist here too — Unity's own partitions/search spaces decide
which mailboxes and handlers a call can reach, mirroring Chapter
04's containment thinking.

### The clients

**Jabber** (on-premises heritage) and **Webex App** (the strategic
client) both: discover services (Chapter 01's SRV records — UDS
on-premises, Webex cloud otherwise), register for calling (CUCM or
Webex Calling), attach messaging (IM&P or Webex cloud), and
integrate voicemail (visual voicemail against Unity's REST). Modes
matter operationally: Webex App with on-premises calling
(unified-CM registration) versus full cloud; Jabber phone-only
versus full UC. The migration story between them is Chapter 07's
hybrid services in practice.

## Design Considerations

- **One IdP for the estate**, assertions mapped to the same LDAP
  identity everywhere; per-app local logins survive only as
  break-glass, documented and monitored.
- **Presence domain planning**: the presence domain should match
  mail/UPN reality; changing it later touches every client profile.
- **Voicemail dial-plan seams deliberately**: voicemail pilot and
  ports in partitions reachable by the *forwarder* CSS paths
  (Chapter 04's classic), MWI mechanisms tested per site.
- **Client strategy explicit**: pick Webex App or Jabber per
  population with a migration path, not both indefinitely by
  default.

## Implementation and Automation

SSO enablement sequence (CUCM shown; Unity and IM&P mirror it):

```text
1. NTP verified everywhere (assertion windows)
2. Export SP metadata: System > SAML Single Sign-On > Export
3. Import into IdP; map NameID -> sAMAccountName/mail per design
4. Import IdP metadata back; Run SSO Test with a browser user
5. Enable cluster-wide; keep the recovery URL documented:
   https://<node>/ssosp/local/login  (break-glass, monitored)
```

Unity Connection integration essentials:

```text
Telephony Integration > Port Group: SIP, to CUCM trunk from Ch.03
  MWI: on/off DNs or SIP NOTIFY per design
Users: LDAP import (same filters as CUCM — one truth)
Call Handler: MAIN-AA, business-hours schedule, caller input 0 ->
  operator DN; greeting recorded via TUI or upload
Routing Rules: forwarded -> attempt sign-in? no: subscriber greeting
```

Client profile via UC Services (Jabber/Webex App on-prem calling):

```text
UC Services: CTI, IM&P, Voicemail (Unity REST), Directory (UDS)
Service Profile: assemble + assign to end users (LDAP-synced)
# Discovery test from a client network:
dig +short SRV _cisco-uds._tcp.example.lab
```

## Validation and Troubleshooting

**SSO**: the browser is the debugger — trace the redirect chain
(SP→IdP→SP), read the SAML response (browser dev tools or SAML
tracer), and check the three usual suspects: certificate validity on
both sides, clock skew, NameID mapping to an existing synced user.
The recovery URL exists so an expired IdP certificate does not lock
every administrator out — rehearse it. **IM&P**: presence blank means
XCP/Presence Engine services or the CUCM-side service profile;
one-user chat failures are usually user assignment to a failed-over
subcluster node. **Unity**: MWI lamps wrong with working voicemail
is the MWI port/NOTIFY mechanism; "direct calls get the subscriber
greeting but forwards get the opening greeting" (or inverse) is
routing rules reading the redirect headers — check what Diversion
arrived (Chapter 05's border rewrites matter here). **Clients**:
sign-in failures decompose by service — discovery (SRV), auth
(SSO/OAuth), then each UC service's own reachability in the client's
diagnostics bundle.

## Security and Best Practices

- SSO shrinks the password attack surface — finish the job: disable
  basic auth paths left behind, monitor recovery-URL use as a
  security event.
- Certificate lifecycle for IdP/SP pairs on the Chapter 01 renewal
  calendar with named owners.
- Voicemail PIN policy and TUI brute-force lockouts; single-inbox
  OAuth to O365 rather than app passwords.
- Federation boundaries explicit: XMPP federation allow-lists, and
  Webex org policies for external messaging.

## References and Knowledge Checks

- CLICA 300-810 v1.2 exam topics (retired February 2026 — SSO 15%, IM&P and cloud messaging
  30%, Unity Connection 30%, clients 25%)
- Cisco SAML SSO deployment guide; Unity Connection and IM&P
  configuration guides

Knowledge checks:

1. Walk the SAML flow and name where each of the three classic
   failures (certs, skew, mapping) interrupts it.
2. Why do forwarded and direct calls hit different Unity behavior,
   and which headers decide it?
3. A user's presence is stale but chat works. Which component and
   HA construct do you inspect?
4. What does the SSO recovery URL trade away, and how do you keep
   that trade honest?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **every objective in the
CLICA 300-810 v1.2 exam guide** — Single Sign-On, IM and Presence, Unity
Connection, and application clients — mapped in the volume README's coverage
tables. **CLICA retired in February 2026**, but its applications content remains
core to a Cisco Collaboration deployment and is the subject of this chapter; the
labs are kept as a complete applications reference. Labs use the IM&P and Unity
Connection CLIs, UCM SSO/OAuth configuration, and Jabber/Webex App
troubleshooting. Each ends **`**Lab verified by:** *pending*`** until a human
runs it.

**Shared prerequisites for Labs 6.1–6.19** — a Unified CM cluster with an IM and
Presence (IM&P) node, a Unity Connection server, an identity provider (IdP) for
SAML SSO, LDAP, and Jabber/Webex App clients. **Cost:** none beyond lab
resources.

### Lab 6.1 — Describe types of SSO for Collaboration (CLICA Objective 1.1)

**Objective:** Read the SSO/authentication mode and its identity source.

```text
admin:run sql select param_name,param_value from processconfig where param_name like '%SSO%'
admin:utils sso status
```

**Expected result:** SSO enabled/disabled and the mode — Collaboration SSO can
key off Integrated Windows AD, Kerberos, two-factor (2FA), or a third-party IdP;
`utils sso status` shows whether SAML SSO is active for the cluster.

**Negative test:** enable SSO with an IdP whose contract/metadata does not
include the UCM SP; login loops back — the trust must be mutual (SP↔IdP).

**Cleanup:** none (read-only).

### Lab 6.2 — Describe the SAML SSO login process flow (CLICA Objective 1.2)

**Objective:** Trace the SAML redirect/POST flow for a UCM login.

```text
admin:file tail activelog /tomcat/logs/ssosp/log4j/  ! SSO SP logs
! Flow: SP (UCM) -> redirect to IdP -> user auth -> SAML assertion POST back -> session
```

**Expected result:** the SP-initiated redirect to the IdP, the assertion POST
back, and session creation — SAML SSO is browser-mediated: UCM (SP) redirects to
the IdP, the IdP authenticates and returns a signed assertion, UCM validates it
and grants the session.

**Negative test:** a clock skew between SP and IdP beyond the assertion's
NotBefore/NotOnOrAfter window rejects the assertion — SSO needs synchronized NTP.

**Cleanup:** none (read-only).

### Lab 6.3 — Describe SAML 2.0 components (CLICA Objective 1.3)

**Objective:** Inspect the SAML metadata (assertion, protocol, binding,
profile).

```text
admin:show cert list own | include SAML
! Download SP metadata from UCM and inspect:
!   Assertion (identity claims), Protocol (request/response), Binding (HTTP-POST/Redirect), Profile (Web Browser SSO)
```

**Expected result:** the SP metadata showing the ACS (Assertion Consumer
Service) binding and signing cert — SAML 2.0 = **assertions** (the identity
statements), a **protocol** (auth request/response), **bindings** (how it's
transported, HTTP-POST/Redirect), and **profiles** (Web Browser SSO combines
them).

**Negative test:** an IdP configured for HTTP-Redirect binding on the ACS while
UCM expects HTTP-POST fails assertion delivery — the binding must match on both
sides.

**Cleanup:** none (read-only).

### Lab 6.4 — Describe SAML SSO configuration (CLICA Objective 1.4)

**Objective:** Verify the SP/IdP metadata exchange and test SSO.

```text
admin:utils sso status
admin:show cert list trust | include IdP
! Run the built-in SSO test during enablement; confirm a successful round trip
```

**Expected result:** the IdP metadata imported into UCM's trust and a passing
SSO test — configuration is a mutual metadata exchange: import IdP metadata into
UCM, upload UCM SP metadata into the IdP, map the LDAP UID claim, then test.

**Negative test:** a UID/NameID mapping mismatch (IdP sends email, UCM expects
sAMAccountName) authenticates the user at the IdP but fails the UCM lookup — the
claim mapping is the fault.

**Cleanup:** none (read-only).

### Lab 6.5 — Describe OAuth 2.0 (CLICA Objective 1.5)

**Objective:** Read the OAuth token configuration UCM uses for clients.

```text
admin:run sql select param_name,param_value from processconfig where param_name like '%OAuth%'
admin:show keys authz
```

**Expected result:** OAuth refresh/access token settings and the authz signing
keys — UCM uses OAuth with refresh tokens so Jabber/Webex App and MRA clients
authenticate once and silently refresh, rather than re-prompting per service.

**Negative test:** disable OAuth with MRA clients deployed; every service login
re-prompts and SSO-over-MRA breaks — OAuth refresh tokens are what make
single-login work across services.

**Cleanup:** none (read-only).

### Lab 6.6 — Configure Cisco Unified IM and Presence on-premises (CLICA Objective 2.1)

**Objective:** Verify IM&P high availability, federation, and persistent chat.

```text
admin:utils dbreplication runtimestate       ! on IM&P
admin:show perf query class "Cisco Presence Engine"
run sql select * from enterprisephoneconfig where name like '%persistent%' 2>/dev/null
```

**Expected result:** IM&P DB replication healthy, the Presence Engine running,
and features (HA sub-cluster, calendar/Exchange, APNs, persistent chat, XMPP/SIP
federation) configured — IM&P provides presence and messaging integrated with
UCM users.

**Negative test:** an IM&P HA sub-cluster with broken DB replication fails
failover; users on the down node lose presence — replication health is the HA
prerequisite.

**Cleanup:** none (read-only).

### Lab 6.7 — Troubleshoot Cisco Unified IM and Presence on-premises (CLICA Objective 2.2)

**Objective:** Diagnose presence/messaging failure (XMPP, HA, federation).

```text
admin:utils service list | include "Cisco XCP"
admin:show perf query counter "Cisco XCP CM" "Active Client Sessions"
admin:file tail activelog /epas/trace/xcp/log/    ! XCP router logs
```

**Expected result:** the XCP (eXtensible Communications Platform) services and
active sessions — presence failures trace to a stopped XCP Router/CM, a federation
(XMPP/SIP) trust problem, or a full-sync issue; the counters and XCP logs
localize it.

**Negative test:** blame the client for missing presence when the XCP Router is
down cluster-wide — a service-level fault presents as every client failing at
once.

**Cleanup:** none (read-only).

### Lab 6.8 — Configure Cisco Unity Connection (CLICA Objective 3.1)

**Objective:** Configure call handlers, greetings, routing, and LDAP.

```text
run cuc dbquery unitydirdb select displayname from vw_callhandler
run cuc dbquery unitydirdb select alias,dtmfaccessid from vw_mailbox limit 5
show cuc cluster status
```

**Expected result:** the call handlers and mailbox users — Unity Connection
routes callers through call handlers (greetings, menus), delivers voicemail with
MWI, uses routing rules for direct/forwarded calls, and imports users via LDAP.

**Negative test:** a call handler transfer to an extension outside the partition
search space fails — Unity's routing obeys its own search scopes, mirroring UCM's
CSS/partition model.

**Cleanup:** remove the test call handler.

### Lab 6.9 — Troubleshoot Cisco Unity Connection (CLICA Objective 3.2)

**Objective:** Diagnose voicemail delivery, MWI, or auto-attendant failure.

```text
run cuc dbquery unitydirdb select displayname,dtmfaccessid from vw_callhandler where isprimary=1
show cuc jetty status
! Use Real-Time Monitoring / Port Monitor for live call/port state
```

**Expected result:** the auto-attendant handler and port/service state — voicemail
that does not deliver traces to a full mailbox, a routing-rule miss, or a port
issue; MWI stuck on traces to the UCM integration (Lab 6.11).

**Negative test:** an auto-attendant that dead-ends traces to a routing rule
whose target handler was deleted — the rule, not the greeting, is the break.

**Cleanup:** none (read-only).

### Lab 6.10 — Implement toll fraud prevention in Unity Connection (CLICA Objective 3.3)

**Objective:** Verify restriction tables that block toll fraud via voicemail.

```text
run cuc dbquery unitydirdb select displayname from vw_restrictiontable
! Confirm transfer/notification/fax restriction tables block off-net patterns
```

**Expected result:** restriction tables denying external/long-distance patterns
— Unity toll fraud comes from call-transfer, message-notification, and greeting
transfer rules dialing out; restriction tables blocking those patterns close it.

**Negative test:** a permissive default restriction table lets a caller "transfer
to an extension" that is really an external number via the operator — the
restriction table is what blocks it.

**Cleanup:** revert any test restriction-table change.

### Lab 6.11 — Troubleshoot Unity Connection integration with UCM (CLICA Objective 3.4)

**Objective:** Diagnose the UCM↔Unity voicemail integration (ports, MWI).

```text
run cuc dbquery unitydirdb select displayname from vw_porthandler 2>/dev/null
! On UCM: verify voicemail pilot, profile, SIP trunk to Unity, MWI on/off DNs
admin:run sql select param_name,param_value from processconfig where param_name like '%MWI%'
```

**Expected result:** the messaging ports and the UCM voicemail pilot/profile —
an integration fault (calls not forwarding to VM, MWI stuck) traces to the SIP
trunk, the voicemail pilot/profile, or the MWI on/off DNs mismatched between UCM
and Unity.

**Negative test:** MWI on/off DNs configured differently on UCM and Unity leaves
lamps stuck on — the two sides must agree on the MWI extensions.

**Cleanup:** none (read-only).

### Lab 6.12 — Describe digital networking in multicluster Unity (CLICA Objective 3.5)

**Objective:** Read the intersite/digital-networking links between Unity servers.

```text
run cuc dbquery unitydirdb select displayname from vw_vmsserver 2>/dev/null
! Confirm HTTP(S) networking / directory replication between Unity locations
```

**Expected result:** the networked Unity locations — digital networking joins
multiple Unity Connection servers/clusters so users in one location can address
mailboxes in another and see a unified directory.

**Negative test:** a networked location whose HTTPS link is down cannot resolve
remote recipients; cross-location voicemail addressing fails — the networking
link is the dependency.

**Cleanup:** none (read-only).

### Lab 6.13 — Configure DNS for service discovery (CLICA Objective 4.1)

**Objective:** Verify the SRV records Jabber/Webex App use to find services.

```text
nslookup -type=SRV _cisco-uds._tcp.example.com
nslookup -type=SRV _collab-edge._tls.example.com
```

**Expected result:** `_cisco-uds` (internal UDS/UCM discovery) and `_collab-edge`
(MRA via Expressway) SRV records — clients discover call control automatically:
`_cisco-uds` on the internal network, `_collab-edge` from outside for MRA.

**Negative test:** a missing `_cisco-uds` SRV forces manual server entry and
breaks zero-touch discovery; a missing `_collab-edge` breaks MRA from outside —
each record enables a discovery path.

**Cleanup:** none (read-only).

### Lab 6.14 — Troubleshoot service discovery (CLICA Objective 4.2)

**Objective:** Diagnose a client that cannot discover its services.

```text
nslookup -type=SRV _cisco-uds._tcp.example.com
! Jabber: view the "Show connection status" / problem report; check UDS vs CUCM lookup
```

**Expected result:** the SRV answer or its absence — discovery failures trace to
missing/misordered SRV records, an unreachable UDS, or a domain mismatch between
the client's email domain and the SRV zone.

**Negative test:** a user whose email domain differs from the DNS SRV zone never
finds the records; discovery fails despite correct records in the other zone —
the domain the client queries must host the SRVs.

**Cleanup:** none (read-only).

### Lab 6.15 — Troubleshoot Jabber/Webex App phone control (CLICA Objective 4.3)

**Objective:** Diagnose softphone/deskphone control (CTI) failure.

```text
admin:show risdb query ctimgr
admin:run sql select name from device where name like 'CSF%' or name like 'BOT%' or name like 'TCT%'
! Confirm CTI-enabled, user CTI permission, and CSF/CTI device registration
```

**Expected result:** the CTI manager sessions and the client's CSF/CTI devices —
phone control (Jabber/Webex App controlling a desk phone or its own softphone)
needs the CTI service, the user in the CTI-enabled group, and the device
registered.

**Negative test:** a user not in "Standard CTI Enabled" cannot control the desk
phone though the softphone works — the CTI permission gates deskphone control
specifically.

**Cleanup:** none (read-only).

### Lab 6.16 — Troubleshoot Jabber/Webex App voicemail integration (CLICA Objective 4.4)

**Objective:** Diagnose visual voicemail in the client.

```text
! Client uses a voicemail (Unity) service profile; verify:
admin:run sql select name from voicemailprofile
admin:run sql select name,fkservice from uccxservice 2>/dev/null
! Confirm the UC Service (voicemail + mailstore) and service profile assigned to the user
```

**Expected result:** the voicemail UC service and profile assigned to the user —
visual voicemail in Jabber/Webex App needs a Voicemail UC service, a Mailstore
service, and both in the user's service profile, plus Unity credentials.

**Negative test:** a user with a voicemail service but no mailstore service sees
message-waiting but cannot open visual voicemail — both UC services are required.

**Cleanup:** none (read-only).

### Lab 6.17 — Troubleshoot certificate validation (CLICA Objective 4.5)

**Objective:** Diagnose a client certificate-trust prompt or failure.

```text
admin:show cert list own
openssl s_client -connect $CUCM:8443 -showcerts </dev/null 2>/dev/null | openssl x509 -noout -subject -issuer -dates
```

**Expected result:** the presented cert chain and its issuer/validity — client
cert prompts come from a Tomcat/CallManager cert signed by a CA the client does
not trust, an expired cert, or a name mismatch (SAN missing the FQDN the client
used).

**Negative test:** a self-signed UCM Tomcat cert whose CN/SAN omits the discovery
FQDN triggers a trust prompt every login — a CA-signed cert with the correct SAN
removes it.

**Cleanup:** none (read-only).

### Lab 6.18 — Describe Unified Attendant Console Advanced integration (CLICA Objective 4.6)

**Objective:** Read the CUACA integration (CTI, presence, directory).

```text
! On UCM: confirm the CUACA application user, CTI ports/route points, and CTI permissions
admin:run sql select name from device where tkclass=10 and name like 'AC%'   ! CTI ports/RP
```

**Expected result:** the CUACA CTI ports/route points and application user —
Cisco Unified Attendant Console Advanced integrates via CTI (to control calls),
presence (IM&P), and the directory, so an operator queues and transfers calls.

**Negative test:** a CUACA app user missing CTI control of its route points
cannot receive queued calls — the CTI association is the integration linchpin.

**Cleanup:** none (read-only).

### Lab 6.19 — Troubleshoot Webex App functions (CLICA Objective 4.7)

**Objective:** Diagnose Webex App login, call signaling, media, and voicemail.

```text
! Collect the Webex App problem report; correlate with:
admin:show risdb query phone | include BOT|TCT|CSF
nslookup -type=SRV _collab-edge._tls.example.com    ! MRA path for remote users
```

**Expected result:** the App's device state plus discovery/MRA path — Webex App
issues split cleanly: login = SSO/OAuth/discovery (Labs 6.1–6.14), call signaling
= UCM registration/CTI, media = QoS/ICE, voicemail = the Lab 6.16 service profile.

**Negative test:** a remote Webex App failing only off-network is an MRA/
`_collab-edge`/Expressway problem, not a client bug — the on-net-works/off-net-
fails split points to the edge.

**Cleanup:** none (read-only).

## Lab Verification

Verification means SSO round-trips with the mapped identity, the
full client stack (discovery, SSO, presence, visual voicemail)
works end to end, and both induced failures were diagnosed from
their proper evidence. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The applications layer is where users actually live: SSO makes
identity singular, IM&P makes presence and messaging a fabric,
Unity Connection answers what the dial plan forwards, and the
clients assemble it all through service discovery. Every
integration is a seam with named failure classes — and all four
CLICA domains map to this one chapter (CLICA was retired in February 2026; the material still serves CLCOR's applications domain).

- [ ] I can trace a SAML assertion and name its three failure points
- [ ] My voicemail seams (CSS, MWI, routing rules) are deliberate
- [ ] My client signs in through discovery + SSO with no manual
      servers
- [ ] Presence, chat, and visual voicemail all work — and I proved
      the failure modes
