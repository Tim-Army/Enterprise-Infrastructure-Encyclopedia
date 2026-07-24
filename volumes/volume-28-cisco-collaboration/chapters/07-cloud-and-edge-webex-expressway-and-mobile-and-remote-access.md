# Chapter 07: Cloud and Edge: Webex, Expressway, and Mobile and Remote Access

## Learning Objectives

- Deploy the Expressway-C/Expressway-E traversal pair and explain
  why the DMZ design works without VPN
- Configure Mobile and Remote Access end to end: discovery,
  traversal zones, certificates, and the registration path
- Describe business-to-business calling through the edge, and the
  DNS and TLS plumbing it rides
- Integrate Webex hybrid services and position Webex Calling,
  Meetings, and Devices in a hybrid estate
- Validate edge flows and troubleshoot the MRA and traversal
  classics

## Theory and Architecture

### The traversal pair: publishing collaboration without VPN

**Expressway-C** (inside) and **Expressway-E** (DMZ) form a
firewall-traversal pair: C registers *outbound* to E across the
inner firewall (so no inbound holes to the trusted network), and E
listens to the internet for the published services. Traffic
patterns: signaling and media both relay through the pair (SSH
tunnels for the traversal link's control; TURN/media relay on E for
media). What this buys CLHCT's hybrid domains: no VPN client,
no inbound trust-network exposure, per-service publishing rather
than network access.

### Mobile and Remote Access

