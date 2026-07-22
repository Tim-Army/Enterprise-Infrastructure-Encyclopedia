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

Run one full six-hour mock on your strongest track's topology (ENT or
DC from this volume's labs, SEC on vSRX, SP on the Chapter 03 core):
a partner or script seeds five faults and adds three build tasks; you
work the clock with the verification battery, journal every miss, and
grade by service outcomes. Produce the readiness verdict: book, or
schedule the next mock.

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
