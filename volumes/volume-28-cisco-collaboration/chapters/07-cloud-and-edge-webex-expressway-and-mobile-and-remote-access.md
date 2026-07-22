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
media). What this buys CLCEI's Key Concepts domain: no VPN client,
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

- CLCEI 300-820 v1.2 exam topics (four domains at 25% each)
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

Deploy the pair (Expressway OVAs in the lab or DevNet sandbox):
base networking, trust stores, traversal zones. Publish MRA for the
Chapter 06 estate — public-style DNS in the lab domain, SAN
worksheet written then embodied in E's certificate, UC discovery
TLS-verified — and sign in from an "external" network segment,
capturing the SRV query and edge registration. Add one B2B search
rule pair and prove a URI call outward to a second lab domain (or
loopback domain), with `Locate` evidence archived. In Control Hub
(free org), enable one hybrid service (Calendar is the least
infrastructure-hungry) and show the client-visible result. Break
and evidence: remove one SAN and reproduce the service-specific MRA
failure; block the traversal media range on the inner firewall and
capture the signaling-works-media-fails signature. Repair both.

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
CLCEI entire and the core's heaviest cloud domain — and it is where
Chapter 02's protocols, 05's border craft, and 06's SSO all meet
the internet.

- [ ] I can draw the traversal trust model and defend each firewall
      rule
- [ ] My SAN worksheet predates my CSR
- [ ] MRA, B2B, and one hybrid service verified with evidence
- [ ] I diagnosed edge failures by chain position, not guesswork