**MRA** publishes CUCM registration through the pair: the client
resolves `_collab-edge._tls.<domain>` (Chapter 01's record) to
Expressway-E, authenticates (SSO from Chapter 06 rides through),
and registers to CUCM as if inside — calling, voicemail, presence
intact. The chain that must all be true: DNS SRV correct publicly;
E's certificate carrying the required SANs (collab-edge domains);
C↔E traversal zone established and its own certificates trusted;
C's discovered UC servers (CUCM, IM&P, Unity) reachable and
TLS-trusted; and the user's home cluster serviceable. MRA
troubleshooting is walking exactly this chain — the exam weights it
25% and operations weight it higher.

### Business-to-business and interop

B2B calling federates SIP (and legacy H.323 interop where it
persists) between organizations through the same pair: DNS SRV
(`_sips._tcp`) discovery of the far side, TLS verification, search
rules on Expressway deciding what egresses and what arrives, and
CPL/policy for admission. Media encryption negotiated end to end
where both sides speak it. The dial-plan seam: Expressway search
rules and transforms are their own routing layer — Chapter 04
thinking, applied at the edge — deciding which URIs route inward to
CUCM and which resolve outward via DNS.

### Webex and hybrid services

The Webex platform delivers Meetings, Messaging, Calling, and
Devices from the cloud; **hybrid services** stitch it to
on-premises: **Hybrid Calendar** (meeting join details, One Button
to Push), **Hybrid Directory**, **Hybrid Message** (IM&P↔Webex
coexistence), and the **Webex Device Connector**/Edge for Devices
path for on-premises-registered devices gaining cloud features. The
management plane is **Control Hub** — org settings, users
(synchronized via Directory Connector or SCIM from the IdP), and
service assignments. Positioning literacy CLCOR v2.0 expects at 25%:
Webex Calling with a **Local Gateway** (a CUBE — Chapter 05 skills
verbatim) for PSTN, versus on-premises CUCM with hybrid services,
versus full-cloud estates, and the migration seams between them.

## Design Considerations

- **Certificates are the edge design**: public CA on E with every
  SAN the services require (collab-edge, XMPP federation, B2B
  domains); the SAN worksheet is written before the CSR, reviewed
  at every domain change.
- **DMZ discipline**: E dual-NIC with static NAT reflection
  understood (the `xConfiguration` NAT address answering the
  far-side SDP question), firewall rules per published service, no
  shortcuts "just for testing."
- **Search rule hygiene**: explicit source zones, target patterns,
  and priorities — the edge's dial plan deserves Chapter 04's
  paper-matrix treatment.
- **Hybrid before rip-and-replace**: calendar and directory hybrids
  deliver cloud value to on-premises estates immediately;
  migrations sequence by population, not by forklift.

## Implementation and Automation

The MRA build sequence (Expressway pair already base-configured):

```text
On Expressway-C:
  Unified Communications mode: Mobile and remote access
  Discover UC servers: CUCM, IM&P, Unity (TLS verify on)
  Traversal Client zone -> E (port 7001, TLS verify, auth creds)

On Expressway-E:
  Traversal Server zone (matching auth)
  DNS: public A record + _collab-edge._tls SRV -> E
  Certificate: public CA, SANs per worksheet
  TURN relays licensed/enabled for media

Firewall:
  Inner: C -> E established/outbound only
  Outer: internet -> E on 8443/5061/TURN ranges per guide
```

B2B search rule shape (E, outbound):

```text
Search rule: "B2B-OUT"
  Source: LocalZone+TraversalZone   Mode: Alias pattern match
  Pattern: (.*)@(?!example\.lab).*  On match: continue
  Target: DNS zone (TLS, SRV _sips._tcp)
```

Webex hybrid enablement is Control Hub-driven: register the
connector hosts (Expressway-based for Calendar/Message), authorize
against the org, assign services per user — then verify from the
client, where hybrid either visibly works (join buttons, unified
presence) or visibly does not.

## Validation and Troubleshooting

MRA validation walks its chain with the platform's own tools:
`Maintenance > Diagnostics` on both Expressways, the **collab-edge
SRV** checked from outside (`dig` against public DNS), C's UC
discovery status page (every server green/TLS-verified), traversal
zone state Active on both ends, and a client sign-in from a truly
external network. Failure classics: certificate SAN gaps (client
connects, then errors on a service whose domain the SAN missed —
read E's cert against the worksheet); traversal zone Active on C
but failing calls (inner firewall passed 7001 but blocked the
media/control ranges); one service failing over MRA only (that
server missing from C's discovery or its certificate untrusted by
C); B2B one-way (far side's SRV or TLS verification — test with
`Locate` on Expressway, which answers "how would I route this URI"
with evidence). Hybrid services: the connector host's status page
and Control Hub's per-user service status narrate their own faults.

## Security and Best Practices

- The edge is an internet-facing SIP presence: fail2ban-equivalent
  protections on E (automated blocking), CPL denying unauthorized
  traversal, and registration/call policy reviewed like firewall
  rules.
- TLS verify ON between C and discovered servers — turning it off
  to make MRA work is deferring the certificate fix into an
  incident.
- Control Hub admin roles least-privileged with SSO enforced;
  Directory Connector/SCIM as the only user-creation path.
- Log retention on both Expressways sized for investigations; edge
  logs are the estate's border camera footage.

## References and Knowledge Checks

- CLHCT 300-820 v2.0 exam topics (formerly CLCEI — seven domains led by Suite and Devices Configuration and Management, 25% each)
- CLCOR 350-801 v2.0 domain 5 (Cloud and Hybrid Services, 25%)
- Cisco Expressway MRA and B2B deployment guides; Webex Control Hub
  documentation

Knowledge checks:

1. Why does the traversal pair require no inbound rule through the
   inner firewall, and which direction establishes the zone?
2. An MRA client signs in but visual voicemail fails; on-network it
   works. Walk the chain to the two likeliest points.
3. What answers "how would this URI route" on Expressway, and why
   is it better evidence than a test call?
4. Which PSTN function does a Local Gateway serve for Webex
   Calling, and which chapter's skills configure it?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **Domain 5 (Cloud and
Hybrid Services) of CLCOR 350-801 v2.0, every objective of CLHCT 300-820 v2.0
(Collaboration Hybrid and Cloud Technologies), and Domain 5 (Remote Connectivity
and Business to Business) of CLACC 300-815 v2.0** — mapped in the volume
README's coverage tables. Labs use the Webex Control Hub, the Webex REST APIs
(`developer.webex.com`), the Expressway CLI/API, and a local gateway (CUBE).
Each ends **`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 7.1–7.41** — a Webex organization with Control
Hub admin, a Webex API token in `$WBX` (an `Authorization: Bearer` header), an
Expressway-C/E pair for MRA and B2B, a local gateway (IOS XE CUBE) registered to
Webex Calling, and a hybrid-connected on-prem UCM. **Cost:** none beyond lab
resources.

### Lab 7.1 — Describe the Webex Suite (CLCOR Objective 5.1)

**Objective:** Read the services licensed in the Webex organization.

```bash
curl -s -H "Authorization: Bearer $WBX" https://webexapis.com/v1/licenses | jq -r '.items[] | "\(.name) \(.totalUnits)"'
```

**Expected result:** the Calling, Meetings, and Messaging licenses — the Webex
Suite unifies cloud calling (Webex Calling), meetings (Webex Meetings), and
messaging (spaces) under one org and identity, administered from Control Hub.

**Negative test:** assign a user a Meetings license but not Calling; they can host
meetings but have no cloud phone number — each service is separately licensed.

**Cleanup:** none (read-only).

### Lab 7.2 — Describe the call routing process in Webex Calling (CLCOR Objective 5.2)

**Objective:** Read how a Webex Calling number routes to PSTN/on-net.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/telephony/config/locations" | jq -r '.locations[] | "\(.name) \(.id)"'
```

**Expected result:** the calling locations and their PSTN connection — Webex
Calling routes on-net by extension/number within the org, and off-net via the
location's PSTN choice (Cisco Calling Plan, local gateway, or Cloud-Connected
PSTN).

