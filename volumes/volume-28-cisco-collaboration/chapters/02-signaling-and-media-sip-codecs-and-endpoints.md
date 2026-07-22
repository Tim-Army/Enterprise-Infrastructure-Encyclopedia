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
a daily skill CLCOR and CLACCM both assume. The grammar:

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
- CLACCM 300-815 v1.2 domain 1 (Signaling and Media Protocols, 20%)
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

Register two endpoints (one hardware or emulated phone, one Webex
App/Jabber) to the Chapter 01 estate. Capture and fully annotate one
call: every SIP message labeled with its transaction and dialog role,
the SDP offer/answer table (codecs offered/selected, addresses,
DTMF), and the RTP stream statistics. Then break it three ways and
capture each signature: remove the common codec from one endpoint's
region (expect 488), block RTP one direction with an ACL (one-way
audio with perfect signaling), and mismatch DTMF relay on one leg
(call fine, digits dead). Restore all three.

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
