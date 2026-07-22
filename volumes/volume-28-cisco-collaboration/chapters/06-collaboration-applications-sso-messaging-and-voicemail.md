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

CLICA opens with SSO (15%) because everything else authenticates
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

- CLICA 300-810 v1.2 exam topics (SSO 15%, IM&P and cloud messaging
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

Onto the Chapter 03–05 estate: enable SAML SSO against a lab IdP
(Keycloak or a trial IdP works) for CUCM and Unity — metadata both
ways, NameID mapped to the LDAP identity, SSO test passed, recovery
URL exercised once deliberately. Integrate Unity Connection: port
group to the Chapter 03 trunk, LDAP-imported users with mailboxes,
MAIN-AA call handler with schedule and 0-out, MWI proven on an
endpoint. Configure service profiles so the Webex App/Jabber client
discovers, signs in via SSO, gets presence from IM&P, and retrieves
a visual voicemail left via a Chapter 04 CFNA. Break and evidence:
expire/replace the IdP-side certificate in a window (observe, then
repair via recovery URL path), and misroute one forwarded call so
Unity plays the wrong greeting — diagnose from the received
Diversion header, then fix.

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
CLICA domains map to this one chapter.

- [ ] I can trace a SAML assertion and name its three failure points
- [ ] My voicemail seams (CSS, MWI, routing rules) are deliberate
- [ ] My client signs in through discovery + SSO with no manual
      servers
- [ ] Presence, chat, and visual voicemail all work — and I proved
      the failure modes