**Negative test:** a location with no PSTN connection can call on-net only;
external calls fail — routing off-net requires a PSTN option on the location.

**Cleanup:** none (read-only).

### Lab 7.3 — Implement toll fraud prevention on Webex Calling (CLCOR Objective 5.3)

**Objective:** Verify outbound calling permissions (OCP) that block toll fraud.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/telephony/config/locations/$LOC/outgoingPermission" | jq '.callingPermissions[] | {callType, action}'
```

**Expected result:** per-call-type actions (allow/block/auth) — Webex Calling
blocks toll fraud with **Outgoing Calling Permissions** per location/user
(block international/premium, require authorization codes) and access-code rules.

**Negative test:** leave "International" at ALLOW for every user; a compromised
account dials premium-rate numbers — restricting the call type per policy closes
it.

**Cleanup:** revert the test OCP change.

### Lab 7.4 — Configure call routing in Webex Calling (CLCOR Objective 5.4)

**Objective:** Configure a dial plan / route to the local gateway.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/telephony/config/premisePstn/routeGroups" | jq -r '.routeGroups[].name'
```

**Expected result:** the route group / trunk to the local gateway — Webex Calling
routes off-net through a **route group** of trunks (local gateways) with dial
plans and route lists, mirroring on-prem route list/route group logic in the
cloud.

**Negative test:** a dial plan whose route choice points to a trunk that is not
registered drops the call — the local gateway must be registered and in the route
group.

**Cleanup:** none (read-only).

### Lab 7.5 — Configure cloud meetings (CLCOR Objective 5.5)

**Objective:** Create and read a Webex meeting via the API.

```bash
curl -s -X POST -H "Authorization: Bearer $WBX" -H 'Content-Type: application/json' \
  https://webexapis.com/v1/meetings -d '{"title":"Lab Meeting","start":"2026-08-01T17:00:00Z","end":"2026-08-01T17:30:00Z"}' | jq '{id, webLink}'
```

**Expected result:** the created meeting with its join link — cloud meetings are
provisioned per user (PMR) or scheduled via the API/Control Hub, with site-level
policies (recording, entry) set centrally.

**Negative test:** create a meeting for a user without a Meetings license; the API
returns an error — the host must be licensed.

**Cleanup:** DELETE the test meeting by its id.

### Lab 7.6 — Configure cloud messaging (CLCOR Objective 5.6)

**Objective:** Create a Webex space and post a message via the API.

```bash
ROOM=$(curl -s -X POST -H "Authorization: Bearer $WBX" -H 'Content-Type: application/json' https://webexapis.com/v1/rooms -d '{"title":"Lab Space"}' | jq -r .id)
curl -s -X POST -H "Authorization: Bearer $WBX" -H 'Content-Type: application/json' https://webexapis.com/v1/messages -d "{\"roomId\":\"$ROOM\",\"text\":\"hello from the lab\"}" | jq '{id, roomId}'
```

**Expected result:** the space and posted message — cloud messaging (spaces) is
persistent, with memberships, files, and threading, administered by org policy
(retention, external sharing).

**Negative test:** post to a space the token's user is not a member of; the API
returns `404`/`403` — membership gates access.

**Cleanup:** DELETE the test room.

### Lab 7.7 — Describe cloud collaboration APIs and webhooks (CLCOR Objective 5.7)

**Objective:** Register a webhook and confirm event delivery.

```bash
curl -s -X POST -H "Authorization: Bearer $WBX" -H 'Content-Type: application/json' \
  https://webexapis.com/v1/webhooks -d '{"name":"lab","targetUrl":"https://example.com/hook","resource":"messages","event":"created"}' | jq '{id, status}'
```

**Expected result:** the webhook registered `active` — the Webex REST APIs are
resource-oriented (people, rooms, messages, meetings), and **webhooks** push
events (message created, membership changed) to your service for event-driven
automation.

**Negative test:** a webhook `targetUrl` that does not return `200` gets disabled
after repeated failures — the receiver must acknowledge deliveries.

**Cleanup:** DELETE the test webhook.

### Lab 7.8 — Configure cloud user management (CLCOR Objective 5.8)

**Objective:** Provision a user and read directory/RBAC via Control Hub/SCIM.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/people?email=labuser@example.com" | jq '.items[] | {emails, licenses, roles}'
```

**Expected result:** the user with licenses and roles — cloud user management runs
from Control Hub, with users synced by **Directory Connector** or **SCIM**, and
admin **RBAC** roles (full/read-only/support/device admin) scoping who can manage
what.

**Negative test:** a user synced from Directory Connector cannot have core
attributes edited in Control Hub (AD is source of truth) — the sync model dictates
authority.

**Cleanup:** none (read-only).

### Lab 7.9 — Describe Cloud-Connected UC (CLCOR Objective 5.9)

**Objective:** Read the CCUC connection for an on-prem cluster.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/devices?product=cucm" 2>/dev/null | jq '.items | length'
! In Control Hub: Connected UC shows on-prem clusters streaming analytics/telemetry
```

