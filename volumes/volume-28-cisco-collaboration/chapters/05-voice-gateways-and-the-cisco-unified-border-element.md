# Chapter 05: Voice Gateways and the Cisco Unified Border Element

## Learning Objectives

- Position gateway roles: TDM/analog interconnect, SIP trunking, and
  the session border function CUBE provides
- Configure dial peers — inbound and outbound matching, digit
  manipulation, and codec negotiation — with confidence in the
  matching order
- Deploy CUBE between CUCM and an ITSP: normalization, security,
  media handling, and high availability
- Retain working literacy in TDM and analog: ISDN PRI debugging and
  FXS/FXO ports where they persist
- Validate and troubleshoot the gateway layer with dial-peer
  evidence and protocol debugs

## Theory and Architecture

### Why a border element exists

Connecting CUCM directly to an ITSP would expose call control to the
internet, weld the estate to one provider's SIP dialect, and leave
media paths unmanaged. **CUBE** is IOS XE's back-to-back user agent
(B2BUA): every call becomes two legs — provider-side and CUCM-side —
so the border can normalize headers, police what enters, anchor or
release media, interwork DTMF (Chapter 02's mismatches, fixed here),
and hide topology. The same router often carries the site's SRST
(Chapter 04) and any remaining TDM — one platform, several duties.

### Dial peers: the gateway's routing table

IOS XE voice routing is **dial peers**. The matching rules are the
exam's and the field's core discipline:

- **Inbound leg**: best match wins in order — incoming called-number
  → answer-address (calling) → destination-pattern against calling
  → port. An unmatched inbound leg lands on default peer 0 with
  default (often wrong) behavior — always configure explicit inbound
  peers.
- **Outbound leg**: longest destination-pattern match, then explicit
  preference; equal candidates hunt.
- Each peer sets its leg's personality: codec (or voice-class codec
  list), DTMF relay, VAD, session target/protocol.

**Digit manipulation** on IOS XE — voice translation rules (regex
profiles applied to called/calling per peer or port) — implements
Chapter 04's "localize at egress" at the boundary the ITSP sees.

### CUBE specifics

- `mode border-element` and address hiding; **media flow-through**
  (anchor, the default border posture) versus **flow-around**
  (release, when both legs are trusted and hairpins waste WAN).
- **Normalization**: SIP profiles rewriting headers per provider
  quirk (From-domain requirements, Diversion handling, history-info)
  — the contained dialect adapter.
- **High availability**: box-to-box redundancy with media
  preservation, or route-list distribution from CUCM across CUBE
  pairs; either way, OPTIONS ping from Chapter 03 keeps truth.
- **TLS/SRTP on the provider leg** where the ITSP supports it; the
  border terminates and re-originates security domains cleanly.

### The TDM remainder

PRI (`isdn switch-type`, `pri-group`, Q.931 debugging) and analog
(FXS for faxes/elevators/paging, FXO for POTS failover) persist at
the edges of modern estates, and DCIT-style troubleshooting still
reaches for `debug isdn q931` when the carrier and the gateway
disagree about a disconnect cause. Literacy, not mastery, is the
target: read a Q.931 cause code, wire an FXS port, and know fax
needs T.38 or G.711 pass-through decided deliberately.

## Design Considerations

- **Explicit inbound peers always** — the "default peer 0 took the
  call" class of mystery is designed out, not debugged out.
- **Voice-class everything** (codec lists, SIP profiles, E.164
  pattern maps): named, reusable policy beats per-peer copies.
- **Redundancy matched to the failure**: provider failure → second
  ITSP/route group; CUBE failure → HA pair or CUCM route-list
  hunting; WAN failure → SRST plus FXO/local trunking where the
  branch justifies it.
- **Capacity honestly**: sessions-per-CUBE from platform datasheets
  with headroom, licensed accordingly, monitored via the same
  perfmon Chapter 09 automates.

## Implementation and Automation

CUBE between CUCM and a (lab-simulated) ITSP:

```text
voice service voip
 mode border-element
 allow-connections sip to sip
 sip
  early-offer forced
  midcall-signaling passthru

voice class codec 10
 codec preference 1 opus
 codec preference 2 g711ulaw

voice class sip-profiles 100
 request INVITE sip-header From modify "@.*>" "@sip.lab-itsp.example>"

! Inbound from ITSP (explicit)
dial-peer voice 100 voip
 description INBOUND-FROM-ITSP
 incoming called-number +1555100....
 voice-class codec 10
 dtmf-relay rtp-nte
 session protocol sipv2

! Outbound to CUCM
dial-peer voice 110 voip
 description TO-CUCM
 destination-pattern +1555100....
 session protocol sipv2
 session target ipv4:10.50.10.20
 voice-class codec 10
 dtmf-relay rtp-nte

! Outbound to ITSP with egress localization
voice translation-rule 20
 rule 1 /^\+1\(.*\)/ /9-1-\1/     ! the lab ITSP's required format
voice translation-profile EGRESS-ITSP
 translate called 20
dial-peer voice 200 voip
 description TO-ITSP
 destination-pattern \+1[2-9]..[2-9]......$
 translation-profile outgoing EGRESS-ITSP
 voice-class sip-profiles 100
 session protocol sipv2
 session target ipv4:203.0.113.10
```

## Validation and Troubleshooting

The gateway's evidence commands, in the order you reach for them:

```text
show dial-peer voice summary          ! what exists, hunt order
csim start +15551002001               ! simulate a call leg (lab)
debug ccsip messages                  ! the two legs, raw
show call active voice brief          ! live legs, codecs, peers
show voip rtp connections             ! media addresses both legs
debug isdn q931                       ! when TDM is in play
```

Method: identify **which leg** misbehaves first — the B2BUA split
means every fault is leg-specific. Wrong inbound peer (personality
defaults applied) shows in `show call active` peer IDs; codec
failures on one leg read as 488 there and normal SDP on the other;
DTMF interworking is proven by watching rtp-nte events arrive on one
leg and the chosen relay leave the other; provider rejections
(403/404 with correct digits) are dialect — compare the INVITE
against the provider spec and fix with a SIP profile, in the profile,
so the fix is named and reviewable.

## Security and Best Practices

- The border is a security boundary: IP trust lists
  (`ip address trusted list`), call thresholds, and toll-fraud
  protections are on before the first provider packet.
- TLS to the ITSP where offered; always between CUBE and CUCM in
  secure estates; SRTP pass-through or interworking configured
  deliberately.
- No SIP ALG anywhere in the path — the fixups fight the B2BUA;
  disable it on intervening firewalls and document that as design.

## References and Knowledge Checks

- CLACC 300-815 v2.0 domain 2 (Session Border Controller and Voice
  Gateway Technologies, 30%); CLCOR domain 4 (10%)
- Cisco CUBE configuration guide; IOS XE voice translation
  documentation

Knowledge checks:

1. Order the inbound dial-peer matching criteria, and explain why
   relying on peer 0 is a design defect.
2. A call completes but the caller ID shown to the ITSP is wrong.
   Which two mechanisms could fix it, and which is preferred, where?
3. When is media flow-around correct, and what do you lose at the
   border by releasing media?
4. The provider rejects INVITEs with 403 despite correct numbers.
   What class of problem is this, and where does the fix live?

## Hands-On Lab

Insert CUBE between the Chapter 03 estate and a simulated ITSP (a
second CML router running as a SIP peer): build the configuration
above — explicit inbound peers, voice-class codec and SIP profiles,
egress translation. Prove end-to-end PSTN-style calls both
directions with `show call active` evidence naming the matched peers
per leg. Break and evidence three faults: remove the inbound peer
(observe peer-0 behavior and its personality defaults), induce a
codec mismatch on the provider leg only, and change the ITSP's
expected From-domain (fix with a SIP profile edit, not a CUCM
change). If TDM hardware or emulation exists, bring up one FXS port
and read one `debug isdn q931` disconnect cause from a reference
capture.

## Lab Verification

Verification means both directions completed with per-leg peer
evidence, all three induced faults were diagnosed to the correct
leg and repaired at the border, and the SIP-profile fix is named in
configuration. Until then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

The border element turns every call into two governable legs: dial
peers route them, translation rules localize them, SIP profiles
speak each provider's dialect, and security thresholds keep the
internet's dial tone out. TDM literacy persists at the edges. This
is CLACC's SBC-and-gateway 30% and CLCOR's border domain, and it
completes the on-premises calling path Chapters 03–04 built.

- [ ] My inbound legs never land on peer 0
- [ ] I can name which leg any fault lives on from the evidence
- [ ] My provider dialect fixes live in named SIP profiles
- [ ] Toll-fraud protections predate my first provider call
