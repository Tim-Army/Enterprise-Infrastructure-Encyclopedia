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

This chapter carries a topic-level walkthrough lab for **Domain 4 (Voice
Gateways and Session Border Controllers) of CLCOR 350-801 v2.0 and Domains 1
(Signaling and Media Protocols) and 2 (SBC and Voice Gateway Technologies) of
CLACC 300-815 v2.0** — mapped in the volume README's coverage tables. Labs use
the IOS XE voice CLI on a CUBE / voice gateway. Each ends
**`**Lab verified by:** *pending*`** until a human runs it.

**Shared prerequisites for Labs 5.1–5.10** — an IOS XE CUBE with SIP trunks to
UCM and an ITSP, a voice gateway with PSTN connectivity, SRST/UCME configured
for a branch, and console/SSH access. **Cost:** none beyond lab resources.

### Lab 5.1 — Configure voice gateway and SBC elements (CLCOR Objective 4.1)

**Objective:** Bring up a CUBE SIP trunk and confirm dial-peer routing.

```text
show dial-peer voice summary
show sip-ua status
show voip rtp connections
```

**Expected result:** inbound/outbound VoIP dial peers in `up` with matching
codecs and a live RTP session on a test call — CUBE is a back-to-back user agent
terminating and re-originating SIP between UCM and the ITSP.

**Negative test:** an outbound dial peer whose `session target` is unreachable
leaves the call at no-answer; `show dial-peer voice <tag>` shows it selected but
the target down — reachability, not matching, is the fault.

**Cleanup:** none (read-only).

### Lab 5.2 — Troubleshoot IOS XE dial plans (CLCOR Objective 4.2)

**Objective:** Diagnose dial-peer matching, translation rules, and SIP profiles.

```text
show dialplan number 14085550123          ! which outbound dial peer matches
test voice translation-rule 10 +14085550123
show voice class sip-profiles 100
```

**Expected result:** the matched dial peer, the translation-rule result, and the
SIP profile — IOS XE selects the longest/highest-preference matching dial peer;
translation rules rewrite digits; SIP profiles rewrite headers/SDP. The three
tools expose exactly what each did.

**Negative test:** a translation rule that rewrites the called number *after*
dial-peer matching surprises you; order matters — `test voice translation-rule`
proves the rewrite independent of matching.

**Cleanup:** none (read-only test commands).

### Lab 5.3 — Describe IOS XE media resources (CLCOR Objective 4.3)

**Objective:** Read the gateway's DSP/media resources (transcoding, conferencing).

```text
show voice dsp group all
show sccp connections
show dspfarm profile 1
```

**Expected result:** DSP farm profiles and active sessions — an IOS XE gateway
provides transcoding, MTP, and conference bridges via DSP resources registered to
UCM over SCCP; the DSP group shows capacity and use.

**Negative test:** a transcoding call with no free DSP credits fails with no
common codec; `show voice dsp group all` shows the farm exhausted — capacity, not
config, is the limit.

**Cleanup:** none (read-only).

### Lab 5.4 — Troubleshoot advanced elements of a SIP conversation (CLACC Objective 1.1)

**Objective:** Read an advanced SIP exchange (REFER, UPDATE, re-INVITE).

```text
debug ccsip messages
show voip trace all      ! IOS XE VoIP Trace (structured per-call)
```

**Expected result:** the REFER (transfer), UPDATE/re-INVITE (media change), and
their responses — advanced call flows use these methods; a failed transfer or
hold traces to a rejected REFER/re-INVITE, visible in VoIP Trace without raw
debugs.

**Negative test:** a transfer failing because the far end rejects REFER (no
`202`) needs SIP-REFER-to-reINVITE consumption on CUBE — the method-level reject
is the clue.

**Cleanup:** `no debug ccsip messages`.

### Lab 5.5 — Describe media optimization and NAT traversal (CLACC Objective 1.2)

**Objective:** Read media-flow-around/through and ICE/STUN/TURN behavior.

```text
show voip rtp connections            ! flow-around vs flow-through
show run | section media
show ip nat translations | include 3478|udp   ! STUN/TURN 3478
```