**Expected result:** the on-prem UCM/Expressway nodes connected to Webex —
**Cloud-Connected UC** onboards on-prem clusters to Control Hub for cloud-based
analytics, certificate, and (with Webex Calling) operational management without
moving call control.

**Negative test:** a cluster whose CCUC agent has no outbound HTTPS to Webex never
appears in Control Hub analytics — the connector needs cloud reachability.

**Cleanup:** none (read-only).

### Lab 7.10 — Describe Webex Hybrid Services (CLCOR Objective 5.10)

**Objective:** Read the hybrid connectors registered to the org.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/hybrid/connectors" 2>/dev/null | jq -r '.items[]? | "\(.type) \(.status)"'
! Control Hub > Services shows Hybrid Calendar, Directory, Calling, Message connectors
```

**Expected result:** the hybrid connectors (Calendar, Directory, Calling, Message)
and their health — Hybrid Services bridge on-prem systems to the cloud: calendar
(Exchange/O365), directory (AD), calling (Expressway), and message (IM&P
interop).

**Negative test:** a Hybrid Calendar connector in "offline" state stops @meet/@webex
keyword scheduling — the connector's health directly gates the hybrid feature.

**Cleanup:** none (read-only).

### Lab 7.11 — Configure SSO for Webex (CLHCT Objective 1.1)

**Objective:** Verify SAML SSO for the Webex org.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/organizations/$ORG" | jq '{displayName}'
! Control Hub > Management > Organization Settings > Authentication shows the IdP/SSO status
```

**Expected result:** the org with SSO configured against the IdP — Webex SSO
redirects user authentication to the enterprise IdP (SAML), the same trust model
as on-prem UCM SSO, so users sign in once with corporate credentials.

**Negative test:** an IdP metadata/cert that has rotated but was not re-uploaded to
Control Hub breaks every SSO login org-wide — the SP↔IdP trust must stay current.

**Cleanup:** none (read-only).

### Lab 7.12 — Configure directory synchronization (CLHCT Objective 1.2)

**Objective:** Confirm Directory Connector sync from AD to Webex.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/people?max=5" | jq -r '.items[] | .emails[0]'
! Control Hub > Users shows sync source (Directory Connector / Azure AD / SCIM)
```

**Expected result:** users present with an on-prem sync source — Directory
Connector (or Azure AD/SCIM) synchronizes user identities from AD into Webex so
the cloud directory matches the enterprise, feeding calling/meeting entitlement.

**Negative test:** a user deleted in AD but with a broken sync remains active in
Webex, keeping a license — sync health governs deprovisioning too.

**Cleanup:** none (read-only).

### Lab 7.13 — Configure hybrid calendar service (CLHCT Objective 1.3)

**Objective:** Verify Hybrid Calendar keyword scheduling via cloud mail.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/hybrid/connectors" 2>/dev/null | jq -r '.items[]? | select(.type=="c_cal") | .status'
! Add @webex to a calendar invite; confirm join details are injected
```

**Expected result:** the calendar connector `operational` and join details
injected into invites — Hybrid Calendar (via O365/Google cloud mail or on-prem
Exchange) turns `@webex`/`@meet` keywords into meeting join info and sets
presence from calendar.

**Negative test:** a mailbox not enabled for the calendar service gets no join
injection despite the keyword — the service must be enabled per user.

**Cleanup:** none (read-only).

### Lab 7.14 — Configure local gateways (CLHCT Objective 1.4)

**Objective:** Register an IOS XE local gateway to Webex Calling.

```text
show run | section voice class tenant       ! Webex tenant on the LGW
show sip-ua status registrar
show voip rtp connections
```

**Expected result:** the local gateway registered to Webex Calling with its
tenant and SIP trunk — the LGW (a CUBE) provides PSTN and on-prem interconnect
for Webex Calling, bridging cloud call control to local/PSTN circuits.

**Negative test:** an LGW whose SBC certificate or SIP credentials are wrong fails
registration to Webex; `show sip-ua status registrar` shows it not registered — the
trust to Webex must be correct.

**Cleanup:** none (read-only).

### Lab 7.15 — Configure site survivability (CLHCT Objective 1.5)

**Objective:** Verify Webex Calling survivability on the local gateway.

```text
show voice register global | include survivability
show voice register pool all
```

**Expected result:** the survivability gateway with locally registered phones —
Webex Calling **Survivability Gateway** (on the LGW) keeps a site's phones calling
locally and to PSTN during a cloud/WAN outage, re-registering to the cloud on
recovery.

**Negative test:** a survivability gateway sized below the site's phone count
leaves some phones down during an outage — capacity must match the site.

