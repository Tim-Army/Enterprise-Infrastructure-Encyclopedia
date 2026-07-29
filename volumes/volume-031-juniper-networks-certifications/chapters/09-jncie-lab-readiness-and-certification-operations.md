# Chapter 09: JNCIE Lab Readiness and Certification Operations

## Learning Objectives

- Understand the four JNCIE practical exams — ENT (JPR-946), SP
  (JPR-962), SEC (JPR-935), DC (JPR-981) — their format, and what
  distinguishes expert-level preparation
- Build a lab regimen that trains speed, verification discipline, and
  recovery rather than configuration recall
- Operate your certification portfolio: scheduling, the three-year
  cycle, and re-certification strategy across tracks
- Assemble the full-track study sequences this volume supports

## Theory and Architecture

### The expert tier in one sentence

Every JNCIE is a **six-hour, hands-on practical** delivered by Juniper
(onsite or remote-proctored) that hands you a broken or half-built
production-scale topology and grades outcomes: services up, policy
correct, failures repaired — not keystrokes. Current exams, verified
against Juniper's pages on 22 July 2026: **JNCIE-ENT JPR-946** (new,
first delivery 13 July 2026, succeeding JPR-944 — confirm which code
your date books), **JNCIE-SP JPR-962**, **JNCIE-SEC JPR-935**, and
**JNCIE-DC JPR-981**. Each requires the corresponding JNCIP.

### What six hours actually tests

