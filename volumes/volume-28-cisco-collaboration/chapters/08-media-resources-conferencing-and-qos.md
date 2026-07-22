# Chapter 08: Media Resources, Conferencing, and QoS

## Learning Objectives

- Provision media resources — conference bridges, transcoders, MTPs,
  music on hold, annunciator — and control their selection with
  media resource groups
- Deploy conferencing: ad hoc and meet-me on-premises, Cisco Meeting
  Server, and Webex meeting integration points
- Engineer QoS for collaboration end to end: classification,
  marking, queuing, and the WAN policies voice and video require
- Measure quality: the metrics, the reports (CMRs), and the
  monitoring that catches degradation before users report it
- Troubleshoot media-quality problems with counters and captures

## Theory and Architecture

### Media resources: the estate's signal-processing pool

Some call features need media manipulation beyond two endpoints
exchanging RTP: **conference bridges** mix audio (hardware DSP on
gateways, software on CUCM, scaled on CMS), **transcoders** convert
codecs (the G.729-leg-meets-G.711-only-resource case),
**MTPs** (media termination points) bridge RTP variants and satisfy
protocol requirements, **music on hold** streams sources (unicast
or multicast), and the **annunciator** speaks tones and
announcements. Selection is governed: resources register to CUCM,
join **media resource groups (MRGs)**, and **media resource group
lists (MRGLs)** assigned to devices/pools order which pool a device
draws from — locality and capacity policy, Chapter 03's cascade
applied to DSPs.

### Conferencing tiers

**Ad hoc** (button-press escalation) and **meet-me** conferences
draw bridges from the MRGL. **Cisco Meeting Server (CMS)** scales
audio/video conferencing on-premises — spaces, call bridge groups,
and CUCM trunk integration — where data sovereignty or scale argues
for it. **Webex Meetings** carries the cloud tier, with Chapter 07's
hybrid calendar providing one-button join across both. Positioning
is the design skill; the packet-level skills stay identical.

### QoS: the network keeping collaboration's promises

Chapter 02 stated the budgets (≤150 ms one-way, jitter buffered,
loss <1%); QoS is how the network meets them. The collaboration
defaults, aligned with Volume III's QoS architecture:

- **Classification/marking at the edge**: voice RTP **EF (DSCP 46)**,
  interactive video **AF41**, signaling **CS3** — marked by
  endpoints (CUCM device settings), trusted or re-marked at the
  access switch, preserved across the WAN.
- **Queuing**: strict-priority (LLQ) for EF sized to the CAC number
  from Chapter 03 (the honesty loop: locations bandwidth = the
  priority queue), bandwidth-guaranteed queues for video and
  signaling.
- **The WAN edge policy** is where theory meets contention;
  sub-interfaces, shapers, and per-class policies live there.
- **Wireless collaboration** inherits Volume III's wireless QoS
  (WMM/UP marking) — voice over Wi-Fi is a design, not an accident.

### Measuring quality

RTCP feeds live stats; CUCM's **Call Management Records (CMRs)**
persist per-call quality (loss, jitter, concealment); RTMT and
serviceability counters expose live streams; and endpoints
themselves report (phone webpages' streaming statistics are the
fastest scene-of-crime evidence). MOS-style scoring aggregates it
for trending — Chapter 09 wires these into the monitoring stack.

## Design Considerations

- **Resource locality**: branches draw conference/MTP resources
  locally where DSPs exist — WAN-hairpinned conferences double the
  Chapter 03 bandwidth math.
- **Transcoding is a smell**: every transcoder session spends DSPs
  to fix a codec-policy inconsistency; design regions so
  transcoding is exceptional.
- **Priority queue sized to CAC, exactly**: bigger wastes WAN;
  smaller makes CAC a liar. Change them together or not at all.
- **Multicast MOH** where branch counts argue for it — one stream
  per source beats per-call unicast across the WAN, and its failure
  mode (silence on hold) is worth the multicast plumbing.

## Implementation and Automation

Media resource governance (CUCM):

```text
Media Resources: register/verify CFB, XCODE (IOS DSP), MTP, MOH, ANN
MRG-HQ:  CFB-HQ, XCODE-HQ, MTP-HQ, MOH-HQ
MRG-BR1: CFB-BR1 (router DSPs), MOH-MCAST
MRGL-HQ:  [MRG-HQ]           -> assigned to DP-HQ
MRGL-BR1: [MRG-BR1, MRG-HQ]  -> branch prefers local, falls back
```

IOS XE DSP resources at the branch:

```text
voice-card 0/1
 dsp services dspfarm
sccp local GigabitEthernet0/0/0
sccp ccm 10.50.10.20 identifier 1 version 7.0
sccp
dspfarm profile 1 conference
 codec g711ulaw
 maximum sessions 4
 associate application SCCP
```

WAN edge QoS (the collaboration classes of Volume III's policy):

```text
class-map match-any VOICE
 match dscp ef
class-map match-any VIDEO
 match dscp af41
class-map match-any CALL-SIG
 match dscp cs3
policy-map WAN-EDGE
 class VOICE
  priority percent 18          ! = locations CAC for this site
 class VIDEO
  bandwidth remaining percent 25
 class CALL-SIG
  bandwidth remaining percent 5
 class class-default
  fair-queue
  random-detect dscp-based
```

Quality evidence, quickly:

```text
# Endpoint truth: phone web page > Streaming Statistics
# Cluster truth: RTMT > Session Trace / CMR export
# Network truth: per-class counters at the WAN edge
show policy-map interface GigabitEthernet0/0/1 output
```

## Validation and Troubleshooting

Validate the loop end to end once, deliberately: place a marked
call, confirm EF survives to the far edge (captures at both WAN
edges), confirm the priority queue increments its counters and not
its drops, and confirm CMRs record the call clean. Then the failure
craft: **choppy audio on WAN calls** — read the priority queue
first (drops there mean the queue is undersized or CAC overshot;
Chapter 03 and this chapter's numbers must move together);
**one-site conference failures** — MRGL selection (is the branch
drawing a dead local bridge instead of falling back?
`show dspfarm profile` and CUCM's media resource status answer);
**hold silence at branches** — multicast MOH reachability (IGMP/PIM
on the path, or the fallback-to-unicast setting); **video sharp,
audio poor** — classification leak (video class stealing EF, or
remarking mid-path — walk the DSCP across hops); **quality fine,
users complain anyway** — pull CMRs before believing anecdotes;
concealment seconds quantify what "sounded bad" means.

## Security and Best Practices

- QoS trust boundaries are security posture too: untrusted access
  re-marks, so a compromised host cannot EF-flood the priority
  queue.
- SRTP through media resources deliberately: secure conferences
  need secure-capable bridges (CMS or secure DSP profiles) — an
  estate-wide SRTP posture includes its media resources.
- MOH sources licensed and controlled — the copyright dimension of
  hold music is a real compliance item this encyclopedia's scope
  rules would remind you to respect.

## References and Knowledge Checks

- CLCOR 350-801 v2.0 domain 6 (Media and QoS, 10%)
- Cisco SRND media resources and QoS chapters; CMS deployment
  guides
- Volume III, Chapter 06 (QoS architecture this chapter applies)

Knowledge checks:

1. A branch device's MRGL lists local then HQ resources. Narrate
   conference setup when the local DSP profile is down, and the
   evidence trail that shows it.
2. Why must the LLQ percentage and locations CAC move together, and
   what symptom appears when only one is changed?
3. Which artifact answers "was that call actually bad," and what
   two counters in it matter most?
4. When does multicast MOH justify its plumbing, and what breaks
   silently when PIM does not span the path?

## Hands-On Lab

Provision the media pool: software CFB/MTP at HQ, IOS DSP
conference profile at the branch, MOH sources (unicast HQ,
multicast to the branch), MRG/MRGL assignments per the design
above. Prove locality: a branch ad hoc conference draws the branch
DSP (dspfarm evidence), then kill the profile and show fallback to
HQ with the WAN cost visible in counters. Build the WAN-EDGE policy
on the lab WAN link sized to the Chapter 03 locations number; place
marked calls and capture DSCP at both edges; then overdrive the
link with iperf and show the priority queue protecting EF while
default weeps. Export CMRs for the test calls and annotate loss/
jitter/concealment. Break one thing subtly — re-mark EF to CS0 at
the access switch — and find it by walking DSCP hop by hop.

## Lab Verification

Verification means locality and fallback were evidenced, EF
survived congestion measurably, CMRs quantified the calls, and the
induced re-marking was found by methodical DSCP walking. Until
then, the lab is unverified.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

Media resources are governed pools (MRG/MRGL policy), conferencing
tiers from DSPs through CMS to Webex, and QoS is the network's
kept promise — classification, LLQ sized to CAC, and measurement
through CMRs that turns "it sounded bad" into numbers. The
smallest CLCOR domain by weight; the largest share of user-felt
quality.

- [ ] My MRGLs draw local first and fall back provably
- [ ] My priority queue and CAC agree to the kilobit
- [ ] EF survived congestion in my capture evidence
- [ ] I can quantify any complaint from CMRs