**Cleanup:** none (read-only).

### Lab 7.16 — Configure Control Hub calling features (CLHCT Objective 1.6)

**Objective:** Configure a calling feature (hot desking / auto attendant).

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/telephony/config/locations/$LOC/autoAttendants" | jq -r '.autoAttendants[].name'
```

**Expected result:** the auto attendants (or hoteling/hot-desk profiles) for the
location — Control Hub configures calling features (auto attendant, hunt groups,
call queues, hot desking) per location without on-prem hardware.

**Negative test:** an auto attendant with a menu key routing to an unassigned
extension dead-ends — the feature's targets must exist, like on-prem.

**Cleanup:** remove the test auto attendant.

### Lab 7.17 — Troubleshoot cloud user management (CLHCT Objective 2.1)

**Objective:** Diagnose a user with wrong licenses/roles or failed sync.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/people?email=labuser@example.com" | jq '.items[] | {licenses, roles, invitePending}'
```

**Expected result:** the user's licenses, roles, and invite state — a user who
cannot call/meet traces to a missing license; one who cannot admin traces to a
missing role; `invitePending true` means they never activated.

**Negative test:** blame calling config for a user whose Calling license was never
assigned — the entitlement, not the dial plan, is the fault.

**Cleanup:** none (read-only).

### Lab 7.18 — Diagnose network issues for Webex (CLHCT Objective 2.2)

**Objective:** Test bandwidth/QoS reachability to the Webex cloud.

```bash
curl -s -o /dev/null -w 'connect=%{time_connect} ttfb=%{time_starttransfer}\n' https://webexapis.com/v1/ping 2>/dev/null
! Verify required ports/IP ranges and DSCP marking egress to Webex media
```

**Expected result:** low connect/TTFB and correct media port/DSCP handling —
Webex media quality depends on reaching the Webex IP ranges on the required
UDP ports with QoS preserved; blocked ports force TCP/443 fallback and degrade
media.

**Negative test:** a firewall blocking Webex media UDP forces media over TCP,
raising latency and jitter — the port/QoS path, not the client, causes the
quality drop.

**Cleanup:** none (read-only).

### Lab 7.19 — Troubleshoot Webex Calling (CLHCT Objective 3.1)

**Objective:** Diagnose a Webex Calling registration/call failure.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/telephony/config/people/$PID/devices" 2>/dev/null | jq '.devices[]? | {model, connectionStatus}'
```

**Expected result:** the device connection status — a phone `disconnected` from
Webex Calling traces to network reachability, provisioning, or credentials;
call failures with registration up trace to the location's PSTN/route.

**Negative test:** a device showing `connected` but calls failing off-net is a
route-group/PSTN problem, not registration — split the two symptoms.

**Cleanup:** none (read-only).

### Lab 7.20 — Troubleshoot call routing in Webex Calling (CLHCT Objective 3.2)

**Objective:** Diagnose a misrouted or failing off-net call.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/telephony/config/locations/$LOC" | jq '{pstnConnectionType: .connectionType}'
! Use the Control Hub Calling > Call History / analytics for the failed call's route
```

**Expected result:** the location's PSTN type and the failed call's route in
analytics — misrouting traces to the dial plan, route choice, or an OCP block;
call history shows the disposition.

**Negative test:** a call blocked by an Outgoing Calling Permission looks like a
routing failure but is policy — call history shows "blocked", not "no route".

**Cleanup:** none (read-only).

### Lab 7.21 — Troubleshoot cloud meetings (CLHCT Objective 3.3)

**Objective:** Diagnose a meeting join/quality problem.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/meetings/$MID" | jq '{state, joinLink}'
! Control Hub > Troubleshooting shows per-participant join method and media quality
```

**Expected result:** the meeting state and per-participant media metrics — join
failures trace to license/entry policy; quality issues trace to the participant's
network (packet loss/jitter), visible in Control Hub Troubleshooting.

**Negative test:** blame the meeting service for one participant's poor audio when
Troubleshooting shows only their leg has loss — it is that participant's network.

**Cleanup:** none (read-only).

### Lab 7.22 — Troubleshoot cloud messages (CLHCT Objective 3.4)

**Objective:** Diagnose message delivery / space access.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/memberships?roomId=$ROOM" | jq -r '.items[].personEmail'
```

**Expected result:** the space's members — a user not seeing messages is usually
not a member, or an org **external communication** policy blocks the space;
membership and policy explain most "missing message" reports.

**Negative test:** an external user blocked by org policy cannot be added to the
space; the add fails — the policy, not a bug, prevents it.

**Cleanup:** none (read-only).

### Lab 7.23 — Troubleshoot endpoint registration to the cloud (CLHCT Objective 3.5)

