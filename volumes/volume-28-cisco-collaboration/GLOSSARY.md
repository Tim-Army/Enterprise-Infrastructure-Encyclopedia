# Volume XXVIII Glossary

Definitions for terms introduced in **Volume XXVIII — Cisco
Collaboration**, alphabetized. See also the [volume index](INDEX.md)
for pointers back to the chapter each term is drawn from, and the
[master glossary](../../GLOSSARY.md) for cross-volume terminology.

**AXL (Administrative XML)** — Cisco Unified CM's SOAP/XML
provisioning API, used for bulk and automated management of devices,
lines, users, and dial-plan objects. Introduced in Chapter 03.

**Calling search space (CSS)** — An ordered list of partitions a
caller may reach; with partitions, it expresses class of service in
the dial plan. Introduced in Chapter 04.

**CUBE (Cisco Unified Border Element)** — IOS XE's session border
controller: a back-to-back user agent that splits each call into two
legs to normalize, secure, and manage signaling and media at the
PSTN/ITSP boundary. Introduced in Chapter 05.

**CMR (Call Management Record)** — A per-call quality record (loss,
jitter, concealment) CUCM produces, used to quantify call quality
after the fact. Introduced in Chapter 08.

**Device pool** — A CUCM object bundling region, location, Unified CM
group, and other settings, assigned to devices so site-wide intent
lives in one place. Introduced in Chapter 03.

**Expressway (C/E pair)** — Cisco's firewall-traversal edge:
Expressway-C inside registers outbound to Expressway-E in the DMZ,
publishing collaboration services (MRA, B2B) without inbound
trust-network exposure or VPN. Introduced in Chapter 07.

**Globalized dial plan** — A design storing and routing all numbers
in +E.164 canonical form, localizing to site or provider formats only
at ingress and egress. Introduced in Chapter 04.

**Hunt pilot / hunt list / line group** — The CUCM construct chain
distributing calls to a set of lines by a selected algorithm.
Introduced in Chapter 04.

**IM and Presence Service (IM&P)** — The CUCM-integrated XMPP
platform providing presence and instant messaging to Jabber and
Webex App, with intra- and inter-domain federation. Introduced in
Chapter 06.

**Location (call admission control)** — A CUCM object with bandwidth
pools that admits or denies calls to protect existing calls' quality
across constrained links. Introduced in Chapter 03.

**MRA (Mobile and Remote Access)** — Publishing CUCM registration
through the Expressway pair so off-network clients get full calling,
voicemail, and presence without a VPN. Introduced in Chapter 07.

**MRGL (Media Resource Group List)** — An ordered list of media
resource groups assigned to devices, governing which conference,
transcoder, MTP, and MOH resources a device draws and in what order.
Introduced in Chapter 08.

**MTP (Media Termination Point)** — A media resource bridging RTP
variants or satisfying protocol requirements between call legs.
Introduced in Chapter 08.

**Partition** — A label applied to dialable objects (DNs, patterns);
combined with calling search spaces, it contains who can call what.
Introduced in Chapter 04.

**Publisher / subscriber** — The CUCM cluster roles: the publisher
holds the writable database, subscribers replicate it and run call
processing. Introduced in Chapter 03.

**Region** — A CUCM object setting the maximum codec between groups
of devices, implementing bandwidth-aware codec policy. Introduced in
Chapter 03.

**Route pattern / route list / route group** — The CUCM routing
pipeline: a dialed pattern selects a route list (strategy) of route
groups (gateway/trunk pools). Introduced in Chapter 04.

**SAML SSO** — Single sign-on in which an identity provider
authenticates the user and returns a signed assertion, so
collaboration applications never handle the password. Introduced in
Chapter 06.

**SDP (Session Description Protocol)** — The offer/answer body in SIP
that negotiates codecs, media addresses, ports, and DTMF handling.
Introduced in Chapter 02.

**SIP dialog** — The established relationship identified by From-tag,
To-tag, and Call-ID that in-dialog SIP requests reference. Introduced
in Chapter 02.

**SNR (Single Number Reach / Mobile Connect)** — A feature ringing
desk and mobile simultaneously with mid-call pull-back. Introduced in
Chapter 04.

**SRST (Survivable Remote Site Telephony)** — A branch router's
resident minimal call agent that registers phones and carries a
reduced dial plan during WAN loss. Introduced in Chapter 04.

**Unity Connection** — Cisco's voicemail and messaging application:
call handlers, mailboxes, and MWI, integrated with CUCM by SIP trunk.
Introduced in Chapter 06.

**Webex Contact Center** — Cisco's cloud contact-center platform:
telephony and routing, tenant configuration and reporting, digital
channels, and AI features; the subject of the CLCCE exam. Introduced
in Chapter 09.

**Webex hybrid services** — Integrations (Calendar, Directory,
Message, Calling via Local Gateway) stitching the Webex cloud to an
on-premises collaboration estate, managed through Control Hub.
Introduced in Chapter 07.
