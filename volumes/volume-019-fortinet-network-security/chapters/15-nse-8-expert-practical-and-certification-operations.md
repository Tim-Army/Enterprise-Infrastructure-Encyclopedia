# Chapter 15: NSE 8 Expert Practical and Certification Operations

## Learning Objectives

- Understand the NSE 8 expert tier as restructured on 15 July 2026: an
  NSE 8 Core practical plus one NSE 8 Specialization practical, with
  the two-year validity and new recertification points
- Build an NSE 8 lab regimen that trains speed, verification, and
  recovery across the Security Fabric
- Operate a Fortinet certification portfolio: the four tracks, the
  transition mapping, recertification, and the currency discipline a
  twice-renamed program demands
- Sequence full-track study across all four tracks of this volume

## Theory and Architecture

### The expert tier in one sentence

NSE 8 is Fortinet's hands-on expert credential, rebuilt in the 2026
change: candidates pass an **NSE 8 Core practical exam module** and one
**NSE 8 Specialization practical exam module**, with the specialization
completed **within one year** of the core; the credential is valid
**two years** and now earns recertification points (verified against
Fortinet Training Institute on 22 July 2026). The legacy FCX practical
(NSE8_870) delivered its final sitting on 15 March 2026; new candidates
take the restructured two-module path. Each track's NSE 7 chain is the
on-ramp.

### What the practical tests

Like every expert lab in this encyclopedia's certification volumes, NSE
8 grades **outcomes across an integrated topology** — a Security Fabric
of FortiGate, FortiManager, FortiAnalyzer, and track-specific products
that must be built, secured, and repaired under time. The skills that
pass are clock management, verification-as-you-go, and knowing the
fabric's diagnostic order cold — configuration recall is table stakes.

### Certification operations, Fortinet edition

This program changed names twice in three years (NSE → FCP/FCSS/FCX →
NSE), so operating a portfolio means verifying the live exam the week
you book, watching Fortinet Training Institute's news, keeping the
Fortinet credential record current, and re-running this volume's
verification pass on the standing currency cadence. The transition
mapping table (legacy FCP/FCSS → NSE level) is the authority on how a
held credential converted — read it rather than assuming.

## Design Considerations

- One track to NSE 8 signals depth; the four tracks share NSE 4, so
  breadth is cheap once the foundation is set
- NSE 8 lab topologies want the Security Fabric wired end to end —
  FortiGate VMs plus the track's products; FortiGate/FortiManager/
  FortiAnalyzer VMs cover most of it on the Chapters 03–09 / Volume XXVI lab host
- Time-boxed full mocks are the only honest readiness gauge; two clean
  mocks before booking the core, and plan the specialization within the
  one-year window
- Budget: NSE 8 is premium and reschedule-hostile; the mock gate
  protects real money

## Implementation and Automation

```text
# The candidate's fabric verification battery (muscle memory for NSE 8)
get system status ; get system ha status          # FortiGate + HA
diagnose sys sdwan health-check                    # SASE/SD-WAN
diagnose test application fortilogd 1              # FortiAnalyzer ingest
execute fmgr install-config ... ; diagnose dvm device list  # FortiManager
diagnose vpn tunnel list | grep -i down            # IPsec
# Run the track-appropriate battery after every task block; the exam is
# many short configure->verify loops, not one long build.
```

## Validation and Troubleshooting

- Practice failure archaeology: start mocks from a fabric a partner or
  script has sabotaged (five seeded faults) — finding them is the skill
  written exams cannot test
- Keep an error journal by category (policy direction, routing
  asymmetry, fabric-connector auth, HA sync); readiness is a shrinking
  journal
- Grade mocks by service outcomes against a rubric, mirroring NSE 8's
  outcome grading
- Recovery drill: from any broken state, reach a known-good baseline
  (FortiManager revision, config backup) without erasing the evidence

## Security and Best Practices

- Book only through Fortinet Training Institute / Pearson VUE; expert
  braindumps are an integrity trap that voids credentials
- Keep the Fortinet credential record and badge wallet current
- Practice on licensed FortiGate VMs and the free Fortinet labs; never
  on production

## References and Knowledge Checks

- Fortinet Training Institute: NSE 8 requirements and prerequisites,
  the 2026 program-change FAQ, and the transition-mapping table (the
  authority on format, booking, and current structure)
- this volume's foundation (Chapters 01–09) and track chapters (10–15)

Knowledge checks:

1. Describe the two-module NSE 8 structure and the one-year rule.
2. Why does outcome-based grading make mid-exam verification more
   valuable than raw speed?