**Objective:** Diagnose a Webex device that will not register/onboard.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/devices" | jq -r '.items[] | "\(.displayName) \(.connectionStatus)"'
```

**Expected result:** each device's connection status — a device stuck offline
traces to a bad activation code, network/proxy blocking Webex, or a certificate
issue; the status plus the device's onboarding method localize it.

**Negative test:** a device behind a proxy that intercepts TLS fails cloud
registration with a cert error — the proxy, not the device, breaks the trust.

**Cleanup:** none (read-only).

### Lab 7.24 — Describe administration functions in Webex (CLHCT Objective 4.1)

**Objective:** Read the org-level administration controls.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/organizations/$ORG/settings" 2>/dev/null | jq '.' | head
! Control Hub: Users, Devices, Services, Analytics, Troubleshooting, Settings, Roles
```

**Expected result:** the org settings surface — Control Hub administers users,
devices, services, analytics, security/compliance, and roles from one pane;
admin functions are RBAC-scoped and audited.

**Negative test:** a read-only admin attempting a config change is denied — the
administration functions honor RBAC.

**Cleanup:** none (read-only).

### Lab 7.25 — Describe AI features in cloud collaboration (CLHCT Objective 4.2)

**Objective:** Read the AI Assistant / analytics features enabled in the org.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/meetingTranscripts" 2>/dev/null | jq '.items | length'
! Control Hub shows AI Assistant, summaries, transcription, and analytics toggles
```

**Expected result:** transcripts/summaries available where AI is enabled — Webex
AI features (meeting summaries, transcription, real-time translation, agent
assist) are org/site-policy controlled and surface in meetings and analytics.

**Negative test:** transcripts absent because the site policy disables recording/
transcription — the AI feature depends on its enabling policy.

**Cleanup:** none (read-only).

### Lab 7.26 — Describe Control Hub migration tool options (CLHCT Objective 4.3)

**Objective:** Read the available on-prem-to-cloud migration tools.

```bash
! Control Hub > migration tools: Webex Calling device migration, UCM-to-Webex, config import
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/telephony/config/jobs/devices/callDeviceSettings" 2>/dev/null | jq '.' | head
```

**Expected result:** the migration jobs/tools available — Control Hub provides
tools to migrate on-prem UCM users/devices to Webex Calling (device migration
tool, bulk CSV, config import), each with pre-checks and rollback.

**Negative test:** running a device migration without the firmware/network
prerequisites fails the pre-check — the tool validates before migrating.

**Cleanup:** none (read-only).

### Lab 7.27 — Configure hybrid and migration from on-premises to cloud (CLHCT Objective 5.1)

**Objective:** Move a user from on-prem calling to Webex Calling.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/telephony/config/people/$PID" | jq '{callingType: .calling.type}'
```

**Expected result:** the user's calling type flipping to Webex Calling — hybrid
migration moves users in phases (calling, meetings, messaging), often coexisting
with on-prem during cutover via directory sync and number porting/routing.

**Negative test:** migrate a user's calling to the cloud without porting or routing
their DID; inbound PSTN still lands on-prem — number routing must move with the
user.

**Cleanup:** revert the test user to on-prem calling.

### Lab 7.28 — Configure advanced dial plans (CLHCT Objective 5.2)

**Objective:** Configure cross-premises/cloud dial-plan interworking.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/telephony/config/premisePstn/dialPlans" 2>/dev/null | jq -r '.dialPlans[]?.name'
```

**Expected result:** the dial plans routing between cloud and on-prem — advanced
dial plans interwork Webex Calling and on-prem UCM so extension dialing, +E.164,
and PSTN egress work consistently during and after migration.

**Negative test:** overlapping extension ranges between cloud and on-prem without
a routing rule cause ambiguous routing — the dial plan must disambiguate.

**Cleanup:** none (read-only).

### Lab 7.29 — Implement Webex security (CLHCT Objective 6.1)

**Objective:** Apply security for admin, endpoints, meetings, and compliance.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/organizations/$ORG" | jq '{isEnforcedStrongPassword: .isEnforcedStrongPassword}' 2>/dev/null
! Control Hub: MFA/SSO for admins, device PIN/lock, meeting entry/lock, compliance (eDiscovery, DLP, retention)
```

**Expected result:** the org security posture — Webex security spans admin
(SSO/MFA, RBAC), endpoints (PIN, encryption), meetings (lock, entry, E2E where
enabled), and compliance (retention, eDiscovery, DLP, legal hold).

**Negative test:** admins without MFA/SSO are a high-value target; a single
compromised admin credential exposes the org — enforcing SSO/MFA for admins closes
it.

**Cleanup:** none (read-only).

### Lab 7.30 — Describe the Webex cloud security realm architecture (CLHCT Objective 6.2)

**Objective:** Read where identity, media, and content trust boundaries sit.