Expert candidates fail on clock management, not knowledge: reading
the whole workbook before typing, banking easy points first,
verifying as they go (a broken early task can invalidate an hour of
later work), and knowing the platform's diagnostic order cold. The
JNCIE grading model rewards **working services at time**, which makes
`commit confirmed`, aggressive use of `show | compare`, and scripted
verification (Chapter 06's JSNAPy habit, mentally internalized) the
actual exam skills.

### Certification operations

Juniper certifications live three years; **any same-or-higher-level
exam pass in any track re-certifies everything at or below that
level** — one JNCIP written every three years can sustain an entire
multi-track portfolio, and a JNCIE defense refreshes the estate. Plan
renewals against exam refresh calendars (this year's JN0-352/JN0-650
/JPR-946 wave shows how quickly codes roll) and always re-verify codes
at registration on Juniper's certification pages — the tracker tables
in this volume's README carry the verified snapshot date for exactly
that reason.

## Design Considerations

- **One track to expert beats four to specialist** for depth-signal
  careers; the re-certification rules then make breadth cheap
- Lab topology sizing: JNCIE practice wants 8–15 nodes; vJunos and
  vLabs cover ENT/SP/DC topologies credibly, vSRX covers SEC —
  hardware is optional, discipline is not
- Time-boxed mock labs (full six hours, no notes) are the only honest
  readiness gauge; two clean mocks before booking is the working rule
- Budget: JNCIE exams are premium-priced and reschedule-hostile; the
  mock-lab gate protects real money

## Implementation and Automation

```text
# The candidate's verification battery — muscle memory, not documentation
show system alarms | except "No alarms"
show interfaces terse | match "down|error"
show bgp summary | except Establ
show ospf neighbor | except Full
show route table inet.0 protocol static
show security flow session summary        # SEC
show evpn database | match <critical-mac> # DC/ENT fabrics
show mpls lsp | except "Up"               # SP
commit check
show | compare rollback 1
```

Build these into per-track one-screen batteries and run them after
every task block in practice — the six-hour exam is thirty
five-minute loops of configure→verify, not one long configure.

## Validation and Troubleshooting

- Practice **failure archaeology**: start every mock from a topology a
  script has sabotaged (five seeded faults, unknown to you) — finding
  them is the skill the written exams cannot test
- Keep a personal error journal by category (policy direction misses,
  zone host-inbound, MTU, RT typos); expert readiness is a shrinking
  journal
- Grade mocks by service outcomes against a rubric, never by "felt
  good" — mirror the exam's outcome grading
- Recovery drill: from any broken state, how fast can you reach a
  known-good baseline (`rollback`, archived configs) without erasing
  the evidence of what went wrong?

## Security and Best Practices

- Book exams only through Juniper's certification portal/Pearson VUE;
  the braindump economy around expert exams is an integrity trap that
  voids certifications
- Keep CertMetrics (Juniper's credential record) current; employers
  verify there
- Practice topologies stay off production networks; licensed images
  only (vJunos/vLabs are free and legal — use them)

## References and Knowledge Checks

- JNCIE-ENT (JPR-946), JNCIE-SP (JPR-962), JNCIE-SEC (JPR-935),
  JNCIE-DC (JPR-981) pages on Juniper's certification site — format,
  booking, and current code authority
- Juniper JNCIE self-study bundles and proctored mock offerings;
  vLabs sandbox catalog

Knowledge checks:

1. Why does outcome-based grading make mid-exam verification more
   valuable than configuration speed?
2. Your JNCIP-SEC expires in four months and you hold JNCIS-ENT and
   JNCIA-DevOps. Name every credential one JNCIP-any pass renews and
   why.
3. Design a five-fault seed list for an ENT mock that exercises three
   different diagnostic layers.

## Hands-On Lab

This chapter carries **integrative, timed-build walkthrough labs** that rehearse
the four JNCIE practical tracks — the expert-level application of the specialist
skills from Chapters 02–05 — plus the certification-operations knowledge that
frames exam day. The JNCIE **written qualifier is the track's JNCIP**; these labs
are for the six-hour hands-on lab. Each ends **`**Lab verified by:** *pending*`**
until a human runs it.

**Shared prerequisites for Labs 9.1–9.5** — a multi-device Junos topology (vMX/
vSRX/vQFX or hardware) sufficient to build each track's scenario, a stopwatch, and
the discipline to build against the clock and then verify. **Cost:** none beyond
lab resources.

### Lab 9.1 — JNCIE-ENT integrative build (Enterprise expert readiness)

**Objective:** Build and verify a full enterprise topology against the clock.

```text
show ospf neighbor
show isis adjacency
show bgp summary
show spanning-tree bridge
show vrrp
```

**Expected result:** OSPF/IS-IS/BGP all converged, a loop-free switched core, and
VRRP redundancy — the JNCIE-ENT lab tests building multi-protocol routing (OSPF +
IS-IS + BGP with redistribution and policy), switching (VLANs, RSTP/MSTP, LAG), and
HA (Virtual Chassis, VRRP, GRES/NSR) **quickly and correctly**, then fixing broken
scenarios.

**Negative test:** a redistribution between IGPs without tag-based loop prevention
introduces a routing loop under the time pressure — the policy discipline from
Chapter 02 is what prevents the classic JNCIE mistake.

**Cleanup:** roll back to the pre-lab configuration group/snapshot.

### Lab 9.2 — JNCIE-SP integrative build (Service Provider expert readiness)

**Objective:** Build and verify an MPLS core with L3VPN/L2VPN services.

```text
show mpls lsp
show ldp session
show route table bgp.l3vpn.0
show l2vpn connections 2>/dev/null
show route table inet6.0
```

**Expected result:** RSVP/LDP LSPs up, VPNv4 (bgp.l3vpn.0) routes, an L2VPN
connection, and IPv6 — the JNCIE-SP lab tests a full provider build: IS-IS/OSPF
core, MPLS (RSVP-TE, LDP, segment routing), **L3VPN** and **L2VPN/EVPN** services,
CoS, and multicast, at expert speed.

**Negative test:** a VPN with correct RTs but a broken core LSP has no PE-PE
transport; the service fails despite correct VRF config — verify the underlay LSP
first, the SP troubleshooting discipline.

**Cleanup:** roll back to the pre-lab snapshot.

### Lab 9.3 — JNCIE-SEC integrative build (Security expert readiness)

**Objective:** Build a chassis cluster with policy, NAT, and IPsec.

```text
show chassis cluster status
show security policies hit-count
show security nat source rule all
show security ike security-associations
show security ipsec security-associations
```

**Expected result:** a healthy cluster, hit-counted policies, working NAT, and IPsec
SAs — the JNCIE-SEC lab tests building an SRX estate: **chassis cluster** HA, zone-
based **security policies**, **NAT** (source/destination/static), **IPsec VPNs**,
IDP/UTM/ATP, and identity-aware policy, then troubleshooting under time.

**Negative test:** a security policy that permits traffic but a source-NAT rule that
does not match leaves return traffic unroutable — policy and NAT must both be
correct for the flow to complete.

**Cleanup:** roll back to the pre-lab snapshot.

### Lab 9.4 — JNCIE-DC integrative build (Data Center expert readiness)

**Objective:** Build an EVPN-VXLAN fabric and verify overlay reachability.

```text
show bgp summary
show evpn database
show ethernet-switching vxlan-tunnel-end-point remote
show route table bgp.evpn.0
ping <remote-host-in-tenant>
```

**Expected result:** the underlay converged, EVPN Type-2/5 routes present, remote
VTEPs discovered, and end-to-end tenant reachability — the JNCIE-DC lab tests
building a spine-leaf **IP fabric** with **EVPN-VXLAN** (ERB), multitenancy (VRFs/
virtual networks), DCI, and (increasingly) **Apstra** intent-based operation.

**Negative test:** inconsistent VNI-to-VLAN mapping on one leaf silently drops
that segment's traffic — the fabric-wide consistency check is the JNCIE-DC
discipline.

**Cleanup:** roll back to the pre-lab snapshot.

### Lab 9.5 — Cross-track troubleshooting and certification operations

**Objective:** Diagnose a mixed fault fast, and confirm exam-operations readiness.

```text
show system commit
show configuration | compare rollback 1
show log messages | last 40
request system snapshot 2>/dev/null
```

**Expected result:** the commit history, a rollback diff, recent logs, and a saved
snapshot — expert readiness is as much **operations** as configuration: use
`rollback`/`compare`, commit confirmed, `traceoptions`, and snapshots to work
safely and fast; and know the certification operations (JNCIP written qualifier,
six-hour lab format, delivery, recertification every three years, JPR code changes)
that frame exam day.

**Negative test:** make a risky change without `commit confirmed`; a mistake that
cuts your management session is unrecoverable without console — `commit confirmed`
auto-rolls-back and is the expert's safety net under time.

**Cleanup:** `rollback 0` and restore the baseline snapshot.

## Lab Verification

Verification means the mock ran the full six hours under exam
conditions, all seeded faults were found or accounted for, the
outcome rubric was scored honestly, and the error journal gained its
entries — the readiness verdict follows the evidence, not the mood.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] All four JNCIE codes and formats recorded from primary source
- [ ] Verification-battery habit built into practice loops
- [ ] One honest six-hour mock completed and graded
- [ ] Re-certification strategy mapped for the personal portfolio
- [ ] Booking gate defined (two clean mocks) and respected
