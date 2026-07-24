# Chapter 02: Signaling and Media: SIP, Codecs, and Endpoints

## Learning Objectives

- Read SIP fluently: methods, responses, headers, transactions, and
  dialogs
- Explain SDP offer/answer and how codec, address, and port
  negotiation actually happens
- Compare media behaviors: RTP/SRTP, DTMF relay options, and what
  early media is for
- Describe endpoint types and their registration flows against CUCM
  and Webex
- Capture and analyze a complete call setup, and diagnose the classic
  signaling and media failures

## Theory and Architecture

### SIP: the protocol you will read every week

SIP is text over UDP, TCP, or TLS (5060/5061), and reading it raw is
a daily skill CLCOR and CLACC both assume. The grammar:

- **Methods** — INVITE (start/modify a session), ACK (complete the
  INVITE handshake), BYE, CANCEL, REGISTER, OPTIONS (keepalive and
  capability probe), REFER (transfer), SUBSCRIBE/NOTIFY (events),
  UPDATE and re-INVITE (mid-call changes).
- **Responses** — 1xx provisional (100 Trying, 180 Ringing, 183
  Session Progress carrying early media), 2xx success, 3xx redirect,
  4xx client errors (401/407 auth challenges, 404, 486 Busy, 488 Not
  Acceptable — the codec-mismatch signature), 5xx server, 6xx global.
- **Headers that matter in anger** — Via (response routing, one per
  hop), From/To (logical parties), Call-ID (the dialog's identity in
  every trace search), CSeq, Contact (where to reach this party
  directly), Route/Record-Route (proxies inserting themselves into
  the dialog path), Max-Forwards.

A **transaction** is request-plus-responses; a **dialog** is the
established relationship (From-tag, To-tag, Call-ID) that in-dialog
requests reference. Troubleshooting language is precise here: "the
INVITE transaction completed but the dialog dropped on the first
re-INVITE" locates a fault class exactly.

### SDP offer/answer: where calls are actually negotiated

The INVITE's body carries SDP: connection address (`c=`), media lines
(`m=audio <port> RTP/AVP <payload types>`), and attributes
(`a=rtpmap`, `a=sendrecv`, direction and DTMF telephone-event
declarations). The answer selects from the offer. Failure modes to
recognize on sight: no overlapping codec → 488; SDP address
unreachable from the peer → one-way or no-way audio (signaling was
fine — the media path, NAT, or firewall was not); mid-call re-INVITE
changing `c=`/ports (hold, transfer, media steering) mishandled by a
middlebox → call drops on hold. **DTMF** deserves its own line:
RFC 2833/4733 telephone-events in-band-in-RTP versus KPML/SIP INFO
signaling — mismatched relay between legs is the "IVR ignores my
keypresses" ticket, and CUBE (Chapter 05) exists partly to interwork
it.

### Media: RTP and its guarantees