```bash
! Conceptual verification: confirm org identity (IdP), KMS for content encryption, and media encryption
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/organizations/$ORG" | jq '{id}'
```

**Expected result:** the org bound to its identity realm and encryption services —
Webex encrypts content with keys from a Key Management Server (cloud or, with
Hybrid Data Security, on-prem) and secures media with SRTP; the "realm" is the
trust domain of the org.

**Negative test:** assuming Webex content is plaintext to Cisco; with standard
encryption Cisco holds keys, and with **Hybrid Data Security** the customer holds
them — the realm choice determines key custody.

**Cleanup:** none (read-only).

### Lab 7.31 — Configure hybrid data security deployment (CLHCT Objective 6.3)

**Objective:** Read the Hybrid Data Security (HDS) node/trust state.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/hybrid/connectors" 2>/dev/null | jq -r '.items[]? | select(.type|test("hds";"i")) | .status'
! Control Hub > Hybrid Data Security shows the on-prem KMS/HDS node cluster
```

**Expected result:** the on-prem HDS cluster `operational` — HDS keeps the content
encryption keys on customer-owned nodes so Webex stores only ciphertext, giving
the customer key custody for compliance.

**Negative test:** an HDS cluster below quorum stops issuing keys and messaging
stalls for the org — HDS must maintain its node quorum.

**Cleanup:** none (read-only).

### Lab 7.32 — Describe App Hub, Developer Portal, and Room OS Portal (CLHCT Objective 7.1)

**Objective:** Identify the developer/integration surfaces.

```bash
! App Hub: pre-built integrations/bots; developer.webex.com: APIs/SDKs; Room OS controls devices
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/applications" 2>/dev/null | jq '.items | length' 2>/dev/null || echo "see App Hub in Control Hub"
```

**Expected result:** the integration surfaces — **App Hub** lists vetted
integrations/bots to enable per org, the **Developer Portal**
(`developer.webex.com`) exposes REST APIs/SDKs, and the **Room OS/Device** APIs
control collaboration endpoints.

**Negative test:** enabling an App Hub integration grants it API scopes; over-broad
scopes are a risk — review the requested permissions before authorizing.

**Cleanup:** none (read-only).

### Lab 7.33 — Describe macros on devices (CLHCT Objective 7.2)

**Objective:** Read the macros deployed on a Room OS device.

```bash
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/deviceConfigurations?deviceId=$DEV" 2>/dev/null | jq '.items | keys' | head
! Room OS: Macros are JavaScript running on the device reacting to xAPI events
```

**Expected result:** the device's configuration/macros — Room OS **macros** are
on-device JavaScript reacting to xAPI events (button press, call state) to
customize the endpoint's behavior and UI without a server.

**Negative test:** a macro with an infinite loop or a bad xAPI call can hang the
device UI — macros run on the endpoint and must be efficient.

**Cleanup:** none (read-only).

### Lab 7.34 — Construct Webex APIs: Messaging, Meeting, Calling, People, Events (CLHCT Objective 7.3)

**Objective:** Chain several Webex APIs in one automation.

```bash
ME=$(curl -s -H "Authorization: Bearer $WBX" https://webexapis.com/v1/people/me | jq -r .id)
curl -s -H "Authorization: Bearer $WBX" "https://webexapis.com/v1/events?resource=messages&max=3" | jq -r '.items[]? | .type'
```

**Expected result:** identity (People), history (Events), and the ability to act
on Messaging/Meeting/Calling — the Webex APIs compose: read People, subscribe to
Events, and drive Messaging/Meetings/Calling for end-to-end automation.

**Negative test:** an integration token missing the `spark:kms` or a required
scope fails encrypted-content calls — each API needs its OAuth scope granted.

**Cleanup:** none (read-only).

### Lab 7.35 — Configure a Mobile and Remote Access solution (CLACC Objective 5.1)

**Objective:** Bring up MRA through the Expressway pair.

```text
xstatus Zone            ! on Expressway-C: UC traversal zone to Expressway-E
xstatus Zone Traversalclient
! On Expressway-E:
xstatus Zone Traversalserver
```

**Expected result:** the traversal client/server zones up between Expressway-C and
-E, and discovered UC services — MRA lets Jabber/Webex App and endpoints register
to UCM from outside the firewall without a VPN, via the Expressway pair.

**Negative test:** a `_collab-edge` SRV missing or an Expressway-E cert without the
external FQDN in its SAN blocks MRA login — discovery and cert SAN are the common
breaks.

**Cleanup:** none (read-only).

### Lab 7.36 — Troubleshoot a Mobile and Remote Access solution (CLACC Objective 5.2)

**Objective:** Diagnose an MRA login/registration failure.

```text
xstatus Zone Traversalclient        ! traversal up?
xstatus Alarm                        ! Expressway alarms (cert, config)
! On Expressway-C: check UC service discovery and SSO-over-MRA (OAuth) status
```

**Expected result:** the traversal state and alarms — MRA failures trace to
`_collab-edge` DNS, the traversal zone, certificate trust between C and E, or
OAuth/SSO-over-MRA; the alarms and zone status localize the layer.

**Negative test:** an MRA client that authenticates but cannot register is usually
a UC service/discovery problem on Expressway-C, not the traversal zone — split
auth from registration.

**Cleanup:** none (read-only).

### Lab 7.37 — Describe Expressway media traversal (CLACC Objective 5.3)

**Objective:** Read the media traversal (Assent/H.460) between C and E.

```text
xstatus Zone Traversalserver
xconfiguration Zones Zone Traversalserver
show voip rtp connections    ! (on associated gateway) media anchored via Expressway
```

**Expected result:** the traversal zone carrying media — Expressway traverses
firewalls for signaling and media using Assent (Cisco) or H.460.18/.19, so a
single outbound-initiated connection carries calls without inbound firewall
pinholes.

**Negative test:** blocking the small set of Expressway-E outbound/large media port
range breaks media while signaling survives — one-way/no audio results; the media
port range must be open on Expressway-E.

**Cleanup:** none (read-only).

### Lab 7.38 — Describe protocol interworking on Expressway (CLACC Objective 5.4)

**Objective:** Read SIP/H.323 and IPv4/IPv6 interworking on Expressway.

```text
xconfiguration Zones Policy SIP
xstatus Calls              ! shows protocol/interworking per call
```

**Expected result:** calls interworked between SIP and H.323 and between IPv4 and
IPv6 — Expressway interworks legacy H.323 endpoints with SIP and bridges dual-stack
networks, so mixed estates and B2B partners interoperate.

**Negative test:** a call between an IPv6-only endpoint and an IPv4-only peer with
interworking disabled fails — Expressway's interworking is what bridges them.

**Cleanup:** none (read-only).

### Lab 7.39 — Configure encrypted calling in Expressway (CLACC Objective 5.5)

**Objective:** Verify TLS/SRTP media encryption through Expressway.

```text
xconfiguration Zones Zone SIP Media Encryption Mode
xstatus Calls | grep -i encrypt
```

**Expected result:** the zone requiring encrypted media and calls showing
SRTP — Expressway can enforce TLS signaling and SRTP media (best-effort or
force-encrypted) so external/B2B calls are protected end to edge.

**Negative test:** a zone set to "force encrypted" toward a peer that offers only
RTP drops the call — the media encryption modes must be compatible.

**Cleanup:** none (read-only).

### Lab 7.40 — Configure security for Cisco Expressway (CLACC Objective 5.6)

**Objective:** Verify Expressway hardening (certs, auth, firewall rules).

```text
xstatus Alarm | grep -i cert
xconfiguration Authentication
xconfiguration SystemUnit Firewall Rules
```

**Expected result:** valid certs, credential authentication, and firewall rules —
Expressway security includes CA-signed certs with correct SANs, restricting
registration authentication, hardening ciphers, and edge firewall rules on
Expressway-E.

**Negative test:** an Expressway-E with default self-signed certs and open
management to the internet is exposed — CA certs and management-access restrictions
are required at the edge.

**Cleanup:** none (read-only).

### Lab 7.41 — Troubleshoot a Business to Business solution (CLACC Objective 5.7)

**Objective:** Diagnose a B2B call failure between organizations.

```text
xstatus Calls
xstatus Zone            ! DNS zone / traversal to the partner
search history          ! Expressway search rules for the B2B domain
```

**Expected result:** the B2B call's search-rule match and zone — B2B calls route
via a DNS zone (SRV lookup of the partner domain) and search rules; failures trace
to DNS/SRV for the partner, search-rule scope, or media encryption/interworking
mismatch.

**Negative test:** a B2B call failing because the partner's `_sips._tcp` SRV does
not resolve is a DNS problem, not an Expressway config problem — verify the
partner's SRV first.

**Cleanup:** none (read-only).

## Lab Verification

Verification means external MRA sign-in worked against the
documented chain, B2B routed with Locate evidence, the hybrid
service is client-visible, and both induced edge failures matched
their predicted signatures. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The edge publishes collaboration per-service instead of per-network:
the traversal pair's outbound trust design, MRA's
DNS-certificate-discovery chain, B2B's DNS-and-search-rule
federation, and Webex hybrid stitching cloud onto premises. It is
CLHCT entire and the core's heaviest cloud domain — and it is where
Chapter 02's protocols, 05's border craft, and 06's SSO all meet
the internet.

- [ ] I can draw the traversal trust model and defend each firewall
      rule
- [ ] My SAN worksheet predates my CSR
- [ ] MRA, B2B, and one hybrid service verified with evidence
- [ ] I diagnosed edge failures by chain position, not guesswork