**Expected result:** whether media flows through CUBE (anchored) or around it,
and any STUN/TURN (port 3478) for ICE — media optimization keeps RTP off the SBC
when possible; ICE with STUN/TURN traverses NAT for endpoints behind firewalls.

**Negative test:** force media flow-around across a NAT boundary with no ICE;
one-way or no audio results — NAT traversal (ICE/TURN) is required when
endpoints are not directly routable.

**Cleanup:** none (read-only).

### Lab 5.6 — Troubleshoot mid-call signaling (CLACC Objective 1.3)

**Objective:** Diagnose a mid-call failure (hold/resume/transfer/codec change).

```text
show voip trace all | include REINVITE|UPDATE|BYE
debug voip ccapi inout
```

**Expected result:** the mid-call re-INVITE/UPDATE and any error — mid-call
signaling problems (hold music absent, transfer dropped, codec renegotiation
failing) trace to a rejected re-INVITE or a delayed-offer/early-offer mismatch.

**Negative test:** a delayed-offer trunk to an early-offer-only peer fails media
renegotiation on hold/resume — the offer model mismatch is the mid-call cause.

**Cleanup:** `no debug voip ccapi inout`.

### Lab 5.7 — Configure Cisco UCME and SIP SRST (CLACC Objective 2.1)

**Objective:** Configure branch survivability and confirm phone fallback.

```text
show voice register global
show voice register pool all
show call-manager-fallback     ! or 'show voice register' for SIP SRST
```

**Expected result:** the SRST/UCME registrar with registered branch phones —
during a WAN outage, phones re-register to the local gateway (SIP SRST) or run
standalone UCME, preserving local and PSTN calling.

**Negative test:** an SRST config with a `max-dn`/`max-pool` lower than the phone
count leaves some phones unregistered in fallback — size SRST to the branch.

**Cleanup:** none (read-only).

### Lab 5.8 — Troubleshoot CUBE dial plan with VoIP Trace (CLACC Objective 2.2)

**Objective:** Use VoIP Trace and `show call active` to find a CUBE dial-plan
fault.

```text
show voip trace cover-buffers
show call active voice compact
show dial-peer voice summary | include DOWN
```

**Expected result:** the per-call VoIP Trace record and the dial peers involved
— a call failing on CUBE traces to no matching outbound dial peer, a codec/DTMF
mismatch, or a down `session target`; VoIP Trace ties the SIP legs together.

**Negative test:** a call matching a catch-all outbound dial peer instead of the
intended one shows the wrong `session target` in the trace — dial-peer
preference/specificity is the cause.

**Cleanup:** none (read-only).

### Lab 5.9 — Troubleshoot CUBE advanced dial-peer features (CLACC Objective 2.3)

**Objective:** Diagnose dial-peer groups, DPG, and server groups.

```text
show voice class dpg 1
show voice class server-group 1
show dial-peer voice <tag> | include huntstop|preference|dpg
```

**Expected result:** the dial-peer group / server group and hunting behavior —
advanced routing uses DPGs (route an inbound peer to a group of outbound peers)
and server groups (multiple targets with failover); huntstop/preference control
the order.

**Negative test:** a DPG whose members all point to a down server group drops
the call despite matching — failover needs at least one reachable target in the
group.

**Cleanup:** none (read-only).

### Lab 5.10 — Configure advanced SIP interoperability with CUBE (CLACC Objective 2.4)

**Objective:** Apply SIP profiles/normalization on CUBE for a third-party trunk.

```text
show voice class sip-profiles 200
show run | section voice class sip-copylist
show sip-ua calls    ! confirm calls traverse after normalization
```

**Expected result:** the SIP profile rewriting requests/responses and any
header copy-list — advanced interoperability on CUBE adapts headers (PAI,
Diversion, unsupported params) and SDP to a provider's dialect so calls
complete.

**Negative test:** an ITSP requiring a specific `From`/PAI format that CUBE does
not send returns `403`/`4xx`; the SIP profile that rewrites it is the fix — the
raw trunk without it fails.

**Cleanup:** unbind the test SIP profile.

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