3. A colleague held FCSS in Security Operations on 14 July 2026 and
   asks what NSE level they now hold. What determines the answer?

## Hands-On Lab

This chapter is the **NSE 8 expert practical** — the top of the program, a two-module
hands-on exam (a **Core** module plus a **Specialization**) that has candidates design,
build, and troubleshoot an integrated Fortinet solution under time pressure. The labs are
integrative (they assume fluency with every prior chapter) and close with a **Design
Exercise** in place of a single command sequence. Each ends **`**Lab verified by:**
*pending*`** until a human runs it.

**Shared prerequisites for Labs 15.1–15.2** — a multi-product lab: at least two FortiGates
(HA + tunnel), FortiManager, FortiAnalyzer, and one track product (FortiWeb, FortiAP, or
FortiSASE), all on current firmware. **Cost:** none beyond lab resources.

### Lab 15.1 — Integrated build-and-break (Topic: NSE 8 Core practical)

**Objective:** Build a Fabric-wide secured service, then diagnose an injected fault
end-to-end.

```text
# Build: HA pair -> ADVPN hub-and-spoke -> UTM inspection -> FortiManager-managed policy
#        -> FortiAnalyzer logging -> a published app behind ZTNA.
# Then inject one fault (e.g. a phase-2 selector mismatch on a spoke) and diagnose:
diagnose vpn tunnel list name <spoke>
diagnose debug flow filter addr <app-ip>
diagnose debug flow trace start 20
diagnose debug enable
get router info routing-table all
diagnose sys ha status
```

**Expected result:** you locate the fault by following the packet — tunnel state → route
→ policy match → NAT → inspection — and correct it so the service recovers, with
FortiAnalyzer showing the restored flow. NSE 8 tests exactly this: integrate many products
and troubleshoot the whole path under time pressure.

**Negative test:** troubleshoot by changing several things at once; you lose track of which
change fixed (or broke) what — expert practice is one hypothesis, one change, re-test, as
`diagnose debug flow` guides you.

**Rollback:** revert the injected fault and tear down lab-only tunnels/policies.

### Lab 15.2 — Design Exercise: multi-site secure architecture (Topic: NSE 8 design)

**Objective:** Produce a defensible design, not a config dump — the NSE 8 design mindset.

> **Scenario.** A retailer has 1 data center, 3 regional hubs, and 200 stores. Stores need
> resilient internet + secure access to data-center apps; PCI traffic must be segmented and
> inspected; the SOC needs unified visibility; remote admins need Zero-Trust access.

Work through the design and **write down**:

1. **Topology** — ADVPN hub-and-spoke over dual-underlay SD-WAN; where HA pairs sit
   (data center, hubs) vs single units (stores); FortiManager ADOM layout for 200 stores.
2. **Segmentation** — VDOMs or VLAN/zone segmentation for PCI vs general traffic; which
   policies carry deep inspection and why.
3. **Security services** — UTM profile strategy (deep inspection where PCI/data flows;
   certificate inspection elsewhere for performance); IPS/AV/web/DNS placement.
4. **Visibility** — FortiAnalyzer/FortiSIEM placement, log-rate sizing, ADOM per region.
5. **Access** — ZTNA/FortiSASE for admins and remote staff; FortiAuthenticator for MFA.
6. **Scale & lifecycle** — template-driven store provisioning, staged firmware upgrade
   paths, and the failure modes you designed against (hub loss, underlay brown-out).

**Expected result:** a written design that names the products, explains each trade-off
(deep vs certificate inspection, VDOM vs zone, HA placement, ADOM structure), and shows how
the pieces form one coherent Security Fabric — the deliverable NSE 8 actually grades.

**Negative test:** submit a pile of CLI with no rationale; NSE 8 rewards *why* (segmentation
model, inspection depth, scale strategy), and an unexplained config cannot be evaluated or
maintained.

**Rollback:** none (design artifact).

## Lab Verification

Verification means the mock ran under exam conditions, all seeded
faults were found or accounted for, outcomes were scored honestly, the
error journal gained entries, and the NSE 8 core/specialization plan
respects the one-year rule.

- **Lab verified by:** *pending*
- **Date:** *pending*

## Summary and Completion Checklist

- [ ] NSE 8 two-module structure and validity recorded from source
- [ ] Fabric verification battery built into practice loops
- [ ] One full mock completed and graded by outcomes
- [ ] Portfolio/recertification strategy mapped across the four tracks
- [ ] Booking gate (two clean mocks) and the one-year rule respected