RTP carries media with sequence numbers and timestamps; RTCP reports
loss and jitter; SRTP encrypts with keys exchanged in SDP
(SDES-sRTP) or via DTLS. Voice quality arithmetic that Chapter 08
budgets: one-way delay target ≤150 ms, jitter absorbed by buffers at
the cost of delay, loss above ~1% audible with modern codecs. Codec
choices in Cisco estates: G.711 (64 kbps, the PSTN's lingua franca),
G.729 (8 kbps legacy WAN), **Opus** (adaptive, the modern default
toward soft clients and Webex), G.722 wideband on-campus.

### Endpoints and registration

Hardware phones (88xx/78xx heritage and current Cisco devices), video
devices (Room/Board/Desk series), and soft clients (Webex App,
Jabber). Registration flows differ and the differences are exam
material: phones boot → DHCP Option 150 → TFTP configuration → SIP
REGISTER to their CUCM group with digest/certificate identity; Webex
App discovers via SRV/UDS (Chapter 01's lab) and registers to CUCM
for calling while attaching to the cloud for messaging; cloud-native
devices onboard to Webex with activation codes. Chapter 07 adds the
MRA path — the same REGISTER, proxied through Expressway.

## Design Considerations

- **Transport and trunk defaults**: TLS everywhere feasible; UDP's
  fragmentation of large INVITEs (many codecs + video + security
  attributes) still bites — TCP/TLS trunks avoid a classic
  intermittent failure.
- **Codec policy by region** (Chapter 03's regions implement it):
  wideband/Opus where bandwidth allows, transcode only where
  unavoidable — every transcode spends DSPs and quality.
- **DTMF consistency end to end**: standardize on RFC 2833/4733,
  document the exceptions, and let CUBE interwork the rest.
- **Early media policy**: 183-with-SDP lets callers hear real ringback
  and announcements from far networks; blocking it "for security"
  produces silent-until-answer complaints.

## Implementation and Automation

The lab's reading exercise — capture a two-party call and annotate
it:

```text
# On the lab CUBE or a SPAN of the phone VLAN:
# Filter the dialog in Wireshark
sip.Call-ID == "<call-id>"
# Or on CUCM, RTMT / file get activelog for SDL/SDI traces

# The sequence you annotate:
INVITE (SDP offer: G.711, G.722, Opus; telephone-event 101)
100 Trying          <- transaction alive, keep waiting
180 Ringing         <- no SDP: local ringback
200 OK (SDP answer: G.722 selected; telephone-event 101)
ACK                 <- dialog established
RTP both directions (verify with rtp.streams in Wireshark)
BYE / 200 OK        <- clean teardown
```

Useful CUCM-side verification while the call is up:

```text
# RTMT: Call Manager > Call Activity; or CLI perfmon
show perf query class "Cisco CallManager" CallsActive
# Device registration state
show risdb query phone | include <MAC|IP>
```

## Validation and Troubleshooting

Method: **signaling first, then media, then quality.** If the call
does not establish, follow the transaction — where did the expected
next message not arrive, and which hop's Via should have carried it?
401/407 loops are identity/digest problems; 488 is codec policy; a
CANCEL after user answer is timing. If the call establishes but audio
fails, go straight to SDP: are the `c=` addresses reachable in both
directions? One-way audio is a routing/NAT statement, not a "voice
problem." If quality degrades, it is Chapter 08's counters (loss,
jitter, MOS from RTCP/CMRs). The discipline: every conclusion cites a
message or a counter — Volume XXVII's evidence habit, applied to
dialogs.

## Security and Best Practices

- SIP TLS and SRTP as the default posture; unencrypted SIP on
  monitored internal segments is legacy to be retired, not policy.
- OPTIONS abuse and REGISTER scanning arrive within hours of any
  internet-exposed 5060 — never expose raw call control; the edge
  (Chapter 07) and CUBE (Chapter 05) exist for boundary duty.
- Log Call-IDs in every ticket; they are the primary key of every
  investigation across platforms.

## References and Knowledge Checks

- RFC 3261 (SIP), RFC 3264 (offer/answer), RFC 4733 (DTMF events)
- CLACC 300-815 v2.0 domain 1 (Signaling and Media Protocols, 10%)
- Cisco Collaboration SRND, media and codec sections

Knowledge checks:

1. Which three values identify a dialog, and why does CANCEL only
   make sense before a final response?
2. A caller hears nothing until answer when calling one carrier.
   Which provisional response behavior explains it?
3. Diagnose from symptoms: call connects, IVR ignores keypresses.
   Name the two most likely mismatches and where you would prove it.
4. Why does one-way audio implicate the network rather than call
   control, and which SDP line do you check first?

## Hands-On Lab

This chapter carries a topic-level walkthrough lab for **Domains 1
(Infrastructure and Design) and 2 (Protocols and Endpoints) of the CLCOR
350-801 v2.0 exam guide** — mapped in the volume README's coverage tables. Labs
use the Unified CM CLI (`admin:` shell), the Real-Time Monitoring Tool (RTMT)
counters, and SIP/registration troubleshooting. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 2.1–2.8** — a Unified CM cluster (publisher +
subscriber) reachable at `$CUCM`, a CUBE (IOS XE) SBC, registered SIP endpoints
and a soft client, and a management station with SSH and the AXL toolkit.
**Cost:** none beyond lab resources.

### Lab 2.1 — Describe on-premises, hybrid, and cloud design elements (Objective 1.1)

**Objective:** Read the deployment model a cluster participates in.

```text
admin:show network cluster
admin:run sql select name,description from processnode
utils service list | grep -i "Cisco CallManager"
```

**Expected result:** the cluster nodes and running call-control service — an
**on-premises** design runs call control locally; **hybrid** adds Webex services
(directory/calendar/calling) via Expressway connectors; **cloud** moves call
control to Webex Calling. The node list plus enabled services locates the model.

**Negative test:** assume "hybrid" from the presence of Expressway alone;
Expressway also serves pure on-prem MRA — the enabled Webex connectors, not the
edge box, define hybrid.

**Cleanup:** none (read-only).

### Lab 2.2 — Describe the purpose of edge devices (Objective 1.2)

**Objective:** Identify each edge device and the boundary it serves.

```text
show running-config | section voice service voip     ! on CUBE
admin:show network eth0 detail                         ! CUCM side
```

**Expected result:** CUBE terminating SIP trunks at the PSTN/ITSP edge, and
(where present) Expressway-C/E at the internet edge for MRA/B2B — edge devices
demarcate trust, normalize SIP, and traverse NAT/firewalls so internal call
control never faces the outside directly.

**Negative test:** point an ITSP trunk straight at UCM with no CUBE; UCM is
exposed to external SIP and cannot normalize provider quirks — the edge device
exists precisely to prevent that.

**Cleanup:** none (read-only).

### Lab 2.3 — Describe the cluster upgrade process for Communications Manager (Objective 1.3)

**Objective:** Read the active/inactive partition state that drives an upgrade.

```text
admin:show version active
admin:show version inactive
admin:utils system upgrade status
```

**Expected result:** the active and inactive versions — UCM upgrades install to
the **inactive partition**, then a switch-version reboots into it, so a rollback
is a switch back; the status command shows an in-progress upgrade's stage.

**Negative test:** attempt a switch-version with no image on the inactive
partition; UCM refuses — the upgrade must complete to the inactive side first.

**Cleanup:** none (read-only).

### Lab 2.4 — Troubleshoot security components (Objective 1.4)

**Objective:** Diagnose a mixed-mode/CTL or certificate problem.

```text
admin:show ctl
admin:utils ctl show
admin:show cert list own
admin:show cert list trust
```

**Expected result:** the CTL file (mixed-mode) and the cluster's own/trust
certificates with expiry — expired or missing certs break TLS SIP, secure
registration, and phone config download; the CTL governs mixed-mode trust.

**Negative test:** an expired CallManager cert leaves TLS phones unregistered
while non-secure phones work — the split symptom points straight at the cert,
not the network.

**Cleanup:** none (read-only).

### Lab 2.5 — Troubleshoot network components (Objective 1.5)

**Objective:** Diagnose a network-layer problem affecting collaboration.

```text
admin:utils network ping <gateway>
admin:utils network traceroute <subscriber>
admin:show network dns
admin:utils ntp status
```

**Expected result:** reachability, DNS resolution, and NTP sync — collaboration
depends on all three: DNS for service discovery, NTP for cert validity and CDR
timestamps, and low-loss paths for media; the four checks localize the layer.

**Negative test:** NTP out of sync silently breaks certificate validation and
database replication across the cluster — a "network" fault that looks like a
security or DB fault until you check the clock.

**Cleanup:** none (read-only).

### Lab 2.6 — Deploy endpoints and soft clients (Objective 2.1)

**Objective:** Add a phone and confirm it registers (on-prem and cloud).

```text
admin:run sql select d.name,d.description,tm.name as model from device d \
  inner join typemodel tm on d.tkmodel=tm.enum where d.name like 'SEP%'
admin:show risdb query phone
```

**Expected result:** the provisioned device and its registration status from the
RIS database — a deployed endpoint appears `Registered` to a specific node;
soft clients (Webex App/Jabber) register the same way through service discovery.

**Negative test:** deploy a phone without associating it to a user/line; it
registers but cannot place calls — provisioning is device **plus** line/user
association.

**Cleanup:** remove the test device if one was added.

### Lab 2.7 — Troubleshoot elements of a SIP conversation (Objective 2.2)

**Objective:** Read a SIP dialog to find where a call fails.

```text
admin:file get activelog /cm/trace/ccm/sdi/  ! or use RTMT SDL/SDI trace
! On CUBE:
debug ccsip messages
show voip rtp connections
```

**Expected result:** the INVITE/100/180/200/ACK exchange — a call failing at a
specific SIP response localizes it: `404` is dial-plan/routing, `403` is
policy/CAC, `488` is codec/SDP mismatch, no `180` is a downstream reachability
problem.

**Negative test:** chase the endpoint for a `488 Not Acceptable Here`; the SDP
offer/answer shows a codec mismatch — the SIP body, not the phone, is the cause.

**Cleanup:** `no debug ccsip messages` on CUBE.

### Lab 2.8 — Troubleshoot endpoint registration on UCM and CUBE (Objective 2.3)

**Objective:** Diagnose an endpoint that will not register.

```text
admin:show risdb query phone | include Unregistered
! On CUBE (SIP SRST / registrar):
show sip-ua status registrar
show voice register statistics
```

**Expected result:** the unregistered endpoint and the registrar's view — UCM
registration failures trace to device pool/TFTP/cert; CUBE/SRST registration
failures trace to `voice register` config or reachability during a WAN outage.

**Negative test:** a phone stuck at "Registering" with a valid config is usually
a TFTP (option 150) or cert-trust problem, not call control — check TFTP reach
before UCM config.

**Cleanup:** none (read-only).

## Lab Verification

Verification means the annotated capture reads like documentation,
and all three induced failures were produced, recognized by
signature, and repaired. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

SIP's grammar, SDP's negotiation, and RTP's delivery are the physics
of this volume: every feature in Chapters 03–09 is these messages
arranged by policy. Read dialogs natively, keep DTMF and codec policy
deliberate, and let every troubleshooting conclusion cite a message.

- [ ] I can annotate a full call capture unaided
- [ ] I recognize 488, one-way-audio, and DTMF signatures on sight
- [ ] My endpoints register by discovery and by Option 150
      respectively
- [ ] My three induced failures matched their predicted signatures
